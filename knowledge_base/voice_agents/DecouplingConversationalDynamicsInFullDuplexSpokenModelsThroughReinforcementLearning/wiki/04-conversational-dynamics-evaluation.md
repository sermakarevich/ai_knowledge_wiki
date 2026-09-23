> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Conversational Dynamics Evaluation
**In one sentence:** DuplexPO improves window-level turn-taking and backchannel behavior, breaks the latency–interruption trade-off in mid-turn regions, and is preferred by a conversation-level judge while preserving model intelligence.
## Key points
- DuplexPO achieves the best overall window-level performance with the highest initiation and yield rates for both turn-taking and backchannels, plus the lowest onset MAE on both Fisher and Seamless datasets.
- SFT Dynamics alone is insufficient: it regresses across all dynamics metrics relative to the SFT Baseline, showing SFT cannot learn robust conversational coordination from natural dynamics patterns.
- In ambiguous mid-turn regions, commercial models and Ultravox get reasonable turn-taking accuracy but high latency (conservative endpointing), while Moshi and PersonaPlex get low latency but high VIR (premature interruptions); SFT Dynamics gets low VIR and high Yield Rate only via long latencies.
- DuplexPO breaks this trade-off: it preserves perfect turn-taking, achieves the highest Yield Rate and lowest latency among all models, and keeps VIR competitively low.
- The conversation-level pairwise judge prefers DuplexPO in 76.9% of Fisher comparisons (n=26) and 69.3% of non-tie Seamless comparisons (n=383), with dimension-level preferences consistent with automatic metrics.
- On model intelligence (Table 4), DuplexPO preserves SFT Baseline capability with small consistent gains (e.g. LlamaQ 75.3 vs 72.0, OBQA 73.7 vs 72.2, MMSU 56.2 vs 54.9, AlpacaE 3.68 vs 3.43, ComE 3.74 vs 3.48).
- DuplexPO releases suppressed <BOS> impulses more selectively than SFT and shifts <EOS>/<BOS> behavior near boundary-control decisions rather than globally suppressing speaking intent.
---
## 6.1 Conversational Dynamics
**Covers:** Section 6.1, Figure 2 (Fisher n=26; Seamless n=383)

Comparison setup (verbatim):

> "We compare DuplexPO with two SFT-only baselines. SFT Baseline is trained without dynamics-aware dialogue data, whereas SFT Dynamics uses the same SFT recipe as DuplexPO and includes the reconstructed dynamics-aware dialogue data."

Window-level results (verbatim):

> "Table 2 shows that DuplexPO consistently improves window-level turn-taking and backchannel behavior on both Fisher and Seamless. SFT Dynamics shows that SFT alone is insufficient for learning robust conversational coordination from natural dynamics patterns, regressing across all dynamics metrics relative to the SFT Baseline. DuplexPO achieves the best overall performance, with the highest initiation and yield rates for both turn-taking and backchannels, as well as the lowest onset MAE on both datasets."

Mid-turn latency–interruption trade-off (verbatim):

> "Table 3 examines whether these window-level gains transfer to ambiguous mid-turn regions where premature responses cause barge-ins. The results reveal a latency-interruption trade-off among existing models. Commercial models and Ultravox achieve reasonable turn-taking accuracy but incur high latency, reflecting conservative endpointing strategies that wait for extended silence. In contrast, open-source duplex models such as Moshi and PersonaPlex reduce latency through always-on listening, but suffer from substantially higher VIR due to premature interruptions. Among our ablations, SFT Dynamics attains low VIR and high Yield Rate only by adopting long latencies, effectively trading responsiveness for caution."

DuplexPO claim (verbatim):

> "DuplexPO breaks this trade-off. It preserves perfect turn-taking, achieves the highest Yield Rate and the lowest latency among all models, and keeps VIR competitively low."

Mechanism interpretation (verbatim):

> "These results suggest that dynamics-aware RL learns coordinated floor control rather than simply biasing the agent toward eagerness or caution. By using mid-turn dynamics evidence to distinguish true completion from disfluent continuation, DuplexPO can respond promptly when the user yields while reliably yielding when the user retains the floor."

Figure 2 — conversation-level pairwise judge:

> "Figure 2: Conversation-level Gemini pairwise evaluation comparing the SFT Baseline (A) with DuplexPO (B). The judge observes timestamps, transcripts, and aggregate dynamics statistics to assess turn-taking, backchanneling, and barge-in handling."

> "(a) Pairwise Judge Evaluation on Fisher test set (n=26)"
> "(b) Pairwise Judge Evaluation on Seamless test set (n=383)"

Outcome (verbatim):

> "Figure 2 evaluates whether these metric gains are reflected at the conversation level. The pairwise judge prefers DuplexPO in 76.9% of Fisher comparisons and 69.3% of non-tie Seamless comparisons. Dimension-level preferences are consistent with the automatic metrics for turn-taking, backchanneling, and user barge-in handling."

## 6.2 Model Intelligence
**Covers:** Section 6.2, Table 4

Claim (verbatim):

> "Table 4 addresses the second side of the proposed intelligence–dynamics trade-off. Across factual QA, instruction following, speech understanding, and reasoning, DuplexPO preserves the SFT Baseline's task-level capability and yields small but consistent improvements. Although the magnitude of these gains is modest, their direction is important because optimizing the real-time speaking policy does not degrade the semantic and reasoning abilities learned during SFT."

Table 4 caption (verbatim):

> "Table 4: Model intelligence evaluation. QA, OpenBookQA, and MMSU metrics are accuracy in %; AlpacaEval and CommonEval are GPT-scores on a 1–5 scale. Baseline results are taken from [Yu et al., 2025, Chen et al., 2024]. FD denotes full duplex. LlamaQ, WebQ, TriQA, OBQA, AlpacaE, and ComE denote Llama Questions, WebQuestions, TriviaQA, OpenBookQA, AlpacaEval, and CommonEval."

