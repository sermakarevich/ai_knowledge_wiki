"""Chapter 04 — code-graded evals: the cheapest tier of evaluation.

Pure code, no LLM judge. Three experiments over the `test` split:

- `triage`    — `triage_v1` traces vs gold: accuracy, macro/micro F1 for
  `category`, accuracy for `priority` / `needs_escalation`, a confusion
  matrix (`confusion.png`) and the JSON-validity rate of the raw output.
  Primary metric `f1_macro`.
- `checks`    — table-driven, deterministic assertions (IFEval-style
  verifiable instructions) over every `answer_v1` reply. Primary
  `all_checks_pass`.
- `similarity`— hand-rolled ROUGE-L and `nomic-embed-text` cosine similarity
  vs the concatenated gold answer points, plus the correlation/AUC of each
  score with the chapter-03 `pass` label (the number that shows whether
  similarity tracks quality). Primary `auroc_embed_vs_label`.

All numbers go through `results.write_metrics` into
`runs/<experiment>/{metrics.json, predictions.jsonl, config.json}` and
`results.build()` turns every committed experiment into
`project/runs/results.md`. Every command is injectable with a fake client
(`evals_tutorial.testing.FakeLLM`), so the test-suite runs offline.
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import typer  # noqa: E402
import yaml  # noqa: E402

from evals_tutorial import handbook as HB  # noqa: E402
from evals_tutorial import llm as _llm  # noqa: E402
from evals_tutorial import results as R  # noqa: E402
from evals_tutorial.config import settings  # noqa: E402
from evals_tutorial.helpdesk import load_traces  # noqa: E402
from evals_tutorial.labels import load_labels  # noqa: E402
from evals_tutorial.tickets import load_tickets  # noqa: E402

CATEGORY_ORDER = [
    "returns",
    "warranty",
    "shipping",
    "payments",
    "damaged_items",
    "international",
    "order_changes",
    "discounts",
    "gift_cards",
    "loyalty",
    "accounts",
    "privacy",
]

_STOPWORDS = frozenset(
    (
        "the a an and or but of in on at to for by with from as is are was were be been being "
        "has have had do does did will would could should may might must its it it's not no yes "
        "your you our we i me my their there here when where what which who whom how why this "
        "that then than so such also very really just only if after before during while out up "
        "down off over under again further once you'll they'll we'll can't cannot won't "
        "would've should've one two".split()
    )
)

_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
# A phone number: 7-13 digits in 2-4 digit groups with optional
# +/()/.-space separators between groups. Requires at least three groups
# (or a large single digit run) so policy text like "30-day window" or
# "3 to 7 business days" never trips the check, while "044 555 044-1234",
# "+1 (555) 123-4567" and a raw 10-digit run do.
_PHONE_RE = re.compile(
    r"(?<!\d)"
    r"\+?"                          # optional international +
    r"\(?"                          # optional opening paren
    r"\d{2,4}[\s.\-]?"              # first digit group (country / area code)
    r"\)?"                          # optional closing paren after area
    r"\d{2,4}[\s.\-]?"
    r"(?:\d{2,4}[\s.\-]?){1,3}"     # at least one more digit group
    r"(?!\d)"
)


def _llm_usage() -> int:
    """Total Ollama calls made so far (hits + misses), via the shared usage log.

    Call `_llm_usage` before the LLM work and again after; the difference is
    this run's contribution (avoids crediting unrelated earlier chapters)."""
    return _llm.usage_log.get("hits", 0) + _llm.usage_log.get("misses", 0)


def _word_count(text: str) -> int:
    text = text or ""
    return len(re.findall(r"\S+", text))


def _f1(precision: float, recall: float) -> float:
    return 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)


def _mean_sd(values: list[float]) -> tuple[float, float]:
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        return 0.0, 0.0
    return float(a.mean()), (float(a.std(ddof=1)) if a.size > 1 else 0.0)


def _auroc(scores: list[float], labels: list[int]) -> float:
    """Area under the ROC curve via Mann-Whitney U (ties give rank 0.5).

    Equivalent to `sklearn.metrics.roc_auc_score` for a binary label, but
    dependency-free so the tutorial can show the math in ~15 lines.
    """
    n_pos = sum(1 for y in labels if y == 1)
    n_neg = len(labels) - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ZeroDivisionError("AUC needs both positive and negative labels")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    rank_sum_pos = sum(ranks[i] for i, y in enumerate(labels) if y == 1)
    u = rank_sum_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def _correlation(scores: list[float], labels: list[int]) -> float:
    a = np.asarray(scores, dtype=float)
    b = np.asarray(labels, dtype=float)
    if a.size == 0 or a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


