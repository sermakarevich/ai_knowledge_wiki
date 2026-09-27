> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Best practices for Claude Code - Claude Code Docs

## Claims vs. evidence

- Core claim: the context window is "the most important resource to manage" — a session holds every message, file read, and command output, and a single debug/explore run burns "tens of thousands of tokens."
- Evidence level: plausible mechanism (window fills → "forgetting," more mistakes) but no numbers: no degradation curves, no per-file-read costs, no before/after token counts in the digest or wiki chunks.
- Claim: "Give Claude a check it can run" turns a watched session into a walk-away one (tests, build exit code, linter, output-diff script, screenshot comparison).
- Evidence level: before/after prompt tables are illustrative, not measured; no data on iteration count, pass rates, or wall-clock savings.
- Claim: Explore → Plan → Implement → Commit with plan mode avoids "solving the wrong problem"; one-sentence-diff heuristic decides when to skip planning.
- Evidence level: procedural wisdom, internally coherent, but untested — no error-rate comparison of planned vs. unplanned tasks.
- Strongest evidenced-adjacent point: the gating taxonomy (same-prompt check vs. `/goal` evaluator vs. Stop-hook gate with the 8-block override vs. fresh-model refutation) admits failure modes rather than promising autonomy.
- Weakest: CLAUDE.md rules in chunk 02 (ES modules, destructure imports, typecheck after changes, single-test runs) are asserted with zero rationale, commands, or timings.
- Unverified UX claims: `/init` starters, `/context` confirmation, and "value compounds" team editing are stated as benefits with no adoption or retention signal.
- Notably absent as evidence: no counterexamples, no "we tried X and it failed" cases, so the reader cannot calibrate when the prescribed patterns break.

## Genuinely new vs. repackaged

- Genuinely new (agentic-tooling specific): the runnable-check-as-autonomy-gate; plan mode as a read-only phase (Shift+Tab, `--permission-mode plan`, Ctrl+G plan editing); CLAUDE.md vs. skills split (persistent broad rules vs. on-demand domain knowledge).
- Genuinely new (interface mechanics): `@`-file references, pasted/dragged images, `/permissions` URL allowlisting, `cat error.log | claude` piping, `/init`, `/context`, `/doctor` maintenance loop, and `claude -p` output contracts (plain text default, single-`result` JSON, line-delimited `stream-json` opening with `init`).
- Repackaged prompt engineering: "be specific," scope the task, point at git history, reference existing patterns (HotDogWidget example), state symptom plus done-state — standard instruction-tuning advice relabeled for an agent harness.
- Repackaged software process: explore-before-code, written plan, verify, commit/PR — the four-phase workflow is design-review orthodoxy, not a Claude invention.
- The cut test ("Would removing this cause mistakes?") and the warning that bloated CLAUDE.md causes instruction-ignoring repackage context-budget insight in memorable form — useful framing, familiar substance.

## Weaknesses and blind spots

- No quantification anywhere: no token budgets, no accuracy/latency/cost trade-offs, no guidance on when the window is "full enough" to compact or restart.
- Assumes a runnable check exists; silent on legacy code, flaky suites, long builds, GPU-bound tests, or UI work with no screenshot oracle.
- Verification-gate trade-offs are named but not resolved: `/goal` evaluators can stall, Stop hooks are overridden after 8 blocks, second-opinion subagents cost a full second inference — no recommendation on which to default to.
- Security and privacy gap: encourages Bash execution, MCP fetches, URL allowlisting, and piping raw logs into the model, with nothing on secrets redaction, env-var leakage, or untrusted fetched content.
- CLAUDE.md lifecycle risk: checked-in, team-compounding memory goes stale; `/doctor`-proposed cuts and `IMPORTANT`-only emphasis are heuristics, not versioning, ownership, or conflict-resolution rules.
- Thin team story beyond "check it into git": no merge-conflict norms for agent edits, no PR-size guidance, no review checklist for agent-authored diffs.
- `claude -p` chunk is reference-thin: three commands and two format facts, nothing on exit codes, stderr, secret handling, or composing JSON/streaming output into scripts.
- No cost model: repeated self-iteration against a check burns tokens per loop, yet there is no stop-budget guidance beyond the built-in hook override.
- Vague skip-planning heuristic ("one-sentence diff") leans entirely on operator judgment with no calibration examples from real diffs.

## Applicability

- Directly applicable to any repo-based agent loop today: adopt the verification check, the plan-mode gate for multi-file work, and the concise checked-in CLAUDE.md pattern.
- Conditionally applicable to notebook/experiment-heavy ML work: the "runnable check" maps to eval scripts and fixture diffs, but long-running training jobs break the tight in-conversation iteration the guide assumes.
- **Relevance to my work**
  - AI/ML engineering: convert "looks done" into script-graded checks (unit tests, eval-set diffs, lint/typecheck) and require evidence (command plus output) before accepting agent results.
  - Agentic systems: reuse the gating ladder — same-turn check, session `/goal`, deterministic Stop-hook gate, fresh-model refutation — and log which gate caught each failure to tune autonomy per task class.
  - Elisity data platform: encode non-guessable environment facts once in CLAUDE.md (commands, runners, env quirks, gotchas), push endpoint/schema/API detail to linked docs or on-demand skills, and scope prompts to services plus token-refresh/session flows rather than "fix the login bug."

## What this changes

- Shifts the operator role from reviewer to check-designer: the highest-leverage prompt line is the verification command, not the feature description.
- Makes context a budget to manage explicitly: prefer `@`-references over pastes, single-test runs over full suites, skills over a fat CLAUDE.md, and plan-mode reads over speculative edits.
- Reframes autonomy as gated, not granted: walk-away sessions are earned per task by the strength of the check, with the 8-block override and stall-then-stop behaviors as reminders that gates leak.
- Downgrades CLAUDE.md from documentation to control plane: every line must change behavior or be cut, and staleness is treated as a defect class, not clutter.
- Extends the same discipline to scripting: default to plain text for humans, single-object JSON for pipelines, and `stream-json` for live consumers — a small contract that prevents brittle parsing later.
- Raises the bar for "done": evidence (test output, command plus return, screenshot diff) replaces assertion, which changes how agent PRs should be reviewed.

## Verdict

- The context-management framing and verification-gate taxonomy survive scrutiny; the prompt-specificity advice and style-rule examples do not add much beyond convention.
- Adopt the check-first workflow and the concise-CLAUDE.md-plus-skills split now; the rest is sensible hygiene worth standardizing but not worth debating.
- Big caveat: without metrics, treat every "walk away" claim as aspirational until your own repo measures iteration count and defect escape rate under each gate type.

**adopt** the verification-check plus plan-mode workflow and the pruned CLAUDE.md discipline; **trial** the Stop-hook and second-opinion gates on one repo before standardizing.
