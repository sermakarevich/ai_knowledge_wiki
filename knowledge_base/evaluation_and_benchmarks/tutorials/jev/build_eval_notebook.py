"""Generate jev_eval_tutorial.ipynb. Run `just build-eval` (or `uv run python build_eval_notebook.py`)."""

from __future__ import annotations

import nbformat as nbf

cells: list = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text: str) -> None:
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


# --------------------------------------------------------------------------- 0
md(r"""
# Testing Jev: accuracy and sensitivity

`jev_tutorial.ipynb` shows how to *use* Jev. This notebook shows how to **test** it, before you
let it gate anything real.

Two questions, kept deliberately separate because they fail in different ways:

- **Accuracy** — when the correct answer is objectively known, does Jev get it right, and is its
  `confidence` honest (a reliability diagram, a Brier score)? This needs *ground truth*.
- **Sensitivity** — does Jev's answer move the *right* amount when the input changes? Two
  sub-questions with opposite desired behaviour:
  - **Invariance**: wording, formatting, key order, or irrelevant filler that does not change the
    substance of the state should *not* change the answer. High sensitivity here is a bug.
  - **Discrimination**: a real change in the underlying thing being judged (more anger markers,
    a ticket that is 80% technical instead of 20%) should move the score or the probability in the
    right direction, ideally proportionally. Low sensitivity here is a bug.

A model can fail on any one of these independently: a judge that is 95% accurate but flips its
answer when you reorder a JSON dict is not safe to gate a workflow with, and a judge whose
confidence is uncorrelated with correctness is not safe to threshold on even if its top-1 answers
are usually right.

## Why not just trust the docs

Public reviews after Jev's September 2026 launch converge on the same gap. TypeSafe's own
711-case dashboard reports 67.8% aggregate accuracy, but the reference labels are an average of
two other LLMs, not human ground truth, so the number describes agreement, not correctness. The
[independent write-up at pearpages.com](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)
put it plainly: *"the documentation contains no calibration curves, no Brier scores and no
reliability diagrams"*, and sensitivity to input changes is *"completely unknown"* outside
TypeSafe's own four workflows. A hands-on test at
[paddo.dev](https://paddo.dev/blog/thirty-cent-judge) ran Jev over 9,081 real low-confidence
product-matching pairs and manually checked 50 verdicts (48 held up) but explicitly stopped short
of a calibration claim, for the same reason: one small hand-checked sample cannot establish that a
0.9 is right 90% of the time. This notebook builds the pieces those write-ups say are missing —
using **synthetic tasks with a computable ground truth**, so accuracy and calibration can be
measured at a sample size a human cannot label by hand, plus controlled perturbations for
sensitivity, all runnable against your own data instead of TypeSafe's four workflows.

Notebook map:
1. Setup and a **noise floor**: how much does Jev's answer vary on the exact same input?
2. **Accuracy** on four synthetic tasks with a computable correct answer (Choice, Score, Noul).
3. **Calibration**: a reliability diagram and Brier / expected-calibration-error scores.
4. **Invariance**: perturbations that should not change the answer (paraphrase, key order, filler).
5. **Discrimination**: controlled sweeps that should change the answer, and by how much.
6. A one-table scorecard, and what to do with a model that fails part of it.
""")

