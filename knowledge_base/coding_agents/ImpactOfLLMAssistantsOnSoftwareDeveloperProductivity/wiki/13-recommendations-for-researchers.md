> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Recommendations for Researchers: Shared Measures and Future Directions
**In one sentence:** Researchers should adopt shared, validated evaluation frameworks, extend multidimensional SPACE coverage (especially Communication), account for confounders like expertise and task complexity, and run longitudinal, field, and team-based studies that triangulate quantitative and qualitative evidence.
## Key points
- Recommendation 1 calls for shared evaluation frameworks and validated instruments to enable comparability, plus longitudinal, field, and team-based studies of long-term outcomes.
- Future work should use standardized cognitive-load measures to reconcile inconsistent findings, and track productivity, code quality, and skill development over extended periods rather than single sessions.
- 90% of studies examine at least two SPACE dimensions (a positive multidimensional shift), but only 15% extend beyond three dimensions, leaving room for more complete evaluation.
- Satisfaction, Performance, and Efficiency are the most investigated SPACE dimensions, while Communication — especially human-human collaboration — remains the least investigated.
- Novices show higher immediate gains but greater over-reliance and long-term skill erosion, while experts achieve sustained efficiency through selective and critical use; LLMs do well on isolated well-defined tasks but validation overhead offsets speed gains in complex context-rich projects.
- Recommendation 3 requires modelling expertise, task complexity, and domain context as covariates, stratifying by novice versus expert, operationalizing complexity, documenting organizational context, and replicating across populations, tools, and contexts.
- The primary evidence base is 59% formative and 38% laboratory experiments (strong internal but limited ecological validity), lacks standardized metrics for code quality and cognitive load, and is temporally concentrated with 77% of included studies published in 2024.
---
## Recommendation 1: shared frameworks and long-term designs
> "Recommendation 1. Researchers should adopt shared evaluation frameworks and validated instruments that allow comparability. Future work should include longitudinal, field, and team-based studies that capture long-term outcomes."

Specific future directions listed:
- (i) employ standardized cognitive load measures to reconcile the current inconsistency in findings;
- (ii) track productivity, code quality, and skill development over extended periods rather than single sessions;
- (iii) conduct organizational case studies that capture real-world complexity;
- (iv) triangulate quantitative metrics with qualitative insights to elucidate the mechanisms underlying observed effects.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
## Productivity as multidimensional and context-sensitive
Existing work agrees developer productivity is "a multi-dimensional and context-sensitive construct [27]", magnified in LLM-assisted development. Evidence:
- 90% of studies examine at least two SPACE dimensions.
- Only 15% extend beyond three dimensions.
- Satisfaction, Performance, and Efficiency are the most frequently investigated dimensions.
- Communication remains underexplored, with human-human collaboration the least investigated communication sub-dimension — consistent with findings on LLM-assistant risks to collaboration.
- As LLMs advance in reasoning and multimodal understanding, future studies should examine how model-capability improvements reshape the balance between productivity, collaboration, and quality.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
## Recommendation 2: address underexplored SPACE dimensions
> "Recommendation 2. Researchers should continue advancing multidimensional evaluations of developer productivity by systematically addressing underexplored SPACE dimensions, particularly Communication and Collaboration. While Satisfaction, Performance, and Efficiency are frequently assessed, the human-human and human-agent interaction aspects remain limited. Future studies should incorporate richer measures of team dynamics and communication patterns to better understand how LLM-assistants affect collaborative workflows."

Priority areas:
- (i) effects of LLM adoption on pair programming and code review practices;
- (ii) developer well-being, occupational stress, and sustainable work practices;
- (iii) shifts in allocation of developer time across tasks following LLM adoption;
- (iv) development and validation of instruments specifically designed for LLM-assisted development contexts.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
## Confounding variables
Variations in reported productivity outcomes are attributed to confounders such as developer experience, task complexity, and domain context:
- Novices may show higher immediate gains but also greater over-reliance and long-term skill erosion [61, 69, 88].
- Expert developers often achieve sustained efficiency through selective and critical use [60, 63, 68].
- LLMs perform well on isolated, well-defined tasks but struggle in complex, context-rich projects where validation overhead offsets speed gains [58, 63].
- Laboratory-based studies have limited ecological validity; future research should explicitly model and report contextual variables for fairer comparisons and cumulative insight.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
## Recommendation 3: account for confounders systematically
> "Recommendation 3. Researchers should systematically account for confounding variables that influence productivity outcomes, including developer expertise, task complexity, and domain context. Study designs should incorporate these as covariates, ensuring that effects attributed to LLM-assistants reflect genuine productivity changes rather than contextual bias. Explicitly reporting these variables will strengthen cross-study comparability and help build a context-aware evidence base."

Essential practices:
- (i) stratifying analyses by experience level and reporting differential effects for novice versus expert developers;
- (ii) operationalizing task complexity along defined dimensions and examining its moderating role on LLM effectiveness;
- (iii) documenting organizational context to facilitate meta-analytic synthesis;
- (iv) conducting replication studies across diverse populations, tools, and contexts to establish boundary conditions.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
## Threats to validity (as appearing in this chunk)
- Study selection bias: exclusion of shorter papers, non-peer-reviewed work, and non-journal/conference publications; mitigated by collaboratively agreed criteria; difficulty isolating human-centered studies because search terms like "performance" or "efficiency" also retrieve technical LLM work; mitigated by three-author review of control papers, iterative validation of search strings using control articles (Zhang, Babar, and Tell [42]), and backward/forward snowballing.
- Bias and repeatability: open-ended questions risk subjective selection; mitigated by multi-step validation, one-author screening/extraction with co-author validation and protocol design, regular weekly meetings over 9 months, and conservative full-text screening with uncertain cases retained and independently reviewed by two senior co-authors.
- Classification rigor: mapping findings to SPACE required interpretive decisions since SPACE was not built for human-LLM collaboration; mitigated by adapting definitions from prior literature [19, 104] and collaborative coding discussions.
- Primary-evidence limits: 59% formative and 38% laboratory experiments (strong internal validity, weak ecological validity, reflecting isolated tasks); lack of standardized metrics for code quality (cyclomatic complexity, coverage, defect density, functional correctness) and cognitive load — diversity hinders comparability but supports triangulation; temporal concentration with search/extraction at end of 2024 and 77% of included studies published in the same year, requiring transparent replicable protocols and periodic updates.

**Covers:** Researcher recommendations, shared measures and future research directions (chunk 13)
