> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# RQ2: Which Code-Smell Types Do LLMs vs Developers Reduce Best?

**In one sentence:** StarCoder2 reduces 10 of 16 smell types — sweeping 7 of 8 implementation smells with large effect sizes — while developers win on complex, context-sensitive design smells around modularization and encapsulation.

## Key points

- StarCoder2 outperforms developers in reducing 10 of the 16 code-smell types, with the split mirroring Table 4 (LLM better on 10, developers better on 6).
- In the implementation category, StarCoder2 wins 7 of 8 types with large Cliff's delta effect sizes (δ from 0.5271 to 0.6310), losing only Missing Default (developer, δ 0.4488, Medium).
- StarCoder2 excels at syntactic, pattern-based smells — Long Statement (δ 0.5406), Long Parameter List (δ 0.5703), Long Identifier (δ 0.5669), Empty Catch Clause (δ 0.6018), Magic Number (δ 0.6310), Complex Conditional (δ 0.5355), Complex Method (δ 0.5271) — all Large.
- In the design category the split is 4–4: StarCoder2 wins Unutilized Abstraction (δ 0.5366), Unnecessary Abstraction (δ 0.5130), Broken Hierarchy (δ 0.5608), Cyclic-Dependent Modularization (δ 0.4815), all Large.
- Developers win 4 design smells — Broken Modularization (δ 0.6417, Large), Deficient Encapsulation (δ 0.5587, Large), Insufficient Modularization (δ 0.6768, Large), Multifaceted Abstraction (δ 0.4636, Medium) — plus Missing Default on the implementation side.
- The mechanism given is that StarCoder2 handles implementation issues where "structured, rule-based corrections can be applied," while developer-won smells (Missing Default, Insufficient Modularization, Multifaceted Abstraction, Deficient Encapsulation, Broken Modularization) "require a deeper understanding of the overall software architecture," class dependencies, and encapsulation.
- Each data point is the per-project reduction rate of a specific smell after refactoring by either StarCoder2 or developers, compared with a Mann-Whitney U-test and quantified with Cliff's delta (δ).

---

## Table 4: Better reduction per smell with Cliff's delta

| Code Smell Category | Code Smell | Better Reduction | Cliff's Delta (δ) | Interpretation |
|---|---|---|---|---|
| Design | Unutilized Abstraction | LLM | 0.5366 | Large |
| Design | Unnecessary Abstraction | LLM | 0.5130 | Large |
| Design | Broken Hierarchy | LLM | 0.5608 | Large |
| Design | Cyclic-Dependent Modularization | LLM | 0.4815 | Large |
| Design | Broken Modularization | Developer | 0.6417 | Large |
| Design | Deficient Encapsulation | Developer | 0.5587 | Large |
| Design | Multifaceted Abstraction | Developer | 0.4636 | Medium |
| Design | Insufficient Modularization | Developer | 0.6768 | Large |
| Implementation | Long Statement | LLM | 0.5406 | Large |
| Implementation | Magic Number | LLM | 0.6310 | Large |
| Implementation | Empty Catch Clause | LLM | 0.6018 | Large |
| Implementation | Complex Conditional | LLM | 0.5355 | Large |
| Implementation | Long Parameter List | LLM | 0.5703 | Large |
| Implementation | Long Identifier | LLM | 0.5669 | Large |
| Implementation | Complex Method | LLM | 0.5271 | Large |
| Implementation | Missing Default | Developer | 0.4488 | Medium |

**Covers:** Table 4 (per-smell winner, δ, interpretation)

## Findings (Section 3.2.3)

> "The LLM outperforms developers in reducing 10 of the 16 types of code smells."

> "StarCoder2 can reduce code smells in 7 out of 8 types of code smells in the implementation category with a significantly large effect size comparing the reduction of code smells."

- StarCoder2 excels at "syntactic and pattern-based smells, such as Long Statement, Long Parameter List, Long Identifier, Empty Catch Clause, and Magic Number, which follow more regular idiomatic, and repetitive patterns."
- "This finding suggests that StarCoder2 is particularly effective at addressing issues related to implementation, where structured, rule-based corrections can be applied."
- "Developers show a better performance in reducing complex and context-sensitive code smells, particularly those related to modularization."
- Developers outperform the LLM on "Missing Default, Insufficient Modularization, and Multifaceted Abstraction, which require a deeper understanding of the overall software architecture and implementation principles."
- "In the design category, StarCoder2 outperforms developers in 4 out of 8 design-related code smells (i.e., Unutilized Abstraction, Unnecessary Abstraction, Broken Hierarchy, and Cyclic-Dependent Modularization)."
- "The LLM's effectiveness in reducing design-related smells suggests that it can eliminate unnecessary complexity and optimize code structure when the issues are relatively straightforward."
- Developers beat StarCoder2 on "more intricate design problems like Deficient Encapsulation and Broken Modularization, which require deeper reasoning about class dependencies, encapsulation, and how components interact at a design level."

**Covers:** Section 3.2.3 Findings

## Summary of Results

> "Our findings suggest that while StarCoder2 performs better at handling implementation-level code smells and some straightforward design issues, such as Long Statement, Magic Number, Long Identifier, etc., developers are better at handling more complex, context-dependent code smells, particularly those related to modularization and encapsulation."

- Stated implication: "the potential value of leveraging the strengths of both LLMs and developers for comprehensive code smell reduction and to improve overall software quality."

**Covers:** Summary of Results box

## Trailing transition: RQ3 setup present in chunk (3.3.1–3.3.2)

- RQ3 motivation (3.3.1): refactoring types are "specific categories of code modifications aimed at improving the structure, readability, and maintainability of software without altering its external behavior" (e.g., renaming variables, extracting methods, reorganizing classes); the question asks whether StarCoder2 or developers focus on different refactoring types.
- Approach start (3.3.2): collect refactorings from both sides; use "RMiner 3.0" to extract refactorings (up to 102 types, "precision of 99.8% and a recall of 98.1%"); compare frequency distributions, compute "code smell reduction rate" per refactoring type, and compare changes in complexity, cohesion, coupling, and modularity.
- Significance: "Mann-Whitney U-test" per data point (reduction in a specific smell per refactoring type, plus quality-metric improvements); if p-value < 0.05 the two sides "significantly target different areas of the code"; effect size via "Cliff's delta (δ)."

**Covers:** Sections 3.3.1–3.3.2 (RQ3 motivation and approach start, as trailed in chunk)

**Covers:** Table 4 + Section 3.2.3 Findings + Summary of Results + RQ3 setup trail (Sections 3.3.1–3.3.2)
