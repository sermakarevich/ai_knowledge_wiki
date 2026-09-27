> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Workspaces and Worktrees: Branch, Terminal, Dev Server per Task
**In one sentence:** A workspace is one database row plus one on-disk container directory holding one git worktree per attached repository, all checked out to a single auto-generated branch, with ephemeral terminal (PTY — pseudo-terminal, an interactive shell session) sessions and per-repo dev-server processes layered on top as execution-process records that do not survive a server restart.

## Key points
- A workspace is persisted as a `workspaces` row (`id`, `task_id`, `container_ref`, `branch`, `archived`, `pinned`, `name`, `worktree_deleted`) plus `workspace_repos` join rows recording each repo's `target_branch`, with runtime state derived from `sessions` and `execution_processes` rather than stored on the workspace itself (`crates/db/src/models/workspace.rs:41-54`, `crates/db/src/models/workspace_repo.rs:11-21`, `crates/db/src/models/execution_process.rs:61-78`).
- One workspace maps to exactly one branch name shared across all its repos, and to one container directory containing one git worktree per repo at `<container>/<repo_name>` (`crates/workspace-manager/src/workspace_manager.rs:290-371`, `crates/local-deployment/src/container.rs:1243-1287`).
- Branch creation is a plain local branch at the tip of the target branch (`GitService::create_branch`), followed by `git worktree add`; recovery never force-resets branches but recreates missing worktrees idempotently (`crates/git/src/lib.rs:193-204`, `crates/git/src/cli.rs:85-108`, `crates/workspace-manager/src/workspace_manager.rs:373-425`).
- Terminal access is an ephemeral WebSocket (a persistent bidirectional connection) to a fresh server-side PTY (pseudo-terminal) process that is destroyed when the socket closes; there is no reattach, no persistence, and nothing is restored on reboot (`crates/server/src/routes/terminal.rs:52-166`, `crates/local-deployment/src/pty.rs:48-155`).
- Dev servers are not port-managed resources: starting one kills any running dev server for the workspace and spawns one `ExecutionProcess` with `run_reason='devserver'` per repo that has a non-empty `dev_server_script`, each running the script with `working_dir=<repo_name>` (`crates/server/src/routes/workspaces/execution.rs:37-137`, `crates/db/src/models/execution_process.rs:50-59`).
- A server restart preserves database rows, branches, committed files, and worktree directories, but kills in-flight child processes on shutdown, marks every `status='running'` execution as `failed` on boot, drops all PTY sessions and dev-server processes, and lazily recreates missing worktrees on next access while sweeping unreferenced directories (`crates/server/src/startup.rs:132-192`, `crates/services/src/services/container.rs:272-326`, `crates/local-deployment/src/container.rs:1603-1633`, `crates/workspace-manager/src/workspace_manager.rs:538-555`).

---
## 1. Workspace data model
### 1.1 `workspaces` row
The `Workspace` struct in `crates/db/src/models/workspace.rs:41-54` is the source of truth for workspace identity:

```rust
pub struct Workspace {
    pub id: Uuid,
    pub task_id: Option<Uuid>,
    pub container_ref: Option<String>,
    pub branch: String,
    pub setup_completed_at: Option<DateTime<Utc>>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub archived: bool,
    pub pinned: bool,
    pub name: Option<String>,
    pub worktree_deleted: bool,
}
```