# --------------------------------------------------------------------------- 1 setup
md(r"""
## 1. Setup

Same client pattern as `jev_tutorial.ipynb`. Everything below is cached to `eval_cache/`
(gitignored) keyed by a hash of the request, so re-running the notebook after a code edit does not
re-call the API for requests you already have an answer for. Delete `eval_cache/` to force a
fresh run.
""")
code(r"""
import asyncio
import hashlib
import json
import os
import random
from pathlib import Path

import pandas as pd
from typesafe_sdk import (
    AsyncTypeSafeClient,
    Choice,
    Noul,
    RetryPolicy,
    Score,
    TypeSafeClient,
)

assert os.environ.get("TYPESAFE_API_KEY"), "Set TYPESAFE_API_KEY in your shell before starting Jupyter"

pd.set_option("display.max_colwidth", 100)
pd.set_option("display.width", 160)

RNG = random.Random(20260917)  # fixed seed: perturbation wording etc. should be reproducible
CACHE = Path("eval_cache")
CACHE.mkdir(exist_ok=True)

USAGE = {"input_tokens": 0, "output_tokens": 0, "requests": 0, "cache_hits": 0}


def _key(state, questions_repr: str) -> str:
    blob = json.dumps({"state": state, "q": questions_repr}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:24]


def answers_to_dict(response) -> dict:
    out = {}
    for name, ans in response.answers.items():
        if hasattr(ans, "choice"):
            out[name] = {"type": "choice", "choice": ans.choice, "confidence": ans.confidence, "probabilities": dict(ans.probabilities)}
        elif hasattr(ans, "score"):
            out[name] = {"type": "score", "score": ans.score, "confidence": ans.confidence, "probabilities": dict(ans.probabilities)}
        else:
            out[name] = {"type": "noul", "noul": ans.noul}
    return out


client = TypeSafeClient(retry=RetryPolicy(max_retries=4, backoff_max=2.0, timeout=60.0))


def ask(state, questions: dict, *, cache_key: str | None = None) -> dict:
    # Sync call with disk caching. cache_key lets two textually-identical requests
    # (e.g. a repeat-call test) be cached under different keys on purpose.
    key = cache_key or _key(state, repr(sorted(questions.items(), key=str)))
    path = CACHE / f"{key}.json"
    if path.exists():
        USAGE["cache_hits"] += 1
        return json.loads(path.read_text())
    response = client.system_one(state, questions)
    USAGE["input_tokens"] += response.usage.input_tokens
    USAGE["output_tokens"] += response.usage.output_tokens
    USAGE["requests"] += 1
    result = answers_to_dict(response)
    path.write_text(json.dumps(result))
    return result


async def ask_many(items: list[tuple[str, object, dict]], concurrency: int = 8) -> dict:
    # items: list of (cache_key, state, questions). Runs uncached ones concurrently.
    sem = asyncio.Semaphore(concurrency)
    out: dict[str, dict] = {}
    todo = []
    for key, state, questions in items:
        path = CACHE / f"{key}.json"
        if path.exists():
            USAGE["cache_hits"] += 1
            out[key] = json.loads(path.read_text())
        else:
            todo.append((key, state, questions))

    async with AsyncTypeSafeClient(retry=RetryPolicy(max_retries=6, backoff_max=5.0, timeout=90.0)) as ac:

        async def one(key, state, questions):
            async with sem:
                response = await ac.system_one(state, questions)
            USAGE["input_tokens"] += response.usage.input_tokens
            USAGE["output_tokens"] += response.usage.output_tokens
            USAGE["requests"] += 1
            result = answers_to_dict(response)
            (CACHE / f"{key}.json").write_text(json.dumps(result))
            return key, result

        for key, result in await asyncio.gather(*(one(*t) for t in todo)):
            out[key] = result
    return out
""")

# --------------------------------------------------------------------------- 2 noise floor
md(r"""
## 2. Noise floor: how much does an identical request vary?

Before calling anything "sensitive to X", we need to know how much Jev's answer moves on **zero**
change to the input. If two identical calls already disagree by 0.05 in probability, a perturbation
test that finds a 0.03 shift found nothing. Each identical call is cached under its own key
(`rep_00`, `rep_01`, ...) so the client does not just return the same cached answer eight times.
""")
code(r"""
NOISE_REPEATS = 8

noise_examples = {
    "choice": (
        "The customer writes: 'I was charged twice for the same order, please refund one of them.'",
        {"department": Choice(instructions="Which team should handle this?", criteria={"billing": None, "technical": None, "sales": None})},
    ),
    "score": (
        "The customer writes: 'This is the third time this week your app has crashed on me. Fix it.'",
        {"frustration": Score(instructions="How frustrated is the customer?", criteria=["calm", "annoyed", "angry"])},
    ),
    "noul": (
        "The customer writes: 'Can I get a refund for my last order?'",
        {"wants_refund": Noul(instructions="Is the customer asking for a refund?")},
    ),
}

noise_rows = []
for kind, (state, questions) in noise_examples.items():
    reps = [ask(state, questions, cache_key=f"noise_{kind}_{i:02d}") for i in range(NOISE_REPEATS)]
    name = next(iter(questions))
    if kind == "choice":
        choices = [r[name]["choice"] for r in reps]
        probs = pd.DataFrame([r[name]["probabilities"] for r in reps])
        noise_rows.append({"kind": kind, "flip_rate": 1 - choices.count(max(set(choices), key=choices.count)) / len(choices),
                            "max_prob_std": round(probs.std().max(), 4), "confidences": [round(r[name]["confidence"], 3) for r in reps]})
    elif kind == "score":
        scores = [r[name]["score"] for r in reps]
        noise_rows.append({"kind": kind, "flip_rate": None, "max_prob_std": round(pd.Series(scores).std(), 4),
                            "confidences": [round(r[name]["confidence"], 3) for r in reps]})
    else:
        nouls = [r[name]["noul"] for r in reps]
        noise_rows.append({"kind": kind, "flip_rate": None, "max_prob_std": round(pd.Series(nouls).std(), 4), "confidences": None})

NOISE_FLOOR = pd.DataFrame(noise_rows).set_index("kind")
NOISE_FLOOR
""")
md(r"""
`max_prob_std` (or the score/noul std for the other two rows) is the **noise floor**: the amount
of jitter present with no change to the input at all. Later sections compare perturbation-induced
drift against this number, not against zero.
""")

