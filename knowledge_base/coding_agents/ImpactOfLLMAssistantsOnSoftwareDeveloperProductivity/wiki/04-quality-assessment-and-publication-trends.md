> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Quality Assessment and Publication Trends
**In one sentence:** After scoring each study on a five-point Likert scale and excluding 5 studies below a 50% quality threshold to leave 39 primary studies, the review finds a ChatGPT-driven surge peaking in 2024 (77% of studies) synthesized via Kitchenham-guided qualitative thematic analysis.
## Key points
- Each quality criterion was graded Excellent (4), Very Good (3), Good (2), Fair (1), Poor (0), with detailed scores in the supplemental appendix.
- Studies failing a minimum 50% average-score threshold were excluded: 5 excluded, leaving a final set of 39 primary studies.
- The majority of studies were rated above 3, with full quality-assessment results in the replication package material.
- Synthesis of RQ findings took three months using qualitative synthesis consistent with Kitchenham's guidelines, with initial plus three targeted thematic iterations (RQ1 methods, RQ2 benefits/risks, RQ3 SPACE mapping).
- Only four included studies were published between 2014 and 2022; interest rose in 2022 with ChatGPT's release and peaked in 2024 with 77% of all included studies.
- Of 154 authors, 147 have one publication, 6 have two, and Igor Steinmacher has three — reflecting a new topic just building momentum.
- By venue focus, 46% are Software Engineering and Computer Science, 18% (7 of 39) Human-Computer Interaction, plus 13% Information Systems and Decision Science, 10% Human-Aspects and Socio-Economic Impact, 8% AI for Software Engineering, and 5% Software Engineering Education.
- The most evaluated tools are ChatGPT (15 studies) and GitHub Copilot (14 studies), followed by Tabnine (3), GPT-4 (3), CodeWhisperer (3), and GPT-3.5 (2), with all others used once.
---
## Quality assessment scoring
**Covers:** quality-assessment scoring and threshold (Section 3.3 tail)

Following the scoring procedure proposed in [48], "each criterion was graded on a five-point Likert scale: Excellent (4), Very Good (3), Good (2), Fair (1), and Poor (0)."

| Detail | Value |
|---|---|
| Scale | Excellent (4), Very Good (3), Good (2), Fair (1), Poor (0) |
| Minimum quality threshold | 50% average score [49] |
| Excluded | 5 studies |
| Final set | 39 primary studies |
| Overall rating | "The majority of the studies were rated above 3." |

"The detailed quality scores for each primary study are provided in the supplemental appendix [20]" and "Detailed results of the quality assessment are available in the replication package material [20]."

## Data extraction and synthesis
**Covers:** Section 3.4 Data Extraction and Synthesis

"In the final stage of the review process, the synthesis of findings for RQs across these studies were conducted over a period of three months." The authors "followed a qualitative synthesis approach, consistent with Kitchenham's guidelines [40]."

Process as stated:
- "first perform an initial thematic analysis iteration over all primary studies to extract relevant data (e.g., study goals, tools, empirical strategy and design, tasks, settings, and key results)"
- "In parallel, for each study, we write a descriptive summary."
- "Then we follow up with three targeted iterations to capture methodological details (RQ1), synthesize benefits and risks (RQ2), and map studies to the SPACE framework (RQ3)."
- "After themes were consolidated, the first and last authors jointly validated the synthesized findings by cross-checking citations against the original text to ensure accuracy and traceability."

## RQ0: Publication years
**Covers:** Section 4 RQ0 stem + Section 4.1 Publication years (Fig. 2)

RQ0: "What are the characteristics of peer-reviewed studies that investigate the impact of LLM-assistants on software developer productivity?"

- "Although we included studies published more than ten years preceding our review, only four were published between 2014 and 2022 [50, 51, 52, 53]."
- "Research interest began to rise in 2022, which coincides with the release of ChatGPT."
- "This culminated in a sharp peak in 2024, which accounts for 77% of all included studies, likely due to increased accessibility and interest following ChatGPT's release."
- Fig. 2 "Publication frequency per year" shows year axis 2014–2025-Jan with counts including 33, 30, 22 visible in the extracted figure text.

## Author distributions
**Covers:** Section 4.2 Author distributions

"We investigate the distribution of papers per author across the 154 authors of primary studies."

| Authors | Publications each |
|---|---|
| 147 | 1 publication |
| 6 | 2 papers |
| 1 (Igor Steinmacher, most prolific) | 3 publications |

"This distribution is probably due to the fact that the investigation of the impact of LLM-assistants on software developer is a relatively new topic that is just starting to build momentum."

## Publication venues
**Covers:** Section 4.3 Publication venues (Table 3)

"We extract the publication venue for each primary study. Table 3 shows the venues categorized by research focus."

| Research focus | Share |
|---|---|
| Software Engineering and Computer Science (PACMSE, TOSEM, ICSE, ICSE-SEIP, FSE, PLDI, ASE, QRS-C, Science of Computer Programming, EASE, ENASE) | 46% |
| Human-Computer Interaction (CHI, IUI, CSCW, TOCHI, Topics in Cognitive Science) | 18% (7 out of 39) |
| Information Systems and Decision Science (JDS, AMCIS, ISEC, DASA, HICSS) | 13% |
| Human-Aspects and Socio-Economic Impact (Futures, Structural Change and Economic Dynamics, CHASE, SAICSIT) | 10% |
| AI for Software / AI Engineering (AI Engineering IEEE/ACM, AIware, GAIIS) | 8% |
| Software Engineering Education (ITiCSE, ICSE-SEET) | 5% |

"The variety of publication venues highlights the breadth and depth of the topic under study. The integration of LLM-assistants into the software development workflow introduces important considerations related to usability, automation, interaction design, and developer behavior."

## Most frequently used LLM tools
**Covers:** Section 4.4 Most frequently used LLM tools (Table 4)

"Table 4 summarizes all LLM-assistants used across the primary studies. The most frequently evaluated tools are ChatGPT (15 studies), Github Copilot (14 studies) and followed by Tabnine (3 studies), GPT-4 (3 studies), CodeWhisperer (3 studies) and GPT-3.5 (2 studies). All Other tools were used only once, such as Claude, and Codex."

| Tool | Count | Primary studies |
|---|---|---|
| ChatGPT | 15 | [56, 57, 60, 62, 63, 64, 68, 69, 70, 77, 78, 82, 83, 85, 88] |
| GitHub Copilot | 14 | [59, 60, 63, 64, 65, 71, 73, 76, 78, 79, 82, 83, 85, 87] |
| Tabnine | 3 | [59, 60, 64] |
| GPT-4 | 3 | [61, 70, 78] |
| CodeWhisperer | 3 | [59, 60, 63] |
| GPT-3.5 | 2 | [70, 73] |
| Claude | 1 | [64] |
| Codex | 1 | [74] |
| Gemini | 1 | [64] |
| GPT-3 | 1 | [67] |
| Ansible Lightspeed | 1 | [66] |
| Bard | 1 | [72] |
| CodeGen2 (7B) | 1 | [59] |
| GILT | 1 | [62] |
| Internal tool: CodeCompose | 1 | [54] |
| NL2Code PyCharm plugin | 1 | [50] |
| StackSpotAI | 1 | [84] |
| StarCoder (7B) | 1 | [59] |
| TransCoder | 1 | [51] |
| aiXcoder | 1 | [59] |
| OpenAI API | 1 | [85] |
| Midjourney | 1 | [85] |

**Covers:** quality-assessment scoring through most-frequently-used LLM tools (chunk 04, §§3.3 tail–4.4 incl. Fig. 2 and Tables 3–4)
