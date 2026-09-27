# The Last Human-Written Paper: Agent-Native Research Artifacts

**Paper:** [The Last Human-Written Paper: Agent-Native Research Artifacts (Liu et al., 2026)](https://arxiv.org/abs/2604.24658)

## Human Readable TL;DR

Imagine a scientist's lab notebook vs. a published paper -- the notebook has all the messy details: failed experiments, wrong guesses, and the "aha" moments. Published papers discard most of that to tell a clean story. This paper argues that as AI assistants start doing research, they need the lab notebook, not the cleaned-up story. So the authors designed a new format for research -- like source code for knowledge -- that keeps everything: the failures, the exact settings, and the full reasoning trail. AI agents working from this format are dramatically better at understanding, reproducing, and extending the research.

## TL;DR

The paper introduces the Agent-Native Research Artifact (ARA), a file-system protocol replacing narrative PDFs with a machine-executable four-layer research package: structured scientific logic, executable code with full specifications, an exploration graph preserving failed experiments, and grounded evidence. Three tooling components support the ecosystem. On PaperBench and RE-Bench benchmarks, ARA raises agent question-answering accuracy from 72.4% to 93.7% and reproduction success from 57.4% to 64.4%.

---

## Problem & Motivation

Scientific publication compresses a non-linear, iterative research process into a polished linear narrative. This imposes two structural costs that were tolerable when humans were the only readers but become critical as AI agents must understand, reproduce, and extend published work:

1. **The Storytelling Tax:** Failed experiments, rejected hypotheses, and branching exploration are discarded to fit a linear narrative. Analysis of 24,008 RE-Bench agent runs shows failed runs account for 90.2% of total dollar cost and 59.2% of tokens, with a median failed-to-success token ratio of 113x. Without failure records, each new agent must independently rediscover every dead end.

2. **The Engineering Tax:** Papers communicate at the level of detail needed to convince a human reviewer, not at the precision required for agent execution. Analysis of PaperBench's 8,921 expert-annotated reproduction requirements across 23 ICML 2024 papers finds only 45.4% are fully specified in the PDF. Code development tasks are the most underspecified (37.3% sufficient); missing hyperparameters alone account for 26.2% of all gaps.

---

## Main Original Ideas

1. **Agent-Native Research Artifact (ARA) Protocol** -- A file-system ontology that transforms research from a narrative document into a machine-executable knowledge package organized around the principle "Knowledge over Narrative." The ARA has four interlocking layers that together eliminate both structural taxes.

2. **Four-Layer Architecture** -- (a) `/logic` (Cognitive Layer): queryable claims, dependency graphs, problem statement, falsifiable assertions; (b) `/src` (Physical Layer): executable code in Kernel Mode (algorithm only) or Repository Mode (full annotated codebase), with every hyperparameter annotated with rationale; (c) `/trace` (Exploration Graph): complete branching research DAG in YAML with five node types including `dead_end` nodes that preserve hypothesis, failure mode, and lessons; (d) `/evidence` (Evidence Layer): machine-readable metric tables and logs grounding every claim in raw outputs.

3. **Live Research Manager** -- An agent skill that captures research decisions and dead ends as natural side-effects of everyday human-AI development via three stages: Context Harvester (scans session records), Event Router (classifies events into 7 types and writes to the appropriate ARA layer), and Maturity Tracker (promotes observations to formal entries when evidence is sufficient). Produces conforming ARAs without additional documentation burden.

4. **ARA Compiler** -- An agent skill that translates legacy PDFs, code repositories, datasets, and experimental logs into ARA format, providing backward compatibility with the existing publication ecosystem. Uses top-down Semantic Deconstruction → Cognitive Mapping → Physical Grounding → Exploration Graph Extraction with iterative refinement.

5. **ARA-Native Review System with Seal Certificates** -- A three-level automated verification credential: Level 1 (Structural Integrity: schema conformance), Level 2 (Argumentative Rigor: 6-dimension epistemic rubric by a Rigor Auditor agent), Level 3 (Execution Reproducibility: scaled-down directional claims verified by a coding agent under a compute budget). Redirects human reviewers from mechanical checking to significance and novelty judgment.

6. **(Human+AI)^2 Research Network** -- A vision of scientific communication where ARAs replace papers as the primary persistent objects. Agents operate on ARAs via `/submit`, `/retrieve`, and `/fork` interfaces; publishing becomes a Git-like operation; the result is a queryable scientific commons where contributions compound like software.

---

## Key Findings

| Metric | Baseline (PDF+repo) | ARA | Gain |
|---|---|---|---|
| Q&A Accuracy -- Overall | 72.4% | 93.7% | +21.3pp |
| Q&A Accuracy -- Fidelity (Cat A) | 80.8% | 95.6% | +14.8pp |
| Q&A Accuracy -- Config Recovery (Cat B) | 67.8% | 92.6% | +24.8pp |
| Q&A Accuracy -- Failure Knowledge (Cat C) | 15.7% | 81.4% | +65.7pp |
| Reproduction Success (difficulty-weighted) | 57.4% | 64.4% | +7.0pp |
| Reproduction -- Easy tasks | baseline | ARA | +4.9pp |
| Reproduction -- Hard tasks | baseline | ARA | +8.5pp |

- ARA advantage on reproduction **widens monotonically with task difficulty**, providing greatest leverage on the hardest tasks.
- On 5 open-ended RE-Bench extension tasks, ARA agents reached a useful first move faster on every task (e.g., on `rust_codecontests` the ARA agent committed to the right approach in 9 minutes vs. 6 hours for the baseline).
- **Model capability modulates value:** On older Sonnet 4.5, ARA consistently outperformed on all extension tasks. On newer Sonnet 4.6 (Claude Sonnet 4.6), more capable agents sometimes exceeded ARA on 2/5 tasks by exploring novel approaches not in the failure trace -- suggesting the failure trace can constrain creative exploration for sufficiently capable agents.
- ARA Seal Level 2 detected 100% of fabricated claims, 100% of over-claims, and 91% of missing falsification criteria, but only 22% of orphan experiments (systematic blind spot from claim-centric traversal).
- Token efficiency: ARA agents consumed 12% fewer tokens on Category A questions, attributed to the layer index enabling targeted file lookup.

---

## Suggestions & Future Directions

1. **Artifact lineage and self-maintaining ecosystems (near-term):** Each ARA should declare parent artifacts and express contributions as structured diffs, enabling agents consuming an ARA to detect and repair staleness, update deprecated dependencies, and propagate corrections upstream.

2. **Knowledge graph and continuous review (medium-term):** Aggregated lineages form a queryable scientific knowledge graph enabling cross-artifact claim alignment, literature synthesis via subgraph queries, and reviewer verification that reported baselines match what cited ARAs recorded.

3. **Cross-disciplinary collective memory (long-term):** Extend ARA beyond ML to experimental sciences and theoretical disciplines, enabling documented failures in one field to become actionable knowledge in another via graph traversal rather than literature search.

4. **Adversarial robustness and privacy:** Current system lacks sandboxed execution, content-level anomaly detection, and granular access control for the Exploration Graph -- these are acknowledged aspirational properties.

5. **Schema evolution and migration:** A stable migration story for major ARA schema revisions including automatic rewriting of archival artifacts and a deprecation policy remains future work.

---

## Authors & Institutions

Jiachen Liu (University of Michigan), Jiaxin Pei (Stanford), Jintao Huang (Ohio State), Chenglei Si (Stanford), Ao Qu (MIT), Xiangru Tang (Yale), Runyu Lu (University of Michigan), Lichang Chen (Meta Superintelligence Labs), Xiaoyan Bai (University of Chicago), Haizhong Zheng (CMU), Carl Chen (University of Washington), Zhiyang Chen (University of Toronto), Haojie Ye (NVIDIA), Yujuan Fu (Meta), Zexue He (Stanford), Zijian Jin (NYU), Zhenyu Zhang (Stanford), Shangquan Sun (Nanyang Technological University), Maestro Harmon (Orchestra Research), Dianzhuo Wang (Harvard), Qian-ze Zhu (Harvard), Jiachen Sun (LinkedIn), Mingyuan Wu (UIUC), Baoyu Zhou (Arizona State), Chenyu You (Stony Brook), Shijian Lu (Nanyang Technological University), Yiming Qiu (University of Hong Kong), Fan Lai (UIUC), Yuan Yuan (Boston College), Yao Li (Portland State), Junyuan Hong (National University of Singapore), Ruihao Zhu (Cornell), Beidi Chen (CMU), Alex Pentland (Stanford), Ang Chen (University of Michigan), Mosharaf Chowdhury (University of Michigan), Zechen Zhang (Harvard & Orchestra Research)
