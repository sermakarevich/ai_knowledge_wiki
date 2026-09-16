# Natural-Language Agent Harnesses

**Paper:** [Natural-Language Agent Harnesses (Pan et al., 2026)](https://arxiv.org/abs/2603.25723)

## Human Readable TL;DR

A talented cook (the AI model) still needs a kitchen rulebook: who chops, who tastes, when a dish counts as done. Today that rulebook is welded into program code, so it is hard to read, move to another kitchen, or test one rule at a time. This paper writes the rulebook as an ordinary document instead — a Natural-Language Agent Harness (NLAH) — and has a shared "kitchen manager" runtime (IHR) read it and run the show: calling agents, handing off work, updating notes, checking results. Across coding, terminal-use, and computer-use benchmarks, the document-run kitchen produces food as good as the code-run kitchen, using a recipe that shrank from tens of thousands of code tokens to a few thousand words of readable text.

## TL;DR

NLAH+IHR externalizes harness policy — decomposition, role contracts, evidence discipline, retry, handoff, validation strategy — into a short natural-language document interpreted by a shared thin runtime (base agent + fixed runtime policy), while deterministic mechanisms (tests, parsers, sandboxing, logging) stay in code. On RQ1, IHR-executed NLAHs are competitive with native code harnesses across SWE-bench Verified/Live-SWE (73.0 vs 67.0), Terminal-Bench 2.0/MHTBA (53.9 vs 36.0), and OSWorld/SeeAct (46.3 vs 47.1), while compressing static policy by roughly 20x (e.g. Live-SWE: 60.1k tokens/68 files → 2.9k tokens/3 files). RQ2 audits show intended mechanisms materialize (Artifact Contract ~1.0, Tool Call Success ~0.93) but parent-child handoff is the main weakness: Information Handoff Recall only 0.32–0.55 vs 1.00 for plain prompting. RQ3 ablations show file-backed state and evidence-backed answering help most, while multi-candidate search (1.1→5.7 agent calls for a score drop) and context compression (−8.3 on OSWorld) hurt.

---

## Problem & Motivation

Modern LM agents are multi-step execution systems, but measured performance depends heavily on the harness — the external execution system deciding inputs, tools, state, validation, recovery, stopping, and call organization.

Native code harnesses bury that policy in tightly coupled controller code mixing prompts, adapters, parsers, retry logic, context policy, and benchmark-specific assumptions. A small change can simultaneously alter call boundaries, tool mediation, state carriers, validation gates, and stopping semantics.

This makes harnesses hard to inspect, port across models, compare, and ablate — even though the harness pattern is often the reusable part. The paper shows the cost concretely: a Claude-tuned terminal harness (MHTBA/Meta-Harness) transplanted to GPT resolves only 32/89 TB2 tasks, mostly stuck in stopping-protocol timeout loops.

The work matters because it changes the unit of analysis from opaque whole systems to a readable, executable, auditable policy document plus a shared runtime.

---

## Main Original Ideas

1. **Natural-Language Agent Harness (NLAH)** — A per-harness natural-language policy document carrying stages, roles, state rules, verification rules, recovery rules, and stopping conditions of a task run. It is the only layer that changes per harness, kept compact (0.8–2.9k tokens) and editable, extending NL carriers like AGENTS.md/CLAUDE.md/SKILL.md from tool descriptions to full-run harness strategy.

2. **Intelligent Harness Runtime (IHR)** — A shared thin runtime (minimal code base agent whose only tool is a terminal + fixed-NL runtime policy) that interprets any NLAH into auditable agent calls, handoffs, state updates, validation gates, and artifact contracts. Even nominally single-agent runs are realized as parent orchestrator plus one executor child to keep the harness/execution boundary visible.

3. **Natural-language / code labor division** — An explicit boundary: natural language carries policy (task decomposition, role contracts, evidence discipline, retry, handoff, validation strategy) while deterministic code carries exact mechanisms (tool execution, parsing, sandboxing, logging, tests, validators). Production guidance: keep safety, permissions, evaluation, and key parsing in code.

4. **Three control regimes framing** — Code harness (hard external control via program logic) vs NLAH+IHR (readable policy executed by a shared runtime via child-agent calls) vs self-harnessing (future: controller model directly harnessing others with no external harness). This clarifies what NLAH+IHR gives up (hard determinism) and gains (inspectability, portability, ablatability).

5. **NLAH writing principles** — Five rules for compact ablatable documents: state the task contract first; separate stages from mechanisms; make state and evidence explicit (path-addressable files, artifact contracts); write module boundaries so they can be ablated (verifier, self-evolution, multi-candidate search, compression, markdown memory); prefer simple enforceable clauses ("write a state file before delegating") over vague exhortations ("be careful").

6. **Mechanism-level evaluation methodology** — Three research questions with dedicated metrics: RQ1 outcome parity (Code vs Prompted NLAH vs IHR-executed NLAH), RQ2 mechanism audits (workflow preservation, stage coverage, artifact contract, tool-call success, orchestration reliability, handoff recall, verification signals), RQ3 module ablations adding one NL module at a time under a shared runtime.

---

## Key Findings

RQ1 — IHR-executed NLAHs preserve competitive performance (Perf. = benchmark primary %):

| Benchmark | Harness | Type | Perf. | LLM Calls | Tool Calls | Run time (min) |
|---|---|---|---|---|---|---|
| SWE Verified | Live-SWE | Code | 67.0 | 23.3 | 17.7 | 28.9 |
| SWE Verified | Live-SWE | Prompt | 77.0 | 36.4 | 48.0 | 5.7 |
| SWE Verified | Live-SWE | NLAH | 73.0 | 41.0 | 63.4 | 6.1 |
| TB2 | MHTBA | Code | 36.0 | 223.2 | 122.9 | 19.5 |
| TB2 | MHTBA | Prompt | 57.3 | 41.5 | 48.0 | 11.1 |
| TB2 | MHTBA | NLAH | 53.9 | 56.4 | 78.0 | 13.5 |
| OSWorld | SeeAct | Code | 47.1 | 23.3 | 47.8 | 9.0 |
| OSWorld | SeeAct | Prompt | 47.9 | 35.3 | 39.2 | 4.9 |
| OSWorld | SeeAct | NLAH | 46.3 | 40.9 | 48.6 | 5.5 |

Static-policy conciseness (audited static files, excludes runtime prompts/logs):

| Benchmark | Harness | Tokens Code | Tokens NLAH | Files Code | Files NLAH |
|---|---|---|---|---|---|
| SWE Verified | Live-SWE | 60.1k | 2.9k | 68 | 3 |
| TB2 | MHTBA | 10.5k | 0.8k | 3 | 1 |
| OSWorld | SeeAct | 47.5k | 1.4k | 5 | 1 |

- IHR-executed NLAHs are operationally viable: Live-SWE NLAH 73.0 beats native code 67.0; OSWorld NLAH 46.3 ≈ Code 47.1; MHTBA NLAH 53.9 far above transplanted code 36.0 (code artifact's TB2 portability failure analyzed in Appendix C).
- Cost profile is prototype-runtime overhead: more model/tool calls and tokens than hand-specialized controllers, but wall-clock can still be faster (Live-SWE NLAH 6.1 vs code 28.9 min); read as engineering target, not representational failure.
- RQ2 strongest evidence in contracts, tools, recovery: Artifact Contract 1.00 (SWE) / 0.96 (MHTBA), Tool Call Success 0.93 / 0.93, Failed Tool Continuation ~0.99–1.00, Verification Signals 9.89 (SWE) / 22.82 (MHTBA) vs code 3.99 / 45.05.
- RQ2 workflow structure preserved: Workflow Preservation ~0.63–0.67, Stage Coverage 0.82 (SWE) / 0.57 (MHTBA), Ordered Workflow 0.78 / 0.54 — policy-guided execution, not random autonomy.
- Main weakness is handoff/orchestration: Orchestration Reliability 0.83 (SWE) / 0.85 (MHTBA) vs Prompt ~0.99–1.00; Information Handoff Recall 0.32 (SWE) / 0.55 (MHTBA) vs Prompt 1.00, because parent-child execution splits work across contexts.
- RQ3 (add one module to Basic; SWE Basic 73.0 / OSWorld Basic 44.4): File-backed state 73.0→75.6 / 44.4→58.3; Self-evolution →78.8 / 52.8; Evidence-backed answering +2.8 on both; Verifier +0.2 / +8.4 — state and acceptance discipline help most.
- RQ3 negative results: Multi-candidate search explodes Agent Calls 1.1→5.7 (SWE) but drops SWE 73.0→71.4; Context compression hurts (72.0 / 36.1, i.e. −1.0 / −8.3); Markdown memory mixed (−2.8 SWE, +5.6 OSWorld).
- Appendix C cautionary tale: MHTBA code artifact under GPT (n=89) — only 32 resolved; 66 end in AgentTimeoutError, of which 21 already have verifier reward 1.0 but fail to stop cleanly. Mechanism: two-call task_complete confirmation loop — GPT answers text-only DONE, gets no-tool warnings and no-op shell commands (e.g. tune-mjcf: reward 1.0 yet timeout after 3600s, 186 episodes, 5.4M tokens).
- Flexible routing is intended: OSWorld NLAH completes GUI tasks via shell/file-edits/package ops with clearer evidence while preserving staged observation, recovery, and completion gates.

---

## Suggestions & Future Directions

1. **Fix parent-child handoff loss** — Information Handoff Recall (0.32–0.55) and Orchestration Reliability (~0.84) are the diagnosed bottleneck; improve task-packet design, STATE_ROOT discipline (TASK.md/NLAH.md/RESPONSE.md, child packets, append-only history), and context semantics (fork_context true/false).
2. **Reduce runtime overhead** — Cut redundant orchestration calls, fixed context overhead, and token costs of the general-agent substrate while preserving outcome parity; treat RQ1 cost deltas as engineering targets.
3. **Keep exact mechanisms in code** — Do not push parsers, sandboxing, permissions, evaluation, or safety into NL; NL imprecision, cross-model interpretation drift, and paraphrase brittleness require code-side precision plus run-time behavior checks.
4. **Build harness representation science** — Once explicit, harnesses become searchable/testable: retrieve, compose, mutate, and optimize NLAH modules under shared runtime assumptions; ask which policy choice causes the win, not just which full system wins.
5. **Harden portability and safety** — Portable harness logic lowers the barrier to spreading risky workflows; deployments need provenance tracking, review, permission control, sandbox isolation, and guards against prompt injection, malicious tool grafting, and supply-chain contamination.
6. **Test self-harnessing and stronger models** — NL remains useful at harness level (task structure, state discipline, acceptance criteria) even as models strengthen and prompt tricks go brittle; explore the no-external-harness controller-model regime and replication via the LinguaClaw package (https://github.com/curated-skills/LinguaClaw).

---

## Authors & Institutions

Linyue Pan, Lexiao Zou, Shuo Guo, Jingchen Ni, Hai-Tao Zheng (corresponding), Shenzhen International Graduate School, Tsinghua University / Harbin Institute of Technology (Shenzhen).
