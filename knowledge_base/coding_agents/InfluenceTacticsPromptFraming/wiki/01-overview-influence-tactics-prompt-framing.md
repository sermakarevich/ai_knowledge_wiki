> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview: Do Influence Tactics Matter in LLM Code Generation?
**In one sentence:** This first large-scale empirical study operationalizes eight Yukl & Falbe influence tactics into reproducible prompt templates and tests them across five open-weight LLMs on LiveCodeBench and SWE-bench Verified, finding that certain framings — particularly urgency/Pressure — were associated with reduced correctness and security.
## Key points
- First large-scale study of influence-induced prompt framing in SE code generation: over 123,000 generations for LiveCodeBench and nearly 57,000 for SWE-bench Verified across models, runs, and tactics.
- Operationalized eight influence tactics (e.g. rational persuasion, ingratiation, exchange) from Yukl & Falbe's taxonomy into reproducible prompt templates using IBQ-G items as requirements.
- Evaluated five leading open-weight LLMs on two benchmarks (LiveCodeBench, SWE-bench Verified) across four quality dimensions: functional correctness, quality, maintainability, and security.
- Key result: urgency-emphasizing framings (notably Pressure) were associated with reduced correctness and security.
- Qualitative triangulation found tactic framings also changed tone, structure, and reliability: some elicited more explanation/technical detail, others increased hallucination rates.
- Theoretical framing: LLMs trained on human communication may learn statistical associations between pragmatic framings and response styles, so influence framings act as distributional cues without requiring the model to understand persuasion or social intent.
- Practical aim: evidence-based guidance for transparent, interpretable human-AI prompt design, revealing risks of psychologically framed prompts in real-world SE workflows.
---
## Abstract
**Covers:** Title block, authors, publication note, Abstract, Keywords

Paper: "Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation" by Alex Deaconu*, Anubhav Gupta* (shared first authorship), Manaal Basha, Nicholas Haydu, Gema Rodríguez-Pérez.

Publication note: "This version of the article has been accepted for publication, after peer review, but is not the Version of Record and does not reflect post-acceptance improvements or any corrections. The Version of Record is available online at: http://dx.doi.org/10.1007/s10664-026-10934-z."

arXiv:2608.11513v1 [cs.SE] 11 Aug 2026.

Core claim (verbatim): "While prompt wording and structure are known to influence model performance, the impact of psychologically inspired prompt framings remains unexplored."

Method in brief: "Drawing on Yukl & Falbe's well-known taxonomy, we operationalized eight influence tactics (like rational persuasion, ingratiation, and exchange) into reproducible prompt templates" evaluated "across five leading open-weight LLMs using two widely adopted benchmarks: LiveCodeBench and SWE-bench Verified" on "four key software quality dimensions: functional correctness, quality, maintainability, and security."

Headline finding (verbatim): "Our results show that certain influence-induced prompt framings, particularly those emphasizing urgency, were associated with reduced correctness and security."

Positioning (verbatim): "This work presents the first large-scale empirical study of influence-induced prompt framing in software engineering tasks, offering insights into how linguistic cues may shape LLM outputs."

Keywords: Empirical Software Engineering · Software Quality · LLMs · GenAI · Human Factors.

## 1 Introduction
**Covers:** Section 1 (pp. 2–3)

LLMs support SE tasks "such as code synthesis [50], API documentation [17], automated bug repair [73], and supporting testing workflows [74]," and prompt phrasing/framing can influence behaviour and code quality [20, 66]. Cited examples:

| Study | Finding in chunk |
|---|---|
| Tony et al. [62] | Recursive Criticism and Improvement technique reduced security weaknesses across some LLMs |
| Liu et al. [37] | Chain-of-thought prompt designs notably improve ChatGPT's coding performance |

Gap: prior work covered syntactic prompt engineering [9], reasoning strategies like chain-of-thought [65,37], and explicit instructions [8]; by contrast, organizational psychology shows request framing affects human compliance/performance [21], e.g. "Yukl & Falbe's influential taxonomy of influence tactics [70] shows how subtle shifts in approach, such as appeals to rational arguments, expressions of urgency, or offers of reciprocity, can change outcomes in collaborative settings."

