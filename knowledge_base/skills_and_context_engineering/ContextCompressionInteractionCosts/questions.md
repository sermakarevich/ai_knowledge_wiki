---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: What Does Context Compression Cost an Agent?

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does the paper mean by saying task completion is a "non-identifying projection" of the full evaluation outcome, and what is the outcome it's a projection of?

> [!tip]- Answer
> The full evaluation outcome is a triple Y = (completion rate, retrieval tool calls, execution tool calls). Completion-only evaluation looks only at the first coordinate and discards the other two, so two conditions with very different interaction (reacquisition) costs can produce the same completion value — the projection can't distinguish them. See [[wiki/02-method|Method]].

### Q2. In the DeepSeek severity sweep, at what compression ratio does retrieval first become significantly elevated, and at what ratio does completion first become significantly worse? Why does the gap between those two points matter?

> [!tip]- Answer
> Retrieval is already significantly elevated at 5× compression (p = .002). Completion only degrades significantly at the far more aggressive 10× ratio (p = .016). The gap matters because it means the cost signal is the earlier, more sensitive warning — a system evaluated only at a shallow compression point (like 5×) would look "lossless" on completion while already paying a real, measurable reacquisition cost. See [[wiki/03-experiments-and-results|Experiments & Results]].

### Q3. The paper distinguishes D-state (externally queryable) from R-state (history-dependent). Why does losing D-state drive up retrieval calls while losing R-state does not?

> [!tip]- Answer
> D-state can in principle be recovered by re-querying the environment (e.g. re-reading a task graph), so when it's dropped the agent responds by repeatedly re-querying — a "re-query loop." R-state only ever existed in the trajectory's history; no single public query can restore it, so its absence doesn't trigger extra retrieval calls — instead it shows up (if at all) as reduced completion, since the agent proceeds under uncertainty rather than searching for something unrecoverable. See [[wiki/01-introduction-and-related-work|Introduction & Related Work]] and [[wiki/04-discussion-and-limitations|Discussion & Limitations]].

### Q4. What does the oracle intervention in Section 4.4 actually do, and what result would have falsified the paper's causal claim about D-state?

> [!tip]- Answer
> The oracle intervention takes the exact dropped state string and injects it back into the compressed context as a trailing message — separately testing D* (queryable state) and R* (history-only state) restoration. Restoring D* cuts tool calls from 72.9 to 35.8 and recovers most of the completion gap (66% → 80%). If restoring D* had left retrieval unchanged (or reduced it no more than restoring R* did), that would have falsified the claim that D-state loss specifically drives the reacquisition cost. See [[wiki/03-experiments-and-results|Experiments & Results]].

### Q5. In the retention-intervention experiments, what is the "selection null," and what result showed that content validity — not selection — is what actually matters?

> [!tip]- Answer
> The selection null is the finding that, among real task-relevant atoms, *which* ones are kept barely matters: random selection matches an offline hindsight-optimal oracle (−22.1% vs. −22.4% retrieval reduction, d ≈ 0.02). In contrast, the D-Irrelevant control — replacing real D-state atoms with fabricated out-of-universe state at the same format, position, and budget — raised retrieval by +11.5 calls (57% relative increase) over the real-content digest, even exceeding the no-digest sliding baseline, while completion stayed statistically unchanged. So fine selection is a null effect, but content validity is a large, load-bearing one. See [[wiki/03-experiments-and-results|Experiments & Results]].

### Q6. Why does the content-validity effect (real vs. fabricated D-state) disappear at the tightest digest budget (B = 100), and what does that imply for someone designing a retention budget under tight memory constraints?

> [!tip]- Answer
> At B = 100 the digest is a small enough fraction of the compacted context window that the agent leans on the recent turns instead, so real-versus-fabricated content becomes behaviorally invisible (Δ +0.6, p = .60) — the content effect is "budget-gated," only visible when the digest dominates the window. The implication for design: under a tight retention budget, prioritize keeping compact, cheap-to-retain history-dependent (R) state, since it stays fully retained at any budget and its loss is what forces defensive D re-querying — and don't expect careful curation of D content to pay off until the digest is large enough to matter. See [[wiki/03-experiments-and-results|Experiments & Results]] and [[wiki/04-discussion-and-limitations|Discussion & Limitations]].

### Q7. What did the ALFWorld probe show, and why does that result matter for how broadly the paper's central finding should be interpreted?

> [!tip]- Answer
> Running the identical sliding-window compression operator in ALFWorld (a household task environment where dropped state can typically be re-observed directly via look/examine/inventory actions) produced no retrieval-like surge at all (paired Δ ≈ −0.13, symmetric around zero) — versus a large positive surge (~+33) in IRBench. This shows the reacquisition cost is environment-dependent, not an automatic consequence of shortening context: the cost only appears when the dropped execution-relevant state cannot be cheaply reacquired through ordinary interaction. It bounds the paper's claim — compression is not intrinsically costly, only costly under specific recoverability conditions. See [[wiki/03-experiments-and-results|Experiments & Results]].

### Q8. Given the critical analysis of this paper, what is its single weakest generalizability link, and why doesn't that weakness undermine the paper's core causal claim?

> [!tip]- Answer
> The weakest link is environmental/operational narrowness: the mechanism is demonstrated in two bounded, deterministic, synthetic-adjacent environments (IRBench and one ALFWorld probe), a single shared compression ratio (5×) across two of the three models, and designed control operators rather than production compressors — so absolute magnitudes shouldn't be assumed to transfer. This doesn't undermine the core causal claim because that claim (oracle-restoration of specific dropped state reduces reacquisition cost) is a genuine controlled, causal experiment within the tested environment, independent of whether the numbers generalize elsewhere — the mechanism is real even if its magnitude in other settings is unverified. See [[critical_thinking|Critical Analysis]].
