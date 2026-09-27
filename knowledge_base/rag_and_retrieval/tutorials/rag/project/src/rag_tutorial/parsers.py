"""Three ways to turn a paper PDF into Markdown, compared side by side.

`pypdf` (already used in chapter 00) gives plain text with almost no
structure. `pymupdf4llm` and Docling both produce Markdown with `#` headings
and reconstructed tables, which matters a lot once we chunk by section
(chapter 04) — a chunk that starts mid-table or mid-heading is much harder to
answer questions from.

`pymupdf4llm` (built on PyMuPDF) is **dual-licensed AGPLv3 / commercial**: free
to use in an open-source project like this tutorial, but a commercial,
closed-source product that links it would need a paid license from Artifex.
Docling (IBM) is MIT-licensed. That is a real, non-technical reason a team
might pick Docling over pymupdf4llm even if the numbers below are similar.
"""

from __future__ import annotations

import re
import time

import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.llm import count_tokens

app = typer.Typer(add_completion=False)
console = Console()

_HEADING_COUNT_RE = re.compile(r"^#{1,6}\s", re.MULTILINE)


def _dehyphenate(text: str) -> str:
    return re.sub(r"-\n(?=[a-z])", "", text)


def parse_pypdf(pdf_path) -> str:
    """Plain-text extraction, page by page, dehyphenated. No headings, no tables."""
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    parts = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = _dehyphenate(page.extract_text() or "")
        parts.append(f"<!-- page {page_num} -->\n{text}\n")
    return "\n".join(parts)


def parse_pymupdf4llm(pdf_path) -> str:
    """Markdown with detected `#` headings and Markdown tables, one page-chunk per page."""
    import pymupdf4llm

    pages = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True, show_progress=False)
    parts = [f"<!-- page {i} -->\n{page['text']}\n" for i, page in enumerate(pages, start=1)]
    return "\n".join(parts)


def parse_docling(pdf_path) -> str:
    """Markdown via Docling's layout model (headings, tables); no per-page markers."""
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    return result.document.export_to_markdown()


PARSERS = {
    "pypdf": parse_pypdf,
    "pymupdf4llm": parse_pymupdf4llm,
    "docling": parse_docling,
}

# The parser used for the committed corpus (chosen in `compare` below).
WINNER = "pymupdf4llm"


def _table_excerpt(text: str, needle: str, n_lines: int = 5) -> str:
    idx = text.find(needle)
    if idx == -1:
        return "(table not found)"
    snippet = text[idx : idx + 600]
    lines = [line for line in snippet.splitlines() if line.strip()]
    return "\n".join(lines[:n_lines])


@app.command()
def compare(
    papers: list[str] = typer.Option(["2401.18059", "2404.16130"], help="arXiv ids to compare (default: RAPTOR, GraphRAG — both table-heavy)"),
    table_needle: str = typer.Option("Table 1", help="Substring marking the start of a known table to quote"),
) -> None:
    """Run all three parsers on the given papers and print a timing/quality table
    plus a 5-line excerpt of one known table from each parser's output."""
    from rag_tutorial.config import settings

    pdf_dir = settings.path("data/corpus/pdf")
    rows = []
    excerpts: dict[str, str] = {}
    for paper in papers:
        pdf_path = pdf_dir / f"{paper}.pdf"
        if not pdf_path.exists():
            console.print(f"[yellow]missing PDF, skipping[/yellow] {paper} (run `just corpus-download` first)")
            continue
        for name, fn in PARSERS.items():
            start = time.monotonic()
            text = fn(pdf_path)
            elapsed = time.monotonic() - start
            headings = len(_HEADING_COUNT_RE.findall(text))
            rows.append(
                {
                    "paper": paper,
                    "parser": name,
                    "seconds": round(elapsed, 1),
                    "characters": len(text),
                    "tokens": count_tokens(text),
                    "headings": headings,
                }
            )
            excerpts[f"{paper}/{name}"] = _table_excerpt(text, table_needle)

    table = Table(title="parser comparison")
    for col in ["paper", "parser", "seconds", "characters", "tokens", "headings"]:
        table.add_column(col, justify="right" if col != "paper" and col != "parser" else "left")
    for row in rows:
        table.add_row(row["paper"], row["parser"], str(row["seconds"]), str(row["characters"]), str(row["tokens"]), str(row["headings"]))
    console.print(table)

    console.print("\n[bold]table excerpts (5 lines each)[/bold]")
    for key, excerpt in excerpts.items():
        console.print(f"\n[cyan]{key}[/cyan]:")
        console.print(excerpt)


if __name__ == "__main__":
    app()
