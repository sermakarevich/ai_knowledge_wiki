[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Investigating and Ensuring the Quality of AI-Assisted Code
**In one sentence:** Quality of AI-assisted code — examined in 19 of 90 papers across correctness, readability/maintainability, and security — trades development speed for risks of subtle errors, insecure patterns, and harder-to-maintain code, requiring verification, better prompting, personalisation, and developer training.
## Key points
- 19 of 90 papers investigate quality of AI-assisted code generation, covering correctness, security, and readability.
- AI assistance accelerates workflows but increases susceptibility to subtle errors, security vulnerabilities, and reduced maintainability, with often syntactically valid yet logically flawed or non-idiomatic output.
- Readability suffers from overly concise structures, unconventional naming, and missing comments, threatening long-term maintainability in team workflows; AI refactoring and explanation tools are proposed mitigations.
- Up to 36% of vulnerabilities in AI-assisted code originate from the LLMs, reflecting replication of insecure training-data patterns and the need for cautious oversight.
- Quality depends on human/organisational factors — verification habits, prompting, and debugging strategies — so best practices extend to education, training, and workflow adaptation.
- Methodologies across the 90 papers: 12 survey, 32 experimental, 38 qualitative, plus 20 not fitting the dichotomy and mixed-methods user studies.
- Future-work analysis of 250 statements yields 17 topics and 10 methods; top topics are productivity (43), design of AI assistance (29), and audits of AI-generated code (28).
---
## Quality of AI-assisted code generation
**Covers:** Section on quality (pp. 20–21, up to section 3.5)

Quality is examined from multiple perspectives, including code correctness, security, and readability, in 19 out of 90 papers (see Fig. 5 for IDs).

| Aspect | Finding (from chunk) |
|---|---|
| Efficiency–correctness trade-off | AI-assisted coding "significantly accelerates development workflows, but at the cost of increased susceptibility to subtle errors, security vulnerabilities, and reduced maintainability". |
| Correctness | Output "often appears syntactically valid" but "can contain logical flaws, insecure patterns, or deviations from best practices"; quality control via "automated verification, static analysis, and model-aware debugging tools" is "critical to responsible adoption". |
| Readability / maintainability | Output "not always optimized for human understanding" due to "overly concise structures, unconventional variable naming, or lack of meaningful comments"; concern for "long-term maintainability, particularly in team-based software development workflows"; "AI-powered refactoring and explanation tools can help mitigate these challenges". |
| Security | "Up to 36% of vulnerabilities in AI-assisted code originate from the LLMs", pointing to "risks of replicating insecure patterns from training data" and "the need for cautious oversight of AI suggestions". |
| Remedies | "Filtering suboptimal suggestions, improving contextual prompting through docstrings and function names"; "adaptive personalisation of code suggestions", i.e. "learning per-developer and per-task policies for when to suggest, which modality to use, how much code to propose, and how much context to include in the prompt". |
| Human/organisational dimension | "Quality outcomes are influenced by how developers interact with AI tools: whether they verify AI-generated code, how they prompt AI models, and whether they develop strategies for AI-assisted debugging"; best practices "include education, training, and overall workflow adaptation". |

## Methodologies (3.5)
**Covers:** Section 3.5 (p. 20)

| Methodology | Count / detail (from chunk) |
|---|---|
| Survey | 12 of 90 papers |
| Experimental design | 32 of 90 papers |
| Qualitative methods | 38 of 90 papers |
| Not fitting qualitative–quantitative dichotomy | 20 studies, e.g. author-experience case studies with system metrics, quantitative analysis on pre-defined task datasets, analyses of Reddit discussions and GitHub Issues |
| Qualitative approaches | Semi-structured interviews; Wizard of Oz paradigm; focus group interviews; Grounded Theory-based analysis |
| Mixed methods | Experimental design complemented by participant interviews ("user study") |

Sample sizes: interview studies 7–61 participants (median = 16); experimental designs 17–214 participants, except one A/B study with 535 participants and one Meta study reporting "thousands"; surveys 68–2,047 participants (median = 507).

## Future work suggested by existing literature (3.6, partial)
**Covers:** Section 3.6 opening + Fig. 6 topic list (pp. 21–22, chunk truncated mid-section)

250 future-work statements were open-coded by topic (what) and method (how), yielding 17 topics and 10 methodological strategies; Fig. 6 gives paper IDs per topic and Fig. 7 maps topic–method combinations. The chunk notes fragmentation: "Some future work suggestions align with the goals of other studies, but these connections are not always explicit, reflecting a fragmented research landscape."

| Future-work topic | Paper count (from chunk) |
|---|---|
| Productivity factors | 43 |
| Design of AI assistance | 29 |
| Audit of AI-generated code | 28 |
| Prompting support | 19 |
| Skill building with AI | 17 |
| Education with AI | 16 |
| Personalization | 16 |
| Explainability and transparency | 15 |
| Verification support | 13 |
| Broader SDLC coverage | 12 |
| Trust and reliability | 11 |
| IDE redesign for AI | 10 |
| Assistant context enrichment | 6 |
| User mental models | 5 |
| Proactivity | 4 |
| User control | 3 |
| AI governance | 3 |

Productivity suggestions in the visible text emphasize "broader sampling and comparative designs, often at a larger scale", studies "with professional developers in realistic settings" and "attention to students and novices" (chunk truncates here; remainder belongs to a later chunk).

**Covers:** Chunk 07-investigating-and-ensuring-the-quality-of.md (quality section through truncated 3.6/Future Work opening and Fig. 6)
