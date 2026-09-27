> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Research Design: Related Work, Questions, and Data Method
**In one sentence:** Prior work on Copilot focused on code correctness, quality, security and expectations but left practices and challenges unstudied, so the authors define six research questions (RQ1–RQ6) and answer them with 169 Stack Overflow posts and 655 GitHub Discussions collected on 23 November 2022, analysed by descriptive statistics (RQ1–RQ3) and constant comparison (RQ4–RQ6).
## Key points
- Gap claim: existing studies focus on correctness and understanding of Copilot-suggested code, with little empirically-rooted evidence on practices and challenges of using Copilot in programming activities.
- Six RQs cover programming languages (RQ1), IDEs (RQ2), technologies (RQ3), functions implemented (RQ4), benefits (RQ5), and limitations/challenges (RQ6), each with an explicit rationale for helping developers choose tools or decide whether to use Copilot.
- SO collection: search term "copilot" returned 557 posts, reduced to 521 unique URLs after deduplication, then to 169 Copilot-related posts after manual filtering with inclusion criterion that the post must provide information referring to Copilot.
- Pilot labelling agreement: two authors labelled 10 SO posts with Cohen's Kappa 0.773, described as decent agreement between the two coders.
- GitHub Discussions collection: all 655 discussions under the "Copilot" category of "GitHub product categories" were included, chosen because Discussions support varied intentions (e.g., reporting errors, discussing development) complementary to SO's Q&A format.
- Extraction rule: an item (D1–D6) was counted only if explicitly mentioned as used with Copilot, and repeated mentions of the same item by the same developer in one post/discussion counted once, while mentions by multiple developers could make instance counts exceed post/discussion counts.
- Analysis split: RQ1–RQ3 use descriptive statistics while RQ4–RQ6 use the Constant Comparison method, with RQ4 categories built from developers' own descriptions of functions and a three-author code–review–consensus workflow.
---
## Related work
**Covers:** Section II

Prior studies cluster on security, quality, and usage behaviour rather than practices/challenges:

- Sandoval et al. [7]: user study on LLMs supporting Copilot; LLMs have a positive impact on correctness of functions, with no decisive impact on safety correctness.
- Imai [8]: Copilot vs human programming; generated code by Copilot is inferior to human-written code.
- Yetistiren et al. [9]: assessed validity, correctness, and efficiency; Copilot is a promising tool.
- Madi et al. [6]: readability and visual inspection via human experiment; programmers should beware of tool-generated code.
- Wang et al. [10]: mixed-methods on expectations; effectiveness and code quality is more important than other expectations.
- Dakhel et al. [11]: empirical evaluation of capabilities; Copilot shows limitations as an assistant for developers.
- Nguyen and Nadi [12]: correctness and comprehensibility; suggestions for different programming languages do not differ significantly, with shortcomings like generating complex code.
- Bird et al. [5]: three studies on how developers use Copilot; developers spent more time assessing Copilot's suggestions than doing the task by themselves.
- Sarkar et al. [13]: compared programming with Copilot to previous conceptualizations of programmer assistance and discussed issues in applying LLMs to programming.

Positioning claim: "Compared to the existing work (e.g., [9], [11]), our work intends to understand the practices and challenges of Copilot by exploring the programming languages, IDEs, technologies used with Copilot, functions implemented by Copilot, and the benefits, limitations, and challenges of using Copilot."

Stated contributions: (1) identified the programming languages, IDEs, and technologies used with Copilot; (2) provided the functions implemented by Copilot, the benefits, limitations, and challenges of using Copilot; (3) present the directions to be further explored.

## Research questions
**Covers:** Section III.A, Table I, Figure 1 (Phase A)

| Research Question | Rationale (as stated) |
|---|---|
| RQ1: What programming languages are used with GitHub Copilot? | Copilot can help practitioners write less code. This RQ aims to collect the programming languages that developers tend to use with Copilot. |
| RQ2: What IDEs are used with GitHub Copilot? | Copilot is a third-party plug-in used in IDEs. This RQ aims to identify the IDEs frequently used with Copilot. The answers can help developers choose which IDE to use when they code with Copilot. |
| RQ3: What technologies are used with GitHub Copilot? | Programmers need to employ certain technologies to complete development. This RQ aims to investigate the technologies (e.g., frameworks), and the answers can help developers choose technologies when they use Copilot. |
| RQ4: What functions are implemented by using GitHub Copilot? | Copilot can complete entire functions according to users' comments. This RQ aims to categorize functions implemented by Copilot, providing guidance when implementing functions by using Copilot. |
| RQ5: What are the benefits of using GitHub Copilot? | Using Copilot can bring many benefits (e.g., reducing workload). This RQ aims to collect the advantages brought to development by applying Copilot. |
| RQ6: What are the limitations and challenges of using GitHub Copilot? | Although Copilot can help programming activities, there are restrictions and problems. This RQ aims to collect limitations/challenges practitioners may experience, helping practitioners make an informed decision when deciding whether to code with Copilot. |

