> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# A Minimal Symbolic IR for Performance Co-design: The Op Abstraction and Builder DSL

**In one sentence:** SMART models any ML workload as a single recursively defined `Op` (loop-nest/subgraph interior nodes plus TPU-priced leaf ops carrying SymPy cost expressions and resource reservation tables), authored through a thin tracing DSL where distribution is expressed as sharding annotations with collectives inferred, not hand-placed.

## Key points

- The `Op` has: symbolic-shape `inputs`/`outputs` tensors; a `cost: OpCost` of SymPy expressions per key cost (compute, memory, comm); an `rrt: RRT` resource reservation table (rows = resources, cols = cycles, cell = units used, e.g. ("MXU", cycle 3) -> 1); and `params` that make it recursive: `Union[InnerLoop(n_iter, body: Graph), GraphParams(graph), LeafParams(...)]`.
- An Op is either an interior node (a loop with trip count + body graph, or a plain subgraph) or a leaf where software meets system: the system side specifies the RRT and OpCost. Leaves are TPU-shaped: `mxu_op` (MXU matmul tile), `load_tile_to_vmem` (VMEM tile load), `allgather` (ICI collective).
- Factoring rule: the algorithm side composes leaves into loop nests, the system side prices them — swapping either side (a new attention variant, a new interconnect generation) touches only its own docs, which is what keeps abstractions stable under architecture churn.
- Builder DSL: models are authored in a thin Python-embedded tracing DSL, never by hand-constructing Ops — decorated blocks trace into named subgraphs, decorated loops become `InnerLoop` nodes (`@smart_loop` = true reduction with carried accumulator, `@smart_map_loop` = parallel map), builder calls emit system-priced leaves; every dimension is a SymPy symbol so trip counts like `Tq/qblk` stay symbolic and one trace serves the whole design space.
- Listing 1 (flash-attention core): a `@smart_map_loop` over query tiles (`n_iter=T_q/q_blk`) containing a `@smart_loop` reduction over KV tiles, with `mxu_op("bhte,bhse->bhts")` scores and `mxu_op("bhts,bhse->bhte")` attention-value products; the (B, H, Tq, Tkv) score matrix never leaves VMEM, and asymmetric Tq/Tkv lets the same nest serve prefill (Tq = Tkv = T) and flash-decoding (Tq = 1, Tkv = Tctx).
- Distribution via sharding annotations, not hand-placed collectives: tensors name the mesh axes each dimension is sharded on, and a sharded-einsum wrapper infers collectives from operand/output shardings (just-in-time AllGather of a sharded contracting weight, ReduceScatter when an output is reduced over a sharded dimension); only layout-moving collectives are explicit (DeepSeekMoE dispatch `all_to_all` moving the expert-parallel axis from token-group onto expert dimension, combine moving it back).

---

## The Op abstraction

```
Op:
  inputs:  List[Tensor]   # symbolic shapes
  outputs: List[Tensor]
  cost:    OpCost         # SymPy exprs per key cost (compute, memory, comm)
  rrt:     RRT            # rows = resources, cols = cycles, cell = units used
  params:  Union[InnerLoop(n_iter, body: Graph), GraphParams(graph), LeafParams(...)]
```

The design demands behind this shape: abstractions must be few, orthogonal, and stable under architecture churn (reliable regeneration constrains the specified artifact, not just the doc style). Recursion is the whole trick — one node type covers a matmul tile and an entire MoE block. The RRT example ("MXU", cycle 3) -> 1 shows leaves carry fine-grained resource-vs-time occupancy, which is what the slow scheduling mode consumes.

## The builder DSL and flash attention

The DSL keeps model authors away from raw Op construction: decoration + tracing produces the graph. The `@smart_loop` vs `@smart_map_loop` distinction (reduction with accumulator vs parallel map) is semantic, not syntactic sugar — it determines how the roll-up treats the loop. Symbolic dimensions throughout mean one trace covers prefill and decode, one build covers a sweep (see [[wiki/04-rollup-modes-validation-conclusion|Roll-up Modes and Validation]]).

## Sharding-annotated distribution

The distribution design pushes placement intelligence into inference (the sharded-einsum wrapper) rather than author-written collectives. Authors declare sharding; the wrapper derives the communication. The DeepSeekMoE exception proves the rule: only collectives that move data layout between sharding schemes (dispatch/combine `all_to_all`) are written explicitly.

**Covers:** Section 3, paragraphs 1–5 (Op abstraction, builder DSL, Listing 1, distribution/sharding, DeepSeekMoE block).
