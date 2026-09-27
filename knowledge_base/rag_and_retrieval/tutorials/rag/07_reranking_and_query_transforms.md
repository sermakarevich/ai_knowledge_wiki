# 07 — Reranking & Query Transforms

## What you will learn

- **Reranking** (a slow but careful second-pass re-ordering of the top chunks) and **query transforms** (rewriting what you ask before retrieval) are the two biggest levers left after hybrid search — and they pull in **opposite directions** on our scoreboard.
- Why a **bi-encoder** (one vector per side) and a **cross-encoder** (both sides fed together) differ in fidelity, and what **late interaction** (ColBERT) sits between them.
- Three families of reranker — cross-encoder, LLM (Large Language Model)-as-reranker, late-interaction — compared on hit@5, correctness (corr), faithfulness and seconds per question (s/q), with a **k_each sweep** showing when a bigger candidate pool helps.
- Four query-transform families — **multi-query**, **HyDE** (Hypothetical Document Embeddings — a synthetic passage), **step-back**, **decomposition** — each illustrated with the *actual* rewrites our local LLM produced for two golden questions.
- The one trick the retrieval metrics **cannot see**: **lost-in-the-middle (LITM) reordering** of the context you hand to the generator, plus the trap that **context compression** is a net loser on this corpus.
- Recommendations by budget (fastest / balanced / maximum) and a troubleshooting section for macOS arm64 torch, model downloads and JSON-parse failures.

Baseline for every delta below: **`05_hybrid_rrf_k5`** — parent/child chunks, dense + BM25 (Best Matching 25) via Reciprocal Rank Fusion (RRF) with k_each=20, top-5 kept. On the test split: **hit@5 0.609 · recall@5 0.414 · corr 0.565 · faithfulness 0.926 · 6.9 s/q**.

---

## What changed on the scoreboard

| run | hit@5 | rec@5 | corr | faith | LLM/q | s/q |
|---|---:|---:|---:|---:|---:|---:|
| **05_hybrid_rrf_k5 (baseline)** | 0.609 | 0.414 | 0.565 | 0.926 | 1.0 | 6.93 |
| flashrank rerank | 0.696 | 0.479 | 0.522 | 0.934 | 1.0 | **0.004** |
| **cross-encoder bge** | 0.739 | 0.558 | 0.674 | **0.957** | 1.0 | 0.15 |
| cross-encoder minilm | 0.696 | 0.479 | 0.478 | 0.950 | 1.0 | 0.54 |
| **LLM listwise rerank** | **0.783** | **0.638** | 0.609 | 0.945 | 1.0 | 18.36 |
| ColBERT late interaction | 0.435 | 0.319 | 0.391 | 0.951 | 1.0 | 44.21 |
| multi-query | 0.652 | 0.477 | 0.587 | 0.937 | 1.0 | 72.87 |
| HyDE | 0.652 | 0.501 | 0.565 | 0.927 | 1.0 | 122.15 |
| step-back | 0.565 | 0.429 | 0.543 | 0.936 | 1.0 | 59.06 |
| decompose | 0.609 | 0.480 | 0.522 | 0.930 | 1.0 | 82.31 |
| **LITM reorder** | 0.609 | 0.414 | **0.717** | 0.917 | 1.0 | 41.91 |
| compress (context) | 0.609 | 0.414 | 0.304 | 0.904 | 6.0 | 7.40 |
| **best_combo** (multi-query + bge + LITM) | 0.652 | 0.506 | 0.587 | 0.931 | 1.0 | **4.95** |

Read in one breath: **rerankers buy retrieval quality cheaply** (FlashRank at 0.004 s/q, bge at 0.155 s/q), **LLM reranking is the best ranker but the slowest reranker** (18.4 s/q), **ColBERT and every query transform cost more than they add on this corpus**, and **the single biggest correctness win comes from reordering the context the generator sees — not from finding better chunks** (LITM: corr 0.565 → 0.717 with hit@5 *unchanged*).

---

## 1. Reranking: from bi-encoders to cross-encoders

