# 02 — Tokenizer and pre-training data: BPE, streaming FineWeb-Edu, packing into blocks

Previous: [01_concepts.md](01_concepts.md) · Next: [03_model_from_scratch.md](03_model_from_scratch.md)

## What you will learn

- What a tokenizer does (bytes → tokens) and why **BPE** (Byte-Pair Encoding) is the standard way to build one
- How to train our own **32k**-vocabulary tokenizer on a stream of real web text, and why we don't just reuse Qwen's 248k one
- **Fertility** (tokens per 1,000 characters) and **embedding parameters** as the two numbers that make that trade-off concrete
- How to stream a dataset that is far larger than local disk (`datasets` `streaming=True`), tokenize it in batches, and measure real throughput (docs/s)
- **Packing**: joining tokenized documents back to back with an `<|endoftext|>` separator instead of padding, and the trade-off it makes
- Why the packed stream is stored on disk as `uint16` shards, and how `PackedDataset` turns them into training batches
- How our token budget (≈14 tokens/parameter) compares to Chinchilla-optimal (≈20) and to what SmolLM/SmolLM2 actually used

Tokenizer training and data preparation are CPU-only and run on `rtx` because they stream tens of gigabytes of text; the Mac only runs unit tests on a synthetic 500-sentence corpus. No GPU is used anywhere in this chapter.

---

## 1. What a tokenizer is, and why BPE

A neural network has no idea what a "word" is — it only multiplies matrices of numbers. The **tokenizer** is the fixed, non-learned lookup table that turns text into a short sequence of integers (and back), so the rest of the model only ever has to deal with numbers. Chapter 01 already used one:

```
text  : 'The capital of France is'
ids   : [760, 6511, 314, 9338, 369]
pieces: ['The', ' capital', ' of', ' France', ' is']
```

The simplest tokenizer would map every **byte** (0–255) to a token. That covers *any* input — no "unknown token" ever appears, because every string is a sequence of bytes — but it makes sequences very long: "France" becomes 6 tokens instead of 1, and a fixed context window (say, 2048 tokens) holds far less real text.

**BPE (Byte-Pair Encoding)** fixes this by *learning* which byte sequences are common enough to deserve their own token:

1. Start with the raw bytes as the initial vocabulary (256 entries).
2. Count every adjacent pair of tokens in the training corpus.
3. Merge the single most frequent pair into one new token; add it to the vocabulary.
4. Repeat until the vocabulary reaches the target size.

The result is a vocabulary where common whole words ("the", " is") get one token, rarer words get split into a few frequent pieces ("un", "believ", "able"), and truly novel byte sequences (emoji, other scripts, typos) still work — they just fall back towards single bytes. This is why LLM tokenizers never need an "unknown" token the way older word-level tokenizers did.

We train ours as **byte-level** BPE (`pre_tokenizers.ByteLevel`): the initial alphabet is the 256 raw bytes, not a hand-picked set of Unicode characters, so any UTF-8 text — any language, emoji included — tokenizes without ever hitting an unknown symbol.

## 2. Training our tokenizer

```bash
just tok-train              # remote-bg on rtx: python -m llm_tutorial.tokenizer train
```

`project/src/llm_tutorial/tokenizer.py::train` streams `n_docs` (200,000) documents from `HuggingFaceFW/fineweb-edu`, config `sample-10BT`, with `datasets.load_dataset(..., streaming=True)` — the dataset is never downloaded to disk, we just pull one row at a time off the network. Those 200,000 document strings are fed straight into `tokenizers.Tokenizer.train_from_iterator`:

```python
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()
trainer = trainers.BpeTrainer(
    vocab_size=32_000,
    special_tokens=["<|endoftext|>", "<|im_start|>", "<|im_end|>", "<|pad|>"],
)
tokenizer.train_from_iterator(texts, trainer=trainer)
```

Four special tokens are reserved before training starts, so they always get low, stable ids that never collide with a learned merge:

- `<|endoftext|>` — the document separator we use for packing (section 5) and the tokenizer's `eos_token`
- `<|im_start|>` / `<|im_end|>` — unused until chapter 05 (SFT), where they wrap chat turns (`<|im_start|>user\n...<|im_end|>`)
- `<|pad|>` — padding token for the SFT/DPO/GRPO stages, which need batches of unequal-length sequences; pre-training (this chapter and chapter 04) never pads

The trained tokenizer is wrapped as `transformers.PreTrainedTokenizerFast` (`eos_token="<|endoftext|>"`, `pad_token="<|pad|>"`) and saved with `save_pretrained("runs/tokenizer_32k")` — three small JSON files (`tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`), no model weights, which is why we commit them to the repo for reproducibility.

