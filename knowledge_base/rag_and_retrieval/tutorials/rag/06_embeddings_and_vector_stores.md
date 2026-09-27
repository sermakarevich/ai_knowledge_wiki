# 06 — Embeddings & Vector Stores

## What you will learn

- Which of the 7 embedding models we run is the best **retrieval** model on our 23-question set, and *why* recall@5 and MRR can disagree.
- Explain why an embedding model outputs a **fixed-size vector** and where that constraint comes from.
- Cut the dimensions of your vectors (Matryoshka) with **measurable** loss — and quantify the cost.
- Apply three quantization schemes in Qdrant, and read what happens to recall when you do.
- Tune HNSW (Hierarchical Navigable Small World) (`m`, `ef_construct`, `ef_search`) and see the latency vs. recall trade-off for **real** numbers.
- Pick one of five vector stores (Chroma, FAISS, LanceDB, pgvector, Qdrant) for a use-case with a clear reason.

---

## What changed on the scoreboard

Chapter 06 is **retrieval-only**. Every benchmark above scores a dense-retrieval head-to-head on the 23-question eval set. It does not add rows to the `scoreboard.md` that chapters 02–05 filled — those rows measured *the full pipeline* (chunk → retrieve → generate → judge). Here the LLM (Large Language Model) is not in the loop, because it is irrelevant to the question we are asking: *how well do different models, dimensions, quantization, and stores rank the right chunks to the top?*

The best **retrieval** numbers on the leaderboard are still the hybrid RRF (Reciprocal Rank Fusion) and BM25 (Best Matching 25) runs from ch.05 (recall@5 ≈ 0.41–0.49 with the hybrid pipeline). This chapter does not chase those numbers — it asks different questions.

---

## 1. Embeddings: what they are and how to measure them

A sentence is a sequence of tokens. A **vector model** maps that sequence to a fixed-length list of floating-point numbers — e.g. 768 or 1,024 floats. Two sentences that mean the same thing land close together in that space; two that don't, land far apart.

We use **cosine similarity** (dot product on normalized vectors) for the rest of this chapter. It's scale-invariant and matches the geometry of most sentence-embedding models.

### Metrics (the ones that matter)

- **hit@k** — *fraction of queries whose relevant chunk appears in the top-k*. Easy to reason about: "50% of the time, the right chunk is in the top 5."
- **recall@k** — *fraction of all relevant chunks for a query that appear in the top-k*. For most questions in our set, exactly one chunk is the correct one, so on this corpus recall@5 ≈ hit@5. On a different corpus they can diverge.
- **MRR** *(mean reciprocal rank)* — *average of 1/rank of the first correct chunk*. "Was the first result correct? That's worth 1. The second? Worth 0.5. The fourth? Worth 0.25."
- **nDCG@k** (normalized Discounted Cumulative Gain) — *grade-weighted, position-sensitive*. For our data it's the least informative because every correct chunk has the same label.

### Why recall@5 ≈ hit@5 on our eval set, and why that's fine

We picked a 23-question set where each question has a **single** golden chunk. That's a fair simplification for the purpose of *ranking* models against each other. For real RAG (Retrieval-Augmented Generation) systems, you'll usually want a set with **multiple relevant chunks per question** — the metric that will bite you then is recall@k.

---

## 2. Seven models, one eval set — a table

All models ran through the same `Ollama` stack, same corpus (1,942 chunks), same 23 questions, same cosine distance, `k=5`.

| Model | Params | Dim | Disk (MB) | hit@5 | recall@5 | MRR | nDCG@5 |
|---|---|---|---:|---:|---:|---:|---:|
| **snowflake-arctic-embed2:568m** | 566.7 M | 1024 | 1107 | 0.565 | **0.428** | **0.393** | 0.424 |
| **bge-m3:567m** | 566.7 M | 1024 | 1104 | **0.609** | 0.415 | 0.377 | **0.432** |
| **embeddinggemma:300m** | 307.6 M | 768 | 593 | 0.478 | 0.370 | 0.370 | 0.393 |
| **nomic-embed-text** | n/a | 768 | n/a | 0.391 | 0.283 | 0.239 | 0.278 |
| **mxbai-embed-large:335m** | 334 M | 1024 | 639 | 0.391 | 0.297 | 0.312 | 0.325 |
| **qwen3-embedding:0.6b** | 595.8 M | 1024 | 610 | 0.348 | 0.261 | 0.208 | 0.242 |
| **all-minilm:22m** | 23 M | 384 | 44 | 0.261 | 0.196 | 0.168 | 0.187 |

