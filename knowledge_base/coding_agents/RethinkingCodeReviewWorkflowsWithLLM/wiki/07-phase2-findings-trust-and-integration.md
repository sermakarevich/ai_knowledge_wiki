> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Phase 2 Findings — Trust and Integration

**In one sentence:** Participants said the assistant improved review quality and reduced effort, especially on large PRs and for newcomers, but its usefulness was limited by missing broader context, overly long output, slow response times, and weak workflow integration.

## Key points
- Participants reported the assistant surfaced findings they would miss manually, including potential deadlocks or race conditions on large PRs a human given 15 minutes could not cover well.
- The assistant reduced review effort by removing the need to search through the codebase or external documentation, and could suggest documentation updates aligning with PR changes.
- Interaction quality depended partly on the reviewer's own prompting skill, with one participant noting they needed to learn to ask more detailed questions.
- Many limitations were traced to missing broader context such as architectural documentation, internal conventions, JIRA tickets, READMEs, and connected repositories.
- Participants wanted tighter workflow integration, e.g. a Slack auto bot triggered on each message with the full review dropped as a message under that thread.
- Output was criticised as overly long and hard to scan; one participant wanted the file and line number listed specifically and briefly, and slow response times were cited as a major adoption barrier.
- Mode A (Co-Reviewer) was seen as valuable for newcomers learning a team/codebase and as a fallback in teams with low review standards or pair-programming preferences, while Mode B (Interactive Assistant) was preferred when reviewers already knew the codebase or wanted full control.

---

## Review quality gains

Participants pointed to improvements in review quality beyond efficiency: the assistant could identify issues that might otherwise go unnoticed, particularly on large pull requests where a human reviewer cannot catch everything.

> "There are probably findings you get in the report that you don't find when you do it manually." [P10]

> "It's taken someone two weeks to write it [...] giving it 15 minutes, you won't have a chance to understand it, at least not well enough to find the hard stuff. I would imagine that the tool would actually raise a flag for a potential deadlock or race condition as well." [P7]

## Reduced effort and documentation help

For some participants, the assistant reduced the effort involved in reviewing by removing the need to search through the codebase or external documentation. Usefulness depended in part on how good the documentation and PR descriptions were to begin with, and one reviewer reflected that the tool could help keep documentation up-to-date by suggesting updates that align with PR changes.

## Prompting skill and interaction quality

One participant reflected on whether the quality of interaction depended on their own ability to ask good questions:

> "Maybe my way of asking questions was also wrong. I did not always feel like I got the response that I was asking for. So, I might need to learn how to be more detailed in my questions." [P10]

## Missing broader context

Many limitations were traced to a lack of access to broader context, such as architectural documentation, internal conventions, or metadata:

> "Ideally, you want to inject as much relevant information as possible [...] like the JIRA ticket, relevant [documentation] pages, the codebase itself, the README, and any similarly named repositories that might be connected to the same service." [P5]

## Integration and output presentation

Beyond integration, participants critiqued how the LLM assistant's output was presented. Several felt the feedback was overly long or difficult to scan:

> "I mean, what's important is that it very clearly lists the file. I'd rather have it list the file and the line number and be very specific, in a short way." [P5]

On integration, one participant suggested:

> "Maybe a Slack auto bot could even be triggered on each message [...] and a full review could be dropped as a message under that thread." [P11]

## Response time friction

Response time was another point of friction. While some delays were tolerated, long wait times were cited as a major barrier to adopting the tool in real development workflows:

> "I think the speed and accuracy are mainly what need to be improved. [...] I wouldn't use this if it took, I don't know, how many minutes it took for it to respond." [P3]

## Usage contexts: newcomers, low-standard teams, and Mode B

Many participants saw the assistant, especially Mode A, as valuable for newcomers:

> "I think if I were in a new team, and I am unsure what is happening, then it could be really good to start with a summary." [P8]

> "Yeah, if you can write questions like 'What is this?' or 'What is this really about?', it could also be a very good tool to get to know the codebase and to learn as a new guy." [P9]

Some saw Mode A as useful in teams where code review standards are lower or in teams that prefer other review methods such as pair programming, serving as a fallback mechanism:

> "I think it would be great for those who usually just skim through and say, 'It looks good to me'. [...] I think the biggest effect would be for those developers, I guess, and those teams." [P5]

Mode B was less preferred in general, but some participants said that where they were already familiar with the codebase or wanted to maintain full control over the review process, they would prefer Mode B:

> "But if it's in some codebase I already know, some codebase where we have a lot of experience and have worked in it a lot. It could probably be nice to have [Mode B]." [P8]

**Covers:** Phase 2 themes: accuracy/trust, efficiency/thoroughness, integration limits.
