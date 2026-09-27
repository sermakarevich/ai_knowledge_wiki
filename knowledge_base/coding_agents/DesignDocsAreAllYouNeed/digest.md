> [[index|Wiki]] | [[summary|Summary]]

# Design Docs Are All You Need — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-motivation-and-regeneration-workflow|Motivation: Why Performance-Modeling Software Rots, and the Regeneration Answer]]

**In one sentence:** ML performance-modeling frameworks decay because model architectures and hardware churn invalidates their abstractions from both directions, while incremental patching (by humans or context-starved agents) compounds technical debt — so SMART makes natural-language design docs the durable artifact and regenerates all code from scratch on every version update.

- Performance-modeling frameworks sit between the two fastest-moving parts of the stack (model architectures above, accelerators/interconnects below) and absorb churn from both sides, e.g. the once-safe assumption "every transformer layer looks the same" is now false under mixture-of-experts routing, latent attention, and heterogeneous inference phases.
- Failure mode 1, incremental generation debt: with spec St at time t and generator G, greenfield builds Ct = G(St) but practice computes Ct+1 = G(St+1, Ct); the debt Dt+1 = G(St+1, Ct) - G(St+1) (Equation 1) compounds because humans find deleting all their code mentally hard and time-consuming.
- Failure mode 2, context-window myopia: agents cannot fit a mature codebase in one prompt, so developers feed fragmented snippets; the agent misses global invariants and cross-module dependencies and produces locally plausible but globally sub-optimal code that degrades structural coherence over time.
- The SMART response: the main branch holds almost no code — only a DAG of self-contained natural-language design docs; coding subagents regenerate the implementation from the docs alone on every version update, and every human change is a natural-language doc edit (self-documenting by construction).
- Figure 1 workflow: design-doc DAG (checked into master) → subagents regenerate the library in topological order (one sub-agent per doc) → symbolic cost model build product → validation (reference-model reconciliation, parameter guards, unit tests) → repair loop; humans only ever edit docs.
- Because Ct = G(St) is recomputed from scratch on a regular cadence, Equation (1) debt is driven to zero by construction, and vague intent surfaces early since a guess must be written into a doc to survive.

## 2. [[wiki/02-design-docs-as-source-of-truth|Design Docs as the Source of Truth]]

**In one sentence:** The master branch is a DAG of self-contained markdown design docs with machine-discovered dependency edges, regenerated into code by one coding sub-agent per doc in topological order under an orchestrator that logs interpretation struggles to guide human doc refinement.

- Main branch contains almost no code: a folder of markdown design docs forming a DAG, where ordering constraints are semantic (e.g. hardware topology and numerics must be generated before collective-cost models, which precede the model catalog).
- DAG edges are machine-discovered, not hand-maintained: read-only agents analyze the docs and infer dependency edges; an orchestrator then walks the DAG in topological order, assigning a dedicated coding sub-agent to implement each self-contained doc.
- The orchestrator keeps a central log of where sub-agents struggled to interpret prose and bugs found in earlier topological waves — this log tells human engineers exactly which docs need prose refinement next version (targeted human iteration).
- Benefit 1, bounded context windows: each generation step is scoped to a single document, limiting each LLM's context and task length and raising per-task correctness odds — a direct attack on context-window myopia.
- Benefit 2/3, dynamic model routing plus cost and speed: foundational docs (e.g. core DSL design) can go to a larger model while downstream docs use smaller cheaper models; a full clean-slate regeneration takes 1.5–3 hours and costs ~100 USD via Claude Code (~20% of a weekly Claude Max budget), making continuous full rebuilds practical.
- Doc style is bottom-up, not top-down: instead of only tests and high-level rules ("a constitution the generator must obey"), docs center on step-by-step worked examples — executable-in-your-head vignettes ("on a 2x2x2 torus with wraparound, the per-node link count is 3, not 6; the all-gather of V bytes therefore costs ...") that act as in-context demonstrations pinning down semantics prose leaves ambiguous.
- Every number-bearing doc ends with a reconciliation anchor: a small preset whose expected outputs are stated exactly and enforced by generated tests.

## 3. [[wiki/03-symbolic-ir-and-builder-dsl|A Minimal Symbolic IR for Performance Co-design: The Op Abstraction and Builder DSL]]

**In one sentence:** SMART models any ML workload as a single recursively defined `Op` (loop-nest/subgraph interior nodes plus TPU-priced leaf ops carrying SymPy cost expressions and resource reservation tables), authored through a thin tracing DSL where distribution is expressed as sharding annotations with collectives inferred, not hand-placed.

