> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method: SodaMem

**In one sentence:** SodaMem is an ingest→store→answer pipeline that turns multi-session dialogue into provenance-checked typed FactEvents in a temporal graph with SUPERSEDES/CONTRADICTS/UPDATES edges and dual BM25/dense indexes, then answers questions via multi-tunnel connection-density retrieval and a planner–reader loop that emits cited, evidence-grounded answers.

## Key points

- A FactEvent is the atomic record: `f = (κ, π, m, τ, ρ, S, σ)` — kind, predicate, modality, temporal fields, entity roles, source spans (MessagePieces), status (active / superseded / invalid); retrieval units are FactEvents, MessagePieces, or raw turns with stable IDs for fusion.
- An evidence-grounded answer requires each material claim to be supported by retrieved evidence with non-empty provenance spans, and citations must name those records.
- Supersession is write-time and deterministic: "f_new supersedes f_old on a competing subject–predicate slot (or matched update pattern); then σ(f_old) becomes superseded and valid_until(f_old) closes at the effective time of f_new."
- Ingest (Algorithm 1) enforces a provenance hard constraint—candidates whose spans do not literally occur in the source turn are rejected—plus deterministic post-processing (modality normalization, absolute-date resolution, mention-time anchor t_s) and an optional TimelineResolution layer for relative dates.
- The store persists facts in SQLite with dense vectors (MiniLM / GTE-class) and BM25 over fact text, spans, and raw turns; typed edges include SUPERSEDES / CONTRADICTS / UPDATES / DERIVED_FROM plus semantic and relation-type expansion edges; "dreaming" rebuilds dirty entity profiles.
- Retrieval (Algorithm 2) is three-tunnel (graph/entity strong, BM25 strong, embedding weak) with per-head expansion, a hard validity gate, and connection-density fusion: default mass weights strong direct 0.4, weak direct 0.2, strong derived 0.1, weak derived 0.05; near-duplicate merge by ID or embedding similarity ≥ θ (e.g., 0.8); conf(i) = density(i) + β·1[i∩W ≠ ∅] with β default 0.3.
- Answering (Algorithm 3) runs a planner–reader loop: a planner may call memory tools (search, inspect, session expand, timeline, count, compute) under a step budget T_max to grow the fused pool, then a separate reader composes the final answer with mandatory citations.
- Implementation notes: frozen LongMemEval stores open read-only with fingerprint echo; density weights (0.4, 0.2, 0.1, 0.05), β, θ, H, and search-head rerank top K are exposed for Recall@k sweeps.

---

## Preliminaries

**Definition 0.1 (FactEvent).** A FactEvent is f = (κ, π, m, τ, ρ, S, σ): kind κ, predicate π, modality m, temporal fields τ, entity roles ρ, source spans S (MessagePieces), and status σ (active / superseded / invalid). Retrieval units are FactEvents, MessagePieces, or raw turns (stable IDs for fusion). Temporal axes: mention (session time t_s), occurrence (occurred start/end), and validity (valid_from / valid_until), closed under supersession.

**Definition 0.2 (Evidence-grounded answer).** Answer a is evidence-grounded if each material claim is supported by retrieved E ⊆ M with non-empty provenance S(f) for f ∈ E, and citations name those records.

**Definition 0.3 (Supersession).** f_new supersedes f_old on a competing subject–predicate slot (or matched update pattern); then σ(f_old) becomes superseded and valid_until(f_old) closes at the effective time of f_new.

**Definition 0.4 (Query temporal intent).** A parser maps q to (W, δ): window W and sort δ ∈ {near→far, far→near}. Absent cues, W = ∅ and δ = near→far.

## Problem Statement

Given a user u, multi-session dialogue history H_u = {H_s}^S_{s=1} with session times {t_s}, and question q, produce an evidence-grounded answer a maximizing judge agreement with gold a★. The system factors as:

- M_u = Ingest(H_u) (1)
- E = Retrieve(q, M_u) (2)
- a = Read(q, E) (3)

SodaMem specifies Ingest, the schema of M_u, Retrieve (multi-signal recall + density fusion + optional planner tools), and Read.

