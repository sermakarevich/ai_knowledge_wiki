> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Question-driven Failure Diagnosis and Repair Hypothesis
**In one sentence:** PracRepair transforms collected static and dynamic evidence into diagnostic understanding by iteratively asking one what/why/how question at a time, answering it via the unified context interface, and summarizing the QA history into a structured four-field repair hypothesis that feeds iterative patch refinement.
## Key points
- Stage II does not generate a patch directly from Stage III-A context; it first builds diagnostic understanding through question-driven failure diagnosis.
- Each round raises one diagnostic question, retrieves evidence to answer it, and appends a QA pair recording question, retrieved evidence, diagnostic answer, and repair implication.
- What-type questions establish factual understanding of the failing execution (executed statements, branch outcomes, variable evolution, deviations), mainly using dynamic evidence.
- Why-type questions connect abnormal runtime behavior to program logic (incorrect control flow, abnormal state transitions, invalid data dependencies), using both static and dynamic evidence.
- How-type questions determine how to change the faulty logic to restore intended semantics, mainly using the diagnosed root cause and static code context.
- Question answering interleaves reasoning and retrieval in a ReAct-inspired loop until enough evidence is collected, and validation feedback from Stage III is incorporated to re-diagnose patch behavior.
- The repair hypothesis has four fields — faulty behavior, supporting evidence, suspected root cause, modification suggestion — and serves as the output of Stage II and input to Stage III.
- Stage III turns the hypothesis into an iterative loop that analyzes behavioral differences before and after patching and feeds unsuccessful-validation feedback back into Stage II.
---
## Question asking
**Covers:** Section III-B.1, Stage II of Figure 2

PracRepair reduces diagnostic uncertainty through three question types grounded in the Table I context-access capabilities:

| Question type | Purpose | Evidence mainly used |
|---|---|---|
| What | Establish factual understanding of failing execution (executed statements, branch outcomes, variable evolution, deviations from expected behavior) | Dynamic evidence |
| Why | Explain failure by connecting abnormal runtime behavior to underlying program logic (incorrect control flow, abnormal state transitions, invalid data dependencies) | Both static and dynamic evidence |
| How | Determine how to change faulty logic to restore intended semantics | Diagnosed root cause + static code context |

To avoid overhead, the LLM does not ask all questions at once; at each step it makes a structured diagnostic decision that either raises one new diagnostic question or returns a stopping signal. A raised question must specify the question type, the target program entity or runtime behavior to inspect, and the evidence needed to answer it — e.g., a what-type question may target a variable value at a suspicious statement, while a why-type question may target the control or data dependency explaining an abnormal state. This constrained format makes diagnosis traceable and prevents multiple unrelated questions in one round. The loop terminates when the diagnosis budget is reached or the LLM returns the stopping signal.

Verbatim: "P RAC R EPAIR does not directly generate a patch from the context constructed in Section III-A. Instead, it first transforms the collected evidence into diagnostic understanding through question-driven failure diagnosis."

## Question answering
**Covers:** Section III-B.2

To answer each diagnostic question, PracRepair lets the LLM retrieve failure-relevant context through the unified interface from Section III-A, inspecting static evidence (dependencies, implementations, structural relations) or dynamic evidence (execution paths, runtime values, statement-level states) depending on question type. Inspired by ReAct [37], the process interleaves reasoning and retrieval until enough evidence is collected. Each answer is paired with its question and appended to the QA history; when Stage III returns validation feedback, the same loop incorporates it to re-diagnose the current patch behavior.

Stage II inputs per the chunk: buggy code, test suite, failure information, accumulated diagnostic QA history, and optionally validation feedback from Stage III.

## Repair hypothesis formulation
**Covers:** Section III-B.3

When the diagnosis loop terminates, PracRepair formulates an explicit repair hypothesis from the accumulated QA history and available failure-relevant evidence, with four fields:

1. Faulty behavior — observed abnormal execution.
2. Supporting evidence — key QA findings and retrieved context.
3. Suspected root cause — why the failure occurs.
4. Modification suggestion — how the faulty logic should be changed.

Example given in the chunk (Figure 1): the hypothesis identifies premature flushing at `shift == 0` as the faulty behavior, uses observed values of `cache` and `shift` as supporting evidence, and suggests changing the in-loop flush condition. The hypothesis is the output of Stage II and the input to Stage III, bridging diagnosis and patch generation.

## Feedback-guided patch refinement
**Covers:** Section III-C, Stage III of Figure 2

PracRepair turns the repair hypothesis into an iterative loop: rather than treating validation as a pass/fail check, it analyzes behavioral differences before and after patching and uses them as new evidence for subsequent diagnosis. A repair hypothesis guides patch generation, patch validation reveals how patched execution differs from the original failing execution, and unsuccessful validation produces feedback fed back into Stage II to refine the diagnosis and the next patch.

**Covers:** Section III-B (Question-driven Failure Diagnosis) through opening of Section III-C (Feedback-guided Patch Refinement); chunk tail fragment on examining concrete program states at specific locations and Table I uniform access interface as basis for Stage III-B.
