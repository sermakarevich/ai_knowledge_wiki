> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Query-Conditioned Routing, Dual-View Retrieval, and Deterministic Calibration

**In one sentence:** At query time, Zero-Mem builds a deterministic query profile that weights the relational graph and temporal hierarchy views (via a routing coefficient ρ), retrieves and fuses evidence from both, closes the resulting evidence set with graph bridges and local neighbors, and then deterministically filters, ranks, and calibrates the reader's answer — so that the only LLM call in the whole pipeline is the final-QA reader itself.

## Key points

- Each query is reduced to a lightweight, gold-answer-free profile ϕ(q) = {subject, keywords, answer-type, temporal-cues, boundary}, which is shared by both routing and later evidence selection.
- Routing is binary and deterministic — Route(q) ∈ {relational, local} — decided from query-structure signals (question form, temporal/aggregation requirements, availability of subject anchors), not from a learned or generative judgment.
- Both the graph view and hierarchical view are always executed in full; routing only controls their relative weight during fusion via a globally shared primary-view weight ρ: relational queries get weights ρ (graph) and 1−ρ (hierarchy), local queries reverse these weights.
- Graph retrieval aligns query entities to observed graph entities by embedding similarity, propagates activation through co-occurring sentences, and runs Personalized PageRank over the relational graph to produce a graph-view ranking, refined afterward by exact lexical/phrase matches.
- Hierarchical retrieval is coarse-to-fine (episode → window → turn → local span), scoring units on semantic relevance plus structural compatibility with the query profile (subject, temporal validity, boundary, answer type, lexical support), and expands to local spans only when a selected turn needs surrounding context.
- The two views' rankings are normalized per query onto a comparable scale and fused with the same coefficient ρ into a single Fused Score, after which evidence closure adds graph bridges (Ng) and local neighbors (Nh) to the fused main evidence (M(q)) and deduplicates by shared identifiers/provenance to yield the Closed Evidence Set C(q).
- Deterministic Evidence Calibration is a two-stage, non-generative filter: first Filter/Rank narrow and order C(q) into R(q) using hard provenance/boundary constraints and profile-based compatibility; then, after the reader emits an initial answer a0, Calibrate checks it against extracted evidence-local candidates A(q) and either preserves a0 (if well-formed and supported) or applies evidence-preserving normalization, extractive shortening, or list pruning.
- The final-QA reader is explicitly the only LLM call in the entire Zero-Mem pipeline — routing, retrieval, closure, filtering, ranking, extraction, and calibration are all deterministic, token-free operations performed before and after that single call.

---

## Query-Conditioned Evidence Routing

For each query, Zero-Mem constructs a lightweight profile:

ϕ(q) = {subject, keywords, answer-type, temporal-cues, boundary}. (6)

The subject and keywords act as content anchors, while the answer type and temporal cues characterize the structural requirements of the requested evidence. When available, the boundary specifies the admissible interaction scope. All of these signals come from the query and available metadata — without using gold answers — and are shared by both routing and subsequent evidence selection.

The profile determines which evidence view receives priority:

Route(q) ∈ {relational, local}. (7)

The relational route denotes graph priority, whereas the local route denotes hierarchy priority. The routing decision is based on deterministic query-structure signals: question form, temporal or aggregation requirements, and the availability of subject anchors. Both views are executed in the full model regardless of the routing decision — routing primarily controls their relative weights during fusion.

Let ρ denote the globally shared primary-view weight. Relational queries assign weights ρ and 1 − ρ to the graph and hierarchical views, respectively, while local queries reverse these weights. In other words, ρ / 1−ρ is a damping-style split: whichever view is designated primary by Route(q) gets ρ, and the other gets 1−ρ. Because both views are always computed, the routing decision never discards a view outright — it only reweights how much each view's ranking contributes to the fused score, and this reweighting is what ultimately produces the graph seeds and hierarchical seeds that feed into dual-view retrieval.

## Dual-View Evidence Retrieval and Closure

### Graph evidence propagation (Dual-View Evidence Retrieval, graph side)

The graph view first aligns each entity ê extracted from the query with its most similar observed graph entity e, using dense representations and cosine similarity:

η0(e | q) = cos(e, ê), e = arg max_{e′∈Ve} cos(e′, ê). (8)

Dense context matches provide context priors when aligned entities are available, and serve as a direct fallback ranking when none is detected; lexical and phrase signals refine the resulting context ranking.

Zero-Mem then expands activation from these matched graph entities through relevant co-occurrence sentences. Let Z(e) denote the set of sentences containing entity e. The propagated activation of entity e′ is:

ηt+1(e′) = Σ_{e∈Et} Σ_{z∈Z(e)∩Z(e′)} ηt(e) sim(q, z), (9)

where t is the propagation step, Et is the set of active graph entities at step t (with E0 consisting of the matched entities), and sim(q, z) denotes the dense similarity between query q and sentence z. An entity therefore receives a high score when it co-occurs with an already-activated graph entity in sentences that are relevant to the query.

The propagated entity activations and dense context priors are combined into a query-specific reset vector rq. Personalized PageRank then distributes this evidence over the relational graph:

π q = (1 − γ) rq + γ P⊤ π q, (10)

where π q is the query-conditioned stationary node-score vector, rq is a normalized reset distribution combining propagated entity activations and dense context priors, P is the row-normalized graph transition matrix, and γ ∈ (0, 1) is the damping factor. PageRank values on context nodes form the graph-view ranking. Exact lexical and phrase matches are finally used to refine this ranking for names, dates, values, titles, and quoted expressions.

