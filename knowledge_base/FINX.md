# FINX — Investor Podcast Signal Aggregation

Extracted from 5 YouTube episodes via the `youtube_transcript` MCP. Each episode was processed by a dedicated subagent that pulled a tickers-to-buy / tickers-to-sell / tickers-owned summary, with reasoning faithful to the speakers.

## Sources

| # | URL | Video ID |
|---|-----|----------|
| 1 | https://www.youtube.com/live/P4cVW9nss9I | P4cVW9nss9I |
| 2 | https://www.youtube.com/live/LFJyM-gXfPc | LFJyM-gXfPc |
| 3 | https://www.youtube.com/live/lijNh0CLXbk | lijNh0CLXbk |
| 4 | https://www.youtube.com/live/6z0BIC0zC54 | 6z0BIC0zC54 |
| 5 | https://www.youtube.com/live/BR4ZzlzPzLo | BR4ZzlzPzLo |

---

## Cross-video tally

`B` = videos calling it BUY/accumulate. `S` = videos calling it SELL/trim/avoid. `O` = videos where speakers own it. Higher B + O with zero S = stronger consensus.

| Ticker    | Name                      | B   | S       | O   | Videos    | Theme                               |
| --------- | ------------------------- | --- | ------- | --- | --------- | ----------------------------------- |
| **META**  | Meta Platforms            | 4   | 0       | 4   | 2,3,4,5   | Distribution moat + ad/AI engine    |
| **AMZN**  | Amazon                    | 4   | 0       | 4   | 2,3,4,5   | AWS + Trainium + chip biz           |
| **SOFI**  | SoFi Technologies         | 4   | 0       | 5   | 1,2,3,4,5 | Fintech / banking ecosystem         |
| **ARM**   | Arm Holdings              | 4   | 0       | 3   | 1,3,4,5   | CPU bottleneck winner               |
| **HIMS**  | Hims & Hers               | 3   | 0       | 3   | 3,4,5     | GLP-1 / peptide tailwind            |
| **AEHR**  | Aehr Test Systems         | 3   | 0       | 3   | 3,4,5     | AI hardware burn-in testing         |
| **CIFR**  | Cipher Mining             | 3   | 0       | 4   | 1,2,4,5   | AI infra "landlord" / power         |
| **WULF**  | TeraWulf                  | 3   | 0       | 2   | 1,4,5     | AI infra / hyperscaler leases       |
| **NBIS**  | Nebius                    | 2   | 0       | 3   | 1,4,5     | Tier-1 neocloud                     |
| **NOW**   | ServiceNow                | 3   | 0       | 2   | 1,2,3     | AI workflow automation              |
| **AAOI**  | Applied Optoelectronics   | 2   | 0       | 2   | 3,5       | Optical interconnects               |
| **AXON**  | Axon Enterprise           | 2   | 0       | 2   | 1,3       | Public-safety SaaS                  |
| **AVGO**  | Broadcom                  | 3   | 0       | 0   | 3,4,5     | Custom AI silicon                   |
| **AMD**   | AMD                       | 3   | 1 wait  | 0   | 1,3,4,5   | CPU bottleneck                      |
| **MU**    | Micron                    | 3   | 0       | 0   | 1,3,4     | Memory bottleneck                   |
| **NVDA**  | Nvidia                    | 3   | 0       | 1   | 1,2,4     | AI compute monopoly                 |
| **GOOGL** | Alphabet                  | 2   | 0       | 0   | 2,5       | Cloud + TPU ramp                    |
| **PLTR**  | Palantir                  | 1   | 0       | 2   | 2,5       | Bespoke AI delivery                 |
| **DOCN**  | Digital Ocean             | 2   | 1 ST    | 3   | 1,2,4     | Inference cloud                     |
| **INTC**  | Intel                     | 3   | 2       | 1   | 1,3,4,5   | Foundry / packaging — controversial |
| **CRDO**  | Credo                     | 1   | 0       | 1   | 3         | Silicon photonics                   |
| **LITE**  | Lumentum                  | 2   | 0       | 1   | 3,5       | Photonics / laser layer             |
| **LSCC**  | Lattice Semi              | 1   | 0       | 1   | 1         | FPGA mid-market                     |
| **AMKR**  | Amkor                     | 1   | 0       | 1   | 4         | CPU packaging                       |
| **ALAB**  | Astera Labs               | 1   | 0       | 1   | 1         | AI interconnect                     |
| **MELI**  | MercadoLibre              | 1   | 0       | 1   | 1         | LatAm e-commerce                    |
| **RKLB**  | Rocket Lab                | 1   | 1 trim  | 1   | 1         | Space launch                        |
| **CRWV**  | CoreWeave                 | 1   | 0       | 0   | 5         | GPU cloud                           |
| **COHR**  | Coherent                  | 1   | 0       | 0   | 5         | Photonics                           |
| **DDOG**  | Datadog                   | 1   | 0       | 0   | 1         | Observability                       |
| **TSMC**  | TSM                       | 1   | 0       | 0   | 1         | Foundry monopoly                    |
| **PURE**  | Pure Storage              | 1   | 0       | 0   | 2         | Storage rerating                    |
| **QCOM**  | Qualcomm                  | 1   | 0       | 0   | 2         | Edge AI rerating                    |
| **HOOD**  | Robinhood                 | 1   | 1       | 1   | 2,5       | Generational banking                |
| **IBIT**  | iShares Bitcoin ETF       | 1   | 0       | 1   | 4         | BTC exposure                        |
| **TSLA**  | Tesla                     | 0   | 0       | 1   | 4         | Physical-AI long hold               |
| **VIK**   | Viking Therapeutics       | 0   | 0       | 1   | 3         | GLP peptide pipeline                |
| **IRON**  | (Iron Mtn / IRM context)  | 0   | 0       | 3   | 2,4,5     | Power/real-asset hyperscaler        |
| **AMCR**  | Amcor                     | 0   | 0       | 1   | 1         | Basket position                     |
| **CRM**   | Salesforce / SaaS broadly | 0   | 1       | 0   | 5         | Margin compression risk             |
| **NET**   | Cloudflare                | 0   | 1       | 0   | 5         | "Soft AI" rerating                  |
| **SNOW**  | Snowflake                 | 0   | 1       | 0   | 5         | Margin compression                  |
| **CRWD**  | CrowdStrike               | 0   | 1       | 0   | 5         | Caught in SaaS sell-off             |
| **SNPS**  | Synopsys                  | 0   | 1 trim  | 0   | 1         | Profit-take, RSI-stretched          |
| **SOUN**  | SoundHound AI             | 0   | 1       | 0   | 2         | Feature, not platform               |
| **POET**  | POET Tech                 | 0   | 1       | 0   | 3         | Governance red flags                |
| **APP**   | AppLovin                  | 0   | 1 avoid | 0   | 4         | SEC/governance noise                |

