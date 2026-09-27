> [[index|Wiki]] | [[summary|Summary]]

# Coding Agents are Strong Prompt Optimizers — Digest

## 1. [[wiki/01-casd-overview|Coding Agents are Strong Prompt Optimizers (CASD overview)]]

**In one sentence:** A single offline pass in which an unmodified coding agent analyzes a static corpus of agent trajectories with executable code and distills the findings into a skill file used directly as the optimized system prompt outperforms iterative search-based prompt optimizers while costing about $1.60 with no environment access or validation data.

## Key points

- Coding-Agent Skill Distillation (CASD) replaces iterative search with a single offline analysis pass over a static corpus of agent trajectories using an off-the-shelf, unmodified coding agent.
- The recipe is deliberately simple: give the coding agent the rollout corpus plus a short natural-language instruction, then use the generated skill file directly as the optimized system prompt.
- CASD requires no optimization loop, validation gate, environment interaction, or held-out validation set, and producing an optimized prompt costs approximately $1.60 — over 22× cheaper than validation-gated search.
- Under matched data access across four agentic benchmarks (ALFWorld, τ-bench retail and telecom, SpreadsheetBench-Verified), a single CASD pass outperforms GEPA on three of four benchmarks and validation-gated reflective search (SkillOpt) on all four.
- Average gain over the unoptimized baseline is 16.6 percentage points for CASD versus 10.9 for GEPA and 5.3 for SkillOpt.
- Even when competing methods are granted additional validation data and unrestricted environment access, CASD remains ahead on two of four benchmarks.
- The key insight is reflection scope: instead of reasoning over a small batch of trajectories per optimization step, the coding agent writes and executes analysis code to compute corpus-wide statistics, identifies systematic failure modes, inspects representative episodes, and distills insights into behavioral rules.

## 2. [[wiki/02-head-to-head-results|Head-to-Head Results and Unrestricted Environment Access]]

**In one sentence:** Despite baselines using extra validation and unrestricted environment access that CASD never uses, CASD remains competitive and outperforms them on two of four benchmarks via a single offline corpus-analysis pass with an unmodified coding agent.

## Key points

- CASD remains competitive against baselines that use extra validation and unrestricted environment access it never uses, outperforming them on 2 of 4 benchmarks.
- CASD replaces iterative validation-gated search with a single offline corpus-analysis pass using an unmodified off-the-shelf coding agent, with no validation loops or additional environment interaction during optimization.
- Reflection scope is a design dimension: expanding reflection from sampled trajectories to corpus-scale analysis can replace iterative validation-gated search.
- Offline goal is formalized as `p* = CASD(D, p0)` from frozen corpus `D = {τi}` alone, without collecting additional trajectories or interacting with the environment.
- Distillation behavior over 24 runs totals 816 tool calls (94 exploring layout, 184 computing statistics, 510 inspecting episodes, 28 writing skill), mean 34.0 calls/run (range 16–51) producing a 5–8 KB skill file.
- Workflow is explore-first then statistics-guided investigation: 34% of calls in first fifth of run and only 5% thereafter (exploration median position 0.0), writing terminal (median 1.0), with median 5 switches between statistics and inspection (up to 16).
- Analysis code computes corpus-level statistics in every run for rewards/pass rates and episode lengths, 96% for termination/failure modes, 92% for tool usage, 79% by task category, and one-third for duplicated tool invocations.
- Resulting skills are evidence-grounded: 12 CASD skills contain 54 quantitative citations (4.6 per 1k words) versus none across 4 GEPA prompts and one across 4 SkillOpt prompts.

## 3. [[wiki/03-method-and-theory|Method and Theory: Unified Optimization View, Bias–Variance, and Operating Regimes]]

**In one sentence:** All prompt optimizers maximize the same expected task reward J(p) from execution experience, but search-based methods infer updates from noisy Monte Carlo rollouts and validation scores while CASD performs a single offline distillation from deterministic corpus-scale statistics, giving CASD lower variance and lower cost under limited budgets at the price of fixed-corpus bias that iterative search can overcome once abundant interaction is available.

## Key points

- All methods share the objective `J(p) = E[R(πθ(p), x)]` and the common update form `pt+1 = Π[pt ⊕ ρ(pt, ϕt)]`, differing only in how feedback `ϕt` is inferred.
- Search-based feedback is `ϕ_search = {(τ,r)} over batch Bt` plus validation score `r̂val(p) = mean R over Dval`, both Monte Carlo estimates with `Var[r̂val(p)] = σ²/|Dval|` that improve only via additional rollouts.
- CASD feedback is `ϕCASD = (Φ(D), {τi} for i in I(Φ))`, where corpus statistics `Φ(D)` are deterministic functions of the fixed rollout corpus, eliminating minibatch sampling variance once the corpus exists.
- The trade-off is variance versus bias: search has decreasing variance with more rollouts, while CASD aggregates the whole corpus for low variance but carries bias whenever the fixed corpus misses important behaviors.
- Offline distillation and iterative search occupy complementary regimes: CASD wins on effectiveness and cost under limited budgets, while search's lower asymptotic bias is expected to dominate as rollout data and environment interaction grow.
- Headline limited-data result (same static pool, mean over 3 seeds): CASD mean gain vs. baseline is +16.6 points, versus +10.9 for GEPA and +5.3 for SkillOpt, best on 3 of 4 benchmarks.
- A CASD pass costs ≈$1.60 per skill with no rollout bill (corpus is a byproduct), totaling 22× cheaper than SkillOpt ($142.5) and below GEPA ($8.4) over four benchmarks.

