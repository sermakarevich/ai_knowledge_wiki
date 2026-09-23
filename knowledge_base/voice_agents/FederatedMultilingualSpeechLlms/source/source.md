# Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking
Source: http://arxiv.org/abs/2609.23825v1
Kind: pdf
Fetched: 2026-09-22T08:51:33.203851+00:00
Tool: pdftotext

                                                              Federated Multilingual Speech-LLMs: Architecture and
                                                                       Aggregation Strategy Benchmarking

                                                                         Jordi Luque ID 1,∗∗ , Aleix Sant ID 1,2 , Fernando López ID 1,3
                                                                              1
                                                                                  Telefónica Innovación Digital, Scientific Research
                                                                                       2
                                                                                          Universitat Politècnica de Catalunya
                                                                                         3
                                                                                           Universidad Autónoma de Madrid
                                                                                            jordi.luque@telefonica.com


                                                                     Abstract                                 connector, and language-decoder components should be coor-
                                         We present a comprehensive benchmark of Federated Learning           dinated under multilingual, non-IID client distributions.




arXiv:2609.23825v1 [cs.CL] 20 Sep 2026
                                         (FL) for multilingual Automatic Speech Recognition (ASR),                 Motivated by these gaps, we focus explicitly on Speech-
                                         evaluating four Speech-LLM architectures on the Multilingual         LLMs under the FL paradigm and benchmark four encoder–
                                         LibriSpeech dataset. We compare FedAvg and FedProx across            LLM families and two aggregation strategies in a realistic mul-
                                         frozen and unfrozen encoder configurations, demonstrating that       tilingual setting. Our study addresses the following questions:
                                         optimized learning rates are critical for performance. Specif-
                                         ically, independently tuning the learning rates for the speech       • (Q1) Architecture: which encoder–LLM combination best
                                         encoder, connector, and decoder yields the lowest error rates,           handles multilingual non-IID client distributions. Does the
                                         with full three-component adaptation (LoRA for encoder and               encoder type (ASR-supervised vs. self-supervised) affect
                                         decoder, full training for the connector) producing the best             federated adaptability of Speech-LLMs?
                                         FL results. We observe that FedProx efficacy is architecture-        • (Q2) Aggregation: does FedProx mitigate client language
                                         dependent, providing notable advantages in multilingual pre-             drift in this multilingual Speech-LLM setting?
                                         trained architectures (e.g., EuroLLM over TinyLlama when                   These questions are particularly acute in multilingual set-
                                         keeping the encoder fixed); this indicates that LLM backbone         tings, where clients differ simultaneously in language, accent,
                                         capacity plays a key role in mediating resilience to heteroge-       speaker population and recording conditions. Such strongly
                                         neous data distributions. These findings offer concrete design       non-IID data cause client drift [13] that destabilises FL opti-
                                         guidance for deploying multilingual Speech-LLMs in privacy-          misation [14] and has motivated aggregation strategies such as
                                         sensitive, distributed environments.                                 FedProx [15] or SCAFFOLD [16].
                                         Index Terms: federated learning, speech recognition, speech                Our FL experiments use a speaker-partitioned split of Mul-
                                         large language models, FedAvg, FedProx, multilingual ASR             tilingual LibriSpeech [17] (8 European languages, 316 clients,
                                                                                                              one speaker per client), inducing simultaneous acoustic, linguis-
                                                               1. Introduction                                tic and domain-level heterogeneity. Local Speech-LLMs are
                                                                                                              fine-tuned with LoRA [18] under frozen and unfrozen speech
                                         Speech large language models (LLMs) have emerged as a                encoders, with the connector and LLM always unfrozen. We
                                         prominent paradigm for end-to-end automatic speech recog-            analyse the interplay between pretrained encoders and LLM
                                         nition (ASR), combining powerful acoustic encoders [1, 2]            backbones, the effect of differential per-component learning
                                         with pre-trained language decoders [3, 4] through a lightweight      rates, and the FL-ASR behaviour of FedAvg and FedProx in
                                         cross-modal connector [5]. This architecture leverages large-        this heterogeneous setting.
                                         scale text pretraining to exploit rich language priors, enabling
                                         instruction-following speech understanding and achieving state-
                                         of-the-art results particularly in multilingual and low-resource                   2. System Architectures
                                         settings. Privacy-sensitive deployments in healthcare, legal,        Speech-LLMs couple three heterogeneous components: an
                                         and personal assistant applications motivate federated learning      acoustic encoder (E), a cross-modal connector (C), and a lan-
                                         (FL) [6], where models are fine-tuned on distributed client data     guage decoder (L), producing a transcript as:
                                         without centralising raw audio.
                                              Federated speech learning predates Speech-LLMs and has                            ŷ = L ([C(E(x)); Etext ]) .                 (1)
                                         mainly targeted ASR, where strongly heterogeneous, privacy-
                                                                                                                  All three components are trained jointly by minimising the
                                         sensitive speech data have motivated methods for non-IID op-
                                                                                                              standard autoregressive cross-entropy loss over the ground-truth
                                         timisation, personalisation, and communication-efficient train-
                                                                                                              transcript tokens y = (y1 , . . . , yS ):
                                         ing [7, 8, 9]. More recent work consolidates parameter-efficient
                                         fine-tuning for pretrained speech encoders in FL, showing that                        S
                                                                                                                               X
                                         LoRA and adapter-based approaches can effectively adapt foun-           LCE (θ) = −         log pθ (ys | C(E(x)), Etext , y<s ) ,   (2)
                                         dation models under tight communication and compute bud-                              s=1
                                         gets [10, 11, 12]. However, these studies operate on monolithic
                                                                                                              where θ collects all trainable parameters (LoRA adapters and
                                         speech encoder-only [11] or language-based architectures [8],
                                                                                                              connector projection), and y<s denotes the preceding tokens
                                         and no previous available work has directly investigated fed-
                                                                                                              supplied via teacher forcing. The loss is computed over tran-
                                         erated training of Speech-LLMs, leaving open how encoder,
                                                                                                              script tokens; audio tokens and prompt embeddings appear as
                                           ** indicates the corresponding author.                             conditioning context. Figure 1 summarises the full pipeline.
                                                                      Algorithm 1 FedAvg [6]. θ: LoRA adapters + connector; K:
                                                                      clients; nk : samples on client k; C: client fraction/round; B:
                                                                      batch size; E=10: local epochs; η=10−4 .
                                                                      Server:
                                                                         initialise θ0
                                                                         for each round t = 1, 2, . . . , T do
                                                                            St ← random set of max(C · K, 1) clients
                                                                            for each client k ∈ St in parallel do
                                                                               θtk ←P ClientUpdate(k, θt−1 )
                                                                            θt ← k∈St P nk nj θtk
                                                                                            j∈St


                                                                      ClientUpdate(k,θ):
                                                                        for local epoch e = 1, . . . , E do
                                                                          for each batch b ⊆ Pk , |b|=B do
                                                                              θ ← AdamW(θ, ▽ℓ(θ; b), η)
                                                                        return θ


                                                                      2-layer MLP projector; a deeper, higher-compression connector
                                                                      in which both MLP layers are trained.

