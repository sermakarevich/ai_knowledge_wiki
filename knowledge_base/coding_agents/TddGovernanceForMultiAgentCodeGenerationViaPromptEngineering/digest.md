> [[index|Wiki]] | [[summary|Summary]]

# TDD Governance for Multi-Agent Code Generation via Prompt Engineering — Digest

## 1. [[wiki/01-tdd-governance-overview|TDD Governance for Multi-Agent Code Generation]]

**In one sentence:** The paper proposes an AI-native TDD framework that turns classical Red-Green-Refactor principles into enforceable prompt-level and workflow-level governance (phase ordering, bounded repair loops, validation gates, atomic mutation control) to make multi-agent LLM code generation more stable and reproducible.

## Key points

- LLMs accelerate software development but exhibit instability, non-determinism, and weak adherence to development discipline in unconstrained workflows.
- Existing LLM-based approaches typically use tests as auxiliary inputs rather than enforceable process constraints; this work treats TDD as governance instead.
- Extracted TDD principles are formalized in a machine-readable manifesto and distributed across planning, generation, repair, and validation stages.
- The layered architecture separates model proposal from deterministic engine authority, with an orchestrator controlling phase order and test-outcome checks before transitions.
- Enforcement mechanisms named in the framing are phase ordering, bounded repair loops, validation gates, and atomic mutation control.
- Even identical prompts often produce different outputs, and a temperature of zero does not ensure consistent results; in multi-agent settings small logic errors can spread across the workflow.
- Classical TDD (via Extreme Programming) defines correctness in advance by writing tests before implementation, but is demanding and can reduce productivity during adoption; LLMs generating repetitive test code are presented as a practical complement.

## 2. [[wiki/02-tdd-foundations-and-llm-instability|Beck's Formulation of TDD Operationalizes Development]]

**In one sentence:** Classical TDD (Beck/Fowler) treats tests as an explicit control mechanism for incremental change via test-first micro-iterations, minimal implementation, and behavior-preserving refactoring, while LLM code generation remains unstable and test-guided prompting improves correctness without enforcing full TDD phase discipline — motivating enforceable, governance-aware prompt structures derived from a bounded Beck/Martin canon.

## Key points

- Beck's TDD operationalizes development as micro-iterations where tests specify behavior before implementation, encourage minimal solutions, and require continuous refactoring after reaching a passing state [1].
- Fowler's refactoring catalog defines safe structural transformations and makes automated tests the prerequisite for verifying behavior preservation [6]; together they frame tests as a control mechanism for incremental design change.
- LLM synthesis fails through contextual dependency errors, insufficient grounding, overconfident interpolation [23], prompt sensitivity, and non-determinism with "zero equal test outputs in up to 75.76% of cases on complex benchmarks" [15].
- Correct-looking LLM code may still fail in clean environments from dependency/configuration issues [21], and retrieval augmentation only reduces hallucinations — reliability depends on prompt context quality as well as model capability.
- Test-guided prompting (TiCoder [5], TDFlow sub-agents [8], WebApp1K [3], test-first interaction guidance [16]) and structured loops (Self-Refine [11], Chain-of-Thought [18], static-analysis feedback [9]) improve correctness but do not enforce phase ordering, minimal implementation, or bounded repair as a governed protocol.
- The chunk's three-observation summary is: (1) classical TDD relies on disciplined phase ordering and test-backed refactoring [1, 6]; (2) LLM engineering exhibits hallucinations, non-determinism, and reproducibility gaps [10, 15, 21, 23]; (3) test-guided prompting improves correctness without enforcing full TDD discipline [3, 5, 8, 14, 16].
- The stated open problem is translating classical TDD into "enforceable, governance-aware prompt structures that ensure bounded autonomy and phase discipline across multi-agent workflows," addressed by the Section 3 framework via deterministic validation, bounded repair, and engine-controlled state mutation.
- Principle extraction is bounded to Beck [1] and Martin [12, 13], selects only prescriptive must/should rules that commonly break under deadline pressure, and encodes each as a JSON governance object with identifier, title, original intent, AI-native interpretation, operational constraints, and anti-patterns.

## 3. [[wiki/03-principle-extraction-and-manifesto|Principle Extraction and Manifesto]]

**In one sentence:** The paper extracts a bounded canonical TDD corpus of historically "right" but economically fragile human-era principles — organized into order, granularity, feedback quality, and design hygiene — and represents each as a structured record (label, canonical quote, intent, bibliographic pointer) to be translated into AI-native governance rules.

## Key points

- Four principle categories are defined in Table 1: Order (Test-first, Red→Green→Refactor), Granularity (minimal failing test, minimal passing code, one failing test at a time), Feedback quality (FAST, independent, repeatable, self-validating, timely tests with meaningful assertions), and Design hygiene (remove duplication, refactor continuously while green) [2, 19].
- Each category has a typical human-era failure mode: "just code it" feels faster than front-loaded thinking; batching reduces perceived overhead but increases hidden risk; slow/flaky suites and weak tests become socially tolerated to ship; delayed invisible refactor benefits make refactoring optional.
- The extracted set intentionally over-represents principles humans find hard to sustain: "run tests constantly" and "refactor as a required step" are accepted but abandoned because short-term cost is salient while benefit is delayed.
- "Tests must be self-validating" is accepted in principle, yet humans commonly ship weak (or non-assertive) tests because they are faster to write.
- The extraction targets known failure points of human-era TDD: principles requiring repeated, immediate investment to preserve long-term optionality.
- Each principle becomes a structured record with label, canonical quote (when available), human-era intent statement, and bibliographic pointer, designed as input for translating human-era discipline into enforceable AI-native governance rules.
- Figure 1 illustrates three enforceable governance principles: requiring pre-change failing tests (RED) for behavior modifications, treating refactoring as a gated phase with full-suite regression and duplication controls, and operationalizing FIRST test quality via quantitative checks for speed, determinism, self-validation, and timeliness.