**Real run on `rtx`:** streaming and training on 200,000 documents took **55.7 s** end to end (network-bound, not CPU-bound — training the BPE merges themselves is fast once the text is in memory).

## 3. Comparing our tokenizer to Qwen's

```bash
just tok-compare             # python -m llm_tutorial.tokenizer compare
```

`compare` loads a list of tokenizers with `AutoTokenizer.from_pretrained`, tokenizes the same sample text with each, and reports **fertility** (tokens per 1,000 characters — lower means a fixed context window holds more text) and the **embedding parameter cost** at a chosen hidden size (`vocab_size × hidden`). Real output from `rtx`:

```
              tokenizer comparison (245 chars, hidden=768)
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ tokenizer          ┃ vocab_size ┃ tokens/1k chars ┃ embedding params ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ runs/tokenizer_32k │     32,000 │           212.2 │       24,576,000 │
│ Qwen/Qwen3.5-0.8B  │    248,044 │           195.9 │      190,497,792 │
└────────────────────┴────────────┴─────────────────┴──────────────────┘
```

(Qwen's tokenizer is a `Qwen2Tokenizer`; its `config.json` quotes `vocab_size: 248320` — `AutoTokenizer`'s live vocabulary is 248,044 once you count only the entries actually usable as ids, a difference of a couple of hundred reserved-but-unused slots. Either number tells the same story.)

**Fertility:** Qwen's much bigger vocabulary is *better* at compressing text — 195.9 vs 212.2 tokens per 1,000 characters, about 8% fewer tokens for the same text. That is the entire point of a larger vocabulary: more of the world's common words and subwords get their own single token.

**Embedding parameters:** but that compression costs `248,044 × 768 = 190,497,792` embedding parameters at hidden size 768 — nearly **190 million** — versus `32,000 × 768 = 24,576,000` for ours, a **7.75×** difference. Our whole model (chapter 01, `tiny-qwen35-110m`) is ≈110M parameters total. Adopting Qwen's tokenizer would mean the embedding table *alone* outweighs the entire rest of the network — for a model this size, that is a bad trade. A 32k vocabulary is not free (8% more tokens to encode the same text, so 8% more compute per fixed amount of training data) but it is the right side of the trade-off at 110M parameters. Larger models (Qwen3.5-4B, Qwen3.8-27B) can afford the bigger vocabulary because the embedding table becomes a smaller fraction of the total.

## 4. Streaming a dataset that does not fit on disk

`FineWeb-Edu`'s `sample-10BT` config alone is ~10 billion tokens of text — tens of gigabytes, more than convenient to keep as a local copy just to read once. `datasets.load_dataset(..., streaming=True)` returns an `IterableDataset`: iterating it opens a network connection and yields rows one (or one shard) at a time, with nothing written to disk beyond a small read-ahead buffer. This is exactly what `tokenizer.py::_stream_texts` and `data.py::_stream_dataset` do — a plain Python generator over `row["text"]`.

