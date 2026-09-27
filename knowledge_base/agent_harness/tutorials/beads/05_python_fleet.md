# 05 — Python driver patterns + fleet orchestration: scripting beads and scaling out

**What you will learn**
- `--json` scripting: `bd list --json | jq` (**JSON** — JavaScript Object Notation, the bracket-and-quotes text format scripts parse; **jq** is a command-line tool that slices and filters JSON)
- `db.py` wrapper patterns: `subprocess` (Python's built-in way of starting other programs), error handling, and parsing
- Batching + idempotency (code you can run twice without damage — **idempotent** means "running it again changes nothing new")
- Tests against a temporary database (`tmp_path` — a throwaway folder pytest creates per test — plus `bd init`)
- Fleet filing: `fleet bd create --cwd <abs> --coder opencode --model opencode-go/muse-spark-1.3-contributor --deps` chains, the spec file format (Problem/Fix/Tests/DoD/Scope), commit-only-own-files + verify + `bd close`
- The worker contract (beads worker: ready → claim → work → commit named paths → verify → close own bead)
- Serialisation (turning a shared tree of beads into a linear `--deps` chain; `isolation_exclude /Users/sergii/.ai` means in-place)
- When to use fleet vs plain `bd`
- Troubleshooting (JSON parse on empty output, claiming an already-claimed bead, fleet races) plus takeaways

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/05_python_fleet`. All command outputs below are real outputs. The `bd` outputs were run in scratch databases created with `bd init --prefix tut` in `/tmp/beads-patterns-tut` and `/tmp/beads-json-tut`, seeded with the shared graph from `project/src/beads_tutorial/seed.py`, and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. This chapter is the beads mirror of the Neo4j tutorial's `05_python_patterns.md`: where Neo4j has a Python driver with sessions and transactions, beads has `db.py` (subprocess + `--json`) and `patterns.py` (claim/close loops) — same ideas, different spelling. This is the final chapter: there is no "next chapter" section at the end.

## 0. The scenario and the shared graph

Same six beads as every chapter (`seed.py`: `ITEMS` + `DEPS`, check-then-create so re-running is safe). Seeding prints the six ids in `ITEMS` order:

```bash
uv run python -m beads_tutorial.seed --cwd /tmp/beads-patterns-tut
```

```
tut-pds
tut-wk4
tut-xei
tut-v57
tut-7ij
tut-dda
```

The mapping for this chapter (yours will differ — ids contain a random hash — but titles and shapes match):

| id | title | type | priority |
|---|---|---|---|
| `tut-pds` | Build website | epic | P1 |
| `tut-wk4` | Design homepage | task | P1 |
| `tut-xei` | Implement homepage | task | P1 |
| `tut-v57` | Write tests | task | P2 |
| `tut-7ij` | Write docs | task | P2 |
| `tut-dda` | Deploy website | task | P1 |

**Priority** is a number 0–4, printed as `P0` (critical) … `P4` (backlog); `P2` is the everyday default. The full list, fresh after seeding — six beads, all `open`:

```bash
bd list
```

```
○ tut-dda ● P1 Deploy website
○ tut-pds ● P1 [epic] Build website
○ tut-wk4 ● P1 Design homepage
○ tut-xei ● P1 Implement homepage
○ tut-7ij ● P2 Write docs
○ tut-v57 ● P2 Write tests

--------------------------------------------------------------------------------
Total: 6 issues (6 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

And who is startable right now — only Design and the epic (everything else waits behind dependencies, chapter 03):

```bash
bd ready --json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(i['id'], '-', i['title']) for i in d]"
```

```
tut-wk4 - Design homepage
tut-pds - Build website
```

A note on running these commands: this machine pins `bd` to the fleet database via the `BEADS_DIR` variable (an environment variable is a named setting inherited by every command you run — chapter 02 troubleshooting covers it). Every `bd` command below was run with that pin removed (`env -u BEADS_DIR bd ...`) from inside the scratch folder, so `bd` uses the scratch database. If your outputs mention a different folder, check `echo $BEADS_DIR` first.

## 1. `--json` scripting: `bd list --json | jq`

Every `bd` read command has a `--json` flag that prints machine-readable JSON instead of the human table. That is the scripting contract this whole chapter builds on: humans read `bd list`, programs read `bd list --json`. One object per bead, same fields every time (`id`, `title`, `description`, `status`, `priority`, `issue_type`, …).

The simplest script is a `jq` one-liner — one compact line per bead:

```bash
bd list --json | jq -r '.[] | "\(.id) \(.status) P\(.priority) \(.title)"'
```

```
tut-8ao open P1 Deploy website
tut-7me open P1 Design homepage
tut-e47 open P1 Implement homepage
tut-i65 open P1 Build website
tut-ngm open P2 Write tests
tut-pcw open P2 Write docs
```

(This ran in a second scratch folder, `/tmp/beads-json-tut`, so the ids differ from §0 — same six titles, same shape.) The `-r` flag means "raw": print plain text, not quoted JSON strings. And counting is trivial:

```bash
bd list --json | jq 'length'
```

```
6
```

Three recipes worth memorizing:

- `bd list --json | jq -r '.[].id'` — just the ids, one per line (feeds `xargs` — a tool that turns lines of text into command arguments — or a `for` loop).
- `bd ready --json | jq -r '.[0].id'` — the first startable bead, or `null` when nothing is ready. That `null` is load-bearing: §3's `claim_next` is exactly this plus a claim.
- `bd list --json | jq '[.[] | select(.status=="open")] | length'` — how many are still open (the scripted version of eyeballing the `Total:` line).

Rule of thumb: `bd list` for your eyes, `bd list --json | jq` for your scripts. Everything from here on — `db.py`, `patterns.py`, the tests — is just this idea with Python holding the pipe.

## 2. `db.py` wrapper patterns: subprocess, errors, parsing

`project/src/beads_tutorial/db.py` is the only module allowed to touch `bd` directly (83 lines — read it whole, it is short). Three patterns inside it cover 90% of what you will ever need:

**Pattern 1: one door for all calls (`run_bd`).** Every command goes through a single function that starts `bd` with `subprocess.run` (Python's built-in way of starting other programs), always in the right folder (`cwd` — current working directory — the project folder whose `.beads/` database you want), and always with `BEADS_DIR` scrubbed from the environment so the fleet pin cannot hijack your scratch database:

```python
def run_bd(*args: str, cwd: str) -> str:
    proc = subprocess.run(
        ["bd", *args], cwd=cwd, capture_output=True, text=True, env=_clean_env()
    )
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(message or f"bd exited with code {proc.returncode}")
    return proc.stdout
```

**Pattern 2: failures become exceptions.** `bd` signals failure with a non-zero exit code; `run_bd` turns that into a Python `RuntimeError` carrying `bd`'s own error text. Callers never check return codes — they either get output or an exception. That is why `seed.py` can write "try adding the dependency, ignore it if it already exists" as plain `try/except RuntimeError` (chapter 03's edges).

**Pattern 3: JSON in, Python out (`bd_json`).** Append `--json` automatically (unless the caller already passed it) and parse the answer:

```python
def bd_json(*args: str, cwd: str) -> list | dict:
    if "--json" not in args:
        args = (*args, "--json")
    return json.loads(run_bd(*args, cwd=cwd))
```

List commands (`ready`, `list`) come back as a Python list of dicts; single-object commands (`create`) as one dict. Two thin helpers sit on top — `bd_create` (returns the new id string) and `bd_ready` (returns the ready list) — and `bd_close` wraps `bd close <ids> [--reason]`. Nothing else in the project imports `subprocess` or calls `bd`: `seed.py`, `explore.py`, and `patterns.py` all go through `db`. One door, one place to fix when `bd` changes.

## 3. `patterns.py`: claim, close, loop

`project/src/beads_tutorial/patterns.py` is the capstone module (under 150 lines, imports only `db`). Three functions, each a direct translation of something you already type by hand:

```python
def claim_next(cwd: str) -> str | None:
    ready = db.bd_ready(cwd=cwd)
    if not ready:
        return None
    bead_id = ready[0]["id"]
    db.run_bd("update", bead_id, "--claim", cwd=cwd)
    return bead_id
```

`claim_next` is the scripted version of "find something startable and take it": `bd ready --json` → first id → `bd update <id> --claim` (sets the assignee to you and the status to `in_progress` in one atomic step — **atomic** means it happens all at once, no other process can slip in between). Empty ready list means `None`, not a crash — the loop in §4 depends on that.

```python
def close_with_reason(bead_id: str, cwd: str, reason: str) -> None:
    db.bd_close([bead_id], cwd=cwd, reason=reason)
```

`close_with_reason` is `bd close <id> --reason "<note>"` — the note is stored with the close action, so future-you (or a teammate) can see *why* it finished, not just *that* it finished. Always pass a reason; bare closes are mysteries a month later.

```python
def ready_loop(cwd: str, limit: int = 5) -> list[str]:
    closed: list[str] = []
    for _ in range(limit):
        bead_id = claim_next(cwd)
        if bead_id is None:
            break
        close_with_reason(bead_id, cwd, "done via ready_loop")
        closed.append(bead_id)
    return closed
```

`ready_loop` chains the two: claim one, close it, repeat up to `limit` times, stop early when nothing is ready. Closing unblocks dependents (chapter 03), so later rounds see beads that were blocked in earlier rounds — the loop drains the graph front-to-back. The **CLI** (Command-Line Interface — the `--flags` you type in the terminal) prints one closed id per line:

```bash
uv run python -m beads_tutorial.patterns --cwd /tmp/beads-patterns-tut --limit 2
```

```
tut-wk4
tut-xei
```

Two rounds: first claimed and closed Design (`tut-wk4`, which was ready), which unblocked Implement (`tut-xei`) — second round claimed and closed that too. The database after the run tells the story:

```bash
bd list
```

```
○ tut-dda ● P1 Deploy website
○ tut-pds ● P1 [epic] Build website
○ tut-7ij ● P2 Write docs
○ tut-v57 ● P2 Write tests

--------------------------------------------------------------------------------
Total: 4 issues (4 open, 0 in progress)
```

Six minus two: Design and Implement are closed. And the new ready list shows the wave moving forward — Tests and Docs are unblocked now:

```bash
bd ready --json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(i['id'], '-', i['title']) for i in d]"
```

```
tut-pds - Build website
tut-7ij - Write docs
tut-v57 - Write tests
```

The epic was ready all along (nothing blocks it); Tests and Docs just joined it. Run the loop again with `--limit 10` and it would drain those three, then Deploy, then report nothing left — each invocation picks up exactly where the last one stopped, because the database remembers.

## 4. Batching + idempotency: run it twice, harm nothing

Two properties make these scripts safe to re-run — important because workers crash, supervisors retry, and humans double-click:

**Check-then-create (seed).** `seed.py` lists existing beads by title first and reuses them; only missing titles get created, and dependency edges whose error message contains "already" are swallowed. The test in `test_seed.py` proves it: seed twice, total stays 6, same ids. New code that creates beads should copy this shape — look up first, create only on miss.

**Stop-on-empty + close-is-final (loop).** `ready_loop` treats "nothing ready" as a normal ending (`None` → `break`), never as an error — so running it on a drained database returns `[]` instead of exploding. And `bd close` on an already-closed bead is accepted quietly, which means a retry that overlaps a finished round does not corrupt anything. The batch size (`limit`, default 5) caps how much one invocation can do — a crashed loop never takes more than `limit` beads with it, and the next run continues from the database state, not from memory.

The general rule: every script in this project derives its next action from the *database* (`bd ready` right now), never from a cached list. Stale plans go wrong; fresh reads do not.

## 5. Tests against a temporary database: `tmp_path` + `bd init`

`project/tests/test_patterns.py` tests the real `bd` binary against a real (throwaway) database — no mocks, no fakes. The trick is three lines:

```python
def _init(repo: str) -> None:
    proc = subprocess.run(
        ["bd", "init", "--prefix", "tut", "--non-interactive"],
        cwd=repo, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
```

`tmp_path` is a folder pytest creates fresh for each test and deletes afterwards — the test seeds it, claims, closes, and asserts, and the real tutorial folder plus the fleet database are never touched. (`monkeypatch.delenv("BEADS_DIR", raising=False)` removes the fleet pin inside the test process so `bd` discovers the database from `cwd`, same as `db.py` does. **Monkeypatch** is pytest's helper for temporarily changing settings during one test.)

Two tests:

- `test_claim_next_returns_id_and_close_removes_from_ready` — seed, `claim_next` returns a real id, the claimed bead is gone from `bd ready`, close it with a reason, and it stays out of ready while still existing in `bd list --all` (closed beads exist; they are just filtered from the default views — chapter 04, §1).
- `test_ready_loop_closes_batch` — seed, `ready_loop(repo, limit=2)` closes exactly 2, neither is in ready afterwards, and a follow-up loop on the drained remainder returns a plain list without crashing.

The full suite (`just test`, i.e. `uv run pytest tests -q`) is green — four test files, six tests:

```
......                                                                   [100%]
6 passed in 54.72s
```

The `justfile` (the file that stores short project commands — run `just --list` to see them) grows one additive recipe for this chapter; existing recipes are untouched:

```
# Claim+close demo loop over the tutorial graph.
patterns repo=".":
    uv run python -m beads_tutorial.patterns --cwd {{repo}}
```

`just patterns repo=/tmp/beads-patterns-tut` runs the §3 demo; `repo` defaults to the current folder.

## 6. Fleet filing: turning a spec into parallel beads

`patterns.py` automates one database. **Fleet** automates *people-shaped* work: it pulls beads from one central queue and runs a coding agent (a program like `opencode` that writes code) on each, in parallel, each in its own folder. You file the work; fleet runs it. Three commands carry the whole workflow: file (`fleet bd create`), inspect (`fleet bd ready`), supervise (`fleet tasks`).

**Filing one bead.** This is the exact shape — title first, then flags:

```bash
fleet bd create "beads tut 05_python_fleet" --cwd /Users/sergii/.ai -p 2 -t task --body-file /abs/spec.md --coder opencode --model opencode-go/muse-spark-1.3-contributor
```

Piece by piece: the title in quotes; `--cwd /Users/sergii/.ai` pins the task's working folder to an absolute path (fleet needs the full path because workers may start anywhere); `-p 2` is priority P2 (everyday default); `-t task` is the bead type; `--body-file /abs/spec.md` reads the work description from a file (long specs do not belong on the command line); `--coder opencode` picks the agent program; `--model opencode-go/muse-spark-1.3-contributor` picks the language model behind it. `fleet bd create` is `bd create` plus interception: `--coder`, `--model`, `--cwd` (and `--deps`, `--isolation`, `--worker`) are stored as per-task instructions instead of being forwarded to `bd`.

**The spec file format.** `--body-file` points at a short markdown spec with five sections — Problem (what hurts), Fix (exactly which files to create or change), Tests (the command that must go green), DoD (**Definition of Done** — the numbered checklist that decides "finished"), Scope & constraints (working folder, which paths may be touched, what is forbidden). This chapter's own task spec is the example: it names exactly two files to create, the `patterns.py` function signatures, the pytest command, the four allowed paths, and "no edits to other chapters". A worker that gets a spec like that needs no further guidance.

**Chaining with `--deps`.** A shared tree of beads becomes a linear worker chain by passing `--deps <id>` on the create call: bead B lists bead A as a dependency, so fleet starts B only after A closes. Three beads filed with `--deps` chaining run strictly in order even though they share one folder — that ordering is what §8 is about.

**Inspect and supervise.** `fleet bd ready` lists queue beads with no blockers (the fleet-wide twin of `bd ready`):

```bash
fleet bd ready
```

```
✨ No ready work found (all issues have blocking dependencies)
```

Empty is a real answer: everything filed is waiting on something else. And `fleet tasks` shows what is actually running right now — ids, elapsed time, context usage, coder and model per task:

```bash
fleet tasks
```

```
                             Fleet — running tasks
┏━━━━━━━┳━━━━━┳━━━━┳━┳━━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳┳┓
┃ID     ┃ St… ┃ E… ┃ ┃ Conte… ┃ … ┃ Cod… ┃ Model                             ┃┃┃
┡━━━━━━━╇━━━━━╇━━━━╇━╇━━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇╇┩
│fleet… │ 16… │ 2… │ │ 40.0k… │ … │ ope… │ opencode-go/muse-spark-1.3-contr… │││
│fleet… │ 16… │ 2… │ │ 95.3k… │ … │ ope… │ opencode-go/muse-spark-1.3-contr… │││
└───────┴─────┴────┴─┴────────┴───┴──────┴───────────────────────────────────┴┴┘
```

Two workers mid-flight, both on `opencode-go/muse-spark-1.3-contributor`. File with `fleet bd create`, check startability with `fleet bd ready`, watch with `fleet tasks` — that is the whole filing loop.

## 7. The worker contract: ready → claim → work → commit → verify → close

A fleet worker is a loop with six steps, and every step has exactly one correct behavior. (Note the beads worker reads its instructions from the *bead body*, not from a `STATE.md` file — `STATE.md` is fleet-supervisor memory; the bead spec is the worker's orders.)

1. **Ready** — find your bead (fleet assigns it; `fleet bd ready` shows the queue). Never grab someone else's bead.
2. **Claim** — mark it yours before touching anything (`bd update <id> --claim`, exactly what `claim_next` does). Unclaimed work invites double-work.
3. **Work** — do only what the spec's Fix section names. Named paths, nothing else: this chapter's spec allowed four paths and forbade other chapters — a worker that "helpfully" reformats chapter 03 fails review.
4. **Commit** — small, named-path commits as you go (`git add <the spec's paths>`, then `git commit -m "..."`). Commit-only-own-files: `git status` before every commit, stage only the spec's paths, never `git add -A` (which stages everything, including other workers' files).
5. **Verify** — run the spec's Tests command yourself (`uv run pytest tests -q` here) plus the DoD checks (`git show HEAD:<path> | grep -c ...`, real command output, not memory).
6. **Close own bead** — `fleet bd close <your-id> --reason "05 done"`, only your own id, only after verify is green. Closing someone else's bead (or closing before tests pass) strands the chain behind you.

Steps 2, 5, and 6 are where chains break: skip the claim and two workers do the same bead; skip verify and the next bead builds on broken code; close the wrong bead and its real owner loses their work record. The contract is short on purpose — six steps, no improvisation.

## 8. Serialisation: one folder, many beads, zero clobbers

The fleet default gives each bead an isolated copy of the project (a **worktree** — a separate folder with the same files, so two workers cannot overwrite each other). This tutorial's beads all set `--cwd /Users/sergii/.ai` with `isolation_exclude /Users/sergii/.ai` — plain words: every worker edits the *same* folder, in place, no copies. That is faster and simpler, but it removes the safety net: two workers writing the same tree at the same time will clobber (overwrite) each other's files.

The fix is **serialisation** — forcing an order on work that shares a folder. Two mechanisms:

- **Linear `--deps` chains.** File bead B with `--deps <A-id>` and fleet will not start B until A closes. A chain of five tutorial beads filed this way runs strictly one-at-a-time through the shared tree: each worker sees the previous worker's commits, never a half-written middle state. Parallel speed is traded for correctness — the right trade when everyone edits one folder.
- **Non-overlapping paths.** Each spec's Fix section names disjoint files (chapter 03 touched `03_dependencies.md`, this chapter touches `05_python_fleet.md` + `patterns.py` + `test_patterns.py` + `justfile`). Even if two beads in the chain ever overlapped in time, they write different files. Belt and suspenders: order *plus* disjoint paths.

When the shared tree bites anyway, the symptom is unmistakable: your commit contains another worker's files, or your tests fail on code you never wrote. Recovery: `git status` to see the damage, unstage what is not yours, re-run your spec's Tests command, and tell the supervisor the chain needs re-linearising (a missing `--deps` on the create call is the usual cause — §9).

## 9. When to use fleet vs plain `bd`

- **Plain `bd`** — you are doing the work yourself, right now, in one terminal: `bd create` a reminder, `bd ready` each morning, `bd close` when done, `patterns.py` for scripted loops. Zero setup, instant answers.
- **Fleet** — the work splits into beads that different agents can do without talking to each other: five tutorial chapters, each with its own files and its own tests, filed once and drained over an afternoon. Setup cost (spec files, `--deps` chains, watching `fleet tasks`) pays off at three-plus beads; below that, just do it yourself with `bd`.
- **The middle ground** — `patterns.py`-style scripts *inside* a fleet worker: the worker claims its bead, then runs a local claim/close loop over a sub-graph, then closes the bead. Fleet for the coarse split (which agent does what), scripts for the fine split (which bead next). This chapter's task ran exactly that way: one fleet bead, one worker, scripts plus tests inside.

One sentence: `bd` tracks work, `patterns.py` works a queue, fleet works many queues with many hands.

## 10. Troubleshooting

**`json.loads` explodes on empty output.** `bd_json` runs `json.loads` on whatever `bd` printed. If `bd` prints nothing (or a human sentence like `No issues found` instead of JSON — some commands do that on empty results), parsing fails with `json.decoder.JSONDecodeError: Expecting value`. Fixes: prefer commands whose empty answer is `[]` or `null` (`bd ready --json` prints `[]` when empty — safe); when scripting a command with a chatty empty answer, check the raw text first (`out = run_bd(...); json.loads(out or "[]")`). `claim_next` never hits this because `bd_ready` always returns a JSON list.

**Claiming an already-claimed bead.** `bd update <id> --claim` on a bead someone else holds fails (or, with `bd ready --claim`, silently picks a different bead — the ready list excludes `in_progress`, so a claimed bead is invisible to the next claimer). If your `claim_next` returns an id you did not expect, re-read `bd ready`: the list moved under you because another worker claimed first. Derive every action from a fresh read (§4) and this stops happening.

**Fleet race: `--deps` must be on the create call.** Dependencies are read when the bead is filed. Filing three beads and *then* wiring dependencies leaves a window where all three look ready and start together on the shared tree — the clobber from §8. Correct order: create A, then create B with `--deps <A>`, then C with `--deps <B>`, checking `fleet bd ready` between calls. No retroactive ordering.

**Shared-tree clobber → chain linearly.** Symptom: your commit has another worker's files, or tests fail on code you never wrote. Cause: two workers in one folder at once. Fix now: `git status`, unstage everything outside your spec's paths, re-run Tests. Fix forever: linear `--deps` chain (§8) plus disjoint file sets per spec. `isolation_exclude /Users/sergii/.ai` means in-place by design — ordering is the isolation.

**`BEADS_DIR` hijack.** Scripts that work in tests but talk to the wrong database in your terminal are reading the fleet pin. `db.py` scrubs it, tests scrub it with `monkeypatch.delenv`, and your terminal scrubs it with `env -u BEADS_DIR`. Three places, same one-line habit.

## Takeaways

- `--json` is the scripting contract: humans read tables, programs read `bd list --json | jq`, and `db.py` is that pipe in Python form (one door: `run_bd`; failures as exceptions; `bd_json` for parsing).
- `patterns.py` reduces queue work to three verbs — `claim_next` (ready → first id → claim), `close_with_reason` (close with a note), `ready_loop` (claim + close up to `limit`, stops on empty) — all derived from fresh reads, all safe to re-run.
- Tests use a real `bd` in a throwaway folder (`tmp_path` + `bd init --prefix tut`), so green means it works against the actual binary, not a mock.
- Fleet scales the same verbs across agents: file precise specs with `fleet bd create` (absolute `--cwd`, `--coder`, `--model`, `--body-file`, `--deps` chains), watch with `fleet bd ready` / `fleet tasks`, and hold every worker to ready → claim → work → commit own files → verify → close own bead.
- Sharing one folder means ordering is isolation: linear `--deps` chains plus disjoint paths, or accept the clobber.

That closes the tutorial. From here the index (`ai show research_topics/agent_harness/tutorials/beads/00_setup` is the front door — ask your assistant for the index page listing all chapters) is the map: 00 sets up the project, 001 explores an unknown database, 01 teaches the bead lifecycle, 02 creates and updates, 03 wires dependencies, 04 searches and counts, and this chapter scripts it all and hands the queue to a fleet. Pick any chapter and re-run its commands — the scratch folders are cheap, the seed graph is idempotent, and `bd` remembers.
