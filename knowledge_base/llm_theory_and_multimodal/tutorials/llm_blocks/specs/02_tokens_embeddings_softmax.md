# Task: chapter 02 — tokens, embeddings, softmax, tied LM head

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `01_*.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch02_tokens_embeddings.py`
- `Embedding` from scratch (a lookup into a `(vocab, d)` matrix via indexing; show it equals one-hot × matrix) — test vs `torch.nn.Embedding`.
- `softmax(x, temperature=1.0)` from scratch with the max-subtraction trick — test vs `torch.softmax`; `cross_entropy(logits, targets)` from scratch — test vs `F.cross_entropy`.
- `TiedLMHead(embedding)` — logits = `h @ E.T`; test equals `nn.Linear` with tied weight.
- `plots` (no download): `02_one_hot_lookup.png` (schematic: token id → one-hot → row of E), `02_softmax_temperature.png` (same logits at T = 0.3 / 1 / 3), `02_cross_entropy.png` (loss vs predicted probability of the correct token, log-x, annotate ln(vocab) for a uniform guess with vocab 32000 and 248320), `02_embedding_size.png` (embedding parameters vs vocab size for hidden 768 and 5120; annotate 32k, 151k, 248k).
- `plots_real` (downloads SmolLM2-135M): `02_tokens_example.png` (a sentence split into tokens as coloured boxes, incl. a rare word and a number split into pieces), `02_embeddings_pca.png` (PCA of the input embeddings of ~60 hand-picked tokens: days, months, numbers, countries, punctuation — coloured by group; `sklearn.decomposition.PCA`), `02_nearest_neighbours.txt` is NOT a figure — instead print cosine nearest neighbours of 5 tokens in `demo-real` and quote them in the chapter.
- `demo`: prints the numbers used in the chapter (embedding params for the vocab/hidden pairs, ln(32000), ln(248320)).

## Chapter — `02_tokens_embeddings_softmax.md`
Why models do not read letters (tokens; BPE = byte-pair encoding in two sentences; the real tokens figure; why numbers and rare words split); the embedding matrix as a lookup table of learned vectors (one-hot picture; "the meaning is in the distances" — the PCA figure and the nearest-neighbour printout); vector size = hidden size; how big the table is (figure + Qwen's 248320 × 5120 ≈ 1.27 B parameters — verify the arithmetic; compare with the 32k tokenizer chosen in `../llm_training/02_tokenizer_and_data.md`); from vectors back to words: the LM head (language-model head) as the reverse lookup, tied vs untied weights and when tying is used (small models — Qwen3.5-0.8B ties? load the config and report `tie_word_embeddings`); softmax as "turn scores into probabilities" with the temperature figure; cross-entropy as "surprise" with the figure and the ln(vocab) starting loss — link to what `../llm_training/03_model_from_scratch.md` checks; Troubleshooting; Exercises.

## Scope limits
Attention is chapter 03. No `index.md` edits.
