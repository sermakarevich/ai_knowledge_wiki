> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Capability Tests and the Stress-Test Deep Dive

**In one sentence:** The capability suite shows current LLMs have near-universal fluency (97.9%) with the raw NOOA interface, but a harder six-family stress-test subset drops to 84.7% and opens a 23-point gap between small and frontier models, and Appendix B's four byte-identical-context transcripts of the hardest stress test show these residual failures are lapses in disciplined harness use — not failures to understand the interface.

## Key points

- The capability suite runs 88 targeted tests across 36 families, five times each across ten models (4,400 records total), finding 97.9% overall pass rate, confirming models can call typed methods, interpret truncated previews, manage state, and return typed values through the harness with little difficulty.
- On the six-family stress-test subset (batch bookkeeping, error recovery, REPL exploration, refinement, task decomposition), pass rates fall to 84.7% (254/300 records), and the small/efficient-vs-large/frontier gap widens from 3.2 points overall to 23 points (70.8% vs 93.9%).
- The reasoning-mode ablation shows inference-time reasoning acts as a **capability equalizer** for smaller models — Nemotron 3 Nano improves 52.5% → 84.8% and the mid-size "Super-v3" variant improves 83.7% → 96.4% with reasoning on — while frontier models like Opus 4.8 (100.0%/99.5%) and GPT-5.5 (99.5%/98.6%) are already saturated regardless of mode.
- Repeating each test five times separates two failure modes by scale: across 880 (test, model) pairs, 94% pass all five runs; **large models have zero 0/5 stress-test scores** (every large-model stress failure is an intermittent reliability miss), while 12.5% of small-model stress pairs fail all five runs (a genuinely absent capability) and 42% are intermittent.
- `sentiment_batch` is the single hardest stress test (31/50, 62% overall), and Appendix B reproduces four complete, byte-identical-context transcripts of it to show exactly why two models pass and two fail.
- Nemotron 3 Ultra and GPT-5.5 passed via opposite strategies — Ultra fanned out per-item classification with `@strategy(PredictStrategy())` and `asyncio.gather`, then called `return_result(results)` inside the same cell (9.6s end-to-end); GPT-5.5 used no subagents at all, manually printing and hand-labeling all 50 items before returning the live `labels` list — both succeeded because they returned an already-computed live variable rather than retyping it.
- Claude Opus 4.8 failed despite its first cell executing the correct subagent fan-out pattern (all 50 classifications correct in the printed output): on the next turn it hand-transcribed the printed results into a literal for a separate `return_result` call instead of calling `return_result(results)` on the live variable, dropping item 43 and producing a 49-item list — a transcription lapse, not a comprehension failure.
- GPT-5.4 Mini failed by writing a keyword-rule classifier fitted only to the ~25 texts visible in the truncated preview, then applying it blind to all 50 live items — mechanically correct interface use (it iterated the true 50-item variable) but a direct violation of the strategy prompt's explicit instruction to use LLM reasoning rather than keyword-matching for language tasks.

---

Before evaluating complete NOOA agents on end-to-end benchmarks (see [[05-swebench-terminal-bench-and-cybergym|SWE-bench, Terminal-Bench, and CyberGym]]), the paper asks a narrower, prior question: do current LLMs actually understand and correctly operate the [[02-agent-loop-strategies-and-context|NOOA interface]] — typed method calls, pass-by-reference state, bounded/truncated previews, and the `execute_python` / `return_result` CodeAct loop? Section 4.1 answers this with a suite of 88 targeted **capability tests** run five times across ten models (4,400 records), finding near-universal interface fluency (97.9% overall). It then isolates six harder **stress tests** — bookkeeping over large batches, error recovery, REPL exploration, refinement, and task decomposition — where pass rates fall to 84.7% and a 23-point gap opens between small/efficient and large/frontier models. Appendix B makes this concrete: it reproduces four complete, byte-identical-context transcripts of the single hardest stress test, `sentiment_batch`, showing exactly how two models pass and two fail — and that the failures are not comprehension failures but lapses in disciplined harness use.

