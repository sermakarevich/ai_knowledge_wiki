# Self-Optimizing Multi-Agent Systems for Deep Research

**Paper:** [Self-Optimizing Multi-Agent Systems for Deep Research (Câmara, Slot, Zavrel, 2025)](https://arxiv.org/abs/2604.02988)

## Human Readable TL;DR

Imagine you have a team of research assistants who each have a specific job -- one plans what to look for, others read documents, another combines findings, and a final one writes the report. Normally, a manager would spend months writing detailed instructions for each assistant. This paper shows that instead, you can give the assistants bare-bones instructions and let them practice on sample questions, automatically figuring out better ways to do their jobs through trial and error -- eventually matching or beating the performance of assistants who were given those months-of-effort instructions.

## TL;DR

This paper applies algorithmic prompt optimization methods (TextGrad and GEPA) to a multi-agent Deep Research system with orchestrator, reader, aggregator, and writer agents. Starting from minimal one-liner prompts, GEPA with a task-specific meta-prompt achieves scores of 0.705 on ScholarQA-CS, surpassing both expert-crafted prompts (0.667) and TextGrad optimization (0.654), demonstrating that self-play prompt exploration can replace costly manual prompt engineering.

---

## Problem & Motivation

Deep Research (DR) systems go beyond single-turn RAG by iteratively planning queries, retrieving from many documents, synthesizing evidence, identifying gaps, and refining research direction. Current DR systems rely heavily on **handcrafted prompts and static architectures** that are:

- **Brittle** -- prompts tuned for one LLM or domain often break when the model is updated or the domain shifts
- **Expensive to maintain** -- restoring quality after changes requires costly trial-and-error by human experts
- **Non-transferable** -- expertise encoded in prompts doesn't generalize across settings

The authors ask: can algorithmic prompt optimization replace this manual engineering, producing agents that self-improve through exploration?

---

## Main Original Ideas

1. **Multi-Agent DR Architecture with Modular Optimization** -- A four-agent pipeline (orchestrator, reader, aggregator, writer) where each agent's prompt is treated as an independently optimizable variable, enabling targeted per-agent improvement without disrupting the full system.

2. **Application of TextGrad to Deep Research** -- Adapting textual gradient descent (critique-based prompt refinement via "loss" and "gradient" metaphors) to the multi-agent DR setting, using execution traces and rubric-based evaluation as the feedback signal.

3. **GEPA with Custom Meta-Prompt for DR** -- Applying a genetic/Pareto-based optimization strategy (GEPA) with a task-specific meta-prompt tailored to Deep Research, which proved more effective than both default GEPA and TextGrad by enabling broader exploration of the prompt space.

4. **Minimal-to-Expert Prompt Bridging** -- Demonstrating that starting from trivial one-liner prompts and running optimization can match or exceed the quality of prompts refined by human experts over more than a year.

---

## Key Findings

| Configuration | Minimal Prompt | Expert Prompt |
|---|---|---|
| **No optimization (baseline)** | 0.513 | 0.667 |
| **OpenAI Optimizer** | 0.583 | 0.667 |
| **TextGrad** | 0.654 | 0.672 |
| **GEPA (default)** | 0.685 | 0.670 |
| **GEPA (custom meta-prompt)** | **0.705** | **0.701** |

- Optimization yields the largest gains from weak starting points (+0.141 for TextGrad from minimal, +0.192 for custom GEPA from minimal)
- Diminishing returns when starting from expert prompts (+0.005 to +0.034)
- GEPA's Pareto-based evolutionary exploration converges faster and more efficiently than TextGrad's greedy hill-climbing
- OpenAI's general-purpose prompt optimizer underperforms -- lacks access to task-specific evaluation signals and agent execution traces
- All optimization runs used GPT-4.1-mini with a budget cap of USD 50 per round

---

## Suggestions & Future Directions

1. **Optimize beyond prompts** -- extend self-optimization to tools, architectural hyperparameters, agent topology, and even code-level changes
2. **Synthetic training signals** -- reduce reliance on expert-authored rubrics by generating self-supervised or LLM-generated evaluation criteria
3. **Cross-domain and cross-model generalization** -- validate on domains beyond Computer Science and with diverse model families (current work limited to GPT-4.1-mini)
4. **Statistical rigor** -- the small test set (50 queries) and single-domain evaluation limit generalizability; larger-scale studies with significance testing are needed
5. **Address LLM-as-judge biases** -- the evaluation may favor verbose outputs; more robust assessment methods should be explored

---

## Authors & Institutions

Arthur Câmara (Zeta Alpha, Amsterdam), Vincent Slot (Zeta Alpha, Amsterdam), Jakub Zavrel (Zeta Alpha, Amsterdam)
