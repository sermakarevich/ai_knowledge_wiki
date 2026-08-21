> [[index|Wiki]] | [[summary|Summary]]

# SodaMem — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-motivation-and-related-work|Motivation & Related Work]]

**In one sentence:** Flat RAG diaries and Markdown logs win needle-in-haystack recall but fail on the four pressures that make long-horizon personal assistants hard—currency/conflict, temporal structure, provenance, and association—so SodaMem reframes memory as an evidence-grounded temporal knowledge graph with supersession edges, mandatory provenance, and a planner–reader answering loop.

- The paper's thesis: LLM agents accompanying users over weeks must remember *what is currently true*, not merely what was once said; flat RAG and Markdown logs "optimize needle retrieval but underserve currency, provenance, and ordered temporal reasoning."
- The field has shifted from "can the model find a needle in the transcript?" to "can the agent maintain a coherent, updatable model of the user (or environment) and use it under the right conditions?"
- Four failure modes (P1–P4) that Markdown/flat RAG leave unresolved: (P1) currency/conflict, (P2) temporal structure, (P3) provenance, (P4) association.
- Motivation's running example: "I love spicy food" → "I am cutting down on spice" → "What should I cook tonight?"—a Markdown log keeps all three and a flat retriever may surface the first; a temporal graph should supersede (or validity-close) the old preference and still cite the justifying turns.
- Six explicit design principles: evidence first, explicit time (mention/occurrence/validity + query window & sort), writable currency as first-class, multi-signal wide recall, connection-density ranking with soft time bonuses, and toolful planner–reader answering.
- Related work is organized in three axes—benchmarks (LoCoMo, LongMemEval), external memory & structure (MemGPT, MemoryBank, Mem0, HippoRAG, Zep), and indexing/conflict/controllers (SimpleMem, RaMem, Memory-R1, AgeMem)—against which SodaMem differentiates on provenance spans, the three temporal axes, write-time supersession, and a cited planner–reader loop.
- Related work also includes "soft time" handling for user misremembering ("two months ago" for a three-month-old fact): hard temporal filters drop the right evidence, so SodaMem parses query time into a soft window + sort direction and treats window match as a ranking bonus.

## 2. [[wiki/02-method-sodamem|Method: SodaMem]]

**In one sentence:** SodaMem is an ingest→store→answer pipeline that turns multi-session dialogue into provenance-checked typed FactEvents in a temporal graph with SUPERSEDES/CONTRADICTS/UPDATES edges and dual BM25/dense indexes, then answers questions via multi-tunnel connection-density retrieval and a planner–reader loop that emits cited, evidence-grounded answers.

- A FactEvent is the atomic record: `f = (κ, π, m, τ, ρ, S, σ)` — kind, predicate, modality, temporal fields, entity roles, source spans (MessagePieces), status (active / superseded / invalid); retrieval units are FactEvents, MessagePieces, or raw turns with stable IDs for fusion.
- An evidence-grounded answer requires each material claim to be supported by retrieved evidence with non-empty provenance spans, and citations must name those records.
- Supersession is write-time and deterministic: "f_new supersedes f_old on a competing subject–predicate slot (or matched update pattern); then σ(f_old) becomes superseded and valid_until(f_old) closes at the effective time of f_new."
- Ingest (Algorithm 1) enforces a provenance hard constraint—candidates whose spans do not literally occur in the source turn are rejected—plus deterministic post-processing (modality normalization, absolute-date resolution, mention-time anchor t_s) and an optional TimelineResolution layer for relative dates.
- The store persists facts in SQLite with dense vectors (MiniLM / GTE-class) and BM25 over fact text, spans, and raw turns; typed edges include SUPERSEDES / CONTRADICTS / UPDATES / DERIVED_FROM plus semantic and relation-type expansion edges; "dreaming" rebuilds dirty entity profiles.
- Retrieval (Algorithm 2) is three-tunnel (graph/entity strong, BM25 strong, embedding weak) with per-head expansion, a hard validity gate, and connection-density fusion: default mass weights strong direct 0.4, weak direct 0.2, strong derived 0.1, weak derived 0.05; near-duplicate merge by ID or embedding similarity ≥ θ (e.g., 0.8); conf(i) = density(i) + β·1[i∩W ≠ ∅] with β default 0.3.
- Answering (Algorithm 3) runs a planner–reader loop: a planner may call memory tools (search, inspect, session expand, timeline, count, compute) under a step budget T_max to grow the fused pool, then a separate reader composes the final answer with mandatory citations.
- Implementation notes: frozen LongMemEval stores open read-only with fingerprint echo; density weights (0.4, 0.2, 0.1, 0.05), β, θ, H, and search-head rerank top K are exposed for Recall@k sweeps.