Field semantics, each backed by model code:
- `id` is generated client-side as `Uuid::new_v4()` before insert (`crates/server/src/routes/workspaces/create.rs:27-48`); `branch` is a git branch name string, non-null since migration `20250923000000_make_branch_non_null` (`crates/db/migrations/`).
- `container_ref` is `Option<String>` holding the absolute workspace container directory path; it starts as `NULL` at `INSERT` (`crates/db/src/models/workspace.rs:311-330`) and is filled in after the directory is created via `Workspace::update_container_ref` (`crates/db/src/models/workspace.rs:138-154`). Path-prefix resolution for editor clients is done by `resolve_container_ref_by_prefix` / `best_matching_container_ref` (`crates/db/src/models/workspace.rs:348-389`).
- `task_id` links a workspace to an optional task row (`crates/db/src/models/task.rs:23-33`); tasks themselves carry `parent_workspace_id` for follow-up chains (`crates/db/src/models/task.rs:30`).
- `archived` / `pinned` / `name` are user-facing list state mutated by `Workspace::update` and `Workspace::set_archived` (`crates/db/src/models/workspace.rs:391-435`); archiving also drives accelerated expiry (1h vs 72h) in `find_expired_for_cleanup` (`crates/db/src/models/workspace.rs:252-309`).
- `worktree_deleted` is a tombstone flag set by `mark_worktree_deleted` and cleared by `clear_worktree_deleted` (`crates/db/src/models/workspace.rs:156-180`); `ensure_container_exists` clears it after a successful recreate (`crates/local-deployment/src/container.rs:1276-1278`).
- `updated_at` is bumped on every access via `Workspace::touch`, itself debounced in memory to avoid SQLite (the embedded relational database) lock contention (`crates/db/src/models/workspace.rs:182-192`, `crates/local-deployment/src/container.rs:1152-1183`); `updated_at` is the clock used by expiry cleanup (`crates/db/src/models/workspace.rs:252-309`).
- Liveness (`is_running` / `is_errored`) is not stored: `find_all_with_status` and `find_by_id_with_status` compute it with `EXISTS` / latest-status subqueries over `sessions` joined to `execution_processes` filtered to `run_reason IN ('setupscript','cleanupscript','codingagent')` (`crates/db/src/models/workspace.rs:498-583`, `crates/db/src/models/workspace.rs:594-670`).

### 1.2 `workspace_repos` join rows
Each attached repo is a `WorkspaceRepo` row (`crates/db/src/models/workspace_repo.rs:11-21`):

```rust
pub struct WorkspaceRepo {
    pub id: Uuid,
    pub workspace_id: Uuid,
    pub repo_id: Uuid,
    pub target_branch: String,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
```

Bulk insert is transactional in `WorkspaceRepo::create_many` (`crates/db/src/models/workspace_repo.rs:46-85`); the enriched view `RepoWithTargetBranch` joins `repos` with the per-workspace `target_branch` (`crates/db/src/models/workspace_repo.rs:29-34`, `crates/db/src/models/workspace_repo.rs:137-188`). The `target_branch` (where changes will eventually merge, e.g. `main`) is distinct from the workspace `branch` (where changes are made); this distinction is user-documented in `docs/workspaces/creating-workspaces.mdx:77-90`.

### 1.3 `repos`, `sessions`, `execution_processes`
- `Repo` rows (`crates/db/src/models/repo.rs:36-54`) describe source checkouts and per-repo scripts: `path`, `name`, `setup_script`, `cleanup_script`, `archive_script`, `copy_files`, `parallel_setup_script`, `dev_server_script`, `default_target_branch`, `default_working_dir`. Deleting a repo cascades to `workspace_repos` / `project_repos` (`crates/db/src/models/repo.rs:336-342`).
- `Session` rows (`crates/db/src/models/session.rs:22-31`) group execution processes inside a workspace; `agent_working_dir` is resolved at creation to `<repo_name>[/<default_working_dir>]` for single-repo workspaces and `NULL` for multi-repo ones (`crates/db/src/models/session.rs:175-191`). Ordering helpers explicitly exclude dev servers from "most recently used" (`crates/db/src/models/session.rs:58-119`).
- `ExecutionProcess` rows (`crates/db/src/models/execution_process.rs:61-78`) record every script/agent run with `status` in `running|completed|failed|killed` (`crates/db/src/models/execution_process.rs:39-48`) and `run_reason` in `setupscript|cleanupscript|archivescript|codingagent|devserver` (`crates/db/src/models/execution_process.rs:50-59`). The `dropped` flag hides superseded history after restore/trim while keeping rows listed (`crates/db/src/models/execution_process.rs:68-73`). Per-repo git positions per process live in `execution_process_repo_states` (`before_head_commit` / `after_head_commit`), backfilled at boot (see section 7).

