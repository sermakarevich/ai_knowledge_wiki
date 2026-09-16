> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Intro, preliminaries, NLAH methodology

**In one sentence:** The paper argues that agent harnesses — the external execution systems that strongly shape agent performance but are usually buried in coupled controller code — can be externalized as executable natural-language documents (NLAHs) interpreted by a shared thin runtime (IHR) that preserves task outcomes while making harness policy inspectable, portable, and ablatable.

## Key points

- Agent performance is strongly shaped by the harness (the external execution system around the model), yet harness logic is usually buried in tightly coupled controller code that is hard to inspect, compare, transfer, and ablate.
- The paper proposes Natural-Language Agent Harnesses (NLAHs): editable documents carrying run-level harness policy, plus an Intelligent Harness Runtime (IHR): a shared runtime that interprets NLAHs into agent calls, handoffs, state updates, validation gates, and artifact contracts.
- Three control regimes are contrasted: code harnesses (hard external control via program logic), NLAH+IHR (readable natural-language policy executed by a shared runtime via child-agent calls), and self-harnessing (future design with no external harness, a controller model directly harnessing others).
- Formal preliminaries define model as `y = LM_m(c)` over text/image/video context, agent as a model-centered multi-call execution process with state and tool feedback, agent call as the atomic unit of harness execution, and harness as the external system deciding inputs, tools, state, observations, validation, recovery, stopping, and call organization.
- NLAH+IHR uses four layers: (1) base agent — minimal code LLM loop whose only tool is a terminal (file I/O, processes, event logging, launching child agents as new instances of itself via task packets); (2) runtime policy — fixed instruction turning the base agent into IHR; (3) NLAH — per-harness natural-language policy (stages, roles, state, verification, recovery, stopping); (4) scripts/adapters — deterministic code for tests, parsers, benchmark tools, validators.
- The labor division is explicit: natural language carries policy (decomposition, role contracts, evidence discipline, retry, handoff, validation strategy) while code carries exact mechanisms (tool execution, parsing, sandboxing, logging); even nominally single-agent runs are realized as parent orchestrator plus one executor child to keep the harness/execution boundary visible.
- Five NLAH writing principles are given: state the task contract first; separate stages from mechanisms; make state and evidence explicit; write module boundaries so they can be ablated (verifier, self-evolution, multi-candidate search, context compression, markdown memory); prefer simple enforceable language over vague exhortations like "be careful."
- Three evaluation questions frame the paper: can IHR-executed NLAHs preserve performance vs code/prompted baselines; do they materialize intended mechanisms beyond ordinary prompting; and can explicit modules (file-backed state, verifier separation, self-evolution, multi-candidate search) be analyzed as interventions — with claimed results of comparable outcomes, shorter static policies, and measurable behavioral traces.

---

## 1. Introduction

Modern LM agents are multi-step execution systems: they use tools, keep state, recover from failures, validate intermediate results, and sometimes delegate to other agents (Yao et al., 2023; Shinn et al., 2023; Wang et al., 2024b; Fourney et al., 2024; Anthropic, 2024).

The **harness** — the external execution system around the model — has large effects on measured performance (LangChain, 2026a; LangChain, 2026b; Bui, 2026). Related concerns appear in work on scaffolds, workflow generation, long-context execution, multi-agent orchestration, and tool-using agents (OpenAI, 2026a; Anthropic, 2025a, 2025b; Ding et al., 2026; Liu et al., 2024; Chroma Research, 2025; Sun et al., 2025).

### Three ways to control an agent run (Figure 1)

