[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The Impact of AI Tool on Engineering at ANZ Bank
**In one sentence:** ANZ Bank ran a six-week controlled experiment with GitHub Copilot (5000-engineer org, ~1000 later adopters) to measure productivity, code quality, security, and engineer sentiment before large-scale adoption.
## Key points
- ANZ Bank employs 5000+ engineers across the full software development life cycle; the study evaluates GitHub Copilot first in a controlled experiment, then via early large-scale adoption data from ~1000 engineers.
- The experiment ran six weeks (mid-June to end-July 2023): two weeks of preparation plus four weeks of active testing, covering sentiment, productivity, code quality, and security.
- Phase 1 had participants use Copilot for proposed use-cases with regular surveys; phase 2 split them into Control (Copilot disabled) and Copilot (Copilot enabled) groups solving the same Python challenges.
- Headline result reported in the chunk: notable boost in productivity and code quality with Copilot, inconclusive impact on code security, overall positive participant sentiment.
- The experiment is an Architecture & Engineering initiative with two objectives: a methodical guide for taking AI pair-programming from experiment to large scale, and statistical measures of productivity, quality, and security.
- Claimed contributions: systematic examination of productivity (code quality, development time, problem complexity), analysis of engineer sentiment, and initial post-production validation from ~1000 engineers.
- Design constraints: Visual Studio Code as the single IDE (to control Copilot metrics breadth), Python as the only language for weeks 3–4 hypothesis testing, algorithmic questions instead of app-development scenarios, and self-reported time rather than active monitoring.
## Abstract
**Covers:** Title, authors, Abstract, Keywords

Paper: "THE IMPACT OF AI TOOL ON ENGINEERING AT ANZ BANK: AN EMPIRICAL STUDY ON GITHUB COPILOT WITHIN CORPORATE ENVIRONMENT" by Sayan Chatterjee, Ching Louis Liu, Gareth Rowland, Tim Hogarth (Australia and New Zealand Banking Group Limited, Melbourne).

> "This study explores the integration of AI tools in software engineering practices within a large organization. We focus on ANZ Bank, which employs over 5000 engineers covering all aspects of the software development life cycle."

Experiment summary: six-week experiment (two weeks preparation, four weeks active testing) evaluating participant sentiment and impact on productivity, code quality, and security; phase 1 proposed use-cases with surveys, phase 2 Control vs Copilot groups on the same Python challenges.

Keywords: Copilot, GitHub, ANZ Bank, Code Suggestions, Code Debugging, Experiment, Software Engineering, AI.

## Introduction
**Covers:** Section 1. INTRODUCTION

- Generative AI framed as "the next wave of productivity through operational efficiency and quicker-informed decisions"; developers use it "as a pair-programmer to increase the output of high-quality code," freeing capacity for innovation.
- Counterweight: AI raises "inherent risks, uncertainties and unintentional consequences regarding intellectual property, data security and privacy," so quantitative and qualitative benefits must be measured before large-scale adoption.
- Tool choice: despite alternatives such as Code Whisperer, GitHub Copilot chosen as a pioneer with robust features.
- Copilot capabilities per chunk: generates "syntactically correct and contextually relevant code snippets" across Java, Python, C#, C++, and others, plus comments explaining purpose/functionality given IDE context.
- IDE compatibility: Visual Studio Code, Neovim, JetBrains suite, GitHub Codespaces; technical preview on VS Code 29 June 2021, subscription service 21 June 2022 for individuals and corporates.
- Architecture: predicated on Generative Pre-trained Transformer (GPT) technology, refined on publicly available GitHub code.
- Key aims (verbatim):
  - "Do the developers at ANZ feel positive and empowered by having access to Copilot?"
  - "How much does access to this tool make employees work faster, if at all?"
  - "Does this tool make developers at ANZ output better?"
  - "Is the code suggested by Copilot secure?"
- Additional questions: "How often are Copilot's suggestions considered useful and accepted?" and "Does the code suggested by Copilot follow best practices?"

## Related work
**Covers:** Section 2. RELATED WORK

| Study | Setup | Finding reported in chunk |
|---|---|---|
| Microsoft 2022 | 95 engineers, HTTP server in JavaScript, treatment (Copilot) vs control | Treatment 55.8% faster; less-experienced, older, or frequent programmers benefited most |
| Yetiştiren et al. (Copilot vs CodeWhisperer vs ChatGPT) | Validity, correctness, security, reliability, maintainability | Copilot 18% improvement in newer versions; Copilot beat CodeWhisperer in engineering context; ChatGPT more general-purpose |
| 2022 sentiment study | Engineer attitudes to Copilot | Positive sentiment on productivity, echoed at ANZ |
| Imai (Copilot vs human pair) | Lines produced vs lines removed | Copilot generated most lines but also most deleted; lines of code ≠ quality |
| Dakhel et al. | (i) fundamental algorithms (sorting, data structures), (ii) Copilot vs human solutions | Copilot solved most fundamentals but some solutions buggy/non-reproducible; humans more often correct, but Copilot errors typically less complex and easier to fix; utility depends on expertise — valuable for experienced developers, risky for novices who may not catch bad suggestions |

Chunk notes ANZ alignment with Microsoft (different tasks, Python language) and with timely Copilot suggestions regardless of task complexity vs humans slowing on harder tasks.

## Study design (part 1)
**Covers:** Section 3. STUDY DESIGN up to A/B Testing header

- Timeline: six weeks mid-June 2023 to end-July 2023; two weeks preparation, four weeks execution.
- Scope: sentiment toward Copilot's VS Code extension plus impact on productivity, code quality, and code security.
- Pre-experiment: IP, data security, and privacy risks assessed with ANZ legal and security teams, yielding participant guidelines (Playbook, required reading/agreement).
- Constraints: VS Code only; Python only for weeks 3–4 statistical testing (widespread use, novice-accessible); algorithmic questions (limited participant time); no active monitoring — self-reported time and feedback.
