> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendices and limits

**In one sentence:** The appendices frame natural-language harnesses as an explicit run-level policy layer over a shared code runtime, document reproducibility via LinguaClaw, show that the Claude-optimized MHTBA code artifact fails to port to GPT (32/89, mostly timeout/stopping-protocol failures), and formalize the NL/code boundary, runtime policy, reusable NLAH modules, and limitations.

## Key points

- NLAHs are a policy layer, not a code replacement: natural language carries roles, contracts, evidence, retry/validation, state handoff and stopping rules, while code keeps parsers, tool execution, sandboxing, adapters, logging, and deterministic validators.
- Replication package is open-sourced at https://github.com/curated-skills/LinguaClaw (Appendix B).
- MHTBA code-artifact portability test on Terminal-Bench 2.0 under GPT (gpt-5.4-mini, reasoning effort xhigh, 1 attempt, n=89): only 32/89 resolved; 66/89 end in AgentTimeoutError, of which 21 already have verifier reward 1.0 but fail to stop cleanly, and 45 are failed timeouts.
- The portability failure is a runtime-protocol symptom: the code artifact requires a two-call task_complete confirmation, GPT answers with text-only DONE plus no tool call, triggering no-tool warnings and no-op shell commands in a loop (e.g. tune-mjcf: reward 1.0 yet AgentTimeoutError after 3600s, 186 episodes, 5.4M input tokens); Prompt/NLAH keep the same terminal-harness ideas but exit via the Codex task-complete event and artifact /sa-output/artifacts/solve.sh.
- Disagreement slices show extreme cost when code fails but NL succeeds: e.g. Code-fail/Prompt-success (N=26) averages 316.5 episodes, 16.3M input tokens, 146.9 no-tool warnings; all-three-success (N=23) averages only 174.3 episodes, 5.2M tokens, 79.1 warnings.
- Formal boundary (Tables 8–10): base runtime code owns execution substrate, fixed-NL runtime policy (IHR) owns interpretation semantics, replaceable-NL NLAH owns task-family roles/stages/validation/recovery/state/delegation, code hooks own exact tests/validators/parsers; production must keep safety, permissions, evaluation, and parsing in code.
- Module ablations (RQ3): Verifier helps only near the benchmark gate (+0.2 SWE, +8.4 OSWorld); file-backed state is positive on both benchmarks while context compression hurts (SWE 73.0→72.0, OSWorld 44.4→36.1) and Markdown memory is mixed (−2.8 SWE, +5.6 OSWorld).

---

## References cited

Chunk 03 is dominated by the bibliography; cited sections in parentheses:

- AGENTS.md (2026), AgentSkills (2026) — community skill specs; cited by §6.
- Anthropic (2024) Building effective agents; Anthropic (2025a) Effective harnesses for long-running agents; Anthropic (2025b) multi-agent research system; LangChain (2026a) Improving deep agents with harness engineering; LangChain (2026b) The anatomy of an agent harness; OpenAI (2026a) Harness engineering: leveraging Codex; Bui (2026) AI coding agents for the terminal — all cited by §1.
- Foundational agent patterns: Yao et al. (2023) ReAct; Shinn et al. (2023) Reflexion; Wang et al. (2024b) Executable code actions — cited by §1 and/or §6.
- Long-context motivation: Liu et al. (2024) Lost in the middle; Chroma Research (2025) Context rot; Sun et al. (2025) context-folding; Ding et al. (2026) OctoBench — cited by §1 and/or §6.
- Benchmarks: Jimenez et al. (2024) SWE-bench and Chowdhury et al. (2024) SWE-bench Verified (§4.3); Merrill et al. (2026) Terminal-Bench (§4.3); Stanford IRIS Lab (2026) Meta-Harness TB2 artifact reporting 76.4% Terminal-Bench 2.0 with Claude Opus 4.6 (§4.3); Zheng et al. (2024a) grounding, Xie et al. (2024) OSWorld, Xia et al. (2025) Live-SWE-agent, Lee et al. (2026) Meta-harness (§4.3).
- Model setting: OpenAI (2026b) GPT-5.4 mini and nano (§4.4).
- Prompt-brittleness caveat: Wang et al. (2024a) on prompt engineering in SE and Cao et al. (2024) on worst-prompt performance (Appendix A).
- Related harness/skill/program work (§6): DSPy (Khattab et al. 2024), APPL (Dong et al. 2025), Prompting is Programming (Beurer-Kellner et al. 2023), SGLang (Zheng et al. 2024b), AgentSpec, MermaidFlow, FlowAgent, AutoFlow, AnyMAC, AgentDropout, MasRouter, MAS-orchestra, Magentic-one, AgentSpawn, ReCreate, OS-symphony, SkillCraft, SkillsBench, ecosystem-scale skills (Li et al. 2026a), single-vs-multi-agent skills (Li 2026), SkillRL, ProcMEM, MemSkill, meta context engineering (Ye et al. 2026), AutoHarness, Agint, ContextCov, sharing state between prompts and programs (Cheng et al. 2025), prompts-are-programs study (Liang et al. 2025), Promptware engineering, RAG (Lewis et al. 2021), math competition bench (An et al. 2025), MathSmith, 3ViewSense, S1 test-time scaling, plus repos OpenClaw/Lobster, OpenProse, PinchBench.

