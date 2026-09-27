# Fleet Orchestrator Landscape Synthesis + SME Platform Roadmap

> One-file synthesis of 14 orchestrator KB entries vs fleet, with a plan to turn fleet
> into a platform for commercial agentic work sold to SMEs (small and medium enterprises —
> non-technical business customers who pay for outcomes, not tooling).
> Jargon, defined on first use: worktree (a separate checkout folder of one repo, so agents
> don't overwrite each other); harness (an adapter that spawns a coder CLI such as Claude Code
> or Codex and normalizes its output); DAG (Directed Acyclic Graph — a workflow with steps and
> dependencies but no loops); TUI (terminal user interface); SQLite (a lightweight file-based
> database); CAS (compare-and-swap — claim an item only if its version number is unchanged);
> DLQ (dead-letter queue — where permanently failed tasks wait for a human);
> SLA (service-level agreement — a promised turnaround/quality a customer pays for).
> Every framework claim below is traceable to its KB entry under
> `/Users/sergii/.ai/knowledge/research/<Name>/` (`summary.md` + `wiki/targeted.md`);
> fleet claims to `docs/OVERVIEW.md`, `docs/ARCHITECTURE.md`, `docs/PRODUCT_PLAN.md`,
> `docs/WORKER_CONTRACT.md` (all read-only; nothing in `/Users/sergii/git/fleet` was changed).

## 1. Framework map

| Framework | Core idea (1 line) | Closest fleet equivalent | Better than fleet at |
|---|---|---|---|
| GasTown | Go daemon running many coder CLIs in isolated tmux sessions + worktrees, tracked in a Dolt-backed task ledger, merged via a rehearsal queue | Fleet supervisor + beads DB + worktree-per-worker | Daemon supervision (heartbeat + watchdog dogs, crash-loop caps) and rehearsal-abort merging that never pushes straight to main |
| GasTownFromClownShowToV10 | Hardening story of how the GasTown factory fixed killers, data loss and DB bloat to reach stable v1.0 | Fleet scale-up runbook / post-mortem guide | Ledger-first discipline ("agent is a bead") plus ephemeral wisp rows kept out of Git history with daily garbage collection |
| Bernstein | Deterministic Python orchestrator: single-threaded tick loop, no LLM (large language model) in coordination, replayable and gated merges | Fleet's Python orchestrator loop + task store + claim logic | Determinism (CAS claims, transition allow-table, strict replay) plus hash-chained audit lineage and bounded model-escalation retries with DLQ |
| AgentOrchestrator | Local-first Go daemon + SQLite control plane with 1 session = 1 worktree = 1 PR (pull request — a review proposal on GitHub) plus CI (continuous integration — automatic checks) automation | Fleet daemon + board UI + worker lifecycle | Derived status computed on read (facts stored, labels derived) plus safety UX: never force-delete dirty worktrees, explicit human-gated merges |
| VibeKanban | Board-first local app: kanban issues to isolated workspaces to agent runs to diff review to PR, with live preview | Fleet board UI + workspace isolation | Diff-first review (inline comments fed into the next prompt) plus live dev-server preview and multi-transport executor adapters |
| ClaudeSquad | Go TUI running parallel agent CLIs, each in its own worktree + tmux session, managed by single keys | Fleet's per-worker worktree + session spawn (execution floor) | Passive observability (tmux pane capture, no worker cooperation needed) plus diff-vs-pinned-base gate and one-command total reset |
| ClaudeOrchestrator | Prose-enforced multi-agent discipline: bounded contracts, evidence labels, merge gates, cross-model review (a playbook, not a runtime) | Fleet task spec + merge validation (supervisor acceptance side) | Evidence labels (direct/proxy/local/blocked) with live-proof gates on money/runtime paths, plus cross-family reviewer loop |
| RalphLoopConductorOrchestratorLandscape | Survey comparing the dumb Ralph re-run loop vs Conductor review cockpit vs micro-protocols for parallel coding | Fleet queue + retry policy + worktree merge | Completion-checks-as-code per task (fleet knows "failed", not "done") plus a janitor verify stage between finish and merge |
| Superharness | Python coordination layer for black-box CLIs: SQLite as sole authority, queue delegation, lifecycle timeouts, crash recovery | Fleet beads DB + atomic inbox claim + watcher loop (near 1:1) | Dual watchdog (idle-timeout plus absolute ceiling) plus atomic claim with dedup index and recovery ceilings with identical-error fuse |
| Harness | Rust server scheduling and isolating external agent executors with policy engine, review loop and GC (garbage collection) | Heavier server version of the fleet supervisor (leased job rows + permits vs beads SQLite) | Lease-generation crash recovery without a watchdog plus policy-as-data gates and primary-challenger review with no-self-review guard |
| Agentflow | Python code-defined agent pipelines with fanout (one step to many parallel copies) / merge (many to one reducer) plus retry-until-approval loops | Fleet YAML workflows + beads queue (fleet has no single DAG object; Agentflow does) | 94-node map-reduce in ~5 lines, pass/fail success gates beyond exit codes, and cross-step Jinja (template `{{...}}` system) wiring |
| OpenOrchestrator | Supervise-don't-replace cockpit TUI: one SQLite status store over isolated worktrees + terminal sessions | Fleet supervisor + worktree isolation + SQLite/beads store | Attention UX (NEEDS YOU / READY TO SHIP / IN FLIGHT lanes) plus pre-merge overlap warnings and smallest-first two-phase merge queue |
| Overstory | Strict role hierarchy (coordinator to lead to scout/builder/reviewer) with overlays, guards, typed mail, watchdog, FIFO (first-in first-out) merge queue | Fleet beads tracker + workers + worktree isolation + merge | Role-shaped agents (generated guard overlays per task), typed SQLite mail with nudge discipline, and 4-tier merge with a learning mulch loop |
| RuahOrch (KB folder `RuahOrch`; spec name Ruah) | File-claim contracts making parallel coding safe: declare owned / shared-append / read-only file globs, reject before start, validate diff after | Fleet worktree isolation + central store (single state file + revision vs fleet SQLite/beads DB) | Claim-aware scheduling (overlap/risk thresholds pick serial vs parallel) plus durable task artifacts (patch + SHAs + claims + gates triple) |