Figure 1: Speech-LLM architecture: encoder E maps speech                                3. Federated Setup
x to frame-level features; connector C downsamples by k; de-
coder L generates ŷ from the projected tokens and task prompt.
                                                                      3.1. Aggregation Strategies
2.1. Encoder–LLM Models                                               Our federated setting uses synchronous client-server optimiza-
                                                                      tion where participating clients (C = 0.3) perform E = 10
The combination of foundational acoustic encoders and pre-            local AdamW epochs before server aggregation via FedAvg or
trained LLMs has become a prominent recipe for multilin-              FedProx. We compute the loss gradient over all data held by
gual end-to-end speech recognition [3]. We evaluate four en-          these clients, C ∗ K = 94 clients for the global server; see
coder–LLM pairings:                                                   Algorithm 1. Two aggregation strategies are considered:
     Whisper + TinyLlama. Whisper large-v3-turbo [1] en-                  FedAvg: Standard weighted averaging of client updates [6]
codes audio into 768-dimensional speech frame representations,        or each round:
projected to 2048-dimensional tokens to align with TinyLlama-                                   X        n
1.1B [19] (22 layers). Whisper is a pretrained end-to-end multi-                      θ (t+1) =      P k        θ (t,k) ,        (3)
lingual ASR model, and its encoder (32 layers) already captures                                 k∈St    j∈St nj
robust cross-lingual acoustic features.
     Whisper + EuroLLM. Identical Whisper encoder, but the            where nk are the training samples on client k and St is the ran-