## 3. [[wiki/03-evaluation-and-results|Evaluation & Results]]

**In one sentence:** On LongMemEval-S SodaMem's store-of-record configuration reaches 92.8% accuracy (464/500; best of N = 3) at a measured mean $0.00161 per question (≈18.3k tokens; median $0.00111 / ≈14.6k) with deepseek-v4-flash, compiling publicly reported systems with estimable API cost into a cost table and cost–accuracy map that place SodaMem near the accuracy frontier at Flash-tier spend, strictly dominating several higher-cost, lower-accuracy public points.

- Evaluation setup: LongMemEval-S (500 questions; ≈115k-token histories) benchmarked via the accuracy–cost trade-off against publicly reported systems with estimable per-question API cost, compiled from disclosed scores, models, and token/$ figures in primary sources rather than re-running every baseline under one harness, converted with 2026 list prices.
- SodaMem run: entity-subject store-of-record (500 users, 235,840 facts); planner, reader, and judge are deepseek-v4-flash with LongMemEval's official yes/no templates; accuracy 464/500 = 92.8% (best of N = 3; median 90.6%).
- Cost: end-to-end planner+reader usage (excluding ingest and judge) at Flash list rates ($0.14 / $0.0028 / $0.28 per 1M for cache-miss / cache-hit input / output) yields a mean of 18,348 tokens/question and $0.00161/question ($1.61 per 10³ Q in Table 1); the median is 14,640 tokens and $0.00111/question ($1.11 per 10³ Q), ≈25% lower—the mean is pulled up by a long tail.
- The same Flash model grades the run (self-grading); absolute accuracy may shift under an independent GPT-4o judge, but released hypotheses support re-evaluation and cost is judge-independent.
- Table 1 (reproduced below) spans 22 methods from agentmemory V4 (96.2%, $60/10³ Q est.) down to MemoryBank (21.0%, $2.21/10³ Q est.); "Est." = priced from disclosed tokens, "Meas." = author-reported / measured USD.
- Result analysis: the dominated quadrant—cost > mean $0.00161 and accuracy < 92.8%—contains Cersei Embed / Hybrid / Full-context, AgentOS, long-context GPT-5-mini, EmergenceMem Simple Fast, and MemoryBank under TiMem (strictly worse cost/accuracy pairs even against SodaMem's mean); under the median ($0.00111), MemoryOS and Fact-Mem0 read would enter as well.
- Public accuracy jumps often track reader upgrades (e.g., Mastra 84.23% → 94.87% from GPT-4o to GPT-5-mini); SodaMem's claim is near-frontier accuracy at Flash-tier spend, undercutting Opus/GPT-4o high-score systems by ≈10–40× in estimated $/question.
- Limitations: single store-of-record configuration under Flash self-grading; no unified re-run of all baselines; peer costs are order-of-magnitude reconstructions; ingest-time spend and timeline-resolution ablations left for follow-up.

## The argument in five moves

1. Long-horizon personal agents fail not on recall but on currency, ordering, provenance, and association — flat RAG/Markdown logs leave these unresolved (P1–P4).
2. Treat memory as an evidence-grounded temporal knowledge graph: typed FactEvents with mandatory source spans and three temporal axes (mention, occurrence, validity).
3. Make currency structural: write-time SUPERSEDES/CONTRADICTS/UPDATES edges close out stale facts deterministically instead of leaving freshness judgment to the reader.
4. Retrieve by connection density across three tunnels (graph, BM25, embedding) with a soft time bonus, not a hard temporal filter — so misremembered dates don't drop the right evidence.
5. Separate planning from answering: a tool-using planner grows the evidence pool, a separate reader writes the cited answer — and on LongMemEval-S this lands at 92.8% accuracy for $0.00161/question, near the frontier at a fraction of the cost of Opus/GPT-4o-tier competitors.
