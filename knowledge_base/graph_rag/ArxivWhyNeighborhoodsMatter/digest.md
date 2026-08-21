> [[index|Wiki]] | [[summary|Summary]]

# Why Neighborhoods Matter — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-motivation|Introduction and Motivation]]

**In one sentence:** In Agentic GraphRAG, final citations only capture part of the information the agent relies on, so citation faithfulness should be treated as a trajectory-level problem where traversal, graph structure, and visited-but-uncited entities jointly shape the answer.

- Hallucination is a fundamental factuality problem in LLMs because models are rewarded for providing an answer rather than admitting uncertainty, and RAG mitigates it by grounding answers in external sources.
- Graph RAG retrieves directly from knowledge graphs, following typed entity-relation-entity triples via explicit paths, making retrieved evidence more structured and auditable than vector-similarity retrieval.
- Agentic GraphRAG adds autonomy: rather than a single retrieval step, the agent iteratively decides what to query, inspects results, and traverses the graph until it can produce a final answer with cited evidence.
- Prior faithfulness work asks whether cited sources truly supported the answer or whether reliance on them was genuine, but Agentic GraphRAG raises the additional question of whether the cited entities are even a complete account of what the agent used.
- The paper hypothesizes that final citations capture only part of the information the agent relies on, and that visited entities plus the structural context have a measurable effect on the accuracy and robustness of generated answers.
- The contributions are: framing citation faithfulness as a trajectory-level problem; introducing a graph-ablation methodology to test whether cited evidence is necessary, sufficient, and complete; and showing cited entities are often necessary but not sufficient.

## 2. [[wiki/02-experimental-design-and-studies|Experimental Design and Studies]]

**In one sentence:** To measure how much agentic GraphRAG answers depend on cited evidence versus the surrounding graph structure, the authors build a 30-question multi-hop QA benchmark over a knowledge base, establish baselines with six LLM systems across three agentic GraphRAG citation regimes, and then run three graph ablation studies (isolation of evidence, cited-evidence removal, visited-but-uncited removal) that surgically remove or mask different entity classes to attribute accuracy to each component.

- The experiment uses a 30-question benchmark built from the 2WikiMultiHopQA development set, chosen for multi-hop questions with supporting facts, evidence triples, and distractor paragraphs.
- The 30 questions break into 12 local-path (clear gold evidence chain), 12 distractor-path (plausible wrong routes via overlapping distractor paragraphs), and 6 summary-vs-local comparison questions.
- The knowledge base was built from 275 unique merged gold+distractor paragraphs chunked into 318 text units, enriched with entities and relationships extracted from distractor text, with Leiden communities, resulting in 1,815 entities, 1,692 relationships, and 7 communities.
- Six systems are evaluated (plain LLM, RAG, non-agentic GraphRAG, and three agentic GraphRAG settings), all using Mistral-Small-4-119B-2603.
- The three agentic settings differ only in citation discipline: unconstrained submission, evidence-first (citations submitted and validated before the final answer), and visited-only (citations rejected unless the cited entities were visited).
- In all ablation studies, each question's entities are sorted into three groups — never visited, visited-and-cited, and visited-but-uncited — and a question-specific modified graph is built by removing entities or restricting access to their text units.
- Study 1 (Isolation) asks whether cited evidence is *sufficient*: Full Isolation removes every non-cited entity; Text-only Isolation keeps the full graph but blocks reading text units attached to non-cited entities, so any accuracy recovery shows the value of graph structure.
- Study 2 (Cited Evidence Ablation) asks whether cited evidence is *necessary*, and controls for the fact that any node removal degrades accuracy structurally, by comparing Cited Removal against Random Removal of an equal-sized set of non-cited, plausibly retrievable text units.
- Study 3 (Visited-but-uncited Ablation) tests the role of navigational context by comparing Entity Removal against Entity text mask, where the masked entities' metadata is also hidden to prevent information leakage from the traversal context.

## 3. [[wiki/03-results-and-discussion|Results and Discussion]]

**In one sentence:** Citation faithfulness in agentic GraphRAG is neither binary nor reducible to whether the final citations support the answer — cited entities are important but not sufficient, because visited-but-uncited entities and the broader graph-interaction trace remain behaviorally relevant to answer generation.

- Agentic systems typically visit 10–12 entities while citing only around 2, creating a gap between the graph-interaction trace and the final provenance trace (e.g., Agentic GraphRAG visits 11.9 entities but cites 1.9).
- Removing cited entities substantially drops accuracy across all systems (e.g., Agentic GraphRAG falls from 76.0% to 36.0%, GraphRAG from 60.0% to 28.0%), showing final citations are not merely decorative.
- Random entity ablation does not produce a comparable accuracy drop and in some cases improves performance (e.g., Agentic GraphRAG rises to 84.0%), indicating the cited-ablation effect is not just a consequence of perturbing the graph.
- Restricting systems to only originally cited entities (full isolation) decreases accuracy in all settings (e.g., GraphRAG drops to 48.0%), so final citations alone do not robustly reconstruct the context needed for accurate answering.
- Text-only isolation (preserving graph structure while masking text of non-cited entities) improves accuracy and answer stability relative to full isolation (e.g., GraphRAG at 60.0% vs 48.0%), suggesting uncited entities' presence, position, and connectivity guide traversal and constrain the search space.

## 4. [[wiki/04-conclusion-and-limitations|Conclusion and Limitations]]

**In one sentence:** Final citations in Agentic GraphRAG are necessary but not sufficient to explain a generated answer's evidence basis, so citation faithfulness must be evaluated as a trajectory-level property that includes graph context and the retrieval path, not just the final outputs.

- Final citations in Agentic GraphRAG are not sufficient to explain the evidence basis of generated answers: cited entities play a necessary role, but accurate answering depends on more than the entities ultimately cited.
- Removing cited entities substantially changes answers and reduces accuracy, confirming their necessity, while removing visited-but-uncited entities and altering traversal/neighborhood structure can also influence how the agent discovers, selects, and interprets evidence.
- A correct citation set can still omit parts of the retrieval trajectory that were relevant to producing the answer, so evaluating citations only by checking whether cited sources support the answer or were visited by the agent is insufficient.
- Faithful citation mechanisms should account for the graph context and retrieval path that shape the final response; provenance in agentic graph-based retrieval should be treated as a trajectory-level property rather than only a final-output property.
- The study is limited by its small benchmark size and by using a controlled knowledge graph built from 2WikiMultiHopQA rather than a large real-world knowledge graph.
- Future work should repeat the interventions on larger datasets, richer graph structures, and domain-specific knowledge bases, and develop citation mechanisms that expose not only final supporting entities but also the relevant traversal context.

## The argument in five moves

1. RAG and GraphRAG ground LLM answers in retrieved evidence, and citations make that evidence auditable — but Agentic GraphRAG lets the agent see far more of the graph than it ends up citing.
2. This creates a hidden gap: the agent's real evidential basis (its traversal trajectory) may be much bigger than its final citation set (~10-12 visited entities vs. ~2 cited).
3. To test whether citations alone explain the answer, the authors build a controlled multi-hop QA benchmark and run three graph-ablation studies that remove or mask cited, random, and visited-but-uncited entities.
4. Cited-entity removal tanks accuracy (necessity confirmed), but restricting the system to only cited entities *also* tanks accuracy (sufficiency denied) — and even masking uncited-but-visited entities hurts, implicating graph structure and traversal context.
5. The conclusion generalizes: citation faithfulness in agentic graph retrieval is a property of the whole trajectory, not just the final answer-citation pair — so provenance tooling needs to expose traversal context, not only final sources.