decoder is replaced by EuroLLM-1.7B-Instruct [4], a decoder-          dom fraction of clients sampled every round.
only model pretrained on multilingual European text corpora.              FedProx: Regularises the client loss, ClientUpdate in Al-
     WavLM + TinyLlama. WavLM-Large [2] replaces Whis-                gorithm 1, with the proximal term µ to limit client drift [15],
per as the encoder (1024-dimensional tokens, 24 layers);              due to data heterogeneity, for each round:
TinyLlama remains the decoder. WavLM is a self-supervised
                                                                                                         µ          2
learning (SSL) model pretrained on masked speech prediction.                          min Llocal (θ) +     θ − θ (t) ,              (4)
Unlike Whisper it has never seen ASR supervision, making it
                                                                                       θ                 2          2

a stronger test of whether FL can adapt an SSL encoder to the         where µ>0 penalises deviation, e.g. due to narrow acoustic
downstream ASR task.                                                  distribution in client data, from the current global model θ (t) .
     Voxtral-Mini Voxtral [20] is an end-to-end multimodal
Speech-LLM composed of a Whisper-large-v3-based audio en-             3.2. Dataset and Partitioning
coder and a 30-layer Ministral-3B [21] text decoder, jointly pre-
trained on audio understanding and ASR.                               3.2.1. Corpus
                                                                      All experiments use the Multilingual LibriSpeech (MLS) cor-
2.1.1. Cross-modal connector.                                         pus [17], an audiobook corpus covering 8 European languages
                                                                      derived from LibriVox recordings. We use the official MLS
The connector C, see Fig. 1, bridges the acoustic encoder and
                                                                      train splits as the federated training pool (685.7 h total), the
the LLM decoder in two steps. First, a frame-stacking oper-
                                                                      MLS dev split for validation during training, and the MLS
ation with stride 2 concatenates each pair of consecutive en-
                                                                      test split as the held-out evaluation benchmark (138 h, 19,492
coder output frames. Second, a single trainable linear layer
                                                                      samples). Table 1 reports training hours and speaker counts per
projects to the input LLM dimension, aligning acoustic rep-
                                                                      language.
resentations with the LLM’s embedding space. This design
is shared by Whisper+TinyLlama, Whisper+EuroLLM, and
                                                                      3.2.2. Multilingual Partition (approximately IID)
WavLM+TinyLlama, where only the single linear projection
is trained from scratch. In contrast, Voxtral uses a different con-   The multilingual partition serves as a control to isolate the ef-
nector, downsampling the audio by a factor of 4, followed by a        fect of data heterogeneity from architecture choice. A random
Table 1: MLS training data by language under the stratified by        Table 2: WER on MLS test set. B: non-IID speaker partition. A:
speaker partition, 316 clients.                                       approximately IID multilingual partition. Gap: WER relative
                                                                      to corresponding FedAvg baseline; negative = improvement. †:
            Language      Hours Speakers/Clients                      best encoder learning rate multiplier (0.02×LLM lr). ‡: re-
                                                                      ported at round 9.
            French         251.6                   15
            German         160.9                   19
                                                                        System               Encoder Setting      WER           Gap
            English        105.3                  256
            Spanish         83.8                    9                   Whisper + TinyLlama-1.1B
            Italian         27.3                    7                   Centralized       frozen                 0.0719         —
            Polish          25.7                    1                   FedAvg            frozen (B)             0.1415         —
            Portuguese      18.5                    5                   FedAvg            frozen (A)‡            0.1284    −0.0131
            Dutch           12.7                    4                   FedAvg            unfrozen (B)†          0.1418    +0.0003
            Total          685.7                  316                   FedProx µ=0.001 frozen (B)               0.1499    +0.0084
                                                                        FedProx µ=0.001 frozen (A)‡              0.1386    +0.0102
                                                                        FedProx µ=0.05 frozen (B)                0.1615    +0.0200
                                                                        FedProx µ=0.1     frozen (B)             0.1843    +0.0428
