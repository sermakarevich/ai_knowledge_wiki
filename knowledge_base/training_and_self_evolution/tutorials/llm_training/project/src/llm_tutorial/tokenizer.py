"""Chapter 02 — train our own 32k byte-level BPE tokenizer and compare it to Qwen's.

`train` streams documents from a Hugging Face dataset (no full download) and fits a
byte-level BPE (Byte-Pair Encoding: start from single bytes, greedily merge the most
frequent adjacent pair, repeat until `vocab_size` is reached) with the `tokenizers`
library, then wraps it as a `transformers` fast tokenizer so it can be `from_pretrained`-
loaded like any Hugging Face tokenizer. `compare` measures fertility (tokens per 1,000
characters — lower is better, it means fewer tokens per unit of text) and the resulting
embedding-parameter cost of each tokenizer's vocabulary.
"""

from collections.abc import Iterable
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
from transformers import PreTrainedTokenizerFast

app = typer.Typer(add_completion=False)
console = Console()

SPECIAL_TOKENS = ["<|endoftext|>", "<|im_start|>", "<|im_end|>", "<|pad|>"]


def train_bpe_from_iterator(texts: Iterable[str], vocab_size: int) -> PreTrainedTokenizerFast:
    """Fit a byte-level BPE tokenizer on `texts` and return it as a HF fast tokenizer."""
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=vocab_size, special_tokens=SPECIAL_TOKENS)
    tokenizer.train_from_iterator(texts, trainer=trainer)

    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        eos_token="<|endoftext|>",
        pad_token="<|pad|>",
        additional_special_tokens=["<|im_start|>", "<|im_end|>"],
    )
    return fast


def _stream_texts(corpus: str, config: str, n_docs: int, text_column: str = "text") -> Iterable[str]:
    from datasets import load_dataset

    ds = load_dataset(corpus, config, split="train", streaming=True)
    for i, row in enumerate(ds):
        if i >= n_docs:
            break
        yield row[text_column]


@app.command()
def train(
    corpus: str = typer.Option("HuggingFaceFW/fineweb-edu", help="HF dataset repo to stream."),
    config: str = typer.Option("sample-10BT", help="HF dataset config name."),
    n_docs: int = typer.Option(200_000, help="Number of streamed documents to train on."),
    vocab_size: int = typer.Option(32_000, help="Target vocabulary size."),
    out: Path = typer.Option(Path("runs/tokenizer_32k"), help="Output directory."),
) -> None:
    """Stream `n_docs` documents and train a byte-level BPE tokenizer of `vocab_size`."""
    import time

    console.print(f"streaming {n_docs:,} docs from {corpus}/{config} …")
    start = time.perf_counter()
    fast = train_bpe_from_iterator(_stream_texts(corpus, config, n_docs), vocab_size)
    elapsed = time.perf_counter() - start

    out.mkdir(parents=True, exist_ok=True)
    fast.save_pretrained(out)
    console.print(f"saved tokenizer to {out} in {elapsed:.1f}s, vocab_size={fast.vocab_size}")


def _fertility(tok, text: str) -> float:
    """Tokens per 1,000 characters — the lower, the more text a fixed context window holds."""
    n_tokens = len(tok(text)["input_ids"])
    return 1000 * n_tokens / max(len(text), 1)


def _embedding_params(vocab_size: int, hidden: int) -> int:
    return vocab_size * hidden


@app.command()
def compare(
    text_file_or_sample: str = typer.Argument(
        None, help="Path to a text file to measure fertility on; if omitted, a built-in sample is used."
    ),
    tokenizers: list[str] = typer.Option(
        ["runs/tokenizer_32k", "Qwen/Qwen3.5-0.8B"],
        "--tokenizer",
        help="Tokenizer dirs/repo ids to compare (repeatable).",
    ),
    hidden: int = typer.Option(768, help="Hidden size used for the embedding-parameter estimate."),
) -> None:
    """Print fertility, vocab size, and embedding-parameter cost for each tokenizer."""
    from transformers import AutoTokenizer

    if text_file_or_sample and Path(text_file_or_sample).exists():
        text = Path(text_file_or_sample).read_text()
    elif text_file_or_sample:
        text = text_file_or_sample
    else:
        text = (
            "The quick brown fox jumps over the lazy dog. Large language models learn to predict "
            "the next token in a sequence of text. Byte-pair encoding merges frequent character "
            "pairs into subword units, keeping vocabularies small while covering any input."
        )

    table = Table(title=f"tokenizer comparison ({len(text)} chars, hidden={hidden})")
    table.add_column("tokenizer")
    table.add_column("vocab_size", justify="right")
    table.add_column("tokens/1k chars", justify="right")
    table.add_column("embedding params", justify="right")

    for name in tokenizers:
        tok = AutoTokenizer.from_pretrained(name)
        fert = _fertility(tok, text)
        emb = _embedding_params(tok.vocab_size, hidden)
        table.add_row(name, f"{tok.vocab_size:,}", f"{fert:.1f}", f"{emb:,}")

    console.print(table)


if __name__ == "__main__":
    app()
