> [[index|Wiki]] | [[summary|Summary]]

# Agent Orchestrator (AO) — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-worktree-isolation|Worktree Isolation]]

**In one sentence:** Every AO worker session gets its own isolated git worktree plus branch (or a managed Scratch directory), so parallel agents never share a checkout and conflicts are prevented by construction rather than resolved after the fact.

- Each worker session in a Git project owns a fresh git worktree + branch, so two agents can never overwrite each other's files.
- Multi-repo workspace projects materialize one root worktree plus registered child worktrees, keeping cross-repo tasks isolated as a unit.
- Scratch sessions use an AO-managed directory with no branch or PR operations, for work that is not yet tied to a repository.
- Cleanup is conservative by design: `ao session kill` never force-deletes a dirty registered worktree, and `ao session cleanup --dry-run` previews reclaimable sessions first.
- Restart reuses the same record and the same worktree: `ao session restore` relaunches a terminated session in place whenever the adapter supports recovery.
- The mental model is explicit in testimonials: agents' work lives in separate worktrees, so the human always keeps the merge decision.
- Only one agent interface is live per session at a time (tmux/conpty terminal or runtime-less Chat controller), with drained handoffs between them.

## 2. [[wiki/02-one-pr-per-agent-flow|One PR per Agent]]

**In one sentence:** Each AO session claims exactly one GitHub pull request, and every downstream fact — checks, review comments, mergeability — is attributed to that owner and routed back to that owner's session until the human merges.

- Each session claims exactly one pull request: either the agent opens it and AO links it, or a human attaches an existing one with `ao session claim-pr <session> <pr>`.
- A takeover guard (`--no-takeover`) refuses PRs already owned by another active session, so two agents can never own the same PR.
- From inside a worker, `AO_SESSION_ID` supplies session context so the agent's own PR open can be auto-linked to the right owner.
- The GitHub SCM observer polls with lazy auth, ETag guards, semantic diffing, and rate-limit respect, then writes PR/check/review facts into SQLite.
- All lifecycle nudges route to the owning session only: failing checks, changes-requested reviews, and merge conflicts each have a defined owner-directed reaction.
- Merge is always explicit and human-gated: desktop merge button or `ao pr merge <n>`; the retired `auto-merge` YAML key is rejected by typed project config.
- Reviewer agents run as a second, separate loop (`ao review trigger/ls/cancel/submit`) whose findings are inspectable before anything is delivered to the worker.

## 3. [[wiki/03-control-surface|Control Surface]]

**In one sentence:** One local Go daemon on loopback owns all state in SQLite and all domain logic, while the Electron desktop, thin CLI, and opt-in mobile clients stay thin; status is never stored but derived at read time, and every change flows to clients as replayable CDC events.

- One Go daemon owns durable state in SQLite plus all domain logic; the Electron/React desktop, `ao` CLI, and Expo mobile clients are thin HTTP/SSE/mux clients.
- The CLI never touches the database and never launches adapters — it is a pure HTTP client that requires the desktop app (and its supervised daemon) to be running.
- Status is never stored: the daemon persists activity, termination, controller generation, and PR/check/review facts, then computes labels (working, needs input, CI failed, ready to merge) on read.
- Storage lives under `~/.ao` (`AO_DATA_DIR` / `AO_RUN_FILE` overrides are advanced-only); SQLite triggers append to `change_log` and a CDC poller broadcasts over SSE with `Last-Event-ID` replay.
- The primary listener is unauthenticated `127.0.0.1:3001` and can never be bound publicly; phone access is a second opt-in plaintext LAN listener with a bearer password, trusted-home-network only.
- The desktop supervises the daemon (discover, launch, restart); `ao status` and `ao doctor --json` diagnose daemon, config, data dir, database, Git, and tmux/conpty health.
- Schema evolution is append-only: new migrations only, never modify a merged migration.

## 4. [[wiki/04-ci-review-feedback-routing|CI, Review, and Feedback Routing]]

**In one sentence:** A daemon-owned GitHub observer records CI, review, and mergeability facts into SQLite, and a built-in lifecycle engine routes signature-deduplicated, mode-aware nudges to the owning session while a separate reviewer-agent loop keeps machine review advisory and human-triaged.

- The SCM observer polls GitHub with lazy auth, ETag guards, semantic diffing, and rate-limit respect, then writes PR, check, review, and mergeability facts — never display strings — into SQLite.
- Every observed fact is attributed to the PR's owning session: failing checks, changes-requested reviews, and merge conflicts each trigger a defined owner-directed reaction.
- Lifecycle messages are signature-deduplicated: an unchanged failure set is never re-sent; only a changed set produces a fresh nudge, which prevents CI-flap spam.
- Delivery is mode-aware: TUI sessions get nudges through their tmux/conpty runtime, Chat sessions get a native provider turn persisted in the structured conversation.
- While a session is blocked on an approval or permission prompt, lifecycle messages are deliberately withheld — automation never talks over a permission gate.
- Reviewer agents run as a second, separate loop (`ao review trigger/ls/cancel/submit`) whose findings are inspectable before anything is delivered to the worker.
- Merge is always explicit and human-gated (desktop button or `ao pr merge`); the legacy `auto-merge` YAML key was retired and is rejected by typed project config.

## 5. [[wiki/05-harness-support-and-fleet-lessons|Harness Support and Fleet Lessons]]

**In one sentence:** Twenty-seven agent harnesses ship compiled into the binary and reuse the user's own CLIs and auth — only four unlock structured Chat behind capability gates — and the orchestrator-plus-workers session topology with per-role defaults yields seven concrete ideas fleet can borrow.

- Twenty-seven worker harnesses are compiled into the Go binary behind port interfaces — there is no plugin marketplace and no `ao plugin install`.
- AO bundles neither provider CLIs nor credentials: it reuses the user's locally installed agent CLIs and existing auth (the daemon inherits a login-shell environment).
- Only four harnesses unlock structured Chat (codex via app-server, claude-code via claude-agent-ACP, opencode + droid via native ACP); the other twenty-three are TUI-only through tmux/ConPTY.
- `ao agent ls --refresh` is the source of truth for harness install/auth readiness; spawn runs an advisory CLI-side preflight (skippable) plus authoritative daemon validation.
- Session roles replace a workflow DSL: `ao spawn --kind worker|orchestrator` with per-project worker/orchestrator agent defaults (e.g. strong planner, cheap executors) documented in guides, not encoded in YAML.
- Fleet can borrow seven concrete ideas: derived status, dirty-worktree protection, signature-deduplicated nudges, mode-aware delivery, per-role default agents, claim-PR fallback, and append-only migrations with CDC events.
- Honest limits bound the borrowing: tracker integration beyond GitHub is incomplete, there is no auto-merge by design, restart is session-level not step-level, and orchestrator-to-orchestrator talk is anecdote, not protocol.

## The argument in five moves

1. Give every agent its own isolated worktree + branch, so parallel work cannot collide by construction.
2. Bind each session to exactly one PR, so every downstream fact has exactly one owner.
3. Observe GitHub centrally and store facts (never status) in one daemon-owned SQLite database.
4. Route deduplicated, mode-aware nudges back to the owner automatically — but keep merge human-gated.
5. Support every harness through compiled-in adapters with per-role defaults, and let the topology (not a YAML DSL) be the workflow.
