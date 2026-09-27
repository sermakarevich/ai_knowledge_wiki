> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Research Questions, Method, and Planning

**In one sentence:** The review follows PRISMA to answer three RQs on studied vs. under-explored HAX areas, key findings and themes, and future directions, using an Impact/Design/Quality taxonomy, 2022–2024 eligibility criteria, a 0–4 quality screen with cutoff >2, and eight digital libraries plus expert supplementation.

## Key points

- The review follows the PRISMA framework (Moher et al., 2010) and is guided by three RQs: RQ1 on extensively studied vs. under-explored HAX/SDLC areas, RQ2 on key findings and methodological trends, and RQ3 on future research directions.
- RQ1 maps studies to Waterfall-model SDLC stages (Alshamrani and Bahattab, 2015), chosen for clear stage delineation, plus study contexts and three HAX aspects from Sergeyuk et al. (2024).
- The in-IDE HAX taxonomy has three dimensions — Impact (effects on developers, tasks, workflows), Design (AI integration and interaction in the IDE), and Quality (correctness, security, readability) — built by two-author open coding, codebook piloting, full coding, third-author adjudication, and consolidation of low-support categories.
- Eligibility requires 2022–2024 English studies on developers/users engaging AI tools in IDEs, investigating in-IDE HAX with empirical (qualitative, quantitative, or mixed-methods) findings; peer-reviewed venues plus relevant preprints and dissertations to counter positive-results bias; no comparison criterion.
- IDE is defined as a workspace offering (a) code editing, (b) immediate execution or preview, and (c) contextual AI feedback in the same window, including IntelliJ, VS Code, Jupyter, and Databricks plus qualifying plug-ins, while web explainers and offline static analysers are excluded.
- Quality screening scores Reporting, Rigor, Credibility, and Relevance at 0 / 0.5 / 1 with inclusion cutoff above 2, done independently by the second and third authors with first-author arbitration; at full-text stage 8 of 79 papers were excluded for scores ≤2.
- Search covered ACM Digital Library, DBLP, IEEE Digital Library, ISI Web of Science, ScienceDirect, Scopus, Springer Link, and arXiv in November 2024 with a two-part Score/Side query (full query in six libraries, Score-only in ACM and DBLP), supplemented by 35 studies from a prior survey and 30 expert-added studies, yielding 223 records entering screening with 30 duplicates removed and 114 excluded as out of scope.

---

## Research questions

**Covers:** RQ definitions, p. 5

- "The following Research Questions (RQs) guided our literature review:"
- RQ 1: "What aspects of software development related to HAX within IDEs have been extensively studied, and which areas remain under-explored?" Method: "we defined the stages of SDLC according to the Waterfall model (Alshamrani and Bahattab, 2015)" because of "its clear delineation of development stages, which facilitated systematic categorization"; also examined "study contexts and three key aspects of HAX identified by a previous literature review (Sergeyuk et al., 2024)."
- RQ 2: "What are the key findings in the field of HAX in IDEs?" Method: "we systematically examined goals, research questions, and key findings from published reports" to "determine key research themes in the field and define methodological trends."
- RQ 3: "What are the potential directions for future research and development in the field of HAX in IDEs?" Method: "we analyzed the lists of future research directions proposed in the reviewed studies, identifying recurring themes and uncovering how studies build on each other's findings."

## In-IDE HAX taxonomy (for RQ1 and RQ2)

**Covers:** taxonomy construction, p. 5

- Applied "an in-IDE HAX taxonomy (Sergeyuk et al., 2024) developed through a staged qualitative procedure."
- Procedure: "Two authors independently conducted open coding of the corpus to propose candidate categories, followed by consensus meetings to merge or split codes, assign names, and draft a codebook with definitions and examples. The codebook was piloted on a subset, refined, and then used to code the full dataset by two authors, with disagreements adjudicated by a third. Categories with low support or conceptual overlap were consolidated to improve parsimony while preserving coverage."
- "The resulting structure comprises three distinct dimensions: Impact (effects on developers, tasks, and workflows), Design (how AI is integrated into and interacted with in the IDE), and Quality (properties of AI outputs such as correctness, security, and readability)."

## Planning: eligibility criteria

**Covers:** Section 2.1 Planning, p. 5–6

| Criterion | Rule stated in chunk |
|---|---|
| Timeframe | Studies published between 2022 and 2024, "to ensure relevance to the advancements in AI-driven IDE features" |
| Language | Only English |
| Publication status | Peer-reviewed journal articles and conference proceedings, plus "preprints and unpublished dissertations" if they "provided unique insights directly relevant to the research objectives" |
| Population | Computer-science studies "that focus on software developers or users engaging with AI-enhanced tools within IDEs" |
| Intervention | Studies "if they investigated in-IDE HAX" |
| Comparison | "Not applicable" |
| Outcomes | Studies "that presented empirical findings, whether qualitative, quantitative, or mixed-methods" |
| Study design | "Original empirical studies" |

