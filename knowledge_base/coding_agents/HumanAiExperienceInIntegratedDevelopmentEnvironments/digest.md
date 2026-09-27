> [[index|Wiki]] | [[summary|Summary]]

# Human-AI Experience in Integrated Development Environments: A Systematic Literature Review — Digest

## 1. [[wiki/01-overview-abstract-introduction|Overview: Abstract and Introduction (in-IDE HAX)]]

**In one sentence:** This systematic literature review of 90 studies defines in-IDE Human-AI Experience (HAX) and organizes findings into Impact, Design, and Quality dimensions, reporting productivity gains alongside verification overhead, over-reliance, and code-quality risks.

- Reviews 90 relevant studies (from 257 identified) via a PRISMA-guided SLR combining database search, backward snowballing, and expert-informed additions, extending an earlier non-systematic survey of 36 papers (Sergeyuk et al., 2024).
- Frames in-IDE HAX as the shift from HCI to HAX where AI acts as an active collaborator rather than just a tool, focused on what happens where code is written, inspected, or tested rather than AI in software engineering broadly.
- Cites industry adoption pressure: 76% of respondents are using or planning to use AI tools (Stack Overflow, 2024), and more than 50% note reduced search time, faster coding, quicker repetitive tasks, and higher productivity (JetBrains, 2024).
- Impact dimension (74/90 studies): AI-assisted coding enhances productivity, especially among experienced users, but increases verification time and raises over-reliance concerns.
- Design dimension (28/90 studies): covers autocompletion, conversational, and emerging hybrid systems; prompt structure plus interface properties — context awareness, transparency/explanations, and user control — shape experience.
- Quality dimension (19/90 studies): evaluates correctness, maintainability, and security of generated code, often calling for improved validation and diagnostic support.
- Claims to be, to the best of the authors' knowledge, the first systematic review of in-IDE HAX, positioned as a foundational reference for cumulative and reproducible progress rather than a follow-up.
- Future agenda: larger and longer evaluations, stronger audit/verification assets, broader SDLC coverage (requirements, testing, deployment), longitudinal and comparative designs, and adaptive assistance under user control; gaps include non-users/stopped-users, educational contexts, AI governance, and proactivity.

## 2. [[wiki/02-research-questions-method-planning|Research Questions, Method, and Planning]]

**In one sentence:** The review follows PRISMA to answer three RQs on studied vs. under-explored HAX areas, key findings and themes, and future directions, using an Impact/Design/Quality taxonomy, 2022–2024 eligibility criteria, a 0–4 quality screen with cutoff >2, and eight digital libraries plus expert supplementation.

- The review follows the PRISMA framework (Moher et al., 2010) and is guided by three RQs: RQ1 on extensively studied vs. under-explored HAX/SDLC areas, RQ2 on key findings and methodological trends, and RQ3 on future research directions.
- RQ1 maps studies to Waterfall-model SDLC stages (Alshamrani and Bahattab, 2015), chosen for clear stage delineation, plus study contexts and three HAX aspects from Sergeyuk et al. (2024).
- The in-IDE HAX taxonomy has three dimensions — Impact (effects on developers, tasks, workflows), Design (AI integration and interaction in the IDE), and Quality (correctness, security, readability) — built by two-author open coding, codebook piloting, full coding, third-author adjudication, and consolidation of low-support categories.
- Eligibility requires 2022–2024 English studies on developers/users engaging AI tools in IDEs, investigating in-IDE HAX with empirical (qualitative, quantitative, or mixed-methods) findings; peer-reviewed venues plus relevant preprints and dissertations to counter positive-results bias; no comparison criterion.
- IDE is defined as a workspace offering (a) code editing, (b) immediate execution or preview, and (c) contextual AI feedback in the same window, including IntelliJ, VS Code, Jupyter, and Databricks plus qualifying plug-ins, while web explainers and offline static analysers are excluded.
- Quality screening scores Reporting, Rigor, Credibility, and Relevance at 0 / 0.5 / 1 with inclusion cutoff above 2, done independently by the second and third authors with first-author arbitration; at full-text stage 8 of 79 papers were excluded for scores ≤2.
- Search covered ACM Digital Library, DBLP, IEEE Digital Library, ISI Web of Science, ScienceDirect, Scopus, Springer Link, and arXiv in November 2024 with a two-part Score/Side query (full query in six libraries, Score-only in ACM and DBLP), supplemented by 35 studies from a prior survey and 30 expert-added studies, yielding 223 records entering screening with 30 duplicates removed and 114 excluded as out of scope.

