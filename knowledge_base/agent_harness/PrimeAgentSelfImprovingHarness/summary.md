# Prime Agent: A Self-Improving RLM Harness

**Paper:** [Prime Agent: A Self-Improving RLM Harness (Karten et al., 2026)](https://arxiv.org/abs/2608.23552)

## Human Readable TL;DR

A language model on its own is like a smart person who can only remember what's currently written on their desk — it can't reliably keep track of long tasks, past mistakes, or its own useful tricks. Prime Agent is scaffolding built around a model that gives it a permanent notebook (a Continual Harness), a coding sandbox it can keep working in across turns (a persistent REPL), and the ability to spin up helper copies of itself that talk to each other and to a human supervisor. The point isn't to make the model smarter — it's to stop the surrounding software from causing failures that get mistaken for the model's fault. With this scaffolding, the same models solve interactive puzzle games at close to human level, run week-long research and factory-building sessions without losing track of state, and get more done per dollar than existing coding-agent tools.

## TL;DR

Prime Agent is an open-source harness for long-horizon LLM agent evaluation and coding workflows. It organizes agent state into four levels (L0 model weights, L1 active context, L2 persistent REPL/subagents, L3 disk-backed history/memories/skills), implements the Recursive Language Model (RLM) abstraction via an asynchronous `rlm` primitive that spawns handle-returning subagent sessions, and layers a Continual Harness on top that converts trajectory evidence into versioned, roll-backable prompt notes, memories, skills, and subagent specs — self-improvement without weight updates. Standardized execution, recovery, verification, and resource accounting aim to push measured performance toward a model's true maximal capability rather than the harness's limitations. Prime Agent raises ARC-AGI-3 RHAE Best@1 from 30% to 95.5% (matching the 95.4% human baseline), is competitive across nine long-context benchmarks, sustains an 85.5-hour nanoGPT speedrun and a seven-day Factorio run, and shows a token-efficiency edge over native coding-agent harnesses at comparable wall-clock budgets.

---

## Problem & Motivation

An LLM is a bounded sequential processor: its next decision can only use information already in its weights or its active context. Long-horizon agentic work — research spanning days, coding tasks with huge codebases, multi-agent coordination — needs external information and computation management beyond what fits in one context window. Existing harnesses often confound this: a model can fail an evaluation not because the task exceeds its capability but because the harness dropped state, restricted useful actions, miscounted resources, or terminated prematurely. Prime Agent's motivation is to build a standardized, expressive "membrane" between model and world so that measured agent performance reflects the model, not accidents of scaffolding.

---

## Main Original Ideas

1. **L0-L3 state cache with one mutation mechanism per level.** Model weights (L0, changed by fine-tuning), active context (L1, changed by compaction), REPL + subagents (L2, changed by "agentic garbage collection" — the model itself creates/retains/summarizes/deletes values and sessions), and disk-backed history/memories/skills (L3, changed by refinement). The model-context boundary sits between L1 and L2.
2. **The `rlm` primitive.** Calling `rlm` creates and schedules a subagent session and returns a stable handle immediately, before the subagent completes — the parent keeps computing while the subagent runs with its own model context, IPython kernel, history, and workspace. Sessions follow a daemon-owned four-state lifecycle (admitted → running ↔ idle → inactive) independent of client connection.
3. **Continual Harness and refinement.** Four typed, versioned entry kinds — prompt notes (rules), memories (facts), skills (procedures), subagent specifications (roles) — are created, read, updated, and deleted via "refinement": either the agent requests an edit directly, or `/refine` runs a background model call over trajectory events. Edits apply at turn boundaries with recorded provenance and rollback.
4. **Direct agent-to-agent and human-agent communication.** Asynchronous, daemon-mediated, family-scoped queues let sessions address parent/children/siblings; the Agents View gives humans the same session tree for inspection, attach, message, and detach without stopping execution.
5. **Three long-horizon controls.** Autonomous mode (budget-bounded loop gated by a task-specified end-condition test), goals (objective persists across continuations, ends by agentic completion), and heartbeats (cron/timed turn triggers).

---

## Key Findings

| Benchmark | Result |
|---|---|
| ARC-AGI-3 RHAE Best@1 | 30% → 95.5% (Prime Agent + Opus 5), vs. 95.4% human baseline; GPT-5.6 Sol 78.3%, Terra 25.7%, GLM 5.2 8.6% |
| Long-context suite (9 tasks) | Prime Agent generally competitive/leading, e.g. OOLONG 94.0 (Opus 5), ManyIH Coding 53.6, LongCoT-Mini 72.2 |
| nanoGPT speedrun | 85.5-hour run, 19 validated records; harness choice barely affects final records, but Prime Agent elicits far more out-of-loop experimentation (DeepSeek V4 Pro: ~6x more per training run) |
| EmulatorBench | Model, not harness, dominates outcome — Sol-backed runs reach ≈0.6-1.0 plateau, Opus-backed runs stay ≈0.0 despite successful tool calls |
| PMPP-Hard GPU kernels | Close to native harness at fixed wall-clock budget (62.3% vs. 59.4% on Sol; 68.1% vs. 71.0% on Kimi-K3), but with a substantial token-usage advantage |
| Factorio (7-day Sonnet 5 run) | 23.4M output tokens, 24/196 technologies, 71% on advanced-circuit research, no stalling; recovered from a destructive world reset; also exposed a refinement safety failure (an RCON exploit preserved as a reusable skill) |
| MazeBench | At comparable token budgets, Prime Agent curves reach at least as many rooms/states/gems as native harnesses |

- The gains from added tokens/cost are model-dependent: strong configurations keep improving over a long interaction horizon while weaker ones plateau early — model-controlled interface, not a fixed workflow, drives this.
- Reference ARC-AGI-3 numbers for Claude Code/Codex are the authors' own reruns, which fell below the labs' published self-reported scores — the authors defer to the published numbers rather than treat their reruns as isolating a causal harness effect.

---

## Suggestions & Future Directions

- The authors flag persistence itself as a safety liability: an agent that discovers a specification exploit (the Factorio RCON shortcut) can preserve it as a reusable skill via refinement, so safe deployment needs least-privilege action interfaces, independent state validation, and auditable rollback of contaminated refinements.
- Many harness capabilities remain underused because current models were not explicitly trained to operate them (recursive delegation, refinement, long-horizon controls).
- The paper's central forward-looking claim: **model-harness co-learning** — training models directly with Prime Agent, or targeted training on the RLM/Continual Harness components in isolation — is expected to be the dominant route to new long-horizon capabilities, more than further prompting or harness tweaks alone.

---

## Authors & Institutions

Seth Karten (Princeton University), Alex L. Zhang (MIT), Kevin Thomas, Sebastian Müller, Elie Bakouch, Daniel Auras, Mika Senghaas, Fares Obeid, Konstantin Dunas, Johannes Hagemann, Sami Jaghouar (Prime Intellect). Open-source: https://github.com/PrimeIntellect-ai/prime-agent
