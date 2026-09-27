> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Benefits Evidence and Code Quality
**In one sentence:** Further evidence shows LLM-assistants support learning, code-adjacent tasks, task initiation, troubleshooting, and measurably improve code quality in several studies, while introducing risks around unmet requirements and over-reliance.
## Key points
- Expert consultation is the most common ChatGPT use case at 62% of analyzed conversations, and 75% of survey respondents call ChatGPT a helpful learning tool [56].
- LLM-assistants lower the barrier to learning new frameworks and 14 experts identify enhancing learning and teaching as the most probable future scenario [64, 83, 80].
- For task initiation, 55% of participants (17 out of 31) in a controlled experiment used ChatGPT primarily to generate initial code scaffolding before shifting to independent refinement [57].
- Ten projects built with LLM-assistants show an 18% improvement across six code-quality metrics (including cyclomatic complexity, coverage, smells, technical debt, defect density) versus ten without [86].
- A five-team Copilot case study finds code smells reduced in three of five teams and defect counts decreased in all five teams after adoption [76].
- Code translation with TransCoder support yields a 51% reduction in error rate versus the control group, though ChatGPT beats Stack Overflow on algorithmic/library tasks but loses on debugging tasks [51, 67].
- Benchmarked code-generation correctness ranges from 31.1% (Amazon CodeWhisperer) to 65.2% (ChatGPT), and 50% of participants cite missing or misunderstood requirement context with ChatGPT 3.5 [78, 68].
- Over-reliance risks include eroded critical thinking in novices/students and observed automation complacency (all three Parasuraman–Manzey characteristics) in a programming exam with Google Bard [61, 69, 88, 72].
---
## Expert consultation and learning support
**Covers:** §6.1.4 (Khojah et al. evidence) – §6.1.5 opening

Further evidence is provided by Khojah et al. [56], who analyze developer interactions with ChatGPT:
- Expert consultation is the most common use case, accounting for 62% of analyzed conversations [56].
- 75% of survey respondents report ChatGPT as a helpful learning tool [56].
- LLM-assistants lower the barrier of learning new frameworks, enabling developers to start immediately rather than navigating extensive tutorials [64, 83].
- One study involving 14 experts in SE finds that enhancing learning and teaching is the most probable future scenario with LLM-assistants [80].

## Support code-adjacent tasks
**Covers:** §6.1.5

Benefits extend beyond coding tasks to code-related activities:
- Ideation by exploring different solution options [85].
- Requirements specifications including functional and non-functional requirements [77, 85].
- Documentation such as in-code documentation and API documentation [54, 58, 60, 85].
- Quality assurance [60, 73].
- Composing emails, generating meeting minutes, and creating onboarding documentation [83].
- AI-assisted teams document significantly more GitHub issues and coordinate more effectively through improved information externalization [53].

## Reduce task initiation overhead
**Covers:** §6.1.6

A common reported benefit is support for task or project initiation [51, 57, 60, 70, 73, 82, 83]:
- Developers rely on these tools as a starting point for a project or task [51, 82], effectively lowering the entry barrier [73].
- Tools help build momentum by reducing time and cognitive effort in early project stages.
- Examples: accelerating proof-of-concept applications by generating multiple candidate implementations for the same task [60]; generating an initial structure when starting new topics [70].
- In a qualitative controlled experiment [57], 55% of participants (17 out of 31) used the assistant primarily to generate initial code scaffolding, then transitioned to independent workflows by refining and correcting code themselves and using the LLM only for targeted questions.

## Improve code quality
**Covers:** §6.1.7