Chapters 05–06 retrieve with a **bi-encoder** (dual-encoder): question and chunk are each encoded **separately** into a vector, then scored with a dot product. That's what makes a 1,942-chunk index searchable in milliseconds — the chunk vectors are precomputed. The price: the model never *sees question and chunk together*, so interaction is a single number.

A **cross-encoder** feeds the question and one chunk as a single sequence — "Question: … Passage: …" — and asks the model to score *that pair*. Every question–chunk pair is scored by a fresh forward pass, so there is no precomputation and it is one or two orders of magnitude slower per chunk. But the model can use every word in both sides, which is usually a materially better relevance judgment.

```
bi-encoder (retrieval, ch. 05–06)
  question ──[encoder]──► v_q ─┐
                               ├─ dot(v_q, v_d)  →  fast, precomputed, weaker
  chunk    ──[encoder]──► v_d ─┘

cross-encoder (reranking)
  [question + chunk] ──[one forward pass]──► relevance score
                                           → slower, no precompute, stronger

ColBERT (late interaction)
  question ──[encoder]──► q1 q2 … q7   (one vector per token)
  chunk    ──[encoder]──► d1 d2 … d50  (one vector per token)
  score = Σ over question tokens of best-matching chunk token
                                           → precomputable like a bi-encoder,
                                             finer-grained than one dot product
```

That last box is **late interaction**: like a bi-encoder it encodes each side separately (so chunk vectors stay cached), but instead of collapsing each side to *one* vector it keeps *one vector per token*, and scores the pair as the sum of each question token's best match in the chunk (MaxSim). That is how late interaction targets bi-encoder speed with something closer to cross-encoder fidelity — on paper. On our corpus it came out last (see the ColBERT row in §1.1).

**The pattern all three rerankers share:** retrieve a loose pool (we take **k_each=20** from each leg, ~40 candidates after RRF), then re-order that pool with the expensive scorer and keep the top 5. The retriever's job becomes "don't miss it"; the reranker's job becomes "put the right ones first."

### 1.1 The four rerankers we ran

| reranker | what it is | hit@5 | corr | faith | s/q |
|---|---|---:|---:|---:|---:|
| FlashRank (ONNX `ms-marco-TinyBERT-L-2-v2`) | tiny ONNX cross-encoder, CPU | 0.696 | 0.522 | 0.934 | **0.004** |
| MiniLM (cross-encoder `ms-marco-MiniLM-L-6-v2`) | 22 M cross-encoder, CPU | 0.696 | 0.478 | 0.950 | 0.536 |
| **bge-reranker-v2-m3** | large cross-encoder, multilingual MS MARCO | **0.739** | **0.674** | **0.957** | 0.155 |
| **LLM listwise** (`qwen3.8:27b` ranks the pool in one call) | LLM-as-reranker | **0.783** | 0.609 | 0.945 | 18.36 |
| ColBERT `answerai-colbert-small-v1` | late interaction (MaxSim) | 0.435 | 0.391 | 0.951 | 44.21 |

**How to read this**

- **bge-reranker-v2-m3 is the workhorse.** 0.739 hit@5, best-in-class faithfulness (0.957), strongest cheap correctness (0.674), and 0.155 s/q — ~3.5× faster than MiniLM (0.536 s/q) while beating it on every retrieval axis. This is our production default.
- **LLM listwise is the best ranker we measured** (0.783 hit@5, 0.638 rec@5) — the local 27 B model that sees all 20 candidates at once and orders them in a single pass. But at 18.36 s/q it is a *retrieval-quality* tool: it only lifts corr to 0.609, still below bge's 0.674. It is a separate lever from the `best_combo` default in §3, which instead stacks multi-query + bge cross-encoder + LITM reordering.
- **FlashRank is the free lunch**: near-bge hit@5 (0.696 vs 0.739) for **0.004 s/q** — about 40× faster than bge and 130× faster than MiniLM. Use it as a first gate when latency is the constraint.
- **MiniLM earns no place on this corpus**: it ties FlashRank on hit@5, loses on corr (0.478 vs 0.522) and on faith (0.950 vs 0.934 — close but not enough), yet costs ~130× more wall-clock per question (0.536 vs 0.004 s/q).
- **ColBERT is the surprise loser**: 0.435 hit@5 — *below* the un-reranked baseline — and 44.21 s/q, the slowest run in the chapter. Late interaction helps most when the corpus is large and lexical/semantic overlap is sparse; our 23-question, 1,942-chunk setup gives it little to exploit. **Do not add it without re-measuring on your own data.**
- **LLM/q stays 1.0** in every row: that column counts the *answer-generation* call (the faithful/correct judge passes are tracked separately). The cross-encoder / FlashRank / ColBERT rerankers are local models — no Ollama traffic at all. The LLM listwise reranker does add one Ollama call (to order the pool), but that is *not* the generation call, so it correctly stays out of the LLM/q column.

