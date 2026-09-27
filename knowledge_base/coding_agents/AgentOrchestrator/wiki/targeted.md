> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agent Orchestrator — Targeted Analysis for Fleet

**In one sentence:** AO is a local-first, single-control-surface fleet runner where one orchestrator session fans out to isolated-worktree worker sessions with one-PR-per-agent ownership and daemon-driven CI/review/merge lifecycle.

## Key points

- Design centers on durable facts in SQLite with status derived at read time, thin clients, loopback-only daemon, and explicit human merge.
- Worker restart = desktop restarts daemon, `ao session restore` reuses the same session + worktree when the adapter supports recovery; failed probes never equal death.
- Conflict safety comes from git worktree isolation + one pull request per session + observed mergeability, with the eligible session asked to rebase and resolve.
- There is no user-facing workflow DSL (Domain-Specific Language — a mini-language for one job); the "abstraction" is session roles + typed project config + built-in lifecycle reactions, after the legacy YAML reactions schema was retired.
- Multi-harness support = 27 compiled-in terminal adapters reusing the user's own CLIs/auth, with 4 Chat-capable harnesses behind capability gates (codex app-server, claude-code via claude-agent-ACP, opencode + droid via native ACP).
- Fleet can borrow at least 7 concrete ideas: derived status, dirty-worktree protection, signature-deduplicated nudges, mode-aware delivery, per-role default agents, claim-PR fallback, and append-only migrations with CDC events.

---

## 1. Design principles

AO's architecture page makes its principles unusually explicit — eight "load-bearing rules" plus structural choices:

1. **Durable facts, derived status.** Store agent activity (active/idle/waiting/blocked/exited), termination, interface mode, controller handle/generation, transition checkpoints, and pull request + check + review facts. Compute display labels (working, needs input, CI failed, ready to merge) when a client reads. Rationale: stored status always drifts from reality under failures; derivation cannot drift.
2. **Observations are not verdicts.** A failed or unknown runtime probe is recorded as an observation, never as proof the session died. The operator reopens the session and looks before killing it.
3. **Conservative workspace handling.** Cleanup refuses to force-delete a dirty registered worktree. `ao session kill` preserves dirty workspaces; `ao session cleanup [--dry-run]` reclaims only eligible terminated ones.
4. **Local-first, single-user, thin clients.** Go daemon owns all domain logic; Electron/React desktop, `ao` CLI, and Expo mobile are thin HTTP/SSE/mux clients. The CLI never opens SQLite or launches adapters. All state lives under `~/.ao` (`AO_DATA_DIR` / `AO_RUN_FILE` overrides exist but are advanced-only).
5. **Loopback by default, explicit opt-in for network.** Primary listener is unauthenticated `127.0.0.1:3001` and can never be bound publicly. Phone access uses a second, explicitly enabled, bearer-password LAN listener (plaintext, trusted-home-network only) that excludes shutdown/telemetry/browser-control routes.
6. **Event sourcing lite.** SQLite triggers append to `change_log`; a CDC poller broadcasts invalidations over `GET /api/v1/events` with `Last-Event-ID` replay, so clients invalidate targeted queries instead of refetching everything.
7. **Built-in over configurable automation.** Lifecycle reactions are daemon-owned and deliberately not user-scriptable in the current rewrite (see §4).
8. **Append-only evolution.** New migrations only; never modify a merged migration.

The product loop this serves is: `add project → start session → isolated worktree → pull request → CI/review → merge → cleanup`, with every session visible on one kanban board (Pending / Iterating / In Review / Ready to merge / Archive) carrying agent, branch, and PR state on the card.

## 2. Worker restart handling

AO separates three restart layers:

- **Daemon restart.** The desktop app discovers, launches, and supervises the daemon. Recovery step #1 in troubleshooting is "quit and reopen the desktop app" — it restarts the daemon and reconnects SSE + terminal streams. `ao status` / `ao doctor` diagnose daemon, config, data dir, database, Git, and tmux/conpty runtime health.
- **Session restore.** `ao session restore <id>` (or the desktop restore action) relaunches a terminated session, reusing the same AO session record and the same worktree whenever the selected adapter supports recovery. Preconditions: the harness CLI must still be installed and authenticated.
- **Interface handoff (Chat ↔ TUI).** Compatible Claude Code and Codex sessions can move the same provider conversation between structured Chat and native terminal UI without changing session or worktree. AO drains or interrupts the old controller before committing the replacement (generation counter + checkpoints + queued messages), so two controllers are never live at once.
- **Stuck/blocked sessions.** If a session is blocked on an approval or permission prompt, AO deliberately withholds lifecycle messages until a human answers — automation never talks over a permission gate. SSE reconnection plus app restart heals stale UI after daemon restarts.

What is notably absent: no documented retry budget, backoff schedule, or checkpoint-resume of in-flight tool calls — durability is at the session/worktree/conversation level, not the individual agent-step level.

## 3. Conflict resolution — worktree isolation, one-PR-per-agent, merge flow

**Worktree isolation (the primary mechanism).** Each worker session in a Git project owns a fresh git worktree + branch (multi-repo workspace projects materialize a root worktree plus registered child worktrees; Scratch sessions use an AO-managed directory with no branch/PR operations). Workers never share a checkout, so two agents cannot overwrite each other's files. Testimonial language reinforces the mental model: "thinking of the agents' work as separate git worktrees kept my mind at peace — the decision is with me, whether I want to merge the branch or not."

**One-PR-per-agent (ownership).** Each session claims exactly one pull request: either the agent opens it and AO links it, or a human attaches an existing one (`ao session claim-pr <session> <pr>`; `--no-takeover` refuses PRs already owned by another active session; `AO_SESSION_ID` supplies worker context). All downstream facts — checks, review comments, mergeability — are attributed to that owner, and all nudges go to that owner's session.

**Merge flow (observed, human-gated).**

1. The GitHub SCM observer polls (lazy auth, ETag guards, semantic diffing, rate-limit respect) and writes PR facts to SQLite.
2. Lifecycle logic reacts: failing checks → send check names + links to the owner; changes-requested/unresolved comments → send focused feedback; merge conflict → ask the eligible session to rebase and resolve; ready-to-merge → durable in-app notification (+ Electron toast); merged/closed → update facts, create/resolve notifications.
3. Messages are signature-deduplicated: an unchanged failure set is not re-sent every poll; a changed set produces a fresh nudge.
4. Reviewer agents are a second, distinct loop: `ao review trigger/ls/cancel/submit` runs a configured reviewer against the worker PR; findings are inspectable before the send-to-worker step.
5. Merge itself is always explicit: desktop merge button or `ao pr merge <n>` through AO's GitHub action engine, plus `ao pr resolve-comments`. There is no auto-merge config — the retired `auto-merge` YAML key is rejected by typed project config.

Net effect: conflicts are prevented by isolation, detected by observation, and resolved by routing — never by concurrent writes to one tree.

## 4. Workflow abstraction — how implemented

There is **no user-facing workflow DSL** in current AO. The retired implementation had a `reactions:` schema (`retries`, `escalateAfter`, `auto-merge`, notifier routing in `agent-orchestrator.yaml`); the Go rewrite removed it — `ao import` reports those legacy fields as dropped, and typed project config rejects unknown fields.

What replaces it is a three-part implicit abstraction:

- **Session roles.** `ao spawn --kind worker|orchestrator` plus per-project `--worker-agent` / `--orchestrator-agent` defaults. The orchestrator pattern (one planning session delegating to worker sessions, per-role harness/model choice) is documented in guides (`per-role-agents`, `parallel-issues`, `multi-project`) rather than encoded in YAML.
- **Typed project configuration.** Base branch, session prefix, env vars, symlinks, setup commands, worker/orchestrator agents, model, permission mode, prompt rules, reviewer agents, tracker intake, container cleanup — set via desktop settings or `ao project set-config` (`--config-json` for scripts). This is environment + defaults, not control flow.
- **Built-in lifecycle reactions** (the table in §3) with mode-aware delivery: TUI sessions receive nudges through their tmux/conpty runtime; Chat sessions receive a native provider turn persisted in the structured conversation. `ao preview`/`.ao/launch.json` (one managed dev-server command per session) and `ao browser` (session-isolated browser control) extend the session model to verification, not orchestration.