### How to read this

- **Snowflake-arctic** wins on MRR and recall (0.393 / 0.428); **bge-m3** wins on hit@5 (0.609) and nDCG (0.432). On our set they're very close — the gap between MRR and hit@5 for bge-m3 is telling: bge-m3 finds the right chunk more often, but *less often in position 1* than snowflake.
- **Snowflake is the right default for this corpus** if you want one strong model. bge-m3 is the right one if you can *also* keep it in a hybrid with BM25 (which ch.05 already showed helps).
- **nomic-embed-text** is the weakest "big" model on this set, but it's the one we'll use in the rest of this chapter because it is the reference model for the Matryoshka and quantization experiments below.
- **all-minilm (23 M, 384-d)** is the smallest model — 44 MB on disk. It ranks a 5th-from-bottom in recall (0.196). This is the model to reach for on a Raspberry Pi or an edge device; it is *not* the model to reach for when you need the best top-1.
- **mxbai, qwen3, embeddinggemma** are all in the mid-band. None is close enough to the top 2 to change a default.

### What "fast" really means here

The `chunks_per_sec` column in the raw run is not a fair speed measure — it depends heavily on whether the model was already in memory, and on the host. Treat it only as a rough ordering. On this host the three 560–590 MB-class models ran at ~7 chunks/s, the two ~610 MB-class models at ~5–22 chunks/s, and miniLM at ~42 chunks/s (23 M, 384-d). That ordering is roughly consistent: *smaller model → faster, but also less recall*.

**Rule of thumb:** a one-time indexing pass over a corpus is a **minutes-scale** job for a 500 MB model on a consumer laptop/GPU — not a blocker in production. If you're re-embedding the whole corpus every time, you'll be fighting your own hardware; you should either cache the vectors or switch to a smaller model.

---

## 3. Matryoshka embeddings — cut the dimensions, keep most of the recall

**Matryoshka embeddings** are a training technique where a model is trained so that *any prefix of the vector is itself a valid, lower-dimensional embedding* (like matryoshka dolls — each smaller one is a full embedding on its own). The model `nomic-embed-text` supports it: 768-d, 512-d, 256-d, 128-d all come from the **same** full 768-d vector by truncation.

We measured the cost:

| Dim | hit@5 | recall@5 | MRR | nDCG@5 |
|---:|---:|---:|---:|---:|
| 768 | 0.391 | 0.283 | 0.239 | 0.278 |
| 512 | 0.391 | 0.283 | **0.232** | 0.274 |
| 256 | 0.348 | 0.261 | 0.233 | 0.262 |
| 128 | 0.261 | 0.196 | 0.185 | 0.204 |

### How to read this

- **768 → 512: free.** Recall@5 is literally *identical* (0.283). Hit@5 identical. MRR drops by only 0.7 points. You cut the vector size by **33%** — same recall.
- **512 → 256:** recall drops **0.022** (about 8% relative). Hit@5 drops 0.043.
- **256 → 128:** recall drops another **0.065** — 128-d is the *painful* cut.

### Why a free 33%?

Two small things: (1) cosine similarity on the first 512-dim components is, for this model, a near-perfect proxy for the full 768-dim version on this corpus. (2) The eval set is a *ranking* of 1,942 chunks — so a single correct chunk being top-5 is a hard event, not a soft one. If the top-512-dim version already puts the right chunk in the top 5, the extra 256-dim of tail signal is only noise.

**Practical read:** if you can use Matryoshka (nomic, bge-m3, snowflake-arctic, GTE — see the Ollama catalog), try the **512-dim** truncation first. If recall is close (within 1–2 points), keep it. If not, go to full.

---