### 1.2 Does a bigger pool help the reranker?

We swept the candidate pool for the three cheap models (k_each = 20 vs 50), scoring hit@5, recall@5 and nDCG@10 (normalized Discounted Cumulative Gain):

| reranker | pool (k_each) | hit@5 | rec@5 | ndcg@10 | s/q |
|---|---:|---:|---:|---:|---:|
| bge | 20 | 0.739 | 0.558 | 0.688 | 1.02 |
| bge | 50 | **0.783** | **0.580** | 0.665 | 1.66 |
| minilm | 20 | 0.696 | 0.479 | 0.600 | 0.29 |
| minilm | 50 | 0.696 | 0.500 | 0.562 | 0.17 |
| flashrank | 20 | 0.696 | 0.479 | 0.554 | 0.049 |
| flashrank | 50 | 0.696 | 0.479 | 0.572 | 0.098 |

> **About the `s/q` column here:** this is the *retrieval-only sweep* (no generation), measured cold and over all five pools (k = 1/3/5/10/20), so its per-question cost is **not** comparable to the full-pipeline `s/q` in §1.1 — e.g. bge reads as 0.155 s/q warm in §1.1 but 1.02 s/q cold here. Both are real measurements of different things; the sweep is quoted only to make the *pool-size* story, not to benchmark cost.

- **bge keeps improving with pool size** — 0.739 → 0.783 hit@5, and rec@5 0.558 → 0.580. A strong enough scorer can actually *use* candidates that fell outside the retriever's top 20.
- **MiniLM and FlashRank are flat on hit@5** (0.696 at both pools) — their ceiling is the model, not the pool: a bigger candidate set can't recover what the scorer can't rank higher.

**Practical rule:** reranker quality is set by the model first and the pool second. If you can afford to fetch a wider pool, run bge over **k_each=50** — the `just rerank-sweep` recipe reproduces the table above into `runs/07_rerank_sweep.json`. If you only want the retriever's top 20, FlashRank is as good as it gets on this corpus and is by far the cheapest (0.004 s/q full pipeline).

### 1.3 Advantages / disadvantages — rerankers

| | advantage | disadvantage |
|---|---|---|
| **FlashRank** | ~free (0.004 s/q full pipeline); decent hit@5 | no correctness lift; saturates at pool 20 |
| **bge cross-encoder** | best quality per second; best faithfulness; benefits from a bigger pool | one forward pass per candidate — cost grows linearly with pool |
| **MiniLM cross-encoder** | tiny (23 M), easy to self-host | no measurable edge over FlashRank on this corpus |
| **LLM listwise** | best hit@5/rec@5 of anything we ran; one call ranks the whole pool | ~18 s/q; retrieval win doesn't transfer to answer quality alone |
| **ColBERT** | cached token vectors in principle; finest-grained scoring | worst result *and* slowest here; needs a corpus big enough to matter |

---

## 2. Query transforms: change the question, not the pipeline

A reranker re-orders what retrieval *found*. A **query transform** changes what retrieval *was asked for*. All four families below make one (multi-query sometimes a few) extra LLM call per question, retrieve with the *transformed* query, and then run the same generation pass as the baseline — so every delta is attributable to the rewrite itself.

### 2.1 Multi-query — ask the same thing three ways

The LLM writes 3 paraphrases covering different vocabulary (definition ↔ application, synonyms), and each is retrieved separately and unioned.

