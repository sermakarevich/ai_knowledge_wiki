> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Phase 2 Experiment Design
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
---
## Recruitment and familiarity split
**Covers:** Phase 2 recruitment (chunk 04)

Participants were recruited again through convenience sampling, with Phase 1 participants invited back; only five were available and agreed to return, and five additional individuals were recruited via internal Slack channels to reach ten total. Of the ten, four belonged to the team responsible for the pull requests used in the experiment and six were from other teams. The code used originated from Team A, the team of the familiar participants. Table II (in source) lists roles and team affiliations. The familiarity split was deliberate: Phase 1 interviews had indicated limited contextual knowledge harms review quality, so measuring AI reliance across familiar vs. unfamiliar groups was expected to yield further insights.

## Experiment setup and mode rationale
**Covers:** Experiment setup; Mode A / Mode B design (chunk 04)

The field experiment evaluated developer experience with LLM assistance under two modes chosen from Phase 1 findings, where developers most frequently wanted clearer up-front summaries plus on-demand explanations of architectural or contextual details. Each iteration had a single participant do a traditional review in their familiar environment with usual tools, plus the LLM review assistant (Fig. 2). The task was two reviews on different PRs with a different mode each, under conditions mirroring normal work as closely as possible.

## Mode A: Co-Reviewer
**Covers:** Mode A definition (chunk 04)

In Mode A the AI automatically generated a summary of the code under review, "highlighting major changes and any potential points of interest or concern, before the reviewer started their own examination." The reviewer used this to guide the review and could ask follow-up questions or "query the AI for clarification or more details about the summarized areas." This mode "directly targeted the challenge previously identified as lacking immediate context, particularly for large or complex PRs."

## Mode B: Interactive Assistant
**Covers:** Mode B definition (chunk 04)

In Mode B the reviewer "reviewed the code in their typical manner" with no proactive summary; the assistant "only responded when explicitly prompted." Reviewers were encouraged to ask "targeted queries rather than requesting an overall summary," covering specific code parts or higher-level architectural questions. This reflected Phase 1 feedback for a lightweight on-demand tool and addressed related studies [5], "where automatically highlighted lines can cause reviewers to miss other important areas" — keeping the AI passive let reviewers "maintained their usual workflow and examined the entire codebase without unconsciously depending on the AI's initial hints."

## PR selection, pilot, and rotation
**Covers:** PR selection, pilot run, counterbalancing (chunk 04)

Two PRs of similar size and complexity from the WirelessCar codebase were selected, each with "a moderate amount of change, requiring genuine reviewer effort without being excessively large or trivial." Before the first session a pilot run with two internal developers outside the main pool walked through the tool, review task, and modes, then informally tested the selected PRs to assess PR suitability, detect usability or technical issues, and check whether introduction and guidance were clear. Each participant reviewed both PRs with alternating modes, and mode-to-PR assignment was rotated across participants to mitigate ordering effects.

## Session procedure and data collection
**Covers:** Onboarding, sessions, post-interviews (chunk 04)

Before sessions each participant got a short onboarding briefing on tool features, study and experiment structure, the two modes, and prompting guidance, then completed the two review sessions consecutively. No in-depth feedback or direct assistance was given during sessions, though limited guidance was offered when needed (e.g. how to interact), and participants not meeting expectations with an answer were occasionally guided to rephrase or retry. Participants were encouraged to think aloud, "often verbalizing their reasoning, confirming the AI's suggestions, or commenting on its usefulness." Researchers were present to observe, record notes, and run post-session collection; afterward short semi-structured interviews reflected on the two modes versus the regular workflow.
