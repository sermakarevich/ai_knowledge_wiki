> [[index|Wiki]] | [[summary|Summary]]
# Towards Practical and Useful Automated Program Repair for Debugging — Digest
## 1. [[wiki/01-motivation-and-pracapr-vision|Motivation and PracAPR Vision]]
**In one sentence:** Current APR is impractical for realistic debugging because it assumes a comprehensive test suite and frequent re-execution, is too slow, and cannot fix multi-location complex bugs — so the authors envision PracAPR, an interactive IDE repair system that works from a suspended debugger state without tests or re-execution.
## Key points
- Debugging consumes up to 50% of programming time [6], motivating APR, which aims to automatically generate a patch correcting a buggy program's misbehavior.
- Over a decade, more than 60 APR techniques [29, 36] have been developed, classified as pattern-based, constraint-based, search-based, and learning-based.
- Current APR assumes a (high-quality) test suite as the correctness criterion, which is unrealistic: developers often write too few tests or none at all [4, 19], bugs are often reported without a revealing test suite [20], and bug-revealing tests for over 90% of Defects4J bugs [15] were introduced only after the bug was identified.
- Prior test-free repair techniques [2, 3, 8, 20, 41] are restricted to specific bug types (e.g., heap-property faults [41]) or static-analyzer-flagged issues, not general semantic bugs arising while debugging.
- Frequent program re-execution for validation is impractical because recreating the failure environment is difficult when the failure appears after a long run or in an interactive session, and it makes repair slow: minutes (e.g., [14]) or even hours per bug [25], while developers prefer not to wait long [30].
- PracAPR is envisioned as an interactive repair system in the IDE that requires no test suite and no program re-execution, assuming the developer uses an IDE debugger with the program suspended where the problem is observed.
- PracAPR's pipeline is: interact with the developer to obtain a problem specification, then test-free flow-analysis-based fault localization, patch generation combining LLM-based local repair with tailored strategy-driven global repair, and re-execution-free validation via simulated trace comparison.
## 2. [[wiki/02-pracapr-architecture-and-pipeline|PracAPR Architecture and Pipeline]]
**In one sentence:** PracAPR is an envisioned IDE-integrated repair system that, starting from a debugger-stopped program and a developer-provided problem specification, performs test-free fault localization, local plus global patch generation, and re-execution-free patch validation to present previewable repair suggestions.
## Key points
- PracAPR is designed to work in conjunction with an IDE debugger, assuming the program is stopped at a location where a problem is observed.
- It interacts with the developer to obtain a description of the problem (the problem specification) and drives fault localization, patch generation, and patch validation from that description.
- It removes the unrealistic test-suite assumption: it does not assume the existence of a test suite and does not require program re-execution.
- Fault localization is flow-analysis-based and takes into account the problem symptom, current values from the debugger, and the current runtime stack to compute a backward slice containing potential repair locations.
- Patch generation is split into local and global repair, to be discussed later in the source.
- Patch validation generates simulated traces via a live programming mechanism that reflect the real executions of the original and repaired programs, then compares the traces to infer patch correctness.
- The developer can choose to preview any of the repairs and further accept it to allow changes to be applied to the program.
## 3. [[wiki/03-rose-interactive-test-free-framework|ROSE interactive test-free framework]]
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
## 4. [[wiki/04-llm-based-local-repair|LLM-Based Local Repair]]
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
## 5. [[wiki/05-global-repair-strategies|REFERENCES — International Conference on Software Engineering (bibliography [1]–[47])]]
**In one sentence:** This chunk is the paper's bibliography entries [1]–[47] on automated program repair, fault localization, debugging, and related empirical studies, with no argumentative prose beyond the citation records and a footer line.
## Key points
- The chunk contains numbered bibliography entries [1] through [47], with entry [47] truncated mid-title ("Keep the Conversation Go-ing: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT.").
- Publication years in the chunk range from 2008 ([18] Ko and Myers) to 2024 ([7] Eladawy et al.; [36] RepairTools 2024).
- Venues named include ICSE, ASE, ISSTA, FSE/ESEC-FSE, OOPSLA, TOSEM, TSE, Commun. ACM, CSUR, ICST, Quality Software, APR workshop, SEEDE/ASE, and arXiv preprints.
- APR approaches cited include template-based TBar [24], semantics/symbolic Angelix [26], GenProg [22], search-based anti-patterns [40], multi-hunk evolution [37], VarFix [44], context-aware patch generation [43], and bug-report-driven iFixR [20].
- Learning/LLM-based repair cited includes Getafix [2], CURE [14], DEAR [23], ChatGPT bug-fixing performance [39], Copiloting the Copilots [42], zero-shot repair [46], large pre-trained LM repair [45], fine-tuning study [10], code-LM impact [13], and patch prioritization with language models [16].
- Empirical/foundational entries include Defects4J [15], patch plausibility vs. correctness [32], overfitting in repair [38] and in semantics-based repair [21], test-suite efficiency [25], single-fault-fix prevalence [31], developer testing behavior [4] and test adoption [19], plus debugging UI work Code Bubbles [5], Whyline-style debugging [18], and reversible debugging [6].
- Author self-citations present are Reiss/Xin SEEDE [35], Quick Repair Facility [34], Quick Repair of Semantic Errors [33], alongside surveys/bibliographies E-APR mapping [1], APR survey [11], CACM APR overview [9], APR bibliography [28], and Living Review [29].
## 6. [[wiki/06-references-tail|References Tail: Nopol through Syntax-Guided Repair]]
**In one sentence:** This chunk contains only bibliography entries [48]–[55] (Nopol through syntax-guided neural repair) with no argumentative prose, methods, results, or claims beyond publication metadata.
## Key points
- [48] Jifeng Xuan et al. (2016) published "Nopol: Automatic repair of conditional statement bugs in Java programs" in IEEE Transactions on Software Engineering 43(1), pages 34–55.
- [49] Jun Yang et al. (2022) published the arXiv preprint arXiv:2207.06590, "Attention: Not just another dataset for patch-correctness checking".
- [50] He Ye and Martin Monperrus (2023) published the arXiv preprint arXiv:2304.12015 (chunk header cites arXiv:2304.00385 (2023)), "ITER: Iterative Neural Repair for Multi-Location Patches".
- [51] Yuan Yuan and Wolfgang Banzhaf (2020) published "Toward better evolutionary program repair: An integrated approach" in ACM TOSEM 29(1), pages 1–53.
- [52] Quanjun Zhang et al. (2023) published "A Survey of Learning-based Automated Program Repair" as arXiv preprint arXiv:2301.03270 (2023).
- [53] Hao Zhong and Zhendong Su (2015) published "An empirical study on real bug fixes" in Proceedings of IEEE/ACM ICSE Vol. 1, pages 913–923.
- [54] Wenkang Zhong et al. (2023) published "Practical Program Repair via Preference-based Ensemble Strategy" as arXiv preprint arXiv:2309.08211 (to appear in ICSE'24).
- [55] Qihao Zhu et al. (2021) published "A syntax-guided edit decoder for neural program repair" in Proceedings of ACM ESEC/FSE 2021, pages 341–353.
## The argument in five moves
1. Realistic debugging has no high-quality test suite and no cheap re-execution, yet current APR assumes both, runs for minutes to hours, and rarely handles multi-location bugs — motivating a new practical vision.
2. PracAPR answers with an IDE repair pipeline starting from a debugger-suspended program and a developer-provided problem specification, chaining test-free flow-analysis fault localization, local plus global patch generation, and re-execution-free simulated-trace validation into previewable suggestions.
3. ROSE provides the test-free framework PracAPR builds on: preview-with-differences interaction, fault localization covering 89% of tested bugs, top-5 validation of all correct repairs, 36/40 QuixBugs and 37/60 Defects4J repaired in seconds, and a user study with 44% more successes and ~16.5% less debugging time.
4. ChatGPT-based local repair shows shallow failure info (buggy location plus input and failing assertion) misdiagnoses the Chart_3 minY/maxY bug, while an augmented prompt with test input, related methods like `add`, and traced state plus user feedback, conversational reflection, pattern/search guidance, and post-processing points toward reliable single-location patches.
5. Single-fault multi-location repair is reframed away from Defects4J's decomposable multi-fault bugs toward 118 detected single-fault multi-location bugs (current tools fix at most 8), whose 75-sample analysis yields 8 partial-patch relationships (DU, OA, RIF, DIF, EOH, SU, ONPF, FU) for tailored global strategies.
6. The bibliography [1]–[55] grounds the arc in APR families, test-free and LLM repair, Defects4J and overfitting empirics, and debugging UI foundations, closing with the goal of making APR an everyday part of debugging.
