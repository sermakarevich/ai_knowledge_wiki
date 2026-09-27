---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: An Empirical Study on the Code Refactoring Capability of Large Language Models

### Q1. What are the three stated goals of the study and why was StarCoder2-15B-instruct chosen?
> [!tip]- Answer
> The goals are to compare LLM vs developer refactoring on code-quality improvement, to compare the refactoring types each applies and their effectiveness, and to test whether one-shot and chain-of-thought prompting improve LLM refactoring. See [[wiki/01-empirical-study-overview|Empirical Study Overview]].
> StarCoder2-15B-instruct (46.3% pass@1 on HumanEval) was chosen because it trains on the public Stack v2 dataset, so the authors could select 30 Java projects outside that dataset to mitigate data leakage. See [[wiki/01-empirical-study-overview|Empirical Study Overview]].

### Q2. How does RQ1 set up a leakage-controlled comparison, and what counts as a pure-refactoring commit?
> [!tip]- Answer
> RQ1 compares StarCoder2 against developers on the same pre-refactoring files across 30 Java projects, measuring refactoring-operation distribution, DesigniteJava smell reduction, and Understand metric improvement. See [[wiki/02-rq1-llm-vs-developers|RQ1: Can LLMs Outperform Developers in Code Refactoring?]].
> The pipeline filters 765 Apache projects (20-MAD) to 195 Java projects, drops 135 overlapping training data, keeps 30 above the median refactoring-commit count, and keeps only commits whose Refactoring Ratio equals 100% using RMiner's 59 refactoring types. See [[wiki/02-rq1-llm-vs-developers|RQ1: Can LLMs Outperform Developers in Code Refactoring?]].

### Q3. Which four quality attributes do the Understand metrics cover, and what does each attribute capture?
> [!tip]- Answer
> The metrics cover complexity, cohesion, coupling, and modularity, with Table 1 listing each metric's description and rationale (e.g., Avg/Max/Sum Cyclomatic for complexity, Percent Lack of Cohesion variants for cohesion). See [[wiki/03-experiment-setup-metrics|Code Metrics Computation (Experiment Setup)]].
> Modularity gauges division into independent components, coupling gauges inter-class interdependence (lower is better), and cohesion gauges how closely a class's responsibilities relate (higher is better). See [[wiki/03-experiment-setup-metrics|Code Metrics Computation (Experiment Setup)]].

### Q4. How are StarCoder2 refactorings generated and judged under Pass@1/3/5?
> [!tip]- Answer
> Each pre-refactoring snippet (one chunk per file in a commit) is fed to StarCoder2 with the Fig. 2 zero-shot prompt ("#" delimiters, no examples) on an Nvidia A100, then Pass@1/3/5 counts success if at least one of 1, 3, or 5 generations passes all unit tests. See [[wiki/04-refactoring-generation-method|Refactoring Generation: We Use the Code]].
> Ties among passing generations are broken first by largest smell reduction, then by best metric improvement, and quality is scored with IR = (A_before − A_after) / A_before × 100 plus Mann-Whitney U-tests (p < 0.05) and Cliff's delta. See [[wiki/04-refactoring-generation-method|Refactoring Generation: We Use the Code]].

### Q5. What are the headline RQ1 results on smell reduction, metric improvement, and test passing?
> [!tip]- Answer
> On the test-passing subset StarCoder2 cuts smells from 12,213 to 6,795 (44.36%) versus developers' 17,429 to 13,199 (24.27%), a 20.1-point gap with U-test p = 0.003, and averages 19.32% metric improvement versus 17.46% for developers. See [[wiki/05-rq1-findings-smell-reduction|StarCoder2 has better performance in code]].
> StarCoder2 leads on cohesion (e.g., PercentLackOfCohesionModified 23.9% vs 21.5%) and complexity (AvgCyclomatic 17.4% vs 14.6%, SumCyclomatic 18.6% vs 15.9%), while developers lead on coupling (CountClassCoupled 24.1% vs 21.4%) despite only 57.15% Pass@5 versus developers' 100%. See [[wiki/05-rq1-findings-smell-reduction|StarCoder2 has better performance in code]].

### Q6. Which smell types does StarCoder2 win versus developers, and what mechanism explains the split?
> [!tip]- Answer
> StarCoder2 wins 10 of 16 types: 7 of 8 implementation smells (Long Statement, Magic Number, Empty Catch Clause, Complex Conditional, Long Parameter List, Long Identifier, Complex Method, all Large δ ≈ 0.53–0.63) plus Unutilized/Unnecessary Abstraction, Broken Hierarchy, and Cyclic-Dependent Modularization. See [[wiki/06-rq2-code-smell-types|RQ2: Which Code-Smell Types Do LLMs vs Developers Reduce Best?]].
> Developers win Missing Default plus Broken Modularization, Deficient Encapsulation, Insufficient Modularization, and Multifaceted Abstraction, because StarCoder2 suits structured rule-based fixes while developer-won smells need architecture, dependency, and encapsulation reasoning. See [[wiki/06-rq2-code-smell-types|RQ2: Which Code-Smell Types Do LLMs vs Developers Reduce Best?]].

### Q7. What can and cannot be recovered from the Figure 6 chunk on refactoring-type frequencies?
> [!tip]- Answer
> Only labels are recoverable: the caption "Distribution of Frequencies of all Refactoring Types Used by StarCoder2 Across 30 Projects," axes (Refactoring Count vs Refactoring Types), an LLM/Developer legend, and ~28 type names such as Rename Parameter, Move Method, and Change Attribute Access Modifier. See [[wiki/07-rq3-refactoring-types|RQ3: Comparison of Refactoring Types (LLM vs Developers)]].
> No per-type counts, rankings, or LLM-vs-developer differences are parseable from the garbled rendering, so no comparison claim can be drawn from this chunk alone. See [[wiki/07-rq3-refactoring-types|RQ3: Comparison of Refactoring Types (LLM vs Developers)]].

