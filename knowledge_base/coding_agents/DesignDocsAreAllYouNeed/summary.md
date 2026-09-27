# Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool

**Paper:** [Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool (Kushnir, Noorbakhsh, Sreedhar, Cheng, Liu, Ranganathan, Alizadeh, Kjolstad, Subramanian, 2026)](https://arxiv.org/abs/2609.05364)

## Human Readable TL;DR

Imagine you maintain a calculator that predicts how fast AI models will run on new chips — but both the models and the chips change every few months, so your calculator's code is always rotting and every fix makes it messier. These authors stopped maintaining the code at all: they keep only a folder of carefully written recipe documents, and whenever something changes they have an AI team rebuild the whole calculator from the recipes from scratch (about 2 hours, about 100 dollars). The recipes work because each one walks through a tiny hand-worked example, like a math teacher showing every step on the board. The rebuilt calculator matches hand-checked reference numbers exactly — suggesting that for fast-moving fields, the documents (not the code) should be the thing you keep.

## TL;DR

The paper presents SMART, a symbolic performance-modeling library for ML systems whose checked-in master contains almost no code: ~50 markdown design docs (~9,000 lines) forming a DAG with machine-discovered edges, from which coding subagents regenerate the full implementation in topological order on every version update (1.5–3 h, ~100 USD via Claude Code). Reliable regeneration rests on two ingredients: (i) a worked-example doc style (step-by-step execution traces with exact intermediate values plus reconciliation anchors enforced as generated tests), and (ii) a minimal recursive `Op` IR with SymPy cost expressions and RRTs, a fast closed-form roll-up for large sweeps, and a slow modulo-scheduling mode for fine-grained studies. Regenerated code reproduces hand-audited references including DeepSeekV3 serving on a TPU pod slice to round-off precision.

---

## Problem & Motivation

ML performance-modeling frameworks live between the two fastest-moving layers of the stack — evolving model architectures above, evolving accelerators/interconnects below — so their abstractions are perpetually invalidated (e.g. "every transformer layer looks the same" is now false under MoE routing, latent attention, heterogeneous prefill/decode). Two failure modes compound the resulting tech debt: (1) incremental generation debt, formalized as Dt+1 = G(St+1, Ct) - G(St+1) (Equation 1) — patching the old implementation instead of rebuilding from the current spec, which humans rarely escape because deleting all their code is psychologically hard; (2) context-window myopia — agents fed fragmented snippets miss global invariants and produce locally plausible, globally sub-optimal code. Meanwhile regenerating an entire library with AI agents has become cheaper than paying down the debt of patching it.

---

## Main Original Ideas

1. **Docs as the durable artifact, code as build product.** Master holds a DAG of self-contained natural-language design docs plus a handful of leaf utilities; every human change is a doc edit (self-documenting by construction); subagents regenerate everything from docs alone, gated by validation (reference-model reconciliation, parameter guards, unit tests) with a repair loop. Recomputing Ct = G(St) from scratch drives Equation (1) debt to zero by construction.
2. **Machine-discovered DAG + orchestrated per-doc subagents.** Read-only agents infer dependency edges between docs; an orchestrator walks the DAG topologically with one coding sub-agent per doc, keeping a central log of interpretation struggles and early-wave bugs that tells humans exactly which docs need prose refinement. Scoping each generation to one doc bounds context windows; complexity-based routing sends hard docs (e.g. core DSL) to larger models and routine docs to cheaper ones.
3. **Worked-example doc doctrine (bottom-up over top-down).** Beyond tests-and-rules "constitutions," every doc centers on executable-in-your-head vignettes with exact intermediate shapes/values/cost expressions (in-context demonstrations per Brown et al. 2020, Dong et al. 2022), and every number-bearing doc ends with a reconciliation anchor — a preset with exactly stated expected outputs enforced by generated tests.
4. **Minimal recursive symbolic IR.** A single `Op` type (loop-nest/subgraph interior nodes; TPU-priced leaves `mxu_op`, `load_tile_to_vmem`, `allgather` carrying SymPy `OpCost` + resource reservation tables), authored via a tracing DSL (`@smart_loop` reduction / `@smart_map_loop` parallel map, all-symbolic dimensions), with distribution as sharding annotations and inferred (not hand-placed) collectives. Algorithm side composes, system side prices — each side's churn touches only its own docs.
5. **Two-mode roll-up + edge-bound symbolics.** Fast mode (trip-count scaling + roofline-style overlap transforms) screens thousands of design points; slow mode (modulo scheduling into RRTs, initiation intervals rolling up recursively) studies the flagged ones. All costs propagate as closed-form SymPy expressions in design-space variables with numeric binding only at the edge — one symbolic build per sweep, and docs can assert exact expected cost expressions.

---

## Key Findings

| Claim | Evidence given |
|---|---|
| Regenerated code matches hand-audited references to round-off precision | Stated for reference models including DeepSeekV3 serving on a TPU pod slice |
| Full clean-slate regeneration is practical and affordable | 1.5–3 h wall-clock, ~100 USD API cost (Claude Code), ~20% of a weekly Claude Max budget |
| System scale at time of writing | ~50 design docs, ~9,000 lines of spec prose; covers TPU topology, collectives, numerics, schedulers, dense/MoE/latent-attention/robotics-VLA model families |
| Flash-attention core fits the IR naturally | Listing 1: one nest serves prefill (Tq = Tkv = T) and flash-decoding (Tq = 1, Tkv = Tctx); score matrix never leaves VMEM |
| Sharding-annotated distribution works for frontier blocks | DeepSeekMoE block needs only explicit dispatch/combine `all_to_all`; all other collectives inferred |

---

## Suggestions & Future Directions

1. **Generalize beyond ML-systems co-design** — the authors explicitly bet the enablers (worked-example docs, machine-discovered DAG, minimal symbolic IR) transfer "wherever specs churn faster than software absorbs them"; testing that bet in another fast-churn domain is the obvious next paper.
2. **Harden the validation story** — round-off agreement is reported on an unspecified number of hand-audited references with one flagship case; a larger reference suite with failure/error-bound reporting would turn an existence proof into a reliability claim.
3. **Close the loop on doc-hardness metrics** — the orchestrator log already ranks docs by agent struggle; publishing that signal (which doc styles fail most, which model sizes suffice per doc type) would make the methodology reproducible rather than anecdotal.
4. **Caveats:** 5-page paper with no ablations (worked examples vs. tests-only docs never compared head-to-head); single-hardware family (TPU) leaves; cost figures tied to one vendor/model tier at one point in time.

---

## Authors & Institutions

Samuel Kushnir (Google DeepMind), Kimia Noorbakhsh (MIT), Kavya Sreedhar, Liqun Cheng, Ming Liu (Google), Parthasarathy Ranganathan (Google), Mohammad Alizadeh (MIT), Fred Kjolstad (Stanford), Suvinay Subramanian (Google DeepMind). arXiv:2609.05364v1 [cs.PL], 4 Sep 2026.
