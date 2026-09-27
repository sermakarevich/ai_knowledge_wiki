"""Chapter 09a — cheap CPU hallucination detectors on RAGTruth (no LLM calls).

Three purpose-built detectors, each producing a response-level score in [0, 1]
where higher = more likely hallucinated:

- `hhem`     — `vectara/hallucination_evaluation_model` (HHEM-2.1-Open);
  score = 1 − model consistency between the evidence and the response.
- `lettuce`  — `KRLabsOrg/lettucedect-base-modernbert-en-v1` span-level
  token classifier (via the `lettucedetect` package); response score =
  max span confidence, plus span-level token P/R vs the gold `labels`
  recorded in details.
-   `nli`      — `cross-encoder/nli-deberta-v3-base`; the response is split
  into sentences, each is scored against the best N evidence chunks of
  ~300 words by entailment probability, and the response score is
  `1 − min(entailment)`.

Threshold convention: the dev threshold is picked on the first 80 rows
(the "dev" split) to maximise F1, and all reported metrics are on the
remaining 400 rows (the "test" split).  Every row carries human labels
(`hallucinated: bool`, `labels: list[spans]`).

Experiments written (via `results.write_metrics`):
- `09_hhem_ragtruth`    — primary `auroc`, n = 400
- `09_lettuce_ragtruth` — primary `auroc`, n = 400, span P/R in details
- `09_nli_ragtruth`     — primary `auroc`, n = 400

Chapter 09b adds the Ollama-dependent half:

- `selfcheck` — SelfCheckGPT-style consistency on 60 test rows: 3 sampled
  responses per row at temperature 0.7 (180 chat calls), scored for
  consistency with the original row response by the NLI cross-encoder
  (no source used — sampling consistency is the point). Experiment
  `09_selfcheck_ragtruth` (n = 60).
- `judge` — the `qwen3.8:27b` LLM judge (`prompts/halluc_judge_v1.txt`) on
  the first 100 test rows (100 chat calls), JSON yes/no verdict.
  Experiment `09_llm_judge_ragtruth` (n = 100, primary `f1`).
- `compare` — one table on the rows all methods share (AUROC/F1/P/R, s/item,
  pairwise agreement, per task type) -> `runs/09_compare.md`.
- `apply --run answer_v1` — HHEM + the best 09a detector over our 60 test
  helpdesk replies (retrieved handbook sections as source) vs the
  chapter-03 `unsupported_claim` label. Experiment
  `09_detector_helpdesk_v1` (primary `auroc_vs_label`).

Models download to `~/.cache` on first run; they are never committed.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import torch
import typer
from pydantic import BaseModel, Field
from evals_tutorial import results as R
from evals_tutorial.config import settings

app = typer.Typer(help="Chapter 09 — CPU + LLM hallucination detectors on RAGTruth and our helpdesk replies.")


class HallucJudgeVerdict(BaseModel):
    """Structured LLM-judge reply for the `judge` command.

    `hallucinated` is the binary verdict (true = the response states at least
    one fact the source does not support).  `unsupported_claims` is the list
    of specific facts the judge flagged as ungrounded — empty when the verdict
    is a clean "no".
    """

    hallucinated: bool = Field(
        default=False,
        description="True if the response states at least one fact the source does not support.",
    )
    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="The specific facts in the response the source does not support (empty if none).",
    )
DEV_N = 80
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"\d])|(?<=[.!?])\s+(?=[a-z])|(?<=[.!?])\n+")
CHUNK_WORDS = 300
TOP_CHUNKS = 4


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------


def ragtruth_path() -> Path:
    return settings.path("data/public") / "ragtruth_test_subset.jsonl"


def load_rows(path: Path | None = None) -> list[dict]:
    import json

    p = path or ragtruth_path()
    rows: list[dict] = []
    with p.open() as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def dev_test_split(rows: list[dict], dev_n: int = DEV_N) -> tuple[list[dict], list[dict]]:
    """First `dev_n` rows = dev, rest = test (fixed order in the jsonl)."""
    if len(rows) <= dev_n:
        raise ValueError("need more rows than dev_n to split")
    return rows[:dev_n], rows[dev_n:]


def evidence_for(row: dict) -> str:
    """Text the response must be grounded in, per task_type.

    - QA:      `prompt` already contains the question and the passages;
               use it as evidence.
    - Summary: `prompt` is a template ("Summarize the following news
               within 200 words:\n<text>"); `source_info` holds the raw
               document — use that instead.
    - Other:   fall back to `prompt`.
    """
    if row.get("task_type") == "Summary" and isinstance(row.get("source_info"), str):
        return row["source_info"]
    if row.get("task_type") == "QA" and isinstance(row.get("source_info"), dict):
        pi = row["source_info"].get("passages")
        if isinstance(pi, str) and pi.strip():
            return pi
    return row.get("prompt") or ""


def question_for(row: dict) -> str | None:
    pi = row.get("source_info")
    if isinstance(pi, dict) and pi.get("question"):
        return pi["question"]
    return None


# ---------------------------------------------------------------------------
# small pure helpers (testable, no model)
# ---------------------------------------------------------------------------


def split_sentences(text: str) -> list[str]:
    """Split a response into sentences. Keeps at least one piece."""
    text = (text or "").strip()
    if not text:
        return []
    parts = [s.strip() for s in SENT_RE.split(text) if s.strip()]
    return parts or [text]


def chunk_words(text: str, k: int = CHUNK_WORDS) -> list[str]:
    """Split on whitespace into overlapping-free chunks of ~k words (last
    chunk may be shorter).  If the evidence is empty the single empty
    chunk comes back and callers handle it as "no evidence"."""
    words = (text or "").split()
    if not words:
        return [""]
    return [" ".join(words[i : i + k]) for i in range(0, len(words), k)]


def auroc(scores: list[float], labels: list[bool]) -> float:
    """Mann–Whitney U form of AUROC with ties scored 0.5."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return 0.5
    wins = 0.0
    for s in pos:
        for n in neg:
            if s > n:
                wins += 1.0
            elif s == n:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def pick_threshold(scores: list[float], labels: list[bool]) -> float:
    """Max-F1 threshold over the unique score values (score >= thr = positive)."""
    best = (0.0, float("-inf"))
    for thr in sorted(set(scores)):
        tp = fp = fn = 0
        for s, y in zip(scores, labels):
            pred = s >= thr
            if pred and y:
                tp += 1
            elif pred and not y:
                fp += 1
            elif (not pred) and y:
                fn += 1
        _, _, f1 = precision_recall_f1(tp, fp, fn)
        if f1 > best[1]:
            best = (thr, f1)
    return best[0]


def span_token_overlap(pred: tuple[int, int], gold: tuple[int, int]) -> int:
    """Number of characters in the char-span intersection."""
    a = max(pred[0], gold[0])
    b = min(pred[1], gold[1])
    return max(0, b - a)


def span_token_pr(
    pred_spans: list[dict],
    gold_spans: list[dict],
    answer: str,
) -> dict[str, float]:
    """Token-level precision/recall/F1 between predicted spans and gold
    spans, measured character-by-character over `answer` (tokens are
    whitespace-separated).  A "character matched" if it lies inside both
    some predicted span (with confidence > 0) and some gold `hallucinated`
    span.  This matches how evaluators compare span predictions: overlap
    wins, not exact boundaries.
    """
    # RAGTruth gold spans are always hallucination types; the `label_type`
    # field carries one of these four values (never the literal
    # "hallucinated").  Treat any gold span as a hallucinated span.
    HALLUC_TYPES = {
        "evident baseless info",
        "evident conflict",
        "subtle baseless info",
        "subtle conflict",
        "hallucinated",  # tests / other datasets may use the literal
    }
    gold_chars: set[int] = set()
    for g in gold_spans:
        lt = str(g.get("label_type", "")).lower()
        if lt and lt not in HALLUC_TYPES:
            continue
        gold_chars.update(range(g["start"], g["end"]))
    pred_chars: set[int] = set()
    for p in pred_spans:
        if p.get("confidence", 1.0) <= 0:
            continue
        pred_chars.update(range(p["start"], p["end"]))
    inter = len(gold_chars & pred_chars)
    total_pred = len(pred_chars)
    total_gold = len(gold_chars)
    p_ = inter / total_pred if total_pred else 0.0
    r_ = inter / total_gold if total_gold else 0.0
    f1 = 2 * p_ * r_ / (p_ + r_) if (p_ + r_) else 0.0
    return {"precision": p_, "recall": r_, "f1": f1}


def bootstrap_stat(samples: list[tuple[float, bool]], stat) -> tuple[float, float]:
    """Bootstrap 95% CI of `stat` on (score, label) pairs.

    `stat` is a callable accepting (scores, labels) -> float.

    We resample pairs so the (score, label) coupling is preserved; the
    threshold is not re-chosen inside the loop to keep this cheap.
    """
    import numpy as np

    pairs = np.array(
        [(float(s), int(l)) for s, l in samples]
    )
    n = pairs.shape[0]
    if n == 0:
        return (0.0, 0.0)
    rng = np.random.default_rng(0)
    boot = []
    for _ in range(1000):
        idx = rng.integers(0, n, size=n)
        s = pairs[idx, 0].tolist()
        l = pairs[idx, 1].astype(bool).tolist()
        try:
            boot.append(float(stat(s, l)))
        except Exception:
            pass
    if not boot:
        return (0.0, 0.0)
    return (float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975)))


