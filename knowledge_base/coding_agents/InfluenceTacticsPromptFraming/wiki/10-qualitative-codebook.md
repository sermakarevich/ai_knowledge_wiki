> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Qualitative Codebook: Topics and Categories (Table 6)
**In one sentence:** The qualitative codebook defines 13 response topics (communication style, tone, structure, reliability) whose tactic-normalized distributions show Legitimating/Exchange/Personal Appeal shifting style and documentation while Pressure and Rational Persuasion raise repeating hallucinations.
## Key points
- The codebook covers 13 topics — Communication Style, Tone, Characteristic, Starts With, Explanation of Code, Test, Complexity, Subject, Emojis, Hallucination Type, Readability, Error Handling, Comments — each with a fixed category set.
- Direct communication was most prevalent under Ingratiation (43.4%) and Inspirational Appeal (44%), while Legitimating prompted a Technical style (41.9%) aligned with its formal, policy-driven tone.
- Exchange and Rational Persuasion contributed more to Conversational style, and Personal Appeal showed higher levels of Friendly tone.
- Structurally, Legitimating outputs more frequently started with Problem description, while Exchange and Personal Appeal more frequently included Explanation of Code.
- Rational Persuasion and Pressure yielded a notably higher proportion of Repeating hallucination, while Neutral and Exchange had the lowest hallucination rates.
- Exchange and Legitimating prompts led to more good-quality comments, and Legitimating plus Ingratiation showed higher rates of error handling.
- RQ3 summary: Legitimating gave more technical responses with better commenting and error handling, Exchange/Personal Appeal gave more explanations, and Pressure/Rational Persuasion were associated with higher hallucination rates.
---
## Table 6: Codebook topics and categories
**Covers:** Qualitative analysis codebook (Table 6)

| Topic | Definition | Categories |
|---|---|---|
| Communication Style | How does the model communicate? Direct, conversational, or technical? | {Direct, Conversational, Technical, None} |
| Tone | Nature of tone: friendly, doubtful, confident? | {Neutral, Friendly, Confident, Doubtful, None} |
| Characteristic | Distribution of response: explanation vs code elements? | {Equally Distributed, Mostly Code, Mostly Explanation, Only Code, Only Explanation} |
| Starts With | How does the response start? Reciprocating vs straight to code? | {Code, Problem Description, Reasoning, Solution Description, Reciprocating} |
| Explanation of Code | Does the response explain the generated code? | {Yes, No} |
| Test | Does the response contain test cases or testing references? | {Yes, No} |
| Complexity | Does the response discuss code complexity? | {Yes, No} |
| Subject | Active/passive voice subject? | {I, You, It, We, None} |
| Emojis | Does the response contain emojis? | {Yes, No} |
| Hallucination Type | Evidence/type of hallucination? | {Repeating, Wrong Programming Language, Stuck Reasoning, None} |
| Readability | Readability of code block: meaningful names, structure, helpers? | {Good, Bad, None} |
| Error Handling | Does the code handle errors? | {Yes, No, None} |
| Comments | Quality of comments: meaningful and helpful? | {Good, Bad, None} |

Together, these dimensions enabled assessment of how influence tactics impacted not only correctness but response delivery and structural form.

## Emergent patterns across tactics (Figure 3)
**Covers:** Frequency of qualitative features normalized per tactic

- Communication Style and Tone: Direct form more prevalent across Ingratiation (43.4%) and Inspirational Appeal (44%); Legitimating prompted more Technical style (41.9%); Exchange and Rational Persuasion contributed more to Conversational style; Personal Appeal showed higher Friendly tone.
- Structural Composition: Legitimating outputs more frequently started with Problem description; Exchange and Personal Appeal more frequently included Explanation of Code.
- Technical Reliability: Rational Persuasion and Pressure tactics yielded a notably higher proportion of Repeating hallucination; Neutral and Exchange tactics had the lowest hallucination rates.
- Other Patterns: Exchange and Legitimating prompts led to more good-quality comments; Legitimating and Ingratiation tactics showed higher rates of error handling.

## RQ3 Summary (verbatim)
**Covers:** RQ3 summary box

> "Prompt framings inspired by different influence tactics partially shaped completeness, reliability, and verbosity of the code. Legitimating prompts led to more technical responses with better commenting and error handling, while Exchange and Personal Appeal prompted more explanations. Some tactics, such as Pressure and Rational Persuasion, were associated with higher rates of hallucination."