Structure gate: all 14 folders present, each with `summary.md` + `wiki/targeted.md`.
UNCOVERED: none.
Name mappings used above: spec "Ruah" = folder `RuahOrch`;
spec "RalphLoop" = folder `RalphLoopConductorOrchestratorLandscape`.

## 2. Pattern comparison

**Worker restarts — best: GasTown + Superharness.**
GasTown pairs checkpoint files and WIP (work-in-progress) commits with a restart tracker
(backoff, crash-loop cap, lazy prime-hook recovery under 24h), so a dead worker's
replacement resumes instead of restarting from zero.
Superharness adds the dual watchdog (idle-timeout plus absolute ceiling over an events
table) with durable recovery counts and fallback rerouting.
Fleet has stall-kill and lease reclaim but no checkpoint/resume trio or cost ceilings —
Overstory's checkpoint/handoff/resume files decoupled from chat context are the model to copy.

**Conflict resolution — best: RuahOrch + GasTown.**
RuahOrch prevents conflicts before they happen with owned/shared-append/read-only claim
sets and overlap-based serial-vs-parallel scheduling, so incompatible tasks never run together.
GasTown's refinery rehearses each branch merge and aborts to a rework task on conflict
instead of ever pushing to main.
Fleet's merge-conflict repair bead is reactive by comparison — Bernstein's `merge-tree`
pre-flight and OpenOrchestrator's overlap warning are cheaper stepping stones.

