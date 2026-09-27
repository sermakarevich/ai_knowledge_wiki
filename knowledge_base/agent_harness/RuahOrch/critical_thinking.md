> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: ruah-orch

## Claims vs. evidence

1. **"Declared file claims make parallel agents safe."** Suggestive. The mechanism is concrete and fully implemented (pre-start overlap/scope rejection in `claims.ts:188-231`, post-execution validation in `contract-validator.ts:104-163`), and the append-only shared semantics are carefully specified. But the analyzed snapshot contains no scale evidence — no benchmarks, no multi-agent trial reports, no conflict-rate numbers. File globs are also a coarse boundary: two agents appending to different sections of the same large file still serialize or conflict.
2. **"Zero runtime dependencies."** Strong. `packages/core/package.json` has no `dependencies` key — only devDependencies (typescript, @types/node, biome). Verified directly from the manifest, not just the README.
3. **"Crash-safe, restart-safe orchestration."** Strong on mechanism (O_EXCL lock, temp-write plus rename, revision compare-and-swap, migration on load, conservative reconciliation), weak on adversarial testing evidence. No fault-injection tests were examined; the 30 s stale-lock override and 5 s lock timeout are unvalidated under real contention.
4. **"Harness-agnostic multi-agent support."** Strong as implemented for seven adapters, but the agnosticism is shallow: each harness is a command-line template, and prompt quality per harness is unmeasured. Capability probing (`claude --help`) is pragmatic but brittle across CLI versions.

## Genuinely new vs. repackaged

Genuinely distinguishing: the three-bucket claim model (owned/shared-append/read-only) with fixed precedence plus append-only byte-prefix enforcement is more specific than generic "file locks" in tmux/worktree runners, and the claim-aware stage planner with numeric thresholds (0.3 overlap, 2.0 risk) is unusual. Repackaged: git-worktree isolation, Markdown task DAGs with ready-set scheduling, and RUAH_* env-var context follow well-worn patterns from CI systems and prior agent harnesses. The single-JSON-state-with-lockfile is the classic small-tool persistence design, executed well rather than invented.

## Weaknesses and blind spots

- No measured evidence on state-file contention: dozens of concurrent tasks queue on one lock file with a 5 s timeout, and failure behavior there is unspecified.
- Glob matching is hand-rolled; brace expansion, negation, and case-sensitivity edge cases are unverified against real repos.
- The shared-append check (byte prefix plus line count) can reject semantically null reformats (line-ending normalization, trailing newline) — noisy in CRLF or formatter-heavy repos.
- Misspelled executor names fail only at spawn time, not at creation time — a late, confusing error.
- Governance gates run synchronously via `execSync` at merge time with no documented timeout; a hanging gate blocks the merge.
- `integration.ts` vs `integrations.ts` near-duplicate names and the double backfill layers in state loading are small maintenance smells.

## Applicability

Works when: one repo, a handful to low-dozens of parallel tasks, file boundaries that map cleanly to globs, harnesses invokable as CLIs, and merges that can proceed in dependency order. Fails or strains when: tasks legitimately interleave within the same files, writer concurrency saturates the state lock, harnesses need interactive sessions, or governance requires asynchronous approvals. Prerequisites are modest: Node >= 18, git, and the harness CLIs on PATH.

**Relevance to my work** —

- **Trial claim locks in fleet:** the owned/shared-append/read-only model with pre-start overlap rejection maps directly onto fleet's parallel coder workers; prototype as a pre-spawn check before any state redesign.
- **Adopt artifact capture:** persisting changedFiles plus full patch with a validation triple is cheap and makes fleet merges auditable — the highest value-to-effort borrow.
- **Trial RUAH_*-style env context:** inheritable parent-task and file-scope variables are a small, harness-agnostic way to scope subagents; easy to pilot.
- **Watch, do not copy, the state file:** fleet's centralized beads DB already solves what `state.json` plus lockfile solves; ruah's revision-guard and temp-plus-rename discipline is worth borrowing as technique, not as architecture.

## What this changes

If the claims hold: parallel coding agents become schedulable like CI jobs — declared, validated, merged in order — and the "who touched what" audit trail becomes automatic, which unblocks fleet-scale multi-agent code work. Second-order effect: harness choice becomes interchangeable plumbing (one adapter entry), shifting competition to agent quality rather than orchestration lock-in. If the claims only partially hold (contention and coarse globs bite at scale), what survives is still valuable: artifact receipts, append-only sharing, and env-var scoping are independently adoptable.

## Verdict

A well-engineered, honestly scoped specialist: the claim/artifact/planner core is concrete, fully cited, and dependency-free, while scale and robustness claims rest on mechanism rather than measurement. Worth mining for fleet's parallel-execution design, with the state layer admired but not imitated. **trial** — prototype claim locks plus artifact capture in fleet before committing further.
