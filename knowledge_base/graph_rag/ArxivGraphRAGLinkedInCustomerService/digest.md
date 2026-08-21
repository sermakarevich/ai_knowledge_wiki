> [[index|Wiki]] | [[summary|Summary]]

# Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-related-work|Introduction and Related Work]]

**In one sentence:** Plain-text chunk-based RAG loses both the structure linking customer-service issue tickets and the logical coherence across ticket segments, degrading retrieval and answer quality, so the paper fuses RAG with a knowledge graph that preserves intra-issue structure and inter-issue relations.

- Conventional RAG for customer-service support treats a corpus of past issue-tracking tickets as plain text, segmenting tickets into fixed-length chunks to fit embedding-model context limits and then embedding each chunk for retrieval — explicitly ignoring the intra-issue structure and the inter-issue relations between tickets.
- **Limitation 1 (compromised retrieval accuracy from ignoring structure):** issue trackers like Jira are inherently structured and interconnected (e.g. "issue A is related to / copied from / caused by issue B"), yet compressing documents into text chunks discards that relationship information; the paper instead parses each ticket into a tree and links tickets into an interconnected graph to maintain entity relationships.
- **Limitation 2 (reduced answer quality from segmentation):** splitting long tickets into fixed-length segments can cut related content apart, yielding incomplete answers — e.g. a ticket that states the issue at the beginning and the solution at the end may be split between the two, so the solution portion is omitted from the retrieved context.
- The method reports outperforming the baseline by **77.6% in MRR** and by **0.32 in BLEU** on their benchmark datasets, and after ~6 months of deployment at LinkedIn it cut median per-issue resolution time by **28.6%**.
- QA-with-KG work is broadly taxonomy'd into three families: **retrieval-based** (relation extraction / distributed representations, weak on multi-entity questions), **template-based** (hand-crafted templates for encoding complex queries, bounded by template scope), and **semantic-parsing-based** (mapping text to logical forms with predicates drawn from KGs).
- Recent LLM+KG integration work cited includes Think-on-Graph and Reasoning-on-Graph (KG-integrated LLM reasoning), Yang et al. (KG-augmented LLM factual reasoning across training phases), and Wen et al.'s Mindmap / Qi et al. (KGs boosting LLM inference in specialized domains such as medicine and food).
- The authors position their system as applying that LLM+KG synergy specifically to customer-service QA: a two-phase pipeline that first builds a KG (tree per ticket + explicit/implicit inter-ticket links + per-node embeddings) and then, at query time, parses the consumer query into named entities and intents to navigate to relevant sub-graphs for answer generation.

## 2. [[wiki/02-knowledge-graph-method|Knowledge Graph Method]]

**In one sentence:** The system models each support ticket as a typed two-level knowledge graph — an intra-ticket tree of fields (summary, description, comments, steps-to-reproduce) plus inter-ticket edges (explicit clone links and implicit similarity links) — and at query time parses the question into entities and intents, ranks candidate tickets by summed node-level cosine similarity, translates the augmented query into a Cypher query to fetch the relevant sub-graph, and has an LLM decode the final answer over that sub-graph.

