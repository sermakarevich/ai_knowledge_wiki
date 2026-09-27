> [[index|Wiki]] | [[summary|Summary]]

# Rethinking Code Review Workflows with LLM — Digest

## 1. [[wiki/01-rethinking-code-review-workflows-with-llm|Rethinking Code Review Workflows with LLM]]

**In one sentence:** The chunk body provided for this page is truncated/garbled, containing only the paper title, author/affiliation block, and a cut-off abstract fragment, so no complete argument can be extracted from it.

## Key points

- The chunk contains the full paper title "Rethinking Code Review Workflows with LLM Assistance: An Empirical Study" and nothing else complete.
- The chunk lists authors Fannar Steinn ADalsteinsson, Björn Borgar Magnússon, Mislav Milicevic, Adam Nirving Davidsson, and Chih-Hong Cheng.
- The chunk lists affiliations WirelessCar Sweden AB, Chalmers University of Technology, and University of Gothenburg, all in Gothenburg, Sweden.
- The only body text is a cut-off abstract fragment beginning "Abstract—Code reviews are a critical yet time-consuming" and ending mid-sentence at "diagnostic and one exploratory. The first question (RQ1)".
- No methods, numbers, results, or conclusions are present in the chunk, so none are reported here to avoid inventing content.
- Per the plan, the full abstract and study framing belong to this page once a complete chunk is available.

## 2. [[wiki/02-background-and-research-questions|Background, Related Work, and Research Questions]]

**In one sentence:** The paper frames code review as scaling-strained but essential, surveys LLM-for-review work as missing the preferred human–AI interaction question, and launches a two-phase WirelessCar study (RQ1: current practices/challenges/AI opportunities; RQ2: perceived interaction preference) built on interviews plus a two-mode field experiment.

## Key points

- Code review is positioned as a cornerstone for quality, defect detection, and knowledge sharing that now struggles with inefficiencies, reviewer fatigue, and inconsistent outcomes as systems scale and cycles accelerate.
- LLMs are credited with strong results on code generation and bug detection and smooth integration into coding activities, but their full potential in code review remains underexplored.
- Prior LLM-for-review work covers replicating reviewer changes, controlled issue-detection/time effects, emotional responses to AI vs human feedback, large-scale standards enforcement, fine-tuning for detection, and multi-agent autonomous review — leaving the preferred collaboration interaction as the gap.
- The study's stance is support-not-replace: LLMs are not treated as human replacements because they remain prone to hallucinations, so RQ2 focuses on practical integration strategies.
- RQ1 is diagnostic (current practices, challenges, expectations, where AI can help and the automation–human balance); RQ2 is exploratory (trust, satisfaction, barriers, usability, and preferred interaction mode).
- The design is two-phase at WirelessCar Sweden AB, where some but not all teams may use AI: Phase 1 exploratory interviews yielding RQ1, then Phase 2 field experiment with AI-led co-reviewer vs interactive assistant yielding RQ2.
- Both phases use semi-structured interviews with thematic analysis, and Phase 2 deliberately emphasizes qualitative interaction value over performance metrics or tool comparisons.

## 3. [[wiki/03-phase1-participants-and-setup|Phase 1 Participants and Setup]]

**In one sentence:** Phase 1 lists ten participants (P1, P2, P3, P5, P7, P8, P9, P10, P11, P12) with their roles and team assignments, anchored by P1 as the Quality Assurance Specialist on Team A.

## Key points

- The chunk lists 10 participants: P1, P2, P3, P5, P7, P8, P9, P10, P11, and P12.
- P1 is the Quality Assurance Specialist and belongs to Team A.
- P2 is the Application Developer on Team A.
- P5 is the Security Engineer on Team B, the only security role in the list.
- Seven participants are Software Engineers: P3, P7, P8, P9, P10, P11, and P12.
- Team A holds four participants (P1, P2, P3, P9), the largest single-team group in the table.
- Remaining assignments are P7 on Teams D & B, P8 and P10 on Team E, P11 on Team F, and P12 on Team G.

## 4. [[wiki/04-phase2-experiment-design|Phase 2 Experiment Design]]

**In one sentence:** Phase 2 ran a controlled field experiment with 10 developers (4 familiar, 6 unfamiliar) each reviewing two WirelessCar PRs, one with proactive Mode A summaries and one with passive on-demand Mode B assistance, with rotated assignment and think-aloud plus post-session interviews.

## Key points

