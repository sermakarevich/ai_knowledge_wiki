> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Refactoring Generation: We Use the Code
**In one sentence:** The study feeds each pre-refactoring code segment (one chunk per file in a commit) to StarCoder2 via a zero-shot prompt and evaluates the generated refactorings with Pass@1/3/5 unit-test checks plus code-smell/metric improvement rates and statistical tests against developer refactorings.
## Key points
- Input is the code segment containing the code before refactoring, compared against the developer-refactored code on the same snippets in a commit, with the prompt comprising snippets across the files in a commit.
- The Fig. 2 zero-shot prompt gives the model no additional examples beyond the initial instruction, uses "#" as a delimiter so the LLM focuses on instructions despite a block of code, and chunks snippets as one chunk per file in a commit via a Python script loaded onto an Nvidia A100 GPU.
- Pass@1 generates a single refactored solution per snippet and counts success only if it passes the corresponding unit tests; Pass@3 generates three independent solutions and succeeds if at least one passes all unit tests; Pass@5 generates up to five solutions with the same at-least-one-passes rule.
- When multiple Pass@3/Pass@5 solutions pass, the best is selected first by which reduces the most code smells, then by highest improvement in code metrics (cohesion, coupling, modularity, complexity) on ties.
- Quality is measured with improvement rate IR = (A_before − A_after) / A_before × 100 (Eq. 2), where A is a smell or metric value, computed on three code versions (unrefactored, developer-refactored, LLM-refactored) whose metrics come from the static analysis tool Understand.
- The null hypothesis H0 is tested by comparing unit-test pass rates, smell reduction rates, and metric improvement rates with a Mann-Whitney U-test (non-parametric, no normality assumption) at 5% confidence (p-value < 0.05), with effect size via Cliff's delta (>0.15 small, 0.33–0.47 medium, >0.47 large).
- Table 2 reports LLM median/average pass rates of 26.8%/28.4% (Pass@1), 47.0%/48.5% (Pass@3), 55.4%/57.2% (Pass@5) with SRR medians/averages of 37.5%/39.5%, 39.6%/40.8%, 43.2%/44.4%, versus developers at 100%/100% pass rate and 23.5%/24.3% SRR.
- The findings text reports 28.36% Pass@1, 57.15% average Pass@5 across the 30 projects, an average 20.1% improvement from Pass@1 to Pass@3 and 8.7% from Pass@3 to Pass@5, and recommends comprehensive testing to ensure correctness of StarCoder2 refactorings.
---
## Zero-shot refactoring prompt (Fig. 2)
Instruction (verbatim):
> "You are a powerful model specialized in refactoring Java code. Code refactoring is the process of improving the internal structure, readability, and maintainability of a software codebase without altering its external behavior or functionality. You must output a refactored version of the code."

Prompt template (verbatim):
> "# unrefactored code snippet(java): {code_segment_before_refactoring} # refactored version of the same code snippet:"

Mechanism details from the chunk: zero-shot means the model "receives no additional examples or guidance beyond the initial instruction"; the "#" symbol is used "as a delimiter to ensure the LLM focuses on the instructions even with a block of code in the prompt"; the LLM is specifically prompted to refactor Java code; snippets are broken "into chunks (i.e., one chunk for each file in a commit)"; "We create a zero-shot prompt for each refactoring commit using a Python script, which is loaded onto an Nvidia A100 GPU."

## Test pass rate evaluation (Pass@1 / Pass@3 / Pass@5)
All use the same zero-shot prompt:
- pass@1: "We generate a single refactored solution for each code snippet in a commit. This solution is evaluated by executing the corresponding unit tests. If the refactored solution passes the unit test, it is considered a successful refactoring under the Pass@1 criterion."
- pass@3: "We generate three refactored solutions for each code snippet in a commit. Each solution is independently evaluated by running the corresponding unit tests. If at least one of these three refactored versions passes all unit tests, the refactoring is considered successful under pass@3."
- pass@5: "We generate up to five refactored solutions for each code snippet in a commit. As with pass@3, we run the unit tests on each of the five refactored versions. If at least one solution successfully passes all unit tests, the refactoring is deemed successful under pass@5."

