> [[index|Wiki]] | [[summary|Summary]]
# An Empirical Study on the Code Refactoring Capability of Large Language Models — Digest

## 1. [[wiki/01-empirical-study-overview|Empirical Study Overview]]
**In one sentence:** This study empirically compares StarCoder2-generated refactorings against developer refactorings on 30 Java projects to measure code-quality improvement and test whether prompting strategies can improve LLM refactoring.
## Key points
- StarCoder2 reduces code smells by 20.1% more than developers on automatically generated refactorings across 30 open-source Java projects.
- StarCoder2 excels at Long Statement, Magic Number, Empty Catch Clause, and Long Identifier smells, while developers perform better on Broken Modularization, Deficient Encapsulation, and Multifaceted Abstraction.
- StarCoder2 outperforms developers on refactoring types that are more systematic and repetitive, while developers surpass it on refactorings requiring deeper code context and architecture understanding.
- One-shot prompting improves the unit test pass rate by 6.15% over the zero-shot prompt and reduces code smells at a 3.52% higher rate.
- Generating five refactorings per input achieves a 28.8% higher unit test pass rate than generating one per input, and combined with one-shot prompting gives the best performance.
- The study uses StarCoder2-15B-instruct (46.3% pass@1 on HumanEval), chosen because it is trained on the public Stack v2 dataset so projects not in that dataset can be selected to mitigate data leakage.
- The corpus comprises 30 open-source Java projects not included in Stack v2, yielding 5,194 developer refactoring commits used as the before/after comparison baseline.

## 2. [[wiki/02-rq1-llm-vs-developers|RQ1: Can LLMs Outperform Developers in Code Refactoring?]]
**In one sentence:** RQ1 asks whether StarCoder2 can reliably automate code refactoring by comparing its refactoring distribution, code-smell reduction (44.36% vs 24.27% for developers), and code-metric improvements against developers, using a controlled setup of 30 leak-free Java projects with pure-refactoring commits.
## Key points
- RQ1 compares StarCoder2-generated refactorings against developer refactorings on the same files (pre-refactoring state), measuring refactoring-operation distribution, code-smell reduction, and code-metric quality improvement.
- StarCoder2 reduces code smells by 44.36% versus 24.27% for developers, and the chunk states it "often surpassing developers" on code-metric quality improvements.
- The study starts from the 20-MAD dataset (765 Apache projects), filters to 195 Java projects, removes 135 projects overlapping StarCoder2 training data to avoid leakage, and ends with a final 30 Java projects balanced by refactoring-commit count (median threshold 129).
- Only pure-refactoring commits are used: a commit is kept when its Refactoring Ratio (Refactoring Code Churn / Total Code Churn × 100%) equals 100%, using 59 refactoring types detected by RMiner (reported precision 99.7%, recall 94.2%).
- Code smells are extracted before and after each refactoring commit with DesigniteJava 2.5.2, which detects 46 smell types (7 architecture, 18 design, 9 implementation, 4 testability, 8 test smells).
- The chunk also previews RQ2–RQ4 claims: StarCoder2 wins on systematic/repetitive smells and within-class refactorings, developers win on complex context-dependent smells and multi-class refactorings, and one-shot prompting (34.51% test pass, 42.97% SRR) beats zero-shot and chain-of-thought.

## 3. [[wiki/03-experiment-setup-metrics|Code Metrics Computation (Experiment Setup)]]
**In one sentence:** The study evaluates refactoring quality with code metrics for complexity, cohesion, coupling, and modularity, extracted with the Understand static-analysis tool and described in Table 1.
## Key points
- Code metrics are used as proxies for quality attributes such as maintainability and complexity [31].
- The collected metrics cover four quality attributes: complexity, cohesion, coupling, and modularity.
- Modularity metrics assess how far the system is divided into independent components, aiding maintenance and testing.
- Coupling metrics measure inter-class interdependence, where lower coupling is preferred for modularity and flexibility.
- Cohesion metrics measure how closely related a class's responsibilities are, with higher cohesion linked to clarity and design quality [35].
- Metrics are extracted with the Understand tool [36], a static code analysis tool.
- Table 1 lists each metric with its description, quality attribute, and rationale for inclusion (e.g., Avg/Max/Sum Cyclomatic for complexity, Percent Lack of Cohesion variants for cohesion).

## 4. [[wiki/04-refactoring-generation-method|Refactoring Generation: We Use the Code]]
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

