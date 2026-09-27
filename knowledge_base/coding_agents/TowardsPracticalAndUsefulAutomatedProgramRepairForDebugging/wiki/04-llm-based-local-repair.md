> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# LLM-Based Local Repair
**In one sentence:** ChatGPT misdiagnoses a `minY`/`maxY` failure when given only the failure message, but succeeds with an augmented prompt containing test input, related method definitions, and execution trace with program state, yet still needs user feedback, conversational repair, traditional-method guidance, and post-processing, while single-fault multi-location repair motivates tailored global strategies.
## Key points
- With only the failure message `expected:<101.0> but was:<102.0>`, ChatGPT misdiagnosed the bug as a loop-copy problem (line 14) instead of the `minY`/`maxY` update in `add` (line 19).
- The failure message omits the triggering test input, the behavior of the invoked `add` method showing how `minY` and `maxY` are updated, and failure-execution details.
- The planned augmented prompt adds the failing test case code including test input, definitions of related methods including `add`, and an execution trace with exercised lines, their order, and key variable/field values.
- With the augmented prompt, ChatGPT understood the failure as related to "how the min and max y values are updated after copying a subset" and produced a correct `minY`/`maxY` update patch.
- Even augmented prompts may fail when the correct handling is ambiguous (e.g., start index greater than end: throw an exception, return a special value, or something else), so user feedback is solicited (e.g., an exception is expected, a line should not execute, a variable should not hold a value).
- Planned mitigations combine ChatGPT with pattern-based and search-based methods for patterns and fix ingredients, conversational repair highlighting negative influence of previous patches for reflection, and post-processing refining and re-fixing.
- Existing global-repair evaluation on Defects4J is misguided because the dataset is filled with multi-fault bugs that decompose into independent single-fault bugs with different failures, whereas developers typically handle one failure at a time.
- The authors' detector found 118 single-fault multi-location bugs in Defects4J v1.2, current approaches repaired at most 8, and analysis of a sample of about one third (75 in total) yielded 8 partial-patch relationships driving specialized global-repair strategies.
---
## Failure message alone gives shallow diagnosis
The chunk opens with the failure message `expected:<101.0> but was:<102.0>`. It states the message does not inform ChatGPT of the test input triggering the failure, nor describe the behavior of the invoked method `add` (line 19) showing how `minY` and `maxY` are updated, nor provide failure-execution details. Due to insufficient failure knowledge, ChatGPT's diagnosis was shallow and inaccurate: it blamed the loop copying the data and did not recognize the `minY`/`maxY` update as the cause, proposing an incorrect patch changing the loop condition (line 14).

## Augmented prompt with test, method, and trace
The planned augmented prompt includes not only what ChatRepair uses but also the failing test case code (including test input), definitions of related methods (including `add`), and an execution trace showing exercised lines and their order plus key program state (variable and field values). Verbatim outcome: ChatGPT successfully understands the failure is related to "how the min and max y values are updated after copying a subset", leading to a patch that correctly updates the min and max y values.

## Limits of augmented prompts and mitigations
An augmented prompt may still fail to reveal what is wrong, and even precise problem understanding may not yield a correct patch when the intended behavior is ambiguous — e.g., ChatGPT may know of an invalid case where the start index is greater than end but be unsure whether to throw an exception, return a special value, or do something else. Mitigations from the chunk:

| Mechanism | Detail from chunk |
|---|---|
| User feedback | Solicit feedback showing for example an exception is expected, a certain line should not be executed, or a variable should not hold a value |
| Hybrid guidance | Combine ChatGPT with traditional pattern-based and search-based methods, finding effective patterns and fix ingredients |
| Conversational repair | Highlight the (negative) influence of previous patches so ChatGPT reflects on mistakes |
| Post-processing | Refine and re-fix patches to improve repair quality |

## Global repair driven by tailored strategies (Section 3.3 opening)
The chunk states the goal to design a global repair approach for single-fault multi-location bugs, analyzing developer (ground-truth) patches for a sample of about one third (75 in total) to learn why multiple locations are needed, characteristics of partial patches, and patch-generation strategies. Existing global-repair techniques' evaluation is based on Defects4J [15] and is severely misguided since the dataset holds multi-fault bugs decomposable into independent single-fault bugs triggering different failures; repairing them simultaneously is uncommon because developers deal with one failure at a time [18, 31]. The authors' detection approach found 118 single-fault multi-location bugs in Defects4J v1.2 and current approaches [23, 37, 44, 46, 50, 51, 55] repaired at most 8 bugs.

The analysis produced 8 partial-patch relationships:

| ID | Relationship as stated in chunk |
|---|---|
| DU | Add the definition of variables, fields, packages, or methods and later use what has been defined for repair |
| OA | Can be done in one repair action or operation, e.g., adding an if-statement wrapping a code hunk |
| RIF | Partial patches address related issues arising in different locations |
| DIF | Partial patches address different issues arising from different program parts that may implement the same functionality |
| EOH | Considered as a single-hunk patch, e.g., only one partial patch is semantically needed and others only improve readability |
| SU | Some partial patches do setup work by updating a variable, field, or method while others use what was updated |
| ONPF | Some partial patches fix the original problem and failure but raise new problems triggering new failures tackled by other partial patches |
| FU | Some partial patches are primary corrections while others undo the negative influence of previous changes |

**Covers:** Section 3.3 opening and failure-message local-repair example (chunk 04-the-failure-message-expected-101-0-but-was-102-0)