**Workflow abstraction — best: Agentflow + Bernstein.**
Agentflow's code-defined graph (fanout/merge reducers, success gates, cycle-until-approval
back-edges) is the most expressive; Bernstein's task DAG with parallel-safe batches, phased
recipes and artifact tasks is the most disciplined.
Fleet's YAML workflows plus beads queue cover scheduling but lack a single DAG object,
per-step runners, and completion predicates — the RalphLoop survey's
"fleet knows failed, not done" critique bites here.

**Multi-harness support — best: GasTown + VibeKanban.**
GasTown treats 13 harnesses as data rows (registry dict plus command builder, no per-harness
class); VibeKanban's executor trait with transport normalization (stream-JSON vs JSON-RPC
vs HTTP vs ACP) plus availability probing is the cleanest code shape.
Fleet's five coder adapters work, but AgentOrchestrator's 27 compiled-in harnesses show
how far data-driven registration can go.

## 3. Borrow list

**1. Harness capability registry (dict + command builder, config-only tool add).**
FROM: GasTown / OpenOrchestrator.
WHY: Adding a coder CLI becomes a config row, not a code change — the fastest way to support whatever model an SME customer already pays for.
EFFORT: S.

**2. Checkpoint/handoff/resume trio decoupled from chat context.**
FROM: Overstory.
WHY: Workers currently die with their context; durable checkpoints let a replacement worker pick up mid-task, which long SME jobs (migrations, content batches) require.
EFFORT: M.

**3. Dual watchdog (idle-timeout + absolute ceiling) over a typed events table.**
FROM: Superharness.
WHY: Fleet's stall-kill catches silence but not slow drift; ceilings bound cost per task, which is what makes fixed-price SME work profitable.
EFFORT: M.

**4. CAS version per bead + stale-claim reset on boot.**
FROM: Bernstein.
WHY: Eliminates double-claim races after supervisor crashes — a correctness floor before any paying customer touches the system.
EFFORT: S.

**5. Rehearsal-abort merge queue (prove feature absorbs base, ordered smallest-first).**
FROM: GasTown / OpenOrchestrator.
WHY: Parallel SME workers will collide; rehearsing merges before touching main keeps output shippable without operator Git skills.
EFFORT: M.

**6. File-claim contracts (owned / shared-append / read-only) with overlap-based serial-vs-parallel scheduling.**
FROM: RuahOrch.
WHY: Prevents conflicts structurally instead of repairing them — highest leverage for multi-worker throughput on shared repos.
EFFORT: M.

**7. Success gates beyond exit codes (output_contains, file_exists) + per-bead done-predicates.**
FROM: Agentflow / RalphLoopConductorOrchestratorLandscape.
WHY: "Worker exited 0" is not "invoice reconciled"; executable acceptance checks are what let fleet report done vs merely finished.
EFFORT: S.

**8. Evidence labels on RESULT claims (direct/proxy/local/blocked) with close-gate check.**
FROM: ClaudeOrchestrator.
WHY: Forces workers to distinguish tested proof from hearsay — cheap defense against confident-but-wrong deliverables to clients.
EFFORT: S.

**9. Derived status + append-only event log (store facts, compute labels on read).**
FROM: AgentOrchestrator.
WHY: Fixes status drift between UI polls and gives audit/replay for free — foundation for client-visible audit trails.
EFFORT: M.

**10. Attention UX lanes (NEEDS YOU / READY TO SHIP / IN FLIGHT) for the board.**
FROM: OpenOrchestrator.
WHY: A non-technical operator should see only what needs them; current Workers/Workflows/Inbox tabs assume a technician.
EFFORT: S.

**11. DLQ with bounded effort-then-model retry (janitor reopens, escalation ladder, replayable DLQ file).**
FROM: Bernstein.
WHY: Turns silent failures into a triageable queue with retry budgets — prerequisite for any SLA promise.
EFFORT: M.

**12. Lease columns (owner/expires_at/generation) + reclaim query, no watchdog needed.**
FROM: Harness.
WHY: Crash recovery by SQL query instead of a supervisor process — simpler and more robust for multi-machine SME hosting later.
EFFORT: M.

