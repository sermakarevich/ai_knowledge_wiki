> [[index|Wiki]] | [[summary|Summary]]
# CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions — Digest

## 1. [[wiki/01-cq4oe-overview-and-motivation|CQ4OE: Overview and Motivation]]
**In one sentence:** CQ4OE is a benchmark for systematic, reproducible evaluation of LLM-based OWL ontology generation from competency questions (CQs), providing CQ-aligned gold standards with explicit CQ-to-term/axiom provenance, two complementary tasks (CQ2Term over 99 CQs, CQ2Onto over 118 CQs), a multi-task metric framework plus an automated explainable reporting pipeline, and baseline results from nine LLMs showing terms are recovered more reliably than full ontologies.
- Ontology generation from CQs is a central yet labor-intensive phase of Ontology Engineering, where conceptualization transforms natural-language CQs into classes, properties, relations, and constraints.
- Current LLM evaluation is fragmented: heterogeneous task formulations (concept extraction, completion, full OWL generation) with incompatible inputs/outputs make direct comparison challenging.
- Reference ontologies are often not finely aligned with their CQs, rarely specifying which classes, properties, or axioms each CQ requires, so requirement satisfaction cannot be judged.
- Existing metrics based on lexical or coarse structural overlap miss property modeling, logical constraints, and reasoning behavior such as wrong domain/range assignments, missing axioms, or flawed hierarchies.
- CQ4OE builds, per ontology, a CQ-driven gold OWL ontology with explicit provenance linking each CQ to the classes, properties, and axioms required to answer it.
- Two tasks are defined: CQ2Term (term-level class/property prediction over 99 CQs) and CQ2Onto (ontology-level evaluation over 118 CQs covering hierarchy, property modeling, and axiom-level structure).
- Baselines run nine LLMs under zero-shot, iterative, and multi-agent strategies, finding LLMs recover explicit vocabulary terms more reliably than complete ontologies, especially for properties, hierarchies, and axioms.

## 2. [[wiki/02-dataset-construction-and-statistics|Dataset construction and statistics]]
**In one sentence:** From 255 published CQs across six source ontologies, a four-phase CQ-aligned workflow retains 110 CQs, adds 8 new CQs (118 total), and builds CQ2Term (99 CQs) and CQ2Onto (118 CQs) gold standards under triple-review adjudication.
- Six source ontologies (Wine, AWO, ODRL, SAREF4WATR, VGO, SWO) contribute 255 published CQs, of which 110 are retained after filtering out CQs requiring external knowledge, unanswerable from the source, or instance-level rather than TBox-level.
- Only 8 new CQs (3.1% of the original 255) are manually authored to cover uncovered core terms, yielding 118 CQs in total.
- CQ2Term keeps only CQs with at least one explicit class or property term (Ei ≠ ∅), excluding 19 inference-heavy CQs from SAREF4WATR, VGO, and SWO, leaving 99 CQs.
- CQ2Onto covers all 118 CQs, linking each CQ to a sufficient TBox axiom set where an axiom is retained only if its removal would make the CQ unanswerable.
- Core terms (Tcore) are selected by ranking named classes/properties by in- and out-degree plus manual verification with owl2diagram and official published requirements.
- Each CQ is annotated with explicit (Ei, surface matches), implicit (Ii, synonyms/equivalents), and derived (Ri, unmentioned but required) term sets, e.g. AWO "Which plants eat animals?" gives Plant, Animal, eats (explicit) plus CarnivorousPlant (derived) with axioms CarnivorousPlant ⊑ Plant and CarnivorousPlant ⊑ ∃eats.Animal.
- Triple-review adjudication finalizes every item only on full agreement of one annotator plus two expert reviewers; 101 of 118 CQs (85.6%) accepted without change, with 17 revisions concentrated in SWO (10), VGO (3), ODRL (2), SAREF4WATR (2).

