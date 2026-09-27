> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Methodology: Search and Selection
**In one sentence:** The review selects primary studies using three inclusion and five exclusion criteria applied to a 9,756-record search across six digital libraries, filtered through PRISMA screening to 39 included studies plus snowballing.
## Key points
- Three inclusion criteria require English-language, full-text-accessible papers from 2014 or later investigating AI/LLM effects on developer productivity.
- Five exclusion criteria remove out-of-scope (EC1), out-of-focus (EC2), non-peer-reviewed or secondary publication types (EC3), short papers under four pages (EC4), and inaccessible full texts (EC5).
- Six libraries were searched (ACM, IEEE Xplore, ScienceDirect, Web of Science, Scopus, SpringerLink) with title/abstract/keyword restriction and NEAR/5 proximity operators in IEEE Xplore, Web of Science, and Scopus only.
- The search string has three AND-joined segments (AI/LLM technology, software-developer actor, productivity concept), refined over five iterations until it retrieved all 17 control papers.
- Initial search yielded 9,756 records; after removing 803 duplicates, 8,953 were screened by title and abstract and 8,725 excluded, leaving 228 for full-text review.
- Full-text screening excluded 189 papers (EC2 out-of-focus largest at 128, EC1 15, EC3 27, EC4 11, EC5 3, ~IC1 5), leaving 39 studies, plus 5 from two weeks of forward/backward snowballing (44 evaluated, 5 excluded, 39 total included).
- Screening was conservative (unclear title/abstract cases advanced to full text): first author screened all records over 47 days in Rayyan with second/last-author validation across three consensus meetings, followed by a 10-week full-text phase with consultation on unclear cases.
---
## Inclusion criteria
- (+) IC1: "The paper investigates the effect of AI or LLMs on software developer productivity."
- (+) IC2: "The paper is in English."
- (+) IC3: "The paper has an accessible full text and was published in 2014 or later."
- Exclusion decisions per study are recorded in supplemental material [20].

**Covers:** Review protocol, search strings, inclusion/exclusion criteria, PRISMA selection process

## Exclusion criteria
- (–) EC1 (Out of Scope): "The paper does not focus on SE or does not explore the impact of AI or LLMs on software developer productivity."
- (–) EC2 (Out of Focus): "The paper mentions the impact of AI or LLM on software developer productivity without it being one of the topics of the study."
- (–) EC3 (Publication Type): secondary studies; work-in-progress, extended abstracts, posters, tool demos, editorials, or grey literature; books, theses, workshop, monographs, keynotes, panels, doctoral symposium, or any venues without formal peer review.
- (–) EC4 (Length): short publications with fewer than four pages.
- (–) EC5 (Accessibility): full text not accessible online (e.g., paywalls without institutional access, unavailable PDFs, inaccessible archives).

**Covers:** Review protocol, search strings, inclusion/exclusion criteria, PRISMA selection process

## Query formulation and refinement
- Followed Kitchenham and Charters guidelines; selected six libraries: ACM Digital Library, IEEE Xplore, ScienceDirect, Web of Science, SpringerLink, and Scopus.
- Rationale: overly broad queries return false positives and reduce precision, while narrow queries risk omitting relevant studies; terminology for AI/LLM in SE varies significantly.
- Iteratively refined candidate queries against control papers over five iterations; all authors held a consensus meeting on the final search string (Table 1), which retrieves all 17 control papers.
- Query structure: three segments joined by AND — (1) AI/LLM technology, (2) actor (software developers), (3) concept (productivity).
- Restricted searches to title, abstract, and keywords to improve precision; used proximity operators "NEAR/5" or "w/5" (terms within five words) only in IEEE Xplore, Web of Science, and Scopus, since ACM, Springer, and ScienceDirect do not support them.

**Covers:** Review protocol, search strings, inclusion/exclusion criteria, PRISMA selection process

## Primary study selection (PRISMA)
| Stage | n |
|---|---|
| Records identified from databases | 9,756 (ACM 4,044; IEEE Xplore 491; ScienceDirect 3,734; Web of Science 271; Scopus 836; Springer 380) |
| Duplicate records removed | 803 |
| Records screened by title and abstract | 8,953 |
| Records excluded at title/abstract | 8,725 |
| Records screened by full text | 228 |
| Records excluded at full text | 189 (EC1: 15; EC2: 128; EC3: 27; EC4: 11; EC5: 3; ~IC1: 5) |
| Records included | 39 |
| Additional records from forward/backward snowballing | 5 |
| Reports evaluated for quality assessment | 44 |
| Records excluded at quality stage | 5 |
| Total records included | 39 |

- Search restricted to publications from 2014 onward.
- Title/abstract screening by first author took 47 days using Rayyan to tag exclusions; second and last authors independently validated exclusions with three consensus meetings.
- Adopted a conservative approach: "records with insufficient information in the title and abstract to support a clear inclusion or exclusion decision were included in full-text review."
- Full-text screening took 10 weeks, led by the first author with second/last-author consultation on unclear cases; detailed rationale in supplemental material [20].
- Snowballing examined references and citations of the 39 selected studies over approximately two weeks, identifying five additional articles (44 primary studies before final quality exclusion).

**Covers:** Review protocol, search strings, inclusion/exclusion criteria, PRISMA selection process

## Quality assessment (introduced)
- Adopted the Lenarduzzi et al. strategy with 11 criteria (QA1–QA11) covering aims, methodology, data analysis rigor, and validity; details and scoring continue on the next page.
- Criteria listed: QA1 research-based vs. lessons-learned; QA2 clear aims; QA3 context description; QA4 appropriate design; QA5 appropriate recruitment; QA6 control group; QA7 data collection addressing the issue; QA8 rigorous analysis; QA9 researcher-participant relationship; QA10 clear findings; QA11 value for research or practice.

**Covers:** Review protocol, search strings, inclusion/exclusion criteria, PRISMA selection process
