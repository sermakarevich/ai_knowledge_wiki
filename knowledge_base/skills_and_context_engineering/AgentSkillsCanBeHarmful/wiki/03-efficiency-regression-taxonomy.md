> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Root Causes of Efficiency Regressions

**In one sentence:** Among the 182 high-confidence efficiency regressions found under the T = 2.0 threshold, most of the wasted cost comes not from bloated skill text but from skills turning optional agent actions into mandatory extra trajectory steps — especially excessive verification and heavier implementation pipelines — while smaller shares come from inflated per-call context and fragile dependency setup.

## Key points

- The analysis uses a conservative **T = 2.0 threshold**: a run counts as a high-confidence efficiency regression only if it more than doubles token use or execution time relative to the reference run, while the other metric also increases (rules out simple token-time tradeoffs and normal run-to-run variance).
- The taxonomy has three top-level categories: **Context Bloat (CO)**, **Excessive Procedure (EP)**, and **Dependency Resolution (DO)**, covering all 182 cases.
- **Excessive Procedure (EP)** is by far the largest category: **114 cases (62.6%)**.
- **Context Bloat (CO)** is second: **46 cases (25.3%)**, split into Skill-Body Context Bloat (43 cases, 23.6%) and Supplementary-Material Bloat (3 cases, 1.6%).
- **Dependency Resolution (DO)**: **22 cases (12.1%)** — task eventually passes, but the skill leads the agent into fragile/incompatible dependency installation, configuration, or repair work.
- Within Excessive Procedure, **Excessive Verification (EV)** is the single largest subcategory of the whole taxonomy: **67 cases (36.8%)** — repeated tests, rebuilds, debugging, or checklist verification after the artifact is already done.
- Also within EP: **Heavy Implementation Pipeline (HIP)** — 30 cases (16.5%), and **Excessive Exploration (EE)** — 17 cases (9.3%).
- Category vs. subcategory assignment is exclusive: each regression gets exactly one subcategory label, and category counts are just the sum of their subcategories; when both context and procedure effects appear in the same case, the label goes to whichever is the larger observed cost driver.

---

## The T = 2.0 threshold

The taxonomy is built specifically over the 182 high-confidence efficiency regressions selected under the primary **T = 2.0** threshold. A case qualifies only if a run **more than doubles** token use or execution time relative to the reference (no-skill or matched-skill) run, **and** the other metric also increases. This dual condition is deliberately conservative: it is designed to separate genuine skill-induced overhead from (a) ordinary token-for-time tradeoffs, where one metric rises because the other falls, and (b) ordinary run-to-run variation that has nothing to do with the skill.

## Context Bloat (CO) — 46 cases, 25.3%

Context Bloat covers cases where the extra cost comes from **each model call becoming more expensive**, not from the agent taking more steps — the overall sequence of task-solving actions stays similar to the reference run, but every call carries more tokens.

- **Skill-Body Context Bloat** — 43 cases (23.6%): the skill's own body text adds enough content to the agent's context window that each model call becomes substantially more expensive.
- **Supplementary-Material Bloat** — 3 cases (1.6%): the skill directs the agent to load or inspect auxiliary references, templates, examples, or documentation, which increases context size or tool-output cost.
- The paper's discussion (Finding 3, below) frames the fix as gating these materials — reference lists and background material — behind explicit lazy-loading triggers rather than always injecting them.

## Excessive Procedure (EP) — 114 cases, 62.6% (largest category)

This is the dominant root cause. EP regressions occur when the skill **changes the execution trajectory itself** — adding exploration, implementation work, debugging, or verification — often by converting optional activities into steps the agent treats as mandatory, even when the actual task doesn't need that much work.

