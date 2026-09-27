# [Hypothesis] Prajwal Tomar — 11-step Cursor/Claude Code loop
- Source: https://x.com/PrajwalTomar_/status/1947272871967174720
- Status: fetched 2026-09-24 (direct x.com fetch; body validated for "PrajwalTomar"; full text recovered from embedded NoteTweet payload)
## Content
- Premise: a repeatable loop that makes vibe coding (improvisational, prompt-driven building) produce shippable products, used with Cursor and Claude Code (Anthropic's agentic coding tool).
- 1/ Load full project context first: Product Requirements Document (PRD), implementation plan, etc.
- 2/ Pull one feature at a time from the implementation plan; no bulk builds.
- 3/ Ask for candidate approaches before any code; 4/ pick the best and demand a detailed action plan.
- 5/ Review the plan carefully before building; 6/ fetch Application Programming Interface (API) docs when needed, review them, attach them inside Cursor as context.
- 7/ Instruct Cursor to stick to the plan while building the feature.
- 8/ Ask for testing instructions and test the feature properly; 9/ commit the changes.
- 10/ Ask Cursor what makes sense to build next; 11/ start a fresh chat and repeat until ship (fresh context per feature avoids drift).
- Reply-added tactic (not the author's): swap models mid-loop — build with one, review with another for gaps.
## Why it was kept
- Solo operator loop ("I build products"); useful as a technique checklist, not team evidence.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
