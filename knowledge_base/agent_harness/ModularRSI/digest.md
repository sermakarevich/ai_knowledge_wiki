> [[index|Wiki]] | [[summary|Summary]]

# ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement — Digest

## 1. [[wiki/01-introduction-abstract|Modular RSI: Modular and Generalizable Recursive Harness Self-Improvement — Abstract and Introduction]]

**In one sentence:** ModularRSI is a benchmark-disjoint, contrastive, and modular framework that converts coarse task-level outcomes into localized harness improvements by contrasting same-task success/failure trajectories, aggregating evidence across tasks, and evolving five functional harness modules independently before integrating them.

## Key points
- Existing harness Recursive Self-Improvement (RSI) typically evolves directly on evaluation benchmarks or subsets drawn from them, so reusable harness improvements cannot be distinguished from benchmark-specific adaptation.
- Trajectory-level ambiguity entangles systematic harness deficiencies with instance-specific reasoning and solution details, so updates from individual or one-sided trajectories produce task-specific modifications that transfer poorly.
- Mechanism-level credit assignment is hard in monolithic harnesses: whole-harness optimization entangles unrelated mechanisms and produces changes that are difficult to attribute and validate.
- ModularRSI addresses this by contrasting successful and failed trajectories for the same task and aggregating evidence across tasks to identify recurring behavioral deficiencies.
- The evolvable harness is decomposed into five functional modules — Agent Loop, Tool Use, Observation Management, Context Management, and Task Completion Detection — each evolved independently within a restricted modification scope, then combined in an integration stage that resolves conflicts.
- A benchmark-disjoint evolution protocol curates 2,000 executable evolution tasks from external data sources fully disjoint from downstream benchmarks, with the evolved harness frozen before evaluation and modifications retained only after validation for correctness, executability, and task-specific overfitting.
- Experiments on TerminalBench 2.0 and SWE-Bench Verified report consistent improvements on unseen in-domain and cross-domain tasks, with transfer across different foundation models; code and datasets at https://github.com/IQuestLab/ModularRSI.

## 2. [[wiki/02-related-work-comparison|Related Work and Comparison of Representative Self-Evolving Frameworks]]

**In one sentence:** Prior harness-evolution work adapts weights, skills, prompts, or whole harnesses but often relies on benchmark-derived data and treats the harness monolithically, so the authors propose benchmark-disjoint evolution plus ModularRSI's fine-grained modular self-evolution via contrastive trajectory analysis.

## Key points
- Prior work reuses execution experience to adapt model weights (Wang et al., 2026c; Zweiger et al., 2026; Luo et al., 2026b).
- Other prior work accumulates reusable skills or context artifacts, or optimizes prompts and external agent mechanisms through trajectory feedback.
- Some approaches use execution traces to diagnose failures and localize editable components, while recent work directly evolves agent implementations or synthesizes harness code.
- TACO specializes harness evolution to observation compression for terminal agents (Ren et al., 2026).
- A central self-improvement challenge is separating transferable improvements from adaptation to development data, making data selection (source-aware rubrics, shortcut filtering) important.
- Existing evaluations cover repository repair, terminal interaction, and online workflows, with HarnessDev, Aspire, and S3 Gym studying harness evolution, feedback budgets, held-out generalization, and hidden evaluation.
- The chunk states that existing harness-evolution methods often rely on evaluation-benchmark data and treat the harness as a monolithic whole, leaving generalizable fine-grained harness improvement underexplored.
- The proposed response is a benchmark-disjoint evolution dataset plus ModularRSI, which decomposes the harness into functional modules and evolves them via contrastive trajectory analysis.

## 3. [[wiki/03-contrastive-trajectory-analysis|Contrastive Trajectory Analysis and Trajectory Memory]]

**In one sentence:** Historical trajectories stored per task across epochs supply contrastive evidence for the Code-Modify Agent's group-wise diagnosis, whose consolidated JSON findings then drive voted, history-aware module modifications gated by validation, cross-module integration, library management, and a 2,000-instance evolution set.

