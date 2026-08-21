[[../index|Wiki]] | [[../summary|Summary]]

# Industrial Deployment: the Loop Around GRA, Two Worked Examples, and the Conclusion

**In one sentence:** In a factory, GRA — the block benchmarked in the earlier sections — sits inside a wider deployment loop where an operator's plain-language rule is feasibility-verified by GRA with graph evidence, and accepted rules are compiled by the Operational Research Agent (ORA) into optimization models and solver code; the chunk demonstrates both outcomes with two fully traced worked examples and closes the paper.

## Key points

- The chunk opens with the final analysis from the benchmark: selective agentic access (not graph topology per se) is GRA's main advantage — +5.1 pp over SQA while reading only 29–33% of SQA's unique input tokens — while the gain over RSA is just +0.3 to +1.9 pp, and the agentic edge shrinks or reverses once tool-call failures exceed a few percent.
- The current corpus is small enough that SQA's 17 k-token prompt fits every model's context window, so the regime where structured navigation helps most (serialization infeasible or too costly) is still untested.
- In deployment, the operator states a rule in plain language; the orchestrator asks GRA for a feasibility verdict, which GRA grounds by navigating the UFK-M hybrid knowledge graph with the generic tools of Table 1, returning a verdict with citations.
- Deployment adds exactly one write primitive, `edit`, used only to register approved rules, and it is outside the benchmarked toolkit; accepted rules go to ORA, which compiles them into mathematical optimization models and solver code (Gurobi, OR-Tools, Hexaly, RL policies) and registers them back into the graph as new rule nodes.
- Plans and execution logs return to the data layer, so the graph substrate keeps accumulating what the loop decides.
- Example 1: the well-formed rule "Aluminium frames go to welding station 1 or 2 on Monday" is **refused for two independent reasons** found only at question time — a conflict with quality rule R7 (station 1 welds carbon frames only) and a capacity shortfall (measured history ≈1,300 min vs. 960 min available) — with two repair options offered.
- Example 2: the rule "At most three colour changes per shift on line 1" is judged **feasible with a measured seasonal risk** (11 of 428 recorded shifts would break the cap), and after operator confirmation and expert pull-request approval, ORA compiles it into a mathematical model plus `scheduling.mzn` code and registers it as node R23.
- The Conclusion: like a coding agent navigating an unfamiliar codebase, GRA answers with seven generic primitives on a graph it has never seen — "seeing less, the agent answers better"; beyond QA it supports rule-feasibility judgment, and the next step is making ORA's natural-language → formula → solver-code translation reliable, verifiable, and grounded in the graph.

## Detail

### Tail of the "Further analysis" section

The chunk begins with the closing assessment of the benchmark results: taken together, **selective agentic access is identified as the primary source of GRA's advantage**. On models that call tools reliably, both agents (GRA and RSA) outperform SQA, with GRA achieving the largest well-supported gain at +5.1 pp while reading only 29–33% of SQA's unique input tokens. That efficiency should matter more as the corpus grows beyond a single prompt, because SQA's cost scales with the full serialized context while the agents read only the fraction they retrieve.

The contribution of **graph topology is much less clear**: GRA exceeds RSA by only +0.3 to +1.9 pp, and the two are indistinguishable on DeepSeek V4-Pro — so the gain over SQA comes mainly from how context is accessed rather than from graph structure itself. **Reliability sets the boundary**: the agentic advantage shrinks or reverses once tool-call failures exceed a few percent, which is why full-context inference remains preferable for weaker tool-callers. And because the current corpus is small enough that SQA's 17 k-token prompt fits comfortably in every model's context window, the regime where structured navigation should help most — where serialization is infeasible or too costly — remains to be tested on substantially larger graphs.

### The deployment loop (structure of Figure 3)

The benchmarked sections measured GRA as a question-answering block; in a factory, the same block sits inside a wider loop (described by the paper in Figure 3, rendered here as structure):

