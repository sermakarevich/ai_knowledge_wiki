---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Graph Retrieval-Augmented Generation: A Survey — Retrieval Practice

Answer from memory before expanding each callout.

## 1. What three concrete limitations of traditional (text-based) RAG does the paper identify, and how does GraphRAG address each one?

> [!tip]- Answer
> (1) **Neglecting Relationships** — RAG finds semantically similar documents but misses structured relationships between them (e.g., citation links between retrieved papers); GraphRAG retrieves explicit graph elements (triples/paths) that carry those relationships. (2) **Redundant Information** — concatenating many text snippets creates overly long prompts and triggers the "lost in the middle" problem; graph data is more compact/abstracted, shortening input length. (3) **Lacking Global Information** — RAG retrieves only a document subset and struggles with Query-Focused Summarization (QFS); GraphRAG can retrieve subgraphs or graph communities that give broader, global context.

## 2. Write out the formal GraphRAG objective (Eq. 3–4) and explain why the sum over all candidate subgraphs is approximated by keeping only the single "optimal" subgraph G*.

> [!tip]- Answer
> Eq. 3: a* = argmax_{a∈A} p(a | q, G) — the best answer a given query q and graph G. This is decomposed (Eq. 4) as p(a|q,G) = Σ_{G⊆G} p_φ(a|q,G)·p_θ(G|q,G), jointly modeled by a graph retriever p_θ and an answer generator p_φ. The sum is approximated as p_φ(a|q,G*)·p_θ(G*|q,G), keeping only the optimal subgraph G*, because the number of candidate subgraphs of a large graph grows exponentially — summing over all of them is computationally intractable, so retrieval must pick one (near-)optimal subgraph instead.

## 3. Name the four indexing schemes covered in Graph-Based Indexing and give one method/system example for each.

> [!tip]- Answer
> **Graph indexing** — preserves full structure for BFS/shortest-path search (used broadly, e.g. [73, 75, 112]). **Text indexing** — converts the graph into text via triple templates (Li et al., Huang et al.) or LLM-generated community summaries (Edge et al., i.e. Microsoft's GraphRAG). **Vector indexing** — embeds graph elements for fast similarity search, e.g. G-Retriever encodes node/edge text, GRAG embeds k-hop ego networks. **Hybrid indexing** — combines schemes, e.g. HybridRAG retrieves vector and graph data together, EWEK-QA pairs text with the KG.

## 4. What are the two core challenges that make graph-guided retrieval hard, and how do the three retriever types (non-parametric, LM-based, GNN-based) trade off against each other in addressing them?

> [!tip]- Answer
> The two challenges are **Explosive Candidate Subgraphs** (candidate subgraphs grow exponentially with graph size) and **Insufficient Similarity Measurement** (measuring similarity between a text query and structured graph data requires understanding both modalities). Non-parametric retrievers (heuristic rules, classic graph search like PCST in G-Retriever) are efficient but can be inaccurate since they aren't trained on the downstream task. LM-based and GNN-based retrievers achieve higher accuracy by learning task-relevant similarity but are computationally heavier. Many systems combine both in hybrid, multi-stage pipelines (e.g., RoG uses an LLM to plan paths, then extracts them from the KG; GenTKGQA uses an LLM to infer relations/constraints before triplet extraction).

## 5. Distinguish the four retrieval granularities (nodes, triplets, paths, subgraphs) and state the main tradeoff each one faces.

> [!tip]- Answer
> **Nodes** — precise, targeted retrieval of individual entities/passages, good for focused queries but no relational context. **Triplets** (subject-predicate-object) — structured and clear for direct relations, but lack depth for indirect/multi-hop reasoning. **Paths** — sequences of relations that support multi-hop reasoning, but the number of possible paths grows exponentially with graph size, raising computation cost. **Subgraphs** — capture the fullest relational context (patterns, dependencies) but are the most expensive to retrieve and process. Hybrid approaches (often LLM agents) adaptively mix granularities to balance completeness against efficiency.

## 6. What is the difference between "query enhancement" and "knowledge enhancement" in the retrieval-enhancement stage, and give one technique for each sub-type (expansion, decomposition, merging, pruning).

> [!tip]- Answer
> **Query enhancement** happens before/during retrieval to improve the query itself: **expansion** enriches a short query with related terms (e.g., Cheng et al. use SPARQL to pull entity aliases from Wikidata); **decomposition** splits a complex query into sub-queries each targeting one relation, retrieved sequentially. **Knowledge enhancement** happens after retrieval to refine the result set: **merging** compresses/aggregates retrieved elements (e.g., KnowledgeNavigator merges nodes via triple aggregation); **pruning** removes irrelevant/redundant results via re-ranking (cross-encoders, Personalized PageRank), new relevance metrics, or LLM-based relevance checks.

## 7. Explain the two ways graph data gets converted for an LM-based generator ("graph languages" vs "graph embeddings"), and what three qualities a good graph language must have.

> [!tip]- Answer
> Because graphs are non-Euclidean and LMs read only text/sequences, retrieved graph data must be translated. **Graph languages** serialize the graph into text-like forms: adjacency/edge tables, natural-language descriptions, code-like forms (GML/GraphML), syntax trees, or node sequences. **Graph embeddings** instead encode the graph numerically (often via a GNN) and feed the embedding into the LM (e.g., via prompt tuning or Fusion-in-Decoder), avoiding long text but risking loss of precise details like exact entity names and generalizing poorly, and mainly works with open-source LMs. A good graph language should be **complete** (captures essential structure), **concise** (avoids "lost in the middle" and length limits), and **comprehensible** (LM can accurately interpret it).

## 8. What is the difference between the "cascaded" and "parallel" hybrid generator paradigms that combine GNNs and LMs?

> [!tip]- Answer
> **Cascaded**: sequential — the GNN first encodes the graph data into a representation, which is then prepended as a prefix to the LM's input embeddings (prompt tuning), and the LM generates the final response. **Parallel**: concurrent — the GNN and LM both process the input at the same time (on different facets of the data), and their outputs/representations are merged afterward via weighted summation, attention, concatenation, or dedicated fusion modules (e.g., GreaseLM Layer, ENGINE's G-Ladders).

