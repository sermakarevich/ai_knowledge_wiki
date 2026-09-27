> [[index|Wiki]] | [[summary|Summary]]

# Economic Scenarios for Transformative AI — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-framework|Introduction and Framework]]

**In one sentence:** The paper builds a task-based framework that maps different assumptions about AI capabilities in 2026-2030 into comparable paths for GDP, wages, labor share, reallocation, and unemployment, illustrated with modest, substantial, and extreme scenarios plus a US survey.

- Published estimates of AI's impact span orders of magnitude and use incomparable frameworks, so the paper offers an integrated model to compare assumptions rather than making predictions or assigning probabilities.
- The model converts share of tasks affected, diffusion of use, productivity gain per task, and automation-versus-augmentation share into paths for productivity, growth, wages, labor share, reallocation, and unemployment through 2030.
- AI directly affects only cognitive occupations (management, professional, sales, office), not other occupations (e.g. construction, electricians); adoption raises productivity and capital demand but displaces cognitive workers facing switching frictions, producing unemployment.
- Modest change adds <0.5 pp to GDP growth by 2030 and +0.1 pp unemployment; substantial leaves GDP 8.3% above no-AI; extreme has AI doing almost half of today's cognitive work, 15% yearly GDP growth, labor share 60% to 45%, nearly one in five cognitive workers unemployed.
- AI-accelerated innovation adds little by 2030 (labor productivity well under 1% via this channel) because research stays bottlenecked by physical tasks in the semi-endogenous setup, so it is likely a lower bound.
- Median answers from 10,980 US adults imply near-substantial outcomes — GDP +8% and cognitive employment -4% by 2030 — while almost all scenario divergence occurs after 2027.

## 2. [[wiki/02-model-production-and-factor-shares|Production, AI Scenarios, and Factor Shares]]

**In one sentence:** Output is a constant-returns task-based aggregate with gross-complementary tasks, competitive factor assignment, five AI scenario parameters, and a factor-price frontier where measured total factor productivity (TFP — output growth not explained by more inputs) gains flow to wages unless inelastic capital pushes up rental rates and displaces cognitive workers.

- Tasks are gross complements with elasticity across tasks `σ = 0.5`, so cheaper AI instances gain expenditure share and become the weak link rather than collapsing in price.
- AI is described by five objects: affected mass `m`, diffusion share `d`, log gain `a`, automation share `ψ`, and reinstatement ratio `ρ`, with `m·d` the fraction of instances AI performs and `m·d·a` that fraction times gain.
- Measured TFP rises by `Δ ln TFP ≈ s_L,t0·m·d·a` regardless of automation versus augmentation, because only the unit-cost decline weighted by expenditure share matters.
- The factor-price frontier `s_L,t0·Δ ln w + s_K,t0·Δ ln r ≈ s_L,t0·m·d·a` splits the same TFP gain between wages and capital rents, so each 1% rise in rents cuts wages by `s_K,t0/s_L,t0 = 2/3%`.
- At fixed rental rates wages track productivity `m·d·a`, not net displacement `(1−ρ)·ψ·m·d`; displacement moves the labor share and capital demand and reaches wages only through the rental rate.
- Wages can fall below the no-AI path when small cost savings are paired with large task transfers and scarce capital — so-so automation — formalized by a threshold capital-supply elasticity `ε*`.
- Target employment in unaffected occupations rises with output and falls with wages with elasticity `σ`, forcing cognitive employment down by a size-scaled amount and requiring reallocation plus frictional unemployment.

## 3. [[wiki/03-model-innovation-and-unemployment|Innovation and Unemployment in the Model]]

**In one sentence:** AI raises research spending by enlarging GDP but adds little to idea growth by 2030, while sticky cognitive wages and slow occupational matching turn displacement into temporary unemployment.