multilingual mixture of utterances is assigned to each client ir-
respective of speaker identity, approximating the IID assump-           Whisper + EuroLLM-1.7B-Instruct
tion. Because MLS is derived from LibriVox audiobooks, the              Centralized      frozen                  0.0660      —
same reader can appear across official train, dev, and test splits.     FedAvg           frozen (B)              0.1330      —
The centralized training pools this full set and therefore carries      FedAvg           frozen (A)‡             0.1224 −0.0106
a 3.5% speaker leakage. For FL experiments , partition (A) in           FedAvg           unfrozen (B)            0.1778 +0.0448
Table 2, same identities overlap contaminating 59 clients out of        FedAvg           unfrozen† (B)           0.1170 −0.0160
K=316 clients (18.7%). These clients contain utterances from            FedProx µ=0.001 frozen (B)               0.1217 −0.0113
test or dev sharing same speakers, totalling 60,825 of 1,726,583        WavLM-Large + TinyLlama-1.1B
training samples (i.e the same 3.5% speaker leakage). Note that         Centralized       frozen                 0.2409         —
these are different utterances of the same speaker, not duplicate       FedAvg            frozen (B)             0.5559         —
audio.                                                                  FedAvg            unfrozen (B)           0.5338    −0.0221
                                                                        Voxtral-Mini-3B-2507
3.2.3. Speaker Partition (non-IID)
                                                                        Centralized        frozen                0.1238         —
The speaker partition, (B) in Table 2, assigns all utterances of        FedAvg             frozen (B)            0.1442         —
a single MLS speaker to one client. With K=316 clients, this            FedAvg             unfrozen (B)          0.1362    −0.0080
creates the strongest possible non-IID distribution: each client’s      FedProx µ=0.001 frozen (B)               0.1492    +0.0050
data is drawn from a single acoustic identity, language, and            FedProx µ=0.001 unfrozen (B)             0.1468    +0.0106
recording environment, producing simultaneous linguistic (each
client speaks at most one language) and acoustic (microphone,
room, speaking rate) heterogeneity. Due to the LibriVox origin
                                                                      over a maximum of 10 epochs; the best-validation-WER check-
of MLS, 8 of 316 clients (2.5%) correspond to speakers also
                                                                      point is selected (typically around epoch 4). Evaluation uses the
present in the MLS test split, accounting for 4,747 of 169,586
                                                                      MLS test split with overall WER reported across all 8 languages
training samples (2.8%), while 3.5% of centralized training data
                                                                      combined. All models are fine-tuned with LoRA [18] adapters
and 18.7% of clients in partition (A) share speakers with the test
                                                                      (rank r=8, α=16, dropout 0.05; Voxtral uses α=32) applied
set. Because these overlap rates are inherited from the standard
                                                                      to the attention projections of the speech encoder (q, k, v) and
MLS splits, the centralized and IID upper bounds benefit from
                                                                      LLM decoder (q, v), together with the fully-trained connector;
acoustic speaker familiarity. Consequently, the actual degrada-
                                                                      only these parameters are trainable and are transmitted between
tion caused by FL non-IID conditions is slightly less severe than
                                                                      clients and the FL server, reducing communication cost over full
the raw distance to the upper bounds suggests.
                                                                      fine-tuning. Unlike the pretrained encoders and LLM decoders,
                                                                      we initialise the connector from scratch (except for Voxtral), so
3.3. Training Configuration                                           it must learn to bridge the modalities entirely from the feder-
All FL experiments use the Flower simulation framework with           ated fine-tuning data. Unless stated otherwise, WER values are
Ray as the backend [22]. Experiments on the non-IID speaker           reported as proportions (e.g., 0.1415 corresponds to 14.15%).
partition (B) train for T = 40 global rounds. For the mul-
tilingual partition (A), results are reported at T = 9 global                      4. Results and Discussion
rounds (‡ in Table 2). This is because the multilingual mix-
                                                                      4.1. Centralized and IID Upper Bounds
