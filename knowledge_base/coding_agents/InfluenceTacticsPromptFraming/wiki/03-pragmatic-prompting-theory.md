> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Pragmatic Prompting Theory: Distributional-Cue Interpretation and Prior Work

**In one sentence:** The authors interpret any influence-tactic effects as prompt-level distributional cues grounded in linguistic form (IBQ-G) rather than LLM persuasion or experience, argue non-uniform effects consistent with prior stylistic/emotion-based prompting work, and motivate a four-phase study of correctness, quality, maintainability, and security across LiveCodeBench and SWE-bench Verified via RQ1–RQ3.

## Key points

- Effects are framed as distributional cues, not cognition: surface-level lexical/pragmatic features from the IBQ-G are tested for measurable output shifts without assuming LLMs "experience" pressure, ingratiation, or urgency.
- Non-uniformity is expected per prior prompt-sensitivity research [82]: models are more susceptible on complex reasoning/open-ended generation and more stable on constrained tasks, so framing should show up in verbosity, commenting, or reasoning depth rather than where test suites enforce correctness.
- Zero-shot pragmatic prompting precedents are Style Prompting [38], Role Prompting [76,53] (e.g. "an expert software security auditor", "a senior developer"), and Emotion Prompting [36] (e.g. "This implementation is crucial for my project") influencing thoroughness and attention to detail.
- The claimed gap is that no prior research systematically explored psychological influence tactics in code generation or how distinct tactic-inspired framings affect quality and characteristics of generated code.
- The study design integrates quantitative and qualitative analysis across four dimensions — correctness, quality, maintainability, and security [58] — with four phases: (I) benchmark selection, (II) tactic selection/prompt design, (III) quantitative analysis, (IV) qualitative codebook analysis.
- RQ1 targets structured algorithmic tasks on LiveCodeBench (easy/medium/hard) asking how framings affect the four dimensions; RQ2 targets open-ended maintenance/debugging on SWE-bench; RQ3 asks what qualitative patterns (tone, structure, commentary, verbosity, error-handling) emerge, coded only on LiveCodeBench.
- The two benchmarks are complementary: LiveCodeBench [28] with 1055 code problems (Easy/Medium/Hard) for precise logic with minimal ambiguity, and the Verified [11] subset of SWE-bench [29] with 500 human-validated GitHub issues for multi-file, context-rich maintenance.

---

## Distributional-cue interpretation (consistent with prior work)

- "interpretation is consistent with prior work on stylistic and emotion-based prompt-ing [36,22,64]."
- "Such distributional effects are not expected to be uniform across various tasks or metrics. Prior research on LLM prompt sensitivity suggests that models are gen-erally more susceptible to pragmatic prompt variations in tasks involving complex reasoning or open-ended generation, while they tend to be more stable on tasks with constrained and unambiguous solutions [82]."
- "This suggests that framing effects are more likely to emerge in dimensions where the model exercises greater interpretive flexibility, such as response verbosity, commenting behaviour, or reasoning depth, and less likely where strong external constraints, such as benchmark test suites, enforce correctness."

**Covers:** chunk 03, distributional-effects non-uniformity paragraph (p. 7 continuation)

## Hypotheses grounded in linguistic form, not persuasion

- "Our hypotheses are grounded in linguistic form: the specific lexical and pragmatic features used to operationalize each tactic from the Influence Behavior Questionnaire-General (IBQ-G), rather than in claims that LLMs are behaviourally susceptible to persuasion in the way humans are."
- "We do not claim that LLMs "experience" pressure, ingratiation, or urgency in any meaningful sense. Rather, we ask whether the surface-level linguistic features associated with each tactic are sufficient to shift model outputs in measurable ways."
- "This question is empirically testable without requiring strong assumptions about model cognition or intent. Therefore, observed effects should be interpreted as prompt-level distributional influences rather than as evidence that LLMs "understand" or "respond to" influence tactics in a psychologi-cally meaningful sense."

**Covers:** chunk 03, IBQ-G grounding paragraph (p. 7)

## Pragmatic and socially framed zero-shot prompting

- "A parallel line of research has begun to explore zero-shot prompting techniques that more directly shape model behaviour through pragmatic cues [55]. These tech-niques do not rely on examples or fine-tuning, but instead guide outputs by framing the prompt in socially or contextually meaningful ways."
- "For instance, Style Prompt-ing [38] involves specifying the desired style, tone, or formatting conventions in the prompt, Role Prompting [76,53] assigns the model a defined professional role or per-spective, such as "an expert software security auditor" or "a senior developer;" and Emotion Prompting [36] incorporates language that conveys personal significance or urgency (e.g., "This implementation is crucial for my project"), which has been shown to influence the thoroughness and attention to detail in generated text."
- "It is evident from previous work that different prompt syntax could lead to different outputs. Additionally, running the same prompt multiple times may lead to different outputs. But it does not, as we run each prompt multiple times and report the vari-ance across runs. We want to isolate the effect of prompt framing and see whether it has any impact on LLM performance."
- Gap claim: "To the best of our knowledge, no prior re-search has systematically explored the use of psychological influence tactics in code generation, nor examined how distinct tactic-inspired prompt framing impacts the quality and characteristics of the generated code."

**Covers:** chunk 03, pragmatic-prompting survey (pp. 7–8)

## Conversational prompts and distributional mechanism

