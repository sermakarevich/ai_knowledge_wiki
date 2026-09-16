> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Two-gate verification and course map

**In one sentence:** Every chapter passes an offline deterministic gate (`verify`) and a live-model gate (`accept`), across a 15-chapter spine where each chapter adds one harness primitive owned by one module.

## Key points

- The course defines two gates because "the tests pass" and "the agent actually works" are different claims (README.md:107).
- `verify` is the offline floor — ruff format plus lint, mypy, pytest, smoke import — while `accept` is the live truth against a real model (README.md:109-112).
- The spine is 15 chapters `ch-00` through `ch-14`, each introducing one harness primitive in its mature form (README.md:57-58).
- Each chapter is its own tagged commit, so `git checkout ch-05` shows the project at chapter 5 and `git checkout main` returns to latest (README.md:114-120).
- Live checks and demos are registered per chapter in two dicts, `ACCEPTANCE` and `DEMOS`, with folded chapters AND-ing all parts so no proven capability is lost (tasks/checks.py:3-8).
- The `tasks/` package is dev tooling only, invoked as `uv run verify` / `accept ch-NN` / `demo ch-NN`, separate from the `model/` and `harness/` runtime (README.md:129).
- The AGENTS.md working rule ships a change only when both gates are green and never claims a chapter works without a green `accept` (AGENTS.md:16-17).

---

## Two gates: floor versus truth

`README.md:107-112` states the rule verbatim:

> Two gates, because "the tests pass" and "the agent actually works" are different claims.
> - **`uv run verify`** is the floor: ruff (format + lint), mypy, pytest, smoke import. Deterministic, offline.
> - **`uv run accept ch-NN`** is the truth: the real agent against a real model, asserting the chapter's capability end to end. A chapter is not done until the agent can really do the thing on a real model.

`AGENTS.md:16-19` restates it as the working contract:

> **Two-gate rule.** `verify` is the floor, `accept` is the truth. Ship a change only when both are green. Never claim a chapter works without a green `accept`.
> - `uv run verify` — ruff format + lint, mypy, pytest, smoke import (deterministic, offline)
> - `uv run accept ch-NN` — the real agent against a real model, asserting the capability

The rationale (`README.md:167-170`) is that a stub returning the right shape proves nothing about a real model, so every chapter passes an offline check and then does the thing for real against a live model; the second gate is slower on purpose.

## Verify: deterministic commit gate

Implemented in `tasks/verify.py:1-4`:

```python
"""Deterministic commit gate: format, lint, types, tests, smoke import.

Runs locally. Hits no network — the live model run is `accept`.
"""
```

Entry point (`tasks/verify.py:19`):

```python
def main(argv: list[str] | None = None) -> int:
```

The sequence (`tasks/verify.py:23-31`):

```python
if _run(["ruff", "format", "--check", "."]) != 0:
if _run(["ruff", "check", "."]) != 0:
if _run(["mypy", "model", "harness", "ui", "tasks"]) != 0:
rc = _run(["pytest"])
if rc not in (0, 5):  # 5 = "no tests collected", expected in the earliest chapters
```

The helper (`tasks/verify.py:14-16`):

```python
def _run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    return subprocess.call(cmd)
```

Smoke import (`tasks/verify.py:34-40`) imports `harness.agent`, `model`, `ui.tui`, and `tasks.checks`, printing `VERIFY OK` (`tasks/verify.py:48`) or `VERIFY FAILED: {failed}` (`tasks/verify.py:46`).

## Accept: live acceptance gate

Implemented in `tasks/accept.py:1-5`:

```python
"""Live acceptance gate: run the real agent against a real model and assert the
chapter's actual capability. REQUIRED before a code commit.

  uv run accept ch-02
"""
```

Entry point (`tasks/accept.py:13`):

```python
def main(argv: list[str] | None = None) -> int:
```

Behavior (`tasks/accept.py:15-26`): it reads the chapter name from argv, prints `usage: uv run accept ch-NN` (`tasks/accept.py:17`) when missing, looks up the check via `from tasks.checks import ACCEPTANCE` (`tasks/accept.py:21`), and returns exit 2 with `no live acceptance check registered for '{chapter}'` (`tasks/accept.py:25`) when unregistered.

