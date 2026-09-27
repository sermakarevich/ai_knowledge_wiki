# [Hypothesis] Ben X — TRD → epics → tickets → fresh session per ticket
- Source: https://x.com/Benn_X1/status/2048468090342486417
- Status: fetched 2026-09-24 | direct x.com fetch (validated: body contains "Benn_X1"); archive fallback not needed
## Content
- Design whole system before any code: no build-as-you-go; write a TRD (technical requirements document) in markdown first, using AI to brainstorm.
- Human must read and fully understand the TRD file before proceeding (he calls it TDD.md; context shows he means the TRD doc).
- With AI, split project into 3+ epics, each with tickets — all markdown files covering implementation detail, folder structure, testing strategy, architecture; read and understand every epic/ticket; optionally commit or gitignore them.
- Implement one ticket per fresh session: put the epic + ticket in context, prompt AI to implement, then stage.
- Review in a second fresh session: AI reviews what it generated and will find bugs; human validates for false positives/hallucinations, corrects or accepts, stages again, commits, marks ticket complete; clear context before next ticket.
- Motivating example: this discipline means you notice when e.g. fastembed is silently removed from dependencies — and you actually own the codebase.
- Caveat from author: he rarely generates code with AI (mainly tests); other methods may be more efficient; the jab at "finding out after the fact" suggests the post replies to someone else's dependency mishap.
## Why it was kept
- Individual method, no team — session-hygiene idea (fresh context per ticket) worth stealing.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
