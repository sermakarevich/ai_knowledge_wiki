> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Experimental Evaluation

This section covers the full empirical record of ML-Master 2.0 as reported in Section 4 and its analysis subsections of the paper. Every number below is drawn directly from the paper (Table 1, Table 2, Figure 1, Figure 4, Figure 5, and the surrounding prose). The system under evaluation is [[ml-master-architecture]] and its core context management mechanism is [[hierarchical-cognitive-caching]].

---

### Setup

#### Benchmark: MLE-Bench (OpenAI)

MLE-Bench [Chan et al., arXiv:2410.07095, 2024] is the evaluation harness used throughout. It comprises **75 real-world Kaggle machine learning competitions**, spanning tabular data, computer vision, NLP, and time-series tasks. The benchmark is explicitly designed to go far beyond code generation: agents must navigate vast, unstructured search spaces through prolonged trial-and-error and must accumulate experience across iterations rather than relying on single-step correctness. MLE-Bench is therefore considered the quintessential test for ultra-long-horizon autonomy in the AI-for-AI (AI4AI) paradigm.

MLE-Bench tasks are graded against the original public Kaggle leaderboard. Each task has a fixed time budget; the agent must produce a valid `submission.csv` file (placed in `./submission/`) that MLE-Bench scores against held-out labels. Scoring thresholds map to bronze, silver, and gold medal bands relative to the human competition leaderboard.

#### MLE-Bench-Lite

A lightweight subset of MLE-Bench is used for ablation studies due to the high computational cost of running all 75 tasks. The paper refers to this subset as **MLE-Bench-Lite**. The ablation table (Table 2) reports results over **22 tasks** (inferred from 95.5% valid submission = 21/22, and 72.7% any-medal = 16/22, rounding consistently). The paper does not state the exact number of Lite tasks explicitly in the text, but the percentages in Table 2 are consistent with 22 tasks. Ablations on Lite use a **single representative run** per configuration (not averaged over multiple seeds), which the authors acknowledge as a limitation of ablation robustness.

#### Time Budget

Each task is allotted a **fixed 24-hour wall-clock execution budget**, matching the standard MLE-Bench protocol.

#### Hardware

Each agent run is provisioned with:
- **36 AMD EPYC vCPUs**
- **2x NVIDIA GeForce RTX 4090 GPUs**
- **1008 GB RAM** (shared across every 4 tasks)
- **1 TB SSD** (shared across every 4 tasks)

The hardware sharing model (4 tasks per machine) means memory and storage are not exclusively dedicated to a single agent run.

#### Base Language Model

The primary backbone LLM is **Deepseek-V3.2-Speciale** [Liu et al., arXiv:2512.02556, 2025], an open-source model. It is used for all coding and research reasoning. **Deepseek-V3.2 with thinking** is additionally used sparingly for context promotion operations (i.e., the P1 phase-level summarization and P2 task-level distillation operators that produce L2 Refined Knowledge and L3 Prior Wisdom entries). This choice deliberately uses an open-source backbone to contrast with the closed proprietary models (GPT-5, Gemini-2.5-Pro, o3, Gemini-3-pro-preview) used by the top competing systems.

#### Prior Wisdom Warm-Up (L3 Initialization)

Before any MLE-Bench evaluation begins, the L3 Prior Wisdom cache is pre-populated using **407 Kaggle competitions** as a warm-up dataset. These 407 competitions are explicitly chosen to **exclude all tasks that appear in MLE-Bench**, preventing data leakage. The warm-up generates task-level wisdom entries (model templates, preprocessing pipelines, stable hyperparameter priors) via the task-level context promotion operator P2 applied to each historical task. This initialization gives the agent a strong starting prior for the bootstrap phase of any new task.

#### Statistical Reporting

Main results (Table 1) are computed as the **mean +/- one standard error of the mean (SEM)** over **3 independent runs with different random seeds**. The asterisk (*) in Table 1 marks methods with incomplete reports; for those, missing seeds are padded with failing scores before computing the mean. Ablation studies (Table 2) use a single representative run per configuration and therefore carry no SEM estimates.

