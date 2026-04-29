# The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break

**Paper:** [The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break (Wang, Bai, Sun, Wang, Zhang, Hu, Schroder, Mutlu, Song, Nowak, 2026)](https://arxiv.org/pdf/2604.11978)

## Human Readable TL;DR

Imagine hiring an assistant who's great at running one or two errands, but the moment you give them a long to-do list, they start forgetting early items, misreading notes, and jumping to wrong conclusions -- and no amount of "hiring a smarter person" seems to fix it. That's what happens to today's AI agents on long tasks. The authors built a diagnostic test-kit called HORIZON that stretches the same task into longer and longer versions across four very different settings (web browsing, operating systems, databases, robotics) and then dissects each failure to figure out exactly what went wrong. They found that agents don't just get gradually worse -- they hit a cliff where they suddenly break, and the cliff comes from planning errors and memory problems rather than the AI's raw intelligence.

## TL;DR

This paper introduces **HORIZON**, a cross-domain diagnostic benchmark that systematically extends task horizons via two mechanisms (depth extension and breadth extension) to study where and why LLM-based agents fail. Evaluating GPT-5-mini and Claude-4-Sonnet on 3100+ trajectories across Web, OS, Database, and Embodied domains, the authors show that success rates do not decay linearly -- they exhibit a sharp "breaking point" beyond which models converge to near-systematic failure. A 7-category FMEA-grounded failure taxonomy, attributed via an LLM-as-a-Judge pipeline (κ=0.84 agreement with humans), reveals that **planning errors, catastrophic forgetting, and memory limitations dominate long-horizon failures** -- not execution-level bugs -- implying that scaling base models alone won't fix long-horizon reliability.

---

## Problem & Motivation

LLM agents are competent on short and mid-horizon tasks but **break down on long-horizon tasks** -- extended, interdependent action sequences like multi-file software debugging, OS workflows, iterative data analysis, or embodied manipulation. Small per-step error rates compound multiplicatively across dependent steps, producing a sharp degradation from reliable performance to near-total failure as tasks get longer.

The field has three gaps that this paper targets:

1. **Fragmented benchmarks:** Existing long-horizon evaluations are domain-specific and use inconsistent definitions of "horizon," making cross-domain comparison impossible.
2. **Aggregate-only metrics:** Most evaluations report terminal success rates, which hide the mechanism of failure.
3. **No shared failure taxonomy:** Analyses either stay within a single domain or use coarse categories, so targeted interventions are hard to design.

The paper asks two research questions: **RQ1 -- Where do agents break down as horizons increase?** and **RQ2 -- Why do these failures emerge?**

---

## Main Original Ideas

1. **HORIZON benchmark.** A cross-domain diagnostic framework combining agent-independent task-structure metrics with controlled task extension. It spans four domains (WebArena, AgentBench-OS, MAC-SQL, and a custom Isaac Sim 5.0 bimanual-robot environment) under one methodology, enabling the first apples-to-apples long-horizon comparison.

2. **Two-layer horizon formalization.** The paper separates the *theoretical* definition -- **Intrinsic Horizon (H\*)**, the minimum number of effective actions an optimal policy needs, and **Compositional Depth (s)**, the maximum count of nested sub-goals or conditional branches -- from the *technical* implementation via **Depth Extension** (inserting mandatory intermediate sub-tasks, for fixed-initial-state domains like OS/DB) and **Breadth Extension** (composing *k* independent baseline tasks into a single workflow, for variable-initial-state domains like Web/Embodied). This cleanly decouples horizon from agent efficiency.

3. **7-category FMEA-grounded failure taxonomy.** Categories are orthogonal (a trajectory can carry multiple tags): **Environment Error**, **Instruction Error**, **False Assumption**, **Planning Error**, **Catastrophic Forgetting**, **History Error Accumulation**, and **Memory Limitation**. The taxonomy is constructed from Failure Mode and Effects Analysis (process-level PFMEA + design-level DFMEA), grounded in the agent execution loop (observation / planning / action / state update), and validated empirically.

4. **Trajectory-grounded LLM-as-a-Judge pipeline.** A scalable failure-attribution tool that reached κ=0.84 agreement with expert human annotators and κ=0.61 inter-annotator agreement among humans themselves, making large-scale, reproducible failure diagnosis feasible.

5. **Empirical "breaking point" phenomenon.** Rather than smooth decay, performance shows an abrupt transition from partial robustness to near-systematic failure at a domain-specific *s*, formalizing the intuition that long-horizon failure is a regime change, not incremental drift.

---

## Key Findings

### Failure-Mode Distribution by Domain

| Domain | Planning Error | Instruction Error | Environment Error | Memory Limitation | History Error Accum. |
|--------|----------------|-------------------|-------------------|-------------------|----------------------|
| **Embodied** | **94.9%** | low | low | low | 0 |
| **Database** | **79.3%** | low | low | low | 0 |
| **Web** | **74.9%** | low | 11.3% | 6.2% | 0 |
| **OS** | 36.7% | 25.9% | 17.3% | 15.1% | 0.1% |

### Failure-Mode Distribution by Model

| Model | Planning Error | Memory Limitation | Environment Error | Instruction Error | Design-level Risks |
|-------|----------------|-------------------|-------------------|-------------------|--------------------|
| **GPT-5-mini** | **64.9%** | 18.3% | low | low | 20.8% |
| **Claude-4-Sonnet** | moderate | 2.2% | **32.5%** | 16.5% | 6.6% |

### Qualitative Findings

- **Non-linear degradation.** Success rates stay stable or decline gradually at small *s*, then drop sharply -- a regime change, not smooth decay.
- **Domain-specific breaking points.** Web collapses at very small *s*; OS and DB hold up longer; Embodied degrades steeply even with minimal *s* increases.
- **Model differentiation vanishes past the cliff.** In Web/OS/DB, model success rates converge to near-zero once agents enter the breaking region -- **raw capacity yields diminishing returns at long horizons**.
- **Planning and memory dominate.** Across all domains and both models, the largest failure share is planning-related (especially sub-plan errors), with catastrophic forgetting and memory limitations rising as horizons grow.
- **Model personality shows in failure mix.** GPT-5-mini fails more on planning + memory; Claude-4-Sonnet retains context better but is more sensitive to environment changes and instruction ambiguity.
- **LLM-as-a-Judge is reliable.** κ=0.84 with human experts on 40-trace pilot -- usable as a standard scalable diagnostic.

---

## Suggestions & Future Directions

1. **Shift from single-point accuracy to horizon-aware evaluation.** Report performance curves over *s*, breaking-point locations, and attributed failure-type distributions rather than a single success rate.
2. **Invest in hierarchical planning.** Sub-planning is the dominant failure mode in structured domains; hierarchical decomposition can tame combinatorial complexity and prevent early, costly deviations.
3. **Add execution-time control.** Build in plan verification, error detection, and repair during execution so small local mistakes don't cascade into irreversible trajectory-level failure.
4. **Build robust memory systems.** Address context-window limits, lossy summarization, and selective retrieval so that long-range constraints survive and re-surface when needed -- directly targeting catastrophic forgetting and memory limitation failures.
5. **Stop relying on base-model scaling alone.** The convergence of model performance past the breaking point shows scaling is insufficient; method-level (scaffold, memory, planning) improvements are required.
6. **Expand taxonomy validation.** The authors note the pilot validation (40 traces) is initial; broader cross-domain human annotation and real-world incident mapping (e.g., OpenClaw) are next.
7. **Community leaderboard.** The released HORIZON project website/leaderboard invites cumulative, reproducible progress on long-horizon agent reliability.

---

## Authors & Institutions

Xinyu Jessica Wang (UW--Madison, equal contribution), Haoyue Bai (UW--Madison, equal contribution, corresponding), Yiyou Sun (UC Berkeley), Haorui Wang (Georgia Tech), Shuibai Zhang (UW--Madison), Wenjie Hu (UW--Madison), Mya Schroder (UW--Madison), Bilge Mutlu (UW--Madison), Dawn Song (UC Berkeley), Robert D. Nowak (UW--Madison, corresponding).