## 4. SME platform gaps

None of the 14 compared tools — nor fleet today, per its own PRODUCT_PLAN audit — offers these;
all are needed before charging SMEs.

**Gap 1 — Multi-tenancy and isolation.**
One home dir, one config, no users/projects/organizations, no auth; agents run with host
permissions and only worktree separation. Commercial hosting needs per-customer sandboxes
(containers at minimum) and login-scoped data.

**Gap 2 — Usage metering + billing.**
No per-customer cost tracking (tokens, minutes, runs), no invoicing hooks. Fleet has analytics
for the operator only — nothing billable per client. Overstory's pricing table + transcript
normalization (`ov costs`) is the closest seed.

**Gap 3 — Client-facing audit trails.**
No tamper-evident, per-customer-visible log of what agents did, approved, and changed.
Bernstein's hash-chained lineage is the closest seed, but it serves engineers, not clients.

**Gap 4 — SLA and retry guarantees.**
Retry policy exists as internal data (RETRY_TABLE) but nothing promises a customer "done in
24h or escalated"; no deadline scheduler, no credit/refund hooks.

**Gap 5 — Non-technical onboarding.**
Setup assumes terminal/Git skills (runtime.toml, worktree repair, triage). No Employee/Playbook
abstraction (persistent role + memory + budgets + acceptance criteria) an SME owner could
configure in plain words.

**Gap 6 — Human-approval steps inside workflows.**
ask_human + Telegram exist, but no first-class gated step (pause pipeline, notify client by
email/Slack, resume on approve/reject with deadline) that auditors and cautious buyers demand.

**Gap 7 — Data privacy and retention.**
No per-customer data boundaries, redaction is weak, no backup/restore or retention-delete story —
a blocker for invoices, HR, legal, or health-adjacent SME data.

**Gap 8 — Intake channels SMEs use.**
Only Telegram + manual UI; no Slack, email-in, webhooks, or file-drop intake a small business
would actually trigger work from.

## 5. SME use cases

**Use case 1 — Invoice processing.**
Buyer: bookkeeper at a 20-person wholesaler.
Trigger: emailed supplier PDF lands in intake inbox.
Agent steps: extract line items, match to purchase orders, flag mismatches, draft ledger entries.
Human checkpoints: approve postings above threshold; reject unknown vendors.
What fleet needs: email intake, done-predicates (totals reconcile), approval gate, per-client audit trail.

**Use case 2 — Support triage.**
Buyer: owner of a SaaS micro-business.
Trigger: new ticket via Slack/email webhook.
Agent steps: classify, draft reply from knowledge base, escalate angry/VIP, file bug beads for real defects.
Human checkpoints: approve outbound replies for first 2 weeks, then spot-check.
What fleet needs: Slack/email intake, Employee memory of tone + past answers, approval steps with deadlines.

**Use case 3 — Content pipeline.**
Buyer: marketing lead at a dental chain.
Trigger: weekly cron with topic list.
Agent steps: draft post, cross-model review pass, image brief, schedule.
Human checkpoints: approve each post before scheduling.
What fleet needs: schedules (exists), review-fanout roles, attention-lane board, retry-until-approved loop.

**Use case 4 — Lead enrichment.**
Buyer: sales manager at a logistics SME.
Trigger: CSV upload of new leads.
Agent steps: research each company, score fit, draft personalized opener.
Human checkpoints: approve openers batch-wise; never auto-send.
What fleet needs: file-drop intake, fanout/merge over rows, metering per lead (billing), no-auto-send policy gate.

**Use case 5 — Contract summarization.**
Buyer: office manager at a property firm.
Trigger: new lease PDF uploaded.
Agent steps: extract key dates/obligations/risks, file renewal reminders, summarize in plain language.
Human checkpoints: lawyer reviews risk flags only.
What fleet needs: claim-set isolation per document, evidence labels on extracted clauses, retention/delete policy.

