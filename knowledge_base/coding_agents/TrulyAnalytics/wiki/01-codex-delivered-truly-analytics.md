> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# What Codex Actually Delivered in Truly Analytics
**In one sentence:** Andrew Southall built Truly Analytics from blank repo to working v1.0 in six weeks with Codex GPT 5.3-codex as an accelerator, and git-history analysis shows Codex committed 42.3% of lines but only 46.5% of its code survived versus 72.1% for human code, proving AI excelled at bounded pattern-driven work while human judgment decided architecture, product context, security and operational risk.
## Key points
- Truly Analytics went from first commit to v1.0 in six weeks and launched across all of Southall's digital properties, built with Codex GPT 5.3-codex as an engineering accelerator rather than an autonomous replacement.
- Across 137 commits, humans made 107 commits (78.1%) and Codex made 30 commits (21.9%); of 21,031 committed lines, AI committed 8,886 lines (42.3%) and humans committed 12,145 lines (57.7%).
- Only 12,892 lines (61.3% of committed lines) survived to v1.0: 8,759 human lines (67.94% of v1.0) and 4,133 robot lines (32.06% of v1.0).
- AI code survival rate was 46.5% (4,133 of 8,886 survived; 4,753 or 53.5% replaced/deleted) versus human survival rate of 72.1% (8,759 of 12,145 survived; 3,386 or 27.9% did not make it).
- Of removed AI code, 3,610 of 4,753 lines (76.0%) were overwritten by the human, while only 546 human lines (4.5% of human committed lines) were overwritten by AI.
- Of 30 Codex PRs, 25 were accepted (83.3%) and 5 rejected (16.7%); Codex worked inside an isolated containerised pipeline with a strict wrapper that controlled branches, pushes and PR creation, with no direct access to git, secrets, database or internal services.
- Codex contributed heavily to mechanical implementation work (routing, database access, admin UI, caching, email integration, Kubernetes scaffolding) while human-authored code dominated product-specific and production-sensitive areas (client-side analytics, enrichment logic, event handling, infrastructure decisions, final integration).
---
## Abstract
**Covers:** Abstract — six-week build, git-history quantification, bounded vs judgment-driven work

Truly Analytics was built "from a blank repository to a working v1.0 product in six weeks, using OpenAI Codex as an engineering accelerator rather than an autonomous replacement for software development."

Scope of analysis per article:

> "This article analyses the resulting git history to quantify how much AI-generated code was committed, how much survived to v1.0, which parts of the system remained human-dominated and where AI assistance proved most useful. Across 137 commits and 21,031 committed lines, Codex contributed heavily to mechanical implementation work such as routing, database access, admin UI, caching, email integration and Kubernetes scaffolding. Human-authored code dominated the more product-specific and production-sensitive areas, including client-side analytics, enrichment logic, event handling, infrastructure decisions and final integration."

Main finding (verbatim):

> "The main finding is that AI-assisted development was highly effective when the task was bounded and pattern-driven, but human judgment remained decisive where architecture, product context, security and operational risk mattered. The useful metric was not how much code AI could generate, but how much of that code survived real development, review, replacement and release."

Caveats: "There's huge bias in this as there's only one engineer and one agent so individual variations could not be eased out of the data. However, given how rare this level of analysis and situation is it's still worth the study." Personal write-up note: "This is a personal write-up of a personal project on my personal site and doesn't include any professionally commissioned work, so the tone is more direct and informal than a formal corporate case study."

## Introduction — origin and pipeline
**Covers:** Introduction — product origin, six-week build, Codex wrapper pipeline

Truly Analytics is "the full production solution to a persistent issue I first ran into about ten years ago while working at a publishing and media firm" (ad-blocking analytics problems; weekend proxy patch blocked by geolocation problem). After freelancing, "with new AI technologies and changes in my life circumstances plus the market being such a mess that I don't want to deal with it, I came back to the idea" to productionise it "in a quick timeframe without shipping garbage."

v1.0 scope: "built in six weeks from first commit to v1.0 launched across all my digital properties and rolling out to case study partners," using "newer cloud infrastructure, now mature languages such as Go & SolidJS."

Pipeline: Codex GPT 5.3-codex "worked inside an isolated, containerised development pipeline with a strict wrapper. It had access to the code in a controlled manner through a fully provisioned image, and it could only generate the code in place before handing back control to the wrapper. Even the Git workflow was restricted. Codex wrote the code, while the wrapper controls around Codex created the branch and handled the push & PR creation."

Isolation: "Codex did not have direct access to the Git repository, secrets, database or anything else. It had outbound internet to research and, you know, work, but couldn't connect to internal services." Wrapper pulled code and prompts from a configured prompt library, kicked off Codex, captured outputs into GitHub and opened a PR; on messes it kept the container running and alerted for manual rescue (usually stale auth). "Therefore auth failures did not affect the below stats."

