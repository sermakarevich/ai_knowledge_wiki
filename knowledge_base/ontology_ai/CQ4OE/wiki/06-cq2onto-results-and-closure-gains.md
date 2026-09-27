> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# CQ2Onto Results and Closure Gains
**In one sentence:** Fig. 3 summarizes CQ2Onto results averaged over nine LLMs across six domains as structural F1 and CQ-conditioned coverage before/after closure rescue, and the surrounding text argues that answering CQs requires recovering implicit and derived terms as coherent OWL structure with provenance-traceable, reusable evaluation, subject to alignment-dependence, restricted closure scope, and contamination caveats.
## Key points
- Fig. 3 reports CQ2Onto results across six benchmark domains with each (domain, strategy) cell averaged over nine LLMs in both panels.
- Panel (a) shows structural F1 across seven evaluation metrics, with AWO Triple cells shown as N/A because the gold range is a complex anonymous OWL expression.
- Panel (b) shows CQ-conditioned coverage before and after closure rescue, where ∆ is the gain in Mean coverage from closure rescue (Closure-Mean − Axioms-Mean).
- Answering a CQ requires moving beyond its explicit terms to recover implicit and derived terms, expressed as property characteristics, property triples, TBox axioms, and hierarchical structure under reasoner-derived closure.
- The CQ4OE pipeline produces per-run Markdown reports and CSV alignment exports tracing each metric back to specific gold and predicted axioms, distinguishing missing vocabulary, unstable property modeling, shallow hierarchy generation, and incomplete local-CQ coverage.
- Reuse is organized as parallel CQ2Term and CQ2Onto directories with gold standards, predictions, scripts, and aggregated reports; new LLMs are added via the predictions folder plus one script, and new domains via the four-phase annotation methodology of Section 3.2 under triple-review adjudication, with persistent W3ID metric identifiers and a public leaderboard.
- All ontology-level metrics depend on term alignment via combined hard, lexical, and semantic one-to-one selection with uniform thresholds τC and τP; closure rescue evaluates only hierarchy-related axioms decomposable into atomic SubClassOf or SubPropertyOf relations including EquivalentClasses with IntersectionOf or UnionOf; mean structural F1 remains low at 26.7% to 33.7% across models; and closure provides only limited recovery when the underlying hierarchy is missing, with performance varying more across domains than across models or generation strategies.
---
## Fig. 3: CQ2Onto results across six domains
**Covers:** Fig. 3 caption — panels (a) and (b)

"Fig. 3: CQ2Onto results across six benchmark domains, with each (domain, strategy) cell averaged over nine LLMs in both panels."

"(a) Structural F1 across seven evaluation metrics (AWO Triple cells shown as N/A because the gold range is a complex anonymous OWL expression)."

"(b) CQ-conditioned coverage before and after closure rescue, where ∆ shows the gain in Mean coverage from closure rescue (Closure-Mean − Axioms-Mean)."

## What CQ-conditioned evaluation requires
**Covers:** requirement from explicit terms to formal OWL

Models must "move beyond the explicit terms of each CQ to recover the implicit and derived terms that the answer also requires, and whether it can express them as a coherent ontology including property characteristics, property triples, TBox axioms, and hierarchical structure under reasoner-derived closure."

"This goes beyond lexical fluency, requiring the structural and inferential commitments that make a CQ formally answerable."

"The transition from natural-language requirements to formal OWL representations remains a central bottleneck in ontology engineering [31,32], which makes this resource particularly relevant to the Semantic Web community."

## Transparent, provenance-explicit evaluation
**Covers:** provenance, per-run reports, community benefit

"By making the CQ-to-term and CQ-to-axiom provenance explicit, CQ4OE enables a transparent evaluation of LLM-generated ontologies, distinguishing failures that arise from missing vocabulary, unstable property modeling, shallow hierarchy generation, or incomplete coverage of the local CQs."

"The CQ4OE pipeline produces per-run Markdown reports and CSV alignment exports that trace each metric back to specific gold and predicted axioms, making evaluation results traceable at the level of individual CQs and axioms, instead of only aggregate scores."

"By enabling transparent, requirement-driven comparison of ontology generation approaches, CQ4OE can benefit not only ontology engineers but the broader Semantic Web community, as LLM-assisted ontology engineering matures and the need for fair, reproducible evaluation grows."

## Reusability and reproducibility
**Covers:** reuse across domains, models, strategies, and workflows

"CQ4OE is designed for reuse across domains, models, prompting strategies, ontology repair pipelines, and human-in-the-loop workflows."

"The repository organizes CQ2Term and CQ2Onto as two parallel directories, each with gold standards, predictions, evaluation scripts, intermediate results, and aggregated reports."

