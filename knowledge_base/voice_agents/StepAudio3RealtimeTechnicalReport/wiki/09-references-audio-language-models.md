> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References: Audio Language Models and Streaming Speech Systems
**In one sentence:** This chunk lists references [4]–[39] of the StepAudio 3 Realtime Technical Report, covering audio-language modeling foundations, prior Step-Audio/omni systems, full-duplex dialogue, ASR data/augmentation, and agent/inference benchmarks.
## Key points
- Reference [4] cites Borsos et al., AudioLM (2023), "a language modeling approach to audio generation," in IEEE/ACM Transactions on Audio, Speech, and Language Processing, 31:2523–2533.
- References [5]–[6] cite generic-hearing and paralinguistic conversation work: SALMONN (ICLR 2024, pp. 16607–16629) and a NeurIPS 2024 (37:131072–131103) paralinguistics-aware speech LLM paper.
- References [7]–[8] cite the direct lineage and omni peers: Step-Audio 2 technical report (arXiv:2507.16632, 2025) and Qwen3-Omni technical report (arXiv:2509.17765, 2025).
- References [9]–[12] cite real-time/full-duplex dialogue systems: Freeze-Omni (arXiv:2411.00774, 2024), Moshi (arXiv:2410.00037, 2024), plus 2026 full-duplex papers on chronological thinking (SIGDIAL pp. 473–485) and DuplexSLA (arXiv:2605.20755, 2026).
- References [13]–[17] cite the Step-Audio research line: Step-Audio unified understanding/generation (arXiv:2502.11946, 2025), Step-Audio-R1 (arXiv:2511.15848, 2025), Step-Audio-R1.5 (arXiv:2604.25719, 2026), StepAudio 2.5 (arXiv:2605.23463, 2026), and mind-paced speaking dual-brain reasoning (arXiv:2510.09592, 2025).
- References [18]–[26] cite ASR methods, data, and robustness work: SpecAugment (arXiv:1904.08779, 2019), ROVER (1997 IEEE ASRU Workshop, pp. 347–354), code-switching ASR (IEEE TASLP 34:1853–1865, 2026), LibriSpeech (ICASSP 2015, pp. 5206–5210), AISHELL-1 (O-COCOSDA 2017, pp. 1–5), WenetSpeech 10000+ hours (ICASSP 2022, pp. 6182–6186), ContextASR-Bench (arXiv:2507.05727, 2025), omni-modal post-training (arXiv:2605.12034, 2026), and Bayling-Duplex (arXiv:2606.14528, 2026).
- References [27]–[31] cite dialogue/inference acceleration work: Multi-bench emotional-intelligence benchmark (arXiv:2511.00850, 2025), speculative sampling (arXiv:2302.01318, 2023), speculative decoding (ICML, pp. 19274–19286, 2023), Medusa multi-head decoding (arXiv:2401.10774, 2024), and multi-token prediction (arXiv:2404.19737, 2024).
- References [32]–[39] cite tool use, agent, and audio-reasoning benchmarks: Toolformer (NeurIPS 36:68539–68551, 2023), Gorilla (NeurIPS 37:126544–126565, 2024), ReAct (arXiv:2210.03629, 2022), Artificial Analysis speech-to-speech methodology (2026) and Big Bench Audio (Hugging Face Blog, 2024), MMSU (ICLR 2026, pp. 31374–31410), MMAU (ICLR 2025, pp. 84929–84964), and MMAR (NeurIPS 38, 2026).
---
## Audio generation and hearing foundations ([4]–[6])
| # | Citation as given |
|---|---|
| [4] | Zalán Borsos, Raphaël Marinier, Damien Vincent, Eugene Kharitonov, Olivier Pietquin, Matt Sharifi, Dominik Roblek, Olivier Teboul, David Grangier, Marco Tagliasacchi, et al. Audiolm: a language modeling approach to audio generation. IEEE/ACM transactions on audio, speech, and language processing, 31:2523–2533, 2023. |
| [5] | Changli Tang, Wenyi Yu, Guangzhi Sun, Xianzhao Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma, and Chao Zhang. Salmonn: Towards generic hearing abilities for large language models. In International Conference on Learning Representations, volume 2024, pages 16607–16629, 2024. |
| [6] | Heeseung Kim, Soonshin Seo, Kyeongseok Jeong, Ohsung Kwon, Soyoon Kim, Jungwhan Kim, Jaehong Lee, Eunwoo Song, Myungwoo Oh, Jung-Woo Ha, et al. Paralinguistics-aware speech-empowered large language models for natural conversation. Advances in Neural Information Processing Systems, 37:131072–131103, 2024. |

