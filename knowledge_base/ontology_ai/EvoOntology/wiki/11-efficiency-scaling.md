> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Efficiency and Scaling: Content Growth, Cost, and Attribution
**In one sentence:** Ontology content growth concentrates in the first three evolution rounds and then flattens alongside performance, while the ontology layer shortens trajectories enough to cut total tokens per task by ~20% and Tool-level edits contribute most of the accepted gain.
## Key points
- Terms grow from 61 in the Initial ontology to 80 after five accepted rounds on DDR-Bench under GPT-5.6-sol, with per-round growth of every tracked element falling below 5% after round three.
- Content-size curves flatten together with Trajectory-Wise performance, indicating expansion is concentrated in early rounds when recurrent semantic gaps are addressed.
- The Initial ontology raises average input tokens per turn from 3.2K to 4.1K due to the manifest and retrieved semantics, while output tokens per turn stay at 0.4K.
- Average trajectory length falls from 14.6 to 11.2 turns with the Initial ontology and to 8.4 turns with the Evolved ontology, cutting total cost from 52.6K to 50.4K to 42.0K tokens per task.
- The Evolved ontology total cost of 42.0K tokens is approximately 20% below Baseline, while Trajectory-Wise performance rises from 69.5 to 89.5 over the same comparison.
- Tool-level edits account for 57% of cumulative gain across six accepted rounds by improving how existing content is exposed through the manifest and MCP tools.
- Content-level edits contribute 34% across eleven accepted rounds and Schema-level edits contribute the remaining 9% across three accepted rounds, with Content edits more frequent and Schema edits addressing limitations not fixable by content changes alone.
---
## Content-layer growth across evolution rounds
**Covers:** Figure 6 section, DDR-Bench under GPT-5.6-sol

| Element | Initial | After five accepted rounds |
|---|---|---|
| Terms | 61 | 80 |
| Per-round growth, all tracked elements | — | <5% after round three |

> "most content growth occurs in the first three rounds."
> "The content-size curves then flatten together with Trajectory-Wise performance."
> "Content expansion is therefore concentrated in the early rounds, when the evolution loop addresses recurrent semantic gaps, and stabilizes once these gaps have been covered."

Tracked elements comprise the four node families — Terms, Mappings, Constraints, and Evidence — together with instantiated Semantic Relations.

## Cost of the ontology layer
**Covers:** Table 8 section, DDR-Bench averaged across the four-backbone analysis subset

| Metric | Baseline | Initial ontology | Evolved ontology |
|---|---|---|---|
| Output tokens / turn (K) | 0.4 | 0.4 | 0.4 |
| Turns / task | 14.6 | 11.2 | 8.4 |
| Total tokens / task (K) | 52.6 | 50.4 | 42.0 |
| Traj-Wise (%, up) | 69.5 | 81.8 | 89.5 |

Average input tokens per turn rise from 3.2K to 4.1K with the Initial ontology because of the manifest and retrieved semantics. The layer adds modest per-turn context while reducing repeated schema discovery over the full trajectory, and evolution strengthens this effect by improving how the agent discovers and grounds relevant semantics.

## Attribution across editable levels
**Covers:** Figure 7 section, accepted evolution gain aggregated over the four-backbone analysis subset

| Level | Share of cumulative gain | Accepted rounds |
|---|---|---|
| Tool | 57% | 6 |
| Content | 34% | 11 |
| Schema | 9% | 3 |

> "These edits mainly improve how existing ontology content is exposed through the manifest and MCP tools."
> "Content edits are more frequent, while Tool edits contribute the largest share of the accumulated gain."

Each accepted round is grouped by its attribution tag and the paired-evaluation improvement contributed by each group is aggregated across the four backbones.

## Case study: evolution of card-legality semantics
**Covers:** Figure 8 opening, text-to-SQL card-legality case

A representative text-to-SQL case requires identifying cards banned in a target game format and illustrates a localized Content-level update extending the ontology without rewriting existing Tool or Schema layers. Initial state: the Initial ontology L0 contains the Terms Card and Legality with an association between them; Card is grounded to Cards.uuid and Legality to legalities.uuid. Tool Layer (both L0 and evolved Lt): Tool 1 browse finds relevant terms (Query to Ranked Terms); Tool 2 resolve retrieves complete semantics (Term IDs to Mappings, Relations, Constraints, and Evidence).
