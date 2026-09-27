"""Chapter 06, part 06a: the local judge under the microscope on MT-Bench.

We test how well `qwen3.8:27b` works as a pairwise LLM-as-judge against **real
human votes** (MT-Bench, Zheng et al. 2023, arXiv 2306.05685):

- `sample`: deterministically pick 150 turn-1 human vote pairs (no ties, one
  vote per ordered (question, model_a, model_b)) with both answers attached →
  `runs/06_pairs.jsonl`, plus the human–human agreement ceiling (no LLM calls).
- `judge --model qwen3.8:27b --order ab|ba`: one pairwise verdict per pair
  (`A` / `B` / `tie` after a short explanation), prompt
  `prompts/pairwise_judge_v1.txt`. Verdicts persist (idempotent: already
  judged pairs are skipped) to `runs/06_verdicts/<model>/<order>.jsonl` and in
  the disk cache; `run_meta.json` records calls and seconds per order.
- `agreement --model qwen3.8:27b`: majority-of-two-orders agreement with the
  human winner (position-averaged) → `06_agreement_<model>`, primary
  `agreement_with_humans` (n=150), human–human and GPT-4 agreements on the
  same pairs in `details`.
- `bias --model qwen3.8:27b`: position flip rate (verdict flips when the order
  is swapped), first-position win share (300 call-level observations), verbosity
  numbers (judge vs humans, agreement split longer-wins vs shorter-wins) →
  `06_bias_<model>`, primary `position_flip_rate`.

`panel`, `bt` and `all` belong to the second half of chapter 06 (06b: gemma4
+ selene-mini judging, the panel and Bradley–Terry ratings) and are stubs here.

Self-preference bias (Zheng et al. 2023) *cannot* be measured on this data:
none of the six MT-Bench models (gpt-4, gpt-3.5-turbo, claude-v1,
vicuna-13b-v1.2, alpaca-13b, llama-13b) is a Qwen, so qwen3.8:27b never
grades one of its own answers — we measure position and verbosity only.

Everything runs through `evals_tutorial.llm` (disk cache) at temperature 0 and
a fixed seed, so re-runs cost zero LLM calls.
"""

from __future__ import annotations

import json
import re
import time
from itertools import combinations
from pathlib import Path

import typer

from evals_tutorial.config import settings
from evals_tutorial.llm import Ollama
from evals_tutorial.results import write_metrics

PROMPTS_DIR = Path(__file__).parent / "prompts"
DATA_DIR = settings.path("data") / "public"
JUDGE_MODEL = "qwen3.8:27b"
N_PAIRS = 150
SEED = 0
PROMPT_VERSION = "v1"
CHAPTER = 6
SYSTEM_PROMPT = "You are an expert evaluator of AI assistant answers."

app = typer.Typer(add_completion=False)

# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------


def load_jsonl(path: Path | str) -> list[dict]:
    out = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def _save_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _runs_dir() -> Path:
    return settings.path("runs")


def load_answers() -> dict[tuple, dict]:
    """`mt_bench_answers.jsonl` keyed by (question_id, model)."""
    return {(r["question_id"], r["model"]): r for r in load_jsonl(DATA_DIR / "mt_bench_answers.jsonl")}


# ---------------------------------------------------------------------------
# sample: 150 turn-1 non-tie pairs + human–human agreement
# ---------------------------------------------------------------------------


def is_tie(winner: str) -> bool:
    return winner.startswith("tie")


def _pair_key(vote: dict) -> tuple:
    return (vote["question_id"], vote["model_a"], vote["model_b"])


def sample_votes(votes: list[dict], n: int = N_PAIRS, seed: int = SEED, answers: dict | None = None) -> list[dict]:
    """Deterministically pick `n` turn-1 non-tie pairs.

    Rules (per spec): `turn == 1`, `winner` not a tie, at most one vote per
    ordered (question_id, model_a, model_b). Candidates are sorted by
    (question_id, model_a, model_b) and taken in order — fully deterministic
    given the vote file (`seed` is recorded for provenance). When `answers` is
    given, the turn-1 question and both answers are attached, and `pair_index`
    (index in the sample) plus `human_winner` (the vote's winner) are added.
    """
    by_key: dict[tuple, dict] = {}
    for v in votes:
        if v.get("turn") != 1 or is_tie(v.get("winner", "")):
            continue
        k = _pair_key(v)
        if k not in by_key:
            by_key[k] = v
    picked: list[dict] = []
    for i, k in enumerate(sorted(by_key)):
        if i >= n:
            break
        vote = dict(by_key[k])
        vote["pair_index"] = i
        vote["human_winner"] = vote["winner"]
        if answers is not None:
            row_a = answers.get((vote["question_id"], vote["model_a"]))
            row_b = answers.get((vote["question_id"], vote["model_b"]))
            vote["question"] = row_a["questions"][0] if row_a else ""
            vote["answer_a"] = row_a["answers"][0] if row_a else ""
            vote["answer_b"] = row_b["answers"][0] if row_b else ""
        picked.append(vote)
    return picked


def vote_pairs(votes: list[dict], turn: int | None = 1) -> dict[tuple, list[dict]]:
    """Group votes by ordered (question_id, model_a, model_b), one turn only."""
    groups: dict[tuple, list[dict]] = {}
    for v in votes:
        if turn is not None and v.get("turn") != turn:
            continue
        groups.setdefault(_pair_key(v), []).append(v)
    return groups