## Capability-Test Methodology

The capability suite is a set of **focused integration tests that isolate one interface behavior at a time** — not whether a model can solve a task, but whether it can call helper methods, write executable cells, interpret bounded variable previews, manage state, and return typed values through the harness. It contains **88 test instances across 36 families**, covering:

- typed method calls
- structured returns
- stateful object manipulation
- routing to helper agents
- context and truncation handling
- REPL and code execution
- batching through generated loops
- error recovery
- task decomposition

Most tests are short (one to five turns); the harder cases stress batch bookkeeping, error recovery, multi-step REPL exploration, and writing reusable helper methods. The complete suite ships in the NOOA repository. Each test is run **five times per model**, across **ten models**, for **4,400 records total** (88 tests × 5 runs × 10 models = 440 records per model).

The ten models are grouped by scale:

- **Small/efficient (4):** Claude Haiku 4.5, Gemini 3.5 Flash, Nemotron 3 Nano 30B, GPT-5.4 Mini
- **Large/frontier (6):** Claude Opus 4.8, Gemini 3.1 Pro, GLM-5.2, Kimi K2.6, Nemotron 3 Ultra, GPT-5.5

### Table 1 — Capability-test pass rates

Each model is evaluated on 440 records: 88 tests, five runs each.

| Model | Passed | Pass rate |
|---|---|---|
| Claude Haiku 4.5 | 430/440 | 97.7% |
| Claude Opus 4.8 | 438/440 | 99.5% |
| Gemini 3.5 Flash | 439/440 | 99.8% |
| Gemini 3.1 Pro (preview) | 438/440 | 99.5% |
| GLM-5.2 | 439/440 | 99.8% |
| Kimi K2.6 | 431/440 | 98.0% |
| Nemotron 3 Nano 30B | 403/440 | 91.6% |
| Nemotron 3 Ultra | 434/440 | 98.6% |
| GPT-5.4 Mini | 417/440 | 94.8% |
| GPT-5.5 | 440/440 | 100.0% |
| **Overall** | **4309/4400** | **97.9%** |

**Reading the table:** small/efficient models pass 96.0% of records overall; large/frontier models pass 99.2%. Every model exceeds 91% (the floor is Nemotron 3 Nano 30B at 91.6%), and six of ten models exceed 98% (Claude Opus 4.8, Gemini 3.5 Flash, Gemini 3.1 Pro, GLM-5.2, Nemotron 3 Ultra, GPT-5.5). GPT-5.5 is perfect on the suite (440/440); Gemini 3.5 Flash and GLM-5.2 each miss only a single test (439/440).

**Reasoning-mode ablation:** pass rates discriminated by reasoning on/off show frontier models already saturating regardless of mode — Opus 4.8 at 100.0%/99.5% and GPT-5.5 at 99.5%/98.6% (off/on) — while the benefit of reasoning grows monotonically as model capability falls within the Nemotron 3 family: Ultra improves 93.4% → 94.1%, the mid-size variant (given in the source as "Super-v3") improves 83.7% → 96.4%, and Nano improves 52.5% → 84.8% (reasoning off → on). The paper's reading: inference-time reasoning acts as a **capability equalizer** for the smaller Nemotron models, closing most of the gap to the frontier tier.

**Headline finding:** the interface itself is not a burden for current-generation LLMs. Models know Python; they can read object documentation, call methods with typed arguments, use returned values, mutate object state, and return values that satisfy the type contract. This zero-shot fluency is offered as validation of the framework's empirical agent readiness — expressing agentic constructs as native software abstractions removes the interface friction other frameworks introduce.

## Stress Tests: Where the Interface Frontier Remains

Residual failures concentrate in **six stress families** — the tests that most resemble real agentic work rather than single tool calls: preserving per-item bookkeeping across a large batch, recovering from errors, iterating in a REPL, refining an intermediate answer, and decomposing repeated transformations into helpers.

### Table 2 — Stress-test pass rates

Each row has 50 records (10 models × five runs), split into the four small/efficient and six large/frontier models defined above.

