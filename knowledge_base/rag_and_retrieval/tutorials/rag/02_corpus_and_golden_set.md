# 02 — Corpus and golden set: parsers compared, chunk schema, golden questions, metrics, scoreboard

## What you will learn
- Why the choice of PDF → Markdown parser matters for RAG (chunking, headings, tables), with real
  timing/quality numbers for `pypdf`, `pymupdf4llm` and Docling on two table-heavy papers.
- The chunk and document data model (`Chunk`, `Document`, deterministic `chunk_id`) every later
  chapter's chunker must produce.
- How the ≈40-question golden set was generated with the LLM (Large Language Model), reviewed by hand, and what got cut.
- The exact definitions of hit@k, recall@k, MRR (Mean Reciprocal Rank) and nDCG@k (normalized
  Discounted Cumulative Gain), worked through on one real question.
- The two judge functions (correctness, faithfulness) that score every generated answer, local
  `qwen3.8:27b` again, and their limitations.
- The two "anchor" scoreboard rows — no retrieval at all, and oracle (perfect) retrieval — and what
  the gap between them does and does not tell you.

This is the one chapter every later chapter depends on: the corpus, the golden set, the metric
definitions and the scoreboard format are frozen here. A later chapter may fix a bug in `evaluate.py`,
but it must say so and re-run the anchors — otherwise old and new scoreboard rows would silently stop
being comparable.

## Parsing: three parsers, the same two papers

Chapter 00 parsed all 12 PDFs with `pypdf` — reliable, dependency-light, but it returns plain text with
no headings and no table structure. That is a real cost once we chunk by section (chapter 04) and once
we ask a question whose answer sits in a table (several papers in this corpus report their key results
that way). `project/src/rag_tutorial/parsers.py` compares three parsers on two table-heavy papers —
**RAPTOR** (2401.18059) and **GraphRAG** (2404.16130), both of which report results in dense multi-row
tables:

```python
def parse_pypdf(pdf_path) -> str: ...        # plain text, page by page, dehyphenated
def parse_pymupdf4llm(pdf_path) -> str: ...  # pymupdf4llm.to_markdown(..., page_chunks=True)
def parse_docling(pdf_path) -> str: ...      # docling.document_converter.DocumentConverter
```

Real output of `just parse-compare`:

| paper | parser | seconds | characters | tokens | `#` headings |
|---|---|---:|---:|---:|---:|
| RAPTOR | pypdf | 0.2 | 77,513 | 20,065 | 0 |
| RAPTOR | pymupdf4llm | 5.7 | 81,751 | 21,366 | 25 |
| RAPTOR | docling | 19.6 | 85,806 | 20,148 | 29 |
| GraphRAG | pypdf | 0.2 | 89,981 | 23,295 | 0 |
| GraphRAG | pymupdf4llm | 3.0 | 94,570 | 25,886 | 52 |
| GraphRAG | docling | 32.0 | 106,103 | 23,633 | 48 |

`pypdf` finds zero headings because it only extracts a flat text stream — every `#` in the corpus table
above comes from the other two parsers actually detecting the paper's layout. Docling's first run also
downloads its layout and OCR models (a one-time cost, not counted differently above since the models
were already cached from a warm-up run — expect an extra 30–60s the very first time you run it).

**Same table (RAPTOR's Table 1), five lines from each parser's output:**

`pypdf` (flattened, no columns):
```
Model ROUGE BLEU-1 BLEU-4 METEOR
SBERT with RAPTOR 30.87% 23.50% 6.42% 19.20%
SBERT without RAPTOR 29.26% 22.56% 5.95% 18.15%
BM25 with RAPTOR 27.93% 21.17% 5.70% 17.03%
BM25 without RAPTOR 23.52% 17.73% 4.65% 13.98%
```

`pymupdf4llm` (reconstructed as a Markdown table):
```
|**Model**|**ROUGE**|**BLEU-1**|**BLEU-4**|**METEOR**|
|---|---|---|---|---|
|**SBERT with RAPTOR**|**30.87%**|**23.50%**|**6.42%**|**19.20%**|
|SBERT without RAPTOR|29.26%|22.56%|5.95%|18.15%|
|**BM25 with RAPTOR**|**27.93%**|**21.17%**|**5.70%**|**17.03%**|
```

`docling` (also a Markdown table, no bold markers):
```
| Model                | ROUGE   | BLEU-1   | BLEU-4   | METEOR   |
|----------------------|---------|----------|----------|----------|
| SBERT with RAPTOR    | 30.87%  | 23.50%   | 6.42%    | 19.20%   |
| SBERT without RAPTOR | 29.26%  | 22.56%   | 5.95%    | 18.15%   |
```

Both `pymupdf4llm` and Docling correctly reconstruct the table; only `pypdf` loses the column
structure entirely (a chunk built from that text would mash "SBERT with RAPTOR" and "30.87%" into an
unstructured run-on sentence). On timing, `pymupdf4llm` was **3–7x faster** than Docling on these two
papers for output that detects roughly the same number of headings and the same table quality.

**License callout:** `pymupdf4llm` is built on PyMuPDF, which is **dual-licensed AGPLv3 /
commercial** (Artifex) — free to use in an open-source project like this tutorial, but a closed-source
commercial product that links it would need a paid license. Docling (IBM) is MIT-licensed, no such
consideration. That is a real, non-technical reason a team might pick Docling anyway even though it is
slower here.

**Winner: `pymupdf4llm`.** For this tutorial's purposes (a from-scratch, from-zero walkthrough,
license already discussed openly) the speed advantage wins; `data/corpus/md/*.md` was re-parsed with
it (`just corpus-parse`, now defaulting to `--parser pymupdf4llm`, `pypdf`/`docling` still available):

