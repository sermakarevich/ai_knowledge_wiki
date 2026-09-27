> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Research-Level Evaluation on TCS-Bench
**In one sentence:** Colosseum is tested for breadth on the 300-task research-level TCS-Bench, where cross-model selection between Gemini 3.1 Pro and Gemini 3.7 Flash runs reaches 71.0% accuracy, beating all direct-model baselines and each individual Colosseum run.
## Key points
- TCS-Bench contains 300 theorem-proving tasks derived from papers published at FOCS, STOC, and SODA between 2020 and 2026, each supplying the mathematical context and asking for a self-contained proof of a target theorem.
- Candidate proofs are scored by a reference-assisted automated grader that also receives the benchmark's ground-truth proof; its prompt was optimized on a separate set of 100 expert-labeled proofs, on which it reported more than 90% accuracy.
- Colosseum is run separately with Gemini 3.1 Pro and Gemini 3.7 Flash, producing one candidate proof from each run for every problem.
- Selection rule: Gemini 3.7 Flash produces eight independently sampled critiques of the Gemini 3.1 Pro proof; if at least five judge that proof correct it is submitted, otherwise the Gemini 3.7 Flash proof is submitted; the benchmark grader only scores the selected proof and plays no role in selection.
- Individual Colosseum runs score 54.0% (with Gemini 3.1 Pro) and 55.0% (with Gemini 3.7 Flash), far above direct Gemini 3.1 Pro evaluation at 30.3% and above Gemini 3.1 DeepThink at 52.0%.
- Cross-model selection reaches 71.0%, above GPT-5.6 Pro (max) at 68.0%, solving 213 problems — an improvement of 48 problems over the stronger individual run — and is the highest accuracy among evaluated non-oracle methods.
- The two runs have nearly identical accuracy but complementary errors: the critique signal distinguishes grader-labeled correct vs. incorrect proofs with an AUC of 0.896, while routing with Gemini 3.1 Pro's internal verifier alone yields only 64.7%; the oracle best-of-two (fraction solved by at least one run) is 77.3% and is an upper bound rather than an achievable selection rule.
---
## Benchmark setup
**Covers:** Section 6, TCS-Bench description and grader

> "To evaluate the breadth of the system on a common set of research-level problems, we also test Colosseum on TCS-Bench [15]. The benchmark contains 300 theorem-proving tasks derived from papers published at FOCS, STOC, and SODA between 2020 and 2026."

Each task supplies the mathematical context needed to state the problem and asks the model to produce a self-contained proof of a target theorem. Candidate proofs are scored by a reference-assisted automated grader that also receives the benchmark's ground-truth proof. Its prompt was optimized on a separate set of 100 expert-labeled proofs, on which it reported more than 90% accuracy. All benchmark accuracies are measured by this grader.

## Cross-model selection rule
**Covers:** Section 6, how the two Colosseum candidates are combined

> "We run Colosseum separately with Gemini 3.1 Pro and Gemini 3.7 Flash, producing one candidate proof from each run for every problem. To select between the two candidates, Gemini 3.7 Flash produces eight independently sampled critiques of the Gemini 3.1 Pro proof. If at least five critiques judge that proof correct, it is submitted; otherwise, the Gemini 3.7 Flash proof is submitted."

The benchmark grader is used only to score the selected proof and plays no role in the selection rule.

## Results
**Covers:** Section 6, Table 2

| Method | Accuracy |
|---|---|
| Direct model evaluation |  |
| Gemini 3.1 Pro | 30.3% |
| Gemini 3.1 DeepThink | 52.0% |
| GPT-5.6 Pro (max) | 68.0% |
| Colosseum evaluation |  |
| Colosseum with Gemini 3.1 Pro | 54.0% |
| Colosseum with Gemini 3.7 Flash | 55.0% |
| Cross-model selection | 71.0% |
| Oracle best-of-two | 77.3% |

Table 2: Direct-model baselines, two Colosseum runs, and cross-model selection on TCS-Bench. The oracle reports the fraction of problems solved by at least one run and is an upper bound rather than an achievable selection rule.

## Complementarity of the two runs
**Covers:** Section 6, paragraph following Table 2

> "The two individual runs have nearly identical overall accuracy, but their errors are sufficiently complementary for cross-model selection to solve 213 problems, an improvement of 48 problems over the stronger individual run."

The critique signal distinguishes proofs labeled correct and incorrect by the benchmark grader with an AUC of 0.896; routing with Gemini 3.1 Pro's internal verifier alone yields 64.7% accuracy. Among the evaluated non-oracle methods on this dataset, cross-model selection gives the highest accuracy.