# --------------------------------------------------------------------------- 3 accuracy
md(r"""
## 3. Accuracy on tasks with a computable ground truth

Subjective tasks ("how severe is this bug") have no ground truth to check against, so they cannot
measure accuracy — only sensitivity (section 5). To measure accuracy we need tasks where the
*correct* answer is a fact we can compute, not an opinion. Four synthetic generators, each large
enough (n=40 by default) to compute a real accuracy percentage and a Brier score, not just "8 out
of 10 looked right":

- **3.1 Numeric comparison (Noul)** — two random numbers stated in text; ground truth is `a > b`.
- **3.2 Unambiguous keyword routing (Choice)** — a ticket template that names its own department
  outright, so any competent reader gets it right; this is a floor test, not a hard case.
- **3.3 Rule-following (Score)** — the *rule* for scoring is stated explicitly in the instructions
  ("0 if fewer than 3 failed logins, 1 if 3-6, 2 if more than 6") and the state gives an exact
  count; this isolates instruction-following from any judgment call.
- **3.4 Negation trap (Noul)** — matched affirmative/negated statement pairs, to check Jev does not
  invert on "does NOT" the way some LLMs do.
""")
code(r"""
N_PER_TASK = 40


def brier_binary(p_yes: list[float], y_true: list[bool]) -> float:
    return sum((p - int(t)) ** 2 for p, t in zip(p_yes, y_true)) / len(y_true)
""")

md(r"""
### 3.1 Numeric comparison
""")
code(r"""
pairs = [(RNG.randint(1, 999), RNG.randint(1, 999)) for _ in range(N_PER_TASK)]
pairs = [(a, b) for a, b in pairs if a != b]  # ties have no unambiguous answer

items = [
    (f"acc_numeric_{i:03d}", f"Number A is {a}. Number B is {b}.",
     {"a_bigger": Noul(instructions="Is Number A bigger than Number B?")})
    for i, (a, b) in enumerate(pairs)
]
numeric_results = await ask_many(items)

rows = []
for (key, _, _), (a, b) in zip(items, pairs):
    p = numeric_results[key]["a_bigger"]["noul"]
    truth = a > b
    rows.append({"a": a, "b": b, "p_a_bigger": p, "predicted": p > 0.5, "truth": truth, "correct": (p > 0.5) == truth})

numeric_df = pd.DataFrame(rows)
numeric_acc = numeric_df["correct"].mean()
numeric_brier = brier_binary(numeric_df["p_a_bigger"].tolist(), numeric_df["truth"].tolist())
print(f"accuracy: {numeric_acc:.1%}   Brier score: {numeric_brier:.4f} (0 = perfect, 0.25 = coin flip)")
numeric_df[~numeric_df["correct"]]
""")

md(r"""
### 3.2 Unambiguous keyword routing
""")
code(r"""
routing_templates = {
    "billing": "This is a billing question: {detail}",
    "technical": "This is a technical bug report: {detail}",
    "sales": "This is a pre-sales pricing question: {detail}",
}
routing_details = {
    "billing": [
        "the invoice for last month looks wrong", "I was charged the wrong amount",
        "my subscription renewed twice", "I need a corrected receipt",
    ],
    "technical": [
        "the app crashes on startup", "the export button does nothing",
        "the login page shows a 500 error", "the API returns malformed JSON",
    ],
    "sales": [
        "what does the enterprise plan cost", "do you offer a student discount",
        "is there a volume discount for 50 seats", "can I get a quote for our team",
    ],
}
# Each detail is only ever combined with its own department's template, so the
# stated department and the detail's actual topic never contradict each other.
routing_cases = [(dept, routing_templates[dept].format(detail=d)) for dept, details in routing_details.items() for d in details]
RNG.shuffle(routing_cases)
routing_cases = routing_cases[:N_PER_TASK]

items = [
    (f"acc_routing_{i:03d}", text,
     {"department": Choice(instructions="Which team should handle this ticket?", criteria={"billing": None, "technical": None, "sales": None})})
    for i, (_, text) in enumerate(routing_cases)
]
routing_results = await ask_many(items)

rows = []
for (key, text, _), (truth, _) in zip(items, routing_cases):
    ans = routing_results[key]["department"]
    rows.append({"text": text, "predicted": ans["choice"], "truth": truth, "confidence": ans["confidence"], "correct": ans["choice"] == truth})

routing_df = pd.DataFrame(rows)
routing_acc = routing_df["correct"].mean()
print(f"accuracy: {routing_acc:.1%}")
pd.crosstab(routing_df["truth"], routing_df["predicted"], margins=True)
""")