Research question (verbatim): "To what extent do prompt framings inspired by these influence tactics lead to measurable differences in LLM-generated code?"

Relevance: SE relies on interactive human-AI workflows needing reliable, maintainable, secure code; developers "naturally tend to use rational persuasion to justify design decisions, invoke pressure to communicate urgency under tight deadlines, or suggest exchanges to motivate cooperation [30]."

Supporting linguistic-cue evidence cited:

| Cue | Finding in chunk |
|---|---|
| Politeness [49] | More polite prompts to GPT-4 lead to longer, more positive outputs; alters length and affective tone |
| Yin et al. [68] | Medium to high politeness levels correspond to fewer comprehension errors |
| Adversarial/social engineering [13] | Persuasive or deceptive framings increase prompt-injection attack success rate |

Interpretive mechanism (verbatim): "Because LLMs are trained on large corpora of human-authored communication, they may learn statistical associations between particular pragmatic framings and particular response styles." Hence "psychologically inspired prompt framings act as distributional cues that may steer generation behaviour without requiring the model to understand persuasion or social intent in a human sense."

Design summary: eight tactics operationalized into templates using "items from the Influence Behavior Questionnaire-General (IBQ-G), a validated instrument for identifying the usage of influence tactics, as requirements to build prompt templates"; plus "a triangulation study to explore the qualitative differences underlying these effects."

Results preview (verbatim): "certain tactic-influenced framings, such as Pressure, were associated with reduced correctness and security" and "lead to qualitative differences in the tone, structure, and reliability of model responses, with some prompting more explanation or technical detail, while others increased hallucination rates."

Three contributions (verbatim):

| Contribution | Detail in chunk |
|---|---|
| Empirical Analysis | "The first large-scale study quantifying the impact of psychologically inspired prompt framings on LLM-generated code, covering over 123,000 generations for LiveCodeBench and nearly 57,000 generations for SWE-bench Verified across multiple models, runs, and influence tactics." |
| Prompt design resource | "A taxonomy-aligned set of reproducible prompt templates operationalizing eight distinct influence tactics for programming and software engineering tasks." |
| Practical insights | "Evidence-based guidance on how linguistic framing choices affect functional, maintainability, and security dimensions of AI-generated code, informing more transparent and interpretable human-AI interactions in SE." |

## 2.1 Influence Tactics and Psychological Framing (partial)
**Covers:** Section 2.1 up to Table 1 header (p. 4)

Definition (verbatim): "an influence tactic is an approach by an agent to achieve some goal from another individual, called the target, where success depends on the tactic applied [72]."

Taxonomy evolution numbers in chunk:

| Study | Numbers in chunk |
|---|---|
| Kipnis et al. [32], study 1 | 165 lower-level managers wrote descriptions of successful influence attempts toward superiors, co-workers, or subordinates; 370 tactics extracted and sorted into 14 greater categories |
| Kipnis et al. [32], study 2 | Factor analysis on a 58-item questionnaire refined these into eight core dimensions |
| Yukl & Falbe [70] | Developed the Influence Behaviour Questionnaire (IBQ) with agent + target data, leading to an updated nine tactic taxonomy; "pressure tactics, characterized by demands or threats, are frequently employed in downward influence attempts, though organizational literature suggests such coercive approaches may provoke resistance or reduce effectiveness [70]" |
| Yukl & Seifert [71] + Yukl, Seifert & Chavez [69] | Two more tactics added (11 total), validated via confirmatory factor analysis establishing "distinctiveness and utility of the expanded autonomy" |
| [72] + refined IBQ-G | "Confirmatory factor analysis again supported the 11-factor structure, with convergent validity tested against competing taxonomies and discriminant validity via low inter-tactic correlations"; refined IBQ-G "we utilize in the design of our influence tactic prompt template" |

Chunk ends at: "Table 1: Evolution of influence tactics across key studies."
