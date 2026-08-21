---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are GRA's seven tools, and which one is unique to graph navigation rather than a direct port of a code-agent tool?

> [!tip]- Answer
> `ls` (list nodes/tables/edges), `cat` (read a node in full), `grep` (literal search), `sems` (semantic/dense+BM25 search), `query` (read-only SQL, capped at 50 rows), `think` (scratchpad), `answer` (submit with citations/confidence). `sems` is the one without a direct code-agent analogue — it lets the agent match a question's words to a graph node by meaning rather than exact string, which matters because "the deciding fact often sits in a table reached through the graph" and a question's words must first be matched to a node. See [[wiki/01-gra-agent-design|GRA Agent Design]].

### Q2. Why does the paper test RSA (graph removed) alongside GRA, and what does the result tell us about where GRA's advantage comes from?

> [!tip]- Answer
> RSA runs the identical execution loop and shares the same strategy prompt verbatim, differing only in substrate (flat text chunks + table schemas instead of a graph). Because GRA beats RSA by only +0.3 to +1.9pp — while both beat SQA by a much larger margin — the paper concludes the bulk of GRA's advantage comes from *selective agentic access* (fetching only what's needed) rather than from the graph's topology itself. See [[wiki/01-gra-agent-design|GRA Agent Design]] and [[wiki/04-industrial-deployment|Industrial Deployment]].

### Q3. How does UFK-M guarantee that every benchmark question is actually answerable, and why does that matter for scoring?

> [!tip]- Answer
> Questions are generated "answer-first": an LLM writes a SQL program over sampled schema cards, the program is executed against the real database, and it's kept only if the result is non-empty, non-degenerate, and ≤10 rows — only then is a natural-language question written to match that already-validated result. This means every gold answer is the literal output of an executed, correct program rather than model-generated text, so a deterministic matcher (not an LLM judge) can score answers exactly. See [[wiki/02-ufkm-benchmark|UFK-M Benchmark]].

### Q4. On the xlarge benchmark, name one backbone model where GRA loses to SQA, and explain the mechanism the paper offers for why.

> [!tip]- Answer
> GPT-5 Nano: GRA loses to SQA by −22.9% relative error reduction (i.e., SQA wins). The paper attributes this to tool-call reliability rather than reasoning depth — GPT-5 Nano fails 10.2% of tool calls (51.6% of questions hit at least one failure), far above the DeepSeek configurations' sub-1% failure rate, and enabling extended reasoning on GPT-5 Nano cuts failures roughly in half and recovers +6.2pp accuracy. Full-context inference is more robust precisely when a model can't reliably drive tools. See [[wiki/03-results|Results]].

### Q5. Why does the paper report "unique input tokens" separately from billed/completion tokens, and what does each measure tell you?

> [!tip]- Answer
> Unique input tokens (counted once per trajectory) measure corpus coverage — how much of the underlying data the agent actually had to read to answer; GRA reads only 29–33% of SQA's unique input. Billed input tokens differ because GRA/RSA resend a growing context across 11–15 turns while SQA averages under 3 turns, so the cost picture flips depending on workload: warm-cache batch evaluation favors SQA's reusable big prefix, while cold-start single-question serving favors the agents since SQA re-pays its full ~17k-token prompt every time. See [[wiki/03-results|Results]].

### Q6. In Example 1 of the industrial deployment section, what were the two independent reasons GRA refused the "aluminium frames to welding station 1 or 2 on Monday" rule, and where did each piece of evidence come from?

> [!tip]- Answer
> (1) A conflict with quality rule R7, found one edge away from station 1 in the graph, stating station 1 welds carbon frames only — aluminium and carbon share no words, so this required following a graph edge, not text matching. (2) A capacity shortfall: at standard times the day's aluminium load (936 min) fits the 960-minute calendar, but recomputing with *measured* historical welding durations (about a third longer than standard, plus changeover time) pushed the true requirement to ≈1,300 minutes — a shortfall only visible by querying real data, not any stored value. See [[wiki/04-industrial-deployment|Industrial Deployment]].

### Q7. What is the tool-call budget "knee" the paper finds, and what would happen to accuracy if the budget were set to 10 instead of 30?

> [!tip]- Answer
> Accuracy rises sharply from B=10 to B=30 and then plateaus (a "knee" at B≈30); above that, additional tool-call budget buys essentially no further accuracy. At B=10, xlarge accuracy drops to 63.6%, driven by a high truncation rate (118 of 258 xlarge questions exhaust the budget before answering) — a budget too tight simply cuts the agent off mid-investigation. See [[wiki/03-results|Results]].

### Q8. The paper claims "seeing less, the agent answers better." What is the single strongest caveat to that claim that the paper itself acknowledges, and why does it limit how far the result generalizes?

> [!tip]- Answer
> The current corpus is small enough that SQA's ~17k-token full-schema prompt fits comfortably inside every tested model's context window — so the regime where serialization becomes genuinely infeasible or too costly (which is exactly where selective navigation should matter most) remains untested. The paper's own gain over RSA (its graph-free control) is also small (+0.3–1.9pp), reinforcing that the demonstrated advantage is about selective access at a modest scale, not proof that graph-structured navigation wins at scale. See [[critical_thinking|Critical Analysis]] and [[wiki/04-industrial-deployment|Industrial Deployment]].
