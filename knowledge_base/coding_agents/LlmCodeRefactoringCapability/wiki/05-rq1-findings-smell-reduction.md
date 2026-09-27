> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# StarCoder2 has better performance in code
**In one sentence:** On refactorings that pass unit tests, StarCoder2 reduces code smells by 44.36% versus 24.27% for developers (20.1 points higher, U-test p=0.003) and achieves a higher average code-metric improvement (19.32% vs 17.46%), leading on cohesion and cyclomatic complexity while developers lead on class coupling.
## Key points
- Initial unrefactored code has 17,429 smells; developer refactoring leaves 13,199 smells (24.27% reduction), while StarCoder2's test-passing subset goes from 12,213 to 6,795 smells (44.36% reduction), 20.1 points higher than developers.
- The U-test for code smell reduction gives p=0.003, and the chunk rejects null hypothesis H0, concluding StarCoder2 performs significantly better in smell reduction and metric improvements.
- From Pass@1 to Pass@5 the smell reduction rate rises 4.91%, driven by Rebellious Hierarchy Smell (+5.18%), Long Method (+8.76%) and Long Statement (+6.32%), with all other smells consistent; the best pass@5 generation is used for the remaining RQs.
- Across Table 3 metrics StarCoder2 averages 19.32% improvement (median 18.2%) versus 17.46% for developers (median 16.9%), with a Pass@5 unit-test pass rate of 57.15% versus 100% for developers.
- StarCoder2 leads on cohesion/modularity: CountDeclInstanceVariable 19.7% vs 17.0%, PercentLackOfCohesion 22.8% vs 20.4%, and PercentLackOfCohesionModified 23.9% vs 21.5% (Cliff's Delta 0.42, Medium).
- StarCoder2 leads on complexity: AvgCyclomatic 17.4% vs 14.6% (Cliff's Delta 0.45, Medium) and SumCyclomatic 18.6% vs 15.9% (Cliff's Delta 0.47, Medium), plus Cyclomatic 16.5% vs 13.5% and MaxCyclomatic 15.8% vs 13.3%.
- Developers lead on coupling-related metrics: CountClassCoupled 24.1% vs 21.4% for StarCoder2, and CountDeclClassVariable 14.9% vs 12.5%, suggesting an edge where deep understanding of class dependencies and variable declarations is required.
---
## 1. Smell counts, reduction rates, and significance
**Covers:** RQ1 findings text around Figures 3/5 (p. 10)

- Dataset baseline: "The initial dataset representing unrefactored code contains 17,429 code smells."
- Developers: "we observe 13,199 code smells, a code smell reduction rate of 24.27%."
- StarCoder2 (only test-passing generations counted): "For code that StarCoder2 passes unit tests for, there is an initial 12,213 code smells before refactoring; we do not include code smells to calculate code smell reduction from code that StarCoder2 cannot successfully generate refactorings for (i.e., the refactorings pass unit tests). StarCoder2 reduces the initial number of code smells from 12,213 to 6,795 showing a code smell reduction rate of 44.36% for 30 projects."

| Actor | Smells before | Smells after | Reduction rate |
|---|---|---|---|
| Developers (all 30 projects) | 17,429 | 13,199 | 24.27% |
| StarCoder2 (test-passing subset) | 12,213 | 6,795 | 44.36% |

- Headline gap: "StarCoder2 reduces code smells at a 20.1% higher rate than developers in our experiments." / "StarCoder2 reduces smells by 44.36%, outperforming developers who achieve a 24.27% reduction, making StarCoder2 20.1% more effective in improving code quality through smell reduction."
- Significance: "The results of the U-test for code smell reduction show a p-value of 0.003, indicating a significant difference in the distribution of code smells per commit before refactoring, after developer refactoring, and after LLM refactoring."

## 2. Pass@k effect and analysis choice
**Covers:** Pass@1/Pass@3/Pass@5 paragraph (p. 10–11)

- "Upon analyzing the 4.91% increase in code smell reduction rate from Pass@1 to Pass@5, we observed a notable rise in the reduction rates of the Rebellious Hierarchy Smell (5.18%), along with improvements in reducing Long Method (8.76%) and Long Statement Smells (6.32%)."
- "The reduction rates for all other code smells remained consistent across Pass@1, Pass@3, and Pass@5."
- Interpretation as written: "This suggests that regenerating refactorings multiple times can enhance the effectiveness of code smell reduction, as the LLM may hallucinate for some refactoring generations that attempt to address complex code smells."
- Analysis decision: "We use the best refactoring generation from pass@5 to answer the remaining research questions. Pass@5 shows better performance than pass@1 and pass@3 in passing unit tests and therefore results in more valid refactorings to analyze. Taking the best refactoring generation from pass@5 results in more data for analyzing refactoring types performed by the LLM as well as code smell types reduced by the LLM."

## 3. Code quality metrics: StarCoder2 vs developers (Table 3)
**Covers:** Table 3 and surrounding metric discussion (pp. 10–11)

Verbatim framing: "The results presented in Table 3 provide a quantitative analysis of the refactoring capabilities of StarCoder2 compared to developers, where a higher percentage reduction indicates a greater ability to improve code quality."

Table 3. Comparison of Improvement in Metrics (%) Over 30 Projects Between StarCoder2 and Developers (Cliff's Delta shown for significantly improved metrics):

| Metric | Quality attribute | LLM (Avg) | LLM (Median) | Dev (Avg) | Dev (Median) | Cliff's Delta (Interpretation) |
|---|---|---|---|---|---|---|
| CountClassCoupled | Coupling | 21.4 | 20.1 | 24.1 | 23.5 | - |
| CountClassCoupledModified | Coupling | 18.3 | 17.5 | 16.8 | 16.2 | - |
| CountClassDerived | Modularity | 17.9 | 16.8 | 15.2 | 14.7 | - |
| CountDeclClassVariable | Modularity | 12.5 | 11.8 | 14.9 | 14.4 | - |
| CountDeclInstanceVariable | Modularity | 19.7 | 18.9 | 17.0 | 16.5 | - |
| PercentLackOfCohesion | Cohesion | 22.8 | 21.7 | 20.4 | 19.9 | - |
| PercentLackOfCohesionModified | Cohesion | 23.9 | 22.8 | 21.5 | 20.7 | 0.42 (Medium) |
| AvgCyclomatic | Complexity | 17.4 | 16.3 | 14.6 | 14.0 | 0.45 (Medium) |
| Cyclomatic | Complexity | 16.5 | 15.4 | 13.5 | 13.0 | - |
| MaxCyclomatic | Complexity | 15.8 | 14.9 | 13.3 | 12.8 | - |
| SumCyclomatic | Complexity | 18.6 | 17.4 | 15.9 | 15.1 | 0.47 (Medium) |
| Average | - | 19.32 | 18.2 | 17.46 | 16.9 | - |

- Cohesion/modularity (StarCoder2 leads): "StarCoder2 achieves a 19.7% average reduction in instance variables (i.e., CountDeclInstanceVariable), outperforming developers, who achieve a 17.0% reduction. Similarly, StarCoder2 leads in reducing PercentLackOfCohesion by 22.8% compared to 20.4% for developers." / "StarCoder2 shows a significant improvement in reducing PercentLackOfCohesionModified, with a 23.9% reduction compared to 21.5% for developers, demonstrating a moderate effect size of 0.42 (Cliff's Delta)."
- Coupling (developers lead): "developers outperform StarCoder2 in reducing the number of coupled classes (i.e., CountClassCoupled and CountDeclClassVariable), with average reductions across 30 projects of 24.1% and 14.9%, respectively. This suggests that while StarCoder2 excels in several areas, developers may still have an edge in refactoring tasks that require a deep understanding of class dependencies and variable declarations."
- Complexity (StarCoder2 leads): "The model reduces AvgCyclomatic by 17.4% and SumCyclomatic by 18.6%, compared to reductions of 14.6% and 15.9% by developers, respectively. Notably, the reduction in SumCyclomatic has a medium effect size of 0.47, highlighting StarCoder2's effectiveness in simplifying code logic across entire projects."
- Hypothesis verdict: "We reject the null hypothesis H0 as StarCoder2 performs significantly better in code smell reduction and various code quality metric improvements compared with developers."

## 4. Chunk's summary box and RQ2 transition present in this chunk
**Covers:** "Summary of Results" box; §3.2–§3.2.2 opening through Table 4 header (pp. 11–12)

Verbatim summary box (quoted in full as given):

> "StarCoder2 outperforms developers across most evaluated code metrics, achieving an average reduction across all metrics of 19.32% compared to 17.46% for developers, demonstrating its strength in automating complex refactoring tasks. StarCoder2 improves unit test pass rates significantly, reaching 57.15% at Pass@5, though developers maintain a 100% pass rate. StarCoder2 excels in code smell reduction, reducing smells by 44.36%, which is 20.1% higher than developers, and particularly effective in addressing smells like long methods and rebellious hierarchy. It also shows superior performance in reducing cohesion and complexity metrics, achieving greater modularity and structure. However, developers outperform StarCoder2 in reducing class coupling, highlighting their advantage in tasks requiring a deeper understanding of class dependencies. Despite this, StarCoder2's ability to simplify code logic and reduce cyclomatic complexity makes it a valuable tool for improving code maintainability."

RQ2 transition also present in this chunk (context only; full RQ2 belongs to chunk 06):

- RQ2 stated as "RQ2. Which types of code smells are most effectively reduced by LLMs or developers?"
- Motivation claims quality refactorings are linked with smell elimination, smells range "from simple syntactic issues, such as Long Statement and Empty Catch Clause, to more complex design flaws, such as Insufficient Modularization and Multifaceted Abstraction," and notes "Developers have domain knowledge and an understanding of software design principles, while LLMs can apply their extensive training on code patterns and idioms to address repetitive and rule-based smells."
- Approach in chunk: "we compare the performance of StarCoder2 and developers in code smell reductions and quantify the differences for each specific type of code smell. Specifically, we examine each commit that contains at least one instance of a code smell," using the "Mann-Whitney U-test [25]" because "our data does not follow a normal distribution."
- The chunk ends at the header "Table 4. Comparison of Code Smell Reductions Between StarCoder2 and Developers." with no Table 4 rows contained in this chunk.

**Covers:** RQ1 findings on smell reduction (17,429→13,199 dev vs 12,213→6,795 StarCoder2; 44.36% vs 24.27%; p=0.003), Pass@1→Pass@5 +4.91% detail, Table 3 metric comparison (avg 19.32% vs 17.46%), Summary of Results box (Pass@5 57.15% vs dev 100%), and RQ2 intro through Table 4 header as contained in chunk 05.
