> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Root Causes of Functional Failures

**In one sentence:** Across the 125 confirmed functional failures, skills almost never fail because they are topically wrong for the task (Applicability Mismatch, 1.6%) — instead they overwhelmingly fail because an on-topic skill causes the agent to fill or omit a required implementation element incorrectly (Task-Implementation Fault, 68.8%), with Environment Mismatch (10.4%) and Artifact Misplacement (19.2%) making up most of the remainder by corrupting the "execution surface" (environment state or output location) rather than the task logic itself.

## Key points

- The 125 confirmed functional failures split into four categories: Applicability Mismatch (APM, 2 cases, 1.6%), Environment Mismatch (EM, 13 cases, 10.4%), Task-Implementation Fault (TIF, 86 cases, 68.8%), and Artifact Misplacement (AM, 24 cases, 19.2%).
- Each failure gets exactly one subcategory label; category counts are the sum of their subcategories' counts.
- Environment Mismatch splits into Broken Dependency or Runtime (5 cases, 4.0%) and Environment-State Mismatch (8 cases, 6.4%).
- Task-Implementation Fault, the largest category by far, splits into Obstructive Workflow Guidance (4 cases, 3.2%), Incorrect Required-Element Fill (46 cases, 36.8% — the single largest subcategory in the whole taxonomy), and Required-Element Omission (36 cases, 28.8%).
- IRF and RRO together account for 82 of the 125 failures (about two-thirds of all functional failures), meaning the dominant failure mode is a topically correct skill that still causes a required piece of the artifact to be wrong or missing.
- Artifact Misplacement (24 cases, 19.2%) is entirely about location: the agent builds a plausible, working artifact but writes or integrates it at the wrong path or integration point, often because it follows repository/package conventions instead of the task-specified path.
- Finding 1: only 2/125 (1.6%) failures are Applicability Mismatch, showing that skills rarely fail by being off-topic — they fail by inducing faults in the implementation of on-topic requirements.
- Finding 2: Environment Mismatch (13 cases, 10.4%) plus Artifact Misplacement (24 cases, 19.2%) show that a substantial share of functional failures occur at "execution-surface boundaries" — where the skill changes the verifier-observed environment state or the artifact's location — rather than in the core task logic.

---

## Applicability Mismatch (APM) — 2 cases, 1.6%

Skill metadata gives an incomplete or misleading applicability signal, causing the agent to apply the skill to a task where its guidance is inappropriate. This is the smallest category in the taxonomy, confirming that skill selection/routing is rarely the root cause of functional failure — the bigger problems occur after a relevant skill has already been correctly invoked.

## Environment Mismatch (EM) — 13 cases, 10.4%

The skill's guidance interacts badly with the task's runtime or state, so the environment the agent ends up validating itself against diverges from the environment the evaluator actually checks.

### Broken Dependency or Runtime — 5 cases, 4.0%

The skill explicitly recommends or depends on a dependency or runtime component that fails in the task environment, causing installation, import, or execution failure.

### Environment-State Mismatch — 8 cases, 6.4%

The skill indirectly leads the agent to change package resolution, working directory, version, installation state, or tool state, so the agent's self-check environment differs from the evaluator's state.

**Worked example (openpyxl):**

- Target trajectory: the agent decides "Old openpyxl version incompatible ... I'll install a modern version," then runs `pip install openpyxl`, `cd /tmp`, and filters `sys.path` to drop any path containing `/workspace/openpyxl`.
- Reference-run trajectory: instead of installing a new version, it patches `openpyxl/formatting/rules.py` in the repository itself, changing `from collections import Mapping` to `from collections.abc import Mapping`.
- Why it's an environment mismatch and not just a content bug: the verifier imports from the repository package, while the target run validates against an external install it just created. Comparing the target run to the reference run shows the failure comes from a mismatched environment state (which package/version is actually being imported), not from the artifact's content alone.

## Task-Implementation Fault (TIF) — 86 cases, 68.8% (largest category)

An on-topic skill induces a fault in the implementation process or generated artifact, preventing the agent from satisfying a concrete task-required implementation element. In many cases the agent over-trusts a topically matched skill and treats its reusable defaults, examples, or templates as if they were task-specific requirements. The skill can make the workflow too heavy to finish, implement a required element incorrectly, or leave a required element out entirely.

### Obstructive Workflow Guidance (OWG) — 4 cases, 3.2%

Otherwise relevant guidance induces excessive exploration, setup, audits, or procedural checks that prevent the agent from producing the required artifact within the available budget.

### Incorrect Required-Element Fill (IRF) — 46 cases, 36.8% (largest subcategory overall)

The skill leads the agent to implement a task-required element with an incorrect method, API, value, policy, or output structure. The target artifact does contain an implementation of the required element — it's just wrong.

**Worked example (spreadsheet: net exports as percent of GDP):**

- Task: calculate net exports as percent of GDP.
- Verifier output: values are about 100x too small.
- Target trajectory: `(Exports - Imports) / GDP` — a bare ratio.
- Reference-run trajectory: `(Exports - Imports) / GDP * 100` — keeps the task-required percentage scaling.
- Why the reference run matters: it distinguishes a skill-induced failure from an ordinary arithmetic mistake — the target run drops the percentage scaling that the task explicitly requires, and the reference confirms that is the missing piece.