| | pages | characters | tokens |
|---|---:|---:|---:|
| all 12 papers, `pymupdf4llm` | 211 | 872,030 | 226,448 |

Total wall time for all 12 papers: **35 seconds** (vs. ~2 seconds for `pypdf`, and Docling would have
taken several minutes at ~20–30s/paper). `corpus.parse --parser docling` and `--parser pypdf` still
work if you want to reproduce the comparison on the full corpus yourself.

## Why headings matter for chunking

A chunk boundary that lands in the middle of a table row, or that separates a heading from its own
section body, produces a chunk that is syntactically valid text but semantically useless — the model
sees `"SBERT with RAPTOR"` with no column headers, or a paragraph with no idea which section of the
paper it came from. `pymupdf4llm`'s `#`-marked headings let chapter 04's Markdown-structure chunker
split *at* section boundaries instead of at an arbitrary character count, and let every chunk carry a
`section` field (`"3 Method > 3.2 Retrieval"`) that a citation can show the reader, not just a raw
character offset.

## The chunk schema (`schema.py`)

Every chunking strategy in every later chapter must produce the same four-field-plus-metadata object:

```python
class Chunk(BaseModel):
    id: str
    paper: str
    section: str
    text: str
    start: int
    end: int
    meta: dict = {}
```

`chunk_id(paper, start, end)` is the first 16 hex characters of `sha1(f"{paper}:{start}:{end}")` — a
**pure function** of the paper id and character offsets, not a random UUID or a row counter. This
matters because retrieval metrics compare *retrieved* chunk ids against *evidence* chunk ids computed
the same way: if the id were random, re-running the same chunker twice would silently produce
different ids for the same text and `hit@k` would compare against the wrong set without erroring.

`detect_sections(text)` walks every `#`-`######` heading, keeps a stack of open ancestors, and assigns
each section a full breadcrumb path (`"3 Method > 3.2 Retrieval"`, resetting the stack when a new
top-level heading starts) — this is what fills a `Chunk`'s `section` field once real chunking exists in
chapter 04. `Document.from_markdown(paper, title, text)` wraps a parsed paper plus its detected
sections.

## Building the golden set

`project/src/rag_tutorial/golden.py generate` asks `qwen3.8:27b` for structured JSON candidates — one
LLM call per candidate, `format=<json schema>`, temperature 0 — for five question types, sampling
~800-token passages from the parsed corpus:

```python
_SINGLE_HOP_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "quote": {"type": "string", "description": "verbatim span (<=300 chars) ..."},
    },
    "required": ["question", "answer", "quote"],
}
```

Every candidate's evidence quote is checked with an **exact, whitespace-normalised substring match**
against the source passage before being kept — a paraphrase would make the evidence useless for
retrieval metrics later, since `retrieval_metrics` needs a literal span to check chunks against:

```python
def quote_in_source(quote: str, source: str) -> bool:
    return _normalize(quote) in _normalize(source)
```

