> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction & Related Work

**In one sentence:** Task completion is an incomplete — formally, non-identifying — projection of the full evaluation outcome of context compression, because compression can substantially raise an agent's interaction cost (reacquisition of dropped state via retrieval tool calls) while leaving completion statistically unchanged, and no prior work measures that reacquisition cost or causally manipulates state availability.

## Key points

- **Core gap:** prior evaluations ask whether task performance survives compression; this paper asks what runtime cost accumulates *before* performance changes — completion measures *retention* (whether needed facts survive) but not *reacquisition* (what the agent does, and what it costs, when execution-relevant state is genuinely absent and must be re-queried).
- **Headline divergence:** at the pre-specified 5× comparison point, completion is statistically unchanged in all six model–regime cells (all p ≥ 0.125), while retrieval calls increase in every one of the six comparisons and account for almost all added interaction (e.g., GPT-5.5: completion 80% → 85%, p = 1.0, while retrieval ~21.0 → 63.9 calls, p = .002, roughly tripling at +42.9 calls).
- **Completion responds only late:** even DeepSeek — the most affected model — shows significant completion change only at the most aggressive 10× ratio (p = .016); the retrieval/cost signal responds at milder compression than completion does.
- **Protocol:** deterministic planning environment, fixed interaction horizon of 24 turns, compression ratio varied via a sliding-window operator; dropped state manipulated via oracle restoration; tool calls decomposed into retrieval (re-acquiring external state) vs execution (task operations); three models — DeepSeek (deepseek-v4-flash, full severity sweep), Qwen (qwen3.7-plus, fixed 5×), GPT-5.5 (fixed 5×) across two task regimes.
- **Causal probes:** retention interventions separate *how much* state is retained from *which* state and *whether retained content is valid* — random selection matches an offline hindsight oracle, while replacing retained D-state with semantically irrelevant content increases retrieval by 57% (p < .001) with completion statistically unchanged (p = 0.41).
- **Boundary of the effect:** in ALFWorld the same sliding operator produces no retrieval surge, so the reacquisition signature is environment-dependent, not intrinsic to shortening context; the cost emerges when execution-relevant state becomes absent and must be reacquired.
- **Three contributions:** (1) non-identifiability of interaction cost by completion (formalized, Proposition 1, Sec. 3.1, and realized under intervention); (2) mechanistic decomposition along a recoverability axis — externally queryable task state (D) vs history-dependent state (R), with loss of R inflating defensive re-querying of D; (3) retention interventions as causal probes, showing state content is behaviorally load-bearing only when the digest occupies a substantial share of the context window.
- **Positioning vs related work:** prior lines cover what to keep (ACON, Memento, RE-TRAC…), whether information survives (Context Codec, Reclaim), whether it is used ("lost in compaction"), and aggregate efficiency (Less Context Better Agents, CostBench) — none measures what the agent does when state is actually gone; the paper's actionable quantity for runtime designers is "which execution-relevant state, if dropped, would the agent spend its budget re-acquiring?"

---

## The problem: completion hides reacquisition cost

Long-horizon agents accumulate trajectories that quickly exceed any context window, so modern runtimes compress — via summarization, sliding windows, or retrieval filters — as a matter of course. The common evaluation view holds that compression succeeds when it preserves task performance while reducing context cost: failure-aware compressors can match full-context performance on many tasks (ACON), and the authors find even a deterministic extractive summary to be **near-lossless at 5× compression**.

The paper's complementary question: "what runtime cost can accumulate before that performance changes?" Task completion is "an incomplete measure of the runtime cost of context compression — it does not by itself reveal the interaction cost incurred when the agent must reacquire compressed-away state."

The conceptual distinction is between **retention** and **reacquisition**:

> "Near-lossless" measures *retention*: whether the surviving context still contains the needed facts. It does not measure *reacquisition*: what the agent does when a piece of execution-relevant state is genuinely absent — re-querying the environment for task graphs, hidden constraints, resource occupancy — and what that costs in the agent's own currency.

Two structural features of completion make it "a blunt instrument for this cost": completion is bounded by the interaction horizon, and it "is co-determined by the interaction horizon and can remain unchanged while the reacquisition burden grows." Tool calls, by contrast, "provide a direct measure of the interaction cost spent on reacquisition." Whether compression becomes costly therefore "is not determined by retained content alone; it also depends on what the agent must do to reacquire the state that is no longer available."