#### Evaluation Metrics

MLE-Bench defines the following metrics, all reported as percentages over the 75 tasks:

- **Valid submission rate**: Fraction of tasks where the agent produces a syntactically and format-valid submission file that MLE-Bench can score. A submission that crashes or produces a malformed CSV scores zero and counts as invalid.
- **Above-median rate (Median+)**: Fraction of tasks where the agent's submission outperforms the median score among all human Kaggle participants in that competition. This is equivalent to "better than 50th percentile human."
- **Any-medal rate (Avg Medal Rate)**: Fraction of tasks where the submission achieves at least a **bronze** medal by Kaggle standards -- i.e., scores in the top ~40% of all human submissions (exact threshold is competition-dependent). This is the headline metric used for ranking in the paper.
- **Silver+ rate**: Fraction of tasks where the submission achieves at least a **silver** medal -- i.e., roughly top 20% of human submissions.
- **Gold rate**: Fraction of tasks achieving a **gold** medal -- roughly top 10% of human submissions, the highest tier.
- **Bronze rate**: Implicitly defined as any-medal minus silver+. Not reported as a standalone column in Table 1 but deducible.

The **average medal rate** (any-medal across the full 75-task set) is treated as the primary ranking criterion throughout the paper.

---

### Main Results

Table 1 from the paper, reproduced in full. All values are percentages. SEM values are shown after the +/- symbol. (*) = incomplete report, padded with failing scores.

**Medal rate by difficulty tier:**

| Agent | Base Model | Low (%) | Medium (%) | High (%) | Avg Medal (%) | Valid (%) | Median+ (%) | Silver+ (%) | Gold (%) |
|---|---|---|---|---|---|---|---|---|---|
| **ML-Master 2.0 (ours)** | Deepseek-V3.2-Speciale | **75.8 +/- 1.5** | **50.9 +/- 3.5** | **42.2 +/- 2.2** | **56.4 +/- 2.5** | **95.6 +/- 1.2** | **63.1 +/- 1.2** | **45.3 +/- 2.0** | **19.6 +/- 0.9** |
| Leeroo* | Gemini-3-pro-preview | 68.2 +/- 2.6 | 44.7 +/- 1.5 | 40.0 +/- 0.0 | 50.7 +/- 1.3 | 50.7 +/- 1.3 | 50.7 +/- 1.3 | 36.4 +/- 1.6 | 21.3 +/- 2.0 |
| Thesis | gpt-5-codex | 65.2 +/- 1.5 | 45.6 +/- 7.2 | 31.1 +/- 2.2 | 48.4 +/- 3.6 | 90.2 +/- 2.4 | 56.0 +/- 2.8 | 32.9 +/- 5.1 | 20.0 +/- 3.4 |
| MLE-STAR-Pro-1.5 | Gemini-2.5-Pro | 68.2 +/- 2.6 | 34.2 +/- 1.5 | 33.3 +/- 0.0 | 44.0 +/- 1.3 | 93.8 +/- 0.4 | 52.9 +/- 1.6 | 30.2 +/- 2.9 | 19.1 +/- 1.8 |
| FM Agent | Gemini-2.5-Pro | 62.1 +/- 1.5 | 36.8 +/- 1.5 | 33.3 +/- 0.0 | 43.6 +/- 0.9 | 96.9 +/- 1.2 | 51.6 +/- 1.2 | 35.1 +/- 1.2 | **22.7 +/- 0.8** |
| R&D-Agent | gpt-5 | 68.2 +/- 2.6 | 21.1 +/- 1.5 | 22.2 +/- 2.2 | 35.1 +/- 0.4 | 53.3 +/- 0.0 | 40.4 +/- 0.9 | 28.4 +/- 1.6 | 16.4 +/- 0.9 |
| AIRA-dojo | o3 | 55.0 +/- 1.5 | 22.0 +/- 1.2 | 21.7 +/- 1.1 | 31.6 +/- 0.8 | **97.5 +/- 0.3** | 45.5 +/- 0.8 | 25.9 +/- 0.8 | 17.3 +/- 0.4 |
| ML-Master (v1) | Deepseek-R1 | 48.5 +/- 1.5 | 20.2 +/- 2.3 | 24.4 +/- 2.2 | 29.3 +/- 0.8 | 93.3 +/- 1.3 | 44.9 +/- 1.2 | 25.0 +/- 0.9 | 17.3 +/- 0.8 |
| AIDE | o1-preview | 35.9 +/- 1.9 | 8.5 +/- 0.4 | 11.7 +/- 1.3 | 17.1 +/- 0.6 | 82.8 +/- 1.1 | 29.4 +/- 1.3 | 13.5 +/- 0.7 | 9.4 +/- 0.8 |
| OpenHands | gpt-4o-24-08 | 12.1 +/- 1.5 | 1.8 +/- 0.9 | 2.2 +/- 2.2 | 4.9 +/- 0.4 | 52.0 +/- 3.3 | 7.1 +/- 1.7 | 4.0 +/- 1.0 | 2.7 +/- 1.1 |
| MLAB | gpt-4o-24-08 | 4.6 +/- 0.9 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 1.6 +/- 0.3 | 44.3 +/- 2.6 | 1.9 +/- 0.7 | 0.8 +/- 0.3 | 0.8 +/- 0.5 |

