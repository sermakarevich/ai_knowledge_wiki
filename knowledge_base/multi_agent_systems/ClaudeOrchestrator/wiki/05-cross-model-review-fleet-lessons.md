> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Cross-Model Review and Fleet Lessons

**In one sentence:** An independent reviewer from a different model family inspects every merged batch through an enforced launch-process-trace gate, and the whole discipline ports to fleet as seven borrowable ideas.

## Key points

- Cross-model review means a different model family (Codex or Pi reviewing Claude-orchestrated work), because same-family reviewers share blind spots (`SKILL.md:641-647`).
- Reported yield: 15×P1 + 37×P2 findings that self-review and mechanical checks both missed — DTO mismatches, state-machine gaps, missing tenant filters, float-cents bugs, fake success toasts, null handling (`SKILL.md:670`; playbook `README.md:62-66`).
- The case study shows reviewer vantage matters more than brand: plan-text-only review (GPT) missed a runtime landmine that repo-access review (DeepSeek) caught (`CASE-STUDY.md:31-33`).
- Enforcement is a three-part gate: current-batch review launched (background OK, not-started blocks next dispatch), previous findings processed (P1 fixed, P2 recorded), written trace with findings count (no record = not run); two consecutive skips stop the run (`SKILL.md:321-325`).
- P2s unfixed for 3+ batches escalate to P1 (`SKILL.md:343-346`); high-risk changes (money, permissions, contracts, migrations, sync, concurrency) are reviewed BEFORE merge with a two-commit audit trail (`SKILL.md:327-341`).
- The review runs via `node "$PLUGIN_ROOT/scripts/codex-companion.mjs" review --wait --base <pre-merge-commit>` — never standalone `codex review` (parameter conflicts, no `--wait`, large-diff timeouts) (`SKILL.md:649-657`).
- Seven fleet-borrowable ideas: evidence labels + no-upgrade rule, ORC-ID vocabulary, anti-shallow-slice classification, review gate with trace + P2 escalation, dispatch-contract checklist, whole-invariant re-review, runbook prune rule.

---

## Mechanics

- **Invocation:** `PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/openai-codex/plugins/codex"`; run the companion script with `--wait --base <pre-merge-commit>` (`SKILL.md:651-657`).
- **Whole-invariant re-review (no ping-pong):** when a finding exposes a shared-invariant bug, fix every face of the invariant at once, then run ONE review of the whole diff — the trap symptom is 2+ rounds with findings in the same just-touched subsystem (`SKILL.md:668`).
- **Pre-merge order for high-risk paths:** commit A → review → commit B fixes → merge, preserving a two-commit audit trail (`SKILL.md:327-341`).

## Multi-harness picture

Three adapters share one core loop, evidence discipline, contract, iron rules, review, and ORC IDs (playbook `README.md:7,19-91`). Claude is synchronous with no ledger/heartbeat (those live in the codex sibling's Go helper, adapter `README.md:97`); the Kimi adapter was not analyzed. Fleet already owns the async side (bead DB, heartbeats, worktrees) and lacks the sync side this skill contributes: bounded contracts, evidence labeling, merge-gate checklists, ORC vocabulary.

## Seven fleet-borrowable ideas

1. **Evidence labels + no-upgrade rule + live-proof gate** (`SKILL.md:508-524,258`; playbook `README.md:29-38`) — tag worker RESULT.json claims `direct/proxy/local/blocked`.
2. **ORC-ID review vocabulary** (`SKILL.md:700-721`) — supervisor rejection reasons keyed by ID.
3. **Anti-shallow-slice classification** (`SKILL.md:126-141`) — required field in fleet task specs.
4. **Review gate with trace + P2 escalation** (`SKILL.md:321-325,343-346`) — supervisor dispatch precondition + finding ledger.
5. **Whole-invariant re-review** (`SKILL.md:668`) — rework-loop policy for supervisor/worker iterations.
6. **Cherry-pick rescue** (`SKILL.md:272-284`) — validation-step salvage for out-of-scope branches.
7. **Runbook prune rule** (`SKILL.md:20`) — periodic fleet-protocol review against dead rules.

## Caveats

Scale numbers (53 batches / ~95 agents / ~70k lines; 43%→0% conflicts; ~57% auto-merge; ~40% of P1s from five patterns; 15×P1+37×P2) ship without datasets, windows, or false-positive rates; thresholds (2-skip stop, P2→P1 after 3 batches, ≤5-line hotfix, max 2–3 parallel, 600s review timeout) are heuristics, not derived constants. The adapter assumes pushing to `origin/main` is always allowed and leaves P1/P2/P3 severity definitions implicit.

**Covers:** claude-orchestrator `SKILL.md:272-284,321-346,641-670`, `README.md:78-97`; orchestration-playbook `README.md:7,62-66,96-102`, `CASE-STUDY.md:22-37`.