Best-solution tie-break (verbatim rule): "In pass@3 and pass@5 scenarios, if multiple refactoring solutions pass the unit test, we select the best solution by analyzing which solution reduces the most amount of code smells. If two or more solutions pass the unit tests and reduce the same amount of code smells, we select the best solution based on which one has the highest improvement in code metrics (i.e. cohesion, coupling, modularity, and complexity)."

## Improvement rate, measurements, and statistical tests
Improvement rate (Eq. 2): let A_before be the attribute (code smell or code metric) value before refactoring and A_after its value after refactoring:
> IR = (A_before − A_after) / A_before × 100

Code metrics are collected with Understand on three versions: "(1) the unrefactored code, to assess its quality before refactoring; (2) the developer-refactored code, to evaluate its quality after developer refactoring; (3) and the LLM-refactored code, to assess its quality after LLM refactoring."

Null hypothesis (verbatim):
> "H0: The refactoring performed by the LLM is as effective as those performed by human developers in reducing code smells and improving code metrics."

Tests: "We test H0 by comparing unit test pass rates, code smell reduction rates, and code metric improvement rates between the LLM and developers. We perform a Mann-Whitney U-test on the distributions of code smell reduction rates across the 30 projects between developers and the LLM, using a confident level of 5% (i.e., p-value<0.05). The U-test assesses whether two or more samples originate from the same distribution. It does not assume a normal distribution since it is a non-parametric statistical test. We also perform the U-test on the distributions of code metric improvement percentages across the 30 projects for the LLM and developers."

Effect size: "We quantify the differences in the effect size using Cliff's delta (δ), which measures the degree of overlap between the distributions from StarCoder2 and developers. A higher effect size indicates a larger magnitude of the differences between the two approaches for that particular type of code smell. A Cliff's delta greater than 0.15 indicates a small effect size, between 0.33 and 0.47 indicates a medium effect size, and greater than 0.47 indicates a large effect size."

## Findings excerpt and Table 2 (as given in this chunk)
Finding (verbatim framing): "Refactorings generated by StarCoder2 can sometimes propose changes that may affect the functionality of the code." Developers "achieve a 100% unit test pass rate as all of their refactorings are accepted pull requests and maintain the same functionality of the code, while StarCoder2's performance varies across the pass metrics."

Table 2. Comparison of Unit Test Pass Rates and SRR Across the 30 Projects (verbatim numbers):

| Source | Metric | Unit Test Pass Rate (Median) | Unit Test Pass Rate (Average) | SRR (Median) | SRR (Average) |
|---|---|---|---|---|---|
| LLM | Pass@1 | 26.8% | 28.4% | 37.5% | 39.5% |
| LLM | Pass@3 | 47.0% | 48.5% | 39.6% | 40.8% |
| LLM | Pass@5 | 55.4% | 57.2% | 43.2% | 44.4% |
| Developer | - | 100% | 100% | 23.5% | 24.3% |

Findings-text numbers (verbatim): "StarCoder2 achieves a 28.36% pass@1"; "StarCoder2 refactored code has an average unit test pass rate of the 30 projects of 57.15% for the pass@5 metric"; "There is an average of 20.1% improvement in unit test pass rate from pass@1 to pass@3 and an average of 8.7% improvement in unit test pass rate from pass@3 to pass@5"; "The refactored code generated by StarCoder2 achieves a 57.15% unit test pass rate at Pass@5, indicating substantial improvement over Pass@1 (28.36%) and Pass@3 (8.7%)." Recommendation (verbatim): "Therefore, it is recommended to have comprehensive testing when utilizing LLMs like StarCoder2 to ensure the correctness and integrity of the refactored code."

Note: Figs. 3–5 in this chunk are distribution plots (unit-test pass rates, code-smell counts, smell reduction rates across the 30 projects) rendered as figure images without extractable data values in the chunk text.

**Covers:** Refactoring generation method: zero-shot prompt (Fig. 2) and Pass@1/3/5 plus improvement-rate/statistical evaluation (chunk §3.1.2–3.1.3 including Table 2 and Eq. 2).
