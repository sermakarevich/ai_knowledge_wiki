# Modern Code Review: A Case Study at Google

**Paper:** [Modern Code Review: A Case Study at Google (Sadowski, Söderberg, Church, Sipko, Bacchelli, 2018)](https://dl.acm.org/doi/10.1145/3183519.3183525)

## Human Readable TL;DR

Imagine a company where every single line of code -- no matter who writes it -- must be read and approved by at least one colleague before it goes live. That is Google, and this paper is a behind-the-scenes look at how that works in practice across tens of thousands of engineers. The researchers interviewed developers, ran a survey, and dug through logs of nine million code submissions to understand why Google does this, how the process actually unfolds, and whether people find it worthwhile. The short answer: reviews at Google are remarkably fast and small compared to other companies, developers genuinely value them -- but not primarily to catch bugs. The real reasons are closer to teaching newcomers the codebase, keeping code readable for future engineers, and ensuring no one can quietly change something important without anyone noticing.

## TL;DR

This paper is the largest industrial study of modern (tool-based, asynchronous) code review: 12 semi-structured interviews + 44-respondent survey + log analysis of ~9 million reviewed changes at Google over two years (Jan 2014 -- Jul 2016). Key findings: the dominant motivations are education, maintaining norms, gatekeeping, and accident prevention -- not defect finding. Quantitatively, the median developer authors ~3 changes/week, the median change size is 24 lines modified, median overall review latency is under 4 hours, fewer than 25% of changes involve more than one reviewer, and developers spend a median of 2.6 hours/week reviewing. Google's internal tool Critique tightly integrates automated static analysis, reviewer recommendation, and comment threading, making the process lighter weight than any previously studied project.

---

## Problem & Motivation

Prior large-scale studies of modern code review (principally Rigby & Bird, FSE 2013) identified five convergent practices across OSS and industrial projects but did so from a broad, multi-project perspective. No study had examined a single organization with a multi-decade history of code review, explicit cultural norms, more than 25,000 active developers, and 20,000+ daily changes -- a scale and longitudinal depth unavailable elsewhere. The paper asks: (RQ1) What motivates code review at Google? (RQ2) What does the process look like quantitatively? (RQ3) How do developers perceive and experience code review, including its breakdowns?

---

## Main Original Ideas

1. **Education as the primary motivation, not defect finding.** Code review was introduced at Google specifically to force developers to write code other developers could understand -- predating concern about bugs. Today's developers still cite education, readability, and knowledge transfer as central values, making Google's review culture distinct from the defect-hunting framing common in inspection research.

2. **The ownership + readability dual-gate system.** Every directory in Google's monorepo has explicit owners who must approve changes to it. Additionally, every change must be authored or reviewed by someone with "readability" certification in the language used -- a formal credential earned by demonstrating deep knowledge of style and idioms. This dual requirement is enforced by Critique and is not present in other studied systems.

3. **Critique as a next-generation review tool.** Critique is an internally developed, centralized, web-based tool that goes beyond comment threading: it integrates automated static analysis results (via Tricorder, covering 110+ analyzers across 30+ languages) directly alongside human comments, provides tool-generated reviewer recommendations, supports pre-commit checks, and logs all developer interactions -- enabling the large-scale empirical analysis in this paper.

4. **Review motivations are relationship-dependent.** By tracking in which author--reviewer relationship each motivation theme arose, the paper shows that education and norm maintenance dominate when a senior or readability expert reviews junior work, while gatekeeping and accident prevention dominate across team boundaries. This context-sensitivity had not been documented before.

5. **Critique used beyond collaborative review.** Developers use Critique to browse change history, understand how bugs were introduced, examine diffs during development (before sending for review), and inspect old approved changes -- extending the tool's value well past the review transaction itself.

---

## Key Findings

### Scale and data sources

| Source | Details |
|---|---|
| Interviews | 12 semi-structured, ~1 hour each; tenure 1 month -- 10 years, median 5 years |
| Survey | Sent to 98 engineers; 44 valid responses (45% response rate) |
| Log data | ~9 million changes (Jan 2014 -- Jul 2016); ~13 million comments (Sep 2014 -- Jul 2016) |
| Active developers | >25,000 authors and reviewers in dataset; >20,000 changes committed per workday |

### Review frequency

| Metric | Value |
|---|---|
| Median changes authored per developer per week | 3 |
| 80th-percentile changes authored per week | <7 |
| Median changes reviewed per developer per week | 4 |
| 80th-percentile changes reviewed per week | <10 |

### Change (CL) size

| Metric | Value |
|---|---|
| Changes modifying only 1 file | >35% |
| Changes modifying fewer than 10 files | ~90% |
| Changes modifying a single line of code | >10% |
| **Median lines modified** | **24** |

Comparison: AMD 44 lines, Lucent 263 lines, Microsoft projects up to 263 lines; OSS projects 11--32 lines. Google matches OSS, not large-company norms.

### Review latency

| Metric | Value |
|---|---|
| Median time to first feedback (small changes) | <1 hour |
| Median time to first feedback (very large changes) | ~5 hours |
| **Median overall review latency (all sizes)** | **<4 hours** |
| Changes committed within 24 hours of mailing | 70% |
| AMD median time to approval | 17.5 hours |
| Chrome OS median time to approval | 14.7 hours |
| Microsoft (3 projects) median | 14.7--18.9 hours |
| Microsoft (separate study) median | 24 hours |

### Reviewer count and comments

| Metric | Value |
|---|---|
| Changes with >1 reviewer | <25% |
| Changes with <=5 reviewers | >99% |
| **Median reviewer count** | **1** |
| Changes with comments from >1 commenter | ~30% |
| Changes with additional non-approver comments | ~5% |
| Peak average comments per change | ~12.5 (at ~1,250 lines changed) |

New developers (<=1 year tenure) receive more than twice as many comments per change as veterans, consistent with the educational role of review.

### Time spent reviewing

| Metric | Value |
|---|---|
| Average hours/week reviewing | 3.2 |
| **Median hours/week reviewing** | **2.6** |
| OSS self-reported comparison | 6.4 hours/week |

Over 80% of all changes involve at most one iteration of resolving comments before approval.

### Developer satisfaction (survey, n=44)

| Statement | Response distribution (1=strongly disagree, 5=strongly agree) |
|---|---|
| "This review was a good use of my time" | 2, 4, 14, 11, 13 |
| "Overall, code review at Google is valuable" | 0, 0, 0, 14, 30 |
| Feedback amount (Too little -- Too much) | 2, 2, 34, 5, 0 |

97% of developers satisfied with code review per internal Critique surveys. All 44 respondents agreed code review is valuable. Only 2 respondents reported a reviewer found a bug in their specific recent change.

### Motivations (open coding from interviews, confirmed by survey)

Each theme was selected by 8--11 of 44 survey respondents for a specific recent code review:
- **Education** -- teaching or learning about the codebase
- **Maintaining norms** -- enforcing style, API patterns, design consistency
- **Gatekeeping** -- controlling ownership boundaries and design artifacts
- **Accident prevention** -- avoiding bugs, security issues, or unwanted side effects

Defect finding is welcomed but is not the primary stated motivation. Expectations depend on the author--reviewer relationship (Finding 2).

### Breakdown themes (interviews, n=12)

| Theme | Description |
|---|---|
| Distance | Geographical or organizational distance causes delays and misunderstandings |
| Social interactions | Negative tone in comments; power dynamics used to coerce behavior |
| Review subject | Disagreement on whether design belongs in code review vs. earlier phases |
| Context | Lack of change rationale leads to mismatched expectations |
| Customization | Non-standard team requirements not fully supported by Critique |

---

## Suggestions & Future Directions

1. **Tools for decomposing large changes.** Large CLs attract more comments but receive less useful feedback per line; the authors call for research and tooling to help developers automatically decompose changes into small, self-contained units.

2. **Investigate non-review uses of review tools.** Critique is used for history browsing, understanding bug introductions, and development-time diffing -- uses not captured by review-focused metrics. Future work should study these uses and their impact on productivity.

3. **Quantify code review's effect on developer fluency.** The number of distinct files seen (edited or reviewed) grows steeply with seniority; reviewing exposes developers to far more of the codebase than editing alone. Future work should measure how this exposure affects fluency and onboarding speed.

4. **Automated feedback loop for static analyzers.** Critique's "Please fix" / "Not useful" buttons on analyzer-generated comments create a feedback loop that fixes or disables low-quality analyzers. The authors flag this as critical for maintaining developer trust and propose it as a design pattern for future tools.

5. **Cross-company replication.** Results may not generalize beyond Google; the authors call for focused, longitudinal studies at other organizations that have reached comparable review maturity, to test whether the convergent practices hold at this scale.

6. **Tone and power dynamics in review comments.** Interviews surfaced these as breakdown sources; prior sentiment-analysis work shows negative-tone comments are less useful. The authors suggest both tool support and organizational intervention as directions for future work.

---

## Authors & Institutions

Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko -- Google, Inc.; Alberto Bacchelli -- University of Zurich. Published in *Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice Track (ICSE-SEIP '18)*, Gothenburg, Sweden, May 27 -- June 3, 2018. DOI: 10.1145/3183519.3183525.
