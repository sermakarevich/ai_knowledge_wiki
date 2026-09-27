> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Production, AI Scenarios, and Factor Shares
**In one sentence:** Output is a constant-returns task-based aggregate with gross-complementary tasks, competitive factor assignment, five AI scenario parameters, and a factor-price frontier where measured total factor productivity (TFP — output growth not explained by more inputs) gains flow to wages unless inelastic capital pushes up rental rates and displaces cognitive workers.

## Key points
- Tasks are gross complements with elasticity across tasks `σ = 0.5`, so cheaper AI instances gain expenditure share and become the weak link rather than collapsing in price.
- AI is described by five objects: affected mass `m`, diffusion share `d`, log gain `a`, automation share `ψ`, and reinstatement ratio `ρ`, with `m·d` the fraction of instances AI performs and `m·d·a` that fraction times gain.
- Measured TFP rises by `Δ ln TFP ≈ s_L,t0·m·d·a` regardless of automation versus augmentation, because only the unit-cost decline weighted by expenditure share matters.
- The factor-price frontier `s_L,t0·Δ ln w + s_K,t0·Δ ln r ≈ s_L,t0·m·d·a` splits the same TFP gain between wages and capital rents, so each 1% rise in rents cuts wages by `s_K,t0/s_L,t0 = 2/3%`.
- At fixed rental rates wages track productivity `m·d·a`, not net displacement `(1−ρ)·ψ·m·d`; displacement moves the labor share and capital demand and reaches wages only through the rental rate.
- Wages can fall below the no-AI path when small cost savings are paired with large task transfers and scarce capital — so-so automation — formalized by a threshold capital-supply elasticity `ε*`.
- Target employment in unaffected occupations rises with output and falls with wages with elasticity `σ`, forcing cognitive employment down by a size-scaled amount and requiring reallocation plus frictional unemployment.

---
## 2.1.1 Technology and factor markets
Task-based constant-returns technology in the tradition of Zeira (1998), Autor et al. (2003), Acemoglu and Autor (2011), and Acemoglu and Restrepo (2018). Output is a CES (constant-elasticity-of-substitution) aggregate over task instances:

`Y_t = ( Σ_i ω_i^{1/σ} y_{i,t}^{(σ−1)/σ} )^{σ/(σ−1)}` (1)

where `Y_t` is final output, `y_{i,t}` is output of an instance of task `i`, and weights `ω_i` with `Σ_i ω_i = 1` are base-period expenditure shares. A task is a type of work, such as reviewing a contract or taking a patient's history. An instance is a single performance, for example one contract review. Instances of a task share its weight equally. AI arrives instance by instance: some contracts are reviewed with AI while others are not, as separate entries with their own prices and quantities. Parameter `σ` is the elasticity of substitution across instances, of the same task or different tasks — the elasticity across tasks. An AI-performed and human-performed instance of the same task are imperfect substitutes with the same elasticity `σ`.

The paper sets `σ = 0.5`, so tasks are gross complements, following Acemoglu and Restrepo (2022) tracing to Humlum (2019). Estimates range below to above one; Jones and Tonetti (2026) assume even lower.

Each instance can be produced by labor or capital:

`y_{i,t} = A_t·α_{L,i,t}·l_{i,t} + α_{K,i,t}·k_{i,t}` (2)

where `l_{i,t}` and `k_{i,t}` are labor and capital per instance, `α_{L,i,t}` and `α_{K,i,t}` are task-specific factor productivities that AI shifts, and `A_t` is the stock of ideas which augments labor on every task and is taken as given here. Labor-augmenting `A_t` supports a balanced growth path without AI; augmenting both factors has only small effects over this horizon. Capital and labor are perfect substitutes within a task and, since `σ < 1`, gross complements across tasks. After assignment, technology is a constant-returns aggregate of total capital `K_t = Σ_i k_{i,t}` and labor `L_t = Σ_i l_{i,t}`.

Without unemployment (introduced in Section 2.3), labor `L_t` is supplied exogenously at wage `w_t` clearing the labor market; capital `K_t` is rented at rate `r_t` clearing the capital market. Markets are competitive, so each instance is priced at unit cost and assigned to the cheaper factor:

`p_{i,t} = c_{i,t} = min{ w_t / (A_t·α_{L,i,t}), r_t / α_{K,i,t} }` (3)

