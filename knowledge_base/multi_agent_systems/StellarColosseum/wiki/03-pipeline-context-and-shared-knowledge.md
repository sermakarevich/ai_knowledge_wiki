> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Pipeline Context and Shared Knowledge
**In one sentence:** Information produced earlier in the pipeline stays available to later stages — within a round (strategy, proof plan, section bodies, verifier findings), across rounds (rejected draft plus verifier feedback, plus a shared knowledge directory of reusable results), and Section 4.3 describes these two forms of cross-round memory.
## Key points
- Within a round, later stages can use the current strategy, the sectioned proof plan, completed section bodies, and verifier findings.
- Across rounds, a rejected proof draft and its verifier feedback are passed directly into the next attempt, so the next round does not start from the original problem alone.
- Cross-round memory has two complementary forms: the full latest proof attempt (grounds the next round in what was actually tried) and a shared knowledge directory (preserves reusable findings that aggregation might otherwise discard).
- The decomposer produces a numbered, sectioned proof skeleton with dependency edges forming a directed acyclic graph (DAG); document order controls exposition while the dependency graph controls the order work can proceed.
- A subproblem becomes eligible once its dependencies are completed, independent sections are solved in parallel, and each retry is local — completed work elsewhere in the dependency graph is preserved.
- Global verification reads the original problem plus the completed document as one argument, uses local subproblem reviews as audit context, and rejects on a single concrete fatal defect (not a majority vote).
- The knowledge curator records four reusable kinds: (1) theorems and lemmas, (2) failed approaches, (3) references, (4) observations — each entry retaining its source and caveats, updated across rounds.
---
## 3.3 Context across Stages
**Covers:** Section 3.3 (chunk lines 3–8)

> "Information produced earlier in the pipeline remains available to later stages. Within a round, this includes the current strategy, sectioned proof plan, completed section bodies, and verifier findings. Across rounds, a rejected proof draft and its verifier feedback are passed directly into the next attempt. A shared knowledge directory further retains reusable results from the wider search. Section 4.3 describes these two forms of cross-round memory."

| Scope | What is carried forward |
|---|---|
| Within a round | Current strategy; sectioned proof plan; completed section bodies; verifier findings |
| Across rounds | Rejected proof draft + its verifier feedback, passed directly into the next attempt |
| Across rounds (wider search) | Shared knowledge directory with reusable results |

## 4.1 Adversarial Generation and Tree-Structured Aggregation
**Covers:** Sections 4.1–4.1.3 (chunk lines 10–81)

At a difficult stage, Colosseum generates a population of candidates, subjects each to targeted falsification, and reduces the candidate–critique bundles through a tree; reviewer roles and output schemas vary by stage but the three operations stay the same.

Parallel generation seeks differences that change the mathematical outcome: representation, principal lemma, proof technique, case split, interpretation of evidence, or location of the main bottleneck; seeds, temperatures, prompt perspectives, tool access, and assumed lines of attack add variation. Each candidate follows a typed schema (e.g. a strategy proposal states mechanism, required lemmas, expected bottleneck, and a falsifiable test; a proof proposal states assumptions and marks gaps). Selected prompt templates and structured output interfaces are in Appendix A.

Targeted falsification: one or more adversarial reviewers examine each candidate, concentrating on defects and proposing an alternative only when it helps establish one. Review covers counterexamples and boundary cases; invalid implications or silently strengthened hypotheses; circularity and undeclared dependencies; misuse of a theorem, computation, or external reference; mismatch between proved statement and target claim; missing assumptions or results needed by later sections. Falsification records stay attached to the candidate; a clean record may reflect weak tests, while a precise objection can make another candidate easier to repair. Failure to find a defect does not establish correctness.

