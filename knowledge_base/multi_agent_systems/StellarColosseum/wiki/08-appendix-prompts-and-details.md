> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix: Prompts and Details — A Strategy with an Unresolved Fatal
**In one sentence:** A strategy with an unresolved fatal bridge can only proceed to decomposition under strict stability and explicit-obligation conditions, after which fixed prompts govern decomposition into a LaTeX skeleton with a dependency DAG, parallel subproblem solving with falser critique and aggregation, and global verification with conservative revision.
## Key points
- A strategy with an unresolved fatal bridge cannot be marked ready, but may proceed to decomposition only if the route and proof architecture are stable and every remaining obligation has a concrete proof or verification path.
- Minor obligations must each be assigned to an explicit proof or certificate section in the proof plan, while a major obligation — one that could force changing the route, reduced target, or core mechanism, or that has no clear repair path — sends the strategy back for further exploration.
- Decomposition output must return blocking issues, fatal bridge claims, theorem and criterion audits, hidden hard steps, minimal remaining obligations, obligation severity, whether decomposition is allowed, and the recommended next action.
- The decomposer produces a standalone LaTeX master-document skeleton (title, concise abstract, one section per subproblem with a specific roadmap and a reserved body location) plus an ordered subproblem list in topological order with dependency indices, and must not silently build on unresolved attacked claims.
- Each subproblem is solved by multiple solvers, critiqued by paired falsers, and combined through a tree aggregator, with retries supplied with the previous attempt and its criticism so progress is retained without hiding unresolved objections.
- Only an executed code probe counts as computational evidence; an unexecuted certificate may only be stated as a reduction, conditional result, or certificate plan with the stronger claim kept as an open obligation.
- A subproblem falser never repairs or rewrites: it classifies sections as ready (later assembly may rely on the result), conditional (useful progress but an explicit bridge or obligation is unresolved), or rejected (wrong target, false or constraint-dropping bridge), since any explicit gap precludes a ready verdict.
- The global verifier reads the entire assembled proof against the original problem (hypotheses, scope, conclusion, theorem uses, citations, computations, boundary cases, attacked/conditional claims), accepts only complete proofs, otherwise writes standalone actionable feedback localizing every material defect; revision is conservative (outline cleanup cannot add sections, reorder the plan, or introduce a new strategy) and code probes are adversarial checks only, never repairs.
---
## Readiness rule: strategies with an unresolved fatal
A strategy with an unresolved fatal bridge cannot be marked ready. It may still proceed to decomposition, but only if:
- the route and proof architecture are stable, and
- every remaining obligation has a concrete proof or verification path.

Verbatim rule:
> "Treat these as minor obligations and assign each to an explicit proof or certificate section in the proof plan."

> "An obligation is major if resolving it could require changing the route, reduced target, or core mechanism, or if it has no clear repair path. In such cases, return the strategy for further exploration."

The strategy report must return:
- blocking issues
- fatal bridge claims
- theorem and criterion audits
- hidden hard steps
- minimal remaining obligations
- obligation severity
- whether decomposition is allowed
- the recommended next action

## A.2 Decomposition into Subproblems
The decomposer turns an approved strategy into a LaTeX skeleton and a DAG (Directed Acyclic Graph — a dependency map with no cycles) of section-level subproblems. Each subproblem lists its earlier dependencies, allowing eligible independent sections to be solved in parallel.

Decomposer inputs (verbatim):
- `{problem}`
- `{knowledge directory, when available}`
- `{approved strategy card}`
- `{falser and readiness-gate reports}`
- `{previous decomposition, proof, and verifier feedback, when available}`

Decomposer instructions (verbatim in substance):
- "Break the original problem into a short list of subproblems in topological order. For each subproblem, list the indices of all earlier subproblems on which it depends."
- "Each subproblem should be mathematically meaningful, nontrivial, and useful for reaching the final proof. Avoid tiny bookkeeping steps."
- "Produce a standalone LaTeX master-document skeleton with a title, a concise abstract describing the proof plan, and one section per subproblem. Inside each section, write a short, mathematically specific roadmap and reserve a unique location for the future section body."
- "Return the master-document skeleton together with the same ordered list of subproblem titles, tasks, and dependency indices. Do not silently build on unresolved attacked claims. Isolate them as explicit subproblems, weaken them, or route around them."

A decomposition aggregator combines candidate skeletons and their subproblem DAGs into one plan. Unresolved bridge lemmas and certificate obligations must remain explicit in that plan.

## A.3 Subproblem Solving and Aggregation
For each subproblem, multiple solvers produce candidate sections, paired falsers critique them, and aggregators combine the candidates through a tree. On retry, the previous attempt and its criticism are supplied so useful progress is retained without hiding unresolved objections.

