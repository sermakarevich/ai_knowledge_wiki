# FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection
Source: https://arxiv.org/abs/2604.01897
Kind: pdf
Fetched: 2026-09-22T09:31:47.242893+00:00
Tool: pdftotext

                                          FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency
                                                                 and Robust Turn Detection
                                         Chengyou Wang1,∗ , Hongfei Xue1,∗ , Mingchen Shao1 , Chunjiang He1 , Jingbin Hu1 , Shuiyuan Wang1 ,
                                                    Bo Wu2 , Yuyu Ji2 , Jimeng Zheng2 , Ruofei Chen2 , Zhou Zhu3 , Lei Xie1,∗∗
                                                                   1
                                                                       Audio, Speech and Language Processing Group (ASLP@NPU)
                                                                                             2
                                                                                               Shengwang
                                                                                             3
                                                                                               QualiaLabs
                                                                               asd6404112a@mail.nwpu.edu.cn, lxie@nwpu.edu.cn


                                                                       Abstract                                       In practical deployments, existing full-duplex spoken dia-
                                                                                                                 logue systems [9, 10] often rely on turn detection to provide a
                                              Recent advances in AudioLLMs have enabled spoken di-               controllable interface between speech processing and response
                                         alogue systems to move beyond turn-based interaction toward             generation. Current turn detection approaches can be broadly
                                         real-time full-duplex communication, where the agent must de-           categorized into two groups. The first group relies on voice
                                         cide when to speak, yield, or interrupt while the user is still talk-   activity detection (VAD) and infers interruption timing from
                                         ing. Existing full-duplex approaches either rely on voice activ-        acoustic energy or activity patterns [11, 12, 13]. These methods
                                         ity cues, which lack semantic understanding, or on ASR-based            are lightweight and fast, but primarily capture speech presence




