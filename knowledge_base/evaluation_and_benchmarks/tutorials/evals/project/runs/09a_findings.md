# Chapter 09a — CPU hallucination detectors on RAGTruth: cheap signals, and one that isn't

Chapters 04–08 graded *our* answer pipeline. This chapter turns to the general
question: **can a small, cheap, CPU-only model tell a hallucinated RAG answer
from a grounded one, without an LLM judge?** We run three detectors from the
public **RAGTruth** benchmark (n=480: 240 QA + 240 Summary, 93 of which are
annotated hallucinations) and score them three ways that matter operationally:

- **AUROC** — *ranking* quality, independent of the (hard-to-pick) threshold.
- **F1 at a fixed threshold** — *deployment* quality. The threshold is chosen
  on the first 80 rows (dev) to maximise F1, then held fixed for the remaining
  400 (test). This is the honest "you can't peek at the labels" number.
- **Span-token P/R** (LettuceDetect only) — *localization* quality: can we
  point at *which* words are made up, not just that something is made up.

Scoring convention across all three: **score ∈ [0,1], higher = more
hallucinated.** HHEM is `1 − P(consistent)`; NLI is `1 − min(entailment)`;
LettuceDetect is the *max* span confidence.

## What we ran

| Experiment | Detector | Model | s/item |
|---|---|---|---|
| `09_hhem_ragtruth` | Vectara HHEM-2.1-Open (T5 flan-t5-base, 2-way seq class) | `vectara/hallucination_evaluation_model` | 0.059 |
| `09_lettuce_ragtruth` | LettuceDetect 0.1.6 (transformer span detector) | HF `TransformerDetector` | 0.116 |
| `09_nli_ragtruth` | NLI cross-encoder as entailment check | `cross-encoder/nli-deberta-v3-base` | 0.785 |

All three are **`llm_calls=0`** — pure CPU inference. Data:
`data/public/ragtruth_test_subset.jsonl`. Dev/test split = first 80 / last 400.

## Results (test split, n=400, threshold fixed by dev)

| Detector | AUROC | 95 % CI (AUROC) | F1 | 95 % CI (F1) | threshold | Precision | Recall |
|---|---|---|---|---|---|---|---|
| **LettuceDetect** | **0.7681** | [0.713, 0.820] | **0.6107** | [0.528, 0.705] | 0.864 | 0.755 | 0.513 |
| HHEM | 0.7581 | [0.660, 0.766] | 0.1702 | [0.126, 0.310] | 0.973 | 0.500 | 0.103 |
| NLI | 0.4835 | [0.419, 0.549] | 0.3128 | [0.267, 0.364] | 0.995 | 0.192 | 0.846 |

Read the two columns differently. **AUROC is nearly tied** for HHEM and
Lettuce (~0.76 both) — as *rankers* they are the same quality. **F1 is not**:
that gap is entirely a threshold story (below). NLI is **at chance** — its
AUROC 0.484 CI includes 0.5, so it is statistically indistinguishable from a
coin flip.

### Per task type (F1)

| Detector | QA (n=240) | Summary (n=160) |
|---|---|---|
| LettuceDetect | **0.735** | 0.476 |
| HHEM | 0.200 | 0.148 |
| NLI | 0.242 | 0.398 |

Lettuce is better at *both*, and much better on QA. Every detector does worse
on Summary than on QA — long summaries are the harder regime (the bad span is
buried in a longer, more *plausibly grounded* paragraph).

## The interesting finding: the same ranker, two different F1s

HHEM and Lettuce have **matching AUROC (~0.76)** but **F1 of 0.17 vs 0.61**.
The difference is *which* threshold the dev split lands on, and it exposes
something real about HHEM's score distribution:

- **HHEM threshold = 0.973.** Its `1 − P(consistent)` mass is skewed — most
  non-hallucinated answers score very low, but the hallucinated ones don't all
  clear a high bar. The dev split's F1-maximising threshold ends up at 0.973,
  which on the test split only fires when the model is *extremely* sure:
  **precision 0.500, recall 0.103.** It flags almost nothing, and half of what
  it flags is wrong on the test set. HHEM is a *conservative* detector here.
- **LettuceDetect threshold = 0.864.** Its max-span-confidence is better
  separated: **precision 0.755, recall 0.513** — it actually *catches half* of
  the hallucinations and is right 3 of 4 times when it does.

So "HHEM AUROC ≈ Lettuce AUROC" is only half the story. **For a deployment
where a single fixed threshold is all you get, Lettuce is the clearly better
detector** — same ranking, far better threshold behaviour. If you can afford to
tune a per-dataset threshold *after* seeing the score distribution, HHEM's
ranking is competitive; but out of the box, on RAGTruth, it under-fires.

