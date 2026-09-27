> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiments and Results
**In one sentence:** ParSer was tested on multi-hop Question Answering (QA, questions that need combining facts from several places) from 7K to 896K tokens and stayed accurate at all lengths, beating sequential memory agents and full-context Large Language Models (LLMs, models that read the whole document at once).

## Key points
- Tests use HotpotQA as the in-distribution set (same data family as training) and 2WikiMultiHopQA as the out-of-distribution (OOD, new data family not seen in training) set, with 8 context lengths from 7K to 896K tokens and scores reported as Sub_EM (Substring Exact Match, percent of answers matching the expected substring).
- With the 4B backbone, ParSer averages 84.6% on HotpotQA, which is +5.7 points over the strongest sequential baseline (ReMemR1 at 78.9%), and the gap grows to +12.0 points at 896K tokens (85.4% vs 73.4%).
- With the 9B backbone, ParSer averages 86.8% on HotpotQA, which is +6.7 points over the strongest sequential baseline (MemAgent at 80.1%), and the gap grows to +9.9 points at 896K tokens (85.9% vs 76.0%).
- The 9B ParSer average of 86.8% beats DeepSeek-V4-Pro (a model with a native 1M-token context) by 6.3 points on HotpotQA (DeepSeek think-max averages 80.5%).
- Accuracy stays nearly flat for ParSer across lengths, while full-context reading drops sharply: for example, Qwen3.5-4B full-context non-thinking falls from 75.8% at 7K to 34.4% at 896K on HotpotQA, and sequential methods also fall by 6-9 points over the same range.
- OOD robustness is uneven for baselines but not for ParSer: on 2WikiMultiHopQA, MemAgent 4B averages only 60.6% and ReMemR1 4B averages 77.4% (down from 78.6% and 78.9% in-distribution), while ParSer 4B averages 87.0%, higher than its own in-distribution average of 84.6%.
- For each trained method, the authors pick the checkpoint (saved model version) with the best in-distribution overall score and report the average over 3 runs.

---
## Evaluation setup
Datasets are HotpotQA (in-distribution) and 2WikiMultiHopQA (OOD). Training uses HotpotQA only, with 32,768 samples of 200 paragraphs each (about 28K tokens).

Evaluation reuses the same 128 questions across 8 length settings per benchmark: 50, 100, 200, 400, 800, 1600, 3200, and 6400 paragraphs, or about 7K to 896K tokens. HotpotQA test sets are reused from MemAgent. 2WikiMultiHopQA test sets are regenerated with the public ReMemR1 script, which loads 2WikiMultiHopQA, keeps supporting-fact evidence, pads with random distractor paragraphs, and shuffles paragraphs.

The metric is Sub_EM (Substring Exact Match), following prior work. For each training-based method, the checkpoint with the best in-distribution overall performance is selected, and the reported score is the average over 3 runs.

## Baselines
Two groups of baselines are compared.

Full-context LLMs (models that take the whole document plus the question as one input): Qwen3.5 and DeepSeek-V4-Pro (preview 2026-04-24, native 1M-token context, reasoning effort set to Max). Qwen3.5 uses its default setup within its native 262K-token window; beyond that, YaRN (a scaling method for Rotary Position Embedding (RoPE), the position system inside the model) with factor 4.0 extends it to about 1M tokens. Generation temperature is 0. Full-context answering uses a two-turn format: first the document plus question with optional thinking, then a short follow-up asking for only the concise final answer, because thinking models often break strict answer formatting after long reasoning.

Sequential memory agents (agents that read the document chunk by chunk while rewriting a small memory): MemAgent and ReMemR1. They are reimplemented under the same training data and backbone models as ParSer, reusing the training settings from their original papers, with rollout group size reduced (8 instead of 16) to control cost.

## Results on HotpotQA (in-distribution)
Values are Sub_EM accuracy in percent. Columns show the average plus selected lengths; the full Table 1 has all 8 lengths from 7K to 896K. Best in each Qwen backbone block is ParSer.

