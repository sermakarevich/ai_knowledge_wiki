> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Model Comparison Results
**In one sentence:** The best SPARQL setup reaches 100% accuracy (21 questions) with the default ontology at temperature 0.0, while the best auto-SQL setup reaches only 57%, and accuracy falls sharply with weaker models or impoverished ontology representations.
## Key points
- Best SPARQL per model: Q36.27B.D (Qwen3.6-27B) and Q36.27B.Q (Qwen3.6-27B-Q8_0) both reach 100% on the default ontology at temp 0.0, with 8.1s/17.6K tokens (baseline) and 14.6s/17.7K tokens (procedural) respectively.
- The FP8 variant Q36.27B.F reaches 95% (default ontology, temp 0.0, guardrails, 7.9s, 17.8K tokens), while smaller/weaker models drop to 57% (Q30.30B.C, Q36.35B.F, Q36.35B.M), 38% (Q30.14B.D), and 24% (Q30.08B.D).
- Across ontology representations (Table 4), default hits 100%, then no-comments 81%, compact-typed 71%, compact-grouped 67%, compact 62%, raw-graph 48%, abstract-dict 19%, and abstract-graph 5%.
- With the default ontology, all three prompts reach 100% (baseline 8.1s, guardrails 8.3s, procedural 8.5s, all Q36.27B.D at temp 0.0), plus procedural with Q36.27B.Q at 14.6s.
- Across temperatures (Table 6, default ontology), temp 0.0 gives 100% (four configurations), temp 0.2 gives 95%, temp 0.4 gives 90%, and temp 0.6 gives 90%.
- Best auto-SQL accuracy (Table 7, wide-table schema) is 12/21 (57%) with comments vs 9/21 (43%) without, achieved by Q36.27B.Q; all other models score 52% or lower with comments.
- Ontology-derived column comments add 3 correct cases for the best SQL model (43% without to 57% with), described as "a considerably larger effect than stripping annotations from the SPARQL ontology (100% to 81%)".
---
## Best SPARQL configuration per model
| Model ID | Model Name | Acc% | Ontology | Temp | Prompt | Avg Time | Tokens | HW |
|---|---|---|---|---|---|---|---|---|
| Q36.27B.D | Qwen3.6-27B | 100 | default | 0.0 | baseline | 8.1s | 17.6K | A |
| Q36.27B.Q | Qwen3.6-27B-Q8_0 | 100 | default | 0.0 | procedural | 14.6s | 17.7K | N |
| Q36.27B.F | Qwen3.6-27B-FP8 | 95 | default | 0.0 | guardrails | 7.9s | 17.8K | A |
| Q30.30B.C | Qwen3-Coder-30B-A3B | 57 | compact-grouped | 0.2 | procedural | 1.0s | 1.9K | A |
| Q36.35B.F | Qwen3.6-35B-A3B-FP8 | 57 | default | 0.6 | guardrails | 25.8s | 17.8K | A |
| Q36.35B.M | Qwen3.6-35B-A3B | 57 | default | 0.2 | procedural | 24.2s | 17.7K | A |
| Q30.14B.D | Qwen3-14B | 38 | default | 0.0 | procedural | 1.8s | 16.8K | A |
| Q30.08B.D | Qwen3-8B | 24 | default | 0.6 | procedural | 0.9s | 16.8K | A |

## Best SPARQL configuration per ontology representation (Table 4, 21 questions)
"Table 4: Best SPARQL configuration per ontology representation (21 questions). Model IDs from Table 3."
| Ontology | Acc% | Temp | Prompt | Avg Time | Tokens | Model ID |
|---|---|---|---|---|---|---|
| default | 100 | 0.0 | baseline | 8.1s | 17.6K | Q36.27B.D |
| no-comments | 81 | 0.0 | procedural | 14.7s | 7.6K | Q36.27B.Q |
| compact-typed | 71 | 0.0 | procedural | 3.0s | 1.9K | Q36.27B.D |
| compact-grouped | 67 | 0.2 | procedural | 2.9s | 1.9K | Q36.27B.D |
| compact | 62 | 0.0 | procedural | 3.1s | 1.7K | Q36.27B.D |
| raw-graph | 48 | 0.4 | guardrails | 3.5s | 4.1K | Q36.27B.D |
| abstract-dict | 19 | 0.6 | baseline | 20.8s | 5.7K | Q36.35B.M |
| abstract-graph | 5 | 0.0 | guardrails | 31.8s | 3.8K | Q36.35B.F |

