> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Method and Theory: Unified Optimization View, Bias–Variance, and Operating Regimes
**In one sentence:** All prompt optimizers maximize the same expected task reward J(p) from execution experience, but search-based methods infer updates from noisy Monte Carlo rollouts and validation scores while CASD performs a single offline distillation from deterministic corpus-scale statistics, giving CASD lower variance and lower cost under limited budgets at the price of fixed-corpus bias that iterative search can overcome once abundant interaction is available.
## Key points
- All methods share the objective `J(p) = E[R(πθ(p), x)]` and the common update form `pt+1 = Π[pt ⊕ ρ(pt, ϕt)]`, differing only in how feedback `ϕt` is inferred.
- Search-based feedback is `ϕ_search = {(τ,r)} over batch Bt` plus validation score `r̂val(p) = mean R over Dval`, both Monte Carlo estimates with `Var[r̂val(p)] = σ²/|Dval|` that improve only via additional rollouts.
- CASD feedback is `ϕCASD = (Φ(D), {τi} for i in I(Φ))`, where corpus statistics `Φ(D)` are deterministic functions of the fixed rollout corpus, eliminating minibatch sampling variance once the corpus exists.
- The trade-off is variance versus bias: search has decreasing variance with more rollouts, while CASD aggregates the whole corpus for low variance but carries bias whenever the fixed corpus misses important behaviors.
- Offline distillation and iterative search occupy complementary regimes: CASD wins on effectiveness and cost under limited budgets, while search's lower asymptotic bias is expected to dominate as rollout data and environment interaction grow.
- Headline limited-data result (same static pool, mean over 3 seeds): CASD mean gain vs. baseline is +16.6 points, versus +10.9 for GEPA and +5.3 for SkillOpt, best on 3 of 4 benchmarks.
- A CASD pass costs ≈$1.60 per skill with no rollout bill (corpus is a byproduct), totaling 22× cheaper than SkillOpt ($142.5) and below GEPA ($8.4) over four benchmarks.
---
## 4.1 A Unified View of Prompt Optimization
Expected task reward:
`J(p) = Ex∼PX [R(πθ (p), x)]`
Common update form (Eq. 1):
`pt+1 = Π[pt ⊕ ρ(pt, ϕt)]`
where `ρ` proposes a prompt modification from execution feedback `ϕt`, `⊕` applies it, and `Π` decides acceptance.
Search-based instantiation (Eq. 2):
`ϕ_search_t = {(τ, r)} over x in Bt, r̂val(p)`, with `r̂val(p) = (1/|Dval|) Σ R(πθ(p), x)` over `x in Dval`, where `Bt` is the sampled rollout batch and `Dval` the validation set.
CASD instantiation (Eq. 3):
`ϕCASD = (Φ(D), {τi} for i in I(Φ))`, where `Φ(D)` denotes corpus statistics over fixed rollout corpus `D`, and `I(Φ)` the index set of representative trajectories selected for inspection.
**Covers:** Section 4–4.1
## 4.2 Bias–Variance Analysis
Search validation score is a Monte Carlo estimate with `Var[r̂val(p)] = σ²/|Dval|`, where `σ²` is per-episode reward variance; prompt updates come from noisy feedback whose reliability improves only through additional rollout evaluations.
Corpus statistics `Φ(D)` are deterministic functions of the observed rollout corpus, eliminating the minibatch sampling variance of repeatedly estimating feedback from sampled trajectory subsets.
Resulting positions: search uses Monte Carlo feedback with variance decreasing as rollouts accumulate; CASD reduces estimator variance by aggregating the entire corpus, at the cost of bias whenever the corpus fails to capture important behaviors.
**Covers:** Section 4.2
## 4.3 Operating Regimes
Under limited rollout budgets, reducing estimator variance is often more valuable than eliminating asymptotic bias, so CASD can simultaneously improve effectiveness at substantially lower cost by replacing iterative search with a single offline distillation step.
As rollout data and interaction grow, search variance decreases while fixed-corpus bias stays unchanged, so the offline advantage is expected to diminish and iterative search becomes increasingly attractive as its lower asymptotic bias dominates.
Verbatim framing: "offline corpus-scale reflection and iterative search occupy complementary operating regimes rather than optimizing different objectives. Offline distillation is particularly well suited to budget-constrained optimization, whereas iterative search is expected to benefit more from abundant interaction budgets."
**Covers:** Section 4.3
## 5 Experimental Setup
Benchmarks: (i) ALFWorld embodied household tasks, ReAct-style scaffold, win rate on 50 held-out games; (ii/iii) τ2-bench retail and telecom tool-using customer-service agents against an LM user simulator, pass@1 on 40 held-out tasks; (iv) SpreadsheetBench-Verified (SSB) spreadsheet manipulation, modified accuracy on 50 held-out items.
Models: target agent (and user simulator where applicable) GPT-5.4-mini with reasoning disabled (no-think); optimizer/reflection LM for all methods Claude Sonnet 5; test accuracy mean over 3 seeds with sample SD (n−1); binomial standard error alone ≈7 points per seed, so seed-level dispersion is reported (Miller 2024).
Methods: Baseline no skill, cost $0; CASD one distillation pass per skill over static-pool rollouts, 3 skills synthesized per benchmark with mean reported (SD = skill-to-skill variance); GEPA evolutionary reflective optimization; SkillOpt reflective search with validation-selection gate.
Data regimes: limited-data headline regime gives every optimizer only the same fixed pool (retail 35, telecom 50, SSB 50 tasks; 50-game ALFWorld pool; GEPA Pareto set = train, SkillOpt splits pool internally); head-to-head regime additionally gives GEPA and SkillOpt a separate held-out validation set plus unlimited environment access for candidate rollouts that CASD never uses.
Optimizer settings: GEPA budget 120 metric calls (telecom resumed to 240 calls returned a byte-identical prompt, so 120-call point reported); SkillOpt 3–5 epochs, minibatch size scaled to train split (8–40), edit budget 4 per step cosine-decayed to 2, validation gate enabled, internal split 25/10 on retail and 35/15 elsewhere for limited-data regime.
**Covers:** Section 5
## 6.1 Matched data access: one pass beats the loops
With every optimizer restricted to the same static pool, CASD is best on ALFWorld (83.3 vs. GEPA's 74.0), retail (40.0 vs. 39.2), and telecom (39.2 vs. 17.5), and second on SSB (51.3 vs. GEPA's 60.7); averaged over benchmarks CASD lifts baseline by +16.6 versus +10.9 GEPA and +5.3 SkillOpt; telecom is the sharpest separation.
Table 1 — Limited-data regime headline, held-out test accuracy (%) mean over 3 seeds (SD); ALFWorld SkillOpt uses its native scaffold (own baseline 58.7%), not directly comparable to column 2:
| Benchmark | Baseline | CASD (ours) | SkillOpt | GEPA |
|---|---|---|---|---|
| ALFWorld | 56.7±1.2 | 83.3±2.3 | 68.0±2.0 | 74.0±2.0 |
| τ2 retail | 32.5±2.5 | 40.0±2.5 | 38.3±10.1 | 39.2±7.2 |
| τ2 telecom | 19.2±5.2 | 39.2±8.0 | 25.8±3.8 | 17.5±4.3 |
| SSB-Verified | 39.3±3.1 | 51.3±3.1 | 38.7±2.3 | 60.7±3.1 |
| Mean gain vs. base | — | +16.6 | +5.3 | +10.9 |
Table 2 — Head-to-head regime in chunk (GEPA and SkillOpt add held-out validation + environment access; CASD unchanged; ALFWorld cells repeat limited-data runs):
| Benchmark | Baseline | CASD (ours) | SkillOpt | GEPA |
|---|---|---|---|---|
| ALFWorld | 56.7±1.2 | 83.3±2.3 | 68.0±2.0 | 74.0±2.0 |
| τ2 retail | 32.5±2.5 | 40.0±2.5 | 38.3±10.1 | 46.7±8.0 |
| τ2 telecom | 19.2±5.2 | 39.2±8.0 | 44.2±5.2 | 15.8±5.2 |
| SSB-Verified | 39.3±3.1 | 51.3±3.1 | 48.0±2.0 | 56.7±1.2 |
**Covers:** Section 6.1, Tables 1–2
## 6.3 Cost
A CASD pass costs ≈$1.60 per skill — one multi-tool coding-agent session, with no rollout bill because the corpus is a byproduct of already-generated rollouts; over four benchmarks this totals 22× cheaper than SkillOpt ($142.5) and below GEPA ($8.4); unlike both, it also runs where no simulator, grader, or validation split exists.
Optimized prompts shift test-time cost: e.g., on telecom, SkillOpt's prompt induces 20.1M prompt tokens over the 3-seed evaluation versus 11.9M for GEPA's — "verbose optimized prompts are not free to deploy."
**Covers:** Section 6.3 (Table 3 summarized; full table body outside this chunk)
