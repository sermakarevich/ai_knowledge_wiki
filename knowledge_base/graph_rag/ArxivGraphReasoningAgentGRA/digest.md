> [[index|Wiki]] | [[summary|Summary]]

# Schema-Agnostic Graph Reasoning Agent — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-gra-agent-design|GRA Agent Design]]

**In one sentence:** The paper argues that a knowledge graph admits the same generic navigation interface as an unfamiliar codebase, and presents GRA — a graph reasoning agent using seven unix-style tools — against two controls (RSA, the same loop without the graph, and SQA, a full-context serialized baseline) on the UFK-M benchmark.

- Tool-calling code agents (ls, cat, grep over files) navigate repositories they have never seen; a labeled property graph admits structurally equivalent operations — listing neighbours, reading node content, searching node descriptions.
- The authors present GRA (Graph Reasoning Agent) for hybrid knowledge graphs, whose nodes are either textual concepts or relational tables, discovering everything domain-specific at run time via seven generic tools.
- Headline result (from the abstract): on UFK-M, an industrial benchmark of 258 analytical questions whose gold answers come from executing validated SQL programs, GRA beats a full-context agent by 5.1 pp (88.4% vs. 83.3%) while reading under a third of its input tokens.
- The abstract frames the two competing philosophies this paper measures: serialize everything into the prompt, versus give the model a bounded context plus tools to fetch what it needs.
- A graph-free control (RSA) shows the gain comes chiefly from selective agentic access rather than graph topology, and the effect depends on a model able to drive tools reliably.
- The assumed substrate contract is minimal: each node has an identifier, natural-language description, labels, optional properties; relations are directed subject–predicate–object triples; some nodes are data tables backed by real DuckDB tables queryable with SQL.
- The design descends from ReAct (interleaving reasoning and tool calls) and SWE-agent (showing a few file-system commands suffice for an unfamiliar repo); prior graph-agent work assumes the vocabulary is known and that traversal alone answers the question — neither holds on a hybrid substrate.
- GRA hard-codes nothing domain-specific: no concept list, no label strings, no table names in tools or system prompt.
- RSA ("fairness enforced by construction") shares the identical execution loop and strategy prompt blocks verbatim with GRA, differing only in substrate (flat text chunks + table schemas) and navigation tools.
- SQA is the serialize-everything baseline: full text description plus fully rendered schema (~17k tokens) up front, answering within at most six turns with no navigation.

## 2. [[wiki/02-ufkm-benchmark|UFK-M Benchmark]]

**In one sentence:** The paper builds and evaluates a synthetic bicycle-factory benchmark (UFK-M) where every question is generated answer-first — SQL written and validated against the database before the natural-language question exists — and tests seven backbone LLMs across four providers under three agentic baselines with deterministic scoring and bootstrap uncertainty.

- UFK-M is a fully synthetic bicycle-assembly factory inspired by real client factories; a founding text states its operational rules, KPIs and industry concepts in prose, backed by a SQL data layer (DuckDB tables) and a semantic layer (a knowledge graph that distills the founding text and maps it onto the tables).
- The benchmark has two nested tiers (large and xlarge) that scale without removing information; baselines are evaluated mostly on xlarge.
- Questions are generated in reverse: an LLM writes a SQL program over sampled schema cards, it is executed and kept only if non-empty, non-degenerate, and ≤10 rows, and only then is a natural-language question written that the result answers.
- Because the SQL is validated before questioning, every question is demonstrably answerable, and the gold answer is the actual output of a run program rather than model-generated text.
- The frozen xlarge set holds 258 questions: 116 table answers, 84 single values, 48 booleans, 10 lists; 147 need at most one join, 45 need two, 66 need three or more; 34 additionally require the semantic layer (a named rule or KPI whose resolved value or formula stays hidden).
- Correctness is decided by a deterministic matcher, not an LLM judge: numerics compared with rounding tolerance, percentages scale-free (fraction vs. percentage independent), tables scored by recall of required gold rows.
- Seven backbone configurations across four providers are tested: DeepSeek V4-Flash (non-thinking, the reference), DeepSeek V4-Pro and V4-Pro-Think (same weights, reasoning off vs. on), GPT-5 Nano (low/high reasoning effort), GLM-4.5-Air, and Qwen3-Coder-Flash.
- Each backbone runs under three agentic baselines: GRA and RSA get 45 LLM-call turns (retrieving via the local embedder multilingual-e5-large-instruct), while SQA gets 6 turns and the full schema in its prompt with no retrieval; SQL tools cap results at 50 rows.
- All models decode greedily (temperature 0), completions capped at 1,024 tokens (8,192 for thinking configurations); primary results use the validated 258-question xlarge set, and uncertainty is quantified via paired bootstrap over questions (B = 104) with 95% percentile intervals.

## 3. [[wiki/03-results|Results]]

