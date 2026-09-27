---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Towards Practical and Useful Automated Program Repair for Debugging

### Q1. What evidence do the authors give that the test-suite assumption of current APR is unrealistic for real debugging?

> [!tip]- Answer
>
> Developers often write too few tests or none at all, bugs are frequently reported without any revealing test suite, and the bug-revealing tests for over 90% of Defects4J bugs were introduced only after the bug was identified. Prior test-free repair work does not fill this gap because it targets narrow bug classes like heap-property faults or static-analyzer warnings rather than general semantic bugs. See [[wiki/01-motivation-and-pracapr-vision|Motivation and PracAPR Vision]].

### Q2. What three limitations make current APR impractical for realistic debugging, according to the paper?

> [!tip]- Answer
>
> Current techniques assume a comprehensive test suite as the correctness criterion and require frequent program re-execution for validation, they are too slow at minutes to hours per bug while developers will not wait long, and they can barely repair complex bugs spanning multiple program locations. Frequent re-execution is additionally infeasible when a failure appears only after a long run or inside an interactive session. See [[wiki/01-motivation-and-pracapr-vision|Motivation and PracAPR Vision]].

### Q3. What are the five stages of the PracAPR pipeline shown in Figure 1?

> [!tip]- Answer
>
> The pipeline runs (1) Problem Specification, where the developer describes the observed problem, to (2) Test-Free Fault Localization yielding repair locations, to (3) Patch Generation with LLM-based local and tailored strategy-driven global branches, to (4) Program Re-execution-Free Patch Validation yielding validated patches, and finally (5) Patch Presentation with patches for preview. The whole pipeline lives inside the IDE alongside the debugger. See [[wiki/02-pracapr-architecture-and-pipeline|PracAPR Architecture and Pipeline]].

### Q4. How do PracAPR's test-free fault localization and re-execution-free patch validation work?

> [!tip]- Answer
>
> Fault localization uses flow analysis over the problem symptom, current debugger values, and the runtime stack to compute a backward slice containing potential repair locations, with the program stopped where the problem is observed. Validation generates simulated traces via a live-programming mechanism that reflect the real executions of the original and repaired programs, then compares the traces to infer patch correctness. The developer can preview any suggested repair with before-and-after differences and accept it into the program. See [[wiki/02-pracapr-architecture-and-pipeline|PracAPR Architecture and Pipeline]].

### Q5. What quantitative results does the paper report for the ROSE framework?

> [!tip]- Answer
>
> ROSE's test-free fault localization included the correct repair location for 89% of tested bugs, and its patch validation ranked all correct repairs in the top 5. A ROSE-based tool repaired 36/40 QuixBugs and 37/60 Defects4J bugs in only seconds, and a user study showed ROSE helped 44% more participants succeed at a debugging task while reducing debugging time by about 16.5%. See [[wiki/03-rose-interactive-test-free-framework|ROSE interactive test-free framework]].

### Q6. Why do the authors say existing ChatGPT-based repair prompts fail, and what does the augmented prompt add?

> [!tip]- Answer
>
> Existing prompts supply only the buggy location with limited context and shallow failure information such as the input and the failing assertion, so on Defects4J Chart_3 ChatGPT blamed the data-copying loop instead of the missing `minY`/`maxY` update in `add`. The augmented prompt adds the failing test code with inputs, definitions of related methods including `add`, and an execution trace with line order plus key variable and field values, which lets ChatGPT correctly diagnose the min/max update failure. Residual ambiguity remains, e.g. whether a start-greater-than-end case should throw or return a special value, motivating targeted user feedback. See [[wiki/04-llm-based-local-repair|LLM-Based Local Repair]].

### Q7. How does the paper reframe multi-location repair, and what did the authors find in Defects4J v1.2?

> [!tip]- Answer
>
> The authors argue Defects4J-based evaluation of global repair is misguided because the dataset holds multi-fault bugs that decompose into independent single-fault bugs with different failures, whereas developers handle one failure at a time. Their detector found 118 single-fault multi-location bugs in Defects4J v1.2, of which current approaches repaired at most 8, and analysis of a 75-bug sample yielded 8 partial-patch relationships (DU, OA, RIF, DIF, EOH, SU, ONPF, FU) driving tailored global-repair strategies. See [[wiki/04-llm-based-local-repair|LLM-Based Local Repair]].

### Q8. Which cited works ground the paper's claims about benchmarks, overfitting, and test-free repair?

> [!tip]- Answer
>
> The Defects4J benchmark is entry [15], patch plausibility versus correctness is [32], and overfitting is covered by [38] with semantics-based overfitting in [21]. Test-suite efficiency [25], single-fault-fix prevalence [31], and developer testing behavior [4, 19] ground the motivation, while Getafix [2], Phoenix [3], crash-constraint repair [8], iFixR [20], and heap-property repair [41] are the narrow test-free predecessors. See [[wiki/05-global-repair-strategies|REFERENCES — International Conference on Software Engineering (bibliography [1]–[47])]].

### Q9. Which entries in the [48]–[55] reference tail concern multi-location, conditional, and learning-based repair?

> [!tip]- Answer
>
> ITER [50] addresses iterative neural repair for multi-location patches, directly relevant to the paper's global-repair agenda, while Nopol [48] repairs conditional-statement bugs and the syntax-guided edit decoder [55] is a neural repair method. The tail also includes a patch-correctness dataset [49], evolutionary repair [51], a learning-based APR survey [52], an empirical study of real bug fixes [53], and preference-based ensemble repair [54]. See [[wiki/06-references-tail|References Tail: Nopol through Syntax-Guided Repair]].

### Q10. Should a team building an IDE debugging assistant invest in a PracAPR-style interactive test-free loop rather than a test-suite-based batch repair pipeline?

> [!tip]- Answer
>
> Yes for interactive debugging settings: ROSE evidence shows test-free localization and validation can repair dozens of QuixBugs and Defects4J bugs in seconds with a 44% user-success uplift, matching developers' unwillingness to wait minutes or hours. A test-suite-based pipeline remains the better fit where high-quality suites already exist and batch repair is acceptable, since PracAPR's vision depends on debugger state and developer interaction. A team should therefore prototype the interactive loop first and fall back to test-based validation when traces or specifications are unavailable. See [[wiki/03-rose-interactive-test-free-framework|ROSE interactive test-free framework]].
