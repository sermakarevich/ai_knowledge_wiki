> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Selection Rule and Appendix Bookkeeping Details
**In one sentence:** RRSI retains the incumbent (𝐻𝑡+1 = 𝐻𝑡) when no candidate is admissible, bounding each candidate by an annealed edit-cardinality budget and admitting winners only through a stability floor plus a gain-dependent cost rule or a shaped within-band rule with structural novelty and domain guards.
## Key points
- Incumbent retention is strict: Algorithm 2 sets 𝐻𝑡+1 ← arg max over admissible set A𝑡 of 𝑆ˆ′, or 𝐻𝑡 if A𝑡 = ∅, and updates 𝑆★ ← max(𝑆★, 𝑆ˆ𝑡+1).
- Each candidate applies a subset 𝑧𝑡 ∈ {0,1}^|𝐸𝑡| of a per-round redrawn atomic-edit pool 𝐸𝑡 from Ω(𝐻𝑡), constrained by ‖𝑧𝑡‖₀ ≤ 𝑏𝑡 (Eq. 9), a cardinality constraint on the update rather than an 𝐿₀ penalty.
- History is per-edit: L𝑡 = {(𝑡𝑖, ℓ𝑖, ℎ𝑖, 𝑑𝑖, Δ𝑆𝑖, Δ𝐶𝑖, 𝑎𝑖)}, 𝑎𝑖 ∈ {0,1}, where 𝑎𝑖 = 1 iff the carrying candidate won its round; admissible losers get 𝑎𝑖 = 0, and candidates failing before valid measurement are ignored.
- Exploration and pruning are explicit inputs: E𝑡 = (𝜎𝑡, U𝑡, 𝑚draft) with stall flag 𝜎𝑡 = 𝟙[𝑆ˆ𝑡 − 𝑆ˆ𝑡−𝑤 ≤ 𝛿] and unexplored set U𝑡 = K \ T𝑡, while B𝑡 = {ℓ ∈ T𝑡 : 𝑔𝑡(ℓ) ≤ 0} marks components with no strictly positive gain in the pruning window for Lasso/𝐿₁-style deletion.
- Selection first enforces the noise-adjusted floor 𝑆ˆ(𝐻′) ≥ 𝑆★ − 𝛿, which permits within-tolerance fluctuation while blocking accumulation of small regressions.
- The acceptance branch splits on measured gain: for Δ𝑆 > 𝛿 the gain-dependent cost rule Δ𝐶 ≤ 𝛽₀ + 𝛽₁Δ𝑆 applies (Ridge/𝐿₂-style analogy), and for Δ𝑆 ≤ 𝛿 the shaped rule 𝑤𝑠Δ𝑆 − 𝑤𝑐Δ𝐶 + 𝑤𝑛𝜈𝑡(𝐻′) > 0 applies, with the coding instance fixing 𝑤𝑠 = 0 so within-band score gain alone cannot admit a candidate.
- Structural novelty counts only new structural types: 𝜈𝑡(𝐻′) = Σ 𝟙[ℓ ∈ comp(𝐻′) ∧ 𝑁𝑡(ℓ) = 0] over Kstr = {client_tool, skill, memory, subagent}, excluding prompt, control-flow, config, output-plumbing, and context-management edits.
- Only the engineering-design instance adds domain guards (𝑔 = 1 for coding and agentic-workspace): reject if valid-output rate falls by more than 0.03 or no-submission rate rises by more than 0.02 relative to the incumbent.
---
## Run setup and retention rule
A run applies Algorithms 1 and 2 for 𝑡 = 0, …, 𝑇 − 1, starting from 𝐻₀ with 𝑆★ = 𝑆ˆ(𝐻₀). Before evolution, the unchanged base harness is evaluated repeatedly to estimate the empirical noise tolerance 𝛿. Algorithm 2, line 16:

| Step | Rule |
|---|---|
| Build admissible set | A𝑡 ← A𝑡 ∪ {𝐻′} only if 𝑆ˆ′ ≥ 𝑆★ − 𝛿 and 𝑐 and 𝑔 (cost check 𝑐, domain guard 𝑔) |
| Retention | 𝐻𝑡+1 ← arg max_{𝐻′ ∈ A𝑡} 𝑆ˆ′, or 𝐻𝑡 if A𝑡 = ∅ |
| Best tracking | 𝑆★ ← max(𝑆★, 𝑆ˆ𝑡+1) |
| Credit assignment | Record each measured edit with 𝑎 = 1 iff its candidate is 𝐻𝑡+1 ≠ 𝐻𝑡 |

Round inputs named in the chunk: F𝑡 is feedback from the current round, L𝑡 is the edit history, 𝑏𝑡 is the annealed edit budget from Equation (4), E𝑡 contains exploration directives, B𝑡 contains structural pruning targets inferred from recent history, and A𝑡 is the set of candidates allowed to replace the incumbent.