ture in partition (A) exhibits rapid convergence leading to early
WER optimization collapse. All hyper-parameter choices—               Centralized training (non-FL) on the pooled partition sets the
encoder learning-rate multiplier λ, FedProx coefficient µ, and        per-architecture performance ceiling (Table 2); all centralized
local epochs E—were selected on the MLS dev set, and the test         models converge within 4–7 epochs. Whisper+EuroLLM
split is used only to evaluate each selected checkpoint. Local        reaches WER 0.066 versus 0.072 for Whisper+TinyLlama,
clients perform E=10 local epochs per round, using AdamW              confirming the multilingual LLM advantage even without non-
optimiser with maximum learning rate η=10−4 , cosine decay,           IID pressure; WavLM+TinyLlama reaches 0.24 (3.3× higher
batch size 16, and half precision bf16. Centralized (non-FL)          than the Whisper variant), showing that ASR pretraining of the
training uses the same AdamW optimiser with cosine decay              encoder decisively beats SSL pretraining for ASR.
                                                                    Table 3: Per-language WER on MLS test set for FL en-
                                                                    coder frozen variants trained on speaker (non-IID) partition.
                                                                    Cent. = Centralized Whisper+TinyLlama. FedAvgWT = FedAvg
                                                                    Whisper+TinyLlama. FedAvgEL = FedAvg Whisper+EuroLLM.
                                                                    FPEL = FedProx µ=0.001 Whisper+EuroLLM. Bold: best FL
                                                                    result per language.

                                                                          Lang.         Cent. FedAvgWT FedAvgEL FPEL
                                                                          Dutch      0.110        0.270         0.265     0.195
                                                                          English    0.049        0.100         0.098     0.090
                                                                          French     0.061        0.075         0.078     0.072
                                                                          German     0.071        0.104         0.098     0.125
                                                                          Italian    0.121        0.233         0.186     0.189
                                                                          Polish     0.110        0.270         0.237     0.228
                                                                          Portuguese 0.093        0.225         0.160     0.177
                                                                          Spanish    0.046        0.085         0.075     0.068
Figure 2: WER vs. encoder learning-rate multiplier (relative              Overall       0.072     0.142         0.133     0.122
to LLM LR). Whisper+TinyLlama (blue, E=5) stays flat at its
frozen baseline while Whisper+EuroLLM (green, E=10) im-
proves monotonically; dashed: frozen-encoder baselines.
                                                                    EuroLLM also outperforms TinyLlama on six of eight lan-
4.2. Aggregation Strategy Comparison                                guages; with the largest gains are on most of low-resource lan-
                                                                    guages, see Table 1, where multilingual priors matter most:
With a frozen encoder, FedAvg reaches WER 0.1415                    Portuguese (−6.5% abs.), Italian (−4.8%), Polish (−3.3%).
(96.8% relative degradation from centralized) for                   FedProx EuroLLM improves over FedAvg on five of eight lan-
Whisper+TinyLlama; replacing only the decoder with                  guages: Dutch (0.265 → 0.195, −7.0% abs.), Polish, English,
EuroLLM reduces it to 0.133 (−6.0% relative), and Voxtral           French, and Spanish. Conversely, it degrades German (+2.6%
(0.144) underperforms the EuroLLM pipeline. WavLM reaches           abs.), Italian, and Portuguese. Note that benefit is strongest for
0.56, confirming that ASR-pretrained encoders are decisive          the least-represented languages (≤ 4 clients), while moderate-
under FL non-IID conditions. FedProx regularisation degrades        resource languages show mixed results.
Whisper+TinyLlama monotonically with µ, and also hurts                   Because the client distribution is strongly skewed toward
Voxtral (frozen 0.144 → 0.149, unfrozen 0.1362 → 0.1468),           English (256 of 316 clients) and the overall WER is domi-
contradicting its non-IID motivation. Strikingly, FedProx           nated by high-resource evaluation words, we also report macro-
µ=0.001 improves Whisper+EuroLLM (WER 0.1217,                       averaged WER (unweighted mean of the per-language values in
−8.5% relative), the best frozen-encoder result.                    Table 3): FedAvg Whisper+TinyLlama is 0.170 versus 0.150
4.3. Encoder LR Tuning under FL                                     for Whisper+EuroLLM. This macro gap (−2.0 points) is larger
                                                                    than the word-weighted gap (−0.9 points), confirming that the
