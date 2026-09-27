> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Robustness, Conclusions, and Appendix
**In one sentence:** Robustness checks show that inelastic capital supply lowers wages and raises capital returns while sticky wages shift AI costs from wage cuts to unemployment, and the authors conclude with a measurable-parameter framework plus a public scenario explorer rather than a single prediction.

## Key points
- In the extreme scenario, varying capital-supply elasticity (Epsilon, a number that measures how easily more machines and buildings are added when returns rise) from 1 to infinity moves 2030 GDP from 21.3% to 43.3% above the no-AI path.
- At inelastic capital supply (Epsilon = 1), the average wage falls below the no-AI path by 1.6% in the substantial scenario and by 9.2% in the extreme scenario, versus +2.1% and +9.7% at baseline Epsilon = 3.
- In the extreme scenario, the net return to capital (yearly profit from owning capital after wear and tear) is 10.3% per year at Epsilon = 1 versus 6.5% when capital is perfectly elastic, while the capital stock ranges from +33.5% to +82.2% above no-AI.
- Wage rigidity (Xi, a number from 0 to 1 that measures how slowly pay adjusts; higher means slower) creates a wage-versus-unemployment trade-off: at baseline Xi = 0.5 the extreme cognitive wage is -11.5% with 17.9% cognitive unemployment, at Xi = 0.9 the wage is +2.8% but unemployment is 24.0%, and at fully flexible Xi = 0 the wage falls 42.2% with only 2.6% unemployment.
- The authors' four conclusions are that outcomes range widely, almost all divergence comes after 2027, mechanics are the same in every scenario with only size and speed differing, and labor-market costs depend on capital elasticity and wage adjustment.
- In the extreme scenario 15% of GDP shifts from labor to capital (labor share 60% to 45.2%), total labor income is flat while capital income rises 81% above no-AI, and compensating cognitive workers would need a transfer of about 9% of GDP.
- The public scenario explorer at anthropic.com/institute/econ-scenarios lets anyone set parameters and see paths for GDP, growth, wages, capital returns, labor share, and unemployment through 2030.
- The survey behind the paper covered 10,980 unique US adults (August 11-23, 2026, Morning Consult panel) with 3,259 answering all five model questions, and median answers imply outcomes close to the substantial scenario.

---
## 4.5 Robustness: supply of capital
The elasticity of capital supply (Epsilon) is one number behind Table 3 that is neither measured nor a scenario dimension.
- Table 5 therefore reruns substantial and extreme at Epsilon = 1, 6, and infinity in place of baseline Epsilon = 3.
- All other parameters stay at Table 1 values; infinity means the rental rate is pegged by world markets.
Two results stand out.
First, elasticity moves capital prices and quantities substantially.

- With very low elasticity (Epsilon = 1) in the extreme scenario, the net return to capital rises to 10.3% per year.
- With perfectly elastic capital, the return stays at 6.5%.
- Capital-stock accumulation is correspondingly smaller when supply is inelastic and larger when elastic.

Second, wages and capital returns move in opposite directions.

- At Epsilon = 1 the wage change flips sign.
- Wages can decline relative to the no-AI path, in the extreme scenario even in absolute terms.
- When capital cannot expand easily, more of the gain stays as capital income rather than passing to wages.

Key 2030 numbers from Table 5 (percent above no-AI unless noted):

- Substantial GDP: 6.4% (Epsilon=1), 8.3% (3), 9.1% (6), 10.0% (infinity).
- Extreme GDP: 21.3%, 32.4%, 37.2%, 43.3%.
- Substantial average wage: -1.6%, +2.1%, +3.7%, +5.6%.
- Extreme average wage: -9.2%, +9.7%, +18.3%, +30.1%.
- Net return to capital, substantial: 7.6%, 7.0%, 6.8%, 6.5%.
- Net return to capital, extreme: 10.3%, 8.3%, 7.5%, 6.5%.
- Capital stock above no-AI, substantial: 9.3%, 13.8%, 15.7%, 18.2%.
- Capital stock above no-AI, extreme: 33.5%, 56.3%, 67.1%, 82.2%.
- Labor share of income, substantial: 55.1%, 56.1%, 56.5%, 57.0%.
- Labor share of income, extreme: 41.2%, 45.2%, 46.9%, 49.1%.