## 9. Contrast "training-free" and "training-based" approaches for GraphRAG retrievers, and explain the "distant supervision" trick used to get training labels when explicit retrieval ground truth doesn't exist.

> [!tip]- Answer
> **Training-free** retrievers use pre-defined rules/classic graph search, or leverage pre-trained embedding models or generative LLMs to select relevant graph elements via prompting — no explicit fine-tuning, common with closed-source LLMs like GPT-4. **Training-based** retrievers are fine-tuned with supervised signals (e.g., maximizing query–ground-truth similarity, or autoregressively predicting the next relation in a path) to better fit the downstream task. Since most datasets lack labeled "correct" retrieval targets, **distant supervision** substitutes: methods extract all (or the shortest) paths connecting the query entities to the known answer entities in the graph and use those paths as pseudo-ground-truth training data (e.g., used by Zhang et al., Feng et al., Luo et al.).

## 10. List the downstream task categories GraphRAG is evaluated on and name at least one GraphRAG-specific benchmark (not a task-specific dataset) along with what it tests.

> [!tip]- Answer
> Downstream task categories: Question Answering (KBQA and CommonSense QA/CSQA), Information Extraction (Entity Linking, Relation Extraction), Fact Verification, Link Prediction, Dialogue Systems, and Recommendation. GraphRAG-specific benchmarks (not tied to one task): **STARK** (LLM retrieval over semi-structured knowledge bases across product search, academic paper search, and precision medicine), **GraphQA** (flexible QA benchmark over real-world textual graphs), **GRBENCH** (1,740 questions over 10 domain graphs), and **CRAG** (structured queries with mock APIs over mock KGs for fair comparison).

## 11. What are three of the seven future-research directions the survey identifies, and why is each currently a limitation of GraphRAG?

> [!tip]- Answer
> Example three (of seven — dynamic/adaptive graphs, multi-modality, scalable retrieval, graph foundation models, lossless compression, standard benchmarks, broader applications): (1) **Dynamic and adaptive graphs** — most methods use static graph databases, but real-world entities/relationships change continuously, so systems need efficient real-time update mechanisms. (2) **Scalable and efficient retrieval** — industrial knowledge graphs can hold millions/billions of entities while most current methods are only tested on graphs of a few thousand entities, so retrieval algorithms and infrastructure need to scale up. (3) **Standard benchmarks** — GraphRAG is a new field lacking unified benchmarks with diverse datasets and well-defined metrics, making it hard to objectively compare methods.

## 12. How does GraphRAG differ from (a) "LLMs on Graphs" research and (b) IR-based KBQA, according to the survey's positioning in Section 2?

> [!tip]- Answer
> (a) "LLMs on Graphs" research (e.g., ENGINE) integrates LLMs with GNNs to improve performance on graph-native tasks like node classification, edge prediction, and graph classification — it is about modeling graphs better, not about answering external queries. GraphRAG instead focuses on retrieving relevant graph elements from an external graph-structured database in response to a query. (b) IR-based KBQA methods (which retrieve information from a knowledge graph to enhance generation) are considered a **subset** of GraphRAG approaches focused specifically on the KBQA downstream task, whereas GraphRAG as a field covers a much broader range of downstream applications beyond KBQA.