md(r"""
### 3.3 Rule-following
""")
code(r"""
buckets = ["low (fewer than 3 failed logins)", "medium (3 to 6 failed logins)", "high (more than 6 failed logins)"]


def true_bucket(n: int) -> int:
    return 0 if n < 3 else (1 if n <= 6 else 2)


counts = [RNG.randint(0, 12) for _ in range(N_PER_TASK)]
items = [
    (f"acc_rule_{i:03d}", f"The account had {n} failed login attempts in the last hour.",
     {"risk": Score(
         instructions="Rate the account's risk level using exactly this rule: fewer than 3 failed logins is low, "
                      "3 to 6 is medium, more than 6 is high. Apply the rule to the exact count given, do not use your own judgment.",
         criteria=buckets,
     )})
    for i, n in enumerate(counts)
]
rule_results = await ask_many(items)

rows = []
for (key, _, _), n in zip(items, counts):
    ans = rule_results[key]["risk"]
    predicted_bucket = round(ans["score"])
    rows.append({"failed_logins": n, "score": ans["score"], "predicted_bucket": predicted_bucket,
                 "true_bucket": true_bucket(n), "correct": predicted_bucket == true_bucket(n),
                 "abs_error": abs(ans["score"] - true_bucket(n))})

rule_df = pd.DataFrame(rows).sort_values("failed_logins")
rule_acc = rule_df["correct"].mean()
print(f"bucket accuracy: {rule_acc:.1%}   mean absolute error: {rule_df['abs_error'].mean():.3f}")
rule_df[~rule_df["correct"]]
""")

md(r"""
### 3.4 Negation trap
""")
code(r"""
negation_pairs = [
    ("The customer says they do want a refund for this order.", True),
    ("The customer says they do NOT want a refund for this order.", False),
    ("The ticket confirms the bug is reproducible.", True),
    ("The ticket confirms the bug is NOT reproducible.", False),
    ("The user explicitly agrees to the new terms.", True),
    ("The user explicitly does not agree to the new terms.", False),
    ("The payment went through successfully.", True),
    ("The payment did not go through.", False),
    ("The manager approved the request.", True),
    ("The manager did not approve the request.", False),
    ("The shipment has arrived at the warehouse.", True),
    ("The shipment has not yet arrived at the warehouse.", False),
] * (N_PER_TASK // 12 + 1)
negation_pairs = negation_pairs[:N_PER_TASK]

items = [
    (f"acc_negation_{i:03d}", text,
     {"holds": Noul(instructions="The state is one sentence describing something that either happened/was approved/holds, "
                                  "or that did NOT happen/was NOT approved/does not hold. Answer yes only if the sentence "
                                  "affirms it. Answer no if the sentence contains a negation such as 'not' or 'NOT'.")})
    for i, (text, _) in enumerate(negation_pairs)
]
negation_results = await ask_many(items)

rows = []
for (key, text, _), (_, truth) in zip(items, negation_pairs):
    p = negation_results[key]["holds"]["noul"]
    rows.append({"text": text, "p_true": p, "predicted": p > 0.5, "truth": truth, "correct": (p > 0.5) == truth})

negation_df = pd.DataFrame(rows)
negation_acc = negation_df["correct"].mean()
negation_brier = brier_binary(negation_df["p_true"].tolist(), negation_df["truth"].tolist())
print(f"accuracy: {negation_acc:.1%}   Brier score: {negation_brier:.4f}")
negation_df[~negation_df["correct"]]
""")