| Regime | Description |
|---|---|
| Code harness | Restrictive: hard external control on a model through program logic |
| NLAH+IHR (this paper's design point) | Harness policy moved into readable natural language; a shared runtime executes that policy through child-agent calls |
| Self-harnessing | No external harness: a possible future design where a controller model directly harnesses other models |

### The problem: harnesses are not clean research objects

A code harness may mix prompts, tool adapters, parser rules, validation scripts, artifact paths, retry logic, context policy, and benchmark-specific assumptions in one controller bundle. A seemingly small change can simultaneously alter call boundaries, tool mediation, state carriers, validation gates, and stopping semantics — making harnesses hard to inspect, port, compare, and ablate, even though the harness pattern is often the reusable part.

### Proposal: NLAHs + IHR

- **NLAHs** write run-level harness policy as editable text.
- **IHR** is a shared runtime executing this policy through agent calls.
- Key separation: natural language carries harness policy; code/runtime carry exact mechanisms (tool execution, parsing, sandboxing, logging).

### Three evaluation questions

1. Can IHR-executed NLAHs control real runs while preserving task performance comparable to code and prompted realizations?
2. Do IHR-executed NLAHs materialize the intended harness mechanisms beyond using the same text as ordinary prompting?
3. Once policy is explicit, can individual modules (file-backed state, verifier separation, self-evolution, multi-candidate search) be analyzed as module-level interventions?

Claimed result: across coding, terminal-use, and computer-use benchmarks, NLAHs are executable and compact, leave measurable behavioral traces, and module-level gains depend on whether a module aligns intermediate control with the benchmark's acceptance condition.

### Contributions

- NLAHs as explicit natural-language representations of harness patterns, distinct from both runtime policy and deterministic code hooks.
- IHR, a shared in-loop runtime turning NLAHs into auditable agent calls, handoffs, state updates, validation gates, and artifact contracts.
- Exploration of the natural-language/code boundary, broadening natural language from local instructions to harness-level strategy.
- Controlled evidence across three benchmark families: comparable outcomes, concise static policies, module-level analyzability.

Paper: arXiv:2603.25723v2 [cs.CL], 18 May 2026. Authors: Linyue Pan, Lexiao Zou, Shuo Guo, Jingchen Ni, Hai-Tao Zheng (corresponding), Shenzhen International Graduate School, Tsinghua University / Harbin Institute of Technology (Shenzhen).

## 2. Preliminaries

Definitions:

- **Model:** callable learned function from context `c` (text, images, or video) to output `y`: `y = LM_m(c)`.
- **Agent:** system wrapping one or more model calls with external interaction — receives a task, maintains execution state, observes tool/environment feedback, decides whether to continue, ask, validate, or stop. A model-centered execution process that can include multiple model calls and external actions.
- **Single model call** is a degenerate special case of an agent call (one-shot answer, no external action).
- **Atomic unit of harness execution:** the **agent call** — the level where prompts, tools, state, validation, and delegation operate.
- **Harness:** the external execution system around a model in an agent — deciding what the model sees, available tools, state storage, observation return, validation timing, failure recovery, stopping, and organization of model/agent calls.
- **Harness engineering:** designing, implementing, adapting, debugging, and evaluating harnesses.

Eleven aspects of harness engineering (detailed in Section D.1): agent loops; tool design and documentation; context engineering; filesystem and workspace management; memory and state; validation and stopping conditions; safety permissions and sandboxing; runtime defaults; observability and replay; retry and recovery; budget control.

## 3. Methodology

Figure 2 framing: a native code harness mixes policy and mechanism inside controller code; NLAH+IHR separates them — NLAH stores readable policy, IHR provides shared execution semantics, scripts/adapters handle exact operations (tools, tests, parsers, validators). Inspired by reusable natural-language carriers such as AGENTS.md, CLAUDE.md, SKILL.md, extended here from tool/workflow descriptions to harness-level strategies.

### 3.1 NLAHs and IHR — four layers

1. **Base agent:** code-form minimal executable substrate — only an LLM loop whose sole external tool is a terminal. Through it: read/write files, run processes, record events, launch child agents (no separate tool needed — start a new instance of itself and pass a child task packet).
2. **Runtime policy:** fixed instruction turning the base agent into IHR by defining how to interpret and execute harness documents.
3. **NLAH:** the natural-language policy document — stages, roles, state rules, verification rules, recovery rules, stopping conditions of a task run. This is the layer that changes per harness.
4. **Scripts and adapters:** deterministic code for exact operations — running tests, parsing results, calling benchmark tools, checking artifacts.

Design points:

- Base agent + adapters = machine interface; runtime policy = shared execution semantics; NLAH = per-harness policy.
- IHR is intentionally thin (base agent + text-form runtime policy). It acts as orchestrator guided by the runtime policy and delegates substantive task work to child agents.
- Nominally single-agent harness: still realized as parent orchestrator + one executor child, so harness control vs task execution stays visible.
- Multi-role/multi-branch harness: IHR launches separate child agents, passes each only its intended task packet, supervises handoff, records behavior.
- IHR is not a large bespoke per-benchmark controller; it is a shared runtime giving natural-language policy a common execution substrate.
- Example NLAH clauses: when to create a task state file, when to ask a verifier to inspect a patch, what evidence must be preserved before answering, when retry is allowed, what condition closes the run. The runtime instantiates these via model calls, child-agent messages, tool calls, files, deterministic hooks.
- NLAHs extend beyond ordinary prompts: they describe the full lifecycle of a task run and subsequent multi-step execution.

Natural-language/code boundary (Section D.2): deterministic code kept where precision matters (tests, parsers, sandboxing, benchmark adapters, artifact validators — exact, reproducible behavior); natural language used for policy (task decomposition, role contracts, evidence discipline, retry logic, state handoff, validation strategy). This avoids overclaiming NL can replace all controller code while moving the most inspectable part of harness design out of opaque logic.

### 3.2 Notes on writing NLAHs

An NLAH is a compact policy document making harness decisions explicit. Five principles:

1. **State the task contract first.** Define input, expected output, allowed tools/artifacts, completion condition — prevents later vagueness. Coding: patch location, test evidence, final answer format. Computer-use: target application state, allowed interaction channels, completion evidence.
2. **Separate stages from mechanisms.** Name stages (e.g., inspect, plan, edit, verify, recover, finalize) but don't reimplement low-level tool operations in prose; define when mechanisms are used and what evidence they must produce. Low-level ops belong to scripts/adapters/hooks.
3. **Make state and evidence explicit.** Long-horizon agents fail when intermediate info is lost or answers lack auditable evidence. Specify where state is stored, which artifacts later agents must reopen, what evidence supports a claim, which files/logs close the run. Especially important for file-backed state, verifier modules, evidence-backed answering.
4. **Write module boundaries so they can be ablated.** Name modules clearly (verifier, self-evolution, multi-candidate search, context compression, markdown memory) so removal/change doesn't silently alter the rest — enabling questions about effects on outcomes, process metrics, solved-set composition under a shared runtime.
5. **Prefer simple and enforceable language.** Short clauses, concrete conditions, explicit artifacts. Weak: "be careful," "think deeply," "act like an expert" (no observable behavior). Strong: "write a state file before delegating," "run the verifier only after producing a candidate patch," "do not finalize without evidence from the target file" — easier for IHR to execute and researchers to audit.

**Covers:** chunk 01
