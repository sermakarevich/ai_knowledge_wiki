# Source copy — Agent Orchestrator (useao.dev)

**Title:** Agent Orchestrator (AO) — Run Coding Agents in Parallel
**URL:** https://useao.dev (+ /docs/, /docs/architecture/, /docs/plugins/, /docs/plugins/agents/, /docs/plugins/workspaces/, /docs/cli/, /docs/configuration/, /docs/configuration/lifecycle-automation/, /docs/troubleshooting/, /docs/guides/)
**Publisher:** Untrivial-ai (GitHub: Untrivial-ai/agent-orchestrator; 11.2k stars at retrieval)
**Retrieved:** 2026-09-09
**Track:** Content track — Article / docs site (single source per session)

## Provenance

Public product landing page + documentation, fetched with WebFetch (no JavaScript (JS — the scripting language that makes web pages interactive) fallback needed; pages returned full content). Docs describe the current Go (a programming language by Google) daemon rewrite; legacy TypeScript (a typed version of JavaScript) `agent-orchestrator.yaml` plugin schema is retired.

## Saved content (abridged extraction)

### Landing (https://useao.dev)
- Tagline: "Stop babysitting agents. Start merging real work." Fleet of coding agents; branches, reviews, CI (Continuous Integration — automatic checks that run on every code change) failures kept manageable.
- Board columns: Pending Work / Iterating / In Review / Ready to merge / Archive. Cards show agent icon, task, branch, live activity ("Editing file 3m ago"), PR (Pull Request — a proposal to merge code) number, check counts ("8/44 passed"), comments, merge action.
- Delegation: each project gets a main orchestrator agent; it plans work, spawns workers into own worktrees, escalates only what needs a human.
- Feedback loop: AO watches every PR it opens; failed checks + review comments route back to owning session until approved.
- Coverage: 25–27 harnesses supported with per-project agent choice (Claude Code, Codex, Cursor, OpenCode, Aider, Goose, Droid, Copilot, Qwen, Grok, Crush, Kimi, Kilo Code, Cline, Amp, Devin, etc.). Install: `brew install agentwrapper/tap/agent-orchestrator`.
- Mobile companion over LAN (Local Area Network — home/office network) or Tailscale; watch sessions, terminal, notifications; code stays on desktop machine.
- Testimonials: context carried across spawned workers; orchestrators communicating with other orchestrators; work seen as separate git worktrees so merge stays a human decision; CI (Continuous Integration) failures auto-routed to right agent; 2–3 PRs/day → 5+ PRs/day.

