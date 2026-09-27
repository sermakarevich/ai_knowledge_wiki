> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Dynamic Traces and Diagnosis
**In one sentence:** Static context and pass/fail validation alone leave repairs stuck on symptoms, so PracRepair motivates static-dynamic context construction (Stage I), question-driven diagnosis (Stage II), and feedback-guided refinement (Stage III).
## Key points
- Static-only repair changes `header.write(cache)` to `header.write(cache & 0xFF)` but still fails with the same error `Unknown property 128`.
- The Dynamic Execution Trace panel shows how `cache` and `shift` evolve across loop iterations and exposes the runtime state where the failure is triggered.
- Full execution traces can contain many irrelevant calls, branches, and state changes that would overwhelm the LLM, motivating static-dynamic context construction in Stage I.
- Raw static-plus-dynamic context is not self-explanatory (C2): even with dynamic evidence, the model still must determine which runtime states matter, as illustrated in the B. Repairing with Static + Dynamic Context panel.
- Question-driven diagnosis uses targeted questions such as cache/shift values when `if (shift == 0)` is entered and how the in-loop flush condition should change, focusing the model on the premature flush and motivating Stage II.
- Validation feedback is often reduced to coarse pass/fail or error messages (C3); the initial patch `if (shift == 0)` to `if (shift < 0)` removes `Unknown property 128` but introduces `Badly terminated header`.
- PracRepair instead extracts structured validation feedback — validation diagnostic, code diff, and trace diff — revealing the post-loop write is inconsistent with the updated in-loop flush, localizing the issue to the final flush condition and yielding the passing patch `if (length > 0 && shift < 7)`.
---
## Static context alone fails
The chunk states that failing tests and validation feedback “do not expose fine-grained execution traces such as executed paths, variable states, and branch outcomes.” In the A. Repairing with Static Context panel, given only bug information and static context, the model changes `header.write(cache)` to `header.write(cache & 0xFF)`. The chunk notes: “This patch appears to address the symptom suggested by Unknown property 128, but still fails with the same error.”
**Covers:** A. Repairing with Static Context panel; `Unknown property 128` failure.

## Dynamic traces motivate Stage I
In contrast, the Dynamic Execution Trace panel “reveals how cache and shift evolve across loop iterations and exposes the runtime state where the failure is triggered.” The chunk cautions that “complete execution traces in real programs may contain many irrelevant calls, branches, and state changes, and directly exposing them to the LLM may overwhelm the repair context.” This motivates “static-dynamic context construction in Stage I of PRACREPAIR.”
**Covers:** Dynamic Execution Trace panel; Stage I motivation.

## C2: Raw context is not self-explanatory
C2 is stated as: “Raw static-dynamic context is not self-explanatory.” Recent agentic APR methods “such as RepairAgent [26] and ReInFix [28], allow the model to interact with external tools, retrieve additional context, or refine patches iteratively,” but “richer context alone does not guarantee that the model will identify the failure-relevant behavior.” The B. Repairing with Static + Dynamic Context panel shows “what may happen when the model is provided with additional dynamic evidence without explicit diagnostic guidance,” suggesting “raw context is useful but not self-explanatory: the model still needs to determine which runtime states matter and how they explain the faulty logic.”
**Covers:** C2 discussion; RepairAgent [26], ReInFix [28]; B. Repairing with Static + Dynamic Context panel.

## Question-driven diagnosis motivates Stage II
In the Question-driven Diagnosis panel, “targeted questions such as `What are cache and shift when if (shift == 0) is entered?` and `How should the in-loop flush condition be changed?` guide the model to focus on the premature flush and formulate a more precise repair hypothesis.” This motivates “question-driven failure diagnosis in Stage II of PRACREPAIR.”
**Covers:** Question-driven Diagnosis panel; premature-flush hypothesis; Stage II motivation.

## C3: Validation dynamics and structured feedback motivate Stage III
C3 is stated as: “Patch-validation dynamics are often underused. Iterative APR methods commonly use validation results to refine patches [25]–[27], but validation feedback is often reduced to coarse outcomes such as pass/fail results or error messages.” As shown in the Validation Feedback panel, “the initial patch changes if (shift == 0) to if (shift < 0), which removes the original failure Unknown property 128 but introduces a new failure, Badly terminated header.” The chunk argues: “If validation is treated only as a pass/fail signal, the model receives limited guidance for the next repair attempt.” Instead, “PRACREPAIR extracts structured validation feedback, including the validation diagnostic, code diff, and trace diff between the original and patched executions.” The trace diff “reveals that after the initial patch, the post-loop write becomes inconsistent with the updated in-loop flush behavior, localizing the remaining issue to the final flush condition,” leading “to the refined patch if (length > 0 && shift < 7), which passes all tests.” This motivates “feedback-guided patch refinement in Stage III of PRACREPAIR.”
**Covers:** C3 discussion; iterative APR [25]–[27]; Validation Feedback panel; `if (shift < 0)` vs `if (length > 0 && shift < 7)`; Stage III motivation.

## Approach overview (Fig. 2)
Section III. Approach states Figure 2 shows the overall workflow of PRACREPAIR, “which aims to improve automated program repair by drawing inspiration from human-like debugging practices.” The three stages are named: “Static-dynamic Context Construction (Stage I), Question-driven Failure Diagnosis (Stage II), and Feedback-guided Patch Refinement (Stage III).” During repair it maintains “three intermediate artifacts: the diagnostic QA history,” plus patch/hypothesis artifacts per the figure (Stage I: CPG constructing / unified context access interface with project, bytecode instrumenting, tests running, trace collecting; Stage II: diagnosis loop for MAX rounds with asking/answering/formulating; Stage III: refinement loop with patch generating, candidate validating, feedback extracting and re-diagnosing).
**Covers:** III. Approach intro; Fig. 2: The Overall Framework of PRACREPAIR.
