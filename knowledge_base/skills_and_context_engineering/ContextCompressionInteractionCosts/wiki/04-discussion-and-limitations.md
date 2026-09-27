> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Discussion & Limitations

**In one sentence:** Context compression has a real, decomposable interaction cost that lives in retrieval (reacquisition of dropped state) rather than in task completion, and this cost appears only under specific model–regime–environment boundaries that completion-only evaluation misses.

## Key points

- Across the six model–regime cells, retrieval increases are significant in five of six after Holm correction, while completion changes are not significant in any cell; GPT-5.5 is the sharpest case — completion statistically unchanged (p = 1.0) while retrieval roughly triples.
- Restoring the externally queryable task graph (D*) removes most of the compensatory retrieval (Sliding 72.9 → 35.8 tool calls, −51%; paired p = .002) and recovers most of the completion gap (66% → 80%); restoring history-dependent state (R*) improves completion (+12 pp) but leaves retrieval nearly unchanged (72.9 → 69.0, −5%; n.s.).
- The added retrieval under compression is dominated by D-reacquisition: D is queryable, so the agent can only recover it by re-querying (the "re-query loop"), while R is history-dependent — no single public query restores it, so the agent proceeds under uncertainty with no retrieval growth.
- Retention matters at the level of validity, not fine selection: within the D-state pool, random selection matches an offline hindsight oracle (Δ+ 0.10 retrieval calls, CI [−2.3, +2.3]), while replacing D atoms with semantically irrelevant state raises retrieval by 57% with completion statistically unchanged.
- The content effect is budget-gated — visible only when the digest dominates the compacted window — so recency is a competitive approximation to recoverability-aware retention under tight budgets.
- In ALFWorld (Sec. 4.7), sliding compression produces no retrieval surge at all — the state can be re-observed directly — so the *presence* of the cost is conditional on what execution-relevant state becomes unavailable, not on context shortening per se.
- Seed-level analysis: the per-seed association between ΔC_R and ΔQ is negative in all three High-regime cells; GPT-5.5 High is the only nominally significant cell (ρ = −0.64, p = .045, bootstrap CI [−0.84, −0.18]).
- Limitations include: only two bounded synthetic-adjacent environments (IRBench, ALFWorld probe), three model families (DeepSeek, Qwen, GPT-5.5) with one shared compression ratio (5×), a deliberately bounded 24-turn horizon, tool-level (not intention-level) retrieval/execution decomposition, only two operators, 10-seed statistical power, and the selection null and content effect confirmed on only a subset of models.

---

## 5.1 — What the protocol measures, and why the metric matters

The protocol decomposes the interaction cost of compression into **state reacquisition (retrieval)** and **task work (execution)**. The headline observation: **task completion is an incomplete measure of this cost.** Across the six cells, retrieval increases are significant in five of six after Holm correction, while completion changes are not significant in any cell. GPT-5.5 illustrates this most sharply — completion statistically unchanged (p = 1.0) while retrieval roughly triples.

Completion is not useless: it becomes a meaningful signal when reacquisition consumes enough of the interaction horizon to limit task progress (as for DeepSeek under high compression). Used alone, it under-states compression's cost on robust models and over-states it on fragile ones. The authors explicitly disclaim that this is an argument that compression "hurts" agents (their own data rule that out); rather, the cost is real, decomposable, and visible in tool behavior before (or without) any change in completion.

Mechanism: under compression, the agent shifts where it spends its budget — the dominant shift is toward retrieval rather than execution, and that reacquisition is what the completion signal can miss.

## 5.2 — Retention versus reacquisition: two separable sources of degradation

The Sliding-vs-Summary contrast isolates the lever: with the same budget, the operator that preserves observed state facts is near-lossless, while the one that drops them degrades completion and triples retrieval. This separates **retention** (does the compressed artifact still contain the state?) from **reacquisition** (what does the agent do when it does not?). The two are complementary to the attention-centric "lost-in-compaction" account: that line shows surviving text can be ignored; this work shows *absent* state must be re-fetched, at a budget cost independent of attention. Runtime optimizations targeting one source of degradation will not address the other.

