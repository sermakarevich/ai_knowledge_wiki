> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References and further reading
**In one sentence:** The paper's 39 references span talking-head generators (Ditto, FLOAT, SoulX), dyadic systems (ARIG, AvatarForcing, DyStream), the LivePortrait/flow-matching/HuBERT methodological core, and the latency/benchmark context (Full-Duplex-Bench, Moshi, voice-agent budgets).
## Key points
- Talking-head and dyadic baselines: Ditto [1], FLOAT [2], SoulX-FlashHead [3], ARIG [4], AvatarForcing [5], DyStream [6].
- Motion–appearance core: LivePortrait [7] for the disentangled representation, stitching, and rendering path.
- Generative and sequence-modeling methods: flow matching [8], attention-stability RMSNorm/scaling work [9–11], gated attention against attention sinks [12], RoPE positions [13], Gated Multimodal Units for the audio-gate design [14], progressive/immiscible noise priors [19–20], classifier-free guidance [21].
- Speech and data tooling: HuBERT [23], wav2vec-S streaming adaptation as the contrast case [24], Multilingual LibriSpeech [25], MODNet matting [26], PySceneDetect [15], Ultralytics YOLO [16], ClearerVoice-Studio audiovisual extraction [17–18].
- Evaluation and deployment context: Full-Duplex-Bench v1.5 [27], Moshi [28], the voice-to-voice latency budget primer [29], OpenBenchmarks voice-agent latency [30], Seamless Interaction dataset [31], FID [32], FVD [33], ArcFace [34], SyncNet [35], dyadic correlation/diversity metrics [36–37], EMOCA features [38], Granger causality [39].
- Optimizer: Adan [22].
---
## Full reference list
- [1] Li et al. Ditto: Motion-space diffusion for controllable realtime talking head synthesis. ACM MM, 2025.
- [2] Ki et al. FLOAT: Generative motion latent flow matching for audio-driven talking portrait. ICCV, 2025.
- [3] Yu et al. SoulX-FlashHead: Oracle-guided generation of infinite real-time streaming talking heads. arXiv:2602.07449, 2026.
- [4] Guo et al. ARIG: Autoregressive interactive head generation for real-time conversations. ICCV, 2025.
- [5] Ki et al. Avatar forcing: Real-time interactive head avatar generation for natural conversation. CVPR, 2026.
- [6] Chen and Liu. DyStream: Streaming dyadic talking heads generation via flow matching-based autoregressive model. arXiv:2512.24408, 2025.
- [7] Guo et al. LivePortrait: Efficient portrait animation with stitching and retargeting control. arXiv:2407.03168, 2024.
- [8] Lipman et al. Flow matching for generative modeling. ICLR, 2023.
- [9] Dehghani et al. Scaling vision transformers to 22 billion parameters. ICML, 2023.
- [10] Zhang and Sennrich. Root mean square layer normalization. NeurIPS, 2019.
- [11] Esser et al. Scaling rectified flow transformers for high-resolution image synthesis. ICML, 2024.
- [12] Qiu et al. Gated attention for large language models. NeurIPS vol. 38, 2025.
- [13] Su et al. RoFormer: Enhanced transformer with rotary position embedding. Neurocomputing, 2024.
- [14] Arevalo et al. Gated multimodal units for information fusion. ICLR Workshop, 2017.
- [15] Castellano. PySceneDetect. 2024.
- [16] Jocher and Qiu. Ultralytics YOLO. 2023.
- [17] Pan et al. Scenario-aware audio-visual TF-GridNet for target speech extraction. ASRU, 2023.
- [18] Pan et al. Plug-and-play co-occurring face attention for robust audio-visual speaker extraction. Interspeech, 2025.
- [19] Ge et al. Preserve your own correlation: A noise prior for video diffusion models. ICCV, 2023.
- [20] Li et al. Immiscible diffusion: Accelerating diffusion training with noise assignment. NeurIPS vol. 37, 2024.
- [21] Ho and Salimans. Classifier-free diffusion guidance. arXiv:2207.12598, 2022.
- [22] Xie et al. Adan: Adaptive nesterov momentum algorithm for faster optimizing deep models. TPAMI 46(12), 2024.
- [23] Hsu et al. HuBERT: Self-supervised speech representation learning by masked prediction of hidden units. IEEE/ACM TASLP, 2021.
- [24] Fu et al. wav2vec-S: Adapting pre-trained speech models for streaming. ACL Findings, 2024.
- [25] Pratap et al. MLS: A large-scale multilingual dataset for speech research. Interspeech, 2020.
- [26] Ke et al. MODNet: Real-time trimap-free portrait matting via objective decomposition. AAAI, 2022.
- [27] Lin et al. Full-duplex-bench v1.5: Evaluating overlap handling for full-duplex speech models, 2026.
- [28] Défossez et al. Moshi: a speech-text foundation model for real-time dialogue, 2024.
- [29] Hultman Kramer and Pipecat Community. Voice AI & voice agents: An illustrated primer. June 2026.
- [30] OpenBenchmarks. Voice agent end-to-end latency, turn by turn. 2026.
- [31] Agrawal et al. Seamless interaction: Dyadic audiovisual motion modeling and large-scale dataset. arXiv:2506.22554, 2025.
- [32] Heusel et al. GANs trained by a two time-scale update rule converge to a local nash equilibrium. NeurIPS, 2017.
- [33] Unterthiner et al. Towards accurate generative models of video: A new metric & challenges. arXiv:1812.01717, 2018.
- [34] Deng et al. ArcFace: Additive angular margin loss for deep face recognition. CVPR, 2019.
- [35] Chung and Zisserman. Out of time: Automated lip sync in the wild. ACCV Workshops, 2017.
- [36] Tran et al. Dyadic interaction modeling for social behavior generation. ECCV, 2024.
- [37] Ng et al. Learning to listen: Modeling non-deterministic dyadic facial motion. CVPR, 2022.
- [38] Danecek et al. EMOCA: Emotion driven monocular face capture and animation. CVPR, 2022.
- [39] Granger. Investigating causal relations by econometric models and cross-spectral methods. Econometrica, 37(3), 1969.
**Covers:** cited references and pointers for further reading.
