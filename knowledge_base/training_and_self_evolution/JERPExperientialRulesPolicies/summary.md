# Joint Learning of Experiential Rules and Policies for Large Language Model Agents

**Paper:** [Joint Learning of Experiential Rules and Policies for Large Language Model Agents (Ye & Yu, 2026)](https://arxiv.org/abs/2606.27136)

## Human Readable TL;DR

Imagine an apprentice who both writes sticky notes to themselves ("always turn on the desk lamp before checking a drawer") and slowly gets better at the job through practice. Most AI agent training does only one of these: either it keeps a notebook of tips without changing the apprentice's underlying skill, or it trains the skill directly and throws away the notebook. This paper trains both at once from the exact same work session -- the agent updates its "skill" (model weights) and its "notebook" (a pool of natural-language rules) from the same batch of attempts, so the notes never go stale relative to how good the apprentice has become.

## TL;DR

JERP (Joint Learning of Experiential Rules and Policies) couples group-relative reinforcement learning (GRPO-style) with a dynamically maintained natural-language experiential-rule pool, updating both from the same sampled trajectory group each training episode. Rules are retrieved by utility score and injected into the prompt alongside task and history; after each episode, an LLM-based contrastive-reflection step edits the rule pool (ADD/EDIT/UPVOTE/DOWNVOTE/MERGE) by comparing current rollouts against accumulated successful trajectories. On AlfWorld and WebShop, JERP beats Vanilla LLM, ReAct, Reflexion, RLOO, and GRPO baselines, with the largest gains on task categories requiring longer action sequences and more intermediate constraints (Clean, Heat, Cool, Pick2).

---

## Problem & Motivation

LLM agents in multi-step interactive environments (web navigation, embodied tasks, tool use) accumulate experience across episodes, and prior work exploits this experience in one of two disconnected ways:

- **Prompt-based rule reuse** (Reflexion, ExpeL, AutoGuide, AutoManual): externalize experience as natural-language rules/reflections fed back as context. Easy to inspect and edit, but the rules only help if the *current* policy can interpret them -- as the policy changes during training, static rules can fall out of sync or become misleading.
- **Parameter updates via RL fine-tuning** (PPO, GRPO, DPO, GiGPO): improve the policy broadly through gradient updates, but reward in interactive tasks is often sparse, so local, specific mistakes may not get timely, targeted correction.

The paper's core question: can the *same* interaction trajectories drive both mechanisms simultaneously, so the rule pool stays aligned with the evolving policy while durable behaviors gradually get absorbed into the model itself?

---

## Main Original Ideas

1. **Joint training objective over policy and rule pool.** JERP defines the learning problem as optimizing both policy parameters θ and a per-task rule pool K jointly (Eq. 6), rather than treating rule extraction as a fixed preprocessing step. The same sampled trajectory group `T_d` feeds two separate updates each episode: a GRPO-style parameter update and a rule-pool update (Eqs. 10-12).

2. **Score-ranked working rule set.** Each task maintains a long-term rule pool `K(d) = {(z_i, s_i)}` of (rule text, utility score) pairs. Before each episode, the top-k rules by score are selected as the working set `K̃(d)` and injected into the prompt alongside the task description and interaction history -- no finer-grained per-instance retrieval is used.

3. **Contrastive-reflection rule updating.** After each episode, an LLM (frozen weights) compares the current trajectory group against a pool of previously accumulated *successful* reference trajectories for the same task and emits structured edit operations: `ADD(z)`, `EDIT(q,z)`, `UPVOTE(q)`, `DOWNVOTE(q)`, `MERGE(Q,z)`. This is the mechanism (extending ExpeL-style reflection) that keeps the rule pool synchronized with the current policy instead of drifting stale.

4. **Merge operation for pool hygiene.** Unlike prior reflection-based memory methods that mostly append, JERP explicitly merges semantically overlapping rules and prunes low-utility ones below a threshold, keeping the pool bounded as training proceeds online.

5. **Shared advantage estimation reused from GiGPO.** Trajectory-level rewards (only available at episode termination) are standardized within the sampled group to form group-relative advantages, applied uniformly across all timesteps of a trajectory (Eq. 19), inside a clipped PPO-style surrogate with a KL penalty against a reference policy.

---

## Key Findings

**Table II -- AlfWorld (task success rate %) and WebShop (avg. score / success rate %):**

| Method | Pick | Look | Clean | Heat | Cool | Pick2 | AlfWorld All | WebShop Score | WebShop Success |
|---|---|---|---|---|---|---|---|---|---|
| Vanilla LLM | 5.9 | 5.5 | 3.3 | 9.7 | 4.2 | 0.0 | 4.1 | 23.1 | 5.2 |
| ReAct | 17.4 | 20.5 | 15.7 | 6.2 | 7.7 | 2.0 | 12.8 | 40.1 | 11.3 |
| Reflexion | 35.3 | 22.2 | 21.7 | 13.6 | 19.4 | 3.7 | 21.8 | 55.8 | 21.9 |
| RLOO (+LoRA) | 71.5 | 68.3 | 61.2 | 34.4 | 41.0 | 19.9 | 48.7 | 71.9 | 57.8 |
| GRPO (+LoRA) | 78.5 | 73.3 | 50.7 | 62.7 | 51.7 | 33.9 | 57.8 | 78.1 | 56.2 |
| **JERP (+LoRA)** | 72.2 | 69.8 | **65.4** | **67.4** | **60.1** | **42.5** | **61.5** | **79.0** | **64.1** |

- JERP wins overall on both benchmarks (61.5% AlfWorld-All, 79.0 WebShop score, 64.1% WebShop success), but GRPO stays higher on the simpler Pick and Look categories -- JERP's edge is concentrated on Clean, Heat, Cool, and Pick2, the categories needing longer action sequences and more intermediate constraints.
- **Ablation (Fig. 3):** freezing the rule pool after its initial update (vs. continuously revising it) noticeably slows mid-to-late training improvement on AlfWorld, confirming that *continual* rule-pool updating -- not just having rules at all -- drives the gain.
- Training curves (Fig. 4) show JERP and GRPO tracking closely early on, with JERP pulling ahead in the middle/late training stages specifically on the longer-horizon task types.
- Vanilla LLM's near-floor performance (4.1% / 5.2%) establishes that all gains come from how methods exploit interaction experience, not from the base model's raw capability.

**Setup:** LoRA (rank 64) fine-tuning on 4x NVIDIA A30 GPUs; learning rate 3e-6; group sampling size 8; results averaged over 3 runs.

---

## Suggestions & Future Directions

1. Explore more adaptive rule-retrieval strategies beyond the current score-ranked top-k selection (the paper explicitly notes this is an implementation choice, not a claim of general superiority over instance-level retrieval).
2. Extend the joint rule/policy learning framework to multi-agent interactive settings.
3. (Implicit limitation) Rule-pool maintenance depends on an LLM-based contrastive-reflection step and accumulated successful trajectories per task instance -- performance in tasks with very sparse or rare successes is not separately analyzed.

---

## Authors & Institutions

Shicheng Ye (Sun Yat-sen University), Chao Yu (Sun Yat-sen University, corresponding author).
