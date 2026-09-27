# 00 findings — impl (code only)

Handoff notes for the 00 writeup task. Everything below was actually run on 2026-09-04 on this Mac.

## Real `just check` output (exit 0)

```
                             evals_tutorial check
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ check                                 ┃ result                             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Ollama reachable                      │ yes (version 0.32.12)              │
│ chat qwen3.8:27b answers              │ 'OK'                               │
│ chat_json 2-field schema              │ model(word='OK', ok=True) valid    │
│ embedding dim (nomic-embed-text)      │ 768 ok                             │
│ data/public/mt_bench_answers.jsonl    │ 480 rows ok                        │
│ data/public/mt_bench_human_votes...   │ 3355 rows ok                       │
│ data/public/mt_bench_gpt4_votes...    │ 2400 rows ok                       │
│ data/public/ragtruth_test_subset...   │ 480 rows ok                        │
│ cache size                            │ 3 entries, 14.6 KB                 │
└───────────────────────────────────────┴────────────────────────────────────┘
```

Tests: `uv run pytest tests/ -q -m "not slow"` → **7 passed in 0.19 s** (CPU, no network).

## Installed versions (uv 0.11.22, just 1.53.0, Python 3.14.6 for this install)

| package | version | | package | version |
|---|---|---|---|---|
| httpx | 0.28.1 | | numpy | 2.5.2 |
| pydantic | 2.13.5 | | pandas | 3.0.5 |
| pydantic-settings | 2.15.0 | | orjson | 3.12.0 |
| python-dotenv | 1.2.3 | | scikit-learn | 1.9.0 |
| typer | 0.27.2 | | matplotlib | 3.11.1 |
| rich | 15.0.0 | | tiktoken | 0.14.0 |
| pyyaml | 6.0.3 | | pytest | 9.1.1 |
| | | | pytest-timeout | 2.4.0 |

## Ollama models on `rtx` (`/api/tags`, version 0.32.12)

| model | size | digest |
|---|---|---|
| qwen3.8:27b (SUT + default judge) | 17.74 GB (27.3B) | 5f86f5def4438e2ec4aa7fd81fb9a15c0ef64c7234124ea794383b869b3d5253 |
| nomic-embed-text:latest (embeddings, 137M) | 274 MB | 0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f |
| gemma4:latest (8.0B) | 9.61 GB | 6736aa30b08b4ad1f96500c6318287a16787c63d08b0e2dca11300c7404b603c |
| tiny-qwen35-110m-sft / dpo (108.6M) | 117 MB | eac6ee… / 5aea75… |
| embedding extras (bge-m3, snowflake-arctic-embed2, mxbai-embed-large, qwen3-embedding, embeddinggemma, all-minilm) | — | present, unused so far |

## Project tree

```
project/{.env,.env.template,.gitignore,justfile,pyproject.toml,uv.lock}
project/src/evals_tutorial/{__init__,config,check,gpu,llm,testing}.py
project/tests/test_00_setup.py
project/data/public/{README,mt_bench_answers,mt_bench_human_votes,mt_bench_gpt4_votes,ragtruth_test_subset}.jsonl (committed, untouched)
project/data/cache/{chat/<2>/<40>.json,embed/nomic-embed-text/<2>/<40>.json}  # 3 entries, 24 KB
```

## What differed from the spec / decisions

1. **Spec said "the three files in `data/public/`" — the README lists 4 jsonl files.** `check.py` and the test verify all 4 rows-counts (480 / 3355 / 2400 / 480) per the README, which is a superset of the spec's "three files".
2. **`usage_log` is a module-level dict `{"hits": n, "misses": n}`** in `evals_tutorial.llm` (spec: "module-level counter of calls made this process (hits vs live)") — reset on import, so experiments sum it to fill `metrics.json: llm_calls`.
3. **`embed` batches misses into ≤32-text requests** (copy of RAG design) but **writes one cache entry per text** so re-embedding only re-fetches the texts that changed.
4. **`think` default False, sent as a top-level Ollama field** (same as RAG); the reason for it (thinking models burn their answer budget on reasoning) went into the `chat` docstring.
5. **`chat_json` validation-retry message** includes the literal word **"retry"**; the test's `FakeLLM` matches canned answers on substrings, so the retry reply is found by that keyword — a writeup reader should know that coupling.
6. **`Ollama(transport=…)`** is exposed so tests inject `httpx.MockTransport` (RAG's module-level `httpx.post` was not testable this way). Production code path is unchanged.
7. **Python here resolved to 3.14.6** (uv picked the newest; `requires-python = ">=3.12"` is unchanged) — fine on 3.12 too, no version pin added.
8. `check.py` treats **Ollama unreachable or chat failing as hard failures** (exit 1); embedding-dim mismatch and missing public data are reported in the table.

## Observations (worth calling out in the chapter)

- The cache made the whole `just check` re-runnable for free: 3 live calls in `project/data/cache/` (2 chat incl. the `chat_json` pair, 1 embed) cover everything the check needs — re-run costs 0 GPU.
- `qwen3.8:27b`'s single-word "OK" response lands in a few seconds over the tunnel once the model is warm; first call of a session is slower (model load).
