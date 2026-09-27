# Graph RAG tutorial — Q&A

Questions and answers collected during Q&A sessions about the Graph RAG tutorial
(`knowledge/research_topics/graph_rag/tutorials/graph_rag/`). Each entry is `question > answer`.

Session started: 2026-08-29

---

**Q: What is the phenomenon sometimes called "lost in the middle"?** (from `01_concepts.md`)

> "Lost in the middle" is the observation that LLMs (Large Language Models) do not read a long prompt evenly. When the answer to a question sits at the very **beginning** or the very **end** of the context, models find it reliably; when the same fact is buried in the **middle** of a long context, accuracy drops sharply — the model behaves as if it had not seen it. Plotted as "accuracy vs. position of the relevant text", the result is a U-shaped curve.
>
> The name comes from the 2023 paper *"Lost in the Middle: How Language Models Use Long Contexts"* (Liu et al., Stanford / UC Berkeley), which tested models on multi-document question answering and key-value retrieval. It showed that a bigger context window does not mean the model *uses* all of that window well: padding the prompt with irrelevant text made answers worse even when everything technically fit.
>
> Why it matters for RAG: this is the second reason the tutorial gives for retrieving instead of pasting the whole corpus into the prompt. Even if the documents fit in the context window, a short, relevant context beats a long, diluted one. Retrieval acts as a filter — find the handful of chunks that matter, put only those in the prompt — so the important text is never "in the middle" of a lot of noise.
>
> Practical consequences in the tutorial: keep the number of retrieved chunks small and ranked; put the highest-scored evidence first (local search in chapter 08 ranks relationships and chunks before building the context); and for whole-corpus questions, summarise first (community summaries in chapter 09) instead of stuffing every chunk into one prompt. Curiously, the survey PDF itself cites this paper, so `Lost in the Middle: How Language Models Use Long Contexts` also appears as a `Paper` entity in the extracted graph (chapters 07–08).

---

**Q: In `_delete_old_chunks` (`project/src/graph_rag/ingest.py:35`) — `MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) DETACH DELETE c` — what happens to the other nodes that were attached to those chunks, especially ones that become orphaned?**

> Short answer: **`_delete_old_chunks` itself does nothing about them.** `DETACH DELETE c` removes each `Chunk` node together with *all* of its relationships — `HAS_CHUNK`, `NEXT_CHUNK`, and every `Chunk -[:MENTIONS]-> Entity` edge — but the nodes on the other end are untouched. So the `Entity` nodes the chunk mentioned stay in the graph, and any entity that was mentioned *only* by this document's chunks is left with zero `MENTIONS` edges: an orphan with no provenance. Likewise, entity-to-entity relationships still carry the deleted chunk ids in their `chunk_ids` list, which now point at chunks that no longer exist (dangling provenance).
>
> Why the code is written this way: `_delete_old_chunks` is a **chapter-02 function**, written when the graph had only the lexical layer (Document, Chunk) and no entities existed yet. Its only job is "the file changed (different sha256), so throw away the old chunking before writing the new one". At that stage there is nothing to orphan.
>
> Where the orphans are actually handled: **`remove_document` in `updates.py` (chapter 10)**. It is the function you should use once a domain graph exists, and it deletes in a deliberate order so that nothing unsupported survives:
> 1. Collect this document's chunk ids.
> 2. Strip those ids from `r.chunk_ids` on every `Entity -> Entity` relationship (provenance from chapter 05).
> 3. Delete relationships whose `chunk_ids` list is now empty — nothing else supports them.
> 4. `DETACH DELETE` the chunks, then the `Document` node.
> 5. Delete every `Entity` that no longer has any incoming `MENTIONS` from any chunk (`MATCH (e:Entity) WHERE NOT (:Chunk)-[:MENTIONS]->(e) DETACH DELETE e`).
> 6. Remove the per-chunk extraction cache files on disk.
>
> Entities that are still mentioned by *another* document keep living — removal only deletes what provenance says is now unsupported. The chapter proves this on a real run: after `add` then `remove` of a second PDF, counts return exactly to Document=1, Chunk=146, Entity=1731, relationships=1669.
>
> And `update_document` (changed file) does **not** call `_delete_old_chunks`; it calls `remove_document(...)` and then `add_document(...)`, so orphans are cleaned up. The `_delete_old_chunks` branch inside `ingest_file` only fires if you run the raw chapter-02 `ingest` on a changed file directly — in which case you *will* leave orphan entities and dangling `chunk_ids`. Two things stay stale even after a correct removal (documented in chapter 10): **community membership/summaries** (communities are only marked `stale = true`, never patched) and **entity-resolution merges** made across old entities.
>
> Cleanup if you did orphan things by accident: run the last two steps of `remove_document` by hand —
> `MATCH (:Entity)-[r]->(:Entity) WHERE size(r.chunk_ids) = 0 DELETE r` and
> `MATCH (e:Entity) WHERE NOT (:Chunk)-[:MENTIONS]->(e) DETACH DELETE e`
> (after first filtering out chunk ids that no longer exist). A defensive improvement to the tutorial would be to make `ingest_file` call `remove_document` instead of `_delete_old_chunks` when a domain graph is present, or to at least note the limitation in chapter 02.

