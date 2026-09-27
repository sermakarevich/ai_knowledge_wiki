> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Ralph loop mechanics

**In one sentence:** The Ralph loop re-runs the same agent on the same prompt file with a fresh context window every pass, keeping all memory in files and git, and stops only when an externally wired completion check (tests green, COMPLETE tag, all PRD stories passing) says done.

## Key points

- Ralph loop = `while :; do cat PROMPT.md | <agent>; done` plus a completion check (tests pass or a COMPLETE tag); state lives on disk and git, each pass starts with a fresh context window.
- The one-item rule drives progress: one task per pass (highest-priority not-done story in `tasks.json` / `prd.json`), then commit and exit, so a crashed agent loses at most one task.
- Fresh context is the whole trick: long sessions rot as the window fills with chatter, so the loop refuses conversational memory and treats the repository as the memory.
- Packaged variants add iteration caps (budget control), typed stop tags (`COMPLETE` / `BLOCKED` / `DECIDE` with exit codes in `ralph.sh`), per-task verification stacks (typecheck + tests + lint), and multi-backend support.
- Ralph fits only "large, well-specified, mechanically verifiable" work (migrations, coverage backfill, refactors); Huntley himself would not use it on an existing codebase, and success criteria must be numbers.
- Cost is the loop's shadow: every pass re-pays input tokens for the full prompt (Thoughtworks flags "significant token cost"), so iteration caps are budget controls, and self-reported overnight wins ($297–$800 runs) are suggestive, not benchmarked.
- Producer and approver must be separate: the agent that writes code must not declare it good — hard gates (compiler, failing tests) beat soft gates (arguable reviewers), which beat pseudo-gates (self-grading).

---

## 1. The loop, stripped to its parts

The Ralph loop, popularized by Geoffrey Huntley in July 2025 and named after Ralph Wiggum ("deterministically simple in an unpredictable world"), is three things plus a rule:

1. **A prompt file** (`PROMPT.md`) holding the goal and the definition of done.
2. **A shell loop** re-running the same coding agent against that prompt: `while :; do cat PROMPT.md | claude -p --dangerously-skip-permissions; done`.
3. **A completion check** that decides when to stop: tests passing, a `COMPLETE` promise tag in output, or every story in a PRD (product requirements document) file reading `passes: true`.
4. **The one-item rule:** one task per pass, then commit and exit. Each pass starts with a **fresh context window** (the model's short-term memory is wiped); everything persistent — code, task list (`tasks.json` / `prd.json` / `progress.txt`), decisions — lives in files and git history.

## 2. Why forgetting works

Long agent sessions rot — the context window fills with the agent's own chatter, it forgets early instructions, quality decays. The loop refuses to carry memory in the conversation at all; the repository *is* the memory. Many forgetful agents, each slightly useful, accumulate into steady progress via git. Restart *is* the design: a crashed agent loses at most one task, so no watchdog is needed — the loop never expected the agent to survive.

## 3. What the packaged versions add

The bare one-liner is harness-agnostic by construction (bash around any headless CLI: `claude -p`, `codex exec`, `cursor-agent`, `aider --message`), which means zero lock-in but zero help. Packaged versions add what it lacks: iteration caps, real stop conditions (`COMPLETE` / `BLOCKED` / `DECIDE` tags with exit codes 0/1/2/3 in `ralph.sh`), per-task verification stacks (typecheck + tests + lint before a task counts as done), and multi-backend support (see ralphy in the micro-patterns page).

## 4. When it fits — and what it costs

Ralph fits "large, well-specified, mechanically verifiable" work: migrations, coverage backfill, refactors, overnight build-out. It does not fit fuzzy existing codebases — Huntley himself would not use it there. Success criteria must be numbers (tests, lint, types, coverage). Cost is the shadow: fresh context every pass re-pays input tokens each iteration (Thoughtworks: "significant token cost"); iteration caps are budget controls, not just correctness controls. Self-reported wins (CURSED language, $297–$800 overnight runs) come from the technique's advocates — treat as suggestive, not benchmarked.

## 5. The producer/approver split

The agent that writes code must not be the one that declares it good. Hard gates (compiler, failing tests) beat soft gates (reviewers you can argue with), which beat pseudo-gates (self-grading). Anthropic's generator/evaluator split and Bernstein's Janitor stage are instantiations of the same back-pressure idea. Ralph's reframing helps budgeting too: the loop is cheap, the *check* is where the money should go.

**Covers:** Ralph loop mechanics (prompt file, shell loop, completion check, one-item rule, fresh-context rationale), packaged-variant additions (caps, stop tags, verification stacks), fit criteria and token-cost caveats, producer/approver separation; sources: ralphloop.sh, futureagi, Wiegold, Osmani trends, Liu harness piece.
