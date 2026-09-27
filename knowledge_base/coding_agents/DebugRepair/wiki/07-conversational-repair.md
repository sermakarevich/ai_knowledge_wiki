> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Debugging-Driven Conversational Repair
**In one sentence:** DebugRepair repairs with a hierarchical conversational loop that feeds the LLM a prompt combining the buggy and instrumented function, purified test context, runtime trace, and prior failure feedback, retries within a session up to K_round, starts fresh debugging sessions up to a global N_session × K_round budget, and then augments the first plausible patch into diverse validated variants.
## Key points
- The repair prompt combines F_buggy, its instrumented version F_inst, the purified test context ⟨T_min, D⟩, the serialized dynamic trace τ_runtime, plus the initial failed patch P0 and its error message E0.
- The stated goal of this comprehensive context is evidence-based reasoning: deducing logic errors by contrasting observed runtime values against expected behaviors rather than relying solely on outcome-level failure symptoms.
- In each round k (1 ≤ k < K_round), the LLM generates candidate Pk from the augmented context plus feedback history; on failure the framework captures compilation or runtime symptoms as ⟨Pk, Ek⟩ and appends them for the next round's Pk+1.
- Iteration continues until a plausible patch is found or the K_round limit is reached, with each failed attempt's specific failure symptoms preserved in the conversation history.
- If K_round attempts fail, the session is terminated, its history discarded, and a new debugging session captures a fresh dynamic trace; the whole process ends on a plausible patch or exhaustion of the global N_session × K_round budget.
- Patch augmentation addresses test overfitting: following prior work [19, 38], the first plausible patch is used as a reference and the LLM generates logically similar but differently implemented variants, all validated against the test suite, outputting a set of plausible patches.
- Evaluation is organized around five research questions (RQ1–RQ5) covering SOTA comparison, repair scenarios (single-function/hunk/line), backbone-LLM generality, component contributions, and post-training-cutoff generalization.
- Benchmarks are Defects4J-V1.2 (391 bugs), Defects4J-V2.0 (+438 bugs), QuixBugs (40 Java + 40 Python), and HumanEval-Java (163 single-hunk cases chosen to reduce GPT-3.5 data-leakage risk), with SL ⊆ SH ⊆ SF categorization.
---
## Repair prompt construction (Fig. 5)
The chunk illustrates the prompt with `testEscapeSurrogatePairs` (`org.apache.commons.lang3.StringUtilsTest`):
- Failing-test context: `[Test] testEscapeSurrogatePairs`, failure line `assertEquals("\uD83D\uDE30", StringEscapeUtils.escapeCsv("\uD83D\uDE30"));`, failure message `java.lang.StringIndexOutOfBoundsException: String index out of range: 2`.
- Buggy method with debug prints and runtime output, e.g. `System.out.println("// DEBUG: initial pos=" + pos + ", len=" + len);`, with trace lines `// DEBUG: initial pos=0, len=2`, `// DEBUG: entering while loop, pos=0, len=2`, `// DEBUG: after translate(), consumed=2`.
- Prompt scaffolding quotes: `"fix may involve changes around these lines or adding new statements if necessary."`, `"The following information helps you repair the bug:"`, `"Based on all the information above, please provide a correct fix for the bug."`, with the response required to enclose the entire function in a ` ```java ... ``` ` block.
- Formally, the prompt carries `𝐹𝑏𝑢𝑔𝑔𝑦`, `𝐹𝑖𝑛𝑠𝑡`, `⟨𝑇𝑚𝑖𝑛, D⟩`, `𝜏𝑟𝑢𝑛𝑡𝑖𝑚𝑒`, `𝑃0`, and `𝐸0`.

## Feedback history loop
- Verbatim mechanism: "In each subsequent round 𝑘 (where 1 ≤ 𝑘 < 𝐾𝑟𝑜𝑢𝑛𝑑), the LLM generates a candidate patch 𝑃𝑘 based on the above augmented context and the feedback history."
- On failure: "the framework captures the specific failure symptoms, including the compilation or runtime errors", collects `⟨𝑃𝑘, 𝐸𝑘⟩`, and appends it to the feedback history for refining `𝑃𝑘+1`.
- Loop ends "until a plausible patch is found or the iteration limit 𝐾𝑟𝑜𝑢𝑛𝑑 is reached."

## Session-level re-debugging
- Trigger: "If a plausible patch is not found after 𝐾𝑟𝑜𝑢𝑛𝑑 attempts, it implies that the current debugging information might be insufficient or misleading."
- Action: "the framework terminates the current session, discards the conversation history, and triggers a new debugging session to capture a fresh dynamic trace."
- Global stop: "when a plausible patch is found or the global budget (𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 × 𝐾𝑟𝑜𝑢𝑛𝑑) is exhausted."

## Patch augmentation
- Motivation: "an initial plausible patch can successfully pass the entire test suite, it may not always represent the semantically correct fix" because of "test overfitting, as incomplete test suites may fail to cover all intended program behaviors."
- Method: "we introduce a patch augmentation module"; "DebugRepair leverages the generated plausible patch as a valuable reference, given that both plausible and correct patches share the characteristic of satisfying the available test suite."
- Output: "we instruct the LLM to generate alternative variants that are logically similar to the initial plausible patch but implemented differently", validated against the test suite, with "a set of plausible patches" as the final output.

## Experimental setup: research questions
- RQ1: How does DebugRepair perform in comparison with SOTA APR techniques?
- RQ2: How does DebugRepair perform across different repair scenarios (single-function, single-hunk, single-line)?
- RQ3: To what extent does DebugRepair improve repair effectiveness of vanilla LLMs across different backbone LLMs of diverse families and sizes?
- RQ4: What are the contributions of different components of DebugRepair?
- RQ5: How well does DebugRepair generalize to bugs introduced after the LLM training data cutoff?

## Experimental setup: benchmarks
| Benchmarks | # Total Bugs | # SF Bugs | # SH Bugs | # SL Bugs |
|---|---|---|---|---|
| Defects4J-V1.2 | 391 | 255 | 154 | 80 |
| Defects4J-V2.0 | 438 | 228 | 159 | 78 |
| QuixBugs-Java | 40 | 40 | 37 | 37 |
| QuixBugs-Python | 40 | 40 | 40 | 40 |
| HumanEval-Java | 163 | 163 | 163 | 74 |
- Category note: "the single-line category is a subset of the single-hunk category, and the single-hunk category is a subset of the single-function category"; "In QuixBugs-Java, all single-hunk bugs correspond to single-line fixes, while in QuixBugs-Python, all fixes are single-line."
- HumanEval-Java: 163 single-hunk cases, "released after the data collection period used to train GPT-3.5 [1], thereby reducing the potential risk of data leakage"; developers convert Python HumanEval programs plus tests into Java/JUnit and "deliberately inject some bugs into these correct Java programs."

**Covers:** chunk 07-test-context-test-fix-may-involve (Fig. 5 prompt construction through §4 Experimental Setup: RQs, benchmarks, Table 1)