So-so technologies example:

- The paper cites "so-so technologies" (Acemoglu and Restrepo 2019): widely used but only marginally more productive per task.
- There labor-income losses can be large relative to GDP gains, so compensation consumes most gains.
- One in-range example combines substantial capability, adoption, and productivity gain with extreme automation share, fast displacement, no reinstatement, and Epsilon = 1.
- Then 2030 GDP is 7.2% above no-AI but total labor income is lower by 4.3% of no-AI GDP.
- Holding cognitive occupations' income at no-AI would take a transfer equal to 84% of GDP gains.

## 4.6 Robustness: wage rigidity
Rigidity parameter Xi governs how fast the cognitive wage moves toward its market-clearing level.
- The gap shrinks by factor Xi per year; Xi = 0 is fully flexible, Xi = 0.5 is baseline, Xi = 0.9 is very rigid with 7-year half-life.
Table 6 reruns substantial and extreme at Xi = 0.75 and 0.9 in place of 0.5, plus extreme at Xi = 0.

- The table shows the trade-off Xi governs: stickier wages mean more layoffs and smaller wage declines.
- At baseline Xi = 0.5 in the extreme scenario, the cognitive wage in 2030 is 11.5% below no-AI and cognitive unemployment is 17.9%.
- At very rigid Xi = 0.9, the cognitive wage is 2.8% above no-AI but cognitive unemployment rises to 24.0%.
- At fully flexible Xi = 0, the cognitive wage falls by more than 42% while cognitive unemployment is just 2.6%.
- Effects are therefore felt in wages or unemployment; baseline shares the cost across both margins.

Table 6 reproduced verbatim (values for 2030):

|  | Substantial |  |  | Extreme |  |  |  |
|---|---|---|---|---|---|---|---|
| Xi: | 0.5 | 0.75 | 0.9 | 0 | 0.5 | 0.75 | 0.9 |
| GDP, pct. above the no-AI path | 8.3 | 7.9 | 7.7 | 36.6 | 32.4 | 30.5 | 29.2 |
| Average wage, pct. above the no-AI path | 2.1 | 2.2 | 2.3 | 1.6 | 9.7 | 11.1 | 11.9 |
| Cognitive wage wC,t, pct. | -0.3 | 0.7 | 1.4 | -42.2 | -11.5 | -2.9 | 2.8 |
| All-other wage wN,t, pct. | 5.9 | 4.5 | 3.7 | 70.1 | 33.6 | 25.8 | 21.1 |
| Cognitive employment, pct. since mid-2026 | -3.9 | -4.6 | -5.0 | -1.3 | -21.5 | -25.9 | -28.5 |
| Unemployment rate, cognitive workers, pct. | 4.5 | 5.1 | 5.4 | 2.6 | 17.9 | 21.7 | 24.0 |
| Unemployment rate, all workers, pct. | 4.6 | 4.9 | 5.2 | 3.1 | 11.9 | 13.9 | 15.2 |

Note: scenarios of Table 3 rerun with rigidity in Equation (30) at Xi = 0, 0.75, 0.9 in place of 0.5; all other parameters as in Table 1.
## Section 5: Conclusions

The paper seeks to place wide-ranging views on AI's economic effects inside a common framework.

- Views become alternative settings of a small number of parameters that can be reasoned about and increasingly measured.
- The framework is a standard task-based model with two occupation groups, an ideas channel, and a frictional labor market.
- The accompanying scenario explorer lets anyone set parameters and see paths for GDP, growth, wages, capital returns, labor share, and unemployment through 2030.

Four main results:

1. Range is wide: modest acts like a "normal technology" with small effects, while extreme is transformative with GDP 32% above no-AI and nearly 1 in 5 cognitive workers unemployed by 2030.
2. Almost all divergence comes after 2027, about 1.5 years from the mid-2026 anchor, because scenarios share today's readings and separate only as AI reach and use diverge.
3. Mechanics are the same in every scenario: output rises, cognitive employment shrinks, other employment grows, and unemployment depends on reallocation size plus how easily displaced workers find jobs outside old occupations; scenarios disagree only on size and speed.
4. Labor-market consequences depend on capital elasticity and wage adjustment: elastic capital lets labor keep more gains while inelastic capital can push average wages below no-AI; labor share falls from 60% to 56% (substantial) and 45% (extreme); cognitive wages fall below no-AI in extreme while other wages rise sharply; costs combine lower relative wages with higher unemployment, with fast adjustment loading onto wages and rigidity loading onto unemployment.

Measurability claim:

- Each explorer parameter is potentially measurable: share of tasks AI can do, share of firms using it, productivity gain per task, and how long displaced workers take to find new jobs.
- Incoming data will therefore tell which scenario applies.
- Today none of the three can be ruled out.
- The hoped lasting contribution is the framework itself: stating disagreements as disagreements about a few measurable parameters.

Transitions and policy:

- Modest or substantial reallocations are sizes the US labor market has absorbed historically, though still costly.
- Extreme means about 18% cognitive unemployment, immense relative-wage falls, and 15% of GDP shifting from payrolls to capital income.
- Aggregate gains are nearly 3x cognitive losses, so compensation resources exist, but growth alone does not deliver them.
- Sharing mechanisms — retraining, income support, universal basic capital or income, and not-yet-designed options — become central economic-policy questions.
- Which world applies may clarify within a year or two, so preparing for disruption is the prudent course.

The authors point readers to the framework and scenario explorer at anthropic.com/institute/econ-scenarios to inform debate on managing the transition.

## Appendix A: simulation strategy highlights

Timing and initialization:
- Monthly grid with step h = 1/12 year; rates converted to continuously compounded rates.
- At t0 AI gaps imply at most 0.25% GDP gap; flows start from steady state at normal-times mu-bar.

Three object groups:
- Fixed parameters: substitution elasticity, base shares, capital elasticity, group employment, ideas parameters, baseline growth, research share, plus frictional parameters.
- Exogenous scenario paths: m, d, a, psi, and rho.
- Endogenous variables: ideas stock, rental gap and capital, shares, wages, output, measured TFP (Total Factor Productivity, overall efficiency turning inputs into outputs), targets, plus per-group flows and pools.

Monthly evaluation order (9 steps):

1. Paths at t and t+1 plus predetermined ideas stock.
2. Capital market: solve one monotone rental-gap equation by bisection (zero at Epsilon = infinity).
3. Wage, shares, targets, output per worker, measured TFP, and t+1 targets.
4. Gaps and sticky cognitive wage, clearing wage, and cognitive labor demand.
5. Separations (quits plus layoffs) and openings.
6. Matching: effective search, hires, finding rates by origin.
7. Stocks: update employment and pools.
8. Reporting: actual-economy GDP, wages, return, capital, labor share, excess pools, reallocation flows, aggregate overhang, and cognitive shift.
9. Ideas: set research uplift to GDP gap and step ideas stock forward one month.

System size and solution:

- Table A.1 writes the full two-group system as 44 equations in 44 unknowns per month plus a once-solved steady state.
- Simulation uses exact rows; first-order rows marked with approximate signs are for intuition only.
- Measured TFP and the ideas update are the two approximate rows under exact simulation (extreme-path ideas within 0.02pp of closed form in 2030).
- Apart from rental-rate and actual-economy blocks, every right-hand side uses only parameters, exogenous paths, predetermined variables, or earlier rows, so the model solves recursively.
- Table A.2 documents every parameter and exogenous object with substantial-scenario values.

## Appendix B: survey details highlights

