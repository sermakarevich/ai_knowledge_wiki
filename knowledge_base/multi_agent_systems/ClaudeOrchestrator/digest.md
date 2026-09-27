> [[index|Wiki]] | [[summary|Summary]]

# Claude-Orchestrator Skill + Orchestration-Playbook Core — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-task-contracts-dispatch|Task Contracts and Dispatch]]

**In one sentence:** Every agent dispatch carries a bounded ten-field contract — outcome, anti-shallow-slice class, change rationale, boundaries, gates, evidence, challenge duty, restart policy, rubric, handoff — and without a contract there is no dispatch.

- The contract is the central domain object: ten required fields, "no contract, no dispatch" (playbook `README.md:40-53`).
- Every task declares an anti-shallow-slice classification — `vertical-completion | runtime-proof | blocked-removal | owner-gated` — plus why it is not repeating an already-completed first slice.
- Boundaries are explicit: allowed paths, forbidden paths, branch name (`build/<slug>`), base commit (`origin/main`); concrete gate commands replace the word "passed".
- Agents have a duty to challenge unclear, risky, or over-broad contracts and stop instead of guessing (`SKILL.md:385-389`).
- The restart policy is inside the contract: repeated same-gate failure, contract drift, or noisy patch-on-patch means stop and recommend a clean restart (`SKILL.md:414-416`).
- The Claude adapter expands the ten fields into a twelve-section prompt template adding MUST-COMMIT, Common P1 Patterns, the Minimalism Ladder, shared-resource append-only rules, and a ≤~30-line handoff cap (`SKILL.md:350-464`).
- Handoffs report branch, commit hashes, file list, actual gate output, and residual risks — never the bare word "passed".

## 2. [[wiki/02-worktree-agents-batch-loop|Worktree Agents and the Batch Loop]]

**In one sentence:** Work flows in synchronous batches — recon, decompose, parallel dispatch into isolated worktrees, accept, merge, cross-model review — where the orchestrator alone owns merge, push, and cleanup.

- The loop is deliberately synchronous: agents "run and return results within the current session — no fire-and-forget, no heartbeat polling" (`SKILL.md:54`), because synchronous dispatch "is what makes review→merge gates enforceable" (`SKILL.md:56`).
- Each agent gets one isolated worktree plus one `build/<slug>` branch, dispatched via concurrent `Agent(isolation:"worktree")` calls in a single message (`SKILL.md:70-79`).
- The orchestrator alone owns merge (`--no-ff` on main), push to `origin/main`, worktree removal, and post-merge integration testing (`SKILL.md:264-309`).
- Same-module tasks are serialized, never parallelized — measured conflicts fell 43% → 0% — and three-agent parallelism requires four preconditions (`SKILL.md:472-496`).
- The worktree base trap (ORC-14): new worktrees must be created from `origin/main` after pushing serial merges, never from a stale local main (`SKILL.md:72-79,314`).
- A Batch Status Report (Delivered / Completed / Rejected / Blocked / Repo State / Next) closes every loop and doubles as the context-rebuild checkpoint after compaction (`SKILL.md:729-757`).
- Durable state is plain markdown — `PROGRESS.md`, `inbox.md`, concepts/glossary, Batch Status Reports — coordination state that survives compaction but is explicitly not proof (`SKILL.md:780-784`).

## 3. [[wiki/03-evidence-discipline-acceptance-rules|Evidence Discipline and Acceptance Iron Rules]]

**In one sentence:** Every acceptance claim carries one of four evidence labels — direct, proxy, local, blocked — upgrading a label is lying, and no branch merges until the orchestrator independently re-verifies commits, diffs, gates, and claims.

- Four evidence levels: `direct` (real target environment), `proxy` (substitute or intermediary), `local` (dev/test only), `blocked` (needs human, credentials, hardware, or a product decision) (playbook `README.md:29-38`).
- House rule: "Upgrading an evidence label is lying" — never upgrade `local→proxy` or `proxy→direct` (`SKILL.md:519`); the founding incident was a local unit test labeled proxy, later cited as direct (playbook `README.md:38`).
- `direct` requires device readback, callback-backed ACKED, processor/DB artifact, or physical evidence; `SENT`/TCP/screenshot/oral confirmation are proxy at best (`SKILL.md:520-521`).
- Iron rule 1: a worker's "committed" is not evidence — acceptance opens by proving `git log <branch> --not main` is non-empty (founding incident: uncommitted work lost with a force-removed worktree).
- Iron rule 2: never trust self-reported gates — re-run key gates on the acceptance side; iron rule 3: review ≠ authorization to merge/push/deploy/cleanup; iron rule 4: remove worktrees only after the merge is verified (playbook `README.md:55-60`).
- The adapter adds a live-proof gate: anything touching runtime, production, device, payment, hardware, provider, or external service needs `direct` proof or an explicit item-specific waiver; `local` gates are insufficient (`SKILL.md:258`).
- A mandatory post-merge integration test runs after every batch because per-branch gates passing does not prove the layers work together (`SKILL.md:302-309`).