- **Heterogeneous sources** — documents, spreadsheets, databases, sensor and operator logs — feed an **LLM-driven construction** of the **UFK-M hybrid knowledge graph**, a versioned, auditable source of truth with two layers:
  - **Semantic layer**: concepts, operational rules, KPIs
  - **Data layer**: tables (orders, operations, changeovers), *backed by* the semantic layer
- The **operator** states a **rule** in plain language.
- The **orchestrator** routes and reports: it asks GRA **"feasible?"** and returns the **report** to the operator.
- **GRA (graph agent)** answers feasibility questions by navigating the graph with its **tools** (`ls · cat · grep`, `sems · query`, `edit · think`), receiving **graph context**. It is the block evaluated in Sections 6–7.
- **ORA (Operational Research Agent)** compiles rules into models and code and **registers rules** back into the graph.
- **Solvers** (Gurobi · OR-Tools · Hexaly · RL policies) run **models and code** to produce **plans and execution logs**, which flow back to the data layer.

In plain terms: an operator states a rule in plain language; the orchestrator receives it and asks GRA whether the rule is feasible; GRA gathers its evidence by navigating the graph with the generic tools of Table 1 and returns a verdict with citations; deployment adds one write primitive, `edit`, used only to register approved rules (outside the benchmarked toolkit); accepted rules are passed to ORA, which turns them into mathematical optimization models and solver code and registers them back into the graph as new rule nodes; and plans plus execution logs return to the data layer, so the substrate accumulates what the loop decides. The two worked examples follow the two possible outcomes — a rule that must be refused, and a rule that is accepted and compiled.

### Example 1 — Refusing an impossible rule, with evidence

**Operator query.** "Aluminium frames go to welding station 1 or 2 on Monday; station 3 is under maintenance." The sentence is clear, well-formed, and would compile into a valid constraint — and it is also impossible, for two reasons that live in two different places.

**GRA's reasoning (four steps):**

1. **Find what the words point to.** The three welding stations are located in the graph, together with the table that records welding operations.
2. **A hidden rule excludes station 1.** Listing the edges of station 1 surfaces an older quality rule (node **R7**): station 1 welds **carbon frames only**, because aluminium dust damages carbon parts. The rule speaks about carbon, the request about aluminium — the two share no word, yet in the graph the rule sits one edge from the station. Station 1 is out; only station 2 remains.
3. **At standard times, the day barely fits.** No stored value answers "can one station absorb the whole Monday?", so the agent computes it: the aluminium frames due that day, multiplied by the standard welding time, need **936 minutes**, and the working calendar (rule **R11**: two shifts of eight hours) offers **960**. On paper, the rule passes.
4. **Measured history says otherwise.** The agent checks the standard against durations actually recorded over past months: real welds run about a third longer than the standard, and each switch of material on the station costs extra minutes. Recomputed with measured values, the day needs about **1,300 minutes** — a shortfall of more than a full shift.

**GRA's advice.** The rule is **refused for two independent reasons**: a conflict with an active quality rule, and a capacity shortfall that only appears when measured history replaces standard times. The refusal comes with its evidence and two repair options: (a) suspend the carbon-only rule for one day (requires quality approval), or (b) move three orders to Tuesday (two deliveries become late). Neither the conflict nor the shortfall was stored anywhere; both were found, or computed, at question time.

**Tool-call reasoning trace — nine calls, all from Table 1:**

| Call | What it does |
|------|-------------|
| `sems("welding station")` | locate the three stations in the graph |
| `ls(welding station 1)` | list its edges — the carbon-only rule appears |
| `cat(rule R7)` | read it: station 1 welds carbon frames only |
| `cat(rule R11)` | daily workload: two shifts, 960 minutes |
| `query` (SQL) | Monday load at standard times: 936 minutes |
| `query` (SQL) | measured weld durations: a third above standard |
| `query` (SQL) | changeover minutes on station 2 |
| `think` | recompute the load: ≈1,300 for 960 available |
| `answer` | refusal, two repairs, evidence cited |