# ============================================================================
# text-similarity helpers
# ============================================================================

def _longest_lcs_len(a: list[str], b: list[str]) -> int:
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return 0
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]


def rouge_l(ref: str | list[str], hyp: str | list[str]) -> dict[str, float]:
    """Hand-rolled ROUGE-L (precision, recall, F-measure) over word tokens.

    `ref` and `hyp` may be a single string or a list of strings (a list is
    concatenated into one candidate). The F-measure uses beta=1 (R-B=1), the
    convention used by the original ROUGE-L paper.
    """
    def _tokens(x) -> list[str]:
        if isinstance(x, (list, tuple)):
            text = " ".join(x)
        else:
            text = x or ""
        return [t.lower() for t in re.findall(r"\w+'?\w*|[^\s\w]", text) if t.isalnum() or t.isalpha()]
    r = _tokens(ref)
    h = _tokens(hyp)
    if not r or not h:
        return {"precision": 0.0, "recall": 0.0, "f": 0.0}
    lcs = _longest_lcs_len(h, r)
    precision = lcs / len(h)
    recall = lcs / len(r)
    f = 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f": f}


def _cosine(a: list[float], b: list[float]) -> float:
    va = np.asarray(a, dtype=float)
    vb = np.asarray(b, dtype=float)
    na = float(np.linalg.norm(va))
    nb = float(np.linalg.norm(vb))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))


def _keyword_keywords(point: str) -> list[str]:
    """The 2 longest (non-stopword) words of an answer point, lower-cased.

    Falls back to all non-stopword words if the point has < 2 real words.
    """
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]*", point)]
    words = [w for w in words if w not in _STOPWORDS and len(w) > 1] or words
    words.sort(key=lambda w: (-len(w), w))
    return words[:2]


def _load_forbidden_phrases() -> list[str]:
    path = settings.path("data") / "checks" / "forbidden_phrases.yaml"
    data = yaml.safe_load(path.read_text()) or {}
    phrases = data.get("phrases", data if isinstance(data, list) else [])
    return [str(p) for p in phrases]


_HANDBOOK_TEXT = "\n".join(HB.SECTION_TITLES.get(sid, sid) for sid in HB.SECTION_IDS)
_HANDBOOK_CONTACTS = set(_EMAIL_RE.findall(_HANDBOOK_TEXT)) | set(_PHONE_RE.findall(_HANDBOOK_TEXT))


# ============================================================================
# the six deterministic checks (the "verifiable instructions" tier)
# ============================================================================

def _check_nonempty(ticket: dict, trace: dict) -> bool:
    out = (trace.get("output") or "").strip()
    return bool(out)


def _check_max_words_150(ticket: dict, trace: dict) -> bool:
    return _word_count(trace.get("output") or "") <= 150


def _check_mentions_section_name(ticket: dict, trace: dict) -> bool:
    gold_sections = (ticket.get("gold") or {}).get("sections") or []
    out = (trace.get("output") or "").lower()
    for sid in gold_sections:
        title = HB.SECTION_TITLES.get(sid, sid).lower()
        if sid.lower() in out or title in out:
            return True
    return False


def _check_no_phone_or_email_invented(ticket: dict, trace: dict) -> bool:
    out = trace.get("output") or ""
    found_emails = set(_EMAIL_RE.findall(out))
    found_phones = set(_PHONE_RE.findall(out))
    return not (found_emails - _HANDBOOK_CONTACTS) and not (found_phones - _HANDBOOK_CONTACTS)


def _check_no_forbidden_promises(ticket: dict, trace: dict) -> bool:
    phrases = _load_forbidden_phrases()
    out = (trace.get("output") or "").lower()
    for p in phrases:
        if p.lower() in out:
            return False
    return True


def _check_mentions_all_answer_point_keywords(ticket: dict, trace: dict) -> bool:
    out = (trace.get("output") or "")
    out_lower = out.lower()
    for point in (ticket.get("gold") or {}).get("answer_points") or []:
        kws = _keyword_keywords(point)
        if not kws:
            continue
        if not any(kw in out_lower for kw in kws):
            return False
    return True