---

**Q: What does this pattern with `app` and its wrapper do?** (`project/src/graph_rag/ingest.py:123-135`)
```python
app = typer.Typer(add_completion=False)

@app.command()
def main(
    path: Path = typer.Argument(..., help="A file or a directory of .pdf/.md/.txt files"),
    max_tokens: int = typer.Option(400, help="Max tokens per chunk"),
    overlap: int = typer.Option(60, help="Token overlap between consecutive chunks"),
) -> None:
    ingest_path(path, max_tokens=max_tokens, overlap=overlap)

if __name__ == "__main__":
    app()
```

> This turns the module into a **command-line tool** using **Typer**, a Python library that builds a CLI (Command-Line Interface) from a plain function's signature. Instead of parsing `sys.argv` by hand, you describe the parameters as typed function arguments and Typer generates the argument parsing, type conversion, defaults, validation and `--help` text for you.
>
> Piece by piece:
> - `app = typer.Typer(add_completion=False)` — creates the CLI application object. `add_completion=False` removes the auto-generated `--install-completion` / `--show-completion` options (shell tab-completion setup) so `--help` stays clean; they are noise for a tutorial script.
> - `@app.command()` — the *wrapper* (a decorator). It registers `main` as a command of the app. Typer reads the function's signature and builds the parser from it: parameter names become option names (`max_tokens` → `--max-tokens`), type hints (`Path`, `int`) become converters and validators, default values become defaults, and `help=` strings become the help text.
> - `typer.Argument(..., help=...)` — declares `path` as a **positional argument** (you write it bare: `ingest data/docs`). The `...` (Ellipsis) means "required, no default". Because the type is `Path`, Typer converts the string into a `pathlib.Path` for you.
> - `typer.Option(400, help=...)` — declares `max_tokens` as a **named option** with default 400: `--max-tokens 300`. Same for `--overlap`. If someone passes `--max-tokens abc`, Typer rejects it with a clear error before your code runs.
> - the body just calls the real library function `ingest_path(...)`. That separation matters: the logic lives in importable functions (`ingest_path`, `ingest_file`) that other modules and tests use directly, and the CLI is a thin shell over them.
> - `if __name__ == "__main__": app()` — only when the file is executed as a script (`python -m graph_rag.ingest ...`), run the app: parse the command line, call `main`, exit with a status code. When the module is *imported* (e.g. `from graph_rag.ingest import ingest_file` in `updates.py`), this block does not run, so importing has no side effects.
>
> Because there is exactly **one** `@app.command()`, Typer treats it as the single default command: you call `python -m graph_rag.ingest data/docs --max-tokens 400`, not `... main data/docs`. Modules with several commands (e.g. `updates.py` with `add`, `remove`, `update`) require the subcommand name: `python -m graph_rag.updates add <path>`.
>
> How it is used in the tutorial: the `justfile` recipe `ingest` runs
> `uv run python -m graph_rag.ingest {{path}} --max-tokens {{max_tokens}}`, so `just ingest data/docs` ends up in this `main` function. Try `uv run python -m graph_rag.ingest --help` to see the generated help page.

---

**Q: Are we ignoring images that might be in the documents we insert in this tutorial?**