### Required-Element Omission (RRO) — 36 cases, 28.8%

The target run leaves a required field, option, behavior, domain rule, validation, or dependent step absent, leaving the artifact incomplete without providing a concrete substitute. The distinction between IRF and RRO is whether the target artifact contains a concrete but wrong implementation of the required element (IRF), or leaves that element absent entirely (RRO).

**Worked example (RAG demo: model_name configurability):**

- Task: chunk size, overlap, top-k, and model parameters must all be configurable.
- Verifier output: `test_model_parameters_configurable` fails.
- Target trajectory: exposes CLI args `--question`, `--chunk-size`, `--chunk-overlap`, `--top-k` — but no model-parameter flag.
- Reference-run trajectory: `RAGConfig` includes `model_name = "gpt-3.5-turbo"` as a configurable field.
- Why it happened: the skill's example shows retrieval parameters (chunk size, overlap, top-k) but never shows how to configure model parameters. The target run faithfully follows that partial example, exposing the retrieval parameters but omitting the required model-parameter field that the reference run adds as `model_name`.

## Artifact Misplacement (AM) — 24 cases, 19.2%

The agent builds a plausible, often functionally correct artifact but writes or integrates it at a location different from the task-specified path or integration point. The target run often follows repository or package-layout conventions instead of the path the task actually specified.

**Worked example (LangChain RAG task, langchain_classic):**

- Task: create files under `libs/langchain/langchain/` — specifically `retrievers/hybrid_retriever.py`, `text_splitter/semantic_chunker.py`, `chains/rag_chain.py`.
- Verifier output: file-path existence tests fail for `libs/langchain/langchain/...`.
- Target trajectory: the agent reasons "The package is `langchain_classic`," decides "I'll use `langchain_classic` since that's the real package," and writes the files under `libs/langchain/langchain_classic/` instead.
- Reference-run trajectory: reasons "I'll create the files at the paths specified in the task" and writes under `libs/langchain/langchain/` as instructed.
- Why it's placement, not quality: the decisive failure is where the artifact was written, not the plausibility or correctness of the generated RAG components themselves.

---

## Table III — Classification of the 125 Confirmed Functional Failures

| Category | Subcategory | Definition | Count | Percentage |
|---|---|---|---|---|
| Applicability Mismatch | — | Skill metadata gives an incomplete or misleading applicability signal, causing the agent to apply the skill to a task where its guidance is inappropriate. | 2 | 1.6% |
| Environment Mismatch | Broken Dependency or Runtime | The skill explicitly recommends or depends on a dependency or runtime component that fails in the task environment, causing installation, import, or execution failure. | 5 | 4.0% |
| Environment Mismatch | Environment-State Mismatch | The skill indirectly leads the agent to change package resolution, working directory, version, installation state, or tool state, so the agent's self-check environment state differs from the evaluator's state. | 8 | 6.4% |
| Environment Mismatch | **Subtotal** | | **13** | **10.4%** |
| Task-Implementation Fault | Obstructive Workflow Guidance | The skill induces excessive exploration, setup, or procedural steps that prevent the agent from producing the required artifact within the available budget. | 4 | 3.2% |
| Task-Implementation Fault | Incorrect Required-Element Fill | The skill leads the agent to implement a task-required element with an incorrect method, API, value, policy, or output structure. | 46 | 36.8% |
| Task-Implementation Fault | Required-Element Omission | The skill leads the agent to leave a task-required element or dependent step absent, leaving the artifact incomplete without providing a concrete substitute. | 36 | 28.8% |
| Task-Implementation Fault | **Subtotal** | | **86** | **68.8%** |
| Artifact Misplacement | — | The skill leads the agent to write or integrate the required artifact at a location different from the task-specified path or integration point. | 24 | 19.2% |
| **Total** | | | **125** | **100.0%** |

---

## Finding 1

> Only 2 of 125 functional failures are classified as Applicability Mismatch (1.6%), while most fall under Task-Implementation Fault, indicating that on-topic skills more often induce task-implementation faults in required implementation elements. Task-Implementation Fault accounts for 86 of 125 functional failures (68.8%), and Incorrect Required-Element Fill (IRF) plus Required-Element Omission (RRO) account for 82 cases.
>
> **Implication:** Skill authors should separate mandatory task requirements from examples, defaults, reusable templates, and optional workflows, so that agents do not mistake reusable guidance for task-specific obligations.

## Finding 2

> A substantial share of functional failures occur at execution-surface boundaries, where the skill changes the verifier-observed environment state or artifact location. Environment Mismatch accounts for 13 cases (10.4%), while Artifact Misplacement accounts for 24 cases (19.2%).
>
> **Implication:** Agent platforms should treat task-specified paths, integration points, package state, and working directories as guarded constraints before accepting skill-guided environment changes or repository-native path substitutions.

---

**Covers:** Section IV (What Are the Root Causes of Functional Failures?)