## 4. [[wiki/04-governed-workflow-and-architecture|Governance-Centric Architecture]]

**In one sentence:** Beyond sequential phase ordering, the system enforces TDD through a governance-centric architecture in which non-authoritative LLM patch proposals are checked by validation gates and role-specific prompt constraints before the orchestration engine alone applies them atomically, with bounded repair loops.

## Key points

- Language models never write directly to the file system; they return structured patch proposals that pass validation gates before application, and all file mutations are performed exclusively by the orchestration engine after validation.
- A structured TDD manifesto encodes extracted principles as declarative constraints that inform prompt construction, validation rules, and phase enforcement logic, serving as the conceptual contract between TDD theory and runtime orchestration.
- Before any mutation, outputs undergo four gates: (1) structural validation (schema and content checks), (2) policy enforcement (e.g., disallowed paths, directory restrictions), (3) phase consistency checks (outputs match the expected phase), and (4) optional human or rule-based approval (in planner mode); only then are changes applied atomically.
- TDD discipline emerges from coordinated constraints distributed across role-specific prompts: system prompt (governance invariants, structured output, phase purity), planner (ordered steps with expected FAIL-then-PASS outcomes), test generation (RED-only test files with meaningful assertions), implementation (minimal changes, no unrelated features), failure repair (structured failure context, minimal localized corrections), and review (no production edits during test review, no over-specification or invented requirements).
- Each GREEN step allows at most N = 3 repair attempts, a fixed retry budget bounding cost while preserving iterative recovery.
- A failure signature S = {exception type, failing tests, normalized message} is computed per iteration, and the loop terminates early if the same S repeats in consecutive iterations, a repair produces no effective code change (via patch comparison), or proposals are semantically equivalent to prior attempts; execution also terminates when tests pass or the iteration cap is reached.
- Extracted principles map to enforcement mechanisms: test-first via planner-ordered steps plus engine-level FAIL gating; minimal implementation via prompt scope restrictions plus engine rejection of no-op or unrelated changes; behavior preservation via post-apply test gates plus automatic rollback during refactoring on failure; controlled refactoring only after passing tests with validation forbidding feature modification or test edits.

## 5. [[wiki/05-discussion-limitations-and-outlook|Discussion, Limitations, and Outlook]]

**In one sentence:** Unlike approaches treating tests as auxiliary inputs or evaluation metrics, the framework encodes TDD as a process-level constraint architecture whose explicit phase ordering, validation gating, and bounded repair improve stability and reproducibility but remain prompt-level, preliminary, and in need of repository-scale validation.

## Key points

- TDD is encoded as a process-level constraint architecture — phase ordering, validation gating, bounded repair, and state authority integrated into the generative loop — rather than as auxiliary test inputs or post-hoc evaluation metrics.
- Proposal generation is separated from state mutation and TDD principles are distributed across planner, generation, repair, and validation stages, reducing uncontrolled iteration and LLM-driven instability.
- Bounded repair loops plus deterministic validation gates improve reproducibility, while the structured TDD manifesto acts as a runtime constraint preserving behavioral safety during iterative synthesis.
- Current constraints are enforced primarily at the prompt level with only partial runtime verification, leaving full semantic compliance as future work.
- The bounded-autonomy model stabilizes execution but may limit exploration in complex refactoring scenarios, and scaling to large multi-module repositories with complex dependencies needs more advanced planning and invariant enforcement.
- Empirical validation is preliminary: explicit phase separation and validation gating appear to reduce unstable retry cycles versus baseline prompting, and test-first ordering with minimal implementation appears to limit speculative code and unnecessary feature expansion.
- Manifesto injection must be balanced against token constraints, a trade-off between governance strength and prompt compactness.
- Planned future work covers repository-scale industrial evaluation including CI/CD integration (stability, defect rates, reproducibility), configurable governance levels calibrated to project complexity, and auditable AI-assisted development for regulated domains.

## The argument in five moves

1. Unconstrained multi-agent LLM code generation is fast but unstable, non-deterministic, and prone to error propagation, so it needs automated guardrails.
2. Classical TDD already supplies the needed discipline — test-first micro-iterations, minimal implementation, and test-backed refactoring — but prior test-guided LLM prompting improves correctness without enforcing that phase discipline.
3. The fragile human-era TDD rules most often dropped under pressure (order, granularity, feedback quality, design hygiene) are therefore extracted from a bounded Beck/Martin canon into a machine-readable manifesto of declarative constraints.
4. Those constraints are operationalized as a distributed governance protocol: role-specific prompts plus an authoritative orchestration engine with validation gates, atomic mutation control, and bounded (N = 3, signature-deduplicated) repair loops.
5. This turns prompt engineering into process-invariant enforcement that preliminarily improves stability and reproducibility, while remaining prompt-level and requiring repository-scale, CI/CD, and configurable-governance validation in future work.