### Q8. How do LLM and developer refactoring-type preferences and their payoffs differ?
> [!tip]- Answer
> StarCoder2 favors syntactic, high-frequency edits (Rename/Extract Method, annotation changes, Change Type Declaration Kind, Move Package) while developers favor structural, dependency-heavy edits (Move Method, Change Attribute Access Modifier, Extract Superclass, Pull Up Method, Move Source Folder). See [[wiki/08-rq3-findings-preferences|RQ3 Findings: Distinct Preferences in Refactoring Types]].
> StarCoder2 wins 9 of 11 significant smell-reduction types (e.g., Remove Method Annotation δ = 0.9619) and 3 of 5 metric types, while developers win Move Attribute and Change Attribute Type on smells plus Encapsulate Attribute and Change Attribute Access Modifier on metrics. See [[wiki/08-rq3-findings-preferences|RQ3 Findings: Distinct Preferences in Refactoring Types]].

### Q9. How do one-shot and chain-of-thought prompts compare to zero-shot for StarCoder2 refactoring?
> [!tip]- Answer
> One-shot leads (34.51% test pass, 42.97% SRR, Rank 1), chain-of-thought is close (32.22%, 42.34%, Rank 1), and zero-shot trails (28.36%, 39.45%, Rank 2), showing vague instructions limit autonomous refactoring. See [[wiki/09-rq4-prompt-engineering|RQ4: Prompt Engineering — One-shot and Chain-of-Thought]].
> One-shot tops complexity metrics and CountClassCoupledModified while chain-of-thought tops CountClassCoupled and CountDeclClassVariable and adds seven new types (Extract/Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, Parameterize Variable), judged by Scott-Knott clustering. See [[wiki/09-rq4-prompt-engineering|RQ4: Prompt Engineering — One-shot and Chain-of-Thought]].

### Q10. What validity limits and related-work positioning frame the conclusion?
> [!tip]- Answer
> Identical-server runs still face hallucination, single-commit sampling, residual training-pattern overlap (internal); Java/Apache-only scope and StarCoder2-15B-Instruct-v0.1 specificity (external); and smell/metric/pass-rate plus RMiner3.0, DesigniteJava, and Understand tool dependence missing readability and performance (construct). See [[wiki/10-rq4-results-validity|RQ4 Results Context and Validity Under Identical Conditions]].
> Related work spans pre/post-LLM generation (DeepCoder, AlphaCode, Codex), LLM refactoring (e.g., Shirafuji GPT-3.5: 95.68% pass@10, 17.35% complexity cut), and prompting/fine-tuning (few-shot, CoT, SCoT), with this study's differentiator being the StarCoder2-vs-developer smell/metric comparison. See [[wiki/10-rq4-results-validity|RQ4 Results Context and Validity Under Identical Conditions]].

### Q11. Which works do bibliography entries [1]–[33] cite for LLM foundations, refactoring, and statistics?
> [!tip]- Answer
> LLM foundations include Brown et al. 2020 (GPT-3), Chowdhery et al. 2022 (PaLM), Kojima et al. 2022 (zero-shot reasoners), Li et al. 2023 (StarCoder), Li et al. 2022 (AlphaCode), and Lozhkov et al. 2024 (StarCoder 2). See [[wiki/11-threats-related-work|References [1]–[33] — First Bibliography Segment]].
> Refactoring sources include Fowler 2018/1999, Opdyke and Johnson 1992, Mens and Tourwé 2004, and Cedrim et al. 2017, with statistics from Jelihovschi et al. 2014 (ScottKnott), McKnight and Najab 2010 (Mann-Whitney U), and Meissel and Yao 2024 (Cliff's Delta). See [[wiki/11-threats-related-work|References [1]–[33] — First Bibliography Segment]].

### Q12. Which works do references [34]–[54] cite for smells, detection tooling, and LLM-for-code evaluation?
> [!tip]- Answer
> Smell and mining works include Palomba et al. 2018 [34], Pantiuchina et al. 2020 [35], Silva et al. 2016 [43], and RefactoringMiner 2.0/Tsantalis et al. 2018 [46][47]. See [[wiki/12-references-appendix|References Tail and Appendix]].
> Tooling cites Understand [36][37], Sharma smells/Designite [38][39][40], LLM-for-code cites Shi et al. 2023 [41], Shirafuji et al. 2023 [42], Svyatkovskiy et al. 2020 [44], Wei et al. 2023 [49], plus LLaMA, Xu et al., Zamfirescu-Pereira et al., and Zheng et al. CodeGeeX [45][50]–[54]. See [[wiki/12-references-appendix|References Tail and Appendix]].

### Q13. Given the complementarity finding plus the validity limits, what refactoring workflow should a team adopt for LLM assistance?
> [!tip]- Answer
> Route systematic implementation smells and syntactic edits (long statements, magic numbers, renames, annotation changes) to StarCoder2 with one-shot prompting and multiple generations, while reserving modularization, encapsulation, and cross-class structural changes for developer review. See [[wiki/08-rq3-findings-preferences|RQ3 Findings: Distinct Preferences in Refactoring Types]].
> Require comprehensive unit testing and human inspection before merging because Pass@5 is only ~57% versus 100% for developers, hallucinations persist, and results are bounded to Java/Apache projects, one model version, and smell/metric/tool constructs. See [[wiki/10-rq4-results-validity|RQ4 Results Context and Validity Under Identical Conditions]].