### Example 2 — Compiling an accepted rule into the scheduling model

**Operator query.** "At most three colour changes per shift on line 1." This rule is admissible — but the scheduling model (MiniZinc code file `scheduling.mzn`) has no object named "colour change", so accepting it takes more than approval: someone must decide what it means, check it against history, and write it into the model.

**GRA's reasoning (four steps):**

1. **Find what the words point to.** "Colour change" refers, through a concept node, to the table that logs every changeover; "shift" refers to the working calendar (rule **R11**): two shifts of eight hours per day.
2. **Check for conflicts.** Listing what already governs line 1 surfaces no rule that contradicts the request.
3. **Replay history.** No stored value can judge this rule, so the agent must count the colours due on each of the **428 shifts** in the recorded history.
4. **Quantify the risk.** On **11** of those shifts more than three changes were unavoidable — on those days the rule would have made planning impossible.

**GRA's advice.** Verdict: **feasible, with a measured seasonal risk**. The agent returns the verdict with two ways to adopt the rule: as a hard limit with a manual override for peak days, or as a soft constraint penalised in the objective, which the solver may violate at a bounded cost when a shift would otherwise be infeasible. The operator confirms the **hard form**. As before, the verdict existed nowhere as stored text — it was computed from the tables at question time.

**ORA compilation.** Once the operator approves, ORA turns the rule into something the solver can run: it first writes the rule as a mathematical constraint — a new variable for the order of jobs on line 1 (`X_s`), a marker for each colour change (`chgs ≥ k_s − 1`), and one line capping the changes per shift at three (`chgs ≤ 3` per shift) — then implements it in the solver code. The same rule now exists in two matching forms: the mathematical model and the `scheduling.mzn` code.

**Human approval and write-back.** The mathematical formulation and the exact lines of code are sent to Oplit's OR experts as a **pull request**, which they review and approve before anything is merged. Only then does the accepted rule become node **R23** in the graph, linked to the exact lines of `scheduling.mzn` and to the validation evidence.

**Tool-call reasoning trace — six calls to reach the verdict, plus ORA and one edit after the pull request is approved:**

| Call | What it does |
|------|-------------|
| `sems("colour change")` | resolve the phrase: a concept node, backed by the changeover table |
| `cat(rule R11)` | what a shift is: two shifts of eight hours per day |
| `ls(line 1)` | list what already governs the line — no conflict |
| `query` (SQL) | colours due per shift, over the 428 recorded shifts |
| `think` | weigh the result: is the risk acceptable? |
| `answer` | feasible, seasonal risk quantified — the operator confirms |
| ORA | formalises the mathematical model, then writes the solver code |
| `edit` | registers rule R23, linked to the new code and the evidence |

### Conclusion

The paper closes with an analogy: a coding agent understands an unfamiliar codebase by **navigating it with a few generic commands rather than reading it whole**. This paper showed that a hybrid industrial knowledge graph admits the same interface — an agent with **seven generic primitives** answers analytical questions over a graph it has never seen, discovering the schema, vocabulary, tables, and join paths through tool use alone. On models that call tools reliably, this schema-agnostic GRA outperforms a full-context agent by up to 5.1 pp while reading a quarter to a third of its input. **Seeing less, the agent answers better**: selective navigation over a structured substrate beats exhaustive context.

Beyond question answering, GRA supports a harder task: inside the loop of Figure 3, it judges whether a new operational rule is feasible, crossing rules, tables, and computed results drawn from both the semantic and data layers. The graph is what makes this tractable — it exposes the paths along which a rule interacts with those already in force, sometimes several hops away, surfacing conflicts and limits that no single system records. A scattered manual investigation becomes a grounded, auditable verdict, produced with the same tools the agent was benchmarked on.

The next step is **ORA**: turning an approved rule into a running constraint requires translating natural language into a correct mathematical formulation, then into formal solver code that composes with the constraints already in force. Future work targets that translation, making it reliable, verifiable, and grounded in the graph.
