# Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable

**Paper:** [Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable (Wang, Shi, Li, Li, Yu, Yang, Panaganti, Mi, Zhou, Leoweiliang, 2026)](https://arxiv.org/abs/2607.13285)

## Human Readable TL;DR

Think of a coding agent's "harness" (the scaffolding that lets an AI model call tools, keep track of state, and run multi-step tasks) as a huge, messy control room with wires running everywhere. When you need to change one light switch's behavior, you first have to trace which of hundreds of wires actually control it -- and that hunting-for-wires step is often harder than fixing the switch itself. This paper builds an auto-generated "handbook" for the control room: instead of a wiring diagram organized by physical location (files and folders), it's organized by what each part of the room actually does (behaviors), with links back to the exact wires. An AI agent asked to change something first looks up the relevant chapter, drills down only as deep as it needs, and then edits with much more confidence about having found every relevant wire. Tested on two real coding-agent codebases, this approach helped an AI planner find the right code locations more accurately and write better edit plans, all while reading less text than searching from scratch.

## TL;DR

The paper identifies "behavior localization" -- finding every code location that implements a described behavior -- as a central bottleneck when evolving large, tightly-coupled agent harnesses. It introduces **Harness Handbook**, an automatically-constructed, behavior-centric representation (an L1-L3 document hierarchy plus a cross-stage state-register view) built from a repository via static analysis and LLM-assisted behavioral organization, and **Behavior-Guided Progressive Disclosure (BGPD)**, a coarse-to-fine navigation workflow that turns a natural-language modification request into verified, source-grounded candidate edit sites. Evaluated on two open-source agent harnesses (Terminus-2 and Codex) across 60 modification requests, Handbook-Assisted planning beats a Baseline that explores the repository directly: overall plan-quality win rates rise by 10.0 points (Codex) and 18.9 points (Terminus-2), localization F1 against independent reference plans improves by 5.0-18.8 points, and planner token usage drops by 12.7% and 8.6% respectively -- better plans at lower cost.

---

## Problem & Motivation

Modern agentic systems depend as much on their harness -- the code that constructs prompts, manages state, invokes tools, and coordinates execution -- as on the underlying foundation model. As models, APIs, execution environments, and requirements change, harnesses must be continually modified. Production harnesses are large, tightly coupled, and behaviorally distributed across files, functions, execution stages, and shared state, whereas a modification request describes *what* should change, not *where* it lives. Both human developers and coding agents must first perform **behavior localization** -- identifying every implementation site tied to a requested behavior -- before they can plan a correct edit. Existing repository-understanding tools (code search, summarization, repository memory, long-context editing) organize knowledge around files, functions, and modules; they surface individual pieces of relevant code but never show how those pieces combine to produce a behavior, or whether every affected site has been found. This missing behavior-to-implementation connection is the gap the paper addresses.

---

## Main Original Ideas

1. **Behavior localization as an explicit task.** The paper formally defines behavior localization -- finding all code locations implementing a described behavior -- as the necessary first step before any harness edit can be planned, distinguishing it from generic code search or retrieval.

2. **Harness Handbook.** A behavior-centric representation with an L1-L3 hierarchy (L1: system overview -- architecture, execution model, stages, global data flow; L2: component overview -- responsibilities, inputs/outputs, dependencies, local state per stage; L3: unit deep-dive -- source-grounded implementation entries) plus a complementary state-register view that records state relationships crossing stage boundaries. Two invariants keep it useful: *progressive disclosure* (readers descend to L3 only when needed) and *behavior-implementation alignment* (every active L3 locator must still resolve against the current repository, or it is frozen until refreshed).

3. **Automated three-phase construction pipeline.** (I) *Static Fact Extraction* -- deterministic, LLM-free parsing that extracts functions, external boundaries, source locations, signatures, and call edges into a program graph, keeping only calls that resolve to an internal function or named boundary. (II) *Behavioral Organization* -- an LLM-assisted proposer/reviewer loop maps source units (functions or files) onto an execution-stage skeleton, in one of two leaf modes: **function-as-leaf** (starts from a trusted seed skeleton; assigns functions to one or more stages) or **file-as-leaf** (infers the stage skeleton from summarized file "cards" when no reliable seed exists or scale exceeds budget). (III) *Hierarchical Synthesis and Packaging* -- converts the stage skeleton into the L1-L3 tree and state-register view, with every L3 entry linked to a statically identified, revalidated source location.

4. **Behavior-Guided Progressive Disclosure (BGPD).** A coarse-to-fine localization workflow: it starts at L1/L2 to identify directly relevant execution stages, follows the state-register view to pull in stages coupled only through shared state (catching structurally distant but behaviorally linked code), selects the most relevant L3 entries, expands the candidate set along call relations (function-call graph or file-call graph depending on leaf mode), then resolves every candidate against the *current* repository and keeps only sites still relevant -- producing verified, source-grounded evidence for planning.

5. **Handbook-guided modification with automatic resynchronization.** A four-step loop (Algorithm 1): BGPD localizes behavior → a planner converts evidence into an edit plan and action declarations (modify/add/remove) → a separate executor applies the plan and produces a diff → any non-empty diff triggers `Resync`, which reparses only changed source, re-fingerprints/matches units, and refreshes only the affected handbook entries (or reruns full construction only if the stage skeleton is invalidated). Content that can't be parsed or classified is frozen or logged rather than guessed, keeping the handbook conservative and trustworthy.

---

## Key Findings

Evaluated on **Terminus-2** (function-as-leaf) and **Codex** (file-as-leaf), 30 behavior-driven modification requests each (Query, Cross-file, Search-Hostile types; Easy/Medium/Hard difficulty). Planner: DeepSeek-V4-Pro via a NexAU-based read-only planner; plan quality independently judged by GPT-5.5, Opus 4.8, and DeepSeek-V4-Pro.

**Plan quality and cost (win rate = Handbook-Assisted vs. Baseline, ties within 3 points excluded):**

| Harness | Overall win rate: Baseline → Handbook-Assisted | Planner tokens/request: Baseline → Handbook-Assisted |
|---|---|---|
| Codex | 28.3% → 38.3% (**+10.0**) | 0.102M → 0.089M (**-12.7%**) |
| Terminus-2 | 26.7% → 45.6% (**+18.9**) | 0.058M → 0.053M (**-8.6%**) |

Per-judge win-rate gaps ranged **+10.0 to +26.7** (Codex) and **+13.3 to +26.7** (Terminus-2) -- consistent across all three judges. Per-dimension average gains: Localization +2.2 (Codex) / +12.2 (Terminus-2); Scope Control +1.1 / +6.7; Reasoning +3.3 / +4.5.

**Localization accuracy vs. independent reference plans (Opus 4.8 and GPT-5.5), macro-averaged:**

| Harness | Level | Metric | Opus 4.8 Gap | GPT-5.5 Gap |
|---|---|---|---|---|
| Codex | File | F1 | +15.2 | +5.0 |
| Codex | Symbol | F1 | +18.8 | +7.4 |
| Terminus-2 | File | F1 | +10.6 | +12.8 |
| Terminus-2 | Symbol | F1 | +12.3 | +16.3 |

All 24 Recall/Precision/F1 comparisons across both harnesses, both reference models, and both granularities favor the Handbook-Assisted arm (F1 gains of 5.0-18.8 points), with recall and precision rising together (ruling out "more candidates at the expense of focus"). "Wrong" (share of requests with zero overlap vs. reference) never increases and falls by up to 25.9 points -- fewer complete localization misses. On Terminus-2, the weaker planner with handbook guidance reaches file-level F1 of 84.7%/89.3% and symbol-level F1 of 77.1%/89.3% against the Opus 4.8/GPT-5.5 references respectively, with precision up to 93.3%.

- Gains hold across request types: all six harness-by-type comparisons favor Handbook-Assisted (+16.3 to +33.3 points). Codex improves most on Query requests (+26.7); Terminus-2 improves most on Search-Hostile requests (+33.3).
- Gains hold across difficulty levels: all six harness-by-difficulty comparisons are positive (+3.7 to +33.3 points), though not monotonic with labeled difficulty.
- The largest gains concentrate on changes with scattered implementation sites, rarely executed code paths, and cross-module interactions -- exactly the cases plain repository exploration handles worst.

---

## Suggestions & Future Directions

- The authors position behavior localization as a prerequisite, complementary problem to (not a replacement for) harness-evolution work on adaptive optimization and automated repair -- Harness Handbook supplies the "where" before those methods decide the "how."
- Proposed broader uses beyond modification planning: behavior auditing and regression-impact analysis, since the handbook is a synchronized, behavior-centric view of the whole system.
- Stated next step: apply Harness Handbook to **harness self-evolution** -- using the handbook as shared behavioral memory so an agent can autonomously close the loop of localization, planning, execution, and resynchronization, moving the harness toward self-improvement.
- Implicit limitations/design constraints acknowledged in the method: construction requires either a trustworthy seed skeleton (function-as-leaf) or enough budget for file summarization (file-as-leaf); unparsable or unclassifiable content is deliberately frozen/logged rather than guessed, meaning handbook coverage can lag until content is revisited; resynchronization scope depends on whether the stage skeleton itself remains valid after a diff, otherwise the more costly full reconstruction is required.

---

## Authors & Institutions

Ruhan Wang (Tencent HY LLM Frontier; Indiana University -- work done during an internship at Tencent Seattle), Yucheng Shi (Indiana University -- Lead Project Collaborator), Zongxia Li (Tencent HY LLM Frontier; University of Maryland, College Park), Zhongzhi Li (Tencent HY LLM Frontier; University of Georgia), Yue Yu (Indiana University), Junyao Yang (Tencent HY LLM Frontier; National University of Singapore), Kishan Panaganti (Tencent HY LLM Frontier), Haitao Mi (Tencent HY LLM Frontier), Dongruo Zhou (Indiana University), Leoweiliang (Tencent HY LLM Frontier).
