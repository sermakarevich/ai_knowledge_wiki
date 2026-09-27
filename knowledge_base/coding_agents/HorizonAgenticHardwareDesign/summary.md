# Agentic Hardware Design as Repository-Level Code Evolution

**Paper:** [Agentic Hardware Design as Repository-Level Code Evolution (Yu, Deng, Pinckney, Khailany — NVIDIA Research, 2026)](https://arxiv.org/abs/2606.28279)

## Human Readable TL;DR

Imagine handing a junior engineer a chip design task the way you'd hand a software engineer a GitHub issue: here's the codebase, here's how to test it, don't stop until the tests pass. The engineer edits files, runs the tests, checks in the changes that work, throws away the ones that don't, and repeats — using the project's own version-control history as their notebook. This paper does exactly that with an AI agent and real hardware-description-language (Verilog/RTL) design tasks instead of ordinary software. The agent keeps grinding — editing, simulating, committing, or discarding — inside a private git copy of the project until the chip design passes its checks, with zero human babysitting. The surprising result: given enough attempts, it eventually passes every benchmark task tried, though some of the hardest verification tasks take over 80 rounds and burn tens of millions of tokens to get there.

## TL;DR

The paper introduces HORIZON, a framework that treats RTL hardware design as repository-level code evolution: a Markdown harness is compiled into a "project pack" (agent policy, executable evaluator, acceptance predicate, git/runtime policy), and a hands-free agent loop then edits an isolated git worktree, evaluates each candidate, and commits or rejects it — using native git diffs/commits/notes as the state, trace, and experience buffer instead of an external datastore. Using a fixed GPT-5.3 backbone (no RL training), HORIZON reaches 100% pass rate across ChipBench, RTLLM-2.0, Verilog-Eval, and nine CVDP task categories (RTL completion, spec-to-RTL, modification, reuse, linting/QoR, stimulus/checker/assertion generation, and debugging), with the one apparent miss traced to a benchmark harness defect rather than agent failure. The paper's main empirical contribution is not the 100% number itself but the convergence-cost analysis: hard CVDP categories need up to 82 iterations and consume the overwhelming majority (97.1%) of the 209.9M total tokens, of which ~91% are cache-served, making token efficiency — not final pass rate — the metric the authors argue actually needs improving.

---

## Problem & Motivation

Modern agentic software engineering (e.g., SWE-bench-style agents) treats coding tasks as repository-level problems — an agent gets a full codebase and must navigate dependencies, run tests, and iterate to a patch. RTL/hardware design has not had an equivalent framing: a syntactically valid Verilog module is only a starting point, since correctness depends on cycle-level, bit-accurate behavior (datapath widths, FSM transitions, reset/ready-valid conventions) that must be checked by compiling, simulating, and inspecting waveforms/traces — feedback loops largely absent from single-turn code-generation setups.

Prior repository-scale, evaluator-gated self-evolution work (AlphaEvolve for algorithmic kernels, SATLUTION for full SAT-solver repos, ABCEvo for the ABC logic-synthesis system) established that an LLM + automated evaluator + version control can drive a *software artifact* to converge under a correctness gate. The gap HORIZON targets: none of that prior work touched the *hardware design artifacts themselves* (RTL sources, testbenches, verification harnesses) — only the EDA tooling/software around them. The paper asks directly: "whether hardware design itself can be managed as repository-level code evolution."

---

## Main Original Ideas

1. **Markdown harness → project pack compilation.** A human-authored structured Markdown harness (goal, domain knowledge, evaluator spec, acceptance predicate) is compiled by a bootstrap agent `G_φ` into a formal project pack `p = (π_agent, E_p, A_p, Γ_p, Ω_p)` — the agent policy/prompt contract, an executable evaluator, an acceptance predicate, a version-control/artifact policy, and domain skills/instructions. This separates *what a human specifies* from *what the agent loop executes on*.

2. **Git as the state, isolation, and trace substrate.** Rather than a separate datastore or explicit memory module, HORIZON uses native git operations directly: each accepted attempt is a `git commit` carrying evaluator verdict/reward as attached notes; rejected attempts are logged too. `git diff --cached` exposes proposed changes, `git log` recovers the full trajectory. This makes the repository's own history *the experience buffer* — successful commits are positive repair examples, rejected diffs are negative ones — with no separate logging system needed.

3. **RTL tasks hosted "as-is" as isolated git worktrees.** Each RTL problem (design + testbench + verification artifacts) becomes a self-contained, isolated, evolving git worktree rather than being reformulated into a single-turn code-generation prompt or a software-engineering surrogate task. This lets one protocol cover generation, completion, modification, reuse, linting, testbench/checker/assertion generation, and debugging uniformly.

4. **Semi-Markov formalization purely for trace bookkeeping.** The loop is described with semi-Markov decision process vocabulary — state `s_t = (tree(w_t), p, z_t, ℓ_{≤t}, μ_t)` at each outer checkpoint, and a variable-length "option" `a_t = (Δ_t, u_{t,1:K_t}, ρ_t)` covering the patch, internal tool calls, and final submit/review decision — explicitly *not* as a Markov behavioral or optimization assumption (the underlying policy is a free-form, history-dependent LLM; no RL training occurs). This gives precise, replayable names to trace objects for future offline policy analysis, reward modeling, or curriculum construction.

5. **Session-reuse for token economics.** HORIZON reuses a persistent model session across iterations so the harness, project pack, and stable sources are served from the provider's prompt cache instead of being re-sent every turn; only the current diff, latest evaluator output, and agent response are freshly billed. This is why cumulative token cost stays low even across dozens of repair iterations, and it directly motivates treating token consumption (not just pass rate) as the paper's key efficiency metric.

---

## Key Findings

**Setup:** agent backbone = GPT-5.3 (fixed throughout, no fine-tuning/RL); host = AMD EPYC 9334 32-core, 512GB RAM; evaluators use each suite's native open-source flow, with CID 012–014 requiring a commercial EDA simulator. All results are single-agent, fully hands-free.

### Pass-rate progression (Table 1)

| Suite/category | Focus | EDA | Iter. 0 (%) | Final iter. | HORIZON (%) |
|---|---|---|---|---|---|
| ChipBench | Mixed RTL generation | Open | 20.0 | 5 | **100.0**¹ |
| RTLLM-2.0 | NL-spec to RTL | Open | 78.0 | 2 | **100.0** |
| Verilog-Eval-v2 | HDLBits-style Verilog gen | Open | 86.2 | 2 | **100.0** |
| CVDP CID 002 | RTL code completion | Open | 3.2 | 82 | **100.0** |
| CVDP CID 003 | NL-spec to RTL | Open | 19.2 | 24 | **100.0** |
| CVDP CID 004 | RTL code modification | Open | 10.9 | 36 | **100.0** |
| CVDP CID 005 | Spec-to-RTL module reuse | Open | 9.1 | 14 | **100.0** |
| CVDP CID 007 | Linting / QoR improvement | Open | 0.0 | 24 | **100.0** |
| CVDP CID 012 | Test-plan → stimulus gen | Comm. | 47.8 | 32 | **100.0** |
| CVDP CID 013 | Test-plan → checker gen | Comm. | 3.8 | 19 | **100.0** |
| CVDP CID 014 | Test-plan → assertion gen | Comm. | 79.1 | 1 | **100.0** |
| CVDP CID 016 | Debugging / bug fixing | Open | 25.7 | 13 | **100.0** |
| **Overall** | All evaluated RTL benchmarks | — | 47.8 | — | **100.0** |

¹ One ChipBench task fails under the original harness due to a specification–harness mismatch, not an agent error; counting it as resolved yields 100%. "Iter. 0" is the pass rate after the *first agentic iteration*, not a standalone LLM Pass@1 measurement.

- RTLLM-2.0 and Verilog-Eval saturate to 100% within 2 iterations; ChipBench climbs from 20.0% → 100% over 5 iterations.
- CVDP categories need far more repair budget: CID 014 reaches 100% in 1 iteration, CID 016 in 13, CID 005 in 14, CID 013 in 19, CID 003 in 24, CID 007 in 24, CID 012 in 32, and CID 002 (RTL completion) needs 82 — described as "a convergence problem," not a one-shot modeling failure, since the agent gradually converts many failing completions into passing designs.
- CID 013 (checker generation, commercial sim) has the *lowest* first-iteration pass rate of any category (3.8%) yet converges in a steady, near-linear, plateau-free climb to 100% by iteration 19 — contrasted with CID 002, where a long tail on a few stubborn designs (not a globally slow start) drives the 82-iteration cost.

### Token consumption (Table 2)

- Total tokens through each benchmark's earliest-best iteration: **209.9M**, of which **~91% are cached input tokens** (session-reuse design), which "significantly lowered the API cost."
- The three legacy suites (ChipBench + RTLLM-2.0 + Verilog-Eval-v2) together consume only **6.0M tokens (2.9%)** of the total; the nine CVDP categories consume **203.9M (97.1%)**.
- Heaviest categories: CID 002 — 56.0M tokens (26.7%); CID 003 — 38.0M (18.1%); CID 012 — 32.2M (15.3%); CID 004 — 23.7M (11.3%); CID 007 — 21.6M (10.3%); CID 013 — 14.2M (6.7%, notably efficient despite its very weak 3.8% start).
- **Takeaway the authors emphasize:** benchmark completion should be reported together with token consumption — the final percentage points on the hardest categories absorb a disproportionate share of the budget, so token efficiency (not final pass rate, which now saturates at 100%) is the more meaningful improvement target.

### Coverage behavior on verification-generation tasks (Table 3, Section 4.3)

| Category | Iter. 0 pass | Iter. 0 coverage | Best iter. | Best pass | Best coverage |
|---|---|---|---|---|---|
| CVDP CID 012 (stimulus gen) | 47.8% | 86.5% | 32 | 100.0% | 97.9% |
| CVDP CID 014 (assertion gen) | 79.1% | 98.1% | 1 | 100.0% | 100.0% |

- CID 012 reaches 100% pass at iteration 32 but only 97.9% average coverage — a deliberate consequence of the acceptance gate being the *pass condition*, not a coverage target: the loop halts on each design the moment the harness passes, so coverage is observational, not optimized. The improvement pattern is lifting a low-coverage tail (designs starting near 20–40% coverage) up toward full coverage, rather than nudging already-high-coverage designs further.
- CID 014 starts near 98% coverage and saturates almost immediately (best iteration = 1).

---

## Suggestions & Future Directions

1. **Reward-hacking / over-solving risk is unaddressed.** Because the agent can inspect simulator messages, evaluation logs, and failure traces from each iteration, a passing result may mean "satisfies the visible traces under the exposed evaluator" rather than "satisfies the specification under all reasonable environments" — a risk the authors flag as especially acute when the same harness is used for both repair feedback and final scoring.
2. **Propose a two-level benchmark protocol** (diagnostic feedback during repair, held-out scoring for final grading) modeled directly on SWE-bench's fail-to-pass/pass-to-pass held-out test separation — via hidden randomized tests, independent reference models, formal equivalence checks, or held-out simulator configurations — since current RTL-agent benchmarks (Verilog-Eval, RTLLM, ChipBench, CVDP) have no mechanism to detect over-solving or benchmark-specific adaptation.
3. **Long feedback turnaround is a major open problem for broader chip-design use.** The RTL pass/fail benchmarks studied here evaluate quickly, but real PPA (power/performance/area) optimization loops — synthesis, placement, routing, timing analysis — can take hours to weeks (the cited SATLUTION case needed ~2 hours on ~800 parallel nodes just for one repository-scale evaluation). Naive edit-evaluate-repair loops become too slow at that scale; agents need to reason under delayed, sparse, and expensive feedback.
4. **ΔQoR (quality-of-results) reward left to future work.** The reward vector formalization supports `[Δpass, Δcoverage, ΔQoR, −tokens, −time]` but this paper only populates pass/coverage/token signals — synthesis quality-of-results is explicitly deferred.
5. **Broader agentic-hardware-design scope is a framework goal, not yet validated.** The authors state the same machinery is *intended* to host architecture exploration, microarchitecture design, verification planning, physical-design interaction, EDA-software self-evolution, and methodology/flow exploration — but this paper only empirically exercises the RTL instantiation; the wider claim is explicitly not yet backed by experiments.
6. **Explicit non-claim:** the authors state plainly that 100% benchmark completion does not mean "agentic hardware design is solved" — current RTL benchmarks are "controlled proxies" for a much broader chip-engineering problem that includes incomplete/changing specs, downstream integration, PPA tradeoffs, and validation targets not represented in these suites.

---

## Authors & Institutions

Cunxi Yu (corresponding author, cunxiy@nvidia.com), Chenhui Deng, Nathaniel Pinckney, Brucek Khailany — all NVIDIA Research.
