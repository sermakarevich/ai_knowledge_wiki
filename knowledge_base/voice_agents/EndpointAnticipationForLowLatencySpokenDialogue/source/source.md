# Endpoint Anticipation for Low-Latency Spoken Dialogue
Source: https://arxiv.org/abs/2606.13450
Kind: pdf
Fetched: 2026-09-22T09:32:58.648752+00:00
Tool: pdftotext

                                                              Endpoint Anticipation for Low-Latency Spoken Dialogue
                                                                  Sathvik Udupa1 , Shinji Watanabe2 , Petr Schwarz1 , Jan Cernocky1
                                                                                      1
                                                                                       Brno University of Technology, Czechia
                                                                                  2
                                                                                      Carnegie Mellon University, United States
                                                                      {udupa, schwarzp, cernocky}@fit.vut.cz, shinjiw@ieee.org




                                                                     Abstract                                    ongoing speech. By generating initial hypotheses and pre-
                                                                                                                 fetching audio frames during the user’s speech, we “pipeline”
                                           While low-latency interaction is critical for spoken dialogue,




arXiv:2606.13450v1 [eess.AS] 11 Jun 2026
                                                                                                                 the generation process to significantly mask system latency.
                                           cascaded architectures are often bottlenecked by reactive turn-            To demonstrate viability, we integrate our model into the
                                           completion detection. We propose Endpoint Anticipation, shift-        Unmute framework using speculative execution. An anticipated
                                           ing from reactive detection to proactive forecasting of end-of-       EOT triggers the system to initiate the LLM-TTS pipeline in the
                                           turn signals. Our speech-based model anticipates endpoints up         background. If the user continues speaking, this constitutes a
                                           to 2.56 seconds in advance, enabling speculative execution of         premature trigger. The system subsequently discards the specu-
                                           LLM and TTS pipelines on partial context. We introduce met-           lative response at the next anticipated signal. Upon a confirmed
                                           rics to quantify the trade-off between realized latency reduction     endpoint, we complete the pre-buffered prefix with the pending
                                           and computational redundancy. Evaluation across conversa-             transcript and continue generation seamlessly from the specula-
                                           tional and task-oriented datasets shows our model consistently        tive tokens. This mechanism introduces a fundamental trade-off
                                           outperforms competitive VAP-based baselines. Integration with         between latency reduction and the computational cost of dis-
                                           the Unmute framework demonstrates a 505 ms average latency            carded generations. Consequently, we propose a comprehensive
                                           reduction with a 28.4% increase in speculative computation, ef-       set of metrics to quantify this balance. These metrics strictly
                                           fectively masking sequential bottlenecks to enable complex rea-       distinguish between successful anticipation horizons and pre-
                                           soning in real-time speech-to-speech interaction.                     mature prediction rates.
                                           Index Terms: spoken dialogue system, low-latency systems,                  The contributions of this work are as follows:
                                           cascaded full-duplex system, endpointing
                                                                                                                1. We propose a speech-based Endpoint Anticipation task and
                                                                                                                    model designed for low-latency spoken dialogue systems.
                                                                1. Introduction                                 2. We define a set of metrics to quantify the trade-off between
                                           Real-time spoken dialogue systems [1] have seen significant              Realized Anticipation (the actual latency reduction provided
                                           growth, driven by advances in large language models (LLMs).              within the target window) and Premature Anticipation (the
                                           These systems [2–9] aim to process audio with low latency to             resulting downstream computational redundancy due to pre-
                                           perform complex tasks, often utilizing streaming speech inputs           dictions made before the valid horizon).
                                           paired with the reasoning capabilities of LLMs to generate re-       3. We evaluate the framework across various anticipation targets
                                           sponses.                                                                 ranging from 320 ms to 2560 ms.
                                                While end-to-end training offers a path to low latency [2],     4. We open-source our implementation and provide a reference
                                           many competitive frameworks such as Unmute1 rely on cas-                 integration with the Unmute full-duplex framework.3
                                           caded architectures that control turn-taking via an endpointer
                                           [10–13]. In these systems, detecting an endpoint triggers a se-
                                           quential pipeline — completing automatic speech recognition
                                                                                                                                    2. Related Work
                                           (ASR), LLM generation, and Text-to-Speech (TTS) — which              Early End-of-Utterance Prediction. Several approaches uti-
                                           imposes a theoretical lower bound on the Time-to-First-Audio         lize ASR to predict End-of-Utterance (EOU) tokens ahead of
                                           (TTFA). Consequently, while humans respond within ∼250 ms            time. Sakuma et al. [17, 18] propose a two-stage method: first
                                           [14], modular setups like ChipChat, Unmute, and Pipecat2 ex-         generating a text hypothesis from streaming ASR, followed by
                                           hibit latencies close to 1–2 seconds [5,15]. This gap persists be-   a language model that predicts future EOU tokens. Chang
                                           cause current systems are reactive, whereas human listeners ac-      et al. [19] similarly exploit early endpoint signals to prefetch
                                           tively anticipate turn completions using linguistic and prosodic     downstream responses, controlling the trigger via a confidence
                                           cues to minimize gaps [16]. This cascaded bottleneck, where          threshold; our method differs in that we parameterize prefetch-
                                           generation cannot begin until speech ends, creates a significant     ing through a fixed anticipation horizon rather than a decision
                                           barrier for integrating further processing such as dialogue man-     boundary, decoupling it from ASR confidence entirely. Sim-
                                           agement, tool-use, or reasoning.                                     ilarly, Zink et al. [20] leverage the decoder of an encoder-
                                                To overcome this, we introduce endpoint anticipation, a         decoder ASR model for early EOU prediction. Unlike these
                                           framework that forecasts EOT signals before turn completion.         text-dependent approaches, our work introduces a speech-only
                                           Unlike standard endpointing, this early forecasting allows the       forecasting model that operates directly on the acoustic signal,
                                           system to initiate LLM and TTS processing during the user’s          entirely bypassing the ASR bottleneck.
                                                                                                                Voice Activity Projection (VAP). VAP [11, 21, 22] projects the
                                              1 https://github.com/kyutai-labs/unmute
                                              2 https://github.com/pipecat-ai/pipecat                              3 https://github.com/bloodraven66/EndpointAnticipation
                                                                                                                     (h)
