# 05 — Retrieval: dense vs BM25 vs hybrid (RRF), MMR, metadata filters, Qdrant native hybrid

## What you will learn
- Why dense (embedding-based) and sparse (keyword-based) retrieval fail on *different* kinds of
  question — dense paraphrases well but blurs exact terms (model names, numbers, acronyms) into an
  average; BM25 (Best Matching 25 — a keyword-scoring formula) matches exact terms exactly but has
  no idea "car" and "automobile" mean the same thing. Two real questions from this tutorial's own
  golden set where only one of the two wins.
- BM25 in plain words, the formula, and a two-document worked example by hand.
- Reciprocal Rank Fusion (RRF) — how to combine a cosine-similarity ranking and a BM25-score ranking
  that live on completely different number scales, worked by hand on real retrieved chunks.
- MMR (Maximal Marginal Relevance) — re-selecting retrieved candidates for *diversity*, not just
  relevance, so top-k does not hand the LLM (Large Language Model) five near-duplicate chunks.
- Metadata filtering (`where={"paper": …}`) and a tiny LLM query router that decides *when* to apply
  it — how often it actually fires on this golden set, and whether it helps.
- The retrieval-only recall@k sweep (k = 1, 3, 5, 10, 20) — cheap (no generation, no judge calls) —
  and what the resulting curves say about picking a k for a real system.
- Qdrant's *native* hybrid search (prefetch + server-side RRF fusion, one round trip) versus doing
  the same fusion in Python across two separate queries — code and a real latency comparison.