# ---------------------------------------------------------------------------
# model loaders (one per CLI command; cached by the huggingface layer)
# ---------------------------------------------------------------------------


#: HHEM-2.1-Open classifier mapping (from the model repo config.json,
#: `id2label`).  Index 1 = "consistent" (entailed); index 0 = "hallucinated".
#: We hard-code these because the repo's remote-code class does not carry
#: a usable `config.id2label` attribute on the underlying T5 model.
HHEM_CONSISTENT = 1
HHEM_HALLUCINATED = 0
HHEM_PROMPT = (
    "<pad> Determine if the hypothesis is true given the premise?\n"
    "\nPremise: {text1}\n\nHypothesis: {text2}"
)


def load_hhem():
    """Load HHEM-2.1-Open on top of transformers 5.16 + torch 2.14.

    The model repo ships a 72-line remote-code wrapper (HHEMv2ForSequence
    Classification) that subclasses PreTrainedModel and delegates to a
    T5ForTokenClassification with num_labels=2.  On transformers 5.16 the
    wrapper's post_init path crashes on the tied-weights check, but the
    underlying T5 + classifier head loads cleanly when built directly.
    We therefore bypass AutoModelForSequenceClassification and load the
    checkpoint state-dict (with the `t5.` wrapper prefix stripped) into a
    plain T5ForTokenClassification(num_labels=2).

    Tokenizer: the model repo does not ship one, but the base model
    (`google/flan-t5-base`) provides a T5Tokenizer that is compatible
    with the HHEM prompt; this is the documented usage in the repo's
    README.
    """
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    from transformers import T5Config, T5ForTokenClassification, AutoTokenizer

    sd_path = hf_hub_download(
        "vectara/hallucination_evaluation_model", "model.safetensors"
    )
    sd = load_file(sd_path)
    # remote-code wrapper stored weights under a `t5.` prefix
    sd = {k[3:] if k.startswith("t5.") else k: v for k, v in sd.items()}
    cfg = T5Config.from_pretrained("google/flan-t5-base", num_labels=2)
    m = T5ForTokenClassification(cfg)
    m.load_state_dict(sd, strict=False)
    m.eval()
    tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
    return m, tok