so capital performs instance `i` if and only if `α_{K,i,t} / (A_t·α_{L,i,t}) > r_t / w_t`. Ranking by capital's comparative advantage `α_{K,i,t} / α_{L,i,t}`, equilibrium is a threshold rule as in Acemoglu and Restrepo (2018). With the final good as numeraire, expenditure shares and price index are:

`s_{i,t} ≡ p_{i,t}·y_{i,t} / (P_t·Y_t) = ω_i·(c_{i,t} / P_t)^{1−σ}`, `P_t = ( Σ_j ω_j·c_{j,t}^{1−σ} )^{1/(1−σ)} ≡ 1` (4)

where `P_t` is the final-good price index.

Let `L_t` (calligraphic set in paper) denote instances performed by labor. Labor and capital shares and wage identity:

`s_{L,t} = Σ_{i ∈ labor} s_{i,t} = w_t·L_t / (P_t·Y_t)`, `s_{K,t} ≡ 1 − s_{L,t}`, `Δ ln w_t = Δ ln(Y_t/L_t) + Δ ln s_{L,t}` (5)

The wage identity holds exactly: any two of wage, output per worker, and labor share determine the third. Base labor share `s_{L,t0} = 0.6`.

In base period `t0 = 2024`, units make all unit costs equal and `s_{i,t0} = ω_i`. Task importance is its initial share of labor payments: `m_i ≡ s_{i,t0} / s_{L,t0} = ω_i / s_{L,t0}`. By construction `Σ_i m_i = 1` over labor tasks. After `t0`, shares `s_{i,t}` move with relative unit costs. Here `Δ` means deviation from the no-AI path and `ln` differences are approximately percent changes.

Capital supply: demand follows from the capital share, `K_t = s_{K,t}·P_t·Y_t / r_t`. Supply is upward-sloping relative to the no-AI path with constant rental `r̄`:

`Δ ln K_t = ε·Δ ln r_t` (6)

where `ε` is the capital-supply elasticity (percent more capital per percent higher rent). Reduced form of Moll, Rachel, and Restrepo (2022). As `ε → ∞` the rate is pegged at `r̄` and any capital is forthcoming; at `ε = 0` capital does not respond. Returns accrue to owners. Net return reported as `r_t − δ`, with `r̄ = 0.115` and depreciation `δ = 0.05` per year, so net return 6.5% without AI and capital-output ratio `s_{K,t0} / r̄ = 3.5`. Footnote mapping: Moll et al. use `Δ ln K_t = η·Δ(r_t − δ)` with `η = 50`; with constant `δ`, `Δ(r_t − δ) ≈ r̄·Δ ln r_t`, so agreement to first order when `ε = η·r̄ ≈ 50 × 0.115 ≈ 6`. They call `η = 50` conservative; the paper sets `ε = 3`, half that value, because steady states take decades.

No-AI economy is a balanced growth path: ideas `A_t` grow at `g`, labor force `L_t` at `n`, rental constant at `r̄`, shares constant. Wage and output per worker grow at `g`, capital at `g + n`, measured TFP at `s_{L,t0}·g`. Calibration `g = 1.67%` per year so `g_A ≡ s_{L,t0}·g = 1%` TFP growth, `n = 0.33%` (Bureau of Labor Statistics range), GDP without AI `g + n = 2%`.

Two occupation groups (islands): cognitive `C` (management, professional, sales, office), whose tasks AI affects, and all other `N` (manual and interpersonal), whose tasks it does not. Base expenditure shares `s_{C,t0} + s_{N,t0} = s_{L,t0}`, employment `l_{C,t}` and `l_{N,t}`. Employment is measured as shares of labor force `L_t` growing at `n`; write `L` without subscript for the normalized constant labor force, so `l_{C,t} + l_{N,t} = L`. Workers are homogeneous; with full employment and free mobility they earn common wage `w_t` (group-specific wages only in Section 2.3 transition). Consequences: AI forces some `C` workers to switch, and inter-group moves require search, raising unemployment. AI changes the division between groups and the between-jobs fraction.

## 2.1.2 AI scenarios
An AI scenario is largely paths for five exogenous objects. At `t`, AI affects subset `A_t` of tasks, all cognitive, with affected mass:

`m_t ≡ Σ_{i ∈ A_t} m_i` — the fraction of the economy's tasks that AI affects.

