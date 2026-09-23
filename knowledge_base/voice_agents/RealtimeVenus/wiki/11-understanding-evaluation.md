> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Understanding evaluation: baselines, memory, speech, and full-duplex results
**In one sentence:** Realtime-Venus-Omni leads online models on six of eight streaming/offline video benchmarks, memory augmentation consistently helps long-video understanding, and the frontends retain strong audio understanding, spoken QA, and overlap-handling full-duplex behavior.
## Key points
- Offline baselines are InternVL3.5, Qwen3-VL, Qwen3.5, Qwen3-Omni, video-SALMONN 2+, AV-Flamingo, and Gemini-3.5-Flash; online baselines are LiveStar, MMDuet2, JoyAI-VL-Interaction, and MiniCPM-o 4.5.
- Realtime-Venus-Omni scores 70.2 on StreamingBench, 64.7 on OVO-Bench, 46.2 on ProactiveVideoQA, and 29.0 on OmniPro, plus 54.0 on WorldSense, 81.3 on Daily-Omni, 39.2 on OmniVideoBench, and 38.9 on LVOmniBench.
- Compared with MiniCPM-o 4.5, it improves StreamingBench by 2.3 points, OVO-Bench by 4.0 points, and OmniPro probe-mode accuracy by 3.4 points, and scores higher on Daily-Omni, OmniVideoBench, and LVOmniBench.
- Among compared online models it is highest on six of eight benchmarks, lower than MiniCPM-o 4.5 on ProactiveVideoQA and WorldSense; offline baselines are reported separately for reference with best/second-best highlighting restricted to online models, and results do not isolate individual training components without controlled ablations.
- Memory augmentation improves Realtime-Venus-Omni across all reported duration bins, notably +5.88 points on the 60–90-minute LVOmniBench subset and +4.76 points on the 40–60-minute LongVideoBench subset, with gains across all CGBench ranges.
- For MiniCPM-o 4.5, memory improves several settings including 9.27–10.44 points across CGBench and 5.89 points on the 60–90-minute LVOmniBench subset, but shows a decrease in the shorter LongVideoBench bin and no change in the longer bin, so benefit depends on backbone and setting.
- Realtime-Venus-Audio achieves 78.0% on MMAU, 63.2% on MMAU-Pro, 65.6% on MMAR, and 66.0% on MMSU (highest among compared models on MMAU and MMAU-Pro; second on MMAR behind Qwen3-Omni; behind Qwen3-Omni and Fun-Audio-Chat on MMSU), and 4.81 AlpacaEval, 83.8% Llama Questions, 75.7% Speech TriviaQA, and 67.8% Speech CMMLU (tied-highest AlpacaEval, highest Llama Questions and Speech CMMLU, second on TriviaQA behind Qwen3-Omni).
- On Full-Duplex-Bench v1.5, Realtime-Venus-Audio has 0.75 response rate under user interruption and continuation rates of 0.97, 0.88, and 0.86 under backchannels, speech directed to others, and background speech; Realtime-Venus-Omni has 0.60, 0.92, 0.90, and 0.85 on the corresponding metrics.
---
## Baselines
The offline baselines are InternVL3.5 (Wang et al., 2025b), Qwen3-VL (Bai et al., 2025), Qwen3.5 (Qwen Team, 2026), Qwen3-Omni (Xu et al., 2025b), video-SALMONN 2+ (Tang et al., 2025), AV-Flamingo (Ghosh et al., 2026), and Gemini-3.5-Flash (Google DeepMind, 2026). The online baselines are LiveStar (Yang et al., 2025), MMDuet2 (Wang et al., 2025d), JoyAI-VL-Interaction (Yao et al., 2026), and MiniCPM-o 4.5 (Cui et al., 2026).
## Results
Realtime-Venus-Omni scores 70.2 on StreamingBench, 64.7 on OVO-Bench, 46.2 on ProactiveVideoQA, and 29.0 on OmniPro. Its offline video understanding scores are 54.0 on WorldSense, 81.3 on Daily-Omni, 39.2 on OmniVideoBench, and 38.9 on LVOmniBench. Compared with MiniCPM-o 4.5, it improves StreamingBench and OVO-Bench accuracy by 2.3 and 4.0 percentage points, respectively, and OmniPro probe-mode accuracy by 3.4 points. It also scores higher on Daily-Omni, OmniVideoBench, and LVOmniBench.
## Scope of the comparison
Among the compared online models, Realtime-Venus-Omni achieves the highest scores on six of the eight benchmarks. Its lower scores on ProactiveVideoQA and WorldSense relative to MiniCPM-o 4.5 underscore the need to assess streaming comprehension, proactive response quality, and offline video understanding separately. We report offline baselines separately for reference and restrict the best- and second-best highlighting to online models. These results also do not isolate the contribution of individual training components, which requires controlled ablations.
## Memory-augmented understanding
Table 3 reports the performance of the long-video memory module on LVOmniBench, LongVideoBench, and CGBench across different video-duration ranges. We report results for both Realtime-Venus-Omni and MiniCPM-o 4.5, comparing each backbone with and without memory augmentation. Overall, the results show that memory augmentation improves Realtime-Venus-Omni across all reported duration bins, with gains for MiniCPM-o 4.5 in several settings as well.
Table 3 Memory-augmented long-video understanding accuracy (%). Duration bins are in minutes.
| Model | LVOmniBench [10,30) | [30,60) | [60,90) | CGBench [40,50) | [50,60) | [60,65) | LongVideoBench [15,40) | [40,60) |
|---|---|---|---|---|---|---|---|---|
| MiniCPM-o 4.5 | 38.58 | 38.56 | 32.35 | 34.27 | 36.10 | 34.58 | 52.89 | 55.56 |
| + memory | 38.80 | 39.89 | 38.24 | 44.71 | 45.37 | 43.93 | 51.90 | 55.56 |
| Realtime-Venus-Omni | 35.48 | 42.91 | 41.18 | 47.84 | 46.63 | 49.53 | 52.89 | 57.14 |
| + memory | 36.36 | 43.10 | 47.06 | 48.71 | 48.31 | 50.47 | 53.29 | 61.90 |
## Effect of memory
Memory augmentation consistently improves Realtime-Venus-Omni across the evaluated duration ranges. In particular, accuracy increases by 5.88 percentage points on the 60–90-minute subset of LVOmniBench and by 4.76 points on the 40–60-minute subset of LongVideoBench, with gains across all evaluated duration ranges of CGBench as well. For MiniCPM-o 4.5, memory also improves performance in several settings, including improvements of 9.27–10.44 points across CGBench and 5.89 points on the 60–90-minute LVOmniBench subset. The gains are consistent across all evaluated bins for Realtime-Venus-Omni, whereas MiniCPM-o 4.5 shows a decrease in the shorter LongVideoBench bin and no change in the longer bin. Thus, the benefit of memory augmentation depends on the backbone and evaluation setting.
## Speech results — audio understanding
Table 4 reports results for both frontend models on MMAU, MMAU-Pro, MMAR, and MMSU. Realtime-Venus-Audio achieves accuracies of 78.0%, 63.2%, 65.6%, and 66.0%, respectively. The speech comparisons include Fun-Audio-Chat, MiniCPM-o 2.6, Baichuan-Omni-1.5, Kimi-Audio, Qwen3-Omni, MiMo-Audio, Step-Audio2-mini, and MiniCPM-o 4.5. Model configurations are listed in Tables 4 and 5.
Table 4 Audio understanding accuracy (%). Higher is better for all benchmarks.
| Model | Size | MMAU | MMAU-Pro | MMAR | MMSU |
|---|---|---|---|---|---|
| Fun-Audio-Chat | 8B | 76.6 | 58.0 | 40.7 | 67.8 |
| MiniCPM-o 2.6 | 7B | 65.2 | 40.5 | 48.6 | 56.5 |
| Baichuan-Omni-1.5 | 7B | 65.6 | 42.9 | 40.7 | 50.6 |
| Kimi-Audio | 9B | 68.4 | 56.6 | 60.8 | 59.3 |
| Qwen3-Omni | 30B-A3B | 77.5 | 61.2 | 66.4 | 69.0 |
| MiMo-Audio | 7B | 74.9 | 53.4 | 63.6 | 61.7 |
| Step-Audio2-mini | 7B | 68.2 | 47.9 | 55.8 | 56.8 |
| MiniCPM-o 4.5 | 9B | 76.9 | 60.0 | 65.3 | 65.8 |
| Realtime-Venus-Omni | 9B | 76.9 | 62.0 | 65.2 | 64.6 |
| Realtime-Venus-Audio | 9B | 78.0 | 63.2 | 65.6 | 66.0 |
## Task-dependent performance
Realtime-Venus-Audio achieves the highest scores among the compared models on MMAU and MMAU-Pro. On MMAR, it ranks second behind Qwen3-Omni. On MMSU, Qwen3-Omni and Fun-Audio-Chat score higher. These results indicate that the interaction-oriented frontend retains general audio understanding, while contextual acoustic reasoning and fine-grained spoken-language understanding remain areas for improvement.
## Spoken question answering
Table 5 reports results for both frontend models. Realtime-Venus-Audio obtains an AlpacaEval score of 4.81 and accuracies of 83.8%, 75.7%, and 67.8% on Llama Questions, Speech TriviaQA, and Speech CMMLU, respectively.
Table 5 Spoken question-answering results. AlpacaEval reports a judge score; other columns report accuracy (%). Higher is better.
| Model | Size | AlpacaEval | Llama Q. | TriviaQA | CMMLU |
|---|---|---|---|---|---|
| Fun-Audio-Chat | 8B | 4.80 | 83.3 | 68.1 | 67.7 |
| MiniCPM-o 2.6 | 7B | 4.42 | 78.0 | 51.8 | 51.4 |
| Baichuan-Omni-1.5 | 7B | 4.50 | 78.5 | 63.0 | 58.4 |
| Kimi-Audio | 9B | 4.46 | 79.3 | 62.1 | 67.0 |
| Qwen3-Omni | 30B-A3B | 4.74 | 83.4 | 75.9 | 47.8 |
| MiMo-Audio | 7B | 4.60 | 79.7 | 52.8 | 56.7 |
| Step-Audio2-mini | 7B | 4.17 | 75.0 | 57.7 | 67.6 |
| MiniCPM-o 4.5 | 9B | 4.81 | 81.0 | 75.5 | 59.2 |
| Realtime-Venus-Omni | 9B | 4.75 | 83.3 | 73.6 | 67.5 |
| Realtime-Venus-Audio | 9B | 4.81 | 83.8 | 75.7 | 67.8 |
## Knowledge coverage
Realtime-Venus-Audio ties MiniCPM-o 4.5 for the highest AlpacaEval score and achieves the highest Llama Questions and Speech CMMLU accuracies among the compared models. It ranks second on Speech TriviaQA, behind Qwen3-Omni. These results cover instruction following and knowledge-based spoken question answering, but do not establish broader reasoning capability. The aggregate scores also do not distinguish errors in speech interpretation from errors in downstream answer generation.
## Full-duplex results — overlap handling (v1.5)
Table 6 reports Full-Duplex-Bench v1.5 results for both frontend models. Realtime-Venus-Audio has a response rate of 0.75 under user interruption and continuation rates of 0.97, 0.88, and 0.86 under user backchannels, speech directed to others, and background speech, respectively. These scenario-specific results assess whether the model responds to interruptions while maintaining conversational continuity during other overlapping speech.
Table 6 Full-Duplex-Bench v1.5 results across four scenarios.
| Model | User interruption C_RESPOND↑ | C_RESUME↓ | User backchannel C_RESPOND↓ | C_RESUME↑ | Talking to others C_RESPOND↓ | C_RESUME↑ | Background speech C_RESPOND↓ | C_RESUME↑ |
|---|---|---|---|---|---|---|---|---|
| Freeze-Omni | 0.72 | 0.12 | 0.07 | 0.80 | 0.58 | 0.25 | 0.62 | 0.25 |
| Moshi | 0.50 | 0.26 | 0.02 | 0.06 | 0.20 | 0.19 | 0.21 | 0.07 |
| Gemini 3.1 Live | 0.77 | 0.20 | 0.02 | 0.95 | 0.27 | 0.66 | 0.28 | 0.66 |
| GPT-4o | 0.78 | 0.10 | 0.03 | 0.70 | 0.91 | 0.02 | 0.93 | 0.04 |
| Joy-Duplex | 0.88 | 0.07 | 0.01 | 0.96 | 0.17 | 0.72 | 0.10 | 0.85 |
| MiniCPM-o 4.5 | 0.60 | 0.36 | 0.00 | 0.95 | 0.18 | 0.79 | 0.16 | 0.82 |
| Realtime-Venus-Omni | 0.60 | 0.37 | 0.02 | 0.92 | 0.06 | 0.90 | 0.12 | 0.85 |
| Realtime-Venus-Audio | 0.75 | 0.23 | 0.00 | 0.97 | 0.11 | 0.88 | 0.11 | 0.86 |
Notes. Arrows indicate the preferred direction of each metric. Moshi and GPT-4o results are taken directly from the original Full-Duplex-Bench v1.5 paper; Joy-Duplex and Gemini 3.1 Live results are taken from the JoyAI-Talker paper.
**Covers:** Audio/visual understanding evaluation setup and offline baselines