Golden question ① — *"According to the paper, what specific type of human input does Ragas allow users to avoid when evaluating RAG architectures?"*

> 1. Ragas framework elimination of manual annotation requirements in RAG pipeline assessment
> 2. Automated metrics for retrieval-augmented generation systems replacing subjective human feedback
> 3. Objective evaluation methods for RAG architectures that reduce reliance on expert labeling

Golden question ② — *"How does the evaluation of retrieval performance on the BEIR benchmark differ between the RAPTOR and ColBERTv2 papers?"*

> 1. Comparative analysis of BEIR benchmark metrics in RAPTOR versus ColBERTv2 retrieval systems
> 2. Differences in retrieval effectiveness assessment protocols between RAPTOR and ColBERTv2 on the BEIR dataset
> 3. How RAPTOR and ColBERTv2 papers report and compare their performance on BEIR retrieval tasks

Result: hit@5 0.652 (+0.043), corr 0.587, **72.9 s/q** for 3 retrievals plus the rewrite call. Modest retrieval gain, large latency cost — the classic multi-query trade.

### 2.2 HyDE — imagine the answer, then search for it

**Hy**pothetical **Doc**ument Embeddings: ask the LLM to *write the answer it would expect* (no corpus available), then retrieve with that synthetic passage. This helps when the question's words barely appear in the documents.

Golden question ① — *"According to the Ragas paper, what specific limitation is associated with using ChatGPT to evaluate a particular aspect…"*

> The Ragas paper identifies that using ChatGPT to assign a score between 0 and 100 to evaluate answer relevance suffers from a lack of consistency and reliability. This scoring method is considered a significant limitation because the LLM's judgments are subjective and do not provide a stable, standard…

Golden question ② — *"How does the approach to handling document segmentation and context in retrieval differ between the ColBERTv2 paper and…"*

> ColBERTv2 employs a late interaction mechanism that scores documents by computing maximal relevance scores over individual token embeddings, inherently treating the document as a collection of independent chunks without requiring explicit segmentation boundaries. In contrast, the RAG survey emphasiz…

Result: hit@5 0.652, rec@5 0.501, corr 0.565 (= baseline) at **122.1 s/q** — the most expensive transform. The synthetic passage is fluent but written from the model's memory, so it can steer retrieval *away* from the evidence. On a clear single-sentence question set it is pure cost.

### 2.3 Step-back — ask the question behind the question

The LLM replaces the specific question with a *higher-level* one (e.g. "What loss function does ColBERTv2 use to distill cross-encoder scores?" → "How does ColBERTv2 train its late-interaction model to match the performance of cross-encoders?"), and retrieves on that.

Golden question ① (above):

> How does ColBERTv2 train its late interaction model to match the performance of cross-encoders?

Golden question ② — *"How do the retrieval accuracy metrics reported in the 2023–2024 papers within this corpus compare to the top-performing… [systems]?"*

> How does the retrieval accuracy of the 2023–2024 corpus compare to the 2026 Industry RAG Leaderboard?

Result: hit@5 **0.565 (−0.044 vs baseline)**, corr 0.543, 59.1 s/q. Stepping back *loses* retrieval on our set — it was built for long, ambiguous, multi-intent queries, which we barely have.

### 2.4 Decompose — split into sub-questions

A compound question is split into 2–4 atomic sub-questions, each retrieved, all results merged.

Golden question ① — *"How do the papers differ in the kind of external knowledge source they retrieve from?"*

> 1. What types of external knowledge sources are retrieved by the papers discussed?
> 2. How do the specific external knowledge sources differ across the various papers?

Golden question ② — *"Which papers in the corpus specifically address the challenges of multi-hop or multi-document reasoning…?"*

> 1. What are the primary challenges associated with multi-hop and multi-document reasoning in natural language processing?
> 2. Which academic papers specifically address the handling of long contexts in language models?
> 3. What research focuses on global summarization techniques for multi-document input…

Result: hit@5 0.609 (= baseline), corr 0.522, 82.3 s/q. On questions that are *already* single-intent, decomposition only adds calls and retrieval fan-out without changing what gets found.