def human_human_agreement(votes: list[dict], include_ties: bool = True) -> dict:
    """The human–human agreement ceiling on MT-Bench turn-1 votes.

    Over all ordered (question, pair) groups with >= 2 human votes, the
    fraction of vote *pairs* (2-combinations) that agree on the winner.
    `include_ties=True` counts tie votes; `False` restricts to non-tie votes.
    """
    agreeing = total = n_groups = 0
    for vs in vote_pairs(votes).values():
        v2 = [v for v in vs if include_ties or not is_tie(v["winner"])]
        if len(v2) < 2:
            continue
        n_groups += 1
        for x, y in combinations(v2, 2):
            total += 1
            if x["winner"] == y["winner"]:
                agreeing += 1
    return {
        "agreeing": agreeing,
        "total": total,
        "groups": n_groups,
        "rate": (agreeing / total) if total else 0.0,
    }


@app.command()
def sample(
    n: int = typer.Option(N_PAIRS, "--n", help="number of pairs to sample"),
    seed: int = typer.Option(SEED, "--seed", help="recorded for provenance (sampling is deterministic)"),
) -> None:
    """Pick 150 turn-1 non-tie human vote pairs -> runs/06_pairs.jsonl; print human–human agreement."""
    votes = load_jsonl(DATA_DIR / "mt_bench_human_votes.jsonl")
    answers = load_answers()
    pairs = sample_votes(votes, n=n, seed=seed, answers=answers)
    out = _runs_dir() / "06_pairs.jsonl"
    _save_jsonl(out, pairs)
    h2h_no = human_human_agreement(votes, include_ties=False)
    h2h_yes = human_human_agreement(votes, include_ties=True)
    print(f"wrote {len(pairs)} pairs -> {out}")
    print(
        f"human-human agreement (turn 1): "
        f"no ties  = {h2h_no['agreeing']}/{h2h_no['total']} = {h2h_no['rate']:.3f} over {h2h_no['groups']} pairs"
    )
    print(
        f"                              "
        f"with ties = {h2h_yes['agreeing']}/{h2h_yes['total']} = {h2h_yes['rate']:.3f} over {h2h_yes['groups']} pairs"
    )


# ---------------------------------------------------------------------------
# judge: one pairwise call per (pair, order)
# ---------------------------------------------------------------------------


def prompt_template() -> str:
    return (PROMPTS_DIR / f"pairwise_judge_{PROMPT_VERSION}.txt").read_text()


def judge_messages(pair: dict, order: str) -> list[dict]:
    """Chat messages for one pair in the given display order (`ab`/`ba`).

    In order `ba` the answers are swapped: the pair's `answer_a` is shown
    second, so a verdict `B` then means the pair's `a` model won.
    """
    if order not in ("ab", "ba"):
        raise ValueError(f"order must be 'ab' or 'ba', got {order!r}")
    first, second = (pair["answer_a"], pair["answer_b"]) if order == "ab" else (pair["answer_b"], pair["answer_a"])
    text = prompt_template().format(question=pair["question"], answer_a=first, answer_b=second)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]


_VERDICT_RE = re.compile(r"judge\s*[:\-]?\s*(?:answer\s*)?([AB])\b", re.IGNORECASE)
_TIE_RE = re.compile(r"tie", re.IGNORECASE)


def parse_verdict(reply: str) -> str:
    """Extract the verdict from a judge reply: `A`, `B` or `tie`.

    The final line wins (a `tie` mention there counts, matching `Judge: A/B`
    after it); otherwise the latest earlier line with a verdict is used, then a
    whole-reply fallback. Replies with no verdict line at all (e.g. the model
    hit `max_tokens` mid-explanation) fall back to `tie` rather than aborting
    a batch — an unparseable reply is treated as "no confident pick".
    """
    lines = [ln.strip() for ln in reply.strip().splitlines() if ln.strip()]
    if lines and _TIE_RE.search(lines[-1]):
        return "tie"
    for ln in reversed(lines):
        m = _VERDICT_RE.search(ln)
        if m:
            return m.group(1).upper()
    m = _VERDICT_RE.search(reply)
    if m:
        return m.group(1).upper()
    return "tie"


def _verdict_path(model: str, order: str) -> Path:
    return _runs_dir() / "06_verdicts" / model / f"{order}.jsonl"


def _load_verdicts(model: str, order: str) -> dict[int, dict]:
    path = _verdict_path(model, order)
    if not path.exists():
        return {}
    return {int(r["pair_index"]): r for r in load_jsonl(path)}


def judge_pair(pair: dict, order: str, model: str, client: Ollama | None = None) -> dict:
    """One pairwise call, parsed and persisted. `client` is injectable for tests."""
    client = client or Ollama()
    reply = client.chat(judge_messages(pair, order), model=model)
    row = {
        "pair_index": pair["pair_index"],
        "question_id": pair["question_id"],
        "model_a": pair["model_a"],
        "model_b": pair["model_b"],
        "order": order,
        "model": model,
        "raw": reply,
        "verdict": parse_verdict(reply),
    }
    _append_jsonl(_verdict_path(model, order), row)
    return row