---

## Top-of-stack reading

**Highest-conviction BUYS (≥3 buy mentions, owned in ≥3 videos, no sell calls):**
- **META** — distribution moat + 33% ad-engine growth, ~18x earnings, top portfolio holding for multiple speakers.
- **AMZN** — AWS reaccelerating to fastest growth in 15 quarters, $225B+ Trainium commitments, mispriced as a retailer.
- **SOFI** — owned in every single episode; both hosts adding through dips, options structures, "membership growth ignored by market."
- **CIFR** — AI-infra landlord; AWS/Google decade leases; held since $10s.
- **AEHR** — burn-in testing for AI hardware; up 4x in 4 months and still added.
- **HIMS** — bought "the wreckage" at $15–20 from $70 peak, GLP-1/peptide compounding tailwind underestimated.
- **ARM** — merchant AGI CPU breaks the custom-only mould (Graviton/Axion/Cobalt), royalty windfall.
- **NBIS** — tier-1 neocloud, Nvidia engineering partner, early Rubin GPU access.
- **NOW** — 15x FCF, no real AI disintermediation risk, Armis acquisition extends TAM.

**Buy-but-not-owned breakouts (worth fresh-money attention):**
- **AVGO** — 3 buy mentions across 3 videos, $40B+ AI chip run-rate; nobody on these shows is currently sized in.
- **MU** — Daniel "pounding Micron at 100"; Rubin certified; no current ownership disclosed.
- **NVDA** — repeatedly called undervalued; only one host bought this cycle, others see upside but don't own size.