**Notes on the table:**
- The Leeroo entry is marked with (*) indicating an incomplete report; results are computed by padding missing seeds with failing scores.
- FM Agent achieves the highest gold rate (22.7%) among all methods, edging out ML-Master 2.0 (19.6%), but its overall any-medal rate (43.6%) is substantially lower.
- AIRA-dojo (o3) achieves the highest valid submission rate (97.5%), marginally above ML-Master 2.0's 95.6%.
- ML-Master 2.0 is the only entry in the top-5 that uses an open-source backbone; all others (Leeroo, Thesis, MLE-STAR-Pro-1.5, FM Agent) use closed proprietary models.
- The paper internally refers to ML-Master 2.0 as "ML-ACE" in some prose passages (Section 4.2 heading), but Table 1 uses "ML-Master 2.0 (ours)" -- this appears to be a naming inconsistency in the manuscript.

---

### Difficulty Breakdown

MLE-Bench partitions its 75 tasks into three difficulty tiers: **Low**, **Medium**, and **High**. The criteria for tier assignment are defined by MLE-Bench itself (based on competition complexity, dataset size, and historical human performance spread). Figure 1 in the paper provides a grouped bar chart comparison across all evaluated systems.

**ML-Master 2.0 vs. ML-Master v1 by tier:**

| Difficulty | ML-Master 2.0 | ML-Master v1 | Absolute gain | Relative gain |
|---|---|---|---|---|
| Low | 75.8% | 48.5% | +27.3 pp | +56.3% |
| Medium | 50.9% | 20.2% | +30.7 pp | +152.0% |
| High | 42.2% | 24.4% | +17.8 pp | +72.9% |
| All (avg) | 56.4% | 29.3% | +27.1 pp | +92.5% |

The paper states: "performance on low-complexity tasks improves from 48.48% to 75.76%, while medium-complexity and high-complexity tasks improve from 20.18% to 50.88% and from 24.44% to 42.22%, respectively." These figures from the introduction prose match the Table 1 values within rounding.

**Key observation:** The largest absolute gains are in the Medium tier (+30.7 pp), suggesting [[hierarchical-cognitive-caching]] is particularly valuable for tasks that require multi-phase iterative refinement -- tasks hard enough to require sustained strategy but not so hard that compute runs out entirely.

**All baselines by difficulty tier (from Table 1 and Figure 1):**

