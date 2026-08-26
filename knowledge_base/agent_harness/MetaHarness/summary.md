> [[index|Wiki]] | [[digest|Digest]]

**Paper:** [Meta-Harness: End-to-End Optimization of Model Harnesses (Lee, Nair, Zhang, Lee, Khattab, Finn, 2026)](https://arxiv.org/abs/2603.28052)

# Meta-Harness: End-to-End Optimization of Model Harnesses

## Human Readable TL;DR

A "harness" is all the code wrapped around an LLM — what it remembers, what it retrieves, how it structures its prompts, when it decides it's done. This paper shows harnesses matter as much as the model itself (a 6x performance swing on the same benchmark just from changing the harness), yet people still hand-tune them. The authors build a system, Meta-Harness, that automates this: a coding agent (like Claude Code) is given full read access to every past attempt's code, scores, and detailed execution logs on a hard drive, and is simply told to write a better harness. No fancy search algorithm, no compressed summaries — just "here's everything that happened, go improve it." This beats both hand-engineered harnesses and prior automatic prompt-optimization tools across text classification, math reasoning, and coding-agent benchmarks.

## TL;DR

Meta-Harness is an outer-loop system that treats "harness engineering" as a code-search problem: a coding-agent proposer is given unrestricted filesystem access to the full history of every prior candidate harness's source code, evaluation scores, and raw execution traces (up to 10M tokens of diagnostic material per evaluation — ~1000x more than prior text optimizers), and repeatedly proposes, evaluates, and stores new harnesses. This wins on three domains: text classification (+7.7 pts over ACE, 4x fewer tokens), retrieval-augmented math reasoning (+4.7 pts average across 5 held-out models), and agentic coding (best Claude Haiku 4.5 harness on TerminalBench-2, #2 overall on Opus 4.6). The core claim: what actually helps is not code search per se but *selective access to prior diagnostic experience* — letting the proposer decide what to look at, rather than force-feeding it summaries.

## Problem & Motivation

LLM system quality depends heavily on the harness (the surrounding code deciding what the model sees), yet harness engineering is manual: engineers inspect failures and hand-tune heuristics. Existing automatic "text optimizers" (OPRO, TextGrad, AlphaEvolve, GEPA, Feedback Descent, TTT-Discover) are poorly suited to this because they compress feedback aggressively — conditioning only on the current candidate, on scalar scores, or on short LLM-written summaries. Harnesses act over long horizons: an early design choice (what to store, when to retrieve) can cause a failure many steps later, and compressed feedback strips out exactly the information needed to trace that failure back to its cause.

## Main Original Ideas

- **Full-history filesystem access as the feedback channel**, instead of a compressed per-candidate summary: every evaluated harness contributes a directory of source code, scores, and raw execution traces, and the proposer queries it with ordinary tools (`grep`, `cat`) rather than having it force-fed as a single prompt.
- **A coding agent as the proposer**, not a raw LLM — because the accumulated experience exceeds any context window, so the proposer must actively decide what to inspect and validate its own edits by interacting with the codebase.
- **No parent-selection rule, no mutation operator.** The proposer can inspect any prior harness and its trace and choose anything from a local tweak to a full rewrite; starting from a strong prior harness emerges naturally rather than being hard-coded.
- **Code-space search as implicit regularization**: representing harnesses as programs biases the search toward coherent, reusable algorithms (not brittle overfit heuristics), and aligns with the read-write-execute workflows coding agents are already trained on.

## Key Findings

| Domain | Result | Comparison |
|---|---|---|
| Online text classification (GPT-OSS-120B; LawBench/Symptom2Disease/USPTO) | 48.6% avg accuracy, 11.4K context tokens | +7.7 pts over ACE (40.9%, 50.8K tokens) — ~4.5x fewer tokens |
| Vs. text optimizers (search-set) | 50.0 median / 56.7 best accuracy | Beats OpenEvolve (39.1/43.3), TTT-Discover (34.1/45.6), GEPA (32.6/40.2) using 0.1x the evaluations |
| OOD generalization (9 unseen datasets) | 73.1% avg accuracy | +2.9 pts over ACE (70.2%); wins 6/9 datasets |
| Retrieval-augmented math (200 IMO-level problems, 5 held-out models) | 34.1% → 38.8% avg | +4.7 pts; beats BM25-only retrieval (+3.4) and dense retrieval (+4.0 at k=5, but with per-model regressions) |
| TerminalBench-2, Claude Opus 4.6 | 76.4% pass rate | #2 overall (only ForgeCode's unreproducible 81.8% is higher); beats Terminus-KIRA (74.7%) |
| TerminalBench-2, Claude Haiku 4.5 | 37.6% pass rate | #1 among all Haiku 4.5 agents; +2.1 pts over Goose (35.5%) |
| Proposer-interface ablation | Full traces: 50.0 median vs. scores-only 34.6, scores+summary 34.9 | Raw execution traces are the ingredient that matters — summaries don't recover it |

## Suggestions & Future Directions

- The authors flag co-evolving the harness *and* the model weights together as a natural next step — letting the discovered harness shape what the model learns, and vice versa.
- Only one proposer agent (Claude Code) was studied across all three domains; how the effect varies across different coding-agent proposers remains open.
- Building a small CLI over the growing experience archive (list Pareto frontier, diff two harnesses, show top-k) is suggested as a practical lever once the filesystem history grows large.
- Skill-text quality (what the proposer is told is forbidden / must produce) dominates other knobs like iteration count or population size — the authors recommend a few short debug runs (3-5 iterations) before committing to a full search.

## Authors & Institutions

Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn (2026-03-30). Institutional affiliations are not stated in the extracted text; the author list spans researchers associated with Stanford-affiliated agentic-systems and ML research groups (based on known prior work by Khattab and Finn).

## Figures

![Meta-Harness teaser results](wiki/images/fig1-teaser.png)
*Headline results: Meta-Harness matches the best prior text optimizer's final accuracy in a handful of evaluations, then keeps climbing past it; on TerminalBench-2 its bar is the tallest among Haiku 4.5 harnesses.*

![Meta-Harness search loop](wiki/images/fig2-search-loop.png)
*The core mechanism: a closed propose → evaluate → store loop where every iteration's full code, traces, and scores are written back to a filesystem the next proposer call can selectively query.*
