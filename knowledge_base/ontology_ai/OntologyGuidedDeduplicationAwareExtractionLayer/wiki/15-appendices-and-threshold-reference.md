> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendices and Threshold Reference

**In one sentence:** Table 22 consolidates every tunable threshold in the extraction and resolution pipeline as deployment defaults tuned on the development corpus, supported by appendices on Kafka consumption, session management, parallel processing, persistence, concurrency tuning, and field issues.

## Key points

- Table 22 is explicitly deployment defaults tuned on the development corpus with no claim of universality, plus a hard-conflict guard on discriminator keys (date of birth, nationality, passport or employee number) that forbids merging however similar names are.
- The class/predicate retrieval floor is 0.72 after the PageRank penalty, overridable via `ONTOLOGY_RETRIEVAL_MIN_SCORE`, superseding an initial 0.50 floor that admitted too many "vaguely related" classes.
- Subclass expansion triggers at ≥0.80 with injected children scored at 0.78, while the predicate vocabulary guard snaps only synonyms ≥0.80 and flags the rest `_novel_predicate`.
- Duplicate handling uses 0.75 candidate / 0.95 auto-merge with full context agreement / 0.90–0.95 human-review band for context-aware detection, and 0.85 auto-merge / 0.60–0.85 manual-review / 0.50 codename-candidate for the embedding-based engine.
- Kafka consumer uses max.poll.interval.ms 1,800,000 ms and session.timeout.ms 300,000 ms to survive LLM inference latency, at the cost of ~6.5 minutes recovery after unclean shutdown.
- Concurrency was tuned down from WORKER_COUNT 10→4 and MAX_IN_FLIGHT_TASKS 40→16 after ten concurrent large PDFs exhausted memory and saturated vLLM, while embedding backfill uses EMBED_BATCH_SIZE 20 with EMBED_PARALLEL_BATCHES 5.
- Field issues were fixed by per-page OCR classification replacing binary whole-document routing, Signal 5 (drawing count >200) for vector-drawn text, and Signal 3 (xref image coverage) for cross-reference images.

---

## A. Threshold reference

Table 22 consolidates every tunable threshold in the extraction and resolution pipeline, the subsystem it governs, and the decision it drives.

| Value | Subsystem (section) | Role / decision |
|---|---|---|
| 0.50 | Class retrieval (§4) | Initial cosine floor; admitted too many "vaguely related" classes, superseded by 0.72. |
| 0.72 | Class/predicate retrieval (§4) | Retrieval floor (min_score) after the PageRank penalty; classes/predicates scoring above it are injected. Env: ONTOLOGY_RETRIEVAL_MIN_SCORE. |
| 0.80 | Subclass expansion (§4) | Trigger: for any class scoring ≥ 0.80, traverse subClassOf one hop downward. |
| 0.78 | Subclass expansion (§4) | Score assigned to injected child classes (just above the 0.72 floor, below the parent). |
| 0.80 | Predicate vocabulary guard (§4) | Embedding snap floor: only predicate synonyms ≥ 0.80 snap to the ontology object-property vocabulary; below it the predicate is left verbatim and flagged _novel_predicate. |
| 0.85 | Source-text variant miner (§6) | Acceptance threshold τ for a mined spelling variant. |
| 0.75 | Context-aware duplicate detection (§6) | Candidate threshold: name similarity ≥ 0.75 (with full context agreement) to consider a pair at all. |
| 0.95 | Context-aware duplicate detection (§6) | Auto-merge cell of the decision surface: name similarity > 0.95 and full contextual agreement on role/organisation/location. |
| 0.90–0.95 | Context-aware duplicate detection (§6) | Human-review band (high name similarity, partial context). |
| 0.85 | Embedding-based resolution engine (§6) | Composite-score auto-merge. |
| 0.60–0.85 | Embedding-based resolution engine (§6) | Manual-review band. |
| 0.50 | Embedding-based resolution engine (§6) | Codename-candidate (with codename pattern); otherwise distinct. |

> "The two "0.80" rows and the two "0.85"/"0.75"/"0.95" rows govern distinct subsystems and are not interchangeable."

> "Independently of any score, a hard-conflict guard on discriminator keys (date of birth, nationality, passport or employee number) forbids merging two entities, however similar their names."

## B. Operational configuration

Collects deployment-level configuration detail: Kafka consumption and session management, evolution from sequential to parallel processing, output persistence, and concurrency tuning.

### B.1 Kafka consumption and record normalisation

The consumer subscribes to the `ingested-objects` Kafka topic and processes two categories:

- **File-based Records:** metadata pointers (`object_id`, filename, `mime.type`) used to locate the raw file under a configurable base path, organized by MIME type into `text/`, `pdf/`, `image/`, `audio/` subdirectories.
- **Database-embedded Records:** full document text inline (`report_text`, `content`, or `text`) plus metadata including title, classification, and timestamps; bypass filesystem resolution entirely.

