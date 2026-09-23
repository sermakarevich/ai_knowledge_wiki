> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References N–Z, Contributions, and Training Data Examples
**In one sentence:** This chunk lists the N–Z references (Fun-Audio-Chat through Daily-Omni), credits the core/contributing/project-lead/advisor teams, and gives one rendered unit-level training example each for omni-proactive event firing and for the full delegate cycle.
## Key points
- N–Z references span speech-to-speech dialogue (Freeze-Omni, Step-Audio 2, MiMo-Audio, Qwen2.5/3-Omni), video/streaming interaction (MMDuet2, ProactiveVideoQA, LiveStar, OmniPro, LongVideoBench, DuplexSLA, JoyAI-VL-Interaction), and benchmarks/tool use (MMSU, InternVL3.5, ReAct, SpeechGPT, Daily-Omni, SigLIP 2, Grok Voice Agent API).
- Core contributors (equal contribution, marked *): Ruixiang Zhao, Hualei Wang, Renhe Sun, Enzhi Zhou, Zihang Liu, plus Jincenzi Wu, Xujie Song, Kexin Shi.
- Contributors list 14 names (Pengcheng Zhu through Yuhui Chen); project leaders Jian Liu, Yuge Huang, Junliang Xing, Yuntao Wang (†, corresponding authors); advisors Weiqiang Wang, Chun Yu, Yuanchun Shi.
- Unit-level format (Section 4.1): each `<unit>` holds one second of aligned `<image>` + `<audio>`; assistant emits `<|listen|>` for silent perception or `<|speak|>` with chunked text ending `<|chunk_eos|>`; `<|turn_eos|>` ends a turn; long `<|listen|>` runs are omitted.
- Omni-proactive example (B.1): user instruction "Let me know when the commentator reacts to a wicket" → 4 listen units omitted → immediate chunked spoken response "The commentator just reacted to the wicket, shouting 'Oh, he's got him!'" + `<|turn_eos|>`, then 7 trailing listen units omitted.
- Delegate example (B.2): after 39 omitted listen units, user asks in Chinese about Beijing plate-restriction tail number and whether tail-7 Jing-plate can drive; assistant acknowledges in 5 spoken chunks ("好,我查一下今天的限行规则。"), emits `<delegate>查询今天北京限行尾号及京牌尾号7能否通行。</delegate>`, closes turn with `<|turn_eos|>`, returns to `<|listen|>` while backend executes.
- Backend re-entry: `<backend>你刚才问的北京限行查到了：今天限行尾号为2和7,你的京牌尾号7在五环路以内道路限行,时段是7点到20点。</backend>` is then re-presented by the model in chunked `<|speak|>` form within the same timeline.
---
## References, second half (N–Z)
**Covers:** pp. 25–26 reference entries (Tongyi Fun Team through Zhou et al.)

| Entry | Citation |
|---|---|
| Fun-Audio-Chat | Tongyi Fun Team, Qian Chen, Luyao Cheng, et al. Fun-Audio-Chat technical report. arXiv:2512.20156, 2025. |
| SigLIP 2 | Tschannen, Gritsenko, Wang, et al. Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. arXiv:2502.14786, 2025. |
| MMSU | Wang, Wu, Li, et al. Massive multi-task spoken language understanding and reasoning benchmark. arXiv:2506.04779, 2025a. |
| InternVL3.5 | Wang et al. Advancing open-source multimodal models in versatility, reasoning, and efficiency. arXiv:2508.18265, 2025b. |
| Freeze-Omni | Wang, Li, Fu, et al. Smart and low latency speech-to-speech dialogue model with frozen LLM. ICML vol. 267, pp. 63345–63354, 2025c. |
| MMDuet2 | Wang, Liu, Wang, et al. Enhancing proactive interaction of video MLLMs with multi-turn RL. arXiv:2512.06810, 2025d. |
| ProactiveVideoQA | Wang, Meng, Wang, et al. Benchmark evaluating proactive interactions in video LLMs. arXiv:2507.09313, 2025e. |
| Step-Audio 2 | Wu, Yan, Hu, et al. Technical report. arXiv:2507.16632, 2025. |
| Adaptive visual memory | Wu, Mathews, Cai, et al. Semantic-aware adaptive visual memory for streaming video understanding. arXiv:2605.07897, 2026. |
| LongVideoBench | Wu, Li, Chen, et al. Benchmark for long-context interleaved video-language understanding. NeurIPS 37:28828–28857, 2024. |
| Grok Voice Agent API | xAI, December 2025. URL https://x.ai/news/grok-voice-agent-api. |
| MiMo-Audio | Xiaomi LLM-Core Team. Audio language models are few-shot learners. arXiv:2512.23808, 2025. |
| Qwen2.5-Omni / Qwen3-Omni | Xu et al. Technical reports. arXiv:2503.20215 (2025a) and arXiv:2509.17765 (2025b). |
| LiveStar | Yang, Zhang, Hu, et al. Live streaming assistant for real-world online video understanding. arXiv:2511.05299, 2025. |
| JoyAI-VL-Interaction | Yao, Zhou, Yang, et al. Real-time vision-language interaction intelligence. arXiv:2606.14777, 2026. |
| ReAct | Yao, Zhao, Yu, et al. Synergizing reasoning and acting in language models. ICLR 2023. |
| SpeechGPT | Zhang, Li, Zhang, et al. Empowering LLMs with intrinsic cross-modal conversational abilities. EMNLP 2023 Findings, pp. 15757–15773. |
| DuplexSLA | Zhang, Chen, Wu, et al. Full-duplex spoken language model with synchronized speech, language, and action. arXiv:2605.20755, 2026. |
| OmniPro | Zhao, Yang, Xin, et al. Comprehensive benchmark for omni-proactive streaming video understanding. arXiv:2605.18577, 2026. |
| Daily-Omni | Zhou, Wang, Wu, et al. Towards audio-visual reasoning with temporal alignment across modalities. arXiv:2505.17862, 2025. |

