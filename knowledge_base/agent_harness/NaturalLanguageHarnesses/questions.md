---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# NaturalLanguageHarnesses — Retrieval Questions

## Q1 (Core recall — §1 Intro/method): What are the four layers of the NLAH+IHR stack, and what does each own?

<details>
<summary>Answer</summary>

1. **Base agent** — minimal code LLM loop whose only tool is a terminal (file I/O, processes, event logging, launching child agents as new instances of itself via task packets).
2. **Runtime policy** — fixed instruction turning the base agent into the IHR (Intelligent Harness Runtime).
3. **NLAH** — per-harness natural-language policy: stages, roles, state, verification, recovery, stopping.
4. **Scripts/adapters** — deterministic code for tests, parsers, benchmark tools, validators.

Labor division: natural language carries policy (decomposition, role contracts, evidence discipline, retry, handoff, validation strategy); code carries exact mechanisms (tool execution, parsing, sandboxing, logging). Even nominally single-agent runs use parent orchestrator + one executor child to keep the harness/execution boundary visible.

</details>

## Q2 (Elaboration — §1 Intro/method): Why must even a "single-agent" run be split into parent orchestrator + executor child, and what breaks if you collapse them?

<details>
<summary>Answer</summary>

The split keeps the harness/execution boundary visible: the parent holds run-level policy (task contract, stages, state, validation gates, recovery, stopping) while the child does the work. If you collapse them into one undifferentiated loop, harness policy and execution trace mix in one context — it becomes hard to inspect, compare, transfer, or ablate the harness (the original complaint about coupled controller code). You also lose clean module boundaries (verifier, self-evolution, multi-candidate search, context compression, markdown memory) and the ability to swap or remove one policy piece without rewriting code.

</details>

## Q3 (Core recall — §2 Experiments): What were the RQ1 head-to-head scores and the shared evaluation setup?

<details>
<summary>Answer</summary>

Three realizations: native Code harness vs Prompted NLAH (plain instructions to Codex CLI) vs IHR-executed NLAH:

- **Live-SWE (coding):** IHR 73.0 vs Code 67.0 vs Prompt 77.0.
- **MHTBA / Terminal-Bench 2.0 (terminal use):** IHR 53.9 vs Code 36.0 vs Prompt 57.3.
- **OSWorld / SeeAct (computer use):** IHR 46.3 vs Code 47.1 vs Prompt 47.9.

Shared setup: one IHR instantiation — Codex CLI 0.123.0, model gpt-5.4-mini, reasoning effort xhigh, Ubuntu 24.04 (64 cores, 251 GiB), Docker caps 32 vCPUs / 84 GiB / 40 GiB — on SWE-bench Verified (resolution rate), Terminal-Bench 2.0 (task success), OSWorld (task success rate). Takeaway: IHR-executed NLAHs are competitive with code harnesses.

Static-policy compression: Live-SWE 60.1k code tokens / 68 files → 2.9k-token / 3-file NLAH; MHTBA 10.5k / 3 → 0.8k / 1; SeeAct 47.5k / 5 → 1.4k / 1.

</details>

## Q4 (Elaboration — §2 Experiments): Why is parent-child handoff the main bottleneck, and what breaks when work is distributed across contexts?

<details>
<summary>Answer</summary>

RQ2 audits show mechanisms mostly materialize (Artifact Contract 1.000 SWE / 0.955 MHTBA; Tool Call Success 0.933 / 0.928; Failed Tool Continuation ~0.992–0.995; Verification Signals 9.89 SWE / 22.82 MHTBA), but orchestration degrades: Orchestration Reliability 0.83 (SWE) / 0.85 (MHTBA) vs Prompt ~0.99–1.00, and Information Handoff Recall only 0.32 (SWE) / 0.55 (MHTBA) vs Prompt 1.00.

Why: parent-child execution distributes work across separate contexts, so evidence and intermediate state must be explicitly handed off instead of living in one shared trace. What breaks if handoff/state discipline is weak: the parent loses details the child saw, recovery and validation gates fire on incomplete evidence, and runs need more episodes/tokens. RQ3 confirms the fix direction: file-backed state and evidence-backed answering help most (e.g. File-backed state 73.0→75.6 SWE, 44.4→58.3 OSWorld; Evidence-backed +2.8 on both), while branching/compression that drifts from the evaluator hurts (Multi-candidate search: Agent Calls 1.1→5.7 but SWE 73.0→71.4; Context compression: OSWorld 44.4→36.1, −8.3).