> **Yes — completely, and silently.** The PDF loader (`project/src/graph_rag/documents.py:_load_pdf`) uses `pypdf`'s `page.extract_text()`, which returns only the text layer of each page. Embedded images, figures, diagrams and charts are never read, never described and never stored; the pipeline does not even record that a page *had* an image. The same is true for Markdown input: `![alt](file.png)` links are kept as plain text (the alt text and the file name), but the image file itself is never opened.
>
> This is not a small thing for the tutorial's own document: the 41-page survey PDF contains **21 embedded images** (architecture figures, the GraphRAG taxonomy diagrams, comparison charts) and the second PDF contains 2. Any fact that lives only in a figure — a pipeline diagram, an axis label, a number in a chart — is invisible to extraction, so no entities or relationships come from it and no question about it can be answered. Text *around* a figure (captions like "Fig. 2. The overview of GraphRAG...") is extracted, because captions are ordinary text on the page, so the figure's title usually survives even though its content does not.
>
> Why the tutorial does this: the pipeline is deliberately text-only to keep the focus on the graph part (schema discovery, extraction, resolution, communities). Chapter 02's "Pitfalls" section lists the related text-layout limits — two-column layouts, tables that extract as loose lines, the References section — but does **not** mention images at all, which is a documentation gap worth fixing.
>
> Related blind spots of the same kind: **scanned PDFs** (image-only pages with no text layer) give `extract_text() == ""`, so `_load_pdf` skips the page entirely and the document may end up with zero chunks — with no warning. **Tables** partially survive as noisy text. **Math** often extracts as garbled symbols.
>
> How to add images if you need them (in increasing cost):
> 1. *Detect and warn:* count `page.images` per page in `_load_pdf` and log pages that have images but little text — cheap, and at least makes the loss visible.
> 2. *OCR* (Optical Character Recognition) for scanned pages, e.g. Tesseract or `ocrmypdf` before ingestion — recovers text that is rendered as pixels.
> 3. *Caption images with a vision LLM:* extract each image (`pypdf` `page.images`, or PyMuPDF), send it to a multimodal model (e.g. `qwen3.6-vl` / `llava` via Ollama) with a prompt like "describe this figure for a text search index", and insert the description into the page text as a new paragraph such as `[Figure on page 6: ...]`. It then becomes a normal chunk: it gets embedded, extracted and cited like any other text. Store `source: "image"` on those chunks so citations are honest.
> 4. *Layout-aware parsers* (Docling, Marker, Unstructured) that output Markdown with tables, figures and captions properly separated — the most robust option for mixed documents, at the price of a heavier dependency.
>
> Option 3 fits this pipeline best because everything downstream already works on chunks; the only change is in `documents.py`.

---

**Q: Chapter 03 says "the Pydantic-to-JSON-schema *trick* that forces the LLM's reply into a shape Python can load directly." Why "trick"? Isn't this exactly how structured output works?**

> You are right — it *is* exactly structured output, and "trick" is the wrong word. What `llm.chat_json` (`project/src/graph_rag/llm.py:55`) does is the standard, documented mechanism:
>
> 1. `schema.model_json_schema()` — Pydantic exports the model class as a **JSON Schema** (the standard format for describing the shape of JSON: field names, types, required fields, enums).
> 2. That schema is passed as Ollama's **`format`** parameter. Ollama applies **constrained decoding** (also called grammar-guided sampling): at every generation step the tokens that would break the schema are masked out, so the model *cannot* emit anything but valid JSON of that shape. This is the same feature OpenAI calls "Structured Outputs" (`response_format` with `json_schema`), Anthropic calls structured outputs / `output_format`, and vLLM/llama.cpp expose as guided decoding or GBNF grammars.
> 3. `schema.model_validate_json(content)` — Pydantic parses the reply back into a typed Python object.
>
> Nothing here is a hack or an undocumented behaviour. The word "trick" in the tutorial is meant in the colloquial sense of "the neat move that makes this work" — namely that the same Pydantic class serves three purposes at once: it is the schema sent to the LLM, the parser/validator for the reply, and the Python type the rest of the pipeline works with. You write the model once and never hand-write JSON schema or parsing code. But the word suggests something clever or fragile, which is misleading for learners, and it should be replaced by "structured output" (or "constrained JSON output").
>
> Two genuine subtleties worth knowing, which is probably why the author flagged it:
> - Constrained decoding guarantees **syntactic** validity (valid JSON, right fields, right types), not **semantic** correctness — the model can still produce an empty list, a wrong value, or invented content in the right shape. That is why `chat_json` still wraps parsing in a retry and why chapters 04–05 validate and normalise the results afterwards. In practice the retry exists because Ollama's constraint is not perfectly airtight with small models (truncated output at `num_predict`, or a schema feature such as `$ref`/`format` that the grammar does not enforce).
> - You often want to send the LLM a **narrower schema than your storage model**. Chapter 04's `ChunkExtraction` has fields like `chunk_id`, `model`, `prompt_version`, `extracted_at` that Python fills in; the LLM is given a smaller model without them, otherwise a small model will happily invent a `chunk_id`. Having two Pydantic classes — "what the LLM answers" vs "what we store" — is a good habit for structured output in general.
>
> Suggested wording change for `03_schema_discovery.md` (line 6 and heading at line 96): "the Pydantic-to-JSON-schema trick" → "structured output: a Pydantic model exported as JSON Schema and passed as Ollama's `format`".