arXiv:2604.01897v6 [cs.SD] 13 Jul 2026
                                         modules, which introduce latency and degrade under overlap-             rather than communicative intent, making them prone to false
                                         ping speech and noise. Moreover, available datasets rarely cap-         triggers from backchannels, hesitations, or background noise.
                                         ture realistic interaction dynamics, limiting evaluation and de-        The second group introduces explicit turn prediction modules
                                         ployment. To mitigate the problem, we propose FastTurn, a               using learned models. Representative examples include Smart
                                         unified framework for low-latency and robust turn detection.            Turn, TEN Turn Detection, and Easy Turn [14]. The second ap-
                                         To advance latency while maintaining performance, FastTurn              proach enhances conversational intent detection by leveraging
                                         combines streaming CTC decoding with acoustic features, en-             learned models and text-based cues, making it more adaptable
                                         abling early decisions from partial observations while preserv-         to complex dialogues.
                                         ing semantic cues. We also release a test set based on real
                                                                                                                      However, turn detection still faces significant challenges in
                                         human dialogue, capturing authentic turn transitions, overlap-
                                                                                                                 both methodology and data. Existing approaches struggle to
                                         ping speech, backchannels, pauses, pitch variation, and envi-
                                                                                                                 balance accuracy and efficiency, particularly in real-time, noisy,
                                         ronmental noise. Experiments show FastTurn achieves higher
                                                                                                                 and overlapping speech scenarios. For instance, Ten Turn relies
                                         decision accuracy with lower interruption latency than repre-
                                                                                                                 on ASR transcripts, and the additional ASR module introduces
                                         sentative baselines and remains robust under challenging acous-
                                                                                                                 latency while performing poorly in noisy environments. Smart
                                         tic conditions, demonstrating its effectiveness for practical full-
                                                                                                                 Turn uses a simple linear layer for prediction, which makes it
                                         duplex dialogue systems.
                                                                                                                 less effective in handling complex conversational scenarios. Al-
                                         Index Terms: spoken dialogue system, full-duplex, turn detec-
                                                                                                                 though Easy Turn generates accurate outputs, it still faces la-
                                         tion
                                                                                                                 tency issues due to the need to first output ASR results, and
                                                                                                                 it has limited capacity to model complex acoustic information.
                                                               1. Introduction                                   Moreover, existing open-source dialogue corpora generally lack
                                         In recent years, rapid advances in AudioLLMs [1, 2, 3, 4, 5, 6]         fine-grained turn-taking annotations, which limits the ability to
                                         have enabled spoken dialogue systems to move beyond tra-                reliably model and evaluate turn detection. Although some di-
                                         ditional turn-based interaction toward more natural real-time           alogue datasets [15, 16] provide partial turn annotations, these
                                         communication. In highly interactive scenarios, this evolution          datasets still fall short of meeting the demands of modern di-
                                         leads to full-duplex interaction, where the system must pro-            alogue systems—especially in real-world scenarios involving
                                         cess speech perception, partial semantic understanding, and re-         multiple participants, background noise, and natural speech in-
                                         sponse planning concurrently while the user is still speaking.          teractions. Furthermore, many turn detection datasets and full-
                                         Unlike turn-based settings [7], a full-duplex system is required        duplex interaction benchmarks [17, 18] are not derived from
                                         to make online decisions about when to continue speaking,               natural dialogues and rarely include realistic interaction struc-
                                         when to yield the floor, and when to insert or interrupt [8, 9, 10].    tures with speech overlap, leading to a mismatch between of-
                                         These decisions involve a delicate latency–accuracy trade-off:          fline benchmarks and real-world deployment.
                                         reacting too late increases overlap and errors, while reacting               To address these limitations, we propose FastTurn, a uni-
                                         too early risks truncating semantics and degrading coherence,           fied framework for low-latency and robust turn detection. Fast-
                                         especially under noisy and overlapped observations. Although            Turn incorporates a streaming Connectionist Temporal Classifi-
                                         large language models excel at reasoning and generation with            cation (CTC) module [19] to enable fast decoding from partial
                                         complete textual inputs, integrating them into low-latency full-        observations, thereby reducing the latency accumulation com-
                                         duplex dialogue systems remains challenging.                            monly introduced by ASR-based cascaded pipelines. By di-
                                                                                                                 rectly integrating acoustic features with learned decision mod-
                                            * These authors contributed equally.                                 eling, the framework mitigates the information loss inherent
                                           ** indicates the corresponding author.                                in text-only approaches while preserving real-time responsive-
           Turn                                                                        FastTurn-Unified. Finally, we enhance robustness by fus-
           State            Sematic Module
                            FastTurn-Semantic
                                                                                  ing semantic and streaming acoustic cues before the final deci-
           LLM
                                LLM(Qwen3-0.6B)
                                     LLM
                                                                                  sion. Intermediate hidden states from the Conformer encoder
                                                                                  are processed by an acoustic adapter to extract fine-grained
           CTC                  CTC
                                CTC                                               acoustic features. These are fused with the LLM’s hidden states
                               Prompt       LLM                 Turn      Turn
          Prompt               Prompt       LLM                                   and forwarded to the turn detector, implemented as a multi-layer
                                           Adapter             Detector   State
                                           Adapter                                perceptron. The detector predicts whether the current speech
                                CTC
           CTC                  CTC
                                                                                  segment is a complete turn. By combining streaming acous-
                                                               Acoustic           tic cues from CTC, LLM-conditioned semantic modeling, and
    Conformer Encoder          Conformer Encoder
                                                               Adapter            acoustic-semantic fusion, the framework improves turn predic-
                                                                                  tion when lexical evidence is ambiguous and prosodic cues are
                                                                                  critical, while maintaining efficient inference.
    (a) FastTurn-Cascaded               (b) FastTurn-Unified
                                                                                  2.2. Train
                      Figure 1: Model architecture
                                                                                  Accurate turn detection relies on the understanding of semantic
                                                                                  information, while acoustic cues are equally essential in com-
                                                                                  plex scenarios. To fully leverage semantic information and ef-