Purpose and conversion:
- Every respondent's answers are mapped to m2030, d2030, psi, a2030, and mu.
- Table 2 reports medians/quartiles of values; Table 4 reports quantiles of model-implied outcomes.
- Table 4 uses 3,259 respondents answering all five items; Table 2 medians use everyone answering each item.
- Unasked parameters use substantial values: rho = 0.25, posting speed = 0.25, Xi = 0.5, Epsilon = 3.
Samples:

- Morning Consult online panel of US adults, eight daily samples near 2,000 each, August 11-23, 2026.
- 10,980 unique people after keeping first responses; weighted to adults on age, gender, education, race, region, and income.
- Screens for speed and attention plus unlikely-event and semantic checks; "not sure" excluded item by item.
- Three questionnaire pilots in July-August 2026 near 2,000 each; random 2027 vs 2030 framing, but only 2030 data used for parameters.

Questionnaire (5 items):
1. Capability: 8 tasks from routine emails through software, studies, online business, to Nobel discovery; rated already-can/by 2027/by 2030/later/never/not sure.
2. Adoption: share of capable tasks regularly used at work in 2030, in 5 bins from under 10% to over 75%.
3. Automation: 5 tasks rated AI-alone / AI-mostly / worker-mostly / worker-alone.
4. Productivity gain: time with AI versus without, from takes longer to one-tenth or less.
5. Re-employment: months for an AI-displaced worker to find a new-occupation job given 3-month baseline, in 8 bins up to over 3 years/never.

Mapping to parameters (Table B.1):

- Capability: count of 8 tasks expected by 2030 times 95% in-person adjustment times 0.62 knowledge-work wage-bill share (e.g. 7/8 gives 0.52; scenarios equal about 3, 4, and 7 tasks).
- Adoption: bin midpoints (e.g. 25-49% coded as 0.37).
- Automation: AI-alone = 1, AI-mostly = 0.5, worker-mostly = 0; worker-alone tasks dropped; psi equals summed counts over performed tasks.
- Productivity: time ratio converted to log speedup a = ln(1/ratio) (quarter-time = 1.39; longer/same = 0).
- Re-employment: mu = 0.17 x 3/months capped at 1 (3.5 months = 0.15; never = 0).
- Binned medians are interpolated linearly within bins; task counts keep plain quantiles.

## Appendix C: innovation-block highlights

Fishing out and research share without AI:

- Without AI, ideas grow at g = 1.67% per year and measured TFP at 1.0%.
- Bloom et al. (2020) fishing-out estimate of 3.1 in TFP units becomes 1-phi-R = 2.86 in labor-augmenting goods units after multiplying by labor share and adding lambda.
- Sustaining growth needs research-input growth near 4.8% per year versus 2% GDP growth.
- Research GDP share must therefore trend up about 2.8% per year, from 3.5% in 2024 to 4.1% in 2030.
- The paper assumes that research-share path with or without AI.

Cumulation, drag, and pass-through:

- Each year adds a new research uplift while accumulated ideas create fishing-out drag on further discovery.
- Growth-gap and closed-form level equations weight uplifts by the baseline research trend.
- Ideas enter the factor-price frontier as lower cost of every labor instance, adding to level-channel wage, share, output, capital, and TFP terms.
- Measured TFP beyond first order uses a CES (Constant Elasticity of Substitution, a flexible averaging formula) price index over tasks at base factor prices.

## Limitations acknowledged
- No Euler equation connects capital returns to economic growth, which could substantially raise returns; planned for a future version.
- Cognitive firms' profit from paying below marginal product is at most 0.5% of GDP on these paths and treated as small.
- Survey runs fix reinstatement, posting speed, wage rigidity, and capital elasticity at substantial values rather than estimating them.
- Ideas monthly stepping and measured TFP use approximations, with extreme-path ideas within 0.02pp of closed form in 2030.
- Wage-bill accounting counts unemployed workers at zero, and precedent-free transfers near 9% of GDP sit beyond the framework.
- Results are scenarios to organize measurable disagreements, not predictions, and none of the three can currently be ruled out.

**Covers:** Sections 4.5-4.6, Section 5, Appendix A-C
