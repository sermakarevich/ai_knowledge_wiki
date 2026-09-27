[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Motivation and PracAPR Vision
**In one sentence:** Current APR is impractical for realistic debugging because it assumes a comprehensive test suite and frequent re-execution, is too slow, and cannot fix multi-location complex bugs — so the authors envision PracAPR, an interactive IDE repair system that works from a suspended debugger state without tests or re-execution.
## Key points
- Debugging consumes up to 50% of programming time [6], motivating APR, which aims to automatically generate a patch correcting a buggy program's misbehavior.
- Over a decade, more than 60 APR techniques [29, 36] have been developed, classified as pattern-based, constraint-based, search-based, and learning-based.
- Current APR assumes a (high-quality) test suite as the correctness criterion, which is unrealistic: developers often write too few tests or none at all [4, 19], bugs are often reported without a revealing test suite [20], and bug-revealing tests for over 90% of Defects4J bugs [15] were introduced only after the bug was identified.
- Prior test-free repair techniques [2, 3, 8, 20, 41] are restricted to specific bug types (e.g., heap-property faults [41]) or static-analyzer-flagged issues, not general semantic bugs arising while debugging.
- Frequent program re-execution for validation is impractical because recreating the failure environment is difficult when the failure appears after a long run or in an interactive session, and it makes repair slow: minutes (e.g., [14]) or even hours per bug [25], while developers prefer not to wait long [30].
- PracAPR is envisioned as an interactive repair system in the IDE that requires no test suite and no program re-execution, assuming the developer uses an IDE debugger with the program suspended where the problem is observed.
- PracAPR's pipeline is: interact with the developer to obtain a problem specification, then test-free flow-analysis-based fault localization, patch generation combining LLM-based local repair with tailored strategy-driven global repair, and re-execution-free validation via simulated trace comparison.
---
## Paper identity
**Covers:** Title block, authors, venue (Abstract header through ACM reference format)

| Item | Value (from chunk) |
|---|---|
| Title | Towards Practical and Useful Automated Program Repair for Debugging |
| Authors | Qi Xin, Haojun Wu (Wuhan University / Hubei Luojia Laboratory), Steven P. Reiss (Brown University), Jifeng Xuan (Wuhan University, corresponding author, jxuan@whu.edu.cn) |
| Identifier | arXiv:2407.08958v1 [cs.SE] 12 Jul 2024 |
| Venue | International Workshop on Software Engineering in 2030 (SE 2030), November 2024, Puerto Galinàs (Brazil); 6 pages |

## Abstract claims
**Covers:** Abstract

Current APR techniques are "far from being practical and useful enough to be considered for realistic debugging" because:

- they "rely on unrealistic assumptions including the requirement of a comprehensive suite of test cases as the correctness criterion and frequent program re-execution for patch validation";
- "they are not fast";
- "their ability of repairing the commonly arising complex bugs by fixing multiple locations of the program is very limited."

Verbatim vision statement:

> "we envision PracAPR, an interactive repair system that works in an Integrated Development Environment (IDE) to provide effective repair suggestions for debugging. PracAPR does not require a test suite or program re-execution. It assumes that the developer uses an IDE debugger and the program has suspended at a location where a problem is observed. It interacts with the developer to obtain a problem specification. Based on the specification, it performs test-free, flow-analysis-based fault localization, patch generation that combines large language model-based local repair and tailored strategy-driven global repair, and program re-execution-free patch validation based on simulated trace comparison to suggest repairs."

Closing goal: "By having PracAPR, we hope to take a significant step towards making APR useful and an everyday part of debugging."

## Motivation: cost of debugging and APR landscape
**Covers:** Section 1 MOTIVATION (debugging cost, APR definition and families)

- "Programs are rarely bug-free. Debugging is an indispensable activity in software development. It is however very costly, and can consume up to 50% of the programming time [6]."
- APR's goal "is to automatically generate a patch that corrects a buggy program's misbehavior" [9, 11, 28, 52].
- "For over a decade, more than 60 APR techniques have been developed [29, 36]" via strategies "generally classified as pattern-based (e.g., [17, 24, 40]), constraint-based (e.g., [26, 48]), search-based (e.g., [12, 43]), and learning-based [52]."
- "Despite the promising potential, current APR techniques are far from being practical and useful enough to be integrated into an IDE for debugging. Three key challenges remain."

## Challenge 1 (as present in chunk): unrealistic assumptions — test suite
**Covers:** Section 1 MOTIVATION (first challenge: test-suite assumption)

- Current approaches "assume the existence of a test suite serving as the correctness criterion and require frequent program re-execution for repair validation."
- "In a realistic debugging scenario, one cannot assume the existence of a (high-quality) test suite, especially in the initial development phase of the software."
- "Studies have shown that developers do not write test suites containing a sufficient number of test cases or even do not write tests at all [4, 19]."
- "As also noted by Koyuncu et al. [20], bugs are often reported without an available test suite revealing them."
- "Surprisingly, the bug-revealing test cases for over 90% of the bugs in the Defects4J dataset [15] were introduced after the bug was identified."
- Existing test-free work is narrow: "While some techniques [2, 3, 8, 20, 41] have sought for test-free repair, they are restricted to handling specific types of bugs (e.g., the heap-property faults [41]) and potential issues flagged by static analyzers and are not designed to repair general semantic bugs that arise while debugging."

## Challenge 1 (continued in chunk): frequent re-execution and speed
**Covers:** Section 1 MOTIVATION (re-execution reliance; chunk ends here)

- "The reliance on frequent program re-execution also makes APR not practical. In a realistic debugging scenario, recreating the environment for the immediate failure caused by the bug can be difficult since the failure can be identified in a long run or in an interactive session."
- "Moreover, frequent program re-execution makes APR not fast. Current approaches can take minutes (e.g., [14]) or even hours to repair one bug [25]."
- "Studies showed that developers prefer not to wait for too long [30] for repair."
- Note: the chunk ends mid-sentence at "One can also imagine that APR," — remaining challenges (speed details, multi-location bugs) and the full PracAPR description belong to later chunks and are not covered here.