future voice activity of two speakers to learn general turn-taking    During deployment, the first frame where ŷt         = 1 acts as the
abilities, introducing a T URN -S HIFT task to predict near-future    trigger for the speculative pipeline.
speaker changes. While VAP focuses on generalized dialogue
states over discrete bins, our work directly targets continuous,      3.3. Model Architectures
fixed-horizon endpoint forecasting. Consequently, we adapt
                                                                      We investigate two modeling strategies to predict the set of an-
VAP’s projected future probabilities to serve as our primary                                (h)
baseline for comparative evaluation.                                  ticipation windows {yt }h∈H defined in Eq. 2.
Computation-Intensive SDS. Recent spoken dialogue systems             EPA-S (Single-Target Learning): We train |H| independent
increasingly incorporate complex, real-time processing. Re-           models, one for each horizon. For a specific horizon h ∈ H, the
cent works [23, 24] introduce chain-of-thought reasoning for          dedicated model extracts the concatenated context vector Z≤t
end-to-end SDS, while KAME [15] uses a secondary LLM for              and estimates the endpoint probability as:
reasoning over partial transcripts, and Stream RAG [25] en-                               pt
                                                                                            (h)
                                                                                                  = σ(W · Z≤t + b)                     (4)
ables low-latency audio tool-calling. While end-to-end archi-
tectures natively accommodate such computational demands,             where σ is the sigmoid function, and W and b are the param-
cascaded systems remain constrained by sequential latency bot-        eters of the projection head. While flexible, the computational
tlenecks. Our framework mitigates this limitation, enabling           and memory cost scales linearly with |H|. Note that, unlike
modular pipelines to integrate complex processing while pre-          VAP [21], the loss is computed only for one primary speaker,
serving low-latency interactions.                                     and the features from other speaker act as conversation context.
                                                                      EPA-M (Multi-target Learning): To improve efficiency, we
                3. Proposed approach                                  use Multi-Task Learning with a shared dual-stream backbone.
                                                                      The model branches only at the final layer to produce predic-
