# Code Reviews Do Not Find Bugs

**Paper:** [Code Reviews Do Not Find Bugs. How the Current Code Review Best Practice Slows Us Down (Czerwonka, Greiler, Tilford, ICSE-SEIP 2015)](https://www.microsoft.com/en-us/research/wp-content/uploads/2015/05/PID3556473.pdf)

## Human Readable TL;DR

Imagine your team spends every afternoon having everyone proofread every memo before it goes out -- the theory being that proofreading catches mistakes. But when you actually count the mistakes found, you discover that almost none are factual errors; most are style notes, and the proofreading pile-up is the biggest bottleneck in your whole office. That is the situation with code reviews at Microsoft. The authors looked at real review data and found that fewer than 15% of reviewer comments flag an actual bug that should stop the code from shipping. The rest is style, maintainability, and knowledge-sharing feedback -- all valuable, but not bug detection. The current blanket rule of "review everything, always" is too blunt: it burns developer time (six hours a week per person) and slows releases by 24+ hours per change, yet the bug-finding payoff is much smaller than assumed.

## TL;DR

Drawing on engineering-workflow data from Microsoft's large-scale CODEMINE platform, Czerwonka et al. argue that code reviews rarely fulfill their assumed primary purpose of blocking functional defects: only ~15% of reviewer comments indicate a possible defect, and blocking defect catches are rarer still. At least 50% of all review comments address long-term code maintainability. Reviewer usefulness is positively correlated with familiarity with the code area -- without prior exposure only 33% of comments are judged useful by the author, rising to ~67% after the reviewer's third encounter with the same region. Review usefulness is also negatively correlated with review size, degrading noticeably for reviews touching 20 or more files. The authors conclude that the blanket "everyone reviews everything" mandate is inefficient and call for a more targeted, skill-aware, cost-conscious approach to review assignment.

---

## Problem & Motivation

Code reviews are the longest single step in the modern code-integration pipeline, yet teams apply them uniformly to every change regardless of risk, reviewer expertise, or expected benefit. The authors identify a mismatch between the stated goal (finding bugs) and observed practice (mostly style and maintainability feedback). With developers spending on average six hours per week reviewing others' code, and a median review round-trip of 24 hours (often days or weeks for contested changes), the process imposes a substantial cost. The paper asks: are we applying code reviews in the most efficient way, or merely the conventional way?

---

## Main Original Ideas

1. **Code reviews do not primarily find bugs.** Only ~15% of reviewer comments flag a possible defect, and blocking defects are a small fraction even of those. The dominant signal is long-term maintainability feedback (at least 50% of all comments). Treating reviews as a bug-detection gate therefore miscalibrates both the effort invested and the metrics used to evaluate review quality.

2. **Reviewer familiarity drives comment usefulness.** Without prior exposure to the code area, a reviewer's comments are judged useful by the author only 33% of the time. After reviewing the same area a third time, usefulness climbs to ~67% -- equivalent to the project long-term average. Reviewer assignment matters enormously: an unfamiliar reviewer is a poor bug-finder and a mediocre quality signal.

3. **Review size is a quality killer.** Reviewer usefulness is negatively correlated with the number of files changed in a single review. The degradation becomes noticeable at 20+ changed files. Large reviews dilute attention, so the per-file bug-detection rate drops precisely when the absolute risk is highest -- inverting the intended safety relationship.

4. **The social dimension is inseparable from the technical one.** People's roles and standing in the team hierarchy influence both who reviews whom and how feedback is received. It is not only the author who is under scrutiny -- reviewers themselves feel evaluated. This social pressure shapes what gets said, how thoroughly reviewers engage, and whether critical feedback is surfaced or softened.

5. **Guidelines must be more sophisticated than "review everything."** The blanket best-practice rule is too coarse. Effective code review policy must account for: reviewer expertise in the specific code area, review size, the actual goal of a given review (bug-finding vs. knowledge transfer vs. maintainability), and the organizational cost of 24+ hour wait cycles on every change.

---

## Key Findings

| Metric | Value |
|---|---|
| Comments indicating a possible defect | ~15% of all review comments |
| Comments related to long-term maintainability | at least 50% of all review comments |
| Comment usefulness -- no prior code exposure | ~33% |
| Comment usefulness -- reviewer's 3rd encounter with same area | ~67% |
| Comment usefulness -- project long-term average (experienced) | ~67% |
| Developer time spent reviewing others' code | ~6 hours per week |
| Median time from review request to all sign-offs | ~24 hours (often days or weeks) |
| Review quality degradation threshold | 20+ changed files |

- Blocking defect catches are rarer than the ~15% "possible defect" headline -- that 15% includes non-blocking concerns.
- The 50%+ maintainability share provides large-scale industry corroboration for Mantyla & Lassenius (2009), who found ~75% of review findings are evolvability defects in smaller academic datasets.
- Long review times create process stalls: anyone waiting to take a dependency on new code is blocked, and longer review time makes it harder for authors to reintegrate feedback without introducing new defects.
- Data sourced from CODEMINE, Microsoft's cross-project software development analytics platform, giving findings a scale and breadth unusual in academic code-review research.

---

## Suggestions & Future Directions

1. **Match reviewers to code areas they know.** Assign reviewers based on demonstrated familiarity with the specific subsystem, not just availability or seniority. Tooling should surface reviewer history per code region.

2. **Break large changes before review.** Enforce or strongly encourage splitting reviews that would touch 20+ files into smaller, focused units. Review size limits should be a first-class policy lever.

3. **Differentiate review goals explicitly.** Separate "bug-blocking review" from "knowledge-sharing review" from "maintainability review" at submission time. Different goals warrant different reviewer pools, time budgets, and sign-off thresholds.

4. **Rethink the blanket "N sign-offs" rule.** Calibrate sign-off requirements to risk level, author experience, and code-area familiarity of available reviewers rather than applying a flat count to every change.

5. **Account for social dynamics in tooling design.** Hierarchy and standing affect what reviewers say and how thoroughly they engage. Structured or anonymized review formats may reduce social inhibition and surface more honest blocking feedback.

6. **Systematize code review as a measured engineering process.** Apply the same data-driven rigor used for testing or build systems -- track reviewer coverage, usefulness rates, and defect-detection yield per review type -- rather than applying reviews by convention alone.

---

## Authors & Institutions

Jacek Czerwonka, Michaela Greiler, Jack Tilford -- Microsoft Corporation, Redmond, WA 98075. Published at ICSE-SEIP (International Conference on Software Engineering, Software Engineering in Practice track), 2015.