ness. In addition, we release the FastTurn test set 1 , specifi-                  fectively handle challenges such as noise or overlapping speech,
cally designed to capture authentic turn transitions and overlap-                 we adopt a four-stage training pipeline, as shown in Figure 2,
ping speech. The dataset includes challenging conversational                      to stabilize the optimization process and establish speech-text
phenomena such as backchannels, pauses, pitch variations, and                     alignment, thereby improving turn prediction accuracy.
environmental noise. Based on this evaluation set, we can sys-                         Semantic Pretraining. To obtain reliable semantic in-
tematically analyze interaction patterns prone to interruption er-                formation, we first train the Conformer encoder and the CTC
rors, bridging the gap between controlled offline benchmarks                      branch on ASR data. Simultaneously, we fine-tune the LLM on
and real-world deployment conditions. Extensive experiments                       text-only data to better adapt it for the turn detection task. By
demonstrate that FastTurn achieves consistently higher decision                   inserting the turn state as a special token in the input sequence,
accuracy while substantially reducing interruption latency com-                   we reduce the number of tokens generated by the LLM, thereby
pared with representative baselines. Notably, the framework                       improving its efficiency for this task.
maintains robust performance under challenging scenarios in-                           Modality Alignment. To address the limitations of CTC
volving conversational backchannels and environmental noise,                      in noisy or overlapping speech conditions, we train the LLM
validating its effectiveness for practical full-duplex spoken dia-                adapter under the ASR objective to map the encoder outputs
logue systems.                                                                    into the LLM input space. This ensures consistency between
                                                                                  speech representations and textual supervision in a shared se-
                            2. FastTurn                                           mantic space.
                                                                                       Joint Training. To activate the LLM’s inherent capability
2.1. Architecture                                                                 for turn detection, we jointly train the LLM and LLM adapter,
As shown in Figure 1, the framework consists of three compo-                      conditioning the prediction on both acoustic embeddings and
nents: FastTurn-Semantic, an acoustic adapter, and a turn detec-                  the CTC prompt. To prevent overfitting to the CTC branch
tor. The architecture is developed in three steps. First, we use                  and preserve the LLM’s language modeling ability, we apply
FastTurn-Cascaded to route a fast CTC transcript to an LLM                        prompt dropout: with a probability of p < 0.5, the CTC prompt
for low-latency decisions, then progressively introduce speech-                   is randomly dropped during training, encouraging better gener-
derived cues to enhance robustness.                                               alization.
     FastTurn-Cascaded. Turn decisions rely on a transcript,                           Modality Fusion. To further improve the robustness and
but generating it introduces decoding latency. To minimize this,                  accuracy of turn detection, we fuse semantic and acoustic cues.
we introduce a CTC branch for fast alignment and greedy de-                       We train the acoustic adapter and turn detector on the same
coding, enabling streaming transcription. The transcription is                    dataset, combining Conformer representations with LLM hid-
formatted as a CTC prompt and fed into the LLM (Qwen3-                            den states. This fusion enables joint modeling of prosodic
0.6B) [20] for turn prediction, providing explicit cues with min-                 and semantic cues, significantly enhancing the accuracy of turn
imal decoding overhead. However, as the LLM input is dom-                         boundary prediction and increasing the overall robustness of the
inated by the CTC transcript, predictions are sensitive to CTC                    system.
errors, especially in the presence of speech overlap and noise.
                                                                                  2.3. FastTurn test set
     FastTurn-Semantic. To reduce reliance on transcript qual-