## 4. Quantization — less RAM, same or better retrieval

Qdrant supports four distance-preserving schemes. We built the same 1,942-chunk × 768-d index in each, and measured **RAM used by the vectors** (analytic estimate, because Qdrant 1.19 has no per-collection RAM API) and **recall@5** on the same 23 questions.

| Scheme | RAM (vectors only) | recall@5 |
|---|---:|---:|
| `float32` (baseline) | 5.689 MB | 0.283 |
| `scalar_int8` | 1.422 MB (−75%) | 0.283 |
| `product_x64` (PQ) | 0.024 MB (−99.6%) | 0.283 |
| `binary` (1 bit/vector) | 0.178 MB | **0.326** ⬆ |

### How to read this

- `scalar_int8`, `product_x64`, and `binary` all **preserved or improved** recall@5 on this corpus. This is the honest headline: on this corpus, quantization is a *free* or *slightly positive* win.
- The `binary` recall is **higher than float**. Why? Binary vectors use a dot-product approximation that — on a corpus with strong topical separation — can *separate the top-5 chunks more sharply*. That's a **corpus-specific artifact**, not a general law. Do not extrapolate.
- `product_x64` cuts RAM by ~99.6% — a 5.7 MB vector index becomes 24 KB — with zero measurable recall loss. For a corpus this size, this is *the* scheme to use.

**Rule of thumb (honest version):** for a corpus up to **1 M chunks**, `scalar_int8` is a safe choice. `product_x64` is *usually* fine and is the biggest RAM win. `binary` is a specialty — great for some retrieval shapes, and it can *hurt* when the correct-answer signal is in the fine-grained low-magnitude part of the vector. Re-run the eval on **your** data before you commit.

---

## 5. HNSW — how you actually store and search vectors in production

Brute-force search ("compute the cosine to *every* vector in the corpus and take the top-k") is O(n) and gets slow. HNSW is the standard fast alternative: a multi-layer graph where each node points only to the *k* (typically 16) nearest neighbors it knows about. Search climbs the levels from the top (rough) down to level 0 (fine), and at each step explores a **beam** of candidates.

```
                 Level 2   ┌───(few nodes, large jumps)───┐
                 Level 1   │     more nodes, medium       │
                 Level 0   │     most nodes, finest       │
        query ──►    ...          nearest neighbors        ...  ──► top-k
```

### Three knobs

| Knob | What it tunes | Where you pay |
|---|---|---|
| `m` | **number of neighbors each node connects to** (at any level). More → better recall, *but* more RAM and a slower build. Set **once** at build time. | RAM + build time |
| `ef_construct` | **how hard the build algorithm searches** when deciding which `m` neighbors to keep. Higher → better initial graph, *slower build*. Set **once** at build time. Indexes built with low `ef_construct` are harder to fix later than they should be. | Build time only |
| `ef_search` | **beam width at query time**: how many candidates the search explores simultaneously. Higher → better recall, **slower per query**. Tuneable at runtime. | Query latency |

On a small corpus (1,942 chunks), all 18 configs in our sweep (m ∈ {8,16,32}; ef_construct ∈ {100,200}; ef_search ∈ {16,64,256}) hit **recall_vs_exact = 1.0** — HNSW found every single correct chunk that an exact search would have found, at all 18 parameter pairs.

**Mean latency** per 23 queries:

| | mean ms |
|---|---:|
| Qdrant (HNSW, m=16, ef_s=64) | **2.78** |
| numpy dot-product (exact, 1,942 × 768) | **0.065** |

**Interpretation:** on this corpus, the HNSW overhead over exact is **~40×**. At 2.8 ms per query, HNSW adds ~2.7 ms per query on top of a 0.065 ms exact search. That overhead will be **negligible** at 10k or 100k chunks (where exact search becomes 65–650 ms), and **noticeable** at 2k chunks. **This is why HNSW exists: its cost is fixed per query, while exact-search cost grows with corpus size.**