## Appendix A — Discussion: NLAHs as a policy layer

- Division of labor: natural language is suited for harness policy (roles, contracts, evidence requirements, retry rules, validation strategy, state handoff, stopping conditions); code remains right for exact mechanisms (parsers, tool execution, sandboxing, benchmark adapters, logging, deterministic validators).
- NLAHs make the policy layer explicit while IHR (shared runtime) and deterministic hooks preserve executable precision — narrower and more defensible than claiming NL should replace controller code.
- Explicit policy matters because hidden controller logic lets researchers compare whole systems but not the policy choices inside; NLAHs change the unit of analysis so a harness can be read as text, executed under a shared runtime, audited via mechanism metrics, and modified module by module (e.g. what a verifier contributes, whether file-backed state matters, whether branching pays, whether compression loses critical info).
- NL remains useful at harness level even as models strengthen: some prompt-level gains diminish and prompt tricks are brittle [Wang et al., 2024a; Cao et al., 2024], but run-level policy (what evidence to preserve, when to delegate, how to verify, when to stop) still matters because stronger models still need task structure, state discipline, and acceptance criteria.
- Toward harness representation science: once explicit, harnesses become searchable/testable — retrieve, compose, mutate, optimize NLAH modules under shared runtime assumptions, shifting from opaque harness engineering to asking which policy choices cause the win, not just which full system wins.

## Appendix B — Reproducibility

- Replication package including source code: https://github.com/curated-skills/LinguaClaw.

## Appendix C — MHTBA code-artifact portability on TB2

- Setup: MHTBA code baseline is the released Meta-Harness TB2 artifact, natively reported under anthropic/claude-opus-4-6 with --n-attempts 5; the controlled RQ1 run transplants the same artifact to the paper's common GPT setting (gpt-5.4-mini, reasoning effort xhigh, one attempt) to test cross-model portability rather than remeasuring the native environment.

### Table 6: Timeout diagnostics (n=89)

| Outcome group | Count | Share | Interpretation |
|---|---|---|---|
| Resolved without timeout | 11 | 12.4% | Solved and stopped normally |
| Resolved with timeout | 21 | 23.6% | Verifier reward already 1.0, but agent loop did not terminate cleanly |
| Failed without timeout | 12 | 13.5% | Failed for reasons other than global agent timeout |
| Failed with timeout | 45 | 50.6% | Dominant failure mode: timeout after long control loop |

- Out of 89 samples, 66 end with AgentTimeoutError; 21 timeout runs already have reward 1.0 (valid task state, failed stop); the 45 failed timeouts are the main source of the 32/89 code score.

### Table 7: Trajectory diagnostics for cross-condition disagreements

| Slice | N | Timeouts | Mean episodes | Mean input tokens | Mean no-tool warnings |
|---|---|---|---|---|---|
| Code fail, Prompt success | 26 | 25 | 316.5 | 16.3M | 146.9 |
| Code fail, NLAH success | 24 | 22 | 285.2 | 14.7M | 124.3 |
| Code fail, both Prompt and NLAH success | 19 | 19 | 318.3 | 15.4M | 146.4 |
| All three settings success | 23 | 16 | 174.3 | 5.2M | 79.1 |

