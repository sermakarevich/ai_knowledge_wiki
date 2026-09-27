# Total Cost of Ownership for Evaluating Agents

**Paper:** [Total Cost of Ownership for Evaluating Agents (Fiddler AI)](https://www.fiddler.ai/resources/agent-evals-tco)

## Human Readable TL;DR

Checking an AI agent's work by asking another big AI model to grade it is like hiring a lawyer to proofread every single email you send -- it works, but the bill grows every time you send more email, and you eventually start only proofreading 1 in 10 to save money, which means mistakes in the other 9 slip through. This piece argues for swapping that expensive lawyer for a small, purpose-built checker that costs a flat, predictable amount no matter how many emails you send, so you can check everything instead of a sample.

## TL;DR

Fiddler AI's resource page argues that using external LLM-as-a-Judge calls to evaluate agentic traces creates unpredictable, linearly-scaling cost ("Evaluation Trust Tax") plus data exposure risk, and that aggressive sampling (to control that cost) leaves blind spots on rare high-impact incidents. It pitches Fiddler's own small "Centor Models" (out-of-the-box detectors for hallucination/safety/toxicity/jailbreak/PII, plus customizable domain evaluators) as a flat-cost alternative that can score 100% of traces instead of ~10%, claiming up to 98% cost reduction versus external LLM judges at scale.

---

## Problem & Motivation

As agentic workflows go into production, every agent trace typically needs to be evaluated for quality, safety, and correctness. The default approach -- calling an external LLM provider to act as a "judge" on each trace -- ties evaluation spend directly to LLM API pricing and trace volume. As trace counts, tokens per trace, and evaluations per trace all grow with agent adoption, this cost grows linearly and becomes hard to forecast or control, pushing teams toward sampling (e.g., evaluating only ~10% of traces) which creates coverage gaps.

---

## Main Original Ideas

1. **The "Evaluation Trust Tax"** -- Framing external LLM-as-a-Judge API spend as an accumulating tax on trust: every additional API call needed to verify agent behavior adds cost that scales with usage, independent of the value delivered.
2. **Centor Models (step-function vs. linear cost)** -- Small, purpose-built evaluation/policy models priced on a step-function basis (cost increases in discrete tiers as capacity is added) rather than per-token/per-call, decoupling evaluation cost from trace volume growth.
3. **Full-coverage evaluation as a risk-reduction lever** -- Positions "evaluate every trace" as materially safer than sampled evaluation, since sampling systematically misses low-frequency, high-impact incidents (the events most likely to cause real harm).
4. **Two-tier model offering** -- Out-of-the-box Centor Models for common risk categories (hallucination, safety, toxicity, jailbreak, PII/PHI) alongside customizable, prompt-based domain-specific evaluators for complex reasoning tasks that don't fit a generic detector.

---

## Key Findings

- Claims **up to 98% cost reduction** using Fiddler Centor Models compared to external LLM-as-a-Judge approaches at scale.
- External LLM-based evaluation setups are characterized as typically **sampling ~10%** of traces; Centor Models are pitched as capable of evaluating **100%** of traces at that same or lower cost.
- Cost drivers identified for external-LLM evaluation TCO: trace volume, tokens per trace, and number of evaluations run per trace -- all compounding under linear per-call pricing.
- Named non-cost risks of the external-LLM approach: **Incident Risk Exposure** (blind spots from sampling) and **Operational Overhead** (API orchestration, model hosting, prompt versioning, calibration work).

---

## Suggestions & Future Directions

1. Move evaluation workloads off general-purpose external LLM judges and onto smaller, purpose-built classifier/detector models where the evaluation task is well-scoped (hallucination, toxicity, PII, jailbreak, safety scoring).
2. Reserve prompt-based LLM evaluation for genuinely complex, domain-specific reasoning checks that resist a fixed classifier -- via Fiddler's "Customizable Models" tier.
3. Treat evaluation coverage (percentage of traces scored) as a first-class metric alongside cost, not a variable to sacrifice for budget control.

---

## Authors & Institutions

Fiddler AI (vendor resource/whitepaper page; no individual authors listed).
