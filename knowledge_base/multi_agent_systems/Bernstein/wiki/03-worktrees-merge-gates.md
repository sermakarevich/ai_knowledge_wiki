> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Per-Task Worktrees, Isolation, and Merge Gates
**In one sentence:** Each task runs in its own git worktree (a separate checked-out copy of the repo) on its own branch, and its work reaches the main branch only after passing checks and a one-at-a-time merge queue.
## Key points
- Each agent session gets its own git worktree under `.sdd/worktrees/<session_id>`, so two agents never write to the same files (`src/bernstein/core/git/worktree.py:3`, `src/bernstein/core/git/worktree.py:40`).
- Each session works on its own branch named `agent/<session_id>`, which is how the system knows which change belongs to which task (`src/bernstein/core/git/merge_queue.py:47`, `src/bernstein/core/worktrees/change_set.py:146`).
- The only shared state between agents is the task list (backlog); a task is claimed with CAS (compare-and-swap, a check that the task version is unchanged before taking it) so two workers cannot claim the same task (`src/bernstein/core/tasks/task_lifecycle.py:2593`).
- Before a merge lands, quality gates can run: lint with ruff, type check with pyright, and tests (`src/bernstein/core/quality/quality_gates.py:203`, `src/bernstein/core/quality/quality_gates.py:205`, `src/bernstein/core/quality/quality_gates.py:207`).
- Merges are serialized (run one at a time, never in parallel) through a FIFO (first-in-first-out) merge queue (`src/bernstein/core/orchestration/orchestrator.py:870`, `src/bernstein/core/git/merge_queue.py:200`).
- Conflicts are detected before merging with `git merge-tree`, which simulates a merge without touching files (`src/bernstein/core/git/merge_queue.py:139`); a real merge that conflicts is aborted with `git merge --abort` (`src/bernstein/core/git/git_pr.py:446`).
- Tasks that produce files instead of code (artifact mode) get a plain directory under `.sdd/workspaces/<session_id>` with no branch and nothing to merge (`src/bernstein/core/agents/spawner_worktree.py:33`, `src/bernstein/core/tasks/artifact_completion.py:168`).
- Worktrees can be turned off with the `use_worktrees` flag (default on); when off, no worktree manager is created (`src/bernstein/core/agents/spawner_core.py:1636`, `src/bernstein/core/agents/spawner_worktree.py:95`).
---
## Worktree creation per task
A worktree is a second checkout of the same git repo in another directory. Bernstein creates one per agent session. The module docstring states the layout (`src/bernstein/core/git/worktree.py:1`):
```
"""WorktreeManager - git worktree lifecycle for agent session isolation.
```
The base directory constant is (`src/bernstein/core/git/worktree.py:40`):
```
_WORKTREE_BASE = ".sdd/worktrees"
```
Usage from the same docstring (`src/bernstein/core/git/worktree.py:9`):
```
    worktree_path = mgr.create("session-abc123")
```
At spawn time the orchestrator calls `worktree_mgr.create(session_id)` and records the path per session (`src/bernstein/core/agents/spawner_core.py:4888`). The classifier, which lists and inspects worktrees, looks in the new location first and falls back to the old one (`src/bernstein/core/worktrees/classifier.py:193`):
```
    runtime = repo_root / ".sdd" / "runtime" / "worktrees"
```
```
    return repo_root / ".sdd" / "worktrees"
```
The supervisor for detached runs (runs that continue without a connected client) keeps its own state under a different path, `<sdd>/runtime/run-service/<run-id>` (`src/bernstein/core/run_service/paths.py:3`), not under the worktree tree. Over SSH (Secure Shell, remote login), per-task worktrees are provisioned under a configured remote root (`src/bernstein/core/run_service/ssh_runner.py:89`):
```
        remote_root: Absolute POSIX path on the host under which per-task
            worktrees are provisioned.
```
## Branch per agent
Every worktree sits on a branch named after its session. The merge-queue job builds the name (`src/bernstein/core/git/merge_queue.py:46`):
```
    def __post_init__(self) -> None:
        self.branch_name = f"agent/{self.session_id}"
```
The change-set resolver, used to answer "which files did this task change", builds the same name (`src/bernstein/core/worktrees/change_set.py:146`):
```
    branch = f"agent/{session_id}"
```
It diffs that branch against the integration branch (default `main`, see `src/bernstein/core/worktrees/classifier.py:73`) using three-dot diff from the fork point, not from the current tip (`src/bernstein/core/worktrees/change_set.py:19`).
## What is shared vs isolated
Isolated per task: working directory, checked-out branch, uncommitted edits, and test runs. Each agent edits only its own worktree, so file writes cannot collide during work.
Shared: the task backlog (the list of open tasks) and the integration branch (`main`). The backlog is claimed atomically, meaning the claim is one indivisible step. The claim code comment says (`src/bernstein/core/tasks/task_lifecycle.py:2592`):
```
        # Claim tasks BEFORE spawning to prevent duplicate agents.
        # Pass expected_version for CAS (compare-and-swap) to prevent two
        # distributed nodes from claiming the same task simultaneously.
```
CAS = compare-and-swap: the store only grants the claim if the task version matches what the worker read, so two workers racing for one task cannot both win. The integration branch is shared at merge time only, guarded by the merge queue below.
## Merge gates (lint, type check, test)
Gates run on the still-alive worktree before the merge lands (`src/bernstein/core/agents/spawner_merge.py:414`):
```
    """Run quality gates on the agent's worktree before merging into base branch (#4393).
```
The gate configuration defaults are (`src/bernstein/core/quality/quality_gates.py:201`):
```
    enabled: bool = True
    lint: bool = True
    lint_command: str = "ruff check ."
```
Type check and test defaults (`src/bernstein/core/quality/quality_gates.py:204`):
```
    type_check: bool = False
    type_check_command: str = "pyright"
    tests: bool = False
    test_command: str = "uv run python scripts/run_tests.py -x"
```
So lint (ruff, a Python checker) is on by default; type check (pyright, a type checker) and tests are opt-in per seed config (`bernstein.yaml`). A blocking failure refuses the merge and leaves the agent branch unmerged (`src/bernstein/core/agents/spawner_merge.py:416`). The module header summarizes the rule (`src/bernstein/core/quality/quality_gates.py:1`):
```
"""Automated quality gates: lint, type-check, test, mutation, and intent verification gates.
```
There is also an evidence gate that seals a proof-of-done bundle at completion. It is fail-open, meaning sealing errors never block completion (`src/bernstein/core/evidence/completion_gate.py:103`):
```
    except Exception as exc:  # fail-open: sealing must never fail a task completion
```
## Merge queue serialization
The orchestrator holds one queue (`src/bernstein/core/orchestration/orchestrator.py:870`):
```
        # FIFO merge queue: serializes branch merges so only one runs at a time.
```
```
        self._merge_queue = MergeQueue()
```
The queue class docstring (`src/bernstein/core/git/merge_queue.py:200`):
```
class MergeQueue:
    """Thread-safe FIFO queue for serializing branch merges.
```
Callers use the `submit` context manager, which enqueues and blocks until the job is at the head of the queue, then holds the merge lock while git runs (`src/bernstein/core/git/merge_queue.py:277`). The drain path (graceful shutdown) instead merges via an agent that cherry-picks (copies individual commits onto `main`) branch by branch, which is a separate shutdown-time flow (`src/bernstein/core/orchestration/drain_merge.py:1`).
## Conflict handling
Two layers. First, a pre-flight check simulates the merge without touching the working tree or index (`src/bernstein/core/git/merge_queue.py:139`):
```
def detect_merge_conflicts(branch: str, base: str, cwd: Path) -> ConflictCheckResult:
    """Pre-flight conflict check using ``git merge-tree`` (no working-tree changes).
```
Second, the real merge runs staged but uncommitted (`src/bernstein/core/git/git_pr.py:374`):
```
        merge_r = run_git(
            ["merge", "--no-commit", "--no-ff", branch],
            cwd,
            timeout=120,
        )
```
If the merge output shows conflicts, it is aborted and the conflicting file list is returned (`src/bernstein/core/git/git_pr.py:443`):
```
    conflicts = _parse_conflict_files(cwd)
    if conflicts:
        # Abort the conflicted merge to restore clean state
        run_git(["merge", "--abort"], cwd, timeout=10)
        return MergeResult(success=False, conflicting_files=conflicts)
```
A merge that would stage forbidden paths (`.sdd/` runtime state, signing material, secrets, `bernstein.yaml`) is also aborted before commit (`src/bernstein/core/git/git_pr.py:404`). Conflicting branches are left intact so an operator can inspect them; the drain-time merge agent aborts a cherry-pick and skips the branch when lint or tests fail (`src/bernstein/core/orchestration/drain_merge.py:70`):
```
        "5. After cherry-pick: run `uv run ruff check src/` -- if it fails, "
        "run `git cherry-pick --abort` and SKIP\n"
        "6. Then run `uv run python scripts/run_tests.py -x` -- if tests fail, "
        "run `git cherry-pick --abort` and SKIP\n"
```
## Artifact-mode workspaces (.sdd/workspaces/)
A session whose tasks all complete via signed receipts instead of commits needs no git checkout. The decision point is (`src/bernstein/core/tasks/artifact_completion.py:168`):
```
def needs_git_worktree(tasks: Sequence[Task]) -> bool:
    """Return ``True`` when the session spawned for ``tasks`` needs a git worktree.
```
Such a session gets a plain directory. The constant and creator are (`src/bernstein/core/agents/spawner_worktree.py:33`):
```
ARTIFACT_WORKSPACES_RELPATH = ".sdd/workspaces"
```
```
    workspace = repo_root / ARTIFACT_WORKSPACES_RELPATH / session_id
```
It is a sibling of `.sdd/worktrees` on purpose, so worktree cleanup never treats a plain directory as a checkout (`src/bernstein/core/agents/spawner_worktree.py:30`). The docs note this directory is working-directory separation, not kernel-level isolation (the OS kernel does not wall it off) (`docs/architecture/sandbox.md:535`):
```
- An artifact-mode task (issue #2996) runs in a plain directory under
  `.sdd/workspaces/` instead of a git worktree. The same caveat applies:
  that directory is working-directory separation, not kernel-level
  isolation - choose a sandboxed backend for untrusted code regardless
  of a task's output mode.
```
## Sandbox backends (opt-in)
Historically the only sandbox (isolation mechanism) was a local git worktree (`docs/architecture/sandbox.md:3`). The backend choice is now pluggable: worktree, docker, e2b, modal, daytona, blaxel, runloop, vercel, microvm (`docs/architecture/sandbox.md:14`). The `sandbox:` block in `plan.yaml` (the run plan file) is optional (`docs/architecture/sandbox.md:472`):
```
`sandbox:` is entirely optional. When omitted the stage runs in the
worktree backend - byte-identical to the pre-pluggable-sandbox
behaviour.
```
Stronger backends are opt-in (the operator must ask for them): remote and VM (virtual machine) backends need installs, keys, or explicit config, and `microvm` is never auto-selected (`docs/architecture/sandbox.md:98`). The worktree backend shares the host filesystem and network; it does not isolate at the kernel level (`docs/architecture/sandbox.md:533`).
## How to disable worktrees
The spawner takes a flag, on by default (`src/bernstein/core/agents/spawner_core.py:1636`):
```
        use_worktrees: bool = True,
```
When off, no manager is created (`src/bernstein/core/agents/spawner_worktree.py:95`):
```
    if not use_worktrees:
        return None
```
Without a manager the agent falls back to the main workdir, and isolation is reported as `none` instead of `worktree` (`src/bernstein/core/agents/spawner_core.py:6194`). One call site always forces worktrees on for isolation plus auto-commit (`src/bernstein/core/orchestration/orchestrator.py:7232`).
**Covers:** src/bernstein/core/git/worktree.py, src/bernstein/core/worktrees/classifier.py, src/bernstein/core/worktrees/change_set.py, src/bernstein/core/git/merge_queue.py, src/bernstein/core/git/git_pr.py, src/bernstein/core/agents/spawner_merge.py, src/bernstein/core/quality/quality_gates.py, src/bernstein/core/evidence/completion_gate.py, src/bernstein/core/agents/spawner_core.py, src/bernstein/core/agents/spawner_worktree.py, src/bernstein/core/tasks/artifact_completion.py, src/bernstein/core/tasks/task_lifecycle.py, src/bernstein/core/orchestration/orchestrator.py, src/bernstein/core/orchestration/drain.py, src/bernstein/core/orchestration/drain_merge.py, src/bernstein/core/run_service/paths.py, src/bernstein/core/run_service/ssh_runner.py, docs/architecture/sandbox.md