md(r"""
### Accuracy summary
""")
code(r"""
accuracy_summary = pd.DataFrame([
    {"task": "3.1 numeric comparison (Noul)", "n": len(numeric_df), "accuracy": numeric_acc, "brier": numeric_brier},
    {"task": "3.2 keyword routing (Choice)", "n": len(routing_df), "accuracy": routing_acc, "brier": None},
    {"task": "3.3 rule-following (Score, bucket)", "n": len(rule_df), "accuracy": rule_acc, "brier": None},
    {"task": "3.4 negation trap (Noul)", "n": len(negation_df), "accuracy": negation_acc, "brier": negation_brier},
]).set_index("task")
accuracy_summary
""")
md(r"""
These are all easy, unambiguous tasks by design (3.2 literally names the answer, 3.3 hands Jev the
rule). Anything below roughly 95% here is a floor problem, not a hard-case problem: it means Jev is
failing at instruction-following or basic entailment on cases with no genuine ambiguity, which is a
different and more serious finding than "confidence is a bit off on hard cases" (section 4).
""")

# --------------------------------------------------------------------------- 4 calibration
md(r"""
## 4. Calibration: is confidence honest?

Pool every (confidence, correctness) pair from the tasks in section 3 that carry a `confidence`
field (Choice and Score; Noul has none, so 3.1/3.4 are excluded here even though they have ground
truth). Bin by confidence and compare the *predicted* confidence against the *empirical* accuracy
in that bin. A well-calibrated judge sits close to the diagonal.
""")
code(r"""
calib_rows = (
    [{"confidence": c, "correct": bool(v)} for c, v in zip(routing_df["confidence"], routing_df["correct"])]
    + [{"confidence": rule_results[k]["risk"]["confidence"], "correct": bool(c)} for k, c in zip([f"acc_rule_{i:03d}" for i in range(len(rule_df))], rule_df["correct"])]
)
calib_df = pd.DataFrame(calib_rows)
calib_df["bin"] = pd.cut(calib_df["confidence"], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)

reliability = calib_df.groupby("bin", observed=True).agg(n=("correct", "size"), mean_confidence=("confidence", "mean"), empirical_accuracy=("correct", "mean"))
reliability["gap"] = (reliability["mean_confidence"] - reliability["empirical_accuracy"]).round(3)
ece = (reliability["n"] / reliability["n"].sum() * reliability["gap"].abs()).sum()
print(f"Expected Calibration Error (weighted mean |confidence - accuracy| across bins): {ece:.3f}")
reliability
""")
md(r"""
Read the `gap` column, not just the ECE headline: a positive gap means Jev is **overconfident**
in that bin (states a higher number than it earns), a negative gap means it is **underconfident**.
Overconfidence is the more dangerous direction for a confidence-gated pipeline, since it is exactly
the case where you would act automatically on a wrong answer. With ~80 pooled points this is a
coarse read, not a production calibration audit — widen `N_PER_TASK` in section 3 for a tighter
one, since ECE's own uncertainty shrinks with more samples per bin.
""")