| Table | What it records about a workspace | Key fields |
|---|---|---|
| `workspaces` | identity, branch, container path, list state | `id`, `branch`, `container_ref`, `archived`, `pinned`, `name`, `worktree_deleted`, `updated_at` (`crates/db/src/models/workspace.rs:41-54`) |
| `workspace_repos` | which repos, and each repo's merge target | `workspace_id`, `repo_id`, `target_branch` (`crates/db/src/models/workspace_repo.rs:11-21`) |
| `sessions` | conversation/execution groupings | `workspace_id`, `executor`, `agent_working_dir` (`crates/db/src/models/session.rs:22-31`) |
| `execution_processes` | every run: setup, agent, cleanup, archive, dev server | `session_id`, `run_reason`, `status`, `dropped`, `executor_action` (`crates/db/src/models/execution_process.rs:61-78`) |
| `repos` | source paths + scripts (setup/cleanup/archive/dev-server) | `path`, `name`, `dev_server_script`, `setup_script` (`crates/db/src/models/repo.rs:36-54`) |

## 2. Branch-per-workspace mechanics
### 2.1 Naming: `<short-uuid>-<slugged-label>`, optional prefix
Branch names and container directory names derive from the same slug scheme. `git_branch_from_workspace` (`crates/services/src/services/container.rs:786-795`):

```rust
async fn git_branch_from_workspace(&self, workspace_id: &Uuid, task_title: &str) -> String {
    let task_title_id = git_branch_id(task_title);
    let prefix = self.git_branch_prefix().await;
    if prefix.is_empty() {
        format!("{}-{}", short_uuid(workspace_id), task_title_id)
    } else {
        format!("{}/{}-{}", prefix, short_uuid(workspace_id), task_title_id)
    }
}
```

`git_branch_id` lowercases, replaces non-alphanumerics with `-`, trims, and truncates to 16 chars (`crates/utils/src/text.rs:4-18`); `short_uuid` takes the first 4 hex chars of the UUID (`crates/utils/src/text.rs:20-24`). The workspace directory name uses the identical scheme without prefix via `dir_name_from_workspace` (`crates/local-deployment/src/container.rs:852-855`). The branch label comes from the workspace name or falls back to `"workspace"` (`crates/server/src/routes/workspaces/create.rs:23-48`); user docs show examples like `vk/abc123-add-login-page` (`docs/workspaces/creating-workspaces.mdx:21-23`).