"To benchmark a new LLM, users add their generated ontologies to the predictions folder and run a single script that extracts atomic axioms, executes the five evaluation steps, and produces the aggregated report."

"To evaluate a single capability, users can apply CQ2Term for term-level recovery or reuse the CQ2Onto layers for ontology-level evaluation independently."

"To extend the benchmark, users simply need to add a new domain following the four-phase annotation methodology of Section 3.2 under the same triple-review, adjudication-based protocol."

"Each metric has a persistent W3ID identifier and a Turtle definition in the metric catalogue, supporting integration into other evaluation pipelines."

"A public leaderboard7 with submission guidelines is maintained in the project repository to facilitate comparison of new methods." Footnote 7: "https://w3id.org/cq4oe/leaderboard"

## Limitations
**Covers:** alignment dependence, closure scope, contamination

"The most consequential is that all ontology-level metrics depend on term alignment, so errors at this layer propagate into downstream scores."

"Our combined hard, lexical, and semantic procedure with one-to-one selection handles lexical variation and reduces many-to-many score inflation, but it can still fail on short property labels or on semantically close yet non-equivalent terms."

"The thresholds τC and τP in Section 4.1 were selected through empirical inspection, informed by previous studies [14,46], and are applied uniformly across all six heterogeneous ontologies without per-domain tuning."

"The pipeline first performs a dry run that exports the complete alignment traces before any scoring."

"After applying the thresholds, manual inspection in all six domains confirmed that most automatic alignments agreed with expert judgment, although borderline cases remain."

"The thresholds are configurable, and users can inspect and, where necessary, manually correct alignments in the intermediate CSV files before re-running the evaluation."

"A second limitation is methodological. The closure rescue mechanism evaluates only those hierarchy-related axioms that can be decomposed into atomic SubClassOf or SubPropertyOf relations, including EquivalentClasses with IntersectionOf or UnionOf."

"Consequently, complex expressions whose semantics cannot be represented by such atomic relations are excluded from quantitative evaluation, since assigning partial credit to individual sub-expressions within a complex axiom remains an open problem."

"A third concern is data contamination, since the source ontologies and some of their published CQs are public and may appear in pre-training data."

Qualifying observations: "First, mean structural F1 remains low at 26.7% to 33.7% across models, suggesting that prior exposure to ontology vocabulary alone does not translate into structurally correct ontology generation." "Second, the CQ-to-term and CQ-to-axiom provenance is manually curated through the triple-review protocol of Section 3.2, introducing an additional manually curated annotation layer that is unlikely to have appeared in pre-training data." "Third, the methodology is portable. Private or post-cutoff ontologies can be added through the documented annotation protocol, future versions of the benchmark plan will include several such ontologies to support evaluations with contamination control."

## Conclusion
**Covers:** Section 7 Conclusion — benchmark, experiments, findings, future work

"We presented CQ4OE, a benchmark for evaluating LLM-based ontology generation from competency questions."

"CQ4OE links each CQ to the terms and TBox axioms required to answer it through two complementary evaluation tasks, CQ2Term and CQ2Onto."

"The CQ4OE pipeline automatically generates Markdown reports and CSV alignment exports that trace every metric back to specific gold and predicted axioms, enabling a detailed diagnosis of why a generated ontology does not satisfy individual CQs."

"Experiments with nine LLMs across six ontologies show that models recover explicit vocabulary more reliably than ontology structure, with performance varying more across domains than across models or generation strategies."

"Reasoning-based closure provides only limited recovery when the underlying hierarchy is missing."

"These findings highlight the need for provenance-aware, multi-dimensional evaluation of LLM-generated ontologies."

"We believe CQ4OE will provide a common evaluation basis for future research on LLM-assisted ontology engineering."

"Future work will extend CQ4OE with additional domains, further refine alignment and evaluation metrics, and incorporate private or post-cutoff ontologies to support contamination-controlled evaluations."

Resource availability: "CQ4OE is openly available under Apache 2.0 at https://github.com/oeg-upm/cq4oe-benchmark, archived on Zenodo (https://doi.org/10.5281/zenodo.20080309) and HuggingFace (https://doi.org/10.57967/hf/8712)." "Persistent metric identifiers are defined at https://w3id.org/cq4oe/metrics."

**Covers:** Fig. 3 (CQ2Onto structural metrics, CQ-level axiom coverage, and hierarchy-closure recovery gains) plus associated bottleneck, provenance, reusability, limitations, conclusion, and resource-availability text in chunk 06-b-cq-conditioned-coverage-and-gain-fig.
