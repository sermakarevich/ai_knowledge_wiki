# AI Scientists Produce Results Without Reasoning Scientifically

**Paper:** [AI scientists produce results without reasoning scientifically (Ríos-García, Alampara, Aghajani, Gupta, Mandal, Mannan, Krishnan, Jablonka, 2026)](https://arxiv.org/abs/2604.18805)

## Human Readable TL;DR

Imagine hiring a brilliant-sounding assistant who confidently produces lab reports, but when you peek over their shoulder, you notice they rarely test their guesses, ignore contradictory evidence they already collected, and never change their mind even when the facts say they should. This paper puts today's "AI scientist" agents under that kind of microscope and finds exactly this behavior: they often get correct answers, but not by thinking like scientists. The authors show that the underlying language model -- not clever wrapper software around it -- determines almost all of this behavior, which means we can't fix it by bolting on better prompts or tools. They argue we've been grading these systems only on whether they got the answer right, missing that the way they "reason" is often arbitrary and unreliable.

## TL;DR

The paper introduces **Corral**, an evaluation framework that analyzes LLM-based scientific agents along two axes: (1) a decomposition of performance into base-model capability vs. scaffold contribution using Item Response Theory and Bayesian variance decomposition, and (2) an epistemological structural analysis of agent traces annotated as graphs of hypothesis / evidence / test / justify / update / commit operations. Across 8 scientific domains, 3 frontier LLMs (GPT-4o, Claude Sonnet 4.5, GPT-OSS-120B), 2 scaffolds (ReAct, structured tool-calling), and 25,000+ runs, reasoning capability of the base model explains 41.4% of task-success variance while scaffold choice explains only 1.5%. Agents exhibit widespread reasoning breakdowns: evidence non-uptake (68% of traces), untested claims (53%), rare refutation-driven belief revision (26%), and almost no convergent multi-test evidence (7%) -- and these patterns do not adapt to the task's epistemic demand. The authors conclude outcome-only benchmarks hide these failures and that progress requires base-model training signals defined on the reasoning process itself.

---

## Problem & Motivation

LLM-based scientific agents are being deployed for autonomous hypothesis generation, experimentation, and manuscript writing, yet their reasoning processes are opaque -- they emerge from statistical regularities rather than inspectable rules like DENDRAL had in 1965. Existing benchmarks measure only task completion and answer accuracy; they reveal whether an agent succeeded but not how or why, so they cannot predict behavior on novel problems or detect whether a correct answer came from rigorous inquiry or from arbitrary guessing. Because the epistemic process determines the justification, predictability, and trustworthiness of scientific knowledge, the paper asks: do LLM agents actually reason the way scientists are supposed to -- testing hypotheses, updating on evidence, resolving contradictions -- or do they just produce outputs?

---

## Main Original Ideas

1. **Corral framework.** A reproducible suite of 8 scientific environments spanning workflow execution (molecular simulation, adsorption surfaces, ML-based property prediction, AFM), strategic reasoning (retrosynthetic planning), and hypothesis-driven inquiry (spectroscopic structure elucidation, inorganic qualitative analysis, circuit inference). Each domain has graded scope levels (S1–S4), standardized tools at three verbosity levels, and scoring functions for both final answers and intermediate subtasks.

2. **LDP decomposition of agent policy.** Modeling agents as Language Decision Processes (a POMDP with text observations and actions) and factoring the policy into π_LLM (base model, token-level choices) × π_scaffold (prompting / routing / orchestration). This lets the authors attribute behaviors to model vs. scaffold rather than conflating them.

3. **Bayesian variance decomposition with IRT latent capabilities.** A two-parameter logistic Item Response Theory model estimates separate "knowledge" and "reasoning" latent capabilities per model-environment pair, which are then fed into a selected Bayesian GLM (M7, chosen via PSIS-LOO among 8 candidates) to quantify the share of task-success variance attributable to reasoning, environment × scope, scaffold, and verbosity.

4. **Epistemic graph annotation.** Agent trajectories are annotated with epistemic operation labels -- Hypothesis, Evidence, Test, Justify, Update, Commit -- and directed edges (tests, observes, contradicts, updates-to). Productive reasoning patterns (Popperian conjecture-and-refutation, abductive inference, convergent multi-test evidence) and anti-patterns (untested claims, evidence non-uptake, contradiction without repair, fixed-belief traces) are detected as structural templates over these graphs.

5. **Trace intervention experiment.** Partial successful or failed trajectories from prior runs are injected into an agent's context to see whether performance and reasoning topology can be rescued by exposure to better reasoning, isolating how much of the deficit is recoverable vs. intrinsic.

6. **Reframing of evaluation for AI scientists.** Shift the field's focus from outcome-based metrics to process-based metrics that can serve as explicit training signals, arguing that as long as agents are graded on outputs alone, their epistemic failures remain invisible and shape the science they help produce.

---

## Key Findings

### Variance decomposition of task success

| Factor | Share of explained variance |
|--------|-----------------------------|
| **Base-model reasoning capability** | **41.4%** |
| Environment × scope interaction | 30.1% |
| Base-model knowledge capability | (substantial, remainder) |
| Scaffold (ReAct vs. structured tool-calling) | 1.5% |
| Tool-description verbosity | 0.1% |

### Prevalence of reasoning patterns across traces

| Pattern | Frequency |
|---------|-----------|
| **Evidence non-uptake (gathered evidence ignored)** | **68%** |
| **Beliefs never updated** | **71%** |
| Untested claims (overall) | 53% |
| Untested claims (hypothesis-driven domains) | 63% |
| Evidence non-uptake in workflow domains | 82% |
| Evidence non-uptake in strategic-reasoning domains | 66% |
| Evidence non-uptake in hypothesis-driven domains | 60% |
| Refutation-driven belief revision | 26% |
| Convergent multi-test evidence | 7% |

### Qualitative findings

- **Performance degrades with epistemic demand.** Agents approach the ceiling on guided workflow tasks but fall below 60% on complex hypothesis-driven domains (Inorganic Qualitative Analysis, Spectroscopic Structure Elucidation), even with the strongest configurations.
- **Subtask gradient.** Across all domains, retrieval > execution > reasoning > validation in reliability.
- **IRT capability divergence.** The gap between the strongest and weakest model on reasoning in Inorganic Qualitative Analysis exceeds 5.3 standard units -- models diverge most on hypothesis-driven reasoning, not on knowledge recall.
- **Rigid reasoning mode.** Agents do not adapt their epistemic operations to task demand or to scope -- the same topology appears whether the task is a simple workflow or open hypothesis-driven inquiry.
- **Model-level invariance of topology.** Stronger models execute existing patterns better but do not adopt fundamentally different epistemic strategies; the shape of their reasoning graphs is similar to weaker models.
- **Trace interventions are domain-dependent.** In workflow domains, injecting 1–2 successful steps exceeds baseline; in hypothesis-driven domains, only near-complete trajectories (n-2, n-1) help. Injecting failed traces is minimally harmful in workflow domains but catastrophic (success ≈ 0) in hypothesis-driven ones.
- **Reliability collapse.** Pass^k (probability all k trials succeed) drops below 0.05 by k=4–6 in hypothesis-driven domains even under early-stage successful interventions.
- **Confidence correlate.** Environments where partial interventions fail to help show lower mean token-level log-probabilities for GPT-OSS, linking epistemic fragility to model uncertainty.

---

## Suggestions & Future Directions

1. **Move training signals onto the reasoning process itself.** Because scaffold engineering contributes ~1.5% of variance, meaningful progress requires base-model training that optimizes for epistemic criteria (hypothesis testing, belief revision, contradiction repair), not just answer accuracy.
2. **Use Corral as a training and evaluation substrate.** Its reproducible tasks, standardized tools, and trajectory-level scoring functions are designed to serve as explicit rewards or evaluation targets on reasoning processes.
3. **Extend the catalog.** New environments, models, scaffolds, and epistemic metrics should be contributed over time so the framework tracks the evolution of AI systems' reasoning behavior as models change.
4. **Stop relying on outcome-only benchmarks.** The authors argue that as long as agents are evaluated solely on outputs, their epistemic deficits remain invisible and silently shape the scientific knowledge they help produce.
5. **Treat base-model capability, not scaffold cleverness, as the lever.** Resources spent refining prompting and tool-routing strategies will yield diminishing returns for scientific reasoning tasks compared to changes at the training level.
6. **Guard against human deskilling.** The paper flags a secondary concern that reliance on epistemically undisciplined AI tools may erode independent human problem-solving, compounding the risk of low-justification AI-generated science.

---

## Authors & Institutions

Martiño Ríos-García (IOMC, Friedrich Schiller University Jena -- co-first author), Nawaf Alampara (IOMC, Friedrich Schiller University Jena -- co-first author), Ali Asghar Aghajani (IOMC, Friedrich Schiller University Jena), Chandan Gupta (Department of Civil Engineering, IIT Delhi), Indrajeet Mandal (School of Interdisciplinary Research, IIT Delhi), Sajid Mannan (Department of Civil Engineering, IIT Delhi), N. M. Anoop Krishnan (Department of Civil Engineering; School of Interdisciplinary Research; Yardi School of AI, IIT Delhi -- corresponding author), Kevin Maik Jablonka (IOMC, Friedrich Schiller University Jena; Center for Energy and Environmental Chemistry Jena; Helmholtz Institute for Polymers in Energy Applications Jena / HIPOLE Jena -- corresponding author).
