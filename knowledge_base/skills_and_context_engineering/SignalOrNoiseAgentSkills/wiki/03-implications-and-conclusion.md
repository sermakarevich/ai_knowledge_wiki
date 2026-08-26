> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Implications and Conclusion

**In one sentence:** Skill injection is a deployment routing decision rather than a configuration default — a Skill's value is a hypothesis about a specific (Skill, project, model) triple, and capturing it requires per-model, position-aware evaluation before paying the injection cost.

## Key points

- Unconditional Skill injection is small-and-negative on every model while adding 72–394% token cost, so injection must be opt-in and crossed against an empirical utility threshold at the (model, project, possibly task-difficulty) level.
- Skill-induced degradation concentrates on easy initial tasks where the model already succeeds, so a reasonable heuristic is to skip the Skill on early tasks and inject only once error rates rise — contradicting the common practice of attaching Skills before any task begins.
- Per-pair Skill effects are near-uncorrelated across models, so marketplaces publishing a single ranking are of limited use; multi-model deployment needs per-model evaluation traces and rankings conditioned on the model backend.
- A useful marketplace listing should report model-conditioned utility, the target stack, prompt length, and whether the gain survives a length-matched control.
- Without the length-matched control (C2), the benchmark would have reported a uniform negative effect, missing that it actually combines a small positive tail with easy-task losses requiring opposite mitigations.
- The paper frames its contribution as methodological: a byte-matched control plus a slice ablation turn a single negative average into a mechanistic account, and these controls should become a default in Agent-Skill benchmarking.
- Seed spread across the three Sonnet replicates (4.4 pp for C0 Pass@2, 3.6 pp for C1) is comparable to the headline effect size, so pair-level estimates need caution even though model-level means are stable at N=3.
- A Skill is a hypothesis about a particular (Skill, project, model) triple, not a portable asset — capturing its value is a routing problem of finding the beneficial minority before paying its injection cost.

---

## Benchmark injection as an opt-in decision

WebDev-Skills-Bench is intended as a pre-deployment audit: does a Skill's marginal gain survive its length cost and its model-specific risks? Since unconditional injection is small-and-negative on every model while inflating token cost by 72–394%, injecting a long Skill at session start — on average — reduces reliability while raising cost. Practical rule: inject a Skill only when a pair-level signal (model, project, possibly task difficulty) crosses an empirical utility threshold.

## Evaluate by chain position, not only by stack

Skill-induced degradation concentrates on easy initial tasks where the model already produces the correct output. A reasonable heuristic follows: skip the Skill on early tasks and inject it only once error rates rise as the task chain progresses. This directly contradicts the common pattern of attaching Skills before any task begins.

## Per-model curation is necessary

Per-pair effects are near-uncorrelated across models (Table 4), so marketplaces publishing a single ranking are of limited use for multi-model deployment. A practical system needs per-model evaluation traces and a ranking conditioned on the model backend. A useful marketplace listing should report: model-conditioned utility, the target stack, prompt length, and whether the gain survives a length-matched control.

## Length-matched control as minimum bar

Without the C2 length-matched control, the study would have reported a uniform negative effect and missed that it arises from two mechanisms needing different mitigations (a small positive tail versus losses on easy tasks). The authors recommend that future Agent-Skill benchmarks adopt a length-matched control as a basic requirement; the workspace-aware protocol of §3 makes this tractable even for multi-file Skills.

## Conclusion

The paper introduces WebDev-Skills-Bench, a controlled benchmark that asks not whether an agent can solve a task, but whether a Skill should have been injected at all. Its contribution is methodological: a byte-matched control and a slice ablation together turn a single negative average into a mechanistic account — a small positive tail, losses on easy tasks, and a length/content split across models that demands opposite mitigations. The central claim is conditional: a Skill is a hypothesis about a particular (Skill, project, model) triple, not a portable asset, and capturing its value is a routing problem — finding the beneficial minority before paying its injection cost. The authors hope that the controls that expose that minority become a default in Agent-Skill benchmarking.

## Limitations

- **Seed spread is non-trivial.** Across the three Sonnet replicates, aggregate C0 and C1 Pass@2 vary by 4.4 and 3.6 pp — comparable to the headline effect size. Individual pair-level estimates should be read with corresponding caution, even though the N=3 panel keeps model-level means stable.
- **C2 measurement caveats.** Only 109 unique length-matched runs were used across the 117 pairs, because some C2 prompts are shared across same-project pairs; a cluster bootstrap and full per-pair C2 deduplication are open follow-ups.
- **Conservative routing.** C1 is evaluated only on the 117 core-tier pairs, so the study cannot speak to what happens when Skills are deployed off-target.
- **Skill-set provenance.** The Skill set is drawn from high-visibility public repositories; closed Skills from enterprise pipelines or fine-tuned skill-routers may produce different patterns.
- **Pre-deployment vs online A/B.** WebDev-Skills-Bench is a pre-deployment benchmark, not an online A/B test: Web-Bench projects approximate realistic WebDev work but include no live user traffic, human developer interventions, or product-specific acceptance criteria.
- **Functional-correctness-only metrics.** Web-Bench measures functional correctness via Playwright rather than visual fidelity or interactive UX, and reports token overhead rather than end-to-end latency; Skills that primarily improve readability, accessibility, design quality, or developer review time may produce gains the metrics do not capture.

**Covers:** Section 5 (Benchmark Implications), Section 6 (Conclusion), Limitations