---

**Q: In `RelationshipType` (`project/src/graph_rag/schema_discovery.py:49-54`), are `source_types` and `target_types` entity types?**

> Yes. `source_types` and `target_types` are lists of **entity type names** — strings that must match the `name` of an `EntityType` in the same `GraphSchema` (the `entity_types` list). They say *which kinds of nodes* a relationship of this type may connect, and in which direction: a relationship goes **from** a node whose label is in `source_types` **to** a node whose label is in `target_types`.
>
> The three classes fit together like this (`GraphSchema` holds both lists):
> - `EntityType` = a **node label** (`Method`, `Dataset`, `Person`, …), with its own `properties` and `examples`.
> - `RelationshipType` = a **relationship type** (`EVALUATED_ON`, `PROPOSED_BY`, …), its `description`, optional `properties` that live on the relationship itself, and the allowed endpoint labels.
> - `source_types` / `target_types` are the **domain and range** of the relationship, in ontology terms.
>
> Real example from the frozen schema (`project/data/extracted/schema.json`), where the entity types are `Method, KnowledgeGraph, Dataset, Task, Metric, Organization, Person, Paper, Technique, Domain`:
> - `PROPOSED_BY`: `source_types=["Method"]`, `target_types=["Person", "Organization"]` → `(:Method)-[:PROPOSED_BY]->(:Person|Organization)`
> - `EVALUATED_ON`: `["Method"]` → `["Dataset"]`
> - `SOLVES_TASK`: `["Method"]` → `["Task"]`
>
> A list rather than a single value because one relationship type often has several legal endpoints (a method can be proposed by a person *or* an organisation). This is the same idea as Neo4j's own schema visualisation (`CALL db.schema.visualization()`), which shows which labels a relationship type connects.
>
> Why they are plain `str` and not a stricter type: the LLM proposes entity types and relationship types in the *same* reply, so a `Literal[...]`/enum of allowed names cannot exist before the answer arrives. Consistency is instead checked afterwards — and this is exactly where the refine step (chapter 03) and the extraction validation (chapter 04) matter: a relationship whose `source_types` names a type that is not in `entity_types` (e.g. the LLM wrote `Model` but the entity type is `Method`) is a schema error to fix before freezing. Downstream, chapter 04 uses these lists in the extraction prompt to tell the model what relationships are allowed between which entities, and chapter 05 writes them as dynamic relationship types between nodes carrying the corresponding labels.

---

**Q: What do these Cypher commands do?** (`project/src/graph_rag/graph_writer.py:84,102`, chapter 05)
```cypher
SET n:$(e.type)
MERGE (a)-[rel:$(r.type)]->(b)
```

