# PreAct: Computer-Using Agents that Get Faster on Repeated Tasks

**Paper:** [PreAct: Computer-Using Agents that Get Faster on Repeated Tasks (Bojie Li, 2026)](https://arxiv.org/abs/2606.17929)

## Human Readable TL;DR

Imagine training an AI assistant to book your weekly team meeting. The first time it figures it out step-by-step, which takes a while. PreAct records that solution like a recipe, verifies the recipe actually works, then uses it to repeat the task instantly next time -- no thinking required. If the app changes slightly, it notices and improvises just that part, saving the new improved recipe afterward. The result is an AI that gets faster the more you use it for the same jobs.

## TL;DR

PreAct compiles successful computer-using agent (CUA) execution traces into state-machine programs -- verified before storage -- and replays them on repeated tasks. On cold runs, standard CUAs act; on warm runs, the state machine executes with per-step UI predicate checks and fallback-to-CUA on mismatch. This achieves 8.5--13x wall-clock speedup with near-zero LLM cost per replay, and a verify-before-store gate prevents 1.75--2.6 task regressions from faulty compilations across AndroidWorld, OSWorld, and WebArena.

---

## Problem & Motivation

Computer-using agents re-solve every task from scratch -- spending full LLM inference budget even when the same task has been completed correctly before. This is wasteful for recurring tasks (recurring calendar events, repeated form fills, routine admin actions). Prior record-and-replay approaches store flat action sequences that break on any UI deviation with no recovery path. PreAct addresses this gap: safe, fast replay of previously-seen tasks that degrades gracefully when conditions change.

---

## Main Original Ideas

1. **State-Machine Compilation** -- Execution traces from successful runs are compiled into directed graphs where each node holds UI verification predicates (XPath, resource IDs, text hints against the accessibility tree) and transitions carry executable actions. Parameterized fields (names, phone numbers, form values) are extracted and rebound at runtime, so a single "add contact" program serves all future contact additions.

2. **Verify-Before-Store Gate** -- After compilation, the program is re-executed from a clean environment state and evaluated by the benchmark's own evaluator before entering the corpus. This blocks "lossy compiles" -- programs that replay to 100% action coverage yet leave the task unsolved (e.g., form fields filled but data not committed). Without the gate, lossy programs silently accumulate and degrade warm performance.

3. **Select-Replay-Fallback-Store Loop** -- (1) A selector retrieves the best candidate program from the corpus; (2) the replayer walks the state graph, checking predicates before each action; (3) on predicate mismatch, the live CUA takes over from that screen; (4) new traces compile and gate-verify before corpus entry. This keeps both speed (replay) and robustness (fallback + re-verify).

4. **Dedup-Signature Upsert** -- Programs are keyed by task-description hash and support `Upsert` (replace, not append). New compiles can overwrite stale programs, so the corpus refines over time rather than accumulating duplicates.

---

## Key Findings

| Platform | Gate ON (warm gain) | Gate OFF (warm gain) | Gate gap |
|---|---|---|---|
| AndroidWorld (15 tasks) | +1.2 tasks | -1.4 tasks | **2.6 tasks** |
| OSWorld (6 tasks) | +0.2 tasks | -2.4 tasks | **2.6 tasks** |
| WebArena (12 tasks) | -4.0 tasks | -5.75 tasks | **1.75 tasks** |

- Wall-clock speedup on successful warm replays: **8.5--13x** with ~0 LLM cost
- Compilation overhead: +162% (Android) / +217% (OSWorld) per first run; amortizes on second repetition
- Five reproducible lossy-compile failure modes documented (Table 3): form fill without commit, path navigation without creation, command execution with state mismatch
- Embedding-based selector (MiniLM-L6) matches LLM-based selector at 100% correct-family retrieval -- cheaper option is sufficient
- Prompt engineering, runtime guardrails, and compile-LLM choice are non-factors
- Out-of-distribution generalization: corpus from 6 seen tasks applied to 30 unseen tasks degrades ~11 percentage points below cold baseline -- value is concentrated in repetition, not transfer

---

## Suggestions & Future Directions

1. Scale corpus to 10³--10⁴ programs and benchmark selector discrimination at that scale
2. Direct architectural baseline against flat-script code generation (current Δ=+0.67 is non-significant at p=0.125)
3. Long-horizon tasks (100+ actions) requiring hierarchical goal decomposition
4. Non-idempotent task verification: gate assumes safe re-execution; irreversible actions (send message, charge payment) need alternative verification paths
5. Internalize corpus knowledge into model weights for zero-shot generalization without runtime retrieval

---

## Authors & Institutions

Bojie Li (Pine AI)

## Figures

_(No screenshots captured -- content retrieved via web fetch)_
