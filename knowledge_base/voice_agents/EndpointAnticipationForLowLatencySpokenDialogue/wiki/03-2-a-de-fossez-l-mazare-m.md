> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# References [2]–[33]: speech dialogue, endpointing, and turn-taking bibliography

**In one sentence:** This chunk is the references tail [2]–[33], listing cited works on full-duplex speech dialogue systems, endpoint/turn-taking prediction, dialogue benchmarks, and supporting methods.

## Key points
- Entries [2]–[9] cite full-duplex and real-time spoken dialogue systems: Moshi (arXiv:2410.00037, 2024), Interspeech 2025 duplex modeling (pp. 2715–2719), Personaplex (arXiv:2602.06053, 2026), ChipChat (arXiv:2509.00078, 2025), SALMONN-Omni (NeurIPS 2025, arXiv:2505.17060), ICLR 2026 listen/look/speak/act (arXiv:2510.16756), GLM-4-Voice (arXiv:2412.02612, 2024), and F-actor (arXiv:2601.11329, 2026).
- Entries [10]–[13] cite endpointing and turn-taking prediction: grid LSTM endpoint detection (Interspeech 2017, pp. 3812–3816), voice activity projection turn-taking (arXiv:2401.04868, 2024), streaming endpointer with neural audio codecs and label-delayed training (ASRU 2025, arXiv:2506.07081), and Easy Turn acoustic-linguistic turn-taking (arXiv:2509.23938, 2025).
- Entries [14]–[16] cite turn-taking foundations and real-time speech-to-speech work: PNAS vol. 106, no. 26, pp. 10 587–10 592 (2009), Frontiers in Psychology vol. 6, p. 136034 (2015), and Kame tandem architecture (arXiv:2510.02327, 2025).
- Entries [20]–[25] cite predictive recognition, voice activity projection, and streaming dialogue reasoning: predictive ASR and end-of-utterance detection (arXiv:2409.19990, 2024), VAP (Interspeech 2022, pp. 5190–5194), multilingual turn-taking prediction (LREC-COLING 2024, pp. 11 873–11 883), thinking-while-listening speech LLMs (arXiv:2510.07497, 2025), chain-of-thought training for open E2E spoken dialogue (Interspeech 2025, pp. 4833–4837), and Stream RAG with streaming tool usage (arXiv:2510.02044, 2025).
- Entries [26]–[28] cite benchmarks and data: SpokenWOZ (NeurIPS, vol. 36, pp. 39 088–39 118, 2023), Switchboard telephone speech corpus (ICASSP, vol. 1, 1992, pp. 517–520), and Silero VAD (github.com/snakers4/silero-vad, 2024).
- Entries [29]–[33] cite modeling and serving infrastructure: "Attention is all you need" (NeurIPS, vol. 30, 2017), RoFormer / rotary position embedding (Neurocomputing, vol. 568, p. 127063, 2024), streaming sequence-to-sequence learning with delayed streams modeling (arXiv:2509.08753, 2025), PagedAttention (SOSP 2023), and Full-Duplex-Bench (arXiv:2503.04721, 2025).

---

## Cited dialogue systems [2]–[9]

| Ref | Verbatim citation |
|---|---|
| [2] | A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou, E. Grave, and N. Zeghidour, "Moshi: a speech-text foundation model for real-time dialogue," arXiv preprint arXiv:2410.00037, 2024. |
| [3] | K. Hu, E. Hosseini-Asl, C. Chen, E. Casanova, S. Ghosh, P. Żelasko, Z. Chen, J. Li, J. Balam, and B. Ginsburg, "Efficient and Direct Duplex Modeling for Speech-to-Speech Language Model," in Interspeech, 2025, pp. 2715–2719. |
| [4] | R. Roy, J. Raiman, S. gil Lee, T.-D. Ene, R. Kirby, S. Kim, J. Kim, and B. Catanzaro, "Personaplex: Voice and role control for full duplex conversational speech models," 2026. [Online]. Available: https://arxiv.org/abs/2602.06053 |
| [5] | T. Likhomanenko, L. Carlson, R. H. Bai, Z. Gu, H. Tran, Z. Aldeneh, Y. Zhang, R. Zhang, H. Zheng, and N. Jaitly, "Chipchat: Low-latency cascaded conversational agent in mlx," arXiv preprint arXiv:2509.00078, 2025. |
| [6] | W. Yu, S. Wang, X. Yang, X. Chen, X. Tian, J. Zhang, G. Sun, L. Lu, Y. Wang, and C. Zhang, "Salmonn-omni: A standalone speech llm without codec injection for full-duplex conversation," NeurIPS, 2025. [Online]. Available: arXiv:2505.17060 |
| [7] | S. Wang, W. Yu, X. Chen, X. Tian, J. Zhang, L. Lu, and C. Zhang, "End-to-end listen, look, speak and act," ICLR, 2026. [Online]. Available: arXiv:2510.16756 |
| [8] | A. Zeng, Z. Du, M. Liu, K. Wang, S. Jiang, L. Zhao, Y. Dong, and J. Tang, "Glm-4-voice: Towards intelligent and human-like end-to-end spoken chatbot," arXiv preprint arXiv:2412.02612, 2024. |
| [9] | M. Züfle, O. Klejch, N. Sanders, J. Niehues, A. Birch, and T. K. Lam, "F-actor: Controllable conversational behaviour in full-duplex models," arXiv preprint arXiv:2601.11329, 2026. |

## Endpointing and turn-taking [10]–[16]

