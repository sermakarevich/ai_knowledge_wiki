---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: GraphRAG under Fire

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does the classic PoisonedRAG attack lose effectiveness against GraphRAG compared to NaiveRAG?

> [!tip]- Answer
> GraphRAG's indexing pipeline uses an LLM to extract entity/relation descriptions from the corpus, and when it encounters both the original clean statement and the isolated poisoning statement, it tends to omit the poisoning content or generate the accurate description anyway — clean knowledge effectively dilutes/filters the injected text before it ever reaches retrieval. See [[wiki/02-rq1-existing-attacks-fail|RQ1: Existing Attacks Fail Under GraphRAG]].

### Q2. What is a "relation" in GraphRAG's knowledge graph, and why does GRAGPOISON target relations instead of answers?

> [!tip]- Answer
> A relation is a labeled edge connecting two entities (e.g., "Stuxnet — uses → DLL Injection"). GRAGPOISON targets relations because a single shared relation can underlie many different queries (e.g., both "how to mitigate" and "how to detect" Stuxnet depend on the same relation), so poisoning one relation compromises all queries that depend on it simultaneously — far more scalable than crafting a separate fake answer per query. See [[wiki/01-introduction-and-threat-model|Introduction and Threat Model]].

### Q3. GRAGPOISON's relation-selection step is formulated as a classical algorithmic problem. Which one, and why does that framing matter?

> [!tip]- Answer
> It's formulated as the set cover problem: given target queries and the relations each one depends on, find the smallest set of relations that collectively "covers" (touches) every target query. A greedy algorithm iteratively picks the relation covering the most still-uncovered queries — the best achievable polynomial-time approximation. It matters because it directly minimizes the total poisoning-text budget needed, which is what makes the attack cheap and stealthy. See [[wiki/03-gragpoison-design|GRAGPOISON Attack Design]].

### Q4. What is a "covering narrative," and why is bare relation-injection text insufficient on its own?

> [!tip]- Answer
> Bare injection text (stating the fake relation directly) creates a logical inconsistency with the original relation already in the corpus, which GraphRAG's indexing can detect and reject. A covering narrative disguises the fake relation as a legitimate update using three combined techniques — temporal ordering (it happened later), explicit negation (it supersedes the original), and contextual explanation (a plausible reason for the change) — so the injected fact reads as consistent, chronologically later information rather than a contradiction. See [[wiki/03-gragpoison-design|GRAGPOISON Attack Design]].

### Q5. In the ablation study, which single "trick" contributes the most to GRAGPOISON's success, and roughly how much does removing it hurt ASR on average?

> [!tip]- Answer
> Temporal ordering contributes the most — removing it drops average ASR by about 18.3 percentage points (as high as −32.9% on Cyber-Security), because dating the fake fact beyond the LLM's training cutoff reduces the model's reliance on its own prior knowledge and increases the chance it trusts the poisoning text as newer, valid information. See [[wiki/04-evaluation-results|Evaluation Results]].

### Q6. How does "relation enhancement" (adding supporting entities) actually help the injected relation win, mechanically?

> [!tip]- Answer
> GraphRAG ranks retrieved relations partly by the degree (number of connections) of their endpoint entities, and ranks community summaries by how many of a query's relevant entities they cover. By attaching several supporting entities to the injected entity, GRAGPOISON raises that entity's degree (winning the relation-ranking competition) and makes it co-selected into the same graph community as other query-relevant entities (winning the community-ranking competition) — targeting both of GraphRAG's ranking mechanisms at once. See [[wiki/03-gragpoison-design|GRAGPOISON Attack Design]].

### Q7. GRAGPOISON operates in a "KG-agnostic" threat model. What does that mean, and how does the attack still work without it?

> [!tip]- Answer
> KG-agnostic means the adversary has no access to GraphRAG's actual constructed knowledge graph, retriever, or generator — only the ability to inject text into the source corpus and knowledge of the target queries themselves. The attack still works because an adversarial LLM is prompted to reason step-by-step (chain-of-thought) over each target query, inferring the likely intermediate entities and relations purely from the query's wording, then aggregating those inferences across queries to identify shared relations to poison. See [[wiki/01-introduction-and-threat-model|Introduction and Threat Model]] and [[wiki/03-gragpoison-design|GRAGPOISON Attack Design]].

### Q8. Of the five defenses evaluated, which one is meaningfully effective, and what would it take to deploy it fully?

> [!tip]- Answer
> Provenance-aware trust scoring is the only defense that meaningfully reduces ASR (dropping MuSiQue ASR from 89.2% to 45.7% in the simplified test where trust labels are appended directly to corpus text). A full deployment would require re-engineering GraphRAG's indexing (to track source trust per extracted fact), retrieval (to weight ranking by trust, not just similarity/degree), and generation (to prompt the LLM to prefer high-trust sources and flag uncertainty on conflicts) — none of which exists in GraphRAG today. See [[wiki/05-defenses-related-work-conclusion|Defenses, Related Work, and Conclusion]].

### Q9. GRAGPOISON was tested against GraphRAG, LightRAG, and nano-GraphRAG with comparable success. What does that cross-system result imply about the nature of the vulnerability?

> [!tip]- Answer
> Comparable ASR across three independently-implemented graph-based RAG systems implies the vulnerability is not an implementation quirk of one codebase, but an inherent structural weakness shared by the graph-based RAG paradigm itself (shared-relation exploitation, degree/community-based ranking) — meaning defenses need to be designed at the paradigm level, not patched into a single tool. See [[wiki/04-evaluation-results|Evaluation Results]].

### Q10. The paper's own tested defenses are weak, and the "fix" it points to (provenance-aware trust scoring) is only a simplified proof of concept. Given that, how strong is the paper's actual evidence for GRAGPOISON's real-world severity, and what would meaningfully increase or decrease your confidence?

> [!tip]- Answer
> The core ASR/QPP/TPQ numbers are well-supported by controlled experiments across four datasets, two adversarial LLMs, multiple GraphRAG variants, and several ablations — that part is solid. But the datasets are synthetic/curated (Wikipedia hierarchies, Hetionet, ATT&CK templates) rather than messy real-world corpora, and the underlying "GraphRAG" is GPT-4o-mini at default settings, not necessarily what a hardened production deployment would run. Confidence would increase with results on a real, live production corpus and against a system that already has some access-control/provenance layer in place, and would decrease if the attack failed to transfer to a differently-tuned or ensembled retrieval configuration. See [[critical_thinking|Critical Analysis]].