SodaMem is a memory infrastructure for LLM agents comprising ingest, durable storage with hybrid multi-signal retrieval, optional maintenance (dream / timeline resolution), and a planner–reader answering loop. Relative to Markdown diaries and flat RAG, the design goal is a maintainable user knowledge state that remains citable—and a retrieval stack that ranks evidence by connection density across graph, lexical, and dense channels under soft temporal scoring.

![SodaMem architecture overview](images/fig1-overview.png)

The diagram lays the system out as a left-to-right pipeline of three panels—**Ingest**, **Temporal Graph Store**, and **Answer**—under the banner goal "evidence-grounded temporal graph memory." On the left, multi-session dialogue flows top-to-bottom through an LLM-based FactEvent extractor, a provenance check, and an optional timeline-resolve step, producing typed FactEvents with source spans. The middle panel holds the store's three components: FactEvent nodes carrying `kind / predicate / time / validity` fields (the figure's sample node shows `kind=Event`, `predicate=visited`, `time≈2024-05-12T10:15Z`, `validity≈[2024-05-12, ∞)`, `source≈doc42:12-18` as illustrative values); typed directed edges in four distinct styles—SUPERSEDES (black solid), CONTRADICTS (red dashed), UPDATES (green solid), DERIVED_FROM (purple dashed); and dual indexes, a BM25 lexical/sparse index alongside a dense-vector semantic index. On the right, the answer side runs hybrid retrieve → planner with memory tools (`search`, `inspect`, `timeline`) → reader with citations → final answer. This is exactly the ingest→store→answer pipeline formalized below.

## Ingest: From Turns to FactEvents

### Segmentation and extraction

For each session H_s with time t_s, turns are segmented and passed to an extractor LLM that emits FactEvent candidates under a fixed schema: kind, predicates, modality, temporal expressions, entity roles, source span ids, and support text. Candidates must name spans that literally occur in the source turn (MessagePieces).

### Provenance hard constraint

Candidates whose spans do not land in the source turn are rejected. Raw turns keep stable rawTurn ids so later BM25/embedding hits can carry full turn text for similarity, deduplication, and density accounting.

### Deterministic post-processing

Post-steps normalize modality, resolve absolute dates when stated, and attach t_s as the mention-time anchor. Optional coarse and entity-subject prompts control granularity and reduce star-graph collapse onto entity user.

### Timeline Resolution Layer

Relative phrases at ingest are under-specified if left only as text. We optionally apply

    τ̂(f) = T(τ_raw(f), t_s(f), context(f)),   (4)

producing comparable timestamps. Unresolvable cases are marked unresolved. At query time, a separate parser yields temporal intent (W, δ) used in soft temporal scoring—aligned with bi-temporal / episodic concerns (Rasmussen et al. 2025; Yang et al. 2026), but coupled to density fusion rather than hard episode filters alone.

### Algorithm 1: IngestSession(H_s, t_s)

1. C ← ExtractLLM(H_s)
2. F ← ∅
3. for each candidate c ∈ C do
4.   if SpansValid(c, H_s) then
5.     c ← NormalizeModalityAndDates(c, t_s)
6.     F ← F ∪ {c}
7.   end if
8. end for
9. F ← TimelineResolve(F, t_s) {optional}
10. WriteFactsAndEdges(F)
11. return F

## Store: Hybrid Index and Graph Relations

**Persistence.** Facts persist in SQLite with dense vectors (MiniLM / GTE-class) and BM25 over fact text, spans, and raw turns. Cards expose predicate text, temporal fields, entity roles, status, and provenance.

**Edges.** We maintain:

- mention / DERIVED_FROM links to spans;
- SUPERSEDES / CONTRADICTS / UPDATES among facts;
- graph expansion edges of two flavors used at retrieve time: **semantic edges** (content-driven neighbor links) and **relation-type edges** (typed predicates between entities).

Product defaults write supersession; observe-only frozen stores are an experimental axis. Dreaming rebuilds dirty entity profiles.

## Retrieve: Multi-Tunnel Recall and Connection-Density Fusion

Retrieval is the core of Retrieve(q, M_u) and follows the initial SodaMem design: wide multi-path recall, per-tunnel head expansion, validity gates, then fusion by connection density with soft time bonuses.

### Query analysis

Parse q into entity mentions, lexical keys, an embedding query, and temporal intent (W, δ). Vague cues ("recently", "a few months ago") are mapped to wide windows to prefer recall over precision; missing cues disable the time bonus rather than inventing a window.