Wrapper reasons given: no time/patience to clean up large AI-agent messes ("If it deleted the database I'd have quit IT entirely"); Codex sometimes forgot to commit then trashed work in transitory Kubernetes jobs so a determinate wrapper output was needed; secrets protection ("All the data goes to external services, in this case OpenAI. I don't want my secrets and other considerations going to OpenAI"); transitory pipeline needs setup anyway.

Post-v1.0 exclusion: "Since then, I have added substantially more complex features, including Network Intelligence and Event Hooks… that would be a separate analysis." v1.0 core covered: "the Google Analytics proxy, the admin client, the backend management system and the engineering needed to handle tens of thousands of requests per second alongside the frontend JS running on each of those user devices."

## Quick Method Summary
**Covers:** Quick Method Summary — v1.0 snapshot, exclusions, git users

- "All code was grabbed from the v1.0 release whereby Truly Analytics went live to the internet, available for sign up and good to go."
- Excludes "features Truly Analytics is more known for such as Network Intelligence (determining the organisation origin for your users) or Event Hooks (tie specific analytics events into your CRM & other systems)."
- "It won't include any code that wasn't committed or was nuked from orbit."
- "The data is obfuscated in places for obvious reasons."
- "There's technically 3 users here, me on my desktop, me on my laptop and then Codex who is it's own git user, hence the reference to human and AI and not directly users."
- "Codex never works outside of that git user profile, so this is a test of codex as a coding agent not AI as a whole."

## Product
**Covers:** Product — GA replacement description, trial

> "Truly Analytics is essentially a drop in replacement for Google Analytics where you put it on your site, it handles privacy and consent better than standard GA and then sends the cleaned and protected data back into Google Analytics so you don't have to replace your analytics stack."

Guard role enables "Event Hooks so you can pass the data from specific events down to your other systems" and "Network Intelligence which provides details on where your traffic is actually coming from such as VPNs, corporate networks, which organisations did what, etc." Offer noted: "It's got a free 3-day no-card, no sales trial."

## Headline numbers
**Covers:** Headline numbers table — commits, lines, survival, PR acceptance

| Metric | Number | Percentage / context |
|---|---|---|
| Total commits | 137 | 100% |
| Human commits | 107 | 78.1% |
| AI commits | 30 | 21.9% |
| Timeline | 6 weeks | First commit to v1.0 release |
| Total committed lines | 21,031 | 100% |
| AI committed lines | 8,886 | 42.3% |
| Human committed lines | 12,145 | 57.7% |
| Final surviving lines in v1.0 | 12,892 | 61.3% of committed lines |
| Final human lines | 8,759 | 67.94% of TA is from a human |
| Final robot lines | 4,133 | 32.06% of TA is from a tin can |
| Human surviving lines | 8,759 | 72.1% of human committed lines |
| Codex PRs rejected | 5 | 16.7% of AI commits / PRs |
| Codex PRs accepted | 25 | 83.3% of AI commits / PRs |

## Human / AI Surviving LoC Sankey
**Covers:** Sankey section — survival rates, overwrite direction, "Fixed" definition

"When measured over time, AI committed 8,886 lines of code throughout the project, all through Codex. Of those, 4,133 lines made it into the v1.0 release. That gives the AI code a survival rate of 46.5%. The remaining 4,753 lines it chucked in the mix, or 53.5%, were replaced or deleted."

"The human, meaning me, committed 12,145 lines of code. Of those, 8,759 made it into the final version, giving the human code a survival rate of 72.1%. The remaining 3,386 lines, or 27.9%, did not make it. Ergo, my work has a 27.9% chance of needing a redo."

| Contributor | Lines committed | Lines surviving in V1 | Survival rate | Lines replaced / deleted | Replacement / deletion rate |
|---|---|---|---|---|---|
| AI / Codex | 8,886 | 4,133 | 46.5% | 4,753 | 53.5% |
| Human | 12,145 | 8,759 | 72.1% | 3,386 | 27.9% |
| Total | 21,031 | 12,892 | 61.3% | 8,139 | 38.7% |

Overwrite direction: "Out of the human code, 546 lines were overwritten by AI. That is only 4.5% of the human's committed lines. Botto knows good stuff when it sees it." vs "3,610 of the 4,753 AI lines that did not make it into v1.0 were overwritten by the human. That is 76.0% of the removed AI code."

Pattern summary (verbatim): "So the pattern is clear. Less than half of the AI code survived, compared with more than 70% of the human code. Very little human code was overwritten by AI, but most of the AI code that disappeared was overwritten by the human."

On wording: "Fixed is the term I would use as it wasn't outright deleted. With a short development cycle it's less likely to be 'changed' as in it's purpose altered but 'changed' as in improved or replaced."