A normalization layer (`normalize_record`) unifies these into a stable internal representation, handling MongoDB-style `_id` objects with nested `$oid` fields, varying timestamp conventions (camelCase versus snake_case), and differing content field names.

### B.1.1 Kafka consumer session management and rebalancing tradeoffs

Configured with `max.poll.interval.ms` of 1,800,000 ms and `session.timeout.ms` of 300,000 ms to accommodate LLM inference latency without triggering rebalances.

Table 23: Kafka Session Timeout Tradeoff Analysis

| Config | Advantages | Disadvantages |
|---|---|---|
| 300 s (current) | Long-running LLM inference calls complete without triggering rebalances; essential for large multi-chunk PDF extractions | Stale consumer sessions block new consumers from acquiring partitions for up to 5 minutes after an unclean shutdown |
| 45 s (Kafka default) | Fast recovery after consumer crashes; new instances acquire partitions within seconds | LLM calls exceeding 45 seconds cause the broker to evict the consumer mid-processing, resulting in rebalance storms and duplicate processing |
| 60–90 s (balanced) | Reasonable recovery time (~1–1.5 minutes) while accommodating most single-chunk LLM calls | May still trigger rebalances on very large documents requiring extended multi-phase extraction |

> "The cost of the long timeout is visible on unclean shutdown: the broker keeps the stale session alive until it expires, so a replacement consumer was observed waiting ~6.5 minutes (the 300-second timeout plus rebalancing overhead) before receiving its first message."

Practical guidance follows the inference-latency profile: 60–90 s suffices for fast local models with small context windows, while 300 s remains necessary for multi-phase extraction of large documents.

### B.2 Evolution from sequential to parallel processing

Sequential processing proved insufficient for large corpora; the redesigned consumer runs a `ThreadPoolExecutor` with tuned worker and in-flight limits (Section B.4, Table 24), with out-of-order completions kept operator-readable by the sequence-ordered output buffer of Fig. 12.

### B.3 Extraction output persistence

Extraction results are saved as individual JSON files, enveloped with traceability metadata (e.g., source file, MIME type, timestamps). The inclusion of the `dedup_candidates` array facilitates subsequent downstream processing or human review.

### B.4 Concurrency and parallelism configuration

Two independent concurrency domains: document-level workers in the Kafka consumer (`ThreadPoolExecutor`) and asynchronous embedding backfill after graph ingestion.

Table 24: Concurrency knobs across the two parallelism domains.

| Domain | Knob | Default → tuned | Rationale |
|---|---|---|---|
| Documents | WORKER_COUNT | 10 → 4 | LLM saturation, OOM on large PDFs |
| Documents | MAX_IN_FLIGHT_TASKS | 40 → 16 | bounds memory; tracks workers |
| Embeddings | EMBED_BATCH_SIZE | 20 | texts per batched API call |
| Embeddings | EMBED_PARALLEL_BATCHES | 5 | concurrent calls (semaphore) |

> "Each worker holds one document's full text plus its extracted entities in memory for the duration of multi-phase extraction; ten concurrent large PDFs exhausted both system memory and the vLLM request queue."

The embedding backfill achieves up to 100 embeddings per round over only five HTTP connections; items that fail within a batch are retried individually via single-item `create()` calls.

## C. Field issue log

Beyond data-quality fixes of the main text; the source-truncation bug is analysed in the main text and omitted here.

### C.1 Issue 2: parallelism-induced resource exhaustion

Ten concurrent workers saturated the local LLM endpoint (request-queuing timeouts) and exhausted memory when several >30-page PDFs were in flight simultaneously. Resolution: reducing WORKER_COUNT to 4 with the in-flight cap following automatically (Section B.4, Table 24).

### C.2 Issue 3: binary PDF routing information loss

The original PDF handling used a single heuristic (`_should_use_text_pdf_path()`) examining overall page statistics (non-empty page ratio, average character count) for a binary text-or-OCR decision for the entire document. A mixed 45-page document with 30 text pages and 15 scanned appendix pages would be routed entirely through one path. Resolution: per-page OCR classification system (Eq. (1), Section 5.1); legacy heuristic retained as fallback only when the classifier reports zero usable pages.

### C.3 Issue 4: vector-drawn text misclassification

Certain PDF pages render text as vector paths rather than font glyphs, reporting zero extractable characters via `get_text("text")` despite readable content. Resolution: drawing count as Signal 5 — pages with more than 200 drawing primitives but zero extractable characters route to the OCR path.

### C.4 Issue 5: xref images missed by block analysis

Some PDFs embed images via cross-reference tables invisible to `get_text("dict")` block analysis, causing scanned-dominated pages to be misclassified as text. Resolution: Signal 3 (xref image coverage via `get_image_info()`), evaluated only when xref images exist (`get_images(full=True)`) to avoid unnecessary computation on text-only pages.

**Covers:** Appendix A (Table 22 threshold reference) through Appendix C (field issues 2–5), operational configuration B.1–B.4 including Tables 23–24
