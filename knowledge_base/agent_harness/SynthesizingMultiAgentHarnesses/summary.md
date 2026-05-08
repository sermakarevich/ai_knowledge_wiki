# Synthesizing Multi-Agent Harnesses for Vulnerability Discovery

**Paper:** [Synthesizing Multi-Agent Harnesses for Vulnerability Discovery (Liu et al., 2026)](https://arxiv.org/abs/2604.20801)

## Human Readable TL;DR

Imagine you're running a security team where each specialist (analyst, tester, verifier) has to collaborate, but someone wrote the rulebook for how they interact badly — and most teams just write these rulebooks by hand. This paper builds a system (AgentFlow) that automatically writes and improves those rulebooks by watching what went wrong in each attempt: did the tester even reach the right part of the code? Did the verifier correctly identify a real bug? By combining a rich shared language for describing team structure with real feedback from the code itself, AgentFlow discovered 10 new, previously unknown security vulnerabilities in Google Chrome — including two critical ones that could let an attacker take over your computer from a webpage.

## TL;DR

AgentFlow introduces a typed graph DSL that jointly covers all five dimensions of multi-agent harness design (agent roles, prompts, tools, communication topology, coordination protocol), paired with a feedback-driven outer loop that consumes runtime signals from the target program (coverage, sanitizer reports, stdout/stderr) to diagnose failures and guide harness rewriting. Evaluated on TerminalBench-2 with Claude Opus 4.6, it achieves 84.3% (top of the public leaderboard). Applied to Google Chrome using the open-weight Kimi K2.5 model, it discovers ten previously unknown zero-day vulnerabilities, including two Critical sandbox-escape CVEs.

---

## Problem & Motivation

State-of-the-art LLM-based vulnerability finders use multi-agent architectures, where specialized agents (analyst, explorer, verifier) collaborate via a "harness" -- the orchestration program that specifies agent roles, prompts, tool access, communication topology, and retry logic. The harness design dramatically affects success rates (several-fold variance using the same underlying LLM), yet most harnesses are hand-crafted.

Existing automated harness optimizers suffer from two fundamental limitations:
1. **Narrow scope** -- each optimizer searches only a restricted slice of the design space (e.g., prompt-only rewriting, or fixed topology with agent additions)
2. **Coarse feedback** -- reliance on binary pass/fail outcomes provides no diagnostic signal about *why* a trial failed (did the agent fail to reach the vulnerable code path? was the crash a false positive?)

---

## Main Original Ideas

1. **Unified Typed Graph DSL** -- A domain-specific language representing a harness as a program `P = (N, E)` with typed nodes (agent roles or `fanout(n, k)` parallel copies) and typed edges (dataflow `n1 -> n2` or guarded `n1 ->g n2`). The DSL formally covers all five harness dimensions: `H = (A, G, Σ, Φ, Ψ)` -- agent set, communication topology, message schemas, tool allocations, and coordination protocols.

2. **Well-Formedness Type System** -- Linear-time structural checks applied before expensive LLM evaluations: all prompt free variables must resolve to upstream outputs or feedback channels; all declared edges must be consumed; graph must be connected. Rejects ~20% of malformed proposals, acting as a budget guard.

3. **Runtime Diagnostic Feedback Loop** -- Instead of pass/fail, the system reads per-run feedback bundles from the *target program itself*: test verdicts, stdout/stderr, line/branch coverage, and sanitizer reports (ASan/UBSan). A dedicated LLM diagnoser analyzes these bundles and produces structured diagnoses: bottleneck agent, intended vs. actual behavior, and a corrective edit suggestion.

4. **Iterative Propose-Execute-Score-Diagnose Loop** -- Four-phase optimization: (1) an LLM proposer generates a new harness conditioned on the latest diagnosis and historical archive; (2) the harness executes across all tasks with full feedback collection; (3) a domain-specific scorer evaluates aggregate results; (4) the diagnoser synthesizes a structured diagnosis to feed back into the next propose step.

5. **Archive with Compression** -- A fixed-size window of `(harness, feedback bundle, diagnosis)` triples, keeping recent and top-scoring iterations in full detail and compressing older entries, enabling the proposer to learn from historical context without unbounded context growth.

---

## Key Findings

### TerminalBench-2 Results (Claude Opus 4.6)

| System | Type | Pass Rate |
|--------|------|-----------|
| **AgentFlow** | **Synthesized** | **84.3%** |
| ForgeCode | Hand-engineered | 81.4% |
| Meta-Harness | Synthesized (single-agent) | 76.4% |

### Ablation Study (TerminalBench-2)

| Configuration | Pass Rate | Drop vs. Full |
|---------------|-----------|---------------|
| Full AgentFlow | 84.3% | -- |
| No prompt search | 51.8% | -32.5 pp |
| No tool search | 71.9% | -12.4 pp |
| No structural search | 76.4% | -7.9 pp |

- Prompt optimization contributes the largest share of gains; structural and tool edits provide complementary improvements.
- Optimization trajectory went from 35.2% → 84.3% across three phases: infrastructure (tool/protocol fixes via stdout), specialization (sub-agents + retry edges), ensemble (fan-out/merge parallel topology).

### Google Chrome Zero-Days (Kimi K2.5, 7-day campaign, 192 H100 GPUs)

| CVE | Severity | Type | Component |
|-----|----------|------|-----------|
| CVE-2026-5280 | **Critical** | Use-after-free (sandbox escape) | -- |
| CVE-2026-6297 | **Critical** | Use-after-free (sandbox escape) | -- |
| + 8 more | High/Medium | Integer overflow, heap buffer overflow, UAF | WebCodecs, Proxy, Network, Codecs, Rendering, WebRTC, WebGL |

All 10 accepted by Chrome Vulnerability Reward Program. The synthesized Chrome harness used 18 agent roles: 7 subsystem analysts, attack-surface mapper, strategy planner, 192 parallel explorers across 7 subsystems, 4-stage crash-triage pipeline, 2-stage validation pipeline, with 6 feedback loops.

---

## Suggestions & Future Directions

1. Extend to **binary-only targets** where source instrumentation (coverage, sanitizers) is unavailable; develop alternative feedback signals for closed-source software.
2. Reduce **computational cost** -- the Chrome campaign required 192 H100 GPUs for 7 days; more efficient synthesis strategies are needed for broader adoption.
3. Apply the synthesis loop to **other complex software domains** beyond security (e.g., automated theorem proving, long-horizon planning tasks).
4. Explore **multi-objective optimization** (vulnerability severity vs. cost vs. false-positive rate) rather than a single scalar score.
5. Investigate **transfer of synthesized harnesses** across similar targets to reduce per-target synthesis cost.

---

## Authors & Institutions

Hanzhi Liu (UC Santa Barbara), Chaofan Shou (Fuzzland), Xiaonan Liu (Fuzzland), Hongbo Wen (UC Santa Barbara), Yanju Chen (UC San Diego), Ryan Jingyang Fang (World Liberty Financial), Yu Feng (UC Santa Barbara)