## 4. [[wiki/04-orc-antipatterns|ORC Anti-Patterns]]

**In one sentence:** Eighteen numbered failure patterns — from shallow-slice disguise and evidence upgrades to stale worktree bases and runbook bloat — give every review a shared rejection vocabulary backed by real incidents.

- ORC IDs are shared verbatim across all three adapters (claude, codex, kimi); the house rule is that every entry is backed by a real incident and a gate that never caught a real bug does not belong (playbook `README.md:15,68-91`).
- ORC-01–03 cover fake completion: shallow-slice disguise, evidence-label upgrade, and blind trust in self-reported gates (`SKILL.md:700-702`).
- ORC-04–08 cover orchestration discipline failures: slot-filling dispatch, review treated as authorization, constraint amnesia, the orchestrator writing worker code, and merging before review (`SKILL.md:703-709`).
- ORC-09–14 cover execution failures: silent stops, idempotency blindness, phantom commits (the #1 Claude Code subagent failure mode), parallel name collisions, same-module parallelism, and the stale worktree base trap (`SKILL.md:710-716`).
- ORC-15–18 cover review and process decay: skipped reviews, role drift, runbook bloat, and motion mistaken for progress (`SKILL.md:717-721`).
- The runbook prune rule (ORC-17) requires every gate to periodically show evidence of catching a real bug or be demoted or deleted (`SKILL.md:20,719`).
- Fleet fit: the ORC table is directly reusable as supervisor rejection reasons and worker guidance keyed by ID.

## 5. [[wiki/05-cross-model-review-fleet-lessons|Cross-Model Review and Fleet Lessons]]

**In one sentence:** An independent reviewer from a different model family inspects every merged batch through an enforced launch-process-trace gate, and the whole discipline ports to fleet as seven borrowable ideas.

- Cross-model review means a different model family (Codex or Pi reviewing Claude-orchestrated work), because same-family reviewers share blind spots (`SKILL.md:641-647`).
- Reported yield: 15×P1 + 37×P2 findings that self-review and mechanical checks both missed — DTO mismatches, state-machine gaps, missing tenant filters, float-cents bugs, fake success toasts, null handling (`SKILL.md:670`; playbook `README.md:62-66`).
- The case study shows reviewer vantage matters more than brand: plan-text-only review (GPT) missed a runtime landmine that repo-access review (DeepSeek) caught (`CASE-STUDY.md:31-33`).
- Enforcement is a three-part gate: current-batch review launched (background OK, not-started blocks next dispatch), previous findings processed (P1 fixed, P2 recorded), written trace with findings count (no record = not run); two consecutive skips stop the run (`SKILL.md:321-325`).
- P2s unfixed for 3+ batches escalate to P1 (`SKILL.md:343-346`); high-risk changes (money, permissions, contracts, migrations, sync, concurrency) are reviewed BEFORE merge with a two-commit audit trail (`SKILL.md:327-341`).
- The review runs via `node "$PLUGIN_ROOT/scripts/codex-companion.mjs" review --wait --base <pre-merge-commit>` — never standalone `codex review` (parameter conflicts, no `--wait`, large-diff timeouts) (`SKILL.md:649-657`).
- Seven fleet-borrowable ideas: evidence labels + no-upgrade rule, ORC-ID vocabulary, anti-shallow-slice classification, review gate with trace + P2 escalation, dispatch-contract checklist, whole-invariant re-review, runbook prune rule.

## The argument in five moves

1. Agent output, not agent writing, is the bottleneck — so governance (contracts, evidence, gates) is the system.
2. Bound every dispatch with a ten-field contract; no contract, no dispatch.
3. Run agents in isolated worktrees in synchronous batches the orchestrator fully owns through merge and cleanup.
4. Accept nothing on trust: re-verify commits, diffs, and gates, and label every claim with honest evidence.
5. Review every batch with a different model family, name every failure with an ORC ID, and prune every rule that stops catching bugs.
