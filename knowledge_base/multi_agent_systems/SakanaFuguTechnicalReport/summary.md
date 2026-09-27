# Sakana Fugu Technical Report

**Paper:** [Sakana Fugu Technical Report (Sakana AI, 2026)](https://arxiv.org/abs/2606.21228)

## Human Readable TL;DR

Different top AI models are good at different things -- one is a great coder, another a great scientist, another a great mathematician. Sakana Fugu is like a smart project manager: instead of doing the work itself, it reads your request and decides on the fly which expert(s) to call in, what to tell them, and how to combine their answers. A fast version (Fugu) picks one expert per request; a slower, more thorough version (Fugu-Ultra) can assemble a whole team with a plan, have them check each other's work, and merge the results -- often beating any single expert model alone.

## TL;DR

Sakana Fugu is a family of trained "orchestrator" LLMs that dynamically construct agentic scaffolds over a pool of frontier worker models (Gemini-3.1-Pro, Claude-Opus-4.8, GPT-5.5) rather than answering directly. **Fugu** attaches a lightweight selection head + singular-value fine-tuning to a backbone LM, trained via supervised fine-tuning (soft worker-ranking distribution) then sep-CMA-ES evolutionary optimization on end-to-end agentic trajectories, to pick one best worker per query at low latency. **Fugu-Ultra** builds on the "Conductor" framework, using GRPO reinforcement learning to output full natural-language agentic workflows (up to 5 steps, arbitrary topologies) with agent isolation and persistent shared memory. Both variants match or exceed the best individual frontier model across coding, reasoning, and scientific benchmarks (e.g., SWE-Bench Pro 73.7 for Fugu-Ultra vs. 69.2 best baseline), demonstrating orchestration as a new, weight-free scaling axis for capability.

---

## Problem & Motivation

Frontier LLMs from different providers increasingly specialize: some excel at math, others at software engineering, others at competitive coding via different strategies (implementing known algorithms vs. combining novel ideas). No single model dominates every domain. Traditional model merging (weight averaging, parameter-space fusion) requires access to model weights and architectural compatibility, making it inapplicable to closed-source, heterogeneous, API-only frontier models. The paper asks: how can the complementary strengths of separately-trained, closed-source models be combined into one system that exceeds any of them individually -- without retraining or weight access, and while remaining a single, simple interface for the user?

---

## Main Original Ideas

1. **Learned orchestration as a model, not a hand-designed scaffold.** Unlike prior multi-agent systems that expose fixed collaboration patterns the user must design/tune, Fugu models are themselves trained LLMs that decide per-query which workers to invoke, what to tell them, and how to merge outputs -- collective intelligence becomes a single callable model interface.

2. **Fugu -- decision-only orchestration for latency.** A lightweight prediction head sits on top of an LM backbone's hidden state and outputs logits scoring which of *L* worker models to dispatch to (single worker per query, no role assignment). Only a small parameter set (the head plus singular-value scales of select backbone weight matrices, via singular-value fine-tuning) is trained, so the system produces a hidden state and routes the query without expensive autoregressive decoding -- keeping orchestration overhead near-zero.

3. **Two-stage training: SFT on soft rankings, then evolutionary refinement on real trajectories.** Stage 1 (SFT) ranks every worker model's performance on each training question via repeated sampling against ground truth, converts the ranking into a soft softmax target distribution (temperature τ), and trains the head + SV-scales to match it via KL divergence -- richer signal than hard-label classification. Stage 2 applies sep-CMA-ES (evolutionary strategy) directly on end-to-end multi-turn agentic trajectories (drawn from real coding-assistant environments like Claude Code, Codex, OpenCode) to maximize terminal task-success reward, which the authors find more stable than further supervised fine-tuning for this stage.

4. **Fugu-Ultra / Conductor -- full workflow generation via RL.** Extends the "Conductor" framework: the orchestrator outputs an entire natural-language *agentic workflow* as a sequence of steps, each specifying a subtask, an assigned worker agent, and an access list of which prior steps' outputs to include in context -- enabling arbitrary topologies (chains, trees, best-of-N, parallel branches). Trained with GRPO using a two-tier reward (0 if the workflow is unparseable, 1 if the executed workflow's final output matches the ground truth, 0.5 otherwise), without KL penalty.

5. **Intra-workflow agent isolation + inter-workflow shared memory.** To prevent "orchestration collapse" (the first agent to touch the environment biases all subsequent agents into following its trajectory), each agent within a single workflow only observes prior outputs through its explicit access list, not the full transcript. But across turns of a multi-turn conversation, agents retain full memory of prior tool calls and artifacts, avoiding redundant re-discovery -- balancing isolation (diversity) against redundancy (efficiency).

6. **Macro-level, weight-free model composition.** Fugu treats frontier models as black boxes and learns to route/coordinate/verify/synthesize their behavior rather than merging weights or activations -- letting it incorporate new closed-source models as they appear, respect provider/privacy/compliance constraints, and scale orchestration as an axis independent of training compute.

---

