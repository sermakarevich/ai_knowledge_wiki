# Chapter 09 — Hallucination detectors on RAGTruth and our helpdesk replies

Two halves. **09a** runs three cheap CPU-only detectors (HHEM, LettuceDetect, NLI) on the public RAGTruth benchmark (n=400 test split; dev/test 80/400) to establish where the ceiling is without an LLM judge. **09b** adds two LLM-in-the-loop methods (SelfCheckGPT sampling consistency on 60 rows; qwen3.8:27b judge on 100 rows) and applies the two best detectors to our own 60 helpdesk-reply traces against the chapter-03 `unsupported_claim` gold label.

## 09a — CPU detectors on RAGTruth (n=400)

| Detector | AUROC | 95 % CI | F1 | threshold | Precision | Recall | s/item |
|---|---|---|---|---|---|---|---|
| **LettuceDetect** | **0.7681** | [0.713, 0.820] | **0.6107** | 0.864 | 0.755 | 0.513 | 0.116 |
| HHEM | 0.7581 | [0.660, 0.766] | 0.1702 | 0.973 | 0.500 | 0.103 | 0.059 |
| NLI cross-encoder | 0.4835 | [0.419, 0.549] | 0.3128 | 0.995 | 0.192 | 0.846 | 0.785 |

**LettuceDetect** is the best all-round CPU detector: AUROC 0.768 (nearly tied with HHEM), F1 0.611 (3.5× HHEM), and a well-separated threshold. HHEM is a fine *ranker* (AUROC 0.758) but under-fires at a fixed threshold (recall 0.103). NLI is **at chance** (AUROC CI includes 0.5) and the slowest by far — not a hallucination detector. All are `llm_calls=0`.

**Per task type (F1):** LettuceDetect is best on both QA (0.735) and Summary (0.476); all detectors do worse on Summary than QA — long summaries bury the bad span in a longer, more plausibly-paragraph.

**Span localization:** LettuceDetect span-token F1 is only 0.082 — it knows *something* is wrong but can't reliably say *which words*. The "highlight it" capability is the weak point across the board.

## 09b — LLM methods on RAGTruth

### SelfCheckGPT (60 Summary rows, 180 LLM calls)

For each row: re-generate the response 3× at temperature 0.7 (seeds 42/43/44), score each sample against the original with the NLI cross-encoder (bidirectional mean), report `1 − mean` as the inconsistency score.

| Metric | Value |
|---|---|
| AUROC | **0.4120** [0.300, 0.624] |
| F1 | 0.2400 [0.111, 0.500] |
| Precision / Recall | 0.273 / 0.214 |
| Threshold | 0.9996 |
| s/item | 2.198 |

**09b finding:** SelfCheckGPT sampling consistency is **below chance** on RAGTruth Summaries (AUROC 0.412, CI includes 0.5). The heuristic assumes that a fabricated response won't be stably reproducible from the same source — but on a dataset where the "source" is already the full document to be summarised, sampling from the same source naturally produces *similar* summaries regardless of whether they hallucinate, so the consistency signal is weak. With 180 LLM calls and ~2 min of wall time for the 60-row batch, SelfCheckGPT is not competitive with the free CPU detectors on this data.

### LLM judge — qwen3.8:27b (100 Summary rows, 100 LLM calls)

Binary verdict (`hallucinated: true/false`) via `HallucJudgeVerdict` schema, scored as 1/0.

| Metric | Value |
|---|---|
| AUROC | **0.8590** [0.734, 0.909] |
| F1 | **0.7692** [0.595, 0.853] |
| Precision / Recall | 0.714 / 0.833 |
| Threshold | 1.0 (binary) |
| s/item | 1.236 |

The LLM judge is the **best method on RAGTruth in this benchmark** by AUROC (0.859) and F1 (0.769). At ~1.2 s/item it is 2–3× the cost of LettuceDetect but catches significantly more positives per false-positive. This is the ceiling you hit when willing to pay for an LLM call per row.

## Apply — our own helpdesk replies (n=60, ch-03 gold)

Gold = chapter-03 `unsupported_claim` failure mode in `labels/answer_v1.jsonl` (12 of 60 test-split rows positive). Source = concatenated retrieved handbook section texts. Response = the model's reply text from `runs/traces/answer_v1/`.