### 2.2 `git worktree` vs branch: two separate steps
Vibe Kanban uses real `git worktree` checkouts (a linked working tree sharing the repo's object database), not bare branches. `WorktreeManager::create_worktree` (`crates/worktree-manager/src/worktree_manager.rs:60-84`) does branch creation first, then worktree attach:

```rust
pub async fn create_worktree(
    repo_path: &Path, branch_name: &str, worktree_path: &Path,
    base_branch: &str, create_branch: bool,
) -> Result<(), WorktreeError> {
    if create_branch {
        // spawn_blocking: GitService::create_branch(repo, branch, base)
    }
    Self::ensure_worktree_exists(repo_path, branch_name, worktree_path).await
}
```

`GitService::create_branch` creates the new branch pointing at the tip commit of the base branch (`crates/git/src/lib.rs:193-204`); `GitService::add_worktree` shells to `git worktree add` via `GitCli::worktree_add` (`crates/git/src/lib.rs:960-971`, `crates/git/src/cli.rs:85-108`), which also reapplies sparse-checkout (partial-clone layout) non-fatally (`crates/git/src/cli.rs:103-105`). Branch existence is checked with `check_branch_exists`, which accepts local or remote branches (`crates/git/src/lib.rs:1241-1254`).

### 2.3 Container layout and multi-repo creation
`WorkspaceManager::create_workspace` (`crates/workspace-manager/src/workspace_manager.rs:290-371`) creates one container directory and one worktree per repo at `<container>/<repo.name>`:

```rust
for input in repos {
    let worktree_path = workspace_dir.join(&input.repo.name);
    match WorktreeManager::create_worktree(
        &input.repo.path, branch_name, &worktree_path, &input.target_branch, true,
    ).await { ... }
}
```

Failure rolls back already-created worktrees and removes the container dir if empty, returning `PartialCreation` (`crates/workspace-manager/src/workspace_manager.rs:337-359`); an empty repo list is rejected with `NoRepositories` (`crates/workspace-manager/src/workspace_manager.rs:297-299`). All repos in one workspace share the same `branch_name` (single working branch across repos), while each keeps its own `target_branch` (`crates/workspace-manager/src/workspace_manager.rs:292-296`, `docs/workspaces/creating-workspaces.mdx:61-90`). Default worktree roots are platform-specific temp dirs (`crates/utils/src/path.rs:108-125`, `crates/worktree-manager/src/worktree_manager.rs:520-523`), overridable to `{custom}/.vibe-kanban-workspaces` (`crates/worktree-manager/src/worktree_manager.rs:511-518`); user docs describe the same locations (`docs/workspaces/managing-workspaces.mdx:96-106`).

### 2.4 Legacy single-worktree migration
Old single-repo workspaces stored the worktree directly at the container root (container dir itself had a `.git` file marker). `migrate_legacy_worktree` (`crates/workspace-manager/src/workspace_manager.rs:463-519`) detects that layout and performs two `git worktree move` operations via a temp sibling path to reach `<container>/<repo_name>`, and `ensure_workspace_exists` attempts this migration first for single-repo inputs (`crates/workspace-manager/src/workspace_manager.rs:373-387`).

## 3. WorktreeManager internals
- `ensure_worktree_exists` (`crates/worktree-manager/src/worktree_manager.rs:88-116`) is the idempotent entry point: it takes a per-path async mutex from the global `WORKTREE_CREATION_LOCKS` map (`crates/worktree-manager/src/worktree_manager.rs:16-17`, `crates/worktree-manager/src/worktree_manager.rs:96-105`), checks `is_worktree_properly_set_up` (path exists AND registered in `<commondir>/worktrees/*/gitdir` metadata AND `validate_worktree` passes, `crates/worktree-manager/src/worktree_manager.rs:156-183`), and recreates otherwise.
- Recreation (`recreate_worktree_internal`, `crates/worktree-manager/src/worktree_manager.rs:119-153`) runs comprehensive cleanup, ensures the parent dir, then `create_worktree_with_retry`, which on `git worktree add` failure force-cleans metadata, removes the physical dir, and retries once (`crates/worktree-manager/src/worktree_manager.rs:302-365`).
- Cleanup (`comprehensive_worktree_cleanup`, `crates/worktree-manager/src/worktree_manager.rs:230-265`) is four steps: `git worktree remove --force`, force-remove stale `<commondir>/worktrees/<name>` metadata, `remove_dir_all` the worktree, `git worktree prune`; if the source repo is unopenable it falls back to plain directory deletion (`crates/worktree-manager/src/worktree_manager.rs:267-300`). `cleanup_worktree` serializes against creation with the same per-path lock and infers the repo via `git rev-parse --git-common-dir` when no repo path is given (`crates/worktree-manager/src/worktree_manager.rs:404-470`); `batch_cleanup_worktrees` logs-and-continues per worktree (`crates/worktree-manager/src/worktree_manager.rs:390-400`).
- `move_worktree` delegates to `git worktree move` (`crates/worktree-manager/src/worktree_manager.rs:490-508`, `crates/git/src/lib.rs:987-997`, `crates/git/src/cli.rs:128-149`); `cleanup_suspected_worktree` only treats dirs whose `.git` is a file (worktree marker, not a full repo) as worktrees (`crates/worktree-manager/src/worktree_manager.rs:525-535`).

## 4. Terminal session handling
Terminal access is a WebSocket endpoint, not a persisted resource. `terminal_ws` (`crates/server/src/routes/terminal.rs:52-93`) requires `workspace_id` plus optional `cols`/`rows`, loads the workspace, rejects workspaces with no `container_ref` or a missing directory, and resolves the initial working directory to `<container>/<repo.name>` for single-repo workspaces (otherwise the container root):

```rust
let container_ref = attempt.container_ref.ok_or_else(||
    ApiError::BadRequest("Attempt has no workspace directory".to_string()))?;
let base_dir = PathBuf::from(&container_ref);
if !base_dir.exists() {
    return Err(ApiError::BadRequest("Workspace directory does not exist".to_string()));
}
```

Each connection mints a fresh PTY via `PtyService::create_session` (`crates/local-deployment/src/pty.rs:48-55`, `crates/server/src/routes/terminal.rs:102-113`), which spawns the interactive shell (`get_interactive_shell`), sets `TERM=xterm-256color`, applies shell-specific prompt normalization, and pumps output through a reader thread into an unbounded channel (`crates/local-deployment/src/pty.rs:58-138`). The handler loop bridges base64-encoded JSON `input`/`resize` commands and `output` messages (`crates/server/src/routes/terminal.rs:118-166`) and unconditionally calls `close_session` when the socket ends (`crates/server/src/routes/terminal.rs:165`). Sessions live only in the in-memory `HashMap<Uuid, PtySession>` (`crates/local-deployment/src/pty.rs:36-39`); there is no reattach protocol, no session record in the database, and a server restart drops every terminal session. `write`/`resize`/`close_session` only operate on live map entries (`crates/local-deployment/src/pty.rs:157-219`).

## 5. Dev server allocation
There is no port allocator and no port bookkeeping in the database. Dev-server behavior is entirely script-driven per repo:
- `POST /workspaces/{id}/execution/dev-server/start` (`crates/server/src/routes/workspaces/execution.rs:37-137`) first kills all currently running dev servers for the workspace (`crates/server/src/routes/workspaces/execution.rs:59-73`), then collects repos with a non-empty `dev_server_script` (`crates/server/src/routes/workspaces/execution.rs:75-85`), returning an error payload if none is configured.
- It reuses the latest session or creates one with `executor: "dev-server"` (`crates/server/src/routes/workspaces/execution.rs:87-101`), then spawns one `ExecutionProcess` per repo with `run_reason = DevServer` and a `ScriptRequest` of `context: DevServer`, `working_dir: <repo.name>` (`crates/server/src/routes/workspaces/execution.rs:103-125`).
- Scripts bind whatever ports they choose; preview/proxy routing is a separate subsystem where the main server and preview proxy bind OS-assigned ports at startup (`crates/server/src/startup.rs:105-128`) and the proxy routes `{port}.localhost` subdomains to the target port (`crates/preview-proxy/src/lib.rs:6-7`). Dev-server processes are excluded from "running workspace" and "most recently used" computations (`crates/db/src/models/execution_process.rs:292-309`, `crates/db/src/models/session.rs:58-119`, `crates/db/src/models/workspace.rs:518-536`), but they block workspace deletion only in the sense that deletion stops them first, while any running non-dev-server process hard-blocks deletion with HTTP 409 (`crates/server/src/routes/workspaces/core.rs:99-139`).
- Archiving a workspace stops its dev servers and optionally runs the archive script (`crates/services/src/services/container.rs:527-561`); deleting a workspace stops dev servers before removing the DB row (`crates/server/src/routes/workspaces/core.rs:117-139`).

## 6. Workspace lifecycle and API surface
Routes are assembled in `crates/server/src/routes/workspaces/mod.rs:24-61`: `GET /workspaces`, `POST /workspaces`, `POST /workspaces/start`, `POST /workspaces/from-pr`, per-id `GET/PUT/DELETE`, plus nested `/git`, `/execution`, `/integration`, `/repos`, `/pull-requests`, `/{id}/attachments`, `/{id}/links` routers.

| Transition | Entry point | Mechanics |
|---|---|---|
| Create record | `POST /workspaces` → `create_workspace` (`crates/server/src/routes/workspaces/create.rs:50-66`) | `create_workspace_record` inserts a row with generated branch name; no worktrees yet (`crates/server/src/routes/workspaces/create.rs:23-48`) |
| Create + start | `POST /workspaces/start` → `create_and_start_workspace` (`crates/server/src/routes/workspaces/create.rs:212-320`) | Validates non-empty prompt and repos, attaches each repo (branch-exists check, `crates/workspace-manager/src/workspace_manager.rs:128-158`), associates attachments, then `container().start_workspace` |
| Materialize container | `create` (`crates/local-deployment/src/container.rs:1201-1235`) / `ensure_container_exists` (`crates/local-deployment/src/container.rs:1243-1287`) | `create` always builds fresh via `WorkspaceManager::create_workspace` and writes `container_ref`; `ensure` reuses stored `container_ref` or derives `<base>/<shortuuid>-<slug>`, calls `ensure_workspace_exists`, backfills `container_ref`, clears `worktree_deleted`, copies project files, writes config files |
| Run / stop execution | `POST .../execution/*` (`crates/server/src/routes/workspaces/execution.rs:29-35`) | `start_execution`, `try_stop`, `stop_workspace_execution`; cleanup/archive script routes call `ensure_container_exists` first (`crates/server/src/routes/workspaces/execution.rs:157-288`) |
| Archive | `PUT /workspaces/{id}` with `archived=true` → `update_workspace` (`crates/server/src/routes/workspaces/core.rs:43-88`) | Sets the flag, then `archive_workspace`: stops dev servers, runs archive script (`crates/services/src/services/container.rs:527-561`). Archive preserves worktree and history (`docs/workspaces/managing-workspaces.mdx:39-49`) |
| Delete | `DELETE /workspaces/{id}?delete_branches=&delete_remote=` → `delete_workspace` (`crates/server/src/routes/workspaces/core.rs:99-183`) | 409 if any non-dev-server process is running; stops dev servers; deletes the DB row; spawns background `spawn_workspace_deletion_cleanup` which removes session log dirs, `batch_cleanup_worktrees` + container dir, and optionally `git branch -D`-equivalent per source repo (`crates/workspace-manager/src/workspace_manager.rs:217-279`, `crates/git/src/lib.rs:1006-1015`). Default preserves branches; user docs confirm branch and commits survive while worktree and history rows are removed (`docs/workspaces/managing-workspaces.mdx:59-81`) |

## 7. Restart and recovery: what survives, what is lost
### 7.1 Boot sequence
`initialize_deployment` (`crates/server/src/startup.rs:132-183`) runs, in order: asset-dir setup, DB copy/migrations, `cleanup_orphan_executions`, `backfill_before_head_commits`, `backfill_repo_names`, analytics, then async executor-options preload. Shutdown runs `perform_cleanup_actions` → `kill_all_running_processes` (`crates/server/src/startup.rs:185-192`, `crates/local-deployment/src/container.rs:1603-1633`).

`cleanup_orphan_executions` (`crates/services/src/services/container.rs:272-326`):

```rust
let running_processes = ExecutionProcess::find_running(&self.db().pool).await?;
for process in running_processes {
    // ... update_completion(pool, process.id, Failed, None)
    // ... capture current HEAD per repo into after_head_commit
}
```

Every row with `status='running'` is flipped to `failed` with no exit code, and the current worktree HEAD per repo is snapshotted into `after_head_commit` so the interrupted run still has a position marker. Nothing is relaunched: no agent, setup, cleanup, or dev-server process is restarted automatically.

### 7.2 Lazy worktree healing
No boot step rebuilds worktrees. Healing happens on next access through `ensure_container_exists` (`crates/local-deployment/src/container.rs:1243-1287`), which calls `WorkspaceManager::ensure_workspace_exists` (`crates/workspace-manager/src/workspace_manager.rs:373-425`): if the branch still exists in the source repo the worktree is re-added at `<container>/<repo_name>`; if the branch is gone it is recreated from `target_branch`. Manually deleted worktrees are therefore recreated from the branch tip on next open, with uncommitted changes unrecoverable — matching user docs (`docs/workspaces/managing-workspaces.mdx:140-146`).

### 7.3 Orphan and expiry sweeping
- `cleanup_orphan_workspaces` (`crates/workspace-manager/src/workspace_manager.rs:538-555`) scans the default and any custom base dir (skipped entirely under `DISABLE_WORKTREE_CLEANUP`) and removes container dirs with no matching `container_ref` in the DB (`crates/workspace-manager/src/workspace_manager.rs:557-610`), cleaning suspected worktrees inside before `remove_dir_all` (`crates/workspace-manager/src/workspace_manager.rs:612-652`). A periodic task runs orphan cleanup once at spawn plus `cleanup_expired_workspaces` every 30 minutes (`crates/local-deployment/src/container.rs:299-320`).
- `cleanup_expired_workspaces` deletes worktree content (marks `worktree_deleted`) for workspaces untouched for 72h (1h if archived, and never pinned/active/running) per `find_expired_for_cleanup` (`crates/db/src/models/workspace.rs:252-309`, `crates/local-deployment/src/container.rs:284-297`).

### 7.4 Survival matrix
| Artifact | Survives restart? | Mechanism |
|---|---|---|
| `workspaces`, `workspace_repos`, `sessions`, `execution_processes`, logs, turns | Yes | SQLite rows; only `status='running'` flips to `failed` (`crates/services/src/services/container.rs:272-326`) |
| Git branches + committed files | Yes | Branches live in source repos; worktree dirs persist on disk unless swept |
| Missing worktree directories | Recreated lazily | `ensure_workspace_exists` on next access (`crates/workspace-manager/src/workspace_manager.rs:373-425`, `crates/local-deployment/src/container.rs:1243-1287`) |
| Running agent/setup/cleanup processes | No (marked `failed`, never resumed) | Boot backfill + shutdown kill (`crates/services/src/services/container.rs:272-326`, `crates/local-deployment/src/container.rs:1603-1633`) |
| Running dev servers | No (must be started again via `POST .../dev-server/start`) | Same as above; no auto-start path exists (`crates/server/src/routes/workspaces/execution.rs:37-137`) |
| Terminal PTY sessions | No (new shell per connection) | In-memory map only (`crates/local-deployment/src/pty.rs:36-39`, `crates/server/src/routes/terminal.rs:165`) |
| In-memory log streams (`MsgStore`) | No (rebuilt from persisted logs on demand) | `stream_raw_logs` / `stream_normalized_logs` fall back to DB-loaded messages (`crates/services/src/services/container.rs:797-872`) |
| Orphaned container dirs | No (deleted) | Startup/periodic orphan sweep (`crates/workspace-manager/src/workspace_manager.rs:538-610`, `docs/workspaces/managing-workspaces.mdx:148-152`) |

**Covers:** workspace row and join-table schema; single-branch multi-worktree layout and naming; `WorktreeManager` create/ensure/cleanup/move internals; ephemeral terminal sessions; script-based dev servers without port allocation; create/start/archive/delete lifecycle; boot/shutdown recovery and survival matrix.