## 5. [[wiki/05-rq1-findings-smell-reduction|StarCoder2 has better performance in code]]
**In one sentence:** On refactorings that pass unit tests, StarCoder2 reduces code smells by 44.36% versus 24.27% for developers (20.1 points higher, U-test p=0.003) and achieves a higher average code-metric improvement (19.32% vs 17.46%), leading on cohesion and cyclomatic complexity while developers lead on class coupling.
## Key points
- Initial unrefactored code has 17,429 smells; developer refactoring leaves 13,199 smells (24.27% reduction), while StarCoder2's test-passing subset goes from 12,213 to 6,795 smells (44.36% reduction), 20.1 points higher than developers.
- The U-test for code smell reduction gives p=0.003, and the chunk rejects null hypothesis H0, concluding StarCoder2 performs significantly better in smell reduction and metric improvements.
- From Pass@1 to Pass@5 the smell reduction rate rises 4.91%, driven by Rebellious Hierarchy Smell (+5.18%), Long Method (+8.76%) and Long Statement (+6.32%), with all other smells consistent; the best pass@5 generation is used for the remaining RQs.
- Across Table 3 metrics StarCoder2 averages 19.32% improvement (median 18.2%) versus 17.46% for developers (median 16.9%), with a Pass@5 unit-test pass rate of 57.15% versus 100% for developers.
- StarCoder2 leads on cohesion/modularity: CountDeclInstanceVariable 19.7% vs 17.0%, PercentLackOfCohesion 22.8% vs 20.4%, and PercentLackOfCohesionModified 23.9% vs 21.5% (Cliff's Delta 0.42, Medium).
- StarCoder2 leads on complexity: AvgCyclomatic 17.4% vs 14.6% (Cliff's Delta 0.45, Medium) and SumCyclomatic 18.6% vs 15.9% (Cliff's Delta 0.47, Medium), plus Cyclomatic 16.5% vs 13.5% and MaxCyclomatic 15.8% vs 13.3%.
- Developers lead on coupling-related metrics: CountClassCoupled 24.1% vs 21.4% for StarCoder2, and CountDeclClassVariable 14.9% vs 12.5%, suggesting an edge where deep understanding of class dependencies and variable declarations is required.

## 6. [[wiki/06-rq2-code-smell-types|RQ2: Which Code-Smell Types Do LLMs vs Developers Reduce Best?]]
**In one sentence:** StarCoder2 reduces 10 of 16 smell types — sweeping 7 of 8 implementation smells with large effect sizes — while developers win on complex, context-sensitive design smells around modularization and encapsulation.
## Key points
- StarCoder2 outperforms developers in reducing 10 of the 16 code-smell types, with the split mirroring Table 4 (LLM better on 10, developers better on 6).
- In the implementation category, StarCoder2 wins 7 of 8 types with large Cliff's delta effect sizes (δ from 0.5271 to 0.6310), losing only Missing Default (developer, δ 0.4488, Medium).
- StarCoder2 excels at syntactic, pattern-based smells — Long Statement (δ 0.5406), Long Parameter List (δ 0.5703), Long Identifier (δ 0.5669), Empty Catch Clause (δ 0.6018), Magic Number (δ 0.6310), Complex Conditional (δ 0.5355), Complex Method (δ 0.5271) — all Large.
- In the design category the split is 4–4: StarCoder2 wins Unutilized Abstraction (δ 0.5366), Unnecessary Abstraction (δ 0.5130), Broken Hierarchy (δ 0.5608), Cyclic-Dependent Modularization (δ 0.4815), all Large.
- Developers win 4 design smells — Broken Modularization (δ 0.6417, Large), Deficient Encapsulation (δ 0.5587, Large), Insufficient Modularization (δ 0.6768, Large), Multifaceted Abstraction (δ 0.4636, Medium) — plus Missing Default on the implementation side.
- The mechanism given is that StarCoder2 handles implementation issues where "structured, rule-based corrections can be applied," while developer-won smells (Missing Default, Insufficient Modularization, Multifaceted Abstraction, Deficient Encapsulation, Broken Modularization) "require a deeper understanding of the overall software architecture," class dependencies, and encapsulation.
- Each data point is the per-project reduction rate of a specific smell after refactoring by either StarCoder2 or developers, compared with a Mann-Whitney U-test and quantified with Cliff's delta (δ).

## 7. [[wiki/07-rq3-refactoring-types|RQ3: Comparison of Refactoring Types (LLM vs Developers)]]
**In one sentence:** This chunk contains only a garbled rendering of Figure 6 ("Distribution of Frequencies of all Refactoring Types Used by StarCoder2 Across 30 Projects") with axis/legend/type labels but no recoverable numeric values, so no LLM-vs-developer comparison claim can be extracted from it.
## Key points
- The chunk body is a garbled figure rendering, not prose: it carries no complete findings, numbers, or mechanisms beyond labels.
- Its title line is "Comparison of Refactoring Types (LLM vs Developers) for LLM-Performed Refactorings."
- Its only verbatim caption is "Fig. 6. Distribution of Frequencies of all Refactoring Types Used by StarCoder2 Across 30 Projects."
- The y-axis is labeled "Refactoring Count Across Projects" with ticks 0–700; the x-axis is labeled "Refactoring Types."
- The legend contains two series: LLM and Developer.
- Refactoring-type labels visible in the garbled text include Rename Parameter, Rename Package, Rename Variable, Rename Class, Move Package, Move And Rename Method, Move And Rename Class, Remove Class Modifier, Remove Method Annotation, Move Method, Remove Class Annotation, Move Class, Remove Attribute Modifier, Add Class Modifier, Change Return Type, Encapsulate Attribute, Move Attribute, Remove Thrown Exception Type, Add Method Annotation, Change Variable Type, Change Type Declaration Kind, Add Class Annotation, Modify Class Annotation, Change Method Access Modifier, Add Attribute Modifier, Change Class Access Modifier, Change Attribute Type, and Change Attribute Access Modifier.
- No per-type counts, rankings, or LLM-vs-developer differences are recoverable from this chunk text.

## 8. [[wiki/08-rq3-findings-preferences|RQ3 Findings: Distinct Preferences in Refactoring Types]]
**In one sentence:** StarCoder2 favors frequent, syntactic rule-based refactorings (e.g., Rename Method, Extract Method, annotation changes) while developers favor dependency-heavy, structural refactorings (e.g., Move Method, Change Attribute Access Modifier), with complementary strengths in smell reduction and metric improvement.
## Key points
- StarCoder2 performs Rename Method and Extract Method at higher frequency than developers, refactorings detectable by following syntactic rules, while developers more frequently perform Move Method and Change Attribute Access Modifier, which require dependency checks and propagate larger code changes.
- On code-smell reduction (p-value < 0.05, all large Cliff's Delta), StarCoder2 wins 9 of 11 significant refactoring types, including Remove Method Annotation (δ = 0.9619), Modify Class Annotation (δ = 0.9589), Move And Rename Method (δ = 0.9394), Add Method Annotation (δ = 0.9117), and Rename Class (δ = 0.5871).
- Developers win only 2 of the 11 significant smell-reduction types, both attribute-level: Move Attribute (δ = 0.7832) and Change Attribute Type (δ = 0.7796), which require deeper context and data-dependency understanding.
- On code-metric improvement, StarCoder2 wins 3 of 5 significant types — Add Class Annotation (δ = 0.8517), Change Return Type (δ = 0.8032), Rename Class (δ = 0.6123) — while developers win Encapsulate Attribute (δ = 0.6798) and Change Attribute Access Modifier (δ = 0.7215).
- Access-control refactorings (Change Method Access Modifier, Encapsulate Attribute) are unique to StarCoder2, applied in a rule-based manner to visibility/encapsulation; developers instead handle Extract Method, Inline Variable, Extract Superclass, and Pull Up Method, requiring class-hierarchy and modularity reasoning.
- Class-level work diverges: StarCoder2 applies simpler Change Type Declaration Kind and Add Class Modifier, developers apply Extract Superclass and Pull Up Method; package/file movement diverges as StarCoder2 doing Move Package versus developers doing granular Move Source Folder.
- The chunk's stated conclusion is complementarity: "StarCoder2 excels in automated, syntactic refactoring types, while developers focus on more complex, structural changes," so a combined LLM-plus-developer approach "could potentially offer the most comprehensive strategy for code refactoring."

## 9. [[wiki/09-rq4-prompt-engineering|RQ4: Prompt Engineering — One-shot and Chain-of-Thought]]
**In one sentence:** One-shot prompting (34.51% test pass, 42.97% smell reduction) and chain-of-thought prompting (32.22%, 42.34%) both reach Scott-Knott Rank 1 and significantly outperform zero-shot prompting (28.36%, 39.45%, Rank 2) for StarCoder2 refactoring.
## Key points
- One-shot prompting achieves the highest unit test pass rate (34.51%) and code smell reduction rate (42.97%), both Scott-Knott Rank 1.
- Chain-of-thought prompting is close behind at 32.22% test pass and 42.34% smell reduction, also Scott-Knott Rank 1.
- Zero-shot prompting is lowest at 28.36% test pass and 39.45% smell reduction (Scott-Knott Rank 2), showing limited autonomous refactoring quality under vague instructions.
- One-shot prompting is strongest on complexity metrics AvgCyclomatic, Cyclomatic, MaxCyclomatic (all Rank 1) and on CountClassCoupledModified (Rank 1, 20.1%).
- Chain-of-thought prompting improves CountClassCoupled (23.4%, Rank 1) and CountDeclClassVariable (14.0%, Rank 1), with average metric improvement 19.99% (Rank 1) vs 20.15% (one-shot, Rank 1) vs 19.32% (zero-shot, Rank 2).
- Chain-of-thought prompting adds seven new refactoring types never seen with zero-shot: Extract Method, Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, and Parameterize Variable.
- Evaluation uses the Scott-Knott hierarchical clustering test across zero-shot, one-shot, and chain-of-thought distributions per project, on smell reduction rate and per-metric improvement.

## 10. [[wiki/10-rq4-results-validity|RQ4 Results Context and Validity Under Identical Conditions]]
**In one sentence:** Experiments run under identical server, hardware, and software setups still face internal, external, and construct validity limits, while related work and the conclusion position StarCoder2 as stronger than developers on implementation smells but weaker on complex design smells, with one-shot prompting improving quality.
## Key points
- Experiments used the same server with consistent hardware and software setups, so rerunning on a different server with comparable resources "should not significantly affect the results."
- StarCoder2 hallucination remains an internal-validity risk because apparently correct output may be logically or syntactically invalid, skewing unit-test pass rates and refactoring-effectiveness measures despite verification by tests and inspection.
- Random single-commit sampling limits internal validity: different project settings or commit subsets could change outcomes, and multi-commit refactorings are missed, potentially underestimating complexity or scope.
- Training-data isolation is incomplete: projects were chosen outside the StarCoder2 training dataset, but similar code patterns or practices could still be present and advantage the model.
- External validity is bounded to a limited set of open-source Java projects from the Apache dataset and to StarCoder2-15B-Instruct-v0.1, so results may not transfer to other languages, domains, LLMs, or versions, though the replication package is public and the evaluation is designed to be adaptable.
- Construct validity rests on code-smell reduction, code-quality-metric improvement, and unit-test pass rates, which may miss readability and performance, and on RMiner3.0, DesigniteJava, and Understand, where different tools "may get different results."
- Conclusion numbers: StarCoder2 achieves 43.36% implementation code-smell reduction versus 24.27% for developers, excels at systematic refactorings while developers handle context-dependent design smells better, and benefits significantly from one-shot prompting.

## 11. [[wiki/11-threats-related-work|References [1]–[33] — First Bibliography Segment]]
**In one sentence:** This chunk contains only the bibliography entries [1] through [33] (truncated mid-entry at [33]), listing cited works on LLMs, refactoring, code metrics, and statistics with full author, year, venue, and identifier details.
## Key points
- Entry [1] is Alshahwan et al. 2024, "Assured Offline LLM-Based Software Engineering," InteNSE '24 (Lisbon), pp. 7–12, DOI 10.1145/3643661.3643953.
- Entries [4], [9], [20], [22], [23], and [25] cite LLM foundations: Brown et al. 2020 (GPT-3 few-shot learners, NeurIPS Vol. 33), Chowdhery et al. 2022 (PaLM, arXiv:2204.02311), Kojima et al. 2022 (zero-shot reasoners, NeurIPS Vol. 35), Li et al. 2023 (StarCoder, arXiv:2305.06161), Li et al. 2022 (AlphaCode, Science 378(6624)), and Lozhkov et al. 2024 (StarCoder 2, arXiv:2402.19173).
- Entries [6], [14], [15], [27], [30], and [32] cite refactoring literature: Fowler 2018 and Fowler et al. 1999 (Refactoring: Improving the Design of Existing Code), Opdyke and Johnson 1992 (Refactoring Object-Oriented Frameworks), Mens and Tourwé 2004 (refactoring survey, IEEE TSE 30(2)), Cedrim et al. 2017 (refactoring impact on smells, ESEC/FSE 2017), and Noei et al. 2023 (refactoring rhythms, IEEE TSE).
- Entries [7], [8], [12], [13], and [21] cite LLM-for-SE studies: Chang et al. 2024 (LLM evaluation survey, ACM TIST 15(3)), Choi et al. 2024 (iterative refactoring with LLMs, SSBSE LNCS Vol. 14767), Fan et al. 2023 (LLMs for SE survey, ICSE-FoSE), Fan et al. 2023 (automated repair from LLMs, ICSE '23), and Li et al. 2023 (structured chain-of-thought prompting for code generation).
- Entries [11], [18], [25], and [26] cite statistical methods: Jelihovschi et al. 2014 (ScottKnott R package), Hazra 2017 (confidence intervals), McKnight and Najab 2010 (Mann-Whitney U Test), and Meissel and Yao 2024 (Cliff's Delta).
- Entry [2] is Balog et al. 2016, "DeepCoder: Learning to Write Programs," CoRR abs/1611.01989; entry [16] is Fraser and Arcuri 2011 on EvoSuite test generation (SIGSOFT/FSE 2011, pp. 416–419).
- The chunk carries page footer markers "22" and "23" and a running head "An Empirical Study on the Code Refactoring Capability of Large Language Models / Trovato et al., Conference acronym 'XX, June 03–05, 2018, Woodstock, NY," and entry [33] (OpenAI et al.) is truncated mid-author-list at "Mark Chen, Ben Chess, Chester."
- No findings, threats to validity, related-work discussion, or conclusions appear in this chunk body despite the plan.md label; all claims above come solely from the reference text.

## 12. [[wiki/12-references-appendix|References Tail and Appendix]]
**In one sentence:** This chunk contains only the tail end of the bibliography (continuation of the GPT-4 Technical Report author list and references [34]–[54]) plus page footers, with no empirical findings or discussion.
## Key points
- The chunk opens with the continuation of a massive author list ending in "...and Barret Zoph. 2024. GPT-4 Technical Report. arXiv:2303.08774 [cs.CL]" with no new claim beyond the citation.
- Reference [34] cites Palomba et al. 2018 on diffuseness and maintainability impact of code smells, published in ICSE '18, page 482, DOI 10.1145/3180155.3182532.
- References [35], [43], [46], and [47] cite mining/refactoring-detection works: Pantiuchina et al. 2020 (30 pages, DOI 10.1145/3408302), Silva et al. 2016 FSE (pages 858–870), RefactoringMiner 2.0 (TSE vol. 48 no. 3, pages 930–950), and Tsantalis et al. 2018 ICSE (pages 483–494).
- References [36]–[40] cite static-analysis tooling sources: Scientific Toolworks Understand (2023), scitools metrics documentation PDF, Sharma code-smells page, Sharma 2024 MSR (pages 284–288), and Sharma et al. 2016 Designite workshop paper (pages 1–4).
- References [41], [42], [44], and [49] cite LLM-for-code works: Shi et al. 2023 ISSTA (pages 39–51), Shirafuji et al. 2023 APSEC (pages 151–160, DOI 10.1109/APSEC60848.2023.00025), Svyatkovskiy et al. 2020 Intellicode Compose (pages 1433–1443), and Wei et al. 2023 ESEC/FSE (pages 172–184).
- References [45], [50]–[53] cite foundation models and evaluation: Touvron et al. 2023 LLaMA (arXiv:2302.13971 [cs.CL]), Xu et al. 2022 machine-programming symposium (pages 1–10, DOI 10.1145/3520312.3534862), Xu et al. 2022 TOSEM (vol. 31 no. 2, 47 pages), and Zamfirescu-Pereira et al. 2023 CHI (Article 437, 21 pages).
- Reference [54] cites Zheng et al. 2023 CodeGeeX, KDD '23, pages 5673–5684, DOI 10.1145/3580305.3599790, and the chunk ends with page number "25" and no replication-package content beyond the reference list itself.

## The argument in five moves
1. The study sets up a leakage-controlled head-to-head: StarCoder2-15B-instruct refactors pre-refactoring code from 5,194 pure-refactoring commits across 30 Java projects outside Stack v2, judged by smell reduction, Understand metrics, and Pass@1/3/5 unit tests against developer refactorings.
2. Headline result: StarCoder2's test-passing refactorings cut smells far more aggressively (44.36% vs 24.27%, p=0.003) and improve average code metrics more (19.32% vs 17.46%), though developers keep a 100% test-pass record versus 57.15% Pass@5 and lead on coupling metrics.
3. The advantage splits by kind: StarCoder2 sweeps systematic, rule-based implementation smells and syntactic refactoring types (renames, annotation changes, extractions), while developers win context-heavy design smells (modularization, encapsulation) and structural, dependency-propagating refactorings (Move Attribute, Change Attribute Type, Encapsulate Attribute).
4. Prompting matters: one-shot (34.51% pass, 42.97% SRR) and chain-of-thought (32.22%, 42.34%) both reach Rank 1 over zero-shot (28.36%, 39.45%), with one-shot strongest on complexity and chain-of-thought widening the refactoring repertoire by seven new types.
5. The close is complementarity under caveats: identical-server runs still face hallucination, sampling, training-overlap, Java/Apache-only, single-model, and metric/tool-construct limits, so the paper positions LLM-plus-developer collaboration — not replacement — as the comprehensive refactoring strategy.