**Controversial / mixed:**
- **INTC** — 3 buy + 2 sell. Bull case: Google/Amazon/SambaNova CPU wins, Terafab consortium. Bear case: trades at "100x forward," already ran ~700%, "wait for pullback."
- **DOCN** — 2 buy + 1 near-term hedge + 3 owned. Long thesis intact (50% growth 2027); near-term sky-high expectations + capacity constraints.
- **RKLB** — 15-bagger for one host, top growth position; small trim only because RSI-stretched, not exit.

**Clear avoids:**
- **SaaS broadly** (CRM/NET/SNOW/CRWD) — structural margin compression as compute costs rise; speakers say "dead money this year, at best a 2027 story."
- **SOUN** — feature layer pretending to be platform; will lose to vertical stacks.
- **POET** — paid promotion history = automatic disqualifier.
- **APP** — too much SEC/governance noise; better risk-adjusted alternatives.
- **SpaceX IPO** — wait for the post-IPO cooldown; offering designed to dump on retail.

**Tactical posture across all 5 videos:**
- QQQ daily RSI 85 → speakers trimming high-RSI winners, building 5–10% cash buffers.
- Dollar allocation rotating from software → hardware/infrastructure (compute, photonics, power, CPUs).
- Mag-7 picks of choice: META + AMZN (not Microsoft, not Apple).
- "Inference cloud / neocloud / AI landlord" theme = NBIS, CIFR, WULF, IRON, DOCN, CRWV.

---

## Per-video extractions

### Video 1 — https://www.youtube.com/live/P4cVW9nss9I

#### Tickers to BUY
- **NVDA** — Both speakers believe Nvidia is undervalued relative to its dominance; one host explicitly told family it's a better alternative than SPY/QQQ at $200 and targets $250 as a "no-brainer." Stock-price lag attributed to sentiment, not fundamentals; one host bought this week.
- **DOCN** — Number-one position for one host; sees a $50B company (5x from ~$10B) on 50% growth guidance for 2027, ~40% EBITDA margins, sticky inference-cloud customer base. Recommends weekly adds at the 9-week EMA for new investors.
- **SOFI** — Both vocally bullish; one host says price action "feels manipulated," is adding aggressively and writing long January 2027 $47 call spreads.
- **MELI** — One of the "biggest disconnects" in the portfolio; one host added a "ton" today; targets $3,000, framed as the Amazon of LatAm in moat-building phase.
- **NOW** — One host recently initiated mid-$80s, may add more; thesis is AI-driven enterprise workflow still early, sentiment overly weak, 20–25% annual compounder; potential Palantir-style bespoke engagements.
- **DDOG** — Major positive catalyst for software broadly; 32% revenue growth, NRR reaccelerating to 121%, billings +37%; first-mover consumption-model name disproving "AI kills software."
- **CIFR** — Held since ~$10–12, kept buying weakness; preferred as pure-play "landlord" without neocloud execution risk.
- **WULF** — Mentioned alongside CIFR as a landlord-type AI infra play with lower execution risk than neoclouds.
- **ALAB** — One host owns it (initiated $60s); pure-play on AI data-movement/interconnect; CPO + optical fabric ramps in 2027–2028.
- **AXON** — One host bought this week.
- **TSMC** — Potentially "really cheap" at PEG <1.0, 30% expected EPS growth for three years, near-monopoly in leading-edge.
- **ARM** — Bullish on doubling AGI CPU revenue demand and merchant-silicon pivot; sees it eventually becoming an XPU/GPU company.
- **RKLB** — 15-bagger (avg ~$6); largest deal in history (5 Neutron launches), $2.2B backlog, 38% gross margins; targets $100B mcap long-term.
- **LSCC** — FPGA mid-market leader; inventory headwinds behind it; AMI acquisition gives firmware attach to every AI server.
- **INTC** — Called early; ran ~700%; cautions it is now "clearly expensive" and to wait for a pullback.
- **MU** — Long-time bull/believer; no specific new buy this episode.