On each affected task `i`, diffusion share `d_{i,t}` is the fraction of the task's instances actually performed with AI, and gain `a_{i,t}` is the log productivity gain per AI-performed instance, or equivalently the log decline in the instance's unit cost. Aggregates: `d_t ≡ Σ_{i ∈ A_t} m_i·d_{i,t} / m_t` is mass-weighted diffusion, and `a_t ≡ Σ m_i·d_{i,t}·a_{i,t} / Σ m_i·d_{i,t}` is average gain over AI-performed instances, so `Σ_i m_i·d_{i,t}·a_{i,t} = m_t·d_t·a_t` identically. All three are cumulative from the pre-AI benchmark. Products read like `m_t`: `m_t·d_t` is the fraction of the economy's task instances that AI performs, and `m_t·d_t·a_t` is that fraction times the gain on each.

Augmentation versus automation: under augmentation AI raises worker productivity `α_{L,i,t}` on that instance by `a_{i,t}` log points. Under automation an AI system performs the instance outright with capital; AI raises capital productivity `α_{K,i,t}` so that at the no-AI rate `r̄`, unit cost `r̄ / α_{K,i,t} = e^{−a_{i,t}}·w̄_t / (Ā_t·α_{L,i})`, that is `a_{i,t}` log points below labor's unit cost without AI (bars mark no-AI path). In either form, unit cost falls by `a_{i,t}` at no-AI factor prices.

Fourth primitive, automation share `ψ_t ∈ [0,1]`, is the fraction of AI-performed instances that are automated rather than augmented. Technology determines it; firms take it as given. The gain on an automated instance is available only if capital performs it; on an augmented instance only if a worker performs it. A firm keeps an automated instance on capital as long as `Δ ln r_t − Δ ln w_t ≤ a_{i,t}` (7) — AI has not raised rents relative to wages by more than the gain.

Fifth object, reinstatement ratio `ρ ∈ [0,1]`, is the mass of newly created labor tasks as a fraction of the mass of automated tasks, in the spirit of Acemoglu and Restrepo (2019) and Autor et al. (2024). A mass `ψ_t·m_t·d_t` of labor tasks is automated and mass `ρ·ψ_t·m_t·d_t` of new labor tasks is created, so labor-task mass changes by `−(1−ρ)·ψ_t·m_t·d_t` net. New tasks belong to cognitive occupations, enter at the same unit cost as remaining labor tasks, offset displacement one-for-one in the affected wage bill, add no separate variety or weak-link term, and leave the factor-price frontier unchanged. Labor is mobile within a group so new tasks are staffed immediately.

Time paths: affected mass and diffusion follow logistics, log gain is linear:

`m_t = m̄ / (1 + e^{−κ_m·(t−t_m)})`, `d_t = d̄ / (1 + e^{−κ_d·(t−t_d)})`, `a_t = a_0 + g_a·(t − t0)` (8)

where overbars are asymptotes, `κ` speeds, `t_m,t_d` midpoints, `a_0` initial gain and `g_a` its growth. Automation share `ψ_t` and reinstatement `ρ` are held constant in the three scenarios. Exact solutions use `=`; first-order approximations use `≈`.

## 2.1.3 Measured TFP and the factor-price frontier
On fraction `d_{i,t}` of task `i` performed with AI, unit cost falls by `a_{i,t}` log points whether augmented or automated. By Hulten's theorem (Hulten, 1978), aggregate productivity gain sums cost declines weighted by Domar weights (sales-to-GDP ratios), here expenditure shares `ω_i`. Dividing `ω_i` by `s_{L,t0}` gives mass `m_i`, so measured TFP rises by:

`Δ ln TFP_t ≈ Σ_i ω_i·d_{i,t}·a_{i,t} = s_{L,t0}·Σ_i m_i·d_{i,t}·a_{i,t} = s_{L,t0}·m_t·d_t·a_t` (9)

This does not involve automation share since only the unit-cost decline matters, identical in both forms.

Distribution is separate. With constant returns and competitive pricing, `P_t·Y_t = w_t·L_t + r_t·K_t`. Measured TFP growth equals its dual, share-weighted factor-price growth. With final good as numeraire, `d ln TFP_t = s_{L,t}·d ln w_t + s_{K,t}·d ln r_t`. Applied to (9):

`s_{L,t0}·Δ ln w_t + s_{K,t0}·Δ ln r_t ≈ s_{L,t0}·m_t·d_t·a_t` (10)

