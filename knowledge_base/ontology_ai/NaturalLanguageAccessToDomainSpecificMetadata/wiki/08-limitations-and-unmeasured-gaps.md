> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Limitations and Unmeasured Gaps
**In one sentence:** The SPARQL-over-SQL advantage comes from OWL representation scaffolding lost in mechanical OWL-to-DDL translation, but the size of that gap is explicitly unmeasured, and the single-domain, 21-question, Qwen3-only evaluation with auto-generated SQL baselines limits generalization.
## Key points
- The representation comparison holds data, naming, annotations, questions, and models constant, isolating the effect of representation: OWL carries domain/range declarations, inverse properties, and class-level grouping as first-class structure that mechanical translation to DDL partly loses.
- The reported SPARQL advantage is specific to SQL schemas auto-generated from the ontology, not schemas designed by a database expert, and the gap magnitude is explicitly unmeasured.
- Qwen3 35B MoE variants peaked at 57% while 27B dense models reached 100% despite fewer total parameters, indicating dense models are the better choice at a given compute budget for structured generation requiring precise schema adherence.
- The simplest baseline prompt with the fewest instructions achieved the highest peak accuracy, with more elaborate guardrail and procedural prompts performing comparably but not better.
- Q8 GGUF quantization preserved accuracy completely at 100% matching full precision, while FP8 quantization showed a small drop to 95%.
- The evaluation is limited to one MRI metadata domain, 21 expert-developed competency questions co-evolved with the ontology and prompt rider, Qwen3-family models only, Jena Fuseki in Docker for metadata volume, and LLM context-window bounds on ontology complexity.
---
## Representation gap and unmeasured difference
The chunk opens on the SQL-vs-SPARQL gap: what the comparison isolates is the effect of representation with data, naming, annotations, questions, and models held constant. The OWL ontology carries domain and range declarations, inverse properties, and class-level grouping as first-class structure, and a mechanical translation to DDL loses part of that scaffolding. Verbatim qualification:
> "gap, and we have not measured by how much."
> "The SQL baselines are auto-generated from the ontology, not designed by a database expert; the SPARQL advantage we report is specific to that setting."

**Covers:** chunk opening fragment on representation gap (pre-Section 6.3)

## Lessons learned
Two findings were counterintuitive:
- Qwen3 MoE variants underperformed Qwen3 dense variants: the 35B MoE variants peaked at 57%, well below the 27B dense models at 100%, despite having more total parameters. The chunk concludes that for structured generation tasks requiring precise schema adherence, dense models appear to be the better choice at a given compute budget.
- The simplest prompt won: the baseline prompt, with the fewest instructions, achieved the highest peak accuracy; more elaborate prompts (guardrails, procedural) performed comparably but not better, suggesting that with a well-designed ontology, the LLM needs minimal additional guidance.

Additional findings stated in the chunk:
- Full ontology in context consistently produced the best results across all models and configurations.
- Readable naming had the largest measurable effect on accuracy.
- Quantization: Q8 GGUF preserved accuracy completely (100%, matching full precision); FP8 showed a small drop (95%).
- Automatic OWL-to-SQL conversion derived a working relational schema directly from the ontology with no manual tuning.
- The combinatorial test driver (Section 4.1) is essential infrastructure, not only research tooling: it drives ontology evolution, with the ontology, prompt rider, and competency questions co-evolving so each iteration of any of the three artifacts is validated by re-running the full suite, making regressions immediately visible. Without this tight feedback loop, the co-design process in Section 3.3 would be more difficult. Ontology evolution slows over time but does not halt as vocabulary and semantics are better resolved.

**Covers:** Section 6.3 Lessons Learned

## Limitations
- Single metadata domain: ontology design principles are described as domain-agnostic, but generalization to other domains needs validation.
- Small test set: 21 competency questions developed with domain experts, with expansion ongoing.
- Co-evolution bias: because the competency questions co-evolved with the ontology and prompt rider, accuracy on novel end-user queries may differ from test-set performance.
- Ontology complexity is bounded by the available LLM context window, with some promise shown for token-dense encodings.
- Metadata volume is bounded by SPARQL server capabilities: Jena Fuseki is used in a Docker container, though a heavy-duty commercial solution could be used for larger archives without changing the architecture.
- Model family narrowness: all models are from the Qwen3 family so results may differ with other families; no comparison against cloud-hosted models (GPT-4, Claude) due to institutional data privacy constraints.
- SQL baseline construction: baselines are auto-generated from the ontology rather than expert-designed, so the SPARQL advantage is specific to that setting.

**Covers:** Section 6.4 Limitations

## Future work
- Cross-domain validation: applying the development process and framework to additional domains, with openness to collaboration.
- Expanded MRI archive use: the MRO ontology builds on DICOM and BIDS standards shared across MRI research sites, so with site-specific ETL adaptation the same ontology and framework could serve other neuroimaging archives.
- Expanded test cases: growing the competency question set, including more complex query patterns.
- Multi-turn refinement: supporting follow-up questions where the LLM refines a previous query based on user feedback, making the web application more conversational.
- LLM model diversity: evaluating non-Qwen model families and cloud-hosted models where domain privacy constraints permit.

**Covers:** Section 6.5 Future Work

## Conclusion claims restated in this chunk
- A reusable framework and development process for natural language access to domain-specific metadata; the key insight is that capturing domain vocabulary and semantics in a well-designed OWL ontology enables LLM-driven query generation against both SPARQL and SQL backends with no fine-tuning, no retrieval augmentation, and no multi-agent orchestration.
- The ontology is the single source of truth: it defines the domain vocabulary, informs the ETL pipeline, and provides the LLM with schema context for SPARQL queries; for the SPARQL-vs-SQL exploration the authors automatically generate a relational schema, transform and load the KG into PostgreSQL, and evaluate the competency questions via SQL.
- Benchmark result on the MRI neuroimaging metadata benchmark: NL text-to-SPARQL achieves 100% accuracy on the competency/regression question set while the analogous NL text-to-SQL achieves 57%; an ablation across eight ontology representations confirms ontology design, particularly readable naming and semantic annotations, is the dominant accuracy factor.
- Reusability and deployment: the framework avoids domain-specific components; the iterative process (ontology, competency questions, prompt rider evolving together) requires domain expertise but no machine learning, database, or programming skills; the process was demonstrated and the framework deployed at a major neuroscience institute enabling end-user natural language search of MRI metadata on a growing image archive, with intent to open source the domain and framework.
- GenAI Usage Disclosure: generative AI tools assisted with manuscript editing and LATEX formatting, and with coding, particularly the web server where little expertise was available.

**Covers:** Section 7 Conclusion + GenAI Usage Disclosure
