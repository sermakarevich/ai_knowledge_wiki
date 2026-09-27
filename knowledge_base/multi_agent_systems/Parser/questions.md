---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: PARSER

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What are context rot and positional bias, and how bad do they get in the paper's measurements?
> [!tip]- Answer
> Context rot is steady accuracy loss as input grows even when it fits the window, and positional bias is systematic neglect of middle evidence in favor of start/end boundaries. Direct full-context Qwen3.5-4B falls from 75.8% at 7K to 34.4% at 896K on HotpotQA, a collapse of tens of points. See [[wiki/01-problem-and-motivation|Problem and Motivation]].

### Q2. Walk through one scatter-gather round: who sees what, and why does depth scale with K rather than T?
> [!tip]- Answer
> The lead agent thinks, scatters one query to all T chunk readers in parallel, drops Unknown abstentions, gathers the rest as one observation, then answers or asks a follow-up conditioned on it. The lead never sees raw document tokens, only the question plus gathered findings, while each frozen subagent sees only its own chunk. Sequential steps thus equal K reasoning rounds, not T chunks, so longer documents add parallel width, not a longer chain. See [[wiki/02-scatter-gather-method|Scatter-Gather Method]].

### Q3. Why does freezing all subagents and training only the lead agent help learning and generalization?
> [!tip]- Answer
> Per-chunk pointed lookup is simple enough for a frozen off-the-shelf model, so all learnable behavior concentrates in one policy: what to ask next from reasoning history. Gradients apply only to lead-agent tokens since subagent observations are masked, keeping training cost independent of document length. Because the lead never sees raw text, it learns question-driven reasoning rather than document-specific summary habits, which the paper credits for stronger out-of-distribution scores. See [[wiki/03-training-lead-agent|Training the Lead Agent]].

### Q4. What are the headline HotpotQA numbers for PARSER-4B, and how does its length curve differ from baselines?
> [!tip]- Answer
> PARSER-4B averages 84.6% versus 78.9% for the strongest sequential baseline ReMemR1 (+5.7), widening to 85.4% versus 73.4% at 896K tokens (+12.0). PARSER stays nearly flat from 7K to 896K while full-context reading collapses and sequential-memory agents fall 6-9 points. The 9B version repeats the pattern at 86.8% average, beating DeepSeek-V4-Pro think-max by 6.3 points. See [[wiki/04-experiments-results|Experiments and Results]].

### Q5. What is the 11x latency claim, under what conditions does it hold, and why do K rounds beat T steps?
> [!tip]- Answer
> At 896K tokens and concurrency 1, amortized time is about 78s per sample for PARSER versus about 876s for MemAgent, roughly 11x faster; at concurrency 16 the gap narrows to about 59s versus 102s (1.7x). MemAgent needs one dependent memory step per chunk so steps grow linearly with length, while PARSER runs all chunks in parallel each round so sequential cost equals K reasoning rounds (about 4), plus far fewer generated tokens. Without KV-cache reuse or at high concurrency the lead shrinks, and at 7K tokens plain reading is still faster. See [[wiki/05-analysis-limits|Analysis, Cost, and Limits]].

### Q6. What breaks if chunks are judged once in document order and never re-read under new queries?
> [!tip]- Answer
> A chunk judged before later chunks arrive can discard a clue whose value only appears after a second hop, making accuracy sensitive to absolute position, logical order, and distance between evidence pieces. Controlled 894K-token tests show MemAgent dipping at the 50th-70th percentile band, degrading under reversed evidence order, and worsening as distractor gap grows, while PARSER stays flat. Re-reading every chunk under each follow-up query moves linking work from lossy document-order memory into the question-driven query chain. See [[wiki/targeted|Targeted Analysis]].

### Q7. Transfer: how would you apply scatter-gather to multi-file data-lake QA over long telemetry logs?
> [!tip]- Answer
> Bind one frozen reader per log file or time shard with an abstain-on-irrelevant format, and let a lead agent issue one focused query per round to all shards in parallel, then chain follow-ups (e.g., error ID first, then owning service). This fits only when evidence is sparse and scattered across 100K+ tokens with a few reasoning hops; for single-fact lookup use plain retrieval instead. Budget parallel serving with prefix caching, since every round fans out to all readers. See [[wiki/targeted|Targeted Analysis]].

### Q8. What is the weakest link in the evidence for PARSER's headline wins?
> [!tip]- Answer
> The flat-to-896K and OOD leads survive inside the authors' harness, but sequential baselines were reimplemented with reduced rollout budget, both datasets are Wikipedia multi-hop QA with the same distractor recipe, and the 11x speed number holds only at concurrency 1 with extra GPUs. Missing are a strong RAG (retrieve-then-read pipeline) rival, non-QA domains, and the Elena/Eleni confusion case where a confident wrong local finding misled the lead. The pattern is worth trialing but not adopting whole. See [[critical_thinking|Critical Analysis]].