Unfreezing the Whisper encoder under FedAvg yields WER              EuroLLM advantage is driven particularly by the low-resource
0.1418, comparable to the frozen baseline (0.1415), even after      languages rather than being masked by them.
sweeping the encoder learning rate ∈ {0.01, 0.02, 0.05, 0.10}
and for different values of local epochs E ∈ {3, 5, 10}, see                              5. Conclusion
Fig. 2. We hypothesise that this stems from encoder-update
cancellation, in which each client adapts the encoder to its        This work benchmarks federated training for Speech-LLMs
own speaker’s acoustics, producing divergent updates that av-       across four architectures and two aggregation strategies using
erage to near-zero under FedAvg, while LLM updates on the           a partition of 316 clients from the Multilingual LibriSpeech
shared linguistic task survive averaging. WavLM confirms the        dataset. The results show that multilingual pre-training is a pri-
pattern. The centralized gap (3.2×) grows to 3.9× under FL          mary driver of FL performance, with EuroLLM outperforming
(0.24 → 0.56), suggesting SSL pretraining misalignment is           TinyLlama, by 6% relative WER, and Voxtral pipelines. Fur-
amplified by heterogeneous data. Unfreezing the WavLM en-           thermore, the efficacy of the FedProx algorithm is architecture-
coder provides only marginal gain. For EuroLLM, after sweep-        dependent, improving Whisper+EuroLLM while degrading
ing the learning rate multiplier for the encoder we can observe     Whisper+TinyLlama and Voxtral configurations. Controlled
a monotonic improvement from 0.178 → 0.117, see Fig. 2, a           paired comparisons suggest that stronger multilingual LLM ca-
12% relative below the encoder-frozen EuroLLM variant. Vox-         pacity helps absorb client drift under proximal regularization,
tral also benefits modestly from unfreezing (0.144 → 0.136).        though broader multi-component variations also introduce sec-
These results suggest that, for multicomponent Speech-LLMs,         ondary effects from connector depth and encoder pre-training.
separately adjusting the encoder and decoder is crucial when the    We also report that differential learning rate tuning (low-rate en-
encoder is well pre-trained, in order to prevent update cancella-   coder vs. high-rate decoder) provides superior results compared
tion during federated aggregation.                                  to frozen encoders, since the components of a Speech-LLM ex-
                                                                    hibit distinct gradient scales and adaptation requirements that
4.4. Per-Language Analysis
                                                                    preclude treating the model as monolithic during FL optimisa-
Table 3 compares FedAvg TinyLlama and EuroLLM against the           tion. These results offer a road map for practitioners deploy-
FedProx with µ=0.001 which reaches the lower WER 0.122              ing robust, cross-lingual Speech-LLM systems in federated set-
between frozen-encoder FL results. For the FedAvg algorithm,        tings.
                 6. Acknowledgements                                       [17] V. Pratap, Q. Xu, A. Sriram, G. Synnaeve, and R. Collobert,
                                                                                “MLS: A large-scale multilingual dataset for speech research,” in
This work has received funding from the European Union’s                        Proc. Interspeech, 2020, pp. 2757–2761.
Horizon Europe research and innovation programme under the
                                                                           [18] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang,
project ELOQUENCE (Grant Agreement No. 101135916).                              L. Wang, and W. Chen, “LoRA: Low-rank adaptation of large lan-
This work was supported by computational resources from the                     guage models,” arXiv preprint arXiv:2106.09685, 2022.
EuroHPC Joint Undertaking under the EuroHPC AI Factory
                                                                           [19] P. Zhang, G. Zeng, T. Wang, and W. Lu, “TinyLlama: An open-
