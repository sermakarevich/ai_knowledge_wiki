> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiments: Turn-Taking and ASR Results
**In one sentence:** With `du = 1.2s` and `da = 0.16s`, the duplex S2S model with integrated streaming ASR head achieves 10.21% average WER while keeping turn-taking/barge-in competitive (90% precision, 95% recall, 100% barge-in accuracy) and improving OpenbookQA to 69.01%.
## Key points
- Delay hyperparameters are `du = 1.2s` (user text) and `da = 0.16s` (agent text), chosen "to achieve a balance between reasonable ASR performance and immediate agent response."
- The duplex model with streaming ASR head achieves 10.21% average WER (LS-clean 3.9, LS-other 8.48, SPGI 4.95, Giga 14.22, Earn22 16.87, AMI 18.36, Tedlium 5.98, Voxpop 8.9), beating dedicated streaming models FastConformer-80ms (11.71%) and FastConformer-multi (11.27%).
- On the internal test set, turn-taking is 90% precision / 95% recall at 431ms latency versus baseline (noASR) 86.1% / 96.9% at 410ms, with 100% barge-in accuracy at 374ms latency versus baseline 393ms.
- Intelligence scores (VoiceBench) are OpenbookQA 69.01%, AlpacaEval 3.83/5, CommonEval 3.11/5, versus baseline 66.59%/3.71/3.24, versus Qwen2-Audio 67.91%/4.11/3.77 and Moshi 26.15%/2.01/1.60.
- FDB-v1 shows better smooth turn-taking TOR (96.12% vs. Moshi 94%), worse user-interruption TOR (94% vs. 100%) but far higher interruption GPT score (3.99 vs. 0.77), and fewer pause-handling false takeovers (TOR 44.4% vs. 98%) at the cost of higher smooth-TT latency (477ms vs. 265ms).
- Adding the streaming ASR head "does not significantly change the turn taking results compared to the baseline model (i.e., no ASR)" except increased smooth turn-taking latency on FDB-v1, while OpenbookQA improves from 66.59% to 69.01%, "which indicates that the model may benefit from the text modality to answer questions."
- Standalone streaming ASR (Table V) gives Ours (1.6s) 8.47% average WER, improving to 7.73% with "+ YODAS and YTC", versus Nemotron-Speech-0.6B 7.16%, Qwen3-ASR-1.7B 5.76%, Qwen3-ASR-0.6B 6.42%, and Kyutai STT-2.6B 6.40%.
---
## Evaluation setup and delays
Experiments use "a user text delay of du = 1.2s and an agent text delay of da = 0.16s. The choice of these hyperparameters is to achieve a balance between reasonable ASR performance and immediate agent response."

Verbatim scope: "Tables I, II, and IV present the complete evaluation results for our duplex S2S model with the integrated streaming ASR head, including streaming ASR performance on the HuggingFace Open ASR Leaderboard [34], turn-taking metrics, intelligence scores, and FDB-v1 [49] results."

Turn-taking metrics are "computed by extracting user speech segments using voice activity detection (VAD) [52], while agent response segments are derived from the model's predicted text with <bos> and <eos> timestamps."

Metric definitions from chunk:
- "Precision measures the proportion of agent turns correctly following user turns, where an agent turn is a true positive if it starts within 1s before to 1.5s after a user segment ends."
- "Recall measures the proportion of user utterances that receive an agent response starting within 1.5s."
- "These thresholds are chosen empirically to align with our subjective experience but one can adjust them and we also compute turn taking latency as a complementary metric."
- "Latency is the average time delay between user speech ending and agent response starting for correctly matched turns."
- "For barge-in evaluation, a barge-in event is detected when the user starts speaking while the agent is still speaking."
- "Barge-in accuracy is the percentage of barge-in events where the agent successfully stops speaking within 1.5s after the user interruption."
- "Barge-in latency is the average time for the agent to stop after a successful barge-in."
- "For intelligence, we report OpenbookQA accuracy, AlpacaEval (AE), and CommonEval (CE) scores from VoiceBench [50]."

## Streaming ASR results (Table I)
"As shown in Table I, our model achieves 10.21% average WER while simultaneously supporting agent response generation and full-duplex conversation."

| Model | LS-clean | LS-other | SPGI | Giga | Earn22 | AMI | Tedlium | Voxpop | Avg |
|---|---|---|---|---|---|---|---|---|---|
| Ours | 3.9 | 8.48 | 4.95 | 14.22 | 16.87 | 18.36 | 5.98 | 8.9 | 10.21 |

"This is better than the FastConformer-80ms (11.71%) and FastConformer-multi (11.27%) models (Table V), which are dedicated streaming ASR models, demonstrating that our approach achieves competitive ASR performance even within the duplex S2S framework."

## Turn-taking and barge-in (Table II)
TABLE II: "TURN-TAKING AND BARGE-IN EVALUATION. PRECISION AND RECALL ARE IN %, AND LATENCIES ARE IN MS."

| Model | Turn-taking Pr ↑ | Turn-taking Rec ↑ | Turn-taking Lat ↓ | Barge-in Acc ↑ | Barge-in Lat ↓ |
|---|---|---|---|---|---|
| Baseline (noASR) | 86.1 | 96.9 | 410 | 100 | 393 |
| Ours | 90 | 95 | 431 | 100 | 374 |

"As shown in Table II, we have achieved competitive turn taking performance (90% precision and 95% recall, with 431ms latency) based on our internal test set, and 100% barge-in accuracy with 374ms barge-in latency."

