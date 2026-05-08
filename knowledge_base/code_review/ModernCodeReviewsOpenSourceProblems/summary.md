# Modern Code Reviews in Open-Source Projects: Which Problems Do They Fix?

**Paper:** [Modern Code Reviews in Open-Source Projects: Which Problems Do They Fix? (Beller, Bacchelli, Zaidman, Juergens, 2014)](https://dl.acm.org/doi/10.1145/2597073.2597082)

## Human Readable TL;DR

When developers check each other's code in modern lightweight review tools, the vast majority of what actually gets changed is about tidiness and long-term maintainability -- not fixing bugs. Think of it like editing a colleague's report: most corrections are about clarity, structure, and style, not factual errors. About three out of four changes in reviewed code are of this "tidiness" kind -- nearly the same ratio found in older, much heavier formal review meetings from decades ago. Surprisingly, the tool used, the reviewer's identity, and whether the project is written in Java or C don't seem to matter much -- the ratio stays remarkably stable. Also, up to one in five changes happens because the author decided to improve things themselves, not because any reviewer explicitly asked.

## TL;DR

Beller et al. manually classified 1,469 code changes from two mature OSS projects -- ConQAT (Java) and GROMACS (C) -- that practice mandatory, continuous Modern Code Review (MCR). Using a classification scheme adapted from Mantyla & Lassenius 2009, they found 75--81% of changes are evolvability-related (maintainability, comments, naming, structure) versus 19--31% functional. This 75:25 split directly replicates the Mantyla 2009 result obtained from heavyweight formal inspections, showing the ratio is robust across review styles. Additionally, 10--22% of all changes are undocumented (not triggered by any review comment), reviewers discard 7--35% of their own suggestions, and the reviewer's identity has no statistically significant effect on the number of changes -- whereas code churn, number of changed files, and task type do.

---

## Problem & Motivation

Prior research analyzed the *comments* reviewers write, not the *changes* that actually appear in accepted code. Comments can be ignored, misunderstood, or overtaken by autonomous author action -- so comment analysis gives an incomplete picture of what MCR actually fixes. Furthermore, all prior defect-type studies used formal inspection processes; it was unknown whether findings generalize to the lightweight, tool-assisted review style dominant in modern OSS.

The paper also replicates and stress-tests the 75% evolvability ratio from Mantyla & Lassenius 2009, which was based on one industrial company and student groups, by applying the same classification to two OSS projects with different languages (Java, C), tools (Eclipse/SVN, Gerrit), and team cultures.

---

## Main Original Ideas

1. **Studying actual fixes, not review comments.** The paper operationalizes "what MCR fixes" as the diff between submitted and accepted source code across all review rounds -- not what reviewers wrote. This requires pairing TMS data with VCS history round-by-round, implemented via a custom Eclipse plugin.

2. **Adapting Mantyla's taxonomy to modern OSS.** The functional vs. evolvability split from Mantyla & Lassenius 2009 is adopted with small adaptations: Java/C-specific constructs added (e.g. `assert`, `abstract` modifier); all sub-categories of the resource functional group removed (too rare); false positives removed as a category (by definition a change either occurred or did not). The taxonomy (Figure 3) is: evolvability -- Structure (solution approach, organization), Visual Representation (supported-by-language, formatting), Documentation (textual, naming); functional -- Larger Defects, Support, Check, Resource, Logic, Interface.

3. **Quantifying undocumented and discarded review activity.** Two phenomena invisible to comment-only studies are measured: (a) 10--22% of all changes are undocumented -- author-initiated improvements not requested by any reviewer; (b) 7--35% of review comments lead to no change (discarded). Both are substantial and absent from prior literature.

4. **Regression model of what drives the number of changes.** A generalized linear model (negative binomial) on 2,880 changes across 973 ConQAT tasks identifies significant predictors: code churn (positive), number of changed files (positive), task type -- corrective/bug-fix tasks yield fewer changes than perfective/new-feature tasks. The reviewer's identity is statistically insignificant.

---

## Key Findings

### RQ1 -- Evolvability vs. functional changes

| Sample | Evolvability | Functional | Notes |
|---|---|---|---|
| **ConQAT-rand** | **81%** | 19% | 892 changes, 100 tasks, Java |
| **ConQAT-100** | 75% | 25% | 361 changes, 89 recent tasks, Java |
| **GROMACS-rand** | 69% | 31% | 216 changes, 60 tasks, C |
| Industrial reviews (Mantyla 2009) | 77% | 23% | Formal inspection baseline |
| Student reviews (Mantyla 2009) | 85% | 15% | Formal inspection baseline |

- All three OSS samples float within a 10-percentage-point band around 75:25, consistent with Mantyla's formal-inspection results.
- Dominant evolvability sub-category across all samples: documentation (comments and identifier naming).
- GROMACS shows zero "documentation-language" changes -- C lacks object-oriented doc constructs (e.g. Javadoc).
- ConQAT has low visual representation changes because developers use Eclipse's auto-formatter.

### RQ1 -- Task and change volume

| Metric | ConQAT-rand | ConQAT-100 | GROMACS-rand |
|---|---|---|---|
| Valid tasks | 100 | 89 | 60 |
| Total changes | 892 | 361 | 216 |
| Average changes/task | 8.81 | 4.00 | 3.24 |
| Median changes/task | 2 | 0 | 0 |
| Max changes/task | 208 | 110 | 93 |

Distribution is heavily skewed: median = 0 for ConQAT-100 and GROMACS, meaning most tasks pass review with no changes at all.

### RQ2 -- Triggers for code changes

| Sample | Review-triggered | Undocumented (author-initiated) |
|---|---|---|
| ConQAT-rand | 86% | 14% |
| ConQAT-100 | 90% | 10% |
| GROMACS-rand | 78% | 22% |

- ConQAT: 93% (rand) / 91% (100) of review comments actually lead to a change; GROMACS: only 65% -- 35% are discarded.
- Undocumented changes occur only when there is at least one review-triggered change in the same task; pure author-only improvement without any reviewer input was not observed.

### RQ3 -- Predictors of number of changes (ConQAT, n=973 tasks)

| Factor | Direction | Significance |
|---|---|---|
| Code churn | Positive (beta = 0.0026) | p < 2.34e-16 ** |
| Number of changed files | Positive (beta = 0.0483) | p < 2e-16 ** |
| Task type: corrective (bug-fix) | Negative (beta = -0.6508) | p = 0.0496 * |
| Task type: perfective (new feature) | Positive (beta = 0.7015) | p = 0.0138 * |
| Reviewer identity | Not significant | p = 0.23 |

Bug-fixing tasks lead to fewer changes than new-feature tasks; large code churn and many touched files predict more review changes.

### Interrater reliability

- Kappa for evolvability vs. functional distinction: 0.5--0.6 ("fair to good agreement") on detailed classification; 0.5--0.8 when only differentiating the two top-level groups ("fair to excellent agreement").
- Kappa for trigger classification (RQ2): 0.8--1.0 ("fair to complete agreement").

---

## Suggestions & Future Directions

1. **Broader multi-project replication.** Only two OSS projects satisfied mandatory continuous-review criteria; more languages, domains, and team sizes are needed to generalize the 75:25 ratio.

2. **Investigate undocumented changes.** The 10--22% of self-motivated changes suggest code review triggers autonomous author reflection beyond explicit reviewer requests -- a phenomenon worth studying to improve review process design.

3. **Characterize discarded comments.** Up to 35% of GROMACS review comments lead to no change. Future work should classify which comment types are discarded and why (disagreement, redundancy, oral resolution).

4. **Review-task recommender tool.** The authors envision a tool that, given a reviewer's time budget, suggests which tasks are most profitable to review, using the regression model's predictors as features.

5. **Cross-method defect-type comparison.** Measure the evolvability/functional split for unit testing, static analysis, and acceptance testing to enable evidence-based QA technique selection.

6. **Task splitting intervention.** The skewed distribution and large-task clustering suggest enforced sub-task splitting could produce more uniform, higher-quality reviews; a controlled experiment is proposed.

---

## Authors & Institutions

Moritz Beller, Alberto Bacchelli, Andy Zaidman -- Delft University of Technology, The Netherlands. Elmar Juergens -- CQSE GmbH, Germany. Published in *Proceedings of the 11th Working Conference on Mining Software Repositories (MSR 2014)*, May 31--June 1, 2014, Hyderabad, India.
