> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# References and Training Appendix (Refs [16]–[40], Appendices A–B)

**In one sentence:** This chunk lists references [16]–[40] on controllable generation, duplex benchmarks, and multi-reward RL, then documents SFT/RL training settings (Table 3), reward-weight and compute details, and the start of the evaluation/checkpoint-selection appendix.

## Key points
- References [16]–[23] cite MO-GRPO (arXiv:2509.22047), CTRL (arXiv:1909.05858), Tülu 3 (arXiv:2411.15124), a controllable-text-generation survey (arXiv:2408.12599), Full-Duplex-Bench v2/v1.5/v1, and GDPO (arXiv:2601.05242).
- References [24]–[32] cite AudioJudge, generative spoken dialogue language modeling (TACL 2023), interactivity alignment in full-duplex speech models, GPT-Realtime docs, rubric-guided self-distillation, PersonaPlex, MMAU, MULTIVOX, and audio hallucination attacks.
- References [33]–[40] cite DeepSeekMath, Qwen3-ASR, policy-aware rubric rewards, synchronous LLMs as full-duplex agents (EMNLP 2024), a full-duplex speech dialogue scheme (NeurIPS 2024), aligning spoken dialogue models from user interactions (ICML 2025), OmniFlatten, and F-Actor.
- SFT uses a Moshi-style 7B backbone on 80 H100 GPUs (batch 8/GPU, global batch 640) for a 3,600-step budget (2.304M draws), with the reported checkpoint at step 2,925 (1.872M draws).
- Both RL stages use component-normalized GDPO with RL lr 5×10−7, KL 0.05/target 0.01 (adaptive, min 0.02, bounded k3 estimator), clip 0.2/grad-clip 1.0, and a response-continuity term (weight 0.5, target 4.0 s); stage 2 adds a continuation-duration bonus (weight 2.0, target 4 s) on noise-robustness and user-backchannel events.
- Reward weights are interactivity 1.0 plus transcript rubric judge 0.75 (Gemini 3.6 Flash); the stage-1 run shows the transcript rubric judge active on turn and interruption strata only, with within-group std 0.14–0.43 and no parse failures in recorded rollouts.
- RL stage 1 ran on four 8×H100-80GB nodes (5.08 h, ~162.7 GPU-h) and stage 2 on one 8×H100-80GB node (4.01 h, ~32.1 GPU-h), excluding queueing, prior setup, benchmark evaluation, and hosted-model compute.
- Evaluation uses Gemini 3.6 Flash for SteerBench/FDB-v2, gpt-5.4-mini (medium reasoning, 3 samples/item for VoiceBench) for AudioMC/VoiceBench/FDB-v1 interruption ratings, and parakeet-tdt-0.6b-v2 for FDB-v1/v2 transcription; checkpoints are frozen on development-set performance alone, and CANDOR pause tasks are flagged diagnostic because 100/216 pause transcripts overlap 96 supervised conversations and official pause clips end only 0.02–0.11 s after the user's last word.

---

## References [16]–[23]

Cited works (verbatim bibliographic details):

- "[16] Y. Ichihara, Y. Jinnai, T. Morimura, M. Sakamoto, R. Mitsuhashi, and E. Uchibe. MO-GRPO: Mitigating reward hacking of group relative policy optimization on multi-objective problems. arXiv preprint arXiv:2509.22047, 2025."
- "[17] N. S. Keskar, B. McCann, L. R. Varshney, C. Xiong, and R. Socher. CTRL: A conditional transformer language model for controllable generation. arXiv preprint arXiv:1909.05858, 2019."
- "[18] N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, et al. Tülu 3: Pushing frontiers in open language model post-training. arXiv preprint arXiv:2411.15124, 2024."
- "[19] X. Liang, H. Wang, Y. Wang, S. Song, J. Yang, S. Niu, J. Hu, D. Liu, S. Yao, F. Xiong, and Z. Li. Controllable text generation for large language models: A survey. arXiv preprint arXiv:2408.12599, 2024."
- "[20] G.-T. Lin, S.-Y. S. Kuan, J. Shi, K.-W. Chang, S. Arora, S. Watanabe, and H.-y. Lee. Full-Duplex-Bench-v2: A multi-turn evaluation framework for duplex dialogue systems with an automated examiner. arXiv preprint arXiv:2510.07838, 2025."
- "[21] G.-T. Lin, S.-Y. S. Kuan, Q. Wang, J. Lian, T. Li, S. Watanabe, and H.-y. Lee. Full-Duplex-Bench v1.5: Evaluating overlap handling for full-duplex speech models. arXiv preprint arXiv:2507.23159, 2025."
- "[22] G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu, and H.-y. Lee. Full-Duplex-Bench: A benchmark to evaluate full-duplex spoken dialogue models on turn-taking capabilities. In Proc. ASRU, 2025."
- "[23] S.-Y. Liu, X. Dong, X. Lu, S. Diao, P. Belcak, M. Liu, M.-H. Chen, H. Yin, Y.-C. F. Wang, K.-T. Cheng, Y. Choi, J. Kautz, and P. Molchanov. GDPO: Group reward-decoupled normalization policy optimization for multi-reward RL optimization. arXiv preprint arXiv:2601.05242, 2026."

