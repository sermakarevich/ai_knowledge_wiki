> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation & Results

**In one sentence:** On LongMemEval-S SodaMem's store-of-record configuration reaches 92.8% accuracy (464/500; best of N = 3) at a measured mean $0.00161 per question (≈18.3k tokens; median $0.00111 / ≈14.6k) with deepseek-v4-flash, compiling publicly reported systems with estimable API cost into a cost table and cost–accuracy map that place SodaMem near the accuracy frontier at Flash-tier spend, strictly dominating several higher-cost, lower-accuracy public points.

## Key points

- Evaluation setup: LongMemEval-S (500 questions; ≈115k-token histories) benchmarked via the accuracy–cost trade-off against publicly reported systems with estimable per-question API cost, compiled from disclosed scores, models, and token/$ figures in primary sources rather than re-running every baseline under one harness, converted with 2026 list prices.
- SodaMem run: entity-subject store-of-record (500 users, 235,840 facts); planner, reader, and judge are deepseek-v4-flash with LongMemEval's official yes/no templates; accuracy 464/500 = 92.8% (best of N = 3; median 90.6%).
- Cost: end-to-end planner+reader usage (excluding ingest and judge) at Flash list rates ($0.14 / $0.0028 / $0.28 per 1M for cache-miss / cache-hit input / output) yields a mean of 18,348 tokens/question and $0.00161/question ($1.61 per 10³ Q in Table 1); the median is 14,640 tokens and $0.00111/question ($1.11 per 10³ Q), ≈25% lower—the mean is pulled up by a long tail.
- The same Flash model grades the run (self-grading); absolute accuracy may shift under an independent GPT-4o judge, but released hypotheses support re-evaluation and cost is judge-independent.
- Table 1 (reproduced below) spans 22 methods from agentmemory V4 (96.2%, $60/10³ Q est.) down to MemoryBank (21.0%, $2.21/10³ Q est.); "Est." = priced from disclosed tokens, "Meas." = author-reported / measured USD.
- Result analysis: the dominated quadrant—cost > mean $0.00161 and accuracy < 92.8%—contains Cersei Embed / Hybrid / Full-context, AgentOS, long-context GPT-5-mini, EmergenceMem Simple Fast, and MemoryBank under TiMem (strictly worse cost/accuracy pairs even against SodaMem's mean); under the median ($0.00111), MemoryOS and Fact-Mem0 read would enter as well.
- Public accuracy jumps often track reader upgrades (e.g., Mastra 84.23% → 94.87% from GPT-4o to GPT-5-mini); SodaMem's claim is near-frontier accuracy at Flash-tier spend, undercutting Opus/GPT-4o high-score systems by ≈10–40× in estimated $/question.
- Limitations: single store-of-record configuration under Flash self-grading; no unified re-run of all baselines; peer costs are order-of-magnitude reconstructions; ingest-time spend and timeline-resolution ablations left for follow-up.

---

## Experiments

The authors evaluate SodaMem on LongMemEval-S (500 questions; ≈115k-token histories) (Wu et al. 2024) via the accuracy–cost trade-off against publicly reported systems with estimable per-question API cost. They compile disclosed scores, models, and token/$ figures from primary sources (rather than re-running every baseline under one harness), convert them with 2026 list prices, and situate the store-of-record run in that landscape. Table 1 sorts methods by accuracy; Figure 2 plots the same points.

### Setup and Cost Protocol

**SodaMem run.** Entity-subject store-of-record (500 users, 235,840 facts). Planner, reader, and judge are deepseek-v4-flash with LongMemEval's official yes/no templates. Accuracy is 464/500 (92.8%; best of N = 3; median 90.6%). End-to-end planner+reader usage totals (excluding ingest and judge), priced at Flash list rates ($0.14 / $0.0028 / $0.28 per 1M for cache-miss / cache-hit input / output), yield a mean of 18,348 tokens/question and $0.00161/question ($1.61 per 10³ Q in Table 1). A long tail pulls the mean up: the median is 14,640 tokens and $0.00111/question ($1.11 per 10³ Q), ≈25% lower, so a typical question is cheaper than the mean bill suggests. The same Flash model grades the run (self-grading); absolute accuracy may shift under an independent GPT-4o judge, but released hypotheses support re-evaluation and cost is judge-independent.

**Baseline cost estimation.** Author-reported USD (or $/correct) is used when available (AgentOS (Framers Lab 2026), Cersei (Pacifio 2026), Fact-Mem0 read (Fact-Memory Cost 2026), EmergenceMem Simple Fast via AgentOS (Haley et al. 2025; Framers Lab 2026)). Otherwise disclosed tokens are priced with the reported answering model: GPT-4o-mini $0.15/$0.60, GPT-4o $2.50/$10, Gemini 2.5 Flash $0.30/$2.50, Claude Opus 4.6 $5/$25, GPT-5-mini $0.25/$2 (per 1M tokens; 90%/10% in/out prior if undisclosed). TiMem Table 6 (Li et al. 2026) and MemOS eval result (MemTensor 2025) report recalled context length; the authors price that plus ≈200 output tokens as an answer-stage lower bound. Mem0's 2026 research mean tokens (Mem0 Research 2026) are priced as GPT-4o under the same prior. Unless marked measured, costs are estimates—order-of-magnitude comparisons, not millidollar rankings. Frozen store fingerprints and usage totals accompany the 92.8% artifact.

### Table 1

LongMemEval-S methods with estimable API cost, sorted by accuracy (desc.). Token cost is USD per 10³ questions (= 1000× per-question cost). SodaMem reports mean cost to match baseline conventions; median is $1.11/10³ Q (≈14.6k tokens). "Est." = priced from disclosed tokens; "Meas." = author-reported / measured USD. SodaMem row highlighted.

| Method | Cite | Date | Model | Acc. | Cost/10³ Q |
|---|---|---|---|---|---|
| agentmemory V4 | (McCann 2026) | 2026-03 | Claude Opus 4.6 | 96.2% | $60 (est.) |
| Mem0 (2026 research) | (Mem0 Research 2026) | 2026-04 | Managed (GPT-4o est.) | 94.4% | $22 (est.) |
| **SodaMem (ours)†** | — | 2026-08 | deepseek-v4-flash | **92.8%** | **$1.61 (meas.)** |
| Cersei Full-context | (Pacifio 2026) | 2026-04 | Gemini 2.5 Flash | 87.6% | $33 (meas.) |
| Cersei Embed | (Pacifio 2026) | 2026-04 | Gemini 2.5 Flash | 86.6% | $1.84 (meas.) |
| Cersei Hybrid | (Pacifio 2026) | 2026-04 | Gemini 2.5 Flash | 86.3% | $10–16 (meas.) |
| AgentOS | (Framers Lab 2026) | 2026-04 | GPT-4o | 85.6% | $7.7 (meas.) |
| LC GPT-5-mini | (Fact-Memory Cost 2026) | 2026-03 | GPT-5-mini | 82.4% | $29.3 (meas.) |
| EmergenceMem Simple Fast | (Haley et al. 2025; Framers Lab 2026) | 2025-06 | GPT-4o | 79.0% | $46 (meas.) |
| MemOS (eval set) | (MemTensor 2025) | 2025-07 | GPT-4o-mini | 77.8% | $0.33 (est.) |
| TiMem | (Li et al. 2026) | 2026-01 | GPT-4o-mini | 76.9% | $0.31 (est.) |
| Memobase | (MemTensor 2025) | 2025-07 | GPT-4o-mini | 72.4% | $0.35 (est.) |
| MemOS (TiMem repro) | (Li et al. 2026, 2025) | 2026-01 | GPT-4o-mini | 68.7% | $0.28 (est.) |
| Mem0 (TiMem repro) | (Li et al. 2026; Chhikara et al. 2025) | 2026-01 | GPT-4o-mini | 65.0% | $0.37 (est.) |
| Zep (eval set) | (MemTensor 2025; Rasmussen et al. 2025) | 2025-07 | GPT-4o-mini | 63.8% | $0.36 (est.) |
| Supermemory (eval set) | (MemTensor 2025) | 2025-07 | GPT-4o-mini | 58.4% | $0.18 (est.) |
| MemoryOS | (Li et al. 2026; Kang et al. 2025) | 2026-01 | GPT-4o-mini | 58.0% | $1.26 (est.) |
| A-MEM | (Li et al. 2026; Xu et al. 2025) | 2026-01 | GPT-4o-mini | 55.4% | $0.72 (est.) |
| Fact-Mem0 (read) | (Fact-Memory Cost 2026) | 2026-03 | GPT-5-mini | 49.0% | $1.3 (meas.) |
| MemU | (MemTensor 2025) | 2025-07 | GPT-4o-mini | 38.4% | $0.20 (est.) |
| MemoryBank | (Li et al. 2026; Zhong et al. 2023) | 2026-01 | GPT-4o-mini | 21.0% | $2.21 (est.) |

† Mean over 500 questions (planner+reader; excl. ingest/judge). Median: $1.11/10³ Q ≈ 14.6k tokens/question—more representative of a typical query; the mean is pulled up by a long tail.

## Result Analysis

### Where SodaMem sits

At 92.8% and mean $0.00161/question (≈18.3k tokens), SodaMem occupies a high-accuracy, mid-low-cost point (Figure 2); the median ($0.00111; ≈14.6k) is more favorable for a typical query, so the plotted mean is a conservative reading of the authors' own distribution. Two higher scores—agentmemory V4 at 96.2% (McCann 2026) and Mem0 2026 at 94.4% (Mem0 Research 2026)—sit roughly an order of magnitude to the right ($0.06 and $0.022 under the authors' assumptions), reflecting Opus / GPT-4o-class generators rather than Flash. Unified GPT-4o-mini academic pipelines (TiMem, MemOS, Memobase, Zep (Li et al. 2026; MemTensor 2025)) are cheaper on the answer-stage lower bound but land at ≈58–78%—well below the planner–reader loop.

