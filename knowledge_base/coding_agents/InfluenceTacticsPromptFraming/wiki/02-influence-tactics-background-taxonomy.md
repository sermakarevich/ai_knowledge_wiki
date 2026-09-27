> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Influence Tactics Background and Taxonomy

**In one sentence:** The influence-tactics taxonomy evolved from Kipnis et al.'s 8 tactics to Yukl et al.'s 11 tactics, meta-analytic evidence shows rational/personal tactics help task outcomes while pressure hurts, and the authors argue this human-communication literature plus known LLM code-quality and prompt-engineering gaps motivates testing whether socially framed prompts shape generated code.

## Key points

- The taxonomy grew over time: Kipnis et al. listed 8 tactics (Assertiveness through Coalitions), Yukl & Falbe listed 9, and Yukl et al. listed 11 by adding Apprising and Collaboration.
- Lee et al.'s meta-analysis of 49 independent samples found rational persuasion, inspirational appeal, apprising, collaboration, ingratiation, and consultation had significant positive relationships with task-oriented outcomes.
- In the same meta-analysis, coalition and exchange tactics had insignificant effects, while pressure tactics were reliably counter-productive to task outcomes.
- Toxic workplace environments (bullying, harassment, ostracism) adversely affect work performance, and McCarthy et al. found email rudeness leads to decline in subsequent task performance.
- LLM code generation has documented defects: 367 defects found by Mohammadi Esfahani et al., 62% GPT-4 API misuse reported by Li and Wang, plus variability and security concerns from training on vulnerable public code.
- Rasheed et al. surveyed 60 software practitioners on LLM usability and performance, complementing technical evaluations of reliability, accuracy, and security.
- Structural prompt engineering (in-context learning, Chain-of-Thought, Self-Consistency, Auto-CoT, decomposition, PICARD constrained decoding, Reflexion, LATS, AgentCoder, LDB, APE, ProTeGi, Bsharat et al.'s 26 principles) improved correctness but left tone, politeness, and persuasive framing under-explored.

---

## Taxonomy evolution: Kipnis to Yukl

| Kipnis et al. [32] | Yukl & Falbe [70] | Yukl et al. [69] |
|---|---|---|
| 1. Assertiveness | 1. Pressure | 1. Pressure |
| 2. Ingratiation | 2. Ingratiation | 2. Ingratiation |
| 3. Rationality | 3. Rational persuasion | 3. Rational persuasion |
| 4. Sanctions | 4. Legitimating tactics | 4. Legitimating tactics |
| 5. Exchange | 5. Exchange | 5. Exchange |
| 6. Upward appeals | 6. Personal appeals | 6. Personal appeals |
| 7. Blocking | 7. Coalition tactics | 7. Coalition tactics |
| 8. Coalitions | 8. Inspirational appeals | 8. Inspirational appeals |
|  | 9. Consultation | 9. Consultation |
|  |  | 10. Apprising |
|  |  | 11. Collaboration |

**Covers:** chunk 02, taxonomy table (Kipnis et al. [32] / Yukl & Falbe [70] / Yukl et al. [69])

## Meta-analysis and workplace communication

- "In a comprehensive meta-analysis of 49 independent samples, Lee et al. [35] found that the categories of the final influence tactic framework [71] differ in both their likelihood of success and the quality of work produced."
- Positive task-outcome tactics: "Rational persuasion, inspirational appeal, apprising, collaboration, ingratiation and consultation all showed significant positive relationships with task-oriented outcomes."
- "Meanwhile, the effects from coalition and exchange tactics were insignificant, and pressure tactics were reliably counter-productive to task outcomes."
- "One study finds that toxic workplace environments (including bullying, harassment and ostracism) can adversely affect employees' work performance [51]."
- "Additionally, evidence suggests that exposure to rudeness in email communication can lead to a decline in subsequent task performance, as demonstrated by McCarthy et al. [40]."
- Bridging claim: "Given that LLMs are trained on a large corpora of human communication, it is reasonable to ask whether these psychologically derived tactics might also shape LLM outputs."

**Covers:** chunk 02, Section 2.1 continuation (Lee et al. meta-analysis through LLM motivation)

## Large Language Models for Code Generation (Section 2.2)

- "Mohammadi Esfahani et al. [19] identified 367 defects in LLM-generated code, primarily related to functionality and algorithmic logic. However, structured prompting was found to reduce some errors."
- "Li and Wang [77] reported that 62% of GPT-4-generated code contained API misuses" — example failure: "calling File.createNewFile() without a try-catch block or checking File.exists() beforehand, producing code that is syntactically correct and functionally aligned with the user's intent, yet prone to crashes in production when the file already exists, or the parent directory is missing."
- "Beer et al. [5] observed significant variability in code correctness and quality between models like ChatGPT and Copilot across different programming languages and time periods."
- "Security remains a major concern, particularly due to LLMs being trained on potentially vulnerable public code repositories [41]."
- "Rasheed et al. [50] surveyed 60 software practitioners to assess LLMs' usability and performance in practical settings."

**Covers:** chunk 02, Section 2.2 (p. 5)

## Prompt Engineering: logical structure (Section 2.3)

- "in-context learning, which provides a few input-output examples in the prompt, was introduced with GPT-3 [7]" and "enabled few-shot code generation by showing the model how to format solutions."
- "Chain-of-Thought (CoT) prompting ... encourages the model to generate intermediate reasoning steps, which boosts performance on complex problems [65]."
- "Wang et al. [63] further improved reliability through Self-Consistency, sampling multiple reasoning paths and letting the model choose the most consistent solution."
- Also named: "Auto-CoT (automatically generating a few-step reasoning example for zero-shot prompts) [75] and knowledge-enhanced prompting that injects factual hints to reduce errors [48]."
- Summary claim: "These advancements in prompt engineering largely focus on the logical structure of the prompts. They involve breaking tasks down, adding reasoning instructions, or incorporating relevant instructions."

**Covers:** chunk 02, Section 2.3 (p. 5–6)

## Structural Prompting Techniques for Code Generation (Section 2.3.1)

- "Chen et al. [9]" (Codex): "providing descriptive docstrings or usage examples in the prompt can guide the model to produce syntactically correct and relevant code," but "purely zero-shot or few-shot prompts often yielded errors in logic or API usage [56]."
- "Prompt decomposition is a technique where a complex coding task is broken into smaller sub-prompts (e.g., first asking for a high-level solution plan, then code) [31]."
- "constrained decoding, illustrated through Scholak et al's PICARD method [54], which restricts the model's output to a grammar (such as SQL syntax) to ensure validity."
- Multi-turn/agentic frameworks: "Reflexion uses the model's own feedback to detect and correct errors in subsequent iterations [57]"; "(LATS) [80] and AgentCoder [26] organize multiple specialized agents (or prompt stages), where one agent writes code, another generates test, and another debugs"; "LLM Debugger (LDB) runs the generated code and feeds back runtime results so the model can fix bugs iteratively [78]."
- Cost: "a tree-search planner might consume hundreds of thousands of tokens per problem to come up with a valid solution [60]."
- Optimization approaches: "Automatic Prompt Engineer (APE) by Zhou et al. [81], treats prompt construction as a search problem"; "ProTeGi, uses gradient-free optimization to iteratively edit prompts for higher performance [46]"; "Bsharat et al. [8] proposed a comprehensive framework of 26 guiding principles designed to improve LLM responses through clarity, specificity, and structured instructions."
- Gap: Bsharat et al. "remains primarily syntax-driven, leaving pragmatic aspects such as tone, politeness, and persuasive framing under-explored," while "LLM behaviour can shift in response to pragmatic or emotional prompting, even when the underlying task content remains similar [36,68,49]."
- Non-programmer relevance: LLMs as "natural language interfaces for programming-like tasks [45]"; "Because these interactions occur through ordinary conversational language, our study examines whether socially framed prompt variations can affect generated code, using influence tactics as a framework."

**Covers:** chunk 02, Section 2.3.1 (pp. 6–7)

## Pragmatic Prompting and Social Framing (Section 2.3.2, opening)

- "LLMs are fundamentally statistical models trained to predict token sequences rather than explicitly reason about intent or social context."
- Hypothesis assumption: "LLM training corpora contain vast amounts of human-authored text from which models may capture statistical associations between specific linguistic framings and particular forms of generated output."
- Stated examples: "coercive or directive language may be associated with shorter, task-focused completions, whereas formal language may correlate with more structured and well-documented responses."
- Interpretation: "influence-tactic framings act as distributional cues that shape model outputs, not because the model comprehends intent, but because these linguistic patterns co-occur with particular response styles in the training data."

**Covers:** chunk 02, Section 2.3.2 opening (p. 7, truncated mid-sentence)

**Covers:** chunk 02-kipnis-et-al-32-yukl (Sections 2.1-table through 2.3.2 opening, pp. 5–7)
