# 07 — Embeddings and vector index: from a question to a graph entry point

## What you will learn
- Why a natural-language question cannot `MATCH` anything in Cypher (Neo4j's query language, see `ai show research_topics/graph_rag/tutorials/neo4j`) until it is turned into the same kind of vector as the graph's `Chunk` and `Entity` nodes.
- How to store those vectors on the node itself (`db.create.setNodeVectorProperty`) versus in an external vector database, and the real trade-off between the two.
- How to create a Neo4j **vector index** (every option explained) and a **full-text index**, and why you must wait for `SHOW INDEXES` to say `ONLINE` before querying.
- The anatomy of a vector query (`db.index.vector.queryNodes`) and a full-text query (`db.index.fulltext.queryNodes`), with real results from three questions about this document.
- **Hybrid search**: combining vector and full-text rankings with Reciprocal Rank Fusion (RRF), with the real merged ranking for one question.

## Embeddings recap
Chapter [01_concepts.md](01_concepts.md) introduced embeddings: an embedding model turns a piece of text into a fixed-length list of numbers (a **vector**) such that texts with similar *meaning* end up as vectors that are close together. "Cosine similarity" measures that closeness: 1.0 means identical direction (same meaning), 0.0 means unrelated, and it ignores vector length so a short and a long description of the same thing can still score close to 1.0. This tutorial's embedding model is `nomic-embed-text` (768 numbers per vector, see `project/.env` / the tutorial [index.md](index.md)), served by Ollama (a local LLM (Large Language Model) server) alongside the chat model.

Chapter 06 already embedded `Entity` nodes once, as an internal step of entity resolution (comparing two entities' embeddings to find likely duplicates). This chapter reuses that same `Entity.embedding` property for a different purpose — retrieval, not deduplication — and adds the missing half: `Chunk.embedding`, the piece of text retrieval actually starts from when a user asks a question.

## What text to embed, and why

| node | text embedded | why |
|---|---|---|
| `Chunk` | `Chunk.text` (the raw passage, chapter 02) | this is literally what a vector-only RAG system would retrieve; embedding it lets a question find the *passage* that discusses it. |
| `Entity` | `name + ": " + description` | a bare name like `"EM"` embeds close to any other two-letter acronym; the description ("Exact Match, a metric...") is what actually carries the entity's *meaning*, so it must be part of the embedded text, not just a lookup key next to it. |

Both are single strings per node — nothing is chunked further at this stage, because `Chunk.text` is already a small passage (chapter 02's `max_tokens=400`) and an entity's `description` is a sentence or two (chapter 04's extraction prompt).

## Storing vectors: on the node vs. an external vector database

Neo4j 5 can store a vector directly as a node property and index it natively. Some architectures instead keep vectors in a dedicated vector database (Pinecone, Qdrant, pgvector, ...) and the graph database only stores IDs. This tutorial stores vectors **on the node**:

| | vector property on the node (this tutorial) | external vector database |
|---|---|---|
| Query shape | one Cypher query does vector search *and* graph traversal in the same call (chapter 08 needs exactly this: "find the closest chunk, then walk its `MENTIONS` edges") | two round trips: vector DB for the ID list, then a second query to the graph DB by ID — more network hops, and the two systems can drift out of sync |
| Operational surface | one database to run, back up, and secure | two databases, two sets of credentials, two things that can be down |
| Scale | fine up to roughly hundreds of thousands to a few million vectors per label, per Neo4j's own vector index documentation; very large corpora (hundreds of millions of vectors) usually outgrow a general-purpose graph database's native index | purpose-built for billions of vectors, with more index tuning knobs (quantization, disk-backed ANN, ...) |
| Freshness | inserting/updating a node updates the vector index automatically, in the same transaction | the graph DB and the vector DB must be kept in sync by application code (write to both, or dual-write failures) |

For a 41-page document (146 chunks, ~1700 entities) the "one database" trade-off is a clear win: no dual-write bugs, no synchronization job. A production system ingesting millions of documents would revisit this trade-off.

## Embedding chunks: `embed_chunks`

```python
def embed_chunks(batch: int = _EMBED_BATCH_SIZE, only_missing: bool = True) -> int:
    """Embed `Chunk.text` for chunks missing `Chunk.embedding` (or every
    chunk if `only_missing=False`), writing vectors back in batches so a
    re-run only pays for what's still missing -- the same "cache as you go"
    pattern chapter 06 uses for `Entity.embedding`.
    """
    where = "WHERE c.embedding IS NULL" if only_missing else ""
    rows = run_query(f"MATCH (c:Chunk) {where} RETURN c.id AS id, c.text AS text ORDER BY c.id")
    return _embed_and_set(rows, label="Chunk", key_prop="id", batch=batch)
```

`embed_entities` is the same shape, reading `name + ': ' + coalesce(description, '')` instead of `text`, and matching on `normalized_name` (chapter 05/06's stable key) instead of `id`. Both call one shared helper:

```python
def _embed_and_set(rows: list[dict], label: str, key_prop: str, batch: int) -> int:
    if not rows:
        return 0
    for i in range(0, len(rows), batch):
        chunk = rows[i : i + batch]
        vectors = embed([r["text"] for r in chunk])
        run_query(
            f"""
            UNWIND $rows AS row
            MATCH (n:{label} {{{key_prop}: row.key}})
            CALL db.create.setNodeVectorProperty(n, 'embedding', row.vec)
            """,
            rows=[{"key": r["id"], "vec": v} for r, v in zip(chunk, vectors)],
        )
    return len(rows)
```

### Why `db.create.setNodeVectorProperty(n, 'embedding', row.vec)` and not `SET n.embedding = row.vec`

A plain `SET n.embedding = $vec` stores whatever list type the Bolt driver happens to send — the Neo4j Python driver can encode a Python list of floats as a mixed `LIST<INTEGER | FLOAT>` if any value happens to be a whole number (e.g. `1.0` serialised as `1`), and a vector index requires a strict, homogeneous float array. `db.create.setNodeVectorProperty` is APOC-adjacent core Neo4j procedure built specifically for this: it validates the input is a flat numeric array and stores it in Neo4j's native vector encoding, the same encoding `CREATE VECTOR INDEX` expects to read. Using `SET` can produce an embedding that *looks* fine in `RETURN n.embedding` but the vector index silently skips the node (query results come back short, with no error) — a hard-to-debug failure mode this procedure avoids entirely.

## Creating the indexes: `ensure_indexes`

```python
def ensure_indexes(embed_dim: int = 768, timeout_s: float = 60.0) -> None:
    for name, label in _VECTOR_INDEXES.items():          # chunk_embedding -> Chunk, entity_embedding -> Entity
        run_query(
            f"""
            CREATE VECTOR INDEX {name} IF NOT EXISTS
            FOR (n:{label}) ON (n.embedding)
            OPTIONS {{indexConfig: {{
                `vector.dimensions`: $dim,
                `vector.similarity_function`: 'cosine'
            }}}}
            """,
            dim=embed_dim,
        )
    for name, (label, props) in _FULLTEXT_INDEXES.items():  # chunk_text -> Chunk.text, entity_names -> Entity.[name,aliases,description]
        prop_list = ", ".join(f"n.{p}" for p in props)
        run_query(f"CREATE FULLTEXT INDEX {name} IF NOT EXISTS FOR (n:{label}) ON EACH [{prop_list}]")
    ...  # wait for SHOW INDEXES to report ONLINE, see below
```

Every option, explained:
- **`FOR (n:Chunk) ON (n.embedding)`** — a vector index is always scoped to one label and one property; you cannot index "any node with an `embedding` property" the way a full-text index can span multiple properties.
- **`` `vector.dimensions`: 768 ``** — must match the embedding model's output size exactly (`nomic-embed-text` = 768). A query vector of the wrong length is rejected outright (see Pitfalls).
- **`` `vector.similarity_function`: 'cosine' ``** — the other option Neo4j supports is `'euclidean'` (straight-line distance). Cosine is the right choice here because embedding models are trained so that *direction*, not magnitude, carries meaning — two paraphrases of the same idea can have very different vector lengths but point the same way.
- **`IF NOT EXISTS`** — makes the whole function safely re-runnable, the same idempotency principle as chapter 02's `MERGE` and chapter 05's constraints.
- **`CREATE FULLTEXT INDEX ... ON EACH [n.name, n.aliases, n.description]`** — a full-text index, unlike a vector index, can span several properties of the same label at once; a query matches if *any* of them contains the term (Lucene's default per-field OR semantics across the field list).

### Why wait for `ONLINE`

`CREATE INDEX` returns as soon as Neo4j has recorded the index's definition — the actual population (reading every existing node's `embedding` or text into the index's internal structure) happens **asynchronously**, in the background. A vector or full-text query issued a moment later can run against an index that is still `POPULATING`: on this document it typically finishes in well under a second (146 chunks, ~1700 entities), but the failure mode is real and worth guarding against explicitly, so `ensure_indexes` polls:

```python
while True:
    rows = run_query(
        "SHOW INDEXES YIELD name, state WHERE name IN $names RETURN name, state", names=all_names
    )
    states = {r["name"]: r["state"] for r in rows}
    if len(states) == len(all_names) and all(s == "ONLINE" for s in states.values()):
        return
    if time.monotonic() > deadline:
        raise TimeoutError(f"indexes not ONLINE after {timeout_s}s: {states}")
    time.sleep(0.5)
```

Real `SHOW INDEXES` output after `just embed`, filtered to the four this chapter creates (plus the constraints chapter 02/05 already added, for context):

```
name              state   type      entityType  labelsOrTypes  properties
chunk_embedding   ONLINE  VECTOR    NODE        [Chunk]        [embedding]
chunk_id          ONLINE  RANGE     NODE        [Chunk]        [id]
chunk_text        ONLINE  FULLTEXT  NODE        [Chunk]        [text]
document_id       ONLINE  RANGE     NODE        [Document]     [id]
entity_embedding  ONLINE  VECTOR    NODE        [Entity]       [embedding]
entity_name       ONLINE  RANGE     NODE        [Entity]       [name]
entity_names      ONLINE  FULLTEXT  NODE        [Entity]       [name, aliases, description]
entity_normalized_name  ONLINE  RANGE  NODE     [Entity]       [normalized_name]
entity_type       ONLINE  RANGE     NODE        [Entity]       [type]
```

## Vector query anatomy: `search_chunks` / `search_entities`

```python
def search_chunks(question: str, k: int = 5) -> list[dict]:
    vector = embed([question])[0]
    return run_query(
        """
        CALL db.index.vector.queryNodes('chunk_embedding', $k, $vector)
        YIELD node, score
        RETURN node.id AS id, node.text AS text, score
        ORDER BY score DESC
        """,
        k=k, vector=vector,
    )
```

Three steps, always in this order: **(1)** embed the question with the *same* model used to embed the chunks (mixing embedding models produces garbage — their vector spaces are not comparable), **(2)** call `db.index.vector.queryNodes(index_name, k, query_vector)`, which does an approximate nearest-neighbour scan and yields the top-`k` nodes plus a cosine `score` in `[0, 1]` (Neo4j remaps raw cosine similarity, which can be negative, into this range), **(3)** join back to whatever node properties you actually need.

Real results, three questions about this document (`nomic-embed-text`, `chunk_embedding` index, `k=3`):

```
Q: how does HippoRAG index memories
  score=0.7501  "2.1 RAG RAG combines external knowledge with LLMs for improved task performance, integrati..."
  score=0.7476  "Graph Retrieval-Augmented Generation: A Survey BOCI PENG∗, School of Intelligence Science ..."
  score=0.7465  "2 Comparison with Related Techniques and Surveys In this section, we compare Graph Retriev..."

Q: what evaluation datasets are used for GraphRAG
  score=0.8960  "9 Applications and Evaluation In this section, we will summarize the downstream tasks, app..."
  score=0.8944  "10.6 Standard Benchmarks GraphRAG is a relatively new field that lacks unified and standar..."
  score=0.8689  "5 Graph-Based Indexing The construction and indexing of graph databases form the foundatio..."

Q: how are communities detected in a knowledge graph
  score=0.8222  "Some approaches transform knowledge graphs into human-readable text using predefined rules..."
  score=0.8143  "3.1 Text-Attributed Graphs The graph data used in Graph RAG can be represented uniformly a..."
  score=0.8110  "Towards Foundation Models for Knowledge Graph Reasoning. In The Twelfth International Con..."
```

The middle question scores noticeably higher (0.87-0.90) than the other two (0.75, 0.81-0.82) because this survey has an entire section literally titled "Applications and Evaluation" — a close *topical* match. `"how does HippoRAG index memories"` scores lower because HippoRAG is mentioned only in passing (as one cited method among many), not explained in depth; this is a real, useful signal — a low top score is itself information ("this document probably doesn't cover that in detail"), which chapter 08's retrieval pipeline can act on.

`search_entities` is the same query against the `entity_embedding` index — see the full-text section below for why a hybrid of both usually beats either alone.

## Full-text search: Lucene syntax, fuzzy matching, and why aliases matter

`db.index.fulltext.queryNodes` runs the query string through Apache Lucene (the text search engine Neo4j's full-text indexes are built on), not a plain substring match:

```python
def search_fulltext(question: str, k: int = 10) -> list[dict]:
    return run_query(
        """
        CALL db.index.fulltext.queryNodes('entity_names', $question) YIELD node, score
        RETURN node.normalized_name AS normalized_name, node.name AS name, node.type AS type, score
        ORDER BY score DESC LIMIT $k
        """,
        question=question, k=k,
    )
```

A few Lucene basics that matter in practice:
- Plain words are OR'd together and scored by TF-IDF-like relevance (rarer terms count for more) — `score` here is **not** in `[0, 1]` like cosine similarity; it is an unbounded relevance score, only meaningful for *ranking within one query*, never for comparing across two different queries.
- **Fuzzy matching** with `~` tolerates typos/spelling variants via edit distance. Real example — a misspelled `"Graph RAGG"` (double G) against `entity_names`:

  ```
  "Graph RAGG"  (no fuzzy)        "Graph RAGG~" (fuzzy)
  Dependency Graph        3.784   CRAG - Comprehensive RAG Benchmark      6.286
  Graph Transformers      3.758   RaFe: Ranking Feedback Improves...RAG   6.046
  graph classification    3.709   GRAG: Graph Retrieval-Augmented Gen.   5.893
  Graph Indexing          3.629   Yago                                    5.888
  patent-phrase graph     3.384   GRAG                                    4.738
  ```
  Without `~`, Lucene only matches the literal words `"Graph"` and `"RAGG"` (which matches nothing except via the shared word `"Graph"`); with `~`, `"RAGG"` fuzzy-matches `"RAG"` and `"GRAG"`, surfacing the actually-relevant entities.
- **Why `entity_names` indexes `aliases` as well as `name`**: chapter 06 showed that a merged entity keeps every historical spelling in `Entity.aliases` (e.g. `Graph-Enhanced Generation (G-Generation)`'s aliases include `G-Generation` and `Graph-Enhanced Generation`). A real query for just the alias `"G-Generation"` finds that entity even though its canonical `name` doesn't contain that exact string:

  ```
  search_fulltext("G-Generation", 5)
  Graph-Enhanced Generation (G-Generation)   Technique   8.518
  G-G-E                                       Method      6.601
  G-Retriever                                 Method      5.568
  ```
  Without indexing `aliases`, this query would only match on stray word overlap and miss the entity entirely — the whole reason chapter 06 carried aliases through every merge instead of discarding them.

## Hybrid search: Reciprocal Rank Fusion (RRF)

Vector search and full-text search fail in different, complementary ways: vector search misses exact rare tokens buried in a long description (it embeds *meaning*, which can dilute a specific acronym), full-text search misses paraphrases with no shared words. Combining their two ranked lists needs a way to merge them that doesn't require their scores to be on the same scale — a cosine similarity of 0.87 and a Lucene score of 6.3 are not comparable numbers. **Reciprocal Rank Fusion (RRF)** sidesteps this by only using each list's **rank**, not its score:

```python
def hybrid_search_entities(question: str, k: int = 10) -> list[dict]:
    vector_hits = search_entities(question, k=max(k, 10))
    fulltext_hits = search_fulltext(question, k=max(k, 10))

    scores: dict[str, float] = {}
    info: dict[str, dict] = {}
    for hits in (vector_hits, fulltext_hits):
        for rank, hit in enumerate(hits, start=1):
            key = hit["normalized_name"]
            scores[key] = scores.get(key, 0.0) + 1.0 / (_RRF_K + rank)   # _RRF_K = 60
            info[key] = hit

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:k]
    return [{**info[key], "rrf_score": round(score, 5)} for key, score in ranked]
```

Each entity's fused score is `sum(1 / (60 + rank))` across every list it appears in — rank 1 in a list contributes `1/61 ≈ 0.0164`, rank 10 contributes `1/70 ≈ 0.0143`, a deliberately gentle slope (`60` is the standard damping constant from the original RRF paper) so one list's single top hit cannot dominate an item that ranks respectably in *both* lists. An entity appearing in both lists, even at modest rank in each, outranks an entity that is rank 1 in only one list.

Real merged ranking for `"how does HippoRAG index memories"` (`entity_embedding` + `entity_names`, k=5):

```
name                                                      type    rrf_score
HippoRAG: Neurobiologically Inspired Long-Term Memory...  Paper   0.03252
HippoRAG                                                  Method  0.03252
Bernal Jiménez Gutiérrez                                  Person  0.03175
Recall@K                                                  Metric  0.01562
Lost in the Middle: How Language Models Use Long Contexts Paper   0.01562
```

Both `HippoRAG` entities score identically (`0.03252` ≈ `1/61 + 1/... `) because each ranked at or near the top of *both* the vector list and the full-text list (the literal word "HippoRAG" is both semantically and lexically the closest match) — exactly the case hybrid search is meant to reward.

## Timing

| operation | count | total time | throughput / latency |
|---|---|---|---|
| embed chunks (`nomic-embed-text`, batch=32) | 146 | ~7 s | ~20 texts/s |
| embed entities (`nomic-embed-text`, batch=32) | 1748 | ~7 s | ~250 texts/s (shorter texts, warmer model) |
| `search_chunks` (1 embed call + vector query) | 1 question | ~0.2 s | dominated by the single embed call |
| `search_entities` (1 embed call + vector query) | 1 question | ~0.08 s | |
| `search_fulltext` (no embed call) | 1 question | ~0.01 s | no Ollama round trip at all |
| `hybrid_search_entities` (1 embed + 2 queries) | 1 question | ~0.08 s | |

The embedding model is dramatically faster than the chat model used in chapters 03-06 (10-60 s per call there, sub-second per batch here) — `nomic-embed-text` is a much smaller model doing much less work per call, and Ollama batches multiple texts into one HTTP round trip.

## Pitfalls

- **Dimension mismatch**: querying a 768-dimension index with a vector of the wrong length fails loudly, not silently — real error from this project:
  ```
  Failed to invoke procedure `db.index.vector.queryNodes`:
  Caused by: java.lang.IllegalArgumentException: Index query vector has 3 dimensions, but indexed vectors have 768.
  ```
  This happens if you ever embed a question with a different model than the one that embedded the corpus (or swap `EMBED_MODEL` in `.env` without re-embedding everything).
- **Index still populating**: a query issued immediately after `CREATE VECTOR INDEX`/`CREATE FULLTEXT INDEX` can run against a `POPULATING` index and return incomplete or zero results with no error at all — this is why `ensure_indexes` blocks on `SHOW INDEXES` before returning, instead of trusting that `CREATE INDEX` finishing means the index is ready.
- **`None` embeddings**: a node with `embedding IS NULL` (never embedded, or created after the last `just embed`) is simply **absent** from vector search results — no error, no warning, it just never shows up as a candidate. `embed_chunks`/`embed_entities`'s `only_missing=True` default exists precisely to make it cheap to close this gap: re-run `just embed` any time new chunks or entities are written and it embeds only what's missing.

## Key takeaways
- A question must be embedded with the *same* model that embedded the corpus before any vector search can run; mixing models produces meaningless similarity scores, and a dimension mismatch fails loudly.
- `db.create.setNodeVectorProperty` is the input for a vector-indexed property, not `SET` — it guarantees the correct, homogeneous float encoding a `CREATE VECTOR INDEX` expects, avoiding a silent "node never shows up in results" failure mode.
- Vector indexes are single-label, single-property; full-text indexes can span several properties (here, `name` + `aliases` + `description`) and match on *any* of them — this is exactly why chapter 06 carried `aliases` through every merge instead of discarding them.
- Always wait for `SHOW INDEXES` to report `ONLINE` before querying a freshly created index — population is asynchronous and a query against a still-`POPULATING` index can silently under-return.
- Reciprocal Rank Fusion combines vector and full-text rankings by rank, not raw score, precisely because a cosine similarity and a Lucene relevance score are not on comparable scales — this is the retrieval building block chapter 08 uses to turn a question into a graph entry point.

Next: [08_retrieval_local_search.md](08_retrieval_local_search.md) — answering a question: vector hit → entities → graph neighbourhood → context assembly → LLM answer with citations.