On larger corpora, the same `m`/`ef_construct`/`ef_search` values will give you **lower recall** than 1.0 because (a) the graph is more ambiguous — each node has more candidates at each step, and (b) the beam-width trade-off becomes real: a fixed `ef_search` covers a *smaller fraction* of the graph. **You will need to bump `ef_search` higher** to match the recall you got here — at the cost of a higher per-query latency. That is the core of HNSW tuning.

**Default we use in this series:** `m=16`, `ef_construct=100`, `ef_search=64`. If you're starting from scratch, that's the place to begin — it sits in the middle of all the swept values.

---

## 6. Five vector stores, one query, one corpus

We built the same 1,942 × 768-d index in **Chroma, FAISS, LanceDB, pgvector, and Qdrant**, then ran the same 23 queries with `k=5` on each. **Recall was 0.283 on every store** — with the same embeddings, same k, same distance, the ranking is *identical*. What differs is the *engineering* around it:

| Store | Build (s) | p50 (ms) | p95 (ms) | QPS (23 queries) | Disk (MB) |
|---|---:|---:|---:|---:|---:|
| **FAISS** | 0.045 | **0.12** | **0.13** | **8152** | 7.6 |
| **Chroma** | 0.737 | 0.83 | 0.95 | 1226 | 34.6 |
| **pgvector** | 3.063 | 1.12 | 2.30 | 752 | 25.8 |
| **Qdrant** | 0.853 | 1.99 | 3.26 | 446 | n/a* |
| **LanceDB** | 0.102 | 2.27 | 2.81 | 437 | 6.8 |

\* Qdrant 1.19 has no per-collection on-disk size API; we leave it blank rather than guess.

### How to read the numbers

- **All five stores return the same top-5.** Recall is identical (0.283). The differentiator is not precision — it's everything *around* the search.
- **FAISS** is the fastest (0.12 ms p50, 8,152 QPS) and uses the least disk (7.6 MB). It's an **in-memory** library — there is no persistent backend. You'd have to serialize/deserialize the index yourself, and it doesn't give you metadata filters, hybrid search, or a SQL layer.
- **Chroma** is the middle of the pack on latency (0.83 ms p50) and sits at 34.6 MB on disk. It's a *client* that wraps an embedded store — for small-to-medium corpora it's "just works" without any service.
- **pgvector** is the SQL layer on top of PostgreSQL. 1.12 ms p50, 752 QPS, 25.8 MB. The build time is the longest (3.1 s) because of the index build *inside* Postgres, but that's a one-time cost.
- **LanceDB** is the lowest-latency *persistent* store in our test besides FAISS (2.27 ms p50, 6.8 MB on disk).
- **Qdrant** is 1.99 ms p50, 446 QPS — slower in absolute terms on this small corpus, but it gives you the **most features**: native hybrid (BM25 + vector) search, multi-tenant collections, filters, and the best quantization story from §4.

### Which store when (a practical rule)

- **Small corpus, fast query, no filters, already has Postgres** → **pgvector**.
- **Small corpus, fastest query, no persistence** → **FAISS**.
- **Small corpus, "just works," need to persist** → **Chroma**.
- **Large corpus + filters + hybrid + quantization** → **Qdrant**.
- **Large corpus, SQL-friendly, low latency required** → **LanceDB**.

None of the above is wrong for our 1,942-chunk corpus. The differences above all become invisible at that scale — *pick the store whose *other* features fit the rest of your stack and move on*; that's the real takeaway.

### Advantages and disadvantages of each store

**FAISS**
- *Advantages:* fastest query (0.12 ms p50, 8,152 QPS); lowest disk (7.6 MB); the most mature ANN (Approximate Nearest Neighbour) library; a full suite of index types (IVF, HNSW, PQ, OPQ).
- *Disadvantages:* **in-memory only** — no persistence, no metadata, no filters, no hybrid search; you own serialization and scaling yourself; no multi-tenant; you'll end up wrapping it in a server of your own.

**Chroma**
- *Advantages:* client-side "just works"; a small API surface that *is* the whole feature list; good for notebooks and small apps; in-process, so no server to run.
- *Disadvantages:* an embedded store, so it scales only to the host that runs it; fewer index options than FAISS/Qdrant; no native BM25 (you bring your own).

