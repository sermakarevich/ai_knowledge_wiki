> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Scatter-Gather Method
**In one sentence:** PARSER splits a long document into chunks with one frozen reader per chunk, and a lead agent that never sees the raw text finds answers by repeating scatter-gather rounds where one query goes to all chunks in parallel and only the few returned findings shape the next step.
## Key points
- The document is split into T fixed-size chunks, and a bank of T subagents is created with exactly one subagent bound to each chunk, while only the lead agent is trained and the subagents stay frozen.
- The lead agent receives only the question and never receives the full document or any raw chunk tokens, so it reasons about the question and the gathered findings instead of reading the document itself.
- Each scatter-gather round follows the same pattern: the lead agent scatters one or more focused queries, all chunk readers run at the same time, and their local findings are gathered into one observation for the lead agent.
- Reasoning depth scales with K rounds rather than T chunks, so adding more chunks adds parallel readers instead of longer chains of dependent steps.
- Every chunk is read symmetrically under the same query in every round, so access to evidence does not depend on chunk position and no chunk is discarded after a single pass.
- Most chunks are irrelevant to a given query, so subagents may abstain, and abstentions are dropped during gathering, which keeps communication sparse.
- Cross-chunk dependencies are not solved inside one chunk read but across successive rounds, because findings from round k enter the lead agent context and shape the query in round k+1.
---
## Scatter-gather round walkthrough
This is the loop from Algorithm 1 in Appendix E.3, shown in the lower panel of Figure 1. Figure 1 contrasts (a) sequential memory methods, which walk through T chunks in a dependent chain, with (b) PARSER, which reads all chunks at once in each round and moves reasoning forward across rounds.
1. Think: the lead agent looks at the question plus history, including findings gathered in earlier rounds, and decides what is still missing.
2. Scatter query: the lead agent issues one or more focused natural-language queries through the `query_agents` tool call.
3. Parallel chunk read: the same query is sent to every subagent at once, and each subagent checks only its own assigned chunk.
4. Abstentions dropped: subagents with no supporting evidence return `Unknown`, and those empty replies are dropped instead of being passed on.
5. Gather as observation: the remaining chunk-level findings are combined into one observation, called R in the paper, and appended to the lead agent history.
6. Condition next query: the lead agent reads that observation and either forms a follow-up query that builds on what was just found or decides it has enough to answer.
7. Answer or next round: the lead agent either writes the final answer inside an `<answer>` block or starts another scatter-gather round, stopping at the latest when it reaches the round limit of at most 9 rounds in training and at most 12 rounds in inference.
## Parallel chunk readers
Each subagent is a Large Language Model (LLM) reader tied to one short chunk. The chunk size is at most 512 tokens in training and at most 4,096 tokens in inference. A small chunk keeps the reader input short and keeps the local search task simple.
For each query, the subagent must answer only from its own chunk. If the chunk holds evidence, it returns a JavaScript Object Notation (JSON) object with two fields: exact copied evidence text and a short answer based on that evidence. If the chunk holds nothing relevant, it returns exactly `Unknown`. The full instruction text and examples are in Appendix E.2.
Because the reading task is narrow, subagents run in non-thinking mode, meaning they do not produce long step-by-step reasoning traces. All subagents are served with the SGLang serving system and run at the same time through concurrent request dispatch, so one round covers the whole document in parallel.
## Question-driven reasoner
The lead agent is the only part that reasons across steps. It starts from the system prompt plus the user question, as listed in Appendix E.1, and never sees document tokens directly.
It works in a Reasoning and Acting (ReAct) loop, meaning thinking and acting alternate: after each thinking step, it either calls `query_agents` to gather more evidence or commits to a final answer. Each new query can depend on all earlier thoughts, queries, and gathered findings. If a generation has neither a valid tool call nor an answer block, the system returns an invalid-action hint and asks the lead agent to retry with correct formatting.
Only this lead-agent loop is sequential. Document reading stays parallel inside every round. The number of rounds actually used, K, follows the number of reasoning steps the question needs, not the number of chunks T.
## Adaptive reading across rounds
Independent chunk reading cannot see links that span two chunks, so PARSER does not ask subagents to solve multi-hop questions directly. Instead, the lead agent breaks the original question into smaller queries whose answers can each be found inside a single chunk.
Cross-chunk links are then rebuilt across rounds. For example, round one can ask for a name, and once that name is gathered, round two can ask about that name across all chunks again. Every chunk is revisited under each new query, so later hops do not depend on document order. This moves the hard linking work from document-order memory updates into the question-driven query chain.
## Sparsity and efficiency
For a normal query, only a few subagents find anything, while most return a short abstention that is dropped before aggregation. This means each round adds only a small set of findings to the lead agent context.
Sequential memory methods instead write a memory update after every chunk, even when most chunks are irrelevant. PARSER therefore creates far fewer output tokens during reading, although it still pays repeated input costs because all chunks are checked again in each round. The paper places the full cost comparison in its time-analysis appendix.
**Covers:** Section 3.2, Figure 1, Appendices E.1-E.3.