The trade-off: no random access (you cannot ask for document #4,000,000 without reading through everything before it), and network hiccups or Hugging Face Hub rate limits show up as stalls instead of a slow local disk read (see Troubleshooting).

## 5. Tokenizing in parallel and packing into blocks

`project/src/llm_tutorial/data.py::prepare` does four things in one streaming pass:

1. **Batch and tokenize.** Documents are grouped into batches of `num_proc` (default 16) and tokenized together with one `tok(batch, add_special_tokens=False)` call — batching amortizes the fast-tokenizer's Rust-side overhead across many documents at once.
2. **Pack with an EOS separator.** `pack_documents(token_lists, eos_id)` concatenates every document's tokens and appends `<|endoftext|>` after each one:

   ```
   doc A tokens  doc B tokens  doc C tokens
   [a1 a2 a3] [b1 b2] [c1 c2 c3 c4]
         │           │            │
         ▼           ▼            ▼
   a1 a2 a3 <eos> b1 b2 <eos> c1 c2 c3 c4 <eos>
   └──────────────────── one long token stream ────────────────────┘
         │                    │                   │
         ▼                    ▼                   ▼
      [ block 0, length 2048 ][ block 1, length 2048 ][ block 2 … ]
   ```

   We pack instead of padding each document to `block_size` because **padding wastes compute**: a padded batch spends matrix-multiply cycles on `<|pad|>` tokens the model will never be asked to predict. Packing spends every single position of every training example on real text — at pre-training scale (billions of tokens) that difference is not cosmetic. The cost is that one training window can span the boundary between two unrelated documents, so attention briefly "sees" content from a different document; in practice the model learns that `<|endoftext|>` reliably marks a hard boundary and mostly ignores what is on the other side of it. This trade only makes sense for **pre-training**; chapter 05 (SFT) goes back to padding (or packing with loss-masking) because there each example needs its own well-defined start and end.
3. **Stop at `target_tokens`.** The stream is cut as soon as `target_tokens - val_tokens` training tokens have been written, then the current in-flight document is finished so no document is split between train and val.
4. **Write `uint16` shards.** `write_shards` buffers the incoming packed arrays and flushes fixed-size (`shard_tokens`, default 100M) `uint16` `.bin` files — `train_000.bin`, `train_001.bin`, … — plus one `val.bin`. `uint16` (2 bytes per token) is exactly enough range for a 32,000-entry vocabulary (max id needs ≤ 16 bits) and *half* the size of the `int32`/`int64` you'd otherwise default to — 1.6B tokens is 3.2 GB as `uint16` instead of 6.4 GB or 12.8 GB. The files are plain contiguous arrays with no header, so training (chapter 04) reads them with `np.memmap(path, dtype=np.uint16, mode="r")` — the OS pages the file in lazily, and a shard many times larger than RAM still works.

`meta.json` records the tokenizer used, `block_size`, exact token counts, documents seen, wall time, docs/s, and a 1,000-document sample of token lengths (used by `data.py::stats` for the histogram below).

### Real runs on `rtx`

**TinyStories smoke corpus** (`just data-prepare name=data-prep-tinystories args="--corpus roneneldan/TinyStories --config '' --target-tokens 50000000 --out-dir runs/data/tinystories"`, for chapter 04's 10-minute smoke test):

```
wrote 40,000,000 train + 10,000,000 val tokens to runs/data/tinystories
in 25.2s (8,557.9 docs/s)
```

215,984 short children's-story documents, 1 shard. Document lengths (tokens):

```
    0-64      0
   64-128    ## 32
  128-256    ################################################## 732
  256-512    ############ 186
  512-1003   ### 50
```

**FineWeb-Edu** (`just remote-bg data-prep-fineweb "python -m llm_tutorial.data prepare"`, the actual pre-training corpus for chapter 04):

```
wrote 1,590,000,000 train + 10,000,000 val tokens to runs/data/fineweb_edu
in 767.7s (2,004.3 docs/s)
```

That's **12.8 minutes** for 1.6B tokens, 1,538,800 documents, 16 train shards (`train_000.bin` … `train_015.bin`, 200 MB each) + `val.bin` (20 MB) — 3.22 GB total on disk, all left on `rtx` (only `meta.json` is pulled to the Mac; see the DoD note below). `sample-10BT` has roughly 10B tokens, so this run consumes about a sixth of that config. Document lengths are far more varied than TinyStories', with a long tail out past 20,000 tokens (full articles, code listings):

```
    0-64      0
   64-128    ### 22
  128-256    ########################## 148
  256-512    ############################################# 258
  512-1024   ################################################## 284
 1024-2048   ################################## 182
 2048-4096   ############ 72
 4096-27328  ##### 34
```

## 6. `PackedDataset`: from shards to training batches

`data.py::PackedDataset(shard_dir, split, block_size)` is a `torch.utils.data.Dataset` over one split's shards:

```python
x = torch.from_numpy(tokens[i : i + block_size].astype(np.int64))
y = torch.from_numpy(tokens[i + 1 : i + 1 + block_size].astype(np.int64))
```

`x` and `y` are the same window, shifted by one token — `y[k]` is the token the model should predict having seen `x[0..k]`, exactly the next-token-prediction objective from chapter 01. Indices `i` are drawn uniformly across all usable offsets in all shards of a split (`np.memmap` means opening a shard costs nothing until it's read). `iter_batches(batch_size, device)` wraps this into an endless generator of `(x, y)` batches shaped `(batch_size, block_size)` that chapter 04's training loop consumes directly, with no separate `DataLoader`/`collate_fn` needed since every example is already a fixed-length, pad-free block.

## 7. Token budgets: how much data is "enough"?

The **Chinchilla** scaling-law result (Hoffmann et al., 2022) says a compute-optimal model trains on roughly **20 tokens per parameter**. Our `tiny-qwen35-110m` (chapter 01: 84M non-embedding + 24.6M tied-embedding ≈ 110M total) prepared **1.6B tokens** — `1.6e9 / 110e6 ≈ 14.5` tokens per parameter, a bit under Chinchilla-optimal but firmly in the same order of magnitude, and enough headroom over the `≈1.5B` figure quoted in `index.md` to not run out mid-training.

For context, real small models are trained far past Chinchilla-optimal, because inference cost (not training cost) dominates once a model ships: **SmolLM** trained a 135M model on **600B** tokens (≈4,440 tokens/parameter) and **SmolLM2** on **2T** tokens (≈14,800 tokens/parameter) — two to three orders of magnitude more data per parameter than we use here. Our 1.6B-token run is sized to finish training in a few hours on one RTX 4090 (chapter 04), not to be competitive with a released model; it is enough to watch loss fall, perplexity drop, and coherent (if simple) text come out the other end.

---

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `Warning: You are sending unauthenticated requests to the HF Hub` and streaming feels slow | anonymous requests to the Hugging Face Hub are rate-limited | set `HF_TOKEN` (a free Hugging Face account token) in `.env`; for large downloads also install `hf_transfer` and set `HF_HUB_ENABLE_HF_TRANSFER=1` for a faster Rust-based downloader |
| `datasets` streaming stalls or times out mid-run | a single flaky network read; streaming has no automatic resume across process restarts | re-run the recipe — `prepare` restarts from document 0, which is why we run it detached with `remote-bg` and check `remote-log`/`remote-wait` rather than babysitting an SSH session |
| `OOM` (out of memory) inside `.map`/tokenization | batching too many long documents into a single tokenizer call at once | lower `num_proc` (the batch size for tokenization, despite the name — it is not process count here); 62 GB RAM on `rtx` comfortably handles the default of 16 |
| decoded text doesn't exactly match the input (`decode(encode(s)) != s`) | `pre_tokenizers.ByteLevel(add_prefix_space=True)` inserts a leading space marker that is not always undone symmetrically by unusual leading punctuation | we use `add_prefix_space=False`; if you change it, re-run `test_02_data.py`'s round-trip test before trusting the tokenizer |
| `np.histogram` raises `bins must increase monotonically` in `data stats` | a fixed bin edge (e.g. `4096`) can exceed `max(doc_length_sample) + 1` when the corpus has only short documents (TinyStories) | `stats` deduplicates and sorts the bin edges before histogramming, so short-document corpora and long-document corpora both work with the same fixed edges |
| `just tok-compare`/`just data-prepare` can't find `runs/tokenizer_32k` on the Mac | tokenizer training happens on `rtx`; only `just pull` brings the small JSON files back | run `just tok-train` (or `just pull`) before comparing or preparing data locally |

## Exercises

1. **Fertility vs. compute.** Our tokenizer has 8% worse fertility than Qwen's (212.2 vs 195.9 tokens/1k chars). For a fixed 1.6B-token training budget, roughly how much *less* raw text (in characters) does our tokenizer see compared to training on the same character budget with Qwen's tokenizer? What would happen to the embedding-parameter trade-off if we instead trained a 64k vocabulary — rerun `just tok-train --vocab-size 64000` and `just tok-compare` and fill in a three-row version of the table in section 3.
2. **Shard math.** `shard_tokens` defaults to 100,000,000 and each token is `uint16` (2 bytes). Confirm the 200 MB shard size we saw on `rtx`, and compute how many shards a 20B-token run (Chinchilla-optimal for our 110M model) would need.
3. **Packing loss.** Section 5 says packing lets attention "see" across an `<|endoftext|>` boundary. Using `PackedDataset` on `runs/data/tinystories` (once pulled or on `rtx`), pick a random window and check via the tokenizer's `decode` whether it happens to straddle two documents. How often does that happen for `block_size=2048` given TinyStories' typical document length (~250 tokens, from the histogram in section 5)?
4. **Token budget stress-test.** `roneneldan/TinyStories` document lengths cluster tightly around 150–300 tokens (histogram in section 5), while FineWeb-Edu ranges from under 100 to over 20,000. Why does that difference make FineWeb-Edu a better *pre-training* corpus but TinyStories a better *smoke-test* corpus for chapter 04's 10-minute sanity run?

---

Previous: [01_concepts.md](01_concepts.md) · Next: [03_model_from_scratch.md](03_model_from_scratch.md)

Numbers in this chapter: `project/runs/tokenizer_32k/compare.txt`, `project/runs/data/fineweb_edu/meta.json`, `project/runs/data/tinystories/meta.json`, all produced on `rtx` on 2026-08-30. Corpus: `HuggingFaceFW/fineweb-edu` (config `sample-10BT`, ODC-BY license) and `roneneldan/TinyStories` (CDLA-Sharing-1.0), both streamed, never fully downloaded.
