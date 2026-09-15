---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: The Bitter Lesson of Tool Calling

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What is the structural difference between how JSON tool calling and programmatic tool calling resolve a two-step chained call (where step 2 needs step 1's result)?

> [!tip]- Answer
> JSON tool calling needs two separate inference turns: the model calls f1, receives its return value in the conversation, then calls f2. Programmatic tool calling writes both calls into a single Python script executed in one subprocess — the model computes the intermediate value in code and passes it directly to f2, resolving the whole chain in one LLM turn. See [[wiki/02-method|Method]].

### Q2. The paper finds that PTC viability splits models into "wins" and "losses" — what actually predicts which side a model falls on, and what specifically causes the losing models to underperform?

> [!tip]- Answer
> Model *generation* (how recently it was trained), not vendor/family, predicts the split — all five Anthropic models and the three newest GPT-5.6 models win or tie, while three older/weaker OpenAI models (GPT-4o, GPT-4.1, GPT-5.4-mini) lose. The specific cause is a code-generation bug: those three models emit literal `\n` escape sequences instead of real newline characters in multiline Python, causing subprocess syntax errors. See [[wiki/04-analysis|Analysis]].

### Q3. Why does JSON tool calling's accuracy collapse at high fan-out while programmatic tool calling's does not, and where does this collapse begin for Claude Sonnet 5?

> [!tip]- Answer
> JSON tool calling must emit a parallel tool-call block containing every call in a single response; past a threshold the model starts omitting calls. Programmatic tool calling expresses fan-out as a loop or `asyncio.gather` in a script, which has no structural cap on call count. For Claude Sonnet 5's baseline, enumeration accuracy is 100% at N ≤ 70, drops to 75% at N = 72, and reaches 0% at N = 100, while PTC holds 100% at both N = 72 and N = 100. See [[wiki/04-analysis|Analysis]].

### Q4. What is "enumeration accuracy" and why do the authors report it separately from aggregation accuracy on the parallelism ablation?

> [!tip]- Answer
> Enumeration accuracy measures whether the model actually issued all N required tool calls; aggregation accuracy measures whether it produced the correct final aggregate answer. They're reported separately because several models produce a correct aggregate answer from parametric world knowledge without executing the enumeration calls at all — a shortcut that would inflate perceived tool-use fidelity if only the final answer were scored. See [[wiki/03-experiments|Experiments]].

### Q5. At roughly what fan-out count (N) does token cost cross over between JSON and programmatic tool calling, and why does the direction reverse at that point?

> [!tip]- Answer
> The crossover is around N ≈ 26. Below it, programmatic tool calling is more expensive because of its fixed system-prompt overhead (the full stub-module source embedded in the prompt). Above it, JSON tool calling becomes more expensive because its response must enumerate all N individual tool-call objects, which grows with N while PTC's script size grows much more slowly. See [[wiki/03-experiments|Experiments]].

### Q6. Under context flooding (128 schemas vs. filtered), how do JSON tool calling, programmatic tool calling, and the filesystem-discovery reference condition each change, and what does the PTC direction (up, not just stable) suggest is happening?

> [!tip]- Answer
> JSON tool calling degrades a mean −2.3%, programmatic tool calling *improves* a mean +5.5%, and the filesystem-discovery condition degrades sharply at −32.0% (every model declines). PTC's improvement is driven by models that struggled with the strict type constraints of the filtered condition but benefited from the flood condition's richer context to identify the correct function — i.e., extra (irrelevant) schemas sometimes helped rather than hurt these specific models. See [[wiki/03-experiments|Experiments]].

### Q7. What are the paper's own stated limitations regarding sample size, and what specifically can and cannot be claimed given them?

> [!tip]- Answer
> Ablation entry counts are small (n = 31–52 per condition), producing wide confidence intervals, so individual per-model results should be read as directional, not conclusive. Only aggregate cross-model patterns — such as "11 of 14 models" on the main evaluation or the consistent PTC improvement under context flood — are large enough to be interpreted reliably. See [[wiki/05-conclusion-and-limitations|Conclusion and Limitations]].

### Q8. BFCL v4 uses echo-return stubs where tool calls return their own arguments verbatim rather than executing real actions. Given this, what is the single weakest link in this paper's evidence, and why?

> [!tip]- Answer
> The echo-return-stub limitation is the weakest link: because no tool call has real latency, unpredictable output, or side effects, programmatic tool calling's chaining advantage (computing an intermediate value once, in a single subprocess) is measured only in a world where the model can often shortcut with parametric knowledge instead of genuinely depending on a prior call's real return value. The advantage could shrink in production settings with real, unpredictable tool responses that require true multi-turn adaptation. See [[critical_thinking|Critical Analysis]].
