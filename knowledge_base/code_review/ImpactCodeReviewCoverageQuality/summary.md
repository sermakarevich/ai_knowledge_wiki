# The Impact of Code Review Coverage and Code Review Participation on Software Quality

**Paper:** [The Impact of Code Review Coverage and Code Review Participation on Software Quality: A Case Study of the Qt, VTK, and ITK Projects (McIntosh, Kamei, Adams, Hassan, MSR 2014 / EMSE 2016)](https://rebels.cs.uwaterloo.ca/papers/emse2016_mcintosh.pdf)

## Human Readable TL;DR

Imagine a factory where workers are supposed to inspect each other's work before shipping it out. Some inspectors just glance at the item and wave it through -- no real conversation, no questions asked. This study asked: does skipping inspections, or doing them half-heartedly, actually lead to more customer complaints later? The answer is yes, but with a twist: simply making sure every item gets glanced at is not enough. What really matters is whether the inspectors actually talk about the work in depth, and whether at least one of them is an expert in that product area. The study found that even 100% inspection coverage still led to defective products when the inspectors did not engage.

## TL;DR

McIntosh et al. mined Gerrit code review data from four releases of Qt (5.0, 5.1), VTK (5.10), and ITK (4.3) -- totaling 1,121--1,339 components per Qt release and 170--218 for VTK/ITK -- and built OLS regression models (with restricted cubic splines and 1,000-iteration bootstrap validation) to explain post-release defect counts as a function of review coverage, participation, and expertise metrics while controlling for size, complexity, churn, entropy, and ownership. Review coverage (proportion of reviewed changes) is negatively associated with post-release defects but achieves statistically significant explanatory power in only 2 of 4 releases; review participation metrics (especially changes without discussion and hastily-reviewed changes) contribute significant explanatory power to all studied releases; reviewer expertise (lacking subject matter expert involvement) contributes significantly in the larger Qt releases. Coverage models achieve adjusted R^2 of 0.39--0.67; participation models 0.46--0.69; expertise models 0.47--0.69, with bootstrap-optimism-reduced values of 0.20--0.68.

---

## Problem & Motivation

Formal code inspections (Fagan 1976) are known to improve quality, but modern lightweight code review -- as practiced via tools like Gerrit -- lacks the mandated structure of formal inspections: no in-person meetings, no checklists, no guaranteed depth of engagement. The key open question was whether lax modern review practices (low coverage, superficial participation, missing expertise) actually allow defect-prone code to reach released software.

The paper tests the conjecture: if many changes are omitted from review (low coverage), reviewed without real discussion (low participation), or not examined by subject matter experts (low expertise), then defect-prone code will permeate into the released product.

---

## Main Original Ideas

1. **Three-dimensional decomposition of review quality.** Prior work treated code review as binary (reviewed / not reviewed). This paper decomposes review quality into three orthogonal dimensions -- coverage, participation, and expertise -- constructing separate metric families for each and measuring their independent contributions while controlling for the others.

2. **Coverage metrics (RQ1).** Two metrics: (a) *proportion of reviewed changes* -- fraction of commits to a component linked to a Gerrit review; (b) *proportion of reviewed churn* -- fraction of added/removed lines that were reviewed. Both computed per component (directory level) over the six-month pre-release window on the release branch.

3. **Participation metrics (RQ2).** Five metrics capturing review depth: *self-approved changes* (author-only approval); *hastily-reviewed changes* (approved faster than 200 lines/hour -- a best-practice threshold from Kemerer and Paulk 2009); *changes without discussion* (approved with zero non-automated comments from other team members); *typical review window* (median time from patch creation to approval, normalized by churn); *typical discussion length* (median number of non-automated comments per change, normalized by churn). The last two are new in the extended EMSE version relative to MSR 2014.

4. **Expertise metrics (RQ3).** Two metrics: *number of changes lacking subject matter expertise* -- changes where neither the author nor any reviewer is a major contributor (>=5% of commits) to that component; *typical reviewer expertise* -- median fraction of prior changes to the component that each approving reviewer has previously authored or approved. Subject matter experts are operationalized using Bird et al. (2011)'s major author definition.

5. **Non-linear OLS regression with restricted cubic splines and bootstrap validation.** The modelling framework (Harrell 2002, rms R package) relaxes the linearity assumption by fitting restricted cubic splines, budgets degrees of freedom at n/15, removes collinear variables via Spearman clustering (|rho|>0.7 cutoff) and redundant variables via R^2>=0.9 analysis, and uses 1,000-iteration bootstrap to compute optimism-reduced adjusted R^2. Effect sizes are estimated by plotting the predicted defect count against each review metric while holding all other variables at their median values.

---

## Key Findings

### Studied system characteristics (Table 1)

| System | Version | Size (LOC) | Components total | Defective rate | Review rate | Authors | Reviewers |
|---|---|---|---|---|---|---|---|
| Qt | 5.0 | 5,560,317 | 1,339 | 19% | 98% | 435 | 358 |
| Qt | 5.1 | 5,187,788 | 1,337 | 14% | 96% | 422 | 348 |
| VTK | 5.10 | 1,921,850 | 170 | 9% | 39% | 55 | 45 |
| ITK | 4.3 | 1,123,614 | 218 | 11% | 98% | 41 | 37 |

Qt and ITK have near-universal review coverage (~96--98%); VTK has only 39%. Post-release defects are counted from fix-keyword VCS commits in the six-month window following each release.

### RQ1 -- Coverage model fit (Table 5)

| Release | Adj. R^2 | Bootstrap-reduced R^2 | Reviewed changes significant? |
|---|---|---|---|
| Qt 5.0 | 0.64 | 0.62 | No (weak rho = -0.10, p<0.001 but not significant in model) |
| Qt 5.1 | 0.67 | 0.65 | **Yes** (Wald chi^2 = 84, p<0.001) |
| VTK 5.10 | 0.39 | 0.20 | **Yes** (Wald chi^2 = 12, p<0.001) |
| ITK 4.3 | 0.44 | 0.22 | No |

Coverage achieves statistically significant explanatory power in 2 of 4 releases. Even components with 100% review coverage can be defective: 87% (222/254) of defective VTK components, 70% (131/187) of defective Qt 5.0, and 83% (20/24) of defective ITK components have full coverage (proportion = 1.0), and the difference in defect incidence between full-coverage and lower-coverage components is only significant for Qt 5.1 (Mann-Whitney p < 2.2 x 10^-16).

### RQ2 -- Participation model fit (Table 7)

| Release | Adj. R^2 | Bootstrap-reduced R^2 | No-discussion significant? | Typical discussion length significant? |
|---|---|---|---|---|
| Qt 5.0 | 0.69 | 0.68 | Yes (chi^2 = 6, p<0.05) | Yes (chi^2 = 20, p<0.001) |
| Qt 5.1 | 0.46 | 0.40 | Yes (chi^2 = 5, p<0.05) | Yes (chi^2 = 37, p<0.001) |
| ITK 4.3 | 0.58 | 0.43 | Yes (chi^2 = 30, p<0.001) | Yes (chi^2 = 3, p~0.05) |

Discussion-related participation metrics survive model construction and contribute significant explanatory power across all three studied releases (VTK was dropped from RQ2 because only 5% of its components survive the 100%-coverage filter). More changes without discussion correlates with a higher estimated post-release defect count. Self-approval does not significantly impact the defect models, likely because Gerrit self-approval rights in Qt are restricted to senior team members.

### RQ3 -- Expertise model fit (Table 9)

| Release | Adj. R^2 | Bootstrap-reduced R^2 | Lacking SME significant? |
|---|---|---|---|
| Qt 5.0 | 0.69 | 0.67 | **Yes** (Wald chi^2 = 80, p<0.001) |
| Qt 5.1 | 0.47 | 0.40 | **Yes** (Wald chi^2 = 34, p<0.001) |
| ITK 4.3 | 0.55 | 0.40 | No (chi^2 < 1) |

"Lacking subject matter expertise" has the highest Spearman rho^2 with post-release defects in Qt 5.0 (adjusted rho^2 ~0.35+, Fig. 12), making it the strongest single predictor. The effect is not significant in ITK, likely due to small sample size (218 components, 41 developers).

### Direction and magnitude of effects (Figures 7, 10, 13)

- **Coverage (Qt 5.1, VTK):** Steep decline in estimated post-release defects as proportion of reviewed changes approaches 1.0, but mostly confined to the 0.9--1.0 interval. Only 41 of 1,337 Qt 5.1 components (3%) have coverage below 0.9.
- **No discussion:** Monotonically increasing estimated defect count as the number of changes without discussion grows (Qt 5.0 and ITK 4.3).
- **Lacking SME (Qt 5.0):** Monotonically increasing estimated defect count as the number of changes without an expert author/reviewer increases, with a slowing trend after count of ~8 changes.
- **Typical discussion length:** Non-monotonic -- an initial sharp increase in defect-proneness as discussion length grows from zero, then a decreasing or flat trend; the net impact on defect counts is small.

### Key takeaway: participation > coverage

Participation metrics consistently outperform coverage metrics in explanatory power. The conclusion for practitioners: enforcing a policy that every commit gets reviewed (coverage) is a necessary but not sufficient condition for quality; the depth of the review discussion and expert involvement are what actually move the needle on post-release defect rates.

---

## Suggestions & Future Directions

1. **Replicate on additional systems.** Only three open source projects satisfied the traceability and review-policy criteria (Android and LibreOffice were dropped because only 2% and 14% of their commits could be linked to reviews). Proprietary systems with tool-traceable reviews are needed to generalize.

2. **Weight defects by severity.** All post-release defects are counted equally. Stratifying by severity -- if reliable severity data can be obtained -- could reveal whether review participation has a stronger effect on critical bugs than on minor ones.

3. **Establish causal mechanisms.** The analysis is correlational. Components lacking subject matter experts may differ systematically in ways not captured by the baseline metrics. Controlled experiments or natural experiments (e.g., team reorganizations) could help establish causality.

4. **Integrate participation metrics into real-time tooling.** The authors suggest monitoring discussion volume and review speed at integration time, not post-hoc, to support automated gatekeeping that flags changes with insufficient engagement before they are merged.

5. **Refine the subject matter expert proxy.** The major-author threshold (>=5% of commits) is a heuristic. Future work should validate this against other expertise signals (file-level ownership metrics, developer self-assessment) and test sensitivity to the threshold choice.

6. **Jointly model all three dimensions.** Each RQ was modelled separately, controlling for coverage before studying participation and expertise. A unified model estimating coverage, participation, and expertise simultaneously could reveal interaction effects -- for example, whether expert participation compensates for lower coverage.

---

## Authors & Institutions

Shane McIntosh, Ahmed E. Hassan -- Software Analysis and Intelligence Lab (SAIL), Queen's University, Canada.
Yasutaka Kamei -- Principles of Software Languages group (POSL), Kyushu University, Japan.
Bram Adams -- Lab on Maintenance, Construction, and Intelligence of Software (MCIS), Polytechnique Montreal, Canada.

Original MSR 2014 Distinguished Paper Award: Proc. 11th Working Conference on Mining Software Repositories, pp. 192--201.
Extended EMSE journal version: Empirical Software Engineering, Springer, DOI: 10.1007/s10664-015-9381-9.