ity, we extend the FastTurn-Cascaded design by incorporat-                        Current open-source dialogue corpora often lack detailed turn-
ing speech-derived features into the LLM. The Conformer en-                       taking annotations, limiting the development of reliable turn
coder extracts high-level acoustic representations, which, along                  detection models. To address this issue, we collected high-
with the CTC prompt, are projected into the LLM input space                       quality dual-channel real human-to-human dialogue data and,
through an LLM adapter, ensuring feature alignment. The                           after precise annotation, constructed our test set. The annota-
LLM then uses both the CTC prompt and aligned acoustic                            tions include detailed labels such as speaker identities, emo-
embeddings for turn-related reasoning. This approach allows                       tions, timestamps, turn boundaries, paralinguistic cues (such as
FastTurn-Semantic to mitigate CTC errors while preserving the                     pauses, overlaps, and backchannels), and transcriptions. These
latency advantage of early textual conditioning.                                  annotations provide a comprehensive understanding of inter-
                                                                                  action structure, temporal alignment, and interruption behav-
   1 https://github.com/qualialabsAI/SmoothConv                                   iors. By combining dual-channel audio with these rich, multi-
            FastTurn-Cascaded               Modality Alignment                  Joint Training                  Modality Fusion


       ASR Data        Text Data                 ASR Data                   Turn-Detection Data                Turn-Detection Data

                                                 Encoder                           Encoder                     FastTurn-Semantic
        Encoder          LLM
                                                           LLM                             LLM
                                           CTC                               CTC                                Encoder     LLM
                                                          Adapter                         Adapter
                                                                                                                Hidden     Hidden
                         Turn                     LLM
          CTC                                                                       LLM
                         State                                                                             Acoustic         Turn
                                      FastTurn-Semantic                 FastTurn-Semantic                  Adapter         Detector

                                                          Figure 2: Training Strategy


dimensional annotations and transcriptions, the test set serves            of 8. Both the LLM and acoustic adapters are based on 4-layer
as an important resource for research on dialogue coordination,            Transformer architectures, each with approximately 24 million
interruption modeling, and full-duplex systems, aimed at accu-             parameters. The turn detector is a 3-layer multi-layer percep-
rately capturing turn transitions and interaction flow in natural          tron (MLP) that predicts turn boundaries using fused features
dialogues.                                                                 from the Conformer encoder and LLM. All experiments are
                                                                           conducted on 8 NVIDIA A6000 GPUs. For the ASR task, the
          Table 1: Statistics of the FastTurn test set.                    learning rate is set to 1 × 10−4 with a warm-up period of 8,000
                                                                           steps, and training lasts for 80,000 steps. For turn detection,
   Turn State      Source          Samples       Duration (h)              LLM fine-tuning is done with a learning rate of 1 × 10−5 for
                                                                           2 epochs, followed by joint training and modality fusion with
   Complete        real-world         14709                 9.64           learning rates of 5 × 10−6 and 1 × 10−4 , respectively, each
   Incomplete      real-world          3643                 2.15           trained for 11,000 steps.
   Backchannel     real-world          3080                 0.42
   Wait            Synthesized         1000                 0.71           3.3. Evaluation metrics
                                                                           To evaluate model performance in full-duplex conversational
    To evaluate turn-state prediction, we construct an evalua-             scenarios, we employ three primary metrics: Accuracy, Miss
tion set consisting of segments from real-world data and 1,000             Rate, and False Alarm Rate. These are derived from turn-state
synthetically generated wait state samples, as shown in Table 1.           classification results, where True Positives (TP) and True Neg-
Since the wait state is rare in natural conversations, we sup-             atives (TN) denote correct predictions, and False Positives (FP)
plement the set with 1,000 samples generated using DeepSeek                and False Negatives (FN) denote errors.
V3 [21] for text and IndexTTS2 [22] for audio synthesis.
                                                                                                            TP + TN
                                                                                         Accuracy =                      .              (1)
                    3. Experiments                                                                     TP + TN + FP + FN

3.1. Datasets                                                                                                    FN
                                                                                                 Miss Rate =           .                (2)
ASR Task. We use large-scale open-source corpora and in-                                                       TP + FN
ternal datasets, including AISHELL-1 [23], AISHELL-2 [24],                                                           FP
WenetSpeech [25], LibriSpeech [26], GigaSpeech [27], and                                     False Alarm Rate =           .             (3)
                                                                                                                  FP + TN
MLS [28], totaling over 30,000 hours of Chinese and English
speech to support robust feature learning.                                 3.4. Main results
Turn Detection Task. We use the Easy Turn training set,
                                                                           To evaluate the model’s performance in complex conversational
augmented with internal conversational data and synthetic cor-
                                                                           scenarios, Table 2 presents the results of the FastTurn model