## Key points
- Trajectory Memory stores historical trajectories and their rewards for each task across evolution epochs, supplying extra contrastive evidence when current rollouts alone are insufficient.
- For the Contrastive group, successful and failed trajectories of the same task are paired and compared to identify function-level factors tied to different outcomes.
- For the Negative group (all current rollouts fail), the agent queries Trajectory Memory for a prior success on the same task and pairs it contrastively if found, otherwise performs single-sided diagnosis of deficiencies such as repetitive loops, incorrect tool usage, ineffective recovery, or premature termination.
- For the Positive group (all rollouts succeed), analysis targets execution quality and efficiency such as redundant actions, repetitive exploration, or unnecessary tool calls.
- Modification Target Selection consolidates semantically similar diagnoses on the same function into candidates with a vote count from distinct supporting tasks, prioritizing the highest-ranked, multi-task-supported candidates.
- Validation gates (Program Check, Diff Review, Execution Validation on two sampled tasks) roll back failures via recorded diffs, and after independent evolution of five modules a cross-module integration epoch resolves conflicts before freezing the library.
- Function Merge plus Task-Aware Function Composition control library complexity, and the evolution set holds 2,000 benchmark-disjoint Harbor-format instances (1,000 SWE-related + 1,000 Terminal-related).

## 4. [[wiki/04-evolution-dataset-protocol|Experiment Setting and Generalization Results]]

**In one sentence:** ModularRSI is evaluated on TerminalBench 2.0 and SWE-Bench-Verified with four metrics and shown to improve accuracy and reliability both in-domain and out-of-domain, across models, and over non-modular and prior RSI baselines.

## Key points
- Evaluation uses TerminalBench 2.0 (89 long-horizon terminal tasks) and SWE-Bench-Verified (500 human-validated software engineering tasks), both run under the Harbor framework with original released versions.
- Four metrics are reported: Accuracy (mean per-trajectory success), Pass@3 (solved in at least 1 of 3 rollouts), StepNum (mean agent-environment steps per rollout), and Pass3 (solved in all 3 rollouts).
- Evolution runs 3 epochs for single-module and joint-module evolution, sampling 120 TB-related plus 120 SWE-related instances from the 2,000-instance evolution dataset, using DeepSeek-V4-Flash-Preview and DeepSeek-V4-Flash-0731 with a 2M TPM limit and batch size 10.
- In-domain evolution improves accuracy from 47.57 to 52.43 on TerminalBench 2.0 and from 73.40 to 76.45 on SWE-Bench-Verified, with largely monotonic gains across RSI generations (see Appendix F).
- Out-of-domain transfer also holds: TB-evolved harness reaches 75.80 on SWE-Bench-Verified and SWE-evolved harness reaches 49.40 on TerminalBench 2.0, and TerminalBench Pass3 rises from 30.34 to 35.96, indicating better reliability.
- A harness evolved with DeepSeek-V4-Flash Preview on TB tasks transfers to other backbones on TerminalBench 2.0 (GLM-5.2: 59.55 to 61.80; MiniMax-2.5: 41.57 to 44.94; DeepSeek-V4-Flash: 47.57 to 52.43).
- Independent per-module evolution plus integration beats joint and non-modular evolution (ModularRSI 52.43 Acc vs. 44.19 joint vs. 46.44 non-modular vs. 47.57 baseline), and all five single-module variants beat baseline with Agent Loop best on accuracy and Observation Management cutting steps to 22.50.
- Against prior methods on TerminalBench 2.0 with DeepSeek-V4-Flash-0731 (Terminus-2 baseline 61.79, 16-epoch AHE/Meta-Harness, web search disabled), AHE (62.54) and Meta-Harness (62.92) stay near baseline while ModularRSI reaches 67.42 Acc, 78.65 Pass@3, 56.18 Pass3.

## 5. [[wiki/05-experimental-results|Experimental Results: Contrastive Analysis, Data Quality, and Conclusion]]

**In one sentence:** ModularRSI's ablations show contrastive trajectory pairs get progressively absorbed into the harness, medium-difficulty evolution data generalizes better (+2.20 pp on SWE-Bench Verified), and the authors conclude benchmark-disjoint modular evolution works while noting missing ablations and subset-scale experiments as limitations.

## Key points
- A gain of more than five points is reported as demonstrating the stronger generalizability of ModularRSI to unseen tasks.
- Contrastive trajectory analysis plus modular evolution is used to localize harness deficiencies more accurately and identify generalizable improvements.
- On Terminal-Bench 2.0 the usable contrastive-pair ratio falls across epochs (reported values 36.67% and 34.17%, Δ = -7.50 pp in Fig. 3), interpreted as the harness absorbing reusable improvements so fewer tasks have coexisting success and failure trajectories.
- Moderately difficult evolution tasks are hypothesized to give the most informative contrasts because easy tasks lack failures and extremely difficult tasks rarely yield successful trajectories.
- The Medium-centered difficulty setting improves consistently more than the Hard & Easy setting during evolution (Fig. 4, DeepSeek-V4-Flash Preview as foundation model), and reaches 76.45% vs 74.25% on SWE-Bench Verified — a 2.20 percentage-point gap.
- Stated limitations are no dedicated ablation isolating contrastive trajectory analysis and use of only a subset of the 2,000 curated evolution instances due to computational cost.

