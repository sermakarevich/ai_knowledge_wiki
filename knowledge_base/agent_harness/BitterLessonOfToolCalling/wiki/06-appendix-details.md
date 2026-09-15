> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix Details

**In one sentence:** The appendices supply the per-category BFCL v4 accuracy breakdown (Table 6) behind the aggregate JSON-vs-PTC numbers, verbatim execution traces showing how a single-LLM-turn programmatic tool call chains and parallelizes stub calls, and the condensed system prompts and stub-module design that define the PTC harness.

## Key points

- Table 6 (Appendix A) reports mean per-category accuracy over all 14 models on BFCL v4 with 95% Wilson CI half-widths: overall JSON 78.6 ± 4.6 vs PTC 77.0 ± 4.7 — within each other's confidence intervals.
- PTC wins the live multi-call category strongly: live_multiple 83.0 ± 7.5 (PTC) vs 73.1 ± 8.7 (JSON), and live_parallel / live par. mult. 56.8 ± 18.4 (PTC) vs 66.1 ± 17.7 (JSON) — the parallel/live-parallel gaps are largely driven by three OpenAI models with `\n` encoding failures (stated in the table caption).
- JSON stays ahead on single-step categories: simple_python 89.5 ± 9.7 (PTC) vs 86.1 ± 10.7 (JSON).
- In B.1 (simple_python), the agent emits one `execute_python` call that imports a stub and prints a JSON dict to stdout; a stop middleware then intercepts the next model call, so the entry completes in a single LLM turn and the scorer recovers the function/argument mapping from stdout.
- In B.2 (chaining), PTC computes the intermediate value (`circ = 2 * math.pi * 7` ≈ 43.98) in Python and passes it to a second stub, so both tool calls resolve inside one subprocess and one LLM turn.
- In B.3 (parallelism/fan-out), one script fans out all seven country-lookup stubs concurrently via `asyncio.gather` over `asyncio.to_thread` and sorts the rankings in the same script — again a single subprocess, single LLM turn.
- Appendix C design: the PTC system prompt embeds the source of a typed Python stub module and requires exactly one `execute` call with a `python3 -c '...'` command that imports the module, calls the functions with correct arguments, and prints results as JSON using real newlines (not `\n` escapes) in multiline scripts.
- Stub modules are generated from the benchmark's function schema: each stub accepts the schema's typed keyword arguments, returns them as a structured dict printed to stdout, and contacts no external service; the scorer parses stdout, normalizes, and compares against ground truth.

---

## Per-Category Accuracy on BFCL v4 (Appendix A)

| Category | n | JSON ± | PTC ± |
|---|---|---|---|
| _simple_python_ | 40 | 86.1 ± 10.7 | **89.5** ± 9.7 |
| _multiple_ | 20 | **95.4** ± 11.1 | 93.9 ± 11.9 |
| _parallel_ | 40 | **85.5** ± 10.9 | 71.4 ± 13.5 |
| _par. multiple_ | 40 | **85.5** ± 10.9 | 71.4 ± 13.5 |
| _live_simple_ | 25 | **76.6** ± 15.9 | 76.3 ± 15.9 |
| _live_multiple_ | 96 | 73.1 ± 8.7 | **83.0** ± 7.5 |
| _live_parallel_ | 24 | **66.1** ± 17.7 | 56.8 ± 18.4 |
| _live par. mult._ | 24 | **66.1** ± 17.7 | 56.8 ± 18.4 |
| **Overall** | 309 | **78.6** ± 4.6 | 77.0 ± 4.7 |

*Table 6: Mean accuracy (%) per BFCL v4 category, averaged across all 14 models. JSON = JSON tool calling; PTC = programmatic tool calling. Means are macro-averaged over models. ± columns show 95% Wilson CI half-widths. Bold indicates the higher value per row. The `parallel` and `par. multiple` gaps are largely driven by the three OpenAI models with `\n` encoding failures.*

The category-level breakdown shows the aggregate near-tie hiding an opposite split: JSON leads every single-step and parallel-simulation category, while PTC leads every live multi-call category — most decisively `live_multiple` (+9.9). The wide CIs (±8.7–18.4) in most rows indicate the per-category differences are statistically soft, with the stated exception of the `\n`-encoding failure mode concentrated in three OpenAI models on the parallel categories.

## Programmatic Tool Calling Worked Example (Appendix B)

