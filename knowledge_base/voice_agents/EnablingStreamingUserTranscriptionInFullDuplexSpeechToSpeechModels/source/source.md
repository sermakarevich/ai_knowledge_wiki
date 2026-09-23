# Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models
Source: https://arxiv.org/abs/2609.15759
Kind: pdf
Fetched: 2026-09-22T09:29:48.886019+00:00
Tool: pdftotext

                                                      Enabling Streaming User Transcription in
                                                       Full-Duplex Speech-to-Speech Models
                                                                      Ke Hu, Nourchene Ferchichi, Edresson Casanova, Ankita Pasad,
                                                                    Elena Rastorgueva, Chen Chen, Nithin Rao Koluguri, Piotr Zelasko,
                                                                          Yifan Peng, Hainan Xu, Zhehuai Chen, Boris Ginsburg
                                                                                                      NVIDIA
                                                                                                kevinhu@nvidia.com


                                            Abstract—Full-duplex speech-to-speech (S2S) models enable         detection and turn-taking modules, but fundamentally rely
                                         natural conversational AI by allowing simultaneous listening         on explicit turn detection rather than simultaneous process-




arXiv:2609.15759v1 [cs.CL] 14 Sep 2026
                                         and speaking. However, these models typically lack inherent          ing. Recently, full-duplex S2S models have emerged that
                                         user speech transcription, which is essential for applications
                                         such as conversation logging, accessibility features, and quality    enable simultaneous listening and speaking. Moshi [27] and
                                         monitoring. In this work, we propose an efficient method to          PersonaPlex [28] are full-duplex conversational models that
                                         add streaming ASR capabilities to an existing duplex S2S model       jointly model both user and agent audio streams with depth-
                                         by introducing a lightweight ASR head in parallel to the agent       based attention mechanisms, but require extensive speech-text
                                         text head. Our approach requires minimal additional parameters       pretraining from scratch and do not provide streaming user
                                         and no significant architectural changes to the base S2S model,
                                         enabling real-time user transcription while preserving full-duplex   transcription capabilities. Other approaches like SyncLLM
                                         conversational capabilities including turn-taking and barge-in       [29] and OmniFlatten [30] also achieve full-duplex conversa-
                                         handling. Experimental results demonstrate that our method           tion through various architectural designs but share the same
                                         achieves streaming average WER of 10.21% on the HuggingFace          limitation of lacking explicit user transcription outputs. Recent
                                         Open ASR Leaderboard within the duplex S2S framework.                work has explored augmenting duplex speech LLMs with
                                         Additionally, we show that the same architecture trained as a
                                         standalone streaming ASR model achieves competitive results          chain-of-thought reasoning by interleaving ASR and reasoning
                                         (7.73% WER) compared to current SOTA models. We will                 tokens within a single text monologue stream [31], though
                                         open-source our training and inference code to facilitate further    this conflates transcription and reasoning into a shared channel
                                         research in joint streaming ASR and S2S modeling.                    rather than treating ASR as a dedicated output.
                                                                                                                 A recent duplex S2S architecture [32], [33] demonstrated
                                                               I. I NTRODUCTION                               that any text LLM can be converted into a full-duplex conver-
                                            Streaming automatic speech recognition (ASR) is fun-              sational agent without requiring extensive speech-text pretrain-
                                         damental to real-time human-computer interaction, enabling           ing, by using a pretrained streaming encoder for user input and
                                         applications such as live captioning, voice assistants, and          parallel text and audio heads for agent output. However, this
                                         conversational AI. As large language models (LLMs) [1]–[10]          architecture does not provide explicit user speech transcription,
                                         have transformed natural language processing, there is growing       which is valuable for downstream applications such as conver-
                                         interest in extending these capabilities to speech or multimodal     sation logging, accessibility features, and quality monitoring.
                                         inputs. Recent work has explored adapting LLMs to process               In this work, we build on this duplex S2S architecture by
                                         speech or multimodal inputs for various tasks [3], [11]–[17].        introducing a streaming ASR head in parallel to the agent
                                         A fully capable conversational speech system benefits from           text head, enabling the model to perform continuous speech
                                         not only agent response generation but also streaming user           recognition while maintaining full-duplex conversational ca-
                                         transcription capabilities alongside features such as turn-taking    pabilities. Our approach enables frame-level streaming ASR
                                         and barge-in handling.                                               within a decoder-only LLM architecture, allowing simulta-
                                            There have been a number of works on incorporating speech         neous speech recognition and agent response generation. We
                                         inputs to LLMs. Traditional spoken dialogue systems cascade          further demonstrate that the same architecture can be trained
                                         ASR, LLM, and TTS modules [18], and while they natu-                 as a standalone streaming ASR model, achieving competitive
                                         rally provide user transcriptions, this approach has potentially     results on standard benchmarks.
                                         higher latency and makes it difficult to incorporate paralinguis-       Our main contributions are as follows:
                                         tic information in S2S modeling. This has motivated research            • We propose an efficient method to add streaming ASR
                                         into end-to-end speech-to-speech (S2S) models. Initial efforts             capabilities to a full-duplex S2S model, requiring minimal
                                         focused on half-duplex, turn-based interactions [13], [16],                additional parameters while preserving turn-taking and
                                         [17], [19]–[23], which still fail to capture the interactive               barge-in performance.
                                         nature of real dialogue. Some systems like gpt-realtime [3],            • We demonstrate that the S2S model achieves stream-
                                         [24], Freeze-Omni [16], FireRedChat [25], and FlexDuo [26]                 ing ASR capability, enabling real-time user transcription
                                         achieve low-latency interactions through external voice activity           alongside agent response generation.
  • We show that the same architecture trained as a stan-                      Agent speech
    dalone ASR model achieves competitive results on the
    HuggingFace Open ASR Leaderboard [34].                                  Streaming TTS
  • We will open-source our training and inference code to              Agent text                                         User text
    facilitate reproducibility and enable further research in          <turn-1>    <silence>     <turn-2>      <silence>   <turn-1>      <silence>
    joint streaming ASR and S2S modeling.
                                                                                  Text head                           ASR head
                     II. R ELATED WORK
   Recent advances in streaming ASR have led to several
                                                                                          Decoder-only LLM
