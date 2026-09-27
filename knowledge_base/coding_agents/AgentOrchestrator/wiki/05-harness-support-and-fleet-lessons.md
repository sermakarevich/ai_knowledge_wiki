> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Harness Support and Fleet Lessons

**In one sentence:** Twenty-seven agent harnesses ship compiled into the binary and reuse the user's own CLIs and auth — only four unlock structured Chat behind capability gates — and the orchestrator-plus-workers session topology with per-role defaults yields seven concrete ideas fleet can borrow.

## Key points

- Twenty-seven worker harnesses are compiled into the Go binary behind port interfaces — there is no plugin marketplace and no `ao plugin install`.
- AO bundles neither provider CLIs nor credentials: it reuses the user's locally installed agent CLIs and existing auth (the daemon inherits a login-shell environment).
- Only four harnesses unlock structured Chat (codex via app-server, claude-code via claude-agent-ACP, opencode + droid via native ACP); the other twenty-three are TUI-only through tmux/ConPTY.
- `ao agent ls --refresh` is the source of truth for harness install/auth readiness; spawn runs an advisory CLI-side preflight (skippable) plus authoritative daemon validation.
- Session roles replace a workflow DSL: `ao spawn --kind worker|orchestrator` with per-project worker/orchestrator agent defaults (e.g. strong planner, cheap executors) documented in guides, not encoded in YAML.
- Fleet can borrow seven concrete ideas: derived status, dirty-worktree protection, signature-deduplicated nudges, mode-aware delivery, per-role default agents, claim-PR fallback, and append-only migrations with CDC events.
- Honest limits bound the borrowing: tracker integration beyond GitHub is incomplete, there is no auto-merge by design, restart is session-level not step-level, and orchestrator-to-orchestrator talk is anecdote, not protocol.

---

## 1. The harness catalog

The daemon registry advertises 27 worker harnesses: `claude-code, codex, opencode, grok, cursor, qwen, copilot, kimi, muse, droid, amp, agy, crush, aider, goose, auggie, continue, devin, cline, kiro, kilocode, vibe, pi, kimchi, prime-agent, autohand, omp`. (The landing page says "25 supported"; treat the CLI as authoritative.) Selection precedence: explicit `ao spawn --agent|--harness <name>` → project worker/orchestrator defaults → typed config model/permission/env/rules. Related: `ao session switch-agent <id> <target>` for compatible sessions.

## 2. How adapters work

Adapters are compiled into the Go binary behind port interfaces. There is no plugin marketplace, no third-party extension point, no `ao plugin install`. AO reuses the user's own installed agent CLI and its existing authentication — the daemon inherits a login-shell environment — so onboarding is "install your agents normally, then point AO at them". Readiness probes report supported / installed / authenticated per harness; `ao spawn` runs an advisory CLI-side preflight (skippable with `--skip-agent-check`) plus authoritative daemon-side validation that can still refuse the spawn.

## 3. Chat vs Terminal-UI gating

All 27 harnesses run through their native terminal interface via the platform runtime (tmux on macOS/Linux, ConPTY on Windows). Four additionally have structured Chat drivers with durable provider-identified conversations (turns, activities, approvals, usage, compaction, rollback):

| Harness | Chat mechanism |
|---|---|
| codex | native app-server |
| claude-code | `claude-agent-ACP` over the user's Claude executable |
| opencode, droid | native ACP (Agent Client Protocol — a standard way for apps to talk to coding agents) |

Every other harness is TUI-only. The initial interface is chosen at spawn (`--mode chat|tui` or the project default); only compatible Claude Code / Codex sessions support later Chat ↔ TUI switching with drained handoffs.

## 4. Session roles instead of a workflow DSL

There is no user-facing workflow language in current AO. The composition primitive is session topology:

- `ao spawn --kind worker|orchestrator` creates workers or orchestrators with separate default harnesses (`--worker-agent` / `--orchestrator-agent` per project).
- The documented pattern — one planning orchestrator session delegating to worker sessions, per-role harness/model choice — lives in guides (`per-role-agents`, `parallel-issues`, `multi-project`), not in YAML.
- Typed project config covers environment + defaults (base branch, session prefix, env vars, symlinks, setup commands, model, permission mode, prompt rules, reviewer agents, tracker intake, container cleanup) via desktop settings or `ao project set-config`. This is environment, not control flow.
- `ao preview` / `.ao/launch.json` (one managed dev-server command per session) and `ao browser` (session-isolated browser control) extend the session model to verification, not orchestration.

In short: workflow = session topology + observed PR state machine + daemon reactions, not user-authored DAGs (Directed Acyclic Graphs — workflows drawn as boxes and arrows).

## 5. Seven ideas fleet can borrow

1. **Derived status from durable facts.** Store activity/termination/PR/check facts and compute worker labels at read time instead of persisting a status string that drifts.
2. **Never force-delete dirty worktrees.** Make kill preserve dirty trees; add `cleanup --dry-run` that lists reclaimable terminated sessions first. Cheapest trust win available.
3. **Signature-deduplicated lifecycle nudges.** Hash the failure/comment set; re-nudge only on change. Prevents CI-flap spam while keeping the "right agent fixes its own CI" loop.
4. **Mode-aware delivery through one session manager.** Route follow-ups through the same path regardless of harness (fleet equivalent: bead comment → owning worker's channel); suppress automation while a worker is blocked on approval.
5. **Per-role default agents.** Separate orchestrator/planner defaults from worker defaults in typed config (strong model plans, cheap model executes) — a stored default, not a CLI flag each time.
6. **Claim-PR fallback + takeover guard.** When auto-linking misses, let the worker claim the PR from inside (session-ID context) and refuse takeovers of PRs owned by live sessions unless forced.
7. **Append-only migrations + CDC event log with replay.** SQLite triggers → `change_log` → SSE with `Last-Event-ID`: every state change becomes a replayable event; thin clients invalidate instead of refetching.

## 6. Honest limits before borrowing

- Tracker integration beyond GitHub issues is incomplete; do not plan workflows assuming every tracker participates in lifecycle automation.
- There is no auto-merge, deliberately — merge stays human-gated.
- Restart is session-level, not step-level: no retry budget, backoff schedule, or checkpoint-resume of in-flight tool calls is documented.
- The "orchestrator talks to other orchestrators" testimonial has no corresponding documented protocol — treat it as anecdote, not architecture.
- Docs say 25 harnesses on the landing page vs 27 in the registry — trust `ao agent ls --refresh`.

**Covers:** docs agents page (catalog, adapters, Chat gating, selection), CLI agent/spawn/switch-agent commands, guides on per-role agents, orchestrator spawn kind, fleet-borrowable ideas + limits (targeted §5–§6).
