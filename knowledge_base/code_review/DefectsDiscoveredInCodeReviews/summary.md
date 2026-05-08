# What Types of Defects Are Really Discovered in Code Reviews?

**Paper:** [What Types of Defects Are Really Discovered in Code Reviews? (Mäntylä & Lassenius, 2009)](https://doi.org/10.1109/TSE.2008.71)

## Human Readable TL;DR

When developers read each other's code looking for problems, most of what they actually find isn't broken behavior -- it's messy code: bad names, missing comments, awkward structure, duplicated work. Three out of four issues spotted in code reviews wouldn't show up if you just ran the program, because they're about how easy the code is to understand and change later. So code reviews are less like a bug hunt and more like a tidiness inspection that pays off most for software you'll keep working on for years.

## TL;DR

The authors analyzed 759 defects from 9 industrial C/C++ code reviews (388 defects) and 23 student Java code reviews (371 defects), and found that ~75% are **evolvability defects** -- issues that hurt maintainability, readability, or modifiability without affecting runtime behavior -- rather than functional defects. They propose a two-tier defect taxonomy: an evolvability classification (documentation, visual representation, structure) constructed from this data, plus a functional classification (resource, check, interface, logic, timing, support, larger defects) consolidated from prior work. They argue this reframes code reviews as complementary to testing rather than redundant, and most valuable for long-lifecycle products.

---

## Problem & Motivation

Most prior code-review research counts defects without classifying their types, giving an "imperfect view" of review benefits. Earlier studies that did look qualitatively (e.g., Siy & Votta) hinted that ~75% of review findings are evolvability defects, but the broader literature kept treating reviews as primarily a tool for catching functional bugs -- which makes reviews look weak when compared to testing techniques that can only find functional defects anyway.

The authors set out to (1) confirm whether evolvability defects really dominate, (2) build a defect taxonomy that explicitly includes evolvability categories prior taxonomies had ignored, and (3) provide a foundation for review checklists, role assignment, and tool building.

---

## Main Original Ideas

1. **Evolvability vs. functional defect distinction.** They formally define an *evolvability defect* as a defect making code less standards-compliant, more error-prone, or harder to modify/extend/understand -- distinct from a *functional defect* that may cause system failure when executed. This separation is the conceptual hinge of the paper.

2. **A new evolvability defect taxonomy.** Three groups -- *documentation* (textual, supported-by-language), *visual representation* (indentation, blank lines, brackets, etc.), and *structure* (organization, solution approach) -- built bottom-up from labeling 563 evolvability defects. Inter-rater Kappa = 0.79 (very good agreement).

3. **A consolidated functional defect taxonomy.** Seven groups -- resource, check, interface, logic, timing, support, larger defects -- derived by reconciling seven prior classifications (Basili & Selby, Chillarege et al., Humphrey, Beizer, Kaner et al., IEEE, Grady) into one schema with explicit mappings (Table 12) and explicit exclusions (Table 13).

4. **Empirical replication of Siy & Votta on a second dataset.** Using two independent contexts (industrial C/C++, student Java) with different reviewers, languages, and codebases, the 75% evolvability finding is reproduced -- 77% (industrial) and 85% (student) once false positives are excluded.

5. **Role-based review proposal.** Drawing on the taxonomy, they sketch five reviewer roles -- documentation reviewer, code structure reviewer, solution approach reviewer, resource/interface reviewer, check/logic reviewer -- mapping each role to a defect class.

---

## Key Findings

### Distribution of code review findings

| Main Group | Industrial Reviews | Student Reviews |
|---|---|---|
| **Evolvability defects** | **276 (71.1%)** | **287 (77.4%)** |
| Functional defects | 83 (21.4%) | 49 (13.2%) |
| False positives | 29 (7.5%) | 35 (9.4%) |
| Total | 388 | 371 |

Excluding false positives: 77% (industrial) / 85% (student) of true defects are evolvability defects -- a 5:1 to 3:1 ratio of evolvability to functional defects.

### Distribution within evolvability defects

| Group | Industrial | Student |
|---|---|---|
| Documentation | 34.8% | 46.3% |
| Visual representation | 9.8% | 10.8% |
| **Structure** | **55.4%** | **43.9%** |

- Within documentation: naming dominates industrial (69.2%), comments dominate student (59.6%) -- likely because the company favored self-descriptive naming over commenting, while students used Java's JavaDoc system.
- Within structure: industrial reviewers found more "move functionality" and "change function" defects (design-level issues); students found more low-level statement issues and dead code.

### Cross-study comparison

Comparison against six other datasets (Siy & Votta, Chillarege, El Emam & Wieczorek, So et al., O'Neill) showed evolvability defects in the majority for 5 of 8 datasets and over half in 7 of 8. Only Chillarege's dataset showed the opposite (~17% evolvability) -- possibly due to misclassification of structural evolvability defects as functional.

### Repeatability

- Functional classification reused prior schemes shown to be repeatable.
- Evolvability classification: second author classified 95 defects independently; agreement = 82%, **Cohen's Kappa = 0.79** (very good).

---

## Suggestions & Future Directions

1. **Cross-context defect distribution studies.** Extend defect-type analysis to more organizations and review settings to see whether the 3:1-to-5:1 evolvability:functional ratio generalizes; only 17% of inspection-found defects ever propagate to user-visible failures (per Berling & Thelin), making this a question of practical importance.

2. **Quantify the impact of individual evolvability defects.** Move beyond aggregate productivity studies to longitudinal tracking of how specific evolvability defects affect comprehension and future development effort -- only one study (Tenny on commenting) compared structure vs. documentation directly.

3. **Reviewer-background effects.** Study how experience, training, and personal taste shape which evolvability defects get spotted -- a junior may miss semantic duplication entirely. This connects to whether capture-recapture estimation methods are usable for evolvability content.

4. **Defect-type studies for other QA methods.** Repeat the analysis for unit testing, acceptance testing, and other techniques to enable evidence-based selection of QA methods rather than choosing them by tradition.

### Practitioner implications the authors flag

- Code reviews are most valuable for **long-lifecycle products** (where evolvability cost compounds); product/service businesses benefit more than custom-project shops.
- Only ~10% of evolvability defects (the visual representation group) can be auto-detected by formatters/linters -- the majority require human judgment.
- Use the classification as a **baseline for checklists and coding standards**, not as an exhaustive ruleset to start from.
- Start checklist design with the three evolvability groups (documentation, visual representation, structure), then add functional groups by need.

### Stated limitations

- Researcher bias from a single primary coder (no triangulation between researchers).
- Industrial sample = 1 company, 6 teams; student sample = 23 groups -- improved over single-source prior studies but still narrow.
- Industrial reviewers' preparation time varied; some admitted to under-preparing.
- Students knew evolvability was a study topic, possibly biasing what they reported.
- Possible per-defect misclassification at category boundaries (functional vs. evolvability).

---

## Authors & Institutions

Mika V. Mäntylä, Casper Lassenius -- Software Business and Engineering Laboratory, Helsinki University of Technology (TKK), Finland. Published in *IEEE Transactions on Software Engineering*, Vol. 35, No. 3, May/June 2009.
