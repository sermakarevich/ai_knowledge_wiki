# The Harness Effect: How Orchestration Design Sets the Token Economics of Enterprise Agentic AI

**Paper:** [The Harness Effect: How Orchestration Design Sets the Token Economics of Enterprise Agentic AI (Sayed Ali et al., Writer Inc., 2026)](https://arxiv.org/abs/2607.06906)

## Human Readable TL;DR

Imagine two delivery drivers with the same truck and the same packages, but one has a smart route planner and one doesn't -- the one without wastes gas circling the block re-reading the same addresses. This paper shows that the "route planner" for AI agents (called the orchestration layer, or "harness") -- the software that decides what the AI re-reads, what tools it sees, and when it retries -- matters more for cost than which AI brain (model) you plug into it. Swapping only that software layer, while keeping the same six AI models and the same 22 tasks, cut the bill by 41%, cut wait time by 44%, and used 38% fewer tokens (the "words" the AI reads and writes, which is what you pay for) -- all while getting the work done just as well.

## TL;DR

The paper argues that "token maxing" -- rising token consumption per task despite falling per-token prices -- is driven by the orchestration layer ("harness"), not the model. In a controlled swap holding 22 locked enterprise tasks and six foundation models fixed, replacing a conventional production agent loop with the Writer Agent Harness cuts blended cost per task 41% ($0.21 to $0.12), median wall-clock 44% (48s to 27s), and tokens per task 38% (14.2k to 8.8k), with quality at parity (0.78 to 0.81, directional at n=22). Efficiency gains are model-invariant (every model gets 33-61% cheaper); quality gains are capability-dependent and correlate almost perfectly with baseline model strength (r=0.99), a phenomenon the authors call "harness leverage." The paper formalizes token economics at the orchestration layer, defines "token maxing," details six mechanism families behind the effect, and compares six widely used agent systems on the same axes.

---

## Problem & Motivation

Agentic tasks unfold over many model turns (system prompt, tool schemas, retrieval, intermediate reasoning, tool outputs), and naive implementations replay the entire transcript on every turn. Falling per-token prices have masked rather than fixed this: teams treat tokens as nearly free at the margin and scale consumption to match -- a Jevons-paradox dynamic borrowed from 19th-century coal economics. The authors name this trajectory **token maxing**: quality is purchased with monotonically growing token intensity at declining marginal quality per token. Most published efficiency work (prompt compression, budget-constrained reasoning, speculative decoding, model routing/cascades) treats the orchestration layer as given and optimizes inside a single call or across model choice. This paper's premise: the harness -- the software that assembles context, exposes tools, sequences turns, delegates work, and retries -- controls every term of the token bill except the model's own verbosity, so it is also the layer that sets the price of work. No prior work isolates the harness as a variable and prices it directly.

---

## Main Original Ideas

1. **Token economics formalized at the orchestration layer.** Per-task cost is decomposed into harness-controlled terms (system prompt, history replay, tool schemas, retrieval payload, user turn), showing that naive full-history replay grows input tokens *quadratically* in turn count while a harness that compacts history, caches the stable prefix, and offloads bulky outputs converts this to roughly *linear* growth -- with no change to the model at all.

2. **An effective-input-price model under prompt caching.** Because providers bill cache-read tokens at roughly 0.1x list price, the effective input price depends on cache-hit rate `h`, which is purely a function of prompt byte-stability -- entirely an orchestration-layer property, not a model or vendor property.

3. **Definition of token maxing as a measurable trajectory.** A development path exhibits token maxing when token intensity grows while marginal quality per token declines -- individually rational for teams graded on benchmark quality, collectively expensive for whoever pays the token bill.

4. **A controlled harness-swap methodology.** The same 22 locked, capability-audited tasks, the same six foundation models across five vendors and three weight classes, and the same judges/price table are run under two orchestration layers (a frozen conventional production loop vs. the Writer Agent Harness) -- isolating the harness as the only variable.

5. **"Harness leverage."** Efficiency gains from adopting a better harness are model-invariant (every model gets cheaper), but quality gains are capability-dependent and track a model's baseline strength almost linearly (r=0.99) -- stronger models convert orchestration structure into quality, weaker models can be overwhelmed by it (a "capability floor" for advanced features like sub-agent delegation).

6. **Six mechanism families that implement the savings**, mapped onto the cost equations:
   - **Cache-shape discipline** -- a "two-zone prompt": a byte-stable prefix (tool schemas, stable system prompt, append-only transcript) that carries provider cache breakpoints, versus a volatile tail (clock, file listings, plan state) that is rebuilt every turn and never cached. Measured at 99.9% cache-read rate on an identical-prefix call.
   - **Structured, incremental, cache-aware compaction** -- at 80% of context budget, older history folds into a typed checkpoint (durable memory, resumability summary, verbatim requirements, skill references) rather than being destructively truncated; summarization runs on a cheap helper model off the paying loop.
   - **Context offload** -- sub-agents act as "context firewalls" (return capped 8KB summaries, citations on a metadata sidecar); skills use progressive disclosure; bulky tool outputs spill to files instead of inflating context; plan/canvas state is event-sourced and re-rendered compactly each turn.
   - **Zero-token waiting** -- waiting for a human/approval/background job suspends durably at zero token cost and resumes on an event, instead of polling turns; a write-ahead log lets crashed runs resume from durable state instead of re-buying tokens.
   - **Failure-spend governance** -- typed failure classification, discarded (not partial) mid-stream attempts, a circuit breaker on repeated identical failing tool calls, and hard caps on loop iterations (50) and tool parallelism (4).
   - **A model-agnostic floor** -- the model/provider/fallback order is a typed route plan (the loop never branches on model name), with schema hygiene (inlined `$refs`, recovered double-encoded JSON, split overloaded schemas) so weaker models can still use native tool calling reliably.

---

## Key Findings

**Blended results (22 tasks x 6 models, baseline vs. Writer Agent Harness):**

| Dimension | Baseline | Harness | Δ | Reading |
|---|---|---|---|---|
| Quality (task-completion) | 0.78 | 0.81 | +0.03 | wash at n=22 |
| Cost / task | $0.21 | $0.12 | **-41%** | decisive |
| Wall-clock / task (median) | 48s | 27s | **-44%** | decisive |
| Tokens / task | 14.2k | 8.8k | **-38%** | decisive |
| Quality per dollar | 3.71 | 6.75 | **+82%** | derived |
| Completions per Mtok (CPM) | 54.9 | 92.0 | **+68%** | derived |

- **Model invariance:** all six models (Claude Sonnet 4.6, Gemini 3.1, Gemini Flash 3.5, Qwen 3.6, GLM 5.1, Palmyra X6) got cheaper under the harness, with per-model cost reductions ranging from -33% (Gemini 3.1) to -61% (Gemini Flash 3.5). On this workload, adopting the harness on any model saved more (33-61%) than switching from the most to least expensive model under the baseline (36%).
- **Quality is model-dependent at the edges:** of 48 capability x model cells, 30 improve, 11 are flat, 7 regress -- all 7 regressions occur on the three smaller models (Flash 3.5, Qwen 3.6, GLM 5.1), concentrated in orchestration-heavy capabilities (MCP tool use, Playbooks, Presentations).
- **Sub-agent delegation (net-new capability)** clears a usable reliability threshold (0.85-0.86 task-completion) only on the two strongest models (Palmyra X6, Sonnet 4.6); it degrades on Gemini 3.1 (0.70) and is not dependable on the fast tier (0.42-0.45) -- a concrete "capability floor."
- **Fleet-scale economics:** at one million agent tasks/month, the harness is worth $90k/month ($1.08M/year) over the baseline, and the saving is model-portable, volume-linear, and stacks with per-token price declines, routing, and prompt compression rather than substituting for them.
- **Comparison of six widely used agent systems** (Claude Code, Claude Cowork, LangGraph, CrewAI, AutoGen/AG2, Hermes Agent, Writer Harness) on structural cache policy, compaction, firewalled delegation, zero-token waits, and per-task accounting: only the Writer Harness has all five mechanisms plus per-task token/cost accounting; most others leave token economics to the application ("app" in their comparison table) or lack a per-task accounting surface at all.

---

## Suggestions & Future Directions

1. Extend the capability-vs-orchestration-feature "floor" concept: harness capabilities should degrade gracefully by model tier (e.g., scoping down tool catalogs, disabling delegation below the floor) rather than presenting one interface to all models.
2. Route requests by orchestration feature demand, not just prompt difficulty -- e.g., route sub-agent-heavy requests to models above the capability floor regardless of apparent text simplicity.
3. Fix the one identified real regression (multi-step research synthesis quality drop on smaller models) before extending general availability to the open-weight candidates.
4. Treat completions-per-million-tokens (CPM) or quality-per-dollar as a release-gate KPI alongside quality, analogous to performance-per-watt in chip design, to prevent "token maxing" from being invisible to teams graded only on benchmark quality.
5. Acknowledged limitations: n=22 tasks is sufficient for the large, uniform efficiency deltas but insufficient for quality inference (quality claims are directional); the baseline was run once and frozen, so its run-to-run variance is unmeasured; the six-model harness-leverage correlation (r=0.99) is suggestive, not conclusive, and awaits a wider model panel; the cross-harness comparison (Table 1) is based on public documentation and a design-time source study, not head-to-head measurement -- a natural direction for future work (e.g., in the style of Harness-Bench).
6. The authors disclose employment at Writer, Inc. (developer of the harness and Palmyra models evaluated), with the evaluation design (frozen baseline, locked prompts, identical judges/price tables, non-excluded candidate-model failures) intended to make the comparison auditable.

---

## Authors & Institutions

Muayad Sayed Ali, Aliaksandra Novik, Anji Boddupally, Artem Yavorskyi, Chris Nickerson, Daniel Rica, Emily DuGranrut, Felix Leung, Garrett Prince, Grace Barnett, Heath Robinson, Hosain Al Ahmad, Jesse Resnick, Juan Carlos Farah, Jyothi Swaroop Meruga, Leonid Kuznetsov, Brock Perry, Luke Gorham, Marie Schmoll, Michael Paciullo, Saumya Das, Sharath Sheripally, Tommy Griscom, Mykyta Osadchyi, Neha Mantri, Nick Westrum, Olivia Benowitz, Parikshith Kulkarni, Radik Chernyshov, Rakshith Vasudev, Rohith Nadimpally, Vikas Gangadevi, Waseem AlShikh -- all Writer, Inc.