### Docs intro (/docs/)
- AO = desktop IDE (Integrated Development Environment — an app for writing and managing code) for supervising AI (Artificial Intelligence) coding agents. Workers get isolated workspaces; Git work connects to PRs, CI, reviews, merge conflicts.
- Basic loop: `add project -> start session -> isolated worktree -> pull request -> CI/review -> merge -> cleanup`.
- Chat vs Terminal UI (TUI — the agent's own text screen inside a terminal): Chat = structured messages/approvals/plans/usage; TUI = harness native terminal. Chat available for Codex, Claude Code, OpenCode, Droid; Claude Code + Codex can switch Chat↔TUI without changing session/worktree.
- Local by design: Go daemon on 127.0.0.1 (loopback — an address meaning "this same computer"); state under `~/.ao`; reuses user's own agent CLIs (Command-Line Interfaces) + auth; GitHub is the shipped source-control observation path.

### Architecture (/docs/architecture/)
- Local single-user system: Electron (a framework for desktop apps built with web tech)/React (a UI (User Interface) library) desktop + optional CLI (thin HTTP (the web protocol) client) + Expo mobile → Go daemon → services/managers → SQLite (a small file-based database). SSE (Server-Sent Events — one-way live updates from server) events, terminal mux (multiplexer — shares terminal sessions), browser bridge.
- Sessions & worktrees: Git projects → isolated worktrees; workspace projects → root + child worktrees; Scratch → AO-managed dir. One agent interface at a time (tmux — a terminal session keeper — on macOS/Linux, conpty on Windows; or runtime-less Chat controller). TUI↔Chat handoff drains/interrupts old controller first.
- Durable facts, derived status: store activity/termination/interface/PR-check-review facts; compute labels (working, needs input, CI failed, ready to merge) at read time. Failed probes are observations, not proof of death. Never force-delete dirty worktree.
- Storage: SQLite under `~/.ao/data`; triggers → change_log → CDC (Change Data Capture — reading the log of what changed) poller → SSE with Last-Event-ID replay.
- Adapters: 20+ agent harnesses, tmux/conpty runtimes, git-worktree isolation, Chat drivers, GitHub SCM (Source Control Management — the system tracking code versions) observer (lazy auth, ETag guards, semantic diffing). Broader tracker lane incomplete.
- PR + lifecycle: CI fail / changes-requested / merge conflict → notify lifecycle; daemon exposes merge + comment-resolve actions + reviewer-agent routes.
- Load-bearing rules (8): derive don't store status; probes ≠ death; never force-delete dirty worktrees; state under ~/.ao; loopback-only primary listener; thin CLI/UI; CDC events via triggers; append-only migrations.

### Built-in capabilities (/docs/plugins/) + agents (/docs/plugins/agents/)
- Compiled-in adapters, no marketplace: 27 worker harnesses; 4 with Chat drivers (codex via app-server; claude-code via claude-agent-ACP (Agent Client Protocol — a standard way for apps to talk to coding agents); opencode + droid via native ACP (Agent Client Protocol)); rest TUI-only.
- Runtimes: tmux (macOS/Linux), ConPTY (Windows), automatic. Workspaces: git worktrees / Scratch dirs, automatic. Trackers: GitHub issue intake (opt-in). SCM: GitHub PR/checks/reviews/mergeability. Notifications: durable in-app + Electron toasts. Terminal: xterm over mux.
- Selection: `ao agent ls --refresh`; `ao spawn --agent <name>`; project worker/orchestrator defaults in typed config. Legacy YAML blocks inactive.

### CLI (/docs/cli/) + configuration (/docs/configuration/)
- Thin client; needs desktop app running. Commands: start/stop/status/doctor; agent ls; project add/ls/get/set-config/rm; spawn (--name, --project, --agent/--harness, --kind worker|orchestrator, --mode chat|tui, --branch, --prompt, --issue, --claim-pr, --no-takeover); session ls/get/kill/restore/rename/cleanup/claim-pr/switch-agent; send; orchestrator ls; pr merge/resolve-comments; review ls/trigger/cancel/submit; preview/browser; import; completion; version.
- Env (Environment variables — named settings outside the program): AO_PORT=3001, AO_RUN_FILE, AO_DATA_DIR, AO_REQUEST_TIMEOUT, AO_SHUTDOWN_TIMEOUT, AO_SESSION_ID, AO_PROJECT_ID. Typed project config: base branch, session prefix, env vars, symlinks, setup commands, worker/orchestrator agents, model, permission mode, rules, reviewer agents, tracker intake, container cleanup.

### Lifecycle automation (/docs/configuration/lifecycle-automation/)
- Built-in, NOT user-configurable reactions schema (retries/escalateAfter/auto-merge YAML retired).
- Table: failing CI → send names+links to owning session; changes-requested/unresolved comments → focused feedback to owner; merge conflict → ask eligible session to rebase+resolve; PR ready → durable notification; merged/closed → update facts; needs-input → human notification. Signature-deduplicated messages. Mode-aware delivery (TUI runtime vs Chat turn). No Slack/Discord/webhook config. Merge explicit: desktop or `ao pr merge`.

### Workspaces (/docs/plugins/workspaces/) + troubleshooting (/docs/troubleshooting/)
- Git repo → fresh worktree + branch; multi-repo workspace → root + children; Scratch → managed dir, no branch/PR. Cleanup conservative: kill preserves dirty worktree; `ao session cleanup --dry-run`.
- Recovery: reopen desktop (restarts daemon); `ao status/doctor`; restore reuses session+worktree when adapter supports recovery; blocked = answer approval prompt (AO won't inject lifecycle msgs while blocked); claim PR via `ao session claim-pr`; SCM polls with rate-limit/ETag respect.