- Pattern: where GPT-based NL realizations succeed but the code artifact fails, the code run spends hundreds of episodes, tens of millions of prompt tokens, and accumulates many no-tool warnings — a runtime-protocol symptom, with task-domain difficulty explaining only part.
- Mechanism: the code completion gate treats task_complete as pending-completion and asks the model to call the completion tool again after a checklist; if the next response lacks that tool call, pending state is cleared and the loop continues. Under GPT, trajectories answer with text like DONE and `Tool Calls: []`, get a no-tool warning, issue a harmless no-op shell command, and re-enter the gate until global timeout.
- Example tune-mjcf: verifier reward 1.0 yet AgentTimeoutError after 3600 seconds, 186 episodes, 5.4M input tokens, alternating task_complete call → text-only DONE → no-tool warning → no-op shell command.
- Interpretation: model-harness adaptation failure — the released artifact was optimized for Claude Opus 4.6 (including Anthropic-specific prompt caching) and its completion/tool-call/stopping assumptions transfer poorly to GPT. Prompt and NLAH preserve high-level terminal-harness ideas (environment bootstrapping, batched shell work, programmatic checking, final review) but avoid the brittle state machine via the Codex execution substrate and reproducible artifacts such as /sa-output/artifacts/solve.sh, ending with the Codex task-complete event and no warning cycle.
- General risk: a code harness discovered for one model can encode latent assumptions about tool-calling and stopping that are more fragile than the NL harness policy it implements.

## Appendix D — Formalization and definitions

### D.1 Harness-engineering aspects (Table 8)

| Aspect | Core question |
|---|---|
| Agent loop | How does the agent observe, plan, act, validate, update state, retry, and stop over a long run? |
| Tool design and documentation | Which tools are exposed, how are schemas/descriptions written, how are errors returned? |
| Context engineering | What should each call see, what loads just in time, when to compress/refresh? |
| Filesystem and workspace | Where do inputs, intermediate/scratch files, and final artifacts live? |
| Memory and state | What persists across steps/retries/compression/future runs, and what is the authoritative carrier? |
| Validation and stopping | What evidence is required before success, failure, retry, or budget exhaustion? |
| Safety, permissions, sandboxing | What actions, files, network, commands, credentials are allowed/blocked? |
| Runtime defaults | What default limits, timeouts, context policies, model settings, execution modes shape behavior? |
| Observability, logging, replay | What trace, provenance, artifacts, metrics are recorded for audit/replay? |
| Retry and recovery | How are failures classified, state restored, what changes next attempt? |
| Budget control | How are token, time, tool-call, candidate, retry, monetary budgets enforced/reported? |

### D.2 NLAH expressivity boundary and code-harness mapping (Tables 9–10)

| Layer | Owner | Responsibility |
|---|---|---|
| Base runtime code | Code | Model APIs, LiteLLM routing, tool schemas, bash execution, timeouts, event streams, message history, context-token estimation, run state; plus anything needing precision, reproducibility, safety, speed, or external systems (tool calls, file execution, sandboxing, parsers, evaluators) |
| Runtime policy / charter | Fixed NL | IHR interpretation semantics: parent-child boundaries, meaning of an agent call, artifact and STATE_ROOT semantics, completion gates, audit requirements; e.g. parent orchestrator does no substantive task work while executor children do the task |
| NLAH | Replaceable NL | Concrete harness roles, stages, loops, validation/recovery/state/delegation policy, module composition; roles, stages, strategies, when to validate, how to recover, sufficient evidence, ablatable modules |
| Scripts / adapters | Code hook | Tests, validators, parsers, benchmark wrappers, artifact post-processing, exact execution; task-family-specific precise ops executed by agents from filesystem via bash |
| Model internals | Not NLAH | Constrained decoding, logit bias, sampling, internal reasoning unless exposed as code-level hooks |