- What changed on the scoreboard when only the retriever changed and the chunking strategy
  (`04_parent_child`, chapter 04's best performer) stayed fixed.

## Why this chapter fixes the chunking strategy

Chapter 04 found `04_parent_child` (parent windows of 800 tokens/100 overlap, child windows of 160
tokens/32 overlap, small-to-big retrieval) the best chunking strategy on every retrieval metric —
hit@5 0.609, recall@5 0.493 — *and* the only top performer that costs zero extra LLM calls (unlike
`04_contextual_512`, which needed ~670 context-generation calls to land worse). This chapter keeps
that chunking fixed — every retriever below dense-searches (or BM25-searches) the same 1942 child
chunks, then swaps hits to their parent and de-duplicates, exactly as `ParentChildRetriever`
introduced in chapter 04 — so any scoreboard movement from here on is attributable to the
*retriever*, not to a different cut of the corpus. `05_dense_k5`'s numbers below are, correctly,
identical to `04_parent_child`'s: same chunking, same retrieval logic, just re-run under this
chapter's harness.

## BM25 in plain words

BM25 (Best Matching 25 — the 25th formula tried in a 1990s-2000s research programme at City
University London) scores how well a document matches a query by rewarding two things: how many
times each query term appears in the document (but with diminishing returns — the 10th occurrence
of a word barely adds more signal than the 5th), and how *rare* that term is across the whole
corpus (a term every document contains, like "the" or "paper", tells you nothing; a term only one
document contains is a strong signal). It never looks at meaning — only at which exact tokens
appear where.

```
score(D, Q) = Σ_{t ∈ Q}  IDF(t) · f(t, D)·(k1 + 1)
                          ────────────────────────────────────
                          f(t, D) + k1·(1 − b + b·|D|/avgdl)

IDF(t) = ln( (N − n(t) + 0.5) / (n(t) + 0.5) + 1 )
```

- `f(t, D)` — how many times term `t` appears in document `D`.
- `|D|` / `avgdl` — this document's length / the corpus's average document length; a term hit in a
  short document counts for more than the same hit in a long one (the length-normalisation term).
- `N` / `n(t)` — total documents / documents containing `t`; `IDF(t)` (Inverse Document Frequency)
  is large for rare terms, small for common ones.
- `k1` (≈1.2-2.0, `bm25s`'s default 1.5) and `b` (≈0.75) are tuning constants: `k1` controls how
  fast repeated occurrences saturate, `b` controls how strongly document length is penalised.

**Two-document worked example.** `D1 = "the cat sat on the mat"` (6 words), `D2 = "the dog chased
the cat around the yard"` (8 words), `avgdl = 7`, query = `"mat"`, `k1=1.5`, `b=0.75`:

`n("mat") = 1` (only `D1` has it), `N = 2`, so `IDF("mat") = ln((2−1+0.5)/(1+0.5) + 1) = ln(2) ≈
0.693`. `D1` has `f("mat", D1) = 1`:

```
score(D1) = 0.693 × (1 × 2.5) / (1 + 1.5×(0.25 + 0.75×6/7))
          = 0.693 × 2.5 / 2.339
          ≈ 0.741

score(D2) = 0   (f("mat", D2) = 0 — "mat" never appears, so the whole term drops out)
```

`D1` scores 0.741, `D2` scores exactly 0 — BM25 does not know or care that a "yard" is a place a cat
might also sit; only the literal token `"mat"` counts. `BM25Retriever` (`retrievers.py`) uses
`bm25s` — the same idea, but with lowercasing, English stopword removal, and a Snowball stemmer
(`PyStemmer`, so "retrieves"/"retrieval"/"retrieved" all collapse to one stem) applied to both the
corpus and every query before scoring; the index (postings + the chunk corpus) is persisted under
`data/indexes/bm25/<name>/`, so an experiment re-run does not re-tokenise 1942 chunks from scratch.

## Where dense and BM25 fail differently — two real questions

**BM25 wins, dense misses** (`single_hop_005`): *"Which specific retrieval system, fine-tuned on
MS-MARCO, was used in the case study with Open-Domain QA?"*

```
dense (top-5, hit@5=0.0): "Based on the provided excerpts, the specific retrieval system ...
                            is DPR ..."                                              — wrong
bm25  (top-5, hit@5=1.0): "The retrieval system ... was Contriever, which was fine-tuned
                            on MS-MARCO [lost_in_the_middle §5]."                     — correct
```

The gold evidence chunk contains the literal string `"-tuned on and transferred from MS-MARCO"`.
`"MS-MARCO"` is a proper noun (a dataset name) that an embedding model has no strong reason to
weight specially — it gets folded into the same 768-dimensional average as every other word in the
chunk, and a paraphrase-y question competes on equal footing with chunks that are topically similar
but do not name that dataset. BM25 has the opposite bias: `"MS-MARCO"` is a rare token (few chunks
in this corpus mention it), so its high IDF makes any chunk containing it jump to the top regardless
of how the rest of the sentence reads.

**Dense wins, BM25 misses** (`multi_hop_003`): *"How do the evaluation metrics 'Answer Relevance'
(defined in the Ragas paper) and 'Directness' (used in the Graph RAG paper) differ in their primary
focus, and what did the Graph RAG study find regarding the performance of vector RAG on the
Directness metric?"*

```
dense (top-5, hit@5=1.0): "... Answer Relevance (Ragas): This metric focuses on the degree to
                            which a response directly addresses ... Directness (Graph RAG):
                            ... Graph RAG study found that vector RAG scored lower ..."  — correct
bm25  (top-5, hit@5=0.0): "I cannot answer this from the provided documents. ..."        — abstained
```

This question shares almost no exact vocabulary with the sentences that answer it — it asks the
model to *compare* two named metrics defined in two different papers, a relationship BM25 cannot
see because it has no notion of "these two spans are about comparable things," only "these two spans
share tokens." Dense retrieval's whole value proposition is exactly this: the embedding of "how does
metric A's focus differ from metric B's" lands close to chunks *defining* metric A and metric B in
vector space, even though the literal words barely overlap.

This is the textbook case for hybrid search: fuse both rankings and each side covers the other's
blind spot.

## Reciprocal Rank Fusion (RRF), worked example

RRF combines several *ranked* lists into one without needing their scores on the same scale — a
cosine similarity (roughly `[-1, 1]`) and a BM25 score (unbounded, corpus-dependent) are not
comparable numbers, but "rank 1" means the same thing in both:

```python
def rrf_fuse(rankings: list[list[str]], rrf_k: int = 60, top_k: int | None = None) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (rrf_k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)[:top_k]
```

`RRF(d) = Σ over rankings r that contain d of 1 / (rrf_k + rank_r(d))` — a document present in
*several* rankings, even at a middling rank in each, can outrank a document that is #1 in only one
of them. `rrf_k = 60` (the value from the original Cormack/Clarke/Buettcher 2009 paper, and Qdrant's
own default) flattens the curve so rank 1 vs rank 2 in one list matters less than "present in both
lists at all."

**Worked example**, real top-5 dense and BM25 rankings for `single_hop_005` (short ids, no overlap
between the two lists on this question):

| rank | dense id | cosine | bm25 id | BM25 score |
|---|---|---|---|---|
| 1 | `8def201b` | 0.7221 | `16c82363` | 8.4199 |
| 2 | `439abffc` | 0.7055 | `05276b0f` | 7.8556 |
| 3 | `f235bf08` | 0.7031 | `3d67679d` | 7.3661 |
| 4 | `f361a9bc` | 0.6954 | `fbe45ad3` (the MS-MARCO chunk) | 7.3102 |
| 5 | `dbb65ae4` | 0.6942 | `aa28b2b1` | 7.2164 |

`RRF(8def201b) = 1/61 ≈ 0.01639` (rank 1 in dense, absent from BM25's top-5), and
`RRF(16c82363) = 1/61 ≈ 0.01639` (rank 1 in BM25) — an exact tie, broken by insertion order (dense
first) since neither id appears in the other list. Fused order: `8def201b, 16c82363, 439abffc,
05276b0f, f235bf08, 3d67679d, f361a9bc, fbe45ad3, dbb65ae4, aa28b2b1` — because the two lists share
no ids here, RRF simply interleaves them by rank. The MS-MARCO chunk (`fbe45ad3`, BM25 rank 4) is
still ranked 8th of 10 overall — RRF alone does not rescue a chunk that both retrievers rank low, it
only makes sure a chunk *either* retriever ranks well survives the fusion (see "the router barely
moved the needle" below for the k=5-truncation consequence of that).

`weighted_fuse` is the alternative: min-max normalise each side's scores to `[0, 1]` *independently*
first (so BM25's 8.42 does not simply outweigh cosine's 0.72 by raw magnitude), then combine as
`alpha·dense_norm + (1-alpha)·sparse_norm` (`alpha=0.5` here). A document missing from one side
counts as 0 on that side, not dropped.

## MMR — diversity, not just relevance

Maximal Marginal Relevance re-selects `k` chunks out of a larger candidate pool so each pick is
relevant to the query *and* different from what has already been picked:

```
MMR = argmax_{d ∈ candidates \ selected} [ λ·sim(d, query) − (1−λ)·max_{s ∈ selected} sim(d, s) ]
```

`λ = 0.7` here (mostly relevance, some diversity). `MMRRetriever` dense-searches the top 20
candidates, then greedily re-selects: the first pick is always the single best match to the query;
every pick after that is scored on relevance *minus* its similarity to whatever has already been
picked, so two near-duplicate top candidates never both make it into the final 5 — the second one
gets swapped for something less relevant but genuinely new information. The candidate embeddings
needed for this cost nothing extra: they are the same vectors already computed once at indexing
time, served from `Ollama`'s on-disk embedding cache, not a new embedding call per MMR run.

## Metadata filtering and the query router

`where={"paper": "2005.11401"}` restricts a `DenseRetriever`/`BM25Retriever`/`HybridRetriever` query
to chunks from one paper. Since most questions in this golden set are *not* about a single named
paper (multi-hop, comparative, and global questions deliberately span several), filtering by default
would be wrong more often than right — so `route_paper` asks the LLM, per question, whether it names
one specific paper clearly enough to filter on, replying with strict JSON (`{"paper": "<arxiv id>" |
null}`) validated against the corpus's real id list (a hallucinated id is treated the same as `null`
— it never silently over-filters):

```python
def route_paper(question: str, papers: list[dict], llm_client=None) -> str | None:
    reply = llm_client.chat(
        [{"role": "system", "content": _ROUTER_SYSTEM},
         {"role": "user", "content": f"Papers:\n{listing}\n\nQuestion: {question}"}],
        json_schema=_ROUTER_SCHEMA, temperature=0, max_tokens=100,
    )
    paper_id = json.loads(reply).get("paper")
    return paper_id if paper_id in {p["id"] for p in papers} else None
```

On the 27-question test split, the router fired (returned a non-null paper id) on **9 of 27
questions (33%)** — mostly `single_hop` questions that name a method or paper by its title. Compared
to unfiltered hybrid RRF, `05_hybrid_rrf_filtered_k5` moved correctness from 0.565 to 0.565 (no
change) and recall@5 stayed at 0.414 — **the router fires often but barely moved the needle** on
this corpus. The reason: `04_parent_child`'s dense/BM25 search over 1942 chunks across 12 papers is
already precise enough that restricting to one paper's ~160 chunks rarely changes which chunk wins
the top-5 — filtering helps most when the *unfiltered* retriever is confusing similarly-worded
chunks from different papers, which was not a common failure mode on this run. It is still a useful
technique: on a larger or more repetitive corpus where several papers reuse the same terminology,
this filter would matter far more, and the router's cost (one small, structured-JSON LLM call per
question) is cheap relative to the generation calls every experiment already pays.

## The recall@k sweep

`just retrieval-sweep` runs a **retrieval-only** comparison — hit/recall/MRR (Mean Reciprocal Rank)/nDCG (normalized Discounted Cumulative Gain) at k ∈ {1, 3, 5,
10, 20}, no generation, no judge calls, so it costs a fraction of a second per question
(`runs/05_retrieval_sweep.json`):

![recall@k: dense vs BM25 vs hybrid RRF](runs/05_retrieval_sweep.png)

*(Plot generated at `project/runs/05_retrieval_sweep.png`; not embedded in the repo image pipeline —
open the PNG directly if it does not render inline.)*

| k | dense recall | bm25 recall | hybrid_rrf recall |
|---|---|---|---|
| 1 | 0.232 | 0.348 | 0.304 |
| 3 | 0.406 | 0.449 | 0.415 |
| 5 | 0.493 | 0.486 | 0.415 |
| 10 | 0.538 | 0.573 | 0.660 |
| 20 | 0.586 | 0.680 | 0.718 |

Two things stand out. First, **BM25 alone beats dense alone at almost every k** on this corpus of
research papers — full of exact terminology (method names, dataset names, metric names) that a
32k-vocabulary keyword match is very good at, and this corpus's questions were themselves generated
to probe specific facts, which skews toward exactly the kind of question BM25 is strong on. Second,
**hybrid RRF only pulls ahead once k ≥ 10** — at k=5, RRF's recall (0.415) is actually *below*
either single retriever (dense 0.493, bm25 0.486), because fusing two 20-candidate lists and cutting
to 5 sometimes evicts a chunk that one retriever ranked #1 but the other did not see at all (exactly
the `single_hop_005` example above, where the true chunk ranked 4th on the BM25 side alone but 8th
after fusion). The practical guidance: if your downstream k is small (5 or fewer chunks shown to the
LLM), fuse from a wide enough candidate pool (`k_each` large relative to `k`) or consider **not**
fusing at all and instead running BM25 alone when the corpus is keyword-heavy; if k can be 10+, RRF's
advantage compounds because it is genuinely combining two different signals rather than just
picking the better of the two lists.

## Qdrant native hybrid vs doing it in Python

`HybridRetriever` above does two separate round trips (one to Chroma for dense, one to the in-memory
`bm25s` index for sparse) and fuses client-side in Python. Qdrant (a vector database with **native**
sparse-vector support) can do both halves and the fusion in a single server-side call:

```python
response = self.client.query_points(
    self.collection_name,
    prefetch=[
        models.Prefetch(query=query_embedding, using="nomic", limit=k_each, filter=query_filter),
        models.Prefetch(query=models.SparseVector(indices=..., values=...), using="bm25",
                         limit=k_each, filter=query_filter),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=k, query_filter=query_filter, with_payload=True,
)
```

The collection carries one dense vector (`"nomic"`, 768-d, cosine) and one sparse vector (`"bm25"`)
per point. The sparse side uses `fastembed`'s `Qdrant/bm25` encoder (a small download — stopword
lists only, no ONNX weights, no GPU) with `Modifier.IDF` so Qdrant applies corpus-wide IDF weighting
server-side, reproducing the same BM25 idea `bm25s` implements client-side, in a format Qdrant's
native sparse index expects.