**LanceDB**
- *Advantages:* fastest *persistent* store in our bench besides FAISS (2.27 ms p50, 6.8 MB disk); columnar storage built for large corpora; supports filters.
- *Disadvantages:* newer, smaller ecosystem; less battle-tested than pgvector for SQL-heavy workloads; quantization story is thinner than Qdrant's.

**pgvector**
- *Advantages:* you keep the data in **Postgres** alongside the rest of your app — one DB, one backup, one auth model; real SQL (JOINs, filters, transactions) over the vectors; the most "standard" choice.
- *Disadvantages:* slowest build (3.1 s) because of the on-disk HNSW index; no native hybrid (BM25 + vector) without extra SQL; you are on the hook for Postgres tuning (`maintenance_work_mem`, `effective_cache_size`, …).

**Qdrant**
- *Advantages:* most features (native hybrid BM25 + vector, multi-tenant collections, rich payload filters, the best quantization story of the five, a real multi-node cluster); the best developer experience for a *dedicated* search service.
- *Disadvantages:* a **server** to run (Docker, networking, auth, upgrades); slower p50 than FAISS/Chroma on this small corpus (1.99 ms vs 0.12 ms) — a protocol cost, not an algorithm one; no SQL layer (you query via its own API).

---

## 7. What to do with all of this

The decision ladder:

1. **Pick an embedding model from §2** (recommend **snowflake-arctic-embed2** for top-1 / MRR on this kind of corpus; **bge-m3** if you can afford the extra disk and you want the best hit@5).
2. **If your model supports Matryoshka (§3) and you want less RAM/disk**, truncate to 512-d and re-run your eval.
3. **Quantize with `product_x64` (§4)** for the biggest RAM/disk win with the least risk.
4. **Default HNSW parameters: `m=16`, `ef_construct=100`, `ef_search=64` (§5)**.
5. **Pick the vector store that fits your rest-of-stack (§6)** — FAISS, Chroma, pgvector, Qdrant, or LanceDB, in that order of "how far you need to be from a database."

---

## 8. What changed on the scoreboard

**Nothing changed on the `scoreboard.md`** — chapter 06 is retrieval-only, and `scoreboard.md` tracks full-pipeline experiments (ch.02–05). The numbers in this chapter are a *separate* retrieval leaderboard (in the `06_*` JSON files) that feeds the decisions in chapters 07 (reranking) and 11 (evaluation).

What this chapter *does* add to the leaderboard is one **retrieval** data point per (model, dim, quant, store) slice — 7 × 4 × 4 × 5 ≈ ~60 slices worth of recall@5, of which a representative subset is surfaced in the tables above.

---

## 9. Troubleshooting

**"Model won't pull / OOM at download time"**
- The 560–590 MB models (snowflake-arctic, bge-m3) are the largest. Make sure your local Ollama has at least ~1.5 GB of free disk before the pull, and ~3 GB of RAM at inference.
- If you're running on a laptop with 8 GB RAM, `bge-m3` (567 M, 1024-d) and `snowflake-arctic` (568 M, 1024-d) will **fight your OS** for RAM. Stick with `embeddinggemma` (300 M) or `nomic` for a smooth dev loop on that machine.

**"My vectors are the wrong dimension"**
- `nomic-embed-text` outputs 768-d. `bge-m3` outputs 1024-d. `all-minilm` outputs 384-d. **You cannot change the dimension of a model at runtime** — each model has a fixed output size. Matryoshka truncation (§3) is the *only* legitimate way to reduce dimension *after the fact*.
- If you've stored 1,000 vectors from model A and now switch to model B (a different dim), you'll get an **error** on store insertion or query. **Delete the old collection** before loading a new model.
- If you're using `product_x64` or Matryoshka truncation on a *non-Matryoshka* model, the low dimensions will **not** correspond to a valid embedding — you'll silently get worse recall without any error.

**"pgvector is 3× slower to build than Chroma"**
- That's the index build cost on disk. For a corpus of 1,942 chunks it's 3 s — one-time. For a corpus of 1 M chunks it's much more. **Pre-build the collection once and reuse it**; don't rebuild on every test run.

