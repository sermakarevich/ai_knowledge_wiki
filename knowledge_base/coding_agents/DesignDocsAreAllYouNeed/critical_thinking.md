> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Design Docs Are All You Need

## Claims vs. evidence

**Claim 1: "Regenerated implementations reproduce hand-audited reference models to round-off precision."**
Suggestive, not strong. Round-off agreement is a genuinely demanding bar — far stricter than "within 5%" — but the paper never says how many reference models were reconciled, which ones besides DeepSeekV3-on-TPU, or what fraction of regeneration attempts passed on the first try vs. after repair-loop iterations. A single flagship case plus unspecified others is an existence proof: it shows the pipeline *can* hit exact agreement, not how reliably it does so. There are no error bars, no failure cases, no distribution of mismatches before repair.

**Claim 2: "Full clean-slate regeneration is practical and economically viable (1.5–3 h, ~100 USD)."**
Reasonably supported as a point estimate, weak as a general claim. The figures are concrete (Claude Code, ~20% of a weekly Claude Max budget) and plausible for a ~9,000-line spec. But they are tied to one vendor, one model tier, one point in time, and one spec size — all four move fast and mostly upward in cost. If the spec grows 10x or frontier-model pricing changes, the "regenerate by default" loop may stop being the obvious choice, and the paper offers no scaling curve (cost vs. doc count) to extrapolate from.

**Claim 3: "Worked examples are the crucial bottom-up ingredient for reliable regeneration."**
Unsupported by any comparison in the paper. The mechanism story is coherent (in-context demonstrations pin down ambiguous semantics; cites Brown et al. 2020, Dong et al. 2022) and the reconciliation-anchor discipline is genuinely testable design. But there is no ablation: worked-example docs are never compared head-to-head against tests-and-rules-only ("constitution") docs, so we cannot tell whether the examples, the anchors, the small per-doc scope, or simply strong base models carry the reliability. The doctrine is asserted from experience, not measured.

**Claim 4 (implicit): "The approach generalizes wherever specs churn faster than software absorbs them."**
A bet, stated honestly as such ("should generalize"), with no evidence beyond the single SMART instance. TPU-only leaves, one team, one hardware family. Plausible — but a reader should treat it as a hypothesis to test, not a result.

## Genuinely new vs. repackaged

Novel: the docs-as-master/code-as-build-product development loop taken literally at repository scale — master with almost no code, machine-discovered doc DAG, orchestrator log as a doc-hardness instrument, and Equation (1) as an explicit formalization of incremental-patching debt (the formalization itself is new packaging of an old intuition). The RRT-carrying recursive Op with edge-bound SymPy propagation is a real IR design contribution for this niche.

Repackaged / built directly on prior work: both roll-up modes are established techniques (roofline bounds per Williams et al. 2009; iterative modulo scheduling per Rau 1994) applied, not invented; the in-context-learning justification for worked examples is imported from Brown/Dong; the tracing-DSL and sharding-annotation ideas follow existing ML-compiler practice (XLA-style tracing, GSPMD-style sharding propagation). The paper's contribution is the composition and the workflow, not the components.

## Weaknesses and blind spots

Acknowledged implicitly: none of the threats are discussed in a dedicated limitations section — the 5-page format leaves no room, so every caveat below is the reader's to supply.

Not addressed:

1. No regeneration-failure analysis. The repair loop in Figure 1 exists, so regeneration sometimes fails — but there is no data on failure rate, dominant failure causes, or how many repair iterations typical docs need. The orchestrator log *contains* this data; not publishing even aggregate statistics is the paper's biggest missed opportunity.
2. No doc-hardness or model-routing results. Dynamic routing (big model for DSL docs, small models downstream) is claimed as a benefit but no routing table, no per-doc model assignment, and no quality-vs-cost comparison is shown.
3. Single hardware family. All leaves are TPU-shaped (MXU, VMEM, ICI). Whether the "few, orthogonal, stable" IR survives contact with GPUs (tensor cores, NVLink hierarchies, CUDA occupancy effects) is untested — and GPUs are where most readers would want to apply it.
4. No human-factors evidence. "Humans only edit docs" and "targeted human iteration" assume engineers can and will write good worked-example prose; there is no measurement of doc-authoring cost, learning curve, or whether prose quality actually improves across versions via the log signal.
5. Reproducibility is thin: no repository link, no doc-count breakdown per subsystem, no reference-model suite described. A 5-page paper cannot carry all of this, but as written the work cannot be independently replicated.

## Applicability

Applies well to: teams doing hardware/software co-design or operating any fast-churn modeling/simulation codebase where abstractions expire regularly; anyone running fleets of coding agents against a spec (the per-doc scoping + machine-discovered DAG + struggle-log is a directly reusable orchestration pattern); authors of SKILL.md/CLAUDE.md-style instruction files (the worked-example + reconciliation-anchor doctrine transfers almost verbatim to agent skill design).

Would not transfer well to: stable domains where specs rarely change (there, regeneration buys nothing and the doc-maintenance overhead is pure cost); codebases whose correctness depends on emergent global properties no single doc can state exactly (the per-doc decomposition assumes clean factorability); resource-constrained settings where 100 USD + hours per change is prohibitive (the economics assume frontier-model API budgets).

**Verdict: trial.** Adopt the workflow pattern (docs-as-artifact, worked examples with exact anchors, struggle-log-guided refinement) on one fast-churn subsystem and measure first-attempt regeneration success before committing a whole repository to it.

## Relevance to my work

- Sergii's fleet orchestrator already decomposes work into beads/tasks for coder workers — the paper's per-doc subagent + topological scheduler + central struggle-log maps almost 1:1 onto a fleet pattern worth stealing: log per-task agent friction (retries, repair loops) and feed it back as a "which task specs need rewriting" signal, exactly the targeted-iteration loop SMART uses for docs.
- The worked-example doctrine applies directly to his SKILL.md / skill files and fleet task descriptions: the paper's evidence-free but plausible claim is that step-by-step traces with exact numbers beat rules-and-constitutions for agent reliability — cheap to A/B test in his own fleet logs (tasks with worked examples vs. without, first-attempt success rate).
- The fleet/add_task + cheaper-coder-model routing in his AGENTS.md hints is the same "dynamic model routing" idea (hard docs → big model, routine docs → small model); SMART's missing routing data is a gap he could fill himself by recording model-per-task vs. success in fleet logs.
- Caution: do not import the cost conclusion uncritically — 100 USD/rebuild assumes Claude-Code-tier pricing and a 9k-line spec; his fleet uses sonnet/qwen workers where the quality-vs-cost tradeoff per task type is unmeasured, so replicate the measurement before adopting "regenerate, don't patch" as policy.
