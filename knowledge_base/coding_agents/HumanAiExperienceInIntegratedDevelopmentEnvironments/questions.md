---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Human-AI Experience in Integrated Development Environments: A Systematic Literature Review

### Q1. What is in-IDE HAX and how does the review organize its findings?

> [!tip]- Answer
> > In-IDE Human-AI Experience is the shift from HCI to HAX where AI acts as an active collaborator where code is written, inspected, or tested, rather than just a tool for software engineering broadly. The review of 90 studies organizes findings into Impact (74/90: productivity gains plus verification overhead and over-reliance), Design (28/90: autocompletion, conversational, and hybrid systems shaped by context awareness, transparency, and user control), and Quality (19/90: correctness, maintainability, security). It claims to be the first systematic review of in-IDE HAX, extending an earlier non-systematic survey of 36 papers. See [[wiki/01-overview-abstract-introduction|Overview: Abstract and Introduction]].

### Q2. What are the review's three research questions, taxonomy, and eligibility rules?

> [!tip]- Answer
> > RQ1 asks which HAX/SDLC areas are well-studied versus under-explored (mapping to Waterfall stages), RQ2 asks for key findings and methodological trends, and RQ3 asks for future research directions. The in-IDE HAX taxonomy has three dimensions — Impact (effects on developers, tasks, workflows), Design (AI integration and interaction), and Quality (correctness, security, readability) — built by two-author open coding, codebook piloting, full coding, and third-author adjudication. Eligibility requires 2022–2024 English empirical studies of developers using AI in IDEs (peer-reviewed plus relevant preprints/dissertations), an IDE defined by code editing plus immediate execution/preview plus contextual AI feedback in one window, and a quality-screen score above 2 on Reporting, Rigor, Credibility, and Relevance. See [[wiki/02-research-questions-method-planning|Research Questions, Method, and Planning]].

### Q3. How did backward snowballing, revision re-verification, and data extraction work?

> [!tip]- Answer
> > Backward snowballing on eligible papers screened citations against Subsection 2.1 criteria, removed already-identified papers, and assessed the rest for inclusion: the first round added 18 papers and the second round added none, with the 18 then quality-assessed per Subsection 2.3. During revision, re-verification removed 2 papers (one out-of-scope, one duplicate) and added 3 overlooked studies for a final total of 90, dated by first public availability between January 2022 and November 2024. Extraction was done manually by the first author with Elicit-assisted summaries of each study's goal, findings, and future work, all cross-verified against originals, with the full 90-study table in supplementary materials. See [[wiki/03-search-screening-snowballing|Search Screening, Snowballing, and Data Extraction]].

### Q4. What does the included-studies table show about the final 90-study corpus?

> [!tip]- Answer
> > The table lists studies ID 42–90 by title and authors (42–66 from Vaithilingam et al. 2023 to Shlomov et al. 2024; 67–90 from Brown et al. 2024 to Zhou et al. 2025b), with the PRISMA-style flow screening 256 papers, assessing 100 for eligibility, and including 90. The corpus splits into 71/90 professional-context and 19/90 educational-context studies, with professional work concentrated on coding (17/71) and maintenance (8/71) while 46/71 specify no SDLC stage. The expanded corpus confirms the initial three-part framing and adds finer subscopes without new top-level dimensions. See [[wiki/04-included-studies-table|Included Studies Table and Review Corpus]].

### Q5. How do study contexts and SDLC coverage break down, and what gaps follow?

> [!tip]- Answer
> > Professional studies dominate while educational studies focus on pedagogical insights such as students using AI to learn programming or solve computational problems, with most educational studies (13/16 in the chunk body) omitting the SDLC stage. The stated gaps are the lack of perspectives from non-users of AI tools, too few educational studies on AI's impact on practical skills acquired during CS education, and widespread omission of the SDLC stage. The remedy is future research that contextualizes AI tool usage across all SDLC stages. See [[wiki/05-study-contexts-sdlc-coverage|Study Contexts and SDLC Coverage]].

### Q6. What is the productivity trade-off of in-IDE AI assistance, including for novices?

> [!tip]- Answer
> > Assistance speeds work via fewer context switches and less boilerplate, letting developers offload repetitive tasks, but gains are inconsistent for proprietary or highly complex logic; verifying suggestions, refining prompts, and reworking output can take up to 50% of developers' time because output is often partially correct yet subtly flawed. Highlighting tokens by predicted edit likelihood speeds review and mitigates automation bias (blindly accepting erroneous suggestions). Novices solve assignments faster with lower mental workload under structured use, but risk over-trust, loss of foundational concepts, and drifting from correct solutions when misled. See [[wiki/06-tasks-across-years|Productivity Trade-offs, Attitude, and Design]].

### Q7. What shapes trust and reliance, and what design direction does the evidence support?

> [!tip]- Answer
> > Attitude is studied in 11/74 papers with trust as the central construct: high-quality context-relevant suggestions raise trust while inconsistency and complexity lower it, and trust drops for high-stakes, production, complex, or open-ended tasks but rises for routine or proof-of-concept work. Over-reliance (accepting without checking) skews toward novices who overestimate reliability, while professionals sometimes under-rely by rejecting correct output lacking rationale, with live programming surfacing runtime values aiding calibration. Design research (28/90) treats autocompletion (low-friction inline) and conversational agents (higher-level reasoning) as complementary and advocates hybrids, grounded in context awareness, explainability/transparency, and user control — though GitHub Copilot dominates at 36/90 studies, risking overgeneralization. See [[wiki/06-tasks-across-years|Productivity Trade-offs, Attitude, and Design]].

### Q8. What does the Quality dimension find about AI-assisted code?

