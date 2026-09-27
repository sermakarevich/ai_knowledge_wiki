> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Term Alignment and Evaluation Metrics
**In one sentence:** Generated ontologies can use different labels for the same class or property, so CQ4OE aligns gold and predicted terms with an aggregated five-method similarity pipeline and then computes CQ2Term term-level and CQ2Onto ontology-level (term, characteristic, triple, axiom, hierarchy-closure) metrics over that alignment.
## Key points
- Label variation (e.g., `hasPart` vs. `containsComponent`) motivates aligning gold and predicted terms before computing CQ2Term and CQ2Onto metrics.
- Seven candidate similarity methods were reduced to five: WordNet synonym matching was excluded for poor domain-term coverage and information-content similarity because it requires a shared taxonomy.
- The final pipeline uses hard exact-string matching, difflib SequenceMatcher sequence matching, Levenshtein and Jaro–Winkler via textdistance, and embeddinggemma-via-Ollama semantic similarity.
- Standalone per-method P/R/F1 use thresholds 1.0 for hard matching, 0.8 for lexical similarities, and 0.6 for semantic similarity; the methods have complementary failure modes (lexical misses paraphrases, semantic gives false positives on short labels).
- Aggregated pair score uses a hard-match override plus the mean of the three highest non-hard method scores, so no single low-scoring method can veto a reasonable match.
- One-to-one alignment applies type-specific thresholds (τC = 0.6 for classes, τP = 0.7 for properties, chosen from {0.5, 0.6, 0.7} on a held-out subset), ranks passing pairs by decreasing score with hard matches prioritized, and selects greedily; the higher property threshold counters spurious matches on short formulaic labels (e.g., `has_`/`is_` prefixes concentrating at 0.6–0.65).
- CQ2Term reports global P/R/F1 over combined term sets (TP = |α|, FP = |Tp| − |α|, FN = |Tg| − |α|) plus CQ-conditioned at-least-one, mean, and full coverage, capturing models that recover vocabulary without attaching terms to the right CQ.
- CQ2Onto evaluates five targets (term recovery, property characteristics, domain/range triples, TBox axioms, HermiT hierarchy closure) with global and alignment-conditioned views, strict equivalence counting, an embedding-cosine diagnostic, and axiom-level plus closure-recovered CQ coverage over required TBox axiom sets Ai.
---
## Term alignment pipeline
**Covers:** Section 4.1 — label variation through five-method pipeline

Generated ontologies "can use labels that differ from the gold standard while denoting the same class or property (e.g., hasPart vs. containsComponent), so we align the gold and predicted terms before computing the CQ2Term and CQ2Onto metrics."

Excluded candidates: "WordNet-based synonym matching [50] due to poor coverage of domain terms and information-content similarity [47,29] as it requires a shared taxonomy."

Final five methods:

| Method | Implementation |
|---|---|
| Hard matching | exact string equality |
| Sequence matching | Python `difflib.SequenceMatcher` |
| Levenshtein | `textdistance` library |
| Jaro–Winkler | `textdistance` library |
| Semantic similarity | `embeddinggemma` served via Ollama |

Standalone reporting: "Precision (P), Recall (R), and F1 are reported per method, using thresholds of 1.0 for hard matching, 0.8 [14] for lexical similarities, and 0.6 [46] for semantic similarity."

Rationale for aggregation: "the methods exhibit complementary failure modes, with exact and lexical matching missing paraphrases, while semantic matching can introduce false positives on short labels."

## Aggregated alignment score and one-to-one selection
**Covers:** Section 4.1 — aggregation formula through alignment set α

Let Tg and Tp denote the gold-standard and predicted term sets, aligned between terms of the same type. Each of the five methods produces sm(tg, tp) ∈ [0, 1] per candidate pair.

Aggregated score: 1 if hard match equals 1, otherwise the mean of the three highest non-hard method scores (Top3). "This aggregation mechanism prevents any single method with a lower score from vetoing a reasonable matching result."

