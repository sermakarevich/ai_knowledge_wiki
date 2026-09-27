---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[summary|Summary]] | [[digest|Digest]] | [[wiki/01-overview-architecture|Wiki]]

# Retrieval Practice: Vibe Kanban

Answer from memory first, then expand each tip to check. Focus on mechanisms, not trivia.

### Q1 — Which two ports does the server bind at startup, and how are they chosen?

> [!tip]- Answer
> The server binds one port for the main app and one for the preview proxy, read from `BACKEND_PORT`/`PORT` and `PREVIEW_PROXY_PORT` with default `0` for OS (Operating System) auto-assignment. Actual ports are published via a temp-dir port file and client info for the UI (User Interface) and MCP (Model Context Protocol, a standard for exposing tools to agents) to discover. Removing the second listener would collapse untrusted preview content onto the app origin. See [[wiki/01-overview-architecture|Architecture Overview]]

### Q2 — What is the executor adapter contract, and how does a run reach the right agent CLI (Command-Line Interface)?

> [!tip]- Answer
> All agents implement `StandardCodingAgentExecutor` (`spawn`, `spawn_follow_up`, `normalize_logs`, MCP config methods), dispatched over the `CodingAgent` enum with nine production adapters plus a `qa-mode`-gated mock. Consumers never build adapters directly; `CodingAgentInitialRequest::spawn` resolves the cached executor profile, applies overrides, attaches approvals, then calls `agent.spawn()`. Adding a harness means a new enum variant plus adapter module, not a plugin registry. See [[wiki/02-executor-adapter-layer|Executor Adapter Layer]]

### Q3 — What is a workspace on disk, and what survives a server restart?

> [!tip]- Answer
> A workspace is one database row plus one container directory holding one git worktree per repo at `<container>/<repo_name>`, all sharing a single auto-generated `<short-uuid>-<slugged-label>` branch. Restart preserves rows, branches, committed files, and worktree dirs, but flips every `status='running'` execution to `failed`, drops PTY (Pseudo-Terminal, an interactive shell session) and dev-server processes, and heals missing worktrees lazily on next access. Never auto-resuming agents is what makes crash recovery safe. See [[wiki/03-workspaces-and-worktrees|Workspaces and Worktrees]]

### Q4 — Why is there no `Workflow` type, and what exactly moves a card automatically?

> [!tip]- Answer
> Board position is data, not code: an issue's column is its `status_id` foreign key into per-project `project_statuses` rows, and drag-drop writes `status_id` plus `sort_order` via bulk update. Only three server-side syncs automate moves: first workspace to In progress, open PR (Pull Request, a proposed change sent for review) to In review, and all-linked-PRs-merged or local merge to Done. Everything else, including sub-issue roll-up, is manual by design. See [[wiki/04-kanban-issues-and-workflow|Kanban Issues and Workflow]]

### Q5 — How are diffs computed, and what happens to inline review comments?

> [!tip]- Answer
> Diffs are worktree-vs-base-commit, not branch-vs-branch: resolve the base commit, stage worktree state into a temp index, run `git diff --cached -M --name-status`, then hydrate bodies with a ~2 MB per-file omit guard and a 200 MB stream cap. Inline `ReviewComment` drafts live only in React frontend state and clear on send or workspace switch, then `generateReviewMarkdown` prepends them as a `## Review Comments` block to the next agent prompt. Losing unsent comments on switch is therefore expected behavior. See [[wiki/05-diff-review-and-pr-flow|Diff Review and PR Flow]]

### Q6 — Why does the backend never allocate the dev-server port, and what breaks if log scraping is removed?

> [!tip]- Answer
> Only the main and proxy ports are auto-assigned; the dev port is whatever user framework binds, found by regex-scanning streamed logs for loopback URLs and normalizing `0.0.0.0` to `localhost`. This avoids building a port allocator, but requires the dev command to print its URL and leaves conflicts to manual `lsof` fixes. Replacing scraping with a registry would fail whenever the framework picks its own port outside the registry. See [[wiki/06-preview-browser-and-dev-server|Preview Browser and Dev Server]]

### Q7 — Where does durable state live, and how do config and MCP (Model Context Protocol) modes differ?

> [!tip]- Answer
> All local state lives in one SQLite (a lightweight file database) file `db.v2.sqlite` with `JournalMode::Delete` and 76 migrations, modeled in 16 domains and mutated through ~20 services behind the `Deployment` trait. Runtime config (`config.json`, `profiles.json`, `credentials.json`) loads with silent-default fallback, so a missing file never fails boot. The stdio MCP server exposes ~30 tools in global mode versus 7 pinned orchestrator tools. See [[wiki/07-persistence-config-and-ops|Persistence, Config, and Ops]]

### Q8 — Why does renaming the "Done" column silently break merge-to-Done?

> [!tip]- Answer
> The three issue syncs match status names case-insensitively (`"Done"`, `"In review"`) instead of stable IDs, and `completed_at` is never set by any sync. Renaming "Done" leaves the `WorkMerged` signal with no target, so merged PRs stop moving cards while the board still looks healthy. The fix is name restoration or ID-based syncing, not re-running merges. See [[wiki/04-kanban-issues-and-workflow|Kanban Issues and Workflow]]

### Q9 — Fleet runs parallel coder workers that can crash mid-task: which Vibe Kanban restart shape should you copy?

> [!tip]- Answer
> Copy crash-and-mark plus lazy heal: persist worker rows, flip running executions to `failed` with a HEAD position snapshot on boot, kill stray children on shutdown, and recreate missing worktrees idempotently on next access. Do not auto-resume agent processes, dev servers, or terminals, since replaying a half-finished agent turn risks divergence. This trades automatic resume for deterministic, reviewable recovery. See [[wiki/03-workspaces-and-worktrees|Workspaces and Worktrees]]

### Q10 — Evaluate: is board-first thin automation plus 60-second PR polling sufficient for a fleet-scale orchestrator?

> [!tip]- Answer
> It is sufficient for human-supervised parallelism because manual drag covers edge cases, unanimous-merge gating prevents premature Done, and polling avoids webhook (an event callback sent by the forge) operations without losing correctness. It fails when status renames, stale open PRs, or `Delete`-mode writer contention silently stall throughput at scale. See [[critical_thinking|Critical Analysis]] and [[wiki/04-kanban-issues-and-workflow|Kanban Issues and Workflow]]