- Production guidance: NLAH offers fast iteration, auditing, portability, module-level experimentation; weaknesses are interpretation uncertainty, model dependence, cost, safety/permission risk — so keep safety, permissions, evaluation, and key parsing in code.
- Table 10 mapping rule: shared-by-all or machine-execution decisions → base code/runtime policy; task-family-specific readable/editable/ablatable decisions → NLAH; exactness-dependent decisions → scripts/adapters. Key examples: agent loop = minimal model-tool loop + child primitive (code) / parent role, child boundary, stop discipline (policy) / task-family stages, branching, roles (NLAH) / fixed-protocol loop drivers (scripts); validation = run commands (code) / contract-first completion (policy) / acceptance gates, verifier roles, evidence (NLAH) / tests, graders (scripts); similarly for tools, context, filesystem, memory, safety, defaults, observability, retry, budget (see chunk lines 580–634).

## Appendix E — Runtime and implementation details

### E.1 Runtime-policy prompt (five enforced ideas)

- Runtime-only parent role: top-level agent is orchestrator, so even a nominally single-agent harness runs as "parent runtime + one task child"; substantive workspace work stays in children, delegation boundaries stay inspectable.
- Minimal delegated baseline: if no/incomplete NLAH, runtime first builds the thinnest runnable baseline from the benchmark contract, then treats NLAH clauses as overlays — this grounds task instructions in a runnable delegated substrate (vs. prompted NLAH).
- Call-graph recovery with explicit context semantics: reconstruct roles, stages, repetition, independence from NLAH text and realize as child launches; fork_context=true = child forks and inherits parent conversational context; fork_context=false = child starts fresh with only the explicitly handed minimal task packet; disposable one-shot and fresh children for independent branches preserve model-call boundaries instead of collapsing into one long dialogue.
- Separated runtime state and final artifacts: durable intermediate state under STATE_ROOT (default /sa-output/runtime) only when needed for reuse/audit; judgeable deliverables to /sa-output/artifacts; stable evidence surfaces without mirroring the workspace.
- Contract-first completion and auditability: benchmark outputs and completion gates are primary, but staged/multi-role claims must leave inspectable evidence — IHR-executed NLAH adds orchestration, context, artifact, and reporting discipline with prompt text as one input.

### E.2 Realizing harness aspects with IHR

- Atomic unit is the agent call; a model call is a degenerate agent call (answer once, no external action) — matching the level of prompts, tools, workflow, memory, retrieval, compression, validation, delegation.
- Prompt design: per-agent initial context; role-specific system prompts can live in separate files that IHR instructs each agent instance to load — precise yet editable NL.
- Tool design: code-backed tools (programs, wrappers, scripts, services, adapters) invoked by agents via terminal under sandbox/permission/budget constraints; NLAH carries tool policy and use-discipline, scripts carry exact behavior.
- Workflow/multi-agent: IHR launches agents, messages running agents, inspects returned state, routes outputs, launches more agents, closes completed roles — materializing call boundaries, handoffs, verification/selector stages, multi-agent execution from NL policy.
- Memory/retrieval: external path-addressable state; NLAH names which facts/decisions/failures/validations/artifacts go to memory files, histories, manifests, evidence records; later agents must reopen them by path; retrieval sources, timing, evidence rules in NLAH, search scripts/indexes via terminal, evidence written to auditable artifacts.
- Compression: contract-preserving operation; NLAH states when allowed, what must be externalized first, required fields of the compact state (goal, constraints, explored paths, failure signals, validation status, key evidence, artifact paths, next actions), what stays recoverable; on long context or stage boundary, agent writes the compact state file, later agents reopen it plus referenced artifacts; FILTER drops redundant dialogue/stale speculation/low-value logs but never acceptance criteria, error signatures, replay-needed commands, or handoff state; CHECK reloads and confirms next action/evidence recoverable before continuing.

## Appendix F — NLAH modules (paraphrastic summaries for RQ3)

