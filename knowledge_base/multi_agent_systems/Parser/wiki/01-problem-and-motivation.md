> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Problem and Motivation
**In one sentence:** Long documents fail not because models lack room, but because one-by-one reading ties the order of the document to the order of thinking, so the paper argues reading and reasoning must be separated.
## Key points
- **Context rot (a steady loss of accuracy as input grows) is real:** direct full-context answering drops by tens of points as documents grow from 77K to 896K tokens, even for million-token models.
- **Positional bias (ignoring the middle of the input) is one cause:** evidence placed away from the start or end boundaries is systematically ignored.
- **Sequential memory couples traversal to reasoning:** the agent reads chunk by chunk and compresses each new chunk plus the old memory into a new memory, and answers only from the final memory.
- **Constraint 1 — evidence-placement sensitivity:** because each chunk is judged before later chunks are seen, accuracy depends on absolute position, logical order, and distance between evidence pieces.
- **Constraint 2 — linear latency (waiting time that grows in direct proportion to length):** chunk T cannot start until chunk T-1 finished, so T chunks need T dependent steps in a row.
- **Decoupling thesis:** document order is imposed by the document, question order is imposed by the question, and the paper proposes to read all chunks in parallel width while keeping only reasoning sequential in depth.
---
## Context rot and positional bias
A Large Language Model (LLM) is a text model trained to read and generate language. Recent models accept a million tokens or more, so lack of space is no longer the main limit.
The paper points to a different limit called context rot: accuracy gets worse as the input gets longer, even when the input still fits easily inside the allowed window.
One visible form is positional bias. Models pay attention to the start and end of a long input and underuse the middle.
On multi-hop Question Answering (QA), which means questions that need combining facts from several places, the authors report the same pattern: full-context accuracy falls by tens of points when length grows from 77K to 896K tokens.
## Sequential memory paradigm
Because the whole document does not fit comfortably into working memory, one family of agents splits the long document into fixed-size chunks and reads them in order while keeping a short written memory.
MemAgent is the base method in this family: it reads one chunk, merges it with the previous memory into an updated memory, repeats to the end, and then answers from memory alone, trained end-to-end with Reinforcement Learning (RL), which means learning from right-or-wrong answer rewards.
ReMemR1 adds a callback module that can revisit earlier memory states, which is an attempt to reduce position bias.
GRU-Mem, named after the Gated Recurrent Unit (GRU) idea of gated memory, adds gates that skip chunks without evidence and can exit early, which is an attempt to save work.
All three keep the same core rule: T chunks require T dependent steps, in document order, in a single pass.
## Two structural constraints explained simply
Think of sequential memory like reading a very long book with a tiny notecard, where you may rewrite the notecard once per chapter and must read chapters in order.
Constraint 1 is judging too early. When you summarize chapter 2, you have not yet seen chapter 50, so you may throw away a clue whose importance only becomes clear later. In multi-hop questions this hurts a lot, because the first clue only makes sense after the second clue is found. The result is sensitivity to three things: where evidence sits, in what logical order the pieces appear, and how far apart they are.
Constraint 2 is waiting in line. Chapter 3 cannot be summarized until chapter 2 is done, so doubling the book doubles the waiting time, no matter how many helpers are available. The paper calls this wall-clock cost growing linearly with document length.
Later fixes trade one problem for the other: revisiting old memory adds extra steps on the same slow path, while skipping empty chunks still requires scanning in order up to the last needed clue.
## Parallel-reading prior work
Parallel reading means different chunks are read independently and their results are combined, instead of passing one memory down a line.
Map-reduce pipelines such as LLM x MapReduce and ToM try this, but most are single-shot: the same fixed question is sent to every chunk once, so they cannot handle multi-hop questions where the next question depends on what the last round found.
LongAgent and XpandA use a leader with per-chunk agents over several rounds, but their coordination rules are hand-specified protocols rather than a learned policy.
Chain-of-Agents gives one chunk to each worker but still passes a single message sequentially down the chain, so it keeps the in-order wait.
Other work encodes chunks separately inside the model and fuses them at the attention level, but those are query-agnostic, single-round, and need changes to model architecture.
The common orchestrator-worker pattern, where a leader sends tasks to isolated workers whose middle steps do not fill the leader context, is the background the paper builds on.
**Covers:** Abstract, Sections 1-2, 3.1.