#### Tickers to SELL
- **RKLB** — Small trim because extended; not a full sell, still top holding.
- **SNPS (Synopsys)** — Trimmed this week to raise 10% cash buffer with QQQ daily RSI at 85.
- **INTC / DOCN / AMD** — All flagged "wait for pullback" for new buyers given RSI >70–85.
- **SpaceX IPO** — Don't buy on IPO day; offering designed to dump liquidity on retail.

#### Tickers OWNED
- **RKLB** — 15-bagger, avg ~$6; top growth-portfolio position after small trim today.
- **DOCN** — Number-one position; not trimming despite runup.
- **SOFI** — Long with active options (March 2027 $138 call spreads, January 2027 $47 calls).
- **MELI** — Actively adding; large conviction; added heavily this week.
- **ALAB** — Initiated $60s; still held.
- **NOW** — Recently initiated mid-$80s.
- **NVDA** — One host bought this week.
- **AXON** — One host bought this week.
- **CIFR** — Held since ~$10–12; continued buying on weakness.
- **NBIS** — One host owns near $200; "confident in the theme."
- **AI5 basket** — ARM (low $100s), INTC ($30s–$40s), AMCR ($30s–$40s); basket up ~50% YTD.
- **LSCC** — Held; long-term bet on AI-server firmware attach.

---

### Video 2 — https://www.youtube.com/live/LFJyM-gXfPc

#### Tickers to BUY
- **NVDA** — "Bewildering" to be undervalued at trillion-dollar revenue book, 75% gross margins, "control tower of the entire AI infrastructure universe"; market wrongly pricing at Intel-like multiples.
- **NOW** — "Wildly undervalued"; tailwinds from AI/agents; enterprise customers are not defecting; market underestimating.
- **PURE** — "Next big rerating story"; storage = next bottleneck after memory as inference data exhaust scales.
- **QCOM** — Near-term rerating candidate; from handset story to AI compute/edge platform; 12–13x forward, 30%+ auto growth, new $10B+ custom data-center chip biz; June investor day catalyst.
- **AMZN** — Stated "best idea." AWS at fastest growth in 15 quarters, $225B+ Trainium commitments outpacing Nvidia in the book, Bedrock spend +170% QoQ; calls $300 stock "very quickly."
- **META** — Other stated "best idea." Ad engine becoming AI engine (33% revenue growth at scale), 10x business chatbot conversations, agentic workflows just beginning.
- **GOOGL** — Cloud +63% YoY, adding more incremental cloud rev/quarter than AWS; operating margins expanded ~18%→34% on TPU efficiency; "running on all cylinders."
- **DOCN** — Thesis described as validated (stock crossed $100, tripled in ~8 months); long-term inference-cloud positioning is right; "perfectly fine holding until thesis breaks."

#### Tickers to SELL
- **SOUN** — "Feature layer trying to become a platform"; no real chance against vertical stacks dominated by end-to-end networks.
- **DOCN** (near-term hedged) — "Probably pulls back near-term"; expectations sky-high, lacks enough data-center capacity. Long-term thesis intact — trim view, not exit.
- **HOOD** — "Crappy earnings report" due to over-dependence on crypto; implied avoidance.

#### Tickers OWNED
- **SOFI** — Both speakers hold. One has six-figure share count, buying every dip; wrote January put spreads (127 contracts, ~$0.85/share collected) to acquire below $12. The other added through put spreads after a tough earnings reaction.
- **META** — Stated best idea; speaker confirms ownership.
- **AMZN** — Stated best idea alongside META; speaker confirms ownership.
- **DOCN** — One held via options (put spreads sold below $25); the other implies holding.
- **IRON / CIFR** — "I'm long these things, but I'm patient"; aware of dilution risk from capital raises.
- **PLTR** — Implied ownership; will post reaction to Monday earnings; high conviction in continued exponential beats.