pora. Dialogue texts are generated by Qwen3-32B [20] and
                                                                           and baseline models. The results indicate that models relying
DeepSeek-v3 [21], then synthesized into speech using In-
                                                                           solely on semantic information, such as Paraformer+Ten Turn
dextts2 [22]. To generate complete and incomplete states, we
                                                                           and FastTurn-Cascaded, perform poorly in both the Complete
use forced alignment to extract word-level timestamps and cre-
                                                                           and Incomplete categories, exhibiting low accuracy along with
ate negative samples by truncating complete turns at random
                                                                           high miss and false alarm rates. In contrast, models that bet-
temporal positions, ensuring linguistic incompleteness through
                                                                           ter integrate semantic and acoustic information, such as Easy
filtering.
                                                                           Turn and FastTurn-Unified, perform better. Notably, FastTurn-
                                                                           Unified achieves the best performance across all categories,
3.2. Experimental setup
                                                                           highlighting the importance of deeply combining semantic and
The model architecture consists of a 12-layer Conformer en-                acoustic features to improve model performance.
coder [29] with approximately 80 million parameters, using 8                    We evaluate the model’s accuracy and latency across multi-
attention heads and a convolutional module with a kernel size              ple test sets to assess its performance and real-time processing
Table 2: Turn-detection performance on the FastTurn test set. Higher Accuracy (↑) and lower Miss Rate (↓) and False Alarm Rate (↓)
are better. Para. denotes Paraformer, green rows indicate our models. Bold numbers show best results; underlined numbers show
second-best results.

                                       Complete                  Incomplete                  Backchannel                   Wait
   Model
                               Acc ↑ Miss ↓       FA ↓     Acc ↑ Miss ↓          FA ↓     Acc ↑ Miss ↓ FA ↓ Acc ↑ Miss ↓ FA ↓
                          2
   Para. [30]+Ten Turn         71.52    28.71     28.34    58.27       32.70     47.15      –        –      –      98.15   2.78     0.31
   Smart Turn 3                49.21    49.97     51.93    49.21       51.93     49.97      –        –      –        –       –       –
   Easy Turn [14]              80.10    21.93     15.46    82.28       35.21     14.14    93.91     6.40   6.03    98.64   2.20     0.05
   FastTurn-Cascaded           73.26    34.60     12.29    65.95       24.11     36.49    86.62    66.24   3.56    97.21   4.89     0.21
    + FastTurn-Semantic        79.69    22.67     15.17    76.41       32.03     21.87    89.55    43.73   4.87    98.57   3.79     0.18
     + FastTurn-Unified        81.64    14.53     14.92    81.01       35.71     15.57    93.93     7.68   5.63    98.75   2.31     0.39

Table 3: Turn-detection performance comparison across test sets. Acc denotes overall accuracy (%), Lat. denotes average latency
(ms), and Params denotes the number of parameters (M). “Com” and “Inc” denote complete and incomplete detection, respectively.

  Model                  Params Smart Turn (zh)           Easy Turn        FastTurn        Smart Turn (en)-Com      Smart Turn (en)-Inc
                                     Acc      Lat.       Acc    Lat.      Acc      Lat.    Acc ↑ Miss ↓    FA ↓    Acc ↑ Miss ↓     FA ↓
  Para.+Ten Turn           7220     83.10    124.3     86.00   212.0     51.97    114.8    79.07   15.27   26.36   79.13   26.44   15.06
  Smart Turn                32      90.53    70.22     76.86   62.28     49.21    116.9    94.71   4.72     5.84   94.71    5.84    4.72
  Easy Turn                 850     57.16    687.8     96.38   355.9     78.05    297.1      –       –        –      –        –       –
  FastTurn-Cascaded         650     75.42    150.1     96.13   153.1     62.50    126.3    76.18    4.93   41.99   76.09   42.76   4.30
   +FastTurn-Unified        700     76.58    139.0     94.50   136.4     79.62    120.1    77.34    5.24   39.40   77.35   40.01   4.59


