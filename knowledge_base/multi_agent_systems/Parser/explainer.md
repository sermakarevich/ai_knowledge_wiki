> [[index|Wiki]] | [[summary|Summary]]

# PARSER — In Plain Language

## What is this about?

Imagine you must answer a hard question from a 900-page binder, and you have a team of assistants. The old way: one person reads page 1, writes a note on a small card, reads page 2, rewrites the card, and so on to the end. By page 900 the card barely remembers page 300.

PARSER does it differently. It gives every assistant a few pages, then a team leader shouts one question to the whole room at once: "Anyone see this name?" Only assistants with something useful answer; the rest stay quiet. The leader reads the answers and shouts a better follow-up question. After a few rounds of this, the leader has enough to answer.

So: many readers working at the same time (parallel), one thinker asking follow-up questions step by step (in depth). Reading is wide; thinking is deep.

The name says it all: read in parallel, reason in depth.

## Why does it matter?

Today's AI models (AI systems that read and write text) can accept huge documents, but their accuracy quietly drops as documents get longer. The middle of a long file gets ignored, and clues found early can be forgotten before later clues arrive. Order matters too much: if clue B only makes sense after clue A, but B appears first in the file, the old one-person reader often throws B away.

If PARSER's idea works, long documents stop being a trap. The answer no longer depends on where facts sit in the file, what order they appear in, or how far apart they are. You ask in the order of your question, not the order of the document.

And it gets much faster: on a very long test document the old method took about 876 seconds per question while PARSER took about 78 seconds — roughly 11 times faster. When many questions run at once the gap shrinks, but PARSER still stays ahead.

## How does it work?

Think of a quiz master and a room of helpers, each holding a few pages:

1. The quiz master reads only the question — never the whole binder.
2. The quiz master shouts a focused question to the whole room, e.g. "Who is Elene's son?"
3. Every helper checks only their own pages, at the same time.
4. Helpers with nothing useful say "Unknown" and are ignored.
5. Helpers with evidence reply with the copied sentence plus a short answer.
6. The quiz master collects these replies into one update.
7. The quiz master thinks: "Now I know the son is Solomon — next, who is Solomon's father?" and shouts the new question to the whole room again.
8. After a few rounds (usually around 4, at most 9–12), the quiz master writes the final answer.

Key trick: no helper ever sees the full question history or other helpers' pages. Hard questions that span pages are solved across rounds, not inside one helper's head.

## Where can this be used?

The paper tests question-answering over long texts, but the same pattern fits anywhere a question hides across a giant pile of text:

- **Legal review:** find every clause about liability across thousands of contracts, then follow up: "which of these mention a specific supplier?"
- **Medical records:** a patient's clue is spread over years of notes; round one finds the diagnosis date, round two finds what drug was given after that date.
- **Codebases:** "where is this setting defined, and which services read it?" — each file gets a reader, the lead follows the trail across files.
- **Data lakes and support logs:** scan millions of log lines in parallel per question instead of reading them in order; quiet "no match" replies cost almost nothing.
- **Research and due diligence:** connect facts across papers, filings, or reports without caring which document mentions them first.

Anywhere today's approach is "read everything top to bottom and take notes," this offers "ask everyone at once, then ask a sharper question."

## Conclusions & takeaways

What to remember in a month:

- **Split reading from thinking.** Let many small readers scan in parallel; let one thinker reason in steps.
- **Position stops mattering.** Tests moved, reordered, and spread out the evidence — PARSER's score stayed nearly flat while older methods swung or sank.
- **Small readers are enough.** A medium-size helper did as well as a big one, and short pages (about 4,096 units of text) beat giving one helper the whole document.
- **Speed comes from fewer waiting steps.** The old way needs one dependent step per chunk; PARSER needs only one step per question round.

Honest limitations:

- It needs many helpers running at once (extra computers), and re-asking every helper each round can cost extra reading work when memory of past reads is full.
- Helpers only see their own pages, so a confident-but-wrong local answer (e.g. mixing up two people with similar names) can fool the leader, who never sees the original page.
- Short documents don't need this: for a 7-page file, plain full reading is faster.
- The paper shows no separate limitations section; these limits come from its failure example and cost analysis.

## Jargon decoder

| Term | What it means in plain words |
|---|---|
| Scatter-gather | Shout one question to all helpers at once (scatter), then collect their replies (gather). |
| Subagent | One helper that reads only its own small slice of the document. |
| Lead agent | The quiz master: asks questions, reads replies, never reads the raw document. |
| Reinforcement learning (RL) | Training by reward: the leader tries answering, gets points for right answers, and adjusts to earn more. |
| Context rot | Accuracy slowly rotting as the input gets longer, even when it still fits. |
| Positional bias | The habit of noticing the start and end of a long file and ignoring the middle. |
| Multi-hop QA | A question needing two or more clues chained together ("find A, then use A to find B"). |
| Exact match | A strict score: the answer counts only if it matches the expected text word for word. |
| Chunk | One small slice of the big document handed to a single helper. |
| Abstention | A helper saying "Unknown" (I have nothing) so its reply is thrown away. |
| Fan-out | Sending one question out to many helpers simultaneously. |
| Out-of-distribution | Test data that looks different from training data — a check of whether the method still holds up on surprises. |
