> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Output: observation text and updated observation state
**In one sentence:** The chunk specifies the per-module function interfaces (Observation returns observation text plus updated state; ToolSet, ContextMgmt, and VerificationLoop define their own I/O) and appends the structured-analysis schema (Table 8, Listing 2) and abridged evolution prompts (C.1–C.4).
## Key points
- `Observation.capture(prev: ObsState, ctx: ModuleCtx) -> tuple[ObsResult, ObsState]` takes the previous observation state and returns observation text (current environment feedback) plus the updated observation state.
- `ToolSet` splits tool use into `parse_llm_response(response: str) -> LLMResponseParseResult` (model text to commands, completion signal, parsing errors) and `execute(call: ToolCall, ctx: ModuleCtx) -> ToolResult` (a tool call to execution result with success, output, error).
- `ContextMgmt` takes conversation history plus the original task and returns updated Chat and an optional handoff prompt via `maybe_compress` and `force_summarize`, both with signature `(chat: Chat, original_instruction: str, ctx: ModuleCtx) -> CompressResult`.
- `VerificationLoop.should_terminate(state: AgentLoopState, ctx: ModuleCtx) -> tuple[bool, str]` takes loop state including recent feedback and signals and returns a stop recommendation plus its reason, but only recommends — the Agent Loop keeps state and controls continuation.
- Implementation refines the Sec. 3.3 trajectory groups into routing buckets without changing trajectory reward: Positive maps to all-pass efficient / all-pass wasteful, Contrastive to mixed, Negative to fixable fail / stuck fail / unreachable fail, and infra-only tasks are excluded from harness diagnosis (Table 8).
- Each analyzed task yields one finding record with fields `task`, `lens`, `locked_module`, `is_culprit`, `divergence`, `would_change_outcome`, `fixable_now`, `suggested_change`, plus `other module or note` for negative attributions and `parse status`; Listing 2 shows an Agent Loop `is_culprit: true` case (missing build/validation, evidence-gated completion fix) versus a contrast-lens `is_culprit: false` case (verifier-side noise).
- The abridged Appendix C prompts enforce: C.1 read-only counterfactual attribution (`is_culprit` only if a concrete module change would move the task from fail toward pass); C.2 general harness modification across the complete finding set, ending with `<validate/>`, `<commit_patch/>`, `<task_complete>true</task_complete>`; C.3 reward-blind diff review (ACCEPT only with a concrete causal link and no task-specific overfit); C.4 at most one coherent cross-module repair with no new capability or benchmark-specific special case.
---
## Observation interface
Output: observation text and updated observation state.
```python
class Observation(Protocol):
    async def capture(
        self, prev: ObsState, ctx: ModuleCtx,
    ) -> tuple[ObsResult, ObsState]: ...
```
Observation Management returns current environment feedback, whereas Context Management updates the accumulated conversation history.
## Tool use
Model text -> commands, completion signal, parsing errors. A tool call -> execution result (success, output, error).
```python
class ToolSet(Protocol):
    def parse_llm_response(
        self, response: str,
    ) -> LLMResponseParseResult: ...

    async def execute(
        self, call: ToolCall, ctx: ModuleCtx,
    ) -> ToolResult: ...
```
## Context management
Input: conversation history and the original task. Output: updated Chat and an optional handoff prompt.
```python
class ContextMgmt(Protocol):
    async def maybe_compress(
        self, chat: Chat, original_instruction: str,
        ctx: ModuleCtx,
    ) -> CompressResult: ...

    async def force_summarize(
        self, chat: Chat, original_instruction: str,
        ctx: ModuleCtx,
    ) -> CompressResult: ...
```
## Task completion detection
Input: loop state, including recent feedback and signals. Output: a stop recommendation and its reason.
```python
class VerificationLoop(Protocol):
    async def should_terminate(
        self, state: AgentLoopState, ctx: ModuleCtx,
    ) -> tuple[bool, str]: ...
```
> "The completion detector returns a recommendation; Agent Loop maintains the state and controls whether execution continues."
## Structured analysis findings
The three trajectory groups in Sec. 3.3 describe the available reward evidence; the implementation refines them into routing buckets that select an analysis path without changing trajectory reward, and tasks with infrastructure-only failures are excluded from harness diagnosis.
| Method group | Implementation buckets |
|---|---|
| Positive | all pass efficient, all pass wasteful |
| Contrastive | mixed |
| Negative | fixable fail, stuck fail, unreachable fail |
| Excluded | infra only |
Table 8: Mapping from the method-level trajectory groups to the routing buckets used by the implementation.
Each analyzed task produces one finding record: `task`, `lens` (analysis mode), `locked_module` (module changeable in the current evolution run), `is_culprit` (causal decision), `divergence` (trajectory evidence), `would_change_outcome` (counterfactual judgment), `fixable_now` and `suggested_change` (whether/how the system can act); for negative attribution, `other module or note` may record an alternative explanation; `parse status` records structured-output parse success, so some optional fields are absent from some records.
Listing 2 (abridged; text values shortened, field names/decisions/causal conclusions unchanged): first record supports an Agent Loop edit — task `draft_dp_3493beee_outa`, lens `agent_loop`, `is_culprit: true`, divergence "The passing roll ran build and package commands. The failing roll ran no build or validation command and repeatedly declared completion.", `would_change_outcome: "Yes. A completion gate that requires validation evidence would force the missing build-and-check stage."`, `fixable_now: true`, suggested change "Add an evidence-gated completion variant. Allow termination only after a successful build, test, or run has been observed." Second record abstains — task `draft_dp_eae0d1ff_outb`, lens `contrast`, `is_culprit: false`, divergence "Both rolls produced functionally equivalent solutions. The failing artifact compiled and passed differential tests against the reference program.", `would_change_outcome: "No. The artifact evidence points to verifier-side noise rather than an Agent Loop failure."`, `fixable_now: false`.
## Abridged prompts used in harness evolution
Full prompts contain task trajectories, module traces, findings, and code diffs inserted at runtime; excerpts preserve original wording and order, with angle brackets for runtime input and bracketed lines for omitted dynamic content or repeated rules.
### C.1 Trajectory analysis
Two modes — contrastive (successful vs failed trajectories) and efficiency (successful but wasteful) — sharing one attribution rule and output format. Excerpt: "You are a READ-ONLY diagnostician deciding ONE thing: would changing the '<TARGET_MODULE>' module actually CHANGE or IMPROVE this task's outcome? You get the SAME task solved on one roll and FAILED on another (same code, different sampling)." / "This is NOT blame-attribution. Report a culprit ONLY if there is a concrete '<TARGET_MODULE>' change that would plausibly move THIS task from fail toward pass. If no such change would help, the answer is no culprit, and you do NOT fix." Decision order: (1) Divergence — where pass and fail rolls stopped behaving the same, citing episodes/steps; (2) counterfactual — YES and fits inside module (`is_culprit` and `fixable_now` true + change), YES but needs architecture change (`is_culprit` true, `fixable_now` false), NO (`is_culprit` false; do not invent a marginal tweak). Required output `<contrast_finding>` JSON with `task`, `is_culprit`, `locked_module`, `divergence`, `would_change_outcome`, `fixable_now`, `suggested_change`.
### C.2 Harness modification
Receives one selected direction plus all supporting findings; asks the Code-Modify Agent to implement the shared mechanism, not a task-specific patch. Excerpt: "The direction below was chosen from a backlog of directions, and the evidence under it is the COMPLETE set of observations that support it - every one of them, not a sample. Build the change that addresses the direction across all of that evidence. Do NOT narrow it to whichever single task reads most vividly: a change that only rescues one named task is worthless here and has sunk a lineage before." Working rules: read involved module(s) first; make the change general across every finding; action-specific ADD/MODIFY/REPLACE rule; then `<validate/>`, `<commit_patch/>`, `<task_complete>true</task_complete>`.
### C.3 Diffs review
Reward-blind: receives proposed diff, stated intent, and trajectory evidence; checks effectiveness and overfit. Excerpt: "You are the terminus-2-modular editor, reviewing a change you just made to the agent's modules. The change is ALREADY applied to the staging copy you can read. Your job now is NOT to edit - it is to decide whether this change should be KEPT or REJECTED." Review: (1) Effective — require concrete causal link between changed mechanism and a trajectory failure (new variants must be Composer-selectable for similar tasks); (2) Overfit — reject task names, task-specific files/outputs, single-task-tuned constants. Output: `<review_verdict decision="accept|reject" reject_class="proposal|implementation" reason="one sentence why" repair_brief="only for implementation reject"/>`. "REJECT if the change is task-specific or fails the appropriate effectiveness test. Otherwise ACCEPT."
### C.4 The cross-module integration
After independently evolved module variants are combined, the run-in prompt guides the Code-Modify Agent to repair interactions. Excerpt: "You are performing integration run-in on a library assembled from independently evolved module lineages. This is not feature evolution. Make at most one coherent cross-module repair; do not add a new capability, tool, behavioral dimension, or benchmark-specific special case." Inputs include same-task same-bundle support evidence (`<TRAJECTORY_SUMMARIES>`) and static conflict candidates (`<CONFLICT_FINDINGS>`).
**Covers:** Appendix: per-module function interfaces (observation/state I/O); structured findings (Table 8, Listing 2); abridged prompts C.1–C.4
