# JAL-Turn: Joint Acoustic-Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialog
Source: https://arxiv.org/abs/2603.26515
Kind: pdf
Fetched: 2026-09-22T09:32:41.320071+00:00
Tool: pdftotext

                                           JAL-Turn: Joint Acoustic–Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in
                                                                       Full-Duplex Spoken Dialogue Systems

                                                                               Guangzhao Yang1* , Yu Pan1* , Shi Qiu1† , Ningjie Bai1†
                                                                                                    1
                                                                                                        Recho Inc, Japan
                                                                    ABSTRACT                                     interaction quality, ultimately undermining user experience and
                                         Despite recent advances, efficient and robust turn-taking detec-        trust. As a result, accurately determining whether a user has
                                         tion remains a significant challenge in industrial-grade Voice          genuinely finished their speaking turn—while still maintaining




arXiv:2603.26515v1 [cs.CL] 27 Mar 2026
                                         AI agent deployments. Many existing systems rely solely on              rapid system responsiveness—has become a critical challenge for
                                         acoustic or semantic cues, leading to suboptimal accuracy and           building effective and user-friendly voice AI agents.
                                         stability, while recent attempts to endow large language models              Turn-taking is a fundamental property of human spoken in-
                                         with full-duplex capabilities require costly full-duplex data and       teraction [1]. In everyday conversation, speaking turns are ex-
                                         incur substantial training and deployment overheads, limiting           changed naturally with minimal delay. In contrast, due to inherent
                                         real-time performance. In this paper, we propose JAL-Turn, a            variability of speech signal and other factors [2–4], achieving sim-
                                         lightweight and efficient speech-only turn-taking framework that        ilarly real-time and stable turn management remains challenging.
                                         adopts a joint acoustic–linguistic modeling paradigm, in which a        Although existing turn-taking detection approaches [5, 6] have
                                         cross-attention module adaptively integrates pre-trained acoustic       made notable progress, they still yield erroneous decisions, re-
                                         representations with linguistic features to support low-latency         sulting in excessive response latency, frequent interruptions, and
                                         prediction of hold vs. shift states. By sharing a frozen ASR            unnatural interaction dynamics that substantially degrade user
                                         encoder, JAL-Turn enables turn-taking prediction to run fully           experience. Therefore, there is an urgent need for real-time and
                                         in parallel with speech recognition, introducing no additional          robust turn-taking techniques.
                                         end-to-end latency or computational overhead. In addition, we                Traditional spoken dialogue systems typically rely on heuris-
                                         introduce a scalable data construction pipeline that automatically      tic, silence-based turn-taking strategies [1]. A common approach
                                         derives reliable turn-taking labels from large-scale real-world         is to wait for a fixed or adaptive duration of silence in the user’s
                                         dialogue corpora. Extensive experiments on public multilingual          speech before deciding that the turn of user has ended, and then
                                         benchmarks and an in-house Japanese customer-service dataset            process the input and generate a response. However, silence alone
                                         show that JAL-Turn consistently outperforms strong state-of-the-        is an unreliable cue for turn completion: users frequently produce
                                         art baselines in detection accuracy while maintaining superior          within-utterance pauses that do not signal a handover [3,7]. Previ-
                                         real-time performance.                                                  ous studies [8, 9] revealed that turn transitions in many languages
                                                                                                                 are rapid, often on the order of 100–500 ms, suggesting listeners
                                           Index Terms— Turn-taking detection, joint acoustic-linguistic         do not merely react to silences, but proactively anticipate upcom-
                                         modeling, full-duplex spoken dialogue system                            ing turn completions using a combination of lexical, prosodic,
                                                                                                                 and multimodal cues.
                                                                                                                      To this end, several works explored data-driven turn-taking
                                                                 1. INTRODUCTION                                 models based on linguistic34 or acoustic56 features. However,
                                                                                                                 due to stringent real-time constraints, these methods typically
                                         In recent years, the rapid proliferation of voice AI agents in appli-   adopt relatively simple model architectures, which limits their
                                         cations such as intelligent customer service, personal assistants,      ability to capture fine-grained discriminative cues and leaves
                                         and human–AI collaboration has substantially raised the demand          substantial room for improvement in both detection accuracy
                                         for natural and high-quality spoken interaction. Unlike traditional     and robustness. Motivated by recent success of large language
                                         dialogue systems, modern voice AI agents are often designed             models (LLMs) [10, 11] and speech language models (SLMs)
                                         for extremely low-latency responses and continuous listening,           [12, 13], numerous works [14–17] directly integrate full-duplex
                                         which makes them prone to intervening before users have fully           capabilities into LLM or SLM backbones. While such systems
                                         completed their utterances. In natural conversation, speakers           can improve detection quality, they exhibit several limitations that
                                         frequently exhibit thinking pauses, hesitations, and self-repairs,      hinder practical deployment. First, they require large amounts
                                         which do not necessarily indicate a turn completion. Overly ag-         of manually annotated dialogue data, which is expensive and
                                         gressive system responses under such conditions can lead to fre-
                                                                                                                 3 https://github.com/ten-framework/ten-turn-detection
                                         quent interruptions, disrupted conversational flow, and degraded        4 https://github.com/pipecat-ai/smart-turn/tree/main
                                                                                                                 5 https://github.com/pipecat-ai/smart-turn/tree/filipi/smart-turn
                                         * denotes equal contribution.
                                         † denotes the corresponding author.                                     6 https://github.com/inokoj/VAP-Realtime
