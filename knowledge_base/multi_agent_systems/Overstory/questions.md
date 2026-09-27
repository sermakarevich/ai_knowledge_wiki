---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Overstory — Retrieval Practice

Answer these from memory before re-reading anything.

## Questions

### 1. Trace what happens from a human objective arriving at the coordinator to code landing on the canonical branch — why is the pipeline split into coordinator → lead → leaf workers with a merge_ready gate in the middle?
> [!tip]- Answer
> The coordinator decomposes the objective into tracker issues and spawns only leads, each lead writes specs and spawns scout/builder/reviewer leaves in isolated worktrees, and nothing merges until the lead verifies commits, issue state, and exit code and sends typed merge_ready mail. The gate exists so builder completion alone authorizes nothing and the coordinator merges only on explicit lead signal, then closes the issue after merge success. This enforces hierarchy, isolates failures to branches, and makes cross-review rework possible before integration.

### 2. Why does Overstory generate a per-task overlay file instead of passing task instructions by mail, and why does writeOverlay() refuse to write when the worktree path equals the project root?
> [!tip]- Answer
> The overlay built by generateOverlay() combines role definition, file scope, branch, parent, depth, quality gates, and spec path into one startup file the agent reads, so state lives in files rather than ephemeral conversation and every worker boots identically. Scouts send only a one-line mail pointing at the spec file for the same reason. The root-write refusal with resolved-path comparison protects the operator's own session file from being overwritten, which matters when dogfooding Overstory on its own repo.

### 3. Why is all harness-specific logic hidden behind the AgentRuntime interface plus a central registry, and which files would you edit to add a new harness?
> [!tip]- Answer
> Orchestration code calls only AgentRuntime methods and never a harness CLI directly, so Claude, Pi, Codex, Copilot, Cursor, Gemini, OpenCode, and Sapling differ only as data in adapters while spawn, guards, readiness, transcripts, and env mapping stay uniform. To add a runtime you create src/runtimes/<name>.ts implementing the interface, register its factory in src/runtimes/registry.ts, add config types if needed, and test spawn plus deployConfig. AI-assisted internals like merge AI-resolve and watchdog triage reuse buildPrintCommand through the same abstraction.

### 4. Trace what happens when a builder sends an urgent worker_done mail to its lead — why are mail reads destructive and why are urgent nudges file-based instead of direct interruption?
> [!tip]- Answer
> The send inserts one row per recipient into the SQLite messages table plus a mail_sent event row, then writes a JSON marker to .overstory/pending-nudges/{agent}.json because priority is high or the type is in the auto-nudge set. The lead's next mail check --inject reads and clears the marker, prepends a priority banner, selects unread rows oldest-first, and immediately marks them read. Destructive check gives at-most-once delivery per check and file markers avoid interrupting a running TUI session, with only dispatch adding a delayed tmux sendKeys poke.

### 5. Trace what happens when two builder branches both modify the same file — why does Tier 2 auto-resolve keep the incoming side but refuse files where the canonical side has real content?
> [!tip]- Answer
> The FIFO merge queue takes the lowest-id pending entry and tries Tier 1 clean git merge, then Tier 2 regex-parses conflict markers keeping the ======= to >>>>>>> incoming hunk, concatenating both sides only for merge=union files. Refusing contentful canonical hunks prevents silent data loss by escalating to Tier 3 AI-resolve or Tier 4 reimagine instead of discarding shared work. Every outcome is recorded as a searchable pattern so tiers with 2+ failures and zero successes on overlapping files are skipped next time.

### 6. Why does the T0 watchdog escalate warn → nudge → AI triage → terminate instead of killing a stalled worker immediately, and how does ZFC health checking prevent false kills?
> [!tip]- Answer
> Progressive escalation gated by nudgeIntervalMs gives slow but healthy agents time to recover, with recovery resetting escalationLevel and stalledSince, while Level 2 triage reads the last 50 log lines and defaults to extend on missing logs or model failure. ZFC means observable tmux/PID liveness outranks recorded sessions.db state, so tmux-alive plus recorded-zombie yields investigate and hold rather than auto-kill. Coordinator and monitor capabilities are exempt from time-based stale detection because long idle waits are normal for them.

### 7. Why does each worker get its own directory plus its own overstory/{agent}/{task} branch, and which file would you edit to change cleanup so unmerged branches are preserved?
> [!tip]- Answer
> Separate directories remove filesystem contention on working-tree files and artifacts while separate branches parented on the same base prevent in-tree markers and clobbered uncommitted state, deferring convergence to the explicit merge pipeline. Cleanup policy lives in src/commands/worktree.ts and src/worktree/manager.ts: clean defaults to completed/zombie sessions, checks git merge-base --is-ancestor, and requires --force to destroy unmerged work with safe -d versus forced -D branch deletion. Failed spawns roll back both artifacts via forced worktree removal plus branch -D on a best-effort path.

### 8. Why does ov sling run a 14-step pipeline with depth, hierarchy, concurrency, and per-task locks instead of just spawning the agent, and how does the tracker backend stay swappable underneath it?
> [!tip]- Answer
> The pipeline validates depth against maxDepth 2, enforces coordinator-spawns-only-leads hierarchy, checks manifest capability, run-id inheritance, maxConcurrent and per-lead ceilings, name uniqueness, and one-agent-per-task locks before creating the worktree, overlay, dispatch mail, claim, identity, and tmux or headless spawn. Sling resolves the tracker via resolveBackend probing .seeds/ then .beads/ and uses only the 7-method TrackerClient contract, with trackerCliName injected into the overlay as sd or bd. This keeps beads envelope differences and seeds JSON-array differences behind adapters.

### 9. Why is worker restart state kept in checkpoint.json plus handoffs.json files rather than conversation history, and trace what happens when a session compacts or crashes?
> [!tip]- Answer
> The three-layer model treats the session as ephemeral but the worktree sandbox and identity record as persistent, so a JSON snapshot with progress, modified files, branch, pending work, and expertise domains survives compaction, crash, or timeout. initiateHandoff saves the checkpoint and appends a pending record with toSessionId null, resumeFromHandoff picks the newest pending record, and completeHandoff stamps the new session id and clears the checkpoint. Recovery via ov prime --compact renders that checkpoint as a session-recovery section plus overlay, group status, mail, and expertise reload.

### 10. Why does cost accounting use transcript parsing plus substring-matched pricing and append-only snapshots, and which files would you edit to add a new model price?
> [!tip]- Answer
> Each runtime parses its own transcript format into normalized input/output/cache-read/cache-create tokens, the runtime-agnostic pricing table in src/metrics/pricing.ts applies per-million-token rates by lowercase substring match with order-sensitive rules, and the SQLite metrics store appends token_snapshots with a latest-per-agent view for live burn-rate joins. To add a model you edit the pricing table and match order in src/metrics/pricing.ts so estimateCost picks it up for ov costs and ov metrics. Sessions keyed by agent plus task carry the aggregated tokens, cost, duration, and merge result for capability-grouped reporting.
```
