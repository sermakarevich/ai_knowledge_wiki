"""Three small, runnable demos for chapter 01 (concepts): why retrieval helps,
what an embedding is, and why tokens/context are a scarce resource.

Run with: uv run python -m rag_tutorial.demo_concepts --help
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR, load_papers
from rag_tutorial.llm import Ollama, count_tokens

app = typer.Typer(add_completion=False)
console = Console()

# Three questions whose answers live in our corpus and are specific enough that
# a model is unlikely to have memorised them precisely from pretraining. Each
# `context` paragraph was located by hand with `grep` in `data/corpus/md/`.
WHY_RETRIEVAL_QUESTIONS = [
    {
        "question": "In the RAPTOR paper, what accuracy did GPT-4 reach on the QuALITY "
        "benchmark when paired with RAPTOR?",
        "paper": "2401.18059 (RAPTOR)",
        "context": (
            "In the QuALITY dataset, as shown in Table 7, RAPTOR paired with GPT-4 sets a new "
            "state-of-the-art with an accuracy of 82.6%, surpassing the previous best result of "
            "62.3%. In particular, it outperforms CoLISA by 21.5% on QuALITY-HARD."
        ),
    },
    {
        "question": "How many failure points does the 'Seven Failure Points' paper list, "
        "and name two of them?",
        "paper": "2401.05856 (Seven Failure Points)",
        "context": (
            "FP1 Missing Content The first fail case is when asking a question that cannot be "
            "answered from the available documents. FP2 Missed the Top Ranked Documents The "
            "answer to the question is in the document but did not rank highly enough to be "
            "returned to the user. FP3 Not in Context - Consolidation strategy Limitations. "
            "FP4 Not Extracted. FP5 Wrong Format. FP6 Incorrect Specificity. FP7 Incomplete."
        ),
    },
    {
        "question": "In the CRAG paper, what upper and lower confidence thresholds were used "
        "on the PopQA dataset to trigger the retrieval evaluator's three actions?",
        "paper": "2401.15884 (CRAG)",
        "context": (
            "The two confidence thresholds for triggering one of the three actions were set "
            "empirically. Specifically, they were set as (0.59, -0.99) in PopQA, (0.5, -0.91) "
            "in PubQA and ArcChallenge, as well as (0.95, -0.91) in Biography."
        ),
    },
]

# Six short sentences: pairs (0,1) and (2,3) each restate the same idea in
# different words; (4) and (5) are unrelated to everything else.
EMBED_SENTENCES = [
    "BM25 ranks documents by term frequency and inverse document frequency.",
    "Sparse lexical retrieval like BM25 scores matches using how often a word "
    "appears and how rare it is across the collection.",
    "HNSW builds a multi-layer graph of vectors to find approximate nearest "
    "neighbours quickly.",
    "Approximate nearest-neighbour search with HNSW navigates a layered "
    "vector graph instead of comparing against every point.",
    "Sourdough bread needs a long, slow fermentation to develop its flavour.",
    "The Eiffel Tower was completed in 1889 for the World's Fair in Paris.",
]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine of the angle between two vectors: 1.0 identical direction, 0.0 unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


def cosine_matrix(vectors: list[list[float]]) -> list[list[float]]:
    """Full pairwise cosine-similarity matrix (symmetric, ones on the diagonal)."""
    n = len(vectors)
    return [[cosine_similarity(vectors[i], vectors[j]) for j in range(n)] for i in range(n)]


@app.command()
def why_retrieval() -> None:
    """Ask the chat model three corpus questions with and without the relevant paragraph."""
    client = Ollama()
    for item in WHY_RETRIEVAL_QUESTIONS:
        no_context = client.chat(
            [{"role": "user", "content": item["question"]}],
            max_tokens=256,
        )
        with_context = client.chat(
            [
                {
                    "role": "user",
                    "content": f"Context:\n{item['context']}\n\nQuestion: {item['question']}",
                }
            ],
            max_tokens=256,
        )
        console.rule(f"[bold]{item['paper']}[/bold]")
        console.print(f"[bold]Q:[/bold] {item['question']}")
        console.print(f"[dim]Source paragraph:[/dim] {item['context']}")
        console.print(f"\n[red]Without context:[/red]\n{no_context.strip()}")
        console.print(f"\n[green]With context:[/green]\n{with_context.strip()}\n")


@app.command()
def embeddings() -> None:
    """Embed six sentences and print the cosine-similarity matrix."""
    client = Ollama()
    vectors = client.embed_documents(EMBED_SENTENCES)
    matrix = cosine_matrix(vectors)

    table = Table(title=f"cosine similarity ({settings.embed_model}, {len(vectors[0])} dims)")
    table.add_column("#")
    for i in range(len(EMBED_SENTENCES)):
        table.add_column(str(i), justify="right")
    for i, row in enumerate(matrix):
        table.add_row(str(i), *[f"{v:.3f}" for v in row])
    console.print(table)

    for i, sentence in enumerate(EMBED_SENTENCES):
        console.print(f"[{i}] {sentence}")


@app.command()
def tokens() -> None:
    """Print token counts: one paper, the whole corpus, and Ollama's configured context."""
    papers = load_papers()
    first_paper = papers[0]
    first_text = (MD_DIR / f"{first_paper['id']}.md").read_text()
    first_tokens = count_tokens(first_text)

    corpus_tokens = 0
    for paper in papers:
        path = MD_DIR / f"{paper['id']}.md"
        if path.exists():
            corpus_tokens += count_tokens(path.read_text())

    table = Table(title="tokens vs context")
    table.add_column("what")
    table.add_column("tokens (cl100k_base approx.)", justify="right")
    table.add_row(f"one paper ({first_paper['id']})", str(first_tokens))
    table.add_row("whole corpus (12 papers)", str(corpus_tokens))
    table.add_row("Ollama num_ctx we use", "16384")
    table.add_row("Ollama server max (num_ctx)", "98304")
    console.print(table)
    console.print(
        f"\nThe whole corpus is ~{corpus_tokens / 16384:.1f}x our configured context window "
        f"and ~{corpus_tokens / 98304:.1f}x the server's maximum — 'just paste everything' does "
        "not fit even at the server's largest setting."
    )


@app.command()
def main() -> None:
    """Run all three demos in order."""
    why_retrieval()
    embeddings()
    tokens()


if __name__ == "__main__":
    app()