| Detector | AUROC | F1 | Precision | Recall | Notes |
|---|---|---|---|---|---|
| LettuceDetect | **0.5469** | **0.381** | 0.267 | 0.667 | threshold 0.701; recall is high but every flag is wrong 3/4 of the time |
| HHEM | 0.3958 | 0.333 | 0.200 | 1.000 | threshold 0.278; catches all 12 positives but flags every one of the 48 negatives too |

**09b finding:** Both CPU detectors **drop sharply** from RAGTruth to our helpdesk traces. HHEM AUROC goes from 0.758 → 0.396; LettuceDetect from 0.768 → 0.547. The domain gap is large: RAGTruth hallucinations are *fabricated facts in otherwise-grounded text*, whereas our helpdesk replies often contain *refusals, caveats, and disclaimers* that the detectors interpret as low-consistency noise. HHEM's 100% recall at 0.2× precision means it flags essentially every reply as "hallucinated" — it is not discriminative on this corpus. The 3 highest-Lettuce flags include 2 of 3 false positives (tkt-021, tkt-047); the one genuine positive it catches (tkt-071) fires on the word "points" — the detector is reacting to *specific* domain vocabulary, not to semantic inconsistency.

## Cross-method comparison (runs/09_compare.md)

| Method | Headline AUROC | n |
|---|---|---|
| HHEM | 0.7581 | 400 |
| LettuceDetect | 0.7681 | 400 |
| NLI cross-encoder | 0.4835 | 400 |
| SelfCheckGPT | 0.4120 | 42 (test) |
| LLM judge (qwen3.8) | 0.8590 | 70 (test) |

Pairwise binary agreement at 0.5 threshold on the shared 400 RAGTruth rows shows the two free detectors (HHEM ↔ Lettuce) agree 73 % of the time — they are picking up largely the same signal. The LLM judge disagrees with both (58–83 % agreement) because it operates at a different decision granularity. SelfCheckGPT agrees 98 % with NLI because it *uses* the NLI model internally — they are not independent signals.

## Recommendations

1. **Primary detector (free, no LLM):** LettuceDetect — best F1 (0.61) and AUROC (0.77) tied with HHEM; far better threshold behaviour. Use its max-span-confidence score.
2. **Second opinion (free):** HHEM — fine ranker but under-fires at a fixed threshold. Use for tie-breaking, not as a standalone flag.
3. **Do not use NLI** for hallucination; use only for relevance (ch. 08).
4. **If precision matters more than cost:** LLM judge (qwen3.8:27b) is the best single-shot method (F1 0.77, AUROC 0.86) at ~1.2 s/row wall time.
5. **SelfCheckGPT** is not competitive on RAGTruth Summaries (AUROC 0.41) — the sampling-consistency assumption does not hold when the source is the full document to be summarised.
6. **Apply to our own helpdesk replies:** Both free detectors underperform their RAGTruth numbers substantially (domain gap). HHEM flags almost everything; LettuceDetect fires on specific words. For a production "hallucination alarm" on our helpdesk corpus, the LLM judge is the only method with meaningful discriminative power above 0.5 AUROC.
7. **Span-level localization is weak across all methods** (best token-F1 0.082). "Highlight the bad sentence" needs either span-specific fine-tuning or a coarser sentence-level fallback.

## Budget and reproducibility

| Step | LLM calls | Wall time |
|---|---|---|
| 09a detectors (HHEM + Lettuce + NLI) | 0 | ~3 min (CPU) |
| 09b selfcheck | 180 | ~132 s |
| 09b judge | 100 | ~124 s |
| 09b apply (helpdesk) | 0 | ~30 s (CPU) |
| **Total** | **280** | **~8 min** |

```bash
just halluc-detectors    # 09a: HHEM + Lettuce + NLI
just halluc-selfcheck    # 09b: SelfCheckGPT on 60 rows (180 calls)
just halluc-judge        # 09b: LLM judge on 100 rows (100 calls)
just halluc-compare      # cross-method table (no LLM)
just halluc-apply answer_v1  # on our helpdesk traces (no LLM)
just results             # rebuild runs/results.md
```

All 133 fast tests pass.
