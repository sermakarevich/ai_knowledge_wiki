"""Chunking strategies. Chapter 03 shipped the first one (`fixed`); this chapter
(04) adds the rest — recursive, sentence, markdown (+ contextual header),
semantic, parent/child (small-to-big), sentence-window and contextual
retrieval — behind the same `CHUNKERS` registry so every later chapter can
swap the chunker without touching the indexing or retrieval code.

Every chunker returns `list[Chunk]`; `meta` carries at least `strategy` plus
whatever extra bookkeeping a retriever needs (`parent_id`, `window`, ...).
"""

from __future__ import annotations

import re

import numpy as np
import tiktoken

from rag_tutorial.schema import Chunk, Document, chunk_id, section_at

_encoding = tiktoken.get_encoding("cl100k_base")

# -- shared helpers ------------------------------------------------------------------


def _n_tokens(text: str) -> int:
    return len(_encoding.encode(text))


def _token_windows(text: str, size: int, overlap: int) -> list[tuple[int, int]]:
    """Character `(start, end)` spans of fixed-size, overlapping token windows.

    Factored out of `fixed_token_chunks` so `markdown_chunks` and
    `parent_child_chunks` can cut a *section* or a *parent* into same-sized
    windows with the exact same token/character mapping.
    """
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    token_ids = _encoding.encode(text)
    n_tokens = len(token_ids)
    step = size - overlap

    windows: list[tuple[int, int]] = []
    start_tok = 0
    while start_tok < n_tokens:
        end_tok = min(start_tok + size, n_tokens)
        start_char = len(_encoding.decode(token_ids[:start_tok])) if start_tok else 0
        end_char = len(_encoding.decode(token_ids[:end_tok]))
        windows.append((start_char, end_char))
        if end_tok >= n_tokens:
            break
        start_tok += step
    return windows


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Character `(start, end)` spans of sentences, split on `.`/`!`/`?` followed
    by whitespace — a simple regex sentence splitter, not a full NLP model."""
    spans: list[tuple[int, int]] = []
    start = 0
    for m in _SENTENCE_SPLIT_RE.finditer(text):
        if m.start() > start:
            spans.append((start, m.start()))
        start = m.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


# -- fixed (chapter 03) ---------------------------------------------------------------


def fixed_token_chunks(doc: Document, size: int = 512, overlap: int = 64) -> list[Chunk]:
    """Split `doc.text` into fixed-size, overlapping windows of `size` tokens.

    See `_token_windows` for how token boundaries are mapped back to character
    offsets. Every chunk's `section` is looked up from `doc.sections` at its
    start offset, so a fixed-size chunk still carries the heading path it
    happened to start in.
    """
    chunks: list[Chunk] = []
    for start_char, end_char in _token_windows(doc.text, size, overlap):
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=doc.text[start_char:end_char],
                start=start_char,
                end=end_char,
                meta={"strategy": "fixed", "size": size},
            )
        )
    return chunks


# -- recursive --------------------------------------------------------------------------

# Tried in this order, coarsest to finest, LangChain's `RecursiveCharacterTextSplitter`
# idea: paragraph -> line -> sentence -> word.
_SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split_keep_sep(text: str, sep: str) -> list[str]:
    """Split on `sep` but keep it glued to the piece before it, so
    `"".join(_split_keep_sep(text, sep)) == text` — offsets stay exact."""
    parts = text.split(sep)
    return [p + sep for p in parts[:-1]] + [parts[-1]]


def _recursive_split(text: str, size: int, seps: list[str]) -> list[str]:
    if _n_tokens(text) <= size or not seps:
        return [text]
    sep, rest = seps[0], seps[1:]
    parts = _split_keep_sep(text, sep)
    if len(parts) <= 1:
        return _recursive_split(text, size, rest)
    result: list[str] = []
    for part in parts:
        result.extend(_recursive_split(part, size, rest))
    return result


def recursive_chunks(doc: Document, size: int = 512, overlap: int = 64) -> list[Chunk]:
    """Split on paragraph, then line, then sentence, then word boundaries — whichever
    is coarsest and still fits `size` tokens — then merge pieces back up to `size`
    tokens with `overlap` tokens of trailing context carried into the next chunk.
    """
    text = doc.text
    pieces = _recursive_split(text, size, _SEPARATORS)
    offsets = []
    pos = 0
    for piece in pieces:
        offsets.append(pos)
        pos += len(piece)

    chunks: list[Chunk] = []
    i, n = 0, len(pieces)
    while i < n:
        start_i = i
        start_char = offsets[i]
        acc = ""
        while i < n and (not acc or _n_tokens(acc + pieces[i]) <= size):
            acc += pieces[i]
            i += 1
        end_char = start_char + len(acc)
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=acc,
                start=start_char,
                end=end_char,
                meta={"strategy": "recursive", "size": size},
            )
        )
        if i >= n:
            break
        back_tokens, j = 0, i
        while j > start_i and back_tokens < overlap:
            j -= 1
            back_tokens += _n_tokens(pieces[j])
        i = max(j, start_i + 1)
    return chunks


# -- sentence -----------------------------------------------------------------------------


def sentence_chunks(doc: Document, n_sentences: int = 5, overlap: int = 1) -> list[Chunk]:
    """Group `n_sentences` sentences per chunk, with `overlap` sentences shared
    between consecutive chunks."""
    spans = sentence_spans(doc.text)
    if not spans:
        return []
    step = max(n_sentences - overlap, 1)

    chunks: list[Chunk] = []
    i = 0
    while i < len(spans):
        group = spans[i : i + n_sentences]
        start_char, end_char = group[0][0], group[-1][1]
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=doc.text[start_char:end_char],
                start=start_char,
                end=end_char,
                meta={"strategy": "sentence", "n_sentences": len(group)},
            )
        )
        if i + n_sentences >= len(spans):
            break
        i += step
    return chunks


# -- markdown (+ contextual header) --------------------------------------------------------


def _section_header(doc: Document, section_path: str) -> str:
    return f"{doc.title} — {section_path}" if section_path else doc.title


def markdown_chunks(doc: Document, size: int = 512, overlap: int = 64) -> list[Chunk]:
    """Split on Markdown heading boundaries first (`doc.sections`), then use the
    `fixed`-style token windows inside any section still longer than `size`
    tokens. Every chunk's text is prefixed with a contextual header line
    `"<paper title> — <section path>"` so it still reads sensibly on its own,
    even outside the paper.
    """
    chunks: list[Chunk] = []
    for section in doc.sections:
        section_text = doc.text[section.start : section.end]
        if not section_text.strip():
            continue
        header = _section_header(doc, section.path)
        if _n_tokens(section_text) <= size:
            windows = [(0, len(section_text))]
        else:
            windows = _token_windows(section_text, size, overlap)
        for w_start, w_end in windows:
            start_char, end_char = section.start + w_start, section.start + w_end
            body = section_text[w_start:w_end]
            chunks.append(
                Chunk(
                    id=chunk_id(doc.paper, start_char, end_char),
                    paper=doc.paper,
                    section=section.path,
                    text=f"{header}\n{body}",
                    start=start_char,
                    end=end_char,
                    meta={"strategy": "markdown", "size": size, "header": header},
                )
            )
    return chunks


# -- semantic -------------------------------------------------------------------------------


def _cosine(a: list[float], b: list[float]) -> float:
    va, vb = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    return float(np.dot(va, vb) / denom) if denom else 0.0


def semantic_chunks(doc: Document, embedder, percentile: float = 20, min_sentences: int = 1) -> list[Chunk]:
    """Embed every sentence, then break right after the sentences whose similarity
    to the *next* sentence is in the bottom `percentile` — a proxy for "this is
    a topic-change point". `embedder` needs an `embed_documents(texts)` method
    (both `rag_tutorial.llm.ollama` and `testing.FakeEmbedder` provide one).
    """
    spans = sentence_spans(doc.text)
    if len(spans) <= 1:
        text = doc.text
        return [
            Chunk(
                id=chunk_id(doc.paper, 0, len(text)),
                paper=doc.paper,
                section=section_at(doc.sections, 0),
                text=text,
                start=0,
                end=len(text),
                meta={"strategy": "semantic", "n_sentences": len(spans)},
            )
        ]

    sentences = [doc.text[s:e] for s, e in spans]
    vectors = embedder.embed_documents(sentences)
    sims = [_cosine(vectors[i], vectors[i + 1]) for i in range(len(vectors) - 1)]
    n_breaks = max(1, round(len(sims) * percentile / 100))
    break_after = set(sorted(range(len(sims)), key=lambda i: sims[i])[:n_breaks])

    groups: list[list[int]] = [[0]]
    for i in range(len(sims)):
        if i in break_after and len(groups[-1]) >= min_sentences:
            groups.append([i + 1])
        else:
            groups[-1].append(i + 1)

    chunks: list[Chunk] = []
    for group in groups:
        start_char, end_char = spans[group[0]][0], spans[group[-1]][1]
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=doc.text[start_char:end_char],
                start=start_char,
                end=end_char,
                meta={"strategy": "semantic", "n_sentences": len(group)},
            )
        )
    return chunks


# -- parent/child (small-to-big) -----------------------------------------------------------


def parent_chunks(doc: Document, size: int = 800, overlap: int = 100) -> list[Chunk]:
    """The ~800-token "parent" windows a `parent_child` retriever hands to the
    LLM once a small child chunk inside them is retrieved."""
    chunks: list[Chunk] = []
    for start_char, end_char in _token_windows(doc.text, size, overlap):
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=doc.text[start_char:end_char],
                start=start_char,
                end=end_char,
                meta={"strategy": "parent", "size": size},
            )
        )
    return chunks


def parent_child_chunks(
    doc: Document,
    parent_size: int = 800,
    parent_overlap: int = 100,
    child_size: int = 160,
    child_overlap: int = 32,
) -> list[Chunk]:
    """Small 128-200 token "child" chunks meant for embedding/retrieval; each
    carries `meta["parent_id"]` pointing at the ~800-token parent window it
    was cut from (see `parent_chunks`), which a `ParentChildRetriever` swaps
    the child for before handing context to the LLM.
    """
    parents = parent_chunks(doc, size=parent_size, overlap=parent_overlap)
    children: list[Chunk] = []
    for parent in parents:
        parent_text = doc.text[parent.start : parent.end]
        for c_start, c_end in _token_windows(parent_text, child_size, child_overlap):
            start_char, end_char = parent.start + c_start, parent.start + c_end
            children.append(
                Chunk(
                    id=chunk_id(doc.paper, start_char, end_char),
                    paper=doc.paper,
                    section=section_at(doc.sections, start_char),
                    text=parent_text[c_start:c_end],
                    start=start_char,
                    end=end_char,
                    meta={"strategy": "parent_child", "parent_id": parent.id, "size": child_size},
                )
            )
    return children


# -- sentence window ------------------------------------------------------------------------


def sentence_window_chunks(doc: Document, window: int = 3) -> list[Chunk]:
    """Index single sentences; `meta["window"]` records how many neighbours a
    `SentenceWindowRetriever` should expand each hit into at query time."""
    chunks: list[Chunk] = []
    for i, (start_char, end_char) in enumerate(sentence_spans(doc.text)):
        chunks.append(
            Chunk(
                id=chunk_id(doc.paper, start_char, end_char),
                paper=doc.paper,
                section=section_at(doc.sections, start_char),
                text=doc.text[start_char:end_char],
                start=start_char,
                end=end_char,
                meta={"strategy": "sentence_window", "window": window, "sentence_index": i},
            )
        )
    return chunks


# -- contextual retrieval (Anthropic-style) --------------------------------------------------

_CONTEXT_SYSTEM = "Reply with only the 2-3 sentence context, no preamble, no quotation marks."


def _context_prompt(abstract: str, section: str, chunk_text: str) -> str:
    return (
        f"Document abstract: {abstract}\n\n"
        f"Section: {section or 'N/A'}\n\n"
        f"Chunk:\n{chunk_text}\n\n"
        "Write a short 2-3 sentence context that situates this chunk within the overall "
        "document, so that the context plus the chunk together are unambiguous out of place. "
        "Answer only with the context, nothing else."
    )


def contextual_chunks(doc: Document, llm_client, abstract: str, size: int = 512, overlap: int = 64) -> list[Chunk]:
    """Anthropic-style contextual retrieval: for every `markdown` chunk, ask the LLM
    for a 2-3 sentence blurb describing where the chunk sits in the document (given
    the paper's abstract and the chunk's section path), then prepend that blurb to
    the chunk text before embedding. `llm_client` is `rag_tutorial.llm.ollama` (or a
    fake in tests) — every call goes through its disk cache.
    """
    base = markdown_chunks(doc, size=size, overlap=overlap)
    out: list[Chunk] = []
    for chunk in base:
        context = llm_client.chat(
            [
                {"role": "system", "content": _CONTEXT_SYSTEM},
                {"role": "user", "content": _context_prompt(abstract, chunk.section, chunk.text)},
            ],
            temperature=0,
            max_tokens=150,
        ).strip()
        out.append(
            Chunk(
                id=chunk.id,
                paper=chunk.paper,
                section=chunk.section,
                text=f"{context}\n\n{chunk.text}",
                start=chunk.start,
                end=chunk.end,
                meta={**chunk.meta, "strategy": "contextual", "context": context},
            )
        )
    return out


CHUNKERS = {
    "fixed": fixed_token_chunks,
    "recursive": recursive_chunks,
    "sentence": sentence_chunks,
    "markdown": markdown_chunks,
    "semantic": semantic_chunks,
    "parent_child": parent_child_chunks,
    "sentence_window": sentence_window_chunks,
    "contextual": contextual_chunks,
}
