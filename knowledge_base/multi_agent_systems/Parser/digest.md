> [[index|Wiki]] | [[summary|Summary]]

# PARSER: Read in Parallel, Reason in Depth — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-problem-and-motivation|Problem and Motivation]]
**In one sentence:** Long documents fail not because models lack room, but because one-by-one reading ties the order of the document to the order of thinking, so the paper argues reading and reasoning must be separated.
- **Context rot (a steady loss of accuracy as input grows) is real:** direct full-context answering drops by tens of points as documents grow from 77K to 896K tokens, even for million-token models.
- **Positional bias (ignoring the middle of the input) is one cause:** evidence placed away from the start or end boundaries is systematically ignored.
- **Sequential memory couples traversal to reasoning:** the agent reads chunk by chunk and compresses each new chunk plus the old memory into a new memory, and answers only from the final memory.
- **Constraint 1 — evidence-placement sensitivity:** because each chunk is judged before later chunks are seen, accuracy depends on absolute position, logical order, and distance between evidence pieces.
- **Constraint 2 — linear latency (waiting time that grows in direct proportion to length):** chunk T cannot start until chunk T-1 finished, so T chunks need T dependent steps in a row.
- **Decoupling thesis:** document order is imposed by the document, question order is imposed by the question, and the paper proposes to read all chunks in parallel width while keeping only reasoning sequential in depth.

## 2. [[wiki/02-scatter-gather-method|Scatter-Gather Method]]
**In one sentence:** PARSER splits a long document into chunks with one frozen reader per chunk, and a lead agent that never sees the raw text finds answers by repeating scatter-gather rounds where one query goes to all chunks in parallel and only the few returned findings shape the next step.
- The document is split into T fixed-size chunks, and a bank of T subagents is created with exactly one subagent bound to each chunk, while only the lead agent is trained and the subagents stay frozen.
- The lead agent receives only the question and never receives the full document or any raw chunk tokens, so it reasons about the question and the gathered findings instead of reading the document itself.
- Each scatter-gather round follows the same pattern: the lead agent scatters one or more focused queries, all chunk readers run at the same time, and their local findings are gathered into one observation for the lead agent.
- Reasoning depth scales with K rounds rather than T chunks, so adding more chunks adds parallel readers instead of longer chains of dependent steps.
- Every chunk is read symmetrically under the same query in every round, so access to evidence does not depend on chunk position and no chunk is discarded after a single pass.
- Most chunks are irrelevant to a given query, so subagents may abstain, and abstentions are dropped during gathering, which keeps communication sparse.
- Cross-chunk dependencies are not solved inside one chunk read but across successive rounds, because findings from round k enter the lead agent context and shape the query in round k+1.

## 3. [[wiki/03-training-lead-agent|Training the Lead Agent]]
**In one sentence:** Only the lead agent is trained with Reinforcement Learning (RL, a method that improves behavior from reward signals), while all subagents stay frozen, so training teaches question-driven reasoning rather than document reading.
- Only the lead agent is trained and the subagents stay frozen, because finding evidence for a pointed query in a short chunk is simple enough for an off-the-shelf model, while the lead agent still must learn how to act from reasoning history.
- The reward is Reinforcement Learning with Verifiable Reward (RLVR, learning from a checkable correct-or-wrong score): a binary exact-match score of 1 for a correct final answer and 0 otherwise, with no format reward because the lead agent uses the backbone model's native tool-calling format.
- The lead agent is optimized with Group Relative Policy Optimization (GRPO, an RL method that compares several outputs for the same prompt), and observation tokens from subagents are masked so gradients apply only to tokens the lead agent generated.
- The backbones are Qwen3.5-4B and Qwen3.5-9B, and Qwen3.5-4B serves as the subagent for both the 4B and 9B lead agents.
- Core hyperparameters are learning rate 1e-6 with 70 warm-up steps, mini-batch size 128, Proximal Policy Optimization (PPO, a stable policy-update method) clipping epsilon 0.2, Kullback-Leibler (KL, a measure of difference between two policies) coefficient beta 1e-3, and group size 5 rollouts per prompt.
- Training uses 32,768 synthetic HotpotQA samples, each with a 200-paragraph context of about 28K tokens.
- Training runs as fully asynchronous RL on 6 NVIDIA H100 Graphics Processing Units (GPUs, processors used for model computation) plus 10 more H100 GPUs for subagents, using the VERL framework with Megatron backend training and SGLang rollouts.
- With RL, average HotpotQA accuracy rises from 74.42 to 84.57 on Qwen3.5-4B and from 76.24 to 86.79 on Qwen3.5-9B, with matching gains on out-of-distribution 2WikiMultiHopQA.