capabilities. Table 3 shows results for the Smart Turn, Easy               achieves performance close to CTC decoding on most evalu-
Turn, and FastTurn test sets. The Smart Turn model outper-                 ation sets. During training, only the adapter parameters are
forms others on its test set due to mismatches in data and la-             updated while all other components remain frozen. This con-
bel categories. The test set, with only two categories (“com-              strained setting limits full adaptation to the ASR objective and
plete” and “incomplete”), does not fully align with our multi-             results in a consistent yet moderate gap compared with CTC
class model, and its simplified data contributes to its better per-        decoding. Nevertheless, the aligned representations effectively
formance. The Easy Turn test set, with 800 samples and no                  inject high-level semantic information into the LLM, enabling
background noise, relies on semantic cues, leading to strong               competitive autoregressive decoding despite restricted parame-
performance from FastTurn-Cascaded. However, FastTurn per-                 ter updates.
forms slightly worse due to a small sample size and sensitivity
to variations. The FastTurn test set, with more echo signals and           3.6. Ablation study
acoustic ambiguity, presents a greater challenge for turn-state
modeling. In terms of latency, Smart Turn’s simplified design              As shown in Table 2, FastTurn-Semantic improves turn detec-
results in low latency but poorer performance in complex sce-              tion performance over FastTurn-Cascaded by reducing reliance
narios. FastTurn-Unified achieves lower latency than both Easy             on transcript quality and incorporating speech-derived features,
Turn and FastTurn-Cascaded while maintaining similar or bet-               which helps compensate for CTC errors in noisy or overlapping
ter accuracy. For the English subset, results met expectations,            speech conditions. FastTurn-Unified further demonstrates the
but did not surpass Paraformer+Ten Turn[30]. Limited opti-                 effectiveness of combining semantic and acoustic cues for real-
mization and English dialogue data affected the model’s perfor-            time turn detection.
mance.

3.5. ASR results
                                                                                                   4. Conclusion
                                                                           This paper presents FastTurn, a framework for efficient turn de-
Table 4: Recognition performance on evaluation sets: Chinese               tection in full-duplex systems. By utilizing fast CTC decod-
CER (%) and English WER (%). For LLM decoding, variants                    ing and integrating acoustic features, FastTurn reduces latency
differ only in the LLM adapter architecture.                               and enhances robustness. We release a comprehensive test set
                                                                           to promote research on conversational turn-taking and speech
 Decoding   LLM Adapter LibriClean TestNet AISHELL-1                       overlap phenomena, specifically designed to capture realistic in-
 CTC greedy –              7.06     9.52      2.33                         teraction dynamics. FastTurn effectively handles complex con-
 LLM        2L MLP         14.09    16.80     6.45
                                                                           versational patterns, such as echo signals and speech overlap,
                                                                           while maintaining high accuracy and low latency. Experimen-
 LLM        2L Transformer  7.19    10.74     5.31
                                                                           tal results demonstrate that FastTurn exhibits strong robustness
 LLM        4L Transformer 5.56     10.74     3.69                         under challenging acoustic conditions, making it a promising
                                                                           solution for real-time, scalable turn detection. Future work will
    As shown in Table 4, LLM-based autoregressive decoding                 focus on optimizing the model’s performance and extending its