- 10 participants total: 5 returnees from Phase 1 via convenience sampling plus 5 new recruits via internal Slack channels.
- 4 participants belonged to the team owning the reviewed PRs and 6 came from other teams, enabling comparison across codebase familiarity levels.
- Each participant performed two code reviews on two different pull requests from separate company repositories, using Mode A for one and Mode B for the other.
- Mode A (Co-Reviewer) auto-generated an up-front summary highlighting major changes and potential concerns before the reviewer started, plus follow-up Q&A.
- Mode B (Interactive Assistant) gave no proactive summary and responded only when explicitly prompted with targeted clarification or architectural questions.
- The two PRs were selected from the WirelessCar codebase for similar size and complexity with a moderate amount of change, and mode-to-PR assignment was rotated to mitigate ordering effects.
- A pilot run with 2 internal developers outside the main pool tested the tool, PR suitability, and onboarding clarity before the real sessions.
- Sessions mirrored normal working conditions in familiar environments, used think-aloud protocol with researcher observation, and ended with short semi-structured interviews comparing modes to regular workflow.

## 5. [[wiki/05-tool-implementation-rag-pipeline|Tool Implementation: RAG Pipeline and Agentic Structure]]

**In one sentence:** The artifact's source code is freely available under GPLv3 and built with a RAG pipeline where `search_requirements` supplies the motivating Jira ticket and Mode A adds a `start_review` sub-agent that reviews the full injected PR data rather than retrieving it via a query engine.

## Key points

- The source code for the artifact is freely available under GPLv3, with a reference to https://www.llamaindex.ai/.
- The tool `search_requirements` contains the feature requirement (the Jira ticket) motivating the PR.
- In Mode A (Co-Reviewer), a fourth tool, `start_review`, was added, containing a sub-agent designed to perform an initial, structured code review based on the full PR data and guided by a detailed review-specific prompt.
- Unlike the main agent, the `start_review` sub-agent did not use `search_pr`, because all PR data was injected into its initial context via a prompt.
- The stated rationale is that injection ensures the agent considers everything in the PR data and examines each file change, whereas retrieving PR data via a query engine might not consider all the data as required for a complete review of all changes; the agentic structure is shown in Fig. 3.
- The same chunk body also carries Phase 1 results material: six themes emerged from thematic analysis (Table III), and a separate Table IV lists four Phase 2 themes (Accuracy/Reliability/Trust; Efficiency/Thoroughness; Integration Expectations/Limitations; Usage Contexts/Interaction Patterns).

## 6. [[wiki/06-phase1-findings-challenges-and-ai-use-cases|Phase 1 Findings: Challenges and AI Use Cases]]

**In one sentence:** Interviewees said AI could catch hard-to-spot defects like race conditions and confirm or extend reviewer judgment, but warned that false positives, over-reliance (especially in Mode A), and poor integration could erode trust, while Phase 2 sessions showed the assistant was often accurate yet sometimes strange or noisy and developers wanted it embedded in GitHub, Slack, or IDEs.

## Key points

- AI was expected to catch defects "borderline impossible to catch on the fly," e.g. race conditions missed in a three-minute review [P7].
- Drawbacks raised were security risks and false positives that reduce trust and divert attention from real issues.
- Phase 2 participants described the assistant as generally accurate, confirming their own thoughts or surfacing issues they would not have seen, including session notes that "the AI caught exactly what he was looking for" and "the summary gave something that he would not have seen."
- Participants also reported incorrect or unclear suggestions, including wrongly flagging a missing import and "slightly strange things" [P8], with one questioning whether the tool was even "doing what it was asked."
- Over-reliance was a concern especially in Mode A where the assistant led, with [P3] fearing focus on LLM improvements could make them miss something else.
- Trust was framed as necessary but not blind: the tool is low-stakes if optional ("As long as there's an opt-out option, there's no real harm" [P5]; "If we miss 10 [issues] today, we might miss two with a tool like this" [P9]), yet misplaced trust wastes hours chasing impossible suggestions [P5] and larger PRs are usable "if you trust it" [P7].
- On efficiency, developers said the assistant could speed up reviews, reduce tedious workload, and catch more issues, but sometimes surfaced low-priority or unclear findings that were hard to separate from important ones in lengthy summaries.
- On integration, developers wanted no new UI but access inside GitHub, Slack, or IDEs, including in-line expandable GitHub comments plus chat follow-ups, a Slack pipeline bot, and liked requirements/Jira context integration [P3][P11].

## 7. [[wiki/07-phase2-findings-trust-and-integration|Phase 2 Findings — Trust and Integration]]

**In one sentence:** Participants said the assistant improved review quality and reduced effort, especially on large PRs and for newcomers, but its usefulness was limited by missing broader context, overly long output, slow response times, and weak workflow integration.

