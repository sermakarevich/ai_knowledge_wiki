> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Contributions

**In one sentence:** This systematic review and mapping of 39 peer-reviewed studies (January 2014–December 2024) finds LLM-assistants mostly benefit developer productivity but carry critical risks, with code-quality effects unresolved and most studies exploratory and multi-dimensional but narrow in scope.

## Key points

- The review synthesizes 39 peer-reviewed studies published between January 2014 and December 2024 on LLM-assistants and developer productivity.
- Commonly reported gains are accelerated development, minimized code search, and automation of trivial and repetitive tasks.
- Commonly reported risks are cognitive offloading and reduced team collaboration.
- Whether LLM-assistants improve or degrade code quality remains unresolved, with contradictory outcomes contingent on context and evaluation criteria.
- 90% of studies examine at least two SPACE dimensions, but only 15% extend beyond three dimensions.
- Satisfaction, Performance, and Efficiency are the most investigated SPACE dimensions; Communication and Activity remain underexplored.
- Most studies are exploratory (59%) and methodologically diverse, but lack longitudinal and team-based evaluations.

---

## Abstract findings

**Covers:** Title, abstract (arXiv:2507.03156v3 [cs.SE] 31 Jul 2026)

Large language model assistants (LLM-assistants) present new opportunities to transform software development, with developers increasingly adopting them across coding, testing, debugging, documentation, and design. The majority of the 39 studies report considerable benefits, though a notable subset identifies critical risks. Artifacts are publicly available at https://zenodo.org/records/18489222.

| Claim | Detail from chunk |
|---|---|
| Scope | 39 peer-reviewed studies, January 2014–December 2024 |
| Benefits | Accelerated development, minimized code search, automation of trivial and repetitive tasks |
| Risks | Cognitive offloading, reduced team collaboration |
| Code quality | Unresolved; contradictory outcomes contingent on context and evaluation criteria |
| SPACE coverage | 90% examine ≥2 dimensions; only 15% extend beyond three dimensions |
| Most studied dimensions | Satisfaction, Performance, Efficiency |
| Least studied dimensions | Communication, Activity |
| Study character | 59% exploratory; methodologically diverse; lack longitudinal and team-based evaluations |

ACM Reference Format: Amr Mohamed, Maram Assi, and Mariam Guizani. 2026. The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study. ACM Trans. Softw. Eng. Methodol. 1, 1 (January 2026), 42 pages. https://doi.org/10.1145/3809494

## Introduction: LLM-assistants and AI pair programming

**Covers:** Section 1 Introduction (pp. 1–2)

The chunk defines LLM-assistants as "generative AI tools powered by LLMs that support software development tasks." Examples given:

- OpenAI's GPT-series (e.g., GPT-4) and GitHub Copilot
- ChatGPT (public release late 2022), plus Cursor, Windsurf, and Bolt

Supported tasks listed: code generation and completion, code translation, debugging and maintenance, documentation, and system design. These tools support "a new development paradigm often referred to as AI pair programming, in which developers interactively engage with LLM-assistants throughout the software development process."

Developer productivity is framed as "a multifaceted construct that encompasses not only the efficiency and quality of software production but also the satisfaction, collaboration, and cognitive load experienced by a developer." Early measurement relied on "quantifiable outputs such as lines of code (LOC) or development velocity," while recent research emphasizes "human-centered factors such as communication, satisfaction, and well-being."

## Contributions

**Covers:** Section 1 contribution list

The paper claims the following contributions:

- "We present the first systematic review and mapping of the literature focused on the impact of LLM-assistants on software developer productivity, synthesizing evidence from 39 peer-reviewed primary studies published between 2014 and December 2024."
- "We provide a structured characterization of the methodological strategies and evaluation practices used to assess developer productivity, and synthesize the reported effects of LLM-assistants, surfacing key benefits (e.g., reduced task initiation overhead, support for code-adjacent tasks) and risks (e.g., over-reliance, flow disruption)."
- "We analyze our findings through the lens of the SPACE framework and employ McLuhan's Tetrad framework in our discussion to reflect on broader socio-technical implications."
- "We offer actionable recommendations for practitioners and researchers, and release a publicly available replication package containing all study data, selection decisions, and exclusion rationales to support transparency and reproducibility."

## Paper structure

**Covers:** Section 1 roadmap

- Section 2: background on software developer productivity
- Section 3: methodology (search strategies, selection criteria, data extraction)
- Sections 4–7: each research question separately
- Section 8: implications, practitioner recommendations, future research
- Section 9: threats to validity
- Section 10: conclusion

**Covers:** Title/abstract + Section 1 Introduction through Section 2 opening (Brooks reference)