time-consuming to obtain and difficult to scale across domains          schemes agree. This future-window design effectively suppresses
and languages. Second, their LLM or SLM backbones need                  backchannels: instantaneous VAD comparisons are easily con-
to support multiple functionalities, such as automatic speech           founded by brief listener responses, whereas future VAD patterns
recognition (ASR), which often introduces additional latency            provide more reliable cues for genuine turn transitions.
[17]. Moreover, this architecture inherently prioritizes semantic
information, thereby discarding fine-grained acoustic cues that         2.2. Context Construction
are crucial for accurate turn-taking detection, and consequently
suffers from notable performance degradation in complex real-           After labeling, training samples are extracted from each VAD
world scenarios.                                                        falling edge following a speech segment, which corresponds to
    In summary, this paper makes the following contributions:           natural turn-taking decision points. For each such point, we con-
                                                                        struct a context window by extending backward to the previous
    • We propose JAL-Turn, a lightweight speech-only turn-              long silence (duration ≥ 2 seconds) and then normalize it to
      taking model that jointly leverages pre-trained acoustic and      a fixed 10-second length through left-padding or truncation as
      linguistic encoders and supports parallel inference with          needed, ensuring that the window always includes a complete
      ASR through encoder sharing, enabling low-latency de-             preceding speech segment to provide sufficient semantic context
      ployment.                                                         for turn prediction.
    • We introduce a scalable data construction pipeline that
      automatically derives reliable turn-taking labels from large-     2.3. Dataset Generation
      scale real-world dialogue corpora without manual annota-          Applying this pipeline to 1,128 hours of in-house stereo con-
      tion, enabling effective training across domains and lan-         versational data yields approximately 2,299 hours of trainable
      guages.                                                           segments, with an estimated labeling accuracy of about 85%
    • We present extensive experiments on a public multilingual         based on manual inspection.
      benchmark and an in-house Japanese customer-service cor-              To further increase data diversity, we also incorporate a 95-
      pus, along with ablation and attribution analyses, demon-         hour in-house dataset in which each recording contains a single
      strating that JAL-Turn consistently outperforms strong            complete utterance spoken by one speaker (e.g. “My phone
      audio-only and LLM-based baselines while satisfying real-         number is 090-8987-2023”). Applying the same segmentation
      time constraints.                                                 procedure produces 749 hours of training segments, where all
                                                                        frames except the final one are labeled as Hold. Although this
                                                                        dataset achieves nearly 100% labeling accuracy, it lacks the con-
                      2. DATA PIPELINE                                  versational variability present in real dialogues.
                                                                            We therefore train our model on a mixture of both datasets,
To enhance the robustness of our turn-taking model, we develop          combining large-scale conversational dynamics with high-quality
an efficient data pipeline that automatically derives reliable train-   utterance-level supervision.
ing labels from large-scale real-world conversational corpora
without requiring any manual annotation.                                                        3. JAL-TURN
    Given stereo conversational audio, we first extract frame-
level voice activity detection (VAD) at 50 Hz. For each channel         As illustrated in Fig. 1, our proposed JAL-Turn framework pri-
c ∈ {0, 1}, we obtain a binary sequence vc = [vc1 , . . . , vcT ] ∈     marily comprises five components: 1) a dual-path encoder for
{0, 1}T , where vct = 1 indicates speech activity at frame t.           acoustic and semantic feature extraction, 2) a cross-attention-
                                                                        based fusion module for integrating heterogeneous representa-
