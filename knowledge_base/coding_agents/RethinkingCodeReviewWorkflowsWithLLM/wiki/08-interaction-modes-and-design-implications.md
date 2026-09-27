> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Interaction Modes and Design Implications
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
---
## Mode A for orientation in unfamiliar code
**Covers:** Mode A orientation findings (chunk 08)

Many participants found Mode A (Co-Reviewer) especially helpful for getting oriented in a pull request, describing the high-level summaries and suggestions at the beginning of the review as useful for gaining quick context, particularly in unfamiliar or complex codebases:

> "I prefer this one [Mode A] where you actually get the overview directly [...] it had a lot of good pointers, that it already found." [P12]

> "The first engine [Mode A] that gave me a breakdown of everything [...] that was quite clever, and I would gladly use that." [P7]

## Mode A for low-risk and large PRs
**Covers:** Mode A low-risk and large-PRs findings (chunk 08)

Mode A was described as particularly useful for low-risk PRs:

> "Let's say the change is relatively small and it's not causing any risk, then I would definitely go with the first one [Mode A], where I let AI do most of the work." [P11]

Participants also frequently noted that Mode A was especially helpful for large PRs:

> "You start out with it just to sum up what the code is doing. Then I look for issues, and then I can ask, 'Are there any further issues?" [P3]

> "Especially for large PRs, it's nice to get the breakdown on what's happening [...] because usually, you always have to do that sort of manually anyway." [P3]

## Scale concern
**Covers:** Scalability concern (chunk 08)

One participant expressed concerns about the assistant's ability to handle very large codebases or complex business logic:

> "I think it's going to be a bottleneck for such things, because there will be so many moving parts in it, so much business logic going around." [P1]

## Situational and combined preferences
**Covers:** Mode combination preferences (chunk 08)

In some cases, participants preferred a combination of both modes or expressed that the preferred interaction mode depended on the situation:

> "I think I'm 50/50 [...] both are useful. One is on demand, the other one is on its own." [P1]

## Extra usage patterns: pre-review aid and validate-after-human-review
**Covers:** Proposed usage patterns beyond study design (chunk 08)

Several participants proposed additional usage patterns not strictly defined by the study design. Some saw Mode A as useful for the author before submitting the PR, rather than during review:

> "I feel it might not be as much of a review help. I think it might be a pre-review help." [P10]

Others proposed an alternative interaction mode where engineers conducted a human-led review first and then used the assistant to validate or catch anything they might have missed.

## VI. Implications
**Covers:** Section VI Implications (chunk 08)

First, AI assistance should be embedded within developers' existing tools (such as GitHub, GitLab, IDEs, or Slack) to minimize friction and support natural adoption. Second, output must be concise, well-structured, and actionable, prioritizing critical findings with precise references to affected files and lines. Fast response times are essential to preserve reviewer flow, although more comprehensive agentic reviews may be acceptable when integrated into automated pipelines. Supporting both proactive (AI-led summaries) and reactive (on-demand Q&A) modes of interaction is key, with a general developer preference for AI-led summaries in large or unfamiliar pull requests. For meaningful support, the assistant must be context-aware and have access to relevant information such as code diffs, source files, and requirement documents; while the tool addressed this via a retrieval-augmented setup, participants still highlighted the need for deeper contextual integration. Finally, an LLM-enabled assistant also shows promise as a pre-review aid, helping authors catch simple issues before submitting a pull request, thus improving code quality upstream in the development lifecycle.

## VII. Concluding Remarks
**Covers:** Section VII Concluding Remarks (chunk 08)

This paper presented a field study and field experiment conducted at WirelessCar to explore the integration of Large Language Models (LLMs) into real-world code review workflows. The study surfaces persistent challenges in current review practices, such as context switching, reviewer fatigue, inconsistent review depth, and developer perceptions of how LLMs can augment the process. By evaluating two interaction modes (AI-led reviews and on-demand assistance), the authors found that developers generally value AI-generated summaries and contextual clarifications, particularly in large or unfamiliar pull requests. However, concerns around trust, false positives, response latency, and integration friction remain. While most participants preferred the AI-led mode in unfamiliar or low-risk scenarios, preferences were context-dependent, with some favoring human-led reviews when code familiarity or criticality increased.

This study contributes practical insights into how LLMs can complement human reviewers, rather than replace them. The findings suggest a promising path forward: integrating AI assistance more tightly into existing development environments, improving response quality and speed, and offering adaptive interaction modes tailored to developer needs.