> Caveat: HHEM's F1 95 % CI is [0.126, 0.310] and the point estimate (0.170)
> sits near the *lower* half of that band; the band is wide because only ~19
> of the 400 test rows are hallucinated. The ranking claim (AUROC) is the more
> reliable of HHEM's two numbers.

### NLI is not a hallucination detector (here)

NLI AUROC **0.484 [0.419, 0.549]** includes 0.5. Its profile is the *worst*
operational shape: **high recall (0.846), very low precision (0.192)** — it
flags almost everything as hallucinated (threshold 0.995 is a near-tautology
on this score shape) and is right only 1 in 5 of those flags. The reason is
structural: NLI asks *"does the whole summary entail this sentence chunk?"* —
that is a very different, much looser question than *"is this chunk grounded in
the source?"*, and it is the **slowest** detector by far (0.785 s/item vs
0.06–0.12 for the other two). Recommendation: **drop NLI** from the
hallucination path; keep a cross-encoder NLI around for *relevance* checks (the
08 retrieval work), not faithfulness.

### LettuceDetect span localization is weak

Lettuce's response-level score is the best in the table, but its
**span-token F1 is only 0.082** (precision 0.090 / recall 0.085). It *decides
correctly* that a response is hallucinated, but it **cannot reliably point at
*which* words** are the hallucinated span. For a product feature like "highlight
the made-up sentence," LettuceDetect as trained on RAGTruth is not enough as-is
— you would want the stronger (larger, or fine-tuned) model, or to fall back to
the *sentence* that contains the worst NLI/entailment chunk as a coarser
highlight.

## Bottom line

- **Best all-round CPU detector on RAGTruth: LettuceDetect** — AUROC 0.768,
  F1 0.611, and the only one with a deployable, well-separated threshold
  (precision 0.755). It is also ~2× faster than NLI and 2× faster than HHEM.
- **HHEM is a fine ranker (AUROC 0.758) but a poor fixed-threshold detector
  here** (F1 0.170, recall 0.103) — it under-fires unless you hand-tune the
  threshold per dataset. Keep it as a cheap second opinion, not the primary.
- **NLI is at chance (AUROC 0.484) and the slowest** — not a faithfulness
  detector; use it for relevance, not hallucination.
- **Span-level localization (the "highlight it" capability) is the weak
  point across the board** — best F1 span-token is 0.082 (Lettuce).

## Engineering notes (gotchas we hit)

- **transformers 5.16 + HHEM remote code.** HHEM's `model.py` wrapper calls a
  `post_init` that references `all_tied_weights_keys`, which changed in
  `transformers 5.x` — the wrapper *crashes on load*. Workaround used in
  `halluc.py`: load `T5ForTokenClassification` directly on
  `google/flan-t5-base`, take the two-way classification head from HHEM's
  state-dict (strip the leading `t5.` prefix), `load_state_dict(strict=False)`.
  One tied weight is left to re-init, zero unexpected keys. Labels are
  hard-coded from HHEM's `config.id2label` = `{"0": "hallucinated",
  "1": "consistent"}`, so `HHEM_CONSISTENT=1` and score = `1 − P(class 1)`.
- **LettuceDetect import path.** In `lettucedetect==0.1.6` the package
  `__init__.py` files are empty — `from lettucedetect import ...` fails. The
  class lives at `lettucedetect.models.inference.TransformerDetector`.
- **Lettuce prompt/offset alignment.** Passing RAGTruth's raw `prompt` through
  `detect_prompt` misaligns the answer's char offsets from the tokenizer's
  offset mapping, which zeroes the span metric. Fix: build the context the way
  Lettuce was trained (split RAGTruth's `passage 1:… passage 2:…` string into
  clean bodies for QA; bare string for Summary) and call `predict(context,
  answer, question=...)`, which re-forms the exact RAGTruth prompt layout and
  keeps offsets consistent.
- **NLI sentence-chunking.** `cross-encoder/nli-deberta-v3-base` needs matching
  `text`/`text_pair` batch lengths — repeat the *summary* once per sentence
  chunk so both sides of the batch line up.

## Reproduce

```bash
just halluc-detectors      # runs hhem + lettuce + nli + rebuilds results.md
# or individually (CPU-only, ~1–7 min total):
PYTHONPATH=src uv run python -m evals_tutorial.halluc hhem
PYTHONPATH=src uv run python -m evals_tutorial.halluc lettuce
PYTHONPATH=src uv run python -m evals_tutorial.halluc nli
# tests:
PYTHONPATH=src uv run pytest tests/test_09_halluc.py -q            # 24 pass
PYTHONPATH=src uv run pytest tests/test_09_halluc.py -m "not slow" -q  # 21 pass (no models)
```
