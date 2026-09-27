> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Training the Lead Agent
**In one sentence:** Only the lead agent is trained with Reinforcement Learning (RL, a method that improves behavior from reward signals), while all subagents stay frozen, so training teaches question-driven reasoning rather than document reading.

## Key points
- Only the lead agent is trained and the subagents stay frozen, because finding evidence for a pointed query in a short chunk is simple enough for an off-the-shelf model, while the lead agent still must learn how to act from reasoning history.
- The reward is Reinforcement Learning with Verifiable Reward (RLVR, learning from a checkable correct-or-wrong score): a binary exact-match score of 1 for a correct final answer and 0 otherwise, with no format reward because the lead agent uses the backbone model's native tool-calling format.
- The lead agent is optimized with Group Relative Policy Optimization (GRPO, an RL method that compares several outputs for the same prompt), and observation tokens from subagents are masked so gradients apply only to tokens the lead agent generated.
- The backbones are Qwen3.5-4B and Qwen3.5-9B, and Qwen3.5-4B serves as the subagent for both the 4B and 9B lead agents.
- Core hyperparameters are learning rate 1e-6 with 70 warm-up steps, mini-batch size 128, Proximal Policy Optimization (PPO, a stable policy-update method) clipping epsilon 0.2, Kullback-Leibler (KL, a measure of difference between two policies) coefficient beta 1e-3, and group size 5 rollouts per prompt.
- Training uses 32,768 synthetic HotpotQA samples, each with a 200-paragraph context of about 28K tokens.
- Training runs as fully asynchronous RL on 6 NVIDIA H100 Graphics Processing Units (GPUs, processors used for model computation) plus 10 more H100 GPUs for subagents, using the VERL framework with Megatron backend training and SGLang rollouts.
- With RL, average HotpotQA accuracy rises from 74.42 to 84.57 on Qwen3.5-4B and from 76.24 to 86.79 on Qwen3.5-9B, with matching gains on out-of-distribution 2WikiMultiHopQA.

---
## What is trained and what stays frozen
- Trained: only the lead agent's policy for deciding the next action from reasoning history, such as issuing another query or giving the final answer.
- Frozen: all subagents bound to document chunks, denoted S(D) in the paper's equations.
- Why freezing works: each subagent answers one focused query over one short chunk, which the paper treats as simple enough for a frozen model.
- Why this helps generalization: the lead agent never sees the document directly, so training builds general question-reasoning skill rather than document-specific summary habits; the paper links this to stronger out-of-distribution behavior than memory-writing baselines.

## Reward and learning objective
- Reward: binary exact match between the predicted answer extracted from the trajectory and the gold answer; no extra reward for output format.
- Reason for no format reward: the lead agent uses the backbone's native multi-turn tool-calling format, which the backbone already follows.
- Objective: GRPO maximizes the average clipped advantage over G outputs per prompt, minus a KL penalty against a reference policy.
- In words, the equation has four parts: the importance ratio, which is the current policy probability divided by the old policy probability for each token; clipping, which limits how far one update can move using epsilon; the KL term, which keeps the new policy near the reference policy with weight beta; and the advantage, which is computed from the relative rewards inside each group of outputs.
- Observation masking: findings gathered from frozen subagents are masked out, so the policy gradient touches only lead-agent tokens.

## Training data recipe
- Start from HotpotQA training questions and keep each question's supporting Wikipedia articles as gold evidence.
- Follow the MemAgent Stage I recipe and do not use MemAgent Stage II data.
- Pad each sample with distractor articles from the same HotpotQA corpus until it has 200 paragraphs, about 28K tokens, then shuffle paragraph order with a fixed random seed, following a RULER-style packing procedure.
- Filter out questions solvable without documents: query Qwen3.5-9B in non-thinking mode with no document, take Best-of-3 answers, and discard any question scoring 100% under the rule-based substring and boxed-answer check.
- Process 41,027 HotpotQA training examples this way and keep the first 32,768 remaining samples as the RL training set.

## Hyperparameters and infrastructure
- Optimization: Adam optimizer with learning rate 1e-6, 70 warm-up steps, constant schedule, beta values (0.9, 0.999), weight decay 0.01, gradient clipping 1.0, and PPO mini-batch size 128.
- RL settings: PPO clip range 0.2, entropy coefficient 0, KL coefficient beta 1e-3, and 5 rollouts per prompt with sampling temperature 1.0.
- Turn and length caps in training: at most 9 lead-agent turns, at most 2,048 generated tokens per turn, at most 512 tokens per document chunk, and at most 512 generated tokens per subagent response.
- Subagent behavior: temperature 0.7 and JavaScript Object Notation (JSON, a structured text format) output to simplify aggregation.
- Stack: VERL framework with Megatron backend in bfloat16 precision, SGLang rollout service in fully asynchronous mode, with parallelism settings 1/1/1/1 and parameter, gradient, and optimizer offloading enabled.
- Machines: 6 H100 GPUs for training, split into 4 GPUs for lead-agent rollouts and 2 GPUs for policy updates, plus a separate SGLang cluster of 10 more H100 GPUs for subagents.
- Speed trick: the subagent prompt is ordered as fixed instructions, then assigned chunk, then current query, so the long shared prefix can be reused from Key-Value (KV, stored attention states) cache; SGLang Radix Cache stores the prefix states and a cache-aware router sends each request to the instance with the longest matching prefix.
- Run length: 180 RL steps take about 312 hours for the 4B model and about 400 hours for the 9B model.
- Training uses smaller 512-token chunks than inference, which uses up to 4,096-token chunks and up to 12 turns, because more chunks lower the paper's stated prefill cost and speed up training.

## Training dynamics
- Training reward, averaged over the first versus last ten steps, rises from 44.9% to 83.2% for the 4B lead agent and from 49.8% to 83.3% for the 9B lead agent.
- Mean number of turns moves from 4.65 to 5.04 for 4B and from 4.85 down to 4.12 for 9B.
- Mean lead-agent response length grows from 1.36K to 2.40K tokens for 4B and from 1.47K to 2.48K tokens for 9B.
- For the 9B run, where this was logged, subagent queries per turn rise from 1.06 to 1.62 even though the reward neither penalizes turns nor rewards parallel queries; the paper reads this as an emergent strategy of placing independent queries in the same turn.
- Tool-call format errors over the first ten steps are only 0.22% for 4B and 0.66% for 9B, then approach zero without any format reward.
- The absolute log-perplexity gap between rollout and actor policies stays around 1e-3, at most 1.41e-3, so the paper concludes that asynchronous staleness causes only a small off-policy mismatch.

## With Reinforcement Learning compared to without it
- HotpotQA average accuracy for ParSer without RL versus with RL is 74.42 versus 84.57 on Qwen3.5-4B and 76.24 versus 86.79 on Qwen3.5-9B.
- On out-of-distribution 2WikiMultiHopQA, the corresponding averages are 82.85 versus 87.04 on Qwen3.5-4B and 84.86 versus 88.48 on Qwen3.5-9B.
- Even without RL, ParSer already beats MemAgent and ReMemR1 by a wide margin and stays nearly flat as document length grows, while sequential-memory agents degrade on long inputs.
- The paper attributes the no-RL strength to format match: the lead agent uses the model's native multi-turn tool-calling template, while sequential-memory agents impose a custom memory-update interface the pretrained checkpoint has not seen.

**Covers:** Section 3.3, Section 4.1, Appendices B.1, C.1, E.4-E.5.