notable systems. Encoder-based models such as FastCon-
former [35], [36] and Parakeet [37] achieve state of the
                                                                                                     Pooling
art performance using conformer blocks with cache-based
inference, but it is unclear how to incorporate them into a full-                    <turn-1>        <silence>         <turn-2>   Agent text
duplex S2S model. Kyutai STT [38] achieves strong streaming                          <silence>        <turn-1>        <silence>       User text
ASR performance but lacks the conversational capabilities                            <silence>        <turn-1>        <silence>
required for a full-duplex framework. LLM-based approaches
such as Qwen-ASR [39] leverage the language understanding
                                                                                      Streaming Speech Encoder
of large models for speech recognition, but rely on chunk-
based processing where minimum latency is determined by
chunk size, making integration with continuously streaming
S2S models prohibitively complex.                                                                                                       User speech
   Separately, significant progress has been made in full-duplex
spoken dialogue modeling. Moshi [27] and PersonaPlex [28]
                                                                                                 Barge-in (user)
enable simultaneous listening and speaking by jointly model-                                     Turn taking (agent)
ing user and agent audio streams, but require extensive speech-
text pretraining from scratch and do not provide streaming user
transcription. Systems like Freeze-Omni [16], FireRedChat           Fig. 1. Our architecture for adding a streaming ASR head to the speech-to-
[25], and FlexDuo [26] reduce interaction latency through           text part of the S2S duplex model. The model takes continuous user audio
                                                                    embeddings, previous ASR and agent text tokens as inputs, and outputs user
external voice activity detection and turn-taking modules, but      ASR and agent text in parallel.
fundamentally rely on explicit turn detection rather than truly
simultaneous processing. SALM-Duplex [32] and its system
demonstration [33] convert any pretrained text LLM into a           user and agent text tokens are autoregressively fed back as
full-duplex agent without requiring speech pretraining, but         inputs to the backbone LLM.
similarly lack explicit user transcription output. A related
                                                                       The model is trained with multi-channel next token pre-
line of work explores augmenting duplex speech LLMs with
                                                                    diction, simultaneously generating user text and agent text
transcription by interleaving ASR and reasoning tokens within
                                                                    through parallel heads. The user and agent embeddings are
a single text stream [31], but this conflates transcription and
                                                                    time-aligned and added before being passed to the decoder-
reasoning into a shared channel rather than treating ASR
                                                                    only LLM, together with input user speech encoding. We use
as a dedicated parallel output. Our work addresses this by
                                                                    equal loss for user and agent text prediction. Unlike streaming
adding a dedicated streaming ASR head to the SALM-Duplex
                                                                    ASR, agent text is predicted without word-level alignment to
architecture, enabling real-time user transcription alongside
                                                                    give the user a preview of the agent response before speech
full-duplex conversation capabilities.
                                                                    generation finishes. Our agent text with turn taking information
                III. M ODEL A RCHITECTURE                           is then fed to a streaming TTS [41] to generate agent speech.
                                                                    In this work, to incorporate user speech transcription, we focus
A. Full-Duplex S2S Model                                            on modifying the speech-to-text part of the architecture.
   Our work builds upon the duplex speech-to-speech (S2S)              In this work, our training includes a pretraining stage
architecture proposed in [32], [33] by adding a streaming ASR       followed by supervised fine-tuning (SFT). During pretraining,
head. As shown in Figure 1, our extended model processes            the model is trained on interleaved speech-to-text conversation
three input streams: user speech, user transcript, and agent        data. In the SFT stage, we fine-tune the model on a mixture of
text. User speech is first encoded by a 600M parameter              diverse data sources including multi-turn conversational data
Parakeet streaming speech encoder [37], generating continuous       and ASR transcription data. To improve robustness to diverse
embeddings at an 80ms frame rate. The backbone LLM is               acoustic conditions, we apply background noise augmentation
initialized from NVIDIA Nemotron-Nano-9B-v2-Base [40], a            during the SFT stage with 0.5 probability, where additive noise
9 billion parameter decoder-only language model optimized           is randomly selected from a collection of over 60,000 noise
for reasoning and instruction-following tasks. The generated        files. The signal-to-noise ratio (SNR) is randomly sampled in
a wide range to enable the model to handle various acoustic       distinct end-of-word token instead of the pad token at word
environments.                                                     boundaries, but did not observe a significant difference in
                                                                  performance.
