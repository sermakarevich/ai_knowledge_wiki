---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Coding Agents are Strong Prompt Optimizers

### Q1. What is the CASD recipe in one pass, and what does it eliminate?

> [!tip]- Answer
> Give an unmodified off-the-shelf coding agent the frozen rollout corpus plus a short natural-language instruction, and use the generated skill markdown file directly as the optimized system prompt. It eliminates the optimization loop, validation gate, environment interaction, and held-out validation set, costing about $1.60 per skill. See [[wiki/01-casd-overview|CASD overview]].

### Q2. What are the headline matched-data results and cost of CASD versus GEPA and SkillOpt?

> [!tip]- Answer
> Under matched data access across ALFWorld, τ-bench retail and telecom, and SpreadsheetBench-Verified, CASD beats GEPA on three of four benchmarks and SkillOpt on all four, with mean gains of +16.6 points versus +10.9 for GEPA and +5.3 for SkillOpt. CASD costs ~$1.60 per skill, over 22× cheaper than validation-gated search, and stays ahead on two of four benchmarks even when baselines get extra validation data and unrestricted environment access. See [[wiki/01-casd-overview|CASD overview]].

### Q3. How is the offline CASD goal formalized, and what is the verbatim distillation instruction?

> [!tip]- Answer
> The goal is `p* = CASD(D, p0)` from the frozen corpus `D = {τi}` alone, with fixed model weights and no new trajectories or environment interaction. The agent is told the results file holds N rollout trajectories, to analyze it directly with no other inputs or precomputed summaries, to use its own judgment on methodology, and to write a skill file capturing behavioral rules for accuracy and token/step efficiency. See [[wiki/02-head-to-head-results|Head-to-Head Results]].

### Q4. What does the coding agent actually do during the 24 distillation runs, and how evidence-grounded are the skills?

> [!tip]- Answer
> Across 24 runs there are 816 tool calls (94 exploring layout, 184 computing statistics, 510 inspecting episodes, 28 writing skill), averaging 34 calls per run and producing a 5–8 KB skill file in an explore-first, statistics-guided workflow with a median of 5 switches between statistics and inspection. Every run computes rewards/pass rates and episode lengths, most compute failure modes, tool usage, and per-category rates, and the 12 CASD skills carry 54 quantitative citations (4.6 per 1k words) versus zero across GEPA prompts and one across SkillOpt prompts. See [[wiki/02-head-to-head-results|Head-to-Head Results]].

### Q5. What objective and update form do all optimizers share, and how does their feedback differ?

> [!tip]- Answer
> All methods maximize expected task reward `J(p) = E[R(πθ(p), x)]` via the common update `pt+1 = Π[pt ⊕ ρ(pt, ϕt)]`, differing only in how feedback `ϕt` is inferred. Search uses `ϕ_search` from a sampled rollout batch plus a Monte Carlo validation score `r̂val(p)` with variance `σ²/|Dval|`, while CASD uses `ϕCASD = (Φ(D), {τi} for i in I(Φ))` where corpus statistics `Φ(D)` are deterministic functions of the fixed corpus. See [[wiki/03-method-and-theory|Method and Theory]].

### Q6. What is the bias–variance trade-off and the resulting operating-regimes claim, with cost numbers?

> [!tip]- Answer
> Search feedback has Monte Carlo variance that falls only with more rollouts, while CASD aggregates the whole corpus for low variance but carries fixed-corpus bias whenever the corpus misses important behaviors. Hence offline distillation and iterative search occupy complementary regimes: CASD wins on effectiveness and cost under limited budgets, while search's lower asymptotic bias should dominate as interaction grows. A CASD pass costs ≈$1.60 with no rollout bill, totaling 22× cheaper than SkillOpt ($142.5) and below GEPA ($8.4) over four benchmarks. See [[wiki/03-method-and-theory|Method and Theory]].

### Q7. What three observations support that corpus-scope reflection, not minibatch anecdotes, explains the win?

> [!tip]- Answer
> First, rules are statistical: the telecom skill's top rule targets fabricated identity-lookup arguments seen in 16/50 episodes (32%), which no single minibatch reliably surfaces and GEPA never addresses. Second, efficiency rules need cross-episode joins, e.g. 123 of 284 `get_details_by_id` calls being exact duplicates — a pandas one-liner invisible to context-window reflection. Third, CASD has no validation gate to overfit, avoiding GEPA-telecom-LD collapsing to 17.5 and SkillOpt retail variance of SD 10.1, with CASD skill variance small (SD ≤ 3.1 on 3 of 4 benchmarks). See [[wiki/04-why-corpus-scope-wins|Why corpus-scope reflection wins]].

### Q8. How does Figure 4 show that corpus-level absences are invisible to minibatch reflection?

> [!tip]- Answer
> A τ2-telecom "no service" ticket has two independent root causes with reward granted only if both are repaired. The device-side cause is visible in any single failed trajectory so all three optimizers encode a rule for it, but the account-side cause appears only as a corpus-level absence — `make_payment` is never invoked in the 50-rollout pool. Only CASD detects the missing behavior from corpus statistics and distills the billing rule, so only CASD solves the episode. See [[wiki/04-why-corpus-scope-wins|Why corpus-scope reflection wins]].

### Q9. How much of the no-think→think gap does no-think plus the CASD skill recover, and does the corpus need thinking traces?

> [!tip]- Answer
> On GPT-5.4-mini, no-think plus skill recovers over 100% of the gap on ALFWorld (56.7→83.3 vs 71.3 think) and retail (32.5→40.0 vs 35.0 think), 78% on telecom (19.2→39.2 vs 45.0), and 55% on SSB (39.3→51.3 vs 61.3), with zero reasoning tokens at 0.6–0.8k output tokens versus 2.9–4.5× more for thinking. Think-distilled versus no-think-distilled skills land within a few points with no consistent winner, so failure-rich no-think rollouts alone suffice and reasoning traces are optional enrichment needed at most once. See [[wiki/05-reasoning-gap-ablation|Recovering the reasoning gap]].

### Q10. (Evaluation) A budget-constrained team with only logged no-think rollouts and no simulator asks whether to adopt CASD as the default first step — what do you recommend and with what caveats?

> [!tip]- Answer
> Recommend CASD first: distill a skill offline from the frozen no-think corpus for ~$1.60, since it beats iterative search under matched data, recovers most or all of the reasoning gap with zero reasoning tokens, and needs no environment, grader, or validation split. Reserve iterative search for later gains only when interaction is cheap, and caveat that CASD inherits the corpus (it cannot discover unlogged behaviors), residual instance-specific deduction gaps remain on telecom/SSB, and results rest on one target model and one distiller with skill-to-skill variance. See [[wiki/05-reasoning-gap-ablation|Recovering the reasoning gap]].