## 3. [[wiki/03-term-alignment-and-evaluation-metrics|Term Alignment and Evaluation Metrics]]
**In one sentence:** Generated ontologies can use different labels for the same class or property, so CQ4OE aligns gold and predicted terms with an aggregated five-method similarity pipeline and then computes CQ2Term term-level and CQ2Onto ontology-level (term, characteristic, triple, axiom, hierarchy-closure) metrics over that alignment.
- Label variation (e.g., `hasPart` vs. `containsComponent`) motivates aligning gold and predicted terms before computing CQ2Term and CQ2Onto metrics.
- Seven candidate similarity methods were reduced to five: WordNet synonym matching was excluded for poor domain-term coverage and information-content similarity because it requires a shared taxonomy.
- The final pipeline uses hard exact-string matching, difflib SequenceMatcher sequence matching, Levenshtein and Jaro–Winkler via textdistance, and embeddinggemma-via-Ollama semantic similarity.
- Standalone per-method P/R/F1 use thresholds 1.0 for hard matching, 0.8 for lexical similarities, and 0.6 for semantic similarity; the methods have complementary failure modes (lexical misses paraphrases, semantic gives false positives on short labels).
- Aggregated pair score uses a hard-match override plus the mean of the three highest non-hard method scores, so no single low-scoring method can veto a reasonable match.
- One-to-one alignment applies type-specific thresholds (τC = 0.6 for classes, τP = 0.7 for properties, chosen from {0.5, 0.6, 0.7} on a held-out subset), ranks passing pairs by decreasing score with hard matches prioritized, and selects greedily; the higher property threshold counters spurious matches on short formulaic labels (e.g., `has_`/`is_` prefixes concentrating at 0.6–0.65).
- CQ2Term reports global P/R/F1 over combined term sets (TP = |α|, FP = |Tp| − |α|, FN = |Tg| − |α|) plus CQ-conditioned at-least-one, mean, and full coverage, capturing models that recover vocabulary without attaching terms to the right CQ.
- CQ2Onto evaluates five targets (term recovery, property characteristics, domain/range triples, TBox axioms, HermiT hierarchy closure) with global and alignment-conditioned views, strict equivalence counting, an embedding-cosine diagnostic, and axiom-level plus closure-recovered CQ coverage over required TBox axiom sets Ai.

## 4. [[wiki/04-experimental-setup-and-baselines|Experimental Setup and Baselines]]
**In one sentence:** Nine LLMs are evaluated on 99 CQs (CQ2Term) and 118 CQs (CQ2Onto) across six ontologies under zero-shot, iterative, and multi-agent repair strategies, yielding 54 runs and 162 ontologies that show strong vocabulary recovery but steep drops to structure, hierarchy closure, and CQ-level completeness.
- CQ2Term covers 99 CQs and CQ2Onto covers 118 CQs across six ontologies, producing 54 runs and 162 ontologies as reference baselines with results and reports in the project repository.
- Nine baselines are tested: DeepSeek V4-Pro, V4-Flash, V3.2; Qwen Plus, Flash, 35B-A3B, 27B; and Gemma 31B-IT, 26B-A4B-IT via OpenRouter at temperature 0 with a 16,384-token output limit, all reusing the MASEO Generation Agent prompting set.
- Three CQ2Onto strategies are compared: zero-shot (full CQ set in one pass), iterative (CQs fed sequentially), and multi-agent (initial ontology refined with RDFLib, HermiT, and OOPS! for up to three iterations with backtracking).
- CQ2Term global F1 spans 59.1% (DeepSeek V3.2) to 66.5% (DeepSeek V4-Pro), class recovery (67.1%) beats property recovery (55.2%), and precision–recall gaps (overall 56.1% vs 71.5%; properties 47.9% vs 69.3%) indicate over-generation.
- CQ-conditioned coverage averages 89.2% at-least-one, 54.8% mean, and only 23.5% full, with Water at 70.6% global F1 but 0% full coverage and Wine at 100% at-least-one but 0% full, so global vocabulary scores hide requirement-localization errors.
- CQ2Onto drops steeply from vocabulary to structure (class F1 averaging 59.7% vs property F1 31.8%; Triple-AC 36.4% vs Triple-G 12.4%; Axiom-AC 35.3% vs Axiom-G 15.0%; closure F1 averaging only 16.7%), and no single model dominates every dimension.
- Strategies differ within 3 percentage points on structural F1 but shape hierarchies differently: iterative is densest (8.6 closure pairs vs 4.9 zero-shot and 4.7 multi-agent) while multi-agent raises CQ-level axiom coverage (Axioms-Mean 18.3% to 24.2%, concentrated in AWO 26.0% to 37.6% and ODRL 23.3% to 32.3%).
- Three recurrent limitations emerge: missing SubClassOf/SubPropertyOf chains, unstable property modeling at nearly half of class F1, and low CQ completeness with Axioms-Full near 2% (2.1%) and Closure-Full unchanged by rescue.