## Appendix A — Contributions
**Covers:** Appendix A, p. 26

- Core contributors: Ruixiang Zhao*, Hualei Wang*, Renhe Sun*, Enzhi Zhou*, Zihang Liu*, Jincenzi Wu, Xujie Song, Kexin Shi (* = equal contribution; within marked/unmarked groups names ordered by last name in reverse alphabetical order).
- Contributors: Pengcheng Zhu, Jiayi Zhou, Baoyue Zhang, Changhao Zhang, Yuqian Ying, Yongxiang Xie, Zitong Wang, Jinhong Wang, Tong Niu, Jingjing Liu, Junan Lin, Haolin He, Hengshuo Chu, Yuhui Chen.
- Project leaders (†, corresponding authors): Jian Liu, Yuge Huang ({rex.lj, huangyuge.hyg}@antgroup.com); Junliang Xing, Yuntao Wang ({jlxing, yuntaowang}@tsinghua.edu.cn).
- Project advisors: Weiqiang Wang, Chun Yu, Yuanchun Shi.

## Appendix B — Training data examples
**Covers:** Appendix B–B.2, pp. 26–29

> "We present one training example for each of the two data families central to this report: proactive duplex interaction and delegate workflows. Both are rendered from raw training records."

Format recap: each `<unit>` contains one second of aligned visual (`<image>`) and audio (`<audio>`); assistant responds with `<|listen|>` or `<|speak|>` + chunked text ending `<|chunk_eos|>`; `<|turn_eos|>` marks end of turn; long identical `<|listen|>` runs omitted.

### B.1 Omni-proactive example
Instruction: `"Let me know when the commentator reacts to a wicket."` After 4 omitted listen units, the model fires immediately in chunks: "The commentator just reacted" → "to the wicket" → ", shouting 'Oh" → ", he's got" → "him!'" → `<|turn_eos|>`, followed by 7 omitted trailing listen units. Per text: "the model must remain silent while nothing relevant occurs and speak immediately when the triggering phrase appears in the audio stream."

### B.2 Delegate example
User (after 39 omitted listen units): `"今天北京限行尾号是啥,我这京牌车尾号7能开吗？"` Assistant acknowledges across 5 chunks ("好,我查一下今天的限行规则。"), then emits `"<delegate>查询今天北京限行尾号及京牌尾号7能否通行。</delegate>"` and closes with `<|turn_eos|>`, "so the frontend returns to listening while the backend executes." Backend result re-enters as `<backend>`: "你刚才问的北京限行查到了：今天限行尾号为2和7,你的京牌尾号7在五环路以内道路限行,时段是7点到20点。" The model then "re-presents it in chunked spoken form within the same conversational timeline" (chunks: 你刚才问的 / 北京限行查 / 到了：今天限 / 行尾号为 / 2和7, / 你的京牌尾 / 号7在五 / 环路以内道路 / 限行,时段 / 是7点到 / 20点。 + `<|turn_eos|>`).
