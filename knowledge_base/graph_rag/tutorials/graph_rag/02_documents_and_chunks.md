# 02 — Documents and chunks: building the lexical graph

## What you will learn
- What "an unknown document" means in this tutorial, and the three file formats the loader handles.
- How PDF text extraction is cleaned up (hyphenated line breaks, running headers/footers, page numbers) — with a real before/after.
- Chunking strategies (fixed size, sentence, heading-aware, semantic) and why this tutorial picks heading-aware chunking with a token overlap.
- The Cypher used to write `Document` and `Chunk` nodes idempotently, and why `MERGE` + `UNWIND` batching instead of `CREATE` per row.
- How to run `just ingest`, explore the result with real Cypher queries, and why re-running it does not create duplicates.

## What "unknown document" means here

This tutorial's premise, from `01_concepts.md`, is: *a document comes in that nobody has read or labelled yet, and it has to end up in a graph with sensible structure — automatically*. Chapter 02 is the first concrete step towards that: before anything can be extracted or reasoned about, the raw file has to become clean, addressable text.

"Unknown" here means two things:
1. **Unknown format** — this tutorial's loader accepts `.pdf`, `.md` (Markdown) and `.txt` (plain text). Our real input, set once in `index.md` and never changed, is a 41-page academic PDF: `data/docs/graphrag_survey_2408.08921.pdf`, the paper *"Graph Retrieval-Augmented Generation: A Survey"* (Peng et al., 2024). PDF is the hard case (see below); Markdown and plain text need far less cleaning.
2. **Unknown content** — the loader and chunker never look at *what* the document is about. That is deliberately deferred to chapter 03 onward. This chapter only builds the **lexical graph**: `Document` and `Chunk` nodes that mirror the physical structure of the text, independent of its subject matter (see the lexical-vs-domain-graph split in `01_concepts.md`).

## The loader: `graph_rag/documents.py`

`load_document(path)` returns a `Document`:

```python
@dataclass
class Document:
    id: str
    path: str
    title: str
    text: str
    sha256: str
    pages: list[Page] = field(default_factory=list)  # empty for non-PDF sources
```

- **`id`** is the sha256 hash of the file's *resolved absolute path*. That makes the id stable across re-runs from the same location, regardless of whether the caller passes a relative or absolute path or runs from a different working directory (a bug we hit while testing this chapter — see Pitfalls).
- **`sha256`** is the hash of the file's *bytes*. `ingest.py` compares this against what's already stored to detect that a document at the same path changed.
- **`title`**: the first `# ` Markdown heading if there is one, else the first non-empty line of the text (this is how our PDF gets its title — the paper has no Markdown headings, but its first line is `Graph Retrieval-Augmented Generation: A Survey`), else the filename.
- Markdown YAML front matter (a `---\n...\n---` block at the top of the file) is stripped before the title is looked for.
- **`pages`** is only populated for PDFs, and is used later in this chapter to record which page(s) each chunk came from.

### PDF cleaning: before and after

Raw text extracted from a PDF page (via `pypdf`) is full of layout noise: a running header repeated on every page, a hyphenated word broken by a line wrap, and inconsistent whitespace. Here is page 6 of the real PDF, extracted with `pypdf` directly, no cleaning:

```python
>>> from pypdf import PdfReader
>>> raw = PdfReader("data/docs/graphrag_survey_2408.08921.pdf").pages[5].extract_text()
>>> raw[:220]
'111:6 Peng et al.\ngraph data used in GraphRAG. Then, we provide formal definitions for two types of models that\ncan be used in the retrieval and generation stages: Graph Neural Networks and Language Models.\n3.1 Text-Attributed Graphs\n...'
```

`111:6 Peng et al.` is the running header this survey repeats on (almost) every page — a page number in the journal's own scheme, followed by the first author's name — and it would otherwise pollute the start of every chunk. Later on the same page, a line wrap splits a word:

```python
>>> raw[raw.find("Sentence-") - 10 : raw.find("Sentence-") + 30]
'RoBERTa [107] and Sentence-\nBERT [140], focus on'
```

`_clean_page_text` in `documents.py` fixes both, in this order — join hyphenated breaks first (they still have their original newline), then drop headers/footers/page numbers, then collapse whitespace:

```python
_RUNNING_HEADER_RE = re.compile(
    r"^\s*(?:\d+:\d+\s+.+|.+\s+\d+:\d+)\s*$|^\s*\d+\s*$", re.MULTILINE
)
_HYPHEN_BREAK_RE = re.compile(r"(\w)-\n(\w)")

def _clean_page_text(text: str) -> str:
    text = _HYPHEN_BREAK_RE.sub(r"\1\2", text)
    text = _RUNNING_HEADER_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text)
    text = _BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()
```

After cleaning, the same page starts clean and the hyphen break is gone:

```python
>>> from graph_rag.documents import _clean_page_text
>>> cleaned = _clean_page_text(raw)
>>> cleaned[:180]
'graph data used in GraphRAG. Then, we provide formal definitions for two types of models that\ncan be used in the retrieval and generation stages: Graph Neural Networks and Language Models.\n3.1 Text-Attributed Graphs\n...'
>>> cleaned[cleaned.find("Sentence") - 10 : cleaned.find("Sentence") + 20]
' RoBERTa [107] and SentenceBERT [140], focus'
```

The `_RUNNING_HEADER_RE` pattern matches this survey's specific header/footer scheme (`111:N Title...` / `Title... 111:N`, a bare page number on its own line). A different PDF with a different header style would need a different regex — this is inherently document-specific, not a general PDF-cleaning solution.

## Chunking: `graph_rag/chunking.py`

### Why chunk at all

A whole 41-page document is far too large to embed as one vector or hand to an LLM (Large Language Model) as retrieval context — both need small, focused pieces of text. Chunking trades off two failure modes: chunks too large dilute the embedding (a vector for 10 unrelated ideas is a poor match for any one of them) and blow past what an LLM can usefully attend to; chunks too small lose surrounding context (a sentence like "It improves on this by 12%" is meaningless without knowing what "it" and "this" are).

### Strategies, and why heading-aware + overlap

| Strategy       | How it works                                                        | Trade-off                                                                                                                               |                                                                                                                    |
| -------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Fixed size     | Cut every N characters or tokens, ignoring text structure           | Simplest, but routinely slices a sentence (or a word) in half                                                                           |                                                                                                                    |
| Sentence-based | Split on sentence boundaries, pack sentences up to a token budget   | Never breaks mid-sentence, but ignores section structure — a chunk can span two unrelated topics                                        |                                                                                                                    |
| Heading-aware  | Split on section headings and paragraphs first, then pack by tokens | Respects the document's own structure and rarely mixes two topics, but needs a heading pattern (regex) that matches the actual document |                                                                                                                    |
| Semantic       | Embed sentences, split where consecutive-sentence similarity drops  | Chunk boundaries follow topic shifts, not layout                                                                                        | Needs an embedding call per sentence just to decide where to cut — expensive, and non-deterministic across re-runs |

This tutorial uses **heading-aware chunking with a token overlap**: split on numbered section headings (`3.2 Related Work`, `10 References` — a pattern typical of academic papers), then on paragraphs, and only fall back to a token-based split for a paragraph too large to fit in one chunk on its own. A **60-token overlap** is carried from the end of one chunk to the start of the next, so a fact split across a chunk boundary is still retrievable from at least one of the two chunks. We picked this over sentence-based chunking because our input is a structured academic paper where section boundaries are meaningful topic boundaries, and over semantic chunking because it would need one extra embedding call per sentence (10-60 seconds each through the Ollama tunnel — see `00_setup.md`) just to decide where to cut, for a document short enough that heading-aware chunking already gives clean, right-sized chunks.

### Token counting

```python
_ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(_ENCODING.encode(text))
```

`tiktoken` (`cl100k_base`, the encoding used by GPT-3.5/GPT-4) counts tokens, not characters, because token count is what actually limits an LLM's context window and what embedding models bill/limit by. This tutorial's chat model is `qwen3.8:27b`, a Qwen model with its own, different tokenizer — `cl100k_base` is **an approximation**, not qwen's real token count. It is close enough to keep chunks roughly the right size and comfortably under any reasonable context window, without pulling in a second tokenizer just to count.

### Splitting and packing

```python
def chunk_text(doc_id: str, text: str, max_tokens: int = 400, overlap: int = 60) -> list[Chunk]:
    sections = _split_into_sections(text)
    pieces: list[str] = []
    for section in sections:
        paragraphs = _split_into_paragraphs(section, max_tokens)
        pieces.extend(_pack_by_tokens(paragraphs, max_tokens, overlap))
    return [
        Chunk(id=f"{doc_id}:{i}", index=i, text=piece, n_tokens=count_tokens(piece))
        for i, piece in enumerate(pieces)
        if piece.strip()
    ]
```

`_split_into_sections` looks for numbered headings with a regex (`^\d+(\.\d+)*\s+[A-Z][^\n]{0,80}$`); `_split_into_paragraphs` splits on blank lines. One PDF-specific wrinkle: a PDF page has no blank lines *inside* it (line breaks are just line wraps, not paragraph marks), so a whole page can come back as a single "paragraph" — `_split_into_paragraphs` further splits any block still bigger than `max_tokens` into sentences, so `_pack_by_tokens` (the greedy bin-packer that assembles paragraphs into `max_tokens`-sized chunks with the token overlap) has natural breakpoints instead of falling back to a mid-sentence hard cut.

