> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Calibration: Parameters and the Pace of AI

**In one sentence:** The model anchors mid-2026 AI use at low levels (14% of tasks affected, 10% diffusion) and then spans 2030 outcomes from modest to extreme by varying capability, diffusion, productivity gains, automation share, reinstatement, and re-employment frictions, with all normal-times labor-market flows tied to CPS (Current Population Survey) data.

## Key points

- Tasks are gross complements with elasticity sigma = 0.5, labor earns 60% of income before AI, and cognitive occupations employ 62.4% of workers in the 2025 CPS (Current Population Survey).
- The affected task mass starts at m = 0.14 in mid-2026 (0.22 in cognitive, 0.01 elsewhere) and reaches m2030 = 0.2 / 0.3 / 0.5 in the modest / substantial / extreme scenarios.
- Diffusion starts at d = 0.10 in mid-2026 and reaches d2030 = 0.2 / 0.4 / 0.6, with ceiling d-bar = 1 and logistic slopes set by Equation (8').
- The log gain per AI instance starts at a = 0.30 / 0.35 / 0.45 in mid-2026 with yearly slopes g_a = 0 / 0.028 / 0.10, implying a2030 = 0.30 / 0.45 / 0.80.
- Disruptiveness is psi = 0.50 / 0.75 / 0.90 automation share, reinstatement ratio rho = 0.50 / 0.25 / 0, search discount mu = 0.17 / 0.08 / 0.04, and posting speed theta_H = 0.10 / 0.25 / 0.50 per month, with wage rigidity xi = 0.50 per year in all scenarios.
- Normal times are calibrated to CPS 2010-19 and 2025: quit rate q-bar = 0.11 per year, separation ratios 0.69 for cognitive and 1.52 for all-other workers, search pool U-bar = 0.038, search discount mu-bar = 0.17, matching curvature iota = 1.27, and mean filling rate 0.65 per month.

---

## Table 1 values in this chunk

A value spanning the three scenario columns is common to all scenarios. Ceilings are natural maxima (m-bar = s_C,t0 / s_L,t0, d-bar = 1); slope and midpoint follow from 2026 anchor, 2030 value, and ceiling by Equation (8').

### B. Pace of AI: diffusion and productivity gain per instance

| Symbol | Meaning | Modest | Substantial | Extreme | Source or basis |
|---|---|---|---|---|---|
| d_t | diffusion share, mid-2026 anchor | 0.10 | 0.10 | 0.10 | firm AI use, Business Trends and Outlook Survey and its 2026 AI supplement (U.S. Census Bureau, 2026; Bonney et al., 2026) |
| d_2030 | diffusion share, 2030 | 0.2 | 0.4 | 0.6 | scenario assumptions |
| d-bar | ceiling on diffusion | 1 | 1 | 1 | every instance |
| a_t | log gain per instance, mid-2026 anchor | 0.30 | 0.35 | 0.45 | scenario assumptions: all-in gains in trials and at the frontier (Brynjolfsson et al., 2025; Huang et al., 2025; Demirer et al., 2026) |
| g_a | slope, per year | 0 | 0.028 | 0.10 | scenario assumptions which imply a_2030 = 0.30 / 0.45 / 0.80 |

What they mean: `d` is how many AI-capable task instances actually use AI; `d-bar = 1` means eventually all could. `a` is the proportional productivity gain when AI is used, in log points; `g_a` is how fast that gain grows per year.

### C. Disruptiveness: automation, new tasks, and search once AI arrives

| Symbol | Meaning | Modest | Substantial | Extreme | Source or basis |
|---|---|---|---|---|---|
| psi_t | automation share, held constant | 0.50 | 0.75 | 0.90 | scenario assumptions: low end similar to current automation-like share of use (Appel et al., 2025) |
| rho | reinstatement ratio | 0.50 | 0.25 | 0 | scenario assumptions: Acemoglu and Restrepo (2019) estimated rho = 0.5 |
| mu | search discount on the path | 0.17 | 0.08 | 0.04 | scenario assumptions: mu-bar = 0.17 is the value consistent with normal-times occupational switching estimated from CPS |
| theta_H | posting speed, per month | 0.10 | 0.25 | 0.50 | scenario assumptions |
| xi | rigidity of the cognitive wage, per year | 0.50 | 0.50 | 0.50 | wage-setting evidence (Section 3.4) |

What they mean: `psi` is the fraction of AI-used instances done by AI alone versus with a worker. `rho` is new human tasks created per task automated. `mu` is how much harder cross-occupation job search is than same-occupation search. `theta_H` is how fast the all-other group posts jobs to absorb displaced workers. `xi` controls how fast the cognitive wage adjusts toward its market-clearing level.

### D. The labor market in normal times, common to the scenarios

| Symbol | Meaning | Value | Source or basis |
|---|---|---|---|
| q-bar | normal quit rate, per year | 0.11 | implied by the pool and the CPS finding rate, rounded (Section 3.2) |
| q_oT / q-bar_o | share of quits that responds to job prospects | 0.55 | elasticity of JOLTS quits to the CPS finding rate (U.S. Bureau of Labor Statistics, 2026a) (Section 3.2) |
| q-bar_C / q-bar; q-bar_N / q-bar | relative separation rates by group | 0.69; 1.52 | IPUMS-CPS 2010-19 (Flood et al., 2025) |
| U-bar | normal search pool, share of L | 0.038 | CPS 2025 (U.S. Bureau of Labor Statistics, 2026b) |
| mu-bar | search discount in normal times | 0.17 | CPS 2010-19 switching matrix from replication files of Carrillo-Tudela and Visschers (2023b), corrected by their method (Section 3.2) |
| iota | matching curvature | 1.27 | den Haan et al. (2000) |
| pi-bar_o, mean | filling rate, per month | 0.65 | JOLTS 2010-19, computed using the method of Davis et al. (2013) |

What they mean: `q-bar` is the economy-wide quit rate when hires equal quits. The `0.55` split says just over half of quits respond to job prospects. The `0.69; 1.52` ratios say cognitive workers separate less often than average and all-other workers more often. `U-bar` is the normal unemployed search pool. `mu-bar`, `iota`, and the filling rate describe matching frictions and hiring speed.

## 3.1 Production-function parameters

- Elasticity across tasks is sigma = 0.5, so tasks are gross complements: a cheap automated task does not fully replace the rest.
- Labor share before AI is 60%; capital share is therefore 40%.
- Cognitive occupations are twelve SOC (Standard Occupational Classification) major groups covering management, professional, sales, and office work; all other occupations are the remaining ten groups.
- Cognitive occupations employ 62.4% of workers in the 2025 CPS, and observed AI exposure is concentrated almost entirely there.
- The ceiling on affected mass is m-bar = s_C,t0 / s_L,t0 in every scenario: in the long run all cognitive work is within AI reach; scenarios differ only in how much is within reach by 2030.
- Observed exposure uses Massenkoff and McCrory (2026): share of occupation task time with significant work-related Claude use, assistive use counted at one half; it is a proxy for AI use generally.
- Ideas parameters: no duplication, fishing-out of 3.1 from Bloom et al. (2020) in TFP (Total Factor Productivity) units and researcher-equivalents, which is 2.86 in model labor-augmenting units with research input in goods; ideas-stock growth 1.67% per year without AI and hence TFP growth of 1%; research budget 3.5% of GDP in 2024 whose share rises at 2.8% per year, with or without AI.
- Capital-supply elasticity is epsilon = 3, higher than five years of saving at historical rates would imply, because compute for automated cognitive work is financed globally and built in a year or two.
- Cognitive group in detail: Management (11); Business and Financial Operations (13); Computer and Mathematical (15); Architecture and Engineering (17); Life, Physical, and Social Science (19); Community and Social Service (21); Legal (23); Educational Instruction and Library (25); Arts, Design, Entertainment, Sports, and Media (27); Healthcare Practitioners and Technical (29); Sales and Related (41); and Office and Administrative Support (43).
- All-other group in detail: Healthcare Support (31); Protective Service (33); Food Preparation and Serving Related (35); Building and Grounds Cleaning and Maintenance (37); Personal Care and Service (39); Farming, Fishing, and Forestry (45); Construction and Extraction (47); Installation, Maintenance, and Repair (49); Production (51); and Transportation and Material Moving (53).
- The scenario explorer labels these two groups "knowledge workers" and "all other workers."
- Any two-way split is a simplification: exposure varies widely within groups and many non-cognitive occupations involve some cognitive work.
- Concentration check: the Massenkoff-McCrory observed-exposure measure matches survey-based generative-AI use (Bick, Blandin, and Deming, 2024) and task-feasibility ratings (Eloundou et al., 2024).
- Logistic mechanics: the slope taking affected mass from mid-2026 m_2026 to 2030 m_2030, three and a half years later, is kappa_m = (1/3.5) x ln[(m-bar - m_2026)/m_2026 x m_2030/(m-bar - m_2030)], and likewise for kappa_d; this is Equation (8').

## 3.2 Normal-times calibration

- Nearly every labor-market number comes from the CPS (Current Population Survey).
- 2025 CPS annual averages give employment shares and the unemployed pool; IPUMS-CPS matched monthly files for 2010-19 give flows.
- Each month on average 22% of unemployed workers found a job; 0.84% of employed cognitive workers and 1.84% of all-other workers became unemployed; calibration uses the ratio of these separation rates.
- Job-finder destinations, after removing coding-error switches by Carrillo-Tudela and Visschers method: 19% of finders from cognitive occupations took all-other jobs, 11% from all-other took cognitive jobs; 14.3% changed group overall.
- Quit rate derivation: hires equal quits in normal times, so CPS finding rate times pool implies 0.219 x 3.84/96.16 = 0.875% of employment per month, or 0.105 per year, rounded to 0.11 per year (0.92% per month); at that value the model steady-state finding rate is 0.23 per month.
- Splitting by separation ratios gives 0.63% per month for cognitive workers and 1.40% for all other workers.
- Search discount mu-bar: odds are 19/81 = 0.23 one way and 11/89 = 0.12 the other; multiplying cancels relative hiring rates and leaves mu-bar squared, so mu-bar = sqrt(0.23 x 0.12) = 0.17, applied symmetrically in both directions.
- Quit split: JOLTS quits moved with the CPS job-finding rate with elasticity 0.53 over 2001-19, rounded to 0.55 for the prospect-responsive share.
- Remaining setup: steady state determines hires, unemployed share, and finding rate by group of origin; matching efficiency chi is set so the employment-weighted mean filling rate is 0.65, computed from JOLTS 2010-19.
- The asymmetry between 19% and 11% crossing rates is interpreted as differences in hiring rates, not asymmetric frictions, because the same mu-bar applies in both directions.
- Equation (35) logic: a cognitive finder’s odds of landing outside equal mu-bar times the relative hiring rate, and the reverse move equals mu-bar times the inverse; multiplying the two odds cancels the hiring-rate ratio.
- Equation (27) logic: quits split into a prospect-responsive part and an unresponsive part; the 0.55 value comes from rounding the 0.53 JOLTS-to-CPS elasticity.
- Equation (38) steady state then pins down hires and group-specific finding rates once matching efficiency chi matches the 0.65 filling rate.

## 3.3 Pace of AI

- All three scenarios share the same mid-2026 readings of m_t and d_t and differ in 2030 values; slopes follow from Equation (8'); paths coincide at mid-2026 and differ by only a few tenths of a percent of GDP before then.
- Affected-mass anchor m = 0.14 overall (0.22 cognitive, 0.01 other), conservative because assistive use counts half, thinly used tasks count zero, and data are late-2025.
- Diffusion anchor d = 0.10: in late 2025, 18% of firms used AI (32% employment-weighted) and workers in 23% of firms used generative AI in their own tasks, but firm shares overstate instance shares because adopters use AI on few tasks and some instances.
- 2030 affected mass m_2030 = 0.2 / 0.3 / 0.5, spanning rated feasibility in Eloundou et al. (2024).
- 2030 diffusion d_2030 = 0.2 / 0.4 / 0.6, below recent rapid frontier LLM (Large Language Model) adoption but allowing for historically slower diffusion.
- Productivity gain per instance starts at 0.30-0.45 in logs from field trials and frontier firms, about one quarter of the 1.6 gain estimated from Claude conversations; modest holds it fixed, extreme reaches 0.80 by 2030.
- Trial and frontier basis: Brynjolfsson et al. (2025), Huang et al. (2025), and Demirer et al. (2026) for the 0.30-0.45 anchor; Tamkin and McCrory (2025) for the 1.6 conversation-based comparison.
- Diffusion context: 2030 diffusion below recent rapid frontier LLM (Large Language Model) adoption (Bick, Blandin, and Deming, 2024), but historical diffusion was much slower (Griliches, 1957; David, 1990; Comin and Hobijn, 2010).
- Census detail: the 18% firm-use and 23% generative-use figures come from the Business Trends and Outlook Survey and its 2026 AI supplement (U.S. Census Bureau, 2026; Bonney et al., 2026).
- Why scenarios coincide early: each path is a logistic through the same mid-2026 anchor with its own slope, so pre-2026 paths differ by only tenths of a percent of GDP.

## 3.4 Disruptiveness

- Automation share psi is the fraction of AI-performed instances done outright by AI rather than with a worker: 0.5 matches chat use today and 0.9 is an agentic-use norm, based on Anthropic Economic Index mode-of-use classification (Appel et al., 2025), about half automation on Claude.ai and about three quarters on the API.
- Reinstatement ratio rho is new labor tasks per automated task: 0.5 matches 1987-2017 history when new tasks ran at about half of automated ones (Acemoglu and Restrepo 2019 decomposition; 1947-87 they roughly kept pace); extreme sets 0, meaning AI creates no new human tasks.
- Search discount mu and posting speed theta_H govern re-employment speed; neither is precisely estimable because AI has not yet displaced many workers.
- Closest evidence is past employment-unemployment-employment episodes: CPS implies mu ~ 0.17, used in the modest scenario.
- Two reasons AI displacement may be harder: within-cognitive heterogeneity (sales and office cross at 28% versus managers and professionals at 10%, the latter implying mu ~ 0.09) and congestion when many search at once for jobs not yet created; hence substantial mu = 0.08 and extreme mu = 0.04.
- Posting speed theta_H closes one tenth, one quarter, and one half of the all-other group's shortfall per month in the three scenarios; mu and theta_H jointly set absorption, so unemployment rises by cognitive releases minus all-other absorption.
- Rigidity xi sets how fast the cognitive wage moves toward clearing: the gap shrinks by factor xi per year; xi = 0.5 in all scenarios means a half-life of one year.
- Motivation for xi = 0.5: stayers face rigid wages reset about yearly with rare nominal cuts (Barattieri et al., 2014; Grigsby et al., 2021), suggesting xi near 0.9, while changers face flexible wages moving with productivity and 10-20% displaced-worker losses on occupation change; large visible permanent shocks erode rigidity, as in 2009, 2020, and 2021-23 inflation when real wages fell several percent in two years; stickier alternatives xi = 0.75 and 0.9 are reported in Section 4.6.
- New-hire flexibility evidence: new hires’ wages move almost one for one with productivity (Haefke et al., 2013).
- Displaced-worker loss evidence: losses of ten to twenty percent, concentrated on occupation changers (Jacobson et al., 1993; Davis and von Wachter, 2011; Huckfeldt, 2022; Braxton and Taska, 2023).
- Real-wage arithmetic: a real wage falling only through inflation takes a decade to close a large gap; nominal cuts became common in 2009 and 2020.
- Trade-off of stickier wages: higher xi means more unemployment and a smaller wage decline.

**Covers:** Section 3 intro, Table 1, Sections 3.1-3.4
