# Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents

**Paper:** [Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents (Lin et al., 2026)](https://arxiv.org/abs/2605.30621)

## Human Readable TL;DR

Imagine you have a personal assistant who uses a rulebook (the "harness") to do their job. Some assistants are great at writing new rules into that rulebook when they encounter a problem; others are great at actually following the rulebook while doing the work. This paper discovered that these two skills are completely separate -- a small, cheap assistant can write just as good rules as an expert one. But whether an assistant actually *benefits* from better rules depends on their skill level in a surprising U-shaped way: average assistants benefit the most, experts are already so good they barely need the rules, and beginners are so unskilled that they can't even find or follow the rules correctly.

## TL;DR

This paper disentangles two capabilities in self-evolving LLM agents: (1) **harness-updating** -- the ability to produce useful persistent updates to the external agent harness (prompts, skills, memories) from execution evidence; and (2) **harness-benefit** -- the ability to leverage those updated harnesses during task solving. Across 7 LLMs and 3 agentic benchmarks, the authors find that harness-updating is flat across model capability tiers (even Qwen3.5-9B matches Claude Opus 4.6 as an evolver), while harness-benefit is non-monotonic -- mid-tier models benefit most, with weak-tier models failing due to harness activation and adherence failures.

---

## Problem & Motivation

Current self-evolving agent systems are evaluated end-to-end: did the agent improve after harness evolution? This metric conflates three sources of gain -- the agent's base capability, the evolver's ability to produce quality updates, and the agent's ability to use those updates. Without decomposing these, developers cannot know whether to invest in a better evolver or a better task-solving agent, nor can they diagnose *why* certain models fail to benefit from evolved harnesses. This paper fills that gap with the first controlled analysis that varies agents and evolvers independently.

---

## Main Original Ideas

1. **Harness-evolution capability decomposition** -- Formally splits the self-evolution pipeline into two measurable capabilities: harness-updating (evolver role) and harness-benefit (agent role), with precise metrics for each using anchor agent/evolver sets.

2. **Harness-updating is flat in base capability** -- Across all three benchmarks, the gap between the best and worst evolver is at most 3.1 percentage points, regardless of model size or family. A 9B open-source model (Qwen3.5-9B) produces skills procedurally isomorphic to Claude Opus 4.6, yielding identical downstream gains.

3. **Harness-benefit is non-monotonic** -- Mid-tier models (Qwen3-235B, GPT-OSS-120B) benefit most from evolution (+19.3 pp on SWE-bench for Qwen3-235B). Strong models hit a performance ceiling; weak models hit a capability floor despite having the most headroom.

4. **Two weak-tier failure modes identified** -- (i) *Harness activation failure*: weak models fail to load relevant skills into context (25% load rate for Qwen3-32B vs. ~96% for strong models). (ii) *Harness adherence failure*: even when loaded, weak models fail to follow the harness guidance (HFR of 14.2% for Qwen3-32B vs. 75.7% for Opus 4.6).

5. **Long-horizon adherence decay** -- Weak models' adherence degays 4× more steeply over a trajectory than strong models (Qwen3-32B drops from 0.52 to 0.13 across phases; Opus 4.6 stays 0.89 to 0.80).

---

## Key Findings

| Model | SWE Base (%) | SWE Δbenefit (pp) | MCP Base (%) | MCP Δbenefit (pp) | SB Base (%) | SB Δbenefit (pp) |
|---|---|---|---|---|---|---|
| Qwen3-32B | 3.6 | 4.4 | 3.6 | 1.0 | 0.0 | 5.8 |
| Qwen3-235B | 20.7 | **19.3** | 25.0 | 4.3 | 4.7 | 1.1 |
| GPT-OSS-120B | 26.2 | 15.8 | 28.0 | **7.0** | 0.0 | **7.0** |
| Haiku 4.5 | 66.0 | 2.4 | 42.4 | 3.6 | 5.8 | **15.1** |
| Sonnet 4.6 | 73.2 | 2.8 | 54.0 | 3.2 | 24.4 | 3.5 |
| Opus 4.6 | 74.2 | 2.6 | 61.0 | 3.6 | 25.6 | 5.8 |

- **Evolver performance is substrate-dependent**: Qwen3-235B leads on SWE (8.2 pp) but ranks last on MCP (0.6 pp); no evolver dominates across benchmarks.
- **Post-evolution score is dominated by agent, not evolver**: fixing the agent, swapping evolvers shifts performance by at most 5.1 pp; fixing the evolver, swapping agents shifts performance by up to 36 pp.
- **Extreme pairings still favor stronger agents**: even when the weakest anchor agent gets its best evolver and the strongest gets its worst, the strong agent wins by 18.6--35.2 pp on every benchmark.
- **Harness activation stats** (SkillsBench): Opus 4.6 = 95.7% SLR, Qwen3-32B = 25.1% SLR.
- **Harness adherence stats** (SkillsBench): Opus 4.6 = 75.7% HFR, Qwen3-32B = 14.2% HFR.

---

## Suggestions & Future Directions

1. **Invest capability budget in the task-solving agent, not the evolver** -- the harness-updating gap across evolvers is at most 3.1 pp; scaling the evolver yields diminishing returns.
2. **Treat harness invocation as a first-class learned skill** -- explicit training on reliable skill loading and action-format compliance is needed, especially for weak-tier models.
3. **Target long-horizon instruction following in agent training** -- use RL or fine-tuning objectives that penalize adherence decay over multi-step trajectories.
4. **Extend analysis to fine-tuning and hybrid adaptation** -- this study covers only harness (non-parametric) evolution with fixed model weights; parametric and hybrid methods remain open.
5. **Broader model coverage** -- a wider model grid (more families, scales, training recipes) would further clarify how harness-evolution capabilities interact with architectural and training differences.
6. **Harness safety in open deployments** -- the paper notes that persistent harness updates can encode incorrect, biased, or sensitive information; update reversibility, auditability, and human oversight should be first-class design requirements.

---

## Authors & Institutions

Minhua Lin (Penn State), Juncheng Wu (UC Santa Cruz), Zijun Wang (UC Santa Cruz), Zhan Shi (Amazon), Yisi Sang (Amazon), Bing He (Amazon), Zewen Liu (Emory University), Tianxin Wei (UIUC), Zongyu Wu (Penn State), Zhiwei Zhang (Penn State), Dakuo Wang (Northeastern University), Xiang Zhang (Penn State), Benoit Dumoulin (Amazon), Cihang Xie (UC Santa Cruz), Yuyin Zhou (UC Santa Cruz), Suhang Wang (Penn State), Hanqing Lu (Amazon)