In this section, we describe the model backbone and introduce         tions for all horizons simultaneously:
the modeling framework for endpoint anticipation.
                                                                                   (h)
                                                                                  pt     = σ(Wh · Z≤t + bh ),     ∀h ∈ H               (5)
3.1. Dual-stream audio representation
                                                                      where Z≤t is the shared latent representation. This setup
Similar to [12, 21], we process User (u) and System (s) audio         learns generalized turn-completion features while maintaining
streams to provide interaction context. Let t denote the times-       horizon-specific decision boundaries via the heads {Wh , bh }.
                                   (u)         (s)
tamp of the current frame. Let X≤t and X≤t represent the
sequences of audio features extracted up to frame t from their                         4. Experimental setup
respective channels. We employ two independent streaming
Transformer encoders, Tu and Ts , to process each stream:             4.1. Dataset
              (u)          (u)       (s)          (s)                 We train and evaluate on SpokenWOZ [26] (8 kHz, task-
            Z≤t = Tu (X≤t ),       Z≤t = Ts (X≤t )             (1)    oriented) and Switchboard [27] (8 kHz, conversational), mod-
     The resulting latent representations are concatenated along      eling the User and Speaker A streams as primary speakers, re-
the feature dimension to form a unified context vector Z≤t =          spectively. To ensure precise endpoint supervision, we refine
   (u)   (s)                                                          raw turn boundaries using Silero VAD [28] to strip trailing si-
[Z≤t ; Z≤t ]. This fused representation is then passed to the pre-
                                                                      lence. To prevent premature predictions at speech onset and
diction heads described below. This ensures the model can learn
                                                                      exclude backchannels4 , we mask the loss for turns shorter than
to anticipate endpoints in the presence of turn-taking conditions
                                                                      2 seconds (also requiring a min. of 3 words for Switchboard).
such as backchannels and interruptions.
                                                                      4.2. Baseline
3.2. Endpoint Anticipation (EPA)
                                                                      We use the pretrained Voice Activity Projection (VAP)5 [21] as
We formulate Endpoint Anticipation (EPA) as a set of indepen-
                                                                      our baseline. Because VAP outputs 50 Hz turn-taking proba-
dent binary classification tasks. Let H = {320, 640, . . . , 2560}
                                                                      bilities over discrete temporal bins, we adapt it to our continu-
be the set of anticipation horizons in milliseconds. For each
                                     (h)                              ous 12.5 Hz horizon-based evaluation. Specifically, we extract
