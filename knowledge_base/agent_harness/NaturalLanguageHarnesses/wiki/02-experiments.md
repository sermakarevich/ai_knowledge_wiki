> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental design and results

**In one sentence:** IHR-executed Natural-Language Agent Harnesses (NLAHs) match native code harnesses on task scores across coding, terminal-use, and computer-use benchmarks while compressing the policy to a few kilobytes of inspectable text, preserving workflow/contract/tool/recovery mechanisms, and enabling module-level ablations — with parent-child handoff loss as the main remaining bottleneck.

## Key points

- RQ1 compares three realizations (native Code harness, Prompted NLAH as plain instructions to Codex CLI, IHR-executed NLAH) and finds IHR-executed NLAHs competitive: Live-SWE 73.0 vs Code 67.0 vs Prompt 77.0; MHTBA/TB2 53.9 vs Code 36.0 vs Prompt 57.3; OSWorld/SeeAct 46.3 vs Code 47.1 vs Prompt 47.9.
- All runs share one IHR instantiation — Codex CLI 0.123.0, model gpt-5.4-mini, reasoning effort xhigh, Ubuntu 24.04 (64 cores, 251 GiB), Docker with per-task caps 32 vCPUs / 84 GiB / 40 GiB — on SWE-bench Verified (resolution rate), Terminal-Bench 2.0 (task success), and OSWorld (task success rate).
- NLAHs expose the policy layer in far fewer static materials: Live-SWE 60.1k code tokens / 68 files → 2.9k-token / 3-file NLAH; MHTBA 10.5k / 3 → 0.8k / 1; SeeAct 47.5k / 5 → 1.4k / 1, separating state, validation, recovery, search, and completion gates from deterministic mechanisms.
- RQ2 mechanism audits show NLAHs materialize intended mechanisms: Artifact Contract 1.000 (SWE) / 0.955 (MHTBA), Tool Call Success 0.933 / 0.928, Failed Tool Continuation ~0.992–0.995, Verification Signals 9.89 (SWE) / 22.82 (MHTBA), plus nontrivial workflow-preservation, stage-coverage, and ordered-workflow scores.
- The main weakness is handoff/orchestration: NLAH Orchestration Reliability 0.83 (SWE) / 0.85 (MHTBA) vs Prompt ~0.99–1.00, and Information Handoff Recall 0.32 (SWE) / 0.55 (MHTBA) vs Prompt 1.00, because parent-child execution distributes work across contexts.
- RQ3 module ablations (added one-by-one to a Basic condition) show state/acceptance discipline helps most — File-backed state 73.0→75.6 (SWE) and 44.4→58.3 (OSWorld), Self-evolution →78.8 / 52.8, Evidence-backed answering +2.8 on both — while Multi-candidate search explodes Agent Calls 1.1→5.7 (SWE) but drops SWE 73.0→71.4, and Context compression hurts OSWorld 44.4→36.1 (−8.3).
- Takeaway: explicit NLAH modules are useful when they shorten the path from intermediate work to auditable evidence and benchmark acceptance, not when they add branching, local process layers, or compressed summaries that drift from the evaluator.

---

## 4 Experimental design

### 4.1 Research questions

- RQ1 (Harness Realization): Can NLAHs shape observable agent behavior while maintaining comparable task outcomes, and how does this control compare with native code harnesses and prompted NLAHs?
- RQ2 (Harness Mechanism Realization): Do IHR-executed NLAHs preserve and materialize intended harness mechanisms, such as workflow structure, contract enforcement, tool use, recovery, and information handoff?
- RQ3 (Module Ablation): Once harness modules are expressed in natural language, can they be cleanly ablated and analyzed at the module level?

### 4.2 Harness realizations

Three realizations of the same harness idea, ordered by directness of execution control:

- **Code Harness:** original code implementation (controller code, workflow scripts, framework defaults, tool adapters). Strongest, most deterministic control, but policy interleaved with implementation details.
- **Prompted NLAH:** same NLAH content given as ordinary prompt/instruction text to the Codex CLI agent, without IHR's shared runtime charter and execution semantics. Tests how much control passive natural-language instructions provide.
- **IHR-executed NLAH:** NLAH interpreted and executed by IHR, with explicit runtime semantics for child lifecycle, artifact/state handling, contract gates, and stopping. Gives up hard determinism of code but gives the natural-language policy an execution substrate that materializes roles, handoffs, state, and verification boundaries.

### 4.3 Benchmarks and harness families

Three benchmark families requiring multi-step control, tool use, durable state, and verification/evidence management:

| Family | Benchmark | Metric | Harness family studied |
|---|---|---|---|
| Coding | SWE-bench Verified (Jimenez et al., 2024; Chowdhury et al., 2024) | issue resolution rate | Live-SWE-Agent (Xia et al., 2025) |
| Terminal-use | Terminal-Bench 2.0 / TB2 (Merrill et al., 2026), long-horizon Linux CLI tasks | task success | MHTBA — SOTA terminal-use code harness from Meta-Harness (Lee et al., 2026) for TB2 with Claude Opus 4.6 (Stanford IRIS Lab, 2026) |
| Computer use | OSWorld (Xie et al., 2024), real desktop environments | task success rate | SeeAct-style GUI harness family (Zheng et al., 2024a) |

### 4.4 Experimental setup

- Same IHR instantiation for all experiments: Codex CLI version 0.123.0, model gpt-5.4-mini (OpenAI, 2026b), reasoning effort xhigh.
- Hosts: Ubuntu 24.04 servers, 64 CPU cores, 251 GiB memory; all runs in Docker containers for reproducibility/sandbox safety.
- Per-task container caps: 32 vCPUs, 84 GiB memory, 40 GiB storage.

## 5 Results

### 5.1 RQ1 — Harness realization

Design: compares native code harness vs same NLAH as ordinary instructions vs same NLAH executed by IHR. Separates (a) whether natural-language harness policy is expressive enough from (b) whether a shared runtime gives stronger execution semantics than prompting alone.

Table 1 — RQ1: NLAH execution preserves competitive task performance while exposing process costs. Perf. = benchmark primary percentage. Code = native code harness, Prompt = NLAH text as ordinary instructions, NLAH = IHR-executed NLAH.

| Benchmark | Harness | Type | Perf. | LLM Calls | Tool Calls | Pr. Tok. | Comp. Tok. | Run time (min) |
|---|---|---|---|---|---|---|---|---|
| SWE Verified | Live-SWE | Code | 67.00 | 23.30 | 17.70 | 283.60k | 3.50k | 28.90 |
| SWE Verified | Live-SWE | Prompt | 77.00 | 36.40 | 48.00 | 2.20M | 27.50k | 5.70 |
| SWE Verified | Live-SWE | NLAH | 73.00 | 41.00 | 63.40 | 2.20M | 32.30k | 6.10 |
| TB2 | MHTBA | Code | 36.00 | 223.20 | 122.90 | 10.40M | 17.50k | 19.50 |
| TB2 | MHTBA | Prompt | 57.30 | 41.50 | 48.00 | 3.10M | 51.80k | 11.10 |
| TB2 | MHTBA | NLAH | 53.90 | 56.40 | 78.00 | 4.20M | 74.80k | 13.50 |
| OSWorld | SeeAct | Code | 47.10 | 23.30 | 47.80 | 1.40M | 8.90k | 9.00 |
| OSWorld | SeeAct | Prompt | 47.90 | 35.30 | 39.20 | 1.10M | 12.30k | 4.90 |
| OSWorld | SeeAct | NLAH | 46.30 | 40.90 | 48.60 | 1.10M | 13.60k | 5.50 |

Findings:

- **IHR-executed NLAHs are operationally viable.** Live-SWE NLAH 73.0 beats native code 67.0, near Prompt 77.0; OSWorld NLAH 46.3 ≈ Code 47.1; MHTBA NLAH 53.9 below Prompt 57.3 but far above native code 36.0 (MHTBA code artifact's TB2 portability analyzed in Appendix C). Supports the central feasibility claim: NLAH + IHR can drive real multi-step behavior.
- **Cost profile = prototype-runtime overhead.** NLAHs often use more model calls, tool calls, or tokens than code harnesses — expected because IHR is built on a general agent substrate with natural-language orchestration rather than a hand-specialized controller. Cost does not destroy performance; added autonomy lets the model choose action granularity more flexibly (e.g., Live-SWE NLAH competitive yet much faster wall-clock than native code: 6.1 vs 28.9 min). Read as engineering target, not representational failure.
- **NLAHs expose the policy layer code hides.** Table 2 conciseness audit is the strongest representation-level result: readable harness policy separated from deterministic mechanisms and directly inspectable (state handling, validation, recovery, candidate search, completion gates), enabling RQ2 auditing and RQ3 ablation.

Table 2 — RQ1: NLAHs expose reusable harness policy in fewer static materials (audited static NLAH files vs code-harness materials; excludes runtime prompts/logs).

| Benchmark | Harness | Tokens Code | Tokens NLAH | Files Code | Files NLAH |
|---|---|---|---|---|---|
| SWE Verified | Live-SWE | 60.10k | 2.90k | 68.00 | 3.00 |
| TB2 | MHTBA | 10.50k | 0.80k | 3.00 | 1.00 |
| OSWorld | SeeAct | 47.50k | 1.40k | 5.00 | 1.00 |

- **Behavior is flexible but policy-guided.** OSWorld shows NLAH as a goal/evidence/gate policy layer: preserves staged observation, action selection, recovery, completion checking, but may pick a different concrete route satisfying the same completion contract (e.g., GUI tasks completed via shell, file edits, or package operations with clearer evidence). Flexible routing is the intended benefit, not loss of control.
- **Takeaway:** harness policy can be externalized into compact natural language and executed by a shared runtime while preserving competitive outcomes; remaining gap is engineering efficiency (handoff loss, fixed context overhead, redundant orchestration calls).

### 5.2 RQ2 — Harness mechanism realization

Question: do IHR-executed NLAHs materialize intended mechanisms, not just match scores? Uses new pattern-preservation and harness-engineering metrics where logs expose event structure. Audit focuses on workflow structure, stage coverage, tool use, contract enforcement, recovery, handoff — since NLAHs operate at policy/contract/gate level.

Table 3 — RQ2: NLAHs preserve recognizable harness-pattern structure. Code row is the reference, so no one-way similarity scores (dashes); Verification Signals reported for all.

| Benchmark | Type | Verification Signals | Prompt Contract | Tool Surface | Workflow Pres. | Stage Cov. | Ordered Workflow | Context Boundary | Model Match |
|---|---|---|---|---|---|---|---|---|---|
| Live-SWE Code | Code | 3.99 | – | – | – | – | – | – | – |
| Live-SWE Prompt | Prompt | 6.51 | 0.89 | 0.82 | 0.70 | 0.75 | 0.74 | 1.00 | 1.00 |
| Live-SWE NLAH | NLAH | 9.89 | 0.81 | 0.87 | 0.67 | 0.82 | 0.78 | 0.76 | 0.76 |
| MHTBA Code | Code | 45.05 | – | – | – | – | – | – | – |
| MHTBA Prompt | Prompt | 13.18 | 1.00 | 0.81 | 0.64 | 0.57 | 0.53 | 1.00 | 0.99 |
| MHTBA NLAH | NLAH | 22.82 | 0.84 | 0.80 | 0.63 | 0.57 | 0.54 | 0.81 | 0.55 |

- NLAH runs keep nontrivial contract/tool/workflow/stage/ordered scores. Live-SWE NLAH raises Verification Signals to 9.89 and beats prompted execution on Stage Coverage and Ordered Workflow. MHTBA NLAH ≈ Prompt on Workflow Preservation, slightly higher Stage Coverage and Ordered Workflow, lower Context Boundary and Model Match because parent-child execution changes topology and splits work across parent/child contexts. Conclusion: policy-guided execution.

Table 4 — RQ2: NLAHs instantiate harness-engineering mechanisms. Prompt uses direct-context variants of Orchestration Reliability / Information Handoff Recall; NLAH uses parent-child handoff variants.

| Benchmark | Type | Artifact Contract | Tool Call Success | Failed Tool Continuation | Cached Token Ratio | Orchestration Reliability | Information Handoff Recall |
|---|---|---|---|---|---|---|---|
| Live-SWE Code | Code | 0.99 | 0.88 | 0.95 | 0.71 | NA | NA |
| Live-SWE Prompt | Prompt | 0.99 | 0.93 | 0.98 | 0.96 | 1.00 | 1.00 |
| Live-SWE NLAH | NLAH | 1.00 | 0.93 | 0.99 | 0.94 | 0.83 | 0.32 |
| MHTBA Code | Code | NA | 0.95 | 0.79 | 0.00 | NA | NA |
| MHTBA Prompt | Prompt | 1.00 | 0.92 | 1.00 | 0.96 | 0.99 | 1.00 |
| MHTBA NLAH | NLAH | 0.96 | 0.93 | 1.00 | 0.94 | 0.85 | 0.55 |

- **Strongest evidence in contracts, tools, recovery:** Live-SWE NLAH 1.000 Artifact Contract, 0.933 Tool Call Success, 0.992 Failed Tool Continuation; MHTBA 0.955 / 0.928 / 0.995. IHR turns text instructions into observable artifacts, tool-mediated execution, recovery.
- **Main weakness = handoff:** NLAH Orchestration Reliability below Prompt on both settings; Handoff Recall drops from Prompt 1.00 to 0.322 (SWE) and 0.553 (MHTBA) under parent-child execution — consistent with RQ1 cost profile. Runtime materializes mechanisms but loses information across boundaries ordinary prompting never creates.
- **Takeaway:** separates mechanism claim from outcome claim — same runs competitive on outcomes and auditable on workflow, contract, verification, tool-use, recovery, handoff; specific gap is handoff and orchestration reliability, not generic overhead.

### 5.3 RQ3 — Module ablation

Table 5 — RQ3: explicit NLAH modules ablated under a shared runtime. Each row adds one module to a benchmark-specific Basic condition. Perf. = main metric; Agent Calls = execution-topology change. Compare within a benchmark column only.

| Setting | SWE Perf. | SWE Agent Calls | OSWorld Perf. | OSWorld Agent Calls |
|---|---|---|---|---|
| Basic | 73.00 | 1.10 | 44.40 | 1.08 |
| + File-backed state | 75.60 (+2.60) | 1.10 (0.00) | 58.30 (+13.90) | 1.11 (+0.03) |
| + Evidence-backed answering | 75.80 (+2.80) | 1.20 (+0.10) | 47.20 (+2.80) | 1.06 (−0.03) |
| + Verifier | 73.20 (+0.20) | 2.30 (+1.20) | 52.80 (+8.40) | 1.42 (+0.33) |
| + Self-evolution | 78.80 (+5.80) | 1.20 (+0.10) | 52.80 (+8.40) | 1.19 (+0.11) |
| + Multi-candidate search | 71.40 (−1.60) | 5.70 (+4.60) | 47.20 (+2.80) | 1.33 (+0.25) |
| + Dynamic orchestration | 74.60 (+1.60) | 1.60 (+0.50) | 47.20 (+2.80) | 1.14 (+0.06) |
| + Context compression | 72.00 (−1.00) | 2.20 (+1.10) | 36.10 (−8.30) | 1.22 (+0.14) |
| + Markdown memory | 70.20 (−2.80) | 1.30 (+0.20) | 50.00 (+5.60) | 1.54 (+0.46) |

Analysis (global; do not average across families; remaining module details in §F.1):

- **Strongest modules tighten state and acceptance discipline:** File-backed state (SWE 73.0→75.6, OSWorld 44.4→58.3); Self-evolution strongest on solve loop (→78.8 / 52.8); Evidence-backed answering consistently positive (+2.8 both). Pattern: preserving state, forcing explicit evidence, sharpening retry decisions cleans the acceptance path.
- **Extra branching ≠ better control:** Multi-candidate search changes topology most (Agent Calls 1.1→5.7 SWE, 1.083→1.333 OSWorld) but yields only +2.8 OSWorld and −1.6 SWE (73.0→71.4). Useful negative result: explicit branching changes search but is too expensive/infrastructure-sensitive under current runtime/budget. More search is not automatically better harness design.
- **Global takeaway:** explicit NLAH modules help when they shorten intermediate-work → auditable-evidence → benchmark-acceptance path; less useful when adding local process layers, extra branching, or compressed summaries whose success notion drifts from the evaluator. This conclusion is hard to reach when harness logic stays buried in code; explicit modules reveal whether and how each helps.

## 6 Related Work (as covered in chunk)

- **Agent harnesses and scaffold-aware evaluation:** performance depends on scaffold (tools, feedback loops, state, validation, workflow structure); code-harness synthesis, scaffold-aware benchmarks, graph compilation, multi-agent routing make this explicit. This work asks whether harness policy itself can be externalized as editable natural language under a shared runtime.
- **Natural-language instruction carriers:** prompts, AGENTS.md, CLAUDE.md, AgentSkills/skill bundles package reusable operational knowledge; skill/memory work learns, evolves, stores, transfers procedures. NLAHs differ: run-level harness-policy layer (roles, call boundaries, state carriers, evidence gates, recovery rules, stopping criteria).
- **Natural language as programs/workflows/constraints:** prompt programming / promptware / LMQL / DSPy / APPL / SGLang treat prompts and LLM calls as programmable; other work compiles NL into workflows, graphs, runtime constraints, executable specs. NLAHs share executable-intent premise but target the full-run agent harness (beyond single call / fixed pipeline / formal graph), keeping freer NL form for editability/expressivity with IHR + deterministic hooks for execution.

## 7 Conclusion (as covered in chunk)

- Studied whether agent harness policy can be externalized as compact, executable, analyzable representation; introduced NLAHs + IHR shared-runtime semantics.
- Across coding, terminal-use, computer-use benchmarks, IHR-executed NLAHs stay competitive with native harnesses while making policy much shorter and inspectable; mechanism audits and module ablations show explicit harness documents support process-level inspection and mechanism-level analysis.
- Acknowledgments: reviewers, plus Ronak Malde and Thomas Wolf for follow-up discussions.

**Covers:** chunk 02