| Ref | Verbatim citation |
|---|---|
| [10] | S.-Y. Chang, B. Li, T. N. Sainath, G. Simko, and C. Parada, "Endpoint Detection Using Grid Long Short-Term Memory Networks for Streaming Speech Recognition," in Interspeech, 2017, pp. 3812–3816. |
| [11] | K. Inoue, B. Jiang, E. Ekstedt, T. Kawahara, and G. Skantze, "Real-time and continuous turn-taking prediction using voice activity projection," arXiv preprint arXiv:2401.04868, 2024. |
| [12] | S. Udupa, S. Watanabe, P. Schwarz, and J. Cernocky, "Streaming endpointer for spoken dialogue using neural audio codecs and label-delayed training," ASRU, 2025. [Online]. Available: arXiv:2506.07081 |
| [13] | G. Li, C. Wang, H. Xue, S. Wang, D. Gao, Z. Zhang, Y. Lin, W. Li, L. Xiao, Z. Fu et al., "Easy turn: Integrating acoustic and linguistic modalities for robust turn-taking in full-duplex spoken dialogue systems," arXiv preprint arXiv:2509.23938, 2025. |
| [14] | T. Stivers, N. J. Enfield, P. Brown, C. Englert, M. Hayashi, T. Heinemann, G. Hoymann, F. Rossano, J. P. De Ruiter, K.-E. Yoon et al., "Universals and cultural variation in turn-taking in conversation," Proceedings of the National Academy of Sciences, vol. 106, no. 26, pp. 10 587–10 592, 2009. |
| [15] | S. Kuroki, Y. Kubo, T. Akiba, and Y. Tang, "Kame: Tandem architecture for enhancing knowledge in real-time speech-to-speech conversational ai," arXiv preprint arXiv:2510.02327, 2025. |
| [16] | S. C. Levinson and F. Torreira, "Timing in turn-taking and its implications for processing models of language," Frontiers in psychology, vol. 6, p. 136034, 2015. |

## Prediction, streaming dialogue, and benchmarks [20]–[28]

| Ref | Verbatim citation |
|---|---|
| [20] | O. Zink, Y. Higuchi, C. Mullov, A. Waibel, and T. Kobayashi, "Predictive speech recognition and end-of-utterance detection towards spoken dialog systems," arXiv preprint arXiv:2409.19990, 2024. |
| [21] | E. Ekstedt and G. Skantze, "Voice activity projection: Self-supervised learning of turn-taking events," in Interspeech, 2022, pp. 5190–5194. |
| [22] | K. Inoue, B. Jiang, E. Ekstedt, T. Kawahara, and G. Skantze, "Multilingual turn-taking prediction using voice activity projection," in Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pp. 11 873–11 883. [Online]. Available: https://aclanthology.org/2024.lrec-main.1036/ |
| [23] | Y.-J. Shih, D. Raj, C. Wu, W. Zhou, S. Bong, Y. Gaur, J. Mahadeokar, O. Kalinli, and M. Seltzer, "Can speech llms think while listening?" arXiv preprint arXiv:2510.07497, 2025. |
| [24] | S. Arora, J. Tian, H. Futami, J. weon Jung, J. Shi, Y. Kashiwagi, E. Tsunoo, and S. Watanabe, "Chain-of-Thought Training for Open E2E Spoken Dialogue Systems," in Interspeech, 2025, pp. 4833–4837. |
| [25] | S. Arora, H. Khan, K. Sun, X. L. Dong, S. Choudhary, S. Moon, X. Zhang, A. Sagar, S. T. Appini, K. Patnaik et al., "Stream rag: Instant and accurate spoken dialogue systems with streaming tool usage," arXiv preprint arXiv:2510.02044, 2025. |
| [26] | S. Si, W. Ma, H. Gao, Y. Wu, T.-E. Lin, Y. Dai, H. Li, R. Yan, F. Huang, and Y. Li, "Spokenwoz: A large-scale speech-text benchmark for spoken task-oriented dialogue agents," NeurIPS, vol. 36, pp. 39 088–39 118, 2023. |
| [27] | J. J. Godfrey, E. C. Holliman, and J. McDaniel, "Switchboard: Telephone speech corpus for research and development," in ICASSP, vol. 1. IEEE, 1992, pp. 517–520. |
| [28] | S. Team, "Silero vad: pre-trained enterprise-grade voice activity detector (vad), number detector and language classifier," https://github.com/snakers4/silero-vad, 2024. |

## Methods and infrastructure [29]–[33]

| Ref | Verbatim citation |
|---|---|
| [29] | A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention is all you need," NeurIPS, vol. 30, 2017. |
| [30] | J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu, "Roformer: Enhanced transformer with rotary position embedding," Neurocomputing, vol. 568, p. 127063, 2024. |
| [31] | N. Zeghidour, E. Kharitonov, M. Orsini, V. Volhejn, G. de Marmiesse, E. Grave, P. Pérez, L. Mazaré, and A. Défossez, "Streaming sequence-to-sequence learning with delayed streams modeling," arXiv preprint arXiv:2509.08753, 2025. |
| [32] | W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica, "Efficient memory management for large language model serving with pagedattention," in Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles, 2023. |
| [33] | G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu, and H.-y. Lee, "Full-duplex-bench: A benchmark to evaluate full-duplex spoken dialogue models on turn-taking capabilities," arXiv preprint arXiv:2503.04721, 2025. |

**Covers:** References [2]–[16] and [20]–[33] (references tail starting at the Défossez/Mazaré block; refs [17]–[19] not present in this chunk).