It resolves the live target for the banner via `from model.provider import Provider` (`tasks/accept.py:30`) and `cfg = Provider.from_env()` (`tasks/accept.py:32`), printing `== live acceptance: {chapter}  (model={cfg.model} @ {cfg.base_url}) ==` (`tasks/accept.py:33`), then prints `ACCEPT OK` or `ACCEPT FAILED` (`tasks/accept.py:39`).

## Checks and demos registry

`tasks/checks.py:1-8` defines the per-chapter contract:

```python
"""Per-chapter live acceptance checks and on-camera demos.

Each chapter appends an entry:
  ACCEPTANCE["ch-NN"] -> callable returning True/False (asserts the capability live)
  DEMOS["ch-NN"]      -> callable that prints the on-camera demonstration
```

Registries (`tasks/checks.py:15-16`):

```python
ACCEPTANCE: dict[str, Callable[[], bool]] = {}
DEMOS: dict[str, Callable[[], None]] = {}
```

Examples: `ACCEPTANCE["ch-01"] = _accept_ch01` (`tasks/checks.py:66`), `ACCEPTANCE["ch-02"] = _accept_ch02` (`tasks/checks.py:93`), through `ACCEPTANCE["ch-14"] = _accept_ch14` (`tasks/checks.py:831`), plus `ACCEPTANCE["streaming"] = _accept_streaming` (`tasks/checks.py:894`). `ch-00` is theory and registers nothing (`tasks/checks.py:8`).

Demo runner (`tasks/demo.py:12`):

```python
def main(argv: list[str] | None = None) -> int:
```

It prints `usage: uv run demo ch-NN` (`tasks/demo.py:15`) when empty and `no demo registered for '{chapter}'` (`tasks/demo.py:24`) when unknown, looked up via `from tasks.checks import DEMOS` (`tasks/demo.py:20`).

## Course map: 15 chapters, one primitive each

The chapter table (`README.md:60-76`):

| Ch | Title | Primitive |
|----|-------|-----------|
| 00 | What is an agent? | The frame: Model + Harness + UI (theory, no code) |
| 01 | Model only | A single model call behind a thin provider seam |
| 02 | History | Conversation state persists across turns |
| 03 | Instructions | System prompt + auto-loaded project files (AGENTS.md) |
| 04 | Context delivery | `@path` references inject file content the model can't read itself |
| 05 | Tools | The tool interface + file tools + the approval gate |
| 06 | Context management | Cache-stable assembly + compaction + door caps |
| 07 | Skills | Advertise, then load `SKILL.md` procedures on demand |
| 08 | Execution environment | Run commands in a hardened sandbox |
| 09 | Durable state + memory | JSON-L sessions on disk + episodic search |
| 10 | Orchestration | Plan steps, gate each, execute, retry |
| 11 | Subagents | Spawn isolated agents; fan out; return answers, not transcripts |
| 12 | Verification | Run candidate code against an oracle; self-verify |
| 13 | Observability | Trace every LLM/tool call as an OTel `gen_ai.*` span tree |
| 14 | UI: Textual TUI | Transcript, live trace tree, approval modal |

The build starts at `ch-00` with what separates an agent from a chatbot or script (`README.md:78-80`), and each chapter shows the capability failing without the primitive, then working with it, against a real model (`README.md:17-19`).

## Primitive to module map and layout

`README.md:82-103` maps each primitive to its owning module, including provider seam (`model/provider.py`, `model/openai_compatible.py`, `model/client.py`), history (`harness/agent.py`), context delivery (`harness/context.py`), context management (`harness/compaction.py`, `harness/limits.py`), tools (`harness/tools.py`, `harness/workspace.py`), and the UI (`ui/tui.py`).

Layout (`README.md:124-131`):

```text
model/          # the provider seam + costing: provider / openai_compatible / fake / client / pricing
harness/        # the loop + every primitive: agent, context, tools, memory, skills, sandbox,
                #   orchestrator, subagents, verification, observability, events, ...
ui/             # the Textual TUI (the only package that imports textual/rich)
tasks/          # uv-run tooling: verify / accept / demo / tui
tests/episodes/ # one behavioral test file per chapter (test_ch01..test_ch14)
```

Dependencies point one way, `ui/` into `harness/` into `model/`, the core never imports the UI, and the agent loop lives only in `harness/agent.py` (`README.md:133-135`). `AGENTS.md:25-29` repeats the same one-way rule and notes `tasks/` is dev tooling.

**Covers:** component 06
