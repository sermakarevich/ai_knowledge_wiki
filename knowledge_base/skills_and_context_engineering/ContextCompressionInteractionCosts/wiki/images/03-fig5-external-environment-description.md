**Figure 5 — External environment boundary (paired Δ retrieval-like actions).**

**What it shows.** A comparison of the *paired* change in retrieval-like actions (Sliding compression minus Full context) for the *same* sliding operator applied in two different environments. The point is to separate the cost of compression from the cost of the environment.

**Axes.**
- **Y-axis:** paired Δ retrieval-like actions, i.e., (Sliding − Full), ranging roughly from −10 to +60.
- **X-axis:** two categorical conditions — *IRBench* (synthetic, High regime) and *ALFWorld* (household).
- Each condition is drawn as a small boxplot/scatter of paired seeds: IRBench as a blue box with dispersed points; ALFWorld as a tight gray cluster.

**Trends.**
- **IRBench:** a large, clearly positive shift — the box and points sit high on the axis (on the order of +30). Sliding compression adds a substantial retrieval-like-action "surge."
- **ALFWorld:** the distribution collapses to roughly zero, symmetric about zero (a few points slightly positive, a few slightly negative). No surge.
- An orange callout explicitly links the two with "same sliding operator → no surge," emphasizing the operator is held constant while the outcome flips.

**Side panel (why the same operator diverges).** For IRBench the dropped state is a D-state (task graph) that is queryable but interaction-expensive and not re-derivable, so its loss forces defensive re-querying → surge. For ALFWorld the same lost facts are recoverable through ordinary interaction actions (look/examine/inventory), so no defensive re-querying → Δ ≈ 0.

**Takeaway.** The retrieval-like-action (reacquisition) signature is *environment-dependent*, not an intrinsic cost of the compression operator. What matters is whether the execution-relevant state that gets dropped can be re-observed; under that condition the identical sliding operator produces a large positive effect in IRBench but a near-zero, symmetric effect in ALFWorld. (Exact values are approximate: IRBench ≈ +30, ALFWorld ≈ 0.)