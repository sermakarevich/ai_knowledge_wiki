# Task: chapter 02 — Tokenizer and pre-training data (BPE training, streaming FineWeb-Edu, packing into blocks)

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `01_concepts.md` first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
A model from scratch needs (1) a tokenizer — we train our own 32k BPE (Byte-Pair Encoding) on a
sample of the corpus and compare it with Qwen's 248k tokenizer — and (2) a token stream packed into
fixed-length blocks stored on disk on `rtx`, so the training loop (chapter 04) never waits on the
network. Everything heavy runs on `rtx`; the Mac only runs unit tests on synthetic text.

## Fix

### `project/src/llm_tutorial/tokenizer.py` (Typer CLI)
- `train(corpus: str = "HuggingFaceFW/fineweb-edu", config: str = "sample-10BT", n_docs: int = 200_000, vocab_size: int = 32000, out: Path = "runs/tokenizer_32k")`: stream `n_docs` documents with `datasets.load_dataset(..., split="train", streaming=True)`, train a byte-level BPE with the `tokenizers` library (`models.BPE`, `pre_tokenizers.ByteLevel(add_prefix_space=False)`, `decoders.ByteLevel`, special tokens `<|endoftext|>`, `<|im_start|>`, `<|im_end|>`, `<|pad|>`), wrap it as `transformers.PreTrainedTokenizerFast` with `eos_token="<|endoftext|>"`, `pad_token="<|pad|>"`, and save with `save_pretrained(out)`. Expose `train_bpe_from_iterator(texts: Iterable[str], vocab_size) -> PreTrainedTokenizerFast` for tests.
- `compare(text_file_or_sample, tokenizers=["runs/tokenizer_32k", "Qwen/Qwen3.5-0.8B"])`: tokens per 1,000 characters ("fertility"), vocabulary size, embedding parameters at hidden 768 for each; print a table. Reuse of the Qwen tokenizer is discussed (Qwen's is `Qwen2Tokenizer`, 248,320 rows → 190M embedding parameters at hidden 768 — more than our whole model — which is why we train a 32k one).

### `project/src/llm_tutorial/data.py` (Typer CLI)
- `prepare(corpus, config, tokenizer_dir, out_dir: Path = "runs/data/fineweb_edu", target_tokens: int = 1_600_000_000, block_size: int = 2048, val_tokens: int = 10_000_000, shard_tokens: int = 100_000_000, num_proc: int = 16)`: stream documents, tokenize in batches (use `datasets` `.map(batched=True)` on the streaming dataset or a `multiprocessing.Pool`; measure and report docs/s), append `<|endoftext|>` after every document, concatenate into one token stream, and write `uint16` numpy shards `train_000.bin …` and `val.bin` (nanoGPT style: contiguous tokens, `np.memmap`-readable). Stop when `target_tokens` are written. Write `out_dir/meta.json` (tokenizer path, block_size, n_train_tokens, n_val_tokens, docs_seen, wall time, docs/s). Expose `pack_documents(token_lists, eos_id) -> np.ndarray` and `write_shards(stream, out_dir, shard_tokens)` for tests.
- `PackedDataset(shard_dir, split, block_size)`: `torch.utils.data.Dataset` returning `x = tokens[i:i+block]`, `y = tokens[i+1:i+1+block]` from random offsets (or a sequential `iter_batches(batch_size, device)` generator that the training loop in chapter 04 will use). Document why packing with an EOS separator is used instead of padding (no wasted compute) and its downside (cross-document attention) in the chapter.
- `stats(out_dir)`: prints tokens, shards, a histogram of document lengths from `meta.json` samples.
- Also `sft_smoke_corpus`: `prepare --corpus roneneldan/TinyStories --config default --target-tokens 50_000_000 --out-dir runs/data/tinystories` for the 10-minute smoke run of chapter 04 (TinyStories column is `text` too).

### `justfile` recipes
`tok-train`, `tok-compare`, `data-prepare` (each = `just remote …` or `remote-bg` for the big one), `data-stats`. Preparing 1.6B tokens streams ~6 GB of text; run it detached: `just remote-bg data-prep "python -m llm_tutorial.data prepare"`, and the tokenizer training as `just remote-bg tok-train …`. Report real timings in the chapter (expect tens of minutes; `sample-10BT` has ~10B tokens so we consume roughly a sixth of it).

### Run for real on `rtx`
1. `just push`, `just remote-sync` if needed. 2. Train the tokenizer (200k docs). 3. `tok-compare`. 4. Prepare TinyStories (50M tokens) and FineWeb-Edu (1.6B tokens — leaves headroom over the 1.5B in `index.md`). 5. `just pull` → `runs/tokenizer_32k/` (tokenizer files are small JSON — commit them, they are needed for reproducibility), `runs/data/*/meta.json`.
Heavy files (`*.bin`) stay on rtx. Do NOT block the GPU — this chapter is CPU-only on rtx (32 cores, 62 GB RAM); do not run `gpu-free`.

### `project/tests/test_02_data.py`
Synthetic corpus of ~500 short sentences: `train_bpe_from_iterator(vocab_size=600)` produces a tokenizer that round-trips text (`decode(encode(s)) == s`) and has the four special tokens; `pack_documents` puts exactly one EOS after each document and total length equals sum(len)+n_docs; `write_shards` + `PackedDataset` (tmp_path, shard_tokens=1000, block_size=16) yield `x`/`y` shifted by one and dtype `uint16`→`int64` tensors; `iter_batches` shape `(batch, block)`.

### `02_tokenizer_and_data.md` (chapter)
What a tokenizer is (bytes → tokens, why BPE), training ours and reading `tokenizer.json`; the comparison table (fertility, vocab, embedding params) and the decision; special tokens and the chat tokens we reserve for chapter 05; streaming a dataset that does not fit on disk; tokenising in parallel (real docs/s and total minutes); packing into blocks (diagram: documents → EOS-joined stream → fixed windows); shards on disk as `uint16` and why (2 bytes/token, 1.6B tokens = 3.2 GB); token budgets: Chinchilla ≈ 20 tokens/parameter, ours ≈ 14; what the SmolLM/SmolLM2 models used (600B / 2T tokens for 135M) to set expectations; Troubleshooting (HF rate limits / `HF_HUB_ENABLE_HF_TRANSFER`, slow streaming, OOM in `.map`, tokenizer `add_prefix_space` pitfalls); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{tokenizer,data}.py`, `project/tests/test_02_data.py`, `project/justfile`, `project/runs/tokenizer_32k/*` (json/txt only), `project/runs/data/*/meta.json`, `02_tokenizer_and_data.md`. Verify token `"What you will learn"` in `02_tokenizer_and_data.md`.

## Scope & constraints
No model training here. Do not use the GPU. Do not change `index.md`, `configs/tiny_*.yaml`.
