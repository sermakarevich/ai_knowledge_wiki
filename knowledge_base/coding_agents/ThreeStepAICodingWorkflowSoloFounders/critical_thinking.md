> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder)

## Claims vs. evidence
- Claim: rushing context is the core failure mode, and slowing down speeds everything up.
  Evidence: anecdotal but coherent — a vague one-liner plus clarifying answers yields a usable PRD and task list in the demo.
  Gap: no baseline comparison (fast vs. slow prompting on the same feature), so magnitude is unproven.
- Claim: the PRD → task list → one-subtask-at-a-time loop reliably builds ~10,000-line features solo.
  Evidence: one demonstrated subtask (Prisma schema edit) plus self-report; no diffs, no failure cases, no second project.
  Gap: "reliably" and "almost never had trouble" rest on a single narrator with no independent check.
- Claim: human-in-the-loop checks plus commit-after-workable-parent-task keeps work recoverable.
  Evidence: the revert heuristic ("how bad would it be to undo") is sensible, but a half-day commit cadence is asserted, not shown.
- Claim: coaching-style prompting ("please think harder, I believe you can do this") recovers stuck agents.
  Evidence: asserted twice, never compared against a terse retry or a fresh subtask prompt.
- Claim: politeness works because models train on human output.
  Evidence: folk theory only; no mechanism, citation, or test offered in the digest or wiki.

## Genuinely new vs. repackaged
- Genuinely useful specifics worth copying:
  - Dot-notation clarifying questions (2.1, 2.2) so answers stay addressable instead of bundled bullets.
  - "Suitable for a junior developer" framing to force concreteness and stop the model assuming obvious details.
  - "You pick / make your best judgment" default so open questions do not stall the loop.
  - A "relevant files" section in the task list grounding each plan in the actual codebase.
  - One-subtask-then-stop with a "y" go-ahead, plus immediate check-off before continuing.
- Repackaged fundamentals: PRD → work breakdown → incremental implementation is standard product engineering.
  Markdown checkboxes, small commits, and agent-mode file mentions predate this workflow.
- The three Cursor rule files are process-as-prompt, not new technology; the Taskmaster CLI contrast
  ("less power, more control") reframes lighter automation as a virtue, which is positioning rather than proof.
- Context tooling (Postgres MCP row checks, Browserbase/Stagehand browser driving,
  Repo Prompt shrinking ~395k/324k tokens to ~12k) is tool selection, not workflow invention —
  though those token numbers are the most concrete datum in the whole piece.
- The "start with markdown, graduate to PM tools later" advice is pragmatic staging, not a discovery.

## Weaknesses and blind spots
- N=1 demo on a toy yacht-club CRM: no evidence the loop survives legacy code, auth, migrations,
  concurrency, flaky tests, or production incidents.
- Model and cost fragility: Claude 3.7 Sonnet Max, Gemini 2.5 Pro Max (~$300–400/month), o3 fallback.
  No account of what breaks when models rotate, rate-limit, or regress on instruction-following.
- Quality gates are thin: "small linter errors" are acknowledged, but tests, type checks, security review,
  schema-migration discipline, and acceptance criteria beyond "workable state" are absent.
- Human bottleneck unexamined: per-subtask "y" approvals scale poorly to 10k lines;
  fatigue and rubber-stamping go unmentioned, as does review quality at midnight.
- Context rot: PRD, task list, and code can drift over a half-day run, with no rule for re-syncing
  the plan when the agent improvises or a subtask expands scope.
- MCP trust gap: chat-driven Postgres queries and cloud-browser actions raise permission, audit,
  and destructive-action questions (writes? prod data? credentials?) the material never addresses.
- Survivorship bias: rabbit holes "without the process" are admitted, but no revert story,
  failed feature, or abandoned PRD is ever shown, so the failure rate is unknowable.
- Single-model stickiness ("learn one model's quirks") trades portability for comfort
  and leaves no exit plan when the chosen model changes behavior.

## Applicability
- Fits best: greenfield CRUD features, solo builders, Cursor users, and well-scoped additions
  (reports, schema fields, small flows) where a checkboxed plan maps cleanly onto files.
- Fits poorly: multi-engineer coordination, regulated or safety-critical code, deep refactors,
  performance work, and anything requiring migration safety or rigorous verification.
- **Relevance to my work**
  - AI/ML engineering: adopt dot-notation Q&A and the relevant-files block for experiment and pipeline specs;
    add eval or test gates per parent task before letting this loop near training or serving code.
  - Agentic systems: the one-subtask-at-a-time plus stop-and-confirm pattern is a usable scaffold for agent runners;
    gate DB/browser tool calls behind scoped credentials, dry-run modes, and audit logs first.
  - Elisity data platform: promising for boilerplate (schemas, reports, connectors) with Repo Prompt-style token budgets;
    but PRDs must add data contracts, migration/backfill plans, idempotency notes, and rollback criteria the video template lacks.

## What this changes
- Changes little about what to build, but offers a concrete discipline for how:
  force clarifying questions, write the PRD down, decompose before coding, execute in small verifiable steps.
- The durable artifacts are the checkable task list and the relevant-files list, not the chat transcript —
  they make agent work reviewable weeks later, which raw vibe-coding does not.
- The explicit-context habit (Repo Prompt file selection over Cursor's background "magic") is worth copying
  even outside Cursor, especially for large repos where whole-repo pastes waste tokens.
- It does not remove the need for tests, review, or ops judgment; it sequences the work so those gates
  have clear insertion points — but the gates themselves still must be built.
- Net effect: lowers the floor for solo founders shipping CRUD, without raising the ceiling on engineering rigor.

## Verdict
- Steal the mechanics, not the mythology: the loop is sensible process hygiene,
  but the 10k-lines-solo and coaching-prompt claims outrun the evidence presented.
- Trial it on one small, non-critical feature with added per-task test and commit gates;
  track rework rate and approval fatigue before trusting it on platform-critical paths.
- **trial**