- **Excessive Exploration (EE)** — 17 cases (9.3%): the skill leads the agent to inspect architecture, search for patterns, audit related files, or compare integration points before making the main task change.
- **Heavy Implementation Pipeline (HIP)** — 30 cases (16.5%): the skill induces a heavier construction process than needed, such as multi-stage conversion, subprocess workflows, or runtime simulation.
- **Excessive Verification (EV)** — 67 cases (36.8%), the largest single subcategory overall: the skill leads the agent to run excessive or repeated testing, debugging, rebuilding, or checklist verification after the main artifact has already been produced.

## Dependency Resolution (DO) — 22 cases, 12.1%

The task **eventually passes**, but the skill leads the agent to depend on a fragile or incompatible runtime dependency that requires installation, configuration, repair, or debugging before the task can pass. Dependency setup/repair becomes part of the (successful) trajectory. Note the boundary with the functional-failure taxonomy: if the same dependency problem is never resolved and causes the verifier to fail, that case instead falls under the functional-failure category **Broken Dependency or Runtime (BDR)**, not under this efficiency-regression category.

## Distinguishing Context Bloat from Excessive Procedure

The two categories are separated by **where the extra cost comes from**:

- **Context Bloat**: each model call becomes more expensive because the skill body or supplementary material increases context size, while the overall sequence of task-solving steps remains similar to the reference run.
- **Excessive Procedure**: the skill changes the trajectory itself by adding extra exploration, implementation work, retries, or verification steps (i.e., cost comes from added steps, not from bigger individual calls).

If a case shows both effects, it is assigned to whichever mechanism is the **larger observed cost driver** in the trajectory.

## Table IV — Classification of the 182 high-confidence efficiency regressions

| Category | Subcategory | Definition | Count | Percentage |
|---|---|---|---|---|
| Context Bloat | Skill-Body Context Bloat | The skill body adds enough text to the agent context that each model call becomes substantially more expensive. | 43 | 23.6% |
| Context Bloat | Supplementary-Material Bloat | The skill directs the agent to load or inspect auxiliary references, templates, examples, or documentation, increasing context or tool-output cost. | 3 | 1.6% |
| Context Bloat | **Subtotal** | | **46** | **25.3%** |
| Excessive Procedure | Excessive Exploration | The skill leads the agent to perform excessive repository, architecture, or pattern exploration before implementation. | 17 | 9.3% |
| Excessive Procedure | Heavy Implementation Pipeline | The skill leads the agent to use a heavier construction pipeline, subprocess workflow, or runtime simulation. | 30 | 16.5% |
| Excessive Procedure | Excessive Verification | The skill leads the agent to run excessive or repeated testing, debugging, rebuilding, or checklist verification after implementation. | 67 | 36.8% |
| Excessive Procedure | **Subtotal** | | **114** | **62.6%** |
| Dependency Resolution | — | The skill leads the agent to use a fragile or incompatible runtime dependency that requires installation, configuration, repair, or debugging before the task passes. | 22 | 12.1% |
| **Total** | | | **182** | **100.0%** |

## Finding 3

> **Finding 3:** When efficiency regressions arise from context overhead, the overhead is almost entirely caused by mandatory skill-body text. Skill-Body Context Bloat (SBCB) accounts for 43 of the 46 context-overhead cases, while Supplementary-Material Bloat (SMB) appears in only 3 cases.
>
> **Implication:** Skill packages should keep always-loaded instructions short and move examples, templates, long checklists, and background material behind explicit lazy-loading triggers.

## Finding 4

> **Finding 4:** High-confidence efficiency regressions are dominated by Excessive Procedure rather than prompt length alone, and the largest sources within Excessive Procedure are excessive verification and heavy implementation pipelines. At T = 2.0, Excessive Procedure accounts for 114 of 182 efficiency regressions (62.6%); within this category, Excessive Verification (EV) contributes 67 cases and Heavy Implementation Pipeline (HIP) contributes 30 cases.
>
> **Implication:** Skill platforms should model the extra actions that skills induce, and skill authors should condition verification scope and pipeline depth on task uncertainty, change size, and budget rather than prescribing exhaustive workflows by default.

---

**Covers:** Section V (What Are the Root Causes of Efficiency Regressions?)
