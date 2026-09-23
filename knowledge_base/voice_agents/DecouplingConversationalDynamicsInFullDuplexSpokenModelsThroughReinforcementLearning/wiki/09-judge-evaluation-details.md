> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Candidate B observable rhythm summary
**In one sentence:** The chunk defines a Candidate B observable-rhythm slot (turns, speech time, overlaps, interruptions, post-user pause) but supplies only unresolved template placeholders rather than values, with the remaining body consisting of appendix material on reward dynamics, window/reward/optimization ablations, a conversational-pattern example, and broader impacts.
## Key points
- Candidate B rhythm fields are listed but unresolved: `n_turns` is `{candidate_b_n_turns}`, `total_speech_ms` is `{candidate_b_total_speech_ms}`, `total_user_overlap_ms` is `{candidate_b_total_user_overlap_ms}`, `n_user_overlaps` is `{candidate_b_n_user_overlaps}`, `n_interrupted_by_user` is `{candidate_b_n_interrupted_by_user}`, and `median_pause_after_user_ms` is `{candidate_b_median_pause_after_user_ms}` — no Candidate B numbers can be reported.
- Total reward "rises monotonically and then plateaus, indicating stable optimisation" (Figure 5 caption/description).
- Stop and start rewards "specialise on yielding and turn initiation respectively, with low cross-talk" (Figure 6 description).
- Window lead-time ablation shows "a clear ordering in mean reward, with overly long lead times causing a substantial performance drop", while varying buffer time "yields no significant separation, with the mean rewards differing by at most 0.02".
- Neural-reward-model (SoulX-Duplug teacher) ablation: NRM improves over SFT Dynamics on several metrics but "does not consistently surpass the original SFT Baseline", whereas FCDR reaches e.g. Fisher Onset MAE 0.69 with 100.0% turn-taking init, 98.7% turn-taking yield, 97.8% backchannel init, 100.0% backchannel yield.
- GRPO vs DPO-style ablation: "GRPO outperforms the DPO-style objective on most window-level dynamics metrics, especially yield rate and backchannel behavior"; DPO is slightly better on Seamless Onset MAE (1.00 vs 1.03) and FDB-v3 VIR (4.0 vs 5.0), but GRPO has higher yield rates across all datasets.
- DuplexPO "maintains and releases <BOS>/<EOS> impulses around user speech instead of remaining near PAD" (SFT baseline comparison, Figure 8), and the broader-impacts note flags misuse for "realistic vishing (voice phishing)" with safeguards "such as watermarking or identity disclosure".
---
## Candidate B observable rhythm summary
The chunk body lists exactly these fields with placeholder values and no resolved numbers:
- n_turns: `{candidate_b_n_turns}`
- total_speech_ms: `{candidate_b_total_speech_ms}`
- total_user_overlap_ms: `{candidate_b_total_user_overlap_ms}`
- n_user_overlaps: `{candidate_b_n_user_overlaps}`
- n_interrupted_by_user: `{candidate_b_n_interrupted_by_user}`
- median_pause_after_user_ms: `{candidate_b_median_pause_after_user_ms}`

No Candidate B values, comparisons, or qualitative rhythm claims are present in the chunk.
## Training dynamics and reward correlations (Figures 5–6)
- Figure 5: "Training dynamics of the total reward and its individual components across optimisation steps. The total reward rises monotonically and then plateaus, indicating stable optimisation."
- Figure 6: "Pairwise correlations between reward components and the behavioural events they shape. Stop and start rewards specialise on yielding and turn initiation respectively, with low cross-talk."
- Verbatim: "specifically for backchannel yielding, while start rewards drive the timing of turn initiation. These correlations indicate that the model decomposes conversational dynamics into distinct, actionable components, effectively addressing both when to yield and when to participate."
## Ablation: window boundary size (lead L vs buffer B)
- "We separately ablate window lead time L and window buffer time B, as shown in Figure 7."
- "Varying Window Lead Time produces a clear ordering in mean reward, with overly long lead times causing a substantial performance drop."
- "In contrast, varying Window Buffer Time yields no significant separation, with the mean rewards differing by at most 0.02."
- Interpretation stated: "dynamics-critical window sampling is primarily sensitive to the amount of anticipatory context required for committing to a speaking decision, rather than to the amount of post-event context retained in the window."
- Figure 7 caption: "Ablation of dynamics-critical window lead and buffer times. Bars show the mean RL reward across checkpoints every 10 training steps. Error bars show ±1 standard deviation across checkpoints." Subpanels: "(a) Varying lead time (buffer = 2s)" and "(b) Varying buffer time (lead = 2s)".
## Ablation: neural reward model (SoulX-Duplug teacher)
- Teacher is "SoulX-Duplug [Yan et al., 2026b], denoted fϕ"; method "does not use assistant ground-truth".
- Inputs per sample: "the user waveform u and its aligned word sequence" producing "a chunk-level teacher timeline T = {(am, bm, sm)} (Eq. 14), sm ∈ {idle, nonidle, speak, blank}".
- Salience weighting: "blank frames have wi,t = 0, frames within ∼160 ms of a SoulX-Duplug transition are weighted 1.0 and other non-blank frames 0.5" (Eq. 15); core reward "subtracts a per-window frozen-reference baseline" (Eq. 16).
- Verbatim finding: "Table 11 shows that NRM provides a useful but less reliable dynamics signal than FCDR. Although NRM improves over SFT Dynamics on several metrics, it does not consistently surpass the original SFT Baseline."