CHECKS: dict[str, callable] = {
    "nonempty": _check_nonempty,
    "max_words_150": _check_max_words_150,
    "mentions_section_name": _check_mentions_section_name,
    "no_phone_or_email_invented": _check_no_phone_or_email_invented,
    "no_forbidden_promises": _check_no_forbidden_promises,
    "mentions_all_answer_point_keywords": _check_mentions_all_answer_point_keywords,
}


# ============================================================================
# experiment drivers: triage, checks, similarity
# ============================================================================

def run_triage(run: str = "triage_v1", split: str = "test", client=None,
               project_root=None) -> Path:
    client = client or _llm.ollama
    labels = load_labels("triage_v1")
    gold_by_tid: dict[str, dict] = {r["ticket_id"]: r["raw"]["gold"] for r in labels}
    tickets = {t["id"]: t for t in load_tickets()}
    traces = {t["ticket_id"]: t for t in load_traces(run)}

    def _rows_for(split_name: str) -> list[dict]:
        out = []
        for tid, tr in traces.items():
            if tickets.get(tid, {}).get("split") != split_name:
                continue
            if tid not in gold_by_tid:
                continue
            o = tr.get("output") if isinstance(tr.get("output"), dict) else {}
            pred = {
                "category": o.get("category"),
                "priority": o.get("priority"),
                "needs_escalation": bool(o.get("needs_escalation")),
            }
            valid = (
                isinstance(tr.get("output"), dict)
                and all(k in tr["output"] for k in ("category", "priority", "needs_escalation"))
            )
            g = gold_by_tid[tid]
            out.append({
                "ticket_id": tid,
                "gold": g,
                "prediction": pred,
                "json_valid": valid,
            })
        return out

    def _metrics(rows: list[dict]) -> dict:
        n = len(rows)
        if n == 0:
            return {"n": 0}
        cat_acc = sum(1 for r in rows if r["gold"]["category"] == r["prediction"]["category"]) / n
        pri_acc = sum(1 for r in rows if r["gold"]["priority"] == r["prediction"]["priority"]) / n
        esc_acc = sum(
            1 for r in rows
            if bool(r["gold"]["needs_escalation"]) is bool(r["prediction"]["needs_escalation"])
        ) / n
        json_rate = sum(1 for r in rows if r["json_valid"]) / n
        all3_acc = sum(
            1 for r in rows
            if r["gold"]["category"] == r["prediction"]["category"]
            and r["gold"]["priority"] == r["prediction"]["priority"]
            and bool(r["gold"]["needs_escalation"]) is bool(r["prediction"]["needs_escalation"])
        ) / n

        # per-category precision / recall / F1 (macro)
        labels_set = sorted(
            {r["gold"]["category"] for r in rows}
            | {r["prediction"]["category"] for r in rows if r["prediction"]["category"]}
        )
        f1s: list[float] = []
        micro_tp = micro_fp = micro_fn = 0
        per_cat: dict[str, dict] = {}
        for lab in labels_set:
            tp = sum(1 for r in rows if r["gold"]["category"] == lab and r["prediction"]["category"] == lab)
            fp = sum(1 for r in rows if r["gold"]["category"] != lab and r["prediction"]["category"] == lab)
            fn = sum(1 for r in rows if r["gold"]["category"] == lab and r["prediction"]["category"] != lab)
            precision = tp / (tp + fp) if (tp + fp) else 0.0
            recall = tp / (tp + fn) if (tp + fn) else 0.0
            f1s.append(_f1(precision, recall))
            micro_tp += tp
            micro_fp += fp
            micro_fn += fn
            per_cat[lab] = {"precision": precision, "recall": recall, "f1": _f1(precision, recall),
                            "support": tp + fn}
        f1_macro = sum(f1s) / len(f1s)
        f1_micro = _f1(micro_tp / (micro_tp + micro_fp), micro_tp / (micro_tp + micro_fn))

        return {
            "f1_macro": f1_macro,
            "f1_micro": f1_micro,
            "category_accuracy": cat_acc,
            "priority_accuracy": pri_acc,
            "needs_escalation_accuracy": esc_acc,
            "category_priority_escalation_accuracy": all3_acc,
            "json_valid_rate": json_rate,
            "n": n,
            "_per_category": per_cat,
        }

    test_rows = _rows_for(split)
    dev_rows = _rows_for("dev")
    m_test = _metrics(test_rows)
    per_cat = m_test.pop("_per_category", {})
    m_dev = _metrics(dev_rows)
    per_cat_dev = m_dev.pop("_per_category", {})

    details = {
        "primary": "f1_macro",
        "notes": f"code-graded classification on {run}; test split n={len(test_rows)}",
        "dev": {k: m_dev[k] for k in m_dev if not k.startswith("_") and k != "n"},
        "per_category": per_cat,
        "per_category_dev": per_cat_dev,
        "category_order": CATEGORY_ORDER,
    }

    # save confusion matrix as PNG
    experiment = f"04_{run}"
    base = (project_root or settings.project_root) / "runs" / experiment
    base.mkdir(parents=True, exist_ok=True)
    _plot_confusion(test_rows, per_cat, base / "confusion.png", CATEGORY_ORDER)

    # predictions.jsonl
    predictions = [
        {
            "ticket_id": r["ticket_id"],
            "split": split,
            "pass": (
                r["gold"]["category"] == r["prediction"]["category"]
                and r["gold"]["priority"] == r["prediction"]["priority"]
                and bool(r["gold"]["needs_escalation"]) is bool(r["prediction"]["needs_escalation"])
            ),
            "prediction": r["prediction"],
            "gold": {k: v for k, v in r["gold"].items() if k in ("category", "priority", "needs_escalation")},
            "scenario": tickets.get(r["ticket_id"], {}).get("scenario"),
            "persona": tickets.get(r["ticket_id"], {}).get("persona"),
        }
        for r in test_rows
    ]

    path = R.write_metrics(
        experiment=experiment,
        chapter=4,
        n=len(test_rows),
        metrics={k: m_test[k] for k in m_test if k != "n"},
        ci={},
        llm_calls=_llm_usage(),
        seconds=0.0,
        details=details,
        predictions=predictions,
        config={
            "run": run,
            "split": split,
            "gold": "data/labels/triage_v1.jsonl",
            "client": type(client).__name__,
            "category_order": CATEGORY_ORDER,
        },
        project_root=project_root,
    )
    print(
        f"triage[{split}] n={len(test_rows)} "
        f"f1_macro={m_test['f1_macro']:.3f}  f1_micro={m_test['f1_micro']:.3f}  "
        f"cat_acc={m_test['category_accuracy']:.3f}  "
        f"pri_acc={m_test['priority_accuracy']:.3f}  "
        f"json={m_test['json_valid_rate']:.3f}  "
        f"-> {path}"
    )
    return path