## Key Findings

**Table 1 -- Model Card (benchmark scores, bold = best, underline = 2nd best):**

| Benchmark | Fugu-Ultra | Fugu | Claude Opus 4.8 | Gemini 3.1 | GPT-5.5 |
|---|---|---|---|---|---|
| SWE Bench Pro | **73.7** | 59.0 | 69.2 | 54.2 | 58.6 |
| Terminal Bench 2.1 | **82.1** | 80.2 | 74.6 | 70.3 | 78.2 |
| LiveCodeBench | **93.2** | 92.9 | 87.8 | 88.5 | 85.3 |
| LiveCodeBench Pro | **90.8** | 87.8 | 84.8 | 82.9 | 88.4 |
| Humanity's Last Exam | **50.0** | 47.2 | 49.8 | 44.4 | 41.4 |
| CharXiv Reasoning | **86.6** | 85.1 | 84.2 | 83.3 | 84.1 |
| GPQA Diamond | 95.5 | **95.5** | 92.0 | 94.3 | 93.6 |
| SciCode | 58.7 | **60.1** | 53.5 | 58.9 | 56.1 |
| τ³ Banking | 20.6 | **21.7** | 20.6 | 8.4 | 20.6 |
| Long Context Reasoning | 73.3 | **74.7** | 67.7 | 72.7 | 74.3 |
| MRCRv2 | 93.6 | 86.6 | 87.9 | 84.9 | **94.8** |

- Fugu-Ultra's gains on SWE-Bench Pro and Terminal Bench 2.1 (~5-6% over next-best) are "consistent with entire generational improvements" among frontier providers (Figure 3).
- Fugu (single-worker, low latency) still beats standalone GPT-5.5 on Terminal Bench by alternating between GPT-5.5 and Claude-Opus-4.8 across a solution's progression.
- Both Fugu variants achieve SOTA on GPQA-Diamond, surpassing even non-public "Mythos Preview" and "Fable 5" model classes purely via orchestration.
- Domain adaptivity: agent routing distributions track known model specializations (GPT-5.5 dominant on Terminal Bench and math sub-questions; Gemini-3.1-Pro dominant on GPQA-Diamond and chemistry/biology).
- **AutoResearch case study** (autonomous ML pipeline optimization, 123 experiments/seed, 3 seeds, single H100): Fugu-Ultra reaches mean best validation BPB **0.9774 ± 0.0019** (best single-seed **0.9748**), vs. Model C 0.9781 ± 0.0011 (0.9766), Model B 0.9793 ± 0.0025 (0.9758), Model A 0.9822 ± 0.0017 (0.9799) -- Fugu-Ultra wins on both mean and best-run, competitive early and pulling ahead mid-training.
- **Classical Japanese kana reading-order recovery** (25 expert-annotated pages, custom benchmark, no prior dataset exists): mean normalized edit distance (NED, higher=better) -- Fugu-Ultra **0.776**, Model A 0.642, Fugu 0.473, Model B 0.449, Model C did not complete the search, seed heuristic baseline 0.116.
- **CAD generation** (mechanical iris mechanism, qualitative): Fugu-Ultra produced a mechanically consistent design (blades rotate around outer pins, opening widens/narrows smoothly); baseline models showed incomplete center coverage, weak linkages, or incomplete closure.
- Qualitative trajectory analysis identifies recurring effective strategies: **debate/aggregation** (tree topologies with a domain-appropriate aggregator, e.g. Gemini for trivia-heavy questions, GPT for math-heavy questions), **build-and-debug** (GPT as builder, Opus as debugger/reviewer, or vice versa), and **bringing in a specialist** (e.g., Opus for a first-pass cryptographic attack, then GPT to re-derive the math from first principles).

---

## Suggestions & Future Directions

1. The authors position **learned orchestration as a new, complementary scaling axis** to raw model scaling -- frontier capability without proportionally larger training runs.
2. Because composition happens at the behavioral/API level, Fugu can **incorporate newly released worker models without retraining**, and agent pools can be configured to respect provider, privacy, or compliance constraints.
3. They speculate this could have **economic and geopolitical effects**, distributing frontier-level capability more broadly across organizations/regions rather than concentrating it in whoever can train the largest models.
4. They explicitly hope the report **encourages further research into multi-agent systems, dynamic query-adaptive agentic scaffolds, and collective intelligence** as a path toward the next frontier of AI capability.
5. No formal limitations section is included in the main text; the paper frames current results as "our evaluations and early user experiences" -- implying this is a first release/first step rather than a mature, fully characterized system.

---

## Authors & Institutions

Yujin Tang (Team & Project Lead), Edoardo Cetin, Jinglue Xu, Qi Sun, Stefan Nielsen, Vincent Richard (core contributors, model), Haruto Goda, Iaroslav Tymchenko, Nhan Nguyen (core contributors, infrastructure), Hyunin Lee, Mari Ashiga, Shashank Kotyan, So Kuroki, Tarin Clanuwat (contributors) -- all Sakana AI.
