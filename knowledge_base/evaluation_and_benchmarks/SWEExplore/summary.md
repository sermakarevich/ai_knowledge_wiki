# SWE-Explore: Benchmarking How Coding Agents Explore Repositories

**Paper:** [SWE-Explore: Benchmarking How Coding Agents Explore Repositories (Zhang et al., 2026)](https://arxiv.org/abs/2606.07297)

## Human Readable TL;DR

When you ask an AI coding assistant to fix a bug, it first has to hunt through thousands of files to find the relevant code -- like a new developer on their first day trying to locate the right drawer in a massive filing cabinet. This paper creates a standardized test to measure how good AI assistants actually are at that hunting step, separate from whether they ultimately fix the bug. It turns out most AI tools are decent at finding the right file, but terrible at pinpointing the exact relevant lines inside it -- and missing those precise lines is what causes fixes to fail.

## TL;DR

SWE-Explore is a benchmark of 848 repository-exploration tasks spanning 203 open-source repos in 10 languages, designed to evaluate coding agents' ability to locate relevant code regions independently of patch generation. Ground truth is derived from the intersection of successful trajectories across multiple strong LLMs (GPT-5.4, Gemini-3-Pro, Sonnet-4.5), with LLM-assisted promotion and human audit. The key finding: agentic explorers achieve ~65% file-level hit rates vs. <15% for classical retrieval, but line-level recall remains stuck at 15--19% for most agents -- the bottleneck for downstream repair. Context efficiency (r=+0.950) and first-useful-hit (r=+0.928) correlate most strongly with actual fix success.

---

## Problem & Motivation

Existing benchmarks like SWE-bench measure end-to-end issue resolution -- whether the agent produces a correct patch. This conflates two distinct problems: (1) *exploration* -- finding the right code regions to understand and modify, and (2) *patching* -- writing the correct fix. When an agent fails, it is unclear whether exploration or patching was responsible.

This matters because exploration is a distinct capability: it requires understanding repository structure, navigating codebases, and deciding which spans of code are relevant to a given issue description. Without isolating it, researchers cannot measure progress on the retrieval-navigation dimension, and practitioners cannot diagnose why agents fail.

---

## Main Original Ideas

1. **Exploration-isolated evaluation** -- SWE-Explore strips out patch generation entirely. Each agent is evaluated only on which code regions it reads/surfaces, not on whether it produces a correct fix. This cleanly separates the two sub-problems for the first time at scale.

2. **Trajectory-grounded ground truth** -- Ground truth is derived from actual successful agent runs: the intersection of what independent strong LLMs (GPT-5.4, Gemini-3-Pro, Sonnet-4.5) each consulted while solving the same issue. An LLM-promotion step then upgrades optional-but-load-bearing regions, followed by human audit. This avoids hand-labeling at scale while remaining grounded in what actually matters for solutions.

3. **Restricted-context validation protocol** -- To confirm that exploration metrics predict real outcomes, each explorer's output is fed as the *sole* visible context to a fixed patching agent (Mini-SWE-Agent + GPT-5.4). Repair success under this constraint is the validation target, ensuring upstream metrics are not measuring irrelevant information.

4. **Multi-dimensional metric suite** -- Three complementary metric families: *coverage/accuracy* (file-level hit rates, line-level precision/recall/F1, region overlap), *ranking efficiency* (nDCG@500, First Useful Hit), and *context efficiency* (fraction of surfaced lines that are core/optional context vs. noise). No single metric suffices; the three together reveal different operating-point tradeoffs.

5. **Benchmark scale and diversity** -- 848 instances across 203 repos in 10 languages (Python 64.5%, Go 9.9%, JavaScript 6.0%, plus Rust, Java, PHP, TypeScript, Ruby, C, C++), with per-instance averages of 4.3 files, 4.7 regions, and 1,578 visible lines inside codebases averaging 759 files.

---

## Key Findings

| Metric | Context Efficiency | First Useful Hit | Recall@100 |
|--------|-------------------|-----------------|------------|
| Pearson r with repair | **+0.950** | +0.928 | +0.926 |
| Spearman ρ | -- | -- | **+0.845** |

**Explorer comparison (K=5 regions, Table 6):**

| Explorer type | File hit rate | Line recall | Notes |
|--------------|--------------|-------------|-------|
| BM25 / TF-IDF | <15% | ~5% | Baseline lexical retrieval |
| General agents (Claude Code, OpenHands, Mini-SWE-Agent) | ~65% | 15--19% | Strong file hits, weak line recall |
| CoSIL (specialized) | highest file | **78.8%** line recall | Iterative code-graph search; only method breaking the line-recall ceiling |
| Academic localizers (AutoCodeRover, OrcaLoca, LocAgent) | moderate | recall-limited | Find files but miss test files; help only when broadening search |

- **File-level vs. line-level gap** -- File hit rates look strong across general agents, but line-level recall reveals the real bottleneck: agents consistently surface the right files without reading the relevant spans inside them.
- **Missing context dominates failures** -- Patchers are more sensitive to missing core evidence than to excess irrelevant context; recall-oriented improvements are more valuable than precision/filtering gains.
- **General agent convergence** -- Five general-purpose agents show closely matched profiles despite different implementations, suggesting a simplified explorer interface is sufficient to study the exploration problem in isolation.
- **Model vs. mechanism** -- Swapping the base LLM alone (within a fixed agentic framework) does not close the exploration gap; improved search mechanisms are required, not just stronger models.
- **Agentic >> classical retrieval** -- Across all metrics, agentic explorers form a clear tier above BM25/TF-IDF, validating the use of interactive codebase navigation over static indexing.

---

## Suggestions & Future Directions

1. **Improve line-level localization** -- The gap between strong file hits (~65%) and weak line recall (~15--19%) for general agents is the highest-leverage improvement target. Techniques like iterative code-graph search (CoSIL) suggest promising directions.

2. **Study full issue distribution** -- The benchmark covers only solvable instances; extending to unsolved or partially solvable issues would better reflect real-world distributions.

3. **Alternative evidence paths** -- Trajectory-derived ground truth captures one successful solution path; future work should investigate whether multiple valid evidence sets exist and whether agents using different paths can still succeed.

4. **Exploration-aware agent training** -- Since exploration quality predicts repair outcomes with r>0.9, exploration metrics could serve as training signals to build agents that are explicitly optimized for codebase navigation.

5. **Broader language and framework coverage** -- Python dominates (64.5%); future benchmark versions should expand coverage of statically-typed and compiled languages where static analysis tools have different tradeoffs.

---

## Authors & Institutions

Shaoqiu Zhang, Yuhang Wang, Jialiang Liang, Yuling Shi, Wenhao Zeng, Maoquan Wang, Shilin He, Ningyuan Xu, Siyu Ye, Kai Cai, Xiaodong Gu
