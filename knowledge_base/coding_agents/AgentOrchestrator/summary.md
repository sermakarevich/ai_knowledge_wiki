# Agent Orchestrator (AO) — Run Coding Agents in Parallel

**Article:** [Agent Orchestrator](https://useao.dev) — useao.dev docs, retrieved 2026-09-09
**Source copy:** [[source/article]]

## Human Readable TL;DR

Imagine hiring ten builders to renovate ten rooms of your house at the same time. Normally that is chaos: they bump into each other, paint over each other's work, and you spend all day answering questions. Agent Orchestrator is like a foreman with a clipboard: each builder gets their own locked room (a separate copy of the code), their own to-do card on one big board, and a rule that nothing is finished until the inspector (automatic tests and code review) signs off. You only step in when the foreman raises a flag — everything else flows from task to finished paperwork on its own.

## TL;DR

Agent Orchestrator (AO, Untrivial-ai, 11.2k GitHub stars) is a local-first desktop control plane for running fleets of AI coding agents: one Go daemon on loopback owns durable state in SQLite, while Electron/React desktop, thin CLI, and opt-in mobile clients stay thin. Each worker session gets an isolated git worktree + branch, exactly one agent interface (native terminal UI or structured Chat), and one pull request whose CI/review/mergeability facts are observed from GitHub and routed back to the owning session. Status is never stored — it is derived at read time from durable facts — and lifecycle automation (CI-failure nudges, review feedback delivery, conflict rebase requests, reviewer agents) is built in rather than user-scripted. Twenty-seven agent harnesses are compiled in (four with Chat drivers); the runtime, workspace, tracker, and SCM layers are daemon-owned, not a plugin marketplace.

---

## Problem & Motivation

Running several coding agents in one checkout creates exactly the failure modes fleet knows: mixed files and branches, lost track of who does what, CI failures nobody owns, review comments landing in the wrong conversation, and merge conflicts discovered late. AO's answer is a single control surface that gives every agent an isolated workspace, one PR per session, and a durable event + observation loop so the human merges instead of babysits. The motivation is throughput with safety: testimonials cite 2–3 PRs/day rising to 5+ PRs/day, and autonomous CI/review recovery.

---

## Main Original Ideas

1. **Orchestrator + workers as first-class session roles.** Every project gets a main orchestrator agent that plans work, spawns workers into their own worktrees, keeps them moving, and escalates only what needs a human; workers and orchestrators are distinct `ao spawn --kind` roles with separate default harnesses.
2. **Durable facts, derived status.** The daemon stores activity, termination, controller generation, PR/check/review facts — never a display string — and computes labels (working, needs input, CI failed, ready to merge) on read, so stored status cannot drift from reality.
3. **One session, one worktree, one interface, one PR.** A session owns an isolated git worktree + branch and exactly one live agent interface (tmux/conpty terminal or runtime-less Chat controller, with drained handoffs); its GitHub PR is claimed/observed and all lifecycle messages route to that owner.
4. **Built-in lifecycle automation instead of user YAML.** CI failures, changes-requested reviews, merge conflicts, and merge readiness trigger daemon-owned reactions (signature-deduplicated nudges, mode-aware delivery, reviewer-agent runs) — the retired `reactions:`/`retries:`/`auto-merge` config schema was deliberately removed.
5. **Compiled-in multi-harness adapters with capability gating.** Twenty-seven terminal harnesses ship in the binary and reuse the user's own installed CLIs/auth; only codex, claude-code, opencode, and droid unlock structured Chat; everything else is Terminal-UI-only, selected per project or per spawn.
6. **Local-first daemon with thin clients and CDC live updates.** SQLite + triggers + `change_log` + CDC poller + SSE replay under `~/.ao`; CLI never touches the DB; primary listener is unauthenticated loopback-only while an opt-in LAN listener serves mobile without shutdown/telemetry/browser routes.

---

## Key Findings

- Isolation model: Git repo → fresh worktree + branch; multi-repo workspace → root + child worktrees; Scratch → AO-managed dir with no branch/PR ops; kill never force-deletes a dirty worktree (`ao session cleanup --dry-run` to preview reclamation).
- Restart/recovery model: desktop owns and restarts the daemon; `ao session restore` reuses the same session + worktree when the adapter supports recovery; failed runtime probes are observations, not death; blocked sessions must be unblocked by answering approvals (lifecycle messages are withheld while blocked).
- Merge flow: SCM observer polls GitHub (lazy auth, ETag, semantic diff) → writes PR facts → lifecycle nudges owner to fix/rebase; human merges explicitly via desktop or `ao pr merge`; reviewer agents run separately and findings are inspectable before delivery to the worker.
- `ao agent ls --refresh` is the source of truth for harness install/auth readiness; spawn does advisory preflight (skippable) plus authoritative validation.
- Tracker lane is incomplete: GitHub issue intake + PR observation are shipped; broader tracker/SCM integrations from older docs are not in the current rewrite.
- Networking posture: `127.0.0.1:3001` loopback-only primary; Connect Mobile is a second opt-in plaintext LAN listener with bearer password, trusted-home-network only.
- Eight load-bearing rules documented (derive status; probes ≠ death; no forced dirty deletes; state under `~/.ao`; loopback primary; thin clients; CDC via triggers; append-only migrations).

---

## Suggestions & Future Directions

1. Per the docs: start with one small worker session (clear, reviewable outcome) before scaling to orchestrator-driven fleets.
2. Use per-role harness defaults (e.g. strong planner as orchestrator, cheap/fast model as workers) via project config rather than one global agent.
3. Keep merges explicit and human-approved; use reviewer-agent runs + `ao review` triage before `ao pr merge`.
4. Treat `ao doctor --json` + `ao status` as the first diagnostics step; reopen desktop to heal daemon/SSE drift.
5. Watch the tracker-lane gap: do not plan workflows assuming every tracker participates in lifecycle automation yet.

---

## Authors & Institutions

Untrivial-ai (GitHub org; also referenced as AgentWrapper in install tap `agentwrapper/tap/agent-orchestrator` and support repo `AgentWrapper/agent-orchestrator`). No individual authors named on the docs pages.