**In one sentence:** On the frozen xlarge benchmark (n = 258), GRA wins with the DeepSeek and GLM backbones while losing to SQA with Qwen3-Coder-Flash and GPT-5 Nano, and the pattern is explained not by extended reasoning but by tool-call reliability, low unique-input-token usage (GRA reads only ~29–33% of SQA's unique input), and a tool-call budget with a knee around B ≈ 30.

- GRA outperforms SQA with DeepSeek V4-Flash (+17.9% relative error reduction), V4-Pro (+26.4%), V4-Pro-Think (+30.5%), and GLM-4.5-Air (+13.5%), but loses with Qwen3-Coder-Flash (−12.1%) and GPT-5 Nano (−22.9%).
- The best per-model accuracies are 87.6–88.4% for the DeepSeek configurations (GRA) versus 74.0–83.3% for SQA, with 95% paired-bootstrap intervals of ±3.9 to ±5.3 pp.
- Tool-call reliability is the dominant factor: under GRA, the three DeepSeek configurations fail under 1% of calls, GPT-5 Nano fails 10.2% of calls (51.6% of questions with ≥1 failure), and enabling reasoning on GPT-5 Nano roughly halves both failure measures (10.2% → 5.8% of calls, 51.6% → 34.9% of questions) for a +6.2 pp accuracy gain.
- Token usage: GRA reads 29–33% of SQA's unique input tokens and RSA 24–29% (measured per question as unique tokens, counting each token once per trajectory); for DeepSeek V4-Flash/V4-Pro SQA's 17.2 k unique input vs. GRA's ~5 k and RSA's 4–5 k.
- Output tokens reverse the pattern: SQA produces 0.5–1.3 k completion tokens per question (single SQL block; e.g. 0.56–0.82 k for V4-Flash/V4-Pro), while the multi-turn agents produce 1.0–2.0 k (e.g. 1.56–1.68 k).
- Billed vs. unique tokens diverge because GRA/RSA resend a growing context over 11–15 turns while SQA averages fewer than three; warm-cache batch eval favours SQA, cold-start single-question serving favours the agents (SQA re-pays its full 17 k-token prompt per question).
- Tool-call budget: accuracy rises sharply from B = 10 to B = 30 then plateaus on both the large (N = 148) and xlarge (N = 258) sets, with truncated questions dropping from 62 → 3 (large) and 118 → 11 (xlarge).
- At B = 10, xlarge accuracy is 63.6%; mean tool-calling turns stabilize at ~11 (large) and ~13 (xlarge) once truncation is rare; no measurable gain above B ≈ 30 calls.
- The budget-aware GRA agent receives the budget up front and a warning after roughly 80% of it is consumed.

## 4. [[wiki/04-industrial-deployment|Industrial Deployment]]

**In one sentence:** In a factory, GRA — the block benchmarked in the earlier sections — sits inside a wider deployment loop where an operator's plain-language rule is feasibility-verified by GRA with graph evidence, and accepted rules are compiled by the Operational Research Agent (ORA) into optimization models and solver code; the chunk demonstrates both outcomes with two fully traced worked examples and closes the paper.

- The chunk opens with the final analysis from the benchmark: selective agentic access (not graph topology per se) is GRA's main advantage — +5.1 pp over SQA while reading only 29–33% of SQA's unique input tokens — while the gain over RSA is just +0.3 to +1.9 pp, and the agentic edge shrinks or reverses once tool-call failures exceed a few percent.
- The current corpus is small enough that SQA's 17 k-token prompt fits every model's context window, so the regime where structured navigation helps most (serialization infeasible or too costly) is still untested.
- In deployment, the operator states a rule in plain language; the orchestrator asks GRA for a feasibility verdict, which GRA grounds by navigating the UFK-M hybrid knowledge graph with the generic tools of Table 1, returning a verdict with citations.
- Deployment adds exactly one write primitive, `edit`, used only to register approved rules, and it is outside the benchmarked toolkit; accepted rules go to ORA, which compiles them into mathematical optimization models and solver code (Gurobi, OR-Tools, Hexaly, RL policies) and registers them back into the graph as new rule nodes.
- Plans and execution logs return to the data layer, so the graph substrate keeps accumulating what the loop decides.
- Example 1: the well-formed rule "Aluminium frames go to welding station 1 or 2 on Monday" is **refused for two independent reasons** found only at question time — a conflict with quality rule R7 (station 1 welds carbon frames only) and a capacity shortfall (measured history ≈1,300 min vs. 960 min available) — with two repair options offered.
- Example 2: the rule "At most three colour changes per shift on line 1" is judged **feasible with a measured seasonal risk** (11 of 428 recorded shifts would break the cap), and after operator confirmation and expert pull-request approval, ORA compiles it into a mathematical model plus `scheduling.mzn` code and registers it as node R23.
- The Conclusion: like a coding agent navigating an unfamiliar codebase, GRA answers with seven generic primitives on a graph it has never seen — "seeing less, the agent answers better"; beyond QA it supports rule-feasibility judgment, and the next step is making ORA's natural-language → formula → solver-code translation reliable, verifiable, and grounded in the graph.

## The argument in five moves

1. Code agents navigate unfamiliar codebases with a few generic file-system commands instead of reading everything — the claim is that this transfers to hybrid knowledge graphs unchanged.
2. GRA implements that transfer literally: seven tools, nothing domain-specific, tested against RSA (same loop, no graph) and SQA (serialize everything) to isolate what actually drives any gain.
3. UFK-M, a synthetic-but-realistic factory benchmark with answer-first, SQL-validated questions, gives all three agents a fair, deterministically-scored 258-question test.
4. GRA wins by 5.1pp over SQA on reliable tool-callers while reading under a third of the tokens — but the gain over RSA is small (+0.3 to +1.9pp), so selective access, not graph topology, is doing most of the work, and the whole advantage depends on the backbone reliably calling tools.
5. Deployed inside a real factory loop, the same agent turns plain-language scheduling rules into grounded feasibility verdicts — refusing one, accepting another with quantified risk — feeding a downstream agent (ORA) that compiles accepted rules into solver code.
