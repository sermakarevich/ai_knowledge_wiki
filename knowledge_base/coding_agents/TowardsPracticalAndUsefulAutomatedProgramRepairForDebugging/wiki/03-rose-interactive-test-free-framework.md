[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# ROSE interactive test-free framework
**In one sentence:** ROSE lets the developer choose a patch for a preview showing before/after differences and ask ROSE to apply it, its test-free fault localization and patch validation proved highly effective in repair experiments and a user study, and PracAPR is planned on top of it with better problem specification and learning-based trace comparison, complemented by a ChatGPT-based local-repair component.
## Key points
- ROSE provides a choose-a-patch-for-preview interaction that highlights code before and after the repair with differences and lets the user ask ROSE to make the repair, with details in [33, 34].
- ROSE's test-free fault localization included the correct repair location for 89% of the bugs tested.
- ROSE's patch validation gave a top-5 rank for all correct repairs.
- A ROSE-based tool repaired as many as 36/40 QuixBugs and 37/60 Defects4J bugs in only seconds.
- In a user study, ROSE helped 44% more participants succeed in a debugging task and reduced debugging time by about 16.5%.
- PracAPR is planned on top of ROSE with two improvements: better user interaction for problem specification and learning-based trace comparison using more execution information to enhance patch validation.
- The planned LLM-based local-repair component uses ChatGPT to infer the problem and provide a low number of promising single-location patches, motivated by a study with three research questions on ChatGPT failures, common mistakes, and improvements.
- Existing ChatGPT-based prompts are weak because they include only the buggy location, limited context, and shallow failure information (input and failing assertion), which is often insufficient to understand program semantics and can produce incorrect patches raising new problems.
---
## Patch preview interaction
> "choose a patch for a preview, which highlights the code before and after the repair with differences, and ask ROSE to make the repair."
- More details in [33, 34].

## ROSE evaluation: repair experiment and user study
> "We evaluated the effectiveness and utility of ROSE with a repair experiment and a user study."
> "Our results showed that ROSE's test-free fault localization and patch validation are highly effective: the fault localization included the correct repair location for 89% of the bugs tested and the patch validation gave a top-5 rank for all correct repairs; that a ROSE-based tool can repair as many as 36/40 QuixBugs and 37/60 Defects4J bugs in only seconds; and that ROSE helped 44% more participants succeed in a debugging task and helped reduce the debugging time by about 16.5%."

| Measure | Exact number from chunk |
|---|---|
| Fault localization includes correct repair location | 89% of bugs tested |
| Patch validation rank of correct repairs | top-5 for all correct repairs |
| QuixBugs repaired | 36/40, in only seconds |
| Defects4J repaired | 37/60, in only seconds |
| User-study success uplift | 44% more participants succeeded |
| User-study time reduction | about 16.5% |

> "Overall, we believe that ROSE is a promising repair framework that can make debugging easier."

## Building PracAPR on ROSE: two improvements
> "We plan to build PracAPR on top of ROSE, and we see two ways for improvement."
- First: improve ROSE's user interaction for problem specification by exploring not only a better presentation of the failure information to facilitate understanding of the program semantics and the failure but also more forms of the specification (based on for example constraints and even natural language) to effectively guide fault localization and patch validation.
- Second: investigate learning-based trace comparison while considering more information about the execution to enhance patch validation.

## Transition to LLM-based local repair (§3.2 opening)
> "The LLM has demonstrated superior abilities in repairing software bugs [45, 47]."
- The chunk states an LLM-based approach is promising for generating high-quality local patches addressing single locations of the program, and considers a ChatGPT-based approach — ChatGPT being widely recognized as a prominent LLM for software engineering tasks — as a key PracAPR component to accurately infer the problem and provide a low number of promising patches.
- Ongoing study asks: "(1) What are the characteristics of the bugs that ChatGPT fails to repair? (2) What are the most common mistakes that ChatGPT makes? and (3) How to improve ChatGPT to repair more bugs?"
- Current finding: prompts with only the buggy location, limited context, and shallow failure information (input and failing assertion) are often insufficient and can yield incorrect patches raising new problems.
- Example given (Figure 2, Defects4J Chart_3 `TimeSeries createCopy(int start, int end)`): the patch adds lines 10–11 (`copy.minY = Double.NaN;` and `copy.maxY = Double.NaN;`); the state-of-the-art ChatRepair [47] prompt for it includes the buggy method code, failing test name `testCreateCopy3`, and failing assertion `assertEquals(101.0, s2.getMaxY(), EPSILON)` (chunk truncates after "and").

**Covers:** ROSE framework, simulated-trace validation, evaluation and user study