- ROOT: choose STATE_ROOT under /sa-output, separate from task workspace; maintain STATE_ROOT/RESPONSE.md as stable runtime status file.
- HANDOFF: nothing (prompt, role instruction, reply, promoted artifact) counts as transferred until it exists as TASK.md, NLAH.md, RESPONSE.md, or another named file under STATE_ROOT.
- CHILD PACKET: each child gets children/<id>/TASK.md, optional children/<id>/NLAH.md, and writes back children/<id>/RESPONSE.md.
- BOOKKEEPING: append-only launch/promotion history in state/task_history.jsonl, index promoted outputs in artifacts/manifest.json, reopen files by path for reuse/recovery.
- ARTIFACT: before any final answer/patch/solved claim, write one standalone evidence document as the designated evidence artifact for the task/stage.
- STRUCTURE: cover problem statement, materials, symptoms, root cause, candidate resolution, validation, residual uncertainty.
- CLAIM DISCIPLINE: each major claim states provenance (direct observation vs inference) plus minimal supporting span/output segment when available.
- GATE: do not release a complete answer while release-critical claims remain uncited, contradicted, or materially incomplete in the evidence document.
- ROLE (Verifier): inspect one candidate against original problem plus lightest sufficient materials; break into checkable subclaims; audit completeness, factual and logical correctness; run at least one central independent check when feasible.
- PROCEDURE/OUTPUT (Verifier): return exactly one primary verdict label plus a report explaining the verdict, naming checks run/blocked, without repairing the candidate.
- LOOP: explicit retry loop with real baseline attempt first, default cap five attempts; after non-successful/partial/unstable/stalled attempt, reflect on concrete failure signals; redesign along prompt/tool/workflow evolution with attempt 2 materially reflecting attempt-1 reflection; continue to judged success or cap, reporting incomplete rather than pretending the last attempt passed.
- BUDGET: explicit candidate budget K (default K=5), restore lost budget if a branch crashes before returning comparable evidence; DIVERSITY across hypothesis/decomposition/evidence-route/tool-plan/risk; SELECTION prunes duplicates/unsupported/dominated/risky then compares on fit, evidence quality, coherence, repair cost; ESCALATION expands/redesigns search rather than forcing a fragile winner.
- AUTONOMY: beyond mandatory task-owning child, add subagents only when delegation improves coverage/latency/specialist focus/QC; smallest adequate topology; classify task shape, non-overlapping responsibilities and success conditions, parallelize only truly independent branches; parent narrates launches/waits/comparisons/integration while children do substantive work; workspace familiarization/probing belongs to children after delegation commitment.
- COMPRESSION TRIGGER/SUMMARY/FILTER/CHECK: compress only after writing/reopening path-addressable state preserving contract, artifacts, failures, next actions; preserve goal, constraints, explored/rejected paths, validation status, risks, exact artifact paths; drop redundancy but never acceptance criteria, error signatures, replay commands, handoff state; reload and confirm recoverability before continuing.
- MEMORY CARRIER/UPDATE/READ/HYGIENE: Markdown memory file with stable headings (facts, decisions, observations, environment, caveats); concise entries after discoveries/validations/failures/decisions, mark superseded entries; reopen before planning/delegation/verification/reporting; source-grounded, task-scoped, not a transcript or speculation dump.

### F.1 Additional RQ3 module observations

- Validation helps only close to the benchmark gate: Verifier positive on both benchmarks but uneven (+0.2 SWE, +8.4 OSWorld); dynamic orchestration is real but modest — recovers some cases without tightening the final acceptance path.
- Durable state beats aggressive compression: compression hurts both (SWE 73.0→72.0, OSWorld 44.4→36.1); Markdown memory mixed (−2.8 SWE, +5.6 OSWorld); file-backed state positive in both — path-addressable durable state preserves action-critical details better than summarization or free-form notes.

## Appendix G — Limitations, risks, broader impact

- Limitation: natural-language imprecision — editable NL policies may be under-specified, interpreted differently across models, or weakened by paraphrase; mitigation is keeping exact mechanisms in code and checking executed behavior through runs, never inferring from text alone.
- Broader impact/risks: externalized modules can cut development cost, improve comparability, encourage reuse of robust workflows; but portable harness logic/scripts may lower the barrier to spreading risky workflows and open attack surfaces (prompt injection, malicious tool grafting, supply-chain contamination) via tool use, artifact handling, and delegation — deployments need provenance tracking, review, permission control, and sandbox isolation.

**Covers:** chunk 03