## The fourth prior questions and the fifth question

Prior work on context compression asks four questions: *what to keep* (methods: ACON; Memento; RE-TRAC), *whether information survives or is recoverable* (Context Codec's round-trip guarantees; Reclaim's black-box recovery), *whether surviving information is used* (the "lost in compaction" attention bottleneck), and *which context-management strategy performs best on capability and efficiency jointly* (aggregate efficiency evaluation; Less Context, Better Agents; agent-evaluation surveys call cost an under-measured axis of LLM-agent assessment). "These lines evaluate what compression preserves or achieves. None measures what the agent does when state is actually gone."

The paper's fifth question is the gap it enters — "a controlled demonstration that the two can diverge":

> **What does it cost the agent to re-acquire what was dropped, and is that cost visible to standard metrics?**

## The controlled measurement protocol

The protocol fixes the confounding variables one by one:

- **Fixed interaction horizon** of 24 turns;
- **Compression ratio varied** via a sliding-window operator (one model swept across severities);
- **Two task regimes** that differ in how much execution-relevant state must be discovered at runtime;
- **Manipulated availability of execution-relevant state** via controlled oracle restoration — injecting specific dropped state back into the context;
- **Decomposed tool calls** into *retrieval* (re-acquiring external state) vs *execution* (performing the task's operations).

Scope across models: DeepSeek (deepseek-v4-flash) at a full severity sweep; Qwen (qwen3.7-plus) and GPT-5.5 at a fixed 5× ratio — "to separate what holds across models from what is model-specific."

## Contributions

**1. Evaluation non-identifiability under context compression.** Task completion is not an identifying projection of interaction cost — formalized as a non-identifiability result and realized under controlled intervention. GPT-5.5 pays the largest reacquisition cost in the study while its completion is not detected as changed (80% → 85%, p = 1.0; retrieval 21.0 → 63.9, p = .002); and in a retention intervention (Sec. 3.5), injecting semantically irrelevant state raises retrieval by 57% (p < .001) while completion is statistically unchanged (p = 0.41). "Completion is blind not only to the *magnitude* of interaction cost, but also to its *behavioral consequence* — completion did not expose the large cost difference induced by the intervention."

**2. A mechanistic decomposition of the hidden cost.** The reacquisition burden is decomposed along a recoverability axis: externally queryable task state (**D**) versus history-dependent state (**R**), "with a re-query loop in which the loss of R inflates defensive re-querying of D." Retrieval calls increase in all six of the model–regime comparisons and account for almost all of the added interaction; restoring dropped state removes roughly half the retrieval cost; and across a retention-budget axis the reduction tracks the retained coverage of D-state — "a dose–response within a fixed digest format."

**3. Retention interventions as causal probes: the behavioral relevance of retained state.** A family of retention interventions separates *how much* state is retained from *which* state is retained and *whether the retained content is valid*. Findings:

- Fine-grained selection among real, task-relevant atoms has limited marginal value — **random selection matches an offline hindsight oracle**;
- Replacing D content with semantically irrelevant state sharply increases retrieval; the content effect replicates across models at the loose budget (GPT-5.5, Sec. 4.6.4), "while its magnitude and budget-gating remain model-specific";
- State content is behaviorally load-bearing, "but this is visible only when the digest occupies a substantial share of the context window (a content × budget interaction)";
- An external probe in ALFWorld (Sec. 4.7) bounds the whole signal: where the relevant state can be re-observed directly, the same operator produces no retrieval surge.

**Boundary of the cost signal.** Across three models and two task regimes: reacquisition cost consistently increases, while its translation into completion loss varies substantially — DeepSeek degrades at high compression, Qwen is largely insensitive, GPT-5.5 does not. The cost signal is also the earlier one: "retrieval responds at milder compression (5×) before completion responds, which for DeepSeek occurs only at 10×." ALFWorld bounds the signal from the other side: "there, the same sliding compression produces no retrieval surge at all, so even the *presence* of the cost is conditional."

**Scope disclaimer.** The paper is "not another compression benchmark, nor a claim that compression uniformly hurts agents — our own data rule that out. It is a *controlled empirical demonstration of an evaluation blind spot*": the reacquisition cost is real, decomposable, and model-dependent — and completion-centric evaluation can miss it, even under an intervention that changes the cost sharply. It does not propose a general theory of agent evaluation; it "exhibit[s] one mechanism by which completion can under-report compression's cost, and… give[s] runtime designers a diagnostic for it."

For runtime designers, "the actionable quantity is not 'which compression ratio is safe' but 'which execution-relevant state, if dropped, would the agent spend its budget re-acquiring?'" — with externally queryable task state identified as a major source of that cost, and retention-budget results (Sec. 3.5) qualifying how much the digest's *content* — as opposed to its mere presence — is responsible for reducing it.

## Related work: the four-category map

Prior work on context compression spans four categories:

| Category | Question | Representative works |
|---|---|---|
| (i) Compression methods | How to compress better — what to keep and when to compact; optimized for agent performance | ACON; Memento; VISTA; RE-TRAC; LLMLingua |
| (ii) Recoverability evaluation | Whether information survives or can be recovered; retention as a property of the compressed artifact | Context Codec's round-trip guarantees; Reclaim's black-box recovery |
| (iii) Long-context utilization | Whether surviving information is actually used; compaction can fail through attention rather than deletion | "lost in compaction" |
| (iv) Aggregate efficiency evaluation | Completion reported with aggregate cost (tokens, latency, runtime); success alone insufficient, must be paired with cost | Less Context, Better Agents; Yehudai et al.; CostBench |

"Each of these lines evaluates what compression preserves, recovers, or achieves. None provides a diagnostic for the interaction cost that completion-centric evaluation does not expose — where the added interaction goes, and whether completion tracks it. This paper is that diagnostic: a controlled protocol, in a fixed setting, that measures the reacquisition cost and tests whether completion exposes it."

## Related work: agent evaluation metrics and the insufficiency of completion

A separate line asks what the *right metric* for an agent is. Production experience: "agents in the wild re-query tools and re-fetch already-computed state, and completion reads the final outcome, not the trajectory behind it." Formalizations of the insufficiency come from different directions:

- **Completion fallacy** (Hou et al.): completion rate compresses process-level variance;
- **Graded reliability / progress-based metrics** (Khanal et al.; AgentBoard): binary pass/fail obscures meaningful differences among failing agents;
- **Verifier Tax**: bounded-horizon outcome decomposition reveals horizon-dependent trade-offs;
- **Cost side**: the tool-calling protocol itself carries an additive accuracy tax (Zhang et al.); cost-optimal planning benchmarked through cost gaps (CostBench); cost-per-return frameworks make effectiveness–efficiency trade-offs explicit (Bogdanov et al.).

Two observations "bracket, but do not fill," the gap: these insufficiency arguments concern what completion fails to reveal about process quality or the outcome — **not** about the runtime cost of context compression; and the cost-accounting frameworks price architecture or protocol choices under an intact context, "without connecting cost to state that compression dropped." On the compression side, reacquisition cost is recognized operationally — tokens-per-task accounts for re-fetching (Factory), truncation rots recall (context-clock), token reduction does not reliably reduce billed cost (Weinberger & Hozez) — but only observationally, "without causal attribution." "None defines a black-box, model-agnostic measure of how much interaction budget an agent spends to reacquire state that generic compression removed, nor manipulates that state's availability causally. Our protocol supplies exactly this measurement (Proposition 1, Sec. 3.1)."

## Related work: closest evaluation-perspective contrasts (Table 1)

Table 1 summarizes the four closest evaluation-perspective works — none measures the interaction budget an agent spends to reacquire state that a compression operator dropped, nor manipulates state availability causally:

| Work | Measures | Manipulates | Decomposes | What completion can miss |
|---|---|---|---|---|
| **CostBench** | cost-optimal planning; cost gaps | tool costs & availability (blocking events) | cost by cost-event type | suboptimal but valid plans — we price reacquiring dropped state |
| **CompressAgent** | reliability & success vs compression level; reasoning collapse | compression failures: tool failures precede execution vs success | no causal manipulation | we add oracle attribution |
| **Token Cost Red.** | billed cost; token vs cost deltas | token reduction strategies | cost by component (cache ≈ 87%) + token savings = cost savings | provider-specific billing; we use a model-agnostic budget |
| **Tool-Use Tax** | accuracy tax of the tool protocol | tool availability (no-op / token reduction) | accuracy gap: Δcmp + Δfrc + Δsty; protocol tax swamps tool gains | accuracy over intact context; we meter cost of lost state via oracle probes |

## Related work: closest contrasts, work by work

- **Lost in Compaction** — shows compaction fails through an attention bottleneck rather than deletion (the "grep-LLM gap": keyword search finds 82–93% of facts while the LLM recalls 0–7% in the compacted zone). The present mechanism targets a distinct failure mode and is experimentally separable: "our sliding condition *deletes* old turns, so the dropped state is genuinely absent and the agent's observable response is to re-fetch it (retrieval calls increase 2–3×; execution calls do not); the oracle condition confirms this attribution by restoring state and removing much of the retrieval cost." The authors do not contest attention-dilution accounts — "they predict our observation that GPT-5.5 tolerates compression — but we isolate a second, independent cost that attention-centric accounts do not capture, because for them the text is still present. Both mechanisms can coexist; we measure the reacquisition side."
- **Context Codec** — formalizes codec-level round-trip recoverability of compressed representations; "Their recoverability is a representation property (can the encoder + decoder round-trip?); ours is a black-box agent-behavioral property (can the agent recover under a bounded budget?). Same word, different layer — complementary."
- **Reclaim Evaluation** — tests recovery of correctable state from a degraded single-carried memory ("a lossy memory is worse than an empty one"); this paper measures the *cascading reacquisition cost inside the agent loop* and manipulates recoverability directly via oracle injection.
- **Plans Don't Persist** — probes latent hidden states to show internal plans don't survive compression; "White-box probing of internal state vs our black-box observation of environment state (ERS); we make no claim about latent reasoning."
- **Memento** — compresses the KV cache within a single inference; this paper studies the cross-turn agent context — the trajectory persisting across tool calls — and the interaction budget spent re-acquiring environment state.
- **ACON** — shows failure-aware compression can match full-context performance; their target is "compression should not hurt," while this paper "reproduce[s] a near-lossless summary in our setup, and show[s] the divergence appears only when execution-relevant state is dropped (sliding), consistent with our claim that compression quality depends on which execution-relevant state is preserved."
- **VISTA** — provides lossless archival recovery of exact bytes (bulky blocks archived as external payloads with stable handles and restored on demand); this paper shows exercising such recovery "is itself a cost continuum under a hard budget: even recoverable task-graph state costs real turns to re-fetch, and that cost can become consequential for performance under a bounded interaction horizon."
- **Less Context, Better Agents** — pruning plus summarization can improve completion while cutting tokens and runtime in an enterprise tool-use workflow; their evaluation is a configuration-choice question reported on completion, tokens, and runtime jointly, alongside a failure taxonomy. This paper asks "a different question at a finer granularity: where the additional interaction goes (retrieval versus execution), and whether completion changes even when that interaction cost does. Our contribution is a decomposition and a diagnostic, not a competing configuration choice; the two are complementary."
- **CompressAgent** — independently observes the same ordering: tool-execution failures appear at milder compression, while task success collapses only under aggressive compression; where they study compression reliability at scale, this paper "isolate[s] the mechanism — state reacquisition — under a controlled budget and intervene[s] on it with oracle restoration."
- **Rate-distortion / memory surveys** — explicitly flag a gap: "agent-level repeated compaction is barely measured and no benchmark shares a budget axis across layers. We provide exactly the missing controlled experiment — operator × regime × model under a fixed interaction budget."

## Closing thesis

> Prior work on context compression asks *what to keep*, *how well compression preserves information*, *whether surviving information is used*, and *which strategy wins on the aggregate outcome*. We ask a fifth question — **what it costs the agent to re-acquire what was dropped, and whether completion metrics expose that cost** — and show that this cost can rise substantially while completion stays unchanged:

> *"Compression is not costly merely because information is lost; it becomes costly when the state that was dropped must be re-acquired through additional interaction under a bounded budget."*

**Covers:** Section 1 (Introduction), Section 2 (Related Work)
