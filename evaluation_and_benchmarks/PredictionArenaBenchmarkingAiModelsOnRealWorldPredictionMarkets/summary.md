# Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets

**Paper:** [Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets (Zhang et al., 2026)](https://arxiv.org/abs/2604.07355)

## Human Readable TL;DR

Imagine giving several AI systems each $10,000 of real money and letting them bet on future events -- weather, sports, politics, crypto -- on actual betting platforms for two months. That's what this paper did. It's like a trading competition where AI models have to put their money where their mouth is, revealing which ones actually understand the world well enough to profit, and which ones just sound smart. The key takeaway: being right matters far more than doing lots of research, and the format of the competition dramatically changes which AI wins.

## TL;DR

Prediction Arena benchmarks frontier LLMs as autonomous trading agents on live prediction markets (Kalshi and Polymarket) with real capital over 57 days. All Cohort 1 models lost money on curated Kalshi markets, with settlement accuracy -- not research volume or token usage -- as the strongest predictor of success. Platform design profoundly influenced outcomes: models averaged -22.6% on Kalshi vs. -1.1% on discovery-based Polymarket during the same period. Cohort 2 paper-trading results showed early positive returns for gpt-5.4 (+1.22%) and gemini-3.1-pro-preview (+6.02% on Polymarket).

---

## Problem & Motivation

Current AI benchmarks rely on synthetic tasks or simulated environments that fail to capture real-world decision-making under genuine consequences -- the "sim-to-real gap." Prediction markets offer objective ground truth (events resolve definitively), real financial stakes, and diverse domain coverage. Prediction Arena was built to test whether frontier AI models can actually make profitable autonomous decisions when money is on the line, rather than merely performing well on static benchmarks that are susceptible to overfitting, data contamination, and prompt engineering.

---

## Main Original Ideas

1. **Real-Capital AI Benchmark** -- Models trade with actual money ($10,000 each) on live prediction markets, creating genuine financial consequences that cannot be gamed through prompt engineering or dataset contamination. This is the first benchmark to introduce real economic pressure for LLM evaluation.

2. **Dual-Platform Design (Curated vs. Discovery)** -- Kalshi provides 29 curated markets across 7 categories testing pure prediction accuracy, while Polymarket requires models to discover their own trading opportunities from the entire market universe. This isolates prediction skill from opportunity identification.

3. **Two-Cohort Longitudinal Evaluation** -- A 57-day evaluation (Jan 12 -- Mar 9, 2026) with 6 legacy models (Cohort 1, live capital) and 4 next-gen models (Cohort 2, paper trading), enabling cross-generational and longitudinal stability analysis across 5,444 snapshots and 2,916 trades.

4. **Profit-as-Calibration Framework** -- Profitable trading requires identifying mispriced markets where the crowd consensus is wrong, turning profit into a direct measure of a model's calibration edge over collective human intelligence.

5. **Minimal Scaffolding Philosophy** -- All models receive standardized prompts and basic tools (web search, notes, trading execution), emphasizing out-of-the-box model capabilities rather than system engineering or custom agent architectures.

---

## Key Findings

### Kalshi Performance (Cohort 1, 57 days, real capital)

| Model | Phase 1 Return | Total Return | Settlement Win Rate | Max Drawdown |
|-------|---------------|-------------|-------------------|-------------|
| glm-4.7 | -7.2% | **-16.0%** | 42.4% | 16.3% |
| grok-4-20-checkpoint | **-4.4%** | -20.0% | **51.9%** | 30.9% |
| claude-opus-4-5 | -7.2% | -20.4% | 40.4% | -- |
| gpt-5.2 | -16.2% | -24.7% | 48.0% | -- |
| gemini-3-pro-preview | -25.3% | -- | 28.8% | -- |
| grok-4-1-fast-reasoning | **-26.8%** | -- | **15.4%** | -- |

### Cohort 2 Preliminary Results (3 days, paper trading)

| Model | Kalshi Return | Polymarket Return |
|-------|-------------|------------------|
| gpt-5.4 | **+1.22%** | -- |
| claude-opus-4-6 | -0.11% | -10.06% |
| glm-5 | -4.09% | -- |
| gemini-3.1-pro-preview | 0 trades | **+6.02%** |

### Critical Insights

- **Settlement accuracy is king**: The strongest predictor of returns across both phases and platforms. Research volume and token usage showed zero correlation with performance.
- **Platform design reshapes the leaderboard**: Cohort 1 averaged -22.6% on Kalshi vs. -1.1% on Polymarket during the same period. Models strong on one platform were not necessarily strong on the other.
- **Weather markets dominated outcomes**: 71--97% of Cohort 1 settled positions were weather-related, making weather prediction accuracy the de facto driver of overall performance on Kalshi.
- **All models exhibited loss-holding bias**: Models consistently cut winning positions early while holding losers -- the classic disposition effect from behavioral finance.
- **Hierarchy of success factors**: (1) initial prediction accuracy, (2) capitalizing when correct, (3) position sizing under uncertainty, (4) exit discipline, (5) research quality, (6) research quantity (uncorrelated).

---

## Suggestions & Future Directions

1. **Performance-Aware Activity Control** -- Investigate whether AI models can autonomously detect when their predictive edge diminishes and adaptively reduce trading activity, rather than continuously trading through drawdowns.

2. **Controlled Cross-Platform Comparison** -- Isolate how market selection ability (Polymarket) interacts with raw predictive accuracy (Kalshi) through more controlled experimental designs.

3. **Full Cohort 2 Live Evaluation** -- Run next-gen models for 30+ days with real capital under identical conditions to Cohort 1 for statistically robust cross-generational comparison.

4. **Calibration Analysis** -- Assess model probability estimates against market prices to understand probabilistic reasoning quality beyond binary win/loss rates.

5. **Multi-Agent Markets** -- Explore AI-vs-AI prediction markets to study information aggregation, strategic interactions, and emergent behaviors without human liquidity effects.

---

## Authors & Institutions

Jaden Zhang (Arcada Labs, Harvard University), Gardenia Liu (Arcada Labs, Harvard University), Oliver Johansson (Arcada Labs), Hileamlak Yitayew (Arcada Labs), Kamryn Ohly (Arcada Labs), Grace Li (Arcada Labs)