---

### Video 3 — https://www.youtube.com/live/lijNh0CLXbk

#### Tickers to BUY
- **NOW** — Starter position initiated; 15x FCF too cheap given no AI disintermediation risk; weakness is timing (Middle East slip, Armis integration), not demand. Armis adds healthcare-security TAM and "touching the physical world."
- **SOFI** — Both bullish; one holds large position; expects above-consensus revenue (~$1.08–1.1B), EPS (~$0.13), 36–37% growth. Should not be in the teens given membership growth + sticky banking ecosystem.
- **AXON** — "Adding every week"; cloud-centric public-safety control center; 30% top-line CAGR for next 3–4 years; safe from AI disintermediation despite stage-4 breakdown punishment.
- **ARM** — One of the "fearsome threesome" of CPU bottleneck (with INTC, AMD); ATH ~$232–$240; META/AMZN Graviton deal = royalty windfall.
- **AMZN** — Top Mag-7 pick for the year; AWS ~$160B run rate at 26% growth, 35% op margins; META Graviton deal confirms thesis; still undervalued vs GOOGL.
- **META** — Other top Mag-7 pick; Zuckerberg's aggressive compute accumulation (GPUs + Graviton CPUs) validates agentic AI buildout.
- **AMD** — Major CPU bottleneck beneficiary; BofA channel data suggests data-center GPU/CPU biz larger than understood.
- **MU** — "Reasonable" at current; fully certified on Nvidia Rubin; example of pullback-then-rip ($350→$500).
- **AVGO** — Strong week; "Broadcom was like $260" example of names that reward buyers on pullbacks.
- **AAOI** — Added during April pullback; deliberate build in photonic/optical interconnect for AI cluster scaling.
- **AEHR** — Added during April pullback; "reliability layer" of optical stack.
- **CRDO** — Added during April pullback; Dust Photonics acquisition extends platform into silicon photonics ahead of copper's physical limits.
- **LITE** — Held and "loved" for laser/light layer of optical stack in AI interconnect theme.

#### Tickers to SELL
- **INTC** — Strong earnings beat and CPU-cycle tailwind, but now at "100-plus times forward" with significant foundry execution risk; would not be entering at $70; thesis "already played out."
- **POET** — "Not a fan"; would not own; history of paying influencers to promote = immediate red flag regardless of tech.

#### Tickers OWNED
- **NOW** — New starter, "tiny," high-conviction patient thesis.
- **AXON** — Adding "every week"; long-term core holding around the cloud/SaaS layer on top of hardware.
- **SOFI** — Large position; bought heavily under $20 in early April.
- **VIK** — Held; considering selling covered calls; bullish on GLP peptide thesis but fully sized.
- **HIMS** — Rotated significant capital in under $20.
- **AMZN** — Top Mag-7 holding.
- **META** — Top Mag-7 holding.
- **AAOI / AEHR / CRDO / LITE** — Photonics bucket built during April/May pullback; current holdings.

---

### Video 4 — https://www.youtube.com/live/6z0BIC0zC54

