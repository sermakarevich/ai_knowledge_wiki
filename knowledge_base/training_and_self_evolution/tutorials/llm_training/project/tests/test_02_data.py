"""Chapter 02 — tokenizer training and data packing on a synthetic corpus.

CPU only, no network: the tokenizer is trained from an in-memory iterator of sentences,
never downloaded, and shards are written to `tmp_path`.
"""

import numpy as np
import torch

from llm_tutorial.data import PackedDataset, pack_documents, write_shards
from llm_tutorial.tokenizer import SPECIAL_TOKENS, train_bpe_from_iterator

SENTENCES = [
    f"The quick brown fox jumps over the lazy dog number {i}. Byte-pair encoding merges frequent pairs."
    for i in range(500)
]


def test_bpe_round_trips_and_has_special_tokens():
    tok = train_bpe_from_iterator(SENTENCES, vocab_size=600)
    for special in SPECIAL_TOKENS:
        assert special in tok.get_vocab()
    for sentence in SENTENCES[:20]:
        ids = tok.encode(sentence)
        assert tok.decode(ids) == sentence


def test_pack_documents_inserts_one_eos_per_doc():
    eos_id = 999
    docs = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    packed = pack_documents(docs, eos_id)
    assert len(packed) == sum(len(d) for d in docs) + len(docs)
    assert list(packed) == [1, 2, 3, 999, 4, 5, 999, 6, 7, 8, 9, 999]
    assert packed.dtype == np.uint16


def test_write_shards_and_packed_dataset(tmp_path):
    rng = np.random.default_rng(0)
    stream = [rng.integers(0, 600, size=300, dtype=np.uint16) for _ in range(5)]
    written = write_shards(iter(stream), tmp_path, shard_tokens=1000, prefix="train")
    assert len(written) >= 1
    assert all(p.name.startswith("train_") for p in written)

    ds = PackedDataset(tmp_path, split="train", block_size=16)
    x, y = ds[0]
    assert x.shape == (16,)
    assert y.shape == (16,)
    assert x.dtype == torch.int64
    assert y.dtype == torch.int64
    assert torch.equal(x[1:], y[:-1])


def test_iter_batches_shape(tmp_path):
    rng = np.random.default_rng(1)
    stream = [rng.integers(0, 600, size=300, dtype=np.uint16) for _ in range(5)]
    write_shards(iter(stream), tmp_path, shard_tokens=1000, prefix="train")
    ds = PackedDataset(tmp_path, split="train", block_size=16)

    batches = ds.iter_batches(batch_size=4, device="cpu")
    x, y = next(batches)
    assert x.shape == (4, 16)
    assert y.shape == (4, 16)