## 3. [[wiki/03-search-screening-snowballing|Search Screening, Snowballing, and Data Extraction]]

**In one sentence:** Backward snowballing added 18 papers (with a second round adding none), revision re-verification settled the set at 90 papers dated by first public availability, and data extraction combined manual coding with Elicit-assisted summaries that were all cross-verified against originals.

- Backward snowballing (Wohlin, 2014) was run on papers deemed eligible: citations were screened against report-related criteria (Subsection 2.1), already-identified papers removed, and the remainder assessed against study-level inclusion criteria.
- The first snowballing round identified 18 new in-scope papers; a second round yielded zero additional relevant papers, and the 18 underwent the Subsection 2.3 eligibility assessment.
- During revision, re-verification removed 2 papers (one out-of-scope, one duplicate) and added 3 previously overlooked studies, yielding a final total of 90 included papers.
- Eligibility was determined by date of first public availability between January 2022 and November 2024, including arXiv preprints; studies later archived in 2025 are cited by archival DOI/venue year but remain in-window via preprint date.
- From all 90 papers the authors extracted Authors, Authors' Affiliation, DOI, Publication Date, Venue, Goal of the Study, Research Questions, Key Findings, Future Work (topic and methodology), Scope, and SDLC Stage, later adding a Context column (professional vs educational setting) plus a classification by investigated task types.
- Extraction was done manually by the first author with support from Elicit (https://elicit.com/), which formulated concise descriptions of each study's goal, key findings, and future work; all tool outputs were reviewed and cross-verified against originals and included only after confirming faithful representation.
- The full 90-study extraction table is in Supplementary materials (Sergeyuk et al., 2025), with a shortened overview presented as Table 1 (IDs 1–41 visible in this chunk).

## 4. [[wiki/04-included-studies-table|Included Studies Table (IDs 42–90) and Review Corpus]]

**In one sentence:** The chunk lists included studies ID 42–90 with titles and authors, reports a 90-study final corpus selected from 256 screened papers, and begins the Results by framing professional (71/90) versus educational (19/90) contexts.

- The table segment covers study IDs 42–66 (Vaithilingam et al. 2023 through Shlomov et al. 2024) and IDs 67–90 (Brown et al. 2024 through Zhou et al. 2025b).
- The review screened 256 papers total, assessed 100 for eligibility, and included 90 studies in the final review stage.
- The PRISMA-style flow reports 223 records screened, with 30 duplicates and 114 out-of-scope exclusions on one path, plus 2 duplicates and 10 out-of-scope exclusions on the other path.
- Full-text assessment split into 79 and 21 articles, with 8 and 2 full-text exclusions respectively, yielding 90 total included studies.
- Professional context accounts for 71/90 studies and educational context for 19/90 studies, with educational studies possibly underrepresented because students do not always work inside full IDEs.
- Within professional studies, coding is 17/71, maintenance is 8/71, requirements gathering is 1/71, and 46/71 do not specify a target SDLC stage.
- The expanded corpus "confirms the adequacy of the initial three-part framing (Sergeyuk et al., 2024) and adds finer subscopes within each dimension, but it does not introduce any new top-level dimensions."

## 5. [[wiki/05-study-contexts-sdlc-coverage|Study Contexts and SDLC Coverage (Fig. 2 / Fig. 3)]]

**In one sentence:** Professional studies dominate the corpus while educational studies focus on pedagogy with little SDLC-stage specificity, revealing gaps around non-users, practical-skill impacts, and SDLC contextualization.

- Educational studies in the chunk body total 16, of which 6/16 address coding, 1/16 addresses requirements formulation, and 13/16 do not specify an SDLC stage.
- The figure labels under extraction read "Fig. 3: Paper IDs by Context and SDLC stage" with an "SDLC Stage" axis and context rows for Educational and Professional (axis tick labels are garbled in extraction).
- Professional-row IDs visible in extraction include 56; 15, 34, 47, 3; 36, 16, 19, 90; 87, 54, 73, 31; 48, 55, 42, 50; 40; and 7, 63, 64, 3; 57, 4, 46, 14, with a "Total N: 46" label.
- Educational-row IDs visible in extraction include 25; 10, 32, 39, 88; 13; 40; and 11, 25, with total labels reading 13 and 40 in garbled layout.
- Verbatim: "Educational studies primarily focus on pedagogical insights. These studies often investigate how students use AI tools to learn programming or solve computational problems."
- Stated gap 1: "Lack of perspectives from people who do not use AI tools for development for a variety of reasons."
- Stated gap 2: "Limited number of educational studies highlighting the need for a deeper exploration of AI's impact on practical skills acquired during CS education, especially as developers constantly learn and re-learn programming practices in development environments."
- Stated gap 3: "Lack of specification of the SDLC stage, suggesting an opportunity for future research to contextualize AI tool usage across all stages of the SDLC."

## 6. [[wiki/06-tasks-across-years|Productivity Trade-offs, Attitude, and Design of In-IDE HAX]]

**In one sentence:** AI assistance in IDEs speeds work via fewer context switches and less boilerplate but adds up to 50% verification time, novices gain speed at the cost of over-reliance risk, trust (11/74 studies) is calibrated by suggestion quality and task stakes, and design research (28/90 studies) converges on hybrid autocompletion-plus-conversation with context awareness, explainability, and user control while Copilot dominates with 36/90 studies.

- Productivity gains are partially attributed to fewer context switches and reduced boilerplate, letting developers offload repetitive tasks and focus on higher-level logic, but gains are inconsistent for proprietary or highly complex logic where assistance struggles with context-specific nuances (Pandey et al., 2024; Khemka and Houck, 2024).
- Verifying suggestions, refining prompts, and reworking AI-generated code can take up to 50% of developers' time (Mozannar et al., 2024a), because output can be partially correct yet subtly flawed (Wermelinger, 2023), requiring stepwise review or re-prompting (Kazemitabaar et al., 2024a).
- Highlighting tokens by predicted edit likelihood improves speed and directs attention to problematic regions (Vasconcelos et al., 2025), mitigating "automation bias" — blindly accepting erroneous suggestions (Al Madi, 2022).
- Novices solve assignments quicker with AI help and report lower mental workload with steady self-efficacy under structured use (Puryear and Sprint, 2022; Rasnayaka et al., 2024; Tanay et al., 2024; Gardella et al., 2024; Kazemitabaar et al., 2023a), but can over-trust AI, lose foundational concepts, and drift from correct solutions when suggestions mislead (Prather et al., 2024; Zhou and Li, 2023).
- Attitude is studied in 11/74 studies with trust as the central construct: high-quality context-relevant suggestions raise trust while inconsistency and unnecessary complexity lower it, and trust drops for high-stakes/production, complex, or open-ended tasks but rises for routine or proof-of-concept work (Amoozadeh et al., 2024; Brown et al., 2024; Wang et al., 2024).
- Over-reliance (accepting without checking) skews toward novices who overestimate reliability, while under-reliance (rejecting correct output lacking rationale) appears among professionals; live environments surfacing runtime values support more calibrated acceptance (Al Madi, 2022; Sun et al., 2022; Ferdowsi et al., 2024).
- Design is studied in 28/90 works (22/28 on integration impact, 17 on design principles): autocompletion gives low-friction inline completions with minimal cognitive load while conversational agents support higher-level reasoning and iterative refinement, and studies advocate hybrid models combining both (Vaithilingam et al., 2023; Yen et al., 2023; Ross et al., 2023a; Robe and Kuttal, 2022; Gu et al., 2024; Weber et al., 2024).
- GitHub Copilot is the most studied tool at 36/90 works, creating overgeneralization risk, while alternatives include IDA, Prompt Sapper, CoLadder, PairBuddy, Slide4N, and RealHumanEval (Shlomov et al., 2024; Cheng et al., 2024b; Yen et al., 2023; Robe and Kuttal, 2022; Wang et al., 2023b; Mozannar et al., 2024c).

## 7. [[wiki/07-quality-dimension-findings|Investigating and Ensuring the Quality of AI-Assisted Code]]

**In one sentence:** Quality of AI-assisted code — examined in 19 of 90 papers across correctness, readability/maintainability, and security — trades development speed for risks of subtle errors, insecure patterns, and harder-to-maintain code, requiring verification, better prompting, personalisation, and developer training.

- 19 of 90 papers investigate quality of AI-assisted code generation, covering correctness, security, and readability.
- AI assistance accelerates workflows but increases susceptibility to subtle errors, security vulnerabilities, and reduced maintainability, with often syntactically valid yet logically flawed or non-idiomatic output.
- Readability suffers from overly concise structures, unconventional naming, and missing comments, threatening long-term maintainability in team workflows; AI refactoring and explanation tools are proposed mitigations.
- Up to 36% of vulnerabilities in AI-assisted code originate from the LLMs, reflecting replication of insecure training-data patterns and the need for cautious oversight.
- Quality depends on human/organisational factors — verification habits, prompting, and debugging strategies — so best practices extend to education, training, and workflow adaptation.
- Methodologies across the 90 papers: 12 survey, 32 experimental, 38 qualitative, plus 20 not fitting the dichotomy and mixed-methods user studies.
- Future-work analysis of 250 statements yields 17 topics and 10 methods; top topics are productivity (43), design of AI assistance (29), and audits of AI-generated code (28).

## 8. [[wiki/08-impact-design-findings|Future Work Directions: Audit, Personalization, Verification, and IDE Redesign]]

**In one sentence:** The reviewed papers propose larger and longer evaluations, stronger audit and verification assets, broader life-cycle coverage, and adaptive assistance that is explainable and under user control.

- Productivity proposals connect gains to interface and workflow choices, calling for concrete design changes and controls plus accounting for project and environment factors.
- Audit proposals seek wider security coverage over time: expanded vulnerability categories and language coverage, longitudinal tracking, targeted test suites and benchmarks, and more unit tests and quality metrics.
- Prompting proposals center on structured conversational prompting with refinement aids, comparative evaluation of prompt-engineering strategies, multi-modal channels, and prompt sanitization with privacy-aware feedback.
- Personalization proposals call for user models keyed to profile, expertise and task state, including frequency/snooze controls, adaptive strategies responding to real-time performance, and style- and context-matched results.
- Verification proposals concentrate on checking outputs before adoption via automatic test generation, reference-example retrieval, post-processing/filtering layers, and multi-alternative comparison interfaces.
- Explainability, trust, and control proposals ask for rationales and code-level explanations, studies of community trust recalibration and interface-driven trust shifts, and richer controls over generation and automation levels.
- IDE and life-cycle proposals argue for AI-aware environments (non-linear input, sketch merging, chat control, edit propagation, memory management and dynamic prompts) and tooling beyond implementation across requirements, design, debugging, testing, deployment, and search.

## 9. [[wiki/09-rq1-gaps-and-coverage|RQ1: Extensively Studied and Under-Explored Aspects of In-IDE HAX]]

**In one sentence:** Evidence is richest for professional coding and maintenance with growing task variety, but frequent omission of the SDLC stage plus a focus on adopters leaves early/late stages and non-adopters under-explored, so stage and task reporting must be standardized.

- The corpus splits into 71/90 professional-use papers and 19/90 educational-use papers, making professional settings the dominant evidence base.
- Within professional settings, most papers examine practical coding and maintenance work, while a large share evaluates assistance without situating it in a specific SDLC stage.
- Educational papers focus on learners using assistance to solve programming problems, but likewise often omit stage information, limiting comparison across contexts.
- Missing stage information weakens interpretability because the same interface may have different effects at requirements, implementation, testing, or evolution.
- Task design shifted over time from small algorithmic exercises resembling games and interview-style problems to project-level workflow analysis plus documentation, testing, debugging, and migration tasks.
- Broadening task scope improved ecological validity but increased the number of papers labelling the task as unspecified, so clearer descriptions and stable taxonomies are needed.
- Several papers frame AI assistance as pair programming with the system as collaborator, creating needs for model-interaction training and oversight in professional teams and control-preserving scaffolds for learners.

## 10. [[wiki/10-methodology-future-directions|Methodology, Validity, and Future Directions]]

**In one sentence:** Across 90 studies with a median of 17 participants, the review finds in-IDE HAX research underpowered and short-term, and recommends justified sample sizes, preregistration, open sharing, and industry collaboration alongside broader tool, lifecycle, and longitudinal coverage.

- Sample sizes are often underpowered and rarely justified, with a median of 17 participants across the corpus.
- HCI benchmarks cited (Caine, 2016): most common sample size 12 and median 18; in-person median 15, remote median 77 — many quantitative studies at these sizes will be underpowered and benefit from replication.
- Recommended rigor: a priori power analysis for confirmatory comparisons, saturation arguments for qualitative designs, and explicit reporting of recruitment constraints.
- Recommended openness: versioned repositories with study materials and data where feasible — codebooks, prompts, task descriptions, analysis scripts, deidentified datasets with metadata and data dictionary — plus preregistration, blinding, randomization when appropriate, and transparency checklists recording methodology, exclusion criteria, and data-sharing plans.
- Academic–industry collaboration is recommended to improve recruitment and enable longitudinal, ecologically valid evaluations, balancing industrial 1–2 month feedback horizons with academic standards.
- Research to date concentrates on a small set of tools (most often GitHub Copilot) and the implementation SDLC stage, leaving requirements, testing, and deployment underexplored; future work should diversify assistants, cover earlier and later lifecycle stages, and prioritize longitudinal and comparative designs.
- Review-level threats acknowledged: sampling bias (recall-oriented query biased toward professional contexts), temporal bias (2022–2024 window), source reliability (including non-peer-reviewed ArXiv papers), interpretation bias in categorizing a large corpus, and industry time-factor constraints on statistical significance.

## 11. [[wiki/11-references-a-l|References A–L: Caine (2016) to Mastropaolo (2023)]]

**In one sentence:** This chunk is the first third of the review's reference list, running alphabetically from Caine K (2016) to Mastropaolo et al. (2023) across pages 32–34 with no findings or argument of its own.

- The chunk contains only bibliographic entries, alphabetically ordered from Caine K (2016) through Mastropaolo et al. (2023), spanning review pages 32–34.
- The earliest entry is Centre for Reviews and Dissemination (UK) (1995) on the Database of Abstracts of Reviews of Effects (DARE), with URL and accessed date 2025-08-10.
- The latest-dated entries are He et al. (2025), Kazemitabaar et al. (2025), and Koohestani and Izadi (2025), with most entries dated 2022–2024.
- Kazemitabaar and co-authors are the most repeated author block in this segment, with five entries: 2023a, 2023b, 2024a, 2024b, and 2025.
- Kitchenham et al. contribute two methods entries: the 2009 systematic literature reviews in software engineering review and the 2010 tertiary study.
- The segment includes one non-paper entry: JetBrains (2024) The State of Developer Ecosystem 2024: AI Insights, with URL and accessed date 2025-08-10.
- Several entries carry verbatim garbled characters for diacritics or quotation marks (e.g. Kruse "Puhlf¨"urβ", Kuang "S¨"oderberg", Lau 'From"" ban it till we understand it""'), reproduced as-is from the chunk.

## 12. [[wiki/12-references-m-s|References M–S: McNutt to Wang (middle third of bibliography)]]

**In one sentence:** This chunk is a bibliography-only segment containing 47 reference entries running alphabetically from McNutt et al. (2023) to Wang et al. (2025), with no synthesis, findings, or argumentative prose.

- The chunk contains 47 bibliography entries and no substantive prose beyond the entries and running heads.
- Coverage runs alphabetically from "McNutt AM, Wang C, Deline RA, Drucker SM (2023)" to "Wang Z, Zhou Z, Song D, Huang Y, Chen S, Ma L, Zhang T (2025)".
- Publication years in the entries range from 2010 (Moher et al., PRISMA statement) to 2025 (Spiess et al.; Vasconcelos et al.; Wang Z et al.).
- The segment includes three Mozannar et al. (2024a/b/c) entries, two Prather et al. entries (2023, 2024), two Ross et al. entries (2023a/b), two Tian et al. entries (2023, 2024), two Vaithilingam et al. entries (2022, 2023), and three Wang entries (2022, 2023a/b, 2024) plus Wang Z et al. (2025).
- Two entries are self-references to the review itself and its data: Sergeyuk et al. (2024) literature review and Sergeyuk et al. (2025) Zenodo dataset (DOI 10.5281/zenodo.16877797, version v2).
- One entry is non-paper grey literature: "Stack Overflow (2024) 2024 Stack Overflow Developer Survey: AI" with URL https://survey.stackoverflow.co/2024/ai, accessed 2025-08-10.
- Page furniture shows the segment spans review pages 35–37 with running heads "in-IDE HAX: Literature Review" (pp. 35, 37) and "Agnia Sergeyuk et al." (p. 36).

## 13. [[wiki/13-references-w-z|References W–Z: Weber (2024) to Ziegler (2022)]]

**In one sentence:** This chunk is the final segment of the review's reference list, running alphabetically from Weber et al. (2024) to Ziegler et al. (2022) with no findings or argument of its own.

- The chunk contains only bibliographic entries, alphabetically ordered from Weber T, Brandmaier M, Schmidt A, Mayer S (2024) through Ziegler A et al. (2022), totalling 14 entries.
- The earliest entry is Wohlin C (2014) on snowballing guidelines, followed by Zhou Y et al. (2015) on quality assessment of systematic reviews.
- The latest-dated entries are the two Zhou X et al. (2025a, 2025b) papers on LLMs for vulnerability detection/repair and on AI pair programming problems.
- Ten of the 14 entries are dated 2022–2024, with three from 2022, four from 2023, and three from 2024.
- Zhou X / Liang P / Zhang B co-author blocks are the most repeated in this segment, appearing in Zhang et al. (2023) and both Zhou et al. (2025a, 2025b) entries.
- Two entries are arXiv preprints: Yen et al. (2023) arXiv:231008699 and Zhang et al. (2023) arXiv:230308733.
- The venues are conference-heavy (IUI, SIGCSE, EASE 18th and 19th, CHI 2024, CHI EA 2023, PROMISE 18th, DIS 2024, Machine Programming 6th), plus three journals: PACM HCI 8(EICS), ACM TOSEM 34(5), and J. Systems and Software 219:112204.

## The argument in five moves

1. In-IDE HAX is defined as AI acting as collaborator where code is written, inspected, or tested, and 90 PRISMA-selected studies are organized into Impact (74/90), Design (28/90), and Quality (19/90) dimensions.
2. Impact evidence shows productivity gains from fewer context switches and less boilerplate, offset by up to 50% verification time, trust calibrated by suggestion quality and task stakes, and novice over-reliance versus professional under-reliance.
3. Design evidence converges on hybrid autocompletion-plus-conversation shaped by context awareness, explainability, and user control, but the evidence base is skewed toward GitHub Copilot (36/90) and the implementation stage.
4. Quality evidence trades speed for subtle errors, insecure patterns (up to 36% of vulnerabilities from LLMs), and maintainability costs, mitigated by verification habits, prompting, personalisation, and tooling.
5. Coverage gaps (early/late SDLC stages, non-users, educational practical skills, missing stage/task reporting) plus underpowered short-term samples (median 17) motivate larger, longer, preregistered, industry-collaborative evaluations with stronger audit/verification assets and adaptive, explainable, user-controlled assistance.
