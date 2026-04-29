# TRIZ and Generative AI -- Example of Prompt (V3.0)

**Paper:** [TRIZ and Generative AI -- Example of Prompt, Version 3.0 (Tanasak Pheunghua & Robert Adunka, 2024)](https://www.triz-consulting.de/wp-content/uploads/2024/04/TRIZ_and_Generative_AI-V3.0.pdf)

## Human Readable TL;DR

TRIZ is a 60-year-old Russian toolkit for solving engineering problems in systematic steps -- but the steps are tedious and demand broad scientific knowledge. The authors realized that chatbots like ChatGPT are already very good at exactly those tedious steps: sifting through facts, listing options, and filling in templates. So they wrote a 120-page cookbook of "recipes" -- carefully worded questions you can paste into ChatGPT, Gemini, or Claude so the AI walks you through each TRIZ tool one step at a time, while you, the human, stay in the driver's seat to judge whether the ideas are any good.

## TL;DR

A practitioner handbook that systematically maps the TRIZ innovation methodology onto prompt-engineered workflows for commodity LLMs (ChatGPT 3.5, Gemini, Claude). Its central thesis is that TRIZ's iterative tool-chain -- where each tool's output feeds the next -- is structurally equivalent to Chain-of-Thought prompting, making TRIZ a natural fit for human-in-the-loop LLM orchestration. The document provides ready-to-use prompt templates for ~30 TRIZ tools spanning MATRIZ Levels 1-3 plus non-curriculum extensions, each wrapped in a "Think before Prompt" meta-frame (what the user needs / what to prepare / what to expect). The work seeds the open-source ccTOPP project (Collaborative and Creative TRIZ Open-Prompts Project) and positions GenAI as a complementary accelerator -- never a replacement -- for human TRIZ analysts.

---

## Problem & Motivation

TRIZ is a comprehensive but effort-intensive methodology: even when practitioners follow identical guidelines, results vary widely with individual knowledge of science, engineering, and research. Two gaps motivated the work:

- **Access gap.** Formal TRIZ training is expensive and slow to acquire; the learning curve blocks wider adoption.
- **Tooling gap.** Generative AI can dramatically reduce the exploration and analysis time TRIZ demands, but no systematic, practitioner-ready catalog of prompt templates existed for the full TRIZ toolset. Ad-hoc prompts (e.g. asking ChatGPT "apply 40 Inventive Principles to X") produce shallow, surface-level output because the model lacks the in-depth definitions and worked examples each tool needs.

The authors therefore set out to document, tool by tool, how to prompt GenAI so that it behaves as a knowledgeable TRIZ assistant while the human analyst retains responsibility for verification and direction.

---

## Main Original Ideas

1. **TRIZ as Chain-of-Thought architecture.** The authors argue that the structured hand-off between TRIZ tools -- where the output of one tool becomes the input to the next -- directly mirrors Chain-of-Thought prompting. This reframes TRIZ not as a legacy methodology in tension with LLMs but as a natural orchestration layer on top of them.

2. **Human-in-the-loop prompt frame.** Every prompt is preceded by a three-part "Think before Prompt" meta-frame: (1) what the user needs, (2) what input the user must prepare, (3) what output to expect from the AI. This scaffolding forces analysts to treat the LLM as a collaborator rather than an oracle.

3. **Tool-stratified prompt catalog.** Prompts are organized along the MATRIZ curriculum hierarchy -- Level 1 (Ideality, 9-Screens, Function Analysis, RCA, CECA, TRIMMING, Scientific Effects, 40 Principles + Contradiction Matrix, Physical Contradictions), Level 2 (Su-Field, 76 Standards, MATChEM, Feature Transfer), Level 3 (TESE trends, Smart Little People, Patent Circumvention, FOS, MFO, Resources Analysis) -- plus a "non-curriculum" set (Morphological Analysis, MOS, Function Redirection, POS, ROS, non-engineering adaptations). This gives readers an entry point at any experience level.

4. **In-context knowledge injection principle.** A consistent authorial stance: pasting only the name of a TRIZ tool into an LLM produces shallow results; pasting the full definition plus worked examples before the instruction produces substantively better ideas. This is operationalized throughout via `[Context] ... [Example] ... [Instruction]` prompt structures.

5. **Seeding the ccTOPP open-prompt project.** The document is framed as the first iteration of a community resource -- the Collaborative and Creative TRIZ Open-Prompts Project -- intending to democratize TRIZ access through shared prompt libraries rather than proprietary tooling.

6. **AI ethics wired into the TRIZ workflow.** A dedicated section addresses trade-secret leakage and copyright exposure specific to TRIZ consulting practice (pasting client IP into public LLMs, AI reproducing copyrighted worked examples), with concrete mitigations (encryption, NDAs, anonymization, audits).

---

## Key Findings

Because this is a practitioner handbook rather than an empirical study, findings are observational and qualitative:

- **Depth of context predicts quality.** Prompts that include full principle definitions and examples produce substantively broader idea sets than prompts that name the principle alone. (Authors' direct observation on the 40 Inventive Principles, p.43.)
- **Cross-platform behavior differs.** Gemini struggles with multi-step prompts in a single message and requires step-by-step session initiation. ChatGPT handles longer prompts better. Claude is used throughout but not benchmarked.
- **Hallucination is reliable on knowledge-heavy tools.** All tested platforms hallucinate when asked about the 76 Standard Solutions without explicit knowledge injection (either full definitions in-prompt or a knowledge-file upload via GPT with Knowledge).
- **Single-problem sessions outperform multi-problem sessions.** Mixing problems in one conversation produces hallucinations and confused context; a new session per problem is the authors' operating rule.
- **Preparation matters more than prompt length.** Vague problem statements yield poor output regardless of prompt engineering; a clear background, problem isolation, and explicit success criteria produce usable results.

No quantitative benchmarks, accuracy rates, or A/B comparisons are reported.

---

## Suggestions & Future Directions

1. **Build the ccTOPP platform.** Develop the open-source Collaborative and Creative TRIZ Open-Prompts Project so practitioners can exchange, version, and audit prompts community-wide.
2. **Expand the prompt catalog.** Future versions should cover additional TRIZ tools, especially non-curriculum extensions that are still being standardized in the TRIZ Body of Knowledge.
3. **Use multiple LLMs in parallel.** Different models surface different ideas; the authors recommend cross-platform triangulation rather than single-tool dependence.
4. **GenAI development should better support complex frameworks.** Native model support for multi-step methodological frameworks (not just one-shot Q&A) would materially improve TRIZ output quality.
5. **Educational initiatives.** Teach practitioners effective use of free or low-cost AI tools, to prevent a resource-disparity divide in access to AI-assisted innovation.
6. **Acknowledged limitations** to keep in mind: LLMs are "complex mathematical functions that process and recombine large datasets" -- not genuinely reasoning; outputs are biased by training data; 76 Standard Solutions and Contradiction Matrix require knowledge-file injection for reliable use; human oversight remains critical for validation.

---

## Authors & Institutions

Tanasak Pheunghua (TRIZ Specialist, primary author), Dr. Robert Adunka (TRIZ Master, co-author and editor) -- TRIZ Consulting GmbH, Germany. Published April 2024 via triz-consulting.de.