The two factor prices absorb the whole TFP gain whatever `ψ_t`, `ρ`, `σ`. If rent does not move (as at `ε = ∞`), wage rises by full gain `Δ ln w_t ≈ m_t·d_t·a_t` (Caselli and Manning, 2019). If capital adjusts slowly and rents rise, wages rise less: each percent rise in rents lowers wages by `s_{K,t0} / s_{L,t0} = 2/3%`. Wages can fall relative to no-AI when `s_{K,t0}·Δ ln r_t > s_{L,t0}·m_t·d_t·a_t`.

Equations (9)–(10) hold to first order for any constant-returns efficient economy; gains may be large so simulations use exact solutions with approximations for intuition. Illustration (substantial-change scenario, start of 2030): `m_t = 30%` of tasks affected, `d_t = 40%` of their instances used with AI, `a_t = 0.45` log-point unit-cost decline. Then AI performs `m_t·d_t = 12%` of instances and `Δ ln TFP_2030 ≈ 0.6 × 0.30 × 0.40 × 0.45 = 0.032`, about 3% (exact 0.029). With rent at `r̄`, all accrues to labor and wage is `m_t·d_t·a_t = 0.054` (5.4%) above no-AI. With `ε = 3`, rent is 4.6% above `r̄`, capital's term is `0.4 × 0.045 = 0.018`, and wage is 1.9% above no-AI rather than 5.5%.

## 2.1.4 First-order solutions
Key first-order equations:

`Δ ln w_t ≈ m_t·d_t·a_t − (s_{K,t0} / s_{L,t0})·Δ ln r_t`,
`Δ ln r_t ≈ 1 / (ε + σ/s_{L,t0}) · [ m_t·d_t·a_t + ((1−ρ) − (1−σ)·a_t)·ψ_t·m_t·d_t / s_{K,t0} ]`,
`Δ ln s_{L,t} ≈ −(1−ρ)·ψ_t·m_t·d_t + (1−σ)·ψ_t·m_t·d_t·a_t − (1−σ)·(s_{K,t0} / s_{L,t0})·Δ ln r_t`,
`Δ ln(Y_t/L_t) ≈ m_t·d_t·a_t + (1−ρ)·ψ_t·m_t·d_t − (1−σ)·ψ_t·m_t·d_t·a_t − σ·(s_{K,t0} / s_{L,t0})·Δ ln r_t` (11)

Wage equation comes from TFP expression (10). Equating capital demand to supply (6) gives the rental gap: bracket is capital AI calls for at unchanged rent — capital keeps pace with output the gains produce, `m_t·d_t·a_t`, plus each automated instance shifting its wage bill to capital and raising output, together calling for `ψ_t·m_t·d_t / s_{K,t0}` more capital (less reinstatement and less expenditure substitution sends back to labor). Rent rises to reconcile demand with supply; demand falls with rent at elasticity `σ / s_{L,t0}` and supply rises at `ε`.

Labor share has three channels. First, automation reassigns tasks: an automated instance's entire wage bill moves to capital however small the saving, so net of reinstatement labor share falls by `(1−ρ)·ψ_t·m_t·d_t`. Second, cost declines on instances labor keeps offset only `(1−ψ_t)·m_t·d_t·a_t` of the wage rise; remaining labor instances become dearer relative to automated ones by `ψ_t·m_t·d_t·a_t` on average. Because `σ < 1`, demand substitutes away less than proportionately — the weak link — so their expenditure share rises, adding back `(1−σ)·ψ_t·m_t·d_t·a_t`. Third, when rents rise, capital's instances become dearer and expenditure follows them, lowering labor share by `(1−σ)·(s_{K,t0} / s_{L,t0})·Δ ln r_t`.

Output per worker follows from labor share in (5); capital from the capital share, `Δ ln K_t = Δ ln s_{K,t} + Δ ln(Y_t/L_t) − Δ ln r_t`.

Two insights. First, at fixed rent wages track productivity `m_t·d_t·a_t`, not net displacement `(1−ρ)·ψ_t·m_t·d_t`. Displacement changes task counts, labor share, and capital demand, reaching wages only via rents. This differs from Caselli and Manning (2019), where perfectly elastic long-run capital fixes rates so technical change cannot lower average wages. Second, wage declines need displacement to outweigh savings with scarce capital: automation transfers wage bill `(1−ρ)·ψ_t·m_t·d_t` regardless of saving size, while distributable saving from (10) is `s_{L,t0}·m_t·d_t·a_t`. If saving per automated task is small relative to transfer and little capital arrives, rents must rise enough to rationalize the transfer; if that exceeds the saving, wages fall below no-AI — labor loses tasks and faces scarce expensive capital. This is so-so automation (Acemoglu and Restrepo, 2019). At baseline `ε = 3` wages rise in 2030 in every scenario, but fall if `ε` is small enough:

`ε > ε_t* ≈ 1/s_{L,t0}·[ s_{K,t0} − σ + ψ_t·(1−ρ)/a_t − (1−σ) ]` (12)

for wages to rise; labor keeps fraction `(ε − ε_t*) / (ε + σ/s_{L,t0})` of the pegged-rent wage gain.

## 2.1.5 Employment in the two groups
Write `l*_{o,t}` for employment in group `o` when workers move freely at no cost at a common wage — the groups' target toward which employment adjusts. The cognitive target is pinned down via unaffected `N` workers.

Key result: AI does not affect `N` task productivity, so each `N` cost depends on the wage, not the automation gain. Labor demand on those tasks is ordinary CES demand at price `w_t`: rises one-for-one with output, falls with wage at elasticity `σ`. As long as AI raises wages with output, `N` employment rises by less than output. With fixed labor supply, `N`'s gains are `C`'s losses, so `C`'s proportional decline is `N`'s rise scaled by relative size `s_{N,t0} / s_{C,t0}`:

`l̃_{N,t} ≡ ln(l*_{N,t} / l_{N,t0}) = Δ ln(Y_t/L_t) − σ·Δ ln w_t`, `(l_{C,t0} − l*_{C,t}) / l_{C,t0} = (s_{N,t0} / s_{C,t0})·(l*_{N,t} − l_{N,t0}) / l_{N,t0}` (13)

When `s_N / s_C < 1`, as here, cognitive employment falls by less than `N` rises, hence by less than output rises; cognitive employment loss is smaller than GDP gain.

Equation (13) gives both targets once output and wage impacts are known; Section 2.1.4 gave them to first order. Exact closed form:

Proposition 1 (The model in closed form). Exact solution:

`s_{L,t} = 1 − s_{K,t0} + s_{L,t0}·Σ_i [ ψ_{i,t}·m_i·d_{i,t}·e^{−(1−σ)·a_{i,t}} − ρ_i·e^{(1−σ)·Δ ln r_t} ]` (14)

`t̃ shorthand l̃_{N,t} = −ln( 1 − Σ_i m_i·d_{i,t}·[ 1 − ρ_i·ψ_{i,t} − (1−ψ_{i,t})·e^{−(1−σ)·a_{i,t}} ] )` (15)

`Δ ln w_t = (Δ ln s_{L,t} + l̃_{N,t}) / (1−σ)`, `Δ ln(Y_t/L_t) = Δ ln w_t − Δ ln s_{L,t}` (16)

where `Δ ln s_{L,t} = ln(s_{L,t} / s_{L,t0})`, targets follow from `l̃_{N,t}` via (13).

`Δ ln K_t = ln((1 − s_{L,t}) / s_{K,t0}) + Δ ln(Y_t/L_t) − Δ ln r_t` (17)

Rental gap is the unique root of capital-market clearing `ε·Δ ln r_t = Δ ln K_t` (18), whose right side (17) strictly decreases in `Δ ln r_t`; at `ε = ∞` root is zero. With uniform parameters the sums are `ψ_t·m_t·d_t·[ e^{−(1−σ)·a_t} − ρ ]` and `m_t·d_t·[ 1 − ρ·ψ_t − (1−ψ_t)·e^{−(1−σ)·a_t} ]`.

Intuition from first-order (11) into (13), or expanding (15):

`l̃_{N,t} ≈ (1−ρ)·ψ_t·m_t·d_t + (1−σ)·(1−ψ_t)·m_t·d_t·a_t`, `l̃_{C,t} ≈ −(s_{N,t0} / s_{C,t0})·l̃_{N,t}` (19)

where `l̃_{C,t} ≡ ln(l*_{C,t} / l_{C,t0})` is required log change in cognitive employment; labels under terms are net displacement and labor released by the gains. Same forces push workers out of cognitive jobs: net displacement (automated tasks net of created tasks) plus `(1−σ)` times gain on augmented instances. Each augmented instance needs `a_t` log points less labor, but complementarity raises demand by `σ·a_t` because it is cheaper, so only fraction `1 − σ` of saved labor is released. At `σ = 0.5`, half of every gain is spent on more of the same task.

**Covers:** Section 2.1 (2.1.1-2.1.5)