</details>

## Q5 (Core recall — §3 Appendices/limits): What did the MHTBA portability test find, and what was the failure mechanism?

<details>
<summary>Answer</summary>

The Claude-optimized MHTBA code artifact was ported to GPT (gpt-5.4-mini, reasoning effort xhigh, 1 attempt, n=89) on Terminal-Bench 2.0: only **32/89 resolved**. **66/89** end in AgentTimeoutError, of which **21 already have verifier reward 1.0 but fail to stop cleanly**, and 45 are failed timeouts.

Mechanism: a runtime-protocol symptom — the code artifact requires a two-call `task_complete` confirmation, but GPT answers with text-only DONE plus no tool call, triggering no-tool warnings and no-op shell commands in a loop (e.g. tune-mjcf: reward 1.0 yet AgentTimeoutError after 3600s, 186 episodes, 5.4M input tokens). Prompt/NLAH keep the same terminal-harness ideas but exit via the Codex task-complete event and artifact `/sa-output/artifacts/solve.sh`. Disagreement cost is extreme: Code-fail/Prompt-success (N=26) averages 316.5 episodes, 16.3M input tokens, 146.9 no-tool warnings vs all-three-success (N=23) at 174.3 episodes, 5.2M tokens, 79.1 warnings.

Replication package: https://github.com/curated-skills/LinguaClaw (Appendix B).

</details>

## Q7 (Evaluation — [[critical_thinking|Critical Analysis]]): The abstract says IHR-executed NLAHs achieve "comparable task outcomes" to code harnesses. Is that the strongest true claim the RQ1 numbers support, and why does it matter?

<details>
<summary>Answer</summary>

No — it understates an inconvenient pattern. On all three benchmarks, Prompted NLAH (plain instructions, no runtime) actually beats IHR: Live-SWE 77.0 vs 73.0, MHTBA 57.3 vs 53.9, OSWorld 47.9 vs 46.3. IHR only clearly beats the Code baseline on two of three (Live-SWE 73.0 vs 67.0, MHTBA 53.9 vs 36.0) and loses to Code on OSWorld (46.3 vs 47.1). So "comparable" is true only in the weak sense that no realization dominates — it hides that the simplest, runtime-free baseline (Prompt) scores best everywhere tested.

Why it matters: the paper's case for NLAH+IHR has to rest on inspectability, portability, and ablatability (20x smaller static policy, mechanism audits, module ablations) rather than on a task-score win, since the raw numbers do not show IHR outperforming plain prompting. Treat "comparable task outcomes" as "no worse, with better legibility," not as "improves scores" — see [[critical_thinking|Critical Analysis]] claim (1) for the full breakdown.

</details>

## Q6 (Transfer — §3 Appendices/limits): You are porting a harness to a new model that ignores the stopping protocol. How do you apply the NL/code boundary to fix it?

<details>
<summary>Answer</summary>

Apply the Tables 8–10 boundary: keep safety, permissions, evaluation, and parsing in code; keep roles, contracts, evidence, retry/validation, state handoff, and stopping rules in the replaceable-NL NLAH; keep interpretation semantics in the fixed-NL runtime policy (IHR) and execution substrate plus exact tests/validators/parsers in code hooks.

Concretely: (1) do not patch stopping by exhorting the model ("be careful / remember to stop") — prefer simple enforceable language; (2) rewrite the NLAH stopping rule to the new runtime's enforceable exit (as the paper did: exit via the Codex task-complete event and artifact `/sa-output/artifacts/solve.sh` instead of the two-call `task_complete` confirmation); (3) keep the verifier gate in code so reward-1.0 work is still accepted even if the model's stop utterance changes; (4) add file-backed state + evidence-backed answering (both helped on SWE and OSWorld) so the stop decision reads auditable evidence, not a free-text DONE. Verifier helps mostly near the benchmark gate (+0.2 SWE, +8.4 OSWorld); avoid context compression (SWE 73.0→72.0, OSWorld 44.4→36.1) and be cautious with Markdown memory (−2.8 SWE, +5.6 OSWorld).

</details>