B. Streaming ASR Head
   We augment the duplex S2S architecture by introducing a                             IV. E XPERIMENTS
streaming ASR module in parallel to the existing agent text       A. Data
head. This module consists of both a separate embedding layer        Our training proceeds in two stages: pretraining and super-
and a prediction head for user transcription. Both layers are     vised fine-tuning (SFT). In the pretraining stage, the model
initialized from the original corresponding LLM backbone          is trained on interleaved speech-to-text data to learn the
layers. As illustrated in Figure 1, the ASR head takes the        fundamental knowledge of user and agent conversations. In
LLM’s hidden states and predicts user transcription tokens in     the SFT stage, we train on a mixture of diverse data sources
a streaming fashion, while the separate embedding layer allows    including: interleaved S2S data, text-to-text conversations,
the model to learn user text representations independently        multi-turn conversational SFT data, multiple-choice question
from the agent text embeddings. This design enables real-time     answering, single-turn speech instruction data, and ASR train-
speech recognition concurrent with agent response generation.     ing data. Background noise augmentation is applied during
   The streaming ASR head shares the same LLM backbone as         the SFT stage only. The multi-turn conversational SFT data is
the agent text head, allowing it to leverage the contextual un-   synthesized following the approach described in [32]. The text-
derstanding from the conversation flow. Only a single decoding    to-text data helps maintain the language modeling capabilities
pass is needed to jointly produce both user and agent texts.      of the backbone LLM. The ASR data provides additional
During training, we add an ASR loss term using next token         supervision for the streaming ASR head and consists of two
prediction that supervises the user transcription output along-   types of data: Open-source and publicly available ASR training
side the agent text loss. This joint training enables the model   data including LibriSpeech [43], VoxPopuli [44], Common
to perform streaming ASR while maintaining its full-duplex        Voice [45], VCTK [46], SPGISpeech [47], etc, as well as
conversational capabilities. For the standalone streaming ASR     our in-house training data. We use the English portions of
configuration, we train the model without the agent text heads,   the ASR training data, totaling 16k hours. The signal-to-noise
focusing solely on the streaming speech recognition task.         ratio (SNR) is randomly sampled between -30 dB and 60 dB
                                                                  to enable the model to handle various acoustic environments.
C. On-the-fly (OTF) Forced Alignment
                                                                     For the standalone streaming ASR experiments, we ad-
   To enable streaming ASR training, we require frame-level       ditionally leverage English data from Granary [48], which
alignment between user speech and transcription text. We use      combines open-source Creative Commons speech corpora in-
the torchaudio CTC-based forced alignment API with the            cluding YODAS (YouTube-Oriented Dataset for Audio and
MMS-FA acoustic model [42] for on-the-fly (OTF) forced            Speech) and YouTube-Commons (YTC). The dataset enhances
alignment during training. Given user speech audio and tran-      quality through a pseudo-labeling pipeline with segmentation,
scripts, the forced aligner produces word-level timestamps that   two-pass ASR inference, and hallucination filtering.
are used to align text with speech. We then use the timestamps       We evaluate our models on two types of test sets. For
to align text tokens with speech frames at the start of each      streaming ASR evaluation, we use benchmarks from the
word.                                                             HuggingFace Open ASR Leaderboard [34], including
   To improve streaming ASR quality, we introduce a user text     LibriSpeech          test-clean         and     test-other,
delay du that shifts the transcription targets forward in time    SPGISpeech, GigaSpeech, Earnings22, AMI,
relative to the speech frames. On the other hand, to facilitate   TED-LIUM, and VoxPopuli. For turn-taking and
agent turn taking, we apply a separate agent text delay da to     conversational evaluation, we use Full-Duplex-Bench
help the agent learn reliable timing to respond. The delays du    V1 (FDB-v1) [49] and an internal test set of interactions
and da are hyperparameters that control the trade-off between     with the model in real-world setups and containing around 60
streaming ASR latency and turn taking accuracy.                   multi-turn conversations covering diverse topics, with each
   For word-level alignment, we experimented with both left       conversation containing roughly 4 turns. The recordings were
alignment (text tokens aligned to the start of each word)         made in various acoustic environments using different devices
and right alignment (text tokens aligned to the end of each       and headsets to ensure robustness evaluation. To create the
word). We found that left alignment yields better performance,    dataset, conversation scripts were first generated using a text
presumably because speech onset is easier to detect in this       LLM, then users recorded their turns while simulating natural
setup. Between consecutive words, we use pad tokens to fill       conversation flow by allowing pauses for agent responses.
the frames where no text prediction is required. For exam-        Multiple conversations were recorded per topic to ensure
ple, the phrase “hello world” with left-aligned tokens would      diversity.
produce the target sequence like: “ hel lo <pad> <pad>
 world <pad> <pad>”, where the underscore denotes word            B. Turn Taking and Streaming ASR