Appendix B ("Walkthroughs") shows verbatim (lightly condensed, workspace paths shortened to `<workspace>/`) execution traces of the programmatic tool calling agent loop across three evaluation settings: a single call (B.1), a chained computation (B.2), and a parallel fan-out (B.3). Each demonstrates that PTC completes the entire entry — including intermediate value passing or concurrency — inside a single `execute_python` subprocess and a single LLM turn, with the stop middleware terminating the loop after the tool returns.

**B.1 — BFCL Single-Call (`simple_python`).** Task (`simple_python_0`): "Find the area of a triangle with a base of 10 units and height of 5 units." The stub module provided to the model contains:

```python
def calculate_triangle_area(
    base: int, height: int,
    unit: str | None = None) -> dict:
    """Calculate the area of a triangle."""
    return _rpc.call('calculate_triangle_area',
                      base=base, height=height,
                      unit=unit)
```

The agent emits a single tool call:

```python
execute_python(code="""
from stubs import calculate_triangle_area
result = calculate_triangle_area(base=10, height=5)
print(__import__('json').dumps(result))
""")
```

The subprocess prints:

```
{"calculate_triangle_area": {"base": 10, "height": 5}}
[exit code 0]
```

The stop middleware intercepts the next model call and terminates the loop. The scorer extracts function name and argument mapping from stdout, compares against ground truth, and records a single LLM turn for the entry.

**B.2 — Chaining Ablation.** Task (`chaining_0`): "Compute the circumference of a circle with radius 7, then use that circumference as the side length of a square to find the square's perimeter." The two relevant stubs are `geometry_circumference(radius)` and `geometry_square_perimeter(side)`. The agent writes a single script that computes the intermediate value in Python before passing it to the second stub:

```python
execute_python(code="""
import json, math
from stubs import (geometry_circumference,
                   geometry_square_perimeter)

f1 = geometry_circumference(radius=7)
circ = 2 * math.pi * 7  # 43.982...

f2 = geometry_square_perimeter(side=circ)
print(json.dumps(f1))
print(json.dumps(f2))
""")
```

Subprocess output:

```
{"geometry.circumference": {"radius": 7}}
{"geometry.square_perimeter": {"side": 43.98}}
[exit code 0]
```

Both calls are resolved in a single subprocess, completing the entry in a single LLM turn.

**B.3 — Parallelism Ablation.** Task (`fanout_population_7_a`): "Of these 7 countries — Zorbania, Keltross, Miventa, Drulan, Quelfor, Hartox, and Bivessa — which 3 have the largest population?" The available stub is `country_info_population(country: str) -> dict`. The agent issues one `execute_python` call that fans out all seven lookups concurrently and ranks the results in the same script:

```python
execute_python(code="""
import asyncio, json
from stubs import country_info_population

pop = country_info_population  # alias
async def main():
    cc = ["Zorbania","Keltross","Miventa",
          "Drulan","Quelfor","Hartox","Bivessa"]
    res = await asyncio.gather(*[
        asyncio.to_thread(pop, country=c) for c in cc
    ])
    pairs = sorted(zip(cc, [r["population"] for r in res]),
                   key=lambda x: x[1], reverse=True)
    top3 = [{"country": c, "population": p} for c, p in pairs[:3]]

    print(json.dumps({"answer": top3}))

asyncio.run(main())
""")
```

Subprocess output:

```
{"answer": [
    {"country":"Bivessa","population":891234567},
    {"country":"Zorbania","population":847293441},
    {"country":"Miventa","population":523019876}]}
[exit code 0]
```

All seven stubs are invoked in parallel and Python sorts the results in the same script, completing the entry in a single LLM turn.

## System Prompts (Appendix C)

**JSON tool calling system prompt (condensed).** The JSON tool calling prompt instructs the model to call the provided tool definitions using the tool-calling API and to emit one JSON tool-call object per required function invocation, with no additional prose. Function schemas are passed as the `tools` parameter of the API request.

**Programmatic tool calling system prompt (condensed).** The programmatic tool calling prompt embeds the source of a typed Python stub module and instructs the model to call `execute` exactly once with a `python3 -c '...'` command that imports the module, calls the required functions with the correct arguments, and prints results as JSON. The prompt specifies that real newlines (not `\n` escape sequences) must be used in multiline scripts. The stop middleware intercepts the first model call after the `execute` tool returns and terminates the agent loop without issuing a second inference.

**Stub module design.** Each stub function is generated from the benchmark's function schema. It accepts the schema's typed keyword arguments, immediately returns them as a structured dict, and prints the result to stdout. No external service is contacted. The scorer parses stdout to recover function name and argument mapping, then normalizes and compares against ground truth.

**Covers:** Appendix A (Table 6), Appendix B, Appendix C