Process overview (Fig. 1): Phase A specifies research questions (RQ1–RQ4 languages/technologies/IDEs/functions; RQ5 benefits; RQ6 limitations); Phase B is data collection and filtering from Stack Overflow [169 posts] and GitHub [655 discussions]; Phase C is data extraction and analysis with [RQ1~RQ3] descriptive statistics and [RQ4~RQ6] constant comparison.

## Data collection and filtering
**Covers:** Section III.B

- Sources chosen: Stack Overflow as a popular Q&A community widely used by developers, plus GitHub Discussions as a project communication feature with various intentions beyond question-answering (e.g., reporting errors, discussing potential development) [14], complementary to SO and acting as a community knowledge base connected with other project artifacts.
- Search date for both sources: November 23rd, 2022.
- Stack Overflow procedure:
  - Search term "copilot" → 557 posts containing the term.
  - After removing duplicate URLs (term may appear more than once per post) → 521 posts with unique URLs.
  - Pilot labelling: two authors labelled 10 retrieved posts; inclusion criterion is that the post must provide information referring to Copilot; Cohen's Kappa 0.773, indicating decent agreement.
  - After excluding irrelevant posts → 169 Copilot-related SO posts.
- GitHub Discussions procedure:
  - Explored categories and found the "Copilot" category containing feedback, questions, and conversations about Copilot [16] under "GitHub product categories".
  - Included all discussions under that category → 655 Copilot-related discussions.

## Data extraction and analysis
**Covers:** Section III.C, Table II

Data items and methods:

| # | Data Item | Description | Analysis Method | RQ |
|---|---|---|---|---|
| D1 | Programming language | Programming language used with Copilot | Descriptive statistics [17] | RQ1 |
| D2 | IDE | IDEs used with Copilot | Descriptive statistics | RQ2 |
| D3 | Technology | Technologies used with Copilot | Descriptive statistics | RQ3 |
| D4 | Function | Functions implemented by Copilot | Constant comparison | RQ4 |
| D5 | Benefit | Benefits brought by using Copilot | Constant comparison | RQ5 |
| D6 | Limitation and Challenge | Restrictions and difficulties when using Copilot | Constant comparison | RQ6 |

Extraction workflow:

- Pilot extraction: first and third authors independently extracted 10 SO posts and 10 GitHub discussions randomly selected from the 169 posts and 655 discussions; second author discussed disagreements to reach agreement, fixing extraction criteria.
- Criteria: (1) for all items D1–D6, extract and count only if explicitly mentioned by developers that they were used with Copilot; (2) if the same developer repeatedly mentioned the same item in one post/discussion, count it once.
- Counting note: multiple developers in one post/discussion may mention items, so total instances of an item may exceed the number of posts and discussions.
- Full extraction: first and third authors extracted from filtered posts/discussions, marked uncertain parts, discussed with the second author to consensus; first author rechecked all extraction results to ensure correctness.

Analysis workflow:

- RQ1–RQ3: descriptive statistics [17].
- RQ4–RQ6: qualitative Constant Comparison method [18], constantly comparing codes to explore differences/similarities and form categories [19]; RQ4 categorization is based on developers' discussions/descriptions of mentioned functions.
- Coding steps: first and third authors coded filtered posts/discussions with D1–D6 items; first author reviewed the third author's coding; first author combined codes into higher-level concepts/categories; second author examined coding and categorization, with divergences discussed until all three authors reached agreement.
- Analysis results are stated to be provided in [20].

Context note: work funded by NSFC Grant No. 62172311 and Special Fund of Hubei Luojia Laboratory; DOI reference 10.18293/SEKE2023-077.

**Covers:** Paper tail of Section I through Section III (Related Work, RQ1–RQ6 in Table I, Figure 1 research process, SO/GitHub collection 23 Nov 2022 with 169 posts + 655 discussions, Table II data items D1–D6 and analysis methods)
