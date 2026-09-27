> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Phase 1 Findings: Challenges and AI Use Cases
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
---
## Expected AI strength: hard-to-spot defects
**Covers:** Phase 1 expected use cases; Phase 2 results intro (chunk 06)

> "An AI would probably be able to identify a race condition, for instance, which, as I said, is an example that's borderline impossible to catch on the fly. In three minutes, you're never going to find that." [P7]

Table IV (in source) provides an overview of the Phase 2 themes along with descriptions of the themes.

## Drawbacks: security risks and false positives
**Covers:** Phase 1 drawbacks (chunk 06)

Some interviewees mentioned potential drawbacks of integrating AI into code review: mostly concerns about security risks and false positives, which could reduce reviewer trust and divert attention from real issues.

> "The problem with those kinds of checks is that, if they're not good enough, you stop reading them. We see that all the time, you get flooded with false positives, and then you miss the real issues because you start ignoring the feedback." [P7]

## 1) Accuracy, Reliability, and Trust
**Covers:** Phase 2 theme 1 (chunk 06)

Participants frequently commented on accuracy and how it influenced trust. Several described the assistant as generally accurate and capable of identifying relevant issues. In multiple cases output was described as confirming the developer's own thoughts or surfacing something they might not have otherwise caught. Observation notes reflect this: one session noting "the user said the AI caught exactly what he was looking for in a certain file"; another where the reviewer remarked "the summary gave something that he would not have seen."

Several participants also reported incorrect or unclear suggestions. One questioned whether the tool was even "doing what it was asked," while another described it incorrectly flagging a missing import.

> "Sometimes it says some slightly strange things." [P8]

When asked about concerns, several warned of over-relying on the assistant, especially in Mode A where the assistant led the review:

> "It feels like I might get a bit colored by getting the improvements from the LLM [...] I feel like maybe I could miss something else, because I would focus on those improvements a lot." [P3]

Not all saw the assistant as risky; some viewed it as low-stakes when use remained optional, even if not always accurate:

> "As long as there's an opt-out option, there's no real harm in it." [P5]

> "If we miss 10 [issues] today, we might miss two with a tool like this." [P9]

Trust emerged as key: for the tool to be useful or even used, it must be trusted, but not blindly, since misplaced trust leads to wasted effort if inaccurate:

> "So I think that worked really well, especially with larger [PRs] [...] you can at least use it if you trust it." [P7]

> "I could go on for hours, just to realize I can never do this. Then I've just lost a few hours trying to pursue something that wasn't possible." [P5]

## 2) Efficiency and Thoroughness
**Covers:** Phase 2 theme 2 (chunk 06)

A strong theme was AI impact on efficiency and review thoroughness/quality. Developers reported the assistant could speed up review, reduce workload on tedious tasks, and potentially catch more issues, although some remarked it sometimes focuses on low-priority findings, introducing noise.

One participant liked the requirements integration:

> "But I really like the integration with the requirements part, because if I open up [a PR] and I don't know what it's about. [...] The first thing I do every time is I open the [Jira] ticket anyway, because I need to see what is supposed to have been achieved here. So I think that's a really nice functionality to have" [P3]

However, some noted the assistant occasionally surfaced low-priority or unclear findings; review sessions also showed participants sometimes had difficulty distinguishing important findings from minor ones, especially in lengthy assistant summaries.

## 3) Design Expectations and Limitations
**Covers:** Phase 2 theme 3 (chunk 06)

Many participants shared expectations about how an AI review assistant should behave and be integrated. A recurring theme was seamless integration into existing workflows and tools. Rather than switching to a new interface, several preferred access directly from familiar environments like GitHub, Slack, or IDEs:

> "I think most of the developers don't want to use something new, like a [new] UI, but rather have an integration to what exists." [P11]

Building on this, another participant preferred assistant comments embedded directly into GitHub's interface with expandable in-line comment boxes, plus ability to ask further questions in a chat interface. Yet another described having it in the pipeline through a Slack bot as useful.
