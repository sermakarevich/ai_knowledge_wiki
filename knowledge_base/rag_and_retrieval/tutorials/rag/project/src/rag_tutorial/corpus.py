"""Download and parse the tutorial's fixed 12-paper arXiv corpus.

`download` fetches the PDFs (skipping ones already on disk, being polite to
arXiv with a delay between requests) and records the real page count in
`papers.yaml`. `parse` turns each PDF into a committed Markdown file with
`pypdf`; chapter 02 compares this against better parsers. `stats` prints the
same table from the Markdown files alone (no PDFs needed).
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import typer
import yaml
from pypdf import PdfReader
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.llm import count_tokens

app = typer.Typer(add_completion=False)
console = Console()

PAPERS_YAML = settings.path("data/corpus/papers.yaml")
PDF_DIR = settings.path("data/corpus/pdf")
MD_DIR = settings.path("data/corpus/md")

_USER_AGENT = "rag-tutorial/0.1 (educational use; contact via github)"
_DOWNLOAD_DELAY_S = 3


def load_papers() -> list[dict]:
    return yaml.safe_load(PAPERS_YAML.read_text())


def save_papers(papers: list[dict]) -> None:
    PAPERS_YAML.write_text(yaml.safe_dump(papers, sort_keys=False, allow_unicode=True))


def _dehyphenate(text: str) -> str:
    """Join words split across a line break with a trailing hyphen."""
    return re.sub(r"-\n(?=[a-z])", "", text)


@app.command()
def download() -> None:
    """Download every paper's PDF (skip if already present) and record its page count."""
    import httpx

    papers = load_papers()
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for i, paper in enumerate(papers):
        dest = PDF_DIR / f"{paper['id']}.pdf"
        if dest.exists():
            console.print(f"[dim]skip (exists)[/dim] {paper['id']}")
        else:
            console.print(f"downloading {paper['id']} ...")
            response = httpx.get(paper["url"], headers={"User-Agent": _USER_AGENT}, follow_redirects=True, timeout=60)
            response.raise_for_status()
            dest.write_bytes(response.content)
            if i < len(papers) - 1:
                time.sleep(_DOWNLOAD_DELAY_S)
        paper["pages"] = len(PdfReader(dest).pages)
    save_papers(papers)
    console.print(f"[green]done[/green] — {len(papers)} PDFs in {PDF_DIR}")


@app.command()
def parse(
    parser: str = typer.Option(
        "pymupdf4llm", help="pypdf | pymupdf4llm | docling — see 02_corpus_and_golden_set.md for the comparison; pymupdf4llm won"
    ),
) -> None:
    """Convert every downloaded PDF into data/corpus/md/<id>.md with the chosen parser.

    `pymupdf4llm` is the default: chapter 02 found it detects headings and
    reconstructs tables as well as Docling, at roughly a quarter of the
    wall-clock cost. It is AGPL-licensed (fine for this tutorial, a
    consideration for closed-source reuse — see the chapter).
    """
    from rag_tutorial.parsers import PARSERS

    if parser not in PARSERS:
        raise typer.BadParameter(f"parser must be one of {list(PARSERS)}")
    parse_fn = PARSERS[parser]

    papers = load_papers()
    MD_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for paper in papers:
        pdf_path = PDF_DIR / f"{paper['id']}.pdf"
        if not pdf_path.exists():
            console.print(f"[yellow]missing PDF, skipping[/yellow] {paper['id']} (run `just corpus-download` first)")
            continue
        body = parse_fn(pdf_path)
        markdown = f"# {paper['title']}\n\n{body}"
        md_path = MD_DIR / f"{paper['id']}.md"
        md_path.write_text(markdown)
        page_count = len(PdfReader(pdf_path).pages)
        rows.append((paper["id"], paper["short_name"], page_count, len(markdown), count_tokens(markdown)))

    _print_table(rows)


@app.command()
def stats() -> None:
    """Print the paper/pages/characters/tokens table from the committed Markdown files."""
    papers = load_papers()
    rows = []
    for paper in papers:
        md_path = MD_DIR / f"{paper['id']}.md"
        if not md_path.exists():
            continue
        text = md_path.read_text()
        page_count = text.count("<!-- page ")
        rows.append((paper["id"], paper["short_name"], page_count, len(text), count_tokens(text)))
    _print_table(rows)


def _print_table(rows: list[tuple]) -> None:
    table = Table(title="rag_tutorial corpus")
    table.add_column("id")
    table.add_column("short_name")
    table.add_column("pages", justify="right")
    table.add_column("characters", justify="right")
    table.add_column("tokens", justify="right")
    total_pages = total_chars = total_tokens = 0
    for id_, short_name, pages, chars, tokens in rows:
        table.add_row(id_, short_name, str(pages), str(chars), str(tokens))
        total_pages += pages
        total_chars += chars
        total_tokens += tokens
    table.add_row("[bold]total[/bold]", "", f"[bold]{total_pages}[/bold]", f"[bold]{total_chars}[/bold]", f"[bold]{total_tokens}[/bold]")
    console.print(table)


if __name__ == "__main__":
    app()