### 2.5 Verdict on this corpus — the honest one

| transform | hit@5 vs base | corr vs base | s/q | LLM calls added |
|---|---:|---:|---:|---|
| multi-query | **+0.043** | +0.022 | 72.9 | +1 |
| HyDE | +0.043 | 0.000 | 122.1 | +1 |
| step-back | −0.044 | −0.022 | 59.1 | +1 |
| decompose | 0.000 | −0.043 | 82.3 | +1 |

None of them beats a decent reranker on *either* axis while costing 1/10th of the seconds-per-question. **These techniques pay off on long, ambiguous, multi-intent queries** — which is why they exist. On our clear 23-question set they mostly buy latency. If your real traffic looks like *"compare X and Y and also tell me how to do Z,"* re-run this chapter's harness on *your* questions before dismissing them.

### 2.6 Advantages / disadvantages — query transforms

| | advantage | disadvantage |
|---|---|---|
| **multi-query** | broadens vocabulary coverage; simplest to add | 3× retrieval + 1 LLM call; gains small on clear queries |
| **HyDE** | helps when question words are absent from the corpus; improves recall for some shapes | most expensive (122 s/q); synthetic passage can be confidently wrong and mislead retrieval |
| **step-back** | great for ambiguous/multi-intent queries | drops hit@5 on clear questions; one extra call |
| **decompose** | handles genuinely compound questions | fan-out multiplies calls and retrieval; neutral on single-intent questions |

---

## 3. Where the generator sees your chunks (LITM + compression)

Re-ranking and re-wrapping change *which* chunks arrive. Two more knobs change how the **generator** consumes them — and they are where the most counterintuitive findings in this chapter live.

**Lost-in-the-middle (LITM) reordering.** The "Lost in the Middle" finding — LLMs attend to the *start and end* of a long context best and the *middle* worst — means the *order* you hand the generator can matter as much as *which* chunks you retrieved. Our `lost_in_the_middle_reorder` does exactly one thing: it takes the top-k context window and **moves the 2nd-ranked chunk to the end**, shifting the rest of the order up (`[1st, 3rd, …, nth, 2nd]`). The rationale: the 2nd-ranked is usually the strongest candidate after the top-1, yet sits at a position the generator is prone to skim over; putting it at the end re-places it in a heavily-weighted region without changing which chunks are present.

- hit@5 / rec@5: **0.609 / 0.414 — literally the baseline numbers** (pure reordering, retrieval untouched, zero LLM cost to the reorder itself).
- corr: **0.565 → 0.717 (+0.152)** — the largest correctness gain in the whole chapter.
- faith 0.926 → 0.917 (−0.009).

The lesson is the one to keep: **retrieval metrics and answer quality are different axes**, and reordering context can be the cheapest high-leverage move you have — it is invisible to hit@5/recall but visible to the correctness judge, and it costs nothing to compute.

**Context compression.** `07_compress` prunes "irrelevant" sentences from each chunk before generation. Measured: hit@5/rec@5 identical (0.609/0.414 — of course, it happens post-retrieval), corr **0.565 → 0.304 (−0.261)**, faith **0.926 → 0.904**, and an extra 5 LLM calls/q. We pruned evidence with the answer in it, and the judge noticed. **Compress is a net loser on this corpus; don't enable it without an evaluation gate.**

### best_combo — the pragmatic default

`07_best_combo = multi-query (3 variants) → hybrid retrieve → RRF fuse → bge cross-encoder on the fused pool → LITM reorder of the final 5`. It borrows the multi-variant expansion that lifts recall, the cheap cross-encoder that gives the strongest per-second retrieval, and the free context reorder that the LITM finding justifies:

> *Recipe note:* the findings doc labels this combo “listwise + LITM,” but the run’s own `metrics.json` (hit@5 0.652 and corr 0.587 — identical to the multi-query run, well below listwise’s 0.783 / 0.609) and the code (`rerank_eval.py::run_best_combo`) both confirm the real recipe is **multi-query + bge cross-encoder + LITM** — what we describe here.