Tree-structured aggregation: let `zi` be a candidate bundled with all its falsification records, `C(0) = {z1, ..., zn}`, with tree shape `(m0, m1, ..., mL)`, `m0 = n`, `mL = 1`. From level `l` to `l+1`, each of the `m(l+1)` aggregation nodes independently draws `k_l` distinct inputs uniformly from the current population (sample size capped by `m_l`); sampling is without replacement within one group but groups may overlap (not a partition). Each node computes `s_j^(l+1) = A(x, K, G_j^(l))`. Expected reuse of a fixed node is `E[R_i^(l)] = m(l+1) * k_l / m_l`; ordinary contraction layers target roughly two to three (example: 128 nodes to 64 with sample size five gives expected reuse 2.5). Intermediate aggregation is constructive (merge compatible components, retain competing branches, repair a localized flaw, or declare unresolved conflict); disagreements and falsification evidence are carried forward, and the root returns a synthesized candidate with any unresolved objections.

## 4.2 The Research Pipeline
**Covers:** Sections 4.2.1–4.2.3 (chunk lines 84–137)

Strategy exploration and readiness: Colosseum explores proof strategies (different reformulations, intermediate claims, connections to known results) to expose what each route requires, what stays conjectural, and where difficulties lie. The readiness gate asks whether a route is concrete enough to support a proof plan — central reduction/mechanism stable, unresolved claims precise enough to assign to sections, no unresolved bridge likely to change the target or architecture; a central lemma may remain difficult if its statement, role, and expected path are explicit. Otherwise exploration continues; if passed, the route goes to decomposition.

Decomposition and parallel proof construction: the decomposer turns the route into a numbered, sectioned proof skeleton, each section with a subproblem plus dependency edges (DAG). A subproblem becomes eligible once its dependencies complete; each solver receives its task plus relevant completed sections, and difficult subproblems can use the Section 4.1 adversarial procedure. Before commit, a local reviewer checks the section against its subproblem and dependencies; on failure the same subproblem reruns with the failed section and review as extra input (local retry, other completed work preserved). Accepted section bodies replace placeholders and become available downstream; the filled skeleton is the candidate proof for global verification.

Global verification and feedback: the global verifier reads original problem plus completed document as a single argument with local reviews as audit context, catching cross-section failures (wrong-assumption dependency use, notation/definition drift, omitted cases, conclusion not matching target, silently inherited conditional/attacked claims). It runs multiple independent reviews plus tree aggregation that merges genuine duplicates while retaining distinct substantive objections — not a majority vote: one concrete fatal defect suffices to reject. The final review gives an overall verdict with material defects localized to the arising section/claim (for dependency errors, both supporting and using sections), making it actionable. On rejection: revision (replace section bodies or modify outline, then re-verify) when the strategy remains viable, else return to exploration.

## 4.3 Shared Research Knowledge
**Covers:** Sections 4.3–4.3.2 (chunk lines 139–171)

> "Colosseum carries information across research rounds in two complementary forms: the latest proof attempt is retained in full, while a shared knowledge directory collects reusable findings from the wider search."

| Form | Mechanism |
|---|---|
| Retaining prior attempts (4.3.1) | Failed round's draft + verifier feedback go directly into the next round; revision fixes concrete defects, re-exploration reconsiders strategy; draft retention does not endorse its claims since feedback stays attached |
| Knowledge directory (4.3.2) | Curator reads strategy proposals and falsification reports; entries keep source and caveats, updated across rounds, available to subsequent agents |

Four curated kinds of reusable knowledge:

1. Theorems and lemmas: results developed during search, with hypotheses, supporting arguments, possible applications.
2. Failed approaches: attempted routes, precise failure points, conditions under which a variant might still work.
3. References: relevant literature, including statements and hypotheses needed for the current problem.
4. Observations: structural properties or computational findings, with evidence and implications for subsequent work.

## 4.4 Inference Configurations (opening line only in this chunk)
**Covers:** Section 4.4 opening (chunk lines 173–175)

> "In this section, we give the inference configurations used in our research campaigns and evaluations. For open-ended research problems (Section 5), we use a range of tree configurations during strategy..."

The sentence is cut off at the chunk boundary; no configuration numbers are present in this chunk.
