> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Targeted Analysis: PARSER Deep Dive

**In one sentence:** This page answers four concrete questions about PARSER (Parallel Reading, Sequential Reasoning, a method where many small readers scan document chunks at the same time while one lead agent reasons step by step): how a scatter-gather round works, why frozen subagents help training, where the long-context wins come from, and what the subagent bank costs.

## Key points

- A scatter-gather round is a fixed loop: the lead agent thinks, scatters one query to all chunk readers in parallel, gathers their findings as one observation, and either answers or asks a deeper follow-up question conditioned on what came back.
- Freezing the subagents helps training because it concentrates all learnable behavior in one place (the lead agent), keeps training cost independent of document length, and stops the system from overfitting to training-document summaries.
- The 896K-token wins come from three structural differences, not a bigger model: every chunk is re-read under every query (no position bias), queries follow the question's logic instead of document order (no order/distance penalty), and accuracy stays flat while sequential memories degrade.
- The subagent bank trades weaker per-chunk readers and extra parallel compute for much lower waiting time: at 896K tokens it answers in about 78 seconds instead of about 876 seconds, with most chunk replies being short abstentions that are dropped before aggregation.
- The price is real: every round fans out to all T readers at once (the paper deploys subagents on 10 extra H100 Graphics Processing Units, processors used for model computation), prefill compute can stay flat or grow without cache reuse, and a confident-but-wrong local finding can mislead the lead agent.
- Bottom line for practice: PARSER fits multi-hop Question Answering (QA, questions that need combining facts from several places) over very long, scattered evidence where reasoning depth is small but document length is huge; it is overkill for short documents or single-fact lookup.

---

## 1. A scatter-gather round in concrete steps

Think of a team of assistants, each holding exactly one page of a very long report, and one coordinator who holds only the question. The coordinator never sees any page directly. One round works like this:

1. **Think.** The lead agent looks at the original question plus everything gathered in earlier rounds, and writes a short private reasoning note (a ReAct-style think step: thinking, then acting, in turns).
2. **Scatter.** The lead agent broadcasts one or more focused queries to *all* T subagents at the same time. Example from the paper's case study: first "Who is Princess Elene of Georgia?" and, after learning she is the mother of Solomon II, a follow-up round asking "Who is the husband of Princess Elene of Georgia?"
3. **Parallel read.** Every subagent searches only its own short chunk (4,096 tokens at inference time) for that query and returns a small structured finding in JSON (JavaScript Object Notation, a standard structured text format), or abstains. Most chunks are irrelevant to any given query, so most subagents emit only a short abstention.
4. **Gather.** Abstentions are dropped. The remaining findings are bundled into a single observation for the lead agent.
5. **Decide.** The lead agent either commits to a final answer or starts the next round with a deeper query conditioned on the new findings. Training allows at most 9 rounds (K <= 9); inference allows up to 12.

Because step 3 covers the whole document in every round, adding more chunks adds parallel readers (width), not longer chains of waiting (depth). The number of rounds K follows the question's reasoning hops, not the document's chunk count T, and in long documents T is far larger than K.

## 2. Why freezing the subagents helps training

Three reasons, each addressing a real training pain:

- **One thing to learn instead of two.** Each subagent's job (find evidence for one pointed query in one short chunk) is simple enough for an off-the-shelf model running in non-thinking mode. The only hard skill, deciding what to ask next from the reasoning history, lives entirely in the lead agent. Reinforcement Learning (RL, improving behavior from reward signals) therefore optimizes one policy, not a coupled reader-plus-reasoner system.
- **Training cost stops depending on document length.** The frozen readers are infrastructure, not parameters to update. Gradients flow only to tokens the lead agent generated (subagent observation tokens are masked out of the Group Relative Policy Optimization, GRPO, update), so longer documents mean more parallel inference calls, not a bigger training problem.
- **Less overfitting to training documents.** Because the lead agent never sees raw document text, it cannot memorize document-specific summary habits the way sequential-memory agents do. The paper credits this for the out-of-distribution result: on 2WikiMultiHopQA (a new data family not seen in training), PARSER with a 4B backbone averages 87.0%, above its own in-distribution average of 84.6%, while MemAgent drops to 60.6%.