## 6. [[wiki/06-module-wise-evolution|1. Agent Loop — Five-Module Harness Architecture]]

**In one sentence:** The chunk defines a five-module harness in which Agent Loop is the outer execution coordinator whose central Loop control maintains execution state, schedules calls, handles retries, and decides whether to continue, while the other four modules exchange call/return inputs and outputs with it and the LLM and terminal environment act as external resources.

## Key points
- The outer box is Agent Loop and the central Loop control box is its runtime logic: maintaining execution state, scheduling calls, handling retries, and deciding whether to continue.
- Each of the other four modules exchanges inputs and outputs with this controller, with bidirectional module arrows indicating a call and its return; the arrows do not prescribe a fixed module-to-module execution sequence.
- The LLM and environment are external resources: the LLM generates responses, while the environment runs commands and stores files and processes; before execution, the composer selects one implementation for each module.
- A normal iteration is: Agent Loop asks Context Management to update conversation history (compressing when needed), sends the current prompt to the LLM, Tool Use parses the response into commands and a completion signal, executes commands in the environment, and returns results or errors.
- Observation Management reads the current terminal output and converts it into agent-readable feedback, which differs from Context Management because Context Management works on the accumulated conversation.
- Task Completion Detection returns a stop recommendation and a reason — the example detector requires two consecutive completion declarations — and Agent Loop maintains that count, issues the confirmation prompt after the first declaration, and follows the recommendation, while evolved loop variants can override it.
- Parsing errors can trigger a retry, and session failures or execution limits can end the run.
- `AgentLoop.run` takes `initial_prompt: str, original_instruction: str, observation: Observation, context_mgmt: ContextMgmt, tools: ToolSet, verification: VerificationLoop, chat: Chat, ctx: ModuleCtx` and returns `AgentLoopResult` (execution status, final text, and failure tag); each implementation is registered with a name, description, and configuration parameters, and the shared `ModuleCtx` provides task configuration, environment access, and recording services.

## 7. [[wiki/07-appendix-function-interfaces|Output: observation text and updated observation state]]

**In one sentence:** The chunk specifies the per-module function interfaces (Observation returns observation text plus updated state; ToolSet, ContextMgmt, and VerificationLoop define their own I/O) and appends the structured-analysis schema (Table 8, Listing 2) and abridged evolution prompts (C.1–C.4).

## Key points
- `Observation.capture(prev: ObsState, ctx: ModuleCtx) -> tuple[ObsResult, ObsState]` takes the previous observation state and returns observation text (current environment feedback) plus the updated observation state.
- `ToolSet` splits tool use into `parse_llm_response(response: str) -> LLMResponseParseResult` (model text to commands, completion signal, parsing errors) and `execute(call: ToolCall, ctx: ModuleCtx) -> ToolResult` (a tool call to execution result with success, output, error).
- `ContextMgmt` takes conversation history plus the original task and returns updated Chat and an optional handoff prompt via `maybe_compress` and `force_summarize`, both with signature `(chat: Chat, original_instruction: str, ctx: ModuleCtx) -> CompressResult`.
- `VerificationLoop.should_terminate(state: AgentLoopState, ctx: ModuleCtx) -> tuple[bool, str]` takes loop state including recent feedback and signals and returns a stop recommendation plus its reason, but only recommends — the Agent Loop keeps state and controls continuation.
- Implementation refines the Sec. 3.3 trajectory groups into routing buckets without changing trajectory reward: Positive maps to all-pass efficient / all-pass wasteful, Contrastive to mixed, Negative to fixable fail / stuck fail / unreachable fail, and infra-only tasks are excluded from harness diagnosis (Table 8).
- Each analyzed task yields one finding record with fields `task`, `lens`, `locked_module`, `is_culprit`, `divergence`, `would_change_outcome`, `fixable_now`, `suggested_change`, plus `other module or note` for negative attributions and `parse status`; Listing 2 shows an Agent Loop `is_culprit: true` case (missing build/validation, evidence-gated completion fix) versus a contrast-lens `is_culprit: false` case (verifier-side noise).
- The abridged Appendix C prompts enforce: C.1 read-only counterfactual attribution (`is_culprit` only if a concrete module change would move the task from fail toward pass); C.2 general harness modification across the complete finding set, ending with `<validate/>`, `<commit_patch/>`, `<task_complete>true</task_complete>`; C.3 reward-blind diff review (ACCEPT only with a concrete causal link and no task-specific overfit); C.4 at most one coherent cross-module repair with no new capability or benchmark-specific special case.

