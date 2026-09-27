> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Regularization View of Harness Evolution
**In one sentence:** RRSI leaves the reachable harness set Ω(H) fully open to any source edit but regularizes the search trajectory through it, splitting regularization into proposal-side capacity control and selection-side survival criteria mapped to L0/L1/L2 analogies.
## Key points
- Let Ω(H) denote harnesses reachable from H by arbitrary source edits — prompts, control flow, configuration, context management, tools, skills, memory, and subagents may all be modified, added, or removed — and RRSI regularizes the trajectory, not the hypothesis space.
- At each round t the proposer generates candidate edits to Ht from finite evolve-set feedback and the selector decides which, if any, replaces the incumbent.
- Proposal regularization has three mechanisms: annealed update sparsity, evidence-aware credit assignment, and structured exploration during stalls.
- Annealed budget follows bt = bmin + (bmax − bmin) · ½(1 + cos(πt/T)) (Eq. 4), decreasing from bmax to bmin so early rounds combine coordinated changes and later rounds are sparse and attributable.
- Selection regularization is non-compensatory: a candidate must pass leakage screening, stability-aware acceptance Ŝ(H′) ≥ S★ − δ (Eq. 5), and complexity-aware acceptance before score justifies replacing the incumbent.
- Complexity-aware acceptance requires ΔC ≤ β0 + β1ΔS (Eq. 7) for gains ΔS > δ, where ΔS = Ŝ(H′) − Ŝ(Ht) and ΔC = (Ĉ(H′) − Ĉ(Ht))/Ĉ(Ht) (Eq. 6), using policy-token cost as footprint proxy with β0, β1 fixed from the evolve set.
- Structural pruning sparsifies the retained harness: components with no strictly positive measured gain over a fixed pruning window are reported as deletion targets, imitating Lasso/L1 sparsification.
---
## Reachable set and two-sided regularization
**Covers:** §3 intro–3.1 (pp. 4–5)

Let Ω(H) denote the set of harnesses reachable from H by arbitrary source edits. RRSI deliberately leaves Ω(H) open rather than restricting the hypothesis space directly, and instead regularizes the search trajectory: the proposer uses evolve-set feedback to generate edits to Ht, and the selector determines replacement of the incumbent.

| Regularization side | What it constrains | Classical analogy |
|---|---|---|
| Proposal: edit budget | Number of independently active edits in one update (cardinality) | L0-style constraint |
| Proposal: structural pruning (retained harness) | Persistently unproductive components removed → sparser structure | Lasso/L1-style sparsification |
| Selection: complexity-aware acceptance | Suppresses unchecked growth in aggregate resource footprint without requiring elimination | Ridge/L2-style shrinkage |

> "Instead of restricting this hypothesis space directly, we regularize the search trajectory through it."
> "On the proposal side, we constrain how much adaptive capacity can be exercised in a single round and where that capacity is spent. On the selection side, we constrain which empirical improvements are strong enough, efficient enough, and sufficiently free of leakage to survive."

Detailed algorithm description is deferred to Appendix C.

## Regularizing the proposal distribution
**Covers:** §3.2 (pp. 4–5)

The proposal distribution determines how aggressively search responds to evolve-set feedback; RRSI regularizes it by (1) annealing per-round update capacity, (2) evidence-aware credit assignment over the whole run, and (3) structuring where capacity is spent.

### L0-style annealed update sparsity
Unconstrained proposers bundle many unrelated modifications into one candidate, raising effective capacity, fitting feedback idiosyncrasies, and obscuring attribution. RRSI caps independently attributable edits per proposal with schedule (Eq. 4):

bt = bmin + (bmax − bmin) · ½(1 + cos(πt/T))

decreasing from bmax to bmin over a T-round run. If attributable edits are binary activity indicators, the budget bounds their cardinality — an L0-style constraint on the update, not on a fixed parameter vector; the edit pool can change across rounds and no L0-penalized objective is optimized.

### Evidence-aware credit assignment
Every evaluation is another adaptive look at the same finite evolve set, so re-testing falsified hypotheses wastes capacity (Dwork et al., 2015). RRSI logs for every evaluated candidate: modified component, hypothesis tested, source diff, score and cost changes, and acceptance. The proposer conditions on this history: rejected mechanisms remain negative evidence, successful ones retain explicit credit. With fewer edits allowed in later rounds, attribution of observed improvements becomes easier.

### Structured exploration
Search is treated as stalled when progress over the previous w rounds stays within empirical noise band δ. During a stall, a small portion of the proposal budget is reserved for components not yet exercised in the run — a diversity/entropy-regularization-like redirect of limited capacity toward underexplored mechanisms (Haarnoja et al., 2018), without changing which mechanisms the harness may contain.

## Regularizing candidate selection
**Covers:** §3.3 (pp. 5–6)

Standard harness evolution can promote the largest measured score even when it reflects leakage, stochastic variation, or costly growth. RRSI keeps the same empirical objective but requires several non-compensatory criteria before a candidate becomes permanent state.

### Leakage screening
Before full evaluation, a critic reads each candidate diff and rejects edits explicitly encoding task names, entity names, task-specific values, answers, benchmark-specific logic, or inert machinery. Generic prompt or tool-description improvements remain valid. Screening before evaluation matters because a leaking candidate never receives the inflated evolve-set score that would attract subsequent rounds.

### Stability-aware acceptance
The unchanged base harness is repeatedly evaluated before evolution to estimate noise band δ. With S★ the best evolve-set score so far, a candidate must satisfy (Eq. 5):

Ŝ(H′) ≥ S★ − δ

preventing downhill walks through individually noise-sized regressions, and making selection conservative to repeated stochastic evaluation on the same evolve set (Dwork et al., 2015).

### Ridge/L2-style complexity-aware acceptance
For candidate H′ vs. current Ht (Eq. 6):

ΔS = Ŝ(H′) − Ŝ(Ht), ΔC = (Ĉ(H′) − Ĉ(Ht))/Ĉ(Ht)

For gains above noise (ΔS > δ), require (Eq. 7):

ΔC ≤ β0 + β1ΔS

where β0 is cost increase tolerated for negligible gain and β1 controls additional allowed cost per unit improvement; both selected on the evolve set and fixed for transfer. Policy-token cost is the measurable footprint proxy. Like Ridge shrinkage, it discourages aggregate magnitude growth without requiring any component's removal. The within-noise-band rule is deferred to Appendix C.3.

### Lasso/L1-style structural pruning
The annealed budget (Eq. 4) sparsifies each update; pruning sparsifies the retained harness. RRSI tracks whether recently exercised components produced strictly positive measured gain over a fixed pruning window; persistently unproductive components become deletion targets. Qualitative Lasso correspondence: Lasso reduces parameter count via L1 regularization, while this rule deletes discrete components by observed contribution — shared intuition of selective sparsification where a mechanism must earn its place (Hastie et al., 2009).