def _plot_confusion(rows: list[dict], per_cat: dict, out_path: Path, order: list[str]) -> Path:
    # Keep the canonical CATEGORY_ORDER first, then append any classes actually
    # seen in this run that are not part of it (so synthetic / out-of-order
    # categories still get drawn instead of being silently dropped).
    seen = {r["gold"]["category"] for r in rows} | {r["prediction"]["category"] for r in rows}
    labels = [lab for lab in order if lab in seen] + sorted(seen - set(order))
    if len(labels) < 2:
        return out_path
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    for r in rows:
        g = r["gold"]["category"]
        p = r["prediction"]["category"]
        if g in labels and p in labels:
            matrix[labels.index(g), labels.index(p)] += 1
    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=110)
    im = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=max(matrix.max(), 1))
    ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(labels)), labels, fontsize=7)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = matrix[i, j]
            if v:
                color = "white" if v > matrix.max() * 0.55 else "black"
                ax.text(j, i, str(v), ha="center", va="center", color=color, fontsize=6)
    ax.set_xlabel("predicted category")
    ax.set_ylabel("gold category")
    ax.set_title("triage_v1 category confusion matrix (test)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight", dpi=110)
    plt.close(fig)
    return out_path


def run_checks(run: str = "answer_v1", split: str = "test", client=None,
               project_root=None) -> Path:
    """Run every deterministic check on the `run`'s traces and report per-check
    + overall pass rates. No LLM calls are made here (the SUT already made
    them upstream)."""
    client = client or _llm.ollama
    tickets = {t["id"]: t for t in load_tickets()}
    traces = [t for t in load_traces(run) if tickets.get(t["ticket_id"], {}).get("split") == split]

    # For each ticket, for each check, record pass/fail.
    per_check: dict[str, int] = {name: 0 for name in CHECKS}
    per_ticket = []
    for tr in traces:
        tid = tr["ticket_id"]
        ticket = tickets[tid]
        outcome = {name: bool(fn(ticket, tr)) for name, fn in CHECKS.items()}
        all_pass = all(outcome.values())
        per_ticket.append({
            "ticket_id": tid,
            "split": split,
            "pass": all_pass,
            "checks": outcome,
            "n_words": _word_count(tr.get("output") or ""),
            "scenario": ticket.get("scenario"),
            "persona": ticket.get("persona"),
        })
        for name, ok in outcome.items():
            per_check[name] += int(ok)

    n = len(per_ticket)
    all_pass = sum(1 for t in per_ticket if t["pass"])
    per_check_rates = {name: (v / n if n else 0.0) for name, v in per_check.items()}

    experiment = f"04_checks_{run}"
    path = R.write_metrics(
        experiment=experiment,
        chapter=4,
        n=n,
        metrics={
            "all_checks_pass": all_pass / n if n else 0.0,
            **{f"check_{name}": rate for name, rate in per_check_rates.items()},
        },
        ci={},
        llm_calls=_llm_usage(),
        seconds=0.0,
        details={
            "primary": "all_checks_pass",
            "notes": f"deterministic assertions ({len(CHECKS)}) on {run} test split",
            "per_check_pass_rate": per_check_rates,
            "fail_breakdown": _tally_failures(per_ticket),
        },
        predictions=per_ticket,
        config={
            "run": run,
            "split": split,
            "client": type(client).__name__,
            "checks": list(CHECKS),
            "forbidden_phrases": _load_forbidden_phrases(),
        },
        project_root=project_root,
    )
    print(
        f"checks[{split}] n={n} all={all_pass}/{n} "
        + "  ".join(f"{k}={v:.2f}" for k, v in per_check_rates.items())
        + f"  -> {path}"
    )
    return path