horizon h ∈ H, the binary target yt at time t is defined as:          the non-active speaker’s probability from the p future distribu-
                       (                                              tion and downsample it to 12.5 Hz via 4-frame mean pooling.
               (h)       1 if 0 ≤ tEOT − t ≤ h,                       To establish the most competitive baseline, we ran inference on
              yt =                                              (2)
                         0 otherwise                                  different p future bin combinations and present the best results;
                                                                      we apply our evaluation threshold to the pooled probabilities of
where tEOT is the timestamp of the user’s turn completion. We         bins [0–1] (0–600 ms) for the 640 ms anticipation window, and
evaluate predictors for all h ∈ H. At our feature frame rate of       bins [1–2] (200–1200 ms) for the 1280 ms window.
12.5 Hz (80 ms period), the smallest horizon h = 320 corre-
sponds to an anticipation window of exactly 4 frames.                 4.3. Metrics
                                                            (h)
     During inference, the model estimates the probability pt
                                                            (h)       While prior works typically rely on aggregate precision and re-
of an upcoming endpoint. The binary anticipation decision ŷt
                                                                      call [21], we introduce four metrics explicitly designed to quan-
is triggered using a predefined threshold θ:
                                                                      tify the practical trade-offs between latency reduction (success-
                                                                      ful anticipation) and wasted computation (premature predic-
                            (
                                     (h)
                      (h)     1 if pt ≥ θ,
                    ŷt =                                   (3)       tions) in real-time systems:
                              0 otherwise
                                                                         4 We mask the loss during primary speaker backchannels, as they
This threshold dictates the operating point. It allows tuning the     lack sufficient context for forecasting turn completion.
balance between latency reduction and premature predictions.             5 https://github.com/ErikEkstedt/VAP
• Median Realized Anticipation (MRA): Measures the actual                 Model       h     MRA (ms) ↑     HEA (%) ↑    PAR (%) ↓     ERC ↓
   latency savings. For turns with a successful prediction inside          VAP       640       160           19.2         68.3         34.5
                                                                          EPA-S      640       640           66.3         66.5         33.9
   the valid anticipation window [tEOT −h, tEOT ], we calculate           EPA-M      640       640           67.0         66.2         33.8
   the duration between the first valid prediction tpred and the           VAP      1280       320           20.8         51.0         33.8
   true endpoint tEOT . We report the median of tEOT − tpred              EPA-S     1280      1200           50.3         53.9         33.7
   across the test set.                                                   EPA-M     1280      1120           49.7         52.8         33.2
• Premature Anticipation Rate (PAR): Assesses turn-level                   VAP      1280        80            7.2         28.8         15.4
   stability by tracking activations that occur before the valid an-      EPA-S     1280       480           22.0         34.4         15.1
                                                                          EPA-M     1280       480           22.1         34.3         15.1
   ticipation window (i.e., tpred < tEOT −h for a given h ∈ H).
   These early triggers result in wasteful downstream computa-          Table 1: Metrics for two specific operating points - ERC ≈
   tion. PAR is the percentage of turns containing at least one         33 % and ERC ≈ 15 %. VAP baseline, along with EPA-
   such premature activation.                                           S and EPA-M models are presented at anticipation window
                                                                        h = {640, 1280} ms
• Expected Redundant Computation (ERC): Because
   longer turns present more opportunities for early triggers,          4.5.1. Unmute Framework
   PAR can be biased by turn duration. We define ERC as the
   ratio of actual premature anticipations to the maximum pos-          The Unmute system is a modular, speech-to-speech architec-
   sible anticipations for a turn of length T , approximated by         ture designed for low-latency interaction, utilizing a pipeline of
   ⌈(T −h)/h⌉. Reported as a mean percentage across all turns,          streaming ASR, TTS [31] and LLM. It uses a semantic VAD
   this metric quantifies the expected proportion of discarded          endpointer to determine when to trigger system responses. The
   speculative computation.                                             backend is a Rust-based WebSocket server, while the Python
• Horizon Entry Accuracy (HEA): Evaluates the model’s                   client manages turn-taking logic and interruption handling. We
   temporal precision in triggering exactly at the target horizon       use Gemma 3 4B7 as the LLM, hosted using vLLM [32].
   boundary t = tEOT − h. We frame this as a binary classifi-
   cation task where predictions within a tight two-frame collar        4.5.2. Speculative Execution Strategy
   {t, t + 1} are true positives6 , and predictions in the subse-
   quent [t + 2, tEOT ] range are false positives. This ensures the     The EPA model runs as a parallel streaming module alongside
   model reliably matches the requested anticipation.                   existing components, following a speculative execution logic:
Metrics are computed only for turns exceeding the horizon win-          1. Trigger & Fork: Upon anticipating an endpoint with horizon
dow (T > h). We present the results as latency versus early-               h, the system “forks” the conversation state. It triggers the
trigger curves at different prediction probability thresholds.             LLM to generate a short look-ahead buffer (e.g., 10 tokens)
                                                                           based on the current partial transcript.
4.4. Training Setup                                                     2. Pre-Synthesis (Cache): These tokens are fed to the TTS en-
                                                                           gine to generate audio frames, which are stored in a specula-
Feature Extraction: We use Mimi neural codec [2] (using the
                                                                           tive cache rather than being played out.
first 8 codebooks) as the feature backbone based on prelimi-
nary experiments. Input audio is upsampled to 24 kHz and fea-           3. Verification: Wait for the duration of the horizon h.
tures are extracted at 12.5 Hz with zero lookahead. We freeze              • Success (True Positive): If the Unmute endpointer detects
the backbone parameters, enabling a modular design where the                 a turn completion within this window, the cached audio is
same feature extractor can serve many downstream tasks.                      released to the output buffer immediately, and generation
Model Configuration: The model is a 25M parameter stream-                    continues by using the full transcript, and currently gener-
ing Transformer [29]. It comprises a 6-layer encoder with 4 at-              ated tokens. This effectively masks the processing latency.
tention heads and a feed-forward dimension of 1024. For long-              • Failure (False Positive): If no endpoint is detected by the
form streaming, we apply RoPE [30] and causal masking with                   end of h, the anticipation module resumes. The cache is
a fixed 250-frame left context.                                              discarded when a new endpoint is anticipated.
Optimization: All proposed models are trained on both the
SpokenWOZ and Switchboard datasets. We use a learning rate              When a speculative cache is available at the true endpoint, sys-
of 3 × 10−4 and a batch size of 16. During training, we sam-            tem latency is reduced to the response time of the endpointer
ple fixed-length segments of 500 frames (40 seconds). To ad-            alone, bypassing the ASR, LLM, and TTS generation bottle-
dress class imbalance, we apply a 10:1 weighted loss between            necks.
                         (h)
the positive (horizon, yt = 1) and negative (non-horizon,
  (h)                                                                   4.5.3. Evaluation Protocol
yt = 0) classes. We mask loss for turns shorter than 2 sec-
onds to prevent early predictions. We track the mean accuracy           We adopt the turn-taking evaluation framework from Full-
across horizon and non-horizon frames and apply early stopping          Duplex Bench V1 [33]. We report two primary performance
with a patience of 6 epochs if no improvement is observed.              indicators: Average Latency, as defined by the benchmark8 ,
                                                                        and our proposed Expected Redundant Computation (ERC).
4.5. Speech-to-Speech Integration                                       We omit metrics for other turn-taking capabilities (e.g., inter-
We demonstrate the utility of Endpoint Anticipation by inte-            ruption handling), as our anticipation module is orthogonal to
grating it into the Unmute framework. This section outlines             these functions and preserves the original performance of the
the baseline architecture and our proposed speculative execu-           Unmute framework.
tion strategy to validate latency reduction in real-world settings.
                                                                           7 https://huggingface.co/google/gemma-3-4b-it
   6 The maximum anticipation provided by the selected VAP bins falls     8 https://github.com/DanielLin94144/
within this collar, ensuring a fair baseline comparison.                Full-Duplex-Bench/
                                                                        System             Avg. Latency (ms) ↓ ERC (%) ↓
                                                                        Unmute Baseline            1195                –
                                                                        Unmute + EPA-M              690               28.4
                                                                      Table 2: Latency reduction and computational overhead of
                                                                      EPA-M (h = 960 ms) integration within Unmute framework.
                                                                      5.2. Conversational vs. Task-Oriented Speech
                                                                      Figure 2 compares performance on spontaneous (Switchboard
                                                                      Eval2000) and structured task-oriented (SpokenWOZ) dia-
                                                                      logues. Across both short (h = 960 ms) and long (h =
                                                                      2560 ms) horizons, the model achieves consistently superior an-
                                                                      ticipation on SpokenWOZ, yielding higher MRA for any fixed
                                                                      PAR, and higher HEA for any given ERC budget. This con-
                                                                      firms that the inherent unpredictability of open-domain conver-
Figure 1: Comparison of the VAP baseline and the proposed             sational speech poses a significant challenge, making endpoint
EPA-M model at anticipation horizons, h ∈ {640, 1280} ms,             anticipation currently most viable for structured applications.
on SpokenWOZ test set
                                                                      5.3. Endpoint Anticipation Architecture
                                                                      Table 1 compares the performance of our two proposed ar-
             5. Results and Discussion                                chitectures: EPA-M and EPA-S (Section 3.3). We observe
                                                                      that both models show comparable results, displaying only mi-
5.1. VAP vs EPA                                                       nor deviations across target horizons and evaluation metrics.
                                                                      While this demonstrates that both architectural formulations
Figure 1 evaluates our proposed EPA-M model (Section 3.3)             are well-suited for endpoint anticipation, EPA-M can be flex-
against the adapted VAP baseline. The results indicate a sub-         ibly deployed across varying target horizons without requiring
stantial gap in performance; EPA-M consistently dominates             horizon-specific retraining.
VAP across both trade-off spaces (MRA vs. PAR and HEA
vs. ERC). While VAP’s generalized training enables zero-shot          5.4. System Integration Evaluation
adaptation to various turn-taking tasks, it struggles to produce
precise, fixed-horizon endpoint forecasts.                            Table 2 presents the latency evaluation of the Unmute system
                                                                      integrated with our EPA model (Section 4.5). Results show that
     Furthermore, Table 1 explicitly compares these results           endpoint anticipation significantly reduces average system la-
across two Expected Redundant Computation (ERC) operating             tency. We report a 505 ms reduction using local LLM and TTS
points of interest. For context, an ERC of 33% implies that inte-     components, these gains would likely be higher for API-based
gration with downstream systems will result in 33% redundant          models with greater inherent latency. The residual ≈690 ms
compute due to early, discarded predictions. At the ≈ 33%             latency consists of standard execution on turns with low antic-
ERC operating point, VAP and EPA-M yield comparable PAR.              ipation, semantic VAD trigger delays, and inter-process Web-
However, EPA-M achieves drastically higher HEA and MRA.               Socket communication. The 28.4% ERC indicates that the
For instance, at h = 640 ms, EPA-M achieves a median antici-          volume of discarded speculative computation is restricted to
pation (MRA) of 640 ms compared to VAP’s 160 ms, showing              roughly 28% of the theoretical maximum for these turns. This
that when a specific computational budget is allowed, EPA can         overhead is lowered by efficient inference [32] and sharing the
reliably match the target anticipation horizon, whereas the VAP       feature extractor for anticipation model and downstream tasks.
baseline falls significantly short. Additionally, at a stricter ERC   Ultimately, this trade-off allows cascaded pipelines to support
constraint of ≈ 15%, EPA-M maintains an MRA of 480 ms                 further real-time processing.
with a 22.1% Horizon Entry Accuracy (HEA), whereas VAP
yields negligible anticipation capabilities.                                               6. Conclusion
                                                                      In this work, we introduced endpoint anticipation as a frame-
                                                                      work to minimize turn-taking latency in modular spoken dia-
                                                                      logue systems. By forecasting end-of-turn signals before speech
                                                                      completion, we enable speculative execution of downstream
                                                                      ASR, LLM, and TTS components. We explored two hori-
                                                                      zon modeling strategies—EPA-S and EPA-M—and proposed
                                                                      a set of metrics to quantify the practical trade-off between
                                                                      realized latency savings and computational redundancy. Our
                                                                      multi-target EPA-M model consistently outperforms competi-
                                                                      tive VAP-based baselines across both conversational and task-
                                                                      oriented datasets.
                                                                           Integrated into the Unmute framework, our approach re-
                                                                      duced average latency by 505 ms alongside a 28.4% increase
                                                                      in speculative computation. This effectively masks sequential
                                                                      bottlenecks in cascaded architectures. We will open-source our
Figure 2: Performance across various anticipation horizons,           implementation. Future work will explore semantic edge cases,
h ∈ {960, 2560} ms, for models trained on the SpokenWOZ               such as mid-turn backtracking and late-arriving critical infor-
(task-oriented) and Switchboard (conversational) datasets.            mation.
         7. Generative AI Use Disclosure                                    [17] J. Sakuma, S. Fujie, and T. Kobayashi, “Response timing estima-
                                                                                 tion for spoken dialog systems based on syntactic completeness
The authors used Gemini 3 Pro exclusively for language refine-                   prediction,” in 2022 IEEE Spoken Language Technology Work-
ment. No AI tools were used to generate technical content. The                   shop (SLT). IEEE, 2023, pp. 369–374.
authors assume full responsibility for this manuscript.                     [18] J. Sakuma, S. Fujie, H. Zhao, and T. Kobayashi, “Improving the
                                                                                 response timing estimation for spoken dialogue systems by reduc-
                        8. References                                            ing the effect of speech recognition delay.” in Interspeech, 2023,
                                                                                 pp. 2668–2672.
 [1] S. Arora, K.-W. Chang, C.-M. Chien, Y. Peng, H. Wu, Y. Adi,
     E. Dupoux, H.-Y. Lee, K. Livescu, and S. Watanabe, “On the             [19] S.-Y. Chang, B. Li, D. Rybach, Y. He, W. Li, T. N. Sainath, and
     landscape of spoken language models: A comprehensive survey,”               T. Strohman, “Low latency speech recognition using end-to-end
     arXiv preprint arXiv:2504.08528, 2025.                                      prefetching.” in Interspeech, 2020, pp. 1962–1966.

 [2] A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou,   [20] O. Zink, Y. Higuchi, C. Mullov, A. Waibel, and T. Kobayashi,
     E. Grave, and N. Zeghidour, “Moshi: a speech-text foundation                “Predictive speech recognition and end-of-utterance detection to-
     model for real-time dialogue,” arXiv preprint arXiv:2410.00037,             wards spoken dialog systems,” arXiv preprint arXiv:2409.19990,
     2024.                                                                       2024.

 [3] K. Hu, E. Hosseini-Asl, C. Chen, E. Casanova, S. Ghosh,                [21] E. Ekstedt and G. Skantze, “Voice activity projection: Self-
     P. Żelasko, Z. Chen, J. Li, J. Balam, and B. Ginsburg, “Effi-              supervised learning of turn-taking events,” in Interspeech, 2022,
     cient and Direct Duplex Modeling for Speech-to-Speech Lan-                  pp. 5190–5194.
     guage Model,” in Interspeech, 2025, pp. 2715–2719.                     [22] K. Inoue, B. Jiang, E. Ekstedt, T. Kawahara, and G. Skantze,
 [4] R. Roy, J. Raiman, S. gil Lee, T.-D. Ene, R. Kirby, S. Kim,                 “Multilingual turn-taking prediction using voice activity projec-
     J. Kim, and B. Catanzaro, “Personaplex: Voice and role control              tion,” in Proceedings of the 2024 Joint International Conference
     for full duplex conversational speech models,” 2026. [Online].              on Computational Linguistics, Language Resources and Evalua-
     Available: https://arxiv.org/abs/2602.06053                                 tion (LREC-COLING 2024), N. Calzolari, M.-Y. Kan, V. Hoste,
                                                                                 A. Lenci, S. Sakti, and N. Xue, Eds. Torino, Italia: ELRA
 [5] T. Likhomanenko, L. Carlson, R. H. Bai, Z. Gu, H. Tran,                     and ICCL, May 2024, pp. 11 873–11 883. [Online]. Available:
     Z. Aldeneh, Y. Zhang, R. Zhang, H. Zheng, and N. Jaitly,                    https://aclanthology.org/2024.lrec-main.1036/
     “Chipchat: Low-latency cascaded conversational agent in mlx,”
     arXiv preprint arXiv:2509.00078, 2025.                                 [23] Y.-J. Shih, D. Raj, C. Wu, W. Zhou, S. Bong, Y. Gaur, J. Ma-
                                                                                 hadeokar, O. Kalinli, and M. Seltzer, “Can speech llms think while
 [6] W. Yu, S. Wang, X. Yang, X. Chen, X. Tian, J. Zhang, G. Sun,                listening?” arXiv preprint arXiv:2510.07497, 2025.
     L. Lu, Y. Wang, and C. Zhang, “Salmonn-omni: A standalone
     speech llm without codec injection for full-duplex conversation,”      [24] S. Arora, J. Tian, H. Futami, J. weon Jung, J. Shi, Y. Kashi-
     NeurIPS, 2025. [Online]. Available: arXiv:2505.17060                        wagi, E. Tsunoo, and S. Watanabe, “Chain-of-Thought Training
                                                                                 for Open E2E Spoken Dialogue Systems,” in Interspeech, 2025,
 [7] S. Wang, W. Yu, X. Chen, X. Tian, J. Zhang, L. Lu, and C. Zhang,            pp. 4833–4837.
     “End-to-end listen, look, speak and act,” ICLR, 2026. [Online].
     Available: arXiv:2510.16756                                            [25] S. Arora, H. Khan, K. Sun, X. L. Dong, S. Choudhary, S. Moon,
                                                                                 X. Zhang, A. Sagar, S. T. Appini, K. Patnaik et al., “Stream rag:
 [8] A. Zeng, Z. Du, M. Liu, K. Wang, S. Jiang, L. Zhao, Y. Dong, and            Instant and accurate spoken dialogue systems with streaming tool
     J. Tang, “Glm-4-voice: Towards intelligent and human-like end-              usage,” arXiv preprint arXiv:2510.02044, 2025.
     to-end spoken chatbot,” arXiv preprint arXiv:2412.02612, 2024.
                                                                            [26] S. Si, W. Ma, H. Gao, Y. Wu, T.-E. Lin, Y. Dai, H. Li, R. Yan,
 [9] M. Züfle, O. Klejch, N. Sanders, J. Niehues, A. Birch, and T. K.           F. Huang, and Y. Li, “Spokenwoz: A large-scale speech-text
     Lam, “F-actor: Controllable conversational behaviour in full-               benchmark for spoken task-oriented dialogue agents,” NeurIPS,
     duplex models,” arXiv preprint arXiv:2601.11329, 2026.                      vol. 36, pp. 39 088–39 118, 2023.
[10] S.-Y. Chang, B. Li, T. N. Sainath, G. Simko, and C. Parada,            [27] J. J. Godfrey, E. C. Holliman, and J. McDaniel, “Switchboard:
     “Endpoint Detection Using Grid Long Short-Term Memory Net-                  Telephone speech corpus for research and development,” in
     works for Streaming Speech Recognition,” in Interspeech, 2017,              ICASSP, vol. 1. IEEE, 1992, pp. 517–520.
     pp. 3812–3816.
                                                                            [28] S. Team, “Silero vad: pre-trained enterprise-grade voice activity
[11] K. Inoue, B. Jiang, E. Ekstedt, T. Kawahara, and G. Skantze,                detector (vad), number detector and language classifier,” https://
     “Real-time and continuous turn-taking prediction using voice ac-            github.com/snakers4/silero-vad, 2024.
     tivity projection,” arXiv preprint arXiv:2401.04868, 2024.
                                                                            [29] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N.
[12] S. Udupa, S. Watanabe, P. Schwarz, and J. Cernocky, “Streaming              Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,”
     endpointer for spoken dialogue using neural audio codecs                    NeurIPS, vol. 30, 2017.
     and label-delayed training,” ASRU, 2025. [Online]. Available:
     arXiv:2506.07081                                                       [30] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu, “Roformer:
                                                                                 Enhanced transformer with rotary position embedding,” Neuro-
[13] G. Li, C. Wang, H. Xue, S. Wang, D. Gao, Z. Zhang, Y. Lin,                  computing, vol. 568, p. 127063, 2024.
     W. Li, L. Xiao, Z. Fu et al., “Easy turn: Integrating acoustic and
     linguistic modalities for robust turn-taking in full-duplex spoken     [31] N. Zeghidour, E. Kharitonov, M. Orsini, V. Volhejn,
     dialogue systems,” arXiv preprint arXiv:2509.23938, 2025.                   G. de Marmiesse, E. Grave, P. Pérez, L. Mazaré, and A. Défossez,
                                                                                 “Streaming sequence-to-sequence learning with delayed streams
[14] T. Stivers, N. J. Enfield, P. Brown, C. Englert, M. Hayashi,                modeling,” arXiv preprint arXiv:2509.08753, 2025.
     T. Heinemann, G. Hoymann, F. Rossano, J. P. De Ruiter, K.-E.
     Yoon et al., “Universals and cultural variation in turn-taking in      [32] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E.
     conversation,” Proceedings of the National Academy of Sciences,             Gonzalez, H. Zhang, and I. Stoica, “Efficient memory manage-
     vol. 106, no. 26, pp. 10 587–10 592, 2009.                                  ment for large language model serving with pagedattention,” in
                                                                                 Proceedings of the ACM SIGOPS 29th Symposium on Operating
[15] S. Kuroki, Y. Kubo, T. Akiba, and Y. Tang, “Kame: Tandem ar-                Systems Principles, 2023.
     chitecture for enhancing knowledge in real-time speech-to-speech
     conversational ai,” arXiv preprint arXiv:2510.02327, 2025.             [33] G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu,
                                                                                 and H.-y. Lee, “Full-duplex-bench: A benchmark to evaluate full-
[16] S. C. Levinson and F. Torreira, “Timing in turn-taking and its im-          duplex spoken dialogue models on turn-taking capabilities,” arXiv
     plications for processing models of language,” Frontiers in psy-            preprint arXiv:2503.04721, 2025.
     chology, vol. 6, p. 136034, 2015.