- The `Op` has: symbolic-shape `inputs`/`outputs` tensors; a `cost: OpCost` of SymPy expressions per key cost (compute, memory, comm); an `rrt: RRT` resource reservation table (rows = resources, cols = cycles, cell = units used, e.g. ("MXU", cycle 3) -> 1); and `params` that make it recursive: `Union[InnerLoop(n_iter, body: Graph), GraphParams(graph), LeafParams(...)]`.
- An Op is either an interior node (a loop with trip count + body graph, or a plain subgraph) or a leaf where software meets system: the system side specifies the RRT and OpCost. Leaves are TPU-shaped: `mxu_op` (MXU matmul tile), `load_tile_to_vmem` (VMEM tile load), `allgather` (ICI collective).
- Factoring rule: the algorithm side composes leaves into loop nests, the system side prices them — swapping either side (a new attention variant, a new interconnect generation) touches only its own docs, which is what keeps abstractions stable under architecture churn.
- Builder DSL: models are authored in a thin Python-embedded tracing DSL, never by hand-constructing Ops — decorated blocks trace into named subgraphs, decorated loops become `InnerLoop` nodes (`@smart_loop` = true reduction with carried accumulator, `@smart_map_loop` = parallel map), builder calls emit system-priced leaves; every dimension is a SymPy symbol so trip counts like `Tq/qblk` stay symbolic and one trace serves the whole design space.
- Listing 1 (flash-attention core): a `@smart_map_loop` over query tiles (`n_iter=T_q/q_blk`) containing a `@smart_loop` reduction over KV tiles, with `mxu_op("bhte,bhse->bhts")` scores and `mxu_op("bhts,bhse->bhte")` attention-value products; the (B, H, Tq, Tkv) score matrix never leaves VMEM, and asymmetric Tq/Tkv lets the same nest serve prefill (Tq = Tkv = T) and flash-decoding (Tq = 1, Tkv = Tctx).
- Distribution via sharding annotations, not hand-placed collectives: tensors name the mesh axes each dimension is sharded on, and a sharded-einsum wrapper infers collectives from operand/output shardings (just-in-time AllGather of a sharded contracting weight, ReduceScatter when an output is reduced over a sharded dimension); only layout-moving collectives are explicit (DeepSeekMoE dispatch `all_to_all` moving the expert-parallel axis from token-group onto expert dimension, combine moving it back).

## 4. [[wiki/04-rollup-modes-validation-conclusion|Roll-up Modes, Symbolic Propagation, Validation, and Conclusion]]

**In one sentence:** Per-op costs become wall-clock time via a fast closed-form analytical roll-up for thousand-point sweeps or a slow modulo-scheduling roll-up for fine-grained studies, all propagated symbolically in SymPy with numerics bound only at the edge — and regenerated implementations reproduce hand-audited references (including DeepSeekV3 serving on a TPU pod slice) to round-off precision.

- Fast mode rolls loops up coarsely: each leaf's cost is scaled by the product of enclosing trip counts, and overlap effects (weight pre-collection, all-to-all hiding) are modeled as composable transforms in the style of a roofline bound (Williams et al., 2009) — closed-form evaluation fast enough for sweeps over thousands of design points.
- Slow mode modulo-schedules (Rau, 1994) each loop into its resource reservation table — software-pipelining the body against per-resource capacity — and the achieved initiation interval rolls up recursively up the tree, giving dependency- and resource-aware schedules for the design points that sweeps flag as interesting.
- The two modes form a funnel: fast mode screens thousands of points, slow mode studies the interesting ones in depth.
- Symbolic propagation: every roll-up produces a closed-form SymPy expression in the design space's free variables (batch, sequence length, bandwidths, mesh axes, datatype widths); numeric binding happens only at the edge — one substitution per design point — so a single symbolic build serves an entire sweep, and a doc can even state the exact expected expression for a collective's cost with generated tests asserting it.
- Validation headline: regenerated implementations reproduce hand-audited reference models — including DeepSeekV3 serving on a TPU pod slice — to round-off precision, which is the paper's evidence that docs (not code) can be the durable artifact for ML-systems co-design tools.
- Scale of the system today: ~50 design docs (~9,000 lines of specification prose) spanning TPU topology, collective cost models, numerics, schedulers, and a catalog of frontier model families (dense, MoE, latent-attention, robotics/VLA variants); master holds only docs plus a handful of leaf utilities, rebuilt by sub-agent orchestration on every version change.
- The closing argument: regenerating from docs pays the incremental-patching debt of Equation (1) to zero at every regeneration and surfaces vague intent early; the enablers (worked-example docs, machine-discovered dependency DAG, minimal symbolic IR) should generalize wherever specs churn faster than software absorbs them.

## The argument in five moves

1. Performance-modeling code rots from both directions (models above, hardware below), and patching compounds the debt (Equation 1) while context-starved agents add myopic damage.
2. So keep only docs: a DAG of self-contained markdown files is the master branch; humans edit prose, agents regenerate all code topologically from scratch.
3. Make docs regenerable: worked-example vignettes with exact numbers plus reconciliation anchors, and machine-inferred DAG edges with an orchestrator log guiding doc refinement.
4. Make the specified system regenerable: one recursive symbolic Op type, a tracing DSL, sharding-inferred collectives, and a fast/slow roll-up funnel with edge-bound SymPy symbolics.
5. It works: round-off agreement with hand-audited references (DeepSeekV3 on TPU) at 1.5–3 h / ~100 USD per rebuild — therefore docs, not code, can be the durable artifact.
