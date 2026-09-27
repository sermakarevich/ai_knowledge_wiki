> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# RQ1: Can LLMs Outperform Developers in Code Refactoring?
**In one sentence:** RQ1 asks whether StarCoder2 can reliably automate code refactoring by comparing its refactoring distribution, code-smell reduction (44.36% vs 24.27% for developers), and code-metric improvements against developers, using a controlled setup of 30 leak-free Java projects with pure-refactoring commits.
## Key points
- RQ1 compares StarCoder2-generated refactorings against developer refactorings on the same files (pre-refactoring state), measuring refactoring-operation distribution, code-smell reduction, and code-metric quality improvement.
- StarCoder2 reduces code smells by 44.36% versus 24.27% for developers, and the chunk states it "often surpassing developers" on code-metric quality improvements.
- The study starts from the 20-MAD dataset (765 Apache projects), filters to 195 Java projects, removes 135 projects overlapping StarCoder2 training data to avoid leakage, and ends with a final 30 Java projects balanced by refactoring-commit count (median threshold 129).
- Only pure-refactoring commits are used: a commit is kept when its Refactoring Ratio (Refactoring Code Churn / Total Code Churn × 100%) equals 100%, using 59 refactoring types detected by RMiner (reported precision 99.7%, recall 94.2%).
- Code smells are extracted before and after each refactoring commit with DesigniteJava 2.5.2, which detects 46 smell types (7 architecture, 18 design, 9 implementation, 4 testability, 8 test smells).
- The chunk also previews RQ2–RQ4 claims: StarCoder2 wins on systematic/repetitive smells and within-class refactorings, developers win on complex context-dependent smells and multi-class refactorings, and one-shot prompting (34.51% test pass, 42.97% SRR) beats zero-shot and chain-of-thought.
---
## 1. RQ1 motivation and comparison design
**Covers:** RQ1 statement through experiment overview (Fig. 1)

Verbatim research question (from chunk):

> "RQ1: Can LLMs outperform developers in code refactoring? We aim to assess whether StarCoder2 can be used as a reliable solution to automate code refactoring."

Comparison dimensions stated in the chunk:

| Dimension | What is compared |
|---|---|
| Refactoring operations | Distribution of refactoring operations performed by StarCoder2 vs developers |
| Effectiveness (smells) | Reduction of code smells |
| Effectiveness (quality) | Improvement on code quality measured by various code metrics |

Headline RQ1 result stated in the chunk:

| Actor | Smell reduction rate |
|---|---|
| StarCoder2 | 44.36% |
| Developer | 24.27% |

Verbatim: "We observe that StarCoder2 achieves a significantly higher performance in reducing code smells by 44.36%, compared to a 24.27% reduction rate for the developer." Verbatim on metrics: "StarCoder2 excels in improving code quality measured by code metrics, often surpassing developers in these areas."

Generation protocol (from chunk): "we prompt StartCoder2 [sic] to generate refactorings on each extracted file in a commit before the developers' refactoring operations."

Approach overview (Fig. 1 in source) has three columns: Data Preparation (195 Java Projects → Project Selection → 30 Java Projects; Refactoring Commits Selection; Unit Test Generation; Code Smell and Metrics Extraction), Results Analysis (Unit Test Execution; Refactorings Generation; Code Smell Extraction; Code Metrics Extraction), and RQs (RQ1–RQ4 as listed in the chunk caption).

## 2. RQ2–RQ4 preview as stated in this chunk
**Covers:** RQ2/RQ3/RQ4 paragraphs and contributions list

These are context for RQ1, quoted/summarised only as written in this chunk:

- RQ2 ("Which types of code smells are most effectively reduced by LLMs or developers?"): "StarCoder2 outperforms developers to address systematic and repetitive issues, such as condensing a long statement or shortening a long parameter list. However, developers show superiority in handling complex, context-dependent code smells, such as correcting a broken modularization or deficient encapsulation."
- RQ3 ("Which refactoring types are most effective for improving code quality?"): "StarCoder2 is particularly effective in refactoring types that improve code within a class. Developers on the other hand excel in refactoring types that involve changes affecting multiple classes."
- RQ4 ("How does prompt engineering affect the quality of LLM-generated refactorings?"): one-shot prompting "yields the highest unit test pass rate of 34.51%, marking an improvement of 6.15% over zero-shot prompting, and a smell reduction rate (SRR) of 42.97%, which is an increase over the zero-shot prompt by 3.52%"; chain-of-thought (with refactoring-type suggestions plus a definition) "achieves a 32.22% unit test pass rate and a 42.34% SRR, which improves upon the numbers from the zero-shot prompting by 3.86% and 2.89% respectively."
- Contributions claimed: comprehensive evaluation of StarCoder2; an evaluation framework focused on quality improvement and functionality preservation; comparison of chain-of-thought and one-shot prompting with practical guidance; replication package at `https://github.com/Software-Evolution-Analytics-Lab-SEAL/LLM_Refactoring_Evaluation`.
- Paper organization: Section 2 experiment setup; Section 3 RQ motivation/approaches/results; Section 4 threats to validity; Section 5 related work; Section 6 conclusion and future directions.

## 3. Experiment setup: project selection
**Covers:** §2–§2.1 Project Selection

- Starting dataset: "the 20-MAD dataset [10], which includes 765 Apache projects," limited to primarily-Java projects because Java refactoring-detection tools perform strongly and refactoring practice is well-established there.
- Exclusion filters producing 195 Java projects: (1) less than 80% Java source code; (2) fewer than the 1st quantile of commit counts (i.e., < 1,021 commits); (3) short lifespan (i.e., < one-year of commit history); and (4) as written, projects with less than one-year of commit history, on the rationale that longer-lived, higher-commit projects likely have more refactorings.
- Leakage control: "we filter out the 135 Java projects from our initial dataset that are included in the StarCoder2."
- Balance filter: projects with fewer than the median number (i.e., 129) of refactoring commits are removed, leaving "a final 30 Java projects for our analysis."
- Refactoring labels come from a previous study's dataset of the 195 Java Apache projects (chunk also says "We use the commits of the 60 projects from this dataset"), with refactorings detected by RMiner [47] covering "59 different types of refactorings" plus modified lines for code churn; prior evaluation reports "an overall precision of 99.7% and a recall of 94.2%."

## 4. Data processing: pure-refactoring commits and smell extraction
**Covers:** §2.2–§2.2.2 Code Smell Extraction

Refactoring-commit rule (to match the developer task to StarCoder2's task and exclude development/bug-fix churn):

> "we select commits that 100% of the lines of code churn consist of refactoring operations."

Equation (1) as given:

> Refactoring Ratio of Commit (i) = Refactoring Code Churn of Commit (i) / Total Code Churn of Commit (i) × 100%

Verbatim rule: "If the code churn is entirely due to refactoring (i.e., Ratio = 100%), then the commit is classified as a refactoring commit." Code churn is defined as "the sum of lines added and removed during a commit," and refactoring code churn as "the sum of lines added and removed in the process of a refactoring operation."

Smell extraction: "We use DesigniteJava 2.5.2 [40] to extract code smells by inputting the source code of each Java file from before and after each refactoring commit," with "comprehensive coverage" across 46 types:

| Category | Count | Examples / description as given |
|---|---|---|
| Architecture smells | 7 | System-architecture issues, e.g. unstable dependencies relying on frequently changing modules |
| Design smells | 18 | Poor design-principle adherence hurting modularity/flexibility/reusability, e.g. unnecessary abstraction |
| Implementation smells | 9 | Source-level maintainability/understanding issues, e.g. large classes, repeated code, very long methods |
| Testability smells | 4 | Design choices hindering test-case development, e.g. hard-wired dependencies and excessive dependency |
| Test smells | 8 | Bad unit-test practices indicating test-code design problems, e.g. empty test, unknown test, constructor initialization |

**Covers:** RQ1–RQ4 overview paragraphs, contributions, paper organization, and §2–§2.2.2 (approach overview, project selection, refactoring-commit rule, smell extraction) as contained in chunk 02.