**A real bug found while generating.** The first run of `generate_global` and `generate_unanswerable`
asked the exact same prompt six times in a row (same paper listing, same instructions) at temperature
0 — which is also the exact cache key `rag_tutorial.llm` hashes on. Six calls, one cache entry, **six
byte-identical questions**. The fix was to vary the *content* of the prompt per candidate: a list of
six distinct "focus areas" for `global` questions (e.g. *"which papers propose alternatives to flat
top-k chunk retrieval"*, *"what failure modes are discussed across multiple papers"*) and six distinct
"hooks" for `unanswerable` questions (*"a specific numeric result from a paper published in 2027"*, *"a
question about an unrelated field"*, ...). This is worth knowing generally: **a temperature-0, fully
cached LLM pipeline will silently deduplicate any batch of calls whose prompts are byte-identical** —
if you want N diverse outputs from one static prompt template, the prompt has to actually differ N
ways, not just be called N times.

### The review pass

`golden.py review` prints every kept candidate with its evidence for a human read. Reading all 40
candidates by hand, I removed **4**:

- **`single_hop_005`** — *"What is the name of the GitHub repository where the authors state their
  open source code for the HyDE preprint is available?"* This is trivia about a URL, not about RAG —
  answerable by anyone who can read one sentence, and it doesn't test whether retrieval found the
  *conceptually* relevant passage, just whether it found a string that happens to contain a URL.
- **`comparative_023`** — *"How does the citation format for arXiv preprints in Passage A differ from
  the citation format for arXiv preprints in Passage B?"* Not a real research comparison — the model
  was comparing bibliography formatting conventions between two unrelated reference-list excerpts, an
  artifact of `sample_passage` occasionally landing in a paper's References section.
- **`single_hop_008`** — a "which 2019 paper by X and Y is cited in this paper's references"
  question — same problem as the GitHub one: citation-hunting trivia rather than a RAG-domain fact.
- **`multi_hop_014`** — its evidence for one of the two passages was *"We analyze several
  state-of-the-art open and closed language models..."*, offered as support for *"the paper does not
  explicitly restrict its evaluation to a single language"* — a claim from the **absence** of a
  restriction, not something the passage actually states. Technically verbatim (the quote passed
  `quote_in_source`), but not genuine supporting evidence for the answer.

That left **36** items, split roughly 1:3 `dev`:`test` (every 4th item by final order is `dev`):

| type | dev | test | total |
|---|---:|---:|---:|
| single_hop | 2 | 8 | 10 |
| multi_hop | 2 | 7 | 9 |
| comparative | 2 | 3 | 5 |
| global | 1 | 5 | 6 |
| unanswerable | 2 | 4 | 6 |
| **total** | **9** | **27** | **36** |

Mean question length: 32.5 tokens. All 12 papers are covered by at least one piece of evidence.

Three example questions per type:

- **single_hop**: *"What specific loss function does ColBERTv2 use to distill cross-encoder scores
  into the ColBERT architecture?"* → "KL-Divergence loss"
- **multi_hop**: *"How does the Graph RAG approach's method for handling source documents differ from
  the Dense Passage Retrieval (DPR) approach in terms of the initial processing of text chunks?"*
- **comparative**: *"How does the evaluation of retrieval performance on the BEIR benchmark differ
  between the RAPTOR and ColBERTv2 papers?"*
- **global**: *"Which papers in the corpus focus on evaluating or benchmarking RAG systems, and what
  specific methodologies do they propose for this assessment?"* → cites 2309.15217 (Ragas) plus
  contrasting mentions of 2401.05856 and 2307.03172.
- **unanswerable**: *"How does the ColBERTv2 late interaction mechanism improve the accuracy of
  predicting protein folding structures in the AlphaFold 2 model?"* — plausible-sounding, entirely
  outside the corpus's field.

## The metrics module (`evaluate.py`)

### Retrieval metrics

A chunk **covers** an evidence quote if it is from the same paper *and* either (a) the quote is an
exact, whitespace-normalised substring of the chunk, or (b) at least 80% of the quote's word tokens
are also in the chunk's token set:

```python
def chunk_covers_quote(chunk: Chunk, evidence: dict) -> bool:
    if chunk.paper != evidence["paper"]:
        return False
    if _normalize(evidence["quote"]) in _normalize(chunk.text):
        return True
    quote_tokens = _tokens(evidence["quote"])
    overlap = len(quote_tokens & _tokens(chunk.text)) / len(quote_tokens)
    return overlap >= 0.8
```

Both checks exist for a reason: the exact-substring check is cheap and exact for the common case (the
whole quote is inside the chunk); the 80%-token-overlap check catches a chunk boundary that cuts off a
trailing word or two of the quote, which a strict substring match would unfairly fail.

From these, `retrieval_metrics(retrieved_chunks, evidence, ks=(5, 10))` computes:
- **hit@k** — 1 if *any* evidence quote is covered by a chunk in the top k, else 0.
- **recall@k** — the *fraction* of evidence quotes covered by some chunk in the top k (matters for
  multi-hop/comparative questions with 2 evidence quotes: covering only one gives recall@k = 0.5).
- **MRR** — `1 / rank` of the first chunk (over the whole ranked list, not just top-k) that covers any
  evidence quote; 0 if none does.
- **nDCG@10** — chunks graded 1 (covers ≥1 quote) or 0, `DCG@10 = Σ rel_i / log2(i+1)`, normalised by
  the ideal ordering's DCG.

**Worked example, one real question** (`single_hop_000`, oracle anchor — the retrieved "chunk" is
literally the evidence quote itself, so this is the trivial best case, but the arithmetic is real):

> Q: *"According to the paper, what specific type of human input does Ragas allow users to avoid when
> evaluating RAG architectures?"*
> Evidence: `[2309.15217]` *"With Ragas, we put forward a suite of metrics which can be used to
> evaluate these different dimensions without having to rely on ground truth human annotations."*
> Retrieved (rank 1): the same quote, wrapped in a `Chunk`.

- hit@5 = 1.0 (the one evidence quote is covered by the rank-1 chunk)
- recall@5 = 1.0 (1 of 1 evidence quotes covered)
- MRR = 1 / 1 = 1.0 (first relevant chunk is at rank 1)
- nDCG@10 = 1.0 (the one relevant chunk is already in the ideal position)

For a harder hand-built case (in `tests/test_02_golden.py`) where the relevant chunk is at **rank 2**
instead of rank 1: hit@5 = 1.0, recall@5 = 1.0 still (it *is* in the top 5), but MRR = 1/2 = 0.5, and
nDCG@10 = `(1/log2(3)) / (1/log2(2))` ≈ 0.631 — both metrics correctly penalise the extra rank even
though hit@k/recall@k, being threshold metrics, do not.

### The judges

`judge_correctness(question, reference, answer)` asks the chat model to score an answer 0 / 0.5 / 1
against the reference, with a one-sentence reason, via a JSON schema at temperature 0. **Limitation:**
a coarse 3-point scale collapses "almost right but missing one number" and "completely wrong" into
different buckets only when the judge notices the difference — it is a stand-in for a human rater, not
a replacement for one, and its own rubric ("correct and complete" / "partially correct" / "wrong") is
itself somewhat subjective.

`judge_faithfulness(answer, contexts)` is RAGAS-style: one LLM call splits the answer into atomic
claims, one more LLM call checks each claim against the contexts, and the score is
`supported / total` (an answer with no verifiable claims, e.g. a refusal, scores 1.0 — nothing is
unsupported because nothing was claimed). **Limitation:** faithfulness with an *empty* context list is
vacuously 1.0 too — the no-retrieval anchor below scores perfect faithfulness for exactly this reason,
which says nothing about whether its answers were actually correct.

For `unanswerable` questions, `judge_abstain(question, answer)` replaces correctness: 1 if the answer
recognises it cannot be determined from the documents, 0 if it guesses. **Limitation:** both anchors
below score abstain = 1.0 on every unanswerable test question — but these particular questions (a 2027
paper, a protein-folding non-sequitur) are the *easiest possible* unanswerable cases, since the LLM's
own general knowledge is enough to notice the anachronism or field mismatch without needing the
corpus at all. A harder unanswerable set would ask about something plausible-*and*-absent (e.g. a
specific number from a real paper's real appendix, `unanswerable_005` in our set) — a good target to
watch as later chapters change the retriever.

## `evaluate_run` and the scoreboard

`evaluate_run(name, chapter, answer_fn, retrieve_fn, split="test")` runs every `test`-split question
through `retrieve_fn(item) -> list[Chunk]` then `answer_fn(item, retrieved) -> (answer, contexts,
n_llm_calls)`, times each question, judges the answer, and writes `runs/<name>/{metrics.json,
predictions.jsonl, config.json}`. `just scoreboard` (`scoreboard.py`) collects every `runs/*/metrics.json`
into `runs/scoreboard.md`, sorted by chapter then name, with anchor rows in **bold**.

## The two anchors

- **`02_no_retrieval`**: `retrieve_fn` always returns `[]`; the LLM answers from memory, prompted to
  say so if it doesn't know.
- **`02_oracle`**: `retrieve_fn` wraps each question's gold evidence quotes directly into `Chunk`
  objects (with their paper id) — retrieval cannot fail because it was skipped; this is the upper
  bound on *generation* quality alone.

Both ran on the 27-question `test` split:

| experiment | chapter | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | unanswerable-abstain | LLM calls/q | s/q |
|---|---|---|---|---|---|---|---|---|---|---|
| **02_no_retrieval** | **02** | **0.000** | **0.000** | **0.000** | **0.000** | **0.174** | **1.000** | **1.000** | **1.000** | **0.000** |
| **02_oracle** | **02** | **1.000** | **0.988** | **1.000** | **1.000** | **0.543** | **0.865** | **1.000** | **1.000** | **0.000** |

**Reading the gap.** Oracle's retrieval metrics are ~1.0 by construction — the "retrieved" chunk *is*
the evidence. Its correctness (0.543) is therefore the ceiling any real retriever can reach on this
question set with this generator and this judge: even handed the exact right quote, the model gets
under half the test questions fully correct, because several are multi-hop/comparative questions
needing correct synthesis across two quotes, not just quote lookup. No-retrieval's correctness (0.174)
is *not* zero — the model has genuinely memorised some facts about famous, widely-cited papers (RAG,
DPR) from pretraining, which is exactly why some single-hop questions in the golden set specifically
target lesser-known numbers (CRAG's confidence thresholds, ColBERTv2's loss function) rather than
headline results. One real example, `single_hop_000` ("what human input does Ragas avoid"):

- **No retrieval:** *"I do not have access to the specific paper you are referring to... please
  provide the title or authors..."* — judged correctness 0.5 (names the right general concept,
  manual annotation, but hedges instead of answering) — faithfulness 1.0 trivially (no context, no
  unsupported claims possible).
- **Oracle:** *"According to the excerpt from paper [2309.15217], Ragas allows users to avoid...
  ground truth human annotations."* — correctness 1.0, faithfulness 0.667 (2 of 3 claims the judge
  extracted were supported by the given excerpt; one, "Ragas is a tool for evaluating RAG
  architectures," is true but not stated *in that specific excerpt*, illustrating how strict
  faithfulness checking can be).

Any real retriever from chapter 03 onward should land its correctness between these two numbers, and
its faithfulness should be judged meaningfully now that there actually is context to check claims
against — a real retriever with faithfulness near 1.0 despite low hit@5 would be a red flag (the
model likely ignored bad context and answered from memory, same as the no-retrieval anchor).

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `generate` produces several byte-identical questions of the same type | The prompt was the same string every call at temperature 0, so the disk cache returned the same cached response every time | Vary the prompt content per candidate (see `_GLOBAL_FOCUS_AREAS`/`_UNANSWERABLE_HOOKS`) — never call the same exact prompt N times expecting N different outputs |
| A candidate is dropped silently during `generate` | Its evidence quote failed `quote_in_source` — the model paraphrased instead of quoting verbatim | Expected behaviour, not a bug; check the "kept N/M requested" line in `generate`'s output, and oversample (`generate_single_hop`/`multi_hop`/etc. already request more candidates than needed) |
| `docling` takes far longer than `pymupdf4llm` on the same PDF | Docling loads a full page-layout model (and OCR models) even for born-digital PDFs with no scanned pages | Expected — Docling's advantage is table/layout fidelity on genuinely hard PDFs, not speed; use `pymupdf4llm` as the default and reach for Docling only when a specific paper's tables come out wrong |
| A run's faithfulness score is 1.0 but correctness is low | The generator answered from memory with no retrieved context — an empty context list makes every claim vacuously "supported" | Faithfulness is only meaningful when `contexts` is non-empty; check `retrieved_chunk_ids` in `predictions.jsonl` before trusting a high faithfulness score |
| `just parse-compare` / `just scoreboard` errors with "unexpected extra argument" | Typer collapses a single-command app so it takes no subcommand name | Run `uv run python -m rag_tutorial.parsers` / `rag_tutorial.scoreboard` with no subcommand, as the `justfile` recipes now do |

## Exercises

1. Run `just parse-compare` yourself and find one place `pymupdf4llm` and Docling *disagree* on
   heading structure (different `#`-nesting for the same section) — pick whichever paper's output
   looks more chunking-friendly to you and say why.
2. Read `unanswerable_005` in `data/golden/qa.jsonl` — the one about a nonexistent appendix section —
   and explain why it is a harder test of retrieval-grounded abstention than the protein-folding one.
3. Pick one `global` question and manually check whether every paper id in its evidence list is
   actually relevant by skimming that paper's abstract in `data/corpus/md/` — does the LLM's global
   question-answering hold up?
4. Using the hand-built example in `tests/test_02_golden.py::test_retrieval_metrics_hand_built_case`,
   change the relevant chunk's rank from 2 to 3 and recompute MRR and nDCG@10 by hand before running
   the test to check your arithmetic.

---
Previous: [01_concepts.md](01_concepts.md) · Next: [03_baseline_rag.md](03_baseline_rag.md)
