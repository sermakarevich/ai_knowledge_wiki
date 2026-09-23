[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# GPT Realtime 2 (medium) — Overall Results (.728±.03 TF, .624±.04 RQ)
**In one sentence:** Across 27 model configurations judged by GPT-5.4-mini, GPT Realtime 2 (medium, thinking) leads task fulfillment at .728±.03 while recovery quality peaks elsewhere (Gemini 2.5 Flash thinking at .704±.04), showing the two axes are partially independent.
## Key points
- 27 model configurations (17 closed-weight systems, 10 open-weight configurations) are evaluated with GPT-5.4-mini (high reasoning) as judge, using three independent epochs per configuration and 95% CIs from a 1000-iteration percentile bootstrap over N=428 per-sample epoch-averaged means.
- GPT Realtime 2 (medium, thinking) achieves the highest task-fulfillment (TF) win rate at .728±.03 with RQ .624±.04, followed by GPT Realtime 2 (xhigh, thinking) at .702±.04 TF / .613±.04 RQ and GPT Realtime 1.5 at .654±.04 TF / .655±.04 RQ.
- Recovery quality (RQ) tells a different story: Gemini 2.5 Flash (thinking) has the highest RQ pass rate at .704±.04 despite lower TF (.586±.04), and GPT Realtime has the highest RQ among GPT models (.680±.04) with only mid-tier TF (.597±.04).
- Thinking/reasoning helps Gemini on TF — Gemini 2.5 Flash thinking (.586±.04) beats non-thinking (.488±.04) and Gemini 3 Flash thinking (.632±.03) beats non-thinking (.598±.04) — but thinking does not consistently improve RQ.
- RQ pass rate is defined as the fraction of interruptions where all rubric criteria are met ("all criteria met → Pass, any criterion not met → Fail"), with criteria tailored to each interruption type (Section 3.2; example rubric in Appendix G).
- TF win rate is measured against the baseline, so TF is 0.50 by construction for baseline vs. baseline (GPT-4o Audio baseline: .500∗ TF, .654±.05 RQ).
- Rankings are validated two ways — re-scoring the whole benchmark with an independent second judge from a different provider and comparing verdicts to human annotations — on the logic that matching ordering and verdict-level agreement rules out judge-setup artifacts.
---
## 5 Results — evaluation setup
**Covers:** Section 5 (setup fragment)
> "We evaluate 27 model configurations on IHB ENCH using GPT-5.4-mini [31] (high reasoning) as the judge. The 27 configurations come from 17 closed-weight systems and 10 open-weight configurations. The evaluation is run with three independent epochs per configuration, and 95% confidence intervals are computed by a 1000-iteration percentile bootstrap [8] over the N =428 per-sample (epoch-averaged) means."

## 5.1 Evaluated models
**Covers:** Section 5.1
- OpenAI models: "GPT-4o Audio and GPT-4o Mini Audio [25]; GPT Audio [26] and GPT Audio Mini [27]; GPT Realtime and GPT Realtime 1.5 [28], GPT Realtime Mini, and GPT Realtime 2 [30]."
- Google models: "Gemini 2.5 Flash and Gemini 2.5 Pro [11]; Gemini 3 Flash and Gemini 3.1 Pro [12]; and Gemini 3.1 Flash Live [13]."
- Open-weight models: "Gemma 4 12B Instruct [14], Qwen3-Omni-30B-A3B-Instruct [45], Qwen2.5-Omni-7B [44], Phi-4-Multimodal-Instruct [1], Voxtral-Small-24B-2507 [24], Qwen2-Audio-7B-Instruct [6], MiMo-Audio-7B-Instruct (in both no-thinking and thinking modes) [42], and Kimi-Audio-7B-Instruct [17]."

## 5.2 Overall results (Table 1)
**Covers:** Section 5.2, Table 1 (TF win rate | RQ pass rate)

| Model | TF | RQ |
|---|---|---|
| GPT Realtime 2 (medium)† | .728±.03 | .624±.04 |
| GPT Realtime 2 (xhigh)† | .702±.04 | .613±.04 |
| GPT Realtime 1.5 | .654±.04 | .655±.04 |
| GPT Audio | .644±.04 | .649±.04 |
| Gemini 3 Flash† | .632±.03 | .605±.04 |
| Gemini 3 Flash | .598±.04 | .661±.04 |
| GPT Realtime | .597±.04 | .680±.04 |
| Gemini 2.5 Flash† | .586±.04 | .704±.04 |
| Gemini 3.1 Pro† | .582±.04 | .649±.04 |
| Gemini 2.5 Pro† | .526±.04 | .695±.04 |
| GPT-4o Audio (baseline) | .500∗ | .654±.05 |
| Gemini 2.5 Flash | .488±.04 | .679±.04 |
| GPT Audio Mini | .484±.04 | .579±.04 |
| Gemini 3.1 Flash Live | .419±.04 | .611±.04 |
| GPT Realtime Mini | .417±.03 | .621±.04 |
| Gemini 3.1 Flash Live† | .405±.04 | .603±.04 |
| GPT-4o Mini Audio | .351±.04 | .654±.05 |
| Gemma 4 12B Instruct† | .511±.03 | .550±.04 |
| Gemma 4 12B Instruct | .505±.04 | .540±.04 |
| MiMo-Audio-7B† | .445±.04 | .519±.04 |
| MiMo-Audio-7B | .337±.03 | .581±.04 |
| Voxtral-Small-24B | .308±.03 | .593±.04 |
| Qwen3-Omni-30B | .304±.03 | .676±.04 |
| Kimi-Audio-7B | .220±.03 | .519±.04 |
| Qwen2.5-Omni-7B | .181±.03 | .530±.04 |
| Phi-4-Multimodal | .104±.02 | .465±.04 |
| Qwen2-Audio-7B | .044±.01 | .395±.04 |

† = thinking/reasoning-enabled. ∗ = "TF win rate is measured against the baseline, so TF is 0.50 by construction for baseline vs. baseline."

Verbatim key findings:
- "GPT Realtime 2 achieves the highest task fulfillment win rate (0.728), followed by GPT Realtime 2 (xhigh) (0.702) and GPT Realtime 1.5 (0.654)."
- "Recovery quality tells a different story: Gemini 2.5 Flash (thinking) achieves the highest RQ pass rate (0.704) despite a lower TF score (0.586), indicating that task advancement and recovery quality are partially independent axes."
- "GPT Realtime has the highest RQ among GPT models (0.680) but only mid-tier TF (0.597), suggesting that older Realtime models are more conservative but more correct in recovery behavior."
- "Thinking/reasoning modes help for Gemini on TF: Gemini 2.5 Flash with thinking outperforms without (0.586 vs. 0.488), and Gemini 3 Flash similarly (0.632 vs. 0.598). However, thinking does not consistently improve RQ."

Rubric note in chunk:
> "Each criterion is assessed as met or not met, and the overall verdict is mechanically consistent: all criteria met → Pass, any criterion not met → Fail. We report the recovery quality pass rate: the fraction of interruptions where all criteria are met. These criteria are tailored to each interruption type (Section 3.2); an example rubric is shown in Appendix G."

## 5.3 Inter-judge agreement (setup) + Figure 3
**Covers:** Section 5.3 opening; Figure 3 caption
> "Every result above rests on a single LLM judge, so we ask whether the rankings are robust to that choice. We validate it two ways: by re-scoring the whole benchmark with an independent second judge from a different provider, and by comparing its verdicts to human annotations. If both judges and human raters recover the same ordering and agree at the verdict level, the conclusions are unlikely to be an artifact of the judging setup."

Figure 3 caption (verbatim): "Figure 3: Per-model task-fulfillment agreement: primary judge (x-axis) vs. the secondary judge, the summarized-context judge, and human annotators (y-axis). Colored lines are OLS fits. RQ counterpart: Figure 7." Legend entries in chunk: "Primary judge (GPT-5.4-mini)", "Secondary Judge (Gemini 3 Flash)", "Perfect Agreement (identity)", "Primary Judge w/ Summarized Context", "Human Annotators".

**Covers:** Chunk 06 (Sections 5–5.3, Table 1, Figure 3 caption); planned Covers per plan.md was "Two-axis scoring: comparative task fulfillment and absolute recovery quality"