**Covers:** run setup, retention rule (Algorithm 2, lines 12–19)

## C.2 Proposal-side bookkeeping — atomic edits and Algorithm 1
At round 𝑡 the proposer drafts a pool 𝐸𝑡 of atomic edits to 𝐻𝑡; a candidate applies subset 𝑧𝑡 with 𝑧𝑡,𝑗 = 1 when edit 𝑗 is included. The pool is redrawn each round from Ω(𝐻𝑡), so |𝐸𝑡| need not be fixed. The annealed budget imposes ‖𝑧𝑡‖₀ ≤ 𝑏𝑡 (9). The chunk states this "limits the number of independently attributable edits bundled into one candidate rather than the set of components that may eventually be modified" and calls it "a cardinality constraint on the update, not an 𝐿₀ penalty on a fixed model parameter vector."

Algorithm 1 (RRSI, proposal side; requires 𝐻𝑡, L𝑡, round 𝑡 of 𝑇; 𝑏min, 𝑏max, stall window 𝑤, noise band 𝛿):

| Line | Operation |
|---|---|
| 1 | F𝑡 ← Analyze(𝐻𝑡, Devolve) |
| 2 | 𝑏𝑡 ← 𝑏min + (𝑏max − 𝑏min)·½(1 + cos π𝑡/𝑇) — 𝐿₀-style edit-cardinality control |
| 3 | 𝜎𝑡 ← 𝟙[𝑆ˆ𝑡 − 𝑆ˆ𝑡−𝑤 ≤ 𝛿] |
| 4 | T𝑡 ← {ℓ𝑖 : (𝑡𝑖, ℓ𝑖, …) ∈ L𝑡} |
| 5 | U𝑡 ← K \ T𝑡 |
| 6 | E𝑡 ← (𝜎𝑡, U𝑡, 𝑚draft) |
| 7 | B𝑡 ← {ℓ ∈ T𝑡 : 𝑔𝑡(ℓ) ≤ 0} — Lasso/𝐿₁-style pruning targets |
| 8 | H𝑡 ∼ 𝑃reg(· \| 𝐻𝑡, F𝑡, L𝑡, 𝑏𝑡, E𝑡, B𝑡) |
| 9 | Tag each atomic edit with component and hypothesis metadata |
| 10 | Return candidates that pass the pre-evaluation screen |

**Covers:** C.2 atomic edit representation, Eq. (9), Algorithm 1

## C.2 Edit history and component summaries
Every atomic edit in an evaluated candidate is tagged with a component ℓ, a hypothesis ℎ, and the candidate source diff 𝑑. A multi-edit candidate contributes one history record per edit; all edits in that candidate share the same measured Δ𝑆, Δ𝐶, and round outcome:

L𝑡 = {(𝑡𝑖, ℓ𝑖, ℎ𝑖, 𝑑𝑖, Δ𝑆𝑖, Δ𝐶𝑖, 𝑎𝑖) : 𝑖 ≤ 𝑛𝑡}, 𝑎𝑖 ∈ {0,1} (10)

where 𝑎𝑖 = 1 iff the carrying candidate was the round winner on the accepted evolution path. Two proposer summaries:

T𝑡 = {ℓ𝑖 : 𝑖 ≤ 𝑛𝑡}, 𝑔𝑡(ℓ) = max{Δ𝑆𝑖 : ℓ𝑖 = ℓ, 𝑡 − 𝑡𝑖 ≤ 𝑛prune}, max ∅ = −∞ (11)

T𝑡 is components with at least one measured edit; 𝑔𝑡(ℓ) is the best recent measured gain for ℓ over the pruning window. The chunk notes "this evidence becomes more attributable as the edit budget anneals toward one" because bundled edits inherit candidate-level measurements.

**Covers:** C.2 edit history, Eqs. (10)–(11)

## C.2 Exploration directives and pruning targets
Editable component vocabulary (Eq. 12):

| Symbol | Members |
|---|---|
| K (9 items) | prompt, control_flow, config, output_plumbing, context_mgmt, client_tool, skill, memory, subagent |

Exploration directive (Eq. 13): E𝑡 = (𝜎𝑡, U𝑡, 𝑚draft), 𝜎𝑡 = 𝟙[𝑆ˆ𝑡 − 𝑆ˆ𝑡−𝑤 ≤ 𝛿], U𝑡 = K \ T𝑡, where 𝜎𝑡 flags stalled progress over 𝑤 rounds within 𝛿, U𝑡 holds components without a measured edit, and 𝑚draft reserves candidate slots for exploratory edits when stalled. Pruning target set (Eq. 14): B𝑡 = {ℓ ∈ T𝑡 : 𝑔𝑡(ℓ) ≤ 0} — exercised but with no strictly positive measured gain in the recent window; the proposer receives B𝑡 plus previously accepted edits on those components with instructions to remove unproductive machinery. The chunk stresses this "is analogous in role to Lasso/𝐿₁-style sparsification because the mechanism acts by deleting discrete structure" and "is not an 𝐿₁-penalized continuous optimization problem."

