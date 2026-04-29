# Effective Strategies for Asynchronous Software Engineering Agents

**Paper:** [Effective Strategies for Asynchronous Software Engineering Agents (Geng & Neubig, 2025)](https://arxiv.org/abs/2603.21489)

## Human Readable TL;DR

Imagine a team of builders working on a house -- if they all try to hammer nails in the same wall at the same time, they'll get in each other's way. This paper proposes giving each builder their own copy of the blueprints and workspace, letting them build their parts independently, then carefully combining everything at the end. Applied to AI coding assistants, this "branch-and-merge" approach -- borrowed from how human software teams already work -- lets multiple AI agents tackle big programming projects much more effectively than a single agent working alone.

## TL;DR

The paper introduces CAID (Centralized Asynchronous Isolated Delegation), a multi-agent coordination paradigm that translates established software engineering primitives -- `git worktree` isolation, `git merge` integration, dependency-aware task decomposition, and test-driven self-verification -- into a structured framework for asynchronous agent collaboration. CAID achieves +26.7% accuracy on PaperBench and +14.3% on Commit0 over single-agent baselines, demonstrating that physical workspace isolation and structured integration outperform both single-agent scaling and linguistically-governed coordination.

---

## Problem & Motivation

Single LLM agents struggle with long-horizon software engineering tasks requiring multiple interdependent subtasks -- they hit reliability and wall-clock time limits. Multi-agent systems offer a path forward but face core challenges: concurrent edits interfere with each other, dependencies between subtasks are hard to synchronize, and integrating partial progress into a coherent whole frequently fails. Existing multi-agent approaches rely primarily on linguistic coordination (role-based pipelines, hierarchical managers) that harmonize intent but fail to prevent physical execution conflicts. Human developers solve these problems daily with version control, isolated workspaces, and automated testing -- CAID translates these proven primitives into an AI agent coordination framework.

---

## Main Original Ideas

1. **Centralized Asynchronous Isolated Delegation (CAID)** -- A branch-and-merge multi-agent paradigm where a manager decomposes tasks into a dependency graph, delegates subtasks to engineer agents working in isolated `git worktrees`, and integrates their contributions via `git merge` with conflict resolution responsibility assigned back to the submitting engineer.

2. **SWE-primitive grounding for agent coordination** -- Rather than relying on natural language instructions to prevent conflicts, CAID uses physical isolation (`git worktree`), version control integration (`git commit`/`git merge`), and executable test suites as the actual coordination mechanisms -- an execution-aware rather than linguistically-governed approach.

3. **Dependency-aware task delegation** -- The manager constructs a directed dependency graph from import statements and test coverage (Commit0) or paper contribution structure (PaperBench), ensuring subtasks are only assigned when upstream dependencies are completed and integrated.

4. **Structured JSON communication protocol** -- Manager-engineer communication uses machine-parsable JSON specifying file paths, target functions, and dependency information, replacing ambiguous natural language task descriptions.

5. **Dynamic re-delegation loop** -- After each engineer completes and merges, the manager reassesses the dependency state and dynamically assigns new tasks, enabling adaptive scheduling rather than static upfront planning.

---

## Key Findings

| Benchmark | Model | Single-Agent | CAID | Improvement |
|---|---|---|---|---|
| PaperBench | MiniMax 2.5 | 10.4% | 36.7% | **+26.3 pp** |
| PaperBench | Claude 4.5 | 57.2% | 63.3% | **+6.1 pp** |
| Commit0-Lite | MiniMax 2.5 | 42.3% | 57.0% | **+14.7 pp** |
| Commit0-Lite | Claude 4.5 | 53.1% | 59.1% | **+6.0 pp** |

- Average improvement: +26.7 pp on PaperBench, +14.3 pp on Commit0-Lite
- Sequential "single-agent then CAID" fallback is inefficient -- nearly additive cost with marginal accuracy gain (e.g., 66.8% vs 63.3% on PaperBench with Claude 4.5, but runtime nearly doubles)
- Doubling iteration budget for single agents yields marginal or negative returns; multi-agent coordination provides substantially larger gains
- `git worktree` isolation is critical -- "soft isolation" (shared workspace + instruction-level constraints) degrades performance on open-ended tasks (55.5% vs 63.3% on PaperBench)
- Optimal parallelism is task-dependent: 4 engineers best for Commit0, 2 for PaperBench; excess parallelism introduces integration overhead and destabilizes execution
- Manager delegation quality is decisive -- failure to assign high-impact dependencies (e.g., `autodiff.py`) bottlenecks entire execution trajectories
- Verification intensity trades off with efficiency: strict review achieves 60.2% pass rate (3689s runtime) vs efficiency-prioritized 54.0% (1909s runtime)

---

## Suggestions & Future Directions

1. **Improve scheduling efficiency** -- Reduce coordination overhead and redundant verification cycles; learn optimal strategies for merging or pruning intermediate states to optimize the cost-performance frontier.

2. **Enhance task delegation** -- Explore reinforcement learning-based delegation policies, dependency-aware planning modules, or adaptive subtask refinement to improve alignment between global objectives and isolated agent execution.

3. **Generalize beyond software engineering** -- Adapt CAID's isolation and integration mechanisms to non-coding domains (document synthesis, research planning, multi-modal content generation) by designing alternative validation methods for domains without executable test suites.

4. **Limitations acknowledged** -- CAID incurs higher runtime and API cost than single-agent execution; manager delegation errors propagate through the entire pipeline; the current evaluation is limited to two benchmarks.

---

## Authors & Institutions

Jiayi Geng (Carnegie Mellon University, Language Technologies Institute), Graham Neubig (Carnegie Mellon University, Language Technologies Institute)