Table 11 (rates in %; Onset MAE in seconds; best per column bolded in source):

| Dataset | Training setting | Onset MAE (↓) | Turn-taking Init (↑) | Turn-taking Yield (↑) | Backchannel Init (↑) | Backchannel Yield (↑) | Barge-in VIR (↓) | Barge-in Yield (↑) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Fisher | SFT Baseline | 1.22 | 91.8 | 78.5 | 92.2 | 79.4 | – | – |
| Fisher | SFT Dynamics | 1.34 | 79.7 | 63.0 | 83.2 | 63.4 | – | – |
| Fisher | NRM reward | 1.22 | 96.4 | 81.6 | 89.2 | 50.0 | – | – |
| Fisher | FCDR reward | 0.69 | 100.0 | 98.7 | 97.8 | 100.0 | – | – |
| Seamless | SFT Baseline | 1.22 | 91.8 | 78.5 | 92.2 | 79.4 | – | – |
| Seamless | SFT Dynamics | 1.34 | 79.7 | 63.0 | 83.2 | 63.4 | – | – |
| Seamless | NRM reward | 1.32 | 84.5 | 67.6 | 93.5 | 74.0 | – | – |
| Seamless | FCDR reward | 1.03 | 98.0 | 93.6 | 99.5 | 93.3 | – | – |
| FDB-v3 | SFT Baseline | – | – | – | – | – | 8.0 | 64.8 |
| FDB-v3 | SFT Dynamics | – | – | – | – | – | 4.0 | 93.3 |
| FDB-v3 | NRM reward | – | – | – | – | – | 4.0 | 93.3 |
| FDB-v3 | FCDR reward | – | – | – | – | – | 5.0 | 100.0 |
## Ablation: optimization methods (GRPO vs DPO-style)
- Setup: "Holding the FCDR-based reward calculation and the dynamics-critical window sampler fixed"; DPO-style variant uses "the highest- and lowest-reward continuations within each sampled window" as preferred/dispreferred pair; evaluated "on Fisher, Seamless, and FDB-v3".

Table 12 (rates in %; Onset MAE in seconds; best per column bolded in source):

| Dataset | Optimization | Onset MAE (↓) | Turn-taking Init (↑) | Turn-taking Yield (↑) | Backchannel Init (↑) | Backchannel Yield (↑) | Barge-in VIR (↓) | Barge-in Yield (↑) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Fisher | DPO | 0.81 | 100.0 | 93.6 | 91.4 | 71.4 | – | – |
| Fisher | GRPO | 0.69 | 100.0 | 98.7 | 97.8 | 100.0 | – | – |
| Seamless | DPO | 1.00 | 95.1 | 77.8 | 95.8 | 84.7 | – | – |
| Seamless | GRPO | 1.03 | 98.0 | 93.6 | 99.5 | 93.3 | – | – |
| FDB-v3 | DPO | – | – | – | – | – | 4.0 | 93.3 |
| FDB-v3 | GRPO | – | – | – | – | – | 5.0 | 100.0 |

- Verbatim: "The results show that GRPO outperforms the DPO-style objective on most window-level dynamics metrics, especially yield rate and backchannel behavior."
- Mechanism stated: DPO reduction to extremes "discards useful ranking information", while "GRPO uses group-normalized advantages over the full set of sampled continuations, providing a denser and more stable optimization signal for dynamics-critical decisions."
- Caveat stated: "Although DPO achieves slightly better Onset MAE on Seamless and a lower VIR on FDB-v3, GRPO achieves higher yield rates across all datasets, indicating better recovery and response behavior in dynamics-critical scenarios."
## Conversational-pattern example and broader impacts
- "Figure 8 contrasts the token-level conversational pattern of DuplexPO with that of the SFT baseline. DuplexPO maintains and releases <BOS>/<EOS> impulses around user speech instead of remaining near PAD, which is consistent with the attention statistics in Appendix D and the suppression metrics defined in Appendix C."
- Figure 8 caption: "Example token-level conversational pattern. Compared with the SFT baseline, DuplexPO maintains and releases <BOS>/<EOS> impulses around user speech instead of staying near PAD." Panels: "(a) SFT Baseline" and "(b) DuplexPO", axes "Probability" vs "Time (s)".
- Broader impacts verbatim: "This work improves the naturalness of full-duplex spoken dialogue models. Positively, this can significantly enhance accessible interfaces and conversational assistants. Negatively, highly human-like voice dynamics (e.g., natural backchanneling and interruption) could be misused for deceptive practices like realistic vishing (voice phishing). Future deployments should consider appropriate safeguards, such as watermarking or identity disclosure, to mitigate these risks."
**Covers:** chunk 09-candidate-b-observable-rhythm-summary (Candidate B placeholder metric list plus appendix sections H–L / Figures 5–8 / Tables 11–12)