| Agent | Low (%) | Medium (%) | High (%) | All (%) |
|---|---|---|---|---|
| ML-Master 2.0 | 75.8 | 50.9 | 42.2 | 56.4 |
| Leeroo* | 68.2 | 44.7 | 40.0 | 50.7 |
| Thesis | 65.2 | 45.6 | 31.1 | 48.4 |
| MLE-STAR-Pro-1.5 | 68.2 | 34.2 | 33.3 | 44.0 |
| FM Agent | 62.1 | 36.8 | 33.3 | 43.6 |
| R&D-Agent | 68.2 | 21.1 | 22.2 | 35.1 |
| AIRA-dojo | 55.0 | 22.0 | 21.7 | 31.6 |
| ML-Master v1 | 48.5 | 20.2 | 24.4 | 29.3 |
| AIDE | 35.9 | 8.5 | 11.7 | 17.1 |
| OpenHands | 12.1 | 1.8 | 2.2 | 4.9 |
| MLAB | 4.6 | 0.0 | 0.0 | 1.6 |

**Observation on high-difficulty tasks:** ML-Master 2.0 achieves 42.2% on High tasks -- considerably ahead of the next best (Leeroo at 40.0%, though Leeroo is marked incomplete). Among complete reports, FM Agent and MLE-STAR-Pro-1.5 both reach 33.3% on High tasks, leaving a gap of approximately 9 percentage points to ML-Master 2.0. This is attributed in the paper to HCC's ability to sustain coherent strategy over tens of hours without context saturation, a problem that disproportionately affects high-complexity tasks with longer interaction sequences.

**Performance over time (Figure 5):** A time-series plot shows ML-Master 2.0's average medal rate rising monotonically as a function of wall-clock hours (0 to 24). The smoothed curve rises steeply in the first 4--8 hours (initial solutions, quick wins) and continues to climb through hours 8--24 (iterative refinement phases). This continuous improvement profile is a direct demonstration that [[context-migration-protocol]] successfully prevents context saturation from stalling progress -- competing systems that hit context limits would show a plateau or decline in this curve.

---

### Ablation Studies (MLE-Bench-Lite)

Table 2 from the paper: ablation of the [[hierarchical-cognitive-caching]] architecture on MLE-Bench-Lite. Each row removes one tier of the cache hierarchy while keeping the others. Experiments use a **single representative run** per configuration (no SEM). Best performances in bold.

| Row | L1 (Experience) | L2 (Knowledge) | L3 (Wisdom) | Valid Sub. (%) | Above Median (%) | Any Medal (%) |
|---|---|---|---|---|---|---|
| 1 -- No L1 (no iterative execution) | X | -- | checkmark | 54.5 | 36.4 | 22.7 |
| 2 -- No L2 (raw context only) | checkmark | X | checkmark | 95.5 | 81.8 | 59.1 |
| 3 -- No L3 (no prior wisdom) | checkmark | checkmark | X | 95.5 | 72.7 | 54.5 |
| 4 -- Full HCC (all three tiers) | checkmark | checkmark | checkmark | **95.5** | **81.8** | **72.7** |

**Interpretation of each ablation row:**

**Row 1 -- Removing L1 (No Evolving Experience / no iterative execution):**
Without L1, the agent loses the capability to iteratively interact with the environment for code refinement. The paper notes that the absence of L1 consequently also entails the absence of L2 (since L2 is populated by promoting L1 traces). Valid submission rate drops sharply from 95.5% to **54.5%**, and any-medal rate collapses from 72.7% to **22.7%**. This is the most catastrophic single ablation. The paper concludes that "evolving experience's foundational role when handling ultra-long-horizon tasks" is confirmed -- without the raw execution loop, the agent cannot generate the trial-and-error cycles that drive improvement.

**Row 2 -- Removing L2 (Raw context only, no Refined Knowledge):**
The agent retains L1 (raw execution traces) and L3 (prior wisdom) but has no L2 summarization layer. All historical interaction traces are kept in raw format in context. Valid submission rate is maintained at 95.5%, and above-median rate is maintained at 81.8% -- matching the full system. However, **any-medal rate drops from 72.7% to 59.1%** (-13.6 pp). The paper states: "retaining raw context allows for average performance, the Refined Knowledge is indispensable for synthesizing the complex solutions required to reach top-tier performance." The L2 cache is critical for converting good solutions into medal-caliber solutions -- it enables the agent to revisit validated insights without carrying verbose execution logs, stabilizing strategic reasoning across tens of hours.