## 8. [[wiki/08-appendix-prompts-integration|Appendix Task–F: Trajectory Case Studies, Difficulty Curation, and Evolution Curve]]

**In one sentence:** Three trajectory-group case studies (contrastive NULL-filter, negative FFmpeg linkage, positive file-write retries) each produce a promoted module update with later-trace confirmation, supported by difficulty-curation settings and a TerminalBench 2.0 evolution curve scored by accuracy plus an Opus-4.8 trajectory judge.

## Key points
- Trajectory evidence across five runs plus replay splits as 732 success–failure pairs (40.67%), 150 all-fail groups paired with historical success (8.33%), 262 all-fail with no earlier success (14.56%), and 648 all-succeed (36.00%).
- Contrastive case (Scala-to-PySpark sales pipeline, NULL categories): successful rollout r0 keeps an isNotNull() filter yielding 47 rows and reward 1, while failed rollout r1 matches legacy Scala behavior yielding 52 rows with five NULLs and reward 0, leading to a persistent task checklist absorbed into planning with guard in generation 9.
- Later observation in epoch 3 with generation 13 shows the same task keeping the NULL filter, an episode-17 completion check, a 47-row output check, all 52 external tests passing, and 2 of 3 rollouts passing versus 1 in the epoch-2 encounter.
- Negative case (build FFmpeg 0.10.16, ldd must show libavcodec, libavformat, libx264): epoch-1 r0 links only libx264.so.164, declares completion twice with empty commands, and scores 1 failed / 9 passed, leading to a completion integrity guard in generation 6; in epoch 3 with generation 14 all three rollouts pass with all 10 external tests passing.
- Positive case (Zip Slip fix in Go file-upload server): epoch-2 rollouts all succeed but take 41, 24, and 43 episodes because multi-line write file calls fall through to the shell ("write file: command not found"), leading to tools/combined robust.py in generation 9; in epoch 3 with generation 12 the helper returns "wrote 2204 bytes", all 60 tests pass, and episodes fall from [41, 24, 43] to [26, 18, 31] with mean 36 to 25.
- Difficulty curation builds two SWE-related evolution sets (Medium-centered vs Hard & Easy) by estimating instance difficulty from eight trajectories from MiniMax M2.7, GLM-5.2, DeepSeek-V4-Pro, and DeepSeek-V4-Flash.
- Evolution-curve evaluation scores successive RSI generations on TerminalBench 2.0 with both benchmark rewards (task accuracy) and an Opus-4.8 LLM trajectory judge over five 1–5 dimensions normalized to 0–100 (Fig. 6 shows Judge around 74.0 and Acc around 52.2 by generation 22).

## The argument in five moves

1. Generalizable harness self-improvement is blocked at three levels — data (evolution on benchmarks confounds reuse with adaptation), trajectory (single or one-sided trajectories entangle harness flaws with task-specific details), and mechanism (monolithic whole-harness edits entangle unrelated components) — so ModularRSI proposes benchmark-disjoint, contrastive, modular evolution.
2. The method turns coarse task-level rewards into localized signals: same-task success/failure pairs are contrasted (Contrastive group), all-fail rollouts fall back to Trajectory Memory or single-sided diagnosis (Negative group), and all-success rollouts are mined for efficiency (Positive group), with diagnoses consolidated into JSON findings and voted across tasks to favor multi-task-supported function edits.
3. Edits are kept reliable by restricting scope to five independently evolved modules (Agent Loop, Tool Use, Observation Management, Context Management, Task Completion Detection), maintaining per-function Evolution History, gating every change through Program Check, reward-blind Diff Review, and Execution Validation with rollback, then reconciling the modules in a cross-module integration epoch before freezing the library.
4. Evolution runs on a curated 2,000-instance benchmark-disjoint Harbor-format pool (1,000 SWE-related + 1,000 Terminal-related) with quality, executability, and similarity filtering; frozen-harness evaluation on TerminalBench 2.0 and SWE-Bench Verified shows in-domain gains, out-of-domain transfer (TB-evolved helps SWE and vice versa, Pass3 reliability up), cross-model transfer, and a clear win for independent-plus-integration modular evolution over joint/non-modular variants and over prior RSI baselines (AHE, Meta-Harness).
5. Ablations and cases close the loop: the contrastive-pair ratio falls as reusable fixes are absorbed, Medium-centered difficulty beats Hard & Easy (+2.20 pp on SWE-Bench Verified), and contrastive/negative/positive case studies each trace a promoted module update to later-trace confirmation — while the authors flag the missing dedicated contrastive-ablation and subset-scale experiments as limitations.