boundaries and <pad> tokens fill the remaining frames within        We evaluate the streaming ASR performance of our model
each word’s duration. We also experimented with using a           when integrated into the full-duplex S2S framework. For all
                                                                     TABLE I
                                                  S TREAMING ASR RESULTS (WER %, ↓) IN S2S MODEL .

              Model        LS-clean        LS-other           SPGI            Giga     Earn22     AMI      Tedlium     Voxpop      Avg

              Ours           3.9               8.48            4.95           14.22    16.87      18.36      5.98        8.9      10.21


                               TABLE II                                               our subjective experience but one can adjust them and we
T URN - TAKING AND BARGE - IN EVALUATION . P RECISION AND RECALL ARE                  also compute turn taking latency as a complementary metric.
                   IN %, AND LATENCIES ARE IN MS .
                                                                                      Latency is the average time delay between user speech ending
                                 Turn-taking                  Barge-in                and agent response starting for correctly matched turns. For
                                                                                      barge-in evaluation, a barge-in event is detected when the
     Model               Pr ↑      Rec ↑       Lat ↓    Acc ↑         Lat ↓
                                                                                      user starts speaking while the agent is still speaking. Barge-
     Baseline (noASR)     86.1      96.9       410        100         393
     Ours                  90        95        431        100         374
                                                                                      in accuracy is the percentage of barge-in events where the
                                                                                      agent successfully stops speaking within 1.5s after the user
                               TABLE III                                              interruption. Barge-in latency is the average time for the agent
                      I NTELLIGENCE EVALUATION .                                      to stop after a successful barge-in.

  Model                 OpenbookQA (%) ↑          AE (/5) ↑       CE (/5) ↑              As shown in Table II, we have achieved competitive turn
                                                                                      taking performance (90% precision and 95% recall, with
  Moshi [27], [50]               26.15                 2.01            1.60
  Qwen2-Audio [50]               67.91                 4.11            3.77           431ms latency) based on our internal test set, and 100%
  Baseline (noASR)               66.59                 3.71            3.24
                                                                                      barge-in accuracy with 374ms barge-in latency. As shown in
  Ours                           69.01                 3.83            3.11           Table III, our model also achieves an AlpacaEval (AE) score
                                                                                      of 3.83 and a CommonEval (CE) score of 3.11 (out of 5), with
                                                                                      OpenbookQA accuracy of 69.01%. This represents a substan-
experiments, we use a user text delay of du = 1.2s and                                tial improvement over Moshi [27]. Compared to Qwen2-Audio
an agent text delay of da = 0.16s. The choice of these                                [50], a turn-based audio LLM, our model achieves slightly
hyperparameters is to achieve a balance between reasonable                            higher OpenbookQA accuracy (69.01% vs. 67.91%) but shows
ASR performance and immediate agent response. Tables I, II,                           a gap in CommonEval (3.11 vs. 3.77).
and IV present the complete evaluation results for our duplex
S2S model with the integrated streaming ASR head, including                              Table IV shows the FDB-v1 [49] results comparing our
streaming ASR performance on the HuggingFace Open ASR                                 model against Moshi [27]. FDB-v1 evaluates three key interac-
Leaderboard [34], turn-taking metrics, intelligence scores, and                       tive behaviors: smooth turn-taking, user interruption handling,
FDB-v1 [49] results.                                                                  and pause handling (we use the Candor set). Our model
   As shown in Table I, our model achieves 10.21% av-                                 achieves better smooth turn-taking (TOR 96.12% vs. 94%)
erage WER while simultaneously supporting agent re-                                   and worse user interruption TOR (94% vs. 100%) to Moshi,
sponse generation and full-duplex conversation. This is                               but a notably higher GPT score (3.99 vs. 0.77), indicating
better than the FastConformer-80ms (11.71%) and                                       significantly better response quality upon interruption. For
FastConformer-multi (11.27%) models (Table V),                                        pause handling, our model produces fewer false takeovers
which are dedicated streaming ASR models, demonstrating                               (TOR 44.4% vs. 98%). The higher smooth turn-taking latency
that our approach achieves competitive ASR performance even                           of our model (477ms vs. 265ms) reflects a trade-off for this
within the duplex S2S framework.                                                      improved pause handling. We note our evaluation is based
                                                                                      on the agent text outputs and agent start and end timestamps
   For turn-taking, we report precision (Pr), recall (Rec), and
                                                                                      are based on explicit agent <bos> and <eos> tokens in
latency (Lat.) for regular turn-taking, as well as barge-in
                                                                                      modeling.
