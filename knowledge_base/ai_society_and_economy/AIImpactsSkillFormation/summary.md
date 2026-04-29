# How AI Impacts Skill Formation

**Paper:** [How AI Impacts Skill Formation (Judy Hanwen Shen, Alex Tamkin, 2026)](https://arxiv.org/pdf/2601.20245)

## Human Readable TL;DR

Imagine you need to learn a new recipe. One group cooks with a chef constantly telling them exactly what to do; another group fumbles through cookbooks, makes mistakes, and figures it out themselves. Afterwards, both groups get tested on the recipe without any help. The second group -- the ones who struggled -- ends up understanding the recipe much better. This study ran that same experiment with software engineers learning a new programming library, and found that using an AI assistant made people finish tasks slightly faster but left them with meaningful gaps in what they actually learned, especially when it came to fixing bugs.

## TL;DR

A between-subjects randomized controlled trial with 52 professional Python developers learning the Trio async library found that AI assistance (GPT-4o chat) did **not** produce a statistically significant speed-up on task completion (p=0.391), but caused a significant 17% drop in post-task quiz scores measuring conceptual understanding, code reading, and debugging (Cohen's d=0.738, p=0.01). The largest deficit was in debugging. Qualitative analysis of screen recordings identified six AI interaction patterns; those involving conceptual inquiry or requesting explanations preserved learning, while delegation-style patterns collapsed it.

---

## Problem & Motivation

Prior research on AI coding assistants focuses almost entirely on the **output** -- speed, lines of code, tasks completed -- and consistently reports productivity gains, especially for novices. But professionals constantly need to acquire new skills on the job (new libraries, new frameworks), and no controlled work has measured whether AI assistance during that learning phase actually builds lasting competence or just hands people the answer. This matters because human supervision of AI-generated code depends on the supervisor having the underlying skills -- particularly debugging -- to catch errors. If AI speeds up task completion at the cost of skill formation, the field is building a workforce that cannot safely oversee its own tools.

---

## Main Original Ideas

1. **Skill formation as a distinct axis from productivity.** The paper explicitly separates "did the task get done faster" (RQ1) from "did the person learn anything" (RQ2), and designs an evaluation quiz administered **without AI** to measure only the retained skills. This reframing -- productivity and learning as potentially opposing outcomes -- is the paper's central conceptual move.

2. **Controlled experiment on new-skill acquisition.** Unlike observational studies of AI coding usage, the authors run a between-subjects RCT where all participants had never used the Trio library, ensuring the experiment measures genuine skill acquisition rather than recall of pre-existing knowledge.

3. **Typology of six AI interaction patterns.** From manual annotation of screen recordings, the authors derive six distinct usage styles (AI Delegation, Progressive Reliance, Iterative Debugging, Conceptual Inquiry, Hybrid Code-Explanation, Generation-Then-Comprehension) and map each to learning outcomes. This is a mechanistic account of **why** AI hurts learning in some cases but not others.

4. **Error exposure as the causal channel.** The control group encountered a median of 3 errors vs. 1 for the AI group, and specifically faced more Trio-specific errors. The paper argues independent error resolution is what drives skill formation, which AI shortcuts.

5. **Debugging-specific deficit.** Exploratory breakdown shows the largest skill gap is in debugging questions, the smallest in code reading -- directly identifying the skills most at risk from AI assistance.

---

## Key Findings

| Measure | Control (no AI) | Treatment (AI) | Significance |
|---|---|---|---|
| Task completion time | ~23 min avg | slightly lower avg | p = 0.391 (**not significant**) |
| Quiz score (out of 27) | higher | **4.15 points lower (17%)** | Cohen's d = 0.738, **p = 0.01** |
| Errors encountered (median) | **3** | 1 | -- |
| Fastest AI subgroup (full delegation, ~20%) | -- | 19.5 min | substantial speed-up but worst learning |

- Productivity gains from AI were highly **heterogeneous**: some AI users spent up to 11 of 35 available minutes composing queries, negating any generation speed-up.
- The skill deficit held **across all prior experience levels**, suggesting the effect is robust to participant background.
- Interaction patterns split cleanly: delegation-style patterns averaged <40% on the quiz; inquiry/explanation patterns averaged >65%, with Conceptual Inquiry reaching 86%.
- Control participants described feeling they understood Trio; AI participants reported feeling "lazy" and acknowledged "gaps in understanding."
- AI participants spent considerably less time actively coding -- time shifted to query composition and reading AI output.

---

## Suggestions & Future Directions

1. **Study agentic AI coding tools**, which require even less human involvement than chat-based assistants, as a likely lower bound for cognitive engagement and learning.
2. **Run longitudinal studies** in real professional settings to measure skill formation over months or years rather than a 35-minute window.
3. **Use participants with genuine job incentives** to learn the target library, to see whether real stakes change engagement and outcomes.
4. **Investigate prompting fluency as a mediator** -- different users may get different learning outcomes partly due to how well they prompt.
5. **Design alternative skill evaluations**, such as performance on a subsequent independent coding task or code design challenges, beyond a quiz.
6. **Compare AI assistance to human assistance** (mentor, tutor) to identify which elements of learning support are specifically lost or preserved.
7. **Design interventions** (UI nudges, prompting scaffolds) that push users toward the high-scoring interaction patterns (conceptual inquiry, explanation-seeking).

---

## Authors & Institutions

Judy Hanwen Shen (Anthropic Fellows Program), Alex Tamkin (Anthropic).