> [!tip]- Answer
> > Quality is examined in 19/90 papers across correctness, readability/maintainability, and security: assistance accelerates workflows but yields syntactically valid yet logically flawed, non-idiomatic output with overly concise structures, unconventional naming, and missing comments that threaten team maintainability. Up to 36% of vulnerabilities in AI-assisted code originate from the LLMs, reflecting insecure training-data patterns that demand cautious oversight. Remedies include verification habits, better prompting (docstrings, function names), filtering and personalisation of suggestions, plus education, training, and workflow adaptation. See [[wiki/07-quality-dimension-findings|Investigating and Ensuring the Quality of AI-Assisted Code]].

### Q9. What future-work directions do the reviewed papers propose?

> [!tip]- Answer
> > Proposals call for larger and longer evaluations linking productivity to interface and workflow choices, stronger audit assets (expanded vulnerability and language coverage, longitudinal tracking, targeted test suites and benchmarks), and verification support such as automatic test generation, reference-example retrieval, and post-processing/filtering layers. They also request structured conversational prompting with refinement aids, personalization keyed to profile and expertise, explainability via rationales and code-level explanations, and AI-aware IDE redesign (non-linear input, chat control, edit propagation, memory management) extended beyond implementation to requirements, testing, and deployment. Less frequent themes include mental models, proactivity, user control, and governance. See [[wiki/08-impact-design-findings|Future Work Directions: Audit, Personalization, Verification, and IDE Redesign]].

### Q10. What does RQ1 conclude about studied versus under-explored areas?

> [!tip]- Answer
> > Evidence is richest for professional coding and maintenance (71/90 professional versus 19/90 educational papers), with task design shifting from small algorithmic exercises to project-level workflows plus documentation, testing, debugging, and migration tasks. However, frequent omission of the SDLC stage weakens interpretability since the same interface may behave differently at requirements, implementation, testing, or evolution, and the focus on adopters leaves non-adopters unexplored. The prescription is to standardize stage and task reporting, include non-adopters, and expand coverage to early and late lifecycle stages. See [[wiki/09-rq1-gaps-and-coverage|RQ1: Extensively Studied and Under-Explored Aspects]].

### Q11. What are the review's methodological findings, validity threats, and rigor recommendations?

> [!tip]- Answer
> > Across 90 studies the median sample is 17 participants, so many quantitative studies are underpowered and rarely justify their size; the review recommends a priori power analysis, saturation arguments for qualitative work, preregistration, blinding, randomization where appropriate, versioned open repositories, and academic–industry collaboration for larger longitudinal evaluations. Acknowledged review-level threats include sampling bias toward professional contexts, temporal bias from the 2022–2024 window, source-reliability concerns from including non-peer-reviewed arXiv papers, interpretation bias in categorizing a large corpus, and industry 1–2 month feedback horizons constraining statistical significance. Core takeaways include treating verification as a main interaction element, designing hybrid autocompletion-plus-conversation with context sharing and scope controls, and staging educational AI contribution with stepwise reveal and quick checks. See [[wiki/10-methodology-future-directions|Methodology, Validity, and Future Directions]].

### Q12. What does the References A–L page contain?

> [!tip]- Answer
> > It is a bibliography-only segment with no findings or argument, running alphabetically from Caine K (2016) to Mastropaolo et al. (2023) across review pages 32–34. The earliest entry is the 1995 Centre for Reviews and Dissemination DARE database, the latest-dated are He et al. (2025), Kazemitabaar et al. (2025), and Koohestani and Izadi (2025), with Kazemitabaar as the most repeated author block (five entries) and one grey-literature entry in JetBrains (2024). See [[wiki/11-references-a-l|References A–L: Caine to Mastropaolo]].

### Q13. What does the References M–S page contain?

> [!tip]- Answer
> > It is a bibliography-only segment of 47 entries running alphabetically from McNutt et al. (2023) to Wang et al. (2025), spanning review pages 35–37 with no synthesis or argumentative prose. It includes three Mozannar et al. (2024a/b/c) entries, two self-references (Sergeyuk et al. 2024 review and the Sergeyuk et al. 2025 Zenodo dataset, DOI 10.5281/zenodo.16877797 v2), and one grey-literature entry in the Stack Overflow (2024) Developer Survey on AI. See [[wiki/12-references-m-s|References M–S: McNutt to Wang]].

### Q14. What does the References W–Z page contain?

> [!tip]- Answer
> > It is the final bibliography-only segment of 14 entries running alphabetically from Weber et al. (2024) to Ziegler et al. (2022), with no findings of its own. Ten of the 14 entries date from 2022–2024, the earliest is Wohlin (2014) on snowballing guidelines, the latest are the two Zhou X et al. (2025a, 2025b) papers, and venues are conference-heavy plus three journals (PACM HCI, ACM TOSEM, J. Systems and Software). See [[wiki/13-references-w-z|References W–Z: Weber to Ziegler]].

### Q15. Should a professional team adopt in-IDE AI assistance as a hybrid system with enforced verification, given this review?

> [!tip]- Answer
> > Yes: adopt a hybrid of autocompletion plus conversational support with context sharing, brief explanations, and scope controls, since that is the review's convergent design recommendation, but make verification a first-class step with tests, static analysis, and runtime evidence kept inside the editor. This pairing is warranted because gains come with up to 50% verification time, subtle correctness and security risks, and novice over-reliance versus professional under-reliance. Report the SDLC stage, diversify beyond a single assistant, and track acceptance, edits, and verification effort rather than time-on-task alone. See [[wiki/10-methodology-future-directions|Methodology, Validity, and Future Directions]].