accuracy (Acc) and barge-in latency (Lat.) in the Barge-in
column using our internal test set. For intelligence, we report                          We have also compared the proposed model to a baseline
OpenbookQA accuracy, AlpacaEval (AE), and CommonEval                                  model without streaming ASR head for turn taking (Table II),
(CE) scores from VoiceBench [50]. The turn-taking metrics                             Intelligence (Table III) and FDB-v1 (Table IV), respectively.
are computed by extracting user speech segments using voice                           Overall, adding streaming ASR head does not signifcantly
activity detection (VAD) [52], while agent response segments                          change the turn taking results compared to the baseline model
are derived from the model’s predicted text with <bos> and                            (i.e., no ASR) as shown Table II and IV, except increasing the
<eos> timestamps. Precision measures the proportion of                                latency of the smooth turn taking set in FDB-v1. However, in a
agent turns correctly following user turns, where an agent                            multi-turn conversation the turn taking latency remains similar
turn is a true positive if it starts within 1s before to 1.5s                         (Table II). On the other hand, adding the ASR head leads to
after a user segment ends. Recall measures the proportion of                          the improvement in OpenbookQA (Table III) from 66.59% to
user utterances that receive an agent response starting within                        69.01%, which indicates that the model may benefit from the
1.5s. These thresholds are chosen empirically to align with                           text modality to answer questions.
                                                                 TABLE IV
                     FDB- V 1 [49] EVALUATION . TOR S ARE IN %, LATENCIES ARE IN MS , AND THE GPT SCORE IS OUT OF 5.

                                                            Smooth TT                    User Interruption            Pause
                                Model                     TOR ↑      Lat ↓        TOR ↑          GPT ↑       Lat      TOR ↓
                                Moshi [27], [49]           94            265          100        0.77        257       98
                                Baseline (noASR)          95.15          257          92.5       4.38        369      51.4
                                Ours                      96.12          477           94        3.99        355      44.4


                                                         TABLE V
              S TANDALONE STREAMING ASR RESULTS (WER %, ↓). N UMBERS IN PARENTHESES INDICATE LATENCY IN TRAINING .

           Model                               LS-clean       LS-other         SPGI      Giga     Earn22      AMI      Tedlium   Voxpop    Avg
           FastConformer-80ms [35]                 2.57           6.31         6.16      14.92     21.03      28.37     6.17      8.12    11.71
           FastConformer-multi (1.12s) [36]        2.19           5.32         5.76      14.47     21.45      27.85     5.70      7.42    11.27
           Nemotron-Speech-0.6B (1.12s) [51]       2.31           4.75         2.62      11.45     12.48      11.58     4.50      7.57     7.16
           Qwen3-ASR-1.7B (2s) [14], [34]          1.63            3.4         2.84       8.74     10.25      10.56     2.28      6.35     5.76
           Qwen3-ASR-0.6B (2s) [14], [34]          2.13           4.45         3.03       9.14     11.06      11.66     2.85      7.07     6.42
           Kyutai STT-2.6B (2.5s) [34], [38]       1.70           4.32         2.03       9.81     10.99      12.17     3.35      6.79     6.40
           Ours (1.6s)                             2.68           6.04         4.87      11.64     15.01      14.20     4.61      8.70    8.47
             + YODAS and YTC [48]                  2.48           6.03         3.66      11.21     13.56      12.97     4.03      7.91    7.73



C. Standalone Streaming ASR                                                      significantly modifying the base S2S architecture. The duplex
   We also train a standalone streaming ASR model using the                      S2S model with integrated ASR achieves 10.21% average
same architecture but without the agent text heads, focusing                     WER while maintaining competitive turn-taking, and barge-in
solely on the streaming speech recognition task. Table V com-                    performance. This enables applications such as conversation
pares our standalone model against state-of-the-art streaming                    logging and accessibility features. Furthermore, we showed
ASR systems on the HuggingFace Open ASR Leaderboard                              that the same architecture trained as a standalone streaming
[34].                                                                            ASR model achieves 7.73% WER on the HuggingFace Open
                                                                                 ASR Leaderboard.
   Our base model with 1.6s streaming delay achieves 8.47%
average WER on the HuggingFace Open ASR Leaderboard,                                        VI. G ENERATIVE AI U SE D ISCLOSURE
and adding YODAS and YTC data from Granary [48] im-                                 Claude Opus 4.8 and Codex with GPT-5.5 are used to format
proves this to 7.73%. Starting from this model, we have also                     tables and references and fix grammatical errors throughout all
done ablations regarding the streaming latency and achieved                      sections of the paper.
7.99 % average WER with a streaming latency of 1.2s. Regard-
ing the LLM backbone, we have also tried a smaller backbone:                                                       R EFERENCES
Qwen 2.5-1.5B-Instruct [53], and achieved an average WER                          [1] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
                                                                                      A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language models
of 8.64%.                                                                             are few-shot learners,” arXiv preprint arXiv:2005.14165, 2020.
   We note that there are still gaps comparing our model to                       [2] A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman,
the SOTA streaming ASR models. For example, the remaining                             A. Mathur, A. Schelten, A. Yang, A. Fan et al., “The llama 3 herd of
                                                                                      models,” arXiv preprint arXiv:2407.21783, 2024.