## Intelligence evaluation (Table III)
TABLE III: "INTELLIGENCE EVALUATION."

| Model | OpenbookQA (%) ↑ | AE (/5) ↑ | CE (/5) ↑ |
|---|---|---|---|
| Moshi [27], [50] | 26.15 | 2.01 | 1.60 |
| Qwen2-Audio [50] | 67.91 | 4.11 | 3.77 |
| Baseline (noASR) | 66.59 | 3.71 | 3.24 |
| Ours | 69.01 | 3.83 | 3.11 |

"As shown in Table III, our model also achieves an AlpacaEval (AE) score of 3.83 and a CommonEval (CE) score of 3.11 (out of 5), with OpenbookQA accuracy of 69.01%. This represents a substantial improvement over Moshi [27]. Compared to Qwen2-Audio [50], a turn-based audio LLM, our model achieves slightly higher OpenbookQA accuracy (69.01% vs. 67.91%) but shows a gap in CommonEval (3.11 vs. 3.77)."

## FDB-v1 evaluation (Table IV)
TABLE IV: "FDB-V1 [49] EVALUATION. TORS ARE IN %, LATENCIES ARE IN MS, AND THE GPT SCORE IS OUT OF 5."

| Model | Smooth TT TOR ↑ | Smooth TT Lat ↓ | User Interruption TOR ↑ | User Interruption GPT ↑ | User Interruption Lat | Pause TOR ↓ |
|---|---|---|---|---|---|---|
| Moshi [27], [49] | 94 | 265 | 100 | 0.77 | 257 | 98 |
| Baseline (noASR) | 95.15 | 257 | 92.5 | 4.38 | 369 | 51.4 |
| Ours | 96.12 | 477 | 94 | 3.99 | 355 | 44.4 |

"Table IV shows the FDB-v1 [49] results comparing our model against Moshi [27]. FDB-v1 evaluates three key interactive behaviors: smooth turn-taking, user interruption handling, and pause handling (we use the Candor set)."

"Our model achieves better smooth turn-taking (TOR 96.12% vs. 94%) and worse user interruption TOR (94% vs. 100%) to Moshi, but a notably higher GPT score (3.99 vs. 0.77), indicating significantly better response quality upon interruption."

"For pause handling, our model produces fewer false takeovers (TOR 44.4% vs. 98%). The higher smooth turn-taking latency of our model (477ms vs. 265ms) reflects a trade-off for this improved pause handling."

"We note our evaluation is based on the agent text outputs and agent start and end timestamps are based on explicit agent <bos> and <eos> tokens in modeling."

## Effect of adding the streaming ASR head
"We have also compared the proposed model to a baseline model without streaming ASR head for turn taking (Table II), Intelligence (Table III) and FDB-v1 (Table IV), respectively."

"Overall, adding streaming ASR head does not significantly change the turn taking results compared to the baseline model (i.e., no ASR) as shown Table II and IV, except increasing the latency of the smooth turn taking set in FDB-v1. However, in a multi-turn conversation the turn taking latency remains similar (Table II)."

"On the other hand, adding the ASR head leads to the improvement in OpenbookQA (Table III) from 66.59% to 69.01%, which indicates that the model may benefit from the text modality to answer questions."

## Standalone streaming ASR results (Table V)
TABLE V: "STANDALONE STREAMING ASR RESULTS (WER %, ↓). NUMBERS IN PARENTHESES INDICATE LATENCY IN TRAINING."

| Model | LS-clean | LS-other | SPGI | Giga | Earn22 | AMI | Tedlium | Voxpop | Avg |
|---|---|---|---|---|---|---|---|---|---|
| FastConformer-80ms [35] | 2.57 | 6.31 | 6.16 | 14.92 | 21.03 | 28.37 | 6.17 | 8.12 | 11.71 |
| FastConformer-multi (1.12s) [36] | 2.19 | 5.32 | 5.76 | 14.47 | 21.45 | 27.85 | 5.70 | 7.42 | 11.27 |
| Nemotron-Speech-0.6B (1.12s) [51] | 2.31 | 4.75 | 2.62 | 11.45 | 12.48 | 11.58 | 4.50 | 7.57 | 7.16 |
| Qwen3-ASR-1.7B (2s) [14], [34] | 1.63 | 3.4 | 2.84 | 8.74 | 10.25 | 10.56 | 2.28 | 6.35 | 5.76 |
| Qwen3-ASR-0.6B (2s) [14], [34] | 2.13 | 4.45 | 3.03 | 9.14 | 11.06 | 11.66 | 2.85 | 7.07 | 6.42 |
| Kyutai STT-2.6B (2.5s) [34], [38] | 1.70 | 4.32 | 2.03 | 9.81 | 10.99 | 12.17 | 3.35 | 6.79 | 6.40 |
| Ours (1.6s) | 2.68 | 6.04 | 4.87 | 11.64 | 15.01 | 14.20 | 4.61 | 8.70 | 8.47 |
| + YODAS and YTC [48] | 2.48 | 6.03 | 3.66 | 11.21 | 13.56 | 12.97 | 4.03 | 7.91 | 7.73 |

**Covers:** Experiments evaluation with `du = 1.2s` / `da = 0.16s`; Table I duplex streaming ASR (10.21% avg WER), Table II turn-taking/barge-in, Table III intelligence (OpenbookQA/AE/CE), Table IV FDB-v1 (smooth TT, user interruption, pause), and Table V standalone streaming ASR numbers.
