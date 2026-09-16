> [[index|Wiki]] | [[summary|Summary]]

# NaturalLanguageHarnesses — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-intro-method|Intro, preliminaries, NLAH methodology]]

**In one sentence:** The paper argues that agent harnesses — the external execution systems that strongly shape agent performance but are usually buried in coupled controller code — can be externalized as executable natural-language documents (NLAHs) interpreted by a shared thin runtime (IHR) that preserves task outcomes while making harness policy inspectable, portable, and ablatable.

- Agent performance is strongly shaped by the harness (the external execution system around the model), yet harness logic is usually buried in tightly coupled controller code that is hard to inspect, compare, transfer, and ablate.
- The paper proposes Natural-Language Agent Harnesses (NLAHs): editable documents carrying run-level harness policy, plus an Intelligent Harness Runtime (IHR): a shared runtime that interprets NLAHs into agent calls, handoffs, state updates, validation gates, and artifact contracts.
- Three control regimes are contrasted: code harnesses (hard external control via program logic), NLAH+IHR (readable natural-language policy executed by a shared runtime via child-agent calls), and self-harnessing (future design with no external harness, a controller model directly harnessing others).
- Formal preliminaries define model as `y = LM_m(c)` over text/image/video context, agent as a model-centered multi-call execution process with state and tool feedback, agent call as the atomic unit of harness execution, and harness as the external system deciding inputs, tools, state, observations, validation, recovery, stopping, and call organization.
- NLAH+IHR uses four layers: (1) base agent — minimal code LLM loop whose only tool is a terminal (file I/O, processes, event logging, launching child agents as new instances of itself via task packets); (2) runtime policy — fixed instruction turning the base agent into IHR; (3) NLAH — per-harness natural-language policy (stages, roles, state, verification, recovery, stopping); (4) scripts/adapters — deterministic code for tests, parsers, benchmark tools, validators.
- The labor division is explicit: natural language carries policy (decomposition, role contracts, evidence discipline, retry, handoff, validation strategy) while code carries exact mechanisms (tool execution, parsing, sandboxing, logging); even nominally single-agent runs are realized as parent orchestrator plus one executor child to keep the harness/execution boundary visible.
- Five NLAH writing principles are given: state the task contract first; separate stages from mechanisms; make state and evidence explicit; write module boundaries so they can be ablated (verifier, self-evolution, multi-candidate search, context compression, markdown memory); prefer simple enforceable language over vague exhortations like "be careful."
- Three evaluation questions frame the paper: can IHR-executed NLAHs preserve performance vs code/prompted baselines; do they materialize intended mechanisms beyond ordinary prompting; and can explicit modules (file-backed state, verifier separation, self-evolution, multi-candidate search) be analyzed as interventions — with claimed results of comparable outcomes, shorter static policies, and measurable behavioral traces.

## 2. [[wiki/02-experiments|Experimental design and results]]

**In one sentence:** IHR-executed Natural-Language Agent Harnesses (NLAHs) match native code harnesses on task scores across coding, terminal-use, and computer-use benchmarks while compressing the policy to a few kilobytes of inspectable text, preserving workflow/contract/tool/recovery mechanisms, and enabling module-level ablations — with parent-child handoff loss as the main remaining bottleneck.