![Cost vs accuracy on LongMemEval-S](images/fig2-cost-accuracy.png)

The scatter plot, titled "Cost–Accuracy Trade-off on LongMemEval-S," compares many long-memory agent frameworks (baselines, shown as lighter dots) against SodaMem (the large dark-blue dot) on two axes: **x-axis** — estimated API cost per question in USD on a log scale (the figure plots per-question cost and labels the lines with the mean $0.00161 / median $0.00111, spanning roughly 10⁻³ to 10⁻¹); **y-axis** — LongMemEval-S accuracy in percent, roughly 20% to 100%. Blue dashed lines mark SodaMem's mean cost and 92.8% accuracy; the shaded quadrant they bound is strictly dominated by SodaMem—higher cost and lower accuracy than the mean operating point. The low-cost cluster (≲10⁻³ USD) mostly sits in the mid-accuracy band (~35–80%): MemU, A-MEM, Zep, Memobase, MemOS variants. SodaMem sits at the top of the low-cost side at ~90+% accuracy and ~10⁻³–10⁻² USD, inside the favorable high-accuracy / low-cost corner. A second group of high-cost methods (10⁻²–10⁻¹ USD) reaches comparable or only marginally higher accuracy (~82–98%)—Cersei Embed/Hybrid, AgentOS, LC GPT-5-mini, EmergenceMem, Mem0 (2026), agentmemory V4—i.e., they spend ≈10–100× more for little or no accuracy gain. Several mid-cost systems (MemoryOS, Fact-Mem0 read, MemoryBank) land in the low-accuracy band, showing cost alone does not guarantee accuracy.