# --------------------------------------------------------------------------- 5 invariance
md(r"""
## 5. Invariance: things that should NOT change the answer

Take one clear-cut base case per primitive and generate perturbations that preserve the meaning of
the state: paraphrase, add irrelevant preamble/suffix text, reorder the `Choice` criteria dict,
change casing, and insert an unrelated distractor sentence. None of these should move the answer
by more than the noise floor from section 2.
""")
code(r"""
base_ticket = "I was charged twice for the same order last week. Please refund the extra charge."
base_questions_ordered = {"department": Choice(instructions="Which team should handle this ticket?", criteria={"billing": None, "technical": None, "sales": None})}
base_questions_reordered = {"department": Choice(instructions="Which team should handle this ticket?", criteria={"sales": None, "technical": None, "billing": None})}

perturbations = {
    "original": base_ticket,
    "paraphrase_1": "Your system billed my card twice for one purchase last week; I'd like the duplicate amount refunded.",
    "paraphrase_2": "Duplicate charge on my last order. Can you refund the second one?",
    "irrelevant_preamble": "Hi team, hope you're having a good week. " + base_ticket,
    "irrelevant_suffix": base_ticket + " By the way, do you have an app for Android too?",
    "casing_and_punctuation": base_ticket.upper().replace(".", "!!"),
    "distractor_sentence": base_ticket + " Also, I noticed your logo changed recently, looks nice.",
}

items = [(f"inv_{name}", text, base_questions_ordered) for name, text in perturbations.items()]
items.append(("inv_reordered_criteria", base_ticket, base_questions_reordered))
inv_results = await ask_many(items)

rows = []
for name, text in perturbations.items():
    ans = inv_results[f"inv_{name}"]["department"]
    rows.append({"perturbation": name, "choice": ans["choice"], "p_billing": round(ans["probabilities"].get("billing", 0), 3), "confidence": round(ans["confidence"], 3)})
ans = inv_results["inv_reordered_criteria"]["department"]
rows.append({"perturbation": "reordered_criteria_dict", "choice": ans["choice"], "p_billing": round(ans["probabilities"].get("billing", 0), 3), "confidence": round(ans["confidence"], 3)})

inv_df = pd.DataFrame(rows).set_index("perturbation")
baseline_p = inv_df.loc["original", "p_billing"]
inv_df["drift_from_original"] = (inv_df["p_billing"] - baseline_p).round(3)
inv_df["flip"] = inv_df["choice"] != inv_df.loc["original", "choice"]
noise_floor_choice = NOISE_FLOOR.loc["choice", "max_prob_std"]
inv_df["exceeds_noise_floor"] = inv_df["drift_from_original"].abs() > 2 * noise_floor_choice
inv_df
""")
md(r"""
`exceeds_noise_floor` flags drift bigger than twice the repeat-call jitter measured in section 2 —
a rough two-sigma-ish bar, not a statistical test. Any `flip == True` row is a harder finding than
a large `p_billing` drift with no flip: the decision itself changed on a meaning-preserving edit.

Caveat worth noticing in the table above: if the base example already sits at `p_billing = 1.0`,
it is at a ceiling and a real perturbation-induced shift has nowhere to show up — an invariance
test needs a base case Jev is not already maximally sure about, or it can only prove "still
certain", not "still stable". Swap `base_ticket` for a harder, less clear-cut example if this
table comes back all zeros.
""")

# --------------------------------------------------------------------------- 6 discrimination
md(r"""
## 6. Discrimination: things that SHOULD change the answer, and how much

### 6.1 A controlled monotonic dial

Insert a known number of anger markers into an otherwise fixed template and ask for a frustration
`Score`. If Jev is actually reading the signal (not just pattern-matching on topic), the score
should rise monotonically with the marker count. We repeat each level a few times to average out
the noise floor from section 2, then compute the Spearman rank correlation between marker count and
mean score.
""")
code(r"""
ANGER_MARKERS = ["!", " This is unacceptable.", " I am furious.", " Fix this NOW.", " I want a manager."]
LEVELS = [0, 1, 2, 3, 4, 5]
REPEATS_PER_LEVEL = 3


def build_text(n_markers: int) -> str:
    text = "The app crashed while I was checking out"
    for i in range(n_markers):
        text += ANGER_MARKERS[i % len(ANGER_MARKERS)]
    return text


items = [
    (f"disc_anger_{level}_{rep:02d}", build_text(level), {"frustration": Score(instructions="How frustrated is the customer?", criteria=["calm", "annoyed", "angry"])})
    for level in LEVELS for rep in range(REPEATS_PER_LEVEL)
]
anger_results = await ask_many(items)

rows = [{"level": level, "rep": rep, "score": anger_results[f"disc_anger_{level}_{rep:02d}"]["frustration"]["score"]} for level in LEVELS for rep in range(REPEATS_PER_LEVEL)]
anger_df = pd.DataFrame(rows)
anger_summary = anger_df.groupby("level")["score"].agg(["mean", "std"])
# Spearman correlation without a scipy dependency: Pearson correlation of the ranks.
spearman = anger_df["level"].rank().corr(anger_df["score"].rank())
print(f"Spearman correlation between anger-marker count and frustration score: {spearman:.3f}")
anger_summary
""")

