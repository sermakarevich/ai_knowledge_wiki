> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# TABLE IV Performance on STIX and MALOnt: Predicate Ontology Typing Results

**In one sentence:** ANCHOR achieves the highest average predicate-typing F1 (0.5484) with its largest gains on UCO (+29.5%) and STIX (+9.4%) while trailing LLM4CTI slightly on small MALOnt (−4.3%), confirming that predicate typing is harder than entity typing for all systems and that hybrid search-plus-navigation matters most on large schemas.

## Key points

- TABLE IV reports predicate-typing F1 on UCO / STIX / MALOnt / average: TTPDrill 0.0033 / 0.0000 / 0.0000 / 0.0011; CTINexus 0.1282 / 0.4289 / 0.4528 / 0.3366; LLM4CTI 0.4000 / 0.5355 / 0.5647 / 0.5001; ANCHOR 0.5180 / 0.5860 / 0.5412 / 0.5484.
- ANCHOR beats LLM4CTI by 29.5% on UCO (0.4000 to 0.5180) and by 9.4% on STIX (0.5355 to 0.5860), but scores 4.3% below LLM4CTI on MALOnt (0.5412 vs. 0.5647).
- TTPDrill records zero on STIX and MALOnt predicate typing because "its template-based approach cannot produce property URIs outside the predefined ATT&CK vocabulary."
- Entity-typing context (Table III): ANCHOR averages 0.7371 and beats LLM4CTI by 62.5% on UCO (0.4521 to 0.7347), 10.6% on STIX (0.7886 to 0.8724), and 0.7% on MALOnt (0.6891 to 0.6942); CTINexus drops 30.3% scaling from MALOnt (0.6370) to UCO (0.4439); TTPDrill "never exceeds 0.2305 on any schema."
- Predicate typing is harder than entity typing for all four systems: "ANCHOR drops by 25.6% (from 0.7371 to 0.5484) and LLM4CTI drops by 22.2% (from 0.6432 to 0.5001)."
- The gap widens as schema size grows (75 classes in MALOnt to 419 in UCO): prompt-based baselines "exhaust the LLM context window and degrade due to the 'lost in the middle' phenomenon [25]," while ANCHOR "retrieves only the relevant ontology fragments and remains stable on the larger schema."
- Ablation (Table V, ground-truth inputs): Hybrid scores 0.9364 on entity typing and 0.7843 on predicate typing; on entities Search-Only (0.9184) nears Hybrid while Recurse-Only falls to 0.7914, whereas on predicates Recurse-Only reaches 0.6416 while Search-Only "collapses to 0.3142"; Hybrid improves 22.2% over Recurse-Only (0.6416 to 0.7843) and "more than doubles the score of Search-Only."

---

## Entity ontology typing (Table III context)

**Covers:** entity-typing results paragraph (Table III)

"For each extracted entity, the system selects the best-matching class URI from the target ontology. As shown in Table III, ANCHOR achieves the highest performance on every schema, with an average F1 of 0.7371."

"Specifically, ANCHOR outperforms the second-best baseline (LLM4CTI) by 62.5% (from 0.4521 to 0.7347) on the UCO schema. The margin shrinks on smaller schemas: ANCHOR outperforms LLM4CTI by 10.6% (from 0.7886 to 0.8724) on STIX and by 0.7% (from 0.6891 to 0.6942) on MALOnt."

"CTINexus, which includes the entire schema in the LLM prompt, suffers a 30.3% performance drop when scaling from MALOnt (0.6370) to UCO (0.4439). TTPDrill never exceeds 0.2305 on any schema because it relies on a simple rule-based pipeline."

"We observe that this performance gap widens as the schema size grows... As the number of candidate classes increases from 75 in MALOnt to 419 in UCO, prompt-based baselines exhaust the LLM context window and degrade due to the 'lost in the middle' phenomenon [25]. In contrast, ANCHOR retrieves only the relevant ontology fragments and remains stable on the larger schema. The small performance difference on MALOnt indicates that hybrid ontology discovery offers limited benefit when the schema fits easily within a single prompt."

## Predicate ontology typing (TABLE IV)

**Covers:** TABLE IV plus predicate-typing analysis paragraphs

"The system maps each extracted relation predicate to a formal property URI (either ObjectProperty or DatatypeProperty). As shown in Table IV, ANCHOR achieves the highest average F1 of 0.5484, outperforming the baselines on the UCO and STIX schemas."