#### Tickers to BUY
- **NVDA** — Core AI infrastructure play; Jensen interview reinforced conviction; 15x forward during the dip viewed as a "steal."
- **MU** — "Pounding Micron at 100"; under 4x forward with room to run; durable trade backed by memory bottleneck.
- **AVGO** — Chopped from $300→$400 then snapped back; nothing fundamentally changed; opportunistic buy moment.
- **HIMS** — Added ~700% to position near bottom ($15–20); FDA clarity on GLPs + legalized peptide compounding = massive leg up.
- **SOFI** — Unfairly punished; expects strong earnings; sees real chance of $40 this year.
- **ARM** — CPU bottleneck top priority; "finally breaking out of a multi-year base" with own AI chip moving from Switzerland-neutral.
- **AMKR** — CPU packaging angle for the agentic-AI CPU surge.
- **INTC** — Narrative/thematic trade post Trump-administration investment; potential to win packaging + wafer deals for AI custom chips.
- **AMD** — All-time highs this week; CPU bottleneck beneficiary.
- **NBIS** — Favorite neocloud pick and "tier-one premium"; Nvidia stamped it as architecture partner, early Rubin access, embedded engineering support.
- **CIFR** — "Tier-two" neocloud framed as "landlord of the AI utility era"; AWS lease alone ~$700M average annualized NOI.
- **WULF** — Deepened position; $900M equity raise framed as management using stock as currency, not red flag.
- **AEHR** — Got in at $8, now $87; AI data-center testing very early; multi-bagger from entry, runway remains.
- **META** — Top pick alongside AMZN; "looked like an idiot for 3 months" but conviction held; re-rated strongly.
- **AMZN** — Other top pick; Graviton CPU exposure is added reason; breaking $250 bullish.
- **IBIT** — Prefers Bitcoin ETF over direct crypto; bullish on crypto into summer with risk-on building.

#### Tickers to SELL
- **Software broadly (SaaS)** — "Dead money this year, at best a 2027 story"; seat-based pricing under threat from agentic-AI tokens; multiples need to be re-earned by quarterly proof.
- **APP** — Not bearish on fundamentals, but "too much noise to buy right now": SEC scrutiny, governance risk, gaming-ad concentration; opportunity cost favors cleaner CPU/infra plays.

#### Tickers OWNED
- **NBIS** — Both own; favorite neocloud; positioned from $20–30.
- **CIFR** — Deepened position; long-term landlord on AI data-center power.
- **WULF** — Owned; deepened alongside CIFR; comfortable with dilution.
- **IRON** — Growth-portfolio holding; "frustrating" because expects more deal announcements given unmatched power-ratio advantage; in common (was options).
- **SOFI** — Both own. One cost basis ~$21, added heavily during pullback. The other owns "so much SoFi."
- **HIMS** — Long since "the wreckage" at $15–20; now near $30 (down from $70 high).
- **TSLA** — 100 shares avg ~$180; nibbled 15 shares at $320; long-term physical-AI / Elon thesis.
- **ARM** — Family portfolio; CPU bottleneck winner.
- **AMKR** — Trading-portfolio CPU packaging angle.
- **AEHR** — In at $8 → $87; trimming as it grows in portfolio (allocation rules), still holds.
- **META** — Top pick; trimmed edges of ad-side after recovery to build cash, remains long.
- **AMZN** — Other top pick; still long.
- **DOCN** — Mentioned alongside AEHR as a name that became too large and required trimming per allocation rules.
- **IBIT** — Implied ownership/preference for Bitcoin ETF vehicle.

---

### Video 5 — https://www.youtube.com/live/BR4ZzlzPzLo