application to more dynamic conversational scenarios.                       [17] G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu,
                                                                                 and H.-y. Lee, “Full-duplex-bench: A benchmark to evaluate full-
                                                                                 duplex spoken dialogue models on turn-taking capabilities,” arXiv
                        5. References                                            preprint arXiv:2503.04721, 2025.
 [1] R. Huang, M. Li, D. Yang, J. Shi, X. Chang, Z. Ye, Y. Wu,              [18] Y. Peng, Y.-W. Chao, D. Ng, Y. Ma, C. Ni, B. Ma, and E. S.
     Z. Hong, J. Huang, J. Liu et al., “Audiogpt: Understanding and              Chng, “Fd-bench: A full-duplex benchmarking pipeline de-
     generating speech, music, sound, and talking head,” in Proceed-             signed for full duplex spoken dialogue systems,” arXiv preprint
     ings of the AAAI Conference on Artificial Intelligence, vol. 38,            arXiv:2507.19040, 2025.
     no. 21, 2024, pp. 23 802–23 804.
                                                                            [19] A. Graves, S. Fernández, F. Gomez, and J. Schmidhuber, “Con-
 [2] Y. Chu, J. Xu, Q. Yang, H. Wei, X. Wei, Z. Guo, Y. Leng, Y. Lv,             nectionist temporal classification: labelling unsegmented se-
     J. He, J. Lin et al., “Qwen2-audio technical report,” arXiv preprint        quence data with recurrent neural networks,” in Proceedings of
     arXiv:2407.10759, 2024.                                                     the 23rd international conference on Machine learning, 2006, pp.
 [3] W. Yu, S. Wang, X. Yang, X. Chen, X. Tian, J. Zhang, G. Sun,                369–376.
     L. Lu, Y. Wang, and C. Zhang, “Salmonn-omni: A codec-free              [20] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu,
     llm for full-duplex speech understanding and generation,” arXiv             C. Gao, C. Huang, C. Lv et al., “Qwen3 technical report,” arXiv
     preprint arXiv:2411.18138, 2024.                                            preprint arXiv:2505.09388, 2025.
 [4] A. Zeng, Z. Du, M. Liu, K. Wang, S. Jiang, L. Zhao, Y. Dong, and       [21] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao,
     J. Tang, “Glm-4-voice: Towards intelligent and human-like end-              C. Deng, C. Zhang, C. Ruan et al., “Deepseek-v3 technical re-
     to-end spoken chatbot,” arXiv preprint arXiv:2412.02612, 2024.              port,” arXiv preprint arXiv:2412.19437, 2024.
 [5] Z. Xie and C. Wu, “Mini-omni: Language models can hear, talk           [22] S. Zhou, Y. Zhou, Y. He, X. Zhou, J. Wang, W. Deng, and
     while thinking in streaming,” arXiv preprint arXiv:2408.16725,              J. Shu, “Indextts2: A breakthrough in emotionally expressive
     2024.                                                                       and duration-controlled auto-regressive zero-shot text-to-speech,”
 [6] X. Geng, Q. Shao, H. Xue, S. Wang, H. Xie, Z. Guo, Y. Zhao,                 arXiv preprint arXiv:2506.21619, 2025.
     G. Li, W. Tian, C. Wang et al., “Osum-echat: Enhancing end-to-         [23] H. Bu, J. Du, X. Na, B. Wu, and H. Zheng, “Aishell-1: An open-
     end empathetic spoken chatbot via understanding-driven spoken               source mandarin speech corpus and a speech recognition base-
     dialogue,” arXiv preprint arXiv:2508.09600, 2025.                           line,” in 2017 20th conference of the oriental chapter of the inter-
 [7] X. Lu, W. Xu, H. Wang, H. Zhou, H. Zhao, C. Zhu, T. Zhao, and               national coordinating committee on speech databases and speech
     M. Yang, “Duplexmamba: Enhancing real-time speech conver-                   I/O systems and assessment (O-COCOSDA). IEEE, 2017, pp.
     sations with duplex and streaming capabilities,” in CCF Interna-            1–5.
     tional Conference on Natural Language Processing and Chinese           [24] J. Du, X. Na, X. Liu, and H. Bu, “Aishell-2: Transform-
     Computing. Springer, 2025, pp. 62–74.                                       ing mandarin asr research into industrial scale,” arXiv preprint
 [8] C. Liu, J. Jiang, C. Xiong, Y. Yang, and J. Ye, “Towards building           arXiv:1808.10583, 2018.
     an intelligent chatbot for customer service: Learning to respond at    [25] B. Zhang, H. Lv, P. Guo, Q. Shao, C. Yang, L. Xie, X. Xu, H. Bu,
     the appropriate time,” in Proceedings of the 26th ACM SIGKDD                X. Chen, C. Zeng et al., “Wenetspeech: A 10000+ hours multi-
     international conference on Knowledge Discovery & Data Min-                 domain mandarin corpus for speech recognition,” in IEEE Inter-
     ing, 2020, pp. 3377–3385.                                                   national Conference on Acoustics, Speech and Signal Processing
 [9] Y. Leviathan and Y. Matias, “Google duplex: An ai system for                (ICASSP). IEEE, 2022, pp. 6182–6186.
     accomplishing real-world tasks over the phone,” Google AI blog,        [26] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, “Lib-
     vol. 8, 2018.                                                               rispeech: an asr corpus based on public domain audio books,”
