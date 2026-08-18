---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Zero-Mem: Zero-Token Memory Operations for LLM Agents

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. The Introduction lays out two existing memory strategies before Zero-Mem's own. What is the specific failure mode of each, and what single joint property does the paper argue neither one delivers on its own?

> [!tip]- Answer
> Generative memory turns memory management into a recurring LLM-generation workload, and its generated abstractions (summaries, compressed notes) can omit details, merge subjects, or blur temporal updates, weakening traceability back to the original interaction. Raw retrieval preserves source evidence but flat lexical/dense search can confuse semantically similar traces from different users, sessions, or temporal states, and can fail when the needed evidence is distributed across multiple interactions. The paper concludes effective memory requires both faithful preservation of original evidence *and* structured, query-conditioned evidence selection — neither strategy provides both. See [[wiki/01-problem-motivation-and-related-work|Problem, Motivation, and Related Work]].

### Q2. What is the edge-weight formula for the entity-context graph, and what does each term mean?

> [!tip]- Answer
> w(d_i, e) = c(e, d_i) / Σ_{e′∈E(d_i)} c(e′, d_i), where c(e, d_i) is the occurrence frequency of entity e in context unit d_i, and E(d_i) is the set of all entities detected in d_i. So the weight is entity e's *share* of total entity mentions within that unit — a normalized frequency rather than a raw count — meaning an entity that dominates a unit's content gets a stronger edge than one that merely co-occurs once alongside many others. See [[wiki/02-memory-substrate-and-structures|Memory Substrate and Structures]].

### Q3. The temporal hierarchy has four granularities: turn, window, episode, and local span. Why is "local span" needed as a distinct fourth unit rather than just relying on turn/window/episode nesting?

> [!tip]- Answer
> Turn, window, and episode form a fixed structural nesting used to *organize and search* the history (atomic utterance → short-range context → coherent event region). Local span is different: it is not a fixed tier but a dynamic, on-demand expansion around whichever specific turn was just selected as evidence, added only when that evidence needs surrounding context to be interpretable (e.g., a pronoun or follow-up reference resolved only by neighboring turns). Without it, evidence retrieval could return an isolated turn that is technically relevant but missing the immediate context needed to use it correctly. See [[wiki/02-memory-substrate-and-structures|Memory Substrate and Structures]].

### Q4. What are the three deterministic corrections that answer-level calibration can apply to the reader's initial answer a0, and when does calibration leave a0 unchanged?

> [!tip]- Answer
> When a0 is not well-supported or well-formed, Calibrate can apply: (1) normalization — evidence-preserving normalization of the answer's form; (2) extractive shortening — trimming to the supported extractive content; or (3) item-wise list pruning — removing unsupported items from a list-form answer. A scalar answer may also be substituted with a unique type-compatible candidate from the extracted set A(q). If a0 is already supported and well-formed, or if no deterministic correction applies, a0 is retained as-is — calibration never invents new content, it only preserves, trims, normalizes, or substitutes using evidence already extracted from R(q). See [[wiki/03-query-routing-retrieval-and-calibration|Query Routing, Retrieval, and Calibration]].

### Q5. Suppose you wanted to apply Zero-Mem's dual-view-plus-routing approach to a codebase-search agent that must remember prior debugging sessions. What would the graph view, the temporal view, and the routing step each become in that setting?

> [!tip]- Answer
> The entity-context graph becomes a graph over code artifacts (files, functions, symbols, error messages) with edges weighted by normalized co-occurrence within a commit, PR, or debugging session — giving relational access like "what else touched this function." The temporal hierarchy becomes sessions → episodes (a debugging effort) → windows (an edit/test cycle) → turns (a single query or edit), with local-span expansion pulling in the surrounding edits or chat turns around a matched turn. At query time, a lightweight profile (target symbol/file as subject, keywords, expected answer type, temporal cues, repo/branch boundary) would route between a relational query ("who else calls this API") and a local/session query ("what did we conclude last session about this bug"), fusing both views by a shared weight before closure and calibration hand the LLM a compact, provenance-tied evidence set — avoiding an LLM call for every memory read or update. See [[wiki/03-query-routing-retrieval-and-calibration|Query Routing, Retrieval, and Calibration]].

### Q6. In the HotpotQA ablation, removing evidence closure drops the full model from 72.07 to 67.90 F1, while removing evidence calibration only drops it to 70.13 F1. Why does removing closure hurt more than removing calibration?

> [!tip]- Answer
> Evidence closure is what *adds* missing evidence back into the set — graph bridges and local neighbors that the fused ranking alone might have ranked below the cutoff — so without it the reader can be missing structurally or locally connected evidence it needs to answer at all, especially for HotpotQA's distributed multi-hop evidence. Calibration, by contrast, only filters, ranks, normalizes, or trims an answer using evidence that has already been retrieved; it cannot recover evidence that was never in the set. So losing closure risks an incomplete evidence set (a larger, more fundamental gap), while losing calibration risks a poorly-formed or slightly unsupported answer built from evidence that was already sufficient (a smaller, more cosmetic gap). See [[wiki/04-experiments-results-and-conclusion|Experiments, Results, and Conclusion]].

### Q7. What is the weakest link in Zero-Mem's evidence for its efficiency claim (zero memory-operation tokens, 57.6% latency reduction)?

> [!tip]- Answer
> See [[critical_thinking|Critical Analysis]] for the verdict. Candidate weak points visible from the wiki alone: the latency comparison is a single-hardware, single-configuration snapshot (one set of baselines, γ = ρ = 0.6, Top-5 capped) measured against LightMem as "the fastest baseline" — it is a relative claim against one particular competitor set rather than an absolute or asymptotic guarantee, and it reports total pipeline time without decomposing how NER, BM25/dense indexing, and PageRank propagation costs individually scale as history length grows. "Zero LLM tokens" is a real and verifiable property of the design, but "faster overall" is an empirical result tied to the specific benchmarks, hardware, and baselines tested, not a proven complexity bound. See [[wiki/04-experiments-results-and-conclusion|Experiments, Results, and Conclusion]].
