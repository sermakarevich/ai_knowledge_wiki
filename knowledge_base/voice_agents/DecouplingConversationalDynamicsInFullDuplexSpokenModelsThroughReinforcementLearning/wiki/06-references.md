> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References (Continued) and Data Details
**In one sentence:** This chunk continues the bibliography from Rekesh through Zheng and opens Appendix A, which details the synthetic and real training-data recipe (speech continuation, instruction QA, synthetic interruptions, ASR-QA, model/speaker pools, and dynamics-aware reconstruction).
## Key points
- Speech-continuation pre-training uses 530K hours of examples derived from large text corpora, converted into two-party pseudo-dialogues with randomized turn lengths and two speaker profiles packed into synchronized two-stream full-duplex examples.
- Instruction-following QA contributes 70K hours of spoken QA (10K hours single-turn broad-topic plus multi-turn up to four minutes), generated with a helpful-assistant prompt conditioned on heterogeneous contexts including Wikipedia and rendered with multi-speaker TTS.
- Synthetic user interruptions are injected only when an agent utterance exceeds four seconds (probability 0.1), with onset sampled uniformly from the 20%–80% span and an 8-token (≈0.64 s) reaction delay before forced end-of-sequence, which masks the audio channel at inference.
- ASR-QA adds real recording conditions using open-source corpora from NeMo ASRSET with LLM-written questions grounded in transcripts, contributing shorter, less knowledge-dense clips with real speaker variation, channel effects, and background noise.
- Synthetic text comes from a pool of instruction-tuned LLMs (GPT-OSS-120B, Qwen2.5-72B Instruct, Llama3.1-70B-Instruct) and multiple TTS backends (Chatterbox, Magpie-TTS, Mooncast), with a voice-conditioning pool of more than 100K prompt segments covering over 20K speakers from LibriTTS, YODAS, and Hifi-TTS 5–10 s segments.
- Dynamics-aware reconstruction uses Fisher and Seamless-Naturalistic-HQ for natural timing signals, recovering utterance segments from word-level alignments while keeping short lexical acknowledgments as standalone backchannels.
---
## References (continued, Rekesh through Zheng)
**Covers:** Bibliography entries, pp. 13–14 in chunk

Representative entries (verbatim):

> "Dima Rekesh, Nithin Rao Koluguri, Samuel Kriman, Somshubra Majumdar, Vahid Noroozi, He Huang, Oleksii Hrinchuk, Krishna Puvvada, Ankur Kumar, Jagadeesh Balam, et al. Fast conformer with linearly scalable attention for efficient speech recognition. In 2023 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU), pages 1–8. IEEE, 2023."

> "Rajarshi Roy, Jonathan Raiman, Sang-gil Lee, Teodor-Dumitru Ene, Robert Kirby, Sungwon Kim, Jaehyeon Kim, and Bryan Catanzaro. Personaplex: Voice and role control for full duplex conversational speech models. arXiv preprint arXiv:2602.06053, 2026."

> "Harvey Sacks, Emanuel A Schegloff, and Gail Jefferson. A simplest systematics for the organization of turn-taking for conversation. language, 50(4):696–735, 1974."

> "John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017."

> "Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024."

> "R. Sutton and A. Barto. Reinforcement learning: An introduction. 2018."

> "Bandhav Veluri, Benjamin N Peloquin, Bokai Yu, Hongyu Gong, and Shyamnath Gollakota. Beyond turn-based interfaces: Synchronous llms as full-duplex dialogue agents. arXiv preprint arXiv:2409.15594, 2024."

> "Donghang Wu, Tianyu Zhang, Yuxin Li, Hexin Liu, Chen Chen, Eng Siong Chng, and Yoshua Bengio. The silent thought: Modeling internal cognition in full-duplex spoken dialogue models via latent reasoning. arXiv preprint arXiv:2603.17837, 2026."

> "L. Zheng and et al. Judging llm-as-a-judge with mt-bench and chatbot arena. arXiv preprint, 2023."

Note: the Yan et al. Soulx-duplug entry appears twice in the chunk (2026a and 2026b) with identical arXiv ID arXiv:2603.14877.

