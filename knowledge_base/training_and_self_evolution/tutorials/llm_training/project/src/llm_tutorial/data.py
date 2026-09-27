"""Chapter 02 — turn a streamed text corpus into fixed-length training blocks on disk.

Pipeline: stream documents -> tokenize -> append `<|endoftext|>` after each document ->
concatenate into one long token stream -> write it as `uint16` shards (nanoGPT style: a
plain array of token ids, memory-mapped at training time). We pack documents back to back
with an EOS separator instead of padding each one to `block_size`: padding wastes compute
on tokens the model does not need to predict, while packing spends every position on real
text. The cost is that a training window can span the end of one document and the start of
the next, so attention briefly looks across unrelated documents — the model still learns to
mostly ignore this because `<|endoftext|>` reliably marks the boundary.
"""

import json
import time
from collections.abc import Iterable, Iterator
from pathlib import Path

import numpy as np
import torch
import typer
from rich.console import Console
from torch.utils.data import Dataset

app = typer.Typer(add_completion=False)
console = Console()


def pack_documents(token_lists: Iterable[list[int]], eos_id: int) -> np.ndarray:
    """Concatenate tokenized documents, appending `eos_id` after each one."""
    pieces = []
    n_tokens = 0
    n_docs = 0
    for tokens in token_lists:
        pieces.append(tokens)
        pieces.append([eos_id])
        n_tokens += len(tokens)
        n_docs += 1
    flat = [t for piece in pieces for t in piece]
    out = np.array(flat, dtype=np.uint16)
    assert len(out) == n_tokens + n_docs
    return out


