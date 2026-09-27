> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Analysis, Cost, and Limits
**In one sentence:** ParSer stays flat when evidence position, order, or distance is perturbed and is much faster than sequential memory at long contexts, but it pays for this with a parallel subagent bank and can still fail when a subagent returns a confident but wrong local finding.
## Key points
- Controlled tests on 894K-token documents varied evidence position (percentile bins), logical order (logical vs reversed), and separation (distractor paragraphs between two evidence pieces): MemAgent (a sequential memory agent) and ReMemR1 (MemAgent plus a callback that revisits earlier memory) swung or degraded, while ParSer stayed nearly flat.
- At 896K tokens and concurrency 1 (one request at a time), amortized time per sample was about 876s for MemAgent vs about 78s for ParSer (about 11x); at concurrency 16 (16 requests at once) it was about 102s vs about 59s (about 1.7x).
- Prefill (the first pass that reads the input) cost falls from O(n squared) for full-context reading to O(n squared / c) with c chunks; decoding (step-by-step output generation) savings come from far fewer generated tokens.
- Larger subagents help only up to a point: with the lead agent fixed, average score went from 78.26% (2B subagent) to 84.57% (4B default) and then flattened at 84.77% (9B).
- Smaller chunks win: the 4,096-token chunk default averaged 84.57%, while a single full-document subagent averaged 73.76% and fell to 53.13% at 896K; larger chunks (16K, 65K, 131K tokens) scored progressively lower.
- The same lead agent works without retraining with other subagent types: lead plus DCI (Direct Corpus Interaction, agents that search raw text with shell tools such as rg and grep) subagents beat standalone DCI, and lead plus thinking subagents beat full-context thinking.
- Known failure mode is context isolation: in Appendix F.2 the lead agent accepted "Prince Nicholas of Greece and Denmark" from a chunk about a different Elena instead of the correct "Prince Archil of Imereti", because subagents see only the query plus their chunk and the lead agent cannot check the subagent source text.
---
## Controlled experiments: position, order, distance
Figure 2 reports three experiments on 894K-token documents. Here LLM means Large Language Model.
### Evidence position control
- Design: 512 HotpotQA questions; all evidence paragraphs placed in a random spot inside one 10-point percentile band ([st, st+10], with st from 0 to 90 in steps of 10); distractors fixed.
- Outcome: ParSer stayed stable across bands; MemAgent dropped clearly when evidence sat between the 50th and 70th percentiles; ReMemR1 partly reduced this dip with its callback module.
- Paper explanation: sequential memory compresses chunks into a fixed-size memory in document order, so middle evidence can be overwritten by later updates, while early evidence can settle early and late evidence faces few further updates.
### Evidence order control
- Design: 512 two-hop bridge-comparison questions from 2WikiMultiHopQA (used because it labels the logical order of evidence); same paragraphs in both versions, only the order of evidence paragraphs changed (logical order vs reversed); distractors fixed.
- Outcome: MemAgent and ReMemR1 degraded substantially under reversed order; ParSer stayed stable.
- Paper explanation: if a paragraph appears before the earlier-hop fact needed to see its value, a sequential agent may skip it or drop it before its use becomes clear; ParSer re-asks every chunk each round with queries that include earlier findings, so it follows the question logic rather than document order.
### Evidence distance control
- Design: 512 two-evidence questions from 2WikiMultiHopQA; logical order kept; the count of distractor paragraphs between the two evidence paragraphs varied; 1,600 paragraphs of padding fixed before the first and after the last evidence paragraph.
- Outcome: MemAgent and ReMemR1 worsened as the gap grew; ParSer stayed stable.
- Paper explanation: the first evidence must survive more memory rewrites before the second arrives, so loss risk rises with distance; ParSer reads the two chunks independently in parallel and joins them in the lead agent, so path length does not grow with physical distance.
## Latency: Table 2 key rows and why K rounds beat T steps
Table 2 reports amortized wall-clock seconds per sample (total time for 128 HotpotQA samples divided by 128) at concurrency 1, 16, and 32. Here GPU means Graphics Processing Unit.
- Concurrency 1, 896K tokens: MemAgent 876.20s, ParSer 78.22s (about 11x gap).
- Concurrency 16, 896K tokens: MemAgent 101.94s, ParSer 58.86s (about 1.7x gap).
- Concurrency 32, 896K tokens: MemAgent 74.96s, ParSer 58.76s (gap narrows further).
- Short documents favor single-pass reading: at 7K tokens and concurrency 1, Full-context (non-thinking) took 1.16s, ParSer 5.33s, MemAgent 10.56s.
- At high concurrency, full-context entries show "-" at 896K because GPU memory ran out before all samples finished.
- Test setup: baselines used one NVIDIA H100 GPU; ParSer used one H100 for all subagents plus one RTX3090 for the lead agent; lead and subagents in one instance alternate because the lead agent waits for subagent replies. ReMemR1 was left out of the latency table because its extra retrieval module adds latency over MemAgent by design.
- Why K rounds beat T steps: MemAgent needs one dependent step per chunk, so its step count grows in proportion to chunk count (linear in document length); ParSer runs all chunks in parallel each round, so its sequential steps equal the number of reasoning rounds (K, the count of lead-agent query rounds, about 4 in measurements), which stays nearly constant for the same questions as length grows.
## Complexity analysis summary (Appendix A)
Here KV-cache means Key-Value cache, the stored attention keys and values that let a model skip re-reading earlier tokens.
- Prefill: full-context prefill is O(n squared) in document tokens n because of attention (the mechanism that compares every token with every other token); splitting into c chunks encoded separately gives c times O((n/c) squared), which equals O(n squared / c).
- Decode: each new output token attends to (looks back at) prior input plus prior output tokens. MemAgent writes roughly 1K memory tokens per chunk, so total output grows with chunk count (Table 6: 2,211 tokens at 7K up to 187,058 at 896K). ParSer subagents mostly return a short finding or "Unknown", so combined lead-plus-subagent output stays small and flat (for example 534+312 at 7K and 541+804 at 896K).
- Computed decode-computation ratio (ParSer over MemAgent, with about 5,000 tokens per chunk and K=4 rounds) falls from 13.9% at 7K to 0.42% at 896K.
- Parallelism across c subagents further divides the subagent part of wall-clock decode latency by c; the lead-agent part stays sequential.
- Catch: the math assumes all chunk KV-caches fit in GPU memory. If caches are evicted (pushed out, common at high concurrency), each round must re-prefill chunks, raising prefill from O(n squared / c) to O(K times n squared / c), or about 4x MemAgent at K=4. MemAgent scans once and never revisits chunks, so it is unaffected. This is why the latency lead shrinks at concurrency 16 and 32.
## Subagent ablations: size and chunk size
- Subagent size (Table 3, lead agent fixed as Qwen3.5-4B, HotpotQA Sub_EM score): 2B averaged 78.26%, 4B default averaged 84.57%, 9B averaged 84.77%. Paper reading: after decomposition into a focused query over a short chunk, 4B capacity is already enough, so 9B saturates; this favors cheap lightweight subagents.
- Chunk size (Table 4, all Qwen3.5-4B): 4,096-token chunks averaged 84.57%; full-document single subagent averaged 73.76% and collapsed on long inputs (56.77% at 448K, 53.13% at 896K); 16,384 averaged 83.59%, 65,536 averaged 81.84%, 131,072 averaged 80.34%. Paper reading: longer inputs hide key facts more easily (context rot, the observed accuracy loss as input grows), so many short chunks beat one long view.
## Alternative subagents without retraining (Section 5.4)
- DCI subagents (Direct Corpus Interaction agents that grep and search the raw corpus with command-line tools): standalone DCI agent averaged 75.61%, lead agent plus DCI subagents averaged 84.67% (all Qwen3.5-4B, HotpotQA).
- Thinking subagents (subagents that write out step-by-step reasoning before answering): full-context thinking averaged 65.82% and fell to 31.25% at 896K, while lead agent plus thinking subagents averaged 85.55%.
- The lead agent was not retrained for either variant, which the paper presents as evidence the lead policy coordinates different worker styles.
## Cost and latency trade-offs of the subagent bank
- Parallel fan-out: all T subagents (one per chunk) run at the same time each round through concurrent request dispatch with SGLang (a model serving framework), so every chunk sees the same query with no position advantage.
- Abstention sparsity: for each query only a few subagents return evidence; the rest emit a short abstention ("Unknown") that is dropped before aggregation, unlike sequential memory which writes hundreds to thousands of memory tokens after every chunk.
- Prefill vs decode: multi-round reading can keep or raise prefill work (especially without KV-cache reuse), but it sharply cuts decode work because total generated tokens stay small and flat while MemAgent output grows with chunk count.
- GPU (Graphics Processing Unit) deployment: training used 6 H100 GPUs for the lead policy (4 for rollouts, 2 for updates) plus 10 extra H100 GPUs to serve subagents; the latency test used 1 H100 for subagents and 1 RTX3090 for the lead agent. Inference reuses chunk prefills via prefix caching (SGLang Radix Cache with cache-aware routing) because each subagent prompt is ordered fixed-instructions, then fixed-chunk, then changing-query, so only the short query suffix is re-prefilled when the cache hits.
## Failure case and acknowledged limits
- Failure case (Appendix F.2, "Who is the husband of Princess Elene of Georgia?"): one finding correctly traced Elene (daughter of Heraclius II, mother of Solomon II) and another supported Prince Archil of Imereti via Solomon II's parents; a third subagent, seeing only a chunk about Grand Duchess Elena Vladimirovna of Russia, returned "Her husband was Prince Nicholas of Greece and Denmark". The lead agent picked the short direct answer and output the wrong husband.
- Mechanism: context isolation. Each subagent gets only the query plus its chunk (no reasoning history), so an underspecified query plus a similar name yields a confident local error; the lead agent gets conclusions without the source passage, so it cannot directly check grounding and may over-trust the error. The paper notes this is occasional and that extra specific queries sometimes fix it, but not always.
- Section 6 (Conclusion) lists no separate limitations section; the constraints stated in the paper are the ones above plus Appendix A: KV-cache eviction at high concurrency removes part of the speed advantage, and Section 5.3 shows chunking is load-bearing (removing it causes a large drop on long documents).
**Covers:** Section 5, Figure 2, Table 2, Section 6, Appendices A, F.
