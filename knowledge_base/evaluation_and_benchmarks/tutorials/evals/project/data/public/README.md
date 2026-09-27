# Public datasets used by the evals tutorial (committed subsets)

| file | source | licence | rows | used in |
|---|---|---|---|---|
| `mt_bench_answers.jsonl` | [lmsys/mt_bench_human_judgments](https://huggingface.co/datasets/lmsys/mt_bench_human_judgments) (Zheng et al. 2023, arXiv 2306.05685) | CC-BY-4.0 | 480 — one row per (question_id, model): `questions[2]`, `answers[2]` for 80 MT-Bench questions × 6 models (gpt-4, gpt-3.5-turbo, claude-v1, vicuna-13b-v1.2, alpaca-13b, llama-13b) | chapter 06 |
| `mt_bench_human_votes.jsonl` | same | CC-BY-4.0 | 3,355 expert pairwise votes: `question_id, model_a, model_b, winner (model_a/model_b/tie), judge (annotator id), turn (1/2)`; some pairs are voted by several annotators — that is how human–human agreement is measured | chapter 06 |
| `mt_bench_gpt4_votes.jsonl` | same (`gpt4_pair` split) | CC-BY-4.0 | 2,400 GPT-4 pairwise votes with the same columns (`judge` = `gpt4_pair`) — a frontier judge to compare the local judge with | chapter 06 |
| `ragtruth_test_subset.jsonl` | [ParticleMedia/RAGTruth](https://github.com/ParticleMedia/RAGTruth) (Niu et al. 2024, arXiv 2401.00396) | MIT | 480 — the `test` split, tasks `QA` (240) and `Summary` (240): first 40 sources of each task × 6 models; fields `id, source_id, task_type, source, prompt, source_info (the reference passages), model, response, labels (list of hallucinated spans with start/end/text/label_type), quality, hallucinated (bool = labels non-empty)`; 93 of 480 responses contain at least one hallucinated span | chapter 09 |

How they were built (2026-09-03): the MT-Bench parquet files were downloaded from the Hugging Face
parquet API and normalised into answers + votes (the original repeats both conversations in every vote
row, 27 MB); RAGTruth `response.jsonl` + `source_info.jsonl` were downloaded from the GitHub repo and
joined, then filtered as above. The raw files live (uncommitted) in `../../research/datasets/`.