> Both use Neo4j's **dynamic label / relationship-type expressions**, added in Neo4j **5.26** (this tutorial runs 5.26.29). The syntax `:$(expr)` means: *evaluate the expression inside the parentheses at runtime and use the resulting string as the label or relationship type*.
>
> - `SET n:$(e.type)` — adds a **label** to node `n`. `e` is the current row of `UNWIND $entities AS e`, and `e.type` is the entity type the LLM extracted (e.g. `"Method"`, `"Dataset"`). So for a row with `type = "Method"` this is equivalent to writing `SET n:Method`. The node keeps its existing `Entity` label (from `MERGE (n:Entity {...})`), so it ends up as `(:Entity:Method)`.
> - `MERGE (a)-[rel:$(r.type)]->(b)` — creates a **relationship** between two already-matched entity nodes, or reuses it if one of that type already exists between them (that is what `MERGE` means). `r.type` is the relationship type string from extraction, e.g. `"EVALUATED_ON"`, so it behaves like `MERGE (a)-[rel:EVALUATED_ON]->(b)`. The `ON CREATE` / `ON MATCH` lines after it then set `weight` and accumulate `chunk_ids` (provenance).
>
> Why this is needed: in classic Cypher a label or relationship type is a **literal token fixed at query-parse time** — you write `:Person`, and `SET n:$type` with a bare parameter has always been a **syntax error**. That is a problem for this tutorial, whose whole point is that the schema is *discovered from the document* (chapter 03): the labels `Method`, `Dataset`, `Person`, … are only known at runtime, from data. Before 5.26 there were two workarounds:
> 1. build the query string in Python (`f"SET n:{etype}"`) — a **Cypher injection** risk, and one query per distinct type, so no single `UNWIND` batch;
> 2. use APOC procedures that take the name as an ordinary string: `CALL apoc.create.addLabels(n, [e.type])` and `CALL apoc.merge.relationship(a, r.type, {...}, {...}, b)`. This works but needs the plugin and reads less like normal Cypher.
>
> `:$(expr)` removes both problems: the value comes from a parameter, so there is no injection, and because it is evaluated per row you can write **one batched `UNWIND` query** for all entity types and all relationship types at once. The tutorial uses the new syntax everywhere and keeps the APOC form only as a comment (`_ENTITY_LABEL_QUERY_APOC`) so you recognise the older idiom in other people's code.
>
> Two details worth noticing in the tutorial's use:
> - `SET n:$(e.type)` runs on **every** sighting (create *and* match). If the LLM typed the same entity as `Method` in one chunk and `Technique` in another, the node accumulates **both** labels (`:Entity:Method:Technique`). That is deliberate — the extra label is a visible signal that chapter 06 (entity resolution) uses, rather than a duplicate node, which is why the `MERGE` key is `normalized_name` alone and not `(type, normalized_name)`.
> - The expression must evaluate to a valid, non-empty name; chapter 04's validation normalises types to `PascalCase` / `UPPER_SNAKE_CASE` and drops unknown ones before they reach these queries.
>
> Requirements: Neo4j **≥ 5.26** (or 2025.x). On older servers this exact syntax fails to parse; use the APOC form instead.

---

**Q: Summarise the steps required to build a Graph RAG — short, simple list.**

> Two phases: **build** the graph once (indexing), then **query** it.
>
> Build (indexing):
> 1. **Load documents** — read PDFs/Markdown/text into clean plain text (chapter 02).
> 2. **Chunk** — cut the text into ~300-400-token pieces with overlap; store `Document` and `Chunk` nodes in Neo4j (chapter 02).
> 3. **Discover a schema** — show the LLM a sample of chunks and let it propose entity types (`Method`, `Dataset`, …) and relationship types (`EVALUATED_ON`, …); review and freeze it (chapter 03).
> 4. **Extract** — for every chunk, ask the LLM for entities and relationships as structured JSON matching the schema; cache results on disk (chapter 04).
> 5. **Write the graph** — `MERGE` entities as nodes with dynamic labels, relationships with dynamic types, and `Chunk -[:MENTIONS]-> Entity` provenance (chapter 05).
> 6. **Resolve duplicates** — merge "GraphRAG" / "Graph RAG" / "Graph-RAG" into one node using normalisation, embedding similarity and an LLM judge; keep aliases (chapter 06).
> 7. **Embed and index** — embed chunks and entities, create vector + full-text indexes for hybrid search (chapter 07).
> 8. **Detect communities and summarise** — cluster the graph (Leiden) and write an LLM summary per community for "big picture" questions (chapter 09).
>
> Query (retrieval + generation):
> 9. **Local search** (specific questions) — embed the question → find matching chunks/entities → walk their graph neighbourhood → assemble context → LLM answers with citations (chapter 08).
> 10. **Global search** (theme questions) — map-reduce over community summaries: each summary answers partially, then one final answer is combined (chapter 09).
>
> Keep it alive:
> 11. **Update incrementally** — add/remove/change one document using provenance instead of rebuilding everything; mark affected communities stale (chapter 10).
> 12. **Evaluate** — a small question set with an LLM-as-judge, plus cost/latency tracking (chapter 10).
>
> One-liner: *text → chunks → LLM-extracted entities & relationships → deduplicated graph in Neo4j → (vector + graph) retrieval → LLM answer.* In this project all of this is `just pipeline` followed by `just ask` / `just ask-global`.

