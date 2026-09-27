> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# SQL by 14, revealing the importance
**In one sentence:** Related work shows LLM query accuracy hinges on semantic annotations and schema representation — not query language alone — with enterprise SQL failing at 0–16%, knowledge-graph/SPARQL variants reaching 54–100%, and ontology representation alone causing a 90-point accuracy spread.
## Key points
- The paper claims four contributions: the NLKGQ framework and ontology-first process for NL access to domain-specific metadata demonstrated on neuroimaging data; evaluation over 8 models, 8 ontology representations, and 768 configurations (over 16,000 runs) showing ontology design dominates accuracy; a generic OWL KG-to-SQL generator enabling SPARQL vs SQL comparison on identical NL questions; and analysis of OWL's structural advantages over SQL DDL for LLM query generation.
- Traditional KGQA (entity linking plus relation prediction) has been extended by LLMs via fine-tuning (SGPT; Zhang et al. GAIL for low-resource KGQA), multi-agent/pipeline orchestration (AGENTiGraph with 95% classification accuracy on a 3,500-query benchmark; CyberBOT with RAG plus ontology-based post-hoc verification), in-context learning with retrieved examples (D'Abramo et al.), query-time graph exploration (GRASP, state-of-the-art on Wikidata zero-shot), and exploratory interfaces (Rhizomer-LLM on BESDUI).
- Rhizomer-LLM's BESDUI evaluation is complementary rather than comparable because it measures task completion, not answer correctness, since, in the authors' words, "semantic correctness cannot be automatically verified", whereas this paper reports execution-level correctness against a reference query for every competency question.
- In text-to-SQL, GPT-4o achieves 0% execution accuracy on real enterprise schemas with hundreds of tables (BEAVER), failures traced to schema retrieval and column mapping; adding column descriptions improves accuracy by over 20% on uninformative columns (Wretblad et al.), and schema presentation directly affects accuracy (Rajkumar et al.).
- Knowledge graphs provide a structural advantage on the same enterprise questions, raising accuracy from 16% (SQL) to 54% (SPARQL) (Sequeda et al.); the authors' controlled ontology is smaller in vocabulary than public KGs like Wikidata or DBpedia but describes large data volumes with compact classes and properties, unlike approaches that cope with unchangeable public ontologies with opaque identifiers.
- For text-to-SPARQL, Giuliani et al.'s heuristic advice (prefer expressive labels over cryptic identifiers) rests on a confounded GPT-3.5 improvement from 0.08 to 0.60 combining renaming, added axioms, and query filtering, whereas this paper's ablation (Table 4) holds model, prompt, and benchmark fixed and isolates a 90-point spread from ontology representation alone, from 100% (default) to 10% (abstract-graph).
- SparqLLM's accuracy depends mostly on its 360 hand-authored query templates rather than zero-shot capability (relaxed-match drops from 66.7% to 55.3% without template retrieval), while this approach needs no per-question templates because the ontology supplied once in the system prompt provides the semantic scaffolding; against Vejvar and Fujimoto's terse-linearization result where SPARQL trails SQL (17.2% vs 29.7% with fine-tuned uT5), the full annotated OWL ontology in context reverses this to 100% SPARQL vs 57% auto-generated SQL.
---
## Contributions claimed
**Covers:** Contributions (1)–(4), Section 2 framing

- (1) The NLKGQ framework and ontology-first development process for enabling NL access to domain-specific metadata, including ontology design principles, a KG builder pattern, and a reusable query server with web interface, demonstrated on neuroimaging research data.
- (2) Systematic evaluation of LLM-driven SPARQL generation across 8 models, 8 ontology representations, and 768 configurations (over 16,000 runs), showing ontology design is a dominant factor in accuracy.
- (3) Generic OWL KG-to-SQL schema generator and data transformer enabling systematic text-to-SPARQL vs text-to-SQL comparison for the same NL questions.
- (4) Analysis of structural advantages OWL provides over SQL Data Definition Language (DDL) for LLM-based query generation.
- Framing claim: domain-specific ontologies are typically smaller in vocabulary than public KGs but may describe large volumes of data with a compact set of classes and properties; the approach assumes the ontology is under the authors' control, unlike work on Wikidata or DBpedia where opaque identifiers give few semantic hints.

## 2.1 Knowledge Graph Question Answering
**Covers:** Section 2.1

- Traditional KGQA systems combine entity linking with relation prediction, mapping NL to structured queries through classification.
- Fine-tuning: SGPT applied a pre-trained generative model combined with knowledge graph embeddings to SPARQL generation; Zhang et al. use GAIL (Generative Adversarial Imitation Learning) to fine-tune LLMs for low-resource KGQA, where the LLM generator's SPARQL is evaluated by a discriminator against expert demonstrations.
- Multi-agent/pipeline: AGENTiGraph deploys intent classification, task planning, and automatic knowledge integration across agents, achieving 95% classification accuracy on a 3,500-query benchmark; CyberBOT combines RAG with an ontology-based verification layer constraining LLM outputs post-hoc.
- In-context learning: D'Abramo et al. show ICL with retrieved SPARQL examples can match fine-tuned models, though it requires example-retrieval infrastructure; GRASP uses the LLM to explore the KG at query time, searching for relevant IRIs and literals, achieving state-of-the-art on Wikidata zero-shot.
- Rhizomer-LLM lowers the barrier via an LLM-assisted exploratory interface over cloud APIs (Gemini, DeepSeek, Llama), evaluated on the BESDUI task-completion benchmark; verbatim caveat: "semantic correctness cannot be automatically verified".
- Synthesis claim: all these approaches build complexity to cope with ontologies they cannot change, typically public KGs like Wikidata or DBpedia with opaque identifiers.

## 2.2 Text-to-SQL and Schema Representation
**Covers:** Section 2.2

- Text-to-SQL progressed on Spider, but depends on schema simplicity: BEAVER shows GPT-4o at 0% execution accuracy on real enterprise schemas with hundreds of tables, failures traced to schema retrieval and column mapping.
- Sequeda et al. show knowledge graphs raise accuracy from 16% (SQL) to 54% (SPARQL) on the same enterprise questions.
- Rajkumar et al. show schema representation — how table and column names are presented — directly affects SQL generation accuracy, paralleling the paper's SPARQL findings.
- Wretblad et al. show adding column descriptions improves text-to-SQL accuracy by over 20% on columns with uninformative names, validating annotation importance.

## 2.3 Text-to-SPARQL
**Covers:** Section 2.3

- Field advanced from sequence-to-sequence models via chain-of-thought prompting and Spider4SPARQL, but most work targets public KGs with opaque identifiers.
- Giuliani et al. propose LLM-friendly heuristics (semantically expressive labels over cryptic identifiers) with one supporting data point of GPT-3.5 improving from 0.08 to 0.60, combining renaming, added axioms, and query filtering in a single step without isolating naming; this paper's Table 4 ablation holds model, prompt, and benchmark fixed with a 90-point spread from 100% (default) to 10% (abstract-graph).
- SparqLLM retrieves from 360 hand-authored query templates via RAG; removing template retrieval drops relaxed-match accuracy from 66.7% to 55.3%, indicating curated templates account for most accuracy; this paper requires no per-question template curation because the ontology alone in the system prompt provides the semantic scaffolding.
- Vejvar and Fujimoto compare SPARQL, SQL, and Cypher on a shared benchmark and find SPARQL trails SQL under terse token-dense linearizations (17.2% vs 29.7% execution accuracy with fine-tuned uT5 models); with the full annotated OWL ontology in context, SPARQL accuracy exceeds auto-generated SQL (100% vs 57%).

**Covers:** Contributions (1)–(4); Related Work Sections 2–2.3 (KGQA, Text-to-SQL and Schema Representation, Text-to-SPARQL)