**"Recall dropped after I changed the quantization"**
- On *this* corpus, quantization didn't drop recall (§4). If it **did** drop recall on *your* data, that's a corpus-specific effect (see §4, last paragraph). **Turn quantization off and re-measure**. Don't assume the quantization is the problem — it might be your eval set.

**"FAISS is 8,000 QPS, why is Qdrant 446?"**
- FAISS is **in-memory only**. Qdrant is a **server**: there's a network call. On this corpus the difference is *the protocol*, not the algorithm. At 10 M chunks, the QPS gap between FAISS and Qdrant shrinks a lot, because the algorithm (HNSW) becomes the bottleneck, not the network.

**"My nomic-embed-text index is *faster* than I expect"**
- The `chunks_per_sec = 13,430` you're seeing in `06_embedding_models.json` is the **cached-in-RAM** number for a single 60-chunk batch. On a cold start (model loading from disk), the same batch takes ~30 s. The cached number is not a *fair* speed metric.

**"Matryoshka says 'free' but my latency is different"**
- Matryoshka truncation is a **free** cut in *storage and RAM*; it is **not** free in *compute*. A 512-d vector is still 512 floats to dot-product at query time. You save **33% of the search cost**, not 100%.

**"HNSW `recall_vs_exact` is 1.0 — are we done tuning?"**
- **No.** 1.0 is a *floor*, not a ceiling. The corpus is small (1,942 chunks). At that size, the graph is nearly complete, so HNSW finds everything exact-search finds. At 1 M chunks, the same parameters will give a **lower** recall. You'll need to re-tune `ef_search` **higher** to match.

---

## 10. Exercises

1. **Re-run the embedding head-to-head with `k=10`** instead of `k=5`. You'll need to re-score, since `hit@10 = "did the golden chunk appear in the top 10?"` — this will *change* the ranking. Which model wins on `k=10`? (Expected: **bge-m3** should gain, **snowflake-arctic** should stay close — the *spread* of positions in the top-5 is what's making bge-m3 win on hit@5 today.)

2. **Quantize the `nomic-embed-text` index with `binary`** and measure recall@5 on a **different** corpus (e.g., a 500-chunk corpus from a non-technical document set). If binary recall *drops* on your corpus, that's the corpus-specific artifact from §4 — write a 3-line explanation of *why*.

3. **Sweep `ef_search` from 16 → 512** on a Qdrant index, plotting the mean query latency and the recall@5. Report the **elbow** point (where each additional 32 units of `ef_search` buys you less than 0.01 of recall@5). Use that value as your "default" and write a one-line commit comment explaining the trade-off.

4. **Migrate a Qdrant collection to pgvector** by exporting the vectors and re-inserting. Measure the **build-time difference** on a corpus of 10k chunks. If the difference is > 5×, explain *what* is the extra cost (Postgres disk index vs. in-memory graph).

5. **Matryoshka on a non-Matryoshka model.** Take the 768-d `nomic-embed-text` index, **truncate** to 32-d, and measure recall@5. You will get *something* — it won't be 0.196 (that's the *trained* 128-d result). How much worse is raw truncation than *trained* truncation, and what does that tell you about Matryoshka training?

6. **Hybrid: BM25 + vector on all five stores.** We only benchmarked the vector-only path in §6. Re-run ch.05's best hybrid recipe (weighted RRF, `k=5`) on **Chroma, FAISS, pgvector, Qdrant, and LanceDB**, and report which is the fastest *hybrid* pipeline. You will need to confirm that each store supports `BM25` (pgvector: `tsvector`; Qdrant: native; FAISS: `rank_bm25` library; Chroma/LanceDB: bring-your-own).

---

## Next

**Next:** [07_reranking_and_query_transforms.md](07_reranking_and_query_transforms.md) — Reranking and query transforms: now that you can *find* the right 50 chunks, how do you **re-order** them so the right 5 are first? We add a cross-encoder as a second pass, measure the cost (recall@5 and latency), and also try a set of **query transformations** (HyDE, multi-query, step-back) to see if we can *find* better chunks before the reranker sees them.