gap compared to Nemotron-Speech-0.6B (7.16% vs 7.73%) is                          [3] OpenAI, “Gpt-4o system card,” arXiv preprint arXiv:2410.21276, 2024.
likely due to utilizing subsets of the Granary dataset. We note                   [4] Q. Team, “Qwen3 technical report,” arXiv preprint arXiv:2505.09388,
that, at the time of training, some portions of the Granary data                      2025.
                                                                                  [5] Anthropic, “The claude 3 model family: Opus, sonnet, haiku,” 2024,
were not available in our training pipeline, and we plan to                           model Card. [Online]. Available: https://www-cdn.anthropic.com/
incorporate the full dataset in future work. Compared to other                        de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model Card Claude
SOTA models such as Qwen3-ASR and Kyutai STT (Table                                   3.pdf
                                                                                  [6] DeepSeek-AI, D. Guo, D. Qin, Z. Fan, Z. Liu, X. Ruan, W. Liang,
V), our model achieves a lower streaming latency, though at                           Y. Shi, Q. Guo, Z. Shao et al., “Deepseek-v3.2: Pushing the frontier of
the cost of higher WER. A direct comparison is also difficult                         open large language models,” arXiv preprint arXiv:2512.02556, 2025.
as the training data of these models differs from ours and is                     [7] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma,
                                                                                      P. Wang, X. Bi et al., “Deepseek-r1: Incentivizing reasoning capability
not fully disclosed.                                                                  in llms via reinforcement learning,” arXiv preprint arXiv:2501.12948,
                                                                                      2025.
                       V. C ONCLUSIONS                                            [8] MiniMax, S. Deng, Q. Yao, J. Jia, X. Zhang, J. Wang, H. Wu, X. Han,
                                                                                      Y. Zhang, W. Xu et al., “Minimax-01: Scaling foundation models with
   We presented an efficient method to add streaming ASR                              lightning attention,” arXiv preprint arXiv:2501.08313, 2025.
capabilities to a full-duplex speech-to-speech model. By in-                      [9] S. Muralidharan, S. T. Sreenivas, R. Joshi, M. Chochowski, M. Patwary,
                                                                                      M. Shoeybi, B. Catanzaro, J. Kautz, and P. Molchanov, “Llm pruning
troducing a lightweight ASR head in parallel to the agent text                        and distillation in practice: The minitron approach,” arXiv preprint
head, our approach enables real-time user transcription without                       arXiv:2407.14679, 2024.
[10] A. Bakhtin, S. Casper, M. Chochowski, J. Du, V. Feinberg, D. Ganguli,      [32] K. Hu, E. Hosseini-Asl, C. Chen, E. Casanova, S. Ghosh, P. Żelasko,
     R. Joshi, J. Kautz, A. Korneev, A. Kosson et al., “Nvidia nemotron              Z. Chen, J. Li, J. Balam, and B. Ginsburg, “Salm-duplex: Efficient and
     nano 2: An accurate and efficient hybrid mamba-transformer reasoning            direct duplex modeling for speech-to-speech language model,” arXiv
     model,” arXiv preprint arXiv:2508.14444, 2025.                                  preprint arXiv:2505.15670, 2025.
[11] Z. Chen, H. Huang, A. Andrusenko et al., “Salm: Speech-augmented           [33] E. Casanova, C. Chen, K. Hu, A. Pasad, E. Rastorgueva, S. L.
     language model with in-context learning for speech recognition and              Narasimhan, S. Deng, E. Hosseini-Asl, P. Żelasko, V. Mendelev,
     translation,” in ICASSP. IEEE, 2024, pp. 13 521–13 525.                         S. Ghosh, Y. Peng, Z. Chen, J. Li, J. Balam, V. Lavrukhin, and B. Gins-
[12] G. Team, R. Anil, S. Borgeaud, J.-B. Casas, N. Fiedel, K. Georgiou,             burg, “Open full-duplex voice agent with speech-to-speech language
     A. Gulati, S. S. Gu, H. Hu, D. Kalashnikov et al., “Gemini 2.5: Pushing         model,” in ASRU, 2025.
     the frontier with advanced reasoning, multimodality, long context, and     [34] H. Face, “Open asr leaderboard,” 2024, hugging Face Space. [Online].
     next generation agentic capabilities,” arXiv preprint arXiv:2507.06261,         Available: https://huggingface.co/spaces/hf-audio/open asr leaderboard
     2025.                                                                      [35] NVIDIA, “STT En FastConformer Hybrid Transducer-CTC Large
[13] Q. Team, K. Xu, Z. Zhang, X. Wang, Y. Dong, Z. Chen, J. Zhou, J. Lin,           Streaming 80ms,” 2023, version 1.20.0, Released June 22, 2023.
     A. Yang, Y. Chu et al., “Qwen3-omni technical report,” arXiv preprint           [Online]. Available: https://catalog.ngc.nvidia.com/orgs/nvidia/teams/
     arXiv:2509.17765, 2025.                                                         nemo/models/stt en fastconformer hybrid large streaming 80ms
[14] Q. Team, “Qwen3-asr technical report,” arXiv preprint                      [36] ——, “STT En FastConformer Hybrid Transducer-CTC Large
     arXiv:2601.21337, 2026.                                                         Streaming Multi,” 2023, hugging Face Model Hub. [Online].