In short: AO implements "workflow" as **session topology + observed PR state machine + daemon reactions**, not as user-authored DAGs (Directed Acyclic Graphs — workflows drawn as boxes and arrows).

## 5. Multi-harness support — how implemented

**Catalog.** The daemon registry advertises 27 worker harnesses: `claude-code, codex, opencode, grok, cursor, qwen, copilot, kimi, muse, droid, amp, agy, crush, aider, goose, auggie, continue, devin, cline, kiro, kilocode, vibe, pi, kimchi, prime-agent, autohand, omp`. The landing page claims "25 supported" with per-project agent choice; docs say 27 — the CLI is authoritative: `ao agent ls --refresh [--json]`.

**Mechanism.** Adapters are compiled into the Go binary behind port interfaces — there is no plugin marketplace and no `ao plugin install`. AO reuses the user's locally installed agent CLI and its existing authentication (daemon inherits a login-shell env); it bundles neither provider CLIs nor credentials. Readiness probes report supported/installed/authenticated; spawn runs an advisory CLI-side preflight (skippable with `--skip-agent-check`) plus authoritative daemon validation.

**Chat vs Terminal UI gating.** All 27 harnesses run through their native terminal interface via the platform runtime (tmux on macOS/Linux, ConPTY on Windows). Four additionally have structured Chat drivers with durable provider-identified conversations (turns, activities, approvals, usage, compaction, rollback): `codex` (native app-server), `claude-code` (`claude-agent-acp` over the user's Claude executable), `opencode` + `droid` (native ACP). Every other harness is TUI-only. Initial interface is chosen at spawn (`--mode chat|tui` or project default); only compatible Claude Code/Codex sessions support later switching.

**Selection precedence.** Explicit `ao spawn --agent|--harness <name>` (aliases) → project worker/orchestrator defaults → typed config model/permission/env/rules. Related: `ao session switch-agent <id> <target>` for compatible sessions, `ao session agent-switch ls` for attempt history.

## 6. What fleet can borrow — 7 concrete ideas

1. **Derived status from durable facts (rule #1).** Fleet's supervisor should store activity/termination/PR/check facts and compute worker labels at read time instead of persisting a status string that drifts. Cheap to adopt; kills a whole class of stale-board bugs.
2. **Never force-delete dirty worktrees.** Make `kill` preserve dirty trees and add a `cleanup --dry-run` that lists reclaimable terminated sessions first. This is the single cheapest trust win with agent fleets.
3. **Signature-deduplicated lifecycle nudges.** Hash the failure/comment set and only re-nudge on change. Prevents CI-flap spam while keeping the "right agent fixes its own CI" loop — directly applicable to fleet's beads/CI watcher.
4. **Mode-aware delivery through one session manager.** Route follow-ups through the same path regardless of harness (fleet equivalent: bead comment → owning worker's channel), and suppress automation while a worker is blocked on an approval prompt.
5. **Per-role default agents.** Separate orchestrator/planner defaults from worker defaults in typed project config (e.g. strong model plans, cheap model executes). Fleet's `coder --model` per-task selection is the same idea; make it a stored default, not a CLI flag each time.
6. **Claim-PR fallback + takeover guard.** When auto-linking misses (agent opened a PR outside the harness flow), let the worker claim it from inside (`AO_SESSION_ID`-style context) and refuse takeovers of PRs owned by live sessions unless forced. Closes the "orphan PR" gap.
7. **Append-only migrations + CDC event log with replay.** SQLite triggers → `change_log` → SSE with `Last-Event-ID` is a small, proven pattern for fleet's beads DB: every state change becomes a replayable event, and thin clients invalidate instead of refetching.

**Honest limits to note before borrowing:** tracker integration beyond GitHub is incomplete; there is no auto-merge (deliberate); restart is session-level, not step-level; and the "orchestrator talks to other orchestrators" testimonial claim has no corresponding documented protocol — treat it as anecdote, not architecture.
