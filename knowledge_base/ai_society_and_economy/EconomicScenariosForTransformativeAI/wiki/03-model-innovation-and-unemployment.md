> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Innovation and Unemployment in the Model
**In one sentence:** AI raises research spending by enlarging GDP but adds little to idea growth by 2030, while sticky cognitive wages and slow occupational matching turn displacement into temporary unemployment.

## Key points
- **Ideas are semi-endogenous via a research budget:** ideas stock `A_t` is produced from research input `R_t`, and research is a share `iota_R,t` of GDP funded by a lump-sum tax, so AI raises `R_t` mainly because AI raises GDP (the level channel).
- **Growth-rate effect is small by construction:** a 5% GDP gap raises idea growth by less than 5% — e.g. measured TFP (Total Factor Productivity) growth from 1.00% to 1.05% per year — because the GDP level gain applies to a ~1% baseline growth rate, and further damped if `lambda < 1` and `Delta ln A_t > 0`.
- **Long-run vs realized idea gains differ sharply:** on the extreme path `Delta ln R_t` reaches 0.28 in 2030, implying a long-run ideas level ~10% above no-AI, but only 0.6% above no-AI is realized by 2030 because cumulation takes decades.
- **Measured TFP mixes ideas and AI level effects:** the Solow residual combines growth in `A_t` and the static AI term `m_t d_t a_t`, both entering with the labor share as Domar weight: `Delta ln TFP_t ≈ s_L,t0 Delta ln A_t + m_t d_t a_t`.
- **Unemployment comes from two frictions:** a cognitive wage that closes only a fraction of its gap to market-clearing each month, forcing layoffs/rationing, plus a search-and-matching process that takes time to re-employ displaced workers.
- **Matching is hard across occupations:** effective search is `S_C = U_C + mu U_N`, `S_N = mu U_C + U_N`, with normal-times discount `mu-bar = 0.17` (1 in 7 job-finders change groups); scenarios set `mu = 0.17, 0.08, 0.04` and hiring-posting speed `theta_H = 0.10, 0.25, 0.50`.
- **Normal-times baseline is CPS-calibrated:** unemployment pool `U-bar = 3.8%` of labor force, monthly quits `q-bar_C = 0.63%` and `q-bar_N = 1.40%`, aggregate finding rate ~0.23/month, mean vacancy filling rate 0.65/month; e.g. software engineer does not instantly become electrician or nurse.

---
## 2.2.1 Ideas production and research funding
So far the ideas stock `A_t` was held at its no-AI path. This section makes it semi-endogenous, with AI entering through resources devoted to research.

Ideas are produced from research input `R_t`, in the tradition of Romer (1990) and Jones (1995):

```
A-dot_t = nu R_t^lambda A_t^{phi_R}
g_A,t = nu R_t^lambda A_t^{phi_R - 1}    (20)
```

- `A-dot_t` / `g_A,t`: change / growth rate of ideas stock; `R_t`: research input (goods/compute/equipment).
- `nu`: idea-production scale; `lambda <= 1`: returns to research input.
- `phi_R < 1`: returns to existing ideas; fishing-out — gains harder as `A_t` grows.

Research uses final output, as in the lab-equipment model of Rivera-Batiz and Romer (1991). The economy devotes fraction `iota_R,t` of GDP to research, funded by a lump-sum tax on households; government pays researcher salaries, equipment and compute from that budget:

```
Y_t = C_t + I_t + R_t ,   R_t = iota_R,t Y_t    (21)
```

- `Y_t`: GDP; `C_t`: consumption; `I_t`: investment; `R_t`: research spending.
- `iota_R,t`: research share of GDP; rises exogenously to capture rising R&D share; no need to split `C_t` vs `I_t`.

Impact effects. AI raises research input because the budget is a share of GDP and AI raises GDP: the level channel makes the economy more productive, and a given share of a bigger economy is a bigger research budget. Log-differencing `R_t = iota_R,t Y_t` against no-AI path gives:

```
Delta ln R_t = Delta ln Y_t    (22)
```