- Preprint/dissertation rationale repeated: arXiv included "to capture insights from emerging fields"; preprints and dissertations reduce "the risk of excluding studies with negative or null findings" given "the prevalence of positive results in published literature."

## Planning: IDE definition

**Covers:** Section 2.1 Planning, p. 5–6

- Verbatim: "IDE in this review denotes any workspace that simultaneously offers (a) code editing, (b) immediate execution or preview, and (c) contextual AI feedback in the same window."
- Included: "Traditional desktop IDEs (IntelliJ, VS Code) and notebook-style environments (Jupyter, Databricks) satisfy all three criteria; plug-ins that embed a full editor and run code inline also qualify."
- Excluded: "Tools that push AI suggestions outside the primary editing surface (e.g., web explainers, offline static analysers) are excluded."

## Planning: quality assessment and extraction

**Covers:** Section 2.1 Planning, p. 6

- Four questions (inspired by Zhou et al., 2015):
  - Reporting: "Is there a clear statement of the aims of the research?"
  - Rigor: "Is the study design clearly defined?"
  - Credibility: "Is there a clear statement of findings related to the aims of research?"
  - Relevance: "Is the study of value for research or practice?"
- Scale: "0 — No, and not considered; 0.5 — Partially; 1 — Yes"; cutoff "higher than 2" for further inclusion.
- Extraction form fields: "authors names and affiliation, DOI, publication date, venue, goal of the study, research questions, key findings, future work, scope (based on the taxonomy defined in previous work (Sergeyuk et al., 2024)), and SDLC stage," plus report name.

## Planning: libraries searched

**Covers:** Section 2.1 Planning, p. 6

- Eight sources: "ACM Digital Library, DBLP, IEEE Digital Library, ISI Web of Science, ScienceDirect, Scopus, Springer Link, and arXiv."

## Identifying and screening (partial in this chunk)

**Covers:** Section 2.2 Identifying and Screening, pp. 6–7 (search date, query, supplementation, screening counts up to out-of-scope exclusion)

- Searched "In November 2024, after finishing the planning phase" over "titles, keywords, and abstracts"; strategy: "optimized for high recall at the search stage and enforced precision during manual screening."
- Query structure: "a core query covering terminology related to AI assistants and Human-AI Experience (Score), optionally combined with a query specifying IDE-related terms (Side)."
- Score terms: "AI Assistant" OR "AI Companion" OR "AI-Powered Programming Tool" OR "Code Completion Tool" OR "Coding Assistant" OR "Copilot" OR "Intelligent Code Assistant" OR "LLM-Based Coding Assistant" OR "LLM-Powered Coding Assistant" OR "LLM4Code" OR "Programming Assistant" OR "Human-AI Experience" OR "Human-AI Co-Creation" OR "Human-AI Collaboration" OR "Human-AI Interaction".
- Side terms: "Integrated Development Environment" OR "Code Editor" OR "Coding Environment" OR "Development Environment" OR "Programming Environment".
- Application: "The full query was used in IEEE Xplore, Web of Science, ScienceDirect, Scopus, Springer Link, and arXiv. In ACM Digital Library and DBLP, we used only Score due to limited filtering capabilities and higher baseline relevance."
- "We did not include 'developer' as a required keyword, since it tended to retrieve general developer studies and exclude relevant work focused on tools or interfaces that met our criteria but were not indexed using that term."
- Supplementation: "35 studies from our prior literature survey (Sergeyuk et al., 2024)" plus "30 relevant studies known to the authors through domain expertise," described as "frequently cited or influential in recent research but were missed due to inconsistent metadata, terminology drift, or indexing limitations"; justified as "recommended in SLR methodology (Wohlin, 2014; Kitchenham et al., 2009)"; all held to "the same quality assessment and eligibility criteria."
- Counts in this chunk: "In total, 223 papers entered the screening phase"; "excluded 30 duplicates"; "identifying 114 papers out of the scope of the current SLR" at initial screening, leaving 79 for eligibility (79 stated in Section 2.3).

## Assessing eligibility (partial in this chunk)

**Covers:** Section 2.3 Assessing Eligibility, p. 7 (quality screen of 79 full texts; snowballing header only)

- "we assessed the eligibility of 79 full-text articles based on their quality" on "Reporting, Rigor, Credibility, and Relevance"; "accepted only if their combined score on these criteria exceeded 2."
- "conducted independently by the second and third authors, followed by a discussion to reconcile any discrepancies. In cases of disagreement, the first author acted as an arbitrator."
- "A total of 8 papers were excluded due to insufficient quality scores lower or equal to 2, dictated by insufficient relevance and rigor."
- Chunk ends at the header "2.4 Backward Snowballing" with no body; snowballing details belong to chunk 03.

**Covers:** Chunk 02 body (pp. 5–7, through Section 2.3 and the header of 2.4); no snowballing or included-studies table in this chunk.