2.1. Future-Window Labeling                                             tions, 3) a self-attention-based Transformer module for temporal
                                                                        modeling, 4) an attention pooling module for utterance-level tem-
Motivated by previous studies on future voice activity projec-          poral pooling, and 5) a binary classification head for hold/shift
tion [18], we employ a future-window strategy that leverages            prediction.
upcoming conversational dynamics. For each frame t, we com-
pute a weighted VAD score over a 2-second future window:
                                                                        3.1. Dual-Encoder Architecture
                               τ fs
                               X                                        In contrast to conventional single-encoder approaches that rely
                       stc =          w(i) vct+i ,               (1)
                                                                        on acoustic or linguistic cues, we adopt a dual-path encoder ar-
                               i=0
                                                                        chitecture to explicitly capture complementary aspects of the
where τ = 2 seconds, fs = 50 Hz, and w(i) is a non-negative             speech signal. Concretely, the primary encoder derives from the
weighting function. Three temporal weighting schemes—linear,            pretrained SenseVoice-Small [19] model, a multilingual speech
square-root, and exponential—independently assign Hold/Shift            foundation model based on a convolution-augmented transformer
labels (Hold if stc ≥ st1−c ), and a label is kept only when all        backbone [20, 21], which is particularly effective at extracting
                              Fig. 1: Overall training architecture of the proposed JAL-Turn framework.


high-level semantic and linguistic elements. The secondary en-                              Q = LayerNorm(h′l )                      (5)
coder is a pretrained contrastive predictive coding (CPC) model                           K/V = LayerNorm(h′a )                      (6)
[22], which emphasizes low-level acoustic regularities via self-
supervised contrastive learning.                                      where dk = d/H denotes the dimensionality of each head, and d
   Given an input waveform x ∈ R1×L , where L denotes the             and H denote the model dimension and the number of attention
waveform length, the two encoders produce frame-level feature         heads, which are set to 256 and 4, respectively. Each layer ad-
sequences:                                                            ditionally incorporates residual connections and a position-wise
                                                                      feed-forward network (FFN).
                hl = EncoderSense (x) ∈ RT1 ×d1 ,              (2)
                                           T2 ×d2                     3.3. Transformer-based Module
               ha = EncoderCPC (x) ∈ R              ,          (3)

where d1 = 512 and d2 = 256 denote the respective output di-          On top of the fused representation, we employ a causal self-
mensions. Both encoders are kept frozen during training in order      attention-based Transformer module. Notably, we adopt Atten-
to preserve their pre-trained knowledge. We then apply linear         tion with Linear Biases (ALiBi) [23] as the positional bias mech-
projection layers to map the features into a shared latent space.     anism, which replaces conventional absolute positional embed-
Overall, this design allows JAL-Turn to jointly exploit high-level    dings by adding a distance-dependent bias directly to the attention
linguistic cues from SenseVoice and fine-grained acoustic patterns    logits. The intuition behind is that ALiBi has been shown to im-
from CPC, yielding richer and more informative representations        prove length extrapolation and naturally encodes a recency bias,
for turn-taking detection.                                            which aligns well with the local temporal patterns that govern
    During training, both the CPC and SenseVoice encoders are         turn-taking behavior.
kept frozen. Importantly, the SenseVoice encoder is shared be-
tween ASR and JAL-Turn, enabling turn-taking predictions to be        3.4. Attention-based Temporal Pooling Module
computed synchronously with ASR during inference. This design         To obtain an utterance-level representation while allowing JAL-
avoids inserting any additional processing stages before or after     Turn to automatically focus on the most informative temporal
ASR decoding, allowing turn-taking decisions and transcriptions       segments, we apply a lightweight attention-based temporal pool-
to be obtained in parallel from a single forward pass of the shared   ing mechanism over the sequence of hidden states htt = 1T pro-
encoder.                                                              duced by the Transformer-like module. Specifically, we compute:

                                                                                        αt = softmax w⊤ ht + b
                                                                                                                   
3.2. Cross-Attention-based Fusion                                                                                                  (7)
                                                                                                       T
To effectively integrate the heterogeneous features produced by                                        X
the dual-path encoders, we introduce a cross-attention-based fu-                             hpool =         αt · h t                (8)
                                                                                                       t=1
sion module, enabling JAL-Turn to dynamically attend to the
most informative regions across different feature spaces.             where w ∈ Rd and b ∈ R are trainable parameters, and αt
    Concretely, the fusion module consists of L = 2 stacked           denotes the normalized attention weight for time step t.