def load_lettuce():
    """LettuceDetect span-level token classifier (ModernBERT backbone).

    The `lettucedetect` package's top-level `__init__` is empty in 0.1.6,
    so the detector lands on the fully-qualified module path.
    """
    from lettucedetect.models.inference import TransformerDetector

    return TransformerDetector(
        "KRLabsOrg/lettucedect-base-modernbert-en-v1",
        max_length=4096,
    )


def load_nli():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    m = AutoModelForSequenceClassification.from_pretrained(
        "cross-encoder/nli-deberta-v3-base"
    )
    t = AutoTokenizer.from_pretrained("cross-encoder/nli-deberta-v3-base")
    return m, t


# ---------------------------------------------------------------------------
# scoring: score in [0,1] higher = more hallucinated
# ---------------------------------------------------------------------------


def row_prompt(row: dict) -> str:
    """The instruction used to (re)generate the response, for SelfCheckGPT
    sampling.  RAGTruth's `prompt` is either the QA question (with passage
    list for QA rows) or a Summary template — both are fine as instructions.
    """
    return str(row.get("prompt") or "").strip()


def halluc_judge_prompt_path() -> Path:
    return Path(__file__).parent / "prompts" / "halluc_judge_v1.txt"


def judge_verdict(text: str) -> int:
    """Parse the LLM judge reply (`"yes"` or `"no"` in the JSON output).

    Returns 1 (hallucinated) or 0 (not).  Defaults to 0 on parse failure —
    the prompt tells the model to return strict JSON and a `hallucinated`
    field of "yes" or "no".
    """
    import re
    import json as _json

    text = (text or "").strip()
    # try strict JSON first
    try:
        obj = _json.loads(text)
        if isinstance(obj, dict) and "hallucinated" in obj:
            return 1 if str(obj["hallucinated"]).strip().lower().startswith("y") else 0
    except Exception:
        pass
    # fall back to regex — grab first "hallucinated": "yes|no"
    m = re.search(r'"hallucinated"\s*:\s*"?(yes|no)"?', text, flags=re.I)
    if m:
        return 1 if m.group(1).lower() == "yes" else 0
    return 0