## 5. [[wiki/05-cq2term-results-by-model-and-domain|CQ2Term results by model and domain]]
**In one sentence:** Fig. 2 reports CQ2Term term-F1 per model–domain pair and CQ-conditioned coverage averaged over nine LLMs, framing CQ2Term as a test of conceptualization (explicit classes/properties in CQs) distinct from CQ2Onto's deeper requirement reasoning.
- Fig. 2 covers six benchmark domains: Wine, AWO, ODRL, Water, VGO, and SWO.
- Fig. 2(a) reports overall term F1 for each model and domain pair, computed by pooling class and property matches before calculating precision, recall, and F1.
- Fig. 2(b) reports CQ-conditioned coverage averaged over nine LLMs, with at-least-one, mean, and full coverage per domain; visible values include 22.0, 20, 8.5, 0.0, 0.6, 0.0.
- The chunk claims CQ-to-axiom provenance at this level is unique: "To our knowledge, no existing benchmark for ontology generation provides this level of CQ-to-axiom provenance."
- CQ2Term targets conceptualization: whether an LLM can recognize and organize the explicit classes and properties in CQs, described as the most immediate semantic content of the requirements and the foundation of downstream ontology since vocabulary selection determines later modeling decisions.
- Isolating conceptualization is said to reduce manual effort enumerating candidate terms and to give a transparent basis for selecting the best-suited model per domain rather than relying on a single aggregate ranking.
- CQ2Onto is introduced as complementary: it evaluates understanding and reasoning over CQ requirements beyond surface vocabulary (sentence truncated in chunk at "whether the model can").

## 6. [[wiki/06-cq2onto-results-and-closure-gains|CQ2Onto Results and Closure Gains]]
**In one sentence:** Fig. 3 summarizes CQ2Onto results averaged over nine LLMs across six domains as structural F1 and CQ-conditioned coverage before/after closure rescue, and the surrounding text argues that answering CQs requires recovering implicit and derived terms as coherent OWL structure with provenance-traceable, reusable evaluation, subject to alignment-dependence, restricted closure scope, and contamination caveats.
- Fig. 3 reports CQ2Onto results across six benchmark domains with each (domain, strategy) cell averaged over nine LLMs in both panels.
- Panel (a) shows structural F1 across seven evaluation metrics, with AWO Triple cells shown as N/A because the gold range is a complex anonymous OWL expression.
- Panel (b) shows CQ-conditioned coverage before and after closure rescue, where ∆ is the gain in Mean coverage from closure rescue (Closure-Mean − Axioms-Mean).
- Answering a CQ requires moving beyond its explicit terms to recover implicit and derived terms, expressed as property characteristics, property triples, TBox axioms, and hierarchical structure under reasoner-derived closure.
- The CQ4OE pipeline produces per-run Markdown reports and CSV alignment exports tracing each metric back to specific gold and predicted axioms, distinguishing missing vocabulary, unstable property modeling, shallow hierarchy generation, and incomplete local-CQ coverage.
- Reuse is organized as parallel CQ2Term and CQ2Onto directories with gold standards, predictions, scripts, and aggregated reports; new LLMs are added via the predictions folder plus one script, and new domains via the four-phase annotation methodology of Section 3.2 under triple-review adjudication, with persistent W3ID metric identifiers and a public leaderboard.
- All ontology-level metrics depend on term alignment via combined hard, lexical, and semantic one-to-one selection with uniform thresholds τC and τP; closure rescue evaluates only hierarchy-related axioms decomposable into atomic SubClassOf or SubPropertyOf relations including EquivalentClasses with IntersectionOf or UnionOf; mean structural F1 remains low at 26.7% to 33.7% across models; and closure provides only limited recovery when the underlying hierarchy is missing, with performance varying more across domains than across models or generation strategies.