def judge_all(pairs: list[dict], model: str, order: str, client: Ollama | None = None) -> dict:
    """Judge all pairs in one order, skipping pairs already judged (idempotent)."""
    client = client or Ollama()
    done = _load_verdicts(model, order)
    started = time.monotonic()
    new_rows: list[dict] = []
    for p in pairs:
        if p["pair_index"] in done:
            continue
        new_rows.append(judge_pair(p, order, model, client))
    elapsed = time.monotonic() - started
    return {"calls": len(new_rows), "cached": len(done), "seconds": round(elapsed, 1)}


def _first_n(pairs: list[dict], limit: int | None) -> list[dict]:
    if limit is None or limit <= 0:
        return pairs
    return [p for p in pairs if p["pair_index"] < limit]


@app.command()
def judge(
    model: str = typer.Option(JUDGE_MODEL, "--model", help="judge model"),
    order: str = typer.Option("ab", "--order", help="display order: ab or ba"),
    limit: int = typer.Option(None, "--limit", help="only the first N pairs (06b gemma4/selene use 100)"),
) -> None:
    """Judge pairs in runs/06_pairs.jsonl in one display order (skips already judged)."""
    pairs = _first_n(load_jsonl(_runs_dir() / "06_pairs.jsonl"), limit)
    stats = judge_all(pairs, model, order)
    meta_path = _runs_dir() / "06_verdicts" / model / "run_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {"orders": {}}
    prev = meta["orders"].get(order, {})
    # accumulate new-call count across re-runs (each run reports only its own new calls)
    meta["orders"][order] = {
        "model": model,
        "calls": prev.get("calls", 0) + stats["calls"],
        "cached": max(prev.get("cached", 0), stats["cached"]),
        "seconds": stats["seconds"],
    }
    meta["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2))
    print(
        f"{model} order={order}: {stats['calls']} new calls, {stats['cached']} cached, "
        f"{stats['seconds']:.1f}s -> {_verdict_path(model, order)}"
    )


# ---------------------------------------------------------------------------
# agreements shared by `agreement` and `bias`
# ---------------------------------------------------------------------------


def _model_winner(verdict: str, order: str) -> str:
    """Map a position-space verdict (A/B/tie) to the pair's model names.

    In order `ab`, position A shows the pair's `model_a`; in order `ba` the
    answers are swapped, so position A shows `model_b` and position B shows
    `model_a`.
    """
    if verdict not in ("A", "B", "tie"):
        raise ValueError(f"bad verdict {verdict!r}")
    if verdict == "tie":
        return "tie"
    first = "model_a" if order == "ab" else "model_b"
    second = "model_b" if order == "ab" else "model_a"
    return first if verdict == "A" else second


def _is_flip(v_ab: str, v_ba: str) -> bool:
    """True when both orders make a definite pick and disagree on the model.

    A tie in either order is not a position flip — it is just no consistent
    winner, which `_majority` already reports as `None`.
    """
    w_ab = _model_winner(v_ab, "ab")
    w_ba = _model_winner(v_ba, "ba")
    return w_ab in ("model_a", "model_b") and w_ba in ("model_a", "model_b") and w_ab != w_ba


def _majority(v_ab: str, v_ba: str) -> str | None:
    """Majority-of-two-orders in *model* space.

    Both orders picking the same model wins; a tie in either order, or the two
    orders picking different models (a position flip) leave no consistent
    winner → `None`.
    """
    w_ab = _model_winner(v_ab, "ab")
    w_ba = _model_winner(v_ba, "ba")
    if w_ab in ("model_a", "model_b") and w_ab == w_ba:
        return w_ab
    return None


def gpt4_agreement(pairs: list[dict], votes: list[dict]) -> dict:
    """GPT-4's agreement with the human winner on our sampled pairs.

    GPT-4's votes (`judge = gpt4_pair`) are single-order: the row gives a
    winner in (model_a, model_b) space, which is order-independent, so the pair
    agrees when some GPT-4 row for that ordered (or reversed) pair has
    `model_a`/`model_b` matching the human winner.
    """
    by_key: dict[tuple, list[dict]] = {}
    for v in votes:
        if v.get("turn") == 1:
            by_key.setdefault(_pair_key(v), []).append(v)

    def agree(pair: dict) -> bool:
        expected = pair["human_winner"]
        for k in (
            (pair["question_id"], pair["model_a"], pair["model_b"]),
            (pair["question_id"], pair["model_b"], pair["model_a"]),
        ):
            # in the reversed row the model names are swapped, so the expected
            # winner in that row's local (model_a/model_b) space is flipped
            for v in by_key.get(k, []):
                if v["winner"] == expected:
                    return True
            if expected in ("model_a", "model_b"):
                expected = "model_b" if expected == "model_a" else "model_a"
        return False

    n = len(pairs)
    agreeing = sum(1 for p in pairs if agree(p))
    return {
        "n": n,
        "agreeing": agreeing,
        "rate": (agreeing / n) if n else 0.0,
    }


def pair_rows(pairs: list[dict], model: str) -> list[dict]:
    """Per-pair agreement/bias rows for one judge model (both orders present)."""
    ab = _load_verdicts(model, "ab")
    ba = _load_verdicts(model, "ba")
    rows: list[dict] = []
    for p in pairs:
        i = p["pair_index"]
        r_ab = ab.get(i)
        r_ba = ba.get(i)
        if r_ab is None or r_ba is None:
            raise RuntimeError(f"missing verdicts for pair {i} of {model}: run judge --order ab and ba first")
        v_ab, v_ba = r_ab["verdict"], r_ba["verdict"]
        maj = _majority(v_ab, v_ba)
        len_a = len(p.get("answer_a", "")) or 0
        len_b = len(p.get("answer_b", "")) or 0
        rows.append(
            {
                "pair_index": i,
                "question_id": p["question_id"],
                "model_a": p["model_a"],
                "model_b": p["model_b"],
                "human_winner": p["human_winner"],
                "verdict_ab": v_ab,
                "verdict_ba": v_ba,
                "majority": maj,
                "agrees": maj == p["human_winner"],
                "flip": _is_flip(v_ab, v_ba),
                "winner_ab": _model_winner(v_ab, "ab"),
                "winner_ba": _model_winner(v_ba, "ba"),
                "len_a": len(p.get("answer_a", "")),
                "len_b": len(p.get("answer_b", "")),
                "longer": (
                    "model_a" if len_a > len_b else "model_b" if len_b > len_a else None
                ),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# agreement
# ---------------------------------------------------------------------------


def agreement_metrics(model: str, pairs: list[dict] | None = None) -> dict:
    """Agreement of `model` with the human winner (majority of the two orders)."""
    pairs = pairs if pairs is not None else load_jsonl(_runs_dir() / "06_pairs.jsonl")
    rows = pair_rows(pairs, model)
    n = len(rows)
    agreeing = sum(1 for r in rows if r["agrees"])
    return {
        "n": n,
        "agreement": (agreeing / n) if n else 0.0,
        "agreeing": agreeing,
        "tie_majorities": sum(1 for r in rows if r["majority"] is None),
        "rows": rows,
    }


@app.command()
def agreement(
    model: str = typer.Option(JUDGE_MODEL, "--model"),
    exp: str = typer.Option(None, "--exp", help="experiment name (default 06_agreement_<model>)"),
    limit: int = typer.Option(None, "--limit", help="only the first N pairs (06b judges use 100)"),
) -> None:
    """Judge-vs-human agreement -> experiments 06_agreement_<model>."""
    name = exp or f"06_agreement_{model.replace('/', '_').replace(':', '_')}"
    pairs = _first_n(load_jsonl(_runs_dir() / "06_pairs.jsonl"), limit)
    res = agreement_metrics(model, pairs)
    human_rows = res["rows"]

    votes = load_jsonl(DATA_DIR / "mt_bench_human_votes.jsonl")
    h2h_no = human_human_agreement(votes, include_ties=False)
    h2h_yes = human_human_agreement(votes, include_ties=True)
    g4 = gpt4_agreement(pairs, load_jsonl(DATA_DIR / "mt_bench_gpt4_votes.jsonl"))

    meta = _runs_dir() / "06_verdicts" / model / "run_meta.json"
    calls = seconds = 0
    if meta.exists():
        m = json.loads(meta.read_text())
        for o in m.get("orders", {}).values():
            calls += o.get("calls", 0)
            seconds += o.get("seconds", 0.0)

    def pred(r: dict) -> dict:
        return {
            "id": f"pair_{r['pair_index']}",
            "output": {"verdict_ab": r["verdict_ab"], "verdict_ba": r["verdict_ba"], "majority": r["majority"]},
            "score": 1.0 if r["agrees"] else 0.0,
            "judge_critique": f"human said {r['human_winner']}; judge majority {r['majority']}",
        }

    write_metrics(
        experiment=name,
        chapter=CHAPTER,
        n=res["n"],
        metrics={
            "agreement_with_humans": round(res["agreement"], 4),
            "tie_majorities": float(res["tie_majorities"]),
        },
        llm_calls=calls,
        seconds=round(seconds, 1),
        details={
            "notes": (
                f"{model} vs humans (majority of ab/ba orders); sample = {len(pairs)} turn-1 non-tie pairs, seed {SEED}; "
                f"ceiling: human-human {h2h_no['rate']:.3f} (no ties) / {h2h_yes['rate']:.3f} (with ties); reference: GPT-4 {g4['rate']:.3f}"
            ),
            "human_human_agreement": {"no_ties": h2h_no, "with_ties": h2h_yes},
            "gpt4_agreement": g4,
            "flip_pairs": sum(1 for r in human_rows if r["flip"]),
        },
        predictions=[pred(r) for r in human_rows],
        config={
            "model": model,
            "prompt": f"pairwise_judge_{PROMPT_VERSION}",
            "n_pairs": len(pairs),
            "seed": SEED,
            "orders": ["ab", "ba"],
        },
    )
    print(
        f"{name}: agreement_with_humans = {res['agreement']:.3f} ({res['agreeing']}/{res['n']}); "
        f"human-human = {h2h_no['rate']:.3f} (no ties) / {h2h_yes['rate']:.3f} (with ties); GPT-4 = {g4['rate']:.3f}"
    )


# ---------------------------------------------------------------------------
# bias
# ---------------------------------------------------------------------------


def bias_metrics(model: str, pairs: list[dict] | None = None) -> dict:
    """Position-flip rate, first-position win share and verbosity numbers."""
    pairs = pairs if pairs is not None else load_jsonl(_runs_dir() / "06_pairs.jsonl")
    rows = pair_rows(pairs, model)
    n = len(rows)

    flips = sum(1 for r in rows if r["flip"])
    # first-position wins over the 300 call-level observations
    obs = [(r["verdict_ab"], r["longer"]) for r in rows] + [(r["verdict_ba"], r["longer"]) for r in rows]
    first_pos = sum(1 for v, _ in obs if v == "A")
    # verbosity: judge picks the longer answer, over both orders (order-aware mapping)
    judge_longer = sum(
        1 for r in rows
        if (r["winner_ab"] != "tie" and r["winner_ab"] == r["longer"])
        or (r["winner_ba"] != "tie" and r["winner_ba"] == r["longer"])
    )
    # humans, over the 150 turn-1 votes in our pairs
    hum_longer = sum(1 for r in rows if r["human_winner"] == r["longer"])
    # agreement conditioned on longer-wins vs shorter-wins (pair-level)
    lw = [r for r in rows if r["human_winner"] == r["longer"]]
    sw = [r for r in rows if r["human_winner"] != r["longer"]]
    agree_lw = sum(1 for r in lw if r["agrees"])
    agree_sw = sum(1 for r in sw if r["agrees"])
    return {
        "n": n,
        "position_flip_rate": (flips / n) if n else 0.0,
        "flips": flips,
        "first_position_wins": first_pos,
        "call_observations": len(obs),
        "judge_picks_longer": judge_longer,
        "judge_picks_longer_rate": (judge_longer / len(obs)) if obs else 0.0,
        "human_picks_longer": hum_longer,
        "human_picks_longer_rate": (hum_longer / n) if n else 0.0,
        "agree_longer_wins": {"n": len(lw), "agreeing": agree_lw, "rate": (agree_lw / len(lw)) if lw else 0.0},
        "agree_shorter_wins": {"n": len(sw), "agreeing": agree_sw, "rate": (agree_sw / len(sw)) if sw else 0.0},
        "rows": rows,
    }


@app.command()
def bias(
    model: str = typer.Option(JUDGE_MODEL, "--model"),
    exp: str = typer.Option(None, "--exp", help="experiment name (default 06_bias_<model>)"),
    limit: int = typer.Option(None, "--limit", help="only the first N pairs (06b judges use 100)"),
) -> None:
    """Position + verbosity bias -> experiments 06_bias_<model> (primary position_flip_rate)."""
    name = exp or f"06_bias_{model.replace('/', '_').replace(':', '_')}"
    pairs = _first_n(load_jsonl(_runs_dir() / "06_pairs.jsonl"), limit)
    res = bias_metrics(model, pairs)
    rows = res["rows"]

    meta = _runs_dir() / "06_verdicts" / model / "run_meta.json"
    calls = seconds = 0
    if meta.exists():
        m = json.loads(meta.read_text())
        for o in m.get("orders", {}).values():
            calls += o.get("calls", 0)
            seconds += o.get("seconds", 0.0)
    votes = load_jsonl(DATA_DIR / "mt_bench_human_votes.jsonl")
    h2h_no = human_human_agreement(votes, include_ties=False)
    g4 = gpt4_agreement(pairs, load_jsonl(DATA_DIR / "mt_bench_gpt4_votes.jsonl"))

    write_metrics(
        experiment=name,
        chapter=CHAPTER,
        n=res["n"],
        metrics={
            "position_flip_rate": round(res["position_flip_rate"], 4),
            "first_position_win_share": round(res["first_position_wins"] / res["call_observations"], 4),
            "judge_picks_longer": round(res["judge_picks_longer_rate"], 4),
            "human_picks_longer": round(res["human_picks_longer_rate"], 4),
            "agreement_longer_wins": round(res["agree_longer_wins"]["rate"], 4),
            "agreement_shorter_wins": round(res["agree_shorter_wins"]["rate"], 4),
        },
        llm_calls=calls,
        seconds=round(seconds, 1),
        details={
            "notes": (
                f"{model}: position flip {res['flips']}/{res['n']} pairs; first-position wins "
                f"{res['first_position_wins']}/{res['call_observations']} calls; verbosity: judge picks longer "
                f"{res['judge_picks_longer']}/{res['call_observations']} vs humans {res['human_picks_longer']}/{res['n']}; "
                f"context: human-human {h2h_no['rate']:.3f}, GPT-4 {g4['rate']:.3f}; "
                f"self-preference NOT measurable: no MT-Bench model is a Qwen family"
            ),
            "human_human_agreement_no_ties": h2h_no,
            "gpt4_agreement": g4,
            "flipped_pairs": [
                {
                    "pair_index": r["pair_index"],
                    "question_id": r["question_id"],
                    "model_a": r["model_a"],
                    "model_b": r["model_b"],
                    "verdict_ab": r["verdict_ab"],
                    "verdict_ba": r["verdict_ba"],
                    "human_winner": r["human_winner"],
                }
                for r in rows
                if r["flip"]
            ],
            "longer_wins_n": res["agree_longer_wins"]["n"],
            "shorter_wins_n": res["agree_shorter_wins"]["n"],
        },
        predictions=[
            {
                "id": f"pair_{r['pair_index']}",
                "output": {
                    "verdict_ab": r["verdict_ab"],
                    "verdict_ba": r["verdict_ba"],
                    "first_pos_wins_ab": r["verdict_ab"] == "A",
                    "first_pos_wins_ba": r["verdict_ba"] == "A",
                },
                "score": 0.0 if r["flip"] else 1.0,
                "judge_critique": (
                    f"flip={r['flip']}; longer={r['longer']} (a={r['len_a']} chars, b={r['len_b']} chars)"
                ),
            }
            for r in rows
        ],
        config={
            "model": model,
            "prompt": f"pairwise_judge_{PROMPT_VERSION}",
            "n_pairs": len(pairs),
            "seed": SEED,
            "orders": ["ab", "ba"],
        },
    )
    print(
        f"{name}: position_flip_rate = {res['position_flip_rate']:.3f} ({res['flips']}/{res['n']}); "
        f"first-position wins = {res['first_position_wins']}/{res['call_observations']}; "
        f"judge picks longer = {res['judge_picks_longer_rate']:.3f} vs humans {res['human_picks_longer_rate']:.3f}"
    )


# ---------------------------------------------------------------------------
# 06b: panel (PoLL majority) + Bradley–Terry, and `all`
# ---------------------------------------------------------------------------

PANEL_JUDGES = ("qwen3.8:27b", "gemma4:latest", "atla/selene-mini")


def panel_verdicts(
    pairs: list[dict],
    judges: tuple[str, ...] = PANEL_JUDGES,
    exp_name: str = "06_panel",
) -> dict:
    """PoLL-style majority over `judges`, each collapsed by majority-of-two-orders.

    For a pair, each judge votes in model space (`model_a`/`model_b`/`None`),
    the judge with a definitive pick that a bare majority of the *available*
    judges agree on wins; otherwise the panel returns a tie. Agreement with the
    human winner is the share of pairs whose panel pick equals `human_winner`.

    Every (pair_index, judge) is included even when verdicts are missing, so the
    returned `rows` and the per-coverage stats describe the full pair set.
    """
    picks: dict[int, list[str]] = {}
    for j in judges:
        ab = _load_verdicts(j, "ab")
        ba = _load_verdicts(j, "ba")
        for p in pairs:
            i = p["pair_index"]
            v_ab, v_ba = ab.get(i, {}).get("verdict"), ba.get(i, {}).get("verdict")
            v = _majority(v_ab, v_ba) if (v_ab is not None and v_ba is not None) else None
            picks.setdefault(i, []).append(v)

    rows: list[dict] = []
    for p in pairs:
        i = p["pair_index"]
        votes = picks.get(i, [])
        avail = [v for v in votes if v is not None]
        if avail:
            counts: dict[str, int] = {}
            for v in avail:
                counts[v] = counts.get(v, 0) + 1
            best = max(counts.values())
            winners = [m for m, c in counts.items() if c == best]
            # a bare majority (strictly more than half) wins, otherwise a tie
            panel = winners[0] if (len(winners) == 1 and best > len(avail) / 2) else "tie"
        else:
            panel = "tie"
        rows.append(
            {
                "pair_index": i,
                "question_id": p["question_id"],
                "model_a": p["model_a"],
                "model_b": p["model_b"],
                "human_winner": p["human_winner"],
                "judge_votes": votes,
                "n_judges": len(votes),
                "n_available": len(avail),
                "panel": panel,
                "agrees": panel == p["human_winner"],
            }
        )

    n = len(rows)
    agreeing = sum(1 for r in rows if r["agrees"])
    covered = sum(1 for r in rows if r["n_available"] >= 2)
    return {
        "n": n,
        "agreement": (agreeing / n) if n else 0.0,
        "agreeing": agreeing,
        "tie_majorities": sum(1 for r in rows if r["panel"] == "tie"),
        "pairs_with_at_least_2_judges": covered,
        "judges": list(judges),
        "exp_name": exp_name,
        "rows": rows,
    }


@app.command()
def panel(
    exp: str = typer.Option(None, "--exp", help="experiment name (default 06_panel)"),
    limit: int = typer.Option(None, "--limit", help="only the first N pairs (06b uses 100)"),
) -> None:
    """PoLL-style majority of the panel judges -> experiment 06_panel (06b, no new LLM calls)."""
    name = exp or "06_panel"
    pairs = _first_n(load_jsonl(_runs_dir() / "06_pairs.jsonl"), limit)
    res = panel_verdicts(pairs, exp_name=name)

    # call budget accumulated across the judges that already produced verdicts
    calls = seconds = 0
    for j in res["judges"]:
        meta = _runs_dir() / "06_verdicts" / j / "run_meta.json"
        if not meta.exists():
            continue
        for o in json.loads(meta.read_text()).get("orders", {}).values():
            calls += o.get("calls", 0)
            seconds += o.get("seconds", 0.0)

    write_metrics(
        experiment=name,
        chapter=CHAPTER,
        n=res["n"],
        metrics={
            "panel_agreement": round(res["agreement"], 4),
            "panel_tie_majorities": float(res["tie_majorities"]),
            "pairs_with_at_least_2_judges": float(res["pairs_with_at_least_2_judges"]),
        },
        llm_calls=calls,
        seconds=round(seconds, 1),
        details={
            "notes": (
                f"panel = bare-majority-of-available picks over {', '.join(res['judges'])}; "
                f"each judge already collapsed by majority of its ab/ba orders; "
                f"n={res['n']} pairs, agreement_with_humans={res['agreement']:.3f}"
            ),
            "judges": res["judges"],
            "per_pair": [
                {
                    "pair_index": r["pair_index"],
                    "model_a": r["model_a"],
                    "model_b": r["model_b"],
                    "human_winner": r["human_winner"],
                    "judge_votes": r["judge_votes"],
                    "panel": r["panel"],
                    "agrees": r["agrees"],
                }
                for r in res["rows"]
            ],
        },
        predictions=[
            {
                "id": f"pair_{r['pair_index']}",
                "output": {"votes": r["judge_votes"], "panel": r["panel"]},
                "score": 1.0 if r["agrees"] else 0.0,
                "judge_critique": f"human said {r['human_winner']}; panel {r['panel']}",
            }
            for r in res["rows"]
        ],
        config={
            "judges": res["judges"],
            "prompt": f"pairwise_judge_{PROMPT_VERSION}",
            "n_pairs": res["n"],
            "seed": SEED,
            "orders": ["ab", "ba"],
        },
    )
    print(
        f"{name}: panel_agreement = {res['agreement']:.3f} ({res['agreeing']}/{res['n']}); "
        f"tie_majorities = {res['tie_majorities']}; >=2 judges cover {res['pairs_with_at_least_2_judges']}/{res['n']}"
    )


# ---------------------------------------------------------------------------
# Bradley–Terry ratings
# ---------------------------------------------------------------------------


def _votes_to_records(votes: list[dict], judge: str | None) -> tuple[list[str], list[str], list[str]]:
    """Normalise a vote file to (xs, ys, winners) with X = left, Y = right, X wins => 'A'."""
    xs: list[str] = []
    ys: list[str] = []
    winners: list[str] = []
    for v in votes:
        if v.get("turn") != 1:
            continue
        if judge is not None and v.get("judge") != judge:
            continue
        a, b, w = v["model_a"], v["model_b"], v["winner"]
        if is_tie(w):
            xs.append(a)
            ys.append(b)
            winners.append("tie")
        elif w == "model_a":
            xs.append(a)
            ys.append(b)
            winners.append("A")
        else:
            xs.append(b)
            ys.append(a)
            winners.append("A")
    return xs, ys, winners


def _fit_bt(xs: list[str], ys: list[str], winners: list[str], models: list[str]) -> dict[str, float]:
    """Bradley–Terry MLE via the MM algorithm.

    Returns a score dict for `models` (max normalised to 1.0). The fixed point is
    `s[i] = sum_j N_ij * P_ij * s[j]/(s[i]+s[j]) / sum_j N_ij * s[j]/(s[i]+s[j])`,
    where `N_ij` is the total number of contests and `P_ij` the share `i` won in
    them — ties split 0.5/0.5.

    A winless model has a true MLE of 0, which the plain MM update can drive to
    exactly 0 and then divide by in the *other* models' terms (``0/0``). We floor
    the scores at a tiny epsilon (``EPS``) throughout; the floor never binds when
    no model is winless (the real data), but it keeps a winless model at a
    distinct, clearly-lowest rating instead of crashing the iteration.
    """
    idx = {m: i for i, m in enumerate(models)}
    n = len(models)
    W = [[0.0] * n for _ in range(n)]  # W[i][j] = contests i won vs j (ties 0.5 each)
    for x, y, w in zip(xs, ys, winners):
        i, j = idx[x], idx[y]
        if w == "tie":
            W[i][j] += 0.5
            W[j][i] += 0.5
        else:
            W[i][j] += 1.0
    N = [[W[i][j] + W[j][i] for j in range(n)] for i in range(n)]
    EPS = 1e-9
    s = [1.0] * n
    for _ in range(2000):
        new = [1.0] * n
        for k in range(n):
            num = den = 0.0
            for j in range(n):
                if N[k][j] == 0:
                    continue
                p_kj = W[k][j] / N[k][j]
                share = s[j] / (s[k] + s[j])
                num += N[k][j] * p_kj * share
                den += N[k][j] * share
            new[k] = max(num / den, EPS) if den > 0 else max(s[k], EPS)
        scale = max(new) or 1.0
        new = [v / scale for v in new]
        if max(abs(a - b) for a, b in zip(new, s)) < 1e-10:
            s = new
            break
        s = new
    return {m: s[i] for i, m in enumerate(models)}


def _spearman(rank_a: dict[str, float], rank_b: dict[str, float]) -> float:
    """Spearman rank correlation between two model->score maps (average-rank ties)."""
    shared = [m for m in rank_a if m in rank_b]
    if len(shared) < 2:
        return 0.0
    models = list(shared)

    def ranks(tbl: dict[str, float]) -> list[float]:
        # 1-based ranks over `models` in ascending value order, ties averaged
        pairs = sorted(((tbl[m], m) for m in models), key=lambda t: t[0])
        ranks: dict[str, float] = {}
        i = 0
        while i < len(pairs):
            j = i
            while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[pairs[k][1]] = avg
            i = j + 1
        return [ranks[m] for m in models]

    x = ranks(rank_a)
    y = ranks(rank_b)
    n = len(models)
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x) ** 0.5
    vy = sum((b - my) ** 2 for b in y) ** 0.5
    if vx == 0 or vy == 0:
        return 0.0
    return cov / (vx * vy)


def _bt_rankings() -> dict:
    votes = load_jsonl(DATA_DIR / "mt_bench_human_votes.jsonl")
    models = sorted({v["model_a"] for v in votes} | {v["model_b"] for v in votes})

    hx, hy, hw = _votes_to_records(votes, None)
    human = _fit_bt(hx, hy, hw, models)

    # qwen's votes: collapse each (pair, order) to its model-space winner, then
    # majority of the two orders (ties/None dropped). Winner is placed on the x
    # side so `_fit_bt` counts x as the winner.
    ab = _load_verdicts(JUDGE_MODEL, "ab")
    ba = _load_verdicts(JUDGE_MODEL, "ba")
    qx: list[str] = []
    qy: list[str] = []
    common = set(ab) & set(ba)
    for i in common:
        ra_r, rb_r = ab[i], ba[i]
        maj = _majority(ra_r.get("verdict"), rb_r.get("verdict"))
        if maj is None:
            continue
        loser = "model_b" if maj == "model_a" else "model_a"
        qx.append(ra_r[maj])
        qy.append(ra_r[loser])
    qw = ["A"] * len(qx)
    qwen = _fit_bt(qx, qy, qw, models)

    human_ranked = sorted(human.items(), key=lambda kv: kv[1], reverse=True)
    qwen_ranked = sorted(qwen.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "models": models,
        "human": human,
        "qwen": qwen,
        "human_ranking": [m for m, _ in human_ranked],
        "qwen_ranking": [m for m, _ in qwen_ranked],
        "spearman": _spearman(human, qwen),
        "n_human_votes": len(hx),
        "n_qwen_votes": len(qx),
    }


@app.command()
def bt(exp: str = typer.Option(None, "--exp", help="experiment name (default 06_bradley_terry)")) -> None:
    """Bradley–Terry ratings from human vs qwen votes -> experiment 06_bradley_terry (06b, no new LLM calls)."""
    name = exp or "06_bradley_terry"
    r = _bt_rankings()
    human_ranked = r["human_ranking"]
    qwen_ranked = r["qwen_ranking"]

    # plot if matplotlib is available
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))
        xs = range(len(r["models"]))
        width = 0.38
        ax.bar([x - width / 2 for x in xs], [r["human"][m] for m in r["models"]], width, label="human votes")
        ax.bar([x + width / 2 for x in xs], [r["qwen"][m] for m in r["models"]], width, label=f"{JUDGE_MODEL}")
        ax.set_xticks(list(xs))
        ax.set_xticklabels(r["models"], rotation=30, ha="right")
        ax.set_ylabel("Bradley–Terry score (max = 1)")
        ax.set_title("Bradley–Terry: human vs qwen rankings\n(spearman rho = %.3f)" % r["spearman"])
        ax.legend()
        fig.tight_layout()
        fig_path = _runs_dir() / "bt_ratings.png"
        fig.savefig(fig_path)
        plt.close(fig)
        plot_note = str(fig_path)
    except Exception as exc:  # noqa: BLE001 - plotting is best-effort
        plot_note = f"plot skipped: {exc}"

    write_metrics(
        experiment=name,
        chapter=CHAPTER,
        n=len(r["models"]),
        metrics={
            "spearman_rho": round(r["spearman"], 4),
            "n_human_votes": float(r["n_human_votes"]),
            "n_qwen_votes": float(r["n_qwen_votes"]),
        },
        llm_calls=0,
        seconds=0.0,
        details={
            "notes": (
                f"Bradley–Terry MLE over {r['n_human_votes']} human turn-1 votes vs "
                f"{r['n_qwen_votes']} qwen majority-of-two votes; "
                f"ranking agreement spearman rho = {r['spearman']:.3f}; {plot_note}"
            ),
            "human_ratings": {m: round(r["human"][m], 4) for m in human_ranked},
            "qwen_ratings": {m: round(r["qwen"][m], 4) for m in qwen_ranked},
            "human_ranking": human_ranked,
            "qwen_ranking": qwen_ranked,
        },
        predictions=[
            {
                "id": m,
                "output": {"human": r["human"][m], "qwen": r["qwen"][m]},
                "score": 0.0 if r["human_ranking"].index(m) != r["qwen_ranking"].index(m) else 1.0,
                "judge_critique": f"human rank {r['human_ranking'].index(m) + 1} vs qwen rank {r['qwen_ranking'].index(m) + 1}",
            }
            for m in r["models"]
        ],
        config={
            "model": JUDGE_MODEL,
            "prompt": f"pairwise_judge_{PROMPT_VERSION}",
            "n_models": len(r["models"]),
            "seed": SEED,
        },
    )
    print(
        f"{name}: spearman_rho = {r['spearman']:.3f}; human ranking = {human_ranked}; "
        f"qwen ranking = {qwen_ranked}"
    )


@app.command(name="all")
def all_() -> None:
    """sample + judge ab/ba + agreement + bias + panel + bt in one go (06a + 06b)."""
    sample(n=N_PAIRS, seed=SEED)
    judge(model=JUDGE_MODEL, order="ab")
    judge(model=JUDGE_MODEL, order="ba")
    agreement(model=JUDGE_MODEL)
    bias(model=JUDGE_MODEL)
    panel()
    bt()


if __name__ == "__main__":
    app()