md(r"""
### 6.2 A decision-boundary sweep

Mix a purely-billing sentence and a purely-technical sentence in varying proportions, and watch
`p(billing)` move as the mixture shifts. This checks two things at once: whether the probability
moves in the right direction as the true mixture shifts, and whether `confidence` drops near the
point where the two are evenly mixed, which is exactly where it should.
""")
code(r"""
billing_sentence = "I was charged twice for my last order and want the extra charge refunded."
technical_sentence = "The app has been crashing every time I try to check out for the last three days."

mix_ratios = [0.0, 0.25, 0.5, 0.75, 1.0]  # fraction technical


def build_mix(frac_technical: float) -> str:
    if frac_technical <= 0:
        return billing_sentence
    if frac_technical >= 1:
        return technical_sentence
    if frac_technical <= 0.5:
        return billing_sentence + " " + technical_sentence.split(".")[0] + " too, occasionally."
    return technical_sentence + " " + billing_sentence.split(".")[0] + " too, occasionally."


items = [
    (f"disc_mix_{int(r*100):03d}", build_mix(r), {"department": Choice(instructions="Which team should handle this?", criteria={"billing": None, "technical": None})})
    for r in mix_ratios
]
mix_results = await ask_many(items)

rows = []
for r in mix_ratios:
    ans = mix_results[f"disc_mix_{int(r*100):03d}"]["department"]
    rows.append({"frac_technical": r, "p_technical": round(ans["probabilities"].get("technical", 0), 3), "confidence": round(ans["confidence"], 3), "choice": ans["choice"]})
mix_df = pd.DataFrame(rows)
mix_df
""")
md(r"""
Read this as a curve, not a table: `p_technical` should climb roughly monotonically left to right,
and `confidence` should be lowest around `frac_technical = 0.5` (where the state genuinely is
ambiguous) and higher at both ends (where it is not).
""")

md(r"""
### 6.3 Distractor flood: does the signal survive padding?

Take one clear-cut case from section 3.2 and bury the actual question-relevant sentence inside a
growing amount of unrelated filler text, up to a meaningful fraction of the ~32k-token request
budget. `pearpages.com`'s review and TypeSafe's own docs both flag this as a known weak point:
accuracy degrading as the state fills with content unrelated to the decision. This checks whether
that shows up on a simple case.
""")
code(r"""
FILLER_SENTENCE = "Our quarterly newsletter also covers unrelated product updates, community events, and upcoming webinars. "
signal_sentence = "This is a billing question: I was charged the wrong amount on my last invoice."
filler_char_counts = [0, 2_000, 8_000, 20_000]


def build_padded(n_chars: int) -> str:
    filler = (FILLER_SENTENCE * (n_chars // len(FILLER_SENTENCE) + 1))[:n_chars]
    half = len(filler) // 2
    return filler[:half] + " " + signal_sentence + " " + filler[half:]


items = [
    (f"disc_flood_{n}", build_padded(n), {"department": Choice(instructions="Which team should handle this?", criteria={"billing": None, "technical": None, "sales": None})})
    for n in filler_char_counts
]
flood_results = await ask_many(items)

rows = []
for n in filler_char_counts:
    ans = flood_results[f"disc_flood_{n}"]["department"]
    rows.append({"filler_chars": n, "choice": ans["choice"], "correct": ans["choice"] == "billing", "confidence": round(ans["confidence"], 3)})
flood_df = pd.DataFrame(rows)
flood_df
""")

md(r"""
### 6.4 Opinion anchoring: does a general recommendation drift with team sentiment?

The question below is phrased as a general best-practice recommendation, not a question about any
specific team: *"Would you recommend using type annotations in Python code?"*. If Jev were purely
answering the general question, the state's sentiment shouldn't move the answer much. But the state
does hand it five framings of the same team's experience along a positive-to-negative gradient
(positive, mildly positive, neutral, mildly negative, negative), so some drift is a legitimate,
defensible response too (the state is, after all, relevant context).
There is no computable ground truth here, unlike section 3: this is a probe, not a pass/fail check.
It exists because this is the exact case tested by hand while drafting this notebook, with visibly
different confidence values on repeat manual runs.
""")
code(r"""
anchor_question = "Would you recommend using type annotations in Python code?"
anchor_states = {
    "positive": ("Our team loves type annotations. We have many newcomers, and type annotations "
                 "simplify the learning curve and lower the entry barrier for people new to the codebase."),
    "mild_positive": ("Our team generally likes type annotations. They take a bit of extra time to write, "
                       "but most people feel they're worth it, especially for newcomers."),
    "neutral": ("Our team does not have a strong opinion on type annotations. Some engineers use "
                "them, some don't, and it has not come up as a topic worth discussing."),
    "mild_negative": ("Our team is somewhat lukewarm on type annotations. A few engineers find them "
                       "helpful, but others feel they add clutter and slow down quick prototyping."),
    "negative": ("All members of the team dislike type annotations, as they trigger more discussion "
                 "about the type annotations themselves than about the actual code."),
}

items = [
    (f"anchor_{sentiment}", state, {"recommend": Choice(instructions=anchor_question, criteria={"Yes": None, "No": None, "Unknown": None})})
    for sentiment, state in anchor_states.items()
]
anchor_results = await ask_many(items)

rows = []
for sentiment, state in anchor_states.items():
    ans = anchor_results[f"anchor_{sentiment}"]["recommend"]
    rows.append({"state_sentiment": sentiment, "state": state, "answer": ans["choice"], "confidence": round(ans["confidence"], 3), "probabilities": ans["probabilities"]})
anchor_df = pd.DataFrame(rows)
anchor_df
""")
md(r"""
Copy/paste block for a post — same three states, formatted as question/answer pairs:
""")
code(r"""
print(f"Q: {anchor_question}\n")
for sentiment, state in anchor_states.items():
    ans = anchor_results[f"anchor_{sentiment}"]["recommend"]
    print(f"State ({sentiment}): {state}")
    print(f"Jev: {ans['choice']} (confidence {ans['confidence']:.2f})\n")
""")