## 4. [[wiki/04-experiments-results|Experiments and Results]]
**In one sentence:** ParSer was tested on multi-hop Question Answering (QA, questions that need combining facts from several places) from 7K to 896K tokens and stayed accurate at all lengths, beating sequential memory agents and full-context Large Language Models (LLMs, models that read the whole document at once).
- Tests use HotpotQA as the in-distribution set (same data family as training) and 2WikiMultiHopQA as the out-of-distribution (OOD, new data family not seen in training) set, with 8 context lengths from 7K to 896K tokens and scores reported as Sub_EM (Substring Exact Match, percent of answers matching the expected substring).
- With the 4B backbone, ParSer averages 84.6% on HotpotQA, which is +5.7 points over the strongest sequential baseline (ReMemR1 at 78.9%), and the gap grows to +12.0 points at 896K tokens (85.4% vs 73.4%).
- With the 9B backbone, ParSer averages 86.8% on HotpotQA, which is +6.7 points over the strongest sequential baseline (MemAgent at 80.1%), and the gap grows to +9.9 points at 896K tokens (85.9% vs 76.0%).
- The 9B ParSer average of 86.8% beats DeepSeek-V4-Pro (a model with a native 1M-token context) by 6.3 points on HotpotQA (DeepSeek think-max averages 80.5%).
- Accuracy stays nearly flat for ParSer across lengths, while full-context reading drops sharply: for example, Qwen3.5-4B full-context non-thinking falls from 75.8% at 7K to 34.4% at 896K on HotpotQA, and sequential methods also fall by 6-9 points over the same range.
- OOD robustness is uneven for baselines but not for ParSer: on 2WikiMultiHopQA, MemAgent 4B averages only 60.6% and ReMemR1 4B averages 77.4% (down from 78.6% and 78.9% in-distribution), while ParSer 4B averages 87.0%, higher than its own in-distribution average of 84.6%.
- For each trained method, the authors pick the checkpoint (saved model version) with the best in-distribution overall score and report the average over 3 runs.

## 5. [[wiki/05-analysis-limits|Analysis, Cost, and Limits]]
**In one sentence:** ParSer stays flat when evidence position, order, or distance is perturbed and is much faster than sequential memory at long contexts, but it pays for this with a parallel subagent bank and can still fail when a subagent returns a confident but wrong local finding.
- Controlled tests on 894K-token documents varied evidence position (percentile bins), logical order (logical vs reversed), and separation (distractor paragraphs between two evidence pieces): MemAgent (a sequential memory agent) and ReMemR1 (MemAgent plus a callback that revisits earlier memory) swung or degraded, while ParSer stayed nearly flat.
- At 896K tokens and concurrency 1 (one request at a time), amortized time per sample was about 876s for MemAgent vs about 78s for ParSer (about 11x); at concurrency 16 (16 requests at once) it was about 102s vs about 59s (about 1.7x).
- Prefill (the first pass that reads the input) cost falls from O(n squared) for full-context reading to O(n squared / c) with c chunks; decoding (step-by-step output generation) savings come from far fewer generated tokens.
- Larger subagents help only up to a point: with the lead agent fixed, average score went from 78.26% (2B subagent) to 84.57% (4B default) and then flattened at 84.77% (9B).
- Smaller chunks win: the 4,096-token chunk default averaged 84.57%, while a single full-document subagent averaged 73.76% and fell to 53.13% at 896K; larger chunks (16K, 65K, 131K tokens) scored progressively lower.
- The same lead agent works without retraining with other subagent types: lead plus DCI (Direct Corpus Interaction, agents that search raw text with shell tools such as rg and grep) subagents beat standalone DCI, and lead plus thinking subagents beat full-context thinking.
- Known failure mode is context isolation: in Appendix F.2 the lead agent accepted "Prince Nicholas of Greece and Denmark" from a chunk about a different Elena instead of the correct "Prince Archil of Imereti", because subagents see only the query plus their chunk and the lead agent cannot check the subagent source text.

## 6. [[wiki/targeted|Targeted Analysis: PARSER Deep Dive]]
**In one sentence:** This page answers four concrete questions about PARSER (Parallel Reading, Sequential Reasoning, a method where many small readers scan document chunks at the same time while one lead agent reasons step by step): how a scatter-gather round works, why frozen subagents help training, where the long-context wins come from, and what the subagent bank costs.
- A scatter-gather round is a fixed loop: the lead agent thinks, scatters one query to all chunk readers in parallel, gathers their findings as one observation, and either answers or asks a deeper follow-up question conditioned on what came back.
- Freezing the subagents helps training because it concentrates all learnable behavior in one place (the lead agent), keeps training cost independent of document length, and stops the system from overfitting to training-document summaries.
- The 896K-token wins come from three structural differences, not a bigger model: every chunk is re-read under every query (no position bias), queries follow the question's logic instead of document order (no order/distance penalty), and accuracy stays flat while sequential memories degrade.
- The subagent bank trades weaker per-chunk readers and extra parallel compute for much lower waiting time: at 896K tokens it answers in about 78 seconds instead of about 876 seconds, with most chunk replies being short abstentions that are dropped before aggregation.
- The price is real: every round fans out to all T readers at once (the paper deploys subagents on 10 extra H100 Graphics Processing Units, processors used for model computation), prefill compute can stay flat or grow without cache reuse, and a confident-but-wrong local finding can mislead the lead agent.
- Bottom line for practice: PARSER fits multi-hop Question Answering (QA, questions that need combining facts from several places) over very long, scattered evidence where reasoning depth is small but document length is huge; it is overkill for short documents or single-fact lookup.

## The argument in five moves
1. One-by-one reading ties document order to thinking order.
2. Scatter one query to all chunks in parallel, then gather findings.
3. Train only the lead agent to reason from gathered findings.
4. Accuracy stays flat to 896K while baselines degrade.
5. Flatness comes from position-, order-, and distance-invariance.
6. Speed comes from K rounds replacing T sequential steps, at the price of a parallel subagent bank and context isolation.
