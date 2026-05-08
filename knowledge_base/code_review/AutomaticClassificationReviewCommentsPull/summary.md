# Automatic Classification of Review Comments in Pull-based Development Model

**Paper:** [Automatic Classification of Review Comments in Pull-based Development Model (Zhixing Li, Yue Yu, Gang Yin, Tao Wang, Qiang Fan, Huaimin Wang, SEKE 2017)](https://doi.org/10.18293/SEKE2017-039)

## Human Readable TL;DR

When developers propose code changes on GitHub, other developers leave review comments -- some pointing out bugs, some approving, some asking questions, some just saying "great work." Normally a human has to read each comment to know what kind it is. This paper is like building a mail-sorting machine for those comments: the authors first drew a map of all possible comment types (11 types across 4 major groups), hand-labeled over 5,600 real comments, and then trained a classifier that sorts new comments automatically. The result is a machine that gets it right significantly more often than a simpler word-counting approach, saving reviewers and researchers from tedious manual triage.

## TL;DR

The paper constructs a two-level taxonomy for pull-request review comments with 4 top-level categories (Correctness, Decision, Management, Interaction) and 11 subcategories, derived via iterative open coding on three popular OSS GitHub projects (Rails, Elasticsearch, Angular.js). The authors manually label 5,645 review comments from 1,800 pull-requests and train a Two-Stage Hybrid Classifier (TSHC) combining rule-based inspection rules with SVM-based text classifiers plus structural metadata features. TSHC achieves weighted average F-measures of 0.780 (Rails), 0.820 (Elasticsearch), and 0.747 (Angular.js) -- improvements of 9.2%, 5.3%, and 7.2% over a text-only SVM baseline.

---

## Problem & Motivation

Pull-based development on platforms like GitHub relies heavily on review comments to gatekeep code quality, but these comments mix heterogeneous intents: code corrections, merge decisions, project management, and social interaction. Prior work studied review outcomes and latency but no study had systematically mapped what reviewers actually talk about, nor automated the identification of comment types. Without such a taxonomy, researchers cannot aggregate findings across studies, and tools cannot provide reviewers with context-aware assistance. The paper fills this gap by building both the taxonomy and a classifier grounded in it.

---

## Main Original Ideas

1. **Fine-grained two-level taxonomy for PR review comments.** The authors develop a 4-category, 11-subcategory taxonomy through an iterative open-coding process: random sampling from three OSS projects, descriptive labeling, bottom-up grouping, and validation by 10 additional participants. The taxonomy covers technical, managerial, and social dimensions -- broader than prior work that focused only on technical or non-technical splits.

2. **Two-Stage Hybrid Classification (TSHC).** Rather than relying on text alone, TSHC pipelines two stages: Stage One applies regex-based inspection rules and SVM text classifiers (TF-IDF features, Porter stemming, stop-word filtering, with reference texts normalized to tokens `cmmcode`, `cmmlink`, `cmmtalk`) to produce a possibility vector. Stage Two combines that vector with structural metadata features -- comment length, comment type (inline vs. issue), core-team authorship, link/ping/code/reference inclusion, and text similarity to PR title and PR description -- via a second-layer SVM. Multi-label output is supported: a comment can belong to multiple categories simultaneously.

3. **High-quality manually labeled dataset of 5,645 comments.** Sampled from 1,800 pull-requests (200 PRs per project per year, 2013--2015, comment count between 1 and 30), across Rails, Elasticsearch, and Angular.js, with labels validated by both authors plus 10 external participants. The dataset is publicly accessible for reuse.

4. **Inspection rule design per category.** For each of the 11 subcategories the authors manually craft regular expressions from discriminating phrases (e.g., "lgtm" / "looks good to me" for Approval; `cc:?|wdy|defer to|br\?` for Convention; blank/extra/line/space for Style). These rules give the classifier hard signal that pure ML misses on short texts.

---

## Key Findings

### Complete Two-Level Taxonomy (Table II)

| Level-1 | Level-2 | Description | Example comment |
|---|---|---|---|
| **Correctness** | Style | Points out extra blank lines, formatting issues, etc. | "scissors: this blank line" |
| **Correctness** | Functionality | Figures out functionality defect, etc. | "let's extract this into a constant. No need to initialize it on every call" |
| **Correctness** | Test | Demands submitter to provide test case, etc. | "this PR will need a unit test, I'm afraid, before it can be merged" |
| **Decision** | Approval | Approves of the pull-request | "PR looks good to me. Can you ..." |
| **Decision** | Disagreeing | Rejects to merge the pull-request, etc. | "I do not think this is a feature we'd like to accept." |
| **Decision** | Questioning | Asks for more use cases | "Can you provide a use case for this change?" |
| **Management** | Roadmap | States the development roadmap, etc. | "Closing as 3-2-stable is security fixes only now" |
| **Management** | Diversion | Assigns other reviewers | "/cc @fxn can you take a look please?" |
| **Management** | Convention | Asks for formulating commit messages, etc. | "Can you squash the two commits into one and also put [ci skip] in the commit message" |
| **Interaction** | Response | Thanks for what other people do, etc. | "Thank you. This feature was already proposed and it was rejected." |
| **Interaction** | Encouragement | Agrees with others' opinion, etc. | "+1: nice one @cristianbica" |

### Dataset Statistics (Table I)

| Project | Language | Domain | Stars | Forks | Contributors | Pull-requests | Total Comments |
|---|---|---|---|---|---|---|---|
| Rails | Ruby | Web Framework | 33,906 | 13,789 | 3,194 | 14,648 | 75,102 |
| Elasticsearch | Java | Search Server | 20,008 | 6,871 | 753 | 6,315 | 38,930 |
| Angular.js | JavaScript | Front-end Framework | 54,231 | 26,930 | 1,557 | 6,376 | 33,335 |

Labeled sample: 1,800 pull-requests, **5,645 review comments**, sampled 200 PRs/project/year over 2013--2015.

### Classifier Performance -- Weighted Average F-measure

| Project | TBC baseline | TSHC (proposed) | Improvement |
|---|---|---|---|
| Rails | 0.688 | **0.780** | +9.2% |
| Elasticsearch | 0.767 | **0.820** | +5.3% |
| Angular.js | 0.675 | **0.747** | +7.2% |

Evaluation: 10-fold cross-validation. Baseline (TBC) uses the same preprocessing and SVM but no metadata features and no inspection rules.

### Per-Category F-measure, TSHC (Table IV)

| Category | Rails | Elasticsearch | Angular.js |
|---|---|---|---|
| Style | 0.78 | 0.61 | 0.77 |
| Functionality | 0.79 | 0.80 | 0.70 |
| Test | 0.76 | 0.56 | 0.75 |
| Approval | 0.68 | 0.88 | 0.82 |
| Disagreeing | 0.53 | 0.80 | 0.56 |
| Questioning | 0.48 | 0.26 | 0.48 |
| Roadmap | 0.76 | 0.72 | 0.74 |
| Diversion | 0.88 | 0.89 | 0.82 |
| Convention | 0.99 | 0.93 | 0.94 |
| Response | 0.88 | 0.88 | 0.85 |
| Encouragement | 0.88 | 0.92 | 0.95 |
| **AVG** | **0.780** | **0.820** | **0.747** |

Convention, Encouragement, and Diversion are consistently the easiest to classify due to distinctive vocabulary and regex-matchable patterns. Questioning and Disagreeing are the hardest -- they lack discriminating terms and overlap surface-form with Functionality comments.

### Qualitative error analysis

A representative misclassification: a Disagreeing comment about a missing npm dependency was labeled Functionality by TSHC because the rejection phrasing had no matching inspection rule and the text resembled a code-level concern. Adding `Comment_type` and `Code_inclusion` features in Stage 2 partially mitigates this but does not fully resolve it, motivating the authors' planned sentiment analysis extension.

---

## Suggestions & Future Directions

1. **Expand the labeled dataset.** The 5,645-comment sample is sufficient for a proof of concept but limiting for rare categories such as Disagreeing and Questioning. More labeled data per class would improve performance where F-measure is currently lowest (~0.26--0.56).

2. **Introduce sentiment analysis.** Disagreeing and Approval comments are semantically close in surface form but differ in polarity. The authors explicitly flag sentiment features as the next planned addition to disambiguate them.

3. **Improve reviewer recommendation and PR prioritization.** Category labels from TSHC can feed downstream tools: routing Disagreeing comments to senior reviewers, or escalating PRs with many Questioning comments to project leads.

4. **Extend to other platforms and project types.** The three projects are all large, mature, high-star OSS repositories. Generalizability to smaller projects or enterprise-internal codebases is untested.

5. **Model label correlation for multi-label output.** A single comment can belong to multiple categories simultaneously. Independent one-vs-all SVMs ignore label co-occurrence; structured or probabilistic multi-label models could improve joint classification.

---

## Authors & Institutions

Zhixing Li, Yue Yu (corresponding author), Gang Yin, Tao Wang, Qiang Fan, Huaimin Wang -- College of Computer, National University of Defense Technology, Changsha, 410073, China. Published at SEKE 2017 (29th International Conference on Software Engineering and Knowledge Engineering), DOI: 10.18293/SEKE2017-039.