Thresholding and selection:
- "A candidate pair passes thresholding if its score reaches the type-specific threshold τ."
- "We selected τC = 0.6 for classes and τP = 0.7 for properties by inspecting correct and spurious alignments at {0.5, 0.6, 0.7} on a held-out subset."
- "The higher property threshold reduces false matches on short formulaic labels (e.g., has_, is_ prefixes), where spurious matches concentrate around 0.6–0.65."
- "Pairs passing thresholding are ranked by decreasing aggregated score, with hard matches prioritized, and selected greedily to obtain a one-to-one alignment: (tg, tp) is kept only if both terms are still unmatched."
- "The same procedure is applied per standalone method using its own score, enabling comparable per-method P/R/F1."
- "The accepted pairs form the final alignment set α = αC ∪ αP, where αC contains accepted class pairs and αP contains accepted property pairs."
- "Since α is a set of one-to-one pairs, we use it in both directions to translate between gold and predicted vocabularies."

## Metric overview (Table 2)
**Covers:** Table 2 — reported metrics per evaluation target

"Table 2 gives an overview of the metrics reported for each evaluation target."

"AC scores use only structures whose named terms align under the alignment set α, G denotes global scores, computed over the full gold and predicted sets. Per-method reports standalone P/R/F1 for the five similarity methods. Diag. denotes standalone embedding-cosine diagnostics. CQ reports at-least-one, mean, and full coverage over terms (t), axiom-level matches (a), or closure-recovered axioms (c)."

| Evaluation tasks | Per-method | Diag. | P/R/F1 (AC) | P/R/F1 (G) | CQ cov. |
|---|---|---|---|---|---|
| Class & property (CQ2Term) | ✓ | — | — | ✓ | t |
| Class & property (CQ2Onto) | ✓ | — | — | ✓ | — |
| Property characteristics | — | — | ✓ | ✓ | — |
| Triple | — | ✓ | ✓ | ✓ | — |
| Axiom-level | — | ✓ | ✓ | ✓ | a |
| Hierarchy closure | — | — | — | ✓ | c |

## CQ2Term evaluation
**Covers:** Section 4.2 — term-level task, global metrics, CQ-conditioned coverage

"CQ2Term is the term-level task in CQ4OE. It evaluates the explicit term sets TiCQ2Term defined in Section 3. The LLM prediction for each CQ is denoted by T̂iCQ2Term." Combined sets: TgCQ2Term = ∪i TiCQ2Term and TpCQ2Term = ∪i T̂iCQ2Term. "The final alignment α = αC ∪ αP from Section 4.1 is applied separately for classes and properties."

Global term-level metrics over combined sets with |α| accepted pairs: "TP = |α|, FP = |TpCQ2Term| − |α|, and FN = |TgCQ2Term| − |α|. Precision P = TP/(TP + FP), Recall R = TP/(TP + FN), and F1 = 2PR/(P + R)." "We set F1 = 0 when P + R = 0." Reported "per standalone similarity method and for the final aggregated alignment."

CQ-conditioned coverage: "a gold term for cq i counts as covered only if α aligns it to a term predicted for cq i. Let covi be the proportion of required explicit terms covered for cq i, and N the number of retained CQs." Definitions: "A1 = |{i : covi > 0}|/N, MC = Σi covi/N, and FC = |{i : covi = 1}|/N", where A1 is at-least-one coverage (share of CQs with ≥1 required term recovered), MC is mean coverage, and FC is full coverage (share whose required terms are all recovered).

"The two views thus capture complementary failure modes, since a model may recover the required vocabulary without attaching each term to the CQ that requires it, leaving individual CQs unanswered despite high overall scores."

## CQ2Onto evaluation
**Covers:** Section 4.3 — five targets, global/AC views, triple/axiom/closure scoring, CQ coverage, evaluation report

"CQ2Onto evaluates LLM-generated ontologies against the ontology-level gold standard defined in Section 3.3 using five evaluation targets: term recovery, property characteristics, domain/range triples, TBox axioms, and hierarchy closure."

