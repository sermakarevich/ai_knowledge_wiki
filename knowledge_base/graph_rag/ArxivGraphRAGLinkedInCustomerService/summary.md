# Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering

**Paper:** [Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering (Xu et al., 2024)](https://arxiv.org/abs/2404.17723)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine a customer-support team with thousands of old support tickets sitting in a filing cabinet. A normal "smart search" tool chops each ticket into text snippets and finds the ones that sound similar to a new question — but it treats every snippet in isolation, so it can miss that a ticket's "problem" is described at the top and its "solution" is buried at the bottom, and it has no idea that ticket #22970 is basically the same issue as tickets #1744 and #3547. LinkedIn's engineers instead built a "map" (a knowledge graph) that keeps each ticket's parts connected (summary → description → comments → steps to fix) and draws lines between related tickets. When a new question comes in, the system reads the map, jumps straight to the right ticket and the right part of it, and has an AI write the answer from that. In a real production test at LinkedIn, this cut the time it took to resolve a customer issue nearly in half.

## TL;DR

The paper fuses RAG with a knowledge graph (KG) to fix two structural weaknesses of plain-text chunk-based retrieval for customer-service QA: loss of intra-ticket structure and inter-ticket relations. Each support ticket becomes a typed intra-issue tree (summary/description/fields/comments/steps) plus explicit (`CLONE_FROM/TO`) and implicit (`SIMILAR_TO`) inter-ticket edges, built by a rule-based + LLM hybrid parser and stored in a graph DB (Neo4j) with node embeddings in a vector DB. At query time an LLM extracts entities/intent from the question, scores tickets by summed cosine similarity per matching section, generates a Cypher query over the top ticket's sub-graph, and an LLM decodes the final answer (falling back to flat-vector retrieval if the graph query fails). On a golden evaluation set this beats a same-LLM/same-embedder text baseline by 77.6% in MRR (0.522→0.927) and 0.32 in BLEU (0.057→0.377); in a live LinkedIn A/B across multiple product lines it cut median per-issue resolution time 28.6% (7h→5h).

---

## Problem & Motivation

Customer-service QA over past support tickets is core to resolution speed, and RAG/EBR/LLMs have improved it — but standard chunk-based RAG has two flaws: (1) it flattens structured, interconnected tickets (e.g. Jira issues with "related to"/"copied from"/"caused by" links) into isolated text chunks, discarding relationship information and hurting retrieval; (2) fixed-length chunking can sever a ticket's problem description from its solution, producing incomplete answers.

---

## Main Original Ideas

1. **Two-level knowledge graph per ticket corpus.** Each ticket is an intra-issue tree (`HAS_SUMMARY`, `HAS_DESCRIPTION`, `HAS_FIELDS`, `HAS_COMMENTS`, `HAS_STEPS_TO_REPRODUCE`), and tickets are linked into a global graph via explicit clone edges (`CLONE_FROM/TO`) and implicit embedding-similarity edges (`SIMILAR_TO`).
2. **Hybrid rule-based + LLM graph construction.** A rule-based parser handles structured fields; an LLM extracts unstructured content (comments, summaries, clone links). Output is stored as a graph DB (Neo4j) plus a vector DB of node embeddings.
3. **Entity/intent-driven retrieval and Cypher generation.** An LLM parses the query into an entity map and intent set matched against the graph template; tickets are ranked by section-matched cosine similarity summed across entities; the top ticket's query is rephrased and translated by an LLM into a Cypher query that pulls the exact relevant sub-graph (potentially spanning multiple ticket trees).
4. **Graceful degradation.** If the Cypher/graph retrieval path fails online, the system falls back to baseline flat-vector text retrieval rather than failing outright.

---

## Key Findings

| | MRR | Recall@1 | Recall@3 | NDCG@1 | NDCG@3 |
|---|---|---|---|---|---|
| Baseline (text EBR) | 0.522 | 0.400 | 0.640 | 0.400 | 0.520 |
| KG-RAG (this paper) | 0.927 | 0.860 | 1.000 | 0.860 | 0.946 |

| | BLEU | METEOR | ROUGE |
|---|---|---|---|
| Baseline | 0.057 | 0.279 | 0.183 |
| KG-RAG | 0.377 | 0.613 | 0.546 |

- Production A/B (LinkedIn customer service, multiple product lines, random split): mean resolution time 40h → 15h; **median (P50) 7h → 5h (−28.6%)**; P90 87h → 47h.
- Both control and experimental arms used the same GPT-4 LLM and the same E5 embedding model, isolating the KG-templated retrieval method as the source of the gain.

---

## Suggestions & Future Directions

1. **Automated graph-template extraction** — templates are currently hand-crafted from support-ticket analysis; automating this would improve adaptability to new domains.
2. **Dynamic KG updates** — investigate updating the knowledge graph in response to user queries for better real-time responsiveness.
3. **Broader applicability** — explore the approach beyond customer service.

---

## Authors & Institutions

Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie Wang, Manasi Deshpande, Xiaofeng Wang, Zheng Li — LinkedIn.

## Figures

![Figure 1: overview of the RAG + knowledge graph framework](wiki/images/01-figure1-overview.png)