### Hierarchical evidence retrieval (Dual-View Evidence Retrieval, hierarchy side)

The hierarchical view retrieves evidence through coarse-to-fine search. Each unit is evaluated by jointly considering its semantic relevance to the query and its structural compatibility with the query profile. Compatibility signals include subject consistency, temporal validity, boundary consistency, expected answer type, and lexical or phrase support — these are used to refine the semantic ranking rather than being treated as independently generated evidence.

Retrieval proceeds from episodes to windows and then to individual turns:

Uepisode → Uwindow → Uturn → Ulocal. (11)

Episodes identify relevant event regions, windows narrow the search to local contexts, and turns expose the original evidence. When a selected turn depends on nearby information, its local span is added to preserve the immediate narrative or conversational state. Unlike graph propagation, this view explicitly maintains ordering, temporal locality, and session-level context.

### Score fusion

Zero-Mem first aligns the graph and hierarchical rankings through query-wise score normalization. For each view v ∈ {g, h}:

Ŝv(d) = 0 if d is absent from view v; (Sv(d) − Svmin) / (Svmax − Svmin) if Svmax > Svmin; 1 if Svmax = Svmin. (12)

where Svmin and Svmax are computed over the candidates returned by view v. The normalized rankings are fused using the dual-view routing coefficient ρ:

Sfuse(d) = ρ Ŝprimary(d) + (1 − ρ) Ŝsecondary(d). (13)

The graph view is primary for relational queries, whereas the hierarchical view is primary for local queries — matching the ρ / 1−ρ assignment already established in routing.

### Evidence closure

Let M(q) denote the main evidence retained after fusion. Zero-Mem augments it with bounded, query-conditioned support from the two views:

C(q) = Dedup (M(q) ∪ Ng(M(q)) ∪ Nh(M(q))). (14)

Here, Ng supplies additional graph-ranked contexts with relational or bridging support (Graph Bridges), while Nh restores neighboring turns or local spans (Local Neighbors); either support set may be empty when no addition is required. Duplicates are merged using shared unit identifiers or source provenance when available, yielding the Closed Evidence Set — a compact evidence set with both relational and local support. This closure step is what distinguishes Zero-Mem's evidence set from raw top-K retrieval: it deliberately reintroduces structurally connected evidence (graph bridges) and locally adjacent evidence (local neighbors) that the fused ranking alone might rank below the cutoff, so the reader sees a main-evidence core supplemented with the connective and contextual material needed to support it.

## Deterministic Evidence Calibration

Zero-Mem applies deterministic calibration at both the evidence and answer levels.

### Evidence-level calibration

After evidence closure, it removes candidates that violate provenance or query-boundary constraints and ranks the remaining evidence by subject, temporal, and answer-type compatibility:

R(q) = Rank_ϕ(q) (Filter (C(q), ϕ(q))). (15)

Here, Filter enforces the hard constraints (provenance and query-boundary violations are removed outright), whereas Rank_ϕ(q) orders the admissible evidence according to the query profile without altering its content. The output R(q) is the ranked, filtered evidence (Evidence Top-K) that is handed to the reader.

### Answer-level calibration

The reader produces an initial answer a0 from R(q) — this reader call is the Final-QA Reader, and it is the only LLM invocation anywhere in Zero-Mem's memory operations and answer pipeline. For answer forms admitting deterministic checks, Zero-Mem extracts evidence-local candidates and calibrates the output:

A(q) = Extract (R(q), ϕtype(q)), (16)
a = Calibrate (a0, q, A(q), R(q), ϕ(q)).

Extract pulls type-compatible candidate answers directly out of the ranked evidence R(q), conditioned on the expected answer type ϕtype(q). Calibrate then compares the reader's initial answer a0 against these evidence-grounded candidates, the evidence itself, the query, and the query profile.

Calibration preserves a0 when it is supported and well-formed; otherwise, it applies one of three evidence-preserving corrections:
- **Normalization** — evidence-preserving normalization of the answer's form.
- **Extractive shortening** — trimming the answer to the supported extractive content.
- **Item-wise list pruning** — removing unsupported items from a list-form answer.

A scalar answer is replaced only by a unique type-compatible candidate found in A(q); if no deterministic correction is available, a0 is retained as-is. In short, calibration never invents content — it only preserves, trims, normalizes, or substitutes with evidence that was already extracted from R(q), keeping every operation up to and including this final check token-free except for the single reader call that produced a0.

![Figure 2 (panels 2-4): Query-Conditioned Evidence Routing, Dual-View Evidence Retrieval and Closure, Deterministic Evidence Calibration](images/fig2-zero-mem-architecture.png)

*Figure 2 shows the full 4-panel Zero-Mem architecture; panel 1 (the provenance-preserving memory substrate) is covered by a different wiki page. This page's focus is panels 2-4: query-conditioned routing weights the graph and hierarchical views, dual-view retrieval and closure fuses and completes the evidence, and deterministic calibration filters/ranks the evidence and checks the reader's output — with the final-QA reader as the only LLM call.*

---

**Covers:** Method §Query-Conditioned Evidence Routing, §Dual-View Evidence Retrieval and Closure, §Deterministic Evidence Calibration (pp. 3-5)