**Real timing** (`query_points_seconds`, wall-clock of the single fused call, k_each=20):
**13.9 ms** per query. The Python-side sweep's mean retrieval-only latency for `hybrid_rrf` was
**1.4 ms** — Qdrant's single round trip over the Docker network (`localhost:6343`) is *slower* here
than two in-process calls against an already-loaded Chroma collection and an in-memory `bm25s`
index, because both of those pay no network cost at all on this corpus's small scale (1942 points).
This is a real, reportable result, not a bug: native hybrid search earns its keep at a scale where
avoiding *two* separate query round trips (over a real network, against much larger collections)
outweighs the fixed cost of any single round trip — not on a 1942-point local index sitting next to
the process that queries it. `05_qdrant_native_hybrid_k5`'s retrieval quality (hit@5 0.565, recall@5
0.471, correctness 0.652 — the best correctness of every chapter-05 experiment) is comparable to
`HybridRetriever`'s Python-side RRF, confirming the two implementations compute close to the same
fusion, just at different cost profiles.

## What changed on the scoreboard

All rows below are `test`-split, on top of the fixed `04_parent_child` chunking (`05_dense_k5` is
identical by construction to `04_parent_child` — same chunks, same retriever):

| experiment | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | s/q |
|---|---|---|---|---|---|---|---|
| **05_dense_k5** (= `04_parent_child`) | 0.609 | 0.493 | 0.433 | 0.474 | 0.500 | 0.901 | 0.003 |
| 05_bm25_k5 | 0.696 | 0.486 | 0.521 | 0.560 | 0.587 | 0.908 | 30.190 |
| 05_hybrid_rrf_k5 | 0.609 | 0.414 | 0.457 | 0.489 | 0.565 | 0.926 | 6.928 |
| 05_hybrid_weighted_k5 | 0.652 | 0.501 | 0.504 | 0.532 | 0.609 | 0.927 | 3.399 |
| 05_hybrid_rrf_k10 | 0.609 | 0.414 | 0.481 | 0.552 | 0.696 | 0.934 | 8.530 |
| 05_dense_mmr_k5 | 0.522 | 0.449 | 0.393 | 0.419 | 0.565 | 0.916 | 18.380 |
| 05_hybrid_rrf_filtered_k5 (router) | 0.609 | 0.414 | 0.457 | 0.489 | 0.565 | 0.936 | 18.507 |
| 05_qdrant_native_hybrid_k5 | 0.565 | 0.471 | 0.500 | 0.506 | 0.652 | 0.943 | 14.527 |

