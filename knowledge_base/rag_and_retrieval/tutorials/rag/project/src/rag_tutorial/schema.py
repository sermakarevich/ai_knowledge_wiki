"""Shared data model: chunks, documents and section detection.

Every chunking strategy in later chapters (fixed, recursive, semantic, ...)
produces a list of `Chunk` objects with the *same* fields, so that retrieval
metrics and the scoreboard can compare them fairly. `chunk_id` is a pure
function of `(paper, start, end)` — the character offsets into the parsed
Markdown — so re-computing it for the same chunk boundaries always yields the
same id, even across processes and runs.
"""

from __future__ import annotations

import hashlib
import re

from pydantic import BaseModel

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$", re.MULTILINE)


def chunk_id(paper: str, start: int, end: int) -> str:
    """Deterministic id for a chunk: first 16 hex chars of sha1(paper:start:end)."""
    digest = hashlib.sha1(f"{paper}:{start}:{end}".encode("utf-8")).hexdigest()
    return digest[:16]


class Chunk(BaseModel):
    id: str
    paper: str
    section: str
    text: str
    start: int
    end: int
    meta: dict = {}


class Section(BaseModel):
    path: str
    level: int
    start: int
    end: int


class Document(BaseModel):
    paper: str
    title: str
    text: str
    sections: list[Section] = []

    @classmethod
    def from_markdown(cls, paper: str, title: str, text: str) -> "Document":
        return cls(paper=paper, title=title, text=text, sections=detect_sections(text))


def detect_sections(text: str) -> list[Section]:
    """Find `#`-heading boundaries and build a heading-path per section.

    A section runs from the character offset right after its heading line to
    the start of the next heading of *any* level (or the end of the text).
    `path` joins the current heading with its open ancestors, e.g.
    `"3 Method > 3.2 Retrieval"`, so a chunk's section field tells you where
    in the paper it came from even after the chunk itself is much smaller
    than the section.
    """
    headings = [(m.start(), m.end(), len(m.group(1)), m.group(2).strip()) for m in _HEADING_RE.finditer(text)]
    if not headings:
        return [Section(path="", level=0, start=0, end=len(text))]

    sections: list[Section] = []
    stack: list[tuple[int, str]] = []  # (level, title)
    for i, (_start, heading_end, level, title) in enumerate(headings):
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        path = " > ".join(t for _lvl, t in stack)
        section_start = heading_end
        section_end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        sections.append(Section(path=path, level=level, start=section_start, end=section_end))

    if headings[0][0] > 0:
        sections.insert(0, Section(path="", level=0, start=0, end=headings[0][0]))
        # re-clip the first heading-based section's start/end already correct

    return sections


def section_at(sections: list[Section], offset: int) -> str:
    """Return the heading path of the section containing character `offset`."""
    for section in sections:
        if section.start <= offset < section.end:
            return section.path
    return sections[-1].path if sections else ""