cross-attention layers. In each layer, the SenseVoice features h′l
act as queries, while CPC features h′a serve as keys and values:      3.5. Classification Head and Training Objective
                                              QK⊤                     Given the pooled representation hpool ∈ Rd , we apply a
                                                   
         CrossAttn(Q, K, V) = softmax √               V       (4)     lightweight linear classification head to produce the shift logit
                                                 dk
ŷ ∈ R, parameterized by trainable weights wcls ∈ Rd and bias           fed into the LLMs for turn-state prediction; and (3) an SLM-
bcls ∈ R. The predicted probability is obtained via a sigmoid           based system, represented by EasyTurn [17], which performs
activation, and the final decision (hold vs. shift) is made using a     turn-taking detection using a speech language model backbone.
fixed threshold τ = 0.5.                                                GPT-5.1 and Gemini-2.5-Flash are evaluated via their official
     The model is trained end-to-end with the standard binary           APIs, whereas Qwen3-0.6B is fine-tuned on the training data and
cross-entropy objective over mini-batches, where y ∈ {0, 1}             served with vLLM10 [24] for efficient inference. All LLM-based
denotes the ground-truth turn label (1 for shift and 0 for hold).       experiments use the same prompt, provided in Appendix ??.


                          4. EXPERIMENTS
                                                                        4.2.1. Comparison with SLM-based Systems
4.1. Experimental Setups                                                We first compare JAL-Turn with representative strong baselines
4.1.1. Datasets                                                         on the Mandarin Easy-Turn corpus (Table 1). Here, Acccp ,
                                                                        Accincp , Accbc , and Accwait denote the turn-taking detection
To comprehensively assess the proposed method, we conduct               accuracy for the complete, incomplete, backchannel, and wait
experiments on the public Mandarin dataset Easy-Turn (approxi-          states, respectively (higher is better). JAL-Turn achieves the
mately 1145 hours), multilingual STurn-v35,6 dataset (containing        best performance on the cp state (96.67%) while operating at
approximately 700 hours of speech in 23 languages), and a large-        an extremely low end-to-end latency of 12 ms. Compared with
scale in-house corpus of real-world Japanese dialogues introduced       Paraformer [25]+TEN Turn Detection and STurn-v2, JAL-Turn
in the previous section.                                                yields markedly higher accuracy of the complete and incomplete
                                                                        states, and reduces latency from 204 ms / 27 ms to 12 ms.
    For Easy-Turn and STurn-v3, we use the original test set                Against EasyTurn, JAL-Turn attains comparable performance
for evaluation, while splitting the training set into training and      on incp and wait (within 4.0 and 6.0 points, respectively) and
validation sets with a 9:1 ratio. For the in-house Japanese corpus,     slightly improves cp accuracy (96.67% vs. 96.33%). However,
we partition all in-house data into training and validation sets        JAL-Turn underperforms on the bc state (80% vs. 91%), which
using the same 9:1 split as well. Regarding the test set, we            we conjecture stems from the intrinsically context-dependent na-
additionally collected 500 samples from real-world business data        ture of backchannels: they are often short, semantically light
for evaluation which are labeled by human. These data covered           responses whose role is better determined with explicit lexi-
various attributes such as gender, age, and business scenario to        cal/semantic cues. Crucially, despite this gap on bc, JAL-Turn
ensure a comprehensive evaluation of the proposed method.               offers a substantially more favorable quality–latency trade-off
                                                                        overall, delivering competitive state-wise accuracy under strict
                                                                        real-time constraints.
4.1.2. Implementation Details
In all experiments, JAL-Turn is trained end-to-end using a single       4.2.2. Comparison with Audio-only Methods
H100 GPU for 10 epochs within the PyTorch framework. We use
the AdamW optimizer with an initial learning rate of 1 × 10−4 ,         As shown in Tables 2 and 3, JAL-Turn consistently achieves the
a weight decay of 0.001, and a batch size of 64. The learning           best detection accuracy and F1-score among audio-only meth-
rate is scheduled using a cosine annealing strategy, decaying to a      ods on both the public multilingual benchmark and the in-house
minimum value of 1 × 10−6 .                                             Japanese corpus. On the public STurn benchmark, JAL-Turn
    Regarding evaluation metrics, we use accuracy and F1-score          attains 93.27% accuracy and 0.934 F1, providing small but con-
for turn-taking detection. In addition, we use latency to quantify      sistent relative gains of approximately 0.2% in accuracy and 0.3%
the responsiveness of the system in full-duplex scenarios.              in F1 over STurn-v3, while outperforming STurn-v2 by about
                                                                        43% relative accuracy and 38% relative F1. On the in-house
                                                                        Japanese corpus, the improvements are much more substantial:
4.2. Main Results                                                       JAL-Turn reaches 92.03% accuracy and 0.925 F1, corresponding
                                                                        to relative gains of roughly 25.6% accuracy and 24.8% F1 over
To comprehensively assess the proposed approach, we evaluate
                                                                        STurn-v3 (73.29%, 0.741), and about 41.3% accuracy and 36.2%
JAL-Turn against three categories of baselines on two public mul-
                                                                        F1 over STurn-v2 (65.12%, 0.679).
tilingual benchmarks and an in-house Japanese corpus. Specifi-
                                                                            In terms of efficiency, STurn-v3 achieves the lowest latency
cally, we consider: (1) audio-only methods, including STurn-v2
                                                                        on both benchmarks (12 ms and 23 ms), but JAL-Turn still op-
and STurn-v3; (2) LLM-based pipelines, including GPT-5.17 ,
                                                                        erates comfortably within the real-time regime, with end-to-end
Qwen3-0.6B8 , and Gemini-2.5-Flash9 , where SenseVoice is first
used to produce ASR transcripts and the resulting text is then          7 https://openai.com/zh-Hans-CN/index/gpt-5-1
                                                                        8 https://huggingface.co/Qwen/Qwen3-0.6B
5 https://huggingface.co/datasets/pipecat-ai/smart-turn-data-v3-train   9 https://poe.com/Gemini-2.5-Flash
6 https://huggingface.co/datasets/pipecat-ai/smart-turn-data-v3-test    10 https://github.com/vllm-project/vllm
                Table 1: Performance comparison of turn-taking detection methods on Mandarin Easy-Turn corpus.
                                 Model                 Acccp Accincp Accbc Accwait Latency (ms)
                    Paraformer+TEN Turn Detection 86.67           89.3       -       91          204
                                STurn-v2               78.67       62        -        -           27
                                Easy-Turn              96.33     97.67      91       98          263
                                JAL-Turn               96.67     93.67      80       92           12


Table 2: Performance comparison of audio-only turn-taking de-        detection quality of substantially heavier LLM-based pipelines,
tection methods on multilingual STurn-v3.                            but also offers an order-of-magnitude lower response latency
            Model      Acc       F1    Latency (ms)                  and avoids the additional overhead of full ASR decoding and
          STurn-v2 65.12 0.679             149                       large-scale language model inference, making it a lightweight yet
          STurn-v3 93.10 0.931              12                       competitive alternative for real-time full-duplex dialogue systems.
          JAL-Turn 93.27 0.934              36

Table 3: Performance comparison of audio-only turn-taking de-
tection methods on in-house Japanese corpus.                         4.3. Ablation Studies
            Model      Acc      F1     Latency (ms)
          STurn-v2 55.46 0.427             140                       To assess the contribution of each component in JAL-Turn, we
          STurn-v3 71.94 0.736               13                      conduct ablation experiments on the in-house Japanese corpus,
          JAL-Turn 92.03 0.925               38                      as summarized in Table 5.

                                                                     Table 5: Ablation studies of the proposed JAL-Turn. w/o
latencies of 22 ms on the public dataset and 43 ms on the in-house   CrossATT denotes using concatenation, w/o ATTPooling rep-
corpus. Compared with the older STurn-v2 system, JAL-Turn            resents using the last layer feature.
not only delivers dramatically higher accuracy and F1, but also
reduces latency by about 85% on the public benchmark (149 ms                     Model           Acc       F1     Latency (ms)
→ 22 ms) and by roughly 69% on the in-house corpus (138 ms                     JAL-Turn         92.03    0.925          38
→ 43 ms). These results demonstrate that the proposed joint                    w/o Sense        72.01    0.698          12
acoustic–linguistic modeling paradigm effectively integrates fine-             w/o CPC          84.18    0.839          26
grained acoustic and linguistic cues, yielding clearly superior              w/o CrossATT       88.59    0.873          41
detection quality while maintaining low end-to-end latency suit-            w/o ATTPooling      90.23    0.895          48
able for deployment in real-time dialogue systems.

4.2.3. Comparison with LLM-based Methods                                 Removing either encoder leads to a clear degradation in de-
                                                                     tection performance. Dropping the SenseVoice encoder (w/o
As shown in Table 4, JAL-Turn also compares favorably with           Sense) causes accuracy to fall from 92.03% to 72.01% and F1
LLM-based turn-taking detectors on the in-house benchmark.           from 0.925 to 0.698, indicating that linguistically enriched repre-
                                                                     sentations are the primary driver of performance. Removing the
