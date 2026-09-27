# Results

58 experiment(s)

experiment | chapter | n | primary metric | 95 % CI | LLM calls | s/item | notes
|---|---|---|---|---|---|---|---|
 |  | 0 |  | — | 0 | 0.0 | 
 |  | 0 |  | — | 0 | 0.0 | 
05_judge_did_not_answer | 05 | 60 | 0.11578947368421055 | [-0.12508, 0.386364] | 238 | 9.645 | did_not_answer v1 (best=v1)
05_judge_missing_required_fact | 05 | 60 | 0.02702702702702693 | [-0.17348, 0.285714] | 240 | 9.726 | missing_required_fact v2 (best=v2)
05_judge_missing_required_fact_nocontext | 05 | 30 | -0.15384615384615447 | [-0.27451, 0.0] | 30 | 2.686 | 
05_judge_overall | 05 | 60 | 0.15492957746478878 | [-0.088083, 0.414077] | 0 | 0.0 | 
05_judge_unsupported_claim | 05 | 60 | -0.11111111111111137 | [-0.189189, -0.030928] | 235 | 9.535 | unsupported_claim v2 (best=v2)
05_judge_wrong_section_retrieved | 05 | 60 | 0.0 | [0.0, 0.0] | 239 | 9.683 | wrong_section_retrieved v2 (best=v2)
05_likert_overall | 05 | 30 | 0.36 | [0.164, 0.584689] | 30 | 2.386 | 
07_ab_answer_v2_vs_v1 | 07 | 60 | 0.0 | [-0.116667, 0.117083] | 0 | 0.0 | v2 (new prompt) vs v1 (baseline), test split, same frozen judge
07_answer_v2_judged_did_not_answer | 07 | 60 | 0.20000000000000007 | — | 237 | 9.061 | did_not_answer v1 (best=v1) on answer_v2
07_answer_v2_judged_missing_required_fact | 07 | 60 | -0.09090909090909054 | — | 239 | 9.137 | missing_required_fact v2 (best=v2) on answer_v2
07_answer_v2_judged_overall | 07 | 60 | 0.15492957746478878 | — | 0 | 0.0 | 
07_answer_v2_judged_unsupported_claim | 07 | 60 | 0.09090909090909054 | — | 240 | 9.176 | unsupported_claim v2 (best=v2) on answer_v2
07_answer_v2_judged_wrong_section_retrieved | 07 | 60 | 0.0 | — | 238 | 9.095 | wrong_section_retrieved v2 (best=v2) on answer_v2
07_answer_v2_pass_rate | 07 | 60 | 0.7 | — | 0 | 0.0 | 
10_agent_transcript_judge | 10 | 60 | -0.23655913978494592 | — | 60 | 28.62 | transcript-only LLM judge vs code grader over 60 episodes; κ = agreement beyond chance
10_agent_v1_multiturn | 10 | 6 | 0.8333 | [0.5, 1.0] | 63 | 48.205 | multiturn (simulated user), 6 tasks x 3 trials; mean user turns = 0.11
10_agent_v1_pass_at_k | 10 | 20 | 0.85 | [0.7, 1.0] | 60 | 0.0 | agent_v1, 20 tasks x 3 trials; pass@k = at least 1 pass over tasks, pass^k = all pass
10_agent_v1_pass_pow_k | 10 | 20 | 0.75 | [0.55, 0.9] | 60 | 0.0 | agent_v1, 20 tasks x 3 trials; pass@k = at least 1 pass over tasks, pass^k = all pass
11_gsm8k_0shot_qwen3.8:27b | 11 | 50 | 0.46 | [0.32, 0.6] | 50 | 0.0 | gsm8k 0-shot via lm-eval
11_gsm8k_5shot_qwen3.8:27b | 11 | 50 | 0.46 | [0.32, 0.6] | 50 | 0.0 | gsm8k 5-shot via lm-eval
11_gsm8k_cot_qwen3.8:27b | 11 | 50 | 0.52 | [0.38, 0.66] | 50 | 0.0 | gsm8k cot-shot via lm-eval
11_gsm8k_gemma4:latest | 11 | 50 | 0.06 | [0.0, 0.14] | 50 | 2.208 | gsm8k on gemma4:latest via lm-evaluation-harness 0.4.13
11_gsm8k_plain_qwen3.8:27b | 11 | 50 | 0.96 | [0.9, 1.0] | 50 | 0.0 | single-shot custom prompt via evals_tutorial.llm (cached)
11_gsm8k_prompt_sensitivity | 11 | 50 | 0.5 | — | 200 | 0.0 | prompt sensitivity: 0-shot / 5-shot / CoT / plain on the same questions
11_gsm8k_qwen3.8:27b | 11 | 50 | 0.46 | [0.32, 0.6] | 50 | 7.376 | gsm8k on qwen3.8:27b via lm-evaluation-harness 0.4.13
11_gsm8k_tiny-qwen35-110m-sft:latest | 11 | 50 | 0.0 | [0.0, 0.0] | 50 | 0.464 | gsm8k on tiny-qwen35-110m-sft:latest via lm-evaluation-harness 0.4.13
11_ifeval_gemma4:latest | 11 | 50 | 0.74 | [0.62, 0.86] | 50 | 5.176 | ifeval on gemma4:latest via lm-evaluation-harness 0.4.13
11_ifeval_qwen3.8:27b | 11 | 50 | 0.82 | [0.72, 0.92] | 50 | 8.581 | ifeval on qwen3.8:27b via lm-evaluation-harness 0.4.13
11_ifeval_tiny-qwen35-110m-sft:latest | 11 | 50 | 0.14 | [0.06, 0.24] | 50 | 0.772 | ifeval on tiny-qwen35-110m-sft:latest via lm-evaluation-harness 0.4.13
12_inspect_gsm8k_qwen3.8:27b | 12 | 50 | 0.96 | [0.9, 1.0] | 0 | 0.0 | 
12_inspect_helpdesk_v1 | 12 | 60 | 0.7 | [0.5833333333333334, 0.8166666666666667] | 0 | 0.0 | 
13_ci_gate_v2_vs_v1 | 13 | 60 | 0.0 | [0.0, 0.0] | 0 | 0.0 | 
13_monitor_answer_v1 | 13 | 112 | 0.008928571428571428 | [0.0, 0.02635027125952937] | 0 | 0.0 | 
04_checks_answer_v1 | 4 | 60 | 0.11666666666666667 | [0.05, 0.2] | 0 | 0.0 | deterministic assertions (6) on answer_v1 test split
04_checks_answer_v2 | 4 | 60 | 0.13333333333333333 | — | 0 | 0.0 | deterministic assertions (6) on answer_v2 test split
04_similarity_answer_v1 | 4 | 60 | 0.8269230769230769 | [0.719148, 0.925563] | 120 | 0.0 | ROUGE-L + embedding cosine; correlation/AUC with ch-03 pass label
04_triage_v1 | 4 | 60 | 0.6971981721981723 | [0.548355, 0.791763] | 0 | 0.0 | code-graded classification on triage_v1; test split n=60
06_agreement_atla_selene-mini | 6 | 100 | 0.62 | [0.52, 0.71] | 200 | 1.466 | atla/selene-mini vs humans (majority of ab/ba orders); sample = 100 turn-1 non-tie pairs, seed 0; ceiling: human-human 0.826 (no ties) / 0.642 (with ties); reference: GPT-4 0.680
06_agreement_gemma4_latest | 6 | 100 | 0.62 | [0.52, 0.71] | 200 | 1.729 | gemma4:latest vs humans (majority of ab/ba orders); sample = 100 turn-1 non-tie pairs, seed 0; ceiling: human-human 0.826 (no ties) / 0.642 (with ties); reference: GPT-4 0.680
06_agreement_qwen3.8_27b | 6 | 150 | 0.6133 | [0.533333, 0.693333] | 272 | 5.052 | qwen3.8:27b vs humans (majority of ab/ba orders); sample = 150 turn-1 non-tie pairs, seed 0; ceiling: human-human 0.826 (no ties) / 0.642 (with ties); reference: GPT-4 0.680
06_bias_atla_selene-mini | 6 | 100 | 0.21 | [0.13, 0.29] | 200 | 1.466 | atla/selene-mini: position flip 21/100 pairs; first-position wins 117/200 calls; verbosity: judge picks longer 82/200 vs humans 72/100; context: human-human 0.826, GPT-4 0.680; self-preference NOT measurable: no MT-Bench model is a Qwen family
06_bias_gemma4_latest | 6 | 100 | 0.21 | [0.14, 0.29] | 200 | 1.729 | gemma4:latest: position flip 21/100 pairs; first-position wins 81/200 calls; verbosity: judge picks longer 83/200 vs humans 72/100; context: human-human 0.826, GPT-4 0.680; self-preference NOT measurable: no MT-Bench model is a Qwen family
06_bias_qwen3.8_27b | 6 | 150 | 0.2067 | [0.1465, 0.273333] | 272 | 5.052 | qwen3.8:27b: position flip 31/150 pairs; first-position wins 172/300 calls; verbosity: judge picks longer 112/300 vs humans 107/150; context: human-human 0.826, GPT-4 0.680; self-preference NOT measurable: no MT-Bench model is a Qwen family
06_bradley_terry | 6 | 6 | 0.7143 | [-0.228495, 1.0] | 0 | 0.0 | Bradley–Terry MLE over 1689 human turn-1 votes vs 118 qwen majority-of-two votes; ranking agreement spearman rho = 0.714; /Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/bt_ratings.png
06_panel | 6 | 100 | 0.7 | [0.61, 0.79] | 672 | 10.773 | panel = bare-majority-of-available picks over qwen3.8:27b, gemma4:latest, atla/selene-mini; each judge already collapsed by majority of its ab/ba orders; n=100 pairs, agreement_with_humans=0.700
08_agreement_metrics | 8 | 28 | 0.5777777777777777 | [0.3630397727272727, 0.8057171474358974] | 0 | 0.0 | Evaluator agreement: Spearman between RAGAS/DeepEval faithfulness and ch-04 embedding cosine, plus AUROC of each against the ch-03 gold pass label and the ch-05 overall verdict. Pure, no LLM calls.
08_deepeval_answer_v1 | 8 | 30 | 0.9867857142857142 | [0.9733244047619047, 0.9976190476190477] | 270 | 96.037 | DeepEval native Ollama judge (Faithfulness/AnswerRelevancy/ContextualPrecision) on the same test split as RAGAS. LLM calls counted on the native OllamaModel.generate/a_generate.
08_ragas_answer_v1 | 8 | 30 | 0.6763555306839468 | [0.5898028581903777, 0.7604333674757782] | 146 | 61.551 | RAGAS classic metrics (faithfulness, answer_relevancy, context_precision) on the test split. response = cached SUT answer from the trace. LLM calls counted on the RAGAS wrapper.
08_retrieval_answer_v1 | 8 | 60 | 0.8416666666666667 | [0.7583333333333333, 0.9166666666666666] | 0 | 0.0 | Per-ticket classical IR metrics on the test split. recall@2 is primary; CIs are bootstrap over tickets. The recall@k curve uses one fresh retrieve(k=kmax) per ticket (embeddings are cached). Failure split: failed tickets whose gold section was not in top-2 are retrieval failures; the rest are generation failures.
08_retrieval_answer_v2 | 8 | 60 | 0.8416666666666667 | [0.7583333333333333, 0.9166666666666666] | 0 | 0.0 | Per-ticket classical IR metrics on the test split. recall@2 is primary; CIs are bootstrap over tickets. The recall@k curve uses one fresh retrieve(k=kmax) per ticket (embeddings are cached). Failure split: failed tickets whose gold section was not in top-2 are retrieval failures; the rest are generation failures.
09_detector_helpdesk_v1 | 9 | 60 | 0.5469 | — | 0 | 0.0 | Gold = chapter-03 `unsupported_claim` label; source = concatenated retrieved handbook sections
09_hhem_ragtruth | 9 | 400 | 0.7581 | [0.6601293449554806, 0.7660406878656218] | 0 | 0.071 | CPU-only detectors; threshold chosen on first 80 rows to maximise F1
09_lettuce_ragtruth | 9 | 400 | 0.7681 | [0.7129477944231438, 0.8198834916233225] | 0 | 0.139 | CPU-only detectors; threshold chosen on first 80 rows to maximise F1
09_llm_judge_ragtruth | 9 | 70 | 0.7692 | [0.5945445445445445, 0.8525761124121778] | 100 | 1.765 | dev/test split within rows; threshold picked on dev to maximise F1
09_nli_ragtruth | 9 | 400 | 0.4835 | [0.41938235461067214, 0.5493757513158175] | 0 | 0.942 | CPU-only detectors; threshold chosen on first 80 rows to maximise F1
09_selfcheck_ragtruth | 9 | 42 | 0.412 | [0.29950825576241136, 0.623812509499924] | 180 | 3.14 | dev/test split within rows; threshold picked on dev to maximise F1
