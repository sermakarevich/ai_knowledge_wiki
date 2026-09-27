> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Roll-up Modes, Symbolic Propagation, Validation, and Conclusion

**In one sentence:** Per-op costs become wall-clock time via a fast closed-form analytical roll-up for thousand-point sweeps or a slow modulo-scheduling roll-up for fine-grained studies, all propagated symbolically in SymPy with numerics bound only at the edge — and regenerated implementations reproduce hand-audited references (including DeepSeekV3 serving on a TPU pod slice) to round-off precision.

## Key points

- Fast mode rolls loops up coarsely: each leaf's cost is scaled by the product of enclosing trip counts, and overlap effects (weight pre-collection, all-to-all hiding) are modeled as composable transforms in the style of a roofline bound (Williams et al., 2009) — closed-form evaluation fast enough for sweeps over thousands of design points.
- Slow mode modulo-schedules (Rau, 1994) each loop into its resource reservation table — software-pipelining the body against per-resource capacity — and the achieved initiation interval rolls up recursively up the tree, giving dependency- and resource-aware schedules for the design points that sweeps flag as interesting.
- The two modes form a funnel: fast mode screens thousands of points, slow mode studies the interesting ones in depth.
- Symbolic propagation: every roll-up produces a closed-form SymPy expression in the design space's free variables (batch, sequence length, bandwidths, mesh axes, datatype widths); numeric binding happens only at the edge — one substitution per design point — so a single symbolic build serves an entire sweep, and a doc can even state the exact expected expression for a collective's cost with generated tests asserting it.
- Validation headline: regenerated implementations reproduce hand-audited reference models — including DeepSeekV3 serving on a TPU pod slice — to round-off precision, which is the paper's evidence that docs (not code) can be the durable artifact for ML-systems co-design tools.
- Scale of the system today: ~50 design docs (~9,000 lines of specification prose) spanning TPU topology, collective cost models, numerics, schedulers, and a catalog of frontier model families (dense, MoE, latent-attention, robotics/VLA variants); master holds only docs plus a handful of leaf utilities, rebuilt by sub-agent orchestration on every version change.
- The closing argument: regenerating from docs pays the incremental-patching debt of Equation (1) to zero at every regeneration and surfaces vague intent early; the enablers (worked-example docs, machine-discovered dependency DAG, minimal symbolic IR) should generalize wherever specs churn faster than software absorbs them.

---

## The two roll-up modes

Fast mode is deliberately coarse — scale leaf costs by enclosing trip-count products, then apply composable overlap transforms — trading fidelity for sweep speed. Slow mode spends the RRT information the leaves carry: modulo scheduling software-pipelines each loop body against per-resource capacity, and initiation intervals compose recursively upward. The roofline-bound analogy (fast) and Rau 1994 citation (slow) anchor both modes in established performance-modeling literature rather than inventing new scheduling theory; the novelty claim sits one level up, in the regeneration workflow and the symbolic treatment.

## Symbolic propagation as a force multiplier

Because costs stay symbolic until the final substitution, the expensive work (tracing, roll-up) happens once per design space, not once per design point. The testability payoff matters for the regeneration story: exact expected expressions in docs become assertions on generated code, so the reconciliation anchors from Section 2 extend from numeric presets all the way to closed-form cost expressions.

## Validation and conclusion

The validation claim is strong in precision (round-off agreement with hand-audited references, DeepSeekV3 on a TPU pod slice named as the flagship case) but narrow in breadth — see [[critical_thinking|Critical Analysis]] for what this does and does not establish. The conclusion restates the system at its current scale (50 docs, ~9,000 lines) and the generalization bet: anywhere specs churn faster than software absorbs them, docs-as-artifact plus regeneration should transfer.

**Covers:** Section 3, paragraphs 6–7 (roll-up modes, symbolic propagation), Section 4 (Conclusion), References.