[15] W. Wang, D. Yan, Z. Li, S. Li, Q. Tian, and X. Chen, “Recent advances           Available: https://huggingface.co/nvidia/stt en fastconformer hybrid
     in speech language models: A survey,” arXiv preprint arXiv:2410.03751,          large streaming multi
     2024.                                                                      [37] S. Sridhar, K. C. Puvvada, Z. Chen, O. Hrinchuk, H. Huang,
[16] X. Wang, Y. Li, C. Fu, Y. Shen, L. Xie, K. Li, X. Sun, and L. Ma,               V. Lavrukhin, J. Balam, and B. Ginsburg, “Parakeet: A natural language
     “Freeze-omni: A smart and low latency speech-to-speech dialogue model           speech recognition model,” NVIDIA Technical Blog, 2024. [Online].
     with frozen llm,” arXiv preprint arXiv:2411.00774, 2024.                        Available: https://nvidia.github.io/NeMo/blogs/2024/2024-01-parakeet/
[17] A. Zeng, Z. Du, M. Liu, K. Wang, S. Jiang, L. Zhao, Y. Dong, and           [38] Kyutai, “STT-2.6b-en: Streaming Speech-to-Text Model,” 2024, hugging
     J. Tang, “Glm-4-voice: Towards intelligent and human-like end-to-end            Face Model Hub. [Online]. Available: https://huggingface.co/kyutai/
     spoken chatbot,” arXiv preprint arXiv:2412.02612, 2024.                         stt-2.6b-en
[18] R. Huang, M. Li, D. Yang, J. Shi, X. Chang, Z. Ye, Y. Wu, Z. Hong,         [39] Y. Chu, J. Xu, Q. Yang, H. Wei, X. Wei, Z. Guo, Y. Leng, Y. Lv, J. He,
     J. Huang, J. Liu et al., “Audiogpt: Understanding and generating speech,        J. Lin, C. Zhou, and J. Zhou, “Qwen2-audio technical report,” arXiv
     music, sound, and talking head,” in Proceedings of the AAAI Conference          preprint arXiv:2407.10759, 2024.
     on Artificial Intelligence, vol. 38, no. 21, 2024, pp. 23 802–23 804.      [40] NVIDIA, “Nemotron-Nano-9B-v2-Base: A 9B Parameter Language
[19] D. Zhang, S. Li, X. Zhang, J. Zhan, P. Wang, Y. Zhou, and X. Qiu,               Model for Reasoning and Instruction Following,” 2025, hugging
     “Speechgpt: Empowering large language models with intrinsic cross-              Face Model Hub. [Online]. Available: https://huggingface.co/nvidia/
     modal conversational abilities,” arXiv preprint arXiv:2305.11000, 2023.         NVIDIA-Nemotron-Nano-9B-v2-Base
                                                                                [41] E. Casanova, J. Kim, M. G. Fuenmayor, S. Hussain, V. Klimkov,
[20] H. Kim, S. Seo, K. Jeong, O. Kwon, J. Kim, J. Lee, E. Song, M. Oh,
                                                                                     V. Mendelev, M. Desta, P. Neekhara, P. Zelasko, C. Chen et al.,
     S. Yoon, and K. M. Yoo, “Unified speech-text pretraining for spoken
                                                                                     “Voicechat-tts: A low-latency continuous speech synthesis model for
     dialog modeling,” arXiv preprint arXiv:2402.05706, 2024.
                                                                                     interactive agents,” arXiv preprint arXiv:2608.13831, 2026.
[21] Z. Xie and C. Wu, “Mini-omni2: Towards open-source gpt-4o with vi-
                                                                                [42] V. Pratap, A. Tjandra, B. Shi, P. Tomasello, A. Babu, S. Kundu,
     sion, speech and duplex capabilities,” arXiv preprint arXiv:2410.11190,
                                                                                     A. Elkahky, Z. Ni, A. Vyas, M. Fazel-Zarandi et al., “Scaling speech
     2024.
                                                                                     technology to 1,000+ languages,” Journal of Machine Learning Re-
[22] X. Xin, Z. Wang, Q. Cheng, X. Chen, Z. Li, X. Jiang, H. Zhao, and               search, vol. 25, no. 97, pp. 1–52, 2024.
     Y. Feng, “Intrinsicvoice: Empowering llms with intrinsic real-time voice   [43] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, “Librispeech:
     interaction abilities,” arXiv preprint arXiv:2410.08035, 2024.                  an asr corpus based on public domain audio books,” in 2015 IEEE
[23] Q. Fang, S. Guo, Y. Zhou, Z. Ma, S. Zhang, and Y. Feng, “Llama-omni:            International Conference on Acoustics, Speech and Signal Processing
     Seamless speech interaction with large language models,” arXiv preprint         (ICASSP). IEEE, 2015, pp. 5206–5210.
     arXiv:2409.06666, 2024.                                                    [44] C. Wang, M. Riviere, A. Lee, A. Wu, C. Talnikar, D. Haziza, M. Schwab,
