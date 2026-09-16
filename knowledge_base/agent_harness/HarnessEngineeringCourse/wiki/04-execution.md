> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Sandbox, orchestrator, subagents, verification

**In one sentence:** The model only ever asks while the harness executes: sandboxed shell commands, planned-and-gated multi-step runs, parallel subagents with isolated context, and nonce-guarded code verification close the loop.

## Key points

- The sandbox prefers hardened Docker (`--network none`, non-root, scoped workdir) and falls back to a scoped local subprocess when no Docker daemon is available (sandbox.py:4).
- The Docker backend is a genuine containment boundary (network-none, non-root, cap-drop, memory + pid limits, read-only rootfs) while the local fallback is teaching-grade, not a security boundary (sandbox.py:11).
- The orchestrator plans a task into steps, runs them in order through an agent, gates each step with approval, and retries on failure (orchestrator.py:3).
- The planner prompt asks for 2-4 short imperative steps returned as a JSON array only, falling back to the whole task as one step on parse failure (orchestrator.py:21).
- Subagents are bounded loops with fresh isolated context and tools that return only the answer, never the transcript, with independent subtasks fanning out in parallel (subagents.py:3).
- `fan_out` preserves task order and `fan_out_tool` rejects non-list `tasks` input to avoid spawning one subagent per character (subagents.py:30).
- Verification runs candidate code plus an assertion check in a fresh scrubbed-env process, with success signalled by a per-run random nonce printed only after the check completes (verification.py:39).

---

## Sandbox

The execution environment rule is stated up front: the harness runs code, the model never does (sandbox.py:1). The sandbox starts closed — no network, a fresh isolated workdir, and a scrubbed environment with no inherited credentials (sandbox.py:7).

The minimal environment handed to sandboxed commands is quoted verbatim:

```python
_SCRUBBED_ENV = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LC_ALL": "C"}
_MAX_OUTPUT = 100_000  # cap returned output so a chatty command can't flood the window
```

from sandbox.py:40. Output is capped by `_cap` (sandbox.py:44), and timeouts kill the whole process group via `_kill_group` using `os.killpg(proc.pid, signal.SIGKILL)` (sandbox.py:49), with the child made its own group leader through `start_new_session=True` (sandbox.py:53).

The `Sandbox` dataclass-style class is configured verbatim (sandbox.py:71):

```python
def __init__(
    self,
    image: str = "busybox",
    timeout: float = 15.0,
    prefer_docker: bool = True,
    trusted: bool = False,
) -> None:
```

`trusted=True` runs in the real environment (unscrubbed) for a coding agent working on its own project, where the approval gate — not network-none isolation — is the control (sandbox.py:81). Dispatch is `run(command, workdir)` (sandbox.py:104): trusted goes local, otherwise Docker when the daemon is up (probed once via `docker info`, sandbox.py:87), else local fallback.

The Docker invocation is hardened verbatim (sandbox.py:118):

```python
argv = [
    "docker", "run", "--rm",
    "--name", name,
    "--network", "none",
    "--user", "65534:65534",
    "--cap-drop", "ALL",
    "--memory", "256m",
    "--pids-limit", "128",
    "--read-only",
    ...
]
```

with `-v {workdir}:/work` for a persistent workspace or `--tmpfs /work:rw,size=16m` throwaway, `-w /work`, and `sh -c command` (sandbox.py:116). On timeout the named container is explicitly killed with `docker kill` and result code 124 is returned (sandbox.py:134). The local fallback uses `bash -c` with `cwd` set to the workdir or a fresh `tempfile.mkdtemp(prefix="sandbox-")` dir (sandbox.py:141), scrubbed env plus `HOME`/`TMPDIR` pointed at the cwd (sandbox.py:147), and exit code 124 plus `error: timed out` on timeout (sandbox.py:162).

The `bash_tool(sandbox, workdir)` adapter (sandbox.py:169) exposes a `bash` tool whose commands run inside the sandbox, returning `[exit {code} via {backend}]` plus combined stdout/stderr (sandbox.py:173).

