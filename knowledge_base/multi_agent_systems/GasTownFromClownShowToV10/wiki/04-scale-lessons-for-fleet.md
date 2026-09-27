> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Scale Lessons for Fleet: Costs, Comparisons, and Borrow List

**In one sentence:** Gas Town's v1.0 is a field manual for fleet: who may operate it and at what cost, why it resembles Kubernetes and Temporal without being either, which seven cheap tricks transfer directly, and what comes next with Gas City and federation.

## Key points

- Gas Town demands Stage 6–7 operators (people already hand-running 3–10+ agents daily), multiple paid agent accounts (Yegge burned through two toward a third in a week), tmux fluency, and tolerance for throughput-first sloppiness — it is "a cash guzzler" by design.
- Kubernetes asks "is it running?" while Gas Town asks "is it done?": same control-plane/node/local-agent/source-of-truth shape, but completion (land the convoy, nuke the worker) instead of uptime, credited workers instead of anonymous pods, terminal goals instead of continuous desired state.
- Temporal gets durability from deterministic replay; Gas Town gets it from NDI (persistent molecule + hook + identity, self-correcting superintelligent executors) — plenty for a dev tool, not a Temporal replacement.
- Seven concrete borrowable ideas: convoy wrapper per dispatch, sling+hook instead of pushed sessions, wisps for control chatter, one Refinery for the merge queue, a Witness babysitter per repo, seance + graceful handoff, mail budgets with nudge-first prompting.
- Scale dangers for fleet's wall: Dolt commit-graph bloat, two-truths sync, killer watchdogs, spawn storms, orphan databases, mail-as-storage, idle-polling token burn, model fragility (Opus 4.7's "just two more things" loop broke convergence), and factory starvation without pre-generated plans.
- Only Claude Code and close clones (Codex, Gemini CLI, Amp, Amazon Q) drive the town today; Beads alone runs on anything ~Sonnet 3.5-smart — the ledger is portable, the orchestration is not yet.
- Gas City is the stated next step: the town split into reusable SDK (Software Development Kit, building blocks) parts (identity, roles, mail, sessions, cost tracking, multi-model dispatch, GUPP, NDI, formulas, convoys, patrols, plugins, seances), plus federation/Wasteland, Mol Mall, remote hyperscaler workers, and real dashboards.

---

## 1. Who may enter, and what it costs

The 8-stage Dev Evolution chart gates adoption: Stage 1–2 (completions, sidebar agents) need not apply; Stage 6 (3–5 parallel CLI agents, YOLO) is the brave minimum; Stage 7 (10+ hand-managed) is the real entry ticket; Stage 8 is building your own orchestrator. Costs are explicit and unapologetic: multiple Claude Code accounts (rate limits force multi-email "siphons"), tmux learning, constant elbow grease ("equal parts guzzoline and elbow grease"), and a vibe-coding mindset where fish fall out of the barrel and that is fine. Fleet implication: budget per-convoy cost tracking from day one and pin known-good models per role instead of floating latest.

## 2. Kubernetes and Temporal: the two comparisons

**Kubernetes.** Control plane (Mayor/Deacon vs scheduler/controller-manager), execution nodes (Rigs vs Nodes), local agents (Witness vs kubelet), ephemeral workers (Polecats vs Pods), source of truth (Beads vs etcd) — the shapes rhyme because both herd unreliable workers toward a goal. Destinations differ: uptime vs completion, replicas-forever vs land-then-nuke, anonymous cattle pods vs credited workers with CV chains over disposable session-cattle, continuous reconciliation vs terminal goals.

**Temporal.** Both promise workflows that survive crashes, but Temporal replays deterministically while Gas Town self-corrects nondeterministically through well-specified molecules executed by superintelligent agents. Yegge's own caveat stands: "Ask your doctor if Gas Town is right for you" — edge cases abound, and anything needing exact-once semantics still wants Temporal.

## 3. The seven borrowable ideas (fleet-ready)

1. **Convoy wrapper for every dispatch** — one parent tracking bead per batch with a live tree view; "landed" = done. Cures "issue wy-a7je4 finished — part of what?" confusion.
2. **Sling + hook, don't push sessions** — per-worker hook list in the DB; dispatch = add row + poke. Fleet already has a task DB; add a hook-per-worker view and restarts become free.
3. **Wisps for control chatter** — heartbeats, patrol ticks, spawn events as DB-only rows burned after ~24h (optional one-line squash). Direct fix for history bloat.
4. **One Refinery for merges** — single merge-queue serializer with worker pre-verify + skip-repeat-CI. Ends mass-rebase "monkey knife fights."
5. **Witness per repo** — a babysitter loop whose only job is un-sticking workers and draining the queue. Bounded job, fewer stuck swarms, less manager prompting.
6. **Seance + graceful handoff** — save session IDs in poke titles; successors auto-`/resume` predecessors to recover dropped notes; explicit tidy-and-restart command.
7. **Mail budget + nudge-first prompting** — cap mails per role, prefer pokes over mails, zero-commit status paths. Cuts commit storms at the source.

## 4. Scale dangers: fleet's wall of warnings

Dolt commit-graph bloat (ephemeral data must be wisp-class with Reaper/Compactor discipline, GC daily+); two-truths sync (one primary store; JSONL snapshots for disaster only); killer watchdogs (stuck-detection in a slow plugin, never the hot loop); spawn storms + orphans (circuit breakers, idempotent spawn, fail loudly on duplicate DBs); mail-as-storage + idle polling (budgets, nudge-first, backoff-to-sleep, wake-on-mutation only); model fragility (Opus 4.6 "worked brilliantly", Opus 4.7 loopiness killed convergence — pin per role); cost and starvation (multiple paid accounts, cap concurrency, generate work ahead via formulas/epics or the factory idles).

## 5. Multi-harness reality and the Gas City roadmap

"Claude Code" in the essays means the whole 2025 CLI form-factor pack: Codex, Gemini CLI, Amp, Amazon Q-developer CLI — all dispatched as tmux sessions with role prompts. Beads alone is harness-neutral (anything ~Sonnet 3.5+); full orchestration is not. Skipped for v1 (federation/remote GCP workers the Python version had, GUI/Emacs/web UIs, Refinery plugins, Mol Mall, the million-step demo) becomes the roadmap: **Gas City** (town factored into importable SDK parts so custom orchestrators reuse identity, GUPP, NDI, formulas, convoys), **federation + Wasteland** (linked towns, shared wanted board, portable reputation), **Mol Mall** (formula marketplace), remote hyperscaler workers, better dashboards, timers/callbacks — plus the training fix of getting factory-worker behavior into frontier-model corpora so less prompting is needed.

**Covers:** Welcome essay warning/comparison/future sections (Figs 2–4, 16) + v1.0 deltas + targeted.md sections 5–7 + Deltas section.
