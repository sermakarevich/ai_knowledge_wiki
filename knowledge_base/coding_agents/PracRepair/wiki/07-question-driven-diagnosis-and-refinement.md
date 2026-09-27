> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Question-Driven Diagnosis and Refinement

**In one sentence:** PracRepair refines the repair hypothesis in a feedback-guided loop of at most 3 rounds — generating a hypothesis-guided patch, validating it by compilation and test execution, and feeding categorized failure outcomes plus diagnostics, code diff, and trace diff back into question-driven re-diagnosis until a plausible patch is found or the budget is exhausted.

## Key points

- The refinement loop continues until the maximum of 3 refinement rounds is reached, or terminates earlier once a plausible patch is found.
- Patch generation uses a structured zero-shot prompt with three parts — bug context (buggy function, triggering tests, failure information), repair hypothesis (suspected root cause and modification suggestions), and a generation instruction to produce a corrected implementation — with no in-context examples.
- Patch validation applies the candidate patch, compiles and executes tests, and collects patched-program execution traces with the same trace-collection procedure as Section III-A so patched behavior can be compared with the original failing execution.
- A patch is regarded as plausible only if the patched program compiles successfully and passes all tests within the maximum execution time of 10 minutes.
- Failed validation is categorized into four outcomes: (1) compilation failures, (2) runtime failures (compiles but triggers runtime exceptions or timeouts), (3) remaining failures (originally failing tests still not fixed), and (4) regression failures (original failure resolved but previously passing tests now fail).
- Each failure yields three complementary feedback forms: validation diagnostics (compiler errors, runtime exceptions, timeout messages, updated failing tests), code diff (patch vs. original buggy function), and trace diff (aligned by executed statement and execution order; changed branch outcomes, added or removed statement executions, divergent runtime values).
- The extracted feedback is fed back into Question-driven Failure Diagnosis as optional diagnostic input (Figure 2), where the LLM re-diagnoses from original bug context plus accumulated QA history plus new feedback, and the resulting QA pairs refine the repair hypothesis for the next generation–validation round.

---

## Patch generating

**Covers:** repair-hypothesis refinement loop; step 1) Patch Generating

Given the current repair hypothesis, PracRepair prompts the LLM to generate a candidate patch for the buggy function. The patch-generation prompt has three parts:

1. bug context, including the buggy function, triggering tests, and failure information;
2. repair hypothesis, including the suspected root cause of the failure and the corresponding modification suggestions;
3. generation instruction, which directs the LLM to produce a corrected implementation of the buggy function.

> "patch generation is guided not only by the observed symptom, but also by the explicit diagnostic understanding accumulated in Stage II."

To preserve input clarity and minimize prompt bias, PracRepair adopts a zero-shot prompting strategy, with patch generation relying solely on the structured prompt rather than in-context examples. Prompt templates are provided in the artifact [38].

## Patch validating

**Covers:** step 2) Patch Validating

After generating a candidate patch, PracRepair applies it to the original program and validates the patched program through compilation and test execution. During this process it also collects execution traces from the patched program using the same trace-collection procedure described in Section III-A, so that patched behaviors can later be compared with the original failing execution.

> "If the patched program compiles successfully and passes all tests within the maximum execution time (i.e., 10 minutes), the patch is regarded as a plausible patch."

## Feedback extracting and re-diagnosing

**Covers:** step 3) Feedback Extracting and Re-diagnosing

If a candidate patch does not pass validation, PracRepair does not treat the result as a simple failure signal. It first determines how the current repair attempt fails, because different validation outcomes provide different high-level directions for the next diagnosis round — e.g., "a compilation failure indicates that the patch itself is syntactically or semantically invalid."

Four coarse-grained outcomes:

| # | Outcome | Meaning in chunk |
|---|---|---|
| 1 | Compilation failures | Patched program cannot be compiled |
| 2 | Runtime failures | Compiles successfully but triggers runtime exceptions or timeouts during testing |
| 3 | Remaining failures | Originally failing test(s) are still not fully fixed |
| 4 | Regression failures | Original failure is resolved but previously passing tests become failing |

Three complementary feedback forms:

1. Validation diagnostics — compiler errors, runtime exceptions, timeout messages, or updated failing tests — describing the observed failure outcome.
2. Code diff between the generated patch and the original buggy function, identifying which statements or conditions have been changed.
3. Trace diff between the original and patched executions: executes the same triggering tests on both versions, collects traces with the same instrumentation procedure, aligns trace records by executed statement and execution order, and extracts changed branch outcomes, added or removed statement executions, and divergent runtime values.

> "The resulting feedback therefore explains not only whether the patch fails, but also how the patch changes the failing behavior."

This feedback is fed back into Question-driven Failure Diagnosis as optional diagnostic input (Figure 2). Based on the original bug context, the accumulated QA history, and the new feedback, the LLM re-diagnoses the current patch failure — e.g., "if the trace diff shows that a branch outcome changes but the failing value remains abnormal, the next diagnosis round can ask why the changed branch still does not restore the expected state." The resulting QA pairs refine the repair hypothesis, which guides the next round of patch generation and validation:

> "Through this feedback-guided loop, PracRepair progressively improves candidate patches until a plausible fix is found or the refinement budget is exhausted."

## Experiment design (as appearing in this chunk)

**Covers:** Section IV Experiment Design header; RQ1–RQ4 list; Datasets paragraph and Table II (partial, continues into next chunk)

Research questions stated in chunk:

- RQ1 (Repair Effectiveness): effectiveness vs. existing APR tools under standard perfect fault-localization setting, and whether it remains effective when exact fault locations are unavailable.
- RQ2 (Repair Scenarios): performance across different repair scenarios.
- RQ3 (Ablation Study): individual contributions of each component.
- RQ4 (Generalizability Study): generalization to unseen datasets with different underlying foundation models.

Datasets stated in chunk:

- Java APR setting; benchmarks Defects4J [3] and RWB (Real-World Bugs) [27]; no other-language datasets such as SWE-Bench.
- Defects4J V1.2: 391 bugs after removing 4 deprecated ones; V2.0: 438 new bugs; scenarios MF (multi-function fix), SF (single-function fix), SH (single contiguous region; SH ⊆ SF), SL (single line; SL ⊆ SH).
- RWB V1.0: 44 single-function bugs (commits after October 2021); RWB V2.0: 29 single-function bugs (commits after March 2023).
- Default fault information: perfect fault localization (exact buggy statement location(s)); a relaxed setting is also included to test dependence on that assumption.

Table II as printed in chunk:

| Dataset | #Total Bugs | #MF Bugs | #SF Bugs | #SH Bugs | #SL Bugs |
|---|---|---|---|---|---|
| Defects4J 1.2 | 391 | 136 | 255 | 154 | 80 |
| Defects4J 2.0 | 438 | 210 | 228 | 159 | 78 |
| #Sum | 909 | 346 | 563 | 390 | 235 |

**Covers:** refinement-loop steps 1–3 (patch generating, validating, feedback extracting and re-diagnosing) through Section IV header, RQ1–RQ4, Datasets text, and Table II; chunk tail (ablation-variant sentences) is truncated and continues in the next chunk.