The paper also checks the reverse: swapping in other reader types (Direct Corpus Interaction search agents, thinking-mode subagents) without retraining the lead agent still beats the standalone alternatives, which suggests the learned querying skill is genuinely reader-independent.

## 3. Where the 896K-token wins come from vs sequential memory

At 896K tokens on HotpotQA, PARSER-4B scores 85.4% against ReMemR1's 73.4% (+12.0 points); the average gap over 7K-896K is +5.7. The paper traces this gap to three controlled experiments on 894K-token documents, each isolating one factor:

- **Position.** Evidence placed in the 50th-70th percentile band of the document hurts MemAgent badly (middle evidence gets overwritten by later memory updates), while PARSER is flat because every chunk faces the same query in every round regardless of its index.
- **Order.** When evidence paragraphs are reversed against their logical dependency order, sequential agents drop sharply: an early-arriving clue whose relevance is not yet visible gets omitted or evicted before its prerequisite appears. PARSER revisits all chunks under queries conditioned on already-found evidence, so it follows the question's logic, not the document's layout.
- **Distance.** As distractor paragraphs between two evidence pieces grow, sequential memories must carry the first clue through more and more lossy updates and lose it; PARSER reads both chunks independently and composes them in the lead agent, so physical distance does not lengthen the reasoning path.

In short: sequential memory degrades with length because loss compounds once per chunk (T dependent steps); PARSER stays flat because loss, if any, compounds once per reasoning round (K steps, with K far smaller than T). Full-context reading degrades even faster (Qwen3.5-4B falls from 75.8% at 7K to 34.4% at 896K), which the paper attributes to context rot and middle-position neglect.

## 4. Cost and latency trade-offs of the subagent bank

What you gain and what you pay:

- **Latency (waiting time): the big win.** At 896K tokens with one request at a time, MemAgent needs about 876 seconds per sample vs about 78 for PARSER (about 11 times faster). At 16 concurrent requests the gap narrows to about 102 vs about 59 seconds (about 1.7 times), because parallelism helps the baseline too, but PARSER still leads.
- **Why it is faster.** The sequential chain of T memory updates (each generating hundreds or thousands of tokens) is replaced by K rounds of parallel reads plus small lead-agent steps. Compute analysis: input-reading cost drops from O(n squared) toward O(n squared / c) with c chunks, and output-generation cost drops because far fewer tokens are generated per step.
- **Sparsity keeps it affordable.** Per query only a handful of subagents return real findings; the rest send short abstentions that are dropped before aggregation. So per-round traffic is small even though the fan-out is wide.
- **The hardware price.** Wide fan-out still needs somewhere to run: the paper deploys subagents across 10 extra H100 cards via SGLang concurrent dispatch, on top of 6 cards for training/rollouts. Without key-value cache reuse across rounds, repeated full-document reads can keep input-reading compute flat or higher; the savings concentrate in generated tokens and wall-clock time.
- **The accuracy price.** Readers are weak by design (small, frozen, no cross-chunk view). The documented failure mode: a subagent matched the wrong "Elena" in its chunk and returned a confident wrong husband ("Prince Nicholas of Greece and Denmark"), and the lead agent accepted it over contradictory identity-grounded evidence for the right answer ("Prince Archil of Imereti"). The lead agent cannot double-check source text it never sees.

**Rule of thumb:** use this shape when evidence is scattered across hundreds of thousands of tokens and the question needs a few reasoning hops; prefer plain full-context reading for short documents and single-fact lookup, where the fan-out overhead buys nothing.

**Covers:** Task-specified questions 1-4, grounded in Sections 3.2-3.3, 5.1-5.2, Appendices A, E, F.2.