#### Tickers to BUY
- **INTC** — Real-time demand validation: GOOGL, AMZN, SambaNova orders; Terafab consortium with TSLA/SpaceX/xAI; clear turnaround on agentic-AI CPU demand; still needs to prove itself in earnings at $60.
- **META** — Top portfolio position (up to 15%); built up on the pullback near $500; ~18x earnings vs S&P average is "criminal" given 3B+ eyeballs, ad margins, distribution moat.
- **AMZN** — One of the two biggest entering the year; Jassy letter discloses $15B annual AI run-rate, Trainium booked through gen 3/4, chip biz potentially $50B externally.
- **PLTR** — Both bullish; 15% weekly drawdown "embarrassingly stupid"; Rule-40 of 120 (highest ever) with further improvement guided for 2026; nibbled more on the dip.
- **GOOGL** — Infrastructure + CPU demand winner (Graviton/Axion, GOOG-Groq-AVGO deals, INTC packaging deal); Gemini + distribution moat.
- **AVGO** — "Showing quite a bit of life"; Google-Groq deal; $40B+ AI chip revenue, benchmark for AMZN's chip ambition.
- **NBIS** — "Tier-one name" in AI cloud/GPU infra; ATH, +8% on the day; named top pick on Fox Business in "AI capacity GPU REIT" world.
- **CRWV** — Strong demand validation (Anthropic mega-deal); bullish on capacity-deployment scale.
- **AAOI** — Started position on pullback into $70s as "highest asymmetric play" in optical/photonics; sits in NVDA-MRVL silicon-photonics supply chain.
- **COHR** — Photonics leader; NVDA invested + spend committed; CEO (Jim Anderson, ex-LSCC) trusted for conservative execution.
- **AEHR** — "Victory lap"; up 4x in 4 months; second-biggest growth-portfolio position; still bullish.
- **CIFR** — Long-term hold; bought ~$10, ran to $24, fell to $10, now ~$17 (70% gain); still long.
- **WULF** — Long-held conviction; "showing quite a bit of life"; hyperscaler data-center buildout beneficiary.
- **LITE** — "Quality institutional name" in photonics with NVDA investment; more telecom-side.
- **HIMS** — Bought more aggressively (5–600% position addition) on pullback to $15 from $70 high; conviction unchanged.
- **HOOD** — Added in $70s after $150 peak; younger generations will bank with HOOD over JPM.
- **SOFI** — Added throughout the drawdown alongside HOOD; same generational banking thesis.
- **ARM** — Merchant AGI CPU fills gap previously served only by custom (Axion, Cobalt, Graviton).
- **AMD** — Lisa Su cited double-digit server CPU growth for 2026, lead times shrinking with 10–15% price increases.

#### Tickers to SELL
- **CRM / SaaS broadly** — Dollar-allocation shift to hardware certainty; ServiceNow, Snowflake, similar names face gross-margin compression 70–80% → 50–60% as they buy compute. Selling overdone but near-term headwind structural.
- **NET** — Down 13% on the day; "soft AI" bucket; no explicit sell — "avoid for now" framing.
- **SNOW** — Down 9% on the day; explicit margin-compression risk; fundamentals intact.
- **CRWD** — Down 5% on the day; hurt by Anthropic Mythos narrative despite being a planned distribution partner — speakers call irrational.

#### Tickers OWNED
- **META** — Top portfolio position (up to 15%); built up entering year alongside AMZN; made it the top holding by selling lower-conviction names near $500 pullback.
- **AMZN** — One of the two biggest entering the year.
- **PLTR** — Held since under $10; nibbled more on the dip; long-term position, not adding aggressively because already large.
- **AEHR** — Second-biggest growth-portfolio position; up 4x in 4 months.
- **CIFR** — Long since ~$10; rode to $24, held through pullback to $10, now ~$17; framed as 5-year hold.
- **WULF** — Long-term hold.
- **HIMS** — Held since under $10; added 5–600% on pullback to $15 from $70.
- **HOOD** — Long; added on dips in $70s.
- **SOFI** — Long; added throughout drawdown.
- **AAOI** — Started new position on pullback into $70s.
- **IRON** — Owned as "very real asset base and genuine power story"; Microsoft cited as hyperscale anchor tenant.
- **NBIS** — Implied long; both speakers tout as top AI infrastructure pick; "we are all Nebius's on the show."

---

## Notes & caveats

- One agent reported `NVTS` for Nebius in Video 5; correct ticker is **NBIS** (NVTS = Navitas Semiconductor, unrelated). Normalized in the tally.
- One agent reported `LSCC (Lumentum)` in Video 5; LSCC = Lattice Semi (FPGA), Lumentum = LITE. Treated the V5 mention as **LITE**. V1 Lattice mention kept as LSCC.
- One agent reported `EEHR (Air Test Systems)` in Video 4; the actual company is **AEHR Test Systems** (ticker AEHR). Normalized.
- "IRON" mentions are ambiguous between Iron Mountain (IRM) and another power/AI-infra entity — agents flagged this; treat with care if acting on it.
- Some "owned" entries are inferred from speaker context ("I'm long these," "we are all X's on the show") rather than explicit position disclosures.
- Speakers often share broad themes rather than ticker-specific BUY calls (e.g., "photonics," "neocloud") — individual names listed under those themes are picked from each agent's reading of the transcript.