**Why is reacquisition cost dominated by retrieval?** The oracle intervention (Sec. 4.4) isolates the mechanism:

- Restoring the externally queryable task graph (**D\**) removes most of the compensatory retrieval (Sliding **72.9 → 35.8** tool calls, **−51%**; paired **p = .002**) and recovers most of the completion gap (**66% → 80%**).
- Restoring history-dependent state (**R\**) improves completion (**+12 pp**) but leaves retrieval nearly unchanged (**72.9 → 69.0, −5%; n.s.**).

The asymmetry follows from the environment's recoverability structure (Sec. 3.3): **D is queryable** — a query restores it — so when it is lost the agent recovers it only by re-querying the environment (documented in production agent systems as *redundant retrieval* or *retrieval thrashing*). **R is history-dependent** — no single public query restores it — so when it is lost the agent proceeds under uncertainty and measured retrieval cost does not grow. The data are consistent: the added retrieval under compression is almost entirely D-reacquisition, while completion depends on both state classes (both D* and R* restore most of the completion gap). The pattern is described as a *re-query loop*; the authors do not claim to observe the agent's internal decision process.

**Where in the loop a retention decision bites** — the retention interventions (Sec. 4.6) give a two-layered answer separating two notions retention policies usually conflate:

- *Within the D-state pool*, which real atoms are retained has little measurable marginal effect: random selection matches an offline hindsight oracle (Δ+ **0.10** retrieval calls, CI **[−2.3, +2.3]**) within a small budget of the best possible selection, because externally queryable atoms are homogeneous in reacquisition cost.
- *Whether the retained content is valid and task-relevant* does matter: replacing D atoms with semantically irrelevant state raises retrieval by **57%** while completion stays statistically unchanged. State content is *behaviorally load-bearing* — the agent does not treat the digest as an inert anchor — but selection granularity works only coarsely (valid vs. not), not finely (which valid atom).
- The effect is **budget-gated**: visible only when the digest dominates the compacted window — so recency is a competitive approximation to recoverability-aware retention when budgets are tight.

Taken together, the four findings form a hierarchy: **state absence** (strong: dropping state inflates reacquisition) > **valid content** (strong: irrelevant content raises cost 57%) > **fine selection** (weak: bounded near zero) > **effect visibility** (budget-gated). A retention decision is consequential at the level of validity and presence, not fine-grained ranking, in this regime.

Two explanations for the selection null are compatible with the data: (a) D atoms are homogeneous — each recoverable by a single public query at comparable cost — so any real subset with equal coverage has equal reacquisition value; or (b) the agent does not exploit fine-grained differences within a short horizon. The D-Irrelevant result favors (a): at B = 265 the agent demonstrably reacts to the digest's D content (re-queries more when content is fake), so it is content-sensitive and within-class flatness is better attributed to D-atom homogeneity.

## 5.3 — Implication for runtime design

For a runtime designer, the actionable question is not "which compression ratio is safe" but **"which execution-relevant state, if dropped, would the agent spend its budget re-acquiring?"** The oracle results point to a concrete answer: externally queryable task state (task graph and constraints) is a major source of reacquisition cost, and restoring it removes roughly half the retrieval overhead. The retention interventions qualify how to act:

- Preserving **history-dependent state (R)** is strongly favored when the retention budget is tight — it is compact enough to retain fully at any budget, and dropping it is what inflates defensive re-querying of D.
- Within the remaining D budget, fine-grained ranking buys little in this setting; what matters is that the retained content is **real and task-relevant**.
- Because the content effect is budget-gated, **recency is a competitive approximation** to recoverability-aware retention under tight budgets — stated for this setting, not as a general law.