| Stress test | Small/efficient | Large/frontier | Overall |
|---|---|---|---|
| sentiment_batch | 8/20 (40%) | 23/30 (76.7%) | 31/50 (62%) |
| calculate_batch | 14/20 (70%) | 27/30 (90%) | 41/50 (82%) |
| refinement | 11/20 (55%) | 30/30 (100%) | 41/50 (82%) |
| task_decomposition | 15/20 (75%) | 30/30 (100%) | 45/50 (90%) |
| error_recovery | 19/20 (95%) | 29/30 (96.7%) | 48/50 (96%) |
| repl_exploration | 18/20 (90%) | 30/30 (100%) | 48/50 (96%) |
| **Stress aggregate** | **85/120 (70.8%)** | **169/180 (93.9%)** | **254/300 (84.7%)** |

The stress subset passes 254/300 records (84.7%), well below the 97.9% overall capability-suite rate. Large/frontier models pass 169/180 (93.9%); small/efficient models pass 85/120 (70.8%) — the scale gap **widens from 3.2 points overall to 23 points on the stress subset**. `sentiment_batch` is the single hardest stress test at 31/50 overall (62%), and is the subject of the Appendix B case studies below.

**Consistency across the five runs:** running each test five times also measures reliability, not just capability. Across the full suite's 880 (test, model) pairs (88 tests × 10 models), 94% pass all five runs, only three pairs fail all five runs, and the rest are intermittent. The stress subset separates two distinct failure modes by model scale: **large models have zero 0/5 scores on stress tests** — every large-model stress failure is intermittent, i.e. a reliability miss on an already-demonstrated capability. **Small models show both modes on stress tests**: 12.5% of small-model stress pairs score 0/5 (a capability genuinely absent) and 42% are intermittent.

The paper's framing: these are not failures to understand the self-object or to call a method correctly; they are **failures of disciplined multi-step harness use**. Basic interface fluency is already widespread — reliable long-horizon batching, recovery, and decomposition at the code/model interface remain the actual capability frontier. Appendix B walks through four complete runs of the hardest stress test to show exactly what that looks like in practice.

## Appendix B: A Stress Test Up Close

Appendix B reproduces four **complete** transcripts of `sentiment_batch` (31/50 overall, the hardest stress test), reconstructed directly from the run traces — every ellipsis and truncation marker was produced by the harness and actually seen by the model. All four runs received **byte-identical context**.

**The test agent** (developer-written):

```python
class SentimentBatchAgent(Agent):
    """You are an agent that classifies sentiment of multiple texts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method_writing = MethodWriting()

    async def classify(
        self, texts: Annotated[list[str], "The texts to classify"]
    ) -> list[Literal["positive", "negative", "neutral"]]:
        """Classify the sentiment of multiple texts."""
        ...
```

The scorer requires an **exact match** against 50 reference labels. `texts` is a live list of 50 strings, but the rendered preview shows only the type, the true length (`list(len=50, ...)`), and 25 of the 50 items (the first 13 and last 12) — the harness's standard truncation behavior. The full 50-item list is bound to the `texts` variable and is fully accessible to code, even though only a slice of it is visible in the rendered context. Two instructions in the cached strategy prompt matter for what follows:

1. **Fan-out for per-item LLM work:** decorate a standalone async function with `@strategy(PredictStrategy())` and an ellipsis body, then run it over the batch with `asyncio.gather`.
2. **Return computed values by variable:** after computing in code, call `return_result(variable)` **from within** `execute_python()`. Do **not** re-type computed values in a separate `return_result` tool call.

The four runs diverge at the first model-authored cell.

### B.1. Nemotron 3 Ultra — passed

Nemotron 3 Ultra produced the intended solution in a **single model-authored cell**: it defined a subagent helper decorated with `@strategy(PredictStrategy())`, fanned it out over the live `texts` variable with `asyncio.gather`, and called `return_result(results)` **from inside the same cell** that computed the results — never re-entering the results as text. End-to-end latency was 9.6 seconds. This is the textbook combination of the two instructions above: fan-out for the per-item classification, and returning the live variable rather than retyping it.