Views: "For property characteristics, domain/range triples, and TBox axioms, we report a global view over the full gold and predicted element sets, and an alignment-conditioned (AC) view restricted to elements whose named terms align under αC and αP. Term recovery is reported only globally" because "term recovery itself evaluates how well α recovers gold terms. An AC view here would only evaluate α in terms that have already been aligned. Hierarchy closure is reported as a single set-based metric over inferred subsumptions translated through α."

Target definitions:
- "Term recovery compares predicted and gold class and property vocabularies using both the final alignment αC ∪ αP and the five standalone similarity methods."
- "Property characteristics compare OWL property characteristic axioms (functional, symmetric, etc.) between aligned property pairs."
- "Domain/range triples assess graph structure by treating domain and range axioms as triples (s, p, o). Properties are compared through αP, class-valued domains and ranges through αC, and datatype ranges by normalized string equality. Triples involving complex anonymous OWL expressions are excluded here and evaluated at the axiom level."
- "TBox axioms compare structural decompositions of TBox axioms, recursively translating named terms through αC and αP and matching datatypes, cardinalities, intersections, unions, and restrictions strictly."
- "Hierarchy closure uses HermiT to compare inferred class and property subsumption closures of the gold and predicted ontologies (with the predicted closure translated to gold vocabulary through α), capturing hierarchy relations that may be entailed rather than explicitly asserted."
- "For domain/range triples and TBox axioms, we additionally report an embedding-cosine diagnostic over normalized textual serializations, which does not affect strict P/R/F1."

P/R/F1 counting: "For term recovery and the non-closure structural targets, P/R/F1 follow Section 4.2. For each target and view, TP counts one-to-one matched pairs that are strictly equivalent, unmatched predicted elements count as FP, unmatched gold elements count as FN, and matched but non-equivalent pairs count as both FP and FN."

Hierarchy closure: "let Clg be the gold closure and Clgp the predicted closure translated to the gold vocabulary through α. We define TP = |Clg ∩ Clgp|, FN = |Clg| − TP, and FP = |Clgp| − TP + U, where U counts predicted closure pairs that cannot be translated through the alignment and are therefore counted as additional FP."

CQ coverage in CQ2Onto (two forms, each summarized with A1/MC/FC): "axiom-level coverage and closure-recovered coverage," computed "over required TBox axioms rather than explicit terms. Let Ai denote the set of TBox axioms required to answer cq i." Axiom-level: "covᵢ^axiom = #axiom-level matches in Ai / |Ai|." Closure-recovered: "checks whether hierarchy-related gold axioms missed by axiom-level matching can be recovered through HermiT reasoning. Only missed hierarchy-related axioms are eligible for closure recovery. They are counted only if they can be decomposed into atomic Subclass or Subproperty pairs, including EquivalentClasses axioms whose IntersectionOf or UnionOf operands yield such pairs and all extracted pairs appear in Clgp. Closure-recovered axioms are counted only among axioms not already matched by the axiom-level evaluation." Combined: "covᵢ^closure = (#axiom-level matches in Ai + #closure-recovered axioms in Ai) / |Ai|." Scope limit: "Closure recovery is restricted to gold axioms that are hierarchy-related and that decompose into atomic Subclass or Subproperty pairs. Other axioms are scored only by matching at the axiom-level."

Evaluation report: "The CQ4OE pipeline generates a Markdown report per-run that aggregates all metrics from Sections 4.2 and 4.3, organized by evaluation target. Each report includes standalone scores for the five similarity methods, the final one-to-one term alignment, TP/FN/FP, and CQ-level traces for matched, closure-recovered, and missed axioms, together with CSV exports of term alignments and per-axiom traces. Each closure-recovered axiom is tagged as directly asserted, chain-inferred, or complex-inferred. For chain-inferred cases, a breadth-first search reconstructs the shortest path through the predicted hierarchy, providing a human-readable explanation of the recovery."

**Covers:** Sections 4.1–4.3 and Table 2 (five-method alignment aggregation with τC = 0.6 / τP = 0.7; CQ2Term global and CQ-conditioned metrics; CQ2Onto term/characteristic/triple/axiom/closure metrics and per-run Markdown + CSV reports).