| System | UCO | STIX | MALOnt | Average |
|---|---|---|---|---|
| TTPDrill [11] | 0.0033 | 0.0000 | 0.0000 | 0.0011 |
| CTINexus [16] | 0.1282 | 0.4289 | 0.4528 | 0.3366 |
| LLM4CTI [17] | 0.4000 | 0.5355 | 0.5647 | 0.5001 |
| ANCHOR | 0.5180 | 0.5860 | 0.5412 | 0.5484 |

"Specifically, ANCHOR outperforms LLM4CTI by 29.5% (from 0.4000 to 0.5180) on UCO and by 9.4% (from 0.5355 to 0.5860) on STIX. On MALOnt, ANCHOR scores 0.5412, which is 4.3% below LLM4CTI at 0.5647. TTPDrill records zero" on STIX/MALOnt, "since its template-based approach cannot produce property URIs outside the predefined ATT&CK vocabulary."

"Predicate ontology typing is more difficult than entity ontology typing for all four systems: ANCHOR drops by 25.6% (from 0.7371 to 0.5484) and LLM4CTI drops by 22.2% (from 0.6432 to 0.5001). The gap is intuitive since a predicate's correct property URI depends not only on the surface verb but also on the domain and range of its subject and object entities, and on the direction of the edge (e.g., uses vs. used by). Single-word embedding similarity alone is therefore insufficient, and the schema-navigation component of hybrid ontology discovery becomes the main contributor to predicate ontology typing, as analyzed in Section V-B."

"The marginal underperformance of ANCHOR on MALOnt (0.5412 vs. 0.5647 for LLM4CTI) is consistent with our earlier observation that hybrid ontology discovery offers limited advantage on small schemas."

"The key findings from the ontology typing analysis are summarized as follows: (i) ANCHOR generalizes to large hierarchical schemas where prompt-based schema inclusion baselines collapse, and (ii) predicate typing remains a harder task than entity typing for all four systems, motivating the ablation study on hybrid ontology discovery in Section V-B."

## Ablation study setup and effect of hybrid discovery (Table V, partial)

**Covers:** Section V-B opening + V-B.1 (figure caption bytes at chunk tail are garbled and omitted)

"We isolate two design choices within hybrid ontology discovery: (i) the combination of embedding search and recursive schema navigation, and (ii) the embedding-similarity threshold tau that controls when the system switches from search to recursive traversal. For both ablations, we use ground-truth entities and triplets as fixed inputs so that the reported scores reflect only the typing performance of each configuration, while all other parameters (ontology schema, candidate inventory, scoring rule) remain unchanged."

"We evaluate three configurations on both ontology typing tasks: Hybrid (ANCHOR), Search-Only, and Recurse-Only. The Hybrid configuration combines embedding-based search with hierarchical recursive navigation, while the others rely solely on one of these strategies."

"As shown in Table V, the Hybrid configuration achieves the highest performance on both tasks, scoring 0.9364 on entity typing and 0.7843 on predicate typing, while the two single-strategy baselines exhibit asymmetric behavior. On entity ontology typing, Search-Only (0.9184) approaches the Hybrid score, whereas Recurse-Only falls to 0.7914. The pattern reverses on predicate ontology typing: Recurse-Only reaches 0.6416, while Search-Only collapses to 0.3142. Notably, the Hybrid configuration improves performance by 22.2% (from 0.6416 to 0.7843) over Recurse-Only and more than doubles the score of Search-Only."

"Entity ontology typing maps a single named entity to a class, a problem that aligns well with semantic similarity over class names and descriptions, so embedding search alone suffices in most cases. In contrast, predicate ontology typing requires reasoning over the subject-object relation, the property hierarchy, and directional constraints that distinguish subject from object, all of which are structurally represented in the schema and accessed through recursive navigation rather than lexical similarity."

Note: the chunk tail contains an Appendix A fragment ("instrumented measurements show that 91.0% of entity-class...") and a figure-caption byte sequence that are truncated/garbled in the chunk body, so they are not quoted here beyond that partial clause.

**Covers:** chunk 06-table-iv-performance-on-stix-and (TABLE IV predicate results on STIX/MALOnt/UCO with entity-typing context and Section V-B hybrid-ablation opening; chunk tail figure bytes garbled)
