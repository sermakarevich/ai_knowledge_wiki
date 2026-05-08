# Information Needs in Contemporary Code Review

**Paper:** [Information Needs in Contemporary Code Review (Pascarella, Spadini, Palomba, Bruntink, Bacchelli, 2018)](https://doi.org/10.1145/nnnnnnn.nnnnnnn)

## Human Readable TL;DR

When one developer looks at another's code to check it, they constantly have questions -- "why did you do it this way?", "could we do this differently?", "does this piece even need to exist?" This paper is like a birdwatcher's field guide for those questions: the authors listened to 900 real code-review conversations and sorted every question into a neat map of seven flavors of curiosity. The big surprise is that the most common question is not "is this broken?" but "is there a better way?" -- reviewers spend more energy proposing alternatives than hunting bugs. And most of these questions get answered in under seven hours, suggesting that if a tool could answer them automatically, it would save reviewers an enormous amount of waiting.

## TL;DR

The authors manually analyzed 900 code review discussion threads from three large OSS projects on Gerrit (OpenStack, Android, Qt) using an open card-sort process to build a two-layer taxonomy of reviewers' information needs: 7 top-level categories and 18 sub-categories. The dominant need is N1 "Suitability of an Alternative Solution" -- far more frequent than all other categories -- followed by N2 "Correct Understanding." All needs receive a response within a median of under 7 hours across projects. The taxonomy was validated with inter-rater agreement of Krippendorff's k = 98% and triangulated through 4 semi-structured interviews and 1 focus group with experienced developers from both OSS and industry.

---

## Problem & Motivation

Modern code review is cognitively demanding: reviewers must evaluate correctness, design, style, and rationale for unfamiliar code, often under time pressure. Despite extensive research on review participation and defect detection, no prior work had systematically catalogued what information reviewers actually need to do their job well. Understanding these needs is a prerequisite for building tools that reduce cognitive load and enable better collaboration, as well as for directing research toward the most impactful open problems.

The gap: prior studies told us code review matters and who participates, but not *what reviewers need to know* while doing it.

---

## Main Original Ideas

1. **A hierarchical taxonomy of reviewers' information needs.** Through iterative open card sorting across three OSS projects, the authors produced a stable two-layer classification: 7 top-level categories and 18 sub-categories. The taxonomy reached saturation -- when applied to two new projects it required no new categories -- and achieved a Krippendorff's k of 98% between two independent coders.

2. **Frequency distribution across all needs.** By counting category occurrences across 900 threads, the paper provides the first empirical ranking of how common each information need is. N1 (Suitability of an Alternative Solution) dominates by a wide margin; N7 (Splittable) is the rarest. This ranking was consistent across all three projects.

3. **Lifecycle analysis of information needs.** The authors tracked when in the review process each need arises (which iteration), how many replies it attracts, and how long it takes to receive a response. Most needs arise at any iteration (median normalized iteration ~0.5), except N5 "Necessity" which tends to emerge later (median 0.67).

4. **Triangulation via interviews and focus group.** Four semi-structured interviews with developers from the three OSS systems, plus a focus group at a European software quality consultancy (3 participants with 15+ years of code review experience), confirmed the taxonomy and its ranking -- with one notable nuance: industrial co-located developers rarely ask N2 "Correct Understanding" questions because they can walk over to a colleague.

5. **Tool implications grounded in empirical data.** The paper translates findings directly into five concrete tool directions: expert recommender systems (N1, N6), early detection of splittable changes (N7), automated alternative-solution mining (N1), synchronous communication channels inside review tools (N2, N3), and automatic change summarization (N2, N3).

---

## Key Findings

### Full Taxonomy of Reviewers' Information Needs

| # | Top-Level Category | Sub-categories | Relative Prevalence |
|---|---|---|---|
| N1 | **Suitability of an Alternative Solution** | N1.A Suggest changes, N1.B Ask changes, N1.C Request actions | Highest -- far exceeds all others; consistent across all 3 projects |
| N2 | **Correct Understanding** | N2.A Request confirmations, N2.B Doubts & clarification, N2.C Opinions | 2nd most frequent; ~200 occurrences total |
| N3 | **Rationale** | N3.A Missing information, N3.B Justifications | 3rd; ~105 occurrences total |
| N4 | **Code Context** | N4.A Context clarification, N4.B Code clarification | 4th; noticeably less frequent than N3 |
| N5 | **Necessity** | N5.A Usefulness, N5.B Obvious prechecks, N5.C Redundant | 5th; emerges later in review lifecycle (median iteration 0.67) |
| N6 | **Specialized Expertise** | N6.A Request solutions, N6.B Need help, N6.C Involve other reviewers | 6th; highest reply-count variance -- most discussion-heavy per thread |
| N7 | **Splittable** | N7.A Postpone changes, N7.B Unrelated changes | Lowest frequency; rarest need overall |

Approximate counts from Figure 4 (total across 3 projects, 900 threads):
- N1: ~420 occurrences
- N2: ~200 occurrences
- N3: ~105 occurrences
- N4: ~40 occurrences
- N5: ~25 occurrences
- N6: ~20 occurrences
- N7: ~10 occurrences

Approximately 4% of threads were discarded (noise, sarcasm, non-informational questions) into a separate "Discarded" meta-category.

### Response Time and Discussion Load

- Median response time for all categories: under 7 hours.
- N1 has the lowest mean reply count (1.7) -- authors often implement the alternative directly without replying, which is statistically distinct from other categories (Mann-Whitney p < 0.01, Cliff's d = medium).
- N6 has the highest reply-count variance -- requests for specialized expertise generate the most extended discussions.
- N5 and N1 show higher median response hours (3rd quartile ~1 day) compared to other categories.
- ~18% of threads received no reply at all (across both merged and abandoned patches).

### Information Needs Over the Review Lifecycle

- Most needs have median normalized iteration ~0.5 (arise evenly throughout the review process).
- N5 Necessity is an outlier (median 0.67) -- questions about whether code is needed tend to appear after the main fixes are already submitted, consistent with perfective change requests coming later in the process.

### Practitioner Validation

- All interviewees confirmed the taxonomy and its frequency ranking; the ordering of importance was: N1 > N2 > N3 > N4, with N7 confirmed as important but rare.
- Focus group (industrial, co-located context) agreed with taxonomy but reported N2 less common in their setting due to direct colleague access.
- Unanimous agreement that patches should be small, self-contained, and that tools should support early splitting of tangled changes.

---

## Suggestions & Future Directions

1. **Expert and reviewer recommendation tools.** Build systems that identify sub-system experts and proactively suggest them to reviewers (not just to change authors) during a review, targeting N1 and N6. This inversion -- recommending experts to reviewers rather than to authors -- is a novel research direction not covered by prior work.

2. **Automated detection and splitting of tangled changes.** No commercial tool offers this feature despite strong practitioner demand and existing academic approaches. Integrate untangling at submission time -- in the IDE -- so authors send atomic patches before review begins.

3. **Mining and surfacing alternative solutions at review time.** Automatically mine public code repositories, Stack Overflow, and project history to propose alternatives for the implementation under review, directly addressing the most frequent information need (N1).

4. **Synchronous communication within review tools.** Facilitate real-time discussion without leaving the review interface. Both OSS and industrial practitioners preferred direct communication (IRC, Slack, in-person) for difficult clarification questions -- integrating lightweight chat could reduce delays and off-tool side channels.

5. **Automatic change summarization.** Use code summarization research (Buse & Weimer, CILDiff, ChangeScribe) to supplement or verify developer-written commit messages, especially for novice contributors whose descriptions are often inadequate, addressing N2 and N3.

6. **Extend study to closed-source and non-Gerrit platforms.** The current dataset is limited to OSS projects using Gerrit. GitHub, GitLab, and Collaborator are explicitly identified as future targets. Industrial co-location may suppress N2 needs that appear prominently in distributed OSS contexts.

7. **Time-sensitive tool support.** Since N5 Necessity appears late in the review lifecycle, explore whether future tools could proactively surface certain questions at specific iteration stages, guiding reviewers toward the right concerns at the right time.

---

## Authors & Institutions

Luca Pascarella -- Delft University of Technology, The Netherlands
Davide Spadini -- Delft University of Technology, The Netherlands
Fabio Palomba -- University of Zurich, Switzerland
Magiel Bruntink -- Software Improvement Group, Amsterdam, The Netherlands
Alberto Bacchelli -- University of Zurich, Switzerland

Published in *Proceedings of the ACM on Human-Computer Interaction (PACMHCI)*, Vol. 2, CSCW, August 2018.