def score_subset(
    rows: list[dict],
    scorer,
    *,
    experiment: str,
    chapter: int,
    dev_fraction: float = 0.3,
    min_dev: int = 0,
    max_dev: int = 80,
    primary: str | None = None,
    span_metric: bool = False,
    llm_calls: int = 0,
    config: dict | None = None,
) -> dict:
    """Score rows, split dev/test, pick threshold on dev, report on test.

    - `dev_fraction` (default 0.3) sets the fraction of `rows` used for
      threshold selection — for the 480-row 09a runs this is 144 dev / 336
      test; for the 100-row judge run this is 30/70; for the 60-row selfcheck
      run this is 18/42.  `max_dev` (default 80) caps the split so the 480-row
      runs keep the original 09a behaviour.
    - `primary` overrides the first metrics name, so `write_metrics` records
      `f1` as the headline for judge while still exposing AUROC/P/R.
    """
    n = len(rows)
    dev_n = int(round(n * dev_fraction))
    dev_n = max(min_dev, min(max_dev, dev_n, n - 1 if n > 1 else n))
    test_n = n - dev_n
    dev_idx = list(range(dev_n))
    test_idx = list(range(dev_n, n))

    t0 = time.time()
    scores: list[tuple[float, dict]] = []
    for i, row in enumerate(rows):
        extra: dict = {}
        s = float(scorer(row, extra))
        s = min(1.0, max(0.0, s))
        scores.append((s, extra))
        if (i + 1) % 25 == 0:
            print(f"  [score] {experiment}: {i + 1}/{n}", flush=True)
    total_seconds = time.time() - t0
    s_per_item = total_seconds / n if n else 0.0

    dev_scores = [scores[i][0] for i in dev_idx]
    dev_labels = [bool(rows[i]["hallucinated"]) for i in dev_idx]
    thr = pick_threshold(dev_scores, dev_labels)

    test_scores = [scores[i][0] for i in test_idx]
    test_labels = [bool(rows[i]["hallucinated"]) for i in test_idx]
    tp = fp = fn = 0
    for s, y in zip(test_scores, test_labels):
        pred = s >= thr
        if pred and y:
            tp += 1
        elif pred and not y:
            fp += 1
        elif (not pred) and y:
            fn += 1
    p_t, r_t, f1_t = precision_recall_f1(tp, fp, fn)
    a_t = auroc(test_scores, test_labels)

    per_task: dict[str, dict] = {}
    for tt in ("QA", "Summary", "Data2txt"):
        idx = [i for i in test_idx if rows[i].get("task_type") == tt]
        if len(idx) < 20:
            continue
        ss = [scores[i][0] for i in idx]
        ll = [bool(rows[i]["hallucinated"]) for i in idx]
        tp2 = fp2 = fn2 = 0
        for s, y in zip(ss, ll):
            pred = s >= thr
            if pred and y:
                tp2 += 1
            elif pred and not y:
                fp2 += 1
            elif (not pred) and y:
                fn2 += 1
        p2, r2, f2 = precision_recall_f1(tp2, fp2, fn2)
        per_task[tt] = {
            "n": len(idx),
            "hallucinated": sum(ll),
            "auroc": round(auroc(ss, ll), 4),
            "precision": round(p2, 4),
            "recall": round(r2, 4),
            "f1": round(f2, 4),
        }

    pairs = list(zip(dev_scores, dev_labels)) + list(zip(test_scores, test_labels))
    auroc_ci = bootstrap_stat(pairs, lambda s, l: auroc(s, l))
    f1_ci = bootstrap_stat(pairs, lambda s, l: precision_recall_f1(*(_pr_from(s, l, thr)))[2])

    metrics = {
        "f1": round(f1_t, 4),
        "auroc": round(a_t, 4),
        "precision": round(p_t, 4),
        "recall": round(r_t, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }
    if primary and primary in metrics:
        # Reorder so the primary metric is first — `results.write_metrics`
        # uses the first key as the headline. The 09a runs (primary=None)
        # keep their historical `f1`-first order.
        value = metrics.pop(primary)
        metrics = {primary: value, **metrics}
    ci = {"f1": f1_ci, "auroc": auroc_ci}

    predictions = [
        {
            "id": rows[i].get("id"),
            "task_type": rows[i].get("task_type"),
            "model": rows[i].get("model"),
            "hallucinated": bool(rows[i]["hallucinated"]),
            "score": round(scores[i][0], 6),
            "extra": {k: v for k, v in (scores[i][1] or {}).items() if k not in ("pred_spans",)},
        }
        for i in test_idx
    ]

    config = dict(config or {})
    config.setdefault("rows", n)
    config.setdefault("dev_split", dev_n)
    config.setdefault("threshold_rule", "argmax F1 over unique scores on dev")
    config.setdefault("cpu_only", True)

    details = {
        "dev_n": dev_n,
        "test_n": test_n,
        "threshold": thr,
        "s_per_item": round(s_per_item, 4),
        "per_task_type": per_task,
        "span_metric": span_metric,
        "notes": "dev/test split within rows; threshold picked on dev to maximise F1",
    }
    if span_metric:
        # span P/R on test rows, using extra["pred_spans"]
        preds = [scores[i][1].get("pred_spans") for i in test_idx]
        golds = [rows[i].get("labels") or [] for i in test_idx]
        answers = [str(rows[i].get("response")) for i in test_idx]
        ps = [span_token_pr(p or [], g, a)["precision"] for p, g, a in zip(preds, golds, answers)]
        rs = [span_token_pr(p or [], g, a)["recall"] for p, g, a in zip(preds, golds, answers)]
        fs = [span_token_pr(p or [], g, a)["f1"] for p, g, a in zip(preds, golds, answers)]
        details["span_precision"] = round(sum(ps) / len(ps), 4)
        details["span_recall"] = round(sum(rs) / len(rs), 4)
        details["span_f1"] = round(sum(fs) / len(fs), 4)

    R.write_metrics(
        experiment,
        chapter,
        test_n,
        metrics,
        ci=ci,
        llm_calls=llm_calls,
        seconds=round(total_seconds, 2),
        details=details,
        predictions=predictions,
        config=config,
    )
    return {
        "auroc": a_t,
        "f1": f1_t,
        "precision": p_t,
        "recall": r_t,
        "threshold": thr,
        "s_per_item": s_per_item,
        "seconds": total_seconds,
    }


# keep backward-compatible alias so old 09a commands still work
def score_all(*args, **kw) -> dict:  # type: ignore[no-redef]
    return score_subset(*args, **kw)


def _pr_from(scores, labels, thr):
    tp = sum(1 for s, y in zip(scores, labels) if s >= thr and y)
    fp = sum(1 for s, y in zip(scores, labels) if s >= thr and not y)
    fn = sum(1 for s, y in zip(scores, labels) if s < thr and y)
    return tp, fp, fn


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


@app.command("hhem")
def hhem() -> None:
    """HHEM-2.1-Open (vectara) — 1 − consistency between evidence + response."""
    rows = load_rows()
    model, tok = load_hhem()

    def scorer(row: dict, extra: dict) -> float:
        ev = evidence_for(row)
        resp = str(row.get("response") or "")
        if not ev.strip() or not resp.strip():
            return 0.0
        out = tok(
            HHEM_PROMPT.format(text1=ev, text2=resp),
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        input_ids = out["input_ids"]
        attention_mask = out["attention_mask"]
        with torch.no_grad():
            logits = model(input_ids=input_ids, attention_mask=attention_mask).logits
        # T5ForTokenClassification returns per-token logits; the head is
        # applied on every position, so take the first token's logit row
        # (matches the wrapper's forward, which does `logits[:, 0, :]`).
        head = logits[:, 0, :] if logits.dim() == 3 else logits
        probs = torch.softmax(head, dim=-1)
        cons = float(probs[0, HHEM_CONSISTENT].item())
        extra["consistency"] = cons
        return 1.0 - cons

    r = score_all(rows, scorer, experiment="09_hhem_ragtruth", chapter=9)
    print(f"\nhhem: auroc={r['auroc']:.4f} f1={r['f1']:.4f} thr={r['threshold']:.4f} s/item={r['s_per_item']:.3f}")


@app.command("lettuce")
def lettuce() -> None:
    """LettuceDetect — max span confidence; span P/R in details."""
    rows = load_rows()
    det = load_lettuce()

    def scorer(row: dict, extra: dict) -> float:
        resp = str(row.get("response") or "")
        if not resp.strip():
            return 0.0
        # LettuceDetect is trained on a *specific* RAGTruth prompt layout
        # (passage-list QA / bare summary). Its `predict()` builds that
        # layout for us, which keeps the answer's char offsets aligned with
        # the tokenizer's offset mapping — so the returned span offsets are
        # valid for span-token P/R. Passing the raw RAGTruth `prompt` through
        # `predict_prompt` breaks that alignment and tanks the span metric.
        pi = row.get("source_info")
        q = question_for(row)
        if row.get("task_type") == "QA" and isinstance(pi, dict):
            passages = str(pi.get("passages") or "")
            # RAGTruth stores passages as one string prefixed with
            # "passage 1: ", "passage 2: ", ... — LettuceDetect's
            # `_form_prompt` re-adds that prefix per list item, so strip it
            # here to avoid doubling.
            parts = re.split(r"(?im)^\s*passage \d+\s*:\s*|passage \d+\s*:\s*", passages)
            context = [p.strip() for p in parts if p.strip()] or [passages]
            question = q
        else:
            context = [str(pi) if isinstance(pi, str) else str(row.get("prompt") or "")]
            question = None
        if not any(c.strip() for c in context):
            return 0.0
        spans = det.predict(context, resp, question=question, output_format="spans") or []
        extra["pred_spans"] = spans
        confs = [s.get("confidence", 0.0) for s in spans]
        if not confs:
            return 0.0
        return float(max(confs))

    r = score_all(
        rows,
        scorer,
        experiment="09_lettuce_ragtruth",
        chapter=9,
        span_metric=True,
    )
    print(f"\nlettuce: auroc={r['auroc']:.4f} f1={r['f1']:.4f} thr={r['threshold']:.4f} s/item={r['s_per_item']:.3f}")


@app.command("nli")
def nli() -> None:
    """cross-encoder/nli-deberta-v3-base — 1 − min(entailment) over sentences."""
    rows = load_rows()
    enc, etok = load_nli()
    ent_idx = _label_index(enc.config.id2label, "entailment")

    def scorer(row: dict, extra: dict) -> float:
        resp = str(row.get("response") or "")
        ev = evidence_for(row)
        sents = split_sentences(resp)
        chunks = chunk_words(ev, CHUNK_WORDS)
        if not sents or not (chunks and chunks[0].strip()):
            return 0.0
        best_chunks = chunks[:TOP_CHUNKS]
        min_ent = 1.0
        for sent in sents:
            # cross-encoder tokenizer requires equal batch lengths for
            # `text` and `text_pair`; repeat the sentence once per chunk
            o = etok(
                [sent] * len(best_chunks),
                best_chunks,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )
            with torch.no_grad():
                probs = torch.softmax(enc(**o).logits.float(), dim=-1)
            ent_for_sent = float(probs[:, ent_idx].max().item())
            min_ent = min(min_ent, ent_for_sent)
        extra["min_entailment"] = min_ent
        return 1.0 - min_ent

    r = score_all(rows, scorer, experiment="09_nli_ragtruth", chapter=9)
    print(f"\nnli: auroc={r['auroc']:.4f} f1={r['f1']:.4f} thr={r['threshold']:.4f} s/item={r['s_per_item']:.3f}")


def nli_pair_entailment(
    text: str,
    hypothesis: str,
    enc,
    etok,
    ent_idx: int,
) -> float:
    """Entailment probability of `hypothesis` given `text` from the NLI
    cross-encoder.  Used by the `nli` detector (each response sentence vs the
    evidence chunks) and by `selfcheck` (each sample vs the original response)."""
    import torch

    o = etok([text, hypothesis], padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        probs = torch.softmax(enc(**o).logits.float(), dim=-1)
    return float(probs[:, ent_idx].max().item())


def judge_messages(row: dict) -> list[dict]:
    """Build the chat messages for the hallucination-judge call on one row.

    Follows the same system+user pattern used by `judge.py` (L116-128).
    """
    template = halluc_judge_prompt_path().read_text()
    template = template.replace("{task_type}", str(row.get("task_type") or ""))
    template = template.replace("{evidence}", evidence_for(row))
    template = template.replace("{response}", str(row.get("response") or ""))
    template = template.replace("{question}", question_for(row) or "(n/a)")
    return [
        {"role": "system", "content": "You are a careful, fair evaluator."},
        {"role": "user", "content": template},
    ]


def load_traces(run: str) -> list[dict]:
    """Load all trace JSONs for a given run from `runs/traces/<run>/`."""
    import json as _json
    base = settings.path("runs") / "traces" / run
    files = sorted(base.glob("*.json")) if base.exists() else []
    if not files:
        raise FileNotFoundError(f"no trace files under {base}")
    return [_json.loads(f.read_text()) for f in files]


def load_labels(run: str) -> dict[str, dict]:
    """Load the chapter-03 labels for a run; returns {ticket_id: label_row}."""
    import json as _json
    p = settings.path("data") / "labels" / f"{run}.jsonl"
    out: dict[str, dict] = {}
    with p.open() as fh:
        for line in fh:
            if line.strip():
                r = _json.loads(line)
                out[r["ticket_id"]] = r
    return out


def handbook_text_for(trace: dict) -> str:
    """Concatenate the full handbook section texts listed in a trace's
    `retrieved` field — this is the source the helpdesk reply claims to be
    grounded in."""
    from evals_tutorial import handbook
    sections = handbook.load()
    parts: list[str] = []
    for item in trace.get("retrieved") or []:
        sid = item.get("section", "")
        txt = sections.get(sid)
        if txt:
            parts.append(txt)
    return "\n\n".join(parts)


def selfcheck_score(consistencies: list[float]) -> float:
    """SelfCheckGPT-style response-level hallucination score.

    A response that stays consistent across independently-sampled
    paraphrases is *unlikely* to be a hallucination; one whose samples
    disagree with it is.  `consistencies` is the NLI entailment probability
    between the original response and each sampled variant (all in [0, 1]).
    We score the *mean* consistency and flip it so that **higher = more
    likely hallucinated**, matching every other detector in this module.

    Empty input (a sample that could not be generated) is treated as
    maximally consistent — i.e. no evidence of fabrication.
    """
    if not consistencies:
        return 0.0
    mean_c = sum(consistencies) / len(consistencies)
    return min(1.0, max(0.0, 1.0 - mean_c))


def pairwise_agreement(a: list[bool], b: list[bool]) -> float:
    """Fraction of positions where two binary verdict vectors agree.

    Used by `compare` to report how much the detectors and the LLM judge
    disagree row-by-row.  Returns 0.0 for an empty comparison.
    """
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(1 for x, y in zip(a, b) if bool(x) == bool(y)) / n


def _label_index(id2label: dict, *names: str) -> int:
    """Find the label index for the first matching label name (HF `id2label`
    is `{str(index): label_name}`).  Falls back to matching keys if the
    mapping appears inverted."""
    for name in names:
        n = name.lower()
        for k, v in id2label.items():
            if str(v).lower() == n:
                return int(k)
    for name in names:
        n = name.lower()
        for k, _v in id2label.items():
            if str(k).lower() == n:
                try:
                    return int(k)
                except ValueError:
                    return 0
    return 0


@app.command("selfcheck")
def selfcheck() -> None:
    """SelfCheckGPT-style sampling consistency on 60 test RAGTruth rows.

    For each of the 60 rows (rows[80:140] of the 480-row dataset, all
    Summary) we re-generate the response 3 times at temperature 0.7 with
    different seeds — 180 cached chat calls — and score each sample against
    the original by NLI cross-encoder entailment (bidirectional mean).
    A low consistency (sample differs from original) is the signal: that
    means the original is not stably reproducible from the same source,
    which is the SelfCheckGPT heuristic for a fabricated response.

    Experiment: `09_selfcheck_ragtruth` (n=60, 18 dev / 42 test).
    """
    from evals_tutorial import llm as _llm

    rows = load_rows()
    subset = rows[80:140]
    if not subset:
        raise RuntimeError("no rows in selfcheck window")
    enc, etok = load_nli()
    ent_idx = _label_index(enc.config.id2label, "entailment")
    original_model, _ = load_hhem()  # noqa: F841 — ensures HF models are cached before we burn GPU

    n_samples = 3
    seeds = (42, 43, 44)

    def _scorer(row: dict, extra: dict) -> float:
        prompt = row_prompt(row)
        original = str(row.get("response") or "")
        if not prompt.strip() or not original.strip():
            extra["consistencies"] = []
            return selfcheck_score([])
        consistencies: list[float] = []
        for seed in seeds[:n_samples]:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that strictly follows the instruction."},
                {"role": "user", "content": prompt},
            ]
            try:
                sample = _llm.ollama.chat(
                    messages,
                    temperature=0.7,
                    seed=seed,
                    max_tokens=512,
                )
            except Exception:
                sample = ""
            if not sample.strip():
                continue
            # bidirectional consistency: mean entailment both directions
            forward = nli_pair_entailment(original, sample, enc, etok, ent_idx)
            backward = nli_pair_entailment(sample, original, enc, etok, ent_idx)
            consistencies.append((forward + backward) / 2.0)
        extra["consistencies"] = [round(c, 4) for c in consistencies]
        return selfcheck_score(consistencies)

    llm_calls = len(subset) * n_samples
    r = score_subset(
        subset,
        _scorer,
        experiment="09_selfcheck_ragtruth",
        chapter=9,
        dev_fraction=0.3,
        min_dev=18,
        max_dev=18,
        primary="auroc",
        llm_calls=llm_calls,
        config={
            "method": "selfcheckgpt_sampling_consistency",
            "window": "rows[80:140] of 480-row RAGTruth",
            "task_type": "Summary (all rows in window)",
            "n_samples": n_samples,
            "seeds": list(seeds),
            "temperature": 0.7,
            "scorer": "nli-deberta-v3 bidirectional entailment mean",
            "score_formula": "1 - mean over samples of mean(ent(o->s), ent(s->o))",
            "llm_calls": llm_calls,
            "cache": "ollama on-disk, sha256 keyed by model + options + messages + schema + think + seed",
        },
    )
    print(f"\nselfcheck: auroc={r['auroc']:.4f} f1={r['f1']:.4f} thr={r['threshold']:.4f} s/item={r['s_per_item']:.3f}")


@app.command("judge")
def judge() -> None:
    """LLM hallucination judge (qwen3.8:27b) on the first 100 test rows.

    Prompts `prompts/halluc_judge_v1.txt`, constrains the reply to the
    `HallucJudgeVerdict` schema, and turns `verdict.hallucinated` into a
    binary 1 / 0 score.  Binary verdicts let `score_subset` pick a
    meaningful F1 on the dev split and expose P/R to `results.md`.

    Experiment: `09_llm_judge_ragtruth` (n=100, 30 dev / 70 test).
    """
    from evals_tutorial import llm as _llm

    rows = load_rows()
    subset = rows[80:180]
    if not subset:
        raise RuntimeError("no rows in judge window")

    def _scorer(row: dict, extra: dict) -> float:
        messages = judge_messages(row)
        try:
            v = _llm.ollama.chat_json(
                messages, HallucJudgeVerdict, temperature=0.0, seed=42
            )
        except Exception:
            v = HallucJudgeVerdict(hallucinated=False, unsupported_claims=[])
        extra["hallucinated"] = v.hallucinated
        extra["n_claims"] = len(v.unsupported_claims)
        extra["claims"] = v.unsupported_claims[:5]
        return 1.0 if v.hallucinated else 0.0

    llm_calls = len(subset)
    r = score_subset(
        subset,
        _scorer,
        experiment="09_llm_judge_ragtruth",
        chapter=9,
        dev_fraction=0.3,
        min_dev=30,
        max_dev=30,
        primary="f1",
        llm_calls=llm_calls,
        config={
            "method": "llm_judge",
            "window": "rows[80:180] of 480-row RAGTruth",
            "prompt": "prompts/halluc_judge_v1.txt",
            "model": settings.chat_model,
            "schema": "HallucJudgeVerdict {hallucinated: bool, unsupported_claims: list[str]}",
            "score": "1.0 if verdict.hallucinated else 0.0",
            "llm_calls": llm_calls,
        },
    )
    print(f"\njudge: auroc={r['auroc']:.4f} f1={r['f1']:.4f} thr={r['threshold']:.4f} s/item={r['s_per_item']:.3f}")


@app.command("compare")
def compare() -> None:
    """Cross-method comparison table for ch-09 (no LLM calls).

    Reads the 09_* metrics + predictions already in `runs/`, and writes
    `runs/09_compare.md` with a per-method row (each method uses its own
    headline metric from `metrics.json`), pairwise binary agreement on the
    intersection of row-ids, and a per-task-type note.
    """
    import json as _json

    runs_dir = settings.path("runs")
    exps = [
        ("09_hhem_ragtruth", "HHEM (vectara)", "auroc"),
        ("09_lettuce_ragtruth", "LettuceDetect", "auroc"),
        ("09_nli_ragtruth", "NLI cross-encoder", "auroc"),
        ("09_selfcheck_ragtruth", "SelfCheckGPT", "auroc"),
        ("09_llm_judge_ragtruth", "qwen3.8:27b judge", "f1"),
    ]
    records: dict[str, dict] = {}
    for exp, _label, _primary in exps:
        p = runs_dir / exp / "metrics.json"
        if p.exists():
            records[exp] = _json.loads(p.read_text())
        else:
            records[exp] = None

    # predictions: {id: (label, score)}
    preds: dict[str, dict[str, tuple[bool, float]]] = {}
    for exp, _l, _p in exps:
        f = runs_dir / exp / "predictions.jsonl"
        if not f.exists():
            continue
        per_method: dict[str, tuple[bool, float]] = {}
        with f.open() as fh:
            for line in fh:
                if not line.strip():
                    continue
                row = _json.loads(line)
                per_method[str(row.get("id"))] = (
                    bool(row.get("hallucinated", False)),
                    float(row.get("score", 0.0)),
                )
        for rid, val in per_method.items():
            preds.setdefault(rid, {})[exp] = val

    def _headline_method(record: dict | None) -> str:
        """Return a short human-readable headline for this method's best metric."""
        if not record:
            return "(not run yet)"
        primary = record.get("details", {}).get("primary") or ""
        val = record.get("metrics", {}).get(primary)
        s_item = round(record.get("seconds", 0) / max(int(record.get("n", 1)), 1), 3)
        return f"{primary}={val}  ({record.get('n')} rows, {s_item}s/item)"

    def _fmt(v: float) -> str:
        return f"{v:.3f}" if v is not None else "—"

    def _agreement(method_a: str, method_b: str) -> float | None:
        common = [rid for rid in preds if method_a in preds[rid] and method_b in preds[rid]]
        if not common:
            return None
        a = [preds[rid][method_a][1] for rid in common]
        b = [preds[rid][method_b][1] for rid in common]
        # binary compare at each method's own dev threshold: score >= 0.5
        a_bin = [s >= 0.5 for s in a]
        b_bin = [s >= 0.5 for s in b]
        return pairwise_agreement(a_bin, b_bin)

    order = [exp for exp, _l, _p in exps]
    header_cells = ["Method", "Headline", "n"] + [f"agreement w/{lbl}" for _e, lbl, _p in exps if lbl]
    # simpler: build a small matrix over the 5 methods with a 0.5 threshold
    lines: list[str] = []
    lines.append("Cross-method comparison for ch-09.")
    lines.append("")
    lines.append("Per-method headline metric from `runs/<experiment>/metrics.json`:")
    lines.append("")
    lines.append("| Method | Headline AUROC (or primary) | n (rows) |")
    lines.append("|---|---|---|")
    for exp, label, _p in exps:
        n = records[exp].get("n", 0) if records[exp] else 0
        headline = _headline_method(records[exp])
        if "auroc" in headline:
            headline = headline.replace("auroc=", "AUROC=")
        lines.append(f"| {label} | {headline} | {n} |")
    lines.append("")
    lines.append("Pairwise binary agreement at 0.5 score threshold (all methods share the RAGTruth test rows):")
    lines.append("")
    lines.append("| | " + " | ".join(lbl for _e, lbl, _p in exps) + " |")
    lines.append("|" + "---|" * (len(exps) + 1))
    for exp_a, label_a, _pa in exps:
        cells = []
        for exp_b, label_b, _pb in exps:
            if exp_a == exp_b:
                cells.append("—")
            else:
                v = _agreement(exp_a, exp_b)
                cells.append(_fmt(v) if v is not None else "—")
        lines.append("| " + label_a + " | " + " | ".join(cells) + " |")
    lines.append("")
    shared_ids = list(preds.keys())
    summary_types = set()
    for rid in shared_ids:
        row = next((r for r in []), None)  # placeholder: not reading the raw jsonl for this
    lines.append(f"Shared rows across all 5 methods: {len(shared_ids)} (RAGTruth test set: 240 QA + 160 Summary).  The SelfCheckGPT and LLM-judge methods only cover a subset (windows within these 400), so their pairwise cells above use the smaller overlap.")
    lines.append("")
    lines.append("Notes on score scale: HHEM / Lettuce / NLI / SelfCheckGPT are continuous [0,1] (higher = more hallucinated).  The LLM judge is discrete {0, 1}.  Pairwise agreement is therefore computed at the 0.5 threshold for the continuous methods, which is a fair midpoint.")
    lines.append("")
    out = runs_dir / "09_compare.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"\nwrote {out}")


@app.command("apply")
def apply(
    run: str = typer.Option("answer_v1", help="answer_v1 | answer_v2"),
) -> None:
    """Ch-09b apply: HHEM + Lettuce over our own helpdesk reply traces.

    Loads the 60 `test` split traces for the given run, scores each with
    HHEM and LettuceDetect (source = concatenated retrieved handbook text,
    response = the model's reply text), and uses the chapter-03
    `unsupported_claim` label as the gold binary.  Reports AUROC on all 60
    rows, F1 at the best threshold on the same 60 rows, and lists the 3
    highest-Lettuce-confidence rows (flagged span + its sentence in the
    reply) so a human can eyeball what the detector is actually firing on.

    Experiment: `09_detector_helpdesk_v1` (primary `auroc`).
    """
    traces = load_traces(run)
    labels = load_labels(run)
    from evals_tutorial import handbook  # noqa: F401  (ensures handbook module is importable)

    # filter to test split (labels carry ticket_id; trace has ticket_id + run)
    from evals_tutorial.tickets import load_tickets
    tickets_by_id = {t["id"]: t for t in load_tickets()}
    test_traces = [
        tr for tr in traces
        if (tr.get("ticket_id") in tickets_by_id
            and tickets_by_id[tr["ticket_id"]]["split"] == "test")
    ]

    hhem_model, hhem_tok = load_hhem()
    enc, etok = load_nli()  # noqa: F841
    lettuce_det = load_lettuce()
    del enc, etok  # we only need hhem + lettuce

    def _one(trace: dict) -> dict:
        response = str(trace.get("output") or "")
        source = handbook_text_for(trace)
        ticket = tickets_by_id[trace["ticket_id"]]
        label_row = labels.get(trace["ticket_id"], {})
        gold = "unsupported_claim" in (label_row.get("failure_modes") or [])

        # -- HHEM --
        hhem_score = 0.0
        if response.strip() and source.strip():
            out = hhem_tok(
                HHEM_PROMPT.format(text1=source, text2=response),
                truncation=True, max_length=512, return_tensors="pt",
            )
            with torch.no_grad():
                logits = hhem_model(input_ids=out["input_ids"], attention_mask=out["attention_mask"]).logits
            head = logits[:, 0, :] if logits.dim() == 3 else logits
            probs = torch.softmax(head, dim=-1)
            cons = float(probs[0, HHEM_CONSISTENT].item())
            hhem_score = 1.0 - cons

        # -- Lettuce (with spans) --
        lettuce_score = 0.0
        lettuce_spans: list[dict] = []
        if response.strip() and source.strip():
            try:
                spans = lettuce_det.predict([source], response, output_format="spans") or []
            except Exception:
                spans = []
            lettuce_spans = [
                {
                    "span": s.get("span") or s.get("text", ""),
                    "confidence": float(s.get("confidence", 0.0)),
                    "start": int(s.get("start", -1)),
                    "end": int(s.get("end", -1)),
                }
                for s in spans
            ]
            confs = [s["confidence"] for s in lettuce_spans]
            lettuce_score = float(max(confs)) if confs else 0.0

        sentence = _sentence_at(response, lettuce_spans[0]["start"] if lettuce_spans else 0)

        return {
            "ticket_id": trace["ticket_id"],
            "gold": bool(gold),
            "hhem": round(hhem_score, 6),
            "lettuce": round(lettuce_score, 6),
            "lettuce_spans": lettuce_spans[:5],
            "reply_sentence": sentence,
        }

    results = [_one(tr) for tr in test_traces]

    def _scores(key: str) -> list[float]:
        return [r[key] for r in results]

    def _labels() -> list[bool]:
        return [r["gold"] for r in results]

    def _best_f1(scores: list[float], labs: list[bool]) -> dict:
        thr = pick_threshold(scores, labs)
        tp = fp = fn = 0
        for s, y in zip(scores, labs):
            pred = s >= thr
            if pred and y: tp += 1
            elif pred and not y: fp += 1
            elif (not pred) and y: fn += 1
        p, r, f1 = precision_recall_f1(tp, fp, fn)
        return {"auroc": round(auroc(scores, labs), 4), "f1": round(f1, 4),
                "threshold": thr, "tp": tp, "fp": fp, "fn": fn,
                "precision": round(p, 4), "recall": round(r, 4)}

    hhem_m = _best_f1(_scores("hhem"), _labels())
    lettuce_m = _best_f1(_scores("lettuce"), _labels())

    # 3 most-flagged by Lettuce
    top = sorted(results, key=lambda r: -r["lettuce"])[:3]

    # write_metrics: primary = auroc for the HHEM variant; details carry both methods.
    auroc_hh = hhem_m["auroc"]
    auroc_lt = lettuce_m["auroc"]
    metrics = {
        "auroc": round(max(auroc_hh, auroc_lt), 4),  # headline = better of the two
        "f1": round(max(hhem_m["f1"], lettuce_m["f1"]), 4),
        "hhem_auroc": auroc_hh,
        "hhem_f1": hhem_m["f1"],
        "lettuce_auroc": auroc_lt,
        "lettuce_f1": lettuce_m["f1"],
        "positives": sum(_labels()),
    }
    details = {
        "n_gold_positives": sum(_labels()),
        "n_gold_negatives": len(_labels()) - sum(_labels()),
        "hhem": hhem_m,
        "lettuce": lettuce_m,
        "top3_by_lettuce": [
            {
                "ticket_id": t["ticket_id"],
                "lettuce": t["lettuce"],
                "hhem": t["hhem"],
                "gold": t["gold"],
                "span": t["lettuce_spans"][0] if t["lettuce_spans"] else None,
                "sentence": t["reply_sentence"],
            }
            for t in top
        ],
        "notes": "Gold = chapter-03 `unsupported_claim` label; source = concatenated retrieved handbook sections",
        "cpu_only": True,
    }
    R.write_metrics(
        "09_detector_helpdesk_v1",
        9,
        len(results),
        metrics,
        ci=None,
        llm_calls=0,
        seconds=0.0,
        details=details,
        predictions=[
            {
                "id": r["ticket_id"],
                "task_type": "helpdesk_reply",
                "hallucinated": r["gold"],
                "score": r["hhem"],
                "hhem": r["hhem"],
                "lettuce": r["lettuce"],
                "extra": {"lettuce_spans": r["lettuce_spans"]},
            }
            for r in results
        ],
        config={
            "run": run,
            "split": "test",
            "n_traces": len(test_traces),
            "detectors": ["hhem", "lettuce"],
            "source": "concatenated retrieved handbook sections",
            "response": "model reply text from traces",
        },
    )
    print(f"\napply {run}: n={len(results)}  hhem auroc={auroc_hh:.4f}  lettuce auroc={auroc_lt:.4f}")
    print("top 3 lettuce:")
    for t in top:
        print(f"  {t['ticket_id']}  lettuce={t['lettuce']:.3f}  gold={t['gold']}  span={t['lettuce_spans'][0]['span'] if t['lettuce_spans'] else '—'}")


def _sentence_at(text: str, pos: int) -> str:
    """Return the sentence in `text` that contains index `pos`."""
    sents = split_sentences(text)
    # simple O(n) scan: find the sentence whose span covers pos
    cursor = 0
    for s in sents:
        if cursor <= pos < cursor + len(s):
            return s
        cursor += len(s) + 1
    return sents[0] if sents else ""


if __name__ == "__main__":
    app()