### Subproblem Solver
Inputs: `{problem and assigned subproblem}`, `{knowledge directory, when available}`, `{current master document}`, `{previous proof and global verifier feedback, when available}`, `{previous attempt and attached criticism, on retry}`, `{executed code-probe result, when available}`.

Verbatim duties:
- "Write the full LaTeX body that replaces this section's placeholder. Do not write a standalone document or repeat earlier sections. You may rely on prior sections only to the extent justified by their text."
- "Address every relevant error already identified by global feedback or a previous falser. If the section remains incomplete, mark the gap explicitly."
- "State exactly what theorem, lemma, reduction, or partial result the section establishes. Separately identify the bridge claims on which it depends and every obligation that remains unproved."
- "Mark the section as solved, partial, or blocked, and request a retry only for a concrete remaining defect."
- "Only an executed code probe counts as computational evidence. If a necessary certificate has not been executed, state only the reduction, conditional result, or certificate plan and retain the stronger claim as an open obligation."

### Subproblem Falser
Inputs: `{original problem}`, `{assigned subproblem}`, `{knowledge directory, when available}`, `{current master document}`, `{proposed section solution}`, `{previous falser report, when available}`.

Verbatim duties:
- "Do not repair or rewrite the section. Decide whether it actually proves the assigned subproblem."
- "Focus first on a fatal bridge: a false equivalence, wrong target, wrong-sided bound, dropped factor, missing constraint, index mismatch, unsupported theorem use, or code-probe misuse."
- "Audit every explicit open obligation and preserve earlier objections unless the new section resolves them."
- "Classify the section as ready, conditional, or rejected. Ready means later assembly may rely on the claimed result. Conditional means useful progress remains but an explicit bridge or obligation is unresolved."
- "Reject a section that proves the wrong target or relies on a false or constraint-dropping bridge. Any explicit gap precludes a ready verdict."
- "Return a concise summary, the fatal objections, and the claims that later stages must not treat as established."

### Subproblem Aggregator
Inputs: `{problem and assigned subproblem}`, `{knowledge directory, when available}`, `{(section solution, falser report) pairs for one subproblem}`, `{current master document}`, `{previous proof and global verifier feedback, when available}`.

Verbatim duties:
- "Synthesize the strongest single section replacement. Consume both each candidate solution and its attached falser report. Do not silently inherit an attacked claim: reject it, weaken it, repair it, or retain it as an open obligation."
- "The resulting section must remain compatible with the notation, assumptions, definitions, and established claims in the already-filled master document. It must not contain a section heading or document preamble."
- "Preserve incomplete but useful progress only with an explicit gap and a status of partial or blocked."
- "Return the synthesized section together with its claimed result, essential bridge claims, unresolved obligations, completion status, and any concrete reason that another attempt is needed."

## A.4 Global Verification and Revision
The global verifier reviews the assembled proof together with compact solver–falser audit cards. If the verifier rejects the proof, its feedback guides targeted outline or section revision, after which the proof is verified again.

### Global Verifier
Inputs: `{original problem}`, `{knowledge directory, when available}`, `{complete assembled proof}`, `{subproblem solver-falser audit cards}`.

Verbatim duties:
- "Evaluate the proof against the original problem, not merely for internal consistency. Read the entire proof from beginning to end even if a fatal gap appears early."
- "Check the exact hypotheses, scope, and conclusion, and audit theorem uses, citations, computations, boundary cases, and every claim attacked or left conditional in a subproblem audit card. A ready local verdict is not itself a proof."
- "If the proof is complete, accept it and preserve the complete document. Otherwise reject it and write a standalone, actionable feedback document that localizes every material defect."
- "Verifier code probes are adversarial checks only. Use them to test a claimed identity, bound, computation, or boundary case, never to repair the proof."

### Revision-Specific Instructions
Inputs: `{original problem}`, `{knowledge directory, when available}`, `{current proof, decomposition, and ordered subproblems}`, `{global verifier feedback}`, `{original section and task, for section revision}`.

Verbatim duties:
- "First identify every concrete mathematical issue in the global review."
- "For the outline cleanup, the allowed changes are to rewrite abstract or roadmap material, slightly revise section names and tasks, and delete redundant, empty, harmful, or superseded sections. Do not add sections, invent placeholder tokens, reorder the surviving plan, or introduce a new proof strategy."
- "For a section revision, fix every review issue that affects that section. Keep material that is already correct and do not rewrite merely for style."
- "Preserve the paragraph order, displayed equations, named environments, and LaTeX labels unless the review gives a concrete mathematical reason to change them. Mark any remaining gap explicitly."
- "Return either a conservatively revised outline or a revised section body, as appropriate. Candidate revisions are aggregated before the proof is reassembled and verified again."

**Covers:** Readiness rule for strategies with an unresolved fatal bridge + Appendix A.2–A.4 (pp. 24–27): decomposition, subproblem solving/aggregation, global verification and revision prompts.