# --------------------------------------------------------------------------- 7 scorecard
md(r"""
## 7. Scorecard

One table combining everything above. This is the shape of report the public reviews said Jev's
own documentation was missing.
""")
code(r"""
scorecard = pd.DataFrame([
    {"check": "accuracy: numeric comparison", "result": f"{numeric_acc:.1%}", "pass": numeric_acc >= 0.95},
    {"check": "accuracy: keyword routing", "result": f"{routing_acc:.1%}", "pass": routing_acc >= 0.95},
    {"check": "accuracy: rule-following (bucket)", "result": f"{rule_acc:.1%}", "pass": rule_acc >= 0.90},
    {"check": "accuracy: negation trap", "result": f"{negation_acc:.1%}", "pass": negation_acc >= 0.90},
    {"check": "calibration: expected calibration error", "result": f"{ece:.3f}", "pass": ece <= 0.15},
    {"check": "invariance: any decision flip on meaning-preserving edit", "result": str(inv_df["flip"].any()), "pass": not inv_df["flip"].any()},
    {"check": "invariance: drift beyond 2x noise floor", "result": str(inv_df["exceeds_noise_floor"].sum()) + " perturbations", "pass": inv_df["exceeds_noise_floor"].sum() == 0},
    {"check": "discrimination: anger-marker Spearman correlation", "result": f"{spearman:.2f}", "pass": spearman >= 0.7},
    {"check": "discrimination: distractor flood keeps correct answer", "result": str(flood_df["correct"].all()), "pass": flood_df["correct"].all()},
    {"check": "opinion anchoring: answer changes across positive/neutral/negative framing", "result": str(anchor_df["answer"].nunique() > 1), "pass": None},
]).set_index("check")
scorecard
""")

md(r"""
## 8. Cost and takeaways
""")
code(r"""
price_per_m_input = 0.042  # USD per 1M input tokens, from the TypeSafe cookbook (2026-09) — check the current price page
print(USAGE)
print(f"approx cost of API calls actually sent: ${USAGE['input_tokens'] / 1e6 * price_per_m_input:.4f}")
print(f"cache hits (not re-sent): {USAGE['cache_hits']}")
""")

md(r"""
**Takeaways**

- Measure accuracy on tasks with a **computable** ground truth, not opinions. A generator that
  produces its own answer key (numeric comparisons, rules stated in the instructions, matched
  negation pairs) lets you run hundreds of cases instead of hand-labelling dozens.
- Establish the **noise floor first** (identical request, repeated). Without it, a small
  perturbation-induced shift is impossible to tell apart from ordinary jitter.
- **Accuracy, calibration, invariance, and discrimination are four different failure modes.** A
  model can be accurate but overconfident, or accurate and well-calibrated but unstable to key
  reordering, or stable but insensitive to a real signal. Test them separately.
- **Overconfidence matters more than underconfidence** for anything gated on a threshold: it is
  the direction where the model states a stronger belief than it has earned, which is exactly when
  a confidence-gated pipeline acts automatically on a wrong answer.
- Re-run this notebook (or a trimmed copy) against **your own domain's tickets/records**, not just
  the synthetic tasks here — public write-ups on Jev agree that a judge calibrated on one workflow
  is not guaranteed to be calibrated on a different one.
- Widen `N_PER_TASK` and `REPEATS_PER_LEVEL` for a tighter read; the numbers above are a
  demonstration of the method at a cost of a few cents, not a final verdict on the model.
""")

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
}
nbf.write(nb, "jev_eval_tutorial.ipynb")
print(f"wrote jev_eval_tutorial.ipynb with {len(cells)} cells")
