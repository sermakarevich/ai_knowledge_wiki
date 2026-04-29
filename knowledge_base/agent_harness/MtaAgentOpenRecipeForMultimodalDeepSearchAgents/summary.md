# MTA-Agent: An Open Recipe for Multimodal Deep Search Agents

**Paper:** [MTA-Agent: An Open Recipe for Multimodal Deep Search Agents (Peng et al., 2026)](https://arxiv.org/abs/2604.06376)

## Human Readable TL;DR

Imagine you're a detective who can both look at photos and search the internet for clues. Today's AI models can do one or the other, but struggle to combine both skills across multiple steps of investigation. This paper builds an AI "detective" that learns to chain together image analysis and web searches to answer complex questions -- like identifying a building in a photo, then finding out who designed it, then discovering what other famous buildings they created. The team created a training dataset of 21,000 practice investigations, and their open-source detective outperforms even expensive commercial AI systems like GPT-5.

## TL;DR

MTA-Agent presents a fully open framework for training multimodal deep search agents that iteratively combine visual and textual tool use across multi-hop reasoning chains. The authors construct MTA-Vision-DeepSearch, a 21K-example dataset of verified multi-hop vision-language trajectories via an automated QA synthesis pipeline. A 32B parameter model trained with DAPO on this dataset achieves 54.63% across six benchmarks, surpassing GPT-5 (+2.78%) and Gemini-2.5-Pro (+3.65%), while a cached tool training approach eliminates API costs during RL training.

---

## Problem & Motivation

Multimodal large language models (MLLMs) can answer simple visual questions but struggle with complex queries requiring multi-step reasoning across visual and textual modalities. Real-world information-seeking often demands chaining together image understanding (e.g., reverse image search, OCR) with web search and reading -- a capability gap that no open-source model adequately addressed. Existing deep search agents are either text-only or proprietary, leaving the community without a reproducible recipe for building multimodal search agents.

---

## Main Original Ideas

1. **MTA-Agent QA Synthesis Pipeline** -- An automated pipeline that transforms simple VQA seeds into verified multi-hop reasoning chains. It uses a five-stage filtering process, four evidence-collection tools, and a QA generation module with five-criterion verification to ensure factual correctness, entity dependency, and answer uniqueness across hops.

2. **Answer Diversity Selection via Jaccard Similarity** -- A novel candidate selection strategy that uses a weak model (Qwen3-VL-32B) to generate predicted search queries, then selects the QA candidate producing the lowest Jaccard similarity (token overlap after stopword removal) against actual retrieval queries. This ensures training trajectories require genuine tool use rather than trivially searchable answers.

3. **Cached Tool Training for RL** -- A method to train agents with reinforcement learning (DAPO) without real-time API calls. Tool response caches are constructed from rollout histories, matched via cosine similarity (threshold >0.75), enabling cost-free RL training while maintaining 95%+ of real-tool performance.

4. **Multi-Difficulty Curriculum** -- Retaining all intermediate difficulty levels (2-hop, 3-hop, 4-hop) during training rather than only the hardest examples. This mixed-difficulty approach yields +1.01% over single-difficulty training, demonstrating the value of progressive reasoning depth for generalization.

---

## Key Findings

### Main Results (Average Across 6 Benchmarks)

| Model | Type | Avg. Accuracy |
|-------|------|:------------:|
| GPT-5 | Proprietary Agent | 51.86% |
| Gemini-2.5-Pro | Proprietary Agent | 50.98% |
| Gemini-3-Pro | Proprietary Agent | 54.46% |
| SenseNova-MARS-32B | Open Agent | -- |
| MM-DeepResearch-32B | Open Agent | -- |
| **MTA-DeepSearch-32B** | **Open Agent** | **54.63%** |
| MTA-DeepSearch-8B | Open Agent | 48.66% |

### Per-Benchmark Breakdown (MTA-DeepSearch-32B)

| Benchmark | Score |
|-----------|:-----:|
| MMSearch | **82.35%** |
| FVQA | **76.00%** |
| HR-MMSearch | 53.95% |
| BrowseComp-VL | 53.77% |
| MMSearch-Plus | 31.93% |
| MTA-test | 29.78% |

- Training increased average reasoning depth from **2.27 to 4.28 turns** (+88%), with 32% of trajectories reaching the 6-turn maximum
- Web search adoption rose from 72% to 99%; reverse image search from 55% to 79%
- Post-training agents developed a consistent **two-stage retrieval pipeline** (text search first, then visual search)
- Cached tool training achieved **46.34%** vs. **48.66%** for real-tool training (8B model), demonstrating caches preserve most of the training signal while eliminating API costs
- Multi-source dataset diversity added **+3.28%** over the base two-source configuration
- Average LLM cost per training sample: **$0.28** with **9.3 tool calls** per sample

---

## Suggestions & Future Directions

1. **Image necessity gap** -- 23.7% of generated questions can be answered without images. While still useful for general search training, future work should improve visual dependency filtering to increase multimodal rigor.

2. **Dataset contamination concerns** -- Gemini-3-Pro shows anomalously high scores on MMSearch (65.88% vs. Gemini-2.5-Pro's 39.8%), suggesting potential pre-training data contamination rather than genuine capability gains. Future benchmarks need contamination-resistant evaluation.

3. **Answer type expansion** -- Currently restricted to named entities across 10 categories. Extending to numeric answers, dates, and free-form responses would broaden applicability.

4. **Multi-image scenarios** -- The current framework handles single-image inputs. Extending to multi-image reasoning chains is a natural next step.

5. **OCR integration gap** -- No OCR tool was included in data generation (relying on seed VQA data for OCR-dependent examples). Adding OCR earlier in the pipeline could improve text-in-image reasoning diversity.

---

## Authors & Institutions

Xiangyu Peng, Can Qin, An Yan, Xinyi Yang, Zeyuan Chen, Ran Xu, Chien-Sheng Wu -- all from **Salesforce AI Research**.

**Code & Data:** [github.com/SalesforceAIResearch/MTA-Agent](https://github.com/SalesforceAIResearch/MTA-Agent)