### Three tunnels (strong vs. weak)

- **Graph / entity tunnel (strong):** hit entities or facts as search heads; expand along selected semantic or relation-type edges (1-hop or limited multi-hop). Each head expands independently, then applies validity, relevance, and soft time scoring; keep search head rerank top K.
- **BM25 tunnel (strong):** lexical hits on facts, MessagePieces, or raw turns. Span hits attach neighboring spans and the parent rawTurn (full text as a field for similarity/dedup); raw-turn hits expand to temporally adjacent turns (±2) for local context.
- **Embedding tunnel (weak):** dense neighbors with the same expansion patterns as BM25, but lower base weights because similarity may retrieve related-but-irrelevant episodes.

Each tunnel uses at most H search heads (default H=10). Direct hits from strong tunnels receive higher base mass than weak-tunnel or derived (expanded) hits.

### Validity gate (hard)

Exclude content whose status is invalid/superseded-as-inactive when inappropriate, or whose validity interval is incompatible with W when a window is stated and the fact's validity is known. This is the **only** hard temporal/status exclusion; occurrence-time mismatch alone does not drop a high-density candidate.

### Connection density and ranking confidence

Let each (tunnel, head, hit) award a mass w to an evidence ID i (fact / span / rawTurn). Defaults (tunable): strong direct 0.4, weak direct 0.2, strong derived 0.1, weak derived 0.05. Masses accumulate when multiple heads hit the same ID (by ID equality, or by embedding similarity ≥ θ, e.g., 0.8, for near-duplicate merge). Writing H(i) for the hits on i:

    density(i) = Σ_{h∈H(i)} w_h,                          (5)

    conf(i) = density(i) + β · 1[i ∩ W ≠ ∅],               (6)

with time bonus β (default 0.3) awarded at most once per merged item if any constituent falls in W. Sort by conf (ties broken by δ). Time thus acts as a ranking feature rather than a hard filter, so user-misdated queries remain recoverable.

### Fusion

Merge per-tunnel lists by ID/similarity, recompute conf, and emit a unique ranked pool (Recall@k cutoffs are experimental knobs).

### Algorithm 2: MultiTunnelRetrieve(q, M_u)

1. (W, δ) ← ParseTemporal(q)
2. pools ← ∅
3. for tunnel t ∈ {graph, BM25, embed} do
4.   heads ← TopHeads(t, q, M_u; H)
5.   for head h ∈ heads do
6.     L ← Expand(h, t); L ← ValidityFilter(L, W)
7.     L ← RerankLocal(L, q, W, δ; top K)
8.     pools ← pools ∪ AwardMass(L, t)
9.   end for
10. end for
11. E ← MergeByIdOrSim(pools; θ); score conf on E
12. return top evidence by conf under δ

## Answer: Planner–Reader Loop

**Planner.** An LLM may further call tools (search, inspect, session expand, timeline, count, compute) under a step budget to grow the fused pool—implementing memory-in-the-loop (Memory in the Loop 2026) when density ranking alone is insufficient (e.g., explicit enumeration).

**Reader.** A separate prompt composes the user-facing answer from selected evidence IDs with mandatory citations. Separation keeps citation discipline out of the tool policy.

### Algorithm 3: Answer(q, M_u)

1. E ← MultiTunnelRetrieve(q, M_u)
2. open ← {q}
3. for t = 1 to T_max do
4.   act ← Planner(q, E, open)
5.   if act = STOP then
6.     break
7.   end if
8.   E ← E ∪ ExecTool(act, M_u)
9. end for
10. a ← Reader(q, E)
11. return a with citations into E

## Implementation Notes

Frozen LongMemEval stores open read-only with fingerprint echo. Density weights (0.4, 0.2, 0.1, 0.05), β, θ, H, and search head rerank top K are exposed for Recall@k sweeps.

**Covers:** Preliminaries (Definitions 0.1–0.4), Problem Statement, proposed method (Ingest / Algorithm 1 with provenance hard constraint and timeline resolution layer; Store with hybrid index and typed edges SUPERSEDES/CONTRADICTS/UPDATES/DERIVED_FROM; Retrieve / Algorithm 2 with three tunnels, connection-density fusion, validity gate; Answer / Algorithm 3 planner–reader loop; Implementation Notes), Figure 1.
