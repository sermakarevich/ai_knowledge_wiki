> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References ([17]–[50])
**In one sentence:** This chunk is the paper's reference list entries [17]–[50] plus the start of Appendix A (Dataset Statistics), citing audio models, full-duplex benchmarks, synthetic-evaluation methods, and statistical tools.
## Key points
- [17] cites the Kimi-Audio technical report (KimiTeam et al., 2025) with the full author list starting Ding Ding and Zeqian Ju.
- [18]–[19] cite synthetic-benchmark methodology: Arena-hard / BenchBuilder pipeline (Li et al., 2024) and WildBench with challenging real-user tasks (Lin et al., 2024).
- [20]–[23] and [37]–[39], [47] cite the full-duplex evaluation family: Full-duplex-bench (turn-taking), v1.5 (overlap handling), v2 (multi-turn with automated examiner), v3 (tool use under disfluency), plus INSTRUCT-FD, the ICASSP 2026 HumDial challenge study, and MTR-DuplexBench.
- [24]–[31] cite vendor voice models: Mistral Voxtral (2025); OpenAI GPT-4o (2024), gpt-audio and gpt-audio-mini (2025), gpt-realtime / Realtime API (2025), o3 and o4-mini (2025), voice-intelligence API models (2026), and GPT-5.4 mini and nano (2026).
- [32], [35], [42], [44]–[45] cite speech/audio foundations and datasets: Whisper robust speech recognition via large-scale weak supervision (Radford et al., 2022), SpokenWOZ speech-text benchmark (Si et al., 2025), Xiaomi Mimo-audio (2025), and Qwen2.5-Omni / Qwen3-Omni technical reports (Xu et al., 2025).
- [33], [36], [41], [46], [50] cite dialogue/interruption-adjacent benchmarks: τ-voice full-duplex voice agents on real-world domains (2026), MultiChallenge multi-turn conversation evaluation (2025), semantic-aware interruption detection (Xia et al., 2026), proactive/transition-aware agents (Yoon et al., 2025), and interruptible web-navigation agents (Zou et al., 2026).
- [34], [37], [40], [43], [48]–[49] cite methods and judges: Schuirmann (1987) TOST equivalence procedure, submodular benchmark selection (Smola, 2026), Self-instruct (Wang et al., 2023), WizardLM (Xu et al., 2025), MT-bench / Chatbot Arena judging (Zheng et al., 2023), and Sotopia interactive social-intelligence evaluation (Zhou et al., 2024).
---
## Cited reports and models ([17], [24]–[31], [42], [44]–[45])
**Covers:** References [17], [24]–[31], [42], [44]–[45]

| Ref | Citation as given |
|---|---|
| [17] | KimiTeam, Ding Ding, Zeqian Ju, Yichong Leng, Songxiang Liu, Tong Liu, Zeyu Shang, Kai Shen, Wei Song, Xu Tan, Heyi Tang, Zhengtao Wang, Chu Wei, Yifei Xin, Xinran Xu, Jianwei Yu, Yutao Zhang, Xinyu Zhou, Y. Charles, Jun Chen, Yanru Chen, Yulun Du, Weiran He, Zhenxing Hu, Guokun Lai, Qingcheng Li, Yangyang Liu, Weidong Sun, Jianzhou Wang, Yuzhi Wang, Yuefeng Wu, Yuxin Wu, Dongchao Yang, Hao Yang, Ying Yang, Zhilin Yang, Aoxiong Yin, Ruibin Yuan, Yutong Zhang, and Zaida Zhou. Kimi-audio technical report, 2025. |
| [24] | Mistral AI. Voxtral, 2025. |
| [25] | OpenAI. Hello GPT-4o. https://openai.com/index/hello-gpt-4o/, 2024. Accessed: 2026-06-09. |
| [26] | OpenAI. gpt-audio. https://developers.openai.com/api/docs/models/gpt-audio, 2025. Accessed: 2026-06-09. |
| [27] | OpenAI. gpt-audio-mini. https://developers.openai.com/api/docs/models/gpt-audio-mini, 2025. Accessed: 2026-06-09. |
| [28] | OpenAI. Introducing gpt-realtime and Realtime API updates for production voice agents. https://openai.com/index/introducing-gpt-realtime/, 2025. Accessed: 2026-06-09. |
| [29] | OpenAI. Introducing OpenAI o3 and o4-mini. https://openai.com/index/introducing-o3-and-o4-mini/, 2025. Accessed: 2026-06-17. |
| [30] | OpenAI. Advancing voice intelligence with new models in the API. https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/, 2026. Accessed: 2026-06-09. |
| [31] | OpenAI. Introducing GPT-5.4 mini and nano. https://openai.com/index/introducing-gpt-5-4-mini-and-nano/, 2026. Accessed: 2026-06-09. |
| [42] | LLM-Core-Team Xiaomi. Mimo-audio: Audio language models are few-shot learners, 2025. |
| [44] | Jin Xu et al. Qwen2.5-Omni technical report, 2025. |
| [45] | Jin Xu et al. Qwen3-omni technical report, 2025. |

