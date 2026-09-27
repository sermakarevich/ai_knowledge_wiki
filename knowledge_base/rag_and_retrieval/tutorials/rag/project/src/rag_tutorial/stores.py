"""Chroma vector store wrapper. Chapter 03 uses this alone (embedded, no server);
chapter 05 adds `QdrantStore` for native hybrid (dense + sparse) search;
chapter 06 compares Chroma/Qdrant against pgvector, FAISS and LanceDB.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import chromadb

from rag_tutorial.config import settings
from rag_tutorial.schema import Chunk

DEFAULT_PERSIST_DIR = "data/indexes/chroma"


class ChromaStore:
    """A single Chroma collection, persisted on disk, cosine distance.

    Uses the embedded `PersistentClient` (no Docker, no server process) —
    Chroma writes its index straight to `persist_dir`. Chunk fields other than
    `id` and `text` are stored as metadata so a query result can be turned
    back into a full `Chunk` without a second lookup.
    """

    def __init__(self, collection_name: str, persist_dir: str | Path | None = None):
        self.collection_name = collection_name
        self.persist_dir = settings.path(persist_dir or DEFAULT_PERSIST_DIR)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Add `chunks` with their pre-computed `embeddings` (same order, same length).

        Batched to stay under Chroma's max batch size (fires with 5000+ chunks,
        e.g. `sentence_window`, whose one-chunk-per-sentence strategy easily
        exceeds it).
        """
        if not chunks:
            return
        max_batch = self.client.get_max_batch_size()
        for i in range(0, len(chunks), max_batch):
            batch = chunks[i : i + max_batch]
            self.collection.add(
                ids=[c.id for c in batch],
                embeddings=embeddings[i : i + max_batch],
                documents=[c.text for c in batch],
                metadatas=[
                    {"paper": c.paper, "section": c.section, "start": c.start, "end": c.end}
                    for c in batch
                ],
            )

    def query(self, embedding: list[float], k: int = 5, where: dict | None = None) -> list[tuple[Chunk, float]]:
        """Top-`k` nearest chunks to `embedding`, most similar first.

        Score is cosine similarity (`1 - cosine distance`), so 1.0 is a
        perfect match and scores generally fall in `[-1, 1]`.
        """
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        out: list[tuple[Chunk, float]] = []
        ids = result["ids"][0]
        docs = result["documents"][0]
        metas = result["metadatas"][0]
        distances = result["distances"][0]
        for id_, doc_text, meta, distance in zip(ids, docs, metas, distances):
            chunk = Chunk(
                id=id_,
                paper=meta["paper"],
                section=meta["section"],
                text=doc_text,
                start=meta["start"],
                end=meta["end"],
            )
            out.append((chunk, 1.0 - distance))
        return out

    def count(self) -> int:
        return self.collection.count()

    def reset(self) -> None:
        """Delete and recreate the collection (used before re-indexing)."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            self.collection_name, metadata={"hnsw:space": "cosine"}
        )

    def on_disk_bytes(self) -> int:
        """Total bytes used by this collection's persist dir (sqlite + HNSW
        segment files). Chapter 06's vector-store bench reads this alongside
        `FaissStore.on_disk_bytes` / `LanceDBStore.on_disk_bytes` /
        `PgVectorStore.on_disk_bytes` to compare on-disk footprint."""
        return _dir_bytes(self.persist_dir)


@lru_cache(maxsize=1)
def _bm25_sparse_model():
    """`fastembed`'s `Qdrant/bm25` sparse encoder: a ~10 MB download (stopword
    lists only — no ONNX weights, no GPU) that turns text into a Qdrant-native
    sparse vector reproducing BM25 term weights. Cached process-wide since
    loading it does file I/O.

    Chosen over hand-rolling a sparse vector from `bm25s`'s own score matrix
    (that matrix's on-disk layout is an internal, undocumented CSC format not
    meant to be read term-by-document from outside the library) — `fastembed`
    gives the same BM25 idea in a format Qdrant's `Modifier.IDF` sparse vectors
    already expect, at negligible extra cost. This is the "our own bm25s term
    weights, or fastembed" choice chapter 05 leaves open; document it here if a
    future chapter switches.
    """
    from fastembed import SparseTextEmbedding

    return SparseTextEmbedding(model_name="Qdrant/bm25")


class QdrantStore:
    """A Qdrant collection with one dense vector (`"nomic"`, cosine) and one
    sparse vector (`"bm25"`, via `fastembed`'s `Qdrant/bm25` encoder,
    `Modifier.IDF` so Qdrant applies corpus IDF weighting server-side) — native
    hybrid search in one round trip, instead of chapter 05's `HybridRetriever`
    which fuses two separate Python-side queries.

    Point ids: chunk ids are 16-hex-char strings (`schema.chunk_id`), and
    Qdrant point ids must be an unsigned integer or a UUID — so each chunk's
    hex id is parsed as an integer (`int(chunk_id, 16)`) for the point id, and
    the original string id is kept in the payload (`chunk_id`) for round-tripping
    back to a `Chunk`.
    """

    DENSE_NAME = "nomic"
    SPARSE_NAME = "bm25"

    def __init__(self, collection_name: str, url: str | None = None, dim: int | None = None):
        from qdrant_client import QdrantClient, models

        self._models = models
        self.collection_name = collection_name
        self.url = url or settings.qdrant_url
        self.dim = dim or settings.embed_dim
        self.client = QdrantClient(url=self.url)

    @property
    def sparse_model(self):
        return _bm25_sparse_model()

    def reset(self) -> None:
        models = self._models
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(self.collection_name)
        self.client.create_collection(
            self.collection_name,
            vectors_config={self.DENSE_NAME: models.VectorParams(size=self.dim, distance=models.Distance.COSINE)},
            sparse_vectors_config={self.SPARSE_NAME: models.SparseVectorParams(modifier=models.Modifier.IDF)},
        )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]], batch_size: int = 256) -> None:
        """Add `chunks` with their pre-computed dense `embeddings`; sparse vectors
        are computed here from `chunk.text` via the BM25 encoder."""
        if not chunks:
            return
        models = self._models
        sparse_vectors = list(self.sparse_model.embed([c.text for c in chunks]))
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            points = [
                models.PointStruct(
                    id=int(chunk.id, 16),
                    vector={
                        self.DENSE_NAME: dense_vec,
                        self.SPARSE_NAME: models.SparseVector(
                            indices=sparse_vec.indices.tolist(), values=sparse_vec.values.tolist()
                        ),
                    },
                    payload={
                        "chunk_id": chunk.id,
                        "paper": chunk.paper,
                        "section": chunk.section,
                        "text": chunk.text,
                        "start": chunk.start,
                        "end": chunk.end,
                    },
                )
                for chunk, dense_vec, sparse_vec in zip(
                    batch, embeddings[i : i + batch_size], sparse_vectors[i : i + batch_size]
                )
            ]
            self.client.upsert(self.collection_name, points=points)

    def _filter_for(self, where: dict | None):
        if not where:
            return None
        models = self._models
        return models.Filter(
            must=[models.FieldCondition(key=key, match=models.MatchValue(value=val)) for key, val in where.items()]
        )

    def _to_chunk(self, payload: dict) -> Chunk:
        return Chunk(
            id=payload["chunk_id"],
            paper=payload["paper"],
            section=payload["section"],
            text=payload["text"],
            start=payload["start"],
            end=payload["end"],
        )

    def query_hybrid(
        self,
        query_text: str,
        query_embedding: list[float],
        k: int = 5,
        k_each: int = 20,
        where: dict | None = None,
    ) -> tuple[list[tuple[Chunk, float]], float]:
        """Native hybrid search in one round trip: Qdrant prefetches the top
        `k_each` candidates from the dense vector and from the sparse (BM25)
        vector, fuses them server-side with Reciprocal Rank Fusion
        (`models.FusionQuery(fusion=models.Fusion.RRF)`), and returns the fused
        top `k`. Returns `(results, seconds)` — the wall-clock time of the
        single `query_points` call — so callers can report native-hybrid
        latency against `HybridRetriever`'s two Python-side queries + fusion.
        """
        import time

        models = self._models
        sparse_query = next(iter(self.sparse_model.query_embed([query_text])))
        query_filter = self._filter_for(where)

        start = time.monotonic()
        response = self.client.query_points(
            self.collection_name,
            prefetch=[
                models.Prefetch(query=query_embedding, using=self.DENSE_NAME, limit=k_each, filter=query_filter),
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_query.indices.tolist(), values=sparse_query.values.tolist()
                    ),
                    using=self.SPARSE_NAME,
                    limit=k_each,
                    filter=query_filter,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=k,
            query_filter=query_filter,
            with_payload=True,
        )
        elapsed = time.monotonic() - start

        results = [(self._to_chunk(point.payload), point.score) for point in response.points]
        return results, elapsed

    def count(self) -> int:
        return self.client.count(self.collection_name).count


def _dir_bytes(path: Path) -> int:
    """Total size in bytes of every file under `path` (0 if it does not exist)."""
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


class FaissStore:
    """`faiss-cpu` store with one of two index types:

    - ``flat``    -> ``IndexFlatIP``: exact inner-product search (the ground
      truth every ANN index is measured against).
    - ``hnsw``    -> ``IndexHNSWFlat(dim, METRIC_INNER_PRODUCT)`` with
      configurable ``m``/``ef_construction`` and search ``ef``.

    Vectors are assumed unit-normalised (all our embeddings are), so inner
    product == cosine similarity — the same score convention Chroma/Qdrant use.
    Chunk rows are kept in a side list (FAISS has no metadata of its own);
    `save()`/`load()` persist index + rows to `persist_dir` (default
    ``data/indexes/faiss``).
    """

    def __init__(self, collection_name: str, kind: str = "flat", m: int = 16, ef_construction: int = 100, ef: int = 64, persist_dir: str | Path | None = None):
        import faiss

        self._faiss = faiss
        self.collection_name = collection_name
        self.kind = kind
        self.persist_dir = settings.path(persist_dir or f"data/indexes/faiss/{kind}")
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._m = m
        self._ef_construction = ef_construction
        self._ef = ef
        self._index = None
        self._rows: list[dict] = []

    def _make_index(self, dim: int) -> None:
        faiss = self._faiss
        if self.kind == "flat":
            self._index = faiss.IndexFlatIP(dim)
        elif self.kind == "hnsw":
            index = faiss.IndexHNSWFlat(dim, self._m, faiss.METRIC_INNER_PRODUCT)
            index.hnsw.efConstruction = self._ef_construction
            self._index = index
        else:
            raise ValueError(f"unknown FaissStore kind {self.kind!r} (use 'flat' or 'hnsw')")

    def reset(self, dim: int | None = None) -> None:
        """Drop all rows (and the index, optionally re-sized for `dim`)."""
        self._rows = []
        if dim is not None:
            self._make_index(dim)

    def add(self, chunks: list[Chunk], embeddings: list[list[float]], batch_size: int = 256) -> None:
        import numpy as np

        if not chunks:
            return
        vectors = np.asarray(embeddings, dtype=np.float32)
        if self._index is None:
            self._make_index(vectors.shape[1])
        self._index.add(vectors)
        self._rows.extend(
            {
                "id": c.id,
                "paper": c.paper,
                "section": c.section,
                "text": c.text,
                "start": c.start,
                "end": c.end,
            }
            for c in chunks
        )

    def query(self, embedding: list[float], k: int = 5, where: dict | None = None) -> list[tuple[Chunk, float]]:
        import numpy as np

        if self._index is None or not self._rows:
            return []
        if self.kind == "hnsw":
            self._index.hnsw.efSearch = self._ef
        vector = np.asarray([embedding], dtype=np.float32)
        scores, ids = self._index.search(vector, k)
        out: list[tuple[Chunk, float]] = []
        for score, row_id in zip(scores[0], ids[0]):
            if row_id < 0:
                continue
            row = self._rows[row_id]
            if where and any(row.get(key) != value for key, value in where.items()):
                continue
            out.append(
                (
                    Chunk(id=row["id"], paper=row["paper"], section=row["section"], text=row["text"], start=row["start"], end=row["end"]),
                    float(score),
                )
            )
        return out

    def count(self) -> int:
        return len(self._rows)

    def on_disk_bytes(self) -> int:
        total = 0
        for name in ("index.bin", "rows.json"):
            path = self.persist_dir / name
            if path.exists():
                total += path.stat().st_size
        return total

    def save(self) -> None:
        import json

        import faiss

        self.persist_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(self.persist_dir / "index.bin"))
        (self.persist_dir / "rows.json").write_text(json.dumps(self._rows))

    def load(self) -> None:
        import faiss

        self._index = faiss.read_index(str(self.persist_dir / "index.bin"))
        self._rows = json.loads((self.persist_dir / "rows.json").read_text())


class LanceDBStore:
    """LanceDB table (embedded mode, no server) holding vectors + chunk column
    data. LanceDB's vector search is IVF-PQ *flat-by-default*: with no training
    data required for small tables, search is exact-ish and fast, which is the
    interesting comparison point against FAISS-Lance (HNSW).
    """

    def __init__(self, collection_name: str, persist_dir: str | Path | None = None):
        import lancedb

        self.persist_dir = settings.path(persist_dir or f"data/indexes/lancedb/{collection_name}")
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = lancedb.connect(str(self.persist_dir))
        self.collection_name = collection_name

    def reset(self) -> None:
        if self.collection_name in self.client.table_names():
            self.client.drop_table(self.collection_name)

    def _table(self):
        return self.client.open_table(self.collection_name)

    @staticmethod
    def _normalize(v: list[float]) -> list[float]:
        import math

        norm = math.sqrt(sum(x * x for x in v))
        return v if norm == 0 else [x / norm for x in v]

    def add(self, chunks: list[Chunk], embeddings: list[list[float]], batch_size: int = 0) -> None:
        # LanceDB's default metric is L2 (no cosine option in 0.38); we unit-normalise
        # so that L2 ranking == cosine ranking — same score convention as Chroma/Qdrant.
        # For unit vectors: L2² = 2(1-cos), so cos_sim = 1 - 0.5*L2².
        if not chunks:
            return
        rows = [
            {"id": c.id, "paper": c.paper, "section": c.section, "text": c.text, "start": c.start, "end": c.end,
             "vector": self._normalize(emb)}
            for c, emb in zip(chunks, embeddings)
        ]
        if self.collection_name not in self.client.table_names():
            self.client.create_table(self.collection_name, data=rows)
        else:
            self._table().add(rows)

    def query(self, embedding: list[float], k: int = 5, where: dict | None = None) -> list[tuple[Chunk, float]]:
        q = self._table().search(self._normalize(embedding)).limit(k)
        if where:
            cond = " and ".join(f'"{key}" == \'{value}\'' for key, value in where.items())
            q = q.where(cond)
        rows = q.to_list()
        return [
            (Chunk(id=r["id"], paper=r["paper"], section=r["section"], text=r["text"], start=r["start"], end=r["end"]),
             1.0 - 0.5 * float(r["_distance"]))
            for r in rows
        ]

    def count(self) -> int:
        return self._table().count_rows() if self.collection_name in self.client.table_names() else 0

    def on_disk_bytes(self) -> int:
        return _dir_bytes(self.persist_dir)


class PgVectorStore:
    """`pgvector/pgvector:pg17` table (`vector(768)` + `vector_cosine_ops` HNSW
    index, per-spec), driven by `psycopg` (v3, sync). `connect_dsn` defaults to
    `postgres://postgres:postgres@localhost:5434/rag`; the table is
    `create-if-missing` with an explicit `dim`.
    """

    DSN = "postgres://postgres:postgres@localhost:5434/rag"

    def __init__(self, collection_name: str, dim: int = 768, dsn: str | None = None):
        self.collection_name = collection_name
        self.dim = dim
        self.dsn = dsn or PgVectorStore.DSN
        self._conn = None

    def _connect(self):
        if self._conn is None:
            import psycopg

            self._conn = psycopg.connect(self.dsn, autocommit=True)
        return self._conn

    def reset(self) -> None:
        # psycopg3's extended protocol cannot execute multi-statement strings
        # (`stmt; stmt`) in a single `.execute()` — split into separate calls.
        conn = self._connect()
        name = self.collection_name
        conn.execute(f'DROP TABLE IF EXISTS "{name}"')
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute(
            f'''CREATE TABLE "{name}" (
                id TEXT PRIMARY KEY,
                paper TEXT NOT NULL,
                section TEXT NOT NULL,
                text TEXT NOT NULL,
                "start" INT NOT NULL,
                "end" INT NOT NULL,
                vector vector({self.dim}) NOT NULL
            )'''
        )
        conn.execute(f'CREATE INDEX "{name}_hnsw" ON "{name}" USING hnsw (vector vector_cosine_ops)')
        conn.commit()

    def add(self, chunks: list[Chunk], embeddings: list[list[float]], batch_size: int = 256) -> None:
        conn = self._connect()
        with conn.cursor() as cur:
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i : i + batch_size]
                rows = [(c.id, c.paper, c.section, c.text, c.start, c.end, "[" + ",".join(str(v) for v in emb) + "]") for c, emb in zip(batch, embeddings[i : i + batch_size])]
                cur.executemany(
                    f'INSERT INTO "{self.collection_name}" (id, paper, section, text, "start", "end", vector) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    rows,
                )

    def query(self, embedding: list[float], k: int = 5, where: dict | None = None) -> list[tuple[Chunk, float]]:
        conn = self._connect()
        vector_literal = "[" + ",".join(str(v) for v in embedding) + "]"
        # param order: [0] score vector, [1..n-1] where values, [n] ORDER BY vector, [n+1] LIMIT k
        where_values: list = []
        where_sql = ""
        if where:
            conds = []
            for key, value in where.items():
                conds.append(f'"{key}" = %s')
                where_values.append(value)
            where_sql = " WHERE " + " AND ".join(conds)
        sql = f"""SELECT id, paper, section, text, "start", "end", 1 - (vector <=> %s) AS score
                  FROM "{self.collection_name}"{where_sql} ORDER BY vector <=> %s LIMIT %s"""
        params = [vector_literal, *where_values, vector_literal, k]
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [(Chunk(id=r[0], paper=r[1], section=r[2], text=r[3], start=r[4], end=r[5]), float(r[6])) for r in rows]

    def count(self) -> int:
        conn = self._connect()
        with conn.cursor() as cur:
            cur.execute(f'SELECT COUNT(*) FROM "{self.collection_name}"')
            return cur.fetchone()[0]

    def on_disk_bytes(self) -> int:
        conn = self._connect()
        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT COALESCE(SUM(pg_total_relation_size(quote_ident(relname))), 0)
                    FROM pg_class WHERE relname = %s OR relname LIKE %s""",
                (self.collection_name, self.collection_name + "_hnsw"),
            )
            return int(cur.fetchone()[0])
