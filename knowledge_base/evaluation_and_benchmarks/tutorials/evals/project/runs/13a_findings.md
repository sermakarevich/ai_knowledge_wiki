# Chapter 13a findings — self-host Langfuse + the `prod` CLI

**One live run against a real Langfuse v4.30.0 stack (compose profile `langfuse`), then torn down.** All model calls came from the disk cache (`data/cache`) — the zero-LLM budget was kept. 209 offline tests + 1 marked-`slow` live test all pass.

## Stack

- Compose file `docker-compose.yml`, **profile `langfuse`**: 6 services, all named `evals-*` (`langfuse-web`, `langfuse-worker`, `postgres`, `clickhouse`, `redis`, `minio`).
- Only the UI exposes a host port, and it's `3030 → 3000` — nothing else is published. The 5 storage/data services are reachable on the internal network only.
- Volumes are all `evals-langfuse-*` so a later stack or project can't collide.
- Image tag used: `docker.langfuse.com/langfuse/langfuse:4` → resolved to the **4.30.0** build (health: `{"status":"OK","version":"4.30.0"}`).
- Bootstrap via `LANGFUSE_INIT_*` env vars (org/project/user + public/secret keys), read by `evals-langfuse-web` on first start. Keys are the same ones in `.env` (gitignored).

## What we pushed, and where

| prod command | result |
|---|---|
| `trace --run answer_v1` | 80 traces pushed; `ticket_id → trace_id` map saved to `data/langfuse/answer_v1` |
| `dataset` | `helpdesk-test` 60 items, `helpdesk-dev` 20 items (each item carries `ticket_id` in metadata) |
| `experiment --version v1` | 60 items, 60 traced, 60 scored |
| `experiment --version v2` | 60 items, 60 traced, 60 scored |
| `scores --run answer_v1` | 80 `human_pass` scores attached to 80 traces (0 skipped) |
| `ci`, `monitor` | chapter **13b** stubs — print a pointer and **exit 2** |

Scores attached: `judge_overall_pass` (ch-05), `all_checks_pass` (ch-04), and `human_pass` (ch-03 labels).

## Gotchas hit while wiring it up (real, not hypothetical)

1. **`.env` keys vs. the SDK's auto-client.** `langfuse`'s `@observe` decorator builds its client from *OS* env, not our pydantic-settings `.env`. With no OS keys it silently degrades to a disabled client ("client will be disabled"). Fix: `tracing.client()` explicitly instantiates a keyed client (from settings) so it becomes the SDK's registered singleton — `get_client(public_key=None)` then returns a client bound to our keys. `tracing.observe()` calls `client()` first for exactly this reason.
2. **`helpdesk.answer` had to stay importable with *no* server.** `observe()` is an identity wrapper when no keys are set, so tests and the offline suite never need a Langfuse stack.
3. **`dict(item)` loses `metadata` on the way into `run_experiment`.** The evaluator needs `ticket_id` from the item's metadata, so the `data=` list is mapped explicitly to `{input, expected_output, metadata}` before the call.
4. **`create_dataset_item` with `id=...` is an upsert** — editing `ticket["id"]` won't replace an existing item's metadata. We deleted the stale datasets/items via the REST API in `upsert_datasets()`, then recreated, so `ticket_id` metadata is present.
5. **Langfuse v4 is `events_only`**: the legacy `GET /api/public/traces/{id}` endpoint returns 404. Scores/OTLP writes still work; reading a single trace by id via the SDK's `api.trace.get` does not (that's a ch-13b/online-UI concern, not a data-loss issue).
6. **Zero-LLM budget held during the live run:** the task function calls `helpdesk.answer` (which is `@observe`-wrapped), but every chat/embed call inside `answer` hits `data/cache` — no Ollama was ever hit during `prod-*`.

## Files that changed / were added

- `docker-compose.yml` (new)
- `.env.template` (+ Langfuse host/keys + `LANGFUSE_INIT_*`)
- `justfile` (+ `langfuse-up|down|logs`, `prod-trace|dataset|experiment|scores`; quoted a `trials=` value)
- `src/evals_tutorial/config.py` (+ `langfuse_*` settings)
- `src/evals_tutorial/tracing.py` (new: `is_live`, `observe`, `client`)
- `src/evals_tutorial/helpdesk.py` (`answer` now `@observe`)
- `src/evals_tutorial/prod.py` (new: `trace`, `dataset`, `experiment`, `scores`, `ci`, `monitor`)
- `tests/test_13_prod.py` (new)