Table 4: Performance comparison of JAL-Turn against LLM-
                                                                     CPC encoder (w/o CPC) is less catastrophic but still non-trivial,
based turn-taking detection methods on the in-house benchmark.
                                                                     reducing accuracy to 84.18% and F1 to 0.839. This shows that
       Model                Acc       F1       Latency (ms)          CPC contributes complementary fine-grained acoustic cues that
  Gemini-2.5-Flash         76.91     0.817         595               further enhance robustness.
    Qwen3-0.6B             78.70     0.782          124                  Eliminating the cross-attention module (w/o CrossATT) while
      GPT-5.1              85.52     0.874         1205              retaining both encoders also results in a noticeable drop, to
     JAL-Turn              92.03     0.925           38              88.59% accuracy and 0.873 F1. This confirms that explicitly
                                                                     modeling interactions between acoustic and linguistic streams is
    Compared with Gemini-2.5-Flash and Qwen3-0.6B, JAL-              more effective than simply co-presenting their features.
Turn improves accuracy by 15.1 and 13.3 absolute points (92.03%          Finally, removing the attention-based temporal pooling (w/o
vs. 76.91% / 78.70%), respectively, and increases F1 by 0.108 and    ATTPooling) leads to a moderate degradation in performance
0.143, while reducing latency from 595 ms and 124 ms to only         (90.23% accuracy and 0.895 F1) and simultaneously increases
38 ms. Relative to GPT-5.1, JAL-Turn further raises accuracy         latency from 38 ms to 48 ms. Thus, the proposed lightweight
from 85.52% to 92.03% and F1 from 0.874 to 0.925, and lowers         attention pooling not only yields more informative utterance-
latency by more than a factor of five (205 ms → 38 ms). These        level representations, but also provides a better accuracy–latency
results indicate that JAL-Turn not only matches or surpasses the     trade-off than simpler temporal aggregation schemes.
4.4. Analysis                                                         4.4.2. Temporal-Level Contribution

To investigate how the proposed model exploits acoustic and lin-      To further analyze how the model allocates attention over time,
guistic cues for turn-taking prediction, we analyze both encoder-     we perform position-regularized temporal attribution using the
level and temporal-level contributions on the STurn-v3 and our        gradient–input product. Temporal contribution scores are pro-
in-house Japanese test sets. We adopt a unified gradient-based        jected onto a normalized 0–100% axis to facilitate direct compar-
attribution framework to quantify representation-level contribu-      ison across variable-length utterances.
tions, complemented by controlled encoder ablations to assess             Across all three languages, contributions from the SenseVoice
the functional role of each information source.                       encoder exhibit a consistent monotonic increase toward the end
                                                                      of the utterance, revealing a strong bias toward utterance-final
                                                                      regions for turn-taking prediction (Fig. 3). However, the degree
4.4.1. Encoder-Level Contribution                                     of temporal concentration varies substantially across languages.
                                                                      In Japanese, the majority of the SenseVoice contribution is con-
For each sample, we backpropagate the classification score to         centrated within the final 5% of the audio context. In contrast,
the encoder outputs and compute encoder-wise scores via the           Chinese shows a broader concentration around the final 10%,
element-wise gradient–activation product. The contribution ratio      while English displays a more gradual accumulation, with peak
for encoder i is defined as                                           contributions occurring around the final 25% of the utterance.
                                                                          This temporal localization reflects language-specific turn-
                          ∥∇xi ⊙ xi ∥2
                    ρi = P               ,                            completion mechanisms. In Japanese, turn-taking cues are tightly
                          j ∥∇xj ⊙ xj ∥2                              associated with utterance-final phonetic structures and sentence-
                                                                      final morphemes, such as polite-form endings (e.g., “-masu” and
where xi denotes the output features of encoder i. We group           “-desu”), which are fully realized only in Shift instances. As a
samples into four duration bins: 0–3 s, 3–6 s, 6–9 s, and >9 s.       result, the model exhibits highly concentrated attention near the
                                                                      end of the utterance, particularly for Shift predictions. In contrast,
                                                                      English relies more heavily on anticipatory prosodic patterns that
                                                                      unfold over a longer temporal span, while Chinese again occupies
                                                                      an intermediate position.
                                                                          Notably, the CPC encoder does not exhibit a comparable tem-
                                                                      poral bias. Its contribution remains relatively uniform across
                                                                      the entire utterance for all three languages, indicating that low-
                                                                      level acoustic representations primarily capture global prosodic
                                                                      characteristics rather than temporally localized turn-completion
                                                                      cues. Together, these findings suggest that SenseVoice is re-
                                                                      sponsible for modeling temporally localized, language-dependent
                                                                      turn-taking signals, whereas CPC provides complementary, glob-
                                                                      ally distributed acoustic information. Across languages, these
                                                                      findings further imply that SenseVoice, as an ASR encoder, pri-
                                                                      marily encodes rich phonetic and sub-lexical information, rather
                                                                      than high-level semantic representations in the traditional sense.
                                                                      Although its overall contribution is relatively smaller, CPC com-