grant EHPC-AIF-2026LS01-004.                                                    source small language model,” arXiv preprint arXiv:2401.02385,
                                                                                2024.
                        7. References                                      [20] H. Liu et al., “Voxtral,” arXiv preprint arXiv:2507.13264, 2025.
 [1] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and                [Online]. Available: https://arxiv.org/abs/2507.13264
     I. Sutskever, “Robust speech recognition via large-scale weak su-     [21] ——, “Ministral 3,” 2026. [Online]. Available: https://arxiv.org/
     pervision,” in Proc. ICML, 2023, pp. 28 492–28 518.                        abs/2601.08584
 [2] S. Chen, C. Wang, Z. Chen, Y. Wu, S. Liu, Z. Chen, J. Li,             [22] D. J. Beutel, T. Topal, A. Mathur, X. Qiu, J. Fernandez-Marques,
     N. Kanda, T. Yoshioka, X. Xiao et al., “WavLM: Large-scale self-           Y. Gao, L. Sani, K. H. Li, T. Parcollet, P. P. B. de Gusmão et al.,
     supervised pre-training for full stack speech processing,” in IEEE         “Flower: A friendly federated learning research framework,” in
     J. Sel. Top. Signal Process., vol. 16, no. 6, 2022, pp. 1505–1518.         Proc. ICLR Workshop on Distributed and Private Machine Learn-
 [3] D. Zhang, S. Li, X. Zhang, J. Zhan, P. Wang, Y. Zhou, and                  ing, 2020.
     X. Qiu, “SpeechGPT: Empowering large language models with
     intrinsic cross-modal conversational abilities,” arXiv preprint
     arXiv:2305.11000, 2023.
 [4] P. H. Martins, P. Fernandes, M. Faysse et al., “EuroLLM:
     Multilingual language models for europe,” arXiv preprint
     arXiv:2409.16235, 2024.
 [5] C. Tang, W. Yu, G. Sun, X. Chen, W. Tan, L. Li, Z. Lu, S. Watan-
     abe, and C. Zhang, “SALMONN: Towards generic hearing abili-
     ties for large language models,” in Proc. ICLR, 2024.
 [6] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Ar-
     cas, “Communication-efficient learning of deep networks from
     decentralized data,” in Proc. AISTATS, 2017, pp. 1273–1282.
 [7] H. Zhu, J. Wang, G. Cheng, P. Zhang, and Y. Yan, “Decoupled
     federated learning for asr with non-iid data,” in Interspeech 2022,
     2022, pp. 2628–2632.
 [8] D. Guliani, F. Beaufays, and G. Motta, “Federated learning for
     ASR based on wav2vec 2.0,” in Proc. ICASSP, 2021, pp. 3040–
     3044.
 [9] Y. Gao, T. Parcollet, S. Zaiem, J. Fernandez-Marques, P. P. B.
     de Gusmao, D. J. Beutel, and N. D. Lane, “End-to-end speech
     recognition from federated acoustic models,” in ICASSP 2022 -
     2022 IEEE International Conference on Acoustics, Speech and
     Signal Processing (ICASSP), 2022, pp. 7227–7231.
[10] Y. Du, Z. Zhang, L. Yue, X. Huang, Y. Zhang, T. Xu, L. Xu, and
     E. Chen, “Communication-efficient personalized federated learn-
     ing for speech-to-text tasks,” in 2024 IEEE International Con-
     ference on Acoustics, Speech and Signal Processing, 2024, pp.
     10 001–10 005.
[11] X. Kan, Y. Xiao, T.-J. Yang, N. Chen, and R. Mathews,
     “Parameter-efficient transfer learning under federated learning
     for automatic speech recognition,” CoRR, vol. abs/2408.11873,
     2024. [Online]. Available: https://arxiv.org/abs/2408.11873
[12] M. N. Ali, D. Falavigna, and A. Brutti, “EFL-PEFT: A
     communication-efficient federated learning framework using peft
     sparsification for asr,” in 2025 IEEE International Conference on
     Acoustics, Speech and Signal Processing, 2025, pp. 1–5.
[13] S. P. Karimireddy, S. Kale, M. Mohri, S. Reddi, S. Stich, and
     A. T. Suresh, “SCAFFOLD: Stochastic controlled averaging for
     federated learning,” in Proc. ICML, 2020, pp. 5132–5143.
[14] P. Kairouz, H. B. McMahan, B. Avent et al., “Advances and open
     problems in federated learning,” Foundations and Trends in Ma-
     chine Learning, vol. 14, no. 1–2, pp. 1–210, 2021.
[15] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and
     V. Smith, “Federated optimization in heterogeneous networks,”
     in Proc. MLSys, 2020.
[16] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chan-
     dra, “Federated learning with non-IID data,” arXiv preprint
     arXiv:1806.00582, 2018.

