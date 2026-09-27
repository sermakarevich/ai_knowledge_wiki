---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Design Docs Are All You Need

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. Write out Equation (1) for incremental generation debt and explain, in your own words, why the authors claim human engineers in practice land far from the zero-debt ideal.

> [!tip]- Answer
> Dt+1 = G(St+1, Ct) - G(St+1): the distance between the incrementally patched system (new spec applied on top of old code) and the system that would have been built greenfield from the new spec alone. Humans land far from zero because deleting all of one's code and starting over is mentally challenging and time-consuming, so incremental patches carry forward compromises that compound with every spec revision. See [[wiki/01-motivation-and-regeneration-workflow|Motivation and Regeneration Workflow]].

### Q2. Contrast the two failure modes from Section 1 (incremental generation debt vs. context-window myopia): which one predates AI coding agents, and by what distinct mechanism does each one degrade structural coherence?

> [!tip]- Answer
> Incremental generation debt predates AI — it is the human habit of patching Ct into Ct+1 instead of rebuilding from St+1, compounding compromises. Context-window myopia is AI-era: finite context forces feeding agents fragmented snippets, so the agent misses global invariants and cross-module dependencies and emits locally plausible but globally sub-optimal code. One degrades through accumulated human compromise, the other through context-blind piecemeal updates. See [[wiki/01-motivation-and-regeneration-workflow|Motivation and Regeneration Workflow]].

### Q3. In Figure 1's workflow, what are the only artifacts humans ever edit, what gates a regenerated build before it replaces the previous one, and what flows back on failure?

> [!tip]- Answer
> Humans edit only the natural-language docs in the design-doc DAG checked into master. A regenerated build must pass validation — reference-model reconciliation, parameter guards, and unit tests — before replacing the previous build; on failure the repair path loops back into regeneration. The generated library itself is never hand-edited. See [[wiki/01-motivation-and-regeneration-workflow|Motivation and Regeneration Workflow]].

### Q4. The orchestrator maintains a central log during topological regeneration. What two kinds of entries does it record, and how do humans use it in the next version cycle?

> [!tip]- Answer
> It records (a) areas where sub-agents struggled to interpret the prose and (b) bugs uncovered in the output of agents from earlier topological waves. Humans use it as a prioritized editing list: the docs where agents struggled most are exactly the ones whose prose needs refinement and clarification next version (targeted human iteration). See [[wiki/02-design-docs-as-source-of-truth|Design Docs as Source of Truth]].

### Q5. The paper contrasts a top-down "constitution" doc philosophy with its own bottom-up ingredient. Name both, explain the mechanism by which the bottom-up ingredient helps in-context learning, and state what every number-bearing doc must end with.

> [!tip]- Answer
> Top-down: tests plus high-level rules the generator must obey. Bottom-up: step-by-step worked examples — executable-in-your-head vignettes tracing pseudo-code on a concrete input with exact intermediate shapes, values, and closed-form cost expressions (e.g. the 2x2x2 torus link-count vignette). They act as in-context demonstrations that pin down semantics prose alone leaves ambiguous (citing Brown et al. 2020, Dong et al. 2022). Every number-bearing doc must end with a reconciliation anchor: a small preset with exactly stated expected outputs enforced by generated tests. See [[wiki/02-design-docs-as-source-of-truth|Design Docs as Source of Truth]].

### Q6. Sketch the recursive Op type (fields and the params union), explain the algorithm-side vs. system-side split at leaf nodes, and state why that split keeps docs stable under churn.

> [!tip]- Answer
> Op has symbolic-shape inputs/outputs, cost: OpCost (SymPy exprs per key cost: compute, memory, comm), rrt: RRT (rows = resources, cols = cycles, e.g. ("MXU", cycle 3) -> 1), and params: Union[InnerLoop(n_iter, body: Graph), GraphParams(graph), LeafParams(...)]. Interior nodes are loops/subgraphs; leaves (mxu_op, load_tile_to_vmem, allgather) are where the system side specifies the RRT and OpCost while the algorithm side composes leaves into loop nests. A new attention variant touches only algorithm docs, a new interconnect generation only system docs. See [[wiki/03-symbolic-ir-and-builder-dsl|Symbolic IR and Builder DSL]].

### Q7. Using Listing 1, explain how a single flash-attention trace serves both prefill and flash-decoding, and how the DeepSeekMoE block demonstrates the "inferred, not hand-placed collectives" principle including its one exception.

> [!tip]- Answer
> The nest maps query tiles with @smart_map_loop and reduces over KV tiles with @smart_loop; because Tq/Tkv are symbolic and asymmetric, the same trace covers prefill (Tq = Tkv = T) and flash-decoding (Tq = 1, Tkv = Tctx), with the score matrix never leaving VMEM. Distribution is declared via sharding annotations while the sharded-einsum wrapper infers collectives (just-in-time AllGather of sharded contracting weights, ReduceScatter on reduced-sharded outputs); the sole explicit collectives are layout-moving ones — the DeepSeekMoE dispatch all_to_all shifting the expert-parallel axis from token-group to expert dimension (and combine shifting it back). See [[wiki/03-symbolic-ir-and-builder-dsl|Symbolic IR and Builder DSL]].

### Q8. Describe the fast/slow roll-up funnel (mechanism of each, and which feeds which), the edge-binding symbolic discipline, and the paper's headline validation result — then state what that validation does NOT establish.

> [!tip]- Answer
> Fast mode scales leaf costs by enclosing trip-count products with roofline-style overlap transforms (weight pre-collection, all-to-all hiding) to screen thousands of design points cheaply; slow mode modulo-schedules each loop into its RRT and rolls achieved initiation intervals recursively upward for dependency- and resource-aware schedules of the flagged points. All costs propagate as closed-form SymPy expressions in design-space variables with numeric binding only at the edge (one substitution per point), so one symbolic build serves a whole sweep. Headline validation: regenerated code reproduces hand-audited references including DeepSeekV3 on a TPU pod slice to round-off precision. What it does NOT establish: breadth — the number of references is unspecified, there are no error bounds or failure cases reported, and everything sits on one hardware family (TPU), so this is an existence proof, not a measured reliability rate. See [[wiki/04-rollup-modes-validation-conclusion|Roll-up Modes and Validation]].
