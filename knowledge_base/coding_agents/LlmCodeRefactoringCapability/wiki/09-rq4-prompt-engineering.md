# 09-rq4-prompt-engineering

**Covers:** RQ4: prompt-engineering setups (one-shot, chain-of-thought)

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# RQ4: Prompt Engineering — One-shot and Chain-of-Thought

**In one sentence:** One-shot prompting (34.51% test pass, 42.97% smell reduction) and chain-of-thought prompting (32.22%, 42.34%) both reach Scott-Knott Rank 1 and significantly outperform zero-shot prompting (28.36%, 39.45%, Rank 2) for StarCoder2 refactoring.

## Key points
- One-shot prompting achieves the highest unit test pass rate (34.51%) and code smell reduction rate (42.97%), both Scott-Knott Rank 1.
- Chain-of-thought prompting is close behind at 32.22% test pass and 42.34% smell reduction, also Scott-Knott Rank 1.
- Zero-shot prompting is lowest at 28.36% test pass and 39.45% smell reduction (Scott-Knott Rank 2), showing limited autonomous refactoring quality under vague instructions.
- One-shot prompting is strongest on complexity metrics AvgCyclomatic, Cyclomatic, MaxCyclomatic (all Rank 1) and on CountClassCoupledModified (Rank 1, 20.1%).
- Chain-of-thought prompting improves CountClassCoupled (23.4%, Rank 1) and CountDeclClassVariable (14.0%, Rank 1), with average metric improvement 19.99% (Rank 1) vs 20.15% (one-shot, Rank 1) vs 19.32% (zero-shot, Rank 2).
- Chain-of-thought prompting adds seven new refactoring types never seen with zero-shot: Extract Method, Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, and Parameterize Variable.
- Evaluation uses the Scott-Knott hierarchical clustering test across zero-shot, one-shot, and chain-of-thought distributions per project, on smell reduction rate and per-metric improvement.

---

## Prompt designs (Fig. 7 and Fig. 8)

**Covers:** Fig. 7 chain-of-thought prompt; Fig. 8 one-shot prompt

- Chain-of-thought prompt (Fig. 7) instructs StarCoder2 as "a powerful model specialized in refactoring Java code," defines refactoring as "improving the internal structure, readability, and maintainability of a software codebase without altering its external behavior or functionality," requires outputting a refactored version plus explaining "the steps you took to refactor the code and why you selected the refactoring type/types you did," and supplies "# Suggested refactoring types: {refactorings developers performed on this commit with definitions}" followed by "# unrefactored code snippet(java): {code_segment_before_refactoring}" and "# refactored version of the same code snippet:".
- One-shot prompt (Fig. 8) uses the same "You are a powerful model specialized in refactoring Java code" instruction and definition, then gives a concrete example pair "# unrefactored code snippet(java): {code_segment_before_refactoring}" / "# refactored version of the same code snippet: {developer_code_after_refactoring}" before the target "# unrefactored code snippet(java): {code_segment_before_refactoring}" / "# refactored version of the same code snippet:".

## Evaluation method

**Covers:** Section 3.4.2 setup — 2 prompt categories, Scott-Knott test

- For each commit, refactorings are generated using the 2 categories of prompts and compared on code quality metric improvement and code smell reduction, with attention to whether StarCoder2 begins refactorings it previously did not perform.
- The Scott-Knott test is "a hierarchical clustering method that partitions distributions into statistically distinct groups, helping to identify whether the differences between groups are meaningful"; samples are per-project quality improvements (smell reduction rate and percentage improvement in code metrics) under each prompt condition.

## Results: pass rate and smell reduction (Table 7)

**Covers:** Section 3.4.3 findings, Table 7

| Prompting Method | Unit Test Pass Rate (%) | SRR (%) | Scott-Knott Rank (SRR) |
|---|---|---|---|
| Zero-shot | 28.36% | 39.45% | 2 |
| Chain-of-thought | 32.22% | 42.34% | 1 |
| One-shot | 34.51% | 42.97% | 1 |

- Verbatim finding: "Applying one-shot prompting and chain-of-thought have more significant influences on code smell reduction than applying zero-shot prompting."

## Results: per-metric improvement (Table 8)

**Covers:** Section 3.4.3 findings, Table 8

| Metric | Zero-shot | Rank (Zero-shot) | Chain-of-thought | Rank (CoT) | One-shot | Rank (One-shot) |
|---|---|---|---|---|---|---|
| CountClassCoupled | 21.4 | 2 | 23.4 | 1 | 22.7 | 1 |
| CountClassCoupledModified | 18.3 | 3 | 19.2 | 2 | 20.1 | 1 |
| CountClassDerived | 17.9 | 2 | 18.1 | 2 | 18.3 | 2 |
| CountDeclClassVariable | 12.5 | 2 | 14.0 | 1 | 13.8 | 1 |
| CountDeclInstanceVariable | 19.7 | 2 | 20.2 | 2 | 19.8 | 2 |
| PercentLackOfCohesion | 22.8 | 2 | 23.5 | 1 | 23.1 | 2 |
| PercentLackOfCohesionModified | 23.9 | 2 | 24.1 | 2 | 24.2 | 2 |
| AvgCyclomatic | 17.4 | 2 | 18.0 | 1 | 18.4 | 1 |
| Cyclomatic | 16.5 | 2 | 17.0 | 1 | 17.3 | 1 |
| MaxCyclomatic | 15.8 | 2 | 16.3 | 1 | 16.6 | 1 |
| SumCyclomatic | 18.6 | 2 | 19.1 | 1 | 19.3 | 1 |
| Average | 19.32 | 2 | 19.99 | 1 | 20.15 | 1 |

- One-shot: highest on AvgCyclomatic, Cyclomatic, MaxCyclomatic (all Rank 1) and CountClassCoupledModified (Rank 1), "contributing to better modularity."
- Chain-of-thought: Rank 1 on CountClassCoupled and CountDeclClassVariable "with statistically significant differences"; "increases the variety of refactoring types performed by the LLM, adding seven new refactoring types not observed with zero-shot prompting: Extract Method, Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, and Parameterize Variable" by "providing specific instructions and definitions."
- Zero-shot: lowest overall; "StarCoder2's ability to autonomously generate high-quality refactorings is limited when given vague or minimal instructions."

## Summary of results (verbatim)

**Covers:** Section 3.4.3 closing summary

- "Our findings highlight the importance of prompt design in leveraging the full potential of LLMs for code refactoring tasks. Incorporating examples (i.e., one-shot prompt) or providing more explicit instructions (i.e., chain-of-thought prompt) significantly improves both the functional correctness and overall quality of the refactorings generated by StarCoder2."
- "One-shot prompting consistently yields the best performance across various metrics, including code complexity and modularity, by providing a concrete example of refactoring. Chain-of-thought prompting follows closely, especially in terms of expanding the types of refactorings performed and showing improvements in coupling and class variables. Both methods significantly outperform the zero-shot baseline, reinforcing the importance of prompt design in optimizing the performance of LLMs for refactoring tasks."
