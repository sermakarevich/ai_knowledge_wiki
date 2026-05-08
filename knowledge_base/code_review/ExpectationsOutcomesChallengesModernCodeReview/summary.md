# Expectations, Outcomes, and Challenges of Modern Code Review

**Paper:** [Expectations, Outcomes, and Challenges of Modern Code Review (Bacchelli & Bird, ICSE 2013)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf)

## Human Readable TL;DR

When programmers look over each other's work before it gets merged into a codebase, most people assume the main point is to catch bugs -- like a spell-checker hunting for errors. This study followed real teams at Microsoft and found that is not what actually happens: the most common outcome is suggestions for cleaner code style, not bug reports. Defect-related comments ranked only fourth out of nine categories despite "finding defects" being everyone's stated top reason for doing reviews. More surprisingly, the biggest challenge is not time or tooling -- it is that reviewers struggle to simply understand what the code does and why the change was made. Think of it like asking a colleague to proofread a memo written in jargon they do not know: they end up asking "what does this mean?" far more than "is this sentence wrong?"

## TL;DR

Bacchelli and Bird conducted a mixed-methods study at Microsoft -- observing 17 developers, interviewing them, manually classifying 570 review comments across 200 CodeFlow threads, and surveying 165 managers and 873 programmers -- to investigate motivations, actual outcomes, and challenges of Modern Code Review (MCR). While "finding defects" is the top-stated motivation (44% of programmers rank it first), defect-related comments comprise only 14% of actual review output, ranking fourth among nine comment categories. Code improvement comments dominate at 29%, followed by understanding-seeking at ~25%. The central challenge is code and change understanding: 91% of programmers report it takes longer to review unfamiliar files, and 82% say file-owner reviewers give substantially deeper feedback. Current review tools address only surface-level understanding needs, leaving a large gap between expectation and practice.

---

## Problem & Motivation

Prior research on code inspection (Fagan-style, 1970s--80s) established defect detection as the primary goal and metric. Modern Code Review -- informal, tool-based, asynchronous -- has become widespread at Microsoft, Google, Facebook, and in open source, but it is not clear whether the lessons from formal inspections carry over. The paper asks three questions: (1) What are the motivations and expectations for MCR, and do they differ between managers and developers? (2) What are the actual outcomes, and do they match expectations? (3) What are the main challenges experienced during MCR? Without answers, organizations risk misaligning review policies with real value and researchers risk building on false premises.

---

## Main Original Ideas

1. **Modern Code Review as a distinct practice.** The authors formally define MCR as review that is (1) informal, (2) tool-based, and (3) conducted regularly -- distinguishing it from Fagan-style inspections. This framing justifies studying MCR on its own terms rather than applying inspection-era findings wholesale.

2. **Six-category motivation taxonomy.** Through card sorting on 1,047 interview and observation units, then validation via surveys, they identify six main motivations: finding defects, code improvement, alternative solutions, knowledge transfer, team awareness and transparency, and shared code ownership. This extends prior work that focused almost entirely on defect detection.

3. **Nine-category empirical comment taxonomy.** By card-sorting 570 actual review comments from CodeFlow, they produce the first large-scale empirical classification of what reviewers actually write: code improvements, understanding, social communication, defects, external impact, testing, review tool, knowledge transfer, and miscellaneous. The distribution directly contradicts the defect-centric expectation.

4. **Understanding as the central challenge.** The paper identifies code and change understanding -- not scheduling, tool limitations, or interpersonal friction -- as the dominant challenge of MCR. Reviewers use an ad hoc range of strategies (reading descriptions, running code, sending emails, meeting in person 20%--40% of the time) because tools provide only basic support.

5. **File ownership as a proxy for review quality.** Reviewers who own the changed files produce comments that are substantially deeper, more conceptual, more actionable, and more likely to find subtle defects. This shows a structural dependency between prior knowledge and review outcome quality that current tool design ignores.

---

## Key Findings

### Comment category distribution (570 comments, 200 threads)

| Category | Count | Approx. % |
|---|---|---|
| **Code Improvements** | **165** | **29%** |
| Understanding | ~140 | ~25% |
| Social Communication | ~85 | ~15% |
| **Defects** | **78** | **14%** |
| External Impact | ~25 | ~4% |
| Testing | ~20 | ~4% |
| Review Tool | ~15 | ~3% |
| Knowledge Transfer | 12 | ~2% |
| Miscellaneous | ~30 | ~5% |