### B.2. Claude Opus 4.8 — failed

Opus 4.8's **first cell executed the identical correct pattern**: a `classify_sentiment` helper via `@strategy(PredictStrategy())`, fanned out with `asyncio.gather` over `texts`, with results printed alongside their source text for a manual sanity check. All 50 classifications were correct in the execution output.

The failure happened on the **next turn**. Instead of calling `return_result(results)` on the already-computed, already-correct live variable, the model instead **transcribed the printed output by hand** into a literal inside a separate `return_result` tool call — exactly the pattern the strategy prompt explicitly says not to do. In copying 50 printed lines back into a hand-typed list, the model **dropped item 43** ("neutral" for "Typical response time."), producing a 49-item list.

**Verdict: list length mismatch — expected 50, got 49.** The live `results` variable held all 50 correct labels the entire time; the model had a one-line, zero-risk path to a perfect score (`return_result(results)`) and instead reconstructed the answer from memory of the printed text, introducing a transcription error along the way.

### B.3. GPT-5.5 — passed

GPT-5.5 used **no subagents at all** — a fully manual approach. Its first cell deliberately defeated the harness's truncation preview by printing every item with its index (`for i, t in enumerate(texts): print(i, repr(t))`), pulling all 50 texts explicitly into the visible context rather than relying on the 25-item preview.

Its second cell hand-labeled every item, one comment per line keyed to its index and a short justification (e.g. `'positive', # 0 This is the best day ever!` ... `'neutral', # 43 typical response`), building the `labels` list directly in code, then called `return_result(labels)`. Despite this being the least "agentic" of the four approaches — no fan-out, no subagents, essentially manual classification — it passed because the bookkeeping was disciplined: every one of the 50 items was explicitly inspected and accounted for, and the final call returned the live, freshly-built list rather than a retyped copy.

### B.4. GPT-5.4 Mini — failed

GPT-5.4 Mini's only cell wrote a **keyword-rule classifier** — matching hand-picked positive/negative keyword lists against each text and falling back to "neutral" — then iterated it over the full, live `texts` variable in a straightforward `for` loop.

The interface use here was mechanically correct: it iterated the true 50-item variable, not the 25-item preview. But the keyword lists were fitted only to the ~25 texts the model could actually see in the rendered preview, and the resulting rule was then applied **blind** to all 50 texts — including 25 it never inspected. This also directly violates the strategy prompt's explicit instruction for language tasks ("use LLM reasoning... don't keyword-match or regex"), substituting a cheap heuristic for the semantic judgment the task required. The produced labels did not match the reference set.

### B.5. What the Four Runs Show

The paper's synthesis: **sophistication and success are orthogonal**. The most advanced harness use in the set — Opus 4.8's correct subagent fan-out — failed on the cheapest possible discipline: return the variable you already computed; don't retype it. The least agentic approach — GPT-5.5's fully manual, one-by-one labeling — passed precisely because it was careful about bookkeeping (inspecting every item, building the list live, returning the live list).

Both failures (Opus 4.8, GPT-5.4 Mini) **ignored an explicit instruction already present in the cached strategy prompt**, and in both cases a safe, correct path was already available through the interface — Opus had the correct `results` variable sitting right there; GPT-5.4 Mini had `texts` fully accessible for genuine per-item inspection rather than keyword-fitting on a partial preview. Neither model failed to understand what the interface offered; both chose (or defaulted to) a riskier, non-compliant path when a compliant one was directly at hand.

This is presented as the pattern behind the aggregate stress-test numbers in Section 4.1: the remaining failures are **not gaps in interface understanding** but **lapses in disciplined use of it** — and the paper explicitly flags these as exactly the behaviors that trajectory-level reinforcement learning (discussed as future work in the paper's later sections, see [[07-comparison-to-other-frameworks|the harness-comparison discussion]]) could target for improvement.

---

**Covers:** Section 4.1 (Capability Tests), Appendix B (A stress test up close)