Chunk `id` is `f"{doc_id}:{index}"` — deterministic and stable across re-runs, which is what makes the `MERGE` in `ingest.py` idempotent (see below).

### Page numbers

Because the input is a PDF, each chunk also records which page(s) it came from (`page_start`, `page_end`), which is what lets the exploration queries below answer "which page is this fact on?". `attach_page_numbers` locates each chunk's text inside the document's full text (matching on whitespace-collapsed copies of both, since packing re-joins text with `"\n\n"` where the original PDF page had single `"\n"` line breaks) and maps the matched character range onto page offsets computed from `Document.pages`.

### Real numbers on the 41-page PDF

```bash
$ uv run python -c "
from graph_rag.documents import load_document
from graph_rag.chunking import chunk_text, attach_page_numbers
d = load_document('data/docs/graphrag_survey_2408.08921.pdf')
chunks = chunk_text(d.id, d.text)
attach_page_numbers(chunks, d.text, d.pages)
print(len(chunks), 'chunks,', sum(c.n_tokens for c in chunks), 'tokens total')
"
146 chunks, 46595 tokens total
```

Token-count histogram (real run, `max_tokens=400`, `overlap=60`):

| token bucket | chunk count |
|---|---|
| 0–100 | 8 |
| 100–200 | 15 |
| 200–300 | 15 |
| 300–400 | 107 |
| 400–500 | 1 |

```
count    146
mean     319.1
std       98.0
min       25
25%      297
50%      362
75%      386
max      458
```

Most chunks land close to the 400-token ceiling — expected, since most of the paper's paragraphs are long enough to need packing all the way up to the limit. The small chunks (under 100 tokens) are typically the last piece of a section (whatever text is left over after packing) or short sections like the abstract's closing line.

## Writing the lexical graph: `graph_rag/ingest.py`

### Constraints

```cypher
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE
CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE
```

A **uniqueness constraint** makes Neo4j reject (or, combined with `MERGE`, deduplicate) more than one node with the same `id` — this is what makes `MERGE (d:Document {id: $id})` an actual "find-or-create" instead of relying on application code to check first. (If you have not used Neo4j constraints before, `knowledge/research_topics/graph_rag/tutorials/neo4j/` covers the basics.)

### `MERGE` vs `CREATE`, and why `UNWIND`

```cypher
MATCH (d:Document {id: $doc_id})
UNWIND $rows AS row
MERGE (c:Chunk {id: row.id})
SET c.index = row.index, c.text = row.text, c.n_tokens = row.n_tokens,
    c.page_start = row.page_start, c.page_end = row.page_end
MERGE (d)-[:HAS_CHUNK]->(c)
```

`CREATE` always makes a new node — running the same ingest twice would double every `Chunk` and `Document`. `MERGE` finds a node matching the given pattern (here, `{id: row.id}`, backed by the constraint above) and only creates it if it does not already exist, then the `SET` after it refreshes the other properties either way. This is what makes `ingest_path` **idempotent**: running it once or five times against the same file produces the same graph (verified below).

`UNWIND` turns a list Cypher parameter into one row per element *inside a single query* — so all 146 chunks are written in one round-trip to Neo4j instead of 146 separate `MERGE` statements, each paying the network latency of a query. The same batching is used for the `NEXT_CHUNK` chain:

```cypher
UNWIND $pairs AS pair
MATCH (a:Chunk {id: pair.prev}), (b:Chunk {id: pair.next})
MERGE (a)-[:NEXT_CHUNK]->(b)
```

### Handling a changed document

If a document is re-ingested at the same path but its content changed (different `sha256` at the same `id`), its old chunks are deleted before new ones are written:

```python
def _delete_old_chunks(doc_id: str) -> None:
    run("MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) DETACH DELETE c", id=doc_id)
```

This is a blunt instrument: it wipes every chunk unconditionally, including any domain-graph data (entities, relationships) that later chapters attach via `MENTIONS` from those chunks. **Chapter 10 refines this** into an update that only removes what the deleted chunks uniquely supported, using the `chunk_ids` provenance described in `01_concepts.md`. For chapter 02 there is no domain graph yet, so the blunt version is safe.

### Running it

```bash
$ just ingest path="data/docs"
uv run python -m graph_rag.ingest data/docs --max-tokens 400
data/docs/graphrag_survey_2408.08921.pdf: document b742937d… 'Graph Retrieval-Augmented Generation: A Survey' -> 146 chunks
```

`just ingest` (see `project/justfile`) accepts a file or a directory (it walks it for `.pdf`/`.md`/`.txt`), and an optional `--max-tokens`.

## Exploring the result

Five real queries against the graph produced by the run above.

