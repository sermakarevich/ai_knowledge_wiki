> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method

**In one sentence:** To test whether programmatic (inline Python) tool calling can replace JSON tool calling without sacrificing accuracy, the authors compare the two paradigms — plus a filesystem-discovery reference condition — on 309 BFCL v4 entries, three targeted ablation subsets, and 14 frontier models at temperature 0, with all accuracy computed by a single deterministic scorer under identical per-entry LLM-call accounting.

## Key points

- Each task entry gives a natural-language query `q`, a function set `F = {f_1, …, f_k}` with typed signatures, and ground-truth calls `C* = {(f_i, a_i)}`; correctness means the model's output matches `C*` under the benchmark's normalized string comparison (punctuation stripped, values lowercased), identically defined across all paradigms — only prompting and output parsing differ.
- In JSON tool calling the model emits structured JSON tool-call objects via the API (the standard deployment reference condition); in programmatic tool calling it writes one Python script over a typed stub module executed in a shell subprocess, with a stop middleware intercepting the next model call so both paradigms consume the same number of LLM calls per entry.
- The evaluation set is 309 BFCL v4 entries sampled proportionally across eight categories (`simple_python`, `multiple`, `parallel`, `parallel_multiple`, `live_simple`, `live_multiple`, `live_parallel`, `live_parallel_multiple`) with per-category minimums for small categories.
- Accuracy = fraction of entries where every required function call is present and correctly parameterized; a subprocess syntax/runtime error scores zero correct calls, and no entries are skipped or excluded.
- The chaining ablation contains `n = 52` entries covering chain lengths `n_chain = 2 – 20`, weighted toward longer chains where paradigms diverge most (`n_chain ≥ 6`: 17 entries; `n_chain ≥ 13`: 10 entries) — chaining needs two model turns in JSON mode but one script in programmatic mode.
- The parallelism ablation uses 32 enumeration-type entries with fan-out counts of 7, 9, 11, 13, 15, 20, 30, 48 (32 of 48 total; aggregation-type entries excluded from accuracy figures), plus probe entries at `N ∈ {60, 70, 72, 75, 100}` to find where Claude Sonnet 5 begins dropping calls under JSON tool calling; enumeration accuracy and aggregation accuracy are reported separately.
- The context rot ablation (31 entries per condition, drawn from the `live_multiple`, `live_parallel`, `live_parallel_multiple` categories) contrasts a `filtered` condition (only the functions the query uses) against a `flood` condition of 128 total schemas mixing relevant functions with decoys from unrelated domains.
- 14 models across Anthropic and OpenAI families, spanning releases from November 2024 to July 2026, are all run at temperature 0, with 95% Wilson confidence intervals per row; small ablation subsets (`n = 31 – 52`) mean per-model results are directional, and only cross-model aggregate patterns are treated as reliable.

---

## Task Definition

Each benchmark entry specifies a natural-language user query `q`, a set of available functions `F = {f_1, …, f_k}` each with a typed signature, and a ground-truth set of function calls `C* = {(f_i, a_i)}` where `a_i` is the argument mapping for call `i`. A model is correct on an entry if and only if its output produces a set of calls that matches `C*` under the benchmark's normalized string comparison, which strips punctuation and lowercases all values before matching. This definition is identical across all three paradigms; differences arise only in how the model is prompted and how its output is parsed.

## Paradigms: JSON tool calling vs. programmatic tool calling

**JSON tool calling.** The model receives a system prompt containing the function schemas formatted as JSON tool definitions and an API call that invokes the tool-calling endpoint. The model outputs a structured JSON object at each function call. This is the standard deployment pattern for tool-augmented LLMs and serves as the reference condition.

**Programmatic tool calling.** The model receives a system prompt that embeds the source of a typed Python module whose functions correspond one-to-one with the benchmark's function schemas. Each stub function captures its arguments and returns them as a structured dict; no external service is contacted. The model writes a Python script that imports this module and calls the appropriate functions. The agent loop executes the script in a native shell subprocess, captures stdout, and the scorer extracts function names and argument values from the printed output. No additional inference turns occur after the subprocess returns: a stop middleware intercepts the next model call and terminates the agent loop. This design ensures that programmatic tool calling and JSON tool calling consume the same number of LLM calls per entry, making accuracy comparisons straightforward.

**Worked example.** A task asks for the circumference of a circle with radius 7 and the area of a square with side 5. In JSON tool calling, the model emits two sequential JSON tool-call objects. In programmatic tool calling, the model writes one script — `execute(command="python3 -c 'import json; from stubs import circumference, area_square; print(json.dumps(circumference(radius=7))); print(json.dumps(area_square(side=5)))'")` — the subprocess captures both lines of stdout, and the scorer matches each printed call against the ground truth. Programmatic tool calling resolves both calls in a single Python expression evaluated in one subprocess, while JSON tool calling requires two separate model outputs.

![Overview of the two primary paradigms evaluated](images/fig1-paradigm-overview.png)

