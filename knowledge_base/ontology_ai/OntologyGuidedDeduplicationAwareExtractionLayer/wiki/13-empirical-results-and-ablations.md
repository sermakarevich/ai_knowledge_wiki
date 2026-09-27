> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Root Cause, Intervention Cost and Expected Lift
**In one sentence:** OCR failures are addressed by five costed roadmap interventions, while a local-vs-cloud benchmark shows local OCR is production-viable, ontology conformance is high with low recall, and end-to-end accuracy reaches ≈93% with only cosmetic gaps.
## Key points
- OCR non-determinism is fixed by multi-pass OCR plus transcript union (2–3× re-transcription per page) at 2–3× OCR time cost for medium–high lift.
- Dense layout regions (multi-column, tight tables) are fixed by crop-and-re-OCR at 400 dpi, an engineering-cost intervention with high expected lift.
- Long-tail OOV vocabulary is fixed by running a dedicated OCR model (e.g. Tesseract with custom dictionary) alongside the VLM and unioning outputs, at infrastructure cost with high lift.
- Local model (Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology via vLLM) trails Gemini 2.5 Flash by ~6 points on entity spans (59.6% vs 65.3% CoNLL04; 60.8% vs 66.6% Re-DocRED) but is at parity on relations, with n = 50/20 so directional only.
- Local OCR matches cloud on clean English (token-F1 0.86–0.95) and beats it on multilingual XFUND scans, with zero runaway/empty-output failures versus cloud looping on dense forms.
- Ontology conformance is high (68–70% Text2KGBench, ≈89% OSKGC) with near-zero hallucination but low triple F1 (22–26% / 35–40%) and 42–50% fine-grained mapping accuracy, motivating retrieval grounding.
- End-to-end accuracy on a synthetic intelligence report is ≈93% across six dimensions (100/100 entity completeness/properties, 90–95 the rest), with residual gaps cosmetic and fixable by Stage 2–3 cleaning.
---
## Root-cause intervention table
| Root cause | Intervention | Cost | Expected lift |
|---|---|---|---|
| OCR non-determinism: different runs recover different names | Multi-pass OCR + transcript union: re-transcribe each page 2–3×, union outputs | 2–3× OCR time | Medium–high |
| Image quality below model's reading floor | Higher DPI (200 → 300 dpi), contrast enhancement, sharpening | +file size | Low–medium |
| Under-specified transcription prompt | Directive prompt: "preserve every all-caps heading, numeric prefix, and bold word" | Free | Low–medium |
| Long-tail vocabulary OOV to vision model | Dedicated OCR model (e.g. Tesseract with custom dictionary) run alongside VLM; union outputs | Infrastructure | High |
| Dense layout regions (multi-column, tight tables) | Crop-and-re-OCR: detect dense regions, re-render at 400 dpi, OCR independently | Engineering | High |

## Benchmark campaign: local model versus cloud ceiling
Campaign compares local model (Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology, served via vLLM) against "a strong cloud model (Gemini 2.5 Flash) used purely as an upper-bound calibration reference, not a production candidate"; four phases with fixed seeds and small samples (n = 8–50), "so results are directional rather than statistically significant."

Table 21 — Phase 1 extraction quality (micro-F1, span-only / pair-only):

| Dataset | Metric | Local | Cloud | Δ |
|---|---|---|---|---|
| CoNLL04 | Entity (span-only) | 59.6% | 65.3% | +5.7 |
| CoNLL04 | Relation (pair-only) | 16.3% | 19.9% | +3.6 |
| Re-DocRED | Entity (span-only) | 60.8% | 66.6% | +5.8 |
| Re-DocRED | Relation (pair-only) | 21.2% | 20.6% | −0.6 |

Phase 2 OCR: "the local model matches the cloud model on clean English (FUNSD forms, CORD receipts) and beats it on multilingual scans (XFUND, German/Spanish), while a classical OCR engine (Paddle) trails everywhere"; "the local model was also the only engine with no runaway or empty-output failures; the cloud model loops on dense forms because its API rejects the repetition penalty"; "Token-F1 of 0.86–0.95 shows recognition is strong even where order-sensitive WER is inflated by ground-truth layout noise."

Phases 3–4: "both providers reach high schema conformance (68–70% on Text2KGBench, ≈89% on OSKGC) with near-zero hallucination, but under-extract: triple-level F1 stays low (22–26% / 35–40%), and on OSKGC the fine-grained type-mapping accuracy is only 42–50% (the model emits a generic Location where the schema expects City)."

Takeaway verbatim: "The local model is production-viable for OCR (at or above the cloud ceiling, especially multilingual) and within ∼6 points on academic extraction, while matching the cloud model on ontology conformance with zero hallucination."

## End-to-end accuracy against a ground-truth document
"Finally, we measure end-to-end accuracy on a synthetic intelligence report with a hand-built ground-truth key (entities, properties, and relationships across nine document sections)"; "the overall accuracy is ≈93%."

Six dimensions: Entity completeness 100, Entity properties 100, Entity typing 90, Relationship completeness 95, Relationship accuracy 90, Qualifier accuracy 90. "All 16 persons were extracted with exact role/organisation attribution"; residual gaps are "cosmetic: redundant generic "Item" typing alongside the specific technology/vehicle types, and a few over-verbose relationship labels lifted verbatim from prose"; "These are exactly the upstream artifacts the Stage 2–3 cleaning fixes (Section 7.3) target, and they are addressable by post-processing without changing the extraction model."

## Limitations (as stated in chunk)
"Evaluation breadth: the case studies derive from single representative documents per condition" with "small public-dataset samples (n = 8–50)"; "OCR recall ceiling: even at the best chunk size, ground-truth vessel-class recall reaches only 58.8%, and the roadmap interventions of Table 20 remain unimplemented"; "similarity-scorer weights, retrieval thresholds (0.72 floor, 0.80 expansion trigger), and indicator-word lists are heuristics tuned on the development corpus"; throughput numbers "reflect one specific local deployment and do not generalise across hardware."

**Covers:** Roadmap intervention table (Table 20) + Sections 8.3–9, pp. 37–39