- **Two-level graph structure:** each ticket `ENT-*` expands into an **intra-issue tree `T_i`** (typed child nodes connected by `HAS_SUMMARY`, `HAS_DESCRIPTION`, `HAS_FIELDS`/`HAS_PRIORITY`/`HAS_ROOT_CAUSE`/`HAS_IMPACT_AREA`, `HAS_COMMENTS`, `HAS_STEPS_TO_REPRODUCE`), and tickets are linked into an **inter-issue graph `G`** (e.g., `ENT-22970` connected to `ENT-1744`, `ENT-3547`, `PORT-133061`).
- **Two edge types between tickets:** **explicit edges `E_exp`** (`CLONE_FROM`/`CLONE_TO`) derived from verbatim cloning references in ticket text, and **implicit edges `E_imp`** (`SIMILAR_TO`) derived from embedding similarity between tickets — so the inter-ticket layer = `E_exp ∪ E_imp`.
- **Construction is a two-phase hybrid:** a rule-based parser handles structured fields (summary, priority, root cause, impact area, steps) while an LLM is used to extract less structured content such as comments, summaries and clone/similarity links; the result is written to a graph database (Neo4j) for structure and a vector database for the node embeddings.
- **Embedding generation:** BERT/E5-class text embeddings are computed for node *values* (the free-text inside each node, not the node type), with text chunking applied within a section, so retrieval operates at node level and is aggregated to ticket level.
- **Query parsing:** given query `q`, an LLM extracts a key–value entity map `P = Map(N → V)` whose keys match fields in the graph template `T_template` plus an intent set `I` (e.g., `I = Set("fix solution")`), i.e. `P, I = LLM(q, T_template, prompt)`; for the login-issue example: `P = Map("issue summary" → "login issue", "issue description" → "user can't log in to LinkedIn")`.
- **Sub-graph retrieval scoring:** for each ticket `i`, the score is `S_Ti = Σ_{(k,v)∈P} Σ_{n∈Ti} I{n.sec = k} · cos(embed(v), embed(n.text))` — cosine similarity between each entity value and all nodes of the ticket in the matching section, summed over entity pairs; the top-`K` tickets by `S_Ti` are selected, so multiple matching entities reinforce a ticket.
- **Cypher translation:** the original query is rephrased to embed the retrieved ticket ID and then translated by an LLM into a Cypher query, e.g. `MATCH (j:Ticket {ticket_ID: 'ENT-22970'})-[:HAS_DESCRIPTION]->(description:Description)-[:HAS_STEPS_TO_REPRODUCE]->(steps_to_reproduce:StepsToReproduce) RETURN steps_to_reproduce.value` — versatile enough to span nodes in one tree or across different trees.
- **Answer generation with fallback:** the LLM acts as a decoder producing the answer from the retrieved sub-graph plus the original query; if graph query execution fails under online serving, a fallback reverts to a baseline text-based (flat vector) retrieval.

## 3. [[wiki/03-experiments-and-production|Experiments and Production Results]]

**In one sentence:** The KG-enhanced RAG system beat the plain-text baseline by 77.6% in MRR and 0.32 in BLEU on the golden dataset, and in a live LinkedIn A/B deployment cut median issue resolution time by 28.6% (7h → 5h).

- Retrieval: MRR jumps from 0.522 (baseline) to 0.927 (experiment) — a 77.6% relative improvement; Recall@3 rises from 0.640 to 1.000 and NDCG@3 from 0.520 to 0.946.
- Exact-hit retrieval also nearly perfect: Recall@1 goes 0.400 → 0.860 and NDCG@1 goes 0.400 → 0.860.
- Generation: BLEU 0.057 → 0.377 (+0.32), METEOR 0.279 → 0.613, ROUGE 0.183 → 0.546 — consistent gains across all answer-quality metrics.
- Production A/B test on LinkedIn's customer-service team (multiple product lines, random split): the tool-using group cut mean resolution time 40h → 15h, median (P50) 7h → 5h (−28.6%), and P90 87h → 47h.
- Both arms used the **same** GPT-4 LLM and the same E5 embedding model, isolating the KG-templated retrieval methodology as the differentiator.
- Evaluation used a curated "golden" dataset of typical queries, support tickets, and their authoritative solutions; retrieved context scored with MRR, Recall@K, NDCG@K, and generated answers scored against golden solutions with BLEU, ROUGE, METEOR.
- Conclusions: KG + RAG improves retrieval, answering accuracy, and overall service effectiveness; three future directions — automated graph-template extraction, dynamic KG updates from user queries, and applicability beyond customer service.

## The argument in five moves

1. Chunk-based RAG for customer-service tickets discards two things that matter: the structure inside a ticket and the relations between tickets — this costs both retrieval accuracy and answer completeness.
2. So model each ticket as a typed tree (summary/description/fields/comments/steps) and link tickets into a graph via explicit clone edges and implicit similarity edges, built by a rule-based + LLM hybrid parser.
3. At query time, have an LLM extract entities and intent from the question, use those to score and rank candidate tickets by section-matched embedding similarity, then translate the augmented query into a Cypher query that fetches exactly the right sub-graph.
4. Decode the final answer with an LLM reading that sub-graph, with a flat-vector fallback if the graph path fails online.
5. On a golden benchmark this beats a matched-LLM/embedder text baseline by 77.6% MRR and 0.32 BLEU, and in a live 6-month LinkedIn deployment it cut median ticket resolution time by 28.6% — evidence that graph-structured retrieval, not just a better LLM or embedder, is what moved the numbers.