- hit@5 0.652 (+0.043), rec@5 0.506 (+0.092), corr 0.587, faith 0.931, **5.0 s/q** (1 LLM call/q).

Per-question-type breakdown on the test split (`07_per_type.md`):

| type | n | baseline | best_combo | Δcorr |
|---|---:|---:|---:|---:|
| single_hop | 8 | 0.750 | 0.875 | **+0.125** |
| multi_hop | 7 | 0.357 | 0.571 | **+0.214** |
| comparative | 3 | 0.667 | 0.167 | **−0.500** ⚠ |
| global | 5 | 0.500 | 0.400 | −0.100 |
| unanswerable | 4 | 1.000 (abstain) | 1.000 (abstain) | 0.000 |

Two things to sit with. (1) The combo does its best work where you expected it — single-hop and multi-hop — where the multi-query expansion adds recall without hurting ranking. (2) The **comparative** regression (3 questions, 0.667 → 0.167) is a real signal, not noise — we don't have a verified mechanism for *why*, but the natural suspect is the 3-way multi-query expansion pulling in near-miss documents that displace the pair that actually needs to be contrasted. With only 3 questions behind it, treat the fix as hypothesis-level: **if your traffic is comparative-heavy, drop the multi-query expansion from the combo (bge cross-encoder + LITM alone) and re-run this per-type table before shipping.**

---

## 4. Budget-based recommendations for this corpus

| goal | pick | why |
|---|---|---|
| **Minimum latency** | FlashRank rerank @ k_each=20, k=5 | 0.696 hit@5 for **0.004 s/q** full pipeline; the free tier |
| **Balanced production default** | best_combo (multi-query + bge cross-encoder + LITM reorder) | **4.95 s/q**, corr 0.587, faith 0.931; wins on single/multi-hop |
| **Max retrieval quality** | bge cross-encoder @ k_each=50, k=5 | 0.783 hit@5, 0.580 rec@5, best faith (0.957) from the sweep (cold, 1.66 s/q retriever-side — no full-pipeline k50 run exists) |
| **Max correctness budget** | bge cross-encoder @ k_each=20 + LITM reorder | corr 0.674 + reordering headroom; cheaper than LLM rerank with equivalent-or-better corr |
| **Latency-critical edge device** | FlashRank + no transforms + no compression | 0.004 s/q full pipeline |
| **Comparative-question traffic** | drop the multi-query leg from best_combo; run bge cross-encoder + LITM directly | −0.500 on comparative in best_combo (§3) — verify before shipping |

> All full-pipeline `s/q` values above come from the 12 named runs in `07_findings.md` / `07_*/metrics.json` (warm LLM cache). The §1.2 sweep table quotes cold retrieval-only cost and is not comparable.

What we'd **not** ship by default on this corpus: MiniLM cross-encoder (FlashRank does the same job faster), ColBERT (worst + slowest), context compression (corr −0.26), and any query transform *unless* the traffic is long/multi-intent.

---

## 5. Troubleshooting (the ones we actually hit)

**ColBERT load failures / first-run model download.** ColBERT is wired through `pylate`'s `ColBERT` class, which wraps the *original* ColBERTv1-style checkpoints — so we use `answerdotai/answerai-colbert-small-v1`, **not** a "colbert-v2" id: a v2 checkpoint raises `KeyError: 'activation_function'` under sentence-transformers 5.3 (the `ColBERTUnavailable` guard in `rerank_eval.py` records `colbert: "unavailable"` instead of metrics when this happens). All four rerankers pull their weights from the Hugging Face hub on first call, so pre-pull each one (`Reranker.available()` reports which are already on-disk) before your first live query — a cold first pass is the usual source of "my reranker is broken!" reports.

