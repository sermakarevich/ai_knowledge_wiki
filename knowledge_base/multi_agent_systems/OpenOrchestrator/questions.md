---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: OpenOrchestrator (`owt`)

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does "supervise, don't replace" mean in owt, and what are two things owt deliberately never does?

> [!tip]- Answer
> It means the cockpit owns prioritization and shipping decisions while the external harnesses own code generation. owt never calls an LLM itself and never edits code — see [[wiki/06-status-mcp-observability|Status/MCP]] and [[summary]] §4.

### Q2. Name the three control-plane lanes and the rule that decides which rows land in NEEDS YOU.

> [!tip]- Answer
> NEEDS YOU / READY TO SHIP / IN FLIGHT (`models/control_plane.py:18-28`). NEEDS YOU = leftover merge/rebase state (MERGE_HEAD check) sorted first plus BLOCKED/ERROR tracker rows — see [[wiki/01-control-plane-cockpit|Cockpit]].

### Q3. What does the footer show, and why is it rebuilt on every render?

> [!tip]- Answer
> Navigation keys plus only the focused row's verb actions (`_build_footer`, `core/control_plane_view.py:412-432`). Rebuilding per render makes the footer a per-row capability display so operators never memorize verbs — see [[wiki/01-control-plane-cockpit|Cockpit]].

### Q4. How does `owt attach` find the right session without `--herdr/--tmux` flags, and what schema habit makes that possible?

> [!tip]- Answer
> Each status row records its owning backend (`backend_kind/session_id/meta`); `select_backend_for_session` reconstructs it (`core/backend_factory.py:120-142`). Backend ownership as durable per-row data — see [[wiki/02-multiplexer-backends|Backends]].

### Q5. How does Conflict Guard compute file overlap, and what are its two key limits?

> [!tip]- Answer
> `git diff --name-only {base}...{branch}` intersected with peers' last-reported `modified_files` from SQLite (`core/merge.py:183-213`). Limits: it reads reported (possibly stale/silent) file lists, not live peer diffs, and the warning is advisory-only — see [[wiki/04-merge-queue-conflict-guard|Merge/Guard]].

### Q6. What are the two phases of `MergeManager.merge`, and what happens on a phase-1 conflict?

> [!tip]- Answer
> Phase 1 merges/rebases base into the feature branch inside the worktree; phase 2 checks out base in the main checkout and merges the feature (`core/merge.py:328-574`). A phase-1 conflict aborts (`--abort` unless `--leave-conflicts`), raises `MergeConflictError`, and phase 2 is never attempted — see [[wiki/04-merge-queue-conflict-guard|Merge/Guard]].

### Q7. What determines `plan_merge_order`, and what explicitly does NOT influence it?

> [!tip]- Answer
> Only COMPLETED/WAITING rows, sorted smallest-first on `(commits_ahead, overlap_count)` unless an explicit DAG `dependency_order` is given (`core/merge.py:283-326`). Branch age and size play no role — see [[wiki/04-merge-queue-conflict-guard|Merge/Guard]].

### Q8. How can a team add a new AI CLI without changing owt code, and which capability flags control generic behavior?

> [!tip]- Answer
> Add a `[tools.<name>]` config table; `register_custom_tools()` builds a `CustomTool` before validation (`config.py:322-326`), with `{{task}}`/`{{worktree}}` argv substitution (`core/tool_registry.py:67-74`). Generic code branches on `supports_hooks/headless/plan_mode` (`core/tool_protocol.py:14-99`) — see [[wiki/03-harness-plugin-layer|Harness layer]].

### Q9. What are Quick Actions with `on_create`, and what does Agent Broadcast (`send --all/--working`) filter on?

> [!tip]- Answer
> `[[actions]]` entries (`config.py:147-158`) are named shell commands runnable via `owt run`, executed automatically after every `owt new` when `on_create = true` (`core/quick_actions.py:103-115`). Broadcast fans out via the recorded backend's `send_text`, with `--working` filtering to rows whose status is WORKING (`commands/agent.py:53-84`) — see [[wiki/05-cli-config-models|CLI/Config]].

### Q10. Why is `--workflow` not a workflow engine, and what is the strongest argument from [[critical_thinking]] for borrowing from owt anyway?

> [!tip]- Answer
> `--workflow` only prepends a classified planning preamble to the prompt; there is no DAG or scheduler — ordering is a ship-loop sort. Borrow anyway because owt's value is decision-surface UX and cheap shipping safety (lanes/verbs/footer, overlap warnings, two-phase merge), which compose with fleet's scheduler rather than competing with it — see [[wiki/targeted|Targeted]] and [[critical_thinking]].
