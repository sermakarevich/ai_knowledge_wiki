# Memento-Skills: Let Agents Design Agents

**Paper:** [Memento-Skills: Let Agents Design Agents (Zhou et al., 2025)](https://arxiv.org/abs/2603.18743)

## Human Readable TL;DR

Imagine hiring a new employee who can never go back to school -- their education is frozen. But what if they kept a notebook of "recipes" for solving problems, and every time they failed, they rewrote the recipe to work better next time? That's Memento-Skills: it gives AI assistants a growing library of reusable problem-solving playbooks that improve through trial and error, so the AI gets smarter over time without needing expensive retraining -- like a chef who never forgets a lesson learned in the kitchen.

## TL;DR

Memento-Skills introduces a continual learning framework for frozen LLM agents that externalizes adaptation into an evolving library of structured, executable skills (markdown files with code and prompts). A closed-loop read-write reflective mechanism attributes failures, rewrites skills, discovers new ones, and gates all mutations via unit tests. A behavior-aligned contrastive router trained with single-step offline RL selects skills by execution success rather than semantic similarity. On GAIA and Humanity's Last Exam, the system achieves +13.7 and +20.8 pp over baselines respectively, with the skill library growing from 5 atomic skills to 235 domain-organized skills.

---

## Problem & Motivation

Deployed LLM agents typically run with **frozen parameters** -- retraining is too expensive and complex for continuous updates. This makes them stateless: they cannot learn from deployment experience, retain knowledge across interactions, or self-correct past mistakes. Existing memory-augmented approaches either store passive interaction logs or produce prompt-level optimizations with limited transferability. Memento-Skills addresses the need for a practical system where a frozen LLM can autonomously build, adapt, and improve task-specific agents through cumulative experience, without human-designed prompts for each new task.

---

## Main Original Ideas

1. **Skills as the Unit of External Memory** -- Instead of storing raw episodic traces or simple prompt tweaks, the system treats structured, executable skill files (markdown with code + declarative specs) as the primary evolving memory unit, enabling reusable and composable knowledge.

2. **Read-Write Reflective Learning Loop** -- A closed-loop mechanism where the Read phase retrieves and executes the best skill, and the Write phase performs failure attribution, targeted skill rewriting, skill discovery (when patching is insufficient), and unit-test gating to prevent regressions -- all without touching model weights.

3. **Behavior-Aligned Contrastive Skill Router** -- Skill retrieval is framed as a one-step offline RL problem. A contrastive router is trained with multi-positive InfoNCE loss on synthetic query-skill pairs to optimize for execution success rather than semantic similarity, yielding a Boltzmann routing policy over a fused sparse+dense retrieval pipeline.

4. **Autonomous Skill Discovery with Escalation** -- When a skill's empirical success rate drops below a threshold, the system escalates beyond in-place patching to fundamentally restructure or synthesize entirely new skills, enabling coverage of novel task regions.

5. **Unit-Test Gate for Skill Mutations** -- Every skill modification is validated by an automatic unit test (synthetic test case generated and executed through the updated skill, scored by a judge), preventing regression and enforcing quality.

---

## Key Findings

### GAIA Benchmark

| Metric | Read-Write Baseline | Memento-Skills | Delta |
|--------|---------------------|----------------|-------|
| Test Accuracy (Overall) | 52.3% | **66.0%** | +13.7 pp |
| Training Accuracy (Round 3) | -- | **91.6%** | -- |

### Humanity's Last Exam (HLE)

| Metric | Read-Write Baseline | Memento-Skills | Delta |
|--------|---------------------|----------------|-------|
| Test Accuracy (Overall) | 17.9% | **38.7%** | +20.8 pp |
| Training Accuracy (Round 3) | -- | **54.5%** | -- |

- Skill library grew from **5 atomic skills to 41** (GAIA) and **235** (HLE), with t-SNE projections showing semantically coherent domain clusters
- The behavior-aligned router (Memento-Qwen) achieved **Recall@1 of 0.60** vs 0.54 for embedding baseline and 0.32 for BM25
- Cross-task transfer was strong on HLE (structured subject taxonomy) but limited on GAIA (highly diverse questions with minimal reasoning overlap)
- Route hit rate improved from 0.53 to 0.58 and judge success rate from 0.79 to 0.80 with behavioral alignment

---

## Suggestions & Future Directions

1. **Scaling skill libraries** -- Investigate how skill library size and organization affect performance at scale, and develop pruning/merging strategies for large libraries.
2. **Convergence analysis** -- Provide more precise theoretical convergence rates for the reflective learning loop under varying task distributions.
3. **Safety mechanisms** -- Integrate sandbox safety and alignment guardrails into self-evolving agent systems to prevent harmful skill mutations.
4. **Stronger base LLMs** -- The modular architecture allows independent upgrades; swapping in more capable LLMs is expected to yield compounding gains.
5. **Better embeddings and routing** -- Further improvements to embedding models and router training could enhance cross-domain skill transfer.
6. **Interpretability** -- The external, structured skill artifacts offer a path toward more transparent and explainable agent behavior.

---

## Authors & Institutions

Huichi Zhou (UCL), Yihang Chen (UCL), Siyuan Guo (Jilin University), Anjie Liu (HKUST-GZ), Zhongwei Yu (HKUST-GZ), Ziqin Gong (HKUST-GZ), Bowen Zhao (HKUST-GZ), Zhixun Chen (HKUST-GZ), Menglong Zhang (HKUST-GZ), Jinsong Li (AI Lab, Yangtze River Delta), Runyu Yang (AI Lab, YRD), Qiangbin Liu (AI Lab, YRD), Xinlei Yu (AI Lab, YRD), Jianmin Zhou (AI Lab, YRD), Na Wang (AI Lab, YRD), Chunyang Sun (AI Lab, YRD), Jun Wang (UCL, Advisor)
