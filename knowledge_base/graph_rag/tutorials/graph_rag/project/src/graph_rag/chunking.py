"""Split a `Document`'s text into `Chunk`s: paragraphs/headings first, then tokens.

Token counting uses `tiktoken` with the `cl100k_base` encoding (used by GPT-3.5/
GPT-4). Our chat model is `qwen3.8:27b` (a Qwen model with its own tokenizer),
not an OpenAI model, so this token count is an *approximation* of what qwen
would count — good enough to keep chunks roughly the same size and well under
qwen's context window, without adding a second tokenizer dependency just for
counting.
"""

import re
from dataclasses import dataclass

import tiktoken

_ENCODING = tiktoken.get_encoding("cl100k_base")

# Numbered section headings typical of academic papers, e.g. "3.2 Related Work"
# or "10 References" at the start of a line.
_HEADING_RE = re.compile(r"^\d+(\.\d+)*\s+[A-Z][^\n]{0,80}$", re.MULTILINE)


@dataclass
class Chunk:
    id: str
    index: int
    text: str
    n_tokens: int
    page_start: int | None = None
    page_end: int | None = None


def count_tokens(text: str) -> int:
    return len(_ENCODING.encode(text))


def _split_into_sections(text: str) -> list[str]:
    """Split on numbered headings, keeping the heading with the section that follows."""
    positions = [m.start() for m in _HEADING_RE.finditer(text)]
    if not positions:
        return [text]
    positions = [0] + positions if positions[0] != 0 else positions
    sections = []
    for start, end in zip(positions, positions[1:] + [len(text)]):
        section = text[start:end].strip()
        if section:
            sections.append(section)
    return sections


_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def _split_into_paragraphs(section: str, max_tokens: int) -> list[str]:
    """Split on blank lines (real paragraph breaks in Markdown/text input).

    PDF text has no blank lines inside a page (line breaks are just line
    wraps), so a whole page can come back as a single "paragraph" here; any
    block still bigger than `max_tokens` gets split into sentences so packing
    below has natural breakpoints instead of falling back to a mid-sentence
    hard token split.
    """
    blocks = [p.strip() for p in section.split("\n\n") if p.strip()] or [section]
    paragraphs: list[str] = []
    for block in blocks:
        if count_tokens(block) <= max_tokens:
            paragraphs.append(block)
        else:
            paragraphs.extend(s.strip() for s in _SENTENCE_RE.split(block) if s.strip())
    return paragraphs


def _pack_by_tokens(paragraphs: list[str], max_tokens: int, overlap: int) -> list[str]:
    """Greedily pack paragraphs into chunks of at most `max_tokens`, with a
    token overlap carried over from the end of one chunk to the start of the
    next so retrieval doesn't lose context right at a chunk boundary.
    """
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = count_tokens(paragraph)

        if paragraph_tokens > max_tokens:
            # A single paragraph is bigger than a chunk: hard-split by tokens.
            if current:
                chunks.append("\n\n".join(current))
                current, current_tokens = [], 0
            tokens = _ENCODING.encode(paragraph)
            for start in range(0, len(tokens), max_tokens - overlap):
                piece = _ENCODING.decode(tokens[start : start + max_tokens])
                chunks.append(piece)
            continue

        if current_tokens + paragraph_tokens > max_tokens and current:
            chunks.append("\n\n".join(current))
            # Carry the tail of the previous chunk forward as overlap context.
            tail_text = current[-1]
            tail_tokens = _ENCODING.encode(tail_text)[-overlap:] if overlap else []
            tail = _ENCODING.decode(tail_tokens) if tail_tokens else ""
            current = [tail] if tail else []
            current_tokens = count_tokens(tail) if tail else 0

        current.append(paragraph)
        current_tokens += paragraph_tokens

    if current:
        chunks.append("\n\n".join(current))
    return chunks


def chunk_text(doc_id: str, text: str, max_tokens: int = 400, overlap: int = 60) -> list[Chunk]:
    """Chunk `text` heading-aware, with a token overlap between consecutive chunks.

    Strategy: split on numbered section headings, then on paragraphs, then
    greedily pack paragraphs up to `max_tokens` tokens per chunk. This keeps
    chunk boundaries at natural text breaks (never mid-sentence) whenever a
    section/paragraph is small enough, and only falls back to a hard token
    split for paragraphs bigger than `max_tokens` on their own.
    """
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


def _page_offsets(pages: list) -> list[tuple[int, int, int]]:
    """Char offset ranges of each page within the "\\n\\n".join(pages) text."""
    offsets = []
    cursor = 0
    for page in pages:
        start = cursor
        end = start + len(page.text)
        offsets.append((page.number, start, end))
        cursor = end + 2  # "\n\n" separator
    return offsets


def _collapse_whitespace(text: str) -> tuple[str, list[int]]:
    """Collapse all whitespace runs to a single space, keeping a map from each
    output char back to its original index in `text` (used to locate chunk
    text that was re-joined with different whitespace during packing).
    """
    out_chars: list[str] = []
    index_map: list[int] = []
    prev_was_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_was_space:
                out_chars.append(" ")
                index_map.append(i)
            prev_was_space = True
        else:
            out_chars.append(ch)
            index_map.append(i)
            prev_was_space = False
    return "".join(out_chars), index_map


def attach_page_numbers(chunks: list[Chunk], full_text: str, pages: list) -> None:
    """Fill in `page_start`/`page_end` on each chunk by locating its text within
    `full_text` (the same text the chunks were produced from) and mapping the
    matched char range onto the page offsets computed from `pages`.

    Matching is done on whitespace-collapsed copies of both texts because
    packing re-joins paragraphs/sentences with "\\n\\n", which does not always
    match the single "\\n" line breaks in the original page text.
    """
    if not pages:
        return
    offsets = _page_offsets(pages)
    norm_text, index_map = _collapse_whitespace(full_text)
    cursor = 0
    for chunk in chunks:
        probe, _ = _collapse_whitespace(chunk.text.strip()[:120])
        if not probe:
            continue
        pos = norm_text.find(probe, cursor)
        if pos == -1:
            pos = norm_text.find(probe)
        if pos == -1:
            continue
        start = index_map[pos]
        end_norm = min(pos + len(probe) + len(chunk.text), len(index_map) - 1)
        end = index_map[end_norm]
        chunk.page_start = next((n for n, s, e in offsets if s <= start < e), None)
        chunk.page_end = next((n for n, s, e in reversed(offsets) if s < end <= e), None)
        if chunk.page_start is None:
            chunk.page_start = chunk.page_end
        if chunk.page_end is None:
            chunk.page_end = chunk.page_start
        cursor = pos