## Step-Audio lineage and omni peers ([7]–[8], [13]–[17])
| # | Citation as given |
|---|---|
| [7] | Boyong Wu, Chao Yan, Chen Hu, Cheng Yi, Chengli Feng, Fei Tian, Feiyu Shen, Gang Yu, Haoyang Zhang, Jingbei Li, et al. Step-audio 2 technical report. arXiv preprint arXiv:2507.16632, 2025. |
| [8] | Jin Xu, Zhifang Guo, Hangrui Hu, Yunfei Chu, Xiong Wang, Jinzheng He, Yuxuan Wang, Xian Shi, Ting He, Xinfa Zhu, et al. Qwen3-omni technical report. arXiv preprint arXiv:2509.17765, 2025. |
| [13] | Ailin Huang, Boyong Wu, Bruce Wang, Chao Yan, Chen Hu, Chengli Feng, Fei Tian, Feiyu Shen, Jingbei Li, Mingrui Chen, et al. Step-Audio: Unified Understanding and Generation in Intelligent Speech Interaction. arXiv preprint arXiv:2502.11946, 2025. URL https://arxiv.org/abs/2502.11946. |
| [14] | Fei Tian, Xiangyu Tony Zhang, Yuxin Zhang, Haoyang Zhang, Yuxin Li, Daijiao Liu, Yayue Deng, Donghang Wu, Jun Chen, Liang Zhao, et al. Step-audio-r1 technical report. arXiv preprint arXiv:2511.15848, 2025. |
| [15] | Yuxin Zhang, Xiangyu Tony Zhang, Daijiao Liu, Fei Tian, Yayue Deng, Jun Chen, Qingjian Lin, Haoyang Zhang, Yuxin Li, Jinglan Gong, et al. Step-audio-r1.5 technical report. arXiv preprint arXiv:2604.25719, 2026. |
| [16] | Bin Lin, Bo Zhao, Boyong Wu, Chao Yan, Chen Wu, Cheng Yi, Chengyuan Yao, Daijiao Liu, Fei Tian, Feng Tian, et al. Stepaudio 2.5 technical report. arXiv preprint arXiv:2605.23463, 2026. |
| [17] | Donghang Wu, Haoyang Zhang, Jun Chen, Hexin Liu, Eng Siong Chng, Fei Tian, Xuerui Yang, Xiangyu Zhang, Daxin Jiang, Gang Yu, et al. Mind-paced speaking: A dual-brain approach to real-time reasoning in spoken language models. arXiv preprint arXiv:2510.09592, 2025. |

## Real-time and full-duplex dialogue ([9]–[12], [26]–[27])
| # | Citation as given |
|---|---|
| [9] | Xiong Wang, Yangze Li, Chaoyou Fu, Yunhang Shen, Lei Xie, Ke Li, Xing Sun, and Long Ma. Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm. arXiv preprint arXiv:2411.00774, 2024. |
| [10] | Alexandre Défossez, Laurent Mazaré, Manu Orsini, Amélie Royer, Patrick Pérez, Hervé Jégou, Edouard Grave, and Neil Zeghidour. Moshi: a speech-text foundation model for real-time dialogue. arXiv preprint arXiv:2410.00037, 2024. |
| [11] | Donghang Wu, Haoyang Zhang, Chen Chen, Tianyu Zhang, Fei Tian, Xuerui Yang, Gang Yu, Hexin Liu, Nana Hou, Yuchen Hu, et al. Chronological thinking in full-duplex spoken dialogue language models. In Proceedings of the 27th Annual Meeting of the Special Interest Group on Discourse and Dialogue, pages 473–485, 2026. |
| [12] | Haoyang Zhang, Jun Chen, Donghang Wu, Yuxin Li, Yuxin Zhang, Xiangyu Tony Zhang, Che Liu, Qingjian Lin, Yizhou Peng, Hexin Liu, et al. Duplexsla: A full-duplex spoken language model with synchronized speech, language, and action. arXiv preprint arXiv:2605.20755, 2026. |
| [26] | Qingkai Fang, Shoutao Guo, and Yang Feng. Bayling-duplex: Native full-duplex speech dialogue with a single autoregressive llm. arXiv preprint arXiv:2606.14528, 2026. |
| [27] | Yayue Deng, Guoqiang Hu, Haiyang Sun, Xiangyu Zhang, Haoyang Zhang, Fei Tian, Xuerui Yang, Gang Yu, and Eng Siong Chng. Multi-bench: A multi-turn interactive benchmark for assessing emotional intelligence ability of spoken dialogue models. arXiv preprint arXiv:2511.00850, 2025. |

