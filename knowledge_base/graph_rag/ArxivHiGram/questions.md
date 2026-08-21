---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: HiGram

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What granularity mismatch does HiGram claim existing graph-memory systems suffer from, and how does that mismatch cause both high retrieval cost and incomplete updates?

> [!tip]- Answer
> Existing systems organize and update memory over the whole flat graph or per individual unit, but the evidence an answer actually depends on is a small, localized, interconnected path. Retrieval over the whole graph pulls in irrelevant context as memory accumulates, and unit-independent updates miss the evidence paths an update propagates along, requiring repeated global re-search to catch all affected facts. See [[wiki/01-hierarchical-memory-and-method|Hierarchical Memory and the HiGram Method]].

### Q2. What are the two node types in HiGram's hierarchical graph, and what job does each do?

> [!tip]- Answer
> Upper-level nodes (subject, object-category, context) provide coarse organizational access, forming an abstraction layer over the facts. MemoryUnits store the fine-grained facts themselves, each with attributes (subject, relation, object, category, time, context, confidence, status) and explicit dependency edges to other MemoryUnits. See [[wiki/01-hierarchical-memory-and-method|Hierarchical Memory and the HiGram Method]].

### Q3. Why are (subject, object-category) chosen as the key for a MicroGraph rather than, say, time or confidence?

> [!tip]- Answer
> Because subject and object-category are stable across temporal updates — they don't change as facts get corrected or superseded — which makes them reliable, cheap keys for narrowing down to a relevant memory region before the more expensive step of scoring individual evidence paths. See [[wiki/01-hierarchical-memory-and-method|Hierarchical Memory and the HiGram Method]].

### Q4. Walk through what happens to a MemoryUnit that depended on a fact that just got updated, if its supporting evidence is no longer consistent.

> [!tip]- Answer
> During inter-unit rewriting, the system identifies the units directly dependent on the changed unit and checks whether their supporting evidence is still consistent. If not consistent, the dependent unit is marked outdated and excluded from the current evidence view — its dependency is not blindly inherited from before the update, so it doesn't keep being used as if still valid. See [[wiki/01-hierarchical-memory-and-method|Hierarchical Memory and the HiGram Method]].

### Q5. On LoCoMo, how does HiGram's token usage compare to full-context and to the strongest compact baseline, and what does the ablation study say drives that token efficiency?

> [!tip]- Answer
> HiGram uses ~2,912 tokens, about 7.2% of full-context's 4,909 tokens, and about 15.8% of ReadAgent's 3,873 tokens under GPT-4o. The ablation shows removing MicroGraph organization specifically raises token use by 68.6% (back toward full-context levels), so the coarse MicroGraph-based localization — not the support-subgraph/path-selection step — is the main driver of token savings. See [[wiki/02-experiments-and-results|Experiments and Results]].

### Q6. On the MemConflict benchmark, why might HiGram's coordinated rewrite outperform a simple Append-Only update strategy even though Append-Only never risks losing information?

> [!tip]- Answer
> Append-Only inserts new facts without modifying old ones, so it never actively corrects stale information — it scored a modest, balanced 42.89 average. HiGram's coordinated rewrite (56.77 average) both records fact-state transitions and revises dependent units' validity, achieving much stronger Static AA (68.75) because it resolves conflicts (recognizing invalid replacements) rather than just accumulating potentially contradictory entries. See [[wiki/02-experiments-and-results|Experiments and Results]].

### Q7. What does the hyperparameter sensitivity analysis (Figure 3) suggest about how carefully K_g and K_p need to be tuned in practice, and why?

> [!tip]- Answer
> Both metrics rise only gradually and then flatten (saturate) as K_g (retrieved MicroGraphs) or K_p (candidate paths) increase, rather than sharply peaking at one specific value. This indicates HiGram is robust to these hyperparameters — its scoring mechanism can identify relevant evidence under a range of search budgets — so careful tuning isn't required for good performance. See [[wiki/02-experiments-and-results|Experiments and Results]].

### Q8. HiGram is evaluated only on LoCoMo and MemConflict. Based on the critical analysis, what's the strongest reason to be cautious about generalizing its reported gains to a different, unrelated deployment setting?

> [!tip]- Answer
> Both benchmarks target long personal/conversational histories with clearly delineated per-fact structure (subject/relation/object), which is exactly the shape HiGram's design assumes; there's no evidence presented for domains with noisier or less structured facts, larger-scale enterprise-style memories, or conflicts that don't reduce cleanly to a single evidence path. See [[critical_thinking|Critical Analysis]].
