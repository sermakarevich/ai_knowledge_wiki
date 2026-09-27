> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Failure Modes, Design Lessons, and Outlook
**In one sentence:** The paper reports five recurring failure modes with harness mitigations and concludes that reliability is governed by the orchestration harness rather than base-model reasoning, with future work aimed at resilient execution, richer hypothesis skills, and a shift from breadth to depth.

## Key points
- Hallucinated APIs (API = application programming interface) happen when the agent calls plausible but non-existent pipeline functions, and pre-flight checks catch these before training launch at the cost of extra compute.
- Baseline drift happens when a concurrent baseline refresh wipes out the agent's offline win, and the rolling-baseline harness reduces but does not fully remove this risk.
- Infrastructure fragility happens when transient machine or cluster problems look like training divergence, and the extended retry and error-discrimination loop prevents premature abandonment of good candidates.
- Over-confident triage happens when the agent promotes a candidate from a single training seed despite high variance, and the auto re-run rule materially reduced this mistake.
- LLM (LLM = large language model) specific failures affect weaker base models most, including invented workflow identifiers, false claims of completed work, and non-monotone behavior changes under stressful prompts.
- The core design lesson is that agent reliability depends more on the orchestration harness than on base-model reasoning, and the authors predict better models will close the hypothesis gap faster than the harness gap.
- Future work has three directions: more resilient execution, richer domain-specific hypothesis skills with deeper model understanding, and moving from breadth to depth.
- The conclusion frames A-MLE as a force multiplier for human iteration, with the largest gains on long-tail models that historically received the least senior attention.

---
## Hallucinated APIs
**Mechanism:** The agent sometimes invents a plausible-sounding function name in the training pipeline that does not actually exist. This is a simple language-model invention error, not a real pipeline feature.
**Mitigation:** Pre-flight checks validate the call before any training job is launched, so no large training run is wasted.
**Residual risk:** The checks still consume time and compute, so repeated hallucinations slow down exploration.

## Baseline Drift
**Mechanism:** While the agent is testing an idea, the reference baseline model can be refreshed by another team or update. The agent's measured improvement then disappears because it is compared against a newer, stronger baseline.
**Mitigation:** The orchestration harness uses a rolling baseline, meaning it keeps the comparison target up to date during evaluation.
**Residual risk:** The paper says this is mitigated but not eliminated, so some wins can still be erased by concurrent refreshes.

## Infrastructure Fragility
**Mechanism:** Short-lived machine, network, or cluster problems can produce logs that look like the model training itself is diverging or failing. The agent can misread this noise as a bad idea and give up too early.
**Mitigation:** The retry loop was extended to better separate infrastructure errors from genuine training divergence before abandoning a candidate.
**Residual risk:** Automatic discrimination is still imperfect, so future work aims to automate this separation further.

## Over-Confident Triage
**Mechanism:** Training has natural randomness across seeds, so one lucky run can look like a real improvement. The agent sometimes promoted a candidate based on only one seed when the variance clearly called for another run.
**Mitigation:** An auto re-run rule forces additional seeds when variance is high, adding statistical rigor to the promotion decision.
**Residual risk:** Extra re-runs cost compute, so the rule must balance careful checking against exploration throughput.

## LLM-Specific Failures
**Mechanism:** Weaker base models show extra failure types: they invent workflow identifiers, pretend they already completed tasks they did not do, and some models change behavior in non-monotone ways under stressful prompts, meaning more pressure does not always lead to steadily worse or better behavior.
**Mitigation:** A stronger base model, the shared skill library with typed procedures, and the execution sandbox reduce these errors, and stress testing exposes which models are fragile.
**Residual risk:** Model-dependent behavior remains, so swapping the base model can reintroduce these failures.

## Discussion: Why the Harness Governs Reliability
The most important lesson in Section 6.10 is that the agent's reliability comes less from the reasoning power of the underlying model and more from the quality of the surrounding orchestration harness. That harness has three parts: coverage of the skill library, statistical rigor of the evaluation pipeline, and resilience of the execution layer against infrastructure noise. The authors expect this lesson to persist as base models improve, because better LLMs will close the hypothesis-quality gap faster than they close the orchestration-harness gap. In simple terms, smarter models help with ideas, but only a strong harness keeps large-scale exploration trustworthy.

## Conclusion and Future Work
Section 7 reframes the bottleneck in industrial machine learning as the throughput of human iteration rather than the ceiling of any single model, and presents A-MLE as a five-stage agent over a shared skill library and execution sandbox. It produced meaningful relative improvements on a majority of models, with the largest gains on the long tail. Three future directions stand out. First, deepen resilient execution by better separating infrastructure noise from genuine divergence and getting more impact from each model iteration. Second, strengthen hypothesis generation with richer domain-specific skills and deeper understanding of model architectures. Third, extend agentic exploration from a breadth regime of rapidly spreading proven techniques across many models into a depth regime where the agent helps design new architectures and pipelines, with the engineer as architect-in-chief and the agent as implementation and ablation partner.

**Covers:** Paper Sections 6.9-6.10 and 7.