## References [24]–[32]

- "[24] P. Manakul, W. H. Gan, M. J. Ryan, A. S. Khan, W. Sirichotedumrong, K. Pipatanakul, W. Held, and D. Yang. AudioJudge: Understanding what works in large audio model based speech evaluation. arXiv preprint arXiv:2507.12705, 2025."
- "[25] T. A. Nguyen, E. Kharitonov, J. Copet, Y. Adi, W.-N. Hsu, A. Elkahky, P. Tomasello, R. Algayres, B. Sagot, A. Mohamed, and E. Dupoux. Generative spoken dialogue language modeling. Transactions of the Association for Computational Linguistics, 11:250–266, 2023."
- "[26] A. Ohashi, N. Zeghidour, A. Défossez, and E. Kharitonov. Multi-faceted interactivity alignment in full-duplex speech models. arXiv preprint arXiv:2606.11167, 2026."
- "[27] OpenAI. GPT-Realtime model. OpenAI Platform documentation, 2025." Accessed 2026-09-09.
- "[28] M. Rezaei, A. Mahmoud, Z. Wang, U. Tyagi, A. Gosai, R.-G. Dumitru, A. Sabharwal, B. Liu, and Y. He. Rubric-guided self-distillation: Post-training without rubric verifiers. arXiv preprint arXiv:2606.12507, 2026."
- "[29] R. Roy, J. Raiman, S.-g. Lee, T.-D. Ene, R. Kirby, S. Kim, J. Kim, and B. Catanzaro. PersonaPlex: Voice and role control for full duplex conversational speech models. arXiv preprint arXiv:2602.06053, 2026."
- "[30] S. Sakshi, U. Tyagi, S. Kumar, A. Seth, R. Selvakumar, O. Nieto, R. Duraiswami, S. Ghosh, and D. Manocha. MMAU: A massive multi-task audio understanding and reasoning benchmark. In International Conference on Learning Representations, 2025."
- "[31] R. Selvakumar, A. Seth, N. Anand, U. Tyagi, S. Kumar, S. Ghosh, and D. Manocha. MULTIVOX: A benchmark for evaluating voice assistants for multimodal interactions. In Proceedings of EMNLP 2025, pages 28481–28493, Suzhou, China, 2025."
- "[32] A. Seth, S. Kumar, R. Selvakumar, N. Anand, U. Tyagi, P. Seetharaman, R. Duraiswami, and D. Manocha. Audio hallucination attacks: Probing the reliability of large audio language models. arXiv preprint arXiv:2603.29263, 2026."

## References [33]–[40]

- "[33] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, and D. Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024."
- "[34] X. Shi, X. Wang, Z. Guo, Y. Wang, P. Zhang, X. Zhang, Z. Guo, H. Hao, Y. Xi, B. Yang, J. Xu, J. Zhou, and J. Lin. Qwen3-ASR technical report. arXiv preprint arXiv:2601.21337, 2026."
- "[35] U. Tyagi, X. Guo, M. Rezaei, D. George, A. Mahmoud, J. Lee, B. Liu, and Y. He. Not every rubric teaches equally: Policy-aware rubric rewards for RLVR. arXiv preprint arXiv:2605.20164, 2026."
- "[36] B. Veluri, B. N. Peloquin, B. Yu, H. Gong, and S. Gollakota. Beyond turn-based interfaces: Synchronous LLMs as full-duplex dialogue agents. In Proceedings of EMNLP 2024, pages 21390–21402, 2024."
- "[37] P. Wang, S. Lu, Y. Tang, S. Yan, W. Xia, and Y. Xiong. A full-duplex speech dialogue scheme based on large language models. In Advances in Neural Information Processing Systems, 2024."
- "[38] A. Wu, L. Mazaré, N. Zeghidour, and A. Défossez. Aligning spoken dialogue models from user interactions. In International Conference on Machine Learning, 2025."
- "[39] Q. Zhang, L. Cheng, C. Deng, Q. Chen, W. Wang, S. Zheng, J. Liu, H. Yu, C. Tan, Z. Du, and S. Zhang. OmniFlatten: An end-to-end GPT model for seamless voice conversation. arXiv preprint arXiv:2410.17799, 2024."
- "[40] M. Züfle, O. Klejch, N. Sanders, J. Niehues, A. Birch, and T. K. Lam. F-Actor: Controllable conversational behaviour in full-duplex models. arXiv preprint arXiv:2601.11329, 2026."