## Key points

- Participants reported the assistant surfaced findings they would miss manually, including potential deadlocks or race conditions on large PRs a human given 15 minutes could not cover well.
- The assistant reduced review effort by removing the need to search through the codebase or external documentation, and could suggest documentation updates aligning with PR changes.
- Interaction quality depended partly on the reviewer's own prompting skill, with one participant noting they needed to learn to ask more detailed questions.
- Many limitations were traced to missing broader context such as architectural documentation, internal conventions, JIRA tickets, READMEs, and connected repositories.
- Participants wanted tighter workflow integration, e.g. a Slack auto bot triggered on each message with the full review dropped as a message under that thread.
- Output was criticised as overly long and hard to scan; one participant wanted the file and line number listed specifically and briefly, and slow response times were cited as a major adoption barrier.
- Mode A (Co-Reviewer) was seen as valuable for newcomers learning a team/codebase and as a fallback in teams with low review standards or pair-programming preferences, while Mode B (Interactive Assistant) was preferred when reviewers already knew the codebase or wanted full control.

## 8. [[wiki/08-interaction-modes-and-design-implications|Interaction Modes and Design Implications]]

**In one sentence:** Participants valued Mode A (Co-Reviewer) AI-led summaries for orientation in unfamiliar, large, or low-risk PRs but preferred the interaction mode situationally, proposing pre-review and human-led-then-validate uses, which leads to implications around embedded, concise, fast, context-aware, dual-mode assistance and a conclusion that LLMs complement rather than replace reviewers.

## Key points

- Mode A high-level summaries and suggestions at the start of review gave quick context, especially in unfamiliar or complex codebases [P12][P7].
- Mode A was preferred for low-risk PRs where participants would let AI do most of the work [P11].
- Mode A was described as especially helpful for large PRs because it replaces the manual breakdown reviewers otherwise do [P3].
- One participant worried Mode A would bottleneck on very large codebases or complex business logic with many moving parts [P1].
- Preference was often situational or split, e.g. "50/50 [...] both are useful. One is on demand, the other one is on its own" [P1].
- Proposed extra patterns were Mode A as author pre-review aid before submitting the PR [P10], and human-led review first with the assistant validating or catching missed issues.
- Implications call for embedding in GitHub, GitLab, IDEs, or Slack; concise, structured, actionable output with precise file/line references; fast responses (with slower agentic reviews acceptable in pipelines); both proactive and reactive modes; and context-awareness via diffs, source files, and requirements (RAG used, deeper integration still wanted).
- Concluding remarks report a WirelessCar field study plus experiment: developers value AI summaries and clarifications in large or unfamiliar PRs, most preferred AI-led mode in unfamiliar or low-risk cases, some favored human-led review as familiarity or criticality rose, while trust, false positives, latency, and integration friction remain.

## The argument in five moves

1. Code review is essential but strained by scale, fatigue, and inconsistency, and prior LLM-for-review work leaves open the preferred human–AI interaction — so the study asks diagnostically what hurts and where AI could help (RQ1) and exploratorily which interaction developers prefer (RQ2).
2. Exploratory interviews at WirelessCar surface informal, expertise-dependent review practice plagued by delays, large PRs, context switching, and missing rationale, alongside informal Copilot/ChatGPT use and a wish list of AI summaries, requirements validation, and hidden-defect detection.
3. Those wishes are operationalised into a field experiment contrasting proactive Mode A (Co-Reviewer up-front summary plus Q&A) with passive Mode B (on-demand assistant only), run across familiar and unfamiliar reviewers on matched real PRs with rotated assignment, think-aloud observation, and post-session interviews, powered by a RAG tool with Jira context and a full-context `start_review` sub-agent for Mode A.
4. In use the assistant often confirms judgment or catches what humans miss (race conditions, deadlocks on large PRs) and cuts search effort, yet it also produces strange, noisy, or low-priority findings, invites over-reliance especially when AI leads, and is held back by missing broader context, overlong output, slow responses, and separation from GitHub/Slack/IDE workflows.
5. Developers therefore prefer the mode situationally — AI-led orientation for unfamiliar, large, low-risk, or newcomer reviews (plus proposed author pre-review and human-first-then-validate patterns), on-demand assistance where familiarity or control is high — yielding design implications (embedded, concise with file/line refs, fast, context-aware, dual-mode, pre-review capable) and the conclusion that LLMs complement rather than replace reviewers, pending trust, accuracy, latency, and integration fixes.
