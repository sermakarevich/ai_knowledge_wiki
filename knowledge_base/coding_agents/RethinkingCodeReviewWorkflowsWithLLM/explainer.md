> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Rethinking Code Review Workflows with LLM — In Plain Language

## What is this about?

Code review is the everyday habit where a teammate reads your code
change before it goes live, looking for bugs and confusing parts.

This study asks a simple question: what is the best way for an AI
assistant to help with that job — should it speak up first, or stay
quiet until asked?

Researchers at a Swedish car-software company called WirelessCar
watched real developers work in two steps.

First, they interviewed developers about what makes review painful
today and where AI might help.

Then they built a review assistant and tested two styles of it with
10 developers reviewing real company code changes.

Style A, the "Co-Reviewer," reads the change first and hands the
reviewer a written summary: what changed, what looks risky, what to
check. The reviewer can then ask follow-up questions.

Style B, the "Interactive Assistant," says nothing up front. It just
waits, and answers only when the reviewer asks it something specific.

## Why does it matter?

Reviews are essential — they catch bugs, spread knowledge, and keep
quality steady — but they are under strain.

Codebases keep growing, delivery keeps speeding up, and reviewers get
tired, rushed, or inconsistent.

A big change that took two weeks to write might get only 15 minutes
of review. Large changes are especially hard: nobody can hold the
whole thing in their head.

AI language models are already good at writing code and spotting some
bugs, but review is trickier. A wrong AI suggestion can waste hours
or, worse, teach reviewers to ignore the tool entirely.

Earlier work tested whether AI *can* find bugs. This study asks what
developers actually *want*: which kind of help feels trustworthy,
saves effort, and fits into a normal workday.

The answer matters because the wrong design — noisy, slow, or sitting
in a separate tool — simply will not get used.

## How does it work?

Phase 1 was diagnosis. Through half-hour interviews, developers
described informal, expert-dependent reviews hurt by delays, giant
changes, interruptions, missing background (why was this built this
way?), and uneven depth — some teammates just write "looks good."

They already used tools like Copilot or ChatGPT informally, and wished
for AI that summarises big changes, checks the change against the
original request ticket, and catches sneaky defects like race
conditions that a human skimming for three minutes will miss.

Phase 2 was a live tryout. Each of the 10 developers reviewed two
real, medium-sized changes — one with Style A, one with Style B —
with the pairing rotated so order effects cancel out.

Some reviewers knew the code well; others did not, so the team could
see whether newcomers lean on AI more.

Sessions happened in the developers' normal setup, with researchers
watching and asking them to think aloud, followed by a short interview
comparing both styles to their usual routine.

Under the hood, the assistant could look up the feature request ticket
behind the change, so its answers had business context — and Style A
used a special sub-step that read the entire change up front instead
of searching it piece by piece, so nothing was skipped.

## Where can this be used?

The clearest wins are large, unfamiliar, or low-risk changes.

A newcomer joining a team can start with the AI summary to learn what
a change is about instead of drowning in files.

A reviewer facing a huge change can let the summary do the manual
"breakdown" work they would otherwise do by hand.

For small, safe changes, several developers said they would happily
let the AI do most of the work.

Reviewers who already know the code well, or who handle safety-critical
logic, mostly preferred Style B: let me lead, and let the AI answer
questions or double-check me at the end.

Two bonus uses came from developers themselves: run the assistant as a
*pre-review* check for the author before the change is even submitted,
and run it as a *second pair of eyes* after a human review to catch
leftovers.

For any of this to stick, developers said the assistant must live
where they already work — inside GitHub, GitLab, the code editor, or
Slack — give short answers with exact file and line numbers, respond
fast, and know the wider context: tickets, docs, team conventions.

## Conclusions & takeaways

AI help genuinely caught things humans missed, including possible
deadlocks and race conditions, and cut the boring searching through
code and docs.

But it also produced wrong, strange, or low-priority notes, buried
important findings in long summaries, answered slowly, and lacked
broader project context.

Trust was the hinge: developers saw the tool as low-risk when it was
optional ("if we miss 10 issues today, we might miss two with a tool
like this"), yet feared being led astray — especially by Style A, where
staring at the AI's list can make you miss everything else.

There was no single winner. Most liked AI-led summaries for unfamiliar
or low-risk work; many wanted quiet on-demand help when they were the
expert. The practical verdict: offer both modes, keep output short and
precise, respond quickly, embed in existing tools, and treat AI as a
complement to reviewers — not a replacement.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Code review | A teammate reading your code change to catch bugs before release |
| Pull request (PR) | A packaged-up code change submitted for review and merging |
| LLM | An AI trained on lots of text and code that can read, summarise, and answer questions |
| Mode A / Co-Reviewer | The AI speaks first: auto-summary of the change, then Q&A |
| Mode B / Interactive Assistant | The AI stays quiet until the reviewer asks it a question |
| RAG pipeline | A setup letting the AI pull in extra documents (like tickets) before answering |
| Jira ticket | The written task request describing what the code change was supposed to achieve |
| Race condition / deadlock | Tricky timing bugs where parallel tasks collide or freeze — easy for humans to miss |
| False positive | An AI warning about a problem that is not actually a problem |
| Over-reliance | Trusting the AI so much you stop checking carefully yourself |
| Thematic analysis | Grouping interview quotes into recurring themes to find patterns |
| Think-aloud protocol | Asking people to narrate their thoughts out loud while they work |