Fig. 2: Encoder-wise contribution ratios across utterance dura-       plements SenseVoice by encoding broader prosodic variations
tions for SenseVoice (left) and CPC (right).                          that are not fully captured by ASR-style encoders, thereby enrich-
                                                                      ing the model’s representation space along additional acoustic
     As shown in Fig. 2, SenseVoice clearly dominates across all      dimensions.
bins, with ρSense increasing from roughly 0.78 (0–3 s) to 0.90 (6–9
s), indicating that linguistically enriched representations are the
primary driver of turn-taking decisions and become even more                                 5. CONCLUSION
influential for longer contexts. CPC exhibits complementary but
smaller contributions, with ρCPC decreasing from about 0.22 (0–3      In this study, we present JAL-Turn, a lightweight and robust
s) to 0.10 (6–9 s) as duration grows, suggesting that prosodic        turn-taking detection framework for full-duplex spoken dialogue
and low-level acoustic cues are most useful for short utterances      systems. By jointly and adaptively modeling acoustic and lin-
when semantic context is limited. Overall, this reveals a length-     guistic elements of the given utterance, together with lightweight
dependent division of labor: SenseVoice provides the dominant         transformer and temporal attention pooling modules, JAL-Turn
semantic signal, while CPC supplies auxiliary acoustic evidence,      supports low-latency and accurate prediction of turn taking de-
particularly in short-context scenarios.                              cisions. A scalable data construction pipeline further enables
Fig. 3: Temporal-level attribution heatmap of three language (normalized to 0–100%). The upper and lower rows correspond to
SenseVoice and CPC encoders, respectively. Red dashed lines indicate the boundary between Hold and Shift samples.


automatic extraction of reliable turn-taking labels from large-                         6. REFERENCES
scale real-world corpora. Experiments on multilingual public
benchmarks and an in-house Japanese customer-service dataset       [1] G. Skantze, “Turn-taking in conversational systems and
show that JAL-Turn consistently outperforms strong baselines in        human-robot interaction: a review,” Computer Speech &
both accuracy and robustness while maintaining real-time perfor-       Language, vol. 67, p. 101178, 2021.
mance.                                                             [2] Y. Pan, Y. Yang, Y. Huang, et al., “Gmp-tl: Gender-
                                                                       augmented multi-scale pseudo-label enhanced transfer learn-
                                                                       ing for speech emotion recognition,” in 2024 IEEE Spoken
                                                                       Language Technology Workshop (SLT). IEEE, 2024, pp.
                                                                       496–501.
                                                                   [3] K. Inoue, B. Jiang, E. Ekstedt, et al., “Real-time and contin-
                                                                       uous turn-taking prediction using voice activity projection,”
                                                                       arXiv preprint arXiv:2401.04868, 2024.
                                                                   [4] Y. Pan, Y. Hu, Y. Yang, et al., “ClapFM-EVC: High-Fidelity
                                                                       and Flexible Emotional Voice Conversion with Dual Control
                                                                       from Natural Language and Speech,” in Interspeech 2025,
                                                                       2025, pp. 4583–4587.
                                                                   [5] N. Gu, K. Lee, M. Basha, et al., “Positive transfer of the
                                                                       whisper speech transformer to human and animal voice ac-
                                                                       tivity detection,” in ICASSP 2024-2024 IEEE International
                                                                       Conference on Acoustics, Speech and Signal Processing
                                                                       (ICASSP). IEEE, 2024, pp. 7505–7509.
                                                                   [6] G. Skantze and B. Irfan, “Applying general turn-taking
                                                                       models to conversational human-robot interaction,” in 2025
                                                                       20th ACM/IEEE International Conference on Human-Robot
                                                                       Interaction (HRI). IEEE, 2025, pp. 859–868.
                                                                   [7] A. R. Majlesi, R. Cumbal, O. Engwall, et al., “Managing
     turn-taking in human-robot interactions: the case of pro-             Acoustics, Speech and Signal Processing (ICASSP). IEEE,
     jections and overlaps, and the anticipation of turn design            2023, pp. 1–5.
     by human participants,” Social Interaction. Video-based          [22] M. Riviere, A. Joulin, P.-E. Mazaré, et al., “Unsupervised
     Studies of Human Sociality, vol. 6, no. 1, 2023.                      pretraining transfers well across languages,” in ICASSP
 [8] T. Stivers, N. J. Enfield, P. Brown, et al., “Universals and          2020-2020 IEEE International Conference on Acoustics,
     cultural variation in turn-taking in conversation,” Proceed-          Speech and Signal Processing (ICASSP). IEEE, 2020, pp.
     ings of the National Academy of Sciences, vol. 106, no. 26,           7414–7418.
     pp. 10 587–10 592, 2009.                                         [23] O. Press, N. A. Smith, and M. Lewis, “Train short, test long:
 [9] K. Inoue, B. Jiang, E. Ekstedt, et al., “Multilingual turn-           Attention with linear biases enables input length extrapola-
     taking prediction using voice activity projection,” in Pro-           tion,” in ICLR, 2022.
     ceedings of the 2024 joint international conference on com-      [24] W. Kwon, Z. Li, S. Zhuang, et al., “Efficient memory man-
     putational linguistics, language resources and evaluation             agement for large language model serving with pagedatten-
     (LREC-COLING 2024), 2024, pp. 11 873–11 883.                          tion,” in Proceedings of the ACM SIGOPS 29th Symposium
