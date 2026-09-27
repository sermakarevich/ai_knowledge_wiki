> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: OpenOrchestrator (`owt`)

## Claims vs. evidence

**"Conflict Guard watches every worktree in real time" (`README.md:5`).** Suggestive, not literal. Detection is `git diff --name-only` intersected with peers' *last-reported* `modified_files` from SQLite (`core/merge.py:183-213`) — real-time only if agents report faithfully, and Pi/OpenCode/custom tools install no hooks (`supports_hooks=False`). A silent agent is invisible to the Guard. The merge-time warning path is verified in source; the "watches in real time" phrasing overclaims the freshness guarantee.

**"Supervise-don't-replace" cockpit (`README.md:5-7`).** Strong. The architecture backs it: no LLM calls anywhere in `src/`, thin view (`core/control_plane_view.py:18-22` states no business logic), hooks as the sole agent→system channel, `fix` literally exiting the cockpit to hand control to the human. The principle is load-bearing, not branding.

**Multi-provider + custom tools without code changes.** Strong. `AIToolProtocol` + `CustomTool` + pre-validation registration (`config.py:322-326`) is genuinely a config-only extension path, with 5 bespoke classes and generic fallback coexisting. The one soft spot: capability flags are coarse — a tool either supports hooks or it doesn't, with no partial-reporting tier, which is exactly why silent tools degrade the Guard.

**Two-phase merge + queue safety.** Suggestive-to-strong. Phase discipline with abort-before-phase-2 is sound and verified (`core/merge.py:328-574`); but phase 2 mutates the operator's main checkout (`clean -fdX` + autostash), and queue ordering ignores branch age, test status, and review state. It prevents mechanical breakage, not semantic breakage.

## Genuinely new vs. repackaged

The lane-sorted decision surface with verb rows and a context-sensitive footer is the most original contribution — worktree boards exist (Conductor, Claude Squad, Vibe Kanban), but the per-row-action + teaching-footer combination is a UX idea, not a rename. Recorded-backend sessions (backend ownership as row data enabling flagless reattach) is a small, genuinely good schema habit. Everything else is well-executed repackaging: worktree isolation (git-native), tmux sessions (industry standard), smallest-first merge order (folk wisdom formalized in 5 lines), plan-preamble "workflows" (prompt engineering labeled as workflow), MCP peer messaging (thin wrapper over the MCP SDK).

## Weaknesses and blind spots

- **No correctness gate before ship.** Nothing requires tests to pass, review to happen, or CI to be green — `s`hip merges on human confidence plus a diff glance. Agent Orchestrator's inspector-gate model is the avoided comparison.
- **Advisory Guard, silent agents.** As above: no hooks → no `modified_files` → no overlaps → false confidence. The system never distinguishes "no overlap" from "no data".
- **Poll loop, no events.** Full section rebuild every 2 s with a perfectly good change token (`MAX(updated_at):COUNT(*)`) unused by the view. Fine at owt's scale; a ceiling on board size and a battery/CPU tax.
- **Phase 2 operates on the live main checkout.** `clean -fdX` in the operator's own working copy during ship is the riskiest single command in the codebase; concurrent human work there during a ship is unguarded.
- **herdr is a second-class backend** (tmux-only plan/automated/argv paths) with sync-over-async bridges — two session stacks to maintain for one abstraction.
- **Bus factor and maturity signals**: single-author (Pedro Lopes), v0.5.0 Beta, ~68 test files (good breadth — merge, backends, MCP peer, control plane all covered), ruff + strict mypy in CI. Healthy hygiene for a solo project; adoption risk is maintainer bandwidth, not code quality.

## Applicability

Works when: a human operator runs 2–20 parallel agents across 1–4 harnesses, mostly Claude/Droid (hook coverage), on macOS/Linux with tmux, shipping to GitHub (PR flow) or a local base branch. Fails or degrades when: agents are silent (no hooks → stale status, blind Guard), scale exceeds dozens of worktrees (poll loop, single SQLite writer model), the main checkout is actively used during ships, or the team needs policy gates (tests/review/CI) rather than human keystrokes. The MCP peer layer needs the `[mcp]` extra on every agent environment — easy to half-deploy.

**Relevance to Sergii's contexts:**
- **Fleet (agentic orchestration):** borrow, don't adopt — 7 items in [[wiki/targeted]] §6 (overlap warnings from stored file lists, verb rows + teaching footer, lane hiding, two-phase merge, smallest-first queue display, `--pr` ship mode, capability-flag harness matrix). All compose with fleet's queue + retry-table rather than replacing them.
- **Elisity data platform:** the status-row-as-contract pattern (agent writes structured state, every consumer polls one store) transfers to pipeline supervision; SQLite-WAL single-file memory is a viable model for small coordinators.
- **AI/ML engineering practice:** hook-gated reporting (`supports_hooks` matrix) is a cautionary tale — design status for silent agents (derive from git, not self-report) from day one.

## What this changes

If the lane+verb decision surface becomes standard, supervising N agents stops scaling with N in operator attention — the board absorbs triage and the human handles only exceptions. If overlap-from-stored-lists becomes standard pre-merge hygiene, a whole class of "surprise conflict" incidents disappears at near-zero cost. Second-order: harnesses that self-report (hooks) become more orchestrable than silent ones, creating pressure on tool authors to emit lifecycle events — a quiet standardization win. What doesn't change: correctness still needs gates owt doesn't build.

## Verdict

A well-built, honestly-scoped cockpit whose architecture matches its marketing, with one overclaimed adverb ("real-time") and one missing layer (correctness gates). For fleet the call is **trial** — not adopt-the-tool, but trial the 7 borrowable mechanisms, headed by Conflict-Guard-from-stored-lists and the verb-row/footer UX, because they are cheap, proven in source, and orthogonal to fleet's scheduler.
