> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Head-to-Head Results and Unrestricted Environment Access
**In one sentence:** Despite baselines using extra validation and unrestricted environment access that CASD never uses, CASD remains competitive and outperforms them on two of four benchmarks via a single offline corpus-analysis pass with an unmodified coding agent.
## Key points
- CASD remains competitive against baselines that use extra validation and unrestricted environment access it never uses, outperforming them on 2 of 4 benchmarks.
- CASD replaces iterative validation-gated search with a single offline corpus-analysis pass using an unmodified off-the-shelf coding agent, with no validation loops or additional environment interaction during optimization.
- Reflection scope is a design dimension: expanding reflection from sampled trajectories to corpus-scale analysis can replace iterative validation-gated search.
- Offline goal is formalized as `p* = CASD(D, p0)` from frozen corpus `D = {τi}` alone, without collecting additional trajectories or interacting with the environment.
- Distillation behavior over 24 runs totals 816 tool calls (94 exploring layout, 184 computing statistics, 510 inspecting episodes, 28 writing skill), mean 34.0 calls/run (range 16–51) producing a 5–8 KB skill file.
- Workflow is explore-first then statistics-guided investigation: 34% of calls in first fifth of run and only 5% thereafter (exploration median position 0.0), writing terminal (median 1.0), with median 5 switches between statistics and inspection (up to 16).
- Analysis code computes corpus-level statistics in every run for rewards/pass rates and episode lengths, 96% for termination/failure modes, 92% for tool usage, 79% by task category, and one-third for duplicated tool invocations.
- Resulting skills are evidence-grounded: 12 CASD skills contain 54 quantitative citations (4.6 per 1k words) versus none across 4 GEPA prompts and one across 4 SkillOpt prompts.
---
## Contributions tail
**Covers:** chunk opening fragment + contributions list
- Baselines benefit from extra validation and unrestricted environment access that CASD never uses; CASD still outperforms them on two of four benchmarks.
- Contributions claimed in chunk:
  - Characterize reflection scope as a fundamental design dimension, showing expanding reflection from sampled trajectories to corpus-scale analysis can replace iterative validation-gated search.
  - Present Coding-Agent Skill Distillation (CASD), replacing iterative search with a single offline corpus-analysis pass using an unmodified off-the-shelf coding agent, eliminating validation loops and additional environment interaction during optimization.
  - Evaluate across four agentic benchmarks, showing single offline pass matches or outperforms state-of-the-art search-based optimizers while substantially reducing optimization cost (cost reduction claimed; no cost table present in this chunk).

## 2 Related Work
**Covers:** §2 Prompt optimization as search; Learning from experience; Coding agents; Offline improvement
- Prompt optimization as search: from gradient-guided token search (Shin et al. 2020) to LM-driven proposals — APE, OPRO, ProTeGi textual gradients, TextGrad/Trace, DSPy/MIPRO; GEPA is strongest reflective variant (population + LM reflection + Pareto front on validation set); Promptbreeder/EvoPrompt mutate populations, PromptAgent plans edits with MCTS; unifying trait is a scoring gate requiring fresh rollouts per candidate — CASD needs none.
- Learning from experience without weight updates: Reflexion, Self-Refine, Voyager/ExpeL, Agent Workflow Memory, memory-stream architectures, plus online test-time loops (Dynamic Cheatsheet, ReasoningBank, ACE); all reflect trajectory-by-trajectory with context-window bottleneck and long-context recall degradation (Liu et al. 2024); CASD differs by executable analysis code whose exact counts over all episodes direct targeted reading, so corpus size enters via interpreter not context window.
- Coding agents: tool-using agents interleaving execution, inspection, editing are now strong enough on repository-level benchmarks (Jimenez et al. 2024) to be treated as general-purpose analysts; CASD repurposes one unmodified as optimizer where the "program" is a prompt and the "test suite" is frozen rollouts.
- Offline improvement and conservatism: fixed-dataset setting of offline RL (Levine et al. 2020) with BCQ/CQL constraints and one-step methods showing single un-iterated step preferable when dataset small; CASD is textual analogue — single support-constrained step over frozen corpus with no off-policy evaluation gate.

## 3 Method — 3.1 Problem Setup
**Covers:** §3–§3.1
- Target agent `πθ(p)` with fixed `θ`, only system prompt `p` optimized; executing initial prompt `p0` over training set produces rollout corpus `D = {τi}^N_{i=1}` recording messages, tool calls, outputs, rewards, metadata; goal is `p* = CASD(D, p0)` without new trajectories or environment interaction.

## 3.2 The Distillation Pass
**Covers:** §3.2 + verbatim instruction
- Invoke unmodified off-the-shelf coding agent with access to `D` and `p0` under single high-level instruction; no prescribed pipeline, metric, or intermediate representation; agent determines own analysis; process terminates when agent writes skill markdown file used directly as `p*`.
- Verbatim instruction from chunk:
  > "There is a results file here containing N agent rollout trajectories for [task family]. Analyze it directly—no other inputs, no precomputed summaries—and distill a skill markdown file capturing the behavioral rules that would make a future agent instance more accurate and more token/step-efficient on this task family. Use your own judgment fully on methodology. Write the skill file into this directory."

## 3.3 Inside the Distillation Process
**Covers:** §3.3 + Figure 2 description
- Classification of 24 runs / 816 calls: exploring corpus layout 94, computing statistics 184, inspecting episodes 510, writing skill 28.
- Patterns: (1) exploration precedes synthesis — median first occurrence 0.0, 34% calls in first fifth vs 5% thereafter, writing median 1.0, 16–51 calls/run mean 34.0, 5–8 KB skill; (2) statistics-guided investigation — alternate modes median 5 switches up to 16, targeting poor pass rates, long trajectories, repeated invocations, early termination; every run measures rewards/pass rates and lengths, 96% termination/failure, 92% tool usage, 79% by category, one-third duplicate search; (3) evidence-grounded synthesis — e.g. "16/50 episodes fabricated an identity-lookup argument" and "get_details_by_id was called 284 times, 123 of them exact duplicates"; 54 citations across 12 skills (4.6/1k words) vs 0 in GEPA and 1 in SkillOpt; workflow is compute statistics → guided inspection → evidence-backed rules.
- Note: this chunk contains no cost table and no additional head-to-head numbers beyond 2/4 benchmarks; Figure 2 panels (a) traces, (b) statistic frequencies, (c) evidence citations are described in text only.

**Covers:** contributions tail + §2 Related Work + §3–§3.3 (Figure 2a–c described, no cost table in chunk)