- **Ideas are semi-endogenous via a research budget:** ideas stock `A_t` is produced from research input `R_t`, and research is a share `iota_R,t` of GDP funded by a lump-sum tax, so AI raises `R_t` mainly because AI raises GDP (the level channel).
- **Growth-rate effect is small by construction:** a 5% GDP gap raises idea growth by less than 5% — e.g. measured TFP (Total Factor Productivity) growth from 1.00% to 1.05% per year — because the GDP level gain applies to a ~1% baseline growth rate, and further damped if `lambda < 1` and `Delta ln A_t > 0`.
- **Long-run vs realized idea gains differ sharply:** on the extreme path `Delta ln R_t` reaches 0.28 in 2030, implying a long-run ideas level ~10% above no-AI, but only 0.6% above no-AI is realized by 2030 because cumulation takes decades.
- **Measured TFP mixes ideas and AI level effects:** the Solow residual combines growth in `A_t` and the static AI term `m_t d_t a_t`, both entering with the labor share as Domar weight: `Delta ln TFP_t ≈ s_L,t0 Delta ln A_t + m_t d_t a_t`.
- **Unemployment comes from two frictions:** a cognitive wage that closes only a fraction of its gap to market-clearing each month, forcing layoffs/rationing, plus a search-and-matching process that takes time to re-employ displaced workers.
- **Matching is hard across occupations:** effective search is `S_C = U_C + mu U_N`, `S_N = mu U_C + U_N`, with normal-times discount `mu-bar = 0.17` (1 in 7 job-finders change groups); scenarios set `mu = 0.17, 0.08, 0.04` and hiring-posting speed `theta_H = 0.10, 0.25, 0.50`.
- **Normal-times baseline is CPS-calibrated:** unemployment pool `U-bar = 3.8%` of labor force, monthly quits `q-bar_C = 0.63%` and `q-bar_N = 1.40%`, aggregate finding rate ~0.23/month, mean vacancy filling rate 0.65/month; e.g. software engineer does not instantly become electrician or nurse.

## 4. [[wiki/04-calibration-parameters-and-ai-pace|Calibration: Parameters and the Pace of AI]]

**In one sentence:** The model anchors mid-2026 AI use at low levels (14% of tasks affected, 10% diffusion) and then spans 2030 outcomes from modest to extreme by varying capability, diffusion, productivity gains, automation share, reinstatement, and re-employment frictions, with all normal-times labor-market flows tied to CPS (Current Population Survey) data.