### Dominated quadrant and reader tier

The shaded region (cost > mean $0.00161 and accuracy < 92.8%) contains Cersei Embed / Hybrid / Full-context (Pacifio 2026), AgentOS (Framers Lab 2026), long-context GPT-5-mini (Fact-Memory Cost 2026), EmergenceMem Simple Fast (Haley et al. 2025), and MemoryBank under TiMem (Li et al. 2026; Zhong et al. 2023)—strictly worse (cost, accuracy) pairs even against the authors' mean. Under the median ($0.00111), MemoryOS and Fact-Mem0 read would enter as well. Public accuracy jumps often track reader upgrades (e.g., Mastra 84.23% → 94.87% from GPT-4o to GPT-5-mini (Mastra 2026)); SodaMem's claim is near-frontier accuracy at Flash-tier spend, undercutting Opus/GPT-4o high-score systems by ≈10–40× in estimated $/question. Caveats: protocols and judges differ; recall-context pricing undercounts multi-call planners; ingest amortization varies. With those limits, Figure 2 still shows a competitive accuracy band outside the high-cost frontier cluster, and strict dominance of several published points.

## Limitations

This preprint reports a single store-of-record configuration under Flash self-grading; the authors do not claim a unified re-run of all baselines. Cost figures for many peers are reconstructed from disclosed tokens or author USD and should be read as order-of-magnitude. Ingest-time spend and timeline-resolution ablations are left for follow-up.

## Conclusion

The authors presented SodaMem, an evidence-grounded temporal graph memory for LLM agents: typed FactEvents with provenance, temporal axes and supersession, hybrid retrieval, and a planner–reader answering loop. On LongMemEval-S, the store-of-record configuration reaches 92.8% accuracy at mean $0.00161 per question (≈18.3k tokens; median $0.00111 / ≈14.6k) with deepseek-v4-flash. Relative to public systems with estimable API cost, this point sits near the accuracy frontier while avoiding the Opus/GPT-4o high-spend cluster, and it strictly dominates several published (cost, accuracy) pairs. Remaining misses—especially temporal reasoning under self-grading—motivate session-anchored timeline resolution at ingest and independent re-judging of released answer hypotheses. The authors plan to release code, prompts, frozen store fingerprints, and the cost–accuracy compilation to support reproducible comparison.

**Covers:** Experiments (Setup and Cost Protocol; SodaMem run 92.8% / $0.00161 mean / median; baseline cost estimation), Table 1 (reproduced), Result Analysis ("Where SodaMem sits", dominated quadrant, Figure 2), Limitations, Conclusion.
