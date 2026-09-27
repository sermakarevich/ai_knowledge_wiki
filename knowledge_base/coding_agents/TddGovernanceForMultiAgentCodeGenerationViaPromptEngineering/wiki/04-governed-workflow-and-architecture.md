> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Governance-Centric Architecture

**In one sentence:** Beyond sequential phase ordering, the system enforces TDD through a governance-centric architecture in which non-authoritative LLM patch proposals are checked by validation gates and role-specific prompt constraints before the orchestration engine alone applies them atomically, with bounded repair loops.

## Key points
- Language models never write directly to the file system; they return structured patch proposals that pass validation gates before application, and all file mutations are performed exclusively by the orchestration engine after validation.
- A structured TDD manifesto encodes extracted principles as declarative constraints that inform prompt construction, validation rules, and phase enforcement logic, serving as the conceptual contract between TDD theory and runtime orchestration.
- Before any mutation, outputs undergo four gates: (1) structural validation (schema and content checks), (2) policy enforcement (e.g., disallowed paths, directory restrictions), (3) phase consistency checks (outputs match the expected phase), and (4) optional human or rule-based approval (in planner mode); only then are changes applied atomically.
- TDD discipline emerges from coordinated constraints distributed across role-specific prompts: system prompt (governance invariants, structured output, phase purity), planner (ordered steps with expected FAIL-then-PASS outcomes), test generation (RED-only test files with meaningful assertions), implementation (minimal changes, no unrelated features), failure repair (structured failure context, minimal localized corrections), and review (no production edits during test review, no over-specification or invented requirements).
- Each GREEN step allows at most N = 3 repair attempts, a fixed retry budget bounding cost while preserving iterative recovery.
- A failure signature S = {exception type, failing tests, normalized message} is computed per iteration, and the loop terminates early if the same S repeats in consecutive iterations, a repair produces no effective code change (via patch comparison), or proposals are semantically equivalent to prior attempts; execution also terminates when tests pass or the iteration cap is reached.
- Extracted principles map to enforcement mechanisms: test-first via planner-ordered steps plus engine-level FAIL gating; minimal implementation via prompt scope restrictions plus engine rejection of no-op or unrelated changes; behavior preservation via post-apply test gates plus automatic rollback during refactoring on failure; controlled refactoring only after passing tests with validation forbidding feature modification or test edits.

---

## Governance-centric architecture: separation of generative autonomy from state authority

The system is designed around a governance-centric architecture that separates generative autonomy from state authority. Language models never directly write to the file system; instead, they return structured patch proposals subject to validation gates prior to application. This separation ensures that "generative variability does not directly translate into uncontrolled state changes" (Figure 2).

## TDD manifesto as declarative constraints

The system incorporates a structured TDD manifesto that encodes extracted principles as declarative constraints. These constraints inform prompt construction, validation rules, and phase enforcement logic, serving as the conceptual contract between TDD theory and runtime orchestration.

## Validation gates before mutation

Before any mutations occur, outputs undergo:

| # | Gate | Content |
|---|---|---|
| 1 | Structural validation | Schema and content checks |
| 2 | Policy enforcement | E.g., disallowed paths, directory restrictions |
| 3 | Phase consistency checks | Ensuring outputs match the expected phase |
| 4 | Optional approval | Human or rule-based approval (in planner mode) |

Only after passing these gates are changes applied atomically.

## Figure 2: governed AI-native TDD workflow

Figure 2 ("Governed AI-native TDD workflow with separation between non-authoritative proposal generation and authoritative execution") illustrates the end-to-end flow: user requirements and TDD manifesto constraints are inputs; the proposal layer generates an execution plan through the planner; during RED, failing tests are proposed; during GREEN, implementation proposals (code patches) are generated; all proposals are routed through the engine governance layer (schema validation, policy enforcement, phase-consistency checks); approved proposals go through a deterministic test run; on failure control returns to the proposal layer for bounded repair iterations, otherwise validated changes are atomically committed to the workspace.

## Prompt distribution across agent roles

TDD discipline is not encoded in a single instruction but emerges from coordinated constraints distributed across role-specific prompts:

| Prompt | Constraint |
|---|---|
| System | Governance invariants, structured output requirements, phase purity |
| Planner | Decomposes specification into ordered steps with expected test outcomes (e.g., FAIL then PASS), encoding test-first progression and constraining phase transitions |
| Test generation | Enforces RED-phase constraints, restricting output to test files and requiring meaningful assertions aligned with the specification |
| Implementation | Restricts synthesis to minimal changes necessary to satisfy failing tests; forbids unrelated feature additions |
| Failure repair | Injects structured failure context (e.g., failure category and test output); enforces minimal, localized corrections |
| Review | Acts as quality gate, prohibiting production edits during test review and preventing over-specification or invented requirements |

Through this distribution, classical TDD properties — test-first execution, minimal implementation, and behavior preservation — are enforced at both prompt and engine levels.

## Bounded repair and loop control

Repair is governed by explicit termination policies to ensure convergence. Each GREEN step allows at most N = 3 repair attempts. A failure signature S = {exception type, failing tests, normalized message} is computed per iteration. The loop terminates early if (1) the same S repeats in consecutive iterations, (2) a repair produces no effective code change (detected via patch comparison), or (3) proposals are semantically equivalent to prior attempts. Execution also terminates when tests pass or the iteration cap is reached. These constraints ensure bounded, reproducible repair behavior.

## From principles to enforceable mechanisms

The extracted TDD principles are translated into concrete enforcement mechanisms:

- Test-first development: planner-ordered steps and engine-level FAIL gating, preventing code generation before failing tests exist.
- Minimal implementation: prompt-level scope restrictions and engine rejection of no-op or unrelated changes.
- Behavior preservation: post-apply test execution gates and automatic rollback during refactoring if tests fail.
- Controlled refactoring: permitted only after successful test passes, subject to validation that forbids feature modification or test edits.

Importantly, these guarantees arise from the interaction between prompt constraints and deterministic validation rules. TDD is therefore "not advisory but operationalized as a distributed governance protocol."

**Covers:** Red-Green-Refactor orchestration, proposal/engine separation, validation gates, role prompts, bounded repair