[24] OpenAI, “Introducing gpt-realtime and realtime api updates for                  J. Pino, and E. Dupoux, “VoxPopuli: A large-scale multilingual speech
     production voice agents,” 2025, blog post. [Online]. Available:                 corpus for representation learning, semi-supervised learning and inter-
     https://openai.com/index/introducing-gpt-realtime/                              pretation,” in Proceedings of the 59th Annual Meeting of the Association
[25] Y. Chen, T. Hu, Y. Li, Y. Tang, H. Su, X. Zheng, Z. Lin, S. Wu,                 for Computational Linguistics, 2021, pp. 993–1003.
     J. Zhang, and J. T. Zhou, “Fireredchat: A pluggable, full-duplex voice     [45] R. Ardila, M. Branson, K. Davis, M. Kohler, J. Meyer, M. Henretty,
     interaction system with cascaded and semi-cascaded implementations,”            R. Morais, L. Saunders, F. Tyers, and G. Weber, “Common voice:
     arXiv preprint arXiv:2509.06502, 2024.                                          A massively-multilingual speech corpus,” in Proceedings of the 12th
[26] Z. Zhang, J. Chen, Y. Liu, H. Li, Y. Zhang, Z. Lin, S. Zhou, W.-                Language Resources and Evaluation Conference, 2020, pp. 4218–4222.
     Q. Zhang, and J. Liu, “Flexduo: A pluggable system for enabling            [46] J. Yamagishi, C. Veaux, and K. MacDonald, “CSTR VCTK corpus: En-
     full-duplex capabilities in speech dialogue systems,” arXiv preprint            glish multi-speaker corpus for CSTR voice cloning toolkit,” in University
     arXiv:2502.13472, 2025.                                                         of Edinburgh. The Centre for Speech Technology Research, 2019.
[27] A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou,       [47] P. K. O’Neill, V. Lavrukhin, S. Majumdar, V. Noroozi, Y. Zhang,
     E. Grave, and N. Zeghidour, “Moshi: a speech-text foundation model              O. Kuchaiev, J. Balam, Y. Huang, A. Krivoshein, and B. Gins-
     for real-time dialogue,” arXiv preprint arXiv:2410.00037, 2024.                 burg, “SPGISpeech: 5,000 hours of transcribed financial audio
[28] R. Roy, J. Raiman, S.-g. Lee, T.-D. Ene, R. Kirby, S. Kim, J. Kim,              for fully formatted end-to-end speech recognition,” arXiv preprint
     and B. Catanzaro, “Personaplex: Voice and role control for full duplex          arXiv:2104.02014, 2021.
     conversational speech models,” in IEEE International Conference on         [48] N. R. Koluguri, M. Sekoyan, G. Zelenfroynd, S. Meister, S. Ding,
     Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2026.                   S. Kostandian, H. Huang, N. Karpov, J. Balam, V. Lavrukhin, Y. Peng,
[29] W. Yu, S. Wang, X. Yang, X. Chen, X. Tian, J. Zhang, G. Sun,                    S. Papi, M. Gaido, A. Brutti, and B. Ginsburg, “Granary: Speech
     L. Lu, Y. Wang, and C. Zhang, “Salmonn-omni: A codec-free llm                   recognition and translation dataset in 25 european languages,” arXiv
     for full-duplex speech understanding and generation,” arXiv preprint            preprint arXiv:2505.13404, 2025.
     arXiv:2411.18138, 2024.                                                    [49] G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu,
[30] Q. Zhang, L. Cheng, C. Deng, Q. Chen, W. Wang, S. Zheng, J. Liu,                and H.-y. Lee, “Full-duplex-bench: A benchmark to evaluate full-duplex
     H. Yu, C. Tan, Z. Du et al., “Omniflatten: An end-to-end gpt model for          spoken dialogue models on turn-taking capabilities,” arXiv preprint
     seamless voice conversation,” arXiv preprint arXiv:2410.17799, 2024.            arXiv:2503.04721, 2025.
[31] Y.-J. Shih, D. Raj, C. Wu, W. Zhou, S. Bong, Y. Gaur, J. Mahadeokar,       [50] Y. Chen, X. Yue, C. Zhang, X. Gao, R. T. Tan, and H. Li,
     O. Kalinli, and M. Seltzer, “Can speech LLMs think while listening?”            “Voicebench: Benchmarking llm-based voice assistants,” arXiv preprint
     arXiv preprint arXiv:2510.07497, 2025.                                          arXiv:2410.17196, 2024.
[51] V. Noroozi, S. Majumdar, A. Kumar, J. Balam, and B. Ginsburg,
     “Stateful conformer with cache-based inference for streaming automatic
     speech recognition,” in ICASSP. IEEE, 2024.
[52] Silero Team, “Silero VAD: pre-trained enterprise-grade voice activity de-
     tector,” https://github.com/snakers4/silero-vad, 2021, gitHub repository.
[53] Q. Team, “Qwen2.5 technical report,” arXiv preprint arXiv:2412.15115,
     2025.