## ASR methods, corpora, and robustness ([18]–[25])
| # | Citation as given |
|---|---|
| [18] | Daniel S Park, William Chan, Yu Zhang, Chung-Cheng Chiu, Barret Zoph, Ekin D Cubuk, and Quoc V Le. Specaugment: A simple data augmentation method for automatic speech recognition. arXiv preprint arXiv:1904.08779, 2019. |
| [19] | Jonathan G Fiscus. A post-processing system to yield reduced word error rates: Recognizer output voting error reduction (rover). In 1997 IEEE workshop on automatic speech recognition and understanding proceedings, pages 347–354. IEEE, 1997. |
| [20] | Hexin Liu, Haoyang Zhang, Qiquan Zhang, Xiangyu Zhang, Dongyuan Shi, Eng Siong Chng, and Haizhou Li. Code-Switching Speech Recognition Under the Lens: Model- and Data-Centric Perspectives. IEEE Transactions on Audio, Speech and Language Processing, 34: 1853–1865, 2026. doi: 10.1109/TASLPRO.2026.3675776. |
| [21] | Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur. Librispeech: an asr corpus based on public domain audio books. In 2015 IEEE international conference on acoustics, speech and signal processing (ICASSP), pages 5206–5210. IEEE, 2015. |
| [22] | Hui Bu, Jiayu Du, Xingyu Na, Bengu Wu, and Hao Zheng. Aishell-1: An open-source mandarin speech corpus and a speech recognition baseline. In 2017 20th conference of the oriental chapter of the international coordinating committee on speech databases and speech I/O systems and assessment (O-COCOSDA), pages 1–5. IEEE, 2017. |
| [23] | Binbin Zhang, Hang Lv, Pengcheng Guo, Qijie Shao, Chao Yang, Lei Xie, Xin Xu, Hui Bu, Xiaoyu Chen, Chenchen Zeng, et al. Wenetspeech: A 10000+ hours multi-domain mandarin corpus for speech recognition. In ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 6182–6186. IEEE, 2022. |
| [24] | He Wang, Linhan Ma, Dake Guo, Xiong Wang, Lei Xie, Jin Xu, and Junyang Lin. ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark. arXiv preprint arXiv:2507.05727, 2025. URL https://arxiv.org/abs/2507.05727. |
| [25] | Che Liu, Lichao Ma, Xiangyu Tony Zhang, Yuxin Zhang, Haoyang Zhang, Xuerui Yang, and Fei Tian. Boosting Omni-Modal Language Models: Staged Post-Training with Visually Debiased Evaluation. arXiv preprint arXiv:2605.12034, 2026. URL https://arxiv.org/abs/2605.12034. |

## Inference acceleration, agents, and audio benchmarks ([28]–[39])
| # | Citation as given |
|---|---|
| [28] | Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, and John Jumper. Accelerating large language model decoding with speculative sampling. arXiv preprint arXiv:2302.01318, 2023. |
| [29] | Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via speculative decoding. In International conference on machine learning, pages 19274–19286. PMLR, 2023. |
| [30] | Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D Lee, Deming Chen, and Tri Dao. Medusa: Simple llm inference acceleration framework with multiple decoding heads. arXiv preprint arXiv:2401.10774, 2024. |
| [31] | Fabian Gloeckle, Badr Youbi Idrissi, Baptiste Rozière, David Lopez-Paz, and Gabriel Synnaeve. Better & faster large language models via multi-token prediction. arXiv preprint arXiv:2404.19737, 2024. |
| [32] | Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. Advances in neural information processing systems, 36: 68539–68551, 2023. |
| [33] | Shishir G Patil, Tianjun Zhang, Xin Wang, and Joseph E Gonzalez. Gorilla: Large language model connected with massive apis. Advances in Neural Information Processing Systems, 37: 126544–126565, 2024. |
| [34] | Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022. |
| [35] | Artificial Analysis. Speech to speech benchmarking methodology, 2026. URL https://artificialanalysis.ai/methodology/speech-to-speech-benchmarking/. |
| [36] | Artificial Analysis. Evaluating audio reasoning with big bench audio. Hugging Face Blog, 2024. URL https://huggingface.co/blog/big-bench-audio-release. |
| [37] | Dingdong Wang, Junan Li, Jincenzi Wu, Dongchao Yang, Xueyuan Chen, Tianhua Zhang, and Helen Meng. Mmsu: A massive multi-task spoken language understanding and reasoning benchmark. In International Conference on Learning Representations, volume 2026, pages 31374–31410, 2026. |
| [38] | Sakshi Sakshi, Utkarsh Tyagi, Sonal Kumar, Ashish Seth, Ramaneswaran Selvakumar, Oriol Nieto, Ramani Duraiswami, Sreyan Ghosh, and Dinesh Manocha. Mmau: A massive multi-task audio understanding and reasoning benchmark. In International Conference on Learning Representations, volume 2025, pages 84929–84964, 2025. |
| [39] | Ziyang Ma, Yinghao Ma, Yanqiao Zhu, Chen Yang, Yi-Wen Chao, Ruiyang Xu, Wenxi Chen, Yuanzhe Chen, Zhuo Chen, Jian Cong, et al. Mmar: A challenging benchmark for deep reasoning in speech, audio, music, and their mix. Advances in Neural Information Processing Systems, 38, 2026. |

**Covers:** References [4]–[39], report pages 23–25
