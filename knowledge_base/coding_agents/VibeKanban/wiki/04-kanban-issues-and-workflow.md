> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Kanban Issues and Workflow: Plan on the Board, Execute in Workspaces
**In one sentence:** There is no first-class `Workflow` type in Vibe Kanban — the "workflow" is an emergent convention where issues carry a per-project `status_id`, workspaces carry a nullable `issue_id`, and three narrow server-side syncs plus manual drag-drop move cards along the board.

## Key points
- **No `Workflow` struct, enum, or trait exists** — the only workflow-named type is a private two-variant `IssueWorkflowSignal` (`ReviewStarted`, `WorkMerged`) in `crates/remote/src/db/issues.rs:33-36`; all other `workflow` hits in `crates/` are comments or unrelated tool-scoping.
- **Issue lifecycle is data, not code:** each project owns its own `project_statuses` rows seeded with six defaults (Backlog, To do, In progress, In review, Done, Cancelled), and an issue's column is just its `status_id` foreign key (`crates/remote/migrations/20260112000000_remote-projects.sql:62`).
- **Board moves are `status_id` + `sort_order` writes:** cross-column drag sends `status_id: <dest-column>` and recomputed `sort_order` values through `POST /v1/issues/bulk` (`packages/web-core/src/shared/lib/remoteApi.ts:125-138`), executed server-side as one transaction in `crates/remote/src/routes/issues.rs:44-49`.
- **Issue-to-workspace linkage is a nullable foreign key:** `workspaces.issue_id REFERENCES issues(id) ON DELETE SET NULL` (`crates/remote/migrations/20260112000000_remote-projects.sql:246`) plus a `local_workspace_id` bridge to the local execution side, so one issue fans out to many workspaces and unlinking never deletes work.
- **Automation covers exactly three transitions** — first-workspace-created moves Backlog/To-do to In progress (`crates/remote/src/db/issues.rs:641-691`), open PR moves to In review, and all-linked-PRs-merged (or local merge without PR) moves to Done (`crates/remote/src/db/issues.rs:523-574`); everything else, including Done-via-direct-merge surfacing, is manual or funneled through those signals.
- **Sub-issues and blocking links carry no cascade semantics:** children have independent statuses, completing all children does not complete the parent (`docs/issue-management.mdx:101-104`), and the only parent promotion is Backlog/To-do to In progress when the child's first workspace is created (`crates/remote/src/db/issues.rs:670-681`).
- **The issue description doubles as the agent prompt:** the workspace-create flow pre-fills its prompt from issue title plus description via `buildWorkspaceCreatePrompt`/`buildLinkedIssueCreateState` (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:131-156`), which is why docs call the issue "the prompt your coding agent receives" (`docs/issue-management.mdx:6`).

---
## 1. Verdict: emergent workflow, not a Workflow abstraction
A repo-wide search for a first-class abstraction returns nothing:

- `grep struct Workflow / enum Workflow / trait Workflow` over `crates/` — zero hits.
- `grep workflow` over `crates/` returns only six hits: two prose comments (`crates/desktop-bridge/src/service.rs:3`, `crates/git/src/lib.rs:57`), one MCP tool-filter test (`crates/mcp/src/task_server/tools/mod.rs:415`), one CLI comment (`crates/git/src/cli.rs:9`), and the two real signals in `crates/remote/src/db/issues.rs:520-597`.

The entire server-side "workflow engine" is this private enum (`crates/remote/src/db/issues.rs:32-36`):

```rust
enum IssueWorkflowSignal {
    ReviewStarted,
    WorkMerged,
}
```

It is never exposed over the API (API Surface: Application Programming Interface — the HTTP contract the frontend calls), never stored, and never extended with states like "workspace created" — that third automation bypasses the enum and calls `move_to_status_if_pending` directly. The user-visible workflow is therefore the composition of (a) per-project status rows, (b) the nullable `workspaces.issue_id` link, (c) pull-request (PR — a proposed code change sent for review) rows that join issues to workspaces, and (d) the three sync functions below.

## 2. Issue lifecycle states: per-project rows, not an enum
Modern issues do **not** use the legacy `TaskStatus` enum still present in the local SQLite (Structured Query Language Lite — the embedded local database) layer (`crates/db/src/models/task.rs:14-21`):

```rust
pub enum TaskStatus {
    Todo,
    InProgress,
    InReview,
    Done,
    Cancelled,
}
```

That enum is a leftover from the pre-remote single-node model. Remote issues (the current system of record, stored in Postgres — the server database) point at a row:

```rust
pub struct Issue {
    pub id: Uuid,
    pub project_id: Uuid,
    pub issue_number: i32,
    pub simple_id: String,
    pub status_id: Uuid,   // <-- the "column" is a FK, not an enum
    ...
}
```

(`crates/api-types/src/issue.rs:21-40`; `status_id` field at `crates/api-types/src/issue.rs:26`.) The status rows themselves are defined in `crates/api-types/src/project_status.rs:9-17` (`id`, `project_id`, `name`, `color`, `sort_order`, `hidden`) and created per project from `crates/remote/src/db/project_statuses.rs:13-20`:

```rust
pub const DEFAULT_STATUSES: &[(&str, &str, i32, bool)] = &[
    ("Backlog", "220 9% 46%", 0, true),
    ("To do", "217 91% 60%", 1, false),
    ("In progress", "38 92% 50%", 2, false),
    ("In review", "258 90% 66%", 3, false),
    ("Done", "142 71% 45%", 4, false),
    ("Cancelled", "0 84% 60%", 5, true),
];
```

Schema source (`crates/remote/migrations/20260112000000_remote-projects.sql:30-38`):

```sql
CREATE TABLE project_statuses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    hidden BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Status lookup is name-based and case-insensitive (`crates/remote/src/db/project_statuses.rs:62-90`, `WHERE project_id = $1 AND LOWER(name) = LOWER($2)`), which is why the sync code matches on `"In progress"`, `"In review"`, `"Done"`, `"Backlog"`, `"To do"` string literals rather than IDs. Users can rename, recolor, reorder, hide, and add statuses; the board renders whatever rows exist. Default user-facing semantics are documented in `docs/issue-management.mdx:74-81`:

| Column | What it means |
|--------|---------------|
| To do | Work that hasn't started yet |
| In progress | An agent or person is actively working on this |
| In review | Work is done and waiting for your review |
| Done | Completed and verified |

Backlog and Cancelled are `hidden = true` by default and only appear under the **All** tab (`docs/issue-management.mdx:81`; board filtering at `packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:415-433`).

Full issue-row DDL (Database Definition Language — the `CREATE TABLE` statement), `crates/remote/migrations/20260112000000_remote-projects.sql:53-89`:

```sql
CREATE TABLE issues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    issue_number INTEGER NOT NULL,
    simple_id VARCHAR(20) NOT NULL,
    status_id UUID NOT NULL REFERENCES project_statuses(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority issue_priority,
    start_date TIMESTAMPTZ,
    target_date TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    sort_order DOUBLE PRECISION NOT NULL DEFAULT 0,
    parent_issue_id UUID REFERENCES issues(id) ON DELETE SET NULL,
    parent_issue_sort_order DOUBLE PRECISION,
    extension_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT issues_project_issue_number_uniq UNIQUE (project_id, issue_number)
);
```

Notable: `completed_at` exists but nothing in the workflow syncs sets it — Done-ness is read from the status name, not the timestamp. Human-readable IDs (`BLO-5` style) come from a trigger that bumps `projects.issue_counter` and prefixes with the org's `issue_prefix` (`crates/remote/migrations/20260112000000_remote-projects.sql:91-121`). Priority is a real enum (`urgent/high/medium/low`, `crates/api-types/src/issue.rs:10-18`); relationships are a separate `issue_relationships` table with a `blocking/related/has_duplicate` enum (`crates/remote/migrations/20260112000000_remote-projects.sql:142-152`).

## 3. Issue API types and routes (CRUD plus bulk)
Shared types live in `crates/api-types/src/issue.rs`: `CreateIssueRequest` (`crates/api-types/src/issue.rs:60-77`) takes `project_id`, `status_id`, `title`, `sort_order` plus optional description/priority/dates/parent; `UpdateIssueRequest` (`crates/api-types/src/issue.rs:80-147`) makes every field optional via the `some_if_present` deserializer so drag-drop can send just `{status_id, sort_order}`; `SearchIssuesRequest` (`crates/api-types/src/issue.rs:155-196`) supports filtering by `status_id(s)`, `priority`, `parent_issue_id`, `assignee_user_id`, `tag_id(s)`, text search, and pagination.

Routes are built with a generic `MutationBuilder` providing list/get/create/update/delete plus two extras (`crates/remote/src/routes/issues.rs:34-49`):

```rust
pub fn router() -> axum::Router<AppState> {
    mutation()
        .router()
        .route("/issues/search", post(search_issues))
        .route("/issues/bulk", post(bulk_update_issues))
}
```

The bulk endpoint is what makes drag-drop atomic: it verifies all touched issues belong to one project, applies each `UpdateIssueRequest` inside a single transaction, then fans out status/title/description/priority notifications (`crates/remote/src/routes/issues.rs:430-584`, handler `bulk_update_issues`). The frontend caller is `bulkUpdateIssues` posting `{updates: [{id, ...changes}]}` to `/v1/issues/bulk` (`packages/web-core/src/shared/lib/remoteApi.ts:125-138`). Single-issue moves go through `update_issue` (`crates/remote/src/routes/issues.rs:340-400`), which also triggers `notify_issue_update_changes` on status/title/description/priority deltas (`crates/remote/src/routes/issues.rs:51-100`).

## 4. Issue-to-workspace linkage mechanics
Linkage is one nullable column (`crates/remote/migrations/20260112000000_remote-projects.sql:242-260`):

```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    owner_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    issue_id UUID REFERENCES issues(id) ON DELETE SET NULL,
    local_workspace_id UUID UNIQUE,
    ...
);
CREATE INDEX idx_workspaces_issue_id ON workspaces(issue_id) WHERE issue_id IS NOT NULL;
```

Semantics: a workspace optionally belongs to exactly one issue; an issue has many workspaces (counted by `WorkspaceRepository::count_by_issue_id`, `crates/remote/src/db/workspaces.rs:230-233`); deleting an issue SETs NULL rather than cascading, so work survives planning churn; `local_workspace_id` is the bridge to the local execution record that actually holds the git worktree (an isolated directory checkout of a code branch), agent session, and diff. Pull requests complete the triangle (`crates/remote/migrations/20260112000000_remote-projects.sql:266-280`): each PR row carries non-null `issue_id` plus nullable `workspace_id`, so PR state can drive issue state even when several workspaces feed one issue.

Creation with a link is `POST /v1/workspaces` with `{project_id, local_workspace_id, issue_id, ...}` (`crates/remote/src/routes/workspaces.rs:40-60`, request struct `CreateWorkspaceRequest` at `crates/remote/src/routes/workspaces.rs:29-39`). After insert, the handler fires the workspace-created sync and analytics (`crates/remote/src/routes/workspaces.rs:70-130`). Unlink is `DELETE /v1/workspaces/{workspace_id}` (unlink handler) versus deleting the local execution record — the issue-panel container does them in that order with separate confirmations (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:209-287`). URL routing mirrors the nesting: `/projects/:projectId/issues/:issueId/workspaces/:workspaceId` and `.../workspaces/create/:draftId` (route files `packages/local-web/src/routes/_app.projects.$projectId_.issues.$issueId_.workspaces.$workspaceId.tsx` and `..._.workspaces.create.$draftId.tsx`; pattern documented in `packages/web-core/src/pages/kanban/ProjectKanban.tsx:44-57`).

The create-from-issue UX pre-fills the agent prompt from the issue: `handleAddWorkspace` builds the prompt from `issue.title` + `issue.description` and attaches `buildLinkedIssueCreateState(issue, projectId)` before opening the workspace-create draft (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:131-180`); the draft serializes the link as `{issue_id, simple_id, title, remote_project_id}` (`packages/web-core/src/shared/lib/workspaceCreateState.ts:39-93`). Linking an existing workspace goes through `WorkspaceSelectionDialog.show({projectId, issueId})` (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:183-192`).

## 5. Board UI implementation
Entry points split by deployment: `LocalProjectKanban` for the local app (`packages/local-web/src/routes/_app.projects.$projectId.tsx:2-7`) and `ProjectKanban` for remote (`packages/web-core/src/pages/kanban/ProjectKanban.tsx:57`), both rendering `KanbanContainer` (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:125`). The board primitive is `KanbanProvider`, a thin wrapper over `@hello-pangea/dnd`'s `DragDropContext` (`packages/ui/src/components/KanbanBoard.tsx:258-270`, re-exporting `DropResult` at `packages/ui/src/components/KanbanBoard.tsx:31`).

Column model (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:409-433`): statuses are sorted by `sort_order`; `visibleStatuses` (non-hidden) become `KanbanBoard` columns keyed by `status.id` with `KanbanCards id={status.id}` (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:984-1009`); `hiddenStatuses` feed the list-view tabs. Card grouping is derived state: `filteredIssues` (via `useKanbanFilters`) are bucketed per `status.id` into `items: Record<statusId, issueId[]>` (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:484-531`).

Ordering uses an explicit positional formula (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:647-655`):

```ts
// Formula: 1000 * [COLUMN_INDEX] + [ISSUE_INDEX] (both 1-based)
const columnIndex = statusColumnIndexMap.get(statusId) ?? 1;
return 1000 * columnIndex + (issueIndex + 1);
```

`handleDragEnd` (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:658-750`) implements the whole move policy: ignore drops outside a column or no-ops; block within-column reorder unless `sortField === 'sort_order'` (manual mode — matching the docs tip in `docs/issue-management.mdx:87-89`); always allow cross-column moves; optimistically splice local `items`; then build bulk updates — every card in the destination column gets `{status_id: destId, sort_order}` and every card in the source column gets a recomputed `sort_order` — and POST them, guarded by an `isSyncingRef` flag that suppresses Electric-sync (Electric — the live database-to-frontend replication layer) rebuild flicker for 500 ms (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:737-747`). Cards also surface linked workspaces inline (`workspacesByIssueId`, `packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:590-645`) with per-workspace PR badges, and the issue panel's **Workspaces** section (`IssueWorkspacesSectionContainer`) offers `+` (create-and-link) and link-icon (link-existing) actions (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:290-302`).

## 6. Automation vs manual moves
Three automations exist, all server-side, all name-matched, all idempotent (re-applying is a no-op when already in the target status):

| Trigger | Code path | Effect | Guard |
|---------|-----------|--------|-------|
| First workspace linked to issue | `create_workspace` route → `IssueRepository::sync_issue_from_workspace_created` (`crates/remote/src/routes/workspaces.rs:100-115`; impl `crates/remote/src/db/issues.rs:641-691`) | Backlog/To-do issue (and its parent, if sub-issue) → In progress; workspace creator added as assignee if issue has none | Only when `count_by_issue_id == 1`; only from `backlog`/`to do` via `move_to_status_if_pending` (`crates/remote/src/db/issues.rs:601-635`) |
| PR opened / linked | `pull_requests.rs` create/update/upsert + `pull_request_issues.rs` link (`crates/remote/src/routes/pull_requests.rs:152`, `crates/remote/src/routes/pull_requests.rs:237`, `crates/remote/src/routes/pull_requests.rs:351`, `crates/remote/src/routes/pull_request_issues.rs:169`) → `sync_status_from_pull_request` (`crates/remote/src/db/issues.rs:579-590`) | issue → In review | Maps `open → ReviewStarted`; no-op if already there |
| All linked PRs merged, or local merge without PR | same PR call sites with `merged/closed → WorkMerged`; local-merge route `POST /v1/workspaces/{id}/sync_issue_status_from_local_merge` (`crates/remote/src/routes/workspaces.rs:46-48`, handler `crates/remote/src/routes/workspaces.rs:158-190`) → `sync_status_from_local_workspace_merge` (`crates/remote/src/db/issues.rs:593-599`), called from local side via `RemoteClient::sync_issue_status_from_local_workspace_merge` (`crates/services/src/services/remote_client.rs:725-736`) and `remote_sync.rs:88` | issue → Done | `WorkMerged` branch lists PRs and returns early unless **all** are `merged` (`crates/remote/src/db/issues.rs:534-542`); core logic in `sync_status_from_workflow_signal` (`crates/remote/src/db/issues.rs:523-574`) |

Everything else is manual: initial status choice (defaults to first visible column, `packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:435-443`), drag-drop between arbitrary columns, Backlog/Cancelled triage, priority/assignee/tag edits, and sub-issue completion (no roll-up). The user docs describe the two most visible automations as product behavior — "Merge … Your task will automatically move to the Done column" (`docs/core-features/completing-a-task.mdx:36`) and "When your PR is merged on GitHub, your task automatically moves to Done" (`docs/core-features/completing-a-task.mdx:62`) — while the board page stresses manual drag (`docs/issue-management.mdx:68`).

## 7. Sub-issues, relationships, and scope limits
Sub-issues are `parent_issue_id` self-references with their own `status_id` and `sort_order`; the docs state the two load-bearing rules explicitly — independent status, no auto-complete of the parent (`docs/issue-management.mdx:101-104`). The blocked-filter treats an issue as unblocked when its blocker sits in the last visible column or any hidden status (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:271-286`). Known limits worth stating plainly: status-name matching means renaming "Done" silently disables the merge-to-Done automation until names are restored; `completed_at` is never set by any sync so timestamp-based queries disagree with board position; multi-workspace issues resolve Done only on unanimous PR merge, so one stale open PR pins the card in In review; and the legacy local `TaskStatus` enum (`crates/db/src/models/task.rs:14-21`) no longer governs anything remote — it is schema debt, not a second lifecycle.

**Covers:** `crates/remote/migrations/20260112000000_remote-projects.sql:30-89, 242-284` · `crates/remote/src/db/project_statuses.rs:13-20, 62-90` · `crates/remote/src/db/issues.rs:30-36, 523-599, 601-691` · `crates/remote/src/db/workspaces.rs:230-233` · `crates/api-types/src/issue.rs:10-40, 60-147` · `crates/api-types/src/project_status.rs:9-17` · `crates/db/src/models/task.rs:14-21` · `crates/remote/src/routes/issues.rs:34-49` · `crates/remote/src/routes/workspaces.rs:29-60, 158-190` · `crates/remote/src/routes/pull_requests.rs:152, 237, 351` · `crates/remote/src/routes/pull_request_issues.rs:169` · `crates/services/src/services/remote_client.rs:725-736` · `packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:409-433, 647-750, 984-1009` · `packages/ui/src/components/KanbanBoard.tsx:258-270` · `packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:131-192, 209-287` · `packages/web-core/src/shared/lib/remoteApi.ts:125-138` · `packages/web-core/src/shared/lib/workspaceCreateState.ts:39-93` · `docs/issue-management.mdx:6-116` · `docs/core-features/completing-a-task.mdx:36, 62`
