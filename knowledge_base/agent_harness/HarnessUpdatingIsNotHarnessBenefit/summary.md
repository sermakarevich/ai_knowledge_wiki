# Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents

**Paper:** [Harness Updating Is Not Harness Benefit (Lin et al., 2026)](https://arxiv.org/abs/2605.30621)

## Human Readable TL;DR

Imagine an AI assistant that can rewrite its own instruction manual based on past mistakes -- adding new procedures, fixing broken ones -- while its core "brain" stays frozen. This paper asks: does the smarts of the AI writing the manual matter? And does the same AI that writes it actually benefit from reading it? Surprisingly, almost any AI can write a useful manual -- even a small, cheap model writes manuals as good as the most powerful ones. But only mid-range AIs reliably benefit from reading the updated manual: weak AIs either forget to open it or can't follow through on what it says, while top AIs are already so good they barely need it.

## TL;DR

This paper formally decomposes harness self-evolution -- the process of updating an LLM agent's external scaffolding (prompts, skills, memory, tools) from execution evidence -- into two distinct capabilities: **harness-updating** (evolver quality) and **harness-benefit** (agent utilization). Across 7 LLMs and 3 benchmarks, they find harness-updating is surprisingly flat across model capability tiers (max gap: 3.1 pp), while harness-benefit is non-monotonic: mid-tier models gain most, weak-tier models fail due to harness activation and adherence failures, and strong-tier models hit performance ceilings. The key implication is to invest capability budget in the task-solving agent, not the evolver.

---

## Problem & Motivation

LLM agents increasingly rely on editable external harnesses -- prompts, skills, memories, tools -- that shape behavior without touching model weights. **Harness self-evolution** lets agents update these harnesses automatically from execution evidence (failures, trajectories, successful procedures). However, all prior work evaluates this end-to-end, leaving two practical questions unanswered:

1. Which models produce useful harness updates (evolver side)?
2. Which models actually benefit from updated harnesses (agent side)?

End-to-end scores conflate both effects. A gain could come from a smarter evolver writing better updates, or from a smarter agent using those updates -- you can't tell which. This ambiguity wastes investment: practitioners may over-invest in powerful evolvers when it doesn't matter, or deploy the wrong model tier as the task-solving agent.

---

## Main Original Ideas

1. **Formal decomposition of harness self-evolution** -- The paper defines two separable metrics: *harness-updating capability* Δ_update(e) (average gain an evolver e produces across anchor agents) and *harness-benefit capability* Δ_benefit(f) (maximum gain an agent f achieves across anchor evolvers). This decoupling enables independent evaluation of each role.

2. **Harness-updating is flat in base capability** -- Across 7 models and 3 benchmarks, the max spread between best and worst evolver is only 3.1 pp on any single benchmark. Even Qwen3.5-9B (the smallest model) produces updates comparable to Claude Opus 4.6 evolvers. No evolver dominates across all benchmarks.

3. **Harness-benefit is non-monotonic** -- Mid-tier models (e.g., GPT-OSS-120B, Qwen3-235B) gain the most from harness evolution; strong-tier models gain less due to performance ceilings; and weak-tier models gain least despite having the most room to improve -- due to two identified failure modes.

4. **Two weak-tier failure modes** -- (a) *Harness activation failure*: weak models fail to invoke harness artifacts at all (Qwen3-32B skill-load rate = 25.1% vs. ~96% for strong models); (b) *Harness adherence failure*: even when loaded, weak models fail to follow procedural guidance over long horizons (adherence decays 4× more steeply in weak-tier models than strong ones: −0.39 vs. −0.09 drift from harness-load to final turn).

5. **Design guidance** -- Practitioners should allocate capability budget to the task-solving agent rather than the evolver, and train agents specifically on harness invocation protocols and long-horizon instruction following.

---

## Key Findings

### Harness-Updating: Evolver Δ_update (pp) across benchmarks

| Evolver | SWE-bench | MCP-Atlas | SkillsBench |
|---|---|---|---|
| Qwen3.5-9B | 6.8 | 1.0 | **3.8** |
| Qwen3-32B | 7.8 | 2.3 | 0.7 |
| Qwen3-235B | **8.2** | 0.6 | 1.5 |
| GPT-OSS-120B | 5.9 | 1.9 | 1.5 |
| Haiku 4.5 | 8.0 | 2.3 | 2.7 |
| Sonnet 4.6 | 7.4 | 2.6 | 1.2 |
| Opus 4.6 | 7.4 | **3.6** | 2.3 |

Max spread on any benchmark: 3.1 pp (MCP-Atlas). No single evolver dominates. Qwen3.5-9B wins SkillsBench despite being the smallest model.

### Harness-Benefit: Agent Δ_benefit (pp)

| Agent | SWE-bench | MCP-Atlas | SkillsBench |
|---|---|---|---|
| Qwen3-32B | 4.4 | 1.0 | 5.8 |
| Qwen3-235B | **19.3** | 4.3 | 1.1 |
| GPT-OSS-120B | 15.8 | **7.0** | **7.0** |
| Haiku 4.5 | 2.4 | 3.6 | 15.1 |
| Sonnet 4.6 | 2.8 | 3.2 | 3.5 |
| Opus 4.6 | 2.6 | 3.6 | 5.8 |

Mid-tier models (Qwen3-235B, GPT-OSS-120B) have largest gains. Strong models (Opus, Sonnet) gain only 2--4 pp due to ceiling effects. Weak models (Qwen3-32B) gain little despite low baselines.

### Failure Mode Metrics (SkillsBench)

| Model | Skill-Load Rate | Harness-Follow Rate | Pass Rate (when loaded) |
|---|---|---|---|
| Qwen3-32B | 0.251 | 0.142 | 0.023 |
| GPT-OSS-120B | 0.446 | 0.442 | 0.040 |
| Haiku 4.5 | 0.794 | 0.600 | 0.099 |
| Qwen3-235B | 0.961 | 0.350 | 0.022 |
| Sonnet 4.6 | 0.959 | 0.730 | 0.145 |
| Opus 4.6 | 0.957 | **0.757** | **0.177** |

Qwen3-235B highlights the separation: near-perfect load rate (0.961) but only 35% adherence -- loading ≠ following.

- Between-agent base capability gap (Opus vs. Qwen3-235B) exceeds within-agent evolver spread by 11× on SWE-bench and 2.2× on SkillsBench.
- Weak-tier adherence decays from 0.52 → 0.13 (drift −0.39) over task execution vs. −0.09 for Opus 4.6.

---

## Suggestions & Future Directions

1. **Invest in the agent, not the evolver** -- The evolver quality gap is at most 3.1 pp; agent selection gap dwarfs it. Use any capable model as evolver; prioritize agent capability.
2. **Train harness invocation as a first-class skill** -- Weak models have 25% skill-load rates; this is not a data problem, it's an agent training target. Action protocol compliance must be explicitly trained.
3. **Strengthen long-horizon instruction following** -- 4× steeper adherence decay in weak models suggests this is a distinct training axis. Existing RLHF/SFT may not address procedural faithfulness over 10--25 turn horizons.
4. **Expand model grid** -- Current 7-model set is representative but not exhaustive; broader coverage of model families, scales, and training recipes would clarify where the non-monotonic breakpoints lie.
5. **Address harness safety** -- Updated harnesses persist across future tasks; incorrect rules, biased procedures, or leaked sensitive data can be written in. Future work should treat harness auditability, reversibility, and human oversight as first-class design requirements.
6. **Explore hybrid adaptation** -- This work fixes model weights throughout; combining harness evolution with parametric fine-tuning or RL remains an open direction.

---

## Authors & Institutions

Minhua Lin (Penn State), Juncheng Wu (UC Santa Cruz), Zijun Wang (UC Santa Cruz), Zhan Shi (Amazon), Yisi Sang (Amazon), Bing He (Amazon), Zewen Liu (Emory University), Tianxin Wei (UIUC), Zongyu Wu (Penn State), Zhiwei Zhang (Penn State), Dakuo Wang (Northeastern University), Xiang Zhang (Penn State), Benoit Dumoulin (Amazon), Cihang Xie (UC Santa Cruz), Yuyin Zhou (UC Santa Cruz), Suhang Wang (Penn State), Hanqing Lu (Amazon)