- RQ1 compares three realizations (native Code harness, Prompted NLAH as plain instructions to Codex CLI, IHR-executed NLAH) and finds IHR-executed NLAHs competitive: Live-SWE 73.0 vs Code 67.0 vs Prompt 77.0; MHTBA/TB2 53.9 vs Code 36.0 vs Prompt 57.3; OSWorld/SeeAct 46.3 vs Code 47.1 vs Prompt 47.9.
- All runs share one IHR instantiation — Codex CLI 0.123.0, model gpt-5.4-mini, reasoning effort xhigh, Ubuntu 24.04 (64 cores, 251 GiB), Docker with per-task caps 32 vCPUs / 84 GiB / 40 GiB — on SWE-bench Verified (resolution rate), Terminal-Bench 2.0 (task success), and OSWorld (task success rate).
- NLAHs expose the policy layer in far fewer static materials: Live-SWE 60.1k code tokens / 68 files → 2.9k-token / 3-file NLAH; MHTBA 10.5k / 3 → 0.8k / 1; SeeAct 47.5k / 5 → 1.4k / 1, separating state, validation, recovery, search, and completion gates from deterministic mechanisms.
- RQ2 mechanism audits show NLAHs materialize intended mechanisms: Artifact Contract 1.000 (SWE) / 0.955 (MHTBA), Tool Call Success 0.933 / 0.928, Failed Tool Continuation ~0.992–0.995, Verification Signals 9.89 (SWE) / 22.82 (MHTBA), plus nontrivial workflow-preservation, stage-coverage, and ordered-workflow scores.
- The main weakness is handoff/orchestration: NLAH Orchestration Reliability 0.83 (SWE) / 0.85 (MHTBA) vs Prompt ~0.99–1.00, and Information Handoff Recall 0.32 (SWE) / 0.55 (MHTBA) vs Prompt 1.00, because parent-child execution distributes work across contexts.
- RQ3 module ablations (added one-by-one to a Basic condition) show state/acceptance discipline helps most — File-backed state 73.0→75.6 (SWE) and 44.4→58.3 (OSWorld), Self-evolution →78.8 / 52.8, Evidence-backed answering +2.8 on both — while Multi-candidate search explodes Agent Calls 1.1→5.7 (SWE) but drops SWE 73.0→71.4, and Context compression hurts OSWorld 44.4→36.1 (−8.3).
- Takeaway: explicit NLAH modules are useful when they shorten the path from intermediate work to auditable evidence and benchmark acceptance, not when they add branching, local process layers, or compressed summaries that drift from the evaluator.

## 3. [[wiki/03-appendices|Appendices and limits]]

**In one sentence:** The appendices frame natural-language harnesses as an explicit run-level policy layer over a shared code runtime, document reproducibility via LinguaClaw, show that the Claude-optimized MHTBA code artifact fails to port to GPT (32/89, mostly timeout/stopping-protocol failures), and formalize the NL/code boundary, runtime policy, reusable NLAH modules, and limitations.

- NLAHs are a policy layer, not a code replacement: natural language carries roles, contracts, evidence, retry/validation, state handoff and stopping rules, while code keeps parsers, tool execution, sandboxing, adapters, logging, and deterministic validators.
- Replication package is open-sourced at https://github.com/curated-skills/LinguaClaw (Appendix B).
- MHTBA code-artifact portability test on Terminal-Bench 2.0 under GPT (gpt-5.4-mini, reasoning effort xhigh, 1 attempt, n=89): only 32/89 resolved; 66/89 end in AgentTimeoutError, of which 21 already have verifier reward 1.0 but fail to stop cleanly, and 45 are failed timeouts.
- The portability failure is a runtime-protocol symptom: the code artifact requires a two-call task_complete confirmation, GPT answers with text-only DONE plus no tool call, triggering no-tool warnings and no-op shell commands in a loop (e.g. tune-mjcf: reward 1.0 yet AgentTimeoutError after 3600s, 186 episodes, 5.4M input tokens); Prompt/NLAH keep the same terminal-harness ideas but exit via the Codex task-complete event and artifact /sa-output/artifacts/solve.sh.
- Disagreement slices show extreme cost when code fails but NL succeeds: e.g. Code-fail/Prompt-success (N=26) averages 316.5 episodes, 16.3M input tokens, 146.9 no-tool warnings; all-three-success (N=23) averages only 174.3 episodes, 5.2M tokens, 79.1 warnings.
- Formal boundary (Tables 8–10): base runtime code owns execution substrate, fixed-NL runtime policy (IHR) owns interpretation semantics, replaceable-NL NLAH owns task-family roles/stages/validation/recovery/state/delegation, code hooks own exact tests/validators/parsers; production must keep safety, permissions, evaluation, and parsing in code.
- Module ablations (RQ3): Verifier helps only near the benchmark gate (+0.2 SWE, +8.4 OSWorld); file-backed state is positive on both benchmarks while context compression hurts (SWE 73.0→72.0, OSWorld 44.4→36.1) and Markdown memory is mixed (−2.8 SWE, +5.6 OSWorld).

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Harnesses strongly shape agent performance yet hide inside coupled controller code.
2. Externalize harness policy as editable natural-language documents (NLAHs) run by a shared thin runtime (IHR).
3. Divide labor so natural language carries policy while code keeps exact mechanisms.
4. Show IHR-executed NLAHs match code harnesses on task scores with far smaller inspectable policies.
5. Audit that intended mechanisms materialize while parent-child handoff remains the main bottleneck.
6. Ablate explicit modules to prove state and verification discipline helps while excess branching and compression hurts.
<!-- FIVE_MOVES_END -->