## A. Training Hyperparameters (Table 3)

"The supervised run uses a Moshi-style 7B backbone, 80 H100 GPUs, and 3,600 steps; the reported SFT checkpoint is step 2,925. Both RL stages leave model parameters trainable, with policy gradients flowing through the text head and shared temporal transformer. Decoded speech and transcripts supply rewards; audio-codebook actions receive no direct policy loss."

| Setting | Value |
|---|---|
| Base model | MOSHI [8] |
| SFT execution | 80 H100 GPUs; batch 8/GPU; global batch 640 |
| SFT budget | 3,600 steps; 2.304M fixed sample draws |
| Reported model checkpoint | step 2,925 (1.872M draws) |
| SFT optimizer | AdamW; lr 2.828×10−6; wd 0.1 |
| Depth-former lr | 5.657×10−6 |
| SFT warmup / gradient clip | 500 steps / 3.0 |
| Audio/text sampling mass | 0.88/0.12 |
| First-codebook / text-pad weight | 100/0.5 |
| Turn / backchannel onset weight | 1.5/3.0 |
| Context and response ceiling | 300 s |
| RL learning rate | 5×10−7 |
| RL algorithm | component-normalized GDPO (weighted sum; final batch normalization) |
| RL KL coefficient / target | 0.05/0.01 (adaptive, minimum coefficient 0.02; bounded k3 estimator; both stages) |
| RL clip / gradient clip | 0.2/1.0 |
| RL response-continuity term | weight 0.5, target 4.0 s (both stages) |
| RL continuation-duration bonus (stage 2) | weight 2.0, target 4 s, on noise-robustness and user-backchannel events |
| RL reward weights | interactivity 1.0; transcript rubric judge 0.75 (Gemini 3.6 Flash) |
| RL event context / max response | 30 s / 30 s |
| RL policy stream | text stream incl. padding actions |
| Parameter dtype | bfloat16 (fp32 master persisted for RL); weight-delta gate (≥ 5% of elements changed, median ≥ 1 ULP) in both stages |
| Gradient checkpointing | on |

Table caption (verbatim): "Table 3. Training settings. RL stages inherit the preceding policy and freeze a copy as reference."

## A.1 Reward Weights

"Table 4 separates rewards with within-group variation from hard validity checks and held-out evaluation metrics. In the stage-1 run the transcript rubric judge is active on the turn and interruption strata only, with within-group standard deviations of 0.14–0.43 and no parse failures in the recorded rollouts."

## A.2 Compute Resources

"The first RL stage ran on four nodes with eight H100 80 GB GPUs each; the second used one eight-GPU H100 80 GB node. From run initialization to saving the checkpoints used in the paper, the recorded intervals were 5.08 and 4.01 hours, respectively, corresponding to approximately 162.7 and 32.1 allocated GPU-hours. These estimates include rollout generation, reward computation, optimization, and checkpoint writes within each interval. They exclude queueing, prior setup, benchmark evaluation, and hosted-model compute. Preliminary runs and training beyond these checkpoints used additional compute, so this subtotal does not represent the full project."

## B. Evaluation and Checkpoint Selection (partial)

B.1 Judges and Checkpoint Selection: "SteerBench and FDB-v2 use Gemini 3.6 Flash. AudioMC, VoiceBench, and FDB-v1 interruption ratings use gpt-5.4-mini at medium reasoning effort; VoiceBench uses three judge samples per item. FDB-v1/v2 transcription uses parakeet-tdt-0.6b-v2. Judge identity and scoring conventions are checked before aggregation. The judge-sensitivity study uses the same generations under both judges; it does not change the reported checkpoint. The development set is separate from benchmark test sets and targets the same capabilities. We select and freeze the checkpoint using development performance alone, then report benchmark results."

B.2 Overlap and Pause Measurement (chunk cuts off mid-sentence): "An overlap check found strong transcript n-gram overlap between 100 of 216 CANDOR pause transcripts and 96 supervised conversations. CANDOR turn and pause tasks are therefore diagnostic for the entire training lineage. Official pause clips also end only 0.02–0.11 seconds after the user's last word, so they cannot measure successful" [chunk ends].

**Covers:** References [16]–[40] (pp. 13–15) + Appendix A (Table 3, A.1–A.2) + Appendix B.1 and start of B.2 (chunk truncates mid-sentence)