## Orchestrator

A single model turn is not a workflow; the orchestrator moves work through time with checkpoints (orchestrator.py:3). The planner prompt is quoted verbatim (orchestrator.py:21):

```python
_PLANNER = (
    "You are a planner. Break the task into 2-4 short imperative steps. "
    "Return ONLY a JSON array of step strings, nothing else."
)
```

`Orchestrator.__init__(model=None, tracer=None)` takes an optional tracer with no behavior change by default (orchestrator.py:35). `_plan` (orchestrator.py:39) calls `chat` with `max_tokens=400` (orchestrator.py:42), records a `plan` span when a tracer is given (orchestrator.py:47), slices the response from the first `[` to the last `]` and parses JSON (orchestrator.py:50), and falls back to `[task]` when parsing yields nothing (orchestrator.py:56).

`run(task, approve=None)` (orchestrator.py:58) lazily imports `Agent` to avoid an import cycle (orchestrator.py:63), defaults approval to always-true (orchestrator.py:65), builds a worker agent with system `"Execute each step using tools when needed. Be concise."` and `default_tools()` (orchestrator.py:67), skips disapproved steps as `[skipped] {step}` (orchestrator.py:74), and returns `OrchestratorResult(plan, results, final)` where `final` is the last result (orchestrator.py:78). `_run_with_retry(worker, step, attempts=2)` (orchestrator.py:81) returns `worker.send(step)` on success and retries any exception, ending with `error: {exc}` (orchestrator.py:86).

## Subagents

Each subagent is a fresh agent with its own isolated context and tools; the default worker system prompt is quoted verbatim (subagents.py:14):

```python
DEFAULT_WORKER_SYSTEM = "You are a focused worker. Do exactly the subtask and answer concisely."
```

`run_subagent(task, *, system=None, model=None, tools=None)` (subagents.py:17) lazily imports `Agent` (subagents.py:24) and sends the task to a new agent with `tools or default_tools()` (subagents.py:26). `fan_out(tasks, *, model=None, max_workers=4)` (subagents.py:30) runs subtasks in a `ThreadPoolExecutor` sized `min(max_workers, len(tasks))`, returns `[]` for empty input (subagents.py:32), and preserves order via `pool.map` (subagents.py:35).

Two tool adapters let the main agent use subagents: `delegate_tool` (subagents.py:38) exposes a `delegate` tool taking a single `task` string (subagents.py:47), and `fan_out_tool` (subagents.py:56) exposes a `fan_out` tool taking `tasks` as an array of strings (subagents.py:79). The fan-out handler validates input — a JSON string instead of a list returns `error: \`tasks\` must be a list of strings` (subagents.py:64) — and joins results labeled `[subtask {i}] {task}` in order (subagents.py:67).

## Verification

The module docstring places it: the sandbox exercise needs it now, but the agent loop does not call it yet — the self-checking feedback loop lands later (verification.py:1). `run_python` keeps the same start-closed posture as the bash sandbox: fresh process, scrubbed environment, scoped temp workdir (verification.py:5).

`extract_code(text)` (verification.py:33) pulls a fenced python block via the `_FENCE` regex `` ```(?:python)?\s*(.*?)``` `` (verification.py:24), returning the text as-is when no fence matches (verification.py:36). `run_python(code, check, timeout=10.0)` (verification.py:39) builds `script = f"{code}\n\n{check}\nprint({nonce!r})\n"` with `nonce = f"VERIFIED-{uuid.uuid4().hex}"` (verification.py:54), writes it to `candidate.py` in a fresh `tempfile.mkdtemp(prefix="verify-")` dir (verification.py:56), and runs `[sys.executable, candidate]` with a scrubbed env of only `PATH`, `HOME`, and `LC_ALL` (verification.py:59). A timeout returns `VerificationResult(False, "error: timed out")` (verification.py:70); otherwise `passed = proc.returncode == 0 and nonce in proc.stdout` (verification.py:72), so candidate code that prints a fixed sentinel and exits early no longer counts as a pass (verification.py:46).

**Covers:** component 04