## 7. [[wiki/07-discussion-limitations-and-references|Discussion, limitations and references (refs 9–53)]]
**In one sentence:** This chunk is the bibliography tail of the CQ4OE paper (references 9–53, pp. 19–20), listing the LLM reports, ontology-engineering methods, datasets, and similarity/evaluation sources cited — not the DeepSeek-V3 technical content itself.
- The chunk contains only numbered bibliography entries 9 through 53, spanning pages marked "CQ4OE 19" and "20 J. Li et al.".
- Reference 9 cites "DeepSeek-AI: DeepSeek-V3 technical report (2024)" at `https://arxiv.org/abs/2412.19437`, and reference 10 cites a "DeepSeek-V4 Technical Report" preview release (April 2026) via HuggingFace.
- Cited LLM reports also include Gemma 4 (Google DeepMind, 2026) and Qwen3.6 (Alibaba Group, 2026).
- Cited ontology-engineering works include NeOn-GPT (2026), MASEO multi-agent system (ESWC 2026), DRAGON-AI (2024), LOT framework (2022), SAMOD (2016), OOPS! pitfall scanner (2014), and CORAL requirements corpus (ESWC 2019).
- Cited benchmarks and evaluation sources include LLMs4OL 2024 (silp_nlp), ISWC 2024 GenAI/Semantic Web sessions (Garijo et al., Plu et al., Rebboud et al.), ELMKE 2025, BIOASQ, OAEI, HELM (2023), and HermiT OWL 2 reasoner (2014).
- Cited similarity/clustering foundations are Levenshtein (1966), Lin (ICML 1998), Resnik (1995), and Sedding & Kazakov (ROMAND 2004).
- Domain ontologies and standards cited include SAREF4WATR water domain (ETSI TS 103 410-9 V1.1.2, 2020), ODRL 2.2 (W3C 2018), Wine ontology (W3C 2004), Software Ontology SWO (2014), African Wildlife Ontology tutorial (2020), videogame interoperability ontology (2017), SAR ontology (2024), and forest-fire emergency modelling (2022).

## The argument in five moves
1. CQ-driven ontology generation is central but unevaluated: existing LLM evaluations use incompatible tasks, CQ-unaligned gold standards, and shallow metrics that miss properties, axioms, and reasoning behavior.
2. CQ4OE builds CQ-aligned gold standards from six ontologies (255 published CQs → 110 retained + 8 new = 118) with explicit/implicit/derived term annotation and CQ-to-axiom provenance under triple-review adjudication, split into CQ2Term (99 CQs) and CQ2Onto (118 CQs).
3. To score fairly under label variation, a five-method alignment pipeline (hard, sequence, Levenshtein, Jaro–Winkler, embedding semantic; τC = 0.6, τP = 0.7) grounds a multi-target metric framework spanning terms, characteristics, triples, TBox axioms, HermiT hierarchy closure, and CQ-conditioned coverage with explainable per-run reports.
4. Nine-LLM baselines show vocabulary is recoverable (CQ2Term F1 ~59–67%, classes beat properties, heavy over-generation) but CQ-localized completeness is low (mean ~55%, full ~24%), and structure collapses further (property/triple/axiom/closure F1 far below class F1; Axioms-Full ~2%).
5. Strategy and domain comparisons plus closure rescue confirm the pattern: domains matter more than models, iterative builds denser hierarchies while multi-agent repair lifts axiom coverage, and reasoning recovers little when SubClassOf/SubPropertyOf chains were never generated.
6. CQ4OE therefore offers a reusable, provenance-traceable evaluation basis (parallel task directories, W3ID metrics, leaderboard) whose limits — alignment dependence, hierarchy-only closure scope, contamination risk — point to extending domains, refining alignment, and adding private/post-cutoff ontologies.