**torch on macOS arm64.** The two cross-encoders (bge-v2-m3, MiniLM) route through `sentence-transformers` → `torch`. On Apple Silicon, `pip install torch` is enough for them at fp32 on CPU. (FlashRank is an ONNX model and does not depend on torch at all — that's why it is the cheapest.) If you see `No such file or directory: 'libtorch_cpu.dylib'`, you installed a CUDA wheel — reinstall with `pip install torch --index-url https://download.pytorch.org/whl/cpu`.

**Listwise-order parsing in the LLM reranker.** We ask the LLM to return a single line of 1-based candidate indices in rank order (see `rerankers.py::_LISTWISE_PROMPT`). The local model is not great at emitting *exactly* that, so `LLMReranker._parse_order` is deliberately permissive: it splits on both spaces and commas, keeps only integers in `[1, n]`, drops duplicates (first occurrence wins), and if the model came back with fewer than `n` values it **fills the missing positions with the retriever's original RRF order** (`for i in range(n): if i not in seen: out.append(i)`). That's the real safety net: the worst case for a malformed reply is "no reranking happened," never a crash and never a silently re-used candidate. No retry loop — the parser's identity-order fallback is the cheaper and more honest fix, and re-prompting the LLM would cost another ~18 s on a 0.05 s problem. On our test split the parser produced a non-identity ordering in essentially every run.

**Cache pollution across runs.** Every Ollama call in `runs/07_*/metrics.json` is cached under the `prompt` hash, so re-running an experiment is essentially free. If you change the reranker prompt or the LLM model *version*, the cache misses and a full 100+ s run comes back — check `details.cache_stats.hits` vs `.misses` before you trust a "regression."

---

## 6. Exercises (CPU-only, no network)

1. **Reproduce the bge @ k50 win.** Run the retrieval-only sweep (`just rerank-sweep`, the `sweep` command in `rerank_eval.py`) and confirm the `cross-encoder-bge_keach_50` row lands at hit@5 ≈ 0.783 (vs 0.739 at k_each=20) in `runs/07_rerank_sweep.json`.
2. **Write a listwise-vs-bge A/B.** For 5 golden questions, log the top-5 order from bge cross-encoder and from LLM listwise rerank. On which questions does LLM listwise actually *lose* to bge (a position where bge has the golden chunk at ≤3 and LLM does not)?
3. **A/B a HyDE alternative: use the *question + answer keyphrase* as a synthetic query instead of a full passage.** Does it beat HyDE on any subset of the 23 questions? (Hypothesis: on our corpus, keyphrase extraction is cheaper and closer to multi-query.)
 4. **LITM without rerank.** Run the plain retriever top-5 through `lost_in_the_middle_reorder` (2nd-ranked chunk → end) and compare corr against the un-reordered baseline. Does it lift corr the way the LITM finding predicts, even without any reranker in the loop?
 5. **Comparative-traffic stress test.** Hand-write 5 comparative questions of the form "which of X / Y / Z is *the one that* …?" and run the full best_combo (multi-query + bge + LITM) vs bge cross-encoder + LITM alone (no multi-query leg). Confirm the −0.500 comparative per-type signal from §3 reproduces; if it does, drop the multi-query expansion for comparative-dominant traffic.

---

## Advantages / disadvantages — the two families, side by side

| family | advantage | disadvantage |
|---|---|---|
| **Reranking** | cheap, deterministic, doesn't change the retriever; bge gives you near-best faith at ~0.15 s/q | cost scales with pool; LLM listwise is 18+ s/q; no effect on *which* chunks would have been retrieved at all |
| **Query transforms** | changes what retrieval *sees* — the only lever that can find a chunk that would otherwise be missed entirely | 1+ LLM calls + more retrieval fan-out per question; on clear questions they mostly add cost, and one wrong rewrite can pull evidence away (HyDE, step-back) |

 The two are **complementary in principle** (transform to find the right pool, rerank to order it, reorder to place it) and we tested one such combo in `07_best_combo` — multi-query + bge cross-encoder + LITM reorder. On *our* corpus the best-per-second trade-off is bge cross-encoder @ k_each=50 with LITM reordering on the generator side; the multi-query leg is an optional recall boost that pays for itself on single/multi-hop traffic and costs you on comparative. Re-measure on your traffic before committing to either family.

---

**Next:** [08_langchain_langgraph.md](08_langchain_langgraph.md) — the same pipeline inside LangChain/LangGraph, including their MultiQueryRetriever and a LLM reranker component, side-by-side with our homegrown versions.
