> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evolution Dynamics: Pairwise Overlap and Cross-Backbone Transfer

**In one sentence:** Different backbones evolve distinct ontology stores from the same initialization (no Term-identifier pair exceeds 0.62 Jaccard overlap), and each store performs best on its own backbone, with every cross-backbone transfer dropping Traj-Wise performance by at least 6.6 points.

## Key points
- Pairwise Jaccard overlap of accepted Term-identifier sets on DDR-Bench never exceeds 0.62 across the four backbones (Figure 5a).
- The two Claude backbones share less with each other (0.55) than the two GPT backbones do (0.61).
- Claude-Opus-4.8 retains more detailed manifest variants than Claude-Sonnet-5, while GPT-5.5 introduces short SQL fragment libraries under Evidence absent from the Claude-Opus-4.8 ontology.
- Identifier overlap alone cannot determine semantic equivalence because different identifiers may encode similar concepts.
- In cross-backbone transfer (Figure 5b), the diagonal is uniformly the highest entry of its column, with every off-diagonal dropping at least 6.6 points relative to the same-backbone store.
- The average column drop from diagonal to off-diagonal ranges from −6.6 (Sonnet-5) to −10.9 (GPT-5.5), indicating backbone-specific evolution is beneficial.
- Context from the same chunk: single-level evolution gains are +13.2 (Tool-only), +8.7 (Content-only), +3.6 (Schema-only) versus +20.0 for the full three-level loop; masking Mappings drops −13.4 and Evidence −8.7 Traj-Wise.

---

## Single-level vs full three-level evolution

Restricting the evolution loop to a single level at a time and comparing against the full three-level variant on DDR-Bench, averaged across the four backbones (Table 6):

| Variant | Gain over Baseline |
|---|---|
| Tool-only | +13.2 |
| Content-only | +8.7 |
| Schema-only | +3.6 |
| Full three-level loop | +20.0 |

> "Tool-only evolution recovers the largest single-level gain (+13.2 over Baseline), consistent with the manifest reshaping being the dominant lever surfaced by the attribution analysis in Figure 7."

> "The results indicate that the three levels are complementary and not substitutable, which validates the design of an evolution loop that ranges over all three editable levels."

## Ablation study on ontology structure

Masking each removable object family from the final Evolved ontology on DDR-Bench, average Traj-Wise performance across four backbones (Table 7):

| Masked family | Traj-Wise drop |
|---|---|
| Mappings | −13.4 |
| Evidence | −8.7 |
| Constraints | −3.5 |
| Relations | −2.1 |
| Terms | cannot be masked in isolation as every other family references them |

> "Masking Mappings causes the largest drop (−13.4 Traj-Wise), which is consistent with the role of Mappings as the only object that grounds a Term to concrete columns and join paths."

> "Masking Evidence drops by −8.7, because without a probe query the agent cannot verify a candidate SQL fragment against the underlying value distribution."

> "These findings identify Mappings and Evidence as the two load-bearing families, which validates our decision to require every committed entry to be anchored in a probe query and not a natural-language description alone."

## Divergence across backbones

> "We investigate whether different backbones converge to similar ontologies or develop distinct ones by comparing the pairwise Jaccard overlap of their accepted Term-identifier sets on DDR-Bench."

Figure 5a results:

| Pair | Jaccard overlap |
|---|---|
| Maximum over all pairs | ≤ 0.62 |
| Claude–Claude | 0.55 |
| GPT–GPT | 0.61 |

> "For example, Claude-Opus-4.8 retains more detailed manifest variants than Claude-Sonnet-5, while GPT-5.5 introduces short SQL fragment libraries under Evidence that do not appear in the Claude-Opus-4.8 ontology."

> "However, identifier overlap alone cannot determine semantic equivalence, since different identifiers may encode similar concepts."

## Cross-backbone transfer

Each evolved store is applied to all four backbones and Traj-Wise performance measured on DDR-Bench (Figure 5b; each row fitted on one backbone, served to every backbone as columns):

- The diagonal is uniformly the highest entry of its column.
- Every off-diagonal drops by at least 6.6 points relative to the same-backbone store.
- The average column drop from diagonal to off-diagonal ranges from −6.6 (Sonnet-5) to −10.9 (GPT-5.5).

> "These results show that different backbones produce different evolved ontology stores from the same initialization."

> "The cross-backbone transfer results further indicate that backbone-specific evolution is beneficial."

## Conclusion (as stated in chunk)

> "In this paper, we introduce EvoOntology, an interactive ontology layer that is automatically constructed and self-evolving for data agents."

> "EvoOntology encapsulates the ontology as an MCP server that the agent actively queries at runtime, and refines it through attribution-guided typed edits admitted only after a backbone-conditional paired evaluation gate."

> "Experiments on benchmarks and six LLM backbones, EvoOntology consistently outperforms both ReAct baselines and traditional semantic-layer baselines, offering an effective solution for helping data agents understand heterogeneous data."

**Covers:** Figure 5a (pairwise Jaccard overlap of accepted Term identifiers between evolved stores of four backbones) / Figure 5b (cross-backbone transfer of evolved store on DDR-Bench) plus adjoining single-level ablation, structure-masking ablation, Divergence across Backbones, and Conclusion text in chunk 10-a-pairwise-jaccard-overlap-of-b.