| Method (HotpotQA) | Avg. | 7K (50) | 224K (1600) | 448K (3200) | 896K (6400) |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Pro non-think | 75.1 | 78.1 | 75.8 | 73.4 | 62.5 |
| DeepSeek-V4-Pro think-max | 80.5 | 82.0 | 81.2 | 77.3 | 78.9 |
| Qwen3.5-4B full-context non-think | 64.4 | 75.8 | 61.7 | 53.1 | 34.4 |
| Qwen3.5-4B full-context think | 65.8 | 80.5 | 60.9 | 46.1 | 31.2 |
| Qwen3.5-4B MemAgent | 78.6 | 81.2 | 79.7 | 74.0 | 72.9 |
| Qwen3.5-4B ReMemR1 | 78.9 | 82.0 | 80.0 | 77.1 | 73.4 |
| Qwen3.5-4B ParSer | 84.6 | 85.7 | 83.1 | 83.1 | 85.4 |
| Qwen3.5-9B full-context non-think | 66.8 | 75.0 | 65.6 | 58.6 | 47.7 |
| Qwen3.5-9B full-context think | 68.8 | 77.3 | 65.6 | 53.9 | 46.9 |
| Qwen3.5-9B MemAgent | 80.0 | 81.8 | 81.2 | 79.7 | 75.0 |
| Qwen3.5-9B ReMemR1 | 78.4 | 81.2 | 78.1 | 77.9 | 76.0 |
| Qwen3.5-9B ParSer | 86.8 | 86.7 | 86.7 | 86.7 | 85.9 |

ParSer leads every column on HotpotQA. The 4B gaps over the strongest sequential baseline are +5.7 on average and +12.0 at 896K. The 9B gaps are +6.7 on average and +9.9 at 896K. Full-context methods fall steeply with length, while sequential agents fall moderately and ParSer stays nearly flat.

## Results on 2WikiMultiHopQA (out-of-distribution)
Values are Sub_EM accuracy in percent. ParSer leads the long-document columns (1600 paragraphs / 224K tokens and above) on 2WikiMultiHopQA.

| Method (2WikiMultiHopQA) | Avg. | 7K (50) | 224K (1600) | 448K (3200) | 896K (6400) |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Pro non-think | 83.0 | 89.8 | 77.3 | 78.9 | 68.8 |
| DeepSeek-V4-Pro think-max | 88.2 | 90.6 | 87.5 | 82.8 | 80.5 |
| Qwen3.5-4B full-context non-think | 73.7 | 85.9 | 69.5 | 66.4 | 46.9 |
| Qwen3.5-4B full-context think | 75.5 | 88.3 | 70.3 | 63.3 | 39.1 |
| Qwen3.5-4B MemAgent | 60.6 | 67.4 | 54.4 | 60.2 | 45.1 |
| Qwen3.5-4B ReMemR1 | 77.4 | 88.5 | 67.7 | 72.4 | 60.7 |
| Qwen3.5-4B ParSer | 87.0 | 87.0 | 85.9 | 88.3 | 87.0 |
| Qwen3.5-9B full-context non-think | 73.7 | 80.5 | 78.9 | 61.7 | 50.0 |
| Qwen3.5-9B full-context think | 79.6 | 88.3 | 82.8 | 57.8 | 52.3 |
| Qwen3.5-9B MemAgent | 73.7 | 80.7 | 65.6 | 75.8 | 60.9 |
| Qwen3.5-9B ReMemR1 | 79.3 | 84.1 | 74.7 | 79.4 | 70.6 |
| Qwen3.5-9B ParSer | 88.5 | 87.8 | 89.6 | 88.5 | 88.0 |

## Out-of-distribution story
MemAgent and ReMemR1 do far worse on the OOD set than on the in-distribution set, while ParSer holds up. For example, MemAgent 4B drops from 78.6% (HotpotQA average) to 60.6% (2WikiMultiHopQA average). ReMemR1 4B is strong at short OOD lengths (88.5% at 7K) but falls to 60.7% at 896K. ParSer 4B averages 87.0% OOD versus 84.6% in-distribution, and ParSer 9B averages 88.5% OOD versus 86.8% in-distribution. The paper links this to design: only the lead agent is trained and it never sees the raw document directly, so it learns general question-reasoning steps instead of document-specific summary habits that overfit the training data.

## Why stability happens
Full-context reading degrades because a single pass over a very long input misses middle evidence and attention cost grows fast with length. Sequential memory agents improve on this but still depend on the order in which chunks enter a small fixed memory, so evidence can be overwritten before it is needed. ParSer instead gives every chunk the same query in parallel each round and lets the lead agent ask follow-up queries based on what came back, so finding evidence does not depend on where it sits or how far apart the pieces are. For the controlled tests of evidence position, order, and distance, see the Analysis page in this wiki.
**Covers:** Sections 4.2-4.3, Table 1, Appendices C.2, D.