---

**Q: Is vector similarity between the question and a chunk the best way to find relevant chunks? A question and a chunk are different formats, written by different people in different styles. Should they be normalised — e.g. generate a standardised question for every chunk with a model, and transform the incoming question the same way?**

> Your concern is real and has a name: **asymmetric retrieval** — a short question ("how does GraphRAG differ from vector RAG?") and a long declarative passage do not look alike, so comparing their raw embeddings is comparing apples to pears. The field has developed several answers, and your proposal is one of them. Ranked by cost:
>
> 1. **Asymmetric embedding models (cheapest, and the tutorial is currently missing it).** Modern retrieval embedders are trained on (question, passage) pairs precisely so that a question lands near the passage that answers it, even though they look nothing alike. Many of them expose this through **task prefixes**: `nomic-embed-text`, the model this tutorial uses, expects `search_query: <question>` for questions and `search_document: <text>` for passages (other models: E5's `query:`/`passage:`, BGE's query instruction). The tutorial's `embed()` (`project/src/graph_rag/llm.py`) sends bare text for both chunks (`embeddings.py:70`) and questions (`embeddings.py:151,165`), so it does **not** use the model's built-in normalisation. Adding the two prefixes is a one-line change per call site and typically improves recall measurably — this is the first fix to make. (Chunk embeddings would need to be recomputed once.)
>
> 2. **Hybrid search.** Vector similarity is not the only signal. The tutorial already combines vector search with **full-text (Lucene, keyword) search** using Reciprocal Rank Fusion (`hybrid_search_entities`, chapter 07) for *entities*; exact terms such as "HippoRAG" or "Recall@K" are matched lexically even when the embedding is fuzzy. Chunks, however, are still fetched by vector only (`search_chunks`) — extending hybrid search to chunks is a second cheap improvement.
>
> 3. **Your proposal: generate questions per chunk ("doc2query" / hypothetical questions).** Yes, this is an established technique: for every chunk, ask an LLM "write 3–5 questions this passage answers", embed *those questions* (kept alongside the chunk, e.g. as `Question` nodes or an extra vector property), and at query time match the user's question against the generated questions — question-to-question, same format, same style. Benefits: the comparison is symmetric; a chunk gets several "entry points"; it helps most with small or weak embedding models. Costs: one LLM call per chunk at index time (146 chunks here, ~40 s each with the local model ≈ 1.5 h extra), more vectors to store, and a risk that the generated questions miss what a real user asks. The variant "also rewrite the *incoming* question into a standard form" is **query rewriting**; it helps for messy or conversational input, but every rewrite adds an LLM call to query latency and can drift from the user's intent, so apply it lightly (e.g. fix typos, resolve "it"/"that" from chat history).
>
> 4. **HyDE (Hypothetical Document Embeddings) — the mirror image of your idea.** Instead of turning chunks into questions, turn the *question* into a fake answer: ask the LLM to write a short hypothetical passage answering the question, embed *that*, and search chunks with it. Now both sides are passages. No index-time cost, one extra LLM call per query, works with the existing chunk embeddings. Weak point: if the model knows nothing about the topic, the hallucinated passage may point in the wrong direction.
>
> 5. **Re-ranking.** Retrieve 30–50 candidates cheaply by vector/hybrid search, then score each (question, chunk) pair with a **cross-encoder re-ranker** (e.g. `bge-reranker`) that reads both texts together and is trained exactly for question-vs-passage relevance. This is the most reliable quality boost in practice and is the standard second stage in production RAG.
>
> How Graph RAG changes the picture: in this tutorial the vector hit is only the **seed**. Local search (chapter 08) goes question → entities (hybrid) → 1–2 hop graph neighbourhood → chunks that mention those entities. The graph walk compensates for imperfect vector matching, because a chunk can be reached through the entities it talks about rather than through its own embedding. And global search (chapter 09) does not use question-to-chunk similarity at all — it map-reduces over community summaries.
>
> Recommendation for this project, in order: (a) add the `search_query:`/`search_document:` prefixes and re-embed; (b) extend hybrid (vector + full-text) search to chunks; (c) add a cross-encoder re-ranker over the top-30 candidates; (d) only then consider doc2query or HyDE, and measure each step with the chapter-10 evaluation harness rather than by intuition — the whole point of that harness is to make choices like this one testable.

---

