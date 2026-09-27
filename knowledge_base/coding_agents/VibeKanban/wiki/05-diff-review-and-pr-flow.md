> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Diff Review and PR Flow: Review in the UI, Feedback to the Agent
**In one sentence:** Vibe Kanban computes workspace diffs locally with git (a version-control tool that tracks file changes) against a merge-base-derived commit, renders them with the `@pierre/diffs` viewer, collects inline comments as ephemeral (temporary, kept only in browser memory) frontend state that is serialized to markdown and prepended to the next agent prompt, and handles pull-request (PR — a proposed code change sent to a hosting site for review) creation and merge-status tracking through `gh`/`az` command-line wrappers plus a 60-second PR monitor.

## Key points
- **Diffs are computed as worktree-vs-base-commit, not branch-vs-branch:** `GitService::get_diffs` (`crates/git/src/lib.rs:327-353`) takes a resolved base `Commit` and calls `GitCli::diff_status` (`crates/git/src/cli.rs:168-228`), which stages worktree state into a temporary index and runs `git diff --cached -M --name-status <base>`.
- **Files over ~2 MB have their contents omitted from the UI stream:** `MAX_INLINE_DIFF_BYTES` (`crates/git/src/lib.rs:61-63`) drops body text while keeping the file entry, and the stream layer caps cumulative payload at 200 MB (`crates/services/src/services/diff_stream.rs:95`).
- **Inline review comments never touch the database:** the `ReviewComment` type (`packages/web-core/src/shared/hooks/useReview.ts:5-12`) lives in a React context (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:16-25`) and is cleared on send or workspace switch (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:44-46`, `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:514-516`).
- **Comment-to-agent delivery is prompt concatenation, not a separate API:** `generateReviewMarkdown` (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:59-88`) emits a `## Review Comments (n)` block that `handleSend`/`handleQueueMessage` join with the chat text via `buildAgentPrompt` (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:501-534`, `packages/web-core/src/shared/lib/promptMessage.ts:11-26`).
- **PR creation is push-then-`gh pr create`:** the `create_pr` route (`crates/server/src/routes/workspaces/pr.rs:188-388`) checks the target branch exists, pushes the workspace branch, delegates to `GitHostService`/`GhCli::create_pr` (`crates/git-host/src/github/cli.rs:225-261`), and stores a local `PullRequest` row.
- **Merge state is polled, not pushed:** `pr_monitor` ticks every 60 seconds (`crates/services/src/services/pr_monitor.rs:68`), calls `get_pr_status`, updates the local row, and archives the workspace when its PRs are all merged or closed (`crates/services/src/services/pr_monitor.rs:128-211`).
- **Conflicts surface through branch-status polling, and direct merge is blocked when a PR is open:** `get_workspace_branch_status` reports `is_rebase_in_progress`, `conflicted_files`, and `conflict_op` (`crates/server/src/routes/workspaces/git.rs:411-429`); `merge_workspace` refuses when an open PR exists or the target is remote (`crates/server/src/routes/workspaces/git.rs:195-213`); rebase conflicts return a typed `MergeConflicts` error with file list (`crates/server/src/routes/workspaces/git.rs:756-770`).

---
## 1. Diff computation path: base commit to `Diff` structs
The review UI never diffs two branches directly. It resolves a base commit (the common ancestor point the workspace started from) and diffs the live worktree files against it.

Step 1 — resolve the base. `compute_diff_stats` (`crates/services/src/services/diff_stream.rs:43-92`) shows the canonical pattern per repo: call `git.get_base_commit(&repo_path, &workspace_branch, &target_branch)`, then `git.get_diffs(&worktree, &base_commit, None)`. The base-commit and branch-status helpers live alongside push and remote checks in `crates/git/src/lib.rs:693-728` (`get_branch_status`, `get_base_commit`, `get_remote_branch_status`) and `crates/git/src/lib.rs:1479` (`push_to_remote`).

Step 2 — name-status via a temporary index. `GitCli::diff_status` (`crates/git/src/cli.rs:168-228`) builds a throwaway `GIT_INDEX_FILE`, runs `read-tree HEAD`, stages current plus untracked paths with `git add -A --pathspec-from-file`, then runs the comparison:

```rust
// `crates/git/src/cli.rs:216-227`
let mut args: Vec<OsString> = vec![
    "-c".into(),
    "core.quotepath=false".into(),
    "diff".into(),
    "--cached".into(),
    "-M".into(),
    "--name-status".into(),
    OsString::from(base_commit.to_string()),
];
```

The `-M` flag enables rename detection; the comment at `crates/git/src/cli.rs:166` notes this path always includes untracked files. Output is parsed by `parse_name_status` (`crates/git/src/cli.rs:466`) into `StatusDiffEntry` values carrying a `ChangeType` (`crates/git/src/cli.rs:47`).

Step 3 — hydrate content. `GitService::get_diffs` (`crates/git/src/lib.rs:326-353`):

```rust
// `crates/git/src/lib.rs:327-353`
pub fn get_diffs(
    &self,
    worktree_path: &Path,
    base_commit: &Commit,
    path_filter: Option<&[&str]>,
) -> Result<Vec<Diff>, GitServiceError> {
    // Use Git CLI to compute diff vs base to avoid sparse false deletions
    let repo = Repository::open(worktree_path)?;
    ...
    let entries = git
        .diff_status(worktree_path, base_commit, cli_opts)
        .map_err(|e| GitServiceError::InvalidRepository(format!("git diff failed: {e}")))?;
```

Each entry becomes a flattened `Diff` via `status_entry_to_diff` (`crates/git/src/lib.rs:435`), mapping `ChangeType` to `DiffChangeKind` (`Added`, `Deleted`, `Modified`, `Renamed`, `Copied`, `PermissionChange`) and loading old text from the base tree blob plus new text from the filesystem with three guards in `read_file_to_string` (`crates/git/src/lib.rs:394-431`): size guard against `MAX_INLINE_DIFF_BYTES` (`crates/git/src/lib.rs:61-63`, ~2 MB), binary guard (null byte), and UTF-8 validation. A cheap file-list-only variant exists as `get_diff_file_paths` (`crates/git/src/lib.rs:358-372`).

Step 4 — stream to the UI. Diffs travel over the websocket (a persistent two-way connection between browser and server) route `GET /diff/ws` (`crates/server/src/routes/workspaces/git.rs:140`), served by `stream_workspace_diff_ws` (`crates/server/src/routes/workspaces/streams.rs:40-42`, query type at `crates/server/src/routes/workspaces/streams.rs:16`). The stream handle owns its filesystem watcher and aborts it on drop (`crates/services/src/services/diff_stream.rs:114-139`); cumulative content is capped at `MAX_CUMULATIVE_DIFF_BYTES` (`crates/services/src/services/diff_stream.rs:95`) before bodies are omitted. Stats badges use the lighter `compute_diff_stats` path (`crates/services/src/services/diff_stream.rs:43-92`), also called after pushes in `crates/server/src/routes/workspaces/git.rs:302` and `crates/server/src/routes/workspaces/git.rs:355`.

| Stage | Function | Input → output |
|-------|----------|----------------|
| Base resolution | `get_base_commit` (`crates/git/src/lib.rs:709`) | workspace branch + target branch → base `Commit` |
| Name-status | `diff_status` (`crates/git/src/cli.rs:168-228`) | worktree + base commit → `StatusDiffEntry[]` |
| Hydration | `status_entry_to_diff` (`crates/git/src/lib.rs:435`) | entry + base tree → `Diff` with `oldContent`/`newContent` |
| Transport | diff websocket + `compute_diff_stats` (`crates/services/src/services/diff_stream.rs:43-95`) | `Diff[]` → live UI patches and file/line counts |

## 2. Frontend diff UI: `@pierre/diffs` viewer plus two comment layers
The changes panel is `ChangesPanelContainer.tsx` (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:1-53`), which renders each file with `FileDiff`/`Virtualizer`/`WorkerPoolContextProvider` from `@pierre/diffs/react` (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:9-18`), using a portable worker (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:15-18`) with a pool of 3 (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:59`).

Backend `Diff` objects are adapted per file by `transformDiffToFileDiffMetadata` (`packages/web-core/src/shared/lib/diffDataAdapter.ts:81-141`), which feeds old/new contents to `parseDiffFromFile` and then overrides the detected kind via `mapChangeKindToChangeType` (`packages/web-core/src/shared/lib/diffDataAdapter.ts:34-56`):

```ts
// `packages/web-core/src/shared/lib/diffDataAdapter.ts:40-45`
case 'added':
  return 'new';
case 'deleted':
  return 'deleted';
case 'modified':
  return 'change';
```

`contentOmitted` files yield an empty-hunk placeholder with `isPartial: true` (`packages/web-core/src/shared/lib/diffDataAdapter.ts:88-107`). View preferences (unified vs side-by-side, wrap, ignore-whitespace) come from `useDiffViewStore` (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:29-33`); the user doc describes the two modes and the navbar/command-bar toggle (`docs/reviewing-code.mdx:40-59`). Large or purely renamed/deleted views auto-collapse via `COLLAPSE_BY_CHANGE_TYPE` and `COLLAPSE_MAX_LINES = 800` (`packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:65-84`).

Two annotation layers share the gutter through one union (`packages/web-core/src/shared/lib/diffDataAdapter.ts:19-21`):

```ts
// `packages/web-core/src/shared/lib/diffDataAdapter.ts:19-21`
export type CommentAnnotation =
  | { type: 'review'; comment: ReviewComment }
  | { type: 'github'; comment: NormalizedGitHubComment };
```

`transformCommentsToAnnotations` (`packages/web-core/src/shared/lib/diffDataAdapter.ts:166-224`) adds all local review comments first, then GitHub PR comments only when no local comment occupies the same `filePath:lineNumber:side` key — local drafts win ties. Renderers split accordingly: `ReviewCommentRenderer` (`packages/web-core/src/pages/workspaces/ReviewCommentRenderer.tsx:6-14`) and `GitHubCommentRenderer`, both built on the shared `CommentCard` (`packages/ui/src/components/CommentCard.tsx:27`).

## 3. Inline comment data model and API: local-only state
There is no comment table, no comment route, and no server round-trip for draft review comments. The model is a frontend interface (`packages/web-core/src/shared/hooks/useReview.ts:5-12`):

```ts
// `packages/web-core/src/shared/hooks/useReview.ts:5-12`
export interface ReviewComment {
  id: string;
  filePath: string;
  lineNumber: number;
  side: DiffSide;
  text: string;
  codeLine?: string;
}
```

(`DiffSide` is 0 = old, 1 = new; mapped to `deletions`/`additions` in `packages/web-core/src/shared/lib/diffDataAdapter.ts:61-63`.) The context API exposes `comments`, `drafts`, `addComment`, `updateComment`, `deleteComment`, `clearComments`, `setDraft`, `generateReviewMarkdown` (`packages/web-core/src/shared/hooks/useReview.ts:22-31`), implemented with `useState` in `ReviewProvider` (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:16-25`):

```tsx
// `packages/web-core/src/shared/hooks/ReviewProvider.tsx:19-25`
const addComment = useCallback((comment: Omit<ReviewComment, 'id'>) => {
  const newComment: ReviewComment = {
    ...comment,
    id: genId(),
  };
  setComments((prev) => [...prev, newComment]);
}, []);
```

The authoring widget is `CommentWidgetLine` (`packages/web-core/src/pages/workspaces/CommentWidgetLine.tsx:15-42`): hover a diff line, type in the `WYSIWYGEditor`, and `handleSave` calls `addComment` with file/side/line plus the source `codeLine`, then clears the draft (`packages/web-core/src/pages/workspaces/CommentWidgetLine.tsx:30-42`). This matches the user doc: hover → comment icon → submit (`docs/reviewing-code.mdx:61-76`), with the warning that comments are batched, not sent individually (`docs/reviewing-code.mdx:77-79`).

GitHub-side comments are a separate, read-only feed: `GET /workspaces/:id/pull-requests/comments?repo_id=` (`crates/server/src/routes/workspaces/pr.rs:850`) runs `get_pr_comments` (`crates/server/src/routes/workspaces/pr.rs:543-615`), which fans out to `fetch_general_comments` plus `fetch_review_comments` in parallel and merges them into a time-sorted `UnifiedPrComment` timeline (`crates/git-host/src/github/mod.rs:300-353`). The two variants are `General` and `Review` with `path`/`line`/`side`/`diff_hunk` (`crates/git-host/src/types.rs:107-131`); raw shapes come from `gh pr view --json comments` and `gh api repos/{o}/{r}/pulls/{n}/comments` (`crates/git-host/src/github/cli.rs:361-399`).

## 4. Comment-to-agent feedback: markdown block inside the next prompt
Sending feedback is the chat send path with one extra context part. `SessionChatBoxContainer` reads the optional review context (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:299-304`):

```tsx
// `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:299-304`
const reviewContext = useReviewOptional();
const reviewMarkdown = useMemo(
  () => reviewContext?.generateReviewMarkdown() ?? '',
  [reviewContext]
);
const hasReviewComments = (reviewContext?.comments.length ?? 0) > 0;
```

`generateReviewMarkdown` (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:59-88`) builds a `## Review Comments (n)` section with `**path** (Line n)`, a fenced or inline code line, and the body as a blockquote, backtick-wrapping anything that looks like a path. Both `handleSend` and `handleQueueMessage` (queueing means parking a message to run after the current agent turn finishes) pass it as context (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:501-534`, `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:557-581`):

```tsx
// `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:501-504`
const handleSend = useCallback(async () => {
  const { prompt, isSlashCommand } = buildAgentPrompt(localMessage, [
    reviewMarkdown,
  ]);
```

`buildAgentPrompt` (`packages/web-core/src/shared/lib/promptMessage.ts:11-26`) joins non-empty context parts ahead of the typed message — except for slash commands (messages starting with `/` that trigger built-in actions instead of free chat), which send only the command text:

```ts
// `packages/web-core/src/shared/lib/promptMessage.ts:11-26`
export function buildAgentPrompt(
  rawUserMessage: string,
  contextParts: (string | null | undefined)[]
) {
  const trimmed = rawUserMessage.trim();
  const isSlashCommand = !!trimmed && isSlashCommandPrompt(trimmed);
  const parts = isSlashCommand
    ? [trimmed]
    : [...contextParts, rawUserMessage].filter(Boolean);
  return {
    prompt: parts.join('\n\n'),
    isSlashCommand,
  };
}
```

After a successful non-command send (or any queue), comments are consumed: `reviewContext?.clearComments()` (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:514-516`, `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:570`), and switching workspaces resets via the `workspaceId` effect (`packages/web-core/src/shared/hooks/ReviewProvider.tsx:44-46`). The chat box shows a badge with count, markdown preview, and clear action while drafts exist (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:1117-1121`). User-facing semantics — comments consumed into chat history, agent sees all inline comments as context, empty panel means no changes or already-merged state — are stated in `docs/reviewing-code.mdx:81-107`.

## 5. PR create, describe, and merge flow
Routes are mounted under `/pull-requests` (`crates/server/src/routes/workspaces/mod.rs:38`) with exactly three endpoints (`crates/server/src/routes/workspaces/pr.rs:846-851`): `POST /` → `create_pr`, `POST /attach` → `attach_existing_pr`, `GET /comments` → `get_pr_comments`.

Create (`crates/server/src/routes/workspaces/pr.rs:188-388`) runs: resolve workspace repo and target branch (defaulting to the stored `target_branch`, `crates/server/src/routes/workspaces/pr.rs:205-209`); resolve remotes including remote-tracking branches like `upstream/main` (`crates/server/src/routes/workspaces/pr.rs:221-232`); fail with typed `TargetBranchNotFound` if the base is missing (`crates/server/src/routes/workspaces/pr.rs:234-254`); `push_to_remote` the workspace branch (`crates/server/src/routes/workspaces/pr.rs:256-271`); pick a host via `GitHostService::from_url` (`crates/server/src/routes/workspaces/pr.rs:273-288`); then `create_pr` with `CreatePrRequest { title, body, head_branch, base_branch, draft, head_repo_url }` (`crates/git-host/src/types.rs:26-34`, request built at `crates/server/src/routes/workspaces/pr.rs:291-298`). The GitHub implementation shells to `gh pr create --repo --head --base --title --body-file [--draft]` (`crates/git-host/src/github/cli.rs:225-261`, body passed via temp file to avoid quoting issues) with 1s–30s exponential retry (`crates/git-host/src/github/mod.rs:205-221`). On success the server records `PullRequest::create_for_workspace`, syncs to remote, auto-opens the browser URL, tracks `pr_created`, and optionally fires an agent follow-up to write the PR description from `DEFAULT_PR_DESCRIPTION_PROMPT` (`crates/server/src/routes/workspaces/pr.rs:304-367`; follow-up builder at `crates/server/src/routes/workspaces/pr.rs:96-186`).

Attach and describe cover existing PRs: `attach_existing_pr` (`crates/server/src/routes/workspaces/pr.rs:390-541`) short-circuits if a PR row already exists, otherwise lists PRs for the branch (open first, then merged/closed via `gh pr list --state all --head`, `crates/git-host/src/github/cli.rs:279-301`), stores the first hit, and archives the workspace when the attached PR is already merged and no open PRs remain (`crates/server/src/routes/workspaces/pr.rs:507-525`). Status reads go through `gh pr view --json number,url,state,mergedAt,mergeCommit,...` (`crates/git-host/src/github/cli.rs:264-276`) mapped to `PullRequestDetail` (`crates/git-host/src/types.rs:142-152`).

Merge itself happens on GitHub (button or `gh pr merge`); Vibe Kanban only observes. `pr_monitor` (`crates/services/src/services/pr_monitor.rs:48-85`) polls every 60s, `get_pr_status` per open PR, persists `update_status` with `merged_at`/`merge_commit_sha`, and calls `try_archive_workspace`, which archives only when zero open PRs remain for the workspace (`crates/services/src/services/pr_monitor.rs:128-211`). Local direct merge (`POST /merge`, `crates/server/src/routes/workspaces/git.rs:141`) is the non-PR path: it refuses when any open PR exists for the repo or when the target is a remote branch, then squash-merges and records `Merge::create_direct` (`crates/server/src/routes/workspaces/git.rs:179-266`).

| Operation | Entry | Effect |
|-----------|-------|--------|
| Create PR | `POST /workspaces/:id/pull-requests` (`crates/server/src/routes/workspaces/pr.rs:848`) | push branch → `gh pr create` → local PR row → optional description follow-up |
| Attach existing | `POST /workspaces/:id/pull-requests/attach` (`crates/server/src/routes/workspaces/pr.rs:849`) | `gh pr list --state all` → store first hit → archive if already merged |
| Read comments | `GET /workspaces/:id/pull-requests/comments` (`crates/server/src/routes/workspaces/pr.rs:850`) | general + inline comments merged by timestamp |
| Direct merge | `POST /workspaces/:id/git/merge` (`crates/server/src/routes/workspaces/git.rs:141`) | blocked with open PR or remote target; else squash merge + archive |
| Status sync | `pr_monitor` 60s loop (`crates/services/src/services/pr_monitor.rs:68-85`) | merged/closed PRs → update row → archive when none open |

## 6. Conflict handling: detection, rebase, abort/continue
Conflict state is derived per repo on every branch-status read (`crates/server/src/routes/workspaces/git.rs:411-429`): `is_rebase_in_progress`, `get_conflicted_files`, and `detect_conflict_op` only when conflicts are non-empty. The op enum distinguishes four git (the underlying version-control tool) operations (`crates/git/src/lib.rs:68-73`):

```rust
// `crates/git/src/lib.rs:65-73`
pub enum ConflictOp {
    Rebase,
    Merge,
    CherryPick,
    Revert,
}
```

Detection checks sentinel files in order — rebase state dirs, then `MERGE_HEAD`, cherry-pick, revert (`crates/git/src/lib.rs:1283-1304`). Conflicted paths come from `git diff --name-only --diff-filter=U` (`crates/git/src/cli.rs:697-700`, surfaced via `crates/git/src/lib.rs:1307-1315`). Rebase progress is defined as the existence of `rebase-merge` or `rebase-apply` state directories (`crates/git/src/cli.rs:551-561`).

Rebase (`POST /rebase`, `crates/server/src/routes/workspaces/git.rs:144`) updates the stored target branch if the new base exists, then calls `rebase_branch` (`crates/server/src/routes/workspaces/git.rs:749-755`), which refuses dirty worktrees (`crates/git/src/lib.rs:1140-1143`), refuses when a rebase is already in progress (`crates/git/src/lib.rs:1145-1148`), and runs `git rebase --onto <new_base> <merge_base(old_base, task_branch)> <task_branch>` where the merge base prefers `--fork-point` with fallback (`crates/git/src/cli.rs:514-549`). Conflict-looking stderr (`could not apply`, `resolve all conflicts`) becomes `GitServiceError::MergeConflicts` with the sampled file list (`crates/git/src/lib.rs:1162-1201`), which the route converts to a typed `GitOperationError::MergeConflicts { op: Rebase, conflicted_files, target_branch }` response (`crates/server/src/routes/workspaces/git.rs:756-770`).

Direct merge is stricter: `merge_changes` (`crates/git/src/lib.rs:575-596`) first blocks when the base has moved ahead (`BranchesDiverged`), then either CLI-merges in the base checkout or falls back to an in-memory squash via `merge_commits` with `fail_on_conflict(true)` (`crates/git/src/lib.rs:1081-1126`), returning `MergeConflicts` without touching the tree when `index.has_conflicts()`. Recovery endpoints are `POST /rebase/continue` → `continue_rebase` (fails on unresolved conflicts, `crates/git/src/cli.rs:610-618`, route at `crates/server/src/routes/workspaces/git.rs:819-839`) and `POST /conflicts/abort` → `abort_conflicts` (rebase → abort or `--quit` when clean; merge/cherry-pick/revert → respective abort; no-op otherwise, `crates/git/src/lib.rs:1333-1368`, route at `crates/server/src/routes/workspaces/git.rs:795-816`). The chat layer reads the same status to offer a resolve dialog (`packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:318-359`).

## 7. Scope note: `crates/review` is a different "review"
The `crates/review` binary is not the in-app diff review above — it is a standalone CLI (command-line interface, a terminal program) that turns a GitHub PR URL into a hosted narrative summary. Its `run` pipeline (`crates/review/src/main.rs:133-260`) parses the URL (`crates/review/src/github.rs:52-88`), fetches PR metadata via `gh pr view --json title,body,baseRefOid,headRefOid,headRefName` with a `gh api` fallback (`crates/review/src/github.rs:147-199`), optionally attaches Claude session files, clones to a temp dir (`crates/review/src/github.rs:202-226`), checks out the head SHA by fetch + checkout so deleted branches still work (`crates/review/src/github.rs:232-268`), tars the tree, then `init → upload → start → poll` against `https://api.vibekanban.com/v1/review/*` with 10s polls and a 10-minute timeout (`crates/review/src/api.rs:85-211`, constants at `crates/review/src/main.rs:21-23`). Do not cite it for inline comments, `ReviewComment`, or the agent feedback loop — those are exclusively the frontend `ReviewProvider` plus chat-send mechanism in sections 3–4.

**Covers:** `crates/git/src/lib.rs:61-73, 326-372, 435, 575-596, 1081-1148, 1283-1368, 1479` · `crates/git/src/cli.rs:47, 166-228, 466, 514-561, 697-700` · `crates/services/src/services/diff_stream.rs:43-95, 114-139` · `crates/services/src/services/pr_monitor.rs:48-85, 128-211` · `crates/server/src/routes/workspaces/git.rs:140-146, 179-266, 302-429, 695-839` · `crates/server/src/routes/workspaces/streams.rs:16, 40-42` · `crates/server/src/routes/workspaces/pr.rs:96-186, 188-388, 390-541, 543-615, 846-851` · `crates/server/src/routes/workspaces/mod.rs:38` · `crates/git-host/src/types.rs:26-34, 94-152` · `crates/git-host/src/github/cli.rs:225-261, 264-301, 361-399` · `crates/git-host/src/github/mod.rs:158-221, 300-353` · `packages/web-core/src/shared/hooks/useReview.ts:5-31` · `packages/web-core/src/shared/hooks/ReviewProvider.tsx:16-25, 44-46, 59-88` · `packages/web-core/src/shared/lib/diffDataAdapter.ts:19-21, 34-63, 81-141, 166-224` · `packages/web-core/src/shared/lib/promptMessage.ts:11-26` · `packages/web-core/src/pages/workspaces/ChangesPanelContainer.tsx:1-33, 59-84` · `packages/web-core/src/pages/workspaces/CommentWidgetLine.tsx:15-42` · `packages/web-core/src/pages/workspaces/ReviewCommentRenderer.tsx:6-14` · `packages/ui/src/components/CommentCard.tsx:27` · `packages/web-core/src/features/workspace-chat/ui/SessionChatBoxContainer.tsx:299-304, 318-359, 501-581, 1117-1121` · `docs/reviewing-code.mdx:6-107` · `crates/review/src/main.rs:21-23, 133-260` · `crates/review/src/api.rs:85-211` · `crates/review/src/github.rs:52-88, 147-199, 202-268`