**Row 3 -- Removing L3 (No Prior Wisdom):**
The agent has L1 and L2 but no warm-started L3 prior wisdom. Valid submission rate remains at 95.5%. Above-median rate drops from 81.8% to **72.7%** (-9.1 pp), and any-medal rate drops from 72.7% to **54.5%** (-18.2 pp). The paper states: "Prior Wisdom provides a strong initialization that substantially reduces ineffective exploration, which is critical for achieving competitive performance." Without L3, the agent wastes early exploration on approaches that experienced wisdom would immediately rule out.

**Synergy of all three tiers:** The full HCC configuration (Row 4) is strictly better than all ablations on any-medal rate. The gains from L2 and L3 are not additive in a simple sense -- the full system's 72.7% exceeds the sum of individual contributions, indicating synergistic interaction between the three cache levels. This aligns with the [[cognitive-accumulation-paradigm]] theoretical framing: each tier supports the others (L1 feeds L2, L2 feeds L3, L3 bootstraps L1).

#### Ablation Limitations

The paper explicitly acknowledges that ablation experiments are conducted on MLE-Bench-Lite (a subset of 75 tasks), with a **single representative run per configuration** (no multiple seeds, no SEM). This means the ablation results carry higher variance than the main results. Direct quantitative comparison between absolute ablation numbers and main-table numbers should be made cautiously, as Lite may not be representative of the full benchmark distribution.

No additional ablation axes are reported in the paper. Specifically, the paper does not include:
- Sensitivity to the warm-up dataset size (407 competitions is presented as a single fixed value with no ablation curve)
- Sensitivity to the retrieval similarity threshold delta used in context prefetching
- Ablations over different base LLMs (only Deepseek-V3.2-Speciale is tested for ML-Master 2.0; ML-Master v1 used Deepseek-R1, but this is a different system version, not a controlled ablation)
- Ablation of the number of exploration directions m or implementation suggestions q per phase

---

### Case Studies

#### Context-Length Case Study: task "random-acts-of-pizza"

Figure 4 in the paper provides the most concrete quantitative illustration of [[context-migration-protocol]] in action, using the task **random-acts-of-pizza** (a Reddit dataset of 5,671 textual pizza requests, where the goal is to predict which requests will receive a pizza donation -- a binary classification problem evaluated on kindness prediction).

**Key numbers from Figure 4:**

| Metric | Without HCC (full context) | With HCC |
|---|---|---|
| Peak context length | > 200,000 tokens | ~70,000 tokens |
| Medal achieved? | Not stated (implied: no, or very late) | Yes -- bronze, during 4th research plan iteration |

The orange line (full context accumulation without HCC) shows context growing monotonically and rapidly past 200k tokens, particularly when debugging is introduced to handle terminal output errors. The blue line (HCC context) is substantially lower throughout -- rising during active phases but being compressed at phase boundaries via context promotion -- and stays near or below 70k tokens at peak.

**Narrative of the four research plan phases (Figure 4 annotation):**

- **Research Plan 1**: Initial approach using pre-trained sentence transformers (all-MiniLM-L6-v2) for text feature generation; additional lexical features including counts of politeness markers; scheduling optimization with subscriber-related features; sentiment scores (compound, positive, negative); Bayesian hyperparameter optimization (Optuna); experiments with boosting types.
- **Research Plan 2**: Fine-tuning a RoBERTa-base transformer model; end-to-end fine-tuning noted as computationally prohibitive; Optuna tuning with full-dataset cross-validation; probability calibration after LightGBM predictions; SHAP-based feature selection; target encoding for subreddit list.
- **Research Plan 3**: Fine-tuning a transformer model (e.g., RoBERTa-base) with additional components; using DeBERTa-v3-base; LIWC feature extraction using LIWC2015 dictionary; comprehensive set of readability and stylistic features; learning subreddit embeddings from scratch; aggregated success statistics for each subreddit using 5-fold target encoding.
- **Research Plan 4**: Computing rolling historical success rate for each request using its timestamp (highlighted as the decisive insight); implementing time-ordered cross-validation. **Gets first medal during this phase.**