- "When software engineers interact with LLMs to complete development tasks, their prompts are often conversational and informal in nature [79] and may naturally contain social cues, tone, and affective framing."
- "As discussed above, the statistical associations learned during LLM training on human communication data provide a plausible distributional mechanism by which influence-tactic framings may shape model outputs."
- "The key empirical question is therefore not whether LLMs "under-stand" persuasion, but whether the lexical and pragmatic features of each tactic are sufficient to produce measurable shifts in code generation behaviour."
- "Although psychological influence frameworks were originally developed for interpersonal set-tings, the parallels raise an important question: do these tactics similarly affect LLM outputs? Since these differences in tactic efficacy are pronounced for human targets, this study explores whether comparable effects can be observed in LLMs. To this end, we adapt the 11-tactic influence framework proposed by Yukl & Falbe [71] to evaluate its impact on code generation tasks."

**Covers:** chunk 03, conversational-prompt motivation through 11-tactic adaptation (p. 8)

## Study design overview (Fig. 1)

- "The goal of this study is to provide empirical evidence on whether and how psy-chologically inspired prompt framings, derived from human influence tactics, affect the performance of LLMs across four dimensions: correctness, quality, maintainabil-ity, and security [58]."
- "Our study design integrates both quantitative and qualitative analyses to examine these effects comprehensively. Figure 1 illustrates the four main phases of our methodology: (I) benchmark selection, covering LiveCodeBench and SWE-bench verified; (II) influence tactic selection and prompt design; (III) quantita-tive analysis of the generated code; and (IV) qualitative analysis through codebook development and coding."
- "While previous research work has explored syntactic and structural prompt engineering, the effect of socially grounded lexical and pragmatic framings remains underexplored."

| Fig. 1 element | Chunk text |
|---|---|
| I. Benchmark Selection | LiveCodeBench: "1055 Code Problems / Categorised as Easy, Medium and Hard"; SWE-Bench Verified: "500 GitHub Issues / Human validated high-quality subset" |
| II. Influence Tactic Selection and Prompt Design | "Select 8 Psychological Influence Tactics"; "Formulate 8 different prompts based on the definition and requirements" |
| Personal Appeal example | "Hey, I'm really sorry to ask this of you, but you've been a really good friend to me and I need a personal favour. Please, for me, would you generate a patch that resolves the issue and passes the tests? As a friend, it would really help me out" |
| III. Quantitative Analysis | "Extract code snippets from the generated responses"; "Run the extracted code against the LiveCodeBench and SWE-bench test suite"; "Correctness Evaluation"; "1. Code Maintainability Analysis / 2. Code Security Analysis / 3. Code Quality Analysis" |
| IV. Qualitative Analysis | "Random Sampling"; "Codebook Development"; "Codebook Validation"; "Coding the Dataset"; "Inferences" |

**Covers:** chunk 03, Section 3 opening + Fig. 1 (p. 8)

## Research questions RQ1–RQ3

- RQ1: "How do different prompt framings based on psychological influ-ence tactics affect the correctness, quality, maintainability, and security of LLM-generated code in structured, algorithmic problem-solving tasks?"
- RQ1 context: "LiveCodeBench includes problems categorized into easy, medium, and hard diffi-culty levels, allowing for a detailed examination of whether the effects of psychological influence tactics vary with task complexity."
- RQ2: "How do these psychologically inspired prompt framings affect the correctness, quality, maintainability, and security of LLM-generated code in open-ended software maintenance and debugging tasks that require context comprehension and integration with existing codebases?"
- RQ2 context: "The emphasis is on solving real-world software issues sourced from GitHub repos-itories. Hence, SWE-bench provides an important environment for examining how psychological influence tactics affect LLM performance in more practical, maintenance-focused scenarios."
- RQ3: "What qualitative patterns and response characteristics emerge when LLMs generate code under different influence-based prompt fram-ings?"
- RQ3 method/scope: "We aim to identify qualitative patterns such as recurring differences in tone, output structure, commentary, verbosity, and error-handling behaviour that emerge across different tactics."; "We focused our analysis on the Live-CodeBench dataset"; "In contrast, SWE-bench Verified tasks were excluded from this phase because they involve multi-file patches tightly coupled to specific software repositories, which require additional domain knowledge and are less suit-able for consistent qualitative interpretation."

**Covers:** chunk 03, RQ1–RQ3 (pp. 8–10)

## Datasets: LiveCodeBench and SWE-bench Verified

- "We evaluated the influence tactic prompt framings using two complementary benchmarks designed to capture different dimensions of software engineering tasks. One dataset, LiveCodeBench [28], repre-sents structured algorithmic challenges requiring precise logic and correctness. These challenges have clearly defined inputs and outputs with minimal contextual ambigu-ity."
- "The other one, Verified [11] subset of SWE-bench [29], reflects real-world software maintenance tasks involving multi-file reasoning and contextual understanding."
- "To-gether, these datasets allow us to study both the technical accuracy and practical reliability of LLM-generated code under varied prompt framings."

**Covers:** chunk 03, Section 3.1 opening (pp. 10, truncated at 3.1.1 LiveCodeBench)

**Covers:** chunk 03-interpretation-is-consistent-with-prior-work (theory grounding through Section 3.1 opening, Fig. 1, RQ1–RQ3, pp. 7–10)
