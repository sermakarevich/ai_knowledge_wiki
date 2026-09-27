> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Increased Test-Time Computation Rather Than Reusable Mechanisms
**In one sentence:** Recent harness-evolution methods gain from increased test-time computation rather than reusable mechanisms, so RRSI regularizes proposal and selection to close the evolve-to-transfer generalization gap.
## Key points
- Generalization is defined as an evolved harness transferring unchanged to unseen benchmarks with different task descriptions, tool interfaces, or verifiers.
- Recent works explicitly separate evolution and evaluation tasks to measure generalization (Huang et al., 2026d; Ke et al., 2026; Zhang et al., 2026d).
- Overfitting arises through three coupled behaviors: benchmark-specific fitting, noise chasing (candidates favored by evaluation noise), and complexity accumulation that improves evolve-set scores without improving the underlying mechanism.
- RRSI keeps the harness fully editable while constraining how finite evolve-set feedback guides search, regularizing both candidate proposal (simpler, reusable edits) and selection (robust criteria).
- RRSI is evaluated on eight benchmarks spanning three domains differing in task type, tooling, and verifier, evolving on one suite per domain and running unchanged on held-out benchmarks.
- RRSI gains up to 14.1 points on the evolving split and improves all six held-out splits by up to 4.7 points out of distribution, on fewer policy tokens than unregularized evolution.
- RRSI outperforms the average prior baseline by up to 22.9% across held-out environments, indicating broadly useful rather than environment-specific harness changes.
- Harness evolution is formalized as adaptive empirical optimization: propose candidates from `H_t` and feedback `F_t`, then select by empirical evolve-set score, reusing `D_evolve` adaptively across rounds.
---
## Test-time compute vs reusable mechanisms
Prior harness-evolution gains come from "increased test-time computation rather than reusable mechanisms (Ding et al., 2026; Lin et al., 2026b; Wang et al., 2026b)."

**Covers:** Introduction, generalization definition and prior separation of evolution/evaluation tasks.
## Overfitting behaviors
> "The evolution search may encode benchmark-specific patterns, promote candidates favored by the evaluation noise, or accumulate complexity that improves evolve-set scores without improving the underlying agent mechanism."

These three behaviors — benchmark-specific fitting, noise chasing, and complexity accumulation — all widen the evolve-to-transfer gap.

**Covers:** Introduction, overfitting diagnosis (cf. Yang et al., 2026a; Zhang et al., 2026d).
## RRSI framework overview
> "RRSI regularizes both sides of the evolution loop: it encourages simpler and more reusable edits when proposing candidates, and applies robust selection criteria to avoid retaining improvements driven by benchmark-specific signals, evaluation noise, or unnecessary complexity."

Key constraint: RRSI "favors edits that transfer beyond evolution set without restricting which harness components may be updated."

**Covers:** Introduction, RRSI proposal (Figure 2 preview); contributions: (1) identify overfitting, (2) regularize proposal and selection with fully editable harness, (3) improve transfer and efficiency across eight benchmarks in three domains.
## Evaluation headline numbers
| Setting | Result |
|---|---|
| Evolving split | up to +14.1 points |
| All six held-out splits | improved, up to +4.7 points out of distribution |
| Token cost | fewer policy tokens than unregularized evolution |
| Held-out environments vs average prior baseline | up to +22.9% |

> "More importantly, RRSI generalizes across held-out environments, outperforming the average prior baseline by up to 22.9%."

**Covers:** Introduction, Figure 1 (b–d) headline results.
## Preliminaries: agents and harnesses
An agent `A = (π, H)` combines backbone policy `π` with harness `H` — "everything around the weights," comprising system/task prompts, control flow (plan/act/reflect/stop), tool interfaces and descriptions, memory/skill files, and context management. A trajectory `τ ∼ A(·|x)` yields deliverable scored by verifier `r(x,τ) ∈ [0,1]` (unit-test suite or LLM-as-a-judge).

Performance and cost on task set `D`:
- `S(H;D) = E_x∼D E_τ∼A(·|x)[r(x,τ)]`
- `C(H;D) = E_x∼D E_τ∼A(·|x)[c(τ)]`, where `c(τ)` is policy tokens consumed.

**Covers:** Section 2, Preliminaries — Agents and Harnesses, Eq. (1).
## Preliminaries: harness evolution loop
Harness evolution fixes the backbone policy and optimizes `H`: at round `t`, execute `H_t` on evolve set `D_evolve`, summarize trajectories into feedback `F_t`, have a proposer LLM generate candidates, evaluate on the same evolve set, and keep the best:
- Candidate set: `H_t = {H_t^(1),...,H_t^(m_t)} ∼ P_0(·|H_t,F_t)`
- Next incumbent: `H_{t+1} = argmax Ŝ(H′;D_evolve)` over `H′ ∈ H_t ∪ {H_t}`
- Empirical estimates `Ŝ`, `Ĉ` use `k` stochastic trials per task (Eq. 3).

Because candidates at round `t` depend on measurements from the same tasks in earlier rounds, "this reuse of D_evolve is adaptive," making evolution "adaptive empirical optimization over an unusually expressive search space."

**Covers:** Section 2, Preliminaries — Harness Evolution, Eqs. (2)–(3).
## RRSI regularization principles and Figure 2
RRSI keeps the harness edit space open but regularizes movement through it, translating ML regularization into adaptive search:
- Sparse updates: limit how many mechanisms change per feedback round (annealed update sparsity — broad early, sparse attributable late).
- Evidence-aware credit assignment: use full history of gains/regressions, not just the latest win.
- Structured exploration: when stalled, redirect toward underexplored components.
- Conservative selection: leakage screening, noise-adjusted performance floor, L1-style complexity-aware acceptance, L0-style structural pruning.

> "Figure 2 | Overview of RRSI. RRSI regularizes the search trajectory, not restricting the potential harness edit space: proposal-side constraints control how search capacity is used, while selection-side constraints control which measured improvements are allowed to become a permanent state."

**Covers:** Section 3 opening through Section 3.1 heading, Figure 2 (p. 3).
**Covers:** Chunk 02-increased-test-time-computation-rather-than-reus — paper pp. 2–3, Introduction (generalization gap, RRSI, headline results) through Sec. 2 Preliminaries and Sec. 3 / Fig. 2 overview up to Sec. 3.1 heading.