[10] J. Bai, S. Bai, Y. Chu, et al., “Qwen technical report,” arXiv        on Operating Systems Principles, 2023.
     preprint arXiv:2309.16609, 2023.                                 [25] Z. Gao, S. Zhang, I. McLoughlin, et al., “Paraformer:
[11] J. Achiam, S. Adler, S. Agarwal, et al., “Gpt-4 technical             Fast and accurate parallel transformer for non-
     report,” arXiv preprint arXiv:2303.08774, 2023.                       autoregressive end-to-end speech recognition,” arXiv
[12] Q. Fang, S. Guo, Y. Zhou, et al., “Llama-omni: Seam-                  preprint arXiv:2206.08317, 2022.
     less speech interaction with large language models,” arXiv
     preprint arXiv:2409.06666, 2024.
[13] Y. Pan, Y. Yang, Y. Hu, et al., “S2st-omni: An efficient and
     scalable multilingual speech-to-speech translation frame-
     work via seamlessly speech-text alignment and streaming
     speech decoder,” arXiv preprint arXiv:2506.11160, 2025.
[14] A. Défossez, L. Mazaré, M. Orsini, et al., “Moshi: a
     speech-text foundation model for real-time dialogue,” arXiv
     preprint arXiv:2410.00037, 2024.
[15] W. Yu, S. Wang, X. Yang, et al., “Salmonn-omni: A codec-
     free llm for full-duplex speech understanding and genera-
     tion,” arXiv preprint arXiv:2411.18138, 2024.
[16] Q. Zhang, L. Cheng, C. Deng, et al., “Omniflatten: An
     end-to-end gpt model for seamless voice conversation,” in
     Proceedings of the 63rd Annual Meeting of the Association
     for Computational Linguistics (Volume 1: Long Papers),
     2025, pp. 14 570–14 580.
[17] G. Li, C. Wang, H. Xue, et al., “Easy turn: Integrating
     acoustic and linguistic modalities for robust turn-taking
     in full-duplex spoken dialogue systems,” arXiv preprint
     arXiv:2509.23938, 2025.
[18] E. Ekstedt and G. Skantze, “Voice activity projection: Self-
     supervised learning of turn-taking events,” arXiv preprint
     arXiv:2205.09812, 2022.
[19] K. An, Q. Chen, C. Deng, et al., “Funaudiollm: Voice
     understanding and generation foundation models for natu-
     ral interaction between humans and llms,” arXiv preprint
     arXiv:2407.04051, 2024.
[20] A. Gulati, J. Qin, C.-C. Chiu, et al., “Conformer:
     Convolution-augmented transformer for speech recognition,”
     arXiv preprint arXiv:2005.08100, 2020.
[21] Y. Yang, Y. Pan, J. Yin, et al., “Hybridformer: Improving
     squeezeformer with hybrid attention and nsr mechanism,”
     in ICASSP 2023-2023 IEEE International Conference on

