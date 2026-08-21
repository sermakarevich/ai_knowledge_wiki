---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the two structural weaknesses of standard chunk-based RAG that this paper identifies, and what concrete example does it give for the second one?

> [!tip]- Answer
> (1) Flattening tickets into plain-text chunks discards the relationships between tickets (e.g. Jira's "related to"/"copied from"/"caused by" links). (2) Fixed-length segmentation can sever related content within a single ticket — the paper's example is a ticket that states the problem at the beginning and the solution at the end, where chunking splits them apart and the retrieved context omits the solution. See [[wiki/01-introduction-and-related-work|Introduction and Related Work]].

### Q2. Describe the two levels of the knowledge graph the system builds, and name the two types of edges that connect different tickets to each other.

> [!tip]- Answer
> Level 1: an intra-issue tree `T_i` per ticket with typed `HAS_*` edges (summary, description, fields/priority/root cause/impact area, comments, steps-to-reproduce). Level 2: an inter-issue graph `G` linking tickets via explicit edges (`CLONE_FROM`/`CLONE_TO`, derived from verbatim clone references) and implicit edges (`SIMILAR_TO`, derived from embedding similarity). See [[wiki/02-knowledge-graph-method|Knowledge Graph Method]].

### Q3. Walk through how a user query is turned into a retrieved sub-graph, from the raw question to the Cypher query.

> [!tip]- Answer
> An LLM parses the query into an entity map `P` (field → extracted value) and an intent set `I`. Each entity value is compared (cosine similarity) against nodes of matching section in every ticket's tree, scores are summed across entities per ticket, and the top-K tickets are ranked (`S_Ti = Σ cos(...)`). The original query is then rephrased to name the top ticket's ID, and an LLM translates that rephrased query into a Cypher query that walks the graph database to the exact relevant node(s) (e.g. `MATCH (j:Ticket {ticket_ID:'ENT-22970'})-[:HAS_DESCRIPTION]->...`). See [[wiki/02-knowledge-graph-method|Knowledge Graph Method]].

### Q4. Why does the system fall back to flat-vector text retrieval, and under what condition does that fallback trigger?

> [!tip]- Answer
> Because the graph/Cypher retrieval path can fail during online serving (e.g. a malformed generated Cypher query or a system error); rather than returning no answer, the system degrades gracefully by reverting to a baseline text-based (flat embedding) retrieval so the QA service keeps functioning. See [[wiki/02-knowledge-graph-method|Knowledge Graph Method]].

### Q5. On the golden evaluation set, what were the MRR and BLEU scores for the baseline vs. the KG-RAG system, and what design choice makes this a fair comparison?

> [!tip]- Answer
> MRR: 0.522 (baseline) → 0.927 (KG-RAG), a 77.6% relative improvement. BLEU: 0.057 → 0.377. The comparison is fair because both the control and experimental arms used the identical LLM (GPT-4) and embedding model (E5) — the only difference was the retrieval methodology (flat text vs. KG-templated). See [[wiki/03-experiments-and-production|Experiments and Production Results]].

### Q6. What was the actual business-metric result of the LinkedIn production A/B test, and why does it matter more than the offline MRR/BLEU numbers?

> [!tip]- Answer
> Median (P50) issue resolution time fell from 7 hours to 5 hours (−28.6%), mean from 40h to 15h, and P90 from 87h to 47h, in a live random-split A/B across multiple LinkedIn product lines. It matters more because it is a real operational outcome measured on live traffic, not just an offline retrieval/generation-quality proxy — it shows the offline gains actually translated into faster real-world support resolution. See [[wiki/03-experiments-and-production|Experiments and Production Results]].

### Q7. Name the three future-work directions the authors propose, and explain why each addresses a limitation of the current system.

> [!tip]- Answer
> (1) Automated graph-template extraction — currently templates are hand-crafted from support-ticket analysis, limiting adaptability to new domains/ticket types. (2) Dynamic KG updates from user queries — the current graph is static once built, so it can't incorporate new information from ongoing interactions. (3) Broader applicability beyond customer service — the method was validated only in this one domain. See [[wiki/03-experiments-and-production|Experiments and Production Results]].

### Q8. What is the weakest link in this paper's evidence, and what would need to be true for its claims to generalize to your own use case?

> [!tip]- Answer
> The evidence is entirely internal and self-reported: a proprietary "golden dataset" that was not released, and a single internal A/B test at one company, with no independent replication or public benchmark comparison. For the claims to generalize, your data would need genuine internal structure and cross-record relationships analogous to Jira tickets (not truly independent, unstructured documents), and you'd need the willingness to hand-build graph templates and a hybrid rule/LLM extraction pipeline. See [[critical_thinking|Critical Analysis]].