- Defects rank 4th despite being the top-stated motivation.
- Among defect comments: 65 on logical issues (e.g., wrong expression in an if clause), 6 on high-level issues, 5 on security, 3 on wrong exception handling -- mostly low-level "micro" defects.
- Among code improvement comments: 58 on better code practices, 55 on removing unnecessary/unused code, 52 on readability.
- Understanding comments (2nd most frequent) are clarification questions and doubts from reviewers trying to grasp the rationale for a change.

### Developer motivations -- top-3 rankings (873-programmer survey)

| Motivation | Ranked 1st | Ranked 2nd | Ranked 3rd |
|---|---|---|---|
| Finding Defects | 383 (44%) | 204 (23%) | 96 (11%) |
| Code Improvement | 337 (39%) | 208 (24%) | 135 (15%) |
| Alternative Solutions | 147 (17%) | 202 (23%) | 152 (17%) |
| Knowledge Transfer | 73 (8%) | 119 (14%) | 141 (16%) |
| Team Awareness | 75 (9%) | 108 (12%) | 149 (17%) |
| Share Code Ownership | 51 (6%) | 100 (11%) | ~90 (10%) |

- 44% of the 165 managers surveyed also rank "finding defects" as top motivation.
- "Alternative solutions" was mentioned by only 4 managers (2%) as a top motivation, despite being ranked 3rd by programmers overall.

### Understanding requirements vs. outcomes

- 798/873 (91%) of programmers confirm it takes longer to review files they are unfamiliar with.
- 716/873 (82%) report that file-owner reviewers give qualitatively different feedback -- deeper, more detailed, more insightful, and more conceptual vs. superficial (naming, style).
- "Finding defects" and "alternative solutions" require the highest level of code understanding among all six motivations (Figure 5 Likert survey).
- The gap in understanding requirements between "finding defects" and "code improvement" directly explains their reversed frequency in actual comments.
- Reviewers go in person to talk with authors 20%--40% of the time to achieve sufficient understanding -- a need no current review tool supports.

---

## Suggestions & Future Directions

1. **Automate low-level review tasks.** Code improvement and micro-defect comments (style, naming, dead code, simple logic errors) are increasingly addressable by static analysis and linters. Automating these frees human reviewers for deeper concerns. Google's FindBugs experiment is cited as an example; boundary condition checking tools have also shown value on real code.

2. **Build program comprehension support into review tools.** All current MCR tools provide only surface-level support (diff highlight, inline commenting, syntax highlighting). Tools should expose call graphs, change rationale, invariants, API documentation, and impact analysis within the review interface to address the dominant challenge the study uncovered.

3. **Study socio-technical effects of MCR directly.** Team awareness and knowledge transfer emerged as strong motivations but leave little trace in review comment data and are difficult to quantify. Future studies should be designed specifically to measure whether awareness and learning increase as a result of code review participation.

4. **Revise quality assurance policies.** Organizations should not rely on MCR as the primary mechanism for catching deep, subtle, or architectural defects -- the evidence shows this is not what MCR reliably delivers. MCR should be positioned as complementary to testing and design review, not a substitute.

5. **Investigate change description standards.** Developers consistently said richer, more precise change descriptions improved review speed and quality substantially. Future work should quantify the effect of description quality on review outcomes and study incentive structures for authors to provide better context.

6. **Replicate in OSS and smaller-organization contexts.** The study is based entirely on Microsoft teams using CodeFlow. OSS settings differ -- expertise gatekeeping may make learning less prominent as a motivation, and shared code ownership may already be assumed. Replication across contexts is needed to assess generalizability.

### Acknowledged limitations

- Single-company setting (Microsoft, 16 product teams); may not generalize to smaller organizations, OSS, or teams using different tools.
- Social motivations (awareness, knowledge transfer) leave little trace in review comments; surveys confirm they occur but cannot measure frequency or magnitude.
- The 570-comment sample from 200 threads may not represent the full distribution of review types across Microsoft's diverse products.
- Primary coding by one researcher; validity strengthened by multi-round cross-researcher agreement but not fully independent dual coding.

---

## Authors & Institutions

Alberto Bacchelli -- REVEAL @ Faculty of Informatics, University of Lugano, Switzerland. Christian Bird -- Microsoft Research, Redmond, Washington, USA. Published at ICSE 2013 (35th International Conference on Software Engineering).