**A practical deployment checklist** (the protocol is not tied to the paper's environment):

1. Hold the agent, task instance, and interaction horizon fixed;
2. Record completion and interaction cost jointly;
3. Where tool semantics permit, decompose interaction cost into retrieval and execution;
4. Where causal attribution is needed, restore the specific dropped state as a control;
5. Report the capability outcome and the interaction overhead together.

This connects to Proposition 1: a strategy that preserves completion but substantially increases reacquisition cost should not be treated as equivalent to the baseline solely on completion metrics.

## 5.4 — The boundary: model, regime, and environment dependence

The reacquisition pattern is consistent across the three models; its **conversion into reduced completion is not** (Fig. 3). The authors read this as a feature: the cost of compression is a property of the *agent–environment interaction*, while whether that cost becomes failure is a property of the *model's* interaction pattern and the *task's* recoverability. Completion-only evaluations may give a distorted view of cost, depending on how readily the model absorbs the extra interaction. The two-axis result (Fig. 3a): interaction cost and task completion are related but *not interchangeable* outcomes, so a cost-level diagnostic is needed to separate the two.

The environment adds a **third boundary axis** (Sec. 4.7): in ALFWorld, where the relevant state can be re-observed directly through available interaction actions, sliding compression produces **no retrieval surge at all** — the cost signal is not an intrinsic consequence of shortening context. The *presence* of the cost, not only its magnitude, is conditional on what execution-relevant state becomes unavailable and how it can be reacquired. A complete account spans three boundary conditions — model, task regime, and environment recoverability — and completion-only evaluation can miss the cost on all three.

## 5.5 — Relation to the broader literature

The work connects to four lines: (1) methods that report cost as a byproduct (this work decomposes it); (2) recoverability frameworks that treat it as a representation property (this work measures it behaviorally, under a budget); (3) attention-dilution accounts (this work isolates a distinct, absent-state failure mode); and (4) aggregate efficiency evaluation (this work asks a finer question: where the additional interaction goes, and whether completion exposes it). The rate-distortion surveys' named gap — no shared budget axis across layers — is precisely where the operator × regime × model matrix sits. The authors do not claim context compression is intrinsically harmful or beneficial; they characterize the interaction cost it introduces and the conditions under which that cost becomes consequential.

## Section 6 — Limitations

1. **Two bounded environments, both synthetic-adjacent.** Core mechanism measured in IRBench (synthetic constraint-planning, two regimes); the ALFWorld probe (Sec. 4.7) shows the reacquisition signature is environment-dependent. No claim that specific cost magnitudes transfer to open-ended tasks; future work should probe partially-observable, long-horizon environments (e.g., WebArena, SWE-bench). The value is the *protocol* and the *decomposition*, which are environment-agnostic.
2. **Three models** (DeepSeek, Qwen, GPT-5.5), not exhaustive; cross-model comparisons are descriptive rather than paired; absolute tool/token counts across providers are not interpreted (serving conditions not fully comparable).
3. **The 24-turn horizon is a design choice** — real agents always operate under a bounded budget; a metric insensitive to a large interaction-cost increase *within* that budget is a structural limitation of the metric, not "not waiting long enough." A different horizon could shift where the cost–failure conversion falls — it is reported as regime-dependent, not universal. The D-Irrelevant intervention (Sec. 4.6) changes cost sharply (and even raised completion directionally) within the same horizon — the completion signal did not expose the cost difference. A horizon sweep is left to future work.
4. **Tool-call count is a proxy for "cost"** — deliberately the budgeted interaction currency (turns, tool calls), not provider-dependent wall-clock latency or dollar cost, which would obscure the structural reacquisition signal.
5. **The retrieval/execution decomposition is tool-level** — each call is attributed to a schema, not a semantic intention (oracle results mitigate); per-message intention analysis is out of scope. Turn-level temporal analysis of when retrieval bursts occur was infeasible: per-run tool-call logs were aggregated to condition-level totals before storage.
6. **The extractive summary is the designed control, not a generic summarizer** — its near-losslessness at 5× is a property of the fact-preserving digest; not evidence that arbitrary LLM summarizers are lossless.
7. **Statistical power at 10 seeds** — the absence of significant completion changes at the pre-specified 5× point is part of the finding: completion is less sensitive to compression than the retrieval signal (significant in five of six cells after Holm). Pre-registered primary comparisons and Holm correction limit multiple-comparison risk; completion-side numbers are noisier.
8. **Single cross-model compression point** — the three-model matrix evaluates one ratio (5×), fixed in the original design; only DeepSeek has a full severity sweep (Sec. 4.2), including the 10× point where DeepSeek completion first becomes significant.
9. **Two operators** — a dropping operator (sliding window) and a fact-preserving extractive summary; patterns of LLM-generated abstractive summaries and token-level compressors remain uncharacterized; specific magnitudes are not claimed to generalize.
10. **The D-Irrelevant fabrication is one kind of irrelevance** — it replaces D atoms with fabricated out-of-universe entities the agent can detect as non-existent, so added retrieval could reflect verification of inconsistent content as well as semantic irrelevance per se; a finer "incorrect values on real entities" control is left to future work. Not claimed specific to "semantically irrelevant" state as opposed to any corrupt content.
11. **The selection null and content replication are each confirmed on a subset of models** — selection null (Random ≈ Hindsight) and coverage dose-response measured on DeepSeek only; the GPT-5.5 subset replicates the content intervention (Sec. 4.6.4) but does not re-run the selection controls, so the selection null is not claimed cross-model. The content effect is confirmed on two models (DeepSeek, GPT-5.5) at the loose budget; its magnitude and budget-gating remain model-specific.

## Appendix A — Seed-level association

Question: within each model–regime cell, is the per-seed cost increase associated with the per-seed completion change? For each of the six cells, per seed at 5×, the authors computed the paired change in retrieval calls (ΔC_R = C_R(Sliding) − C_R(Full)) and completion (ΔQ, pp), and the Spearman correlation:

| Model | Regime | ρ | p | 95% bootstrap CI |
|---|---|---|---|---|
| DeepSeek | High | −0.40 | .25 | [−0.97, +0.49] |
| DeepSeek | Low | — | — | completion invariant across seeds |
| Qwen | High | −0.32 | .37 | [−0.75, +0.29] |
| Qwen | Low | +0.16 | .67 | — |
| GPT-5.5 | High | −0.64 | .045 | [−0.84, −0.18] |
| GPT-5.5 | Low | — | — | completion invariant across seeds |

The direction is **negative in all three High-regime cells**, and **GPT-5.5 High reaches nominal significance** (ρ = −0.64, p = .045) with a bootstrap CI excluding zero: seeds with larger retrieval increases tend to show larger completion decreases, consistent with reacquisition consuming the interaction budget. The two Low-regime cells are undefined because completion is invariant across seeds (every seed completes all tasks in both conditions).

Caveats: these are exploratory, descriptive within-seed associations, not causal estimates; with n = 10 per cell and multiple comparisons, the single significant cell should be read cautiously. Model–regime cells are **not pooled** — cross-cell heterogeneity in baseline difficulty and model response makes a pooled association difficult to interpret. The negative High-regime direction is consistent with — but does not establish — the re-query loop account of Sec. 5.

## Acknowledgments & References

Acknowledgments note that portions of the manuscript (language translation and polishing) were developed with the assistance of AI language models, while all experimental design, implementation, data collection, and analysis were conducted independently by the author. The References list (24 entries: ACON, LLMLingua, rate-distortion frameworks, agent-evaluation surveys, context management, and related 2024–2026 work) is omitted from this wiki page.

**Covers:** Section 5 (Discussion), Section 6 (Limitations), Appendix A (Seed-level association)
