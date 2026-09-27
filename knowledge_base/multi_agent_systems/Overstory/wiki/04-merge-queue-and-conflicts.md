> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Merge Queue and Conflict Resolution
**In one sentence:** Overstory serializes agent branch integration through a SQLite-backed FIFO (first-in-first-out) merge queue and resolves each branch with a strictly ordered 4-tier escalation from clean merge to full reimplementation.
## Key points
- Queue is SQLite table `merge_queue` with `INTEGER PRIMARY KEY AUTOINCREMENT` ordering, WAL (write-ahead logging) mode, 5s busy timeout, and statuses `pending,merging,merged,conflict,failed` (`src/merge/queue.ts:45-57`, `src/merge/queue.ts:104-110`).
- FIFO (first-in-first-out) is enforced by `SELECT ... WHERE status='pending' ORDER BY id ASC LIMIT 1`; `dequeue()` deletes by id while `peek()` is non-destructive and `list()` is id-ordered (`src/merge/queue.ts:135-137`, `src/merge/queue.ts:188-209`, `src/merge/queue.ts:211-221`).
- Tier order is fixed: 1 clean-merge, 2 auto-resolve, 3 AI (artificial intelligence)-resolve, 4 reimagine; tiers are attempted in order, disabled or historically failed tiers are skipped (`src/merge/resolver.ts:4-12`, `src/merge/resolver.ts:796-796`, `src/merge/resolver.ts:836-836`, `src/merge/resolver.ts:872-872`).
- Tier 2 keeps incoming agent hunks by regex-parsing conflict markers, concatenates both sides for `merge=union` files, and refuses to discard non-empty canonical hunks (`src/merge/resolver.ts:142-155`, `src/merge/resolver.ts:173-186`, `src/merge/resolver.ts:273-279`).
- Tiers 3-4 shell out to a configured print-command runtime, reject prose-like output via `looksLikeProse()`, and Tier 4 aborts the merge then reimplements each listed file from `git show canonical:file` versus `git show branch:file` (`src/merge/resolver.ts:340-409`, `src/merge/resolver.ts:314-333`, `src/merge/resolver.ts:415-495`).
- CLI (command-line interface) surface is `ov merge --branch <name> | --all [--into <branch>] [--dry-run] [--json]`; `--all` processes pending entries sequentially in FIFO (first-in-first-out) order and rewrites queue status to `merged` or `conflict` (`src/commands/merge.ts:7-12`, `src/commands/merge.ts:24-30`, `src/commands/merge.ts:300-316`, `src/commands/merge.ts:240-240`).
- Doctor checks validate database readability, table schema, >24h stale `pending/merging` entries, and duplicate branch rows, with auto-fixes that delete stale rows and deduplicate to `MAX(id)` per branch (`src/doctor/merge-queue.ts:40-70`, `src/doctor/merge-queue.ts:88-128`, `src/doctor/merge-queue.ts:132-160`).
---
## Queue storage and ordering
Backing store is SQLite via `bun:sqlite` with synchronous access, documented as FIFO (first-in-first-out) ordering guaranteed via autoincrement id (`src/merge/queue.ts:2-7`). Database setup enables concurrent multi-agent access (`src/merge/queue.ts:104-110`):
```ts
db.exec("PRAGMA journal_mode = WAL");
db.exec("PRAGMA synchronous = NORMAL");
db.exec("PRAGMA busy_timeout = 5000");
```
Schema is created if absent with two indexes (`src/merge/queue.ts:45-62`):
```sql
CREATE TABLE IF NOT EXISTS merge_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  branch_name TEXT NOT NULL,
  task_id TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  files_modified TEXT NOT NULL DEFAULT '[]',
  enqueued_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK(status IN ('pending','merging','merged','conflict','failed')),
  resolved_tier TEXT
    CHECK(resolved_tier IS NULL OR resolved_tier IN ('clean-merge','auto-resolve','ai-resolve','reimagine'))
)
```
`files_modified` is a JSON (JavaScript Object Notation) array stored as text and parsed with empty-array fallback (`src/merge/queue.ts:39-39`, `src/merge/queue.ts:64-84`). On open, a migration renames legacy `bead_id` to `task_id` only when the old column exists and the new one does not (`src/merge/queue.ts:90-96`).
Queue flow:
```
enqueue(branch) --> SQLite APPEND (id=N, status=pending)
                        |
handleAll: list(pending ORDER BY id) --> for each entry in order:
                        |
              resolver.resolve(entry, canonical)
                        |
              updateStatus(branch, merged|conflict, tier)
                        |
dequeue/peek: SELECT pending ORDER BY id ASC LIMIT 1 (dequeue DELETEs)
```
## Queue operations
Interface exposes five operations plus close (`src/merge/queue.ts:13-31`):
```ts
enqueue(entry: Omit<MergeEntry, "enqueuedAt" | "status" | "resolvedTier">): MergeEntry;
dequeue(): MergeEntry | null;
peek(): MergeEntry | null;
list(status?: MergeEntry["status"]): MergeEntry[];
updateStatus(branchName: string, status: MergeEntry["status"], tier?: ResolutionTier): void;
close(): void;
```
`enqueue()` serializes `filesModified` to JSON (JavaScript Object Notation), timestamps with `new Date().toISOString()`, and uses `INSERT ... RETURNING *` (`src/merge/queue.ts:169-186`, `src/merge/queue.ts:130-133`). `dequeue()` fetches the lowest-id pending row then deletes that id, returning `null` when empty (`src/merge/queue.ts:188-199`). Its selector is (`src/merge/queue.ts:135-137`):
```sql
SELECT * FROM merge_queue WHERE status = 'pending' ORDER BY id ASC LIMIT 1
```
`peek()` uses the same selector without deletion (`src/merge/queue.ts:201-209`). `list()` returns all rows or status-filtered rows in id order (`src/merge/queue.ts:211-221`). `updateStatus()` looks up by branch name, throws `MergeError` when absent, and writes status plus nullable tier (`src/merge/queue.ts:223-239`). `close()` runs a passive WAL (write-ahead logging) checkpoint before closing (`src/merge/queue.ts:241-244`).
## 4-tier conflict resolution in order
Resolver header defines the escalation contract: each tier attempted in order, failures fall through, disabled tiers skipped (`src/merge/resolver.ts:4-12`):
```ts
*   1. Clean merge — git merge with no conflicts
*   2. Auto-resolve — parse conflict markers, keep incoming (agent) changes
*   3. AI-resolve — use Claude to resolve remaining conflicts
*   4. Re-imagine — abort merge and reimplement changes from scratch
```
Skipping tiers without attempting lower ones is the named `TIER_SKIP` failure in the merger agent contract (`agents/merger.md:13-13`).
### Tier 1: clean merge
Runs `git merge --no-edit <branch>`; exit 0 means success, otherwise collects conflicted files via `git diff --name-only --diff-filter=U` (`src/merge/resolver.ts:235-248`, `src/merge/resolver.ts:119-125`):
```ts
const { exitCode } = await runGit(repoRoot, ["merge", "--no-edit", entry.branchName]);
```
### Tier 2: auto-resolve
Parses conflict markers and keeps content between `=======` and `>>>>>>>` (`src/merge/resolver.ts:256-259`). Core regex keeps the second capture group, the incoming side (`src/merge/resolver.ts:142-155`):
```ts
const conflictPattern = /^<{7} .+\n([\s\S]*?)^={7}\n([\s\S]*?)^>{7} .+\n?/gm;
return content.replace(conflictPattern, (_match, _canonical: string, incoming: string) => {
  return incoming;
});
```
Two safety branches exist. For files with `merge=union` gitattribute, detected by `git check-attr merge -- <file>`, both sides are concatenated (`src/merge/resolver.ts:210-214`, `src/merge/resolver.ts:173-186`). For normal files, if the canonical (`HEAD`) side contains non-whitespace, the file is skipped and escalated with a content-drop warning instead of silently discarding canonical work (`src/merge/resolver.ts:273-279`, `src/merge/resolver.ts:193-204`). Resolved files are staged with `git add` and committed with `git commit --no-edit`; any file without markers, failed add, or read error stays in `remainingConflicts` (`src/merge/resolver.ts:285-307`).
### Tier 3: AI-resolve
For each remaining file, sends full conflicted content to a print-command runtime with a strict raw-output prompt (`src/merge/resolver.ts:340-365`):
```ts
"You are a merge conflict resolver. Output ONLY the resolved file content.",
"Rules: NO explanation, NO markdown fencing, NO conversation, NO preamble.",
```
Empty output, nonzero exit, prose-like output, or failed `git add` keeps the file conflicted (`src/merge/resolver.ts:381-399`). Prose detection matches LLM (large language model) preambles, fencing, and refusal patterns (`src/merge/resolver.ts:314-333`). Success commits all files (`src/merge/resolver.ts:407-408`). Past successful resolutions for overlapping files are injected as history context (`src/merge/resolver.ts:353-356`).
### Tier 4: reimagine
Aborts the in-progress merge, then for every file in `entry.filesModified` reads both `git show canonical:file` and `git show branch:file`, asks the model to reimplement branch changes onto canonical content, validates non-prose output, stages, and finally commits with `Reimagine merge: <branch> onto <canonical>` (`src/merge/resolver.ts:415-495`, `src/merge/resolver.ts:422-422`, `src/merge/resolver.ts:427-436`, `src/merge/resolver.ts:488-492`). Any missing object, empty output, prose output, or failed add aborts the whole tier (`src/merge/resolver.ts:438-484`). If all enabled tiers fail, the resolver runs `git merge --abort` defensively and returns `status: failed` with the last attempted tier (`src/merge/resolver.ts:906-924`).
## Pre-merge guards and history learning
Before Tier 1, the resolver avoids checkout when already on the canonical branch via `git symbolic-ref --short HEAD`, preventing worktree errors (`src/merge/resolver.ts:672-691`). It then checks dirty tracked files with unstaged plus staged `git diff --name-only`, auto-commits only `os-eco` runtime state paths such as `.seeds/`, `.overstory/`, `.mulch/`, `CLAUDE.md`, and stashes any remaining dirty files with restore in `finally` (`src/merge/resolver.ts:696-724`, `src/merge/resolver.ts:59-76`, `src/merge/resolver.ts:102-114`, `src/merge/resolver.ts:925-929`). It also deletes untracked files that overlap `entry.filesModified` so `git merge` does not refuse to overwrite them (`src/merge/resolver.ts:735-758`).
Learning uses Mulch, a pattern store client. Search output is parsed by regex for `Merge conflict <resolved|failed> at tier <tier>. Branch: <b>. Agent: <a>. Conflicting files: <files>` (`src/merge/resolver.ts:501-535`). History builder scopes patterns to files overlapping the current entry; a tier with at least 2 failures and 0 successes for those files enters `skipTiers`, while successful descriptions become prompt context and overlapping historical files become predictions (`src/merge/resolver.ts:549-602`, `src/merge/resolver.ts:575-580`). Lookup is fire-and-forget with empty history on error (`src/merge/resolver.ts:608-619`). Every non-clean outcome is recorded with branch, agent, files, tier, and evidence task id, also fire-and-forget (`src/merge/resolver.ts:626-650`).
## Merger agent role
Merger is a branch integration specialist that merges completed worker branches into the target in dependency order, or completion order when no dependencies are declared, verifying tests after each merge because a failed merge blocks later merges (`agents/merger.md:66-70`, `agents/merger.md:148-153`). Its workflow is review-then-merge: inspect `git log target..branch` and `git diff target...branch`, identify multi-branch conflict zones, escalate Tier 1 through Tier 4, run quality gates, close the tracker issue, and mail a result (`agents/merger.md:100-146`, `agents/merger.md:134-146`). Required mail reports tier used, conflicts, and test status (`agents/merger.md:140-146`). Constraints forbid writing outside the assigned worktree and file scope, pushing to canonical branches, running `git push`, spawning sub-workers, and closing before quality gates pass (`agents/merger.md:26-32`). Non-trivial Tier 2+ merges must record Mulch learnings; clean Tier 1 merges are exempt (`agents/merger.md:52-57`, `agents/merger.md:18-18`). Unresolvable conflicts must be escalated by mail as urgent errors, not silently dropped (`agents/merger.md:16-16`).
## Cross-review rework loop
Reviewer is strictly read-only: no `Write`/`Edit`, no `git commit/checkout/merge/reset`, no filesystem or install mutations; violations and errors must be mailed to the parent (`agents/reviewer.md:23-35`, `agents/reviewer.md:9-15`). Its role is validation specialist checking correctness, edge cases, types, error handling, style, security, dependencies, tests, and performance (`agents/reviewer.md:67-69`, `agents/reviewer.md:123-133`). Workflow is read overlay and spec, `ml prime` for conventions, `git diff base...feature` plus full file reads, run quality gates, close with `PASS`/`FAIL`, and mail detailed feedback (`agents/reviewer.md:98-121`). The loop is therefore reviewer `PASS/FAIL` mail to parent or builder, builder rework on its own branch, then merger integration; the reviewer never merges (`agents/reviewer.md:29-30`) and the standard worker/merger path never pushes directly to canonical (`agents/merger.md:28-29`). Review findings carry a suggested Mulch classification — `foundational`, `tactical`, or `observational` — so the parent records them accurately (`agents/reviewer.md:93-94`).
## Merge CLI surface
`ov merge` requires either `--branch <name>` or `--all` (`src/commands/merge.ts:140-144`). Target branch resolution is `--into` flag, else `.overstory/session-branch.txt`, else configured canonical branch (`src/commands/merge.ts:149-161`). Queue lives at `.overstory/merge-queue.db` and the resolver is constructed from `aiResolveEnabled` and `reimagineEnabled` config flags (`src/commands/merge.ts:162-169`). Branch names follow `overstory/{agentName}/{taskId}` with `unknown` fallback for both fields (`src/commands/merge.ts:37-56`). Ad-hoc branches not already queued are verified with `git rev-parse --verify refs/heads/<branch>`, have modified files detected with `git diff --name-only canonical...branch`, and are enqueued before merging (`src/commands/merge.ts:200-224`, `src/commands/merge.ts:62-87`). Single-branch mode supports `--dry-run` listing without merging and `--json` structured output; on real merges it writes `merged` or `conflict` plus tier back to the queue and throws on failure (`src/commands/merge.ts:227-253`). `--all` mode lists `pending` entries, short-circuits with a hint or empty JSON (JavaScript Object Notation) result when none exist, otherwise resolves sequentially, updates each entry, prints each result, and summarizes `successCount/failCount` (`src/commands/merge.ts:260-324`).
## Doctor checks
`checkMergeQueue` validates `merge-queue.db` under the `.overstory` directory (`src/doctor/merge-queue.ts:10-12`). Absent database is a pass as normal for new installations (`src/doctor/merge-queue.ts:14-22`). Unopenable or unreadable databases are fixable failures (`src/doctor/merge-queue.ts:24-37`, `src/doctor/merge-queue.ts:46-58`). Missing `merge_queue` table is a fixable schema failure; otherwise a pass reports entry count (`src/doctor/merge-queue.ts:60-86`). Entries in `pending` or `merging` older than 24 hours produce a fixable warning listing branch, status, and age; the fix deletes rows with `enqueued_at` older than the threshold (`src/doctor/merge-queue.ts:88-129`). Duplicate branch names produce a fixable warning; the fix keeps only `MAX(id)` per branch (`src/doctor/merge-queue.ts:132-160`).
**Covers:** src/merge/queue.ts, src/merge/resolver.ts, src/commands/merge.ts, src/doctor/merge-queue.ts, agents/merger.md, agents/reviewer.md