## 4. [[wiki/04-why-corpus-scope-wins|6.4 Why does corpus-scope reflection win?]]

**In one sentence:** Corpus-scope reflection wins because it writes statistical rules from the whole rollout pool — frequency-counted errors, cross-episode duplicates, and corpus-level absences — in a single gateless pass that avoids validation-gate overfitting.

## Key points

- The chunk's explanation is reflection scope: three observations support that corpus-wide statistics, not minibatch anecdotes, explain the win.
- Statistical, not anecdotal rules: the telecom skill's top rule targets fabricated identity-lookup arguments seen in 16/50 episodes (32% frequency), which no single-minibatch reflection reliably surfaces and GEPA's telecom prompts never address.
- Efficiency rules need duplicate counts: detecting that 123 of 284 `get_details_by_id` calls were exact duplicates requires joining tool calls across the whole episode set — a one-liner in pandas but invisible in context-window reflection.
- No gate, no gate-overfitting: search methods keep an edit only if a small validation batch approves, which overfits small pools and inflates variance.
- The overfitting cost is concrete: GEPA-telecom-LD collapses to 17.5, SkillOpt retail variance reaches SD 10.1, while CASD's single pass has no acceptance step and variance across independently produced skills is small (SD ≤ 3.1 on 3 of 4 benchmarks).
- Figure 4 mechanism: a single test ticket has two independent root causes and reward is granted only if the target agent repairs both.
- The device-side cause is visible in any individual failed trajectory and all three optimizers encode a rule for it; the account-side cause appears only as an absence — a payment call no rollout ever makes — so only CASD writes a rule for it and only CASD solves the episode.

## 5. [[wiki/05-reasoning-gap-ablation|Table 4: Recovering the reasoning gap]]

**In one sentence:** A no-think policy plus the distilled skill recovers most or all of the no-think→think accuracy gap with zero reasoning tokens, and failure-rich no-think rollouts alone suffice as the distillation corpus.

## Key points

- On ALFWorld, no-think + CASD skill reaches 83.3 vs 71.3±1.2 for think mode, recovering >100% of the no-think→think gap from a 56.7 baseline.
- On τ-2 retail, no-think + skill reaches 40.0 vs 35.0±6.6 for think mode, recovering >100% of the gap from a 32.5 baseline.
- On τ-2 telecom, no-think + skill reaches 39.2 vs 45.0±2.5 for think mode, recovering 78% of the gap from a 19.2 baseline.
- On SSB-Verified, no-think + skill reaches 51.3 vs 61.3±1.2 for think mode, recovering 55% of the gap from a 39.3 baseline.
- Per-episode output stays at or below the no-think budget (0.6–0.8k tokens) with zero reasoning tokens, where thinking costs 2.9–4.5× more (think → skill: 3.7k→0.8k, 1.6k→0.6k, 2.1k→0.6k, 3.3k→0.8k).
- Distilling from think rollouts vs no-think rollouts lands within a few points with no consistent winner (ALFWorld 81.3 vs 78.7; retail 45.8 vs 40.8; telecom 32.5 vs 33.3; SSB reversed, 46.0 vs 56.0), so expensive reasoning traces are optional corpus enrichment needed at most once at corpus-construction time.
- Residual gaps on telecom and SSB suggest a portion of thinking — instance-specific deduction rather than reusable policy — that no static prompt recovers; closing it is future work.
- Limits: skill-to-skill variance (3 independently distilled skills) vs seed variance of a single prompt, one target model (GPT-5.4-mini no-think) and one coding agent (Claude Sonnet 5 / Claude Code) with untested distiller-capability sensitivity, and CASD inherits the corpus so it cannot discover behaviors absent from logged rollouts.

## The argument in five moves

1. Search-based prompt optimizers are bottlenecked by design: every candidate edit needs fresh environment rollouts and validation, and each step sees only a small trajectory sample.
2. CASD replaces the loop with a single offline pass — an unmodified coding agent analyzes the frozen rollout corpus with executable code and writes a skill file used directly as the optimized prompt, with no environment access, validation gate, or held-out set.
3. Under matched data access this one pass beats iterative search (best on 3 of 4 benchmarks, +16.6 vs +10.9 vs +5.3 mean gains) at ≈$1.60 per skill, and stays ahead on 2 of 4 even when baselines get extra validation data and unlimited environment access.
4. Theory frames this as variance versus bias: all methods maximize the same expected reward, but CASD's deterministic corpus statistics give low variance at fixed-corpus bias, winning under limited budgets while search's lower asymptotic bias should dominate as interaction grows.
5. The win comes from reflection scope — frequency-counted rules, cross-episode duplicate detection, and corpus-level absences invisible to minibatch reflection — without gate-overfitting, and the distilled skill recovers most or all of the no-think→think gap with zero reasoning tokens, though instance-specific deduction and corpus coverage remain limits.