def _tally_failures(per_ticket: list[dict]) -> dict[str, int]:
    tally: dict[str, int] = {}
    for t in per_ticket:
        for name, ok in t["checks"].items():
            if not ok:
                tally[name] = tally.get(name, 0) + 1
    return dict(sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])))


def _gold_answer_concat(gold: dict) -> str:
    points = gold.get("answer_points") or []
    return " ".join(points)


def run_similarity(run: str = "answer_v1", split: str = "test", client=None,
                   project_root=None) -> Path:
    client = client or _llm.ollama
    calls_before = _llm_usage()
    tickets = {t["id"]: t for t in load_tickets()}
    labels = {r["ticket_id"]: r for r in load_labels("answer_v1")}
    ch03 = {
        tid: bool(labels[tid]["pass"])
        for tid in labels
        if tid in tickets and tickets[tid].get("split") == split
    }

    rows = []
    all_replies: list[str] = []
    all_gold: list[str] = []
    for tid, tr in ({t["ticket_id"]: t for t in load_traces(run)}.items()):
        if tickets.get(tid, {}).get("split") != split:
            continue
        reply = tr.get("output") or ""
        gold_points = _gold_answer_concat(tickets[tid].get("gold") or {})
        all_replies.append(reply)
        all_gold.append(gold_points)
        rows.append({
            "ticket_id": tid,
            "reply": reply,
            "gold_concat": gold_points,
        })

    n = len(rows)
    rouge_f_scores: list[float] = []
    rouge_p_scores: list[float] = []
    rouge_r_scores: list[float] = []
    embed_scores: list[float] = []

    for row in rows:
        rl = rouge_l(row["gold_concat"], row["reply"])
        rouge_f_scores.append(rl["f"])
        rouge_p_scores.append(rl["precision"])
        rouge_r_scores.append(rl["recall"])

    if n:
        # Both sides via embed_documents: consistent prefix (nomic document-side)
        # keeps the cosine symmetric with respect to the pair.
        doc_vecs = client.embed_documents(all_gold, model=settings.embed_model)
        reply_vecs = client.embed_documents(all_replies, model=settings.embed_model)
        for a, b in zip(reply_vecs, doc_vecs):
            embed_scores.append(_cosine(a, b))

    rouge_f_mean, rouge_f_sd = _mean_sd(rouge_f_scores)
    emb_mean, emb_sd = _mean_sd(embed_scores)

    # Correlation/AUC of each similarity vs ch03 pass label
    labels_seq = [ch03[r["ticket_id"]] for r in rows]
    labels_int = [1 if b else 0 for b in labels_seq]
    has_both = len(set(labels_int)) == 2
    auroc_rouge = _auroc(rouge_f_scores, labels_int) if has_both else float("nan")
    auroc_embed = _auroc(embed_scores, labels_int) if has_both else float("nan")

    corr_rouge = _correlation(rouge_f_scores, labels_int) if n > 1 else 0.0
    corr_embed = _correlation(embed_scores, labels_int) if n > 1 else 0.0

    predictions = []
    for i, r in enumerate(rows):
        passed = ch03.get(r["ticket_id"])
        predictions.append({
            "ticket_id": r["ticket_id"],
            "split": split,
            "pass": bool(passed),
            "rouge_f": round(rouge_f_scores[i], 4),
            "rouge_p": round(rouge_p_scores[i], 4),
            "rouge_r": round(rouge_r_scores[i], 4),
            "embed_cosine": round(embed_scores[i], 4) if i < len(embed_scores) else None,
            "scenario": tickets[r["ticket_id"]].get("scenario"),
            "persona": tickets[r["ticket_id"]].get("persona"),
        })

    n_embed = len(embed_scores)
    experiment = f"04_similarity_{run}"
    path = R.write_metrics(
        experiment=experiment,
        chapter=4,
        n=n,
        metrics={
            "auroc_embed_vs_label": auroc_embed,
            "auroc_rouge_vs_label": auroc_rouge,
            "rouge_f_mean": rouge_f_mean,
            "rouge_f_sd": rouge_f_sd,
            "embed_cosine_mean": emb_mean,
            "embed_cosine_sd": emb_sd,
            "corr_rouge_vs_label": corr_rouge,
            "corr_embed_vs_label": corr_embed,
        },
        ci={},
        llm_calls=_llm_usage() - calls_before,
        seconds=0.0,
        details={
            "primary": "auroc_embed_vs_label",
            "notes": "ROUGE-L + embedding cosine; correlation/AUC with ch-03 pass label",
            "n_embed_calls": n_embed,
            "n_positive_labels": sum(labels_int),
        },
        predictions=predictions,
        config={
            "run": run,
            "split": split,
            "client": type(client).__name__,
            "embed_model": settings.embed_model,
        },
        project_root=project_root,
    )
    print(
        f"similarity[{split}] n={n} "
        f"rougeF={rouge_f_mean:.3f}±{rouge_f_sd:.3f} "
        f"embed={emb_mean:.3f}±{emb_sd:.3f} "
        f"AUC(rouge)={auroc_rouge:.3f} AUC(embed)={auroc_embed:.3f}  ->  {path}"
    )
    return path