where `Delta ln Y_t` is the GDP gap and the research share, common to both paths, drops out. AI automates research by automating the goods used to produce ideas.

Impact on growth. Writing `Delta g_t = g_A,t - g` for the growth-rate gap and log-differencing (20):

```
Delta ln g_t = lambda Delta ln R_t - (1 - phi_R) Delta ln A_t    (23)
```

This is the key equation of the section. The percent gap in the growth rate is smaller than the percent gap in research inputs, which in turn equals the GDP gap.

Why small by 2030:

- The GDP gap is a level gain, but here it applies to a growth rate around 1% per year.
- A 5% GDP gap therefore raises idea growth by less than 5%, e.g. raising measured TFP growth from 1.00% to 1.05%.
- Even smaller since `Delta ln A_t > 0` and to the extent `lambda < 1$.

Accumulation over time. A one-time rise in `R` keeps adding to `A_t` year after year. Because returns to ideas are decreasing (`phi_R < 1`), a given `R` is consistent with baseline growth `g` at only one ideas level: setting `g_A,t = g` in (20) gives `A* = (nu R^lambda / g)^{1/(1-phi_R)}`, so `A* proportional to R^{lambda/(1-phi_R)}` and a held uplift moves long-run ideas by:

```
Delta ln A* = gamma Delta ln R,   gamma = lambda / (1 - phi_R) = 1 / 2.86 ≈ 0.35    (24)
```

where `gamma` uses Bloom et al. (2020). Equation (24) gives the order of magnitude. On the extreme path, uplift `Delta ln R_t` reaches 0.28 in 2030, so ideas are headed for ~10% above no-AI path (even less in TFP units). That is the most the channel delivers for a one-off change of that size. Realized values by 2030 are smaller because long-run gains take decades: on the extreme path ideas are just 0.6% above no-AI in 2030.

No feedback from ideas to AI gains `a_t` in this setup. Research raises productivity of everything people do but does not itself automate tasks. Instead `a_t` and `psi_t` are scenario parameters. In that sense recursive self-improvement (RSI) gains are hard-coded into `a_t`.

## 2.2.2 Measured TFP
The ideas stock `A_t` is not what an econometrician would measure as TFP (Total Factor Productivity). Measured TFP is the Solow residual:

```
d ln TFP_t = d ln Y_t - s_L,t d ln L_t - s_K,t d ln K_t
```

- `s_L,t`, `s_K,t`: labor/capital shares; `L_t`, `K_t`: labor/capital inputs.
- `g_w,t`, `g_r,t`: wage / rental-rate growth; `s_L,t0`: base labor share; `m_t d_t a_t`: AI level term.

Because factor payments exhaust output, the residual equals its dual:

```
g_TFP,t = s_L,t g_w,t + s_K,t g_r,t    (25)
```

Both the AI level term `m_t d_t a_t` and the growth term `Delta ln A_t` enter the residual with the labor share, its Domar weight. Ideas lower the cost of every labor instance by `d ln A_t`, and the level channel lowers the cost of affected instances by `a_t`. To first order, the cumulative gap vs no-AI is:

```
Delta ln TFP_t ≈ s_L,t0 Delta ln A_t + m_t d_t a_t    (26)
```

## 2.3.1 Separations and job openings
Flows move employment toward targets at monthly horizon. In normal times a pool `U-bar` of unemployed workers is between jobs, so base employment is `l_C,t0 + l_N,t0 = L - U-bar`. Targets are adjusted for steady-state unemployment, with `l_N,t0 = (s_N,t0 / s_L,t0)(L - U-bar)`, and also sum to `L - U-bar`. Head counts are shares of labor force `L_t` (grows at `n` with or without AI); rates (`q, f, pi, theta_H`) are per month.

Workers in group `o in {C, N}` — C = cognitive, N = all-other — face quits plus displacement layoffs. Quit rate:

```
q_o,t = q_o^X + q_o^T (f_o,t-1 / f-bar_o)    (27)
```

- `q_o^X` / `q_o^T`: exogenous base quits / sensitivity to prospects; `f_o,t-1 / f-bar_o`: finding rate vs steady state.
- In normal times `q_o,t = q_o^X + q_o^T = q-bar_o`.

Each month employers compare employment with next month's target. On scenario paths cognitive target only falls and other only rises, so cognitive has an employment overhang and other a shortfall, as log gaps:

```
G_C,t = max{0, ln l_C,t - ln l*_C,t+1},   B_N,t = max{0, ln l*_N,t+1 - ln l_N,t}    (28)
```

Expanding occupations post openings for fraction `theta_H` of shortfall per month. Shrinking occupations lay off workers they do not demand at slowly-adjusting wage. Unemployment reflects two frictions: wage falling too slowly to keep displaced employed, and search taking time.

Cognitive wage and layoffs. Let `N_C,t` be cognitive labor force attached to group, employed plus excess cognitive-origin unemployed:

```
N_C,t = l_C,t + max{0, U_C,t - U-bar_C}    (29)
```

Let `w^c_C,t` be wage that would clear cognitive group at `N_C,t`, i.e. if no extra C workers were pushed into unemployment. In normal times it is common wage `w_t`, but during displacement the full-employment wage is even lower.

Cognitive wage is slow to adjust, so market does not clear (Blanchard and Gali 2007):

```
(w_C,t / w_t) = (w_C,t-1 / w_t-1)^{xi_m} (w^c_C,t / w_t)^{1-xi_m},   xi_m = xi^{1/12}    (30)
```

- `w_C,t`: actual cognitive wage; `xi in [0,1)`: yearly rigidity; `xi = 0` clears monthly, `xi -> 1` stays at common wage `w_t`.

At this wage firms adjust employment to labor demand. Employment is predetermined within month, so firms reach demand via separations. Let `l^d_C,t` be labor demanded at `w_C,t`, and `E_t = max{0, l_C,t - l^d_C,t}` excess employment carried into month. Quits from surplus posts are not replaced, and displacements `D_C,t` (“layoffs”) remove rest:

```
D_C,t = max{0, E_t - q_C,t l_C,t}    (31)
```

so cognitive employment is on demand curve from next month. Layoffs are job rationing (Michaillat 2012): while wage exceeds clearing level, firms demand fewer cognitive workers than attached, difference laid off rather than employed at lower wage. While rationing binds, employed cognitive workers are paid marginal product.

Job openings. Firms post openings to replace quits and close fraction `theta_H` of shortfall. For cognitive, shortfall is demand beyond employment `Z_t = max{0, l^d_C,t - l_C,t}`, typically zero; for all-other, log gap `B_N,t` to target. Openings `v_o,t` (flow per month):

```
v_C,t = (max{0, q_C,t l_C,t - E_t} + theta_H Z_t) / pi-bar_C,   v_N,t = (q_N,t + theta_H B_N,t) l_N,t / pi-bar_N    (32)
```

- `pi-bar_o < 1`: normal-times filling rate employers expect.
- At `theta_H = 1` all-other posts entire shortfall at once; `theta_H < 1` spreads postings, standing for recruiting/training capacity.

## 2.3.2 Matching
Separated workers enter unemployment; tracked by origin `U_C,t` and `U_N,t`. They search in both groups, but searching outside origin is disadvantaged, reflecting occupation-specific human capital (Kambourov and Manovskii 2009) otherwise outside model: a software engineer does not become an electrician or nurse at once. Discount `mu in (0,1]` on cross-group search, so effective search per group:

```
S_C,t = U_C,t + mu U_N,t,   S_N,t = mu U_C,t + U_N,t    (33)
```

Hires in group `j` use matching function of den Haan et al. (2000):

```
H_j,t = chi S_j,t v_j,t / (S_j,t^iota + v_j,t^iota)^{1/iota},   j in {C,N}    (34)
```

- Standard curvature `iota = 1.27`, matching efficiency `chi <= 1`.
- Constant returns to scale; filling rate and hires per effective search depend only on tightness `theta_j,t = v_j,t / S_j,t`.
- Filling rate `pi_j,t = H_j,t / v_j,t = chi [1 + theta_j,t^iota]^{-1/iota}`; hires per search `H_j,t / S_j,t = theta_j,t pi_j,t`.
- Both lie between zero and `chi`, so hires never exceed searchers or openings — why this form is used instead of Cobb-Douglas, which needs caps that kink simulated paths. As `iota -> infinity`, function becomes `chi min{S_j,t, v_j,t}`.

Job-finding rates by origin (worker supplies 1 unit in origin group, `mu` in other):

```
f_C,t = H_C,t / S_C,t + mu H_N,t / S_N,t,   f_N,t = mu H_C,t / S_C,t + H_N,t / S_N,t    (35)
```

A laid-off cognitive worker's chance is high when other occupations post heavily and `mu` near one, low otherwise. Employment evolves via quits, layoffs and hires; unemployment pools evolve via separations minus finders:

```
l_o,t+1 = (1 - q_o,t) l_o,t - D_o,t + H_o,t,   o in {C,N}    (36)
U_o,t+1 = U_o,t + q_o,t l_o,t + D_o,t - f_o,t U_o,t,   o in {C,N}    (37)
```

where `D_N,t = 0`, and a hire into `j` counts as `j` worker thereafter. Since `f_C,t U_C,t + f_N,t U_N,t = H_C,t + H_N,t`, every hire leaves pool and every separation enters it, so `l_C + l_N + U_C + U_N = L` always. New labor-force entrants join groups/pool proportionally, so laws hold in shares. All separations pass through unemployment, including group changers; focus is scenarios where displaced workers cross through unemployment.

Steady state. Hiring replaces quits and each origin inflow equals outflow:

```
H-bar_o = q-bar_o l_o,t0 = f-bar_o U-bar_o
f-bar_o = sum_j (H-bar_j / S-bar_j) mu-bar_o_j
pi-bar_o = chi [1 - (H-bar_o / chi S-bar_o)^iota]^{1/iota}    (38)
```

for `o in {C,N}`, where `mu-bar_o_o = 1` and `mu-bar_C_N = mu-bar_N_C = mu-bar`, `S-bar_j` is (33) at steady stocks with `mu-bar`, and `U-bar_C + U-bar_N = U-bar`. First conditions split pool and imply aggregate finding rate `f-bar = q-bar (L - U-bar)/U-bar`. Third inverts matching function for normal filling rates used in (32), solvable while hiring per search is below `chi`.

Calibration: `chi` set so employment-weighted mean of `pi-bar_C`, `pi-bar_N` is 0.65/month (daily model of Davis et al. 2013 applied to JOLTS 2010-19: 4.0% per working day, 26-day mean duration). Gap between `chi` and `pi-bar_o` is room for filling rate to rise when many displaced search at once.

Normal times: pool `U-bar = 3.8%` of labor force; quits `q-bar_C = 0.63%` and `q-bar_N = 1.40%` per month (0.92% economy-wide split by CPS (Current Population Survey) separation proportions); implied aggregate finding rate 0.92 × 96.2/3.8 ≈ 0.23/month vs 0.22 in data. Pool splits into 1.76% cognitive-origin and 2.08% other-origin (2.9% of one group, 5.4% of other). Filling rates 0.66 and 0.64, `chi = 0.76`.

Search discount `mu-bar = 0.17`, calibrated so 1 in 7 job-finders change groups as in CPS. Steady state evaluated at `mu-bar` in every scenario, so `U-bar` unaffected by AI by construction.

Two key search parameters are scenario objects: modest, substantial, extreme set `mu = 0.17, 0.08, 0.04` in (33)/(35) and `theta_H = 0.10, 0.25, 0.50`. Modest keeps normal-times discount; others put displaced cognitive workers at steeper disadvantage switching occupations.

## 2.3.3 Summary of the model with unemployment
Simulated economy features unemployment that initially rises as labor market adjusts to AI. Cognitive workers are paid sticky wage `w_C,t`, while all-other workers are paid marginal product `w_N,t`. Full equation system solved in simulations is stated in Table A.1.

**Covers:** Sections 2.2 (2.2.1-2.2.2) and 2.3 (2.3.1-2.3.3)