- Tasks are gross complements with elasticity sigma = 0.5, labor earns 60% of income before AI, and cognitive occupations employ 62.4% of workers in the 2025 CPS (Current Population Survey).
- The affected task mass starts at m = 0.14 in mid-2026 (0.22 in cognitive, 0.01 elsewhere) and reaches m2030 = 0.2 / 0.3 / 0.5 in the modest / substantial / extreme scenarios.
- Diffusion starts at d = 0.10 in mid-2026 and reaches d2030 = 0.2 / 0.4 / 0.6, with ceiling d-bar = 1 and logistic slopes set by Equation (8').
- The log gain per AI instance starts at a = 0.30 / 0.35 / 0.45 in mid-2026 with yearly slopes g_a = 0 / 0.028 / 0.10, implying a2030 = 0.30 / 0.45 / 0.80.
- Disruptiveness is psi = 0.50 / 0.75 / 0.90 automation share, reinstatement ratio rho = 0.50 / 0.25 / 0, search discount mu = 0.17 / 0.08 / 0.04, and posting speed theta_H = 0.10 / 0.25 / 0.50 per month, with wage rigidity xi = 0.50 per year in all scenarios.
- Normal times are calibrated to CPS 2010-19 and 2025: quit rate q-bar = 0.11 per year, separation ratios 0.69 for cognitive and 1.52 for all-other workers, search pool U-bar = 0.038, search discount mu-bar = 0.17, matching curvature iota = 1.27, and mean filling rate 0.65 per month.

## 5. [[wiki/05-survey-of-us-expectations|What US Adults Expect: The Survey]]

**In one sentence:** In August 2026, a representative survey of 10,980 US adults found people expect fast AI (Artificial Intelligence) capability growth by 2030 but limited workplace use, with the median answers landing near the paper's substantial-change scenario and views varying widely.

- The survey covered 10,980 US adults via Morning Consult on August 11–23, 2026, asking five questions about capability timing, use, speed gains, automation, and job-finding.
- On what AI can already do today, 24 percent say it can build and maintain a software product and 19 percent say it can run a small online business.
- By 2030, 52 percent expect AI to run an online business with no employees, while 39 percent expect a Nobel-level scientific discovery and 40 percent say such discoveries will never happen.
- The median respondent expects AI to handle six of the eight tasks by 2030, implying AI capability m_2030 (share of knowledge work impacted) of 0.44 with interquartile range [0.20, 0.59].
- Median adoption d_2030 (share of feasible tasks actually used at work) is 0.40 [0.22, 0.61], median automation psi (share done alone rather than with a worker) is 0.47 [0.25, 0.65], and median productivity gain a_2030 (log speed-up) is 0.44 [0.09, 1.02].
- Median job-finding parameter mu (speed of finding a new occupation, where three months equals 0.17) is 0.064 [0.025, 0.111], implying about eight months for a worker displaced by AI to find a new-occupation job.
- Views are widely dispersed: about 30 percent expect AI to save no time at all on a suited task, while 49 percent expect it to cut task time at least in half.

## 6. [[wiki/06-results-three-scenarios|Results: The Three Scenarios]]

**In one sentence:** By 2030 AI adds 1.6% to GDP in the modest scenario, 8.3% in the substantial scenario, and 32.4% in the extreme scenario — with the labor-market pain concentrated on cognitive (knowledge-work) occupations.

- **Modest scenario GDP:** GDP is 1.6% above the no-AI path in 2030 (index 114.5 vs 112.7 with 2024 = 100), growing at 2.4%/yr vs 2.0%/yr without AI — about ten extra months of normal growth over four years.
- **Modest labor effects are tiny:** average wage +0.7% (cognitive +0.4%, other +1.1%), labor share 60.0 → 59.4%, cognitive employment −0.5% since mid-2026, overall unemployment 3.9% vs 3.8% normal.
- **Substantial scenario GDP:** GDP is 8.3% above the no-AI path in 2030 (index 122.1), growing at 5.4%/yr — faster than the 4.7% peak of the 1990s dot-com boom.
- **Substantial distribution split:** average wage +2.1% hides cognitive wages −0.3% vs other occupations +5.9%; labor share falls 60 → 56% (capital 40 → 44%), a 4-point shift in four years ≈ the whole US labor-share decline since 1980.
- **Substantial jobs:** cognitive employment −3.9% since mid-2026 (other occupations +4.6%); cognitive unemployment rises 2.9 → 4.5% (over 50% higher), overall unemployment 4.6%.
- **Extreme scenario is transformative:** GDP +32.4% above no-AI (40% above mid-2026), growth 15.4%/yr (incomes double every ~5 years); labor share collapses 60 → 45.2%, capital share 40 → 54.8%, return to capital 6.5 → 8.3%.
- **Extreme labor pain + survey check:** cognitive employment −21.5%, cognitive unemployment 17.9%, overall 11.9%; cognitive wages −11.5% vs no-AI (flat in absolute terms) while other wages +33.6%; the median survey respondent implies outcomes near substantial (GDP +8.6%, cognitive employment −4.2%, unemployment ~4.6%).

## 7. [[wiki/07-robustness-conclusions-appendix|Robustness, Conclusions, and Appendix]]

**In one sentence:** Robustness checks show that inelastic capital supply lowers wages and raises capital returns while sticky wages shift AI costs from wage cuts to unemployment, and the authors conclude with a measurable-parameter framework plus a public scenario explorer rather than a single prediction.

- In the extreme scenario, varying capital-supply elasticity (Epsilon, a number that measures how easily more machines and buildings are added when returns rise) from 1 to infinity moves 2030 GDP from 21.3% to 43.3% above the no-AI path.
- At inelastic capital supply (Epsilon = 1), the average wage falls below the no-AI path by 1.6% in the substantial scenario and by 9.2% in the extreme scenario, versus +2.1% and +9.7% at baseline Epsilon = 3.
- In the extreme scenario, the net return to capital (yearly profit from owning capital after wear and tear) is 10.3% per year at Epsilon = 1 versus 6.5% when capital is perfectly elastic, while the capital stock ranges from +33.5% to +82.2% above no-AI.
- Wage rigidity (Xi, a number from 0 to 1 that measures how slowly pay adjusts; higher means slower) creates a wage-versus-unemployment trade-off: at baseline Xi = 0.5 the extreme cognitive wage is -11.5% with 17.9% cognitive unemployment, at Xi = 0.9 the wage is +2.8% but unemployment is 24.0%, and at fully flexible Xi = 0 the wage falls 42.2% with only 2.6% unemployment.
- The authors' four conclusions are that outcomes range widely, almost all divergence comes after 2027, mechanics are the same in every scenario with only size and speed differing, and labor-market costs depend on capital elasticity and wage adjustment.
- In the extreme scenario 15% of GDP shifts from labor to capital (labor share 60% to 45.2%), total labor income is flat while capital income rises 81% above no-AI, and compensating cognitive workers would need a transfer of about 9% of GDP.
- The public scenario explorer at anthropic.com/institute/econ-scenarios lets anyone set parameters and see paths for GDP, growth, wages, capital returns, labor share, and unemployment through 2030.
- The survey behind the paper covered 10,980 unique US adults (August 11-23, 2026, Morning Consult panel) with 3,259 answering all five model questions, and median answers imply outcomes close to the substantial scenario.

## The argument in five moves

1. Published estimates disagree wildly, so the paper builds a comparable task-based framework instead of a prediction.
2. AI lowers task costs through five parameters, splitting gains between wages and capital via the factor-price frontier.
3. Calibration anchors 2026 at low use while scenarios and a US survey span modest to extreme paces and frictions.
4. By 2030 GDP runs +1.6% to +32.4% above no-AI with pain concentrated on cognitive workers.
5. Robustness shows capital and wage frictions govern who bears costs, leaving a measurable-parameter explorer rather than a forecast.