[10] A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou,        in 2015 IEEE international conference on acoustics, speech and
     E. Grave, and N. Zeghidour, “Moshi: a speech-text foundation                signal processing (ICASSP). IEEE, 2015, pp. 5206–5210.
     model for real-time dialogue,” arXiv preprint arXiv:2410.00037,        [27] G. Chen, S. Chai, G. Wang, J. Du, W.-Q. Zhang, C. Weng, D. Su,
     2024.                                                                       D. Povey, J. Trmal, J. Zhang et al., “Gigaspeech: An evolving,
[11] X. Wang, Y. Li, C. Fu, Y. Shen, L. Xie, K. Li, X. Sun, and L. Ma,           multi-domain asr corpus with 10,000 hours of transcribed audio,”
     “Freeze-omni: A smart and low latency speech-to-speech dia-                 arXiv preprint arXiv:2106.06909, 2021.
     logue model with frozen llm,” arXiv preprint arXiv:2411.00774,         [28] V. Pratap, Q. Xu, A. Sriram, G. Synnaeve, and R. Collobert,
     2024.                                                                       “Mls: A large-scale multilingual dataset for speech research,”
[12] J. Chen, Y. Hu, J. Li, K. Li, K. Liu, W. Li, X. Li, Z. Li, F. Shen,         arXiv preprint arXiv:2012.03411, 2020.
     X. Tang et al., “Fireredchat: A pluggable, full-duplex voice in-       [29] A. Gulati, J. Qin, C.-C. Chiu, N. Parmar, Y. Zhang, J. Yu, W. Han,
     teraction system with cascaded and semi-cascaded implementa-                S. Wang, Z. Zhang, Y. Wu et al., “Conformer: Convolution-
     tions,” arXiv preprint arXiv:2509.06502, 2025.                              augmented transformer for speech recognition,” arXiv preprint
[13] C. Fu, H. Lin, X. Wang, Y.-F. Zhang, Y. Shen, X. Liu, H. Cao,               arXiv:2005.08100, 2020.
     Z. Long, H. Gao, K. Li et al., “Vita-1.5: Towards gpt-4o               [30] Z. Gao, S. Zhang, I. McLoughlin, and Z. Yan, “Paraformer: Fast
     level real-time vision and speech interaction,” arXiv preprint              and accurate parallel transformer for non-autoregressive end-to-
     arXiv:2501.01957, 2025.                                                     end speech recognition,” arXiv preprint arXiv:2206.08317, 2022.
[14] G. Li, C. Wang, H. Xue, S. Wang, D. Gao, Z. Zhang, Y. Lin,
     W. Li, L. Xiao, Z. Fu, and L. Xie, “Easy turn: Integrating acous-
     tic and linguistic modalities for robust turn-taking in full-duplex
     spoken dialogue systems,” in IEEE International Conference on
     Acoustics, Speech and Signal Processing (ICASSP), 2026.
[15] W. Kraaij, T. Hain, M. Lincoln, and W. Post, “The ami meeting
     corpus,” in Proc. International Conference on Methods and Tech-
     niques in Behavioral Research, 2005, pp. 1–4.
[16] Z. Yang, Y. Chen, L. Luo, R. Yang, L. Ye, G. Cheng, J. Xu, Y. Jin,
     Q. Zhang, P. Zhang et al., “Open source magicdata-ramc: A rich
     annotated mandarin conversational (ramc) speech dataset,” arXiv
     preprint arXiv:2203.16844, 2022.

