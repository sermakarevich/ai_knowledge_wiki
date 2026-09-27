# Datasets research (2026-08-30, live web research)

## 1. Pre-training corpora (100M–500M model, 1–5B tokens subset)

| Dataset | HF ID | Size | License | Notes |
|---|---|---|---|---|
| FineWeb-Edu sample | `HuggingFaceFW/fineweb-edu` config `sample-10BT` | ~10B GPT-2 tokens, 27.6 GB | ODC-BY | streams well; best "high quality web text" |
| SmolLM-Corpus | `HuggingFaceTB/smollm-corpus` configs `cosmopedia-v2` (28B tok synthetic textbooks), `fineweb-edu-dedup` (220B), `python-edu` (4B) | | odc-by | what SmolLM-1 135M/360M/1.7B trained on (600B tok) |
| TinyStories | `roneneldan/TinyStories` | 7.62 GB, 2.12M train / 22k val | cdla-sharing-1.0 | tiny vocab; 1M–33M param models produce coherent text; minutes on a 4090 |
| Cosmopedia v1 | `HuggingFaceTB/cosmopedia` | ~25B tok | odc-by | |

SmolLM-135M/360M/1.7B: 600B tokens on SmolLM-Corpus. SmolLM2-135M: 2T tokens; 360M: 4T. Not reproducible on a 4090; tutorial trains 100–500M on 1–5B tokens (undertrained vs Chinchilla, but shows loss decreasing and plausible English in 1–4 h).

## 2. SFT datasets

| Dataset | HF ID | Size | License | Format |
|---|---|---|---|---|
| SmolTalk | `HuggingFaceTB/smoltalk` | 4.15 GB | Apache-2.0 | `messages` list — purpose-built for small models |
| Tulu-3 SFT | `allenai/tulu-3-sft-mixture` | 939k rows | mixed, some non-commercial | messages |
| OpenHermes-2.5 | `teknium/OpenHermes-2.5` | 1M rows | messy | |
| Alpaca-cleaned | `yahma/alpaca-cleaned` | 44 MB | CC-BY-4.0 | instruction/input/output |
| No Robots | `HuggingFaceH4/no_robots` | 10k | CC-BY-NC-4.0 | human-written |
| smoltalk2, Nemotron-Post-Training, OpenThoughts3 | | | UNVERIFIED | |

## 3. Preference datasets (DPO)

| Dataset | HF ID | Size | License | Format |
|---|---|---|---|---|
| UltraFeedback binarized | `HuggingFaceH4/ultrafeedback_binarized` | 650 MB, 64k prompts | MIT | chosen/rejected |
| HelpSteer3 | `nvidia/HelpSteer3` | 40k | CC-BY-4.0 | two responses + preference score, needs reshaping |

## 4. Verifiable-reward datasets (GRPO)

| Dataset | HF ID | Size | License | Notes |
|---|---|---|---|---|
| GSM8K | `openai/gsm8k` | 7,473 train / 1,319 test | MIT | THE standard small-model GRPO target |
| MATH-500 | `HuggingFaceH4/MATH-500` | 500 | UNVERIFIED | held-out eval |
| OpenR1-Math-220k | `open-r1/OpenR1-Math-220k` | 220k | Apache-2.0 | reasoning-distillation SFT |
| Countdown-Tasks-3to4 | `Jiayi-Pan/Countdown-Tasks-3to4` | UNVERIFIED | UNVERIFIED | mini-R1 "aha" reproduction (philschmid, Qwen2.5-3B TRL GRPO) |

## 5. Domain fine-tuning candidates

| Domain | HF ID | Size | License | Metric |
|---|---|---|---|---|
| Medical | `openlifescienceai/medmcqa` | 194k MCQ | UNVERIFIED | 4-option exact match |
| Medical | `GBaker/MedQA-USMLE-4-options` | 11.4k dev / 1,273 test | UNVERIFIED | 4-option |
| Medical | `qiaojin/PubMedQA` | 1k expert labelled | MIT | yes/no/maybe |
| Legal | `coastalcph/lex_glue` case_hold | | UNVERIFIED | 5-way MCQ |
| Finance | `gbharti/finance-alpaca` | 43 MB | UNVERIFIED | no held-out set |
| **Cybersecurity** | `tihanyin/CyberMetric` (80/500/2000/10000 MCQ, 9 domains, arXiv 2402.07688) | | UNVERIFIED | 4-option exact match, expert validated |
| Cybersecurity/CTI | `AI4Sec/cti-bench` (CTI-MCQ, CTI-RCM, CTI-VSP) | | UNVERIFIED | MCQ exact match |
| **Graph/Cypher** | `neo4j/text2cypher-2025v1` | 35.9k train / 4.44k test, 5 MB | Apache-2.0 | execution accuracy (needs Neo4j) or exact match |
| Graph/Cypher (older) | `neo4j/text2cypher-2024v1` | 39.5k / 4.8k | Apache-2.0 | same |
| SQL | `gretelai/synthetic_text_to_sql` | 100k / 5,851 | Apache-2.0 | execution / exact match |

Recommendation: `neo4j/text2cypher-2025v1` and CyberMetric are the strongest "domain vs general accuracy" candidates for this user.

## 6. lm-evaluation-harness tasks

| Task | # examples | Type |
|---|---|---|
| MMLU | 14,042 (57 subjects) | log-likelihood |
| ARC-Easy / Challenge | 2,376 / 1,172 | log-likelihood |
| HellaSwag | 10,003 | log-likelihood |
| WinoGrande | 1,267 | log-likelihood |
| TruthfulQA mc1/mc2 | 817 | log-likelihood |
| GSM8K | 1,319 | generative |
| IFEval | 541 | generative, rule-verified |
| PIQA | 16,113 | log-likelihood |

Runtime on 4090: UNVERIFIED; log-likelihood tasks with `--limit` a few hundred/task → well under an hour for ≤8B.

## Sources
https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu, https://huggingface.co/datasets/HuggingFaceTB/smollm-corpus, https://github.com/huggingface/blog/blob/main/smollm.md, https://huggingface.co/datasets/roneneldan/TinyStories, https://huggingface.co/HuggingFaceTB/SmolLM-135M, https://huggingface.co/datasets/HuggingFaceTB/smoltalk, https://huggingface.co/datasets/allenai/tulu-3-sft-mixture, https://huggingface.co/datasets/yahma/alpaca-cleaned, https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized, https://huggingface.co/datasets/nvidia/HelpSteer3, https://huggingface.co/datasets/openai/gsm8k, https://huggingface.co/datasets/Jiayi-Pan/Countdown-Tasks-3to4, https://www.philschmid.de/mini-deepseek-r1, https://huggingface.co/datasets/tihanyin/CyberMetric, https://arxiv.org/abs/2402.07688, https://huggingface.co/datasets/AI4Sec/cti-bench, https://huggingface.co/datasets/neo4j/text2cypher-2025v1, https://neo4j.com/blog/developer/introducing-neo4j-text2cypher-dataset/, https://huggingface.co/datasets/gretelai/synthetic_text_to_sql, https://github.com/EleutherAI/lm-evaluation-harness
