> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# TDD Governance for Multi-Agent Code Generation via Prompt Engineering — In Plain Language

## What is this about?

Imagine hiring a team of very fast but impulsive programmers. They write code
at lightning speed, but each one improvises, ignores the plan, and rarely
checks their work against yours. This paper is about giving that team a strict
but fair foreman.

The authors take a classic human discipline — Test-Driven Development (TDD) —
and turn it into enforceable rules for teams of AI coding agents.

In classic TDD, the rhythm is simple: write a failing test first (Red), write
just enough code to pass it (Green), then tidy up without breaking anything
(Refactor). Humans know this rhythm works, but often skip it under deadline
pressure because it feels slower.

The paper's idea: don't just *suggest* this discipline to AI agents in a
prompt — *enforce* it with machinery. A machine-readable rulebook (a "TDD
manifesto") is spread across every agent role, and a deterministic orchestrator
engine controls who acts when, checks test results before allowing the next
step, and applies code changes itself.

## Why does it matter?

AI code generators are powerful but shaky. The same prompt can produce
different code on different runs — on complex benchmarks, up to three-quarters
of repeated runs share zero identical test outputs. Setting the model's
"temperature" to zero does not fix this.

In a multi-agent setup the problem compounds: one agent's small logic error
gets passed along, and the next agent builds on it. The result is fast output
that is hard to reproduce, hard to trust, and prone to speculative extras —
features nobody asked for.

Earlier approaches already use tests to help AI code better (for example,
feeding tests into the prompt or using them to score the result). But they
treat tests as helpful hints or after-the-fact grades, not as traffic lights
that control the workflow. This paper argues the discipline itself — the
order of steps, the small batch sizes, the bounded retries — is what needs
to be enforced.

## How does it work?

Think of it as separation of powers: agents propose, the engine disposes.

First, the fragile human rules most often dropped under pressure are written
down. The authors limit themselves to the classic Kent Beck / Robert C. Martin
books and sort the rules into four buckets: Order (test first, Red-Green-
Refactor), Granularity (one small failing test and minimal passing code at a
time), Feedback quality (tests must be fast, independent, repeatable,
self-checking, timely, with real assertions), and Design hygiene (remove
duplication, refactor continuously while tests are green).

Each rule becomes a structured record — a label, what it originally meant for
humans, how to interpret it for AI, the concrete constraints, and the
anti-patterns to forbid. Together these records form the TDD manifesto.

Then the manifesto is put to work in two places at once:

1. **In the prompts.** Every agent role gets tailored constraints. The planner
   must output ordered steps with expected FAIL-then-PASS outcomes. The test
   writer may only touch test files and must include meaningful assertions.
   The coder may only make minimal changes — no bonus features. The repair
   agent gets the structured failure log and must fix locally. The reviewer
   checks tests without editing production code or inventing requirements.

2. **In the engine.** AI models never touch files directly. They submit
   structured patch proposals that pass four gates before anything changes:
   structural checks (is the patch well-formed?), policy checks (allowed
   paths?), phase checks (is this output right for the current phase?), and
   optional human or rule approval. Only then does the engine apply the
   change atomically — all at once or not at all.

Repair is deliberately bounded. Each fix step gets at most 3 attempts. The
engine fingerprints each failure (error type, failing tests, normalized
message) and stops early if the same failure repeats, if a "fix" changes
nothing, or if proposals are just rewordings of earlier tries. Refactoring is
allowed only while all tests pass, and any failure triggers automatic rollback.

## Where can this be used?

Anywhere teams let AI agents write code with minimal supervision and need the
result to be stable and auditable:

- Multi-agent coding pipelines where planner, writer, fixer, and reviewer
  agents collaborate on one codebase.
- CI/CD-integrated AI development, where reproducibility and defect rates
  matter more than raw generation speed.
- Regulated domains (finance, health, safety-critical software) where every
  change should be traceable to a test and applied through a gated process.
- Large or legacy codebases where speculative extra code and untested edits
  are especially costly — though the authors note scaling there still needs
  stronger planning and is future work.
- Teams calibrating strictness: the authors envision configurable governance
  levels, strict for critical paths and lighter for prototypes.

## Conclusions & takeaways

- Prompt engineering here is not clever phrasing — it is encoding process
  invariants (order, small steps, bounded retries) so AI teams cannot
  silently skip them.
- Separating "who suggests" (models) from "who changes files" (the engine)
  stops random model variation from becoming random codebase damage.
- Bounded repair (max 3 tries plus duplicate detection) trades a little
  exploratory freedom for much better reproducibility and cost control.
- Early, still preliminary results: fewer unstable retry loops and less
  speculative code than baseline prompting — but enforcement is mostly at
  the prompt level so far, and repository-scale, cross-model validation in
  real CI/CD pipelines is still to come.
- The honest trade-off: stronger governance costs prompt tokens and can
  constrain creative refactoring; teams will need to tune strictness to
  the project's complexity.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| TDD (Test-Driven Development) | Write the test before the code, so "done" is defined up front. |
| Red–Green–Refactor | The TDD loop: failing test (Red), minimal fix (Green), tidy up (Refactor). |
| Multi-agent code generation | Several specialized AI agents (planner, coder, fixer) splitting up the job. |
| Prompt engineering | Writing the instructions that steer an AI model toward desired behavior. |
| Governance / guardrails | Automatic rules and checks that keep AI work inside safe bounds. |
| Manifesto (TDD manifesto) | The machine-readable rulebook of TDD principles used to build prompts and checks. |
| Orchestrator / engine | The deterministic boss program that orders phases and applies file changes. |
| Validation gate | A checkpoint a proposal must pass (format, policy, phase) before it is applied. |
| Atomic mutation control | Code changes are applied all-at-once by the engine, never half-written by agents. |
| Bounded repair loop | Fixing is capped (here: 3 tries) with early stop on repeated or empty fixes. |