**Use case 6 — Timesheet and expense reconciliation.**
Buyer: founder of a 15-person agency.
Trigger: Friday cron + bank CSV.
Agent steps: match expenses to projects, flag anomalies, draft payroll inputs.
Human checkpoints: approve flags and final numbers.
What fleet needs: SLA scheduling, dual watchdog cost caps, client-visible audit of every posting.

## 6. Recommended roadmap

**Phase 1 — now (trust + operator leverage; unblock first revenue).**
(a) CAS claims + stale-claim reset and lease columns (borrow 4/12) — crash safety before customers.
(b) Done-predicates + success gates + evidence labels (borrow 7/8) — report done truthfully.
(c) Approval-gate workflow step with email/Slack notify + deadline (gap 6) — the feature every cautious buyer asks for first.
(d) Attention-lane board (borrow 10) — let a non-technical operator run it.

**Phase 2 — next (throughput + money).**
(a) Rehearsal-abort merge queue + overlap warnings (borrow 5) and file-claim contracts (borrow 6) — parallel workers without collisions.
(b) Checkpoint/handoff/resume + dual watchdog cost ceilings (borrow 2/3) — long jobs survive and stay profitable.
(c) Per-customer metering + invoicing hooks (gap 2) and client audit trails on derived event log (borrow 9, gap 3) — charge money with proof.
(d) Slack/email/file-drop intake (gap 8) — meet SMEs where they work.

**Phase 3 — later (scale + compliance).**
(a) Multi-tenancy with per-customer containers + auth (gap 1) and privacy/retention controls (gap 7) — host strangers safely.
(b) SLA scheduler with deadline escalation + DLQ triage (borrow 11, gap 4) — sell guarantees.
(c) Plain-words onboarding: Employee/Playbook abstraction with memory + budgets (gap 5) — remove the technician.
(d) Harness registry maturity to 15+ CLIs (borrow 1 extended) — run whatever the customer brings.

Verdict: fleet's core (beads queue, worker contract with STATE/RESULT discipline, worktree isolation, retry-as-data) is a sound kernel — closest in spirit to Bernstein's determinism plus Superharness's black-box coordination — but every compared tool beats it at something load-bearing, and none of them is an SME platform either. The SME opportunity is therefore open: adopt the cheap correctness wins now, buy throughput with merge/claim machinery next, and build the commercial layer (tenancy, metering, audit, approvals) that no surveyed framework has.

Per-framework call: adopt — Bernstein, GasTown; trial — Superharness, RuahOrch, Agentflow, OpenOrchestrator, Overstory, GasTownFromClownShowToV10, ClaudeOrchestrator; watch — Harness, AgentOrchestrator, VibeKanban, ClaudeSquad; skip — RalphLoopConductorOrchestratorLandscape as a runtime (it is a survey — mine it, don't run it).

Sources (KB `connections.md` link style): [[GasTown/summary|GasTown]], [[GasTownFromClownShowToV10/summary|GasTown v10 story]], [[Bernstein/summary|Bernstein]], [[AgentOrchestrator/summary|AgentOrchestrator]], [[VibeKanban/summary|VibeKanban]], [[ClaudeSquad/summary|ClaudeSquad]], [[ClaudeOrchestrator/summary|ClaudeOrchestrator]], [[RalphLoopConductorOrchestratorLandscape/summary|Ralph/Conductor landscape]], [[Superharness/summary|Superharness]], [[Harness/summary|Harness]], [[Agentflow/summary|Agentflow]], [[OpenOrchestrator/summary|OpenOrchestrator]], [[Overstory/summary|Overstory]], [[RuahOrch/summary|RuahOrch]].
Fleet docs (read-only): `docs/OVERVIEW.md`, `docs/ARCHITECTURE.md`, `docs/PRODUCT_PLAN.md`, `docs/WORKER_CONTRACT.md`.
