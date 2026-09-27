---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Designing Proactive Thought Partners for Writing

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

> Note: `critical_thinking.md` was missing at time of writing, so this set contains 9 content questions only; evaluation question omitted.

### Q1. Define proactive thought partners and place them in Figure 1 design space.
> [!tip]- Answer
> Proactive thought partners are AI assistants that take initiative to offer customizable higher-level cognitive support during writing without explicit prompting. Figure 1 maps initiative (reactive vs proactive) against level of support (textual vs cognitive), placing them in the proactive-plus-cognitive quadrant. See [[wiki/01-introduction-and-gap|Introduction]].

### Q2. Name the three event triggers in the probe and their default timings.
> [!tip]- Answer
> The probe uses Long Pause after 5s inactivity, Sentence End after sentence completion plus 1s idle, and Text Selection after selection plus 5s idle. All three are customizable and one or more can be enabled per partner. See [[wiki/03-technology-probe-system|Technology Probe]].

### Q3. What is the two-part format of a proactive suggestion?
> [!tip]- Answer
> Each suggestion pairs an acknowledgement of what the writer just did or may try next with a question-style suggestion tailored to context. The acknowledgement makes system understanding visible before guidance, following writing-feedback research. See [[wiki/03-technology-probe-system|Technology Probe]].

### Q4. Describe the engagement trio: ignore, inspire, execute.
> [!tip]- Answer
> Ignore means continuing to write while the floating tag fades after 15s with no explicit dismissal. Inspire means clicking the tag to expand the suggestion card for ideas or follow-up chat without changing the draft. Execute means clicking Help Me Write to insert or revise text directly with accept or revert control. See [[wiki/03-technology-probe-system|Technology Probe]].

### Q5. Summarize the study scale: participants, duration, sessions, and requirement.
> [!tip]- Answer
> Sixteen everyday writers with prior AI-for-writing experience joined a one-week deployment with a 60-minute onboarding, a 7-day diary, and a 60-minute exit interview. They completed 66 sessions (mean 4.13 per person), with substantive sessions defined as at least 20 minutes active writing or 300 words plus a self-contained piece. See [[wiki/04-user-study-method|User Study]].

### Q6. Why does the triggers versus heuristics split matter for timing?
> [!tip]- Answer
> Event triggers only mark broad candidate moments to check relevance, while contextual heuristics specify precise conditions for whether and which support appears. The split matters because one event maps to different states, such as a pause meaning stuck, concentrating, or reviewing. See [[wiki/02-related-work-and-design-goals|Related Work and Design Goals]].

### Q7. Why does question-framing preserve ownership compared with directives?
> [!tip]- Answer
> Question-style suggestions invite reflection while leaving the writer to decide whether and how to respond, unlike directives that prescribe a response. Participants reported questions kept everything under control and felt like partnership rather than instruction. See [[wiki/05-findings|Findings]].

### Q8. What breaks if the max-2 partner activation limit is removed?
> [!tip]- Answer
> Without the limit, multiple partners could fire at once and flood the peripheral panel, raising interruption cost and breaking the lightweight fading-tag design. It would also weaken the decision engine's role in selecting only the best-matching heuristics, reducing contextual alignment. See [[wiki/03-technology-probe-system|Technology Probe]].

### Q9. Design a thought partner for Sergii's agent-orchestration work using role, triggers, and heuristic.
> [!tip]- Answer
> A Fleet Review Partner could hold the role of challenging multi-agent plans for missing edge cases and unclear handoffs. Enable it on sentence end and text selection, with a heuristic such as intervening when a task plan lacks acceptance criteria or names no owner. See [[wiki/06-discussion-ethics-limitations|Discussion]].