## Cited voice / dialogue benchmarks ([18]–[23], [33], [35]–[36], [38]–[39], [41], [46]–[47])
**Covers:** References [18]–[23], [33], [35]–[36], [38]–[39], [41], [46]–[47]

| Ref | Citation as given |
|---|---|
| [18] | Tianle Li et al. From crowdsourced data to high-quality benchmarks: Arena-hard and benchbuilder pipeline, 2024. |
| [19] | Bill Yuchen Lin et al. Wildbench: Benchmarking llms with challenging tasks from real users in the wild, 2024. |
| [20] | Guan-Ting Lin et al. Full-duplex-bench-v3: Benchmarking tool use for full-duplex voice agents under real-world disfluency, 2026. |
| [21] | Guan-Ting Lin et al. Full-duplex-bench-v2: A multi-turn evaluation framework for duplex dialogue systems with an automated examiner, 2026. |
| [22] | Guan-Ting Lin et al. Full-duplex-bench v1.5: Evaluating overlap handling for full-duplex speech models, 2026. |
| [23] | Guan-Ting Lin et al. Full-duplex-bench: A benchmark to evaluate full-duplex spoken dialogue models on turn-taking capabilities, 2025. |
| [33] | Soham Ray et al. τ-voice: Benchmarking full-duplex voice agents on real-world domains, 2026. |
| [35] | Shuzheng Si et al. Spokenwoz: A large-scale speech-text benchmark for spoken task-oriented dialogue agents, 2025. |
| [36] | Ved Sirdeshmukh et al. Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging to frontier llms, 2025. |
| [38] | Yuzhi Tang et al. INSTRUCT-FD: Can your full-duplex speech system follow turn-taking instructions?, 2026. |
| [39] | Chengyou Wang et al. Full-duplex interaction in spoken dialogue systems: A comprehensive study from the icassp 2026 humdial challenge, 2026. |
| [41] | Kangxiang Xia et al. Semantic-aware interruption detection in spoken dialogue systems: Benchmark, metric, and model, 2026. |
| [46] | Yejin Yoon et al. Beyond task-oriented and chitchat dialogues: Proactive and transition-aware conversational agents, 2025. |
| [47] | He Zhang et al. Mtr-duplexbench: Towards a comprehensive evaluation of multi-round conversations for full-duplex speech language models, 2026. |
| [50] | Henry Peng Zou et al. When users change their mind: Evaluating interruptible agents in long-horizon web navigation, 2026. |

## Cited methods, speech foundations, and judge literature ([32], [34], [37], [40], [43], [48]–[49])
**Covers:** References [32], [34], [37], [40], [43], [48]–[49]

| Ref | Citation as given |
|---|---|
| [32] | Alec Radford et al. Robust speech recognition via large-scale weak supervision, 2022. |
| [34] | Donald J. Schuirmann. A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. Journal of Pharmacokinetics and Biopharmaceutics, 15(6):657–680, 1987. |
| [37] | Alexander Smola. Submodular benchmark selection. arXiv preprint arXiv:2605.02209, 2026. |
| [40] | Yizhong Wang et al. Self-instruct: Aligning language models with self-generated instructions, 2023. |
| [43] | Can Xu et al. Wizardlm: Empowering large pre-trained language models to follow complex instructions, 2025. |
| [48] | Lianmin Zheng et al. Judging llm-as-a-judge with mt-bench and chatbot arena, 2023. |
| [49] | Xuhui Zhou et al. Sotopia: Interactive evaluation for social intelligence in language agents, 2024. |

## Appendix start
**Covers:** Page 10, Appendix A heading fragment

Verbatim heading fragment present in chunk:

> "A Dataset Statistics RQ Pass Rate"

No dataset numbers accompany the heading in this chunk; the statistics body belongs to a later chunk.

**Covers:** References [17]–[50] (paper pp. 8–10) and Appendix A heading fragment
