> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Tool Implementation: RAG Pipeline and Agentic Structure
**In one sentence:** The artifact's source code is freely available under GPLv3 and built with a RAG pipeline where `search_requirements` supplies the motivating Jira ticket and Mode A adds a `start_review` sub-agent that reviews the full injected PR data rather than retrieving it via a query engine.
## Key points
- The source code for the artifact is freely available under GPLv3, with a reference to https://www.llamaindex.ai/.
- The tool `search_requirements` contains the feature requirement (the Jira ticket) motivating the PR.
- In Mode A (Co-Reviewer), a fourth tool, `start_review`, was added, containing a sub-agent designed to perform an initial, structured code review based on the full PR data and guided by a detailed review-specific prompt.
- Unlike the main agent, the `start_review` sub-agent did not use `search_pr`, because all PR data was injected into its initial context via a prompt.
- The stated rationale is that injection ensures the agent considers everything in the PR data and examines each file change, whereas retrieving PR data via a query engine might not consider all the data as required for a complete review of all changes; the agentic structure is shown in Fig. 3.
- The same chunk body also carries Phase 1 results material: six themes emerged from thematic analysis (Table III), and a separate Table IV lists four Phase 2 themes (Accuracy/Reliability/Trust; Efficiency/Thoroughness; Integration Expectations/Limitations; Usage Contexts/Interaction Patterns).
---
## Artifact availability
The chunk states that the source code for the artifact is freely available under GPLv3, with the reference `https://www.llamaindex.ai/`.

## RAG tools: search_requirements
- `search_requirements`: contains the feature requirement (the Jira ticket) motivating the PR.

## Mode A (Co-Reviewer): start_review sub-agent
- In Mode A (Co-Reviewer), a fourth tool, `start_review`, was added.
- This tool contained a sub-agent designed to perform an initial, structured code review based on the full PR data and guided by a detailed review-specific prompt.
- Unlike the main agent, this sub-agent did not use `search_pr`, as all PR data was injected into its initial context via a prompt.
- This ensured that the agent considers everything in the PR data and examines each file change.
- By retrieving the PR data via a query engine, the agent might not consider all the data as required when generating a complete code review of all changes.
- The agentic structure for this setup is shown in Fig. 3.

## Phase 1 results material present in this chunk
- Six themes emerged from the thematic analysis of the qualitative data (Table III).
- Observed review process is described as similar to typical asynchronous, tool-supported modern code review (MCR), but with informal assignment/communication sometimes through Slack introducing variability, plus heavy reliance on domain experts for critical components.
- Common challenges include delayed reviews, large/complex PRs causing superficial reviews or delays, context switching, and missing context about why a change was made.
- Current AI use covers GitHub Copilot (https://github.com/features/copilot) and ChatGPT (https://chatgpt.com/) for boilerplate, syntax, and documentation; teams allowed to use them only via enterprise subscription where data is not used for training; no formal integration into code review except occasional informal pasting into ChatGPT.
- Potential AI use cases mentioned include summarizing PR changes/descriptions and validating requirements, plus detecting hidden bugs/vulnerabilities such as race conditions or dependency issues.

### Verbatim quotes in chunk
- "As soon as you need to context switch, even if it's just a three-minute thing, it's 20 minutes of lost time." [P7]
- "[...] as to help to create the boilerplate stuff, it's outstanding, right? I mean, you do it in 30 seconds instead of a couple of hours. So I try to use it as much as possible during the development process." [P7]
- "Sometimes you need to ping people more often, and sometimes the PR is very big, so people don't dare to pick it up" [P2]
- "When you create the pull request, an AI bot could say, 'Hey, you're trying to achieve this—do you want this as your summary or description?" [P5]
- "As I see it, they were quite accurate [...] It was quite nice, not all of them, but a lot of them." [P9]

### Table III — Identified themes from Phase 1 interview data
| Theme | Description |
|---|---|
| Informal Review Process and Practices | Describes how teams coordinate and manage code reviews in practice, including informal communication, tool use, and the absence of structured processes or metrics. |
| Review Strategies and Evaluation Focus | Captures what developers focus on during the actual code review process. |
| Learning, Knowledge, and Review Expertise | Explores how code reviews serve as opportunities for learning and knowledge sharing within teams. It also captures the role of reviewer expertise in conducting effective reviews and the challenges that arise when reviewers lack sufficient understanding of the codebase or architecture. |
| Code Review Challenges | Identifies recurring challenges and inefficiencies encountered in the code review process. |
| Current AI adoption | Describes the current state of AI tool usage in development and code review. |
| Possible AI adoption in code reviews | Describes developers' expectations, suggestions, and concerns regarding future AI assistance in code reviews. |

### Table IV — Identified themes from Phase 2 data
| Theme | Description |
|---|---|
| Accuracy, Reliability, and Trust | Focuses on the perceived correctness of AI-generated feedback, concerns about over-reliance, and varying levels of trust in the assistant's recommendations. |
| Efficiency and Thoroughness | Captures how the assistant affects review speed, cognitive load, issue detection, and the overall thoroughness of the code review process. |
| Integration Expectations and Limitations | Highlights developer expectations for seamless integration, responsive design, and context-aware suggestions, while also surfacing frustrations related to current UX and tooling limitations. |
| Usage Contexts and Interaction Patterns | Describes how interaction with the assistant varied based on review context, including preferences for different modes, alternative usage strategies, and team-specific practices. |

**Covers:** Prototype chat UI, RAG pipeline, and agentic tool structure (chunk 05-source-code-for-the-artifact-is; note: chunk body also contains interleaved Phase 1/Phase 2 results text and Tables III–IV as extracted above).