Figure 1 is a side-by-side process diagram holding inputs (task description, function catalog) constant while contrasting the two execution pipelines: the JSON baseline emits one JSON tool-call object per function and needs an extra LLM turn for chained calls, whereas the programmatic pipeline runs all calls in one script in a single subprocess and a stop middleware suppresses the second LLM turn. A dashed filesystem-discovery condition is shown as a secondary reference point, consistent with the primary contrast between per-turn JSON round-trips and single-subscript script execution.

## Benchmark and Evaluation

BFCL v4 (Vaghasiya et al., 2026) provides 309 representative entries drawn from eight task categories: `simple_python`, `multiple`, `parallel`, `parallel_multiple`, `live_simple`, `live_multiple`, `live_parallel`, and `live_parallel_multiple`. Entries were sampled proportionally to mirror the category distribution of the full BFCL v4 benchmark, with per-category minimums applied to ensure sufficient entries in smaller categories. The complete entry ID list is released with the evaluation harness. Simple and multiple categories test single-call and multi-call accuracy on curated queries; live categories use queries sampled from real user interactions; parallel categories require the model to issue two or more function calls whose arguments are independent of each other. All three paradigms use a deterministic scorer that normalizes predicted and ground-truth argument values before comparison. Accuracy is reported as the fraction of entries where every required function call is both present and correctly parameterized. When the shell subprocess raises a syntax or runtime error, the entry is scored as zero correct calls. No entries are skipped or excluded from reported totals.

## Ablation Design

The three ablation studies target task structures where paradigm choice has been claimed to matter. Each ablation subset was constructed by selecting entries from BFCL v4 that represent the target task structure without duplicating main-evaluation entries; the complete entry ID lists are released with the evaluation harness.

**Chaining.** Sequential multi-hop function calls, where the output of `f_1` must be computed and passed as an argument to `f_2`. In JSON tool calling this requires two model turns (call `f_1`, receive the return value, then call `f_2`); in programmatic tool calling both calls appear in a single script, with the model computing the intermediate value using parametric knowledge and passing it directly. The chaining subset (`n = 52`) was optimized to cover the full range of chain lengths (`n_chain = 2 – 20`), with the distribution weighted toward longer chains where JSON tool calling and programmatic tool calling diverge most (`n_chain ≥ 6`: 17 entries; `n_chain ≥ 13`: 10 entries).

**Parallelism.** Independent fan-out function calls, where `N` calls must be issued in a single step. JSON tool calling issues them as parallel tool-call objects; programmatic tool calling writes an `asyncio.gather` block or a sequential loop. The parallelism subset (`n = 32`) covers fan-out counts of 7 to 48 (7, 9, 11, 13, 15, 20, 30, 48), drawn from a synthetic corpus. Only enumeration-type entries are reported (`n = 32` of 48 total), excluding aggregation-type entries from the accuracy figures. To locate the fan-out threshold at which Anthropic frontier models begin dropping calls under JSON tool calling, the corpus is extended with probe entries at `N ∈ {60, 70, 72, 75, 100}` and evaluated with Claude Sonnet 5 baseline and programmatic tool calling. Enumeration accuracy (did the model issue all `N` required calls?) and aggregation accuracy (did the model produce the correct aggregate answer?) are reported separately, since programmatic tool calling can answer aggregation questions from parametric knowledge without executing every call.

**Context rot.** The flood condition injects decoy function schemas into the context alongside the entry's relevant schemas, increasing total context size to 128 schemas. The two conditions are `filtered` (only the functions the query uses) and `flood` (128 total schemas, including the relevant functions plus corpus decoys drawn from unrelated domains). The context rot subset uses 31 entries per condition, drawn from the `live_multiple`, `live_parallel`, and `live_parallel_multiple` categories, where function schemas are most easily contaminated by domain-unrelated decoys.

## Models

We evaluate 14 models spanning two families and 20 months of releases (Table 1), all run at temperature 0:

- **Anthropic:** Claude Haiku 4.5 (`claude-haiku-4-5`), Claude Sonnet 4.5 (`claude-sonnet-4-5`), Claude Sonnet 4.6 (`claude-sonnet-4-6`), Claude Opus 4.8 (`claude-opus-4-8`), Claude Sonnet 5 (`claude-sonnet-5`)
- **OpenAI:** GPT-4o (`gpt-4o-2024-11-20`), GPT-4.1 (`gpt-4.1-2025-04-14`), GPT-5-nano (`gpt-5-nano-2025-08-07`), GPT-5 (`gpt-5-2025-08-07`), GPT-5.4-mini (`gpt-5.4-mini-2026-03-17`), GPT-5.4 (`gpt-5.4-2026-03-05`), GPT-5.6-Luna (`gpt-5.6-luna`), GPT-5.6-Sol (`gpt-5.6-sol`), GPT-5.6-Terra (`gpt-5.6-terra`)

All tables report 95% Wilson confidence intervals per row. Because ablation entries are small (`n = 31 – 52`), intervals are wide and individual model results should be treated as directional rather than conclusive. Only cross-model aggregate patterns are interpreted as reliable findings. Pairwise per-model comparisons are not corrected for multiple testing, and no claim is made that any individual model result is statistically significant in isolation.

**Covers:** Section 3 (Method): 3.1 Task Definition, 3.2 Paradigms, 3.3 Benchmark and Evaluation, 3.4 Ablation Design, 3.5 Models; Figure 1