The critical insight enabling the medal -- computing temporal success rates using timestamps -- is exactly the type of dataset-specific strategy that L3 Prior Wisdom from similar text classification tasks would prime the agent to consider. The HCC architecture, by keeping the research plan history in compact L2 summaries rather than raw traces, allowed the agent to reach Research Plan 4 without hitting the context limit that would have forced early termination.

Without HCC, the agent's context would have exceeded 200k tokens somewhere during Research Plan 2 or 3, either truncating critical history or triggering a context overflow error that prevents further iteration. The medal is only achievable because the fourth iteration is reachable -- a direct demonstration of the value of [[hierarchical-cognitive-caching]].

#### Qualitative Example: Context Migration in task "plant-pathology-2021-fgvc8"

Figure 3 in the paper illustrates an example of context migration (all three context migration operations: prefetch, hit, and promotion) using the task **plant-pathology-2021-fgvc8** (multi-label image classification of apple leaf diseases from RGB images, evaluated on validation F1 score).

**Context Prefetch phase (L3 -> context):**
The agent queries L3 with the task embedding. Retrieved prior wisdom includes:
- "Augmentation: Apply training augmentation including cropping [more augmentation related wisdom...]"
- "Backbone: vit_base_patch16_224 (Vision Transformer); Initialization: [more model related wisdom...]"

This gives the agent an informed starting point before any code is executed.

**Context Hit phase (L1/L2 retrieval during active execution):**
During the active phase, the agent's context includes (shown in the figure):
- Initial code skeleton referencing the backbone (vit_base_patch16_224, Vision Transformer)
- Terminal output showing: "Epoch 8/8 - Loss: 0.1677 - Val F1 (0.5): 0.87701"
- Research plan entry: "The research confirmed that interventions like Asymmetric Loss proved [more refined knowledge...]"
- Instruction: "Please implement the idea xxx based on current best code [current best code...]"

**Context Promotion phase (L1 -> L2 -> L3):**
After phase completion, the promotion operator P1 produces a refined knowledge entry. The figure shows the resulting L2 Refined Knowledge entry containing:
- `"model_design": {"1": "Use ConvNeXt Large (timm: 'convnext_large_in22h1k') with [...]", "2": "[detailed ideas...]"}`
- `"loss_design": [{(more detailed ideas...)}]`

Subsequently, P2 produces a task-level wisdom entry noting: "The research confirmed that scaling to a ConvNeXt Large backbone with 384x384 resolution was the decisive factor. [more refined knowledge...]"

This example concretely shows L2 capturing actionable judgments ("ConvNeXt Large at 384x384 is decisive") in a compact structured form, and L3 capturing that judgment as transferable wisdom for future vision classification tasks.

#### Performance-over-Time Profile (Figure 5)

Figure 5 plots the evolution of ML-Master 2.0's average medal rate on the y-axis against iteration time (0--24 hours) on the x-axis. Both the raw (noisy) curve and a smoothed curve are shown. Qualitative features:

- The curve rises continuously from 0% at t=0 toward approximately 55--60% by t=24 hours.
- There is no visible plateau or decline, which would be the signature of context saturation.
- The steepest ascent occurs in the first 4--8 hours as initial solutions are generated.
- A secondary improvement phase is visible around hours 8--16, corresponding to iterative refinement phases guided by L2 knowledge.
- The curve is still climbing at t=24 hours, suggesting additional time budget might yield further gains -- the 24-hour limit is a benchmark constraint, not a performance ceiling.

