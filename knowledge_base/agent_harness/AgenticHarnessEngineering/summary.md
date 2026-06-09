# Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses

**Paper:** [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses (Lin et al., 2026)](https://arxiv.org/abs/2604.25850)

## Human Readable TL;DR

Imagine you have a highly skilled worker (an AI), but their performance depends heavily on the tools and instructions you give them. Until now, improving those tools required an expert to watch the worker struggle, figure out what went wrong, and manually fix the setup -- a slow and tedious process. This paper builds a system that does that improvement loop automatically: it watches what the AI does, figures out why it failed, tweaks the tools and instructions, checks if things improved, and repeats -- all without human intervention. After ten rounds of self-improvement, the AI's coding success rate jumped by over 7 percentage points, beating human-designed setups. And the improved toolkit even worked when handed to completely different AI models.

## TL;DR

AHE (Agentic Harness Engineering) is a closed-loop system that automatically evolves coding-agent harnesses -- tools, prompts, middleware, memory, and sub-agents -- using three observability mechanisms: component-level file representations, trajectory evidence distillation via an Agent Debugger, and falsifiable edit predictions verified each iteration. On Terminal-Bench 2, AHE lifts pass@1 from 69.7% to 77.0% over ten iterations, outperforming human-designed baselines (Codex-CLI: 71.9%) and automated alternatives (ACE, TF-GRPO). The evolved harness transfers without re-evolution to SWE-bench-verified and five alternate model families (+2.3 to +10.1 pp).

---

## Problem & Motivation

Coding-agent harnesses -- the scaffolding of tools, prompts, and middleware surrounding a base model -- require constant manual engineering. As base models advance rapidly, developers must repeatedly inspect execution trajectories, diagnose failures, and hand-craft component edits. This process does not scale: trajectories are voluminous (millions of tokens), components are heterogeneous (prompts vs. code vs. config), and failure attribution is ambiguous. The core insight is that the bottleneck is not agent capability but **observability** -- the lack of structured access to what components exist, what went wrong, and whether a fix worked.

---

## Main Original Ideas

1. **NexAU Substrate (Component Observability):** The harness exposes seven orthogonal component types -- system prompt, tool descriptions, tool implementations, middleware, skills, sub-agent configs, and long-term memory -- as distinct editable files in a decoupled workspace. Starting from a deliberately minimal seed (NexAU0, bash-only) prevents seed bias and ensures clean failure attribution.

2. **Agent Debugger (Experience Observability):** Instead of feeding raw trajectories to the evolution agent, a dedicated debugger agent navigates trajectories as a file-based environment, produces per-task root cause analyses, and aggregates them into benchmark-level overview documents. This layered evidence corpus reduces token consumption while improving decision quality.

3. **Falsifiable Edit Predictions (Decision Observability):** Every harness edit is accompanied by a manifest entry specifying the failure evidence, inferred root cause, targeted fix, and predicted task-level impacts (expected fixes and at-risk regressions). The next evaluation round verifies these predictions; edits that violate their predictions are rolled back at file granularity.

4. **Closed-Loop AHE Algorithm:** A six-phase iteration -- rollout generation, trajectory cleaning, prior-manifest attribution and rollback, evidence distillation, workspace editing, and git commit -- forms a repeatable loop that compounds improvements over ten iterations without human intervention.

---

## Key Findings

| Method | All Tasks | Easy | Medium | Hard |
|--------|-----------|------|--------|------|
| NexAU0 (seed) | 69.7% | 87.5% | 78.2% | 51.7% |
| Codex-CLI (human) | 71.9% | -- | -- | -- |
| ACE (self-evolve) | 68.9% | 91.7% | 78.2% | 48.9% |
| TF-GRPO | 72.3% | **100.0%** | 79.4% | 55.6% |
| **AHE** | **77.0%** | **100.0%** | **88.2%** | 53.3% |

- **Structural beats prose:** Memory (+5.6 pp), tools (+3.3 pp), and middleware (+2.2 pp) contribute positively in ablations; system-prompt-only edits regress by 2.3 pp. Structural components transfer; semantic instructions do not.
- **Non-additive interactions:** Component ablation gains sum to +11.1 pp but full AHE yields only +7.3 pp, indicating redundant verification mechanisms compete for trajectory budget.
- **Cross-model transfer:** Gains of +2.3 to +10.1 pp across GPT-5.4 medium/xhigh, Qwen-3.6-plus, Gemini-3.1-flash-lite, and DeepSeek-v4-flash. Less-saturated models benefit more.
- **Cross-benchmark transfer:** On SWE-bench-verified, AHE achieves 75.6% success with 12--32% token reduction vs. baselines; gains concentrate on larger repositories.
- **Attribution precision:** Fix-prediction precision 33.7% (5x random baseline 6.5%); regression-prediction precision 11.8% (2x random baseline 5.6%) -- the loop reliably finds helpful edits but struggles to foresee regressions.

---

## Suggestions & Future Directions

1. **Interaction-aware evolution:** Components interact non-additively; future work should model component interactions explicitly to avoid redundant verification overhead and more precisely cap gains.
2. **Regression prediction:** The clearest limitation -- the system cannot reliably anticipate regressions before committing edits. Defensive or speculative rollout strategies could address this.
3. **Broader benchmarks:** Evaluation is limited to Terminal-Bench 2 and SWE-bench-verified; extending to human-in-the-loop workflows, non-English domains, and other task types is needed.
4. **Operating-point decoupling:** Cross-model gains confound harness portability with operating-point adaptation (step budgets, timeouts); controlled ablations separating these would clarify transferability claims.
5. **Governance and safety:** AHE is presented as a research prototype; mature deployment requires complete guardrails on self-modification scope beyond the current workspace boundary.

---

## Authors & Institutions

Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui
