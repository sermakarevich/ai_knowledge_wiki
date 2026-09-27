"""Load an unknown file (PDF, Markdown or plain text) into a `Document`.

"Unknown" means: we don't control the format ahead of time and nobody has
hand-cleaned the text. This module turns a path on disk into one `Document`
dataclass with a stable id, a title, and cleaned full text (PDF cleaning is
the hard part; Markdown/text need much less).
"""

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader

# Matches a running header/footer like "111:6 Peng et al." or the mirrored
# "Graph Retrieval-Augmented Generation: A Survey 111:21" that this survey PDF
# repeats on every page, plus a bare page number on its own line.
_RUNNING_HEADER_RE = re.compile(
    r"^\s*(?:\d+:\d+\s+.+|.+\s+\d+:\d+)\s*$|^\s*\d+\s*$", re.MULTILINE
)
_HYPHEN_BREAK_RE = re.compile(r"(\w)-\n(\w)")
_WHITESPACE_RE = re.compile(r"[ \t]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")
_MD_FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
_MD_HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass
class Page:
    """One page of extracted, cleaned PDF text (used to keep chunk page numbers)."""

    number: int  # 1-based
    text: str


@dataclass
class Document:
    id: str
    path: str
    title: str
    text: str
    sha256: str
    pages: list[Page] = field(default_factory=list)  # empty for non-PDF sources


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _doc_id(path: Path) -> str:
    """sha256 of the resolved absolute path, so the same file gets the same id
    regardless of the working directory or a relative-vs-absolute call site.
    """
    return hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()


def _clean_page_text(text: str) -> str:
    """Clean one page of raw PDF-extracted text.

    Order matters: join hyphenated line breaks first (they still have the
    original newline), then drop repeated running headers/footers and bare
    page numbers, then collapse whitespace.
    """
    text = _HYPHEN_BREAK_RE.sub(r"\1\2", text)
    text = _RUNNING_HEADER_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text)
    text = _BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()


def _load_pdf(path: Path) -> tuple[str, list[Page]]:
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        cleaned = _clean_page_text(page.extract_text() or "")
        if cleaned:
            pages.append(Page(number=i, text=cleaned))
    full_text = "\n\n".join(p.text for p in pages)
    return full_text, pages


def _strip_front_matter(text: str) -> str:
    return _MD_FRONT_MATTER_RE.sub("", text, count=1)


def _title_from_text(text: str, fallback: str) -> str:
    """First `# ` Markdown heading, else the first non-empty line, else `fallback`."""
    match = _MD_HEADING_RE.search(text)
    if match:
        return match.group(1).strip()
    first_line = text.strip().splitlines()[0].strip() if text.strip() else ""
    if 0 < len(first_line) <= 200:
        return first_line
    return fallback


def load_document(path: str | Path) -> Document:
    """Load a `.pdf`, `.md` or `.txt` file into a `Document`.

    `id` is the sha256 of the path string (stable across re-runs from the same
    location); `sha256` is the hash of the file's bytes, used by `ingest.py` to
    detect that a document at the same path changed.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    raw_bytes = path.read_bytes()

    if suffix == ".pdf":
        text, pages = _load_pdf(path)
        title = _title_from_text(text, fallback=path.stem)
    elif suffix in {".md", ".txt"}:
        raw_text = raw_bytes.decode("utf-8")
        if suffix == ".md":
            raw_text = _strip_front_matter(raw_text)
        text = raw_text.strip()
        pages = []
        title = _title_from_text(text, fallback=path.stem)
    else:
        raise ValueError(f"unsupported file type: {path}")

    return Document(
        id=_doc_id(path),
        path=str(path),
        title=title,
        text=text,
        sha256=_sha256(raw_bytes),
        pages=pages,
    )