This contrasts with the expected behavior of systems without HCC, which would show flattening or degradation after context saturation as the agent can no longer maintain coherent strategy.

---

### Failure and Limitation Analysis

#### Where ML-Master 2.0 Still Fails

ML-Master 2.0 achieves **42.2% on High-difficulty tasks**, meaning it fails to earn any medal on **57.8% of the hardest tasks**. Even on Low tasks, it achieves only 75.8%, failing on approximately 1 in 4 easy tasks. The paper does not provide a detailed breakdown of failure modes by task type (e.g., specific failure rates for vision vs. tabular vs. NLP), so granular analysis is not possible from the reported data.

The **valid submission rate of 95.6%** implies approximately 3--4 tasks out of 75 where the agent fails to produce even a scoreable submission -- likely due to environment crashes, format errors, or time budget exhaustion before any valid code runs.

The paper does not discuss specific tasks where ML-Master 2.0 systematically underperforms relative to its competition (e.g., tasks where R&D-Agent or FM Agent beat it on gold rate). FM Agent achieves a higher gold rate (22.7% vs. 19.6%), suggesting that for the highest-difficulty top-tier competitions, FM Agent's architecture may have advantages -- possibly due to different search or ensembling strategies.

#### Evaluation Robustness Limitations

- **Ablations on a single seed**: Table 2 (ablation study) uses a single representative run per configuration on MLE-Bench-Lite. This is insufficient to reliably estimate variance; differences of ~10--15 pp between ablation rows could partially reflect run-to-run variability rather than purely architectural effects.
- **Leeroo marked incomplete**: The primary competitor (Leeroo at 50.7%) is marked with an asterisk indicating an incomplete report -- missing seeds are padded with failing scores. This means Leeroo's true performance could be higher than 50.7%, narrowing or eliminating ML-Master 2.0's 5.7 pp lead over the previous proprietary SOTA.
- **No cross-task analysis**: The paper does not report per-task performance, which would reveal whether ML-Master 2.0's gains are broadly distributed or concentrated in particular task categories.
- **Warm-up dataset not ablated**: The effect of using 407 vs. fewer warm-up competitions on L3 wisdom quality is not investigated. It is possible that much of the L3 benefit comes from a small fraction of highly relevant competitions, and the full 407 are not necessary.
- **Hardware sharing**: The 4-tasks-per-machine hardware sharing model means that individual runs may experience variable compute availability, introducing an additional source of variance beyond random seed.

#### Compute Costs

The paper does not explicitly report per-run token consumption, GPU-hours, or API costs. The statement "due to the expensive cost of running complete MLE-Bench" (Section 4.1) acknowledges that full MLE-Bench evaluation is costly, motivating the use of reported baselines rather than re-running all competing systems. No quantitative cost figure (USD, GPU-hours, or token count) is provided for a single ML-Master 2.0 run.

The use of Deepseek-V3.2-Speciale (open-source) rather than GPT-5 or Gemini-2.5-Pro is noted as an explicit design choice, implying that operational cost was a consideration. The use of Deepseek-V3.2 with thinking "sparingly" for context promotion further suggests that thinking-mode calls are reserved for high-value distillation operations to control cost.

---

### Relative Improvements and Competitive Positioning

#### Versus ML-Master v1 (prior system)

| Metric | ML-Master v1 | ML-Master 2.0 | Absolute change | Relative change |
|---|---|---|---|---|
| Avg Medal Rate | 29.3% | 56.4% | +27.1 pp | +92.5% |
| Valid Submission | 93.3% | 95.6% | +2.3 pp | +2.5% |
| Above Median | 44.9% | 63.1% | +18.2 pp | +40.5% |
| Silver+ | 25.0% | 45.3% | +20.3 pp | +81.2% |
| Gold | 17.3% | 19.6% | +2.3 pp | +13.3% |
| Low difficulty | 48.5% | 75.8% | +27.3 pp | +56.3% |
| Medium difficulty | 20.2% | 50.9% | +30.7 pp | +152.0% |
| High difficulty | 24.4% | 42.2% | +17.8 pp | +72.9% |