**Covers:** C.2 exploration and pruning, Eqs. (12)–(14)

## C.3 Selection-side bookkeeping — floor, novelty, and acceptance branches
Noise-adjusted floor (from Eq. 5): 𝑆ˆ(𝐻′) ≥ 𝑆★ − 𝛿, applied after the leakage critic and before full evaluation. Novelty uses only structural components: Kstr = {client_tool, skill, memory, subagent} (15); with 𝑁𝑡(ℓ) the count of previously accepted records for ℓ before round 𝑡 and comp(𝐻′) the touched component types, 𝜈𝑡(𝐻′) = Σ_{ℓ ∈ Kstr} 𝟙[ℓ ∈ comp(𝐻′) ∧ 𝑁𝑡(ℓ) = 0] (16) — the count of distinct structural types touched that never appeared in a winning edit.

Algorithm 2 (RRSI, selection side; requires screened H𝑡, (𝐻𝑡, 𝑆ˆ𝑡, 𝐶ˆ𝑡), 𝑆★, 𝛿, 𝑘; 𝛽₀, 𝛽₁, 𝑤𝑠, 𝑤𝑐, 𝑤𝑛):

| Line | Operation |
|---|---|
| 2–5 | For each 𝐻′ in parallel: 𝑆ˆ′, 𝐶ˆ′ ← Evaluate(𝐻′, Devolve, 𝑘); Δ𝑆 ← 𝑆ˆ′ − 𝑆ˆ𝑡; Δ𝐶 ← (𝐶ˆ′ − 𝐶ˆ𝑡)/𝐶ˆ𝑡; 𝜈 ← 𝜈𝑡(𝐻′) |
| 6–7 | If Δ𝑆 > 𝛿: 𝑐 ← [Δ𝐶 ≤ 𝛽₀ + 𝛽₁Δ𝑆] (gain-dependent cost rule, Eq. 7) |
| 8–9 | Else: 𝑐 ← [𝑤𝑠Δ𝑆 − 𝑤𝑐Δ𝐶 + 𝑤𝑛𝜈 > 0] (within-band rule, Eq. 17) |
| 11–14 | 𝑔 ← DomainGuard(𝐻𝑡, 𝐻′); if 𝑆ˆ′ ≥ 𝑆★ − 𝛿 and 𝑐 and 𝑔 then A𝑡 ← A𝑡 ∪ {𝐻′} |

For Δ𝑆 > 𝛿 the rule Δ𝐶 ≤ 𝛽₀ + 𝛽₁Δ𝑆 "allows more inference cost only when accompanied by a larger measured improvement"; the Ridge/𝐿₂-style analogy "is functional rather than mathematical" and "is not a squared-norm penalty." For Δ𝑆 ≤ 𝛿 the shaped condition is 𝑤𝑠Δ𝑆 − 𝑤𝑐Δ𝐶 + 𝑤𝑛𝜈𝑡(𝐻′) > 0 (17) with 𝑤𝑠, 𝑤𝑐, 𝑤𝑛 ≥ 0 fixed per evolution instance (reported in Table 5); cost reduction helps via −𝑤𝑐Δ𝐶 and untried structural mechanisms help via 𝑤𝑛𝜈𝑡. The coding instance sets 𝑤𝑠 = 0; agentic-workspace and engineering-design use positive 𝑤𝑠. Equation (17) "is an implementation-level tie-breaking/admissibility rule inside the uncertainty region" and "is not itself identified with an 𝐿𝑝 penalty."

**Covers:** C.3 floor, novelty, acceptance branches, Eqs. (5), (7), (15)–(17), Algorithm 2, Table 5 reference

## C.3 Domain-specific guards
After stability and cost checks, guard 𝑔(𝐻𝑡, 𝐻′) ∈ {0,1} may apply: coding and agentic-workspace instances use no additional guard (𝑔 = 1); engineering-design additionally rejects a candidate if its valid-output rate falls by more than 0.03 relative to the incumbent or its no-submission rate rises by more than 0.02. Purpose as stated: "to prevent a gain in the primary pass-rate objective from compensating for a substantial degradation in basic execution validity."

**Covers:** C.3 domain guards (coding / agentic-workspace 𝑔 = 1; engineering-design 0.03 / 0.02 thresholds)

**Covers:** chunk 08-with-1-if-no, Appendix C.2–C.3, Algorithms 1–2, Eqs. (9)–(17), pp. 19–21