**1. Chunk count and total tokens:**
```cypher
MATCH (c:Chunk) RETURN count(c) AS n_chunks, sum(c.n_tokens) AS total_tokens
```
```
n_chunks, total_tokens
146, 46595
```

**2. The first chunk:**
```cypher
MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk {index: 0})
RETURN d.title AS title, c.id AS id, c.n_tokens AS n_tokens, left(c.text, 120) AS preview
```
```
title: "Graph Retrieval-Augmented Generation: A Survey"
id: "b742937d...:0"
n_tokens: 396
preview: "Graph Retrieval-Augmented Generation: A Survey\nBOCI PENG∗, School of Intelligence Science and Technology, Peking Univers"
```

**3. Walk `NEXT_CHUNK` from chunk 10, three hops forward:**
```cypher
MATCH (c0:Chunk {index: 10})-[:NEXT_CHUNK*0..3]->(c)
RETURN c.index AS idx, c.page_start AS page_start ORDER BY idx
```
```
idx, page_start
10, 4
11, 4
12, 5
13, 5
```
The chain walks forward through the document exactly in reading order, and the page numbers increase monotonically — chunk 12 is the first one on page 5.

**4. Chunks that mention "knowledge graph", with pages:**
```cypher
MATCH (c:Chunk) WHERE toLower(c.text) CONTAINS 'knowledge graph'
RETURN c.index AS idx, c.page_start AS page_start, c.page_end AS page_end LIMIT 5
```
```
idx, page_start, page_end
1, 1, 1
4, 2, 2
5, 2, 3
9, 4, 4
13, 5, 5
```
This is plain keyword search over `Chunk.text` (no vector index yet — that's chapter 07); it's already enough to jump straight to the pages that discuss knowledge graphs.

**5. Idempotency demo — run `just ingest` a second time, counts unchanged:**
```bash
$ just ingest path="data/docs"
data/docs/graphrag_survey_2408.08921.pdf: document b742937d… 'Graph Retrieval-Augmented Generation: A Survey' -> 146 chunks
```
```cypher
MATCH (d:Document) RETURN count(d) AS documents
```
```
documents
1
```
`Document`, `Chunk` and `HAS_CHUNK`/`NEXT_CHUNK` counts are identical before and after the second run (see `test_ingest_is_idempotent` in `tests/test_02_ingest.py`, which asserts this directly).

## Pitfalls

- **`Document.id` depends on the path string.** The first version of `documents.py` hashed the path exactly as given, so ingesting `data/docs/x.pdf` from the project root and `/abs/path/data/docs/x.pdf` from a test created *two* `Document` nodes for the same file — caught by this chapter's own test suite. The fix: hash the *resolved absolute path* (`path.resolve()`), so the id only depends on which file it is, not on how it was referred to.
- **Two-column layouts.** This survey is single-column, so `pypdf`'s extraction reads top-to-bottom correctly. A two-column PDF would need per-column extraction (or a layout-aware library) — `pypdf`'s plain `extract_text()` would otherwise interleave the two columns mid-sentence.
- **Tables** extract as loose, unstructured lines of numbers and headers with no row/column structure preserved — they chunk like prose but read like noise. Detecting and either skipping or specially formatting tables is out of scope here.
- **The References section** is 100+ numbered citations that chunk just like body text, taking up real "context budget" for something that is rarely useful to retrieve for a content question. A reasonable improvement (not implemented here, to keep this chapter focused on the lexical graph) is to detect a `References` heading and drop everything after it before chunking.
- **Huge chunks**: a paragraph bigger than `max_tokens` on its own (rare in this paper, but common in e.g. a long code listing or a table row extracted as one line) forces a hard token-level split, which can cut mid-sentence — the one trade-off heading/paragraph-aware chunking does not fully avoid.

## Key takeaways
- The lexical graph (`Document`, `Chunk`, `HAS_CHUNK`, `NEXT_CHUNK`) is built once, purely from document structure, before anything about the document's *content* is considered.
- PDF text needs real cleaning — hyphenated line breaks, repeated headers/footers, page numbers — before it is usable text; this is document-format-specific work that Markdown/text input mostly skips.
- Heading-aware chunking with a token overlap gets natural, right-sized chunks (146 chunks, mean 319 tokens, for this 41-page PDF) without the cost of a semantic, embedding-per-sentence approach.
- `MERGE` (backed by uniqueness constraints) plus `UNWIND` batching makes ingestion both idempotent and fast: one round-trip writes all 146 chunks, and running `just ingest` twice leaves the graph unchanged.
- Provenance groundwork here (`page_start`/`page_end`, deterministic chunk ids) is what later chapters build citations and incremental updates on top of.

Next: [03_schema_discovery.md](03_schema_discovery.md) — letting the LLM propose entity types, relationship types and properties from samples of these chunks, then freezing that schema before bulk extraction.