Interpretation:

- **BM25 alone is the best single retriever on hit@5 and MRR** (0.696, 0.521) — this corpus's
  questions skew toward exact-term lookups, and BM25's keyword match wins outright often enough to
  beat dense on the metric that counts "was the answer's evidence anywhere in the top 5" (hit@5),
  even though its recall@5 (0.486, fraction of *all* evidence chunks found) is essentially tied with
  dense (0.493) — BM25 finds *a* right chunk reliably, not necessarily *every* right chunk.
- **`05_hybrid_weighted_k5` is the best all-round performer at k=5** — highest correctness (0.609)
  and recall@5 (0.501) of every k=5 experiment, beating both single retrievers on recall. Weighted
  fusion's independent min-max normalisation avoids RRF's k=5-truncation penalty (see the sweep
  section above) because it blends *scores*, not just ranks, so a chunk that is merely "pretty good"
  on both sides can still outrank a chunk that is #1 on only one side.
- **`05_hybrid_rrf_k5` underperforms both single retrievers on recall@5** (0.414 vs dense's 0.493
  and bm25's 0.486) — this is exactly the sweep's k=5 finding: RRF fusing two 20-wide candidate
  lists and truncating to 5 evicts chunks that ranked well on only one side. At `k=10`
  (`05_hybrid_rrf_k10`) the picture flips — same recall@5 (0.414, unchanged since it is still
  computed on the first 5 of a longer list) but the best correctness of any k=5-scale experiment
  except Qdrant native (0.696), because the LLM now sees more chunks and can piece together an
  answer even when the single best chunk is not in the top-5.
- **The router (`05_hybrid_rrf_filtered_k5`) fired on 9/27 questions but changed nothing measurable**
  versus unfiltered `05_hybrid_rrf_k5` — see "the query router" above for why (this corpus is small
  and topically distinct enough per paper that unfiltered search rarely confuses papers).
- **MMR (`05_dense_mmr_k5`) trades hit@5/recall@5 for correctness** (0.522/0.449 vs plain dense's
  0.609/0.493, but 0.565 vs 0.500 correctness) — deliberately swapping out a near-duplicate for a
  more diverse chunk means MMR sometimes drops the exact evidence quote to make room for background
  context, but the LLM answering from a more varied set of chunks scores better on correctness more
  often than it loses from a missing exact match.
- **Qdrant native hybrid has the best correctness (0.652) and faithfulness (0.943) of every
  experiment**, at 14.5 seconds/question dominated by generation+judge calls, not the 13.9ms fused
  retrieval call itself (see the timing section above).

## Advantages and disadvantages

| retriever | strengths | weaknesses |
|---|---|---|
| **Dense** (cosine) | Understands paraphrase and synonymy; one index, one embedding call per query; cheapest to reason about | Blurs rare/exact terms (proper nouns, numbers, acronyms) into an average; needs a good embedding model for the domain |
| **BM25** (`bm25s`) | Exact-term precision is unbeatable when the term is rare and the question names it; no embedding model or GPU needed; fast, deterministic | Zero understanding of meaning — synonyms/paraphrases are invisible; needs matching tokenisation between corpus and query (stemmer/stopword mismatches silently hurt recall) |
| **Hybrid (Python RRF/weighted)** | Combines both retrievers' strengths; RRF needs no score calibration; weighted fusion (with normalisation) can outperform RRF at small k | Two round trips per query; RRF specifically can *underperform* either single retriever at small k if the candidate pool isn't wide enough (see the k=5 sweep result above) |
| **Qdrant native hybrid** | One round trip, one API call; scales better than two separate queries as collection size and network distance grow; built-in filtering on both prefetch legs | Needs a running Qdrant server (`just up qdrant`); on a small local collection the network round trip can be *slower* than doing both queries in-process (measured above); an extra sparse-encoder download (`fastembed`'s `Qdrant/bm25`) |

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `QdrantHybridRetriever`/`QdrantStore` calls hang or raise a connection error | Qdrant is not running | `just up qdrant` first (waits for the container's healthcheck); `just check` reports `Qdrant /readyz` |
| first `QdrantStore`/`fastembed` call is slow the first time it runs | `fastembed.SparseTextEmbedding("Qdrant/bm25")` downloads its (small, stopword-lists-only) model files on first use, cached under `~/.cache/fastembed` afterward | expected once per machine; subsequent runs are fast |
| BM25 recall looks worse than expected after changing the tokenizer (e.g. disabling the stemmer) | the corpus was indexed with one tokenisation (lowercase + stopwords + stemmer) but queries are tokenised with a different one — BM25 only matches identical *stemmed tokens*, so a mismatch silently drops matches | always rebuild the persisted index (`BM25Retriever.from_chunks(..., rebuild=True)`) after changing `_tokenize`'s settings; `data/indexes/bm25/<name>/` does not know its own tokenisation config |
| `bm25s.BM25.retrieve()` returns chunk *dicts* instead of ids, crashing `self._chunks[i]` lookups | `bm25s.BM25.load(..., load_corpus=True)` sets the loaded `BM25` object's own `.corpus` attribute, which `.retrieve()` silently falls back to when its own `corpus=` argument is `None` — a freshly `.build()`-ed index never sets `.corpus`, so this only bites *after* a reload from disk | `BM25Retriever.load()` clears `self._bm25.corpus = None` right after extracting `self._chunks`, restoring the same (indices-only) behaviour a fresh build has |
| the query router (`route_paper`) never fires, even on questions that clearly name a paper | the router's paper listing was built from a different corpus snapshot than the one indexed, or the LLM named a paper id that isn't in `papers` | `route_paper` validates the returned id against the known id list and returns `None` on any mismatch (including a hallucinated id) by design — check `papers` is `corpus.load_papers()`'s current output, not a stale list |

## Exercises

1. Pick one `single_hop` question from `data/golden/qa.jsonl` whose evidence quote contains a
   number or a proper noun (a dataset name, a model name). Run it through `05_dense_k5`'s and
   `05_bm25_k5`'s `predictions.jsonl` — does BM25 retrieve it and dense miss it, the way
   `single_hop_005` does above?
2. Change `HybridRetriever`'s `k_each` from 20 to 5 and re-run `05_hybrid_rrf_k5`. Does recall@5 get
   better or worse, and does that match the "wider candidate pool helps RRF at small k" reasoning
   from the sweep section?
3. `weighted_fuse`'s `alpha` defaults to 0.5 (equal weight). Try `alpha=0.8` (mostly dense) and
   `alpha=0.2` (mostly BM25) on `05_hybrid_weighted_k5` — which end of that range performs closer to
   BM25 alone, and does either beat `alpha=0.5`'s correctness (0.609)?
4. `route_paper`'s system prompt tells the LLM to only name a paper "if the question is clearly and
   specifically about that one paper." Loosen that instruction (remove "clearly and specifically")
   and re-measure the router's fire rate on the 27 test questions — does a looser router fire on more
   *multi-hop*/*global* questions than it should, and does over-filtering hurt recall?
5. (Open-ended) `MMRRetriever` uses `lambda_mult=0.7`. Sweep `lambda_mult` from 1.0 (pure relevance,
   equivalent to plain dense top-k) down to 0.3 (mostly diversity) and plot correctness against it —
   is there a sweet spot, or does correctness degrade monotonically as diversity is weighted higher?

---
Previous: [04_chunking.md](04_chunking.md) · Next: [06_embeddings_and_vector_stores.md](06_embeddings_and_vector_stores.md)
