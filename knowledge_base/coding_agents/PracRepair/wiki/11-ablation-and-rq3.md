[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Answer to RQ3: PracRepair
**In one sentence:** All three PracRepair stages — Static-dynamic Context Construction, Question-driven Failure Diagnosis, and Feedback-guided Patch Refinement — integrate effectively to improve correct repair effectiveness, and the approach generalizes across RWB benchmarks and foundation models.
## Key points
- Answer to RQ3 states all three stages (Static-dynamic Context Construction, Question-driven Failure Diagnosis, Feedback-guided Patch Refinement) can be effectively integrated to improve correct repair effectiveness.
- RQ4 generalizability study evaluates PracRepair on the RWB benchmark under the perfect fault localization setting, following ThinkRepair [27].
- PracRepair is instantiated with GPT-4, GPT-3.5, DeepSeek-v3, DeepSeek-Coder, and Llama-3, and compared against published ThinkRepair [27] and ReInFix [28] results on the same benchmark.
- On RWB V1.0 (44 bugs), PracRepair repairs 23 bugs with GPT-4 and DeepSeek-v3, outperforming ReInFix (21 with GPT-4) and ThinkRepair (19 with GPT-3.5); it also repairs 22 with Llama-3 and 21 with GPT-3.5.
- On RWB V2.0 (29 bugs), PracRepair repairs 13 bugs with DeepSeek-Coder, compared with 12 by ReInFix and 10 by ThinkRepair.
- Results are described as best or tied-best across both RWB datasets and all evaluated model settings, including competitive effectiveness with open-source models, indicating generalization rather than dependence on a specific dataset or model family.
- Internal threats are manual validation of plausible patches (exact match to developer fix, else manual semantic-equivalence check per prior APR work) and potential data leakage, mitigated by RWB evaluation on post-training-cutoff commits with strong results across models.
- External threat is evaluation on Defects4J and RWB, two real-world Java benchmarks that may not represent other languages or much larger codebases; broader evaluation remains future work.
---
## Answer to RQ3
Verbatim answer given in the chunk:
> "PracRepair is well designed, and all three stages, i.e., Static-dynamic Context Construction, Question-driven Failure Diagnosis, and Feedback-guided Patch Refinement, can be effectively integrated to improve the correct repair effectiveness of PracRepair."
## RQ4: Generalizability study
Setup, per the chunk: evaluate PracRepair on the RWB benchmark under the perfect fault localization setting, following ThinkRepair [27]; instantiate with GPT-4, GPT-3.5, DeepSeek-v3, DeepSeek-Coder, and Llama-3; report published ThinkRepair [27] and ReInFix [28] results for comparison. RWB V1.0 and RWB V2.0 consist of bug-fixing commits collected after the training cutoff dates of GPT-3.5 and DeepSeek-Coder, respectively [27].
### Result analysis (Table VII as reported in text)
- Best or tied-best repair performance across both RWB datasets and all evaluated model settings.
- RWB V1.0 (44 bugs): 23 bugs with GPT-4 and DeepSeek-v3, vs. ReInFix 21 (GPT-4) and ThinkRepair 19 (GPT-3.5); 22 bugs with Llama-3 and 21 with GPT-3.5, indicating stable effectiveness across model backbones.
- RWB V2.0 (29 bugs): 13 bugs with DeepSeek-Coder, vs. 12 (ReInFix) and 10 (ThinkRepair).
- With open-source models such as GPT-4, DeepSeek-v3, and Llama-3, PracRepair maintains competitive repair effectiveness; the chunk concludes the approach generalizes well across benchmarks and foundation models rather than depending on a specific dataset or model family.
## Threats to validity
### Internal validity
- Manual validation of plausible patches: passing all tests does not guarantee semantic correctness, so a plausible patch is first checked for exact match to the developer-provided fix, otherwise manually assessed for semantic equivalence, following prior APR work.
- Potential data leakage (benchmark bugs or reference patches in LLM pre-training data), mitigated by additional evaluation on RWB, whose bug-fixing commits were collected after LLM training cutoff dates; strong results there suggest gains are not mere memorization.
### External validity
- Evaluation on Defects4J and RWB, two widely used real-world Java bug benchmarks, reduces unrepresentative-evaluation risk, but both are Java-limited and may not represent other languages or much larger codebases; evaluating on additional languages and broader repair settings remains future work.
## Related work (opening, as present in chunk)
- Existing APR approaches are categorized from three perspectives: non-learning-based, learning-based, and LLM-based approaches.
- Non-learning-based APR studied for over a decade [17]: search-based repair with manually designed mutation operators or fix patterns [18], [46]; learning transformation templates or repair patterns from human-written patches [47], [48]; synthesis via symbolic execution, constraints, and SMT solving [49], [50]; integration of repair into static analysis.
**Covers:** ablation answers and per-stage contribution.