def run_all(client=None, project_root=None) -> tuple[Path, Path, Path, Path]:
    triage = run_triage("triage_v1", "test", client=client, project_root=project_root)
    checks = run_checks("answer_v1", "test", client=client, project_root=project_root)
    similarity = run_similarity("answer_v1", "test", client=client, project_root=project_root)
    results = R.build(project_root)
    return triage, checks, similarity, results


# ============================================================================
# Typer CLI
# ============================================================================

app = typer.Typer(add_completion=False)


@app.command(name="triage")
def triage_cmd(
    run: str = typer.Option("triage_v1", help="SUT run id"),
    split: str = typer.Option("test", help="split name: test | dev"),
) -> None:
    """Code-graded classification eval on triage."""
    run_triage(run, split)


@app.command(name="checks")
def checks_cmd(
    run: str = typer.Option("answer_v1", help="SUT run id"),
    split: str = typer.Option("test", help="split name: test | dev"),
) -> None:
    """Deterministic (IFEval-style) assertions on answer replies."""
    run_checks(run, split)


@app.command(name="similarity")
def similarity_cmd(
    run: str = typer.Option("answer_v1", help="SUT run id"),
    split: str = typer.Option("test", help="split name: test | dev"),
) -> None:
    """ROUGE-L + embedding cosine vs gold answer points."""
    run_similarity(run, split)


@app.command(name="all")
def all_cmd() -> None:
    """Run all three code-graded experiments and rebuild `runs/results.md`."""
    run_all()


if __name__ == "__main__":
    app()
