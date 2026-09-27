# PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents

**Paper:** [PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents (Li, Qiu, Zhang, King, Meng, 2026)](https://arxiv.org/html/2609.06702)

## Human Readable TL;DR
Imagine a very long report split into pages, with one helper holding each page and one coordinator who only knows the question.
The coordinator shouts one focused question to all helpers at once, collects the few useful answers, then shouts a better follow-up question based on what came back.
This repeats for a few scatter-gather rounds until the coordinator has enough to answer.
Because all pages are checked in parallel every round, no clue is lost in the middle and long reports take little extra waiting time.

## TL;DR
PARSER (Parallel Reading, Sequential Reasoning) is a Long-Context Large Language Model (LLM, a text model trained to read and generate language) agent that splits a document into chunks with one frozen reader per chunk and one trained lead agent that never sees raw text.
The lead agent reasons across a few scatter-gather rounds: it scatters one query to all chunk readers in parallel, gathers their findings, and conditions the next query on them.
Only the lead agent is trained with Reinforcement Learning (RL, learning from right-or-wrong answer rewards); subagent outputs are masked from the update.
With a 4B (4-billion-parameter) backbone it averages 84.6% on HotpotQA, +5.7 points over the strongest sequential baseline, and with a 9B backbone it averages 86.8%, staying nearly flat out to 896K tokens.

---

## Problem & Motivation

Long documents fail not because models lack room, but because one-by-one reading ties the order of the document to the order of thinking.

- **Context rot (steady accuracy loss as input grows) is real:** direct full-context answering on multi-hop Question Answering (QA, questions that need combining facts from several places) drops by tens of points from 77K to 896K tokens, even for million-token models. For example, Qwen3.5-4B full-context falls from 75.8% at 7K to 34.4% at 896K.
- **Positional bias (ignoring the middle of the input) is one cause:** evidence away from the start or end is systematically underused.
- **Sequential memory couples traversal to reasoning:** agents such as MemAgent (a sequential memory agent) read chunk by chunk, merging each new chunk plus old memory into new memory, and answer only from the final memory. ReMemR1 (MemAgent plus a callback that revisits earlier memory) and GRU-Mem (a gated-memory variant named after Gated Recurrent Unit, a gated memory idea) keep the same core rule.
- **Constraint 1 — evidence-placement sensitivity:** each chunk is judged before later chunks are seen, so accuracy depends on absolute position, logical order, and distance between evidence pieces.
- **Constraint 2 — linear latency (waiting time growing in direct proportion to length):** chunk T cannot start until chunk T-1 finished, so T chunks need T dependent steps in a row.
- **Decoupling thesis:** document order is imposed by the document, question order is imposed by the question, so the paper reads all chunks in parallel width while keeping only reasoning sequential in depth.

---

## Main Original Ideas

1. **Scatter-gather reading loop** — The lead agent repeats scatter-gather rounds: think about what is missing, scatter one focused query to all chunk readers at the same time, gather their local findings into one observation, then either answer or ask a deeper follow-up. Reasoning depth scales with K rounds (K <= 9 in training, <= 12 in inference) rather than T chunks, so longer documents add parallel readers, not longer waiting chains.

2. **Frozen per-chunk subagent bank** — The document is split into T fixed-size chunks (512 tokens in training, 4096 tokens in inference), with exactly one reader bound to each chunk. Readers stay frozen and run in non-thinking mode, returning either a short structured finding or `Unknown` for abstain. Only the lead agent is trained, so training teaches question-driven reasoning rather than document reading.

3. **Question-driven reasoner that never sees raw text** — The lead agent receives only the question plus gathered findings, never full-document tokens. It works in a Reasoning and Acting (ReAct, alternating thinking and acting) loop with a `query_agents` tool call or a final `<answer>` block. Cross-chunk links are rebuilt across scatter rounds: findings from round k shape the query in round k+1.

4. **Sparse abstention gathering** — Most chunks are irrelevant to a given query, so most subagents abstain and their replies are dropped before aggregation. Each scatter round therefore adds only a small set of findings to the lead context, unlike sequential memory which writes a memory update after every chunk even when most chunks are empty.

5. **RLVR (Reinforcement Learning with Verifiable Reward, learning from a checkable correct-or-wrong score) training with observation masking** — Reward is binary Exact Match (1 for correct final answer, 0 otherwise) with no format reward, optimized with Group Relative Policy Optimization (GRPO, an RL method that compares several outputs for the same prompt). Subagent observation tokens are masked so gradients apply only to lead-agent tokens. Training uses 32,768 synthetic HotpotQA samples of about 28K tokens each.

---

## Key Findings

Scores are Sub_EM (Substring Exact Match, percent of answers matching the expected substring) on HotpotQA unless noted. Best in each block is bold.

| Method (HotpotQA) | Avg. 7K-896K | 7K | 224K | 448K | 896K |
| --- | --- | --- | --- | --- | --- |
| Qwen3.5-4B full-context non-think | 64.4 | 75.8 | 61.7 | 53.1 | 34.4 |
| Qwen3.5-4B MemAgent | 78.6 | 81.2 | 79.7 | 74.0 | 72.9 |
| Qwen3.5-4B ReMemR1 | 78.9 | 82.0 | 80.0 | 77.1 | 73.4 |
| **Qwen3.5-4B ParSer** | **84.6** | **85.7** | **83.1** | **83.1** | **85.4** |
| DeepSeek-V4-Pro think-max | 80.5 | 82.0 | 81.2 | 77.3 | 78.9 |
| Qwen3.5-9B MemAgent | 80.1 | 81.8 | 81.2 | 79.7 | 75.0 |
| Qwen3.5-9B ReMemR1 | 78.4 | 81.2 | 78.1 | 77.9 | 76.0 |
| **Qwen3.5-9B ParSer** | **86.8** | **86.7** | **86.7** | **86.7** | **85.9** |

- **4B backbone:** ParSer averages 84.6%, +5.7 points over the strongest sequential baseline ReMemR1 at 78.9%. The gap grows to +12.0 at 896K tokens (85.4% vs 73.4%).
- **9B backbone:** ParSer averages 86.8%, +6.7 points over the strongest sequential baseline MemAgent at 80.1%. The gap grows to +9.9 at 896K tokens (85.9% vs 76.0%).
- **Beats large full-context model:** 9B ParSer at 86.8% beats DeepSeek-V4-Pro think-max (a model with native 1M-token context) at 80.5% by 6.3 points.
- **Flat vs degrading:** ParSer stays nearly flat across 7K to 896K while full-context and sequential methods fall 6-40 points.
- **Out-of-Distribution (OOD, new data family not seen in training) robustness:** on 2WikiMultiHopQA, ParSer-4B averages 87.0% vs MemAgent 60.6%, and even above its own in-distribution 84.6%. ReMemR1-4B averages 77.4% OOD. ParSer-9B averages 88.5% OOD vs 86.8% in-distribution.
- **Latency (waiting time):** at 896K tokens and concurrency 1 (one request at a time), about 876s per sample for MemAgent vs about 78s for ParSer (about 11x faster). At concurrency 16 (16 requests at once), about 102s vs about 59s (about 1.7x). Short 7K documents still favor plain full-context reading.
- **Controlled perturbation tests at 894K tokens:** ParSer stays flat when evidence position, logical order, or separation distance is varied, while MemAgent and ReMemR1 swing or degrade.
- **Ablation (removing one part to test its effect) — subagent size:** with lead fixed, HotpotQA average goes 78.26% (2B subagent) to 84.57% (4B default) then flattens at 84.77% (9B), so cheap 4B readers are enough.
- **Ablation — chunk size:** 4,096-token chunks average 84.57%; a single full-document subagent averages 73.76% and falls to 53.13% at 896K; larger 16K/65K/131K chunks score progressively lower.
- **Ablation — RL on vs off:** without RL 74.42% vs with RL 84.57% on 4B, and 76.24% vs 86.79% on 9B. Even without RL, ParSer already beats MemAgent and ReMemR1 and stays flat with length.
- **Alternative readers without retraining:** lead plus DCI (Direct Corpus Interaction, agents that search raw text with shell tools such as rg and grep) subagents averages 84.67% vs standalone DCI 75.61%; lead plus thinking subagents averages 85.55% vs full-context thinking 65.82%.

---

## Suggestions & Future Directions

1. **Fix context isolation errors:** the known failure mode is a confident-but-wrong local finding misleading the lead agent (for example accepting "Prince Nicholas of Greece and Denmark" from a chunk about a different Elena instead of "Prince Archil of Imereti"). Future work could pass short source passages for verification or add a cross-check query round.
2. **Reduce the parallel hardware price:** scatter-gather rounds fan out to all T readers each round (paper uses 10 extra H100 Graphics Processing Units, processors used for model computation, for subagents plus 6 for training). Explore selective routing so only likely chunks are queried in later rounds.
3. **Handle Key-Value (KV, stored attention states) cache eviction:** without cache reuse across rounds, repeated full-document reads raise input-reading cost from O(n squared / c) toward O(K times n squared / c). Better prefix caching with SGLang (a model serving framework) routing or fewer rounds would protect the latency lead at high concurrency.
4. **Tune chunk size per task:** chunking is load-bearing — removing it causes a large long-document drop. Adaptive or overlapping chunks could help tasks where evidence spans chunk boundaries.
5. **Test beyond multi-hop QA:** current wins are on HotpotQA and 2WikiMultiHopQA with short answers and a few reasoning hops. Extend to summarization, code, or agent tasks where reasoning depth K may be larger.
6. **Learn when to stop scattering:** mean scatter rounds sit near 4-5 and queries per turn rise emergently from 1.06 to 1.62 during RL. An explicit stop/skip policy could save fan-out cost on short documents where plain full-context reading already wins.

---

## Authors & Institutions

Kun Li, Zexuan Qiu, Tianhua Zhang, Irwin King, Helen Meng — The Chinese University of Hong Kong, September 2026. arXiv 2609.06702.