- Interview participants in [82] report using these tools to rewrite and improve code quality.
- 14% of survey respondents in [58] identify improved code quality as a key advantage.
- [86] compares ten projects with LLM-assistant support versus ten without, evaluating six metrics (cyclomatic complexity, code coverage, code smells, technical debt, defect density): 18% improvement across all metrics for LLM-assisted projects.
- [76] case study of five development teams before/after Copilot adoption: three of five teams experience measurable reduction in code smells; all five show a decrease in software defects.
- Controlled study [67]: ChatGPT group (treatment) versus Stack Overflow group (control) — higher code quality for ChatGPT in algorithmic and library-usage tasks, control group outperforming in debugging tasks.
- [51] evaluates code translation quality with versus without TransCoder using translation-related metrics (Translation Error, Language Error, Spurious Error): LLM-supported group exhibits fewer translation errors, a 51% reduction in error rate.

## Support troubleshooting / debugging
**Covers:** §6.1.8

- LLM-assistants play an active role in debugging and troubleshooting [85].
- Help interpret error messages by explaining potential causes and suggesting actionable fixes [68].
- Accelerate debugging by enabling faster bug identification and early defect detection via recognizing patterns/errors developers may miss at manual check [70].
- Eliminate the need to consult extensive documentation [58].

## Risks overview
**Covers:** §6.2 and Table 9

| Theme | Summary |
|---|---|
| Fail to meet requirements | Often do not meet functional or non-functional requirements [60, 63]; not all outputs have good accuracy [82, 84]; limited controllability [63]; out of context [63, 68]; over-deliver with too much information or repetitive code [63, 73]; code generation correctness ranges from 31–65% [78] |
| Promote over-reliance and cognitive offloading | Diminishing critical thinking among novices and students [61, 69, 88]; automation complacency reported [72]; worry about skill erosion and loss of creativity [64]; recommend cautious informed use emphasizing interactive engagement over passive acceptance [57, 69, 83] |
| Limit code quality | Concerns about quality/accuracy of generated code [58, 71]; vulnerabilities and bugs if developer overestimates tool [68]; may not yield better code quality [57, 75] |
| Disrupt the flow | Unwanted suggestions [82]; interface switching [73]; verbose answers [73]; inadequate suggestion speed [73]; competing suggestions from multiple tools [54]; developers spend average 51.5% of coding time in LLM interaction states [71]; notification fatigue in human-AI teams [53] |
| Reduce team collaboration | Risk of hindering collaboration/communication [56]; traditional help channels less active as developers prefer AI [64]; loss of organic conversations and synergy [64]; need to study human-human and human-agent collaboration impacts [52] |

Table 9 lists five risk categories: limit code quality, fail to meet requirements, promote over-reliance and cognitive offloading, reduce team collaboration, and disrupt the flow.

## Fail to meet requirements
**Covers:** §6.2.1

- Not all LLM-assistant suggestions are accurate [82].
- Survey participants in [60, 63] mention assistants often fail both functional and non-functional requirements.
- Perceived as difficult to control [63]; responses out of context [63, 68] or over-deliver with too much information or repetitive code [63, 73].
- 50% of participants report missing or misunderstanding the requirement context as the two main issues with ChatGPT 3.5 [68].
- Generic or inaccurate suggestions require extra modification effort, leading to iterative prompt refinement and learning to interact effectively [84].
- Benchmarking: correctness from 31.1% (Amazon CodeWhisperer) to 65.2% (ChatGPT) [78].

## Promote over-reliance and cognitive offloading
**Covers:** §6.2.2

- Heavy reliance and excessive trust raise concerns about erosion of critical thinking, especially for novices and students [61, 69, 88].
- [88] develops an AI tutor limiting direct ChatGPT interaction via predefined prompts to promote critical thinking; students still worried post-experiment that reliance might hinder learning progress [88].
- Among professionals: programming exam with Google Bard [72] observes all three Parasuraman and Manzey [102] automation-complacency characteristics: human monitoring of an automated system, infrequent monitoring, and degraded performance.
- Survey respondents express overreliance concerns, reporting diminished ability to think independently [64].
- Studies advocate interactive, reflective engagement with outputs [57], caution against blind trust [69], encourage understanding capabilities and limitations; balancing AI support with developer competence remains an open challenge [83].
