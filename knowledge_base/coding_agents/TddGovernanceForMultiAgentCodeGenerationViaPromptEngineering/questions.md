---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: TDD Governance for Multi-Agent Code Generation via Prompt Engineering

### Q1. What problem does the paper's AI-native TDD framework address, and what is its core thesis?

> [!tip]- Answer
> > The framework addresses instability, non-determinism, and weak development discipline in unconstrained multi-agent LLM code generation, where small logic errors spread across the workflow. Its thesis is that encoding software engineering discipline directly into prompt orchestration — treating TDD as enforceable governance rather than auxiliary test inputs — improves stability and reproducibility. See [[wiki/01-tdd-governance-overview|TDD Governance for Multi-Agent Code Generation]].

### Q2. How does the layered architecture separate model proposal from deterministic engine authority?

> [!tip]- Answer
> > LLMs never write directly to the file system; they return structured patch proposals that must pass validation gates before application. An orchestrator controls phase order, checks test outcomes before transitions, and alone applies approved changes atomically, so generative variability does not become uncontrolled state change. See [[wiki/01-tdd-governance-overview|TDD Governance for Multi-Agent Code Generation]].

### Q3. What are the three observations that motivate enforceable TDD governance, per Section 2?

> [!tip]- Answer
> > First, classical TDD relies on disciplined phase ordering and test-backed refactoring (Beck/Fowler). Second, LLM engineering exhibits hallucinations, non-determinism (up to 75.76% zero equal test outputs on complex benchmarks), and reproducibility gaps. Third, test-guided prompting (TiCoder, TDFlow, WebApp1K) improves correctness without enforcing phase discipline as a governed protocol. See [[wiki/02-tdd-foundations-and-llm-instability|Beck's Formulation of TDD Operationalizes Development]].

### Q4. Why do prior test-guided prompting approaches fall short of full TDD discipline?

> [!tip]- Answer
> > Approaches like TiCoder, TDFlow sub-agents, Self-Refine, Chain-of-Thought, and static-analysis feedback improve correctness by using tests as executable specifications or feedback signals. However, they do not enforce phase ordering, minimal implementation, or bounded repair cycles across multi-agent workflows, leaving the open problem of translating TDD into governance-aware prompt structures. See [[wiki/02-tdd-foundations-and-llm-instability|Beck's Formulation of TDD Operationalizes Development]].

### Q5. What are the four principle categories in Table 1, and why were these principles selected for extraction?

> [!tip]- Answer
> > The categories are Order (test-first, Red→Green→Refactor), Granularity (minimal failing test, minimal passing code, one failing test at a time), Feedback quality (FAST, self-validating, timely tests with meaningful assertions), and Design hygiene (remove duplication, refactor continuously while green). They were selected because they are prescriptive must/should rules from a bounded Beck/Martin canon that humans accept yet commonly abandon under deadline pressure. See [[wiki/03-principle-extraction-and-manifesto|Principle Extraction and Manifesto]].

### Q6. How is each extracted TDD principle represented, and how does Figure 1 illustrate its translation into governance?

> [!tip]- Answer
> > Each principle becomes a structured record with a label, canonical quote (when available), human-era intent statement, and bibliographic pointer, later encoded as a JSON governance object with AI-native interpretation, operational constraints, and anti-patterns. Figure 1 shows three translations: pre-change failing tests (RED) for behavior changes, refactoring as a gated phase with full-suite regression, and FIRST quality via quantitative checks on speed, determinism, self-validation, and timeliness. See [[wiki/03-principle-extraction-and-manifesto|Principle Extraction and Manifesto]].

### Q7. What are the four validation gates applied before any mutation, and how is TDD discipline distributed across role-specific prompts?

> [!tip]- Answer
> > The four gates are structural validation (schema/content checks), policy enforcement (disallowed paths, directory restrictions), phase consistency checks (output matches expected phase), and optional human or rule-based approval in planner mode. Discipline is distributed across prompts: system (invariants, phase purity), planner (FAIL-then-PASS ordered steps), test generation (RED-only with meaningful assertions), implementation (minimal changes only), repair (minimal localized corrections), and review (no production edits, no invented requirements). See [[wiki/04-governed-workflow-and-architecture|Governance-Centric Architecture]].

### Q8. How does the bounded repair loop work, including the retry budget and early-termination conditions?

> [!tip]- Answer
> > Each GREEN step allows at most N = 3 repair attempts, bounding cost while preserving iterative recovery. A failure signature S = {exception type, failing tests, normalized message} is computed per iteration, and the loop terminates early if S repeats consecutively, a repair produces no effective code change, or proposals are semantically equivalent to prior attempts — or when tests pass or the cap is reached. See [[wiki/04-governed-workflow-and-architecture|Governance-Centric Architecture]].

### Q9. What are the framework's stated limitations and the trade-off around manifesto injection?

> [!tip]- Answer
> > Constraints are enforced primarily at the prompt level with only partial runtime verification, so full semantic compliance remains future work; the bounded-autonomy model may limit exploration in complex refactoring, and empirical validation is still preliminary. Scaling to large multi-module repositories needs more advanced planning and invariant enforcement, and manifesto injection must be balanced against token constraints (governance strength vs. prompt compactness). See [[wiki/05-discussion-limitations-and-outlook|Discussion, Limitations, and Outlook]].

### Q10. Should a team adopt this TDD-governance framework for production multi-agent code generation today?

> [!tip]- Answer
> > Adopt it as a promising pilot rather than a proven production standard: its process-level constraints (phase ordering, validation gates, bounded repair) plausibly reduce unstable retries and speculative code versus baseline prompting. But enforcement is still largely prompt-level, validation is preliminary, and repository-scale, cross-model, and CI/CD evidence is missing — so require measured evaluation of stability, defect rates, and auditability before committing regulated or large-repo workflows. See [[wiki/05-discussion-limitations-and-outlook|Discussion, Limitations, and Outlook]].
