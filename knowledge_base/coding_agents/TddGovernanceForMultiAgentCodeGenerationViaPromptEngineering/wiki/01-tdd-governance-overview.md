> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# TDD Governance for Multi-Agent Code Generation

**In one sentence:** The paper proposes an AI-native TDD framework that turns classical Red-Green-Refactor principles into enforceable prompt-level and workflow-level governance (phase ordering, bounded repair loops, validation gates, atomic mutation control) to make multi-agent LLM code generation more stable and reproducible.

## Key points

- LLMs accelerate software development but exhibit instability, non-determinism, and weak adherence to development discipline in unconstrained workflows.
- Existing LLM-based approaches typically use tests as auxiliary inputs rather than enforceable process constraints; this work treats TDD as governance instead.
- Extracted TDD principles are formalized in a machine-readable manifesto and distributed across planning, generation, repair, and validation stages.
- The layered architecture separates model proposal from deterministic engine authority, with an orchestrator controlling phase order and test-outcome checks before transitions.
- Enforcement mechanisms named in the framing are phase ordering, bounded repair loops, validation gates, and atomic mutation control.
- Even identical prompts often produce different outputs, and a temperature of zero does not ensure consistent results; in multi-agent settings small logic errors can spread across the workflow.
- Classical TDD (via Extreme Programming) defines correctness in advance by writing tests before implementation, but is demanding and can reduce productivity during adoption; LLMs generating repetitive test code are presented as a practical complement.

---

## Paper identity

| Item | Value |
|---|---|
| Title | TDD Governance for Multi-Agent Code Generation via Prompt Engineering |
| Authors | Tarlan Hasanli, Shahbaz Siddeeq, Bishwash Khanal, Pyry Kotilainen, Tommi Mikkonen, Pekka Abrahamsson (Hasanli and Siddeeq contributed equally) |
| Affiliations | University of Jyväskylä; Tampere University |
| Preprint | arXiv:2604.26615v1 [cs.SE] 29 Apr 2026 |
| Venue | Proceedings of the 30th International Conference on Evaluation and Assessment in Software Engineering (EASE 2026), 9–12 June 2026, Glasgow, Scotland, United Kingdom; 5 pages |
| CCS Concepts | Software and its engineering → Software development techniques; Automatic programming; Computing methodologies → Artificial intelligence; Machine learning |
| Keywords | Test-Driven Development, Large Language Models, Multi-Agent Systems, Prompt Engineering, Software Engineering Governance |

**Covers:** Title page + Abstract + Section 1 Introduction (partial, up to agentic-AI guardrails sentence)

## Abstract claims

- Problem: LLMs accelerate development "but often exhibit instability, non-determinism, and weak adherence to development discipline in unconstrained workflows."
- Gap: "existing LLM-based approaches typically use tests as auxiliary inputs rather than enforceable process constraints."
- Proposal: "an AI-native TDD framework that operationalizes classical TDD principles as structured prompt-level and workflow-level governance mechanisms."
- Mechanism: "Extracted principles are formalized in a machine-readable manifesto and distributed across planning, generation, repair, and validation stages within a layered architecture that separates model proposal from deterministic engine authority."
- Controls: "The system enforces phase ordering, bounded repair loops, validation gates, and atomic mutation control to improve stability and reproducibility."
- Thesis: "encoding software engineering discipline directly into prompt orchestration ... offers a promising direction for reliable LLM-assisted development."

## Introduction: why governance is needed

- Shift: "autonomous LLM-based agents take on complex coding tasks" with "role-specific agents collaborat[ing] to achieve programming goals with limited human intervention."
- Instability: "LLMs remain non-deterministic. Even identical prompts often produce different outputs, and a temperature of zero does not ensure consistent results."
- Multi-agent risk: "small logic errors can spread across the workflow, which makes automated guardrails essential for code quality and reliability."
- TDD background: "introduced through Extreme Programming, where tests are written before implementation so correctness is defined in advance."
- Adoption cost: "TDD can be demanding because developers must maintain both design intent and detailed test logic, which often reduces productivity during adoption."
- Complement: "TDD provides clear pass or fail constraints, and LLMs can generate much of the repetitive test code that developers often find tedious."
- Framework sketch: "Specialized agents follow explicit guidance, and an orchestrator controls phase order and checks test outcomes before transitions. It also limits repair loops."

**Covers:** Abstract through Introduction opening (chunk 01 of 5; ends mid-sentence at "This section reviews the empirical evidence that motivates encod-")