## Appendix A — Data Details
**Covers:** Appendix A opening through dynamics-aware reconstruction (chunk lines 112–161)

Framing (verbatim):

> "In this chapter, we illustrate all the synthetic and real data we used in this work. In pre-training, we use the speech-continuation data to make the model understand speech input under full-duplex modeling. Then, all other data is used in SFT to improve the reasoning ability and build a helpful speech agent. The broader data-construction recipe follows the released Nemotron-VoiceChat materials [NVIDIA, 2026]."

1. Speech-continuation data (verbatim):

> "Speech-continuation pre-training uses 530K hours of examples derived from large text corpora [Su et al., 2025]. Each continuous passage is converted into a two-party pseudo-dialogue by assigning successive sentences to the user and agent streams. Turn lengths are randomized: a turn stops after one sentence with probability 0.8, while longer turns are formed by appending additional sentences with a decaying continuation probability; turns longer than 200 words are handed to the other speaker. The resulting turns are synthesized with two speaker profiles, aligned in time, and packed into synchronized two-stream full-duplex examples. We also swap user and agent roles to increase coverage of both conversational directions."

2. Instruction-following QA data (verbatim):

> "The instruction-following mixture contributes 70K hours of spoken QA data. Within this set, 10K hours are single-turn examples spanning broad topics, and the remaining multi-turn examples train the assistant to maintain conversations lasting up to four minutes. Dialogue generation uses a helpful-assistant prompt and is conditioned on heterogeneous textual contexts, including Wikipedia pages. The generated turns are then rendered with the multi-speaker TTS pipeline."

3. Synthetic user interruption (verbatim):

> "We augment multi-turn examples with simulated barge-ins. When an agent utterance lasts more than four seconds, a user interruption is inserted with probability 0.1, and its onset is sampled uniformly from the 20%–80% span of the agent utterance. After the interruption begins, the agent stream is given an 8-token reaction delay (≈ 0.64 s) before it is forced to emit an end-of-sequence (<EOS>) token. At inference time, an <EOS> on the text channel masks the corresponding audio channel to silence."

| Interruption parameter | Value |
|---|---|
| Trigger condition | Agent utterance > 4 s |
| Insertion probability | 0.1 |
| Onset sampling | Uniform over 20%–80% of agent utterance |
| Reaction delay | 8 tokens (≈ 0.64 s), then forced <EOS> |
| Inference effect of <EOS> | Masks corresponding audio channel to silence |

4. ASR-QA data (verbatim):

> "ASR-QA examples expose the model to real recording conditions. We use speech segments from the open-source corpora aggregated in NeMo ASRSET [Noroozi et al., 2024b] as acoustic contexts. Following Noroozi et al. [2024a], an LLM writes questions grounded in the ASR transcripts. These clips are shorter and less knowledge-dense than the synthetic QA conversations, but they add real speaker variation, channel effects, and background noise to the full-duplex training mixture."

Model diversity and prompt speaker pool (verbatim):

> "The synthetic portions of our training mixture are generated with several text and acoustic models rather than a single generator. Text responses are sampled from a pool of instruction-tuned LLMs, including GPT-OSS-120B, Qwen2.5-72B Instruct, and Llama3.1-70B-Instruct. Speech rendering is performed with multiple TTS backends, including Chatterbox, Magpie-TTS, and Mooncast. For voice conditioning, we build a prompt pool from all 5–10 s speech segments in LibriTTS [Zen et al., 2019], YODAS [Li et al., 2023], and Hifi-TTS [Bakhturina et al., 2021]. This pool contains more than 100K prompt segments and covers over 20K speakers."

Dynamics-aware dialogue reconstruction (verbatim, truncated in chunk):

> "Fisher [Cieri et al., 2004] and Seamless-Naturalistic-HQ (Seamless) [Agrawal et al., 2025] provide the natural timing signals used for rhythm-aware training. Starting from word-level alignments, we recover utterance segments by merging nearby words while keeping short lexical acknowledgments as standalone backchannels."

**Covers:** Bibliography continuation (Rekesh through Zheng, pp. 13–14) and Appendix A Data Details opening (speech continuation 530K hrs; QA 70K hrs; synthetic interruption; ASR-QA; model/speaker pool; reconstruction intro)