"The baseline prompt (the simplest of the three) achieves 100%, suggesting that with a well-designed ontology, elaborate prompting is unnecessary."

## Best SPARQL configurations per system prompt (Table 5, 21 questions, default ontology)
"Table 5: Best SPARQL configurations per system prompt (21 questions). All use default ontology."
| Prompt | Acc% | Model ID | Temp | Avg Time |
|---|---|---|---|---|
| baseline | 100 | Q36.27B.D | 0.0 | 8.1s |
| guardrails | 100 | Q36.27B.D | 0.0 | 8.3s |
| procedural | 100 | Q36.27B.D | 0.0 | 8.5s |
| procedural | 100 | Q36.27B.Q | 0.0 | 14.6s |

## Best SPARQL configurations per temperature (Table 6, 21 questions, default ontology)
"Table 6: Best SPARQL configurations per temperature (21 questions). All use default ontology."
| Temp | Acc% | Model ID | Prompt | Avg Time |
|---|---|---|---|---|
| 0.0 | 100 | Q36.27B.D | baseline | 8.1s |
| 0.0 | 100 | Q36.27B.D | guardrails | 8.3s |
| 0.0 | 100 | Q36.27B.D | procedural | 8.5s |
| 0.0 | 100 | Q36.27B.Q | procedural | 14.6s |
| 0.2 | 95 | Q36.27B.Q | baseline | 14.2s |
| 0.4 | 90 | Q36.27B.F | guardrails | 7.8s |
| 0.6 | 90 | Q36.27B.F | procedural | 8.0s |

## Auto-SQL results (Section 5.4, Table 7)
"Table 7 shows auto-SQL accuracy with and without ontology-derived column comments."
"Table 7: Best auto-SQL accuracy per model (21 questions, wide-table schema). Model IDs from Table 3."
| Model ID | With comments | No comments |
|---|---|---|
| Q36.27B.Q | 12/21 (57%) | 9/21 (43%) |
| Q36.27B.D | 11/21 (52%) | 7/21 (33%) |
| Q36.27B.F | 11/21 (52%) | 8/21 (38%) |
| Q36.35B.M | 11/21 (52%) | 6/21 (29%) |
| Q36.35B.F | 11/21 (52%) | 7/21 (33%) |
| Q30.14B.D | 9/21 (43%) | 7/21 (33%) |
| Q30.08B.D | 8/21 (38%) | 6/21 (29%) |
| Q30.30B.C | 8/21 (38%) | 7/21 (33%) |

"The best model achieves 57% on auto-SQL compared to 100% on SPARQL. Ontology-derived column comments add 3 cases for the best model (43% without, 57% with), a considerably larger effect than stripping annotations from the SPARQL ontology (100% to 81%). The Q8 model (Q36.27B.Q) on institutional hardware achieves the highest SQL accuracy, suggesting that the chain-of-thought reasoning enabled in llama.cpp benefits the more complex SQL generation task."

## Practical deployment on modest hardware (Section 5.5)
"For SPARQL with the default ontology, both 27B dense variants (Q36.27B.D and Q36.27B.Q) achieve 100% accuracy at t=0.0, Q36.27B.D with all three prompts, while the FP8 variant (Q36.27B.F) reaches 95%."

"The complex pipelines in prior work [28, 33–35] exist for a reason: they cope with ontologies not designed for LLM consumption. When the ontology can be designed, which is the case for every new domain metadata project, the simpler path is available."

## Per-query comparison (Table 8, header only in chunk)
"Table 8: Per-query comparison using each backend's best configuration. SPARQL: Q36.27B.D, default ontology, t=0.0, baseline. Auto-SQL: Q36.27B.Q, with comments, t=0.0. Q# from Table 2. Time is LLM generation in seconds." (Row-level Q# results are not present in this chunk.)

**Covers:** Tables 4–8 (best SPARQL per model/ontology/prompt/temperature; auto-SQL per model; per-query comparison header); Sections 5.4 Auto-SQL Results and 5.5 Practical Deployment on Modest Hardware.