| Method | FD | LlamaQ | WebQ | TriQA | SDQA | AlpacaE | ComE | OBQA | MMSU |
|---|---|---|---|---|---|---|---|---|---|
| Moshi [Défossez et al., 2024] | ✓ | 54.5 | 22.1 | 16.7 | 15.6 | 2.01 | 1.60 | 25.9 | 24.0 |
| Freeze-Omni [Wang et al., 2024b] | ✓ | 56.2 | 27.9 | 28.5 | 53.5 | 4.03 | 3.46 | 31.0 | 28.1 |
| SALMONN-omni [Yu et al., 2025] | ✓ | 73.6 | 43.7 | 56.0 | - | 3.22 | - | - | 30.0 |
| SALM-Duplex [Hu et al., 2025] | ✓ | 51.3 | 25.0 | 16.9 | 26.0 | 2.99 | 2.50 | 39.6 | 26.3 |
| GLM-4-Voice [Zeng et al., 2024] | ✗ | 65.7 | 37.0 | 47.5 | 37.0 | 3.97 | 3.42 | 53.4 | 39.8 |
| Qwen2-Audio [Chu et al., 2024] | ✗ | 69.7 | 45.2 | 40.3 | 35.7 | 3.74 | 3.43 | 49.5 | 35.7 |
| Kimi-Audio [Ding et al., 2025] | ✗ | 68.3 | 37.3 | 51.2 | 63.1 | 4.46 | 3.97 | 83.5 | 62.2 |
| Baichuan-Audio [Li et al., 2025] | ✗ | 74.0 | 40.7 | 53.0 | 45.8 | 4.41 | 4.08 | 71.7 | 53.2 |
| STITCH-R [Chiang et al., 2025] | ✗ | 70.0 | 50.3 | 49.6 | - | 2.70 | - | - | - |
| SFT Baseline | ✓ | 72.0 | 44.3 | 48.1 | 47.2 | 3.43 | 3.48 | 72.2 | 54.9 |
| DuplexPO | ✓ | 75.3 | 44.5 | 49.9 | 49.8 | 3.68 | 3.74 | 73.7 | 56.2 |

## 6.3 Discussion and Visualization; Limitations; Conclusion
**Covers:** Sections 6.3–7, Figure 3

Suppressed-intent metrics defined in Appendix C (verbatim):

> "We analyze how DuplexPO reshapes conversational behavior using two metrics defined in Appendix C: Suppressed Intent Rate (SIR), measuring how often latent boundary intent is suppressed, and Suppression Release Ratio (SRR), measuring whether suppressed intent is later released."

Findings (verbatim):

> "Figure 3(b) shows that DuplexPO releases suppressed <BOS> impulses more selectively than the SFT model, while Figure 3(a) shows consistent <EOS> urge trajectories around user barge-ins."

> "Overall, DuplexPO does not globally suppress speaking intent, but instead shifts behavior near boundary-control decisions, releasing latent <BOS> and <EOS> impulses according to the local conversational state."

Figure 3 caption (verbatim):

> "Figure 3: Analysis of suppressed boundary intent in SFT Baseline and DuplexPO. (a) <EOS> impulse around user interruption onset on Fisher test set (n=148 events from 20 conversations). Both policies are evaluated on the SFT trajectory; shaded regions show 95% CI. (b) Suppressed-intent analysis."

Figure 3(b) values (in %):

| Dataset | <BOS> Impulses SIR | <BOS> Impulses SRR | <EOS> Impulses SIR | <EOS> Impulses SRR |
|---|---|---|---|---|
| Fisher | 11.0 | 70.6 | 4.9 | 100.0 |
| FDB-v3 | 10.8 | 71.9 | 0.9 | 100.0 |

Ablations in chunk (verbatim, three design choices):

> "First, longer lead times sharply reduce mean RL reward, whereas buffer time has a milder effect, showing that supervision must stay close to boundary events (Appendix H; Figure 7). Second, replacing FCDR with a neural reward model based on a learned temporal state predictor yields partial gains over SFT Dynamics but remains less reliable than FCDR, likely because coarse teacher-derived states can disturb fine-grained SFT behaviors."

> "Third, replacing GRPO with a DPO objective based on the highest- and lowest-reward continuations yields weaker performance on most dynamics metrics, particularly yield-oriented metrics, suggesting that group-normalized advantages better exploit the full reward distribution rather than only the extremes (Appendix J)."

Limitations (verbatim):

> "DuplexPO's factorized rewards enable interpretable event-level credit assignment, but may miss subtle pragmatic factors such as user intent, discourse content, speaker style, and culture-specific timing preferences. Human timing annotations are also not unique ground truth, since turn initiation, backchanneling, and yielding can vary across speakers, languages, and conversational settings. As policy updates are restricted to local dynamics-critical windows, DuplexPO may also miss long-range dialogue effects."

Conclusion (verbatim):

> "We identified the trade-off between conversational dynamics and model intelligence in full-duplex spoken language models. We argue that this trade-off largely stems from coupling what to say with when to speak, rather than from an inherent conflict between the two. We propose DuplexPO, an RL framework that preserves instruction-tuned semantic capability while optimizing real-time speaking decisions over dynamics-critical windows. Experiments show that DuplexPO improves turn-taking, backchanneling, and barge-in handling without degrading instruction following, factual QA, speech understanding, or reasoning."

**Covers:** Sections 6.1–7; Figure 2 (Fisher n=26, Seamless n=383); Table 4; Figure 3 (Fisher n=148 events from 20 conversations; SIR/SRR table)
