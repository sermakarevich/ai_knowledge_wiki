"""Chapter 04's late-chunking demo — NOT run on the scoreboard (see 04_chunking.md
for why: it needs its own retrieval path, and this chapter's budget went to the
11 named experiments instead). Late chunking (Günther et al., arXiv:2409.04701,
CC BY-NC-SA — discussed, not redistributed here) embeds the *whole* document
first with a long-context model, then mean-pools the *token* embeddings within
each chunk's character span — so every chunk vector still saw the whole
document through attention, unlike embedding each chunk's text separately.

The spec's suggested model, `jinaai/jina-embeddings-v2-small-en`, ships custom
`trust_remote_code` modeling code that imports `transformers.onnx.OnnxConfig`
and `transformers.pytorch_utils.find_pruneable_heads_and_indices` — both
removed from the `transformers` version pinned in this project (5.8.1, see
`04_chunking.md`). We use `BAAI/bge-m3` instead: a standard (no custom code)
long-context (8192 token) embedding model that loads on CPU with today's
`transformers`, on one paper from the corpus.
"""

from __future__ import annotations

import numpy as np
import torch
import typer
from transformers import AutoModel, AutoTokenizer

from rag_tutorial.chunkers import _token_windows
from rag_tutorial.golden import load_documents

MODEL_NAME = "BAAI/bge-m3"

app = typer.Typer(add_completion=False)


def late_chunk_embeddings(text: str, size: int = 256, overlap: int = 0) -> list[np.ndarray]:
    """One mean-pooled, L2-normalised vector per `size`-token character window of
    `text`, computed from token embeddings of the *whole* `text` in one forward pass."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).eval()

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=8192, return_offsets_mapping=True)
    offsets = inputs.pop("offset_mapping")[0].tolist()
    with torch.no_grad():
        token_embeddings = model(**inputs).last_hidden_state[0]  # (n_tokens, hidden)

    text_len = max(end for _start, end in offsets)  # special tokens have a (0, 0) offset
    windows = _token_windows(text[:text_len], size, overlap)
    vectors = []
    for start_char, end_char in windows:
        idx = [i for i, (s, e) in enumerate(offsets) if s < e and s < end_char and e > start_char]
        pooled = token_embeddings[idx].mean(dim=0).numpy()
        vectors.append(pooled / np.linalg.norm(pooled))
    return vectors


@app.command()
def demo(size: int = 256) -> None:
    """Run late chunking on the first paper of the corpus and print vector count/dim."""
    doc = next(iter(load_documents().values()))
    vectors = late_chunk_embeddings(doc.text, size=size)
    print(f"{doc.paper} ({doc.title}): {len(vectors)} late-chunked vectors, dim={vectors[0].shape[0]}")


if __name__ == "__main__":
    app()