def write_shards(stream: Iterable[np.ndarray], out_dir: Path, shard_tokens: int, prefix: str = "train") -> list[Path]:
    """Buffer token arrays from `stream` and flush `shard_tokens`-sized `uint16` shard files.

    Pending chunks are only concatenated once a shard boundary is crossed (not on every
    incoming array) so the total copying work stays O(total tokens), not O(total tokens^2).
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    pending: list[np.ndarray] = []
    pending_len = 0
    idx = 0
    for arr in stream:
        pending.append(arr)
        pending_len += len(arr)
        while pending_len >= shard_tokens:
            buffer = np.concatenate(pending)
            shard, rest = buffer[:shard_tokens], buffer[shard_tokens:]
            path = out_dir / f"{prefix}_{idx:03d}.bin"
            shard.tofile(path)
            written.append(path)
            pending = [rest] if len(rest) else []
            pending_len = len(rest)
            idx += 1
    if pending_len > 0:
        path = out_dir / f"{prefix}_{idx:03d}.bin"
        np.concatenate(pending).tofile(path)
        written.append(path)
    return written


class PackedDataset(Dataset):
    """Random `block_size` windows over one or more `uint16` token shards of a split."""

    def __init__(self, shard_dir: str | Path, split: str, block_size: int):
        shard_dir = Path(shard_dir)
        if split == "val":
            paths = sorted(shard_dir.glob("val*.bin"))
        else:
            paths = sorted(shard_dir.glob(f"{split}_*.bin"))
        if not paths:
            raise FileNotFoundError(f"no shards for split={split!r} in {shard_dir}")

        self.block_size = block_size
        self.shards = [np.memmap(p, dtype=np.uint16, mode="r") for p in paths]
        self._usable = [max(len(s) - block_size - 1, 0) for s in self.shards]
        self._cum = np.cumsum(self._usable)

    def __len__(self) -> int:
        return int(self._cum[-1]) if len(self._cum) else 0

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        shard_idx = int(np.searchsorted(self._cum, idx, side="right"))
        local_idx = idx - (int(self._cum[shard_idx - 1]) if shard_idx > 0 else 0)
        tokens = self.shards[shard_idx]
        block = self.block_size
        x = torch.from_numpy(tokens[local_idx : local_idx + block].astype(np.int64))
        y = torch.from_numpy(tokens[local_idx + 1 : local_idx + 1 + block].astype(np.int64))
        return x, y

    def iter_batches(self, batch_size: int, device: str = "cpu") -> Iterator[tuple[torch.Tensor, torch.Tensor]]:
        """Yield an endless stream of `(x, y)` batches of shape `(batch_size, block_size)`."""
        n = len(self)
        while True:
            idxs = torch.randint(0, n, (batch_size,))
            xs, ys = zip(*(self[int(i)] for i in idxs))
            yield torch.stack(xs).to(device), torch.stack(ys).to(device)


def _stream_dataset(corpus: str, config: str | None, text_column: str) -> Iterable[str]:
    from datasets import load_dataset

    ds = load_dataset(corpus, config, split="train", streaming=True) if config else load_dataset(
        corpus, split="train", streaming=True
    )
    for row in ds:
        yield row[text_column]


def _batched(iterable: Iterable, batch_size: int) -> Iterator[list]:
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


@app.command()
def prepare(
    corpus: str = typer.Option("HuggingFaceFW/fineweb-edu", help="HF dataset repo to stream."),
    config: str = typer.Option("sample-10BT", help="HF dataset config name (empty string for none)."),
    tokenizer_dir: str = typer.Option("runs/tokenizer_32k", help="Tokenizer dir or hub id."),
    out_dir: Path = typer.Option(Path("runs/data/fineweb_edu"), help="Output directory for shards + meta.json."),
    target_tokens: int = typer.Option(1_600_000_000, help="Total tokens to write (train + val)."),
    block_size: int = typer.Option(2048, help="Recorded in meta.json for the training loop."),
    val_tokens: int = typer.Option(10_000_000, help="Tokens set aside for val.bin."),
    shard_tokens: int = typer.Option(100_000_000, help="Tokens per train shard file."),
    num_proc: int = typer.Option(16, help="Batch size for tokenization (docs per `.tokenizer()` call)."),
    text_column: str = typer.Option("text", help="Column holding the document text."),
) -> None:
    """Stream, tokenize, pack with EOS separators, and write uint16 shards until `target_tokens`."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(tokenizer_dir)
    eos_id = tok.eos_token_id
    out_dir.mkdir(parents=True, exist_ok=True)

    train_target = target_tokens - val_tokens
    cfg = config or None
    texts = _stream_dataset(corpus, cfg, text_column)

    doc_length_sample: list[int] = []
    docs_seen = 0
    n_train_tokens = 0
    n_val_tokens = 0
    train_written = False
    val_chunks: list[np.ndarray] = []
    start = time.perf_counter()

    def train_stream() -> Iterator[np.ndarray]:
        nonlocal docs_seen, n_train_tokens, train_written, n_val_tokens
        for batch in _batched(texts, num_proc):
            encoded = tok(batch, add_special_tokens=False)["input_ids"]
            for tokens in encoded:
                if len(doc_length_sample) < 1000:
                    doc_length_sample.append(len(tokens))
            docs_seen += len(encoded)
            arr = pack_documents(encoded, eos_id)
            if not train_written:
                if n_train_tokens + len(arr) >= train_target:
                    remaining = train_target - n_train_tokens
                    n_train_tokens += remaining
                    train_written = True
                    yield arr[:remaining]
                    val_chunks.append(arr[remaining:])
                else:
                    n_train_tokens += len(arr)
                    yield arr
            else:
                val_chunks.append(arr)
                n_val_tokens += len(arr)
                if n_val_tokens >= val_tokens:
                    return

    written = write_shards(train_stream(), out_dir, shard_tokens, prefix="train")
    val_arr = np.concatenate(val_chunks)[:val_tokens] if val_chunks else np.empty(0, dtype=np.uint16)
    val_arr.tofile(out_dir / "val.bin")
    n_val_tokens = len(val_arr)

    elapsed = time.perf_counter() - start
    docs_per_sec = docs_seen / elapsed if elapsed > 0 else 0.0

    meta = {
        "tokenizer": str(tokenizer_dir),
        "block_size": block_size,
        "n_train_tokens": int(n_train_tokens),
        "n_val_tokens": int(n_val_tokens),
        "docs_seen": docs_seen,
        "wall_time_s": elapsed,
        "docs_per_s": docs_per_sec,
        "n_shards": len(written),
        "doc_length_sample": doc_length_sample,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    console.print(f"wrote {n_train_tokens:,} train + {n_val_tokens:,} val tokens to {out_dir} "
                  f"in {elapsed:.1f}s ({docs_per_sec:.1f} docs/s)")


def export_val_text(shard_dir: str | Path, tokenizer_dir: str, out_path: str | Path, max_bytes: int = 200_000) -> Path:
    """Decode the front of `val.bin` back to text with `tokenizer_dir`'s tokenizer, stopping once
    `out_path` holds `max_bytes` of UTF-8 text. Used by chapter 07's `llama-perplexity` runs, which
    need a raw text file rather than the packed `uint16` token shards."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(tokenizer_dir)
    val_path = Path(shard_dir) / "val.bin"
    tokens = np.fromfile(val_path, dtype=np.uint16)

    text = ""
    chunk = 4096
    pos = 0
    while len(text.encode("utf-8")) < max_bytes and pos < len(tokens):
        piece = tokens[pos : pos + chunk].tolist()
        text += tok.decode(piece, skip_special_tokens=True)
        pos += chunk
    text = text.encode("utf-8")[:max_bytes].decode("utf-8", errors="ignore")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text)
    console.print(f"wrote {len(text.encode('utf-8')):,} bytes of val text to {out_path}")
    return out_path


@app.command("export-val-text")
def export_val_text_cmd(
    shard_dir: str = typer.Option("runs/data/fineweb_edu", help="dir with val.bin"),
    tokenizer_dir: str = typer.Option("runs/tokenizer_32k", help="tokenizer used to decode val.bin"),
    out_path: str = typer.Option("runs/export/val_sample.txt", help="output text file"),
    max_bytes: int = typer.Option(200_000, help="stop once this many bytes of text are written"),
) -> None:
    """CLI wrapper around `export_val_text` (chapter 07 perplexity input)."""
    export_val_text(shard_dir, tokenizer_dir, out_path, max_bytes=max_bytes)


@app.command()
def stats(out_dir: Path = typer.Argument(Path("runs/data/fineweb_edu"))) -> None:
    """Print token/shard counts and a document-length histogram from `meta.json`."""
    meta = json.loads((out_dir / "meta.json").read_text())
    n_shards = len(list(out_dir.glob("train_*.bin")))
    console.print(f"train tokens: {meta['n_train_tokens']:,}")
    console.print(f"val tokens:   {meta['n_val_tokens']:,}")
    console.print(f"shards:       {n_shards}")
    console.print(f"docs seen:    {meta['docs_seen']:,}")
    console.print(f"docs/s:       {meta['docs_per_s']:.1f}")

    lengths = meta.get("doc_length_sample", [])
    if lengths:
        bins = sorted({0, 64, 128, 256, 512, 1024, 2048, 4096, max(lengths) + 1})
        hist, edges = np.histogram(lengths, bins=bins)
        for count, lo, hi in zip(hist, edges[:-1], edges[1:]):
            bar = "#" * int(50 * count / max(hist)) if max(hist) else ""
            console.print(f"{int(lo):>6}-{int(hi):<6} {bar} {count}")


if __name__ == "__main__":
    app()
