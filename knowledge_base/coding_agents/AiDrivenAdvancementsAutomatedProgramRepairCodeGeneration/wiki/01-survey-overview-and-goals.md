> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Survey Overview and Goals
**In one sentence:** This survey reviews 27 recent papers split into Automated Program Repair and LLM-based code generation to summarize how LLMs improve bug fixing and code generation, which repair scenarios and languages they cover, how LLMs are integrated into those workflows, and what limitations remain.
## Key points
- The survey reviews 27 recent papers, split into two groups: Automated Program Repair (APR) with LLM integration, and code generation using LLMs.
- The APR group covers bug detection and repair methods including semantic-error localization, security vulnerabilities, and runtime-failure bugs, emphasizing context-aware fixes that reduce manual debugging.
- The code-generation group covers general-purpose LLMs fine-tuned for programming and task-specific models, plus improvements such as identifier-aware training, instruction-level fine-tuning, and incorporating semantic code structures.
- The survey contrasts APR and code-generation methodologies to identify trends: LLM use, feedback loops for iterative code improvement, and open-source models.
- LLMs are favored because training on extremely large datasets with billions of parameters gives strong performance without training models from scratch.
- Core challenges named are achieving functional correctness and security, building language-agnostic APR tools, and handling complex areas such as benchmarking, repair scenarios, repair techniques, and testing of repairs.
- The survey method in this chunk comprises systematic literature review with inclusion/exclusion criteria, taxonomy development, and comparative analysis with tabular and graphical visualization.
---
## Survey identity and scope
This chunk is the paper front matter (title, authors, abstract, reference format) plus Section 1 (Introduction) and the start of Section 2 (Survey Methodology). Bibliographic details stated verbatim in the chunk:

| Field | Value as stated in chunk |
|---|---|
| Title | "A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation" |
| Authors | Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj, Indraprastha Institute of Information Technology, India |
| Identifier | arXiv:2411.07586v1 [cs.AI] 12 Nov 2024 |
| Length | 19 pages (per ACM Reference Format block) |
| Papers reviewed | 27 recent papers |

Verbatim scope claim: "In this survey, 27 recent papers have been reviewed and split into two groups: one dedicated to Automated Program Repair (APR) and LLM integration and the other to code generation using LLMs."

## Introduction — why LLMs for APR and code generation
The chunk states that bug fixing and code generation have been core software-development research topics for many years, and that "recent explosive growth in Large Language Models has completely transformed these spaces." It lists LLM-assisted tasks — code summarization, natural-language-to-code generation, fixing bugs in pre-existing code, and understanding large/complex repositories — but scopes this paper to only code generation and bug fixing, divided into those two categories for clarity.

Mechanisms and prior techniques named for existing APR/code-generation tools include Abstract Syntax Trees (ASTs), heuristics for ranking plausible patches, patterns, and context-matching. The stated advantage of large LLMs is being "trained on extremely large datasets and billions of parameters," making it "easier to employ large LLMs to do particular tasks pertaining to programming" with "impressive performance and sizable advantages when compared to training models from scratch."

The chunk also stresses complexity: employing LLMs in APR and code generation spans benchmarking, repair scenarios (syntactic errors, semantic errors, etc.), repair techniques (recompilation, binary rewriting, etc.), and testing of repairs (patch generation, input testing, coevolution), so understanding prior work is "quite complex and time consuming." For each of the 27 papers the survey summarizes the LLMs used, the programming languages covered (and hence difficulties in building language-agnostic APR tools), the repair/generation approach, and open challenges.

## Stated aims of the paper
The chunk lists four aims verbatim:

> (1) Collect research done on APR and code generation using LLMs and summarize the goals achieved.
> (2) Elucidate the repair scenarios these tools can be used for and the programming languages they work on.
> (3) How LLMs are integrated into the workflow of repairing and generating code and the challenges faced in doing so.
> (4) The limitations of using LLMs in code-related tasks and cases which are still being worked on.

## Survey methodology as presented in this chunk
Section 2 ("Survey Methodology") states it covers the measures for searching, collecting, and filtering models, papers, and journals. Two subsections begin in this chunk:

### Research questions
Four research questions are listed verbatim:

> (1) How have AI techniques, especially large language models (LLMs), improved software debugging and bug fixing? What are some recent trends and common challenges in using AI for these tasks?
> (2) How do modern debugging tools and benchmarks help evaluate the effectiveness of bug-fixing methods? What are the common gaps or limitations in these tools?
> (3) What are the key differences between popular code generation models? How do these models perform on tasks like code completion and code summarization?
> (4) How do different AI models and tools compare in handling various code-related tasks? What are the main strengths and weaknesses of these models?

Inclusion rule stated in chunk: criteria and metrics "focuses mostly on whether it has helped us to answer any of these questions more comprehensively" and "any resource that added no value on any of these topics were discarded."

### Methods employed
Three methods are listed verbatim:

> (1) Systematic Literature Review — "A review of the available literature on the subject of interest and related work," with "clear inclusion and exclusion criteria," searching databases, applying the criteria, then "categorizing the selected papers/models under umbrella categories of Code Generation and Automated Program Repair as shown in Fig. 1."
> (2) Taxonomy Development — "creating a classification of the AI techniques, tools and methods used for debugging, bug fixing and code generation," compared on "objectives, techniques and outcomes," identifying "overlaps and distinctions between categories."
> (3) Comparative Analysis — comparison "between the selected papers using various evaluation criteria such as performance, accuracy etc." with "tabular and graphical description for a better visualization."

**Covers:** Survey scope, goals, and the APR vs code-generation split (paper front matter through Section 1 Introduction and opening of Section 2 Survey Methodology: research questions and methods employed).