The paper's abstract states a **92.7% relative improvement** over ML-Master (v1). This matches the computed 92.5% within rounding (the abstract rounds 29.3% to 29%, so 27.1/29.3 = 0.925 = 92.5%; or 27.14/29.3 = 92.6% when using the abstract's "92.7%").

v1 used rule-based Monte Carlo Tree Search (MCTS) as its exploration mechanism and Deepseek-R1 as its backbone. v2 replaces MCTS with the HCC-governed agent-centric loop, substitutes Deepseek-V3.2-Speciale for Deepseek-R1, and adds the full three-tier [[hierarchical-cognitive-caching]] architecture.

#### Versus Previous Proprietary SOTA

The paper identifies Leeroo (Gemini-3-pro-preview, avg medal 50.7%) as the previous best proprietary LLM-based method.

| Metric | Leeroo* | ML-Master 2.0 | Absolute change | Relative change |
|---|---|---|---|---|
| Avg Medal Rate | 50.7% | 56.4% | +5.7 pp | +11.2% |
| Valid Submission | 50.7% | 95.6% | +44.9 pp | +88.6% |
| Above Median | 50.7% | 63.1% | +12.4 pp | +24.5% |
| Silver+ | 36.4% | 45.3% | +8.9 pp | +24.5% |
| Gold | 21.3% | 19.6% | -1.7 pp | -8.0% |

The **valid submission rate** comparison is striking: Leeroo submits validly on only 50.7% of tasks, while ML-Master 2.0 achieves 95.6%. This large gap suggests that Leeroo frequently fails to produce a scoreable submission -- possibly due to time management issues, context exhaustion, or environment handling problems. ML-Master 2.0's robustness advantage is therefore not only in medal quality but in task completion reliability.

The **gold rate** is the one dimension where ML-Master 2.0 trails Leeroo (19.6% vs. 21.3%), though Leeroo is marked as an incomplete report, making this comparison uncertain.

#### Open-Source vs. Closed-Source Context

This is highlighted prominently by the authors as a key finding. ML-Master 2.0 achieves state-of-the-art medal rates using **Deepseek-V3.2-Speciale (open-source)**, while the top competing systems use:
- Leeroo: Gemini-3-pro-preview (closed, proprietary Google model)
- Thesis: gpt-5-codex (closed, proprietary OpenAI model)
- MLE-STAR-Pro-1.5: Gemini-2.5-Pro (closed, proprietary)
- FM Agent: Gemini-2.5-Pro (closed, proprietary)
- AIRA-dojo: o3 (closed, proprietary OpenAI model)

The implication is that the [[cognitive-accumulation-paradigm]] and [[hierarchical-cognitive-caching]] architecture provide an architectural advantage that more than compensates for any capability gap between open-source and proprietary frontier models. The paper frames this as evidence that "structured cognitive accumulation is the critical enabler" -- i.e., the agent's architecture matters more than raw model capability for ultra-long-horizon tasks.

---

### Connections to Architecture

The experimental results map directly onto the architectural components described in the HCC framework:

- The ablation showing L1 removal collapses valid submission rate to 54.5% validates the claim that [[ml-master-architecture]]'s iterative execution loop (the L1 Evolving Experience layer) is foundational -- without raw execution feedback, the agent cannot debug or refine solutions.
- The ablation showing L3 removal drops medal rate by 18.2 pp validates the [[context-migration-protocol]]'s task-level promotion operator P2: the 407-competition warm-up database meaningfully bootstraps each new task.
- The context-length case study (70k with HCC vs. >200k without) validates the core design claim that [[hierarchical-cognitive-caching]] prevents context saturation -- empirically demonstrating that phase-boundary promotion via P1 and the context hit policy compress context by approximately 65--70% on a representative task.
- The continuous performance improvement profile (Figure 5) validates that HCC enables genuine ultra-long-horizon autonomy -- the system does not plateau, which would be the signature of context window saturation in competing systems.