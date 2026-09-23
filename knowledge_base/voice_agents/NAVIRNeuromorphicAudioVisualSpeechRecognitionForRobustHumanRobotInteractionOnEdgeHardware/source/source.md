# NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware
Source: http://arxiv.org/abs/2609.24391v1
Kind: pdf
Fetched: 2026-09-22T08:32:56.106504+00:00
Tool: pdftotext

                      NAVIR: Neuromorphic Audio-Visual Speech
                      Recognition for Robust Human–Robot Interaction
                      on Edge Hardware
                      LEONIDAS DELIMPASIS1 , PANAGIOTA MORAITI2 , ANTONIS PORICHIS3 , PANOS CHATZAKOS2,3 ,
                      and MICHAIL KARAMOUSADAKIS1
                      1
                           Plaixus Ltd., Spyrou Patsi 62, 11855, Athens, Greece
                      2
                           Tech Hive Labs, 280 Kifisias Ave., 152 32 Halandri, Greece
                      3
                           AI Innovation Centre, University of Essex, Little Abington, CB21 6GP Cambridge, U.K.
                      Corresponding author: Leonidas Delimpasis (e-mail: leonidasd@disroot.org).
                      This work was carried out within the NAVIR project, which received funding from the European Union’s Horizon Europe Research and




arXiv:2609.24391v1 [cs.LG] 21 Sep 2026
                      Innovation Programme (dAIEDGE) under Grant Agreement No. 101120726.




                                         ABSTRACT Voice-controlled interaction in industrial settings is hampered by acoustic noise, which severely
                                         degrades audio-only speech recognition. Audio-visual speech recognition (AVSR) addresses this by fusing
                                         lip-motion cues with the audio stream, but state-of-the-art pipelines rely on three-dimensional convolutions,
                                         recurrent units, and attention modules that exceed the budget of typical edge devices. We present NAVIR, an
                                         end-to-end AVSR system targeting the BrainChip Akida neuromorphic processor, which natively supports
                                         only sequential two-dimensional convolutional inference. The pipeline factorises spatial and temporal
                                         encoding into separate AkidaNet-based modules: a per-frame visual encoder, a temporal video encoder,
                                         and a spectrogram audio encoder, fused by a lightweight predictor head and decoded by constrained beam
                                         search. Models are trained with connectionist temporal classification on noise-augmented audio and then
                                         fine-tuned with quantization-aware training. On the GRID benchmark, the quantized audio-visual model
                                         reaches 14.0% word error rate (WER) under noise on the unseen-speaker split and 3.3% WER on the
                                         overlapped-speaker split, against 22.5% and 11.8% for audio-only baselines, and it attains 98.6% command
                                         accuracy at 1.5% WER on a task-specific industrial-command corpus. Operation-count analysis indicates a
                                         13-fold energy advantage of the spiking formulation over its artificial neural network counterpart at 27.6%
                                         mean firing rate. On-board measurements show roughly 5-fold lower energy per inference than a Raspberry
                                         Pi central processing unit on the lip-reading model, and over 100-fold lower than a laptop graphics processing
                                         unit, while sustaining 14.5 inferences per second. To the best of our knowledge, this is the first complete
                                         multimodal AVSR pipeline running on neuromorphic hardware of this class.


                                         INDEX TERMS Akida, audio-visual speech recognition, BrainChip, edge computing, energy efficiency,
                                         human-robot interaction, lip reading, neuromorphic hardware, spiking neural networks.

                        I. INTRODUCTION                                                                              Modern high-accuracy AVSR pipelines, however, rely
                                                                                                                  on three-dimensional convolutions, attention-based encoders,
                      S    PEECH is one of the most natural modalities for human-
                           machine interaction, yet its deployment in industrial
                      environments remains limited because acoustic noise from
                                                                                                                  conformer back-ends or large transformer language mod-
                                                                                                                  els. These architectural choices implicitly assume GPU-class
                      machinery, ventilation and ambient activity sharply degrades                                hardware and are difficult to deploy on the embedded, battery-
                      the performance of audio-only automatic speech recognition                                  powered or thermally constrained platforms found in mobile
                      (ASR). Workers therefore fall back on manual interfaces such                                robotics. This creates a tension between recognition perfor-
                      as keypads, touchscreens or physical switches, which slow                                   mance and deployment feasibility that is central to embedded
                      workflows and can compromise safety in tasks that require                                   multimodal speech interfaces.
                      both hands free. The human perceptual system mitigates this                                    Neuromorphic processors offer a promising route through
                      fragility by integrating the visual appearance of the speaker’s                             this tension. Inspired by biological neural systems, they pro-
                      mouth, an effect captured most vividly by the McGurk illu-                                  cess sparse, event-driven binary spikes rather than dense
                      sion [1]. Audio-visual speech recognition (AVSR) systems                                    floating-point activations, so that energy consumption scales
                      aim to exploit the same redundancy and have been shown                                      with network activity rather than nominal compute capacity.
                      to deliver substantial robustness gains at low signal-to-noise                              The BrainChip AKD1000 is a commercially available neuro-
                      ratios.                                                                                     morphic system-on-chip that natively executes convolution-

                                                                                                                                                                              1
                                                L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




based spiking neural networks (SNNs) compiled via the                   SNNs, by virtue of their event-driven binary computation, can
Akida MetaTF/CNN2SNN toolchain. It connects to a host                   in principle replace energy-intensive multiply-accumulate
platform, in our case a Raspberry Pi 5, via PCIe, with total            (MAC) operations with sparse synaptic accumulate (AC) op-
system draw in the 350–430 mWh band over a five-minute                  erations, achieving substantial reductions in power consump-
inference session. Despite growing interest in neuromorphic             tion.
computing for sensor-level event detection and gesture recog-              Early convolutional SNN architectures established the fea-
nition, its application to multi-stream temporally structured           sibility of directly training deep spiking networks via surro-
tasks such as AVSR has not previously been demonstrated at              gate gradients. The spatio-temporal backpropagation frame-
the system level.                                                       work of Wu et al. [3] unrolled leaky integrate-and-fire dy-
   Contributions. The NAVIR project closes this gap with the            namics across time and approximated the non-differentiable
following contributions.                                                spike function with a smooth surrogate. Deep residual SNNs
   • An end-to-end AVSR pipeline that satisfies the strict              followed: SEW-ResNet [4] and MS-ResNet [5] demonstrated
      architectural constraints of the AKD1000 (no 3D convo-            that residual connections could be applied within spiking net-
      lutions, no recurrent layers, no attention, fixed quantiza-       works, with membrane-shortcut designs guaranteeing strictly
      tion) by factorising spatial and temporal encoding into           binary spike communication and thus efficient hardware de-
      separate AkidaNet-based stages.                                   ployment.
   • A constrained beam-search decoder that exploits the                   To bridge the energy and accuracy gap with transformer-
      known grammar of the target vocabulary to guarantee               based ANNs, Spikformer [6] introduced spiking self-
      grammatically valid output and reduce the search space            attention with binary query, key and value tensors. The Spike-
      at inference time.                                                driven Transformer [7] pushed this further by redesigning at-
   • Noise-robust training through aggressive Urban-                    tention as a mask-and-add operation, reducing all components
      Sound8K augmentation, demonstrating consistent mul-               to sparse addition.
      timodal robustness gains over audio-only baselines on                Beyond classification, SNNs have been extended to time
      the GRID benchmark and on an internal industrial-                 series [8] and to audio-visual settings. He et al. [9] propose
      command corpus.                                                   the S-CMRL framework, combining cross-modal comple-
   • A theoretical and practical energy analysis comparing              mentary attention with semantic-alignment loss. Li et al. [10]
      our SNN against state-of-the-art (SOTA) artificial neural         introduce a Tucker-fusion transformer to couple binary spike
      network (ANN) lip readers using the operation-count               sequences with floating-point representations. Liu et al. [11]
      framework with Horowitz’s 45 nm CMOS energy con-                  take a human-inspired approach using dynamic-vision-sensor
      stants [2], and against CPU- and GPU-based inference              lip events as cues for cross-modal attention. These archi-
      via on-board power measurements.                                  tectures grapple with ensuring the full network operates in
   • An interactive demonstration coupling the pipeline to              a spike-driven manner. The AKD1000 imposes a stricter
      a uFactory xArm 6 robotic arm, providing closed-loop              regime, since it supports only sequential convolutional in-
      validation from voice command to physical action on               ference, precluding recurrence and attention. We therefore
      commodity embedded hardware.                                      build on the convolutional SNN literature and treat spike
   The remainder of the paper is organised as follows.                  encoder design and firing-rate control as the primary levers
Section II reviews neuromorphic SNN architectures, prior                for accuracy and energy.
AKD1000 applications and the GRID lip-reading state of
the art. Section III describes the NAVIR architecture and               B. APPLICATIONS OF THE BRAINCHIP AKD1000
decoding strategy. Section IV introduces the two evaluation             The AKD1000 is a first-generation digital neuromorphic
corpora, and Section V the experimental setup. Recognition              system-on-chip whose architecture supports the conversion
results are reported in Section VI, followed by the energy and          of pre-trained CNNs into SNN-compatible models via the
power analysis in Section VII. Section VIII presents the robot          MetaTF/CNN2SNN toolchain. Lunghi et al. [12] provide
demonstration system, Section IX discusses limitations and              the most rigorous quantitative evaluation to date in a space-
future work, and Section X concludes. Appendix A explains a             applications context, reporting EuroSAT inference energies
hardware-mapping behaviour of the AKD1000 toolchain that                of 0.63–1.38 mJ per frame at 0.66–1.41 ms latency for 4-
affects the audio-video deployment, and Appendix B details              bit-quantized CNNs. They also identify a 911 mW idle floor
the layer composition of every module.                                  that dominates the runtime budget on resource-constrained
                                                                        platforms. Chemnitz and Ermis [13] compare the AKD1000
II. RELATED WORK                                                        directly to an NVIDIA GTX 1080 and report 99.5% lower
A. NEUROMORPHIC ARCHITECTURES FOR SPIKING                               energy and 76.7% lower latency on a GXNOR MNIST
NEURAL NETWORKS                                                         classifier, with the energy advantage maintained but the la-
The development of hardware-compatible SNN architectures                tency margin shrinking on a YOLOv2 detector. Lenz and
has accelerated alongside the maturation of neuromorphic                McLelland [14] apply the AKD1000 to maritime ship detec-
processors such as Intel Loihi, IBM TrueNorth and Brain-                tion in satellite imagery via a two-stage AkidaNet/YOLOv5
ScaleS. The motivation across this body of work is that                 pipeline, reducing total energy to less than a quarter of a
2
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




Jetson-Nano-only baseline. Benoot et al. [15] integrate the                   TABLE 1. State-of-the-art lip-reading WER on the GRID corpus. All
                                                                              baselines use full 3D convolutions, recurrent layers or attention, none of
AKD1000 (and the forthcoming AKD1500) into a heteroge-                        which are supported on AKD1000.
neous on-board satellite data-processing unit. In the biomedi-
cal domain, Lutes et al. [16] exploit on-chip edge learning for                          Model              Year      Setting      WER (%)
individualised braking-intent EEG classification, and Bråt-
                                                                                         LipNet [28]       2016     Overlapped        4.80
man and Dow [17] characterise edge-learning hyperparame-                                 WLAS [29]         2017     Overlapped        3.00
ters for intracranial-pathology CT classification. Across these                          LCANet [30]       2018     Overlapped        2.90
works, the AKD1000 consistently delivers strong energy ad-                               LipSound [31]     2019     Overlapped        2.50
                                                                                         DualLip [32]      2020     Overlapped        2.71
vantages on lightweight, sparse inference, while its primary                             HLR-Net [33]      2021     Overlapped        3.30
limits are single-node model capacity, the high idle floor and                           LCSNet [34]       2023     Overlapped        2.30
constraints on architectural primitives.                                                 Wu et al. [35]    2024     Overlapped        1.83
                                                                                         LipNet [28]       2016       Unseen          11.40
C. AVSR DATASETS AND AUDIO-ONLY SNN BENCHMARKS                                           HLR-Net [33]      2021       Unseen           9.70
                                                                                         Wu et al. [35]    2024       Unseen          10.21
The GRID corpus [18] is the standard sentence-level bench-
mark for lip reading. LRW [19], LRS2 [20], LRS3 [21],
TCD-TIMIT [22], AVSpeech [23] and ASPIRE [24] extend
                                                                              AVSR fusion on GRID under noisy audio conditions, present-
coverage to in-the-wild sentences and noisy conditions. On
                                                                              ing both a gap in the literature and a relevant comparison point
the SNN side, DVS-Lip-Audio [25] provides event-based
                                                                              for any neuromorphic approach.
audio-visual lip data, while SHD/SSC [26] and the broader
Speech Commands corpus [27] provide audio-only bench-
                                                                              III. PROPOSED SYSTEM
marks. Detailed descriptions of the corpora used in this work
                                                                              A. ARCHITECTURE OVERVIEW
are deferred to Section IV.
                                                                              The system takes as input the cropped lip region of a speaker,
D. LIP READING ON THE GRID CORPUS                                             extracted from video using the off-the-shelf MediaPipe Face
Published evaluation on GRID is almost exclusively visual-                    Mesh model, alongside the corresponding audio signal. From
only. LipNet [28] established the modern baseline by com-                     these two streams, the model produces spoken-word pre-
bining three-dimensional spatio-temporal CNNs with bidi-                      dictions at the clip level through a multi-stage audio-visual
rectional GRUs and connectionist temporal classification                      pipeline shown in Figure 1.
(CTC) loss, mapping mouth-region frames directly to char-
acter sequences and achieving 4.8% WER on the overlapped                      B. ALIGNED WINDOWING
split (11.4% WER unseen-speaker). The Watch, Listen, At-                      Raw video frames and audio are first segmented into over-
tend, and Spell (WLAS) architecture [29] added attention-                     lapping clips using a sliding window. The video window is
based sequence-to-sequence decoding and curriculum learn-                     parameterised by its size in frames and a step size, set to
ing, reaching 3.0% WER. LCANet [30] addressed CTC’s                           roughly one third of the window size so adjacent windows
conditional-independence assumption via cascaded attention-                   share substantial overlap. This avoids missed words at bound-
CTC decoding, reaching 2.9% WER. LipSound [31] recon-                         aries and produces a dense sequence of clip-level predictions
structed the mel-spectrogram from lip video and ran ASR on                    that the decoder later aggregates.
the result, reaching 2.5% WER. DualLip [32] introduced a                          The audio (spectrogram) window is treated as an indepen-
generation/recognition dual learning scheme. HLR-Net [33]                     dent hyperparameter. It is expressed in spectrogram time bins
combined inception modules with attention-CTC, reaching                       and is in general not equal to the video window size, since
3.3% WER overlapped and 9.7% WER unseen-speaker. LC-                          the two streams are sampled at different rates and the optimal
SNet [34] added channel-attention and selective-feature fu-                   acoustic context may differ from the optimal visual context.
sion, reaching 2.3% WER. Most recently, the landmark-                         To keep the modalities synchronised at the predictor input,
guided cross-speaker model of Wu et al. [35], built on a hybrid               every audio window is centre-aligned with its corresponding
CTC/attention conformer back-end with mutual-information                      video window. Concretely, given a video window centred
regularisation, reached 1.83% WER overlapped and 10.21%                       at time tc , the audio window is taken as the spectrogram
WER on the unseen-speaker split. These results are sum-                       segment of the configured length whose centre also lies at
marised in Table 1.                                                           tc , regardless of the relative widths of the two windows. This
   Several trends are noteworthy. First, attention-augmented                  decoupling lets the audio context be widened or narrowed
decoders consistently improve over CTC alone by better                        without changing the video tiling, while preserving a one-
modelling output dependencies. Second, the visual front-end                   to-one temporal correspondence between video and audio
remains a primary bottleneck, and methods that improve it                     embeddings at the fusion stage.
through channel attention, landmark localisation or interme-
diate acoustic reconstruction yield large gains. Third, the                   C. FRAME-LEVEL VISUAL ENCODING
gap between overlapped and unseen-speaker performance                         Each frame in a clip is independently encoded into a com-
remains substantial. Finally, no published results exist for full             pact embedding using an AkidaNet-based CNN, an archi-
                                                                                                                                                           3
                                                   L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




FIGURE 1. NAVIR audio-visual pipeline. Aligned video and audio windows are independently encoded by AkidaNet-based per-frame, temporal-video and
spectrogram-audio encoders. Embeddings are concatenated and fed to an MLP predictor head, whose CTC output is decoded by constrained beam search.
All blocks are AKD1000-compatible (no 3D convolutions, recurrence or attention).



tecture purpose-designed for the BrainChip Akida hardware.                    The beam search maintains the top-B active hypotheses,
Processing frames individually rather than as a volumet-                   each represented as a partial token prefix and an accumulated
ric sequence is a deliberate architectural choice, since the               score. At each frame, three transition types are considered:
AKD1000 does not support 3D convolutions, recurrent con-                   emitting a blank or silence token (prefix unchanged), repeat-
nections or attention. Factorising encoding into a spatial stage           ing the last emitted token (absorbing duplicate frame predic-
(per frame) and a temporal stage (across frames) keeps the                 tions), or advancing to a new token drawn from the legal-next-
entire pipeline hardware-compatible.                                       token set for the current prefix. Beams are pruned to the top
                                                                           B after expansion, and the best fully terminated hypothesis
D. VIDEO-CLIP TEMPORAL ENCODING                                            is tracked throughout. If no beam reaches a valid terminal
Once each frame has been encoded, the resulting embeddings                 sentence, a fallback extends the best partial prefix into the
are stacked along the time axis into a 2D representation                   nearest valid sentence. If no extension exists, the prefix is
of the clip (time × embedding features). A second Akida-                   progressively shortened, ultimately defaulting to the globally
compatible network applies temporal convolutions across this               shortest valid sentence. This guarantees grammatically valid
stack, producing a single video-clip embedding that captures               output at all times.
motion and short-range temporal dynamics.
                                                                           H. TRAINING AND QUANTIZATION
E. SPECTROGRAM-CLIP AUDIO ENCODING                                         The model is trained with CTC loss, which marginalises over
In parallel, the audio corresponding to each clip is converted             all alignments between input frames and target tokens via
into Mel-frequency cepstral coefficients (MFCCs), the stan-                a special blank label, allowing weakly supervised training
dard CNN-friendly audio representation. The spectrogram                    where only the spoken sentence is annotated. Word error
is processed by a third AkidaNet-based encoder to yield an                 rate (WER), the minimum edit distance between prediction
audio-clip embedding.                                                      and reference normalised by reference length, is the primary
                                                                           metric. For the industrial-command corpus we additionally
                                                                           report sentence-level command accuracy.
F. PREDICTOR HEAD AND AUDIO-VISUAL FUSION
                                                                              The Akida hardware requires integer-precision weights
The video-clip embedding and the audio-clip embedding are                  and activations. Quantization is parameterised by three bit-
concatenated into a joint audio-visual representation, fed to a            widths, written as a triple win /w/a, where win is the weight
lightweight MLP predictor head that outputs a vector of logits             bit-width of the first layer, w the weight bit-width of all
over the vocabulary. Per-token probabilities are obtained via              subsequent layers and a the activation bit-width. Standard
softmax.                                                                   AKD1000-compatible models use 8/4/4 throughout. Our
                                                                           modular pipeline uses a hybrid scheme. The image encoder
G. CONSTRAINED BEAM-SEARCH DECODING                                        and the spectrogram encoder, which receive raw pixel and
At inference time, the head produces a token-score matrix of               spectrogram inputs respectively, use 8/4/4. The video encoder
shape T ×V (clip windows × vocabulary). Rather than greedy                 and the predictor head, which operate on intermediate embed-
decoding, we use a constrained beam search exploiting the                  dings produced upstream, use 4/4/4. Quantization is followed
known grammar of the evaluation datasets. Both corpora                     by quantization-aware training (QAT) to recover any post-
consist of sentences drawn from a fixed, finite grammar.                   quantization accuracy loss. Throughout both float and QAT
The decoder restricts every per-frame transition to tokens                 phases we use only ℓ2 weight decay (the same regulariser as
that form a valid prefix of some legal sentence, dramatically              the original AkidaNet recipe [12]). No magnitude pruning or
shrinking the search space.                                                ℓ1 penalty is applied.
4
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




IV. DATASETS                                                                  TABLE 2. Per-dataset training and pre-processing hyperparameters.
A. GRID AUDIOVISUAL SENTENCE CORPUS
GRID [18] is the canonical sentence-level lip-reading bench-                                                       GRID                NAVIR
mark and our primary public evaluation. It contains audio-                    Batch size                             16                 3
visual recordings from 34 speakers, each uttering 1,000 sen-                  Epochs, float (unseen/overlap)     30 / 100          — / 200
                                                                              Epochs, QAT (unseen/overlap)       15 / 100          — / 200
tences drawn from a fixed six-word grammar:                                   Video window (frames)                  15                18
      command (4) + colour (4) + preposition (4) + letter                     Video overlap (frames)                 10                12
                                                                              Audio (spectrogram) window             60                60
      (25) + digit (10) + adverb (4)                                          Sample rate (Hz)                    50,000            32,000
For example, ‘‘set blue with H seven again’’. The grammar                     FFT points                           2,048             1,024
                                                                              Hop length                            512               320
yields up to 64,000 distinct sentences. All clips are approx-                 Mel bands                             112               112
imately 3 s long, recorded at 25 fps and 720×576 pixels,                      Noise augmentation ratio              0.8               0.8
and ship with word-level alignments. Standard protocols use                   SNR sweep (dB)                 {−15, −10, −5, 0} {−15, −10, −5, 0}
                                                                              Image encoder (α)                     0.50              0.25
either an overlapped split (some speakers in both train and test              Spec encoder (α)                      0.50              0.25
sets) or an unseen-speaker split. We chose GRID for its public                Video encoder dim (α)              256 (1.0)         128 (0.5)
availability, manageable size and the abundance of published                  Predictor head (units)             512, 256             256
baselines (Section II-D).

B. NAVIR INDUSTRIAL-COMMAND CORPUS (INTERNAL)                                 from {−15, −10, −5, 0} dB during training. For evaluation,
The NAVIR corpus is a custom audio-visual dataset of robot-                   the noisy-audio test condition uses a fixed SNR of −10 dB.
manipulation commands developed for this project. It is an                    The first predefined fold is held out for evaluation.
internal corpus, used to fine-tune and evaluate the deployed
system but not publicly released. The corpus consists of 183                  V. EXPERIMENTAL SETUP
distinct commands drawn from a structured vocabulary of                       Table 2 summarises the configuration of both training runs.
approximately 39 words, organised in five categories.                         On GRID we report both the standard unseen-speaker pro-
   1) Move [object] into [location] (e.g., ‘‘Move the blue                    tocol of LipNet [28] and an overlapped-speaker protocol
      cube into the box’’).                                                   (speakers shared between train and test, sentences disjoint),
   2) Pick up [object] (e.g., ‘‘Grab the mouse’’).                            which is the other widely reported GRID setting. NAVIR
   3) Place [object] in [location] (e.g., ‘‘Put the green cube                uses an 80/20 sentence-level split that holds out a random
      in the box’’).                                                          subset of commands across both speakers, so the evaluation
   4) Go to [object/location/position] (e.g., ‘‘Go above the                  set probes generalisation to unseen sentences rather than
      blue cube’’, ‘‘Return to home’’).                                       unseen speakers (the corpus contains only two speakers).
   5) Rotate [object] clockwise (e.g., ‘‘Spin the battery clock-              Both runs apply horizontal-flip augmentation (p = 0.5) and
      wise’’).                                                                temporal jitter (p = 0.05). After float training, models are
Objects are: blue cube, yellow cube, green cube, white ball,                  quantized using the hybrid scheme of Section III-H and fine-
mouse, battery. Locations are: box, bin. Positional targets                   tuned with QAT (15 epochs on GRID unseen-speaker, 100
are: home, up, ready. Each command admits multiple syn-                       epochs on GRID overlapped, 200 epochs on NAVIR; the
onymous phrasings (e.g., move / transfer / relocate / shift /                 longer NAVIR schedule reflects the smaller corpus and the
bring), introducing lexical variation while preserving seman-                 longer overlapped schedule reflects the harder cross-sentence
tic equivalence. Two speakers each produced the full set of                   generalisation within a fixed speaker set).
183 commands, yielding 366 recordings. Compared to GRID,
NAVIR is domain-specific and command-oriented, making it                      VI. RECOGNITION RESULTS
more representative of the target deployment.                                 A. GRID WORD ERROR RATE
                                                                              Tables 3 and 4 report WER under the standard unseen-speaker
C. URBANSOUND8K NOISE AUGMENTATION                                            split, and Tables 5 and 6 report WER under the overlapped-
UrbanSound8K [36] is a publicly available corpus of 8,732                     speaker split. Results are broken down by training modality
labelled urban-sound excerpts of up to 4 s, drawn from ten                    (clean audio, noisy audio, video only, or fused) and evaluation
classes (air conditioner, car horn, children playing, dog bark,               condition (clean / noisy audio).
drilling, engine idling, gun shot, jackhammer, siren and                         Under clean audio, all audio-capable models on the unseen-
street music) and pre-folded for ten-fold cross-validation.                   speaker split perform comparably (3.2–7.7% WER across
We use it solely as a noise-augmentation source. Following                    configurations). The interesting contrast appears under noise.
CochleaNet [37], we extract the mechanical and machinery                      Training on clean audio collapses to roughly 77–80% WER
subset (air conditioner, drilling, engine idling, jackhammer),                when noise is introduced, while training on noisy audio
which is representative of the ambient noise found in in-                     brings this down to 21.0% (float) and 22.5% (quantized).
dustrial settings, and mix these clips into the clean audio                   Crucially, fusing noisy audio with video reduces WER further
tracks of GRID and the NAVIR corpus at SNRs sampled                           to 16.6% (float) and 14.0% (quantized), confirming that the
                                                                                                                                                  5
                                                    L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




TABLE 3. Non-quantized WER (%) on GRID (unseen-speaker split) under         TABLE 5. Non-quantized WER (%) on GRID (overlapped-speaker split)
clean and noisy audio test conditions.                                      under clean and noisy audio test conditions. Both float and QAT models
                                                                            were trained for 100 epochs in this regime.

          Training modalities    Clean audio   Noisy audio
                                                                                       Training modalities    Clean audio    Noisy audio
          Clean audio                3.7           79.9
          Noisy audio                4.4           21.0                                Clean audio                 1.3           79.8
          Video                     34.0           34.0                                Noisy audio                 1.9           10.4
          Noisy audio + video        7.7           16.6                                Video                       9.1            9.1
          Clean audio + video        3.6           78.6                                Noisy audio + video         0.7            2.8
                                                                                       Clean audio + video         0.7           77.4

TABLE 4. Quantized WER (%) on GRID (unseen-speaker split) after QAT.
                                                                            TABLE 6. Quantized WER (%) on GRID (overlapped-speaker split) after
                                                                            QAT.
          Training modalities    Clean audio   Noisy audio
          Clean audio                4.2           77.3                                Training modalities    Clean audio    Noisy audio
          Noisy audio                5.2           22.5
                                                                                       Clean audio                 2.0           78.7
          Video                     35.3           35.3
                                                                                       Noisy audio                 2.3           11.8
          Noisy audio + video        5.3           14.0
                                                                                       Video                       6.7            6.7
          Clean audio + video        3.2           77.8
                                                                                       Noisy audio + video         0.8            3.3
                                                                                       Clean audio + video         0.8           77.1


visual modality anchors recognition when the acoustic signal
degrades. Interestingly, in this fused noisy condition the quan-            tions), whereas training on noisy audio reduces noisy-test
tized model is marginally better than its float counterpart,                WER by nearly an order of magnitude (10.4% float and
although the effect is small and not consistent across all                  11.8% quantized). The Pareto analysis in Section VII-C uses
configurations.                                                             both the overlapped- and unseen-speaker video-only stats for
   The video-only model reaches 34.0% (float) and 35.3%                     cross-method comparison.
(quantized) WER on the unseen-speaker split. While this is
higher than the SOTA range of 9.7–11.4% (Section II-D),                     B. NAVIR WORD ERROR RATE AND COMMAND
those baselines all employ 3D convolutions, attention-                      ACCURACY
augmented decoders and large-scale pre-training, none of                    Tables 7 and 8 report WER and sentence-level command
which are AKD1000-compatible. The factorised AkidaNet                       accuracy on the NAVIR corpus.
pipeline trades representational depth for hardware deploya-                   NAVIR results are strong across vision-based modalities
bility, and even so fusion still extracts useful information from           both before and after quantization. The video-only model
the visual stream when audio is corrupted.                                  retains near-perfect performance through quantization (0.5%
   On the overlapped-speaker split (Tables 5 and 6), where                  to 0.7% WER, 100% command accuracy preserved), and the
train and test sets share speakers but not sentences, every trend           noisy-audio + video fusion model degrades only marginally
observed in the unseen-speaker regime is preserved and the                  (0.3% to 0.6% WER clean and 0.9% to 1.5% noisy). Audio-
absolute numbers tighten substantially. The video-only model                only models are far less robust. The clean-audio model col-
reaches 9.1% (float) and 6.7% (quantized) WER, approaching                  lapses entirely under noise both before (97.5%) and after
the 1.83–4.8% range of unconstrained ANN baselines despite                  (98.7%) quantization, confirming that without visual input
the AKD1000-imposed architectural budget. Notably, QAT                      the system has no path to reliable performance in real-world
improves the video-only model over its float counterpart                    acoustic environments. The 200-epoch QAT schedule is well
by 2.4 absolute points in this setting, an effect of similar                matched to the small corpus size, with multimodal models
direction to the one observed in the unseen-speaker fused                   retaining most of their float accuracy.
condition, though again we do not claim a consistent QAT
advantage across configurations. As in the unseen-speaker                   C. CROSS-DATASET DISCUSSION
case, fusing the two modalities yields a clear improvement                  Across both benchmarks, multimodal fusion provides a ro-
over either modality alone: under noise, the noisy-audio +                  bust gain over single-modality baselines, especially under
video model reaches 2.8% (float) and 3.3% (quantized) WER,                  noise. QAT preserves accuracy and in some configurations
against 10.4% (float) and 11.8% (quantized) for noisy audio                 slightly improves it. The video-only ceiling on the GRID
alone, and 9.1% (float) and 6.7% (quantized) for video alone,               unseen-speaker split (35.3% WER) reflects the architectural
confirming that the visual modality anchors recognition when                constraints of the AKD1000 rather than a fundamental limit
the acoustic signal degrades. Under clean audio, fusion re-                 of lip reading itself. On NAVIR, where the visual task is much
duces WER to 0.7% (float) and 0.8% (quantized), below both                  easier (small command vocabulary, controlled recording con-
single-modality baselines. As in the unseen-speaker case,                   ditions, two speakers), the same architecture saturates near
training on clean audio alone collapses under noise (77.1–                  0% WER.
79.8% WER across the four clean-audio-trained configura-
6
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




TABLE 7. Non-quantized NAVIR results: WER (%) / command accuracy              TABLE 9. Model complexity and theoretical ANN inference energy on
(%).                                                                          GRID.


           Training modalities    Clean audio    Noisy audio                    Model                WER (%)      Params    FLOPs       ANN energy
           Clean audio              5.4 / 93.0    97.5 / 2.8                    LipNet [28]            11.4        4.57 M   10.69 G       19.78 mJ
           Noisy audio             11.0 / 81.7    42.6 / 52.1                   Wu et al. [35]        10.21       10.89 M   84.62 G      156.54 mJ
           Video                   0.5 / 100.0    0.5 / 100.0                   Ours (video-only)     35.30        1.49 M    2.24 G        4.15 mJ
           Noisy audio + video     0.3 / 100.0    0.9 / 100.0
           Clean audio + video      4.3 / 93.0    95.6 / 2.8
                                                                              TABLE 10. Theoretical SNN energy and efficiency gain.

TABLE 8. Quantized NAVIR results after QAT: WER (%) / command
accuracy (%).                                                                    Model               ANN energy      SNN energy       ANN/SNN gain
                                                                                 LipNet [28]           19.78 mJ          —                 —
                                                                                 Wu et al. [35]       156.54 mJ          —                 —
           Training modalities    Clean audio    Noisy audio
                                                                                 Ours (video-only)      4.15 mJ       314.92 µJ          13.17×
           Clean audio              6.6 / 91.5    98.7 / 0.0
           Noisy audio             12.1 / 77.5    43.1 / 47.9
           Video                   0.7 / 100.0    0.7 / 100.0
           Noisy audio + video      0.6 / 98.6     1.5 / 98.6                    The SNN energy advantage stems from the combination of
           Clean audio + video      4.3 / 93.0    95.7 / 4.2                  spike sparsity and the AC-vs-MAC asymmetry. Our model
                                                                              achieves a measured average firing rate of 27.55% (i.e.,
                                                                              72.45% sparsity) across spiking layers, evaluated empirically
VII. ENERGY AND POWER ANALYSIS                                                on GRID. Substituting this into the SNN formula yields a
A. THEORETICAL ENERGY METHODOLOGY                                             theoretical 13.17× gain over the equivalent ANN, reducing
We adopt the operation-count framework that has become a                      per-sentence inference cost to 314.92 µJ. Combined with the
standard in the SNN/ANN comparison literature [6], [5], [11],                 already-low ANN baseline of 4.15 mJ, this places our model
[38], parameterised by the per-operation energy constants                     approximately 62.8× below LipNet [28] and 497× below
reported by Horowitz [2] for 45 nm CMOS. Horowitz [2] does                    Wu et al. [35] when both are evaluated as ANNs (Table 10).
not propose a model-level methodology, only the underlying                    LipNet and Wu et al. are not directly convertible to SNN
primitive-cost numbers. The methodology consists of sum-                      equivalents and are quoted as ANN comparison points only.
ming the relevant operations in the model and weighting them
by these primitive costs. The energy of a conventional ANN                    C. PARETO ANALYSIS OF ACCURACY VS. COMPUTATIONAL
inference is                                                                  COST
                  EANN = MACs × EMAC ,                    (1)                 Figure 2 situates our model in the GFLOPs–WER plane
with EMAC ≈ 3.7 pJ. For an SNN, synaptic operations                           against the SOTA lip readers reviewed in Section II-D. Two
reduce to additions, since spike values are binary and inactive               test conditions are plotted: unseen-speaker (blue circles) and
neurons contribute nothing, at EAC ≈ 0.9 pJ, scaled by the                    overlapped-speaker (red diamonds). Bubble area encodes pa-
empirically measured average firing rate r̄:                                  rameter count. Our model is the only point at low FLOPs
                                                                              (2.24 GFLOPs) and the smallest by parameters (1.49 M),
                   ESNN = MACs × r̄ × EAC .                          (2)      while the SOTA cluster (LipNet, HLR-Net, Wu et al.) sits
The combined effect of spiking sparsity and the lower per-                    at 10–85 GFLOPs and 4–11 M parameters, achieving 1.83–
operation cost yields a theoretical efficiency gain                           11.4% WER. We are deliberately Pareto-incomparable. At the
                                                                              cost of higher unseen-speaker WER, NAVIR offers an order
                EANN       EMAC          3.7                                  of magnitude or more lower computational cost, which is the
                      =             =           .          (3)
                ESNN      EAC × r̄     0.9 × r̄                               relevant axis for neuromorphic edge deployment. We also
These figures are theoretical estimates derived from operation                note that the overlapped-speaker number for our quantized
counts. They do not capture memory-access cost, hardware                      video-only model (6.7% WER) is the first reported result for
parallelism or implementation-specific factors, but they serve                an SNN-compatible architecture on GRID and approaches the
as a standard, reproducible cross-architecture baseline.                      1.83–4.8% range of unconstrained ANN baselines despite our
                                                                              fixed-quantization, no-3D-conv, no-attention budget.
B. THEORETICAL RESULTS ON GRID
Table 9 reports parameter counts, FLOPs and ANN inference                     D. PRACTICAL HARDWARE POWER MEASUREMENTS
energy for our video-only model alongside two SOTA lip-                       To quantify the AKD1000’s practical efficiency, we measured
reading baselines, accounting for the total number of model                   power consumption on the Raspberry Pi 5 demo platform with
calls required for a sentence-level prediction. Our model is                  a FNIRSI FNB58 USB power meter, repeatedly calling the
substantially more compact, with 3.1× fewer FLOPs than                        model on pre-computed inputs over a 5-minute window so
LipNet [28] and 37.8× fewer than Wu et al. [35]. This                         that average draw stabilised. We also ran the same benchmark
translates directly into a 4.8× and 37.8× lower ANN energy                    on a laptop with an NVIDIA RTX 3060 Mobile GPU using
footprint respectively.                                                       continuous nvidia-smi polling. The two measurement
                                                                                                                                                     7
                                                     L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




                                                                             TABLE 12. Audio-video model: per-inference power consumption across
                                                                             backends. Same idle baselines and measurement scopes as Table 11.


                                                                             Backend                     it/s   mWh@5 min        ∆mWh       mWh/inf.
                                                                             Pi + AKD1000 (Akida)      2.61          459.9         69.9      0.0894
                                                                             Pi + CPU (Akida)          13.36         737.2        347.2      0.0866
                                                                             Pi + CPU (Keras)          0.63          528.5        138.5      0.7381
                                                                             Laptop + GPU (Keras)      1.29        2,566.2       1,286.2     3.3354




FIGURE 2. Pareto view of GRID lip-reading models, computational cost
(GFLOPs, log scale) versus word error rate, for both overlapped-speaker
(red diamonds) and unseen-speaker (blue circles) test conditions. Bubble
area is proportional to parameter count. Our quantized video-only model
(green) sits alone on the low-FLOPs frontier.


TABLE 11. Video-only model: per-inference power consumption across
backends. Idle baselines: Pi 390 mWh / 5 min, GPU 1,280 mWh / 5 min. Pi
figures cover total system draw (FNB58). GPU figures cover GPU-only
draw via nvidia-smi, normalised to a 5-minute window.
                                                                             FIGURE 3. NAVIR demonstration system. An Obsbot Meet SE webcam
                                                                             supplies frame and audio capture. A Raspberry Pi 5 with an M.2 HAT hosts
Backend                    it/s    mWh@5 min       ∆mWh       mWh/inf.       the BrainChip AKD1000 co-processor. A uFactory xArm 6 robotic arm
                                                                             executes the recognised commands.
Pi + AKD1000 (Akida)      14.55        462.0         72.0       0.0165
Pi + CPU (Akida)          15.55        768.0        378.0       0.0810
Pi + CPU (Keras)           1.10         531.9       141.9       0.4306
Laptop + GPU (Keras)       2.54       2,569.6      1,289.6      1.6913       ference at comparable throughput. Against the Pi-CPU Keras
                                                                             float baseline the gap widens to 26×. Against the laptop GPU
                                                                             it widens further to over 100×.
scopes differ: the Pi figures cover total system draw, whereas                  The audio-video pipeline (Table 12) extends the video-only
the GPU figures cover only the GPU itself, with known preci-                 pipeline with a spectrogram encoder (348 NPs, 9 sequences)
sion limitations [39]. Both effects make the GPU comparison                  and a larger predictor head (2 NPs, 1 sequence), for a total
favourable to the GPU.                                                       of 22 passes per inference. Per-inference Akida energy rises
   The CPU-backend idle draw on the Pi settled at approxi-                   to 0.0894 mWh, broadly comparable to the Pi-CPU Akida
mately 390 mWh / 5 min, which we adopt as the baseline for                   backend (0.0866 mWh/inf.) but at lower throughput (2.61
inference-attributable consumption. The Akida-backend idle                   vs. 13.36 it/s). Against the laptop GPU the AKD1000 still
draw is essentially identical (387.59 mWh), and the bare Pi                  consumes 37× less energy per inference. The reason the
with no script running drew 370.92 mWh. The GPU’s idle                       AKD1000 loses its per-inference advantage on the audio-
draw alone was 1,280 mWh / 5 min, more than three times                      video model is a hardware-mapping behaviour of the Akida
the Pi’s total system draw.                                                  toolchain that is independent of architecture, analysed in
   The most informative on-device comparison is the                          Appendix A. Even so, 2.61 it/s is comfortably above real-time
AKD1000 against the same SNN-converted model running                         for command recognition.
on CPU under the Akida software backend (the strongest CPU
baseline). The Pi-CPU Keras backend, which executes the                      VIII. DEMONSTRATION SYSTEM
float Keras model rather than the SNN, is reported alongside                 The demo system, shown in Figure 3, is built around a 16 GB
for completeness but is the weakest competitor. Comparing                    Raspberry Pi 5 chosen for its balance of processing capability,
AKD1000 against laptop-GPU Keras measures the chip’s                         compact form factor and peripheral-stack compatibility. An
standing against a typical accelerated-computing baseline.                   M.2 HAT exposes a PCIe-backed M.2 slot through which
   The video-only pipeline (Table 11) consists of an image                   the AKD1000 M.2 card is connected directly to the host,
encoder (75 NPs, 1 sequence), a temporal encoder (41 NPs,                    enabling low-latency communication between the Pi and the
3 sequences) and a predictor head (2 NPs, 1 sequence), for a                 neuromorphic accelerator without an external workstation.
total of 5 AKD1000 passes per inference. The Akida back-                     Visual input comes from an Obsbot Meet SE webcam at full
end reaches 14.55 it/s at 0.0165 mWh/inf. Against the same                   HD, the same model used during NAVIR-corpus collection,
model on CPU under the Akida backend (0.0810 mWh/inf.,                       ensuring identical lens optics, colour response and field of
15.55 it/s) the AKD1000 is 4.9× more energy-efficient per in-                view at deployment time. Recording start and stop is driven
8
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




by a standard USB keyboard. A uFactory xArm 6 robotic arm                     command accuracy and 1.5% WER. On the deployment plat-
is connected directly to the Pi, closing the loop from voice                  form it sustains real-time throughput at approximately 5×
command to physical action. Video and audio are captured,                     less energy per inference than the strongest CPU baseline
processed through the neuromorphic pipeline, and the recog-                   (the SNN-converted model running on the Akida software
nised commands are dispatched to the arm in real time. The                    backend) and over 100× less than a laptop GPU on the
complete system is self-contained, edge-deployable and runs                   video-only model. To the best of our knowledge, this is the
entirely on commodity embedded hardware augmented by the                      first end-to-end multimodal AVSR system demonstrated on
AKD1000.                                                                      neuromorphic hardware of this class. The remaining gap to
                                                                              unconstrained SOTA accuracy is consistent with the chip’s
IX. DISCUSSION AND LIMITATIONS                                                deliberate architectural simplicity, and Appendix A identifies
The system has several known limitations. First, the                          a concrete path, sparsity-aware fine-tuning, to further close
AKD1000’s architectural constraints preclude 3D convolu-                      the gap between the video-only and audio-video deployment
tions, recurrence and attention, which together account for                   points.
most of the SOTA accuracy on unconstrained lip-reading
benchmarks. The 35.3% video-only WER on the GRID                              APPENDIX A WHY THE AUDIO-VIDEO MODEL IS
unseen-speaker split reflects this gap rather than any limit of               SLOWER ON THE AKD1000
the proposed factorisation. Second, the audio-video model’s                   Table 12 reports a substantial throughput drop for the audio-
hardware mapping is not yet optimal, as Appendix A makes                      video model relative to the video-only frequency in Table 11.
precise. The image encoder spills across 9 sequences in the                   Upon inspecting the per-module hardware mapping of the
audio-video checkpoint despite mapping to a single sequence                   audio-video checkpoint, the cause becomes clear. The im-
in the video-only checkpoint. Third, the NAVIR corpus, while                  age encoder, structurally identical between the video-only
well matched to the target deployment, contains only 366                      and audio-video pipelines, maps to 75 NPs in 1 sequence
recordings from two speakers and does not yet probe unseen-                   in the video-only checkpoint but to 348 NPs spread over 9
speaker generalisation or broader vocabulary.                                 sequences in the audio-video checkpoint, the same footprint
   Several directions naturally extend this work. The forth-                  as the spectrogram encoder in that checkpoint (also 348 NPs
coming AKD1500, which promises lower static power and                         in 9 sequences). Each additional sequence corresponds to one
supports more complex topologies, may relax some cur-                         extra hardware context switch on the AKD1000 mesh, so the
rent constraints. Sparsity-aware fine-tuning, motivated by the                remapped image encoder alone accounts for the bulk of the
mapping analysis in Appendix A, could equalise the audio-                     throughput reduction.
video and video-only sequence counts and yield a one-shot                        The root cause lies in the Akida runtime’s map-
throughput gain on existing hardware. Expanding the NAVIR                     ping algorithm. akida.Model.map() is not a purely
corpus along the speaker, vocabulary and noise axes would                     structural operation. It runs an internal binary search
strengthen the system’s claim to industrial readiness. The                    over cnp_max_filters, the maximum number of
AKD1000’s on-chip few-shot edge-learning capability [16],                     neurons that can share a single Convolutional Neu-
[17] suggests a route to user-personalised speech recognition                 ral Processor, and at each candidate value invokes the
without full retraining, which may be particularly valuable in                C++ hardware-constraint solver with the model’s actual
a multi-operator industrial setting. Finally, the front-end face-             weight tensors. The solver inspects each layer’s non-zero
landmark extractor (MediaPipe Face Mesh) currently runs on                    weight connectivity, computed as incoming_conn =
the Pi CPU and is the only non-neuromorphic stage in the                      np.count_nonzero(weights[ ...,0]), when de-
pipeline. Distilling it into an Akida-compatible CNN would                    ciding whether the candidate split satisfies the chip’s routing
close the loop and make the entire perception pipeline, from                  and bandwidth constraints. Two checkpoints with identical
raw frames to spoken-word predictions, run on the neuromor-                   architecture but different trained weights therefore produce
phic accelerator, removing the CPU dependency for landmark                    different connectivity patterns, drive the binary search to
detection and consolidating the energy budget on a single                     different convergence points and ultimately partition into
device.                                                                       different sequence counts. Denser or differently distributed
                                                                              weight matrices make the solver fall back to a smaller
X. CONCLUSION                                                                 cnp_max_filters, which fits per-NP routing budgets
We have presented a complete neuromorphic AVSR pipeline                       only by spilling layers across additional sequences.
running end-to-end on the BrainChip AKD1000 chip,                                The training setup used in this work follows the original
with hardware-aware architectural choices, a constrained-                     AkidaNet recipe, which applies ℓ2 weight decay only. While
grammar beam-search decoder and a hybrid quantization                         ℓ2 regularisation penalises weight magnitude, it does not
scheme tailored to the chip’s deployment requirements. On                     drive weights to exact zero, and the mapper counts non-zeros
the public GRID benchmark, the quantized fusion model at-                     regardless of their magnitude. As a result, the connectivity-
tains 14.0% WER under noise on the unseen-speaker split and                   induced asymmetry between the video-only and audio-video
3.3% WER under noise on the overlapped-speaker split. On                      checkpoints persists through training. A future revision could
a task-specific industrial-command corpus it reaches 98.6%                    investigate magnitude pruning of the encoder weights below
                                                                                                                                           9
                                             L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




a small threshold before quantization, or fine-tuning under          TABLE 13. Temporal-video encoder layers. Filter counts use the width
                                                                     multiplier α (1.0 on GRID, 0.5 on NAVIR). The output dimension D is 256
an additional ℓ1 penalty. Either intervention would directly         on GRID and 128 on NAVIR. On NAVIR, conv blocks are conv → batch
reduce incoming_conn for every convolutional layer and               normalisation → ReLU. On GRID, batch normalisation is omitted, leaving
                                                                     conv → ReLU.
is expected to equalise the audio-video and video-only map-
pings without further changes to the architecture. The map-
                                                                         Layer                       Kernel    Filters     Output
ping behaviour identified here is a generic property of the
AKD1000 toolchain and therefore relevant to any work that                Input                       —         —           (T , 1, 128)
                                                                         Rescaling                   —         —           (T , 1, 128)
deploys multiple checkpoints of the same architecture on this            video_conv_0 (block)        3×3       ⌊64α⌋       (T , 1, ⌊64α⌋)
hardware.                                                                video_conv_1 (block)        3×3       ⌊96α⌋       (T , 1, ⌊96α⌋)
                                                                         video_conv_2 (block)        3×3       ⌊128α⌋      (T , 1, ⌊128α⌋)
                                                                         Global avg. pool            —         —           (1, 1, ⌊128α⌋)
APPENDIX B MODULE LAYER COMPOSITION                                      Dropout (0.03)              —         —           (1, 1, ⌊128α⌋)
This appendix details the layer composition of every module              video_dense                 —         D           (D)
in the NAVIR pipeline. The image encoder and the spectro-                Batch norm. + ReLU          —         —           (D)
gram encoder reuse the AkidaNet backbone with the dense
classification head removed, so we describe them by refer-
ence. The temporal-video encoder and the predictor head are          primitive operate as an effective 1D temporal convolution.
NAVIR-specific and are detailed in full.                             Table 13 lists every layer.
                                                                        All conv layers use padding=’same’ and stride 1, so
A. IMAGE ENCODER AND SPECTROGRAM ENCODER                             the temporal axis is preserved through the convolution stack.
(AKIDANET BACKBONE)                                                  Global average pooling collapses the temporal axis to produce
Both the image and the spectrogram encoders are instances of         a single video-clip embedding, which is projected to D di-
the standard AkidaNet ImageNet model, instantiated through           mensions by a final dense layer with batch normalisation and
akida_models.akidanet_imagenet with one chan-                        bounded ReLU. The same ℓ2 weight decay used in AkidaNet
nel input. AkidaNet is a MobileNet-style CNN designed                is applied throughout.
to be fully compatible with the AKD1000 hardware. The
                                                                     C. PREDICTOR HEAD
backbone consists of an input rescaling layer, four full
convolution blocks (conv_0–conv_3, with strided con-                 The predictor head is a small multilayer perceptron that con-
volutions at conv_0 and conv_2), ten separable con-                  sumes the concatenated (Dv + Ds )-dimensional fused em-
volution blocks (separable_4–separable_13, with                      bedding and emits per-clip token logits of dimension V (the
strided convolutions at separable_4, separable_6                     vocabulary size, including the CTC blank symbol). The depth
and separable_12), and a global average pooling at the               of the head differs between the two datasets, reflecting the
output of separable_13. Each conv or separable block is              different complexity of their decoding tasks.
conv → batch normalisation → ReLU. Filter counts double                 On GRID the input is a vector of dimension Dv + Ds =
through the network, from 32 at conv_0 up to 1024 at                 256 + 512 = 768. The head has two hidden layers:
separable_12 and separable_13, scaled uniformly                         1) Dense layer with 512 units, followed by ReLU bounded
by the width multiplier α.                                                  at 6.0.
   In our pipeline the standard AkidaNet classification head            2) Dense layer with 256 units, followed by ReLU bounded
(the dropout and 1000-way dense classifier) is removed and                  at 6.0.
replaced with a single dense projection followed by a ReLU              3) Dense layer with V units, no activation. The output is
bounded at 6.0, sized to the desired embedding dimension.                   the raw logit vector consumed by the CTC loss during
We use 128-dimensional per-frame embeddings for the im-                     training and by the constrained beam-search decoder at
age encoder, and 512-dimensional per-clip embeddings for                    inference time.
the spectrogram encoder. On GRID we use α = 0.50 for                    On NAVIR the input is a vector of dimension Dv + Ds =
both encoders. On NAVIR we use α = 0.25. Input shapes                128 + 512 = 640. The head uses a single hidden layer:
are 32 × 64 × 1 (image, GRID) and 88 × 176 × 1 (image,                  1) Dense layer with 256 units, followed by ReLU bounded
NAVIR), and 112 × 112 × 1 (spectrogram, both datasets). For                 at 6.0.
full architectural details we refer the reader to the origi-            2) Dense layer with V units, no activation.
nal AkidaNet specification distributed with the BrainChip               For modality-specific configurations the absent stream is
MetaTF SDK [40].                                                     omitted from the input. The head is quantized to 4-bit weights
                                                                     and activations alongside the upstream encoders, and is fine-
B. TEMPORAL-VIDEO ENCODER                                            tuned jointly with them during the QAT phase.
The temporal-video encoder takes the stacked per-frame im-
age embeddings as a 4D tensor of shape (T , 1, F), where             References
T is the video window size and F = 128 is the per-frame               [1]    H. Mcgurk and J. Macdonald, ‘‘Hearing lips and seeing
embedding dimension produced by the image encoder. The                       voices,’’ Nature, vol. 264, no. 5588, pp. 746–748, Dec.
width axis of size 1 lets the AKD1000’s 2D convolution                       1976.
10
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




 [2]   M. Horowitz, ‘‘1.1 Computing’s energy problem (and                     [16]    N. Lutes, V. Sriram, S. Nadendla, and K. Krishna-
       what we can do about it),’’ 2014 IEEE International                            murthy, ‘‘Few-shot transfer learning for individualized
       Solid-State Circuits Conference Digest of Technical                            braking intent detection on neuromorphic hardware,’’
       Papers (ISSCC), pp. 10–14, 2014.                                               Journal of Neural Engineering, vol. 22, 2024.
 [3]   Y. Wu, L. Deng, G. Li, J. Zhu, and L. Shi,                             [17]    E. Bråtman and L. Dow, Neuromorphic Medical Image
       ‘‘Spatio-Temporal Backpropagation for Training                                 Analysis at the Edge : On-Edge Training with the Akida
       High-Performance Spiking Neural Networks,’’ Fron-                              Brainchip. 2023.
       tiers in Neuroscience, vol. 12, 2017.                                  [18]    M. Cooke, J. Barker, S. Cunningham, and X. Shao,
 [4]   W. Fang, Z. Yu, Y. Chen, T. Huang, T. Masquelier,                              ‘‘An audio-visual corpus for speech perception and au-
       and Y. Tian, ‘‘Deep Residual Learning in Spiking                               tomatic speech recognition,’’ The Journal of the Acous-
       Neural Networks,’’ in Neural Information Processing                            tical Society of America, vol. 120, pp. 2421–2424, 5 Pt
       Systems, 2021.                                                                 1 Nov. 2006. PMID: 17139705.
 [5]   Y. Hu, L. Deng, Y. Wu, M. Yao, and G. Li, ‘‘Advanc-                    [19]    J. S. Chung and A. Zisserman, ‘‘Lip Reading in the
       ing Spiking Neural Networks Toward Deep Residual                               Wild,’’ in Asian Conference on Computer Vision, 2016.
       Learning,’’ IEEE Transactions on Neural Networks                       [20]    T. Afouras, J. S. Chung, A. W. Senior, O. Vinyals, and
       and Learning Systems, vol. 36, pp. 2353–2367, 2021.                            A. Zisserman, ‘‘Deep Audio-Visual Speech Recog-
 [6]   Z. Zhou et al., ‘‘Spikformer: When spiking neural                              nition,’’ IEEE Transactions on Pattern Analysis and
       network meets transformer,’’ in The Eleventh Interna-                          Machine Intelligence, vol. 44, pp. 8717–8727, 2018.
       tional Conference on Learning Representations, 2023.                   [21]    T. Afouras, J. S. Chung, and A. Zisserman, Lrs3-ted:
 [7]   M. Yao et al., ‘‘Spike-driven transformer,’’ in Thirty-                        A large-scale dataset for visual speech recognition,
       seventh Conference on Neural Information Processing                            2018. arXiv: 1809.00496 [cs.CV].
       Systems, 2023.                                                         [22]    N. Harte and E. Gillen, ‘‘TCD-TIMIT: An Audio-
 [8]   C. Lv, Y. Wang, D. Han, X. Zheng, X. Huang, and                                Visual Corpus of Continuous Speech,’’ IEEE Transac-
       D. Li, ‘‘Efficient and Effective Time-Series Forecast-                         tions on Multimedia, vol. 17, pp. 603–615, 2015.
       ing with Spiking Neural Networks,’’ in International                   [23]    A. Ephrat et al., ‘‘Looking to listen at the cocktail
       Conference on Machine Learning, 2024.                                          party,’’ ACM Transactions on Graphics (TOG), vol. 37,
 [9]   X. He, D. Zhao, Y. Dong, G. Shen, X. Yang, and Y.                              pp. 1–11, 2018.
       Zeng, Enhancing audio-visual spiking neural networks                   [24]    M. Gogate, K. Dashtipour, A. Adeel, and A. Hussain,
       through semantic-alignment and cross-modal residual                            ‘‘ASPIRE - Real noisy audio-visual speech enhance-
       learning, 2025. arXiv: 2502.12488 [cs.CV].                                     ment corpus,’’ 2020.
[10]   W. Li, P. Wang, R. Xiong, and X. Fan, ‘‘Spiking                        [25]    G. Tan, Y. Wang, H. Han, Y. Cao, F. Wu, and Z.
       Tucker Fusion Transformer for Audio-Visual Zero-                               Zha, ‘‘Multi-grained Spatio-Temporal Features Per-
       Shot Learning,’’ IEEE Transactions on Image Process-                           ceived Network for Event-based Lip-Reading,’’ 2022
       ing, vol. 33, pp. 4840–4852, 2024.                                             IEEE/CVF Conference on Computer Vision and Pat-
[11]   Q. Liu, J. Wang, Y. Wang, X. Yang, G. Pan, and H. Li,                          tern Recognition (CVPR), pp. 20 062–20 071, 2022.
       ‘‘Human-Inspired Computing for Robust and Efficient                    [26]    B. Cramer, Y. Stradmann, J. Schemmel, and F. Zenke,
       Audio-Visual Speech Recognition,’’ IEEE Transac-                               ‘‘The Heidelberg Spiking Data Sets for the Systematic
       tions on Computers, vol. 74, pp. 2950–2961, 2025.                              Evaluation of Spiking Neural Networks,’’ IEEE Trans-
[12]   P. Lunghi, S. Silvestrini, D. Dold, G. Meoni, A. Had-                          actions on Neural Networks and Learning Systems,
       jiivanov, and D. Izzo, ‘‘Energy efficiency analysis of                         vol. 33, pp. 2744–2757, 2019.
       Spiking Neural Networks for space applications,’’ As-                  [27]    P. Warden, Speech commands: A dataset for limited-
       trodynamics, vol. 9, pp. 909–932, 2025.                                        vocabulary speech recognition, 2018. arXiv: 1804 .
[13]   C. Chemnitz and M. Ermis, Comparison of Akida Neu-                             03209 [cs.CL].
       romorphic Processor and NVIDIA Graphics Processor                      [28]    Y. M. Assael, B. Shillingford, S. Whiteson, and N. de
       Unit for Spiking Neural Networks. 2025.                                        Freitas, Lipnet: End-to-end sentence-level lipreading,
[14]   G. Lenz and D. McLelland, Low-power ship detec-                                2016. arXiv: 1611.01599 [cs.LG].
       tion in satellite images using neuromorphic hardware,                  [29]    J. S. Chung, A. W. Senior, O. Vinyals, and A. Zisser-
       2024. arXiv: 2406.11319 [cs.CV].                                               man, ‘‘Lip Reading Sentences in the Wild,’’ 2017 IEEE
[15]   W. Benoot, N. Destrycker, and A. De Brabanter, ‘‘De-                           Conference on Computer Vision and Pattern Recogni-
       velopment of a robust onboard data processing unit                             tion (CVPR), pp. 3444–3453, 2016.
       using commercial off-the-shelf system-on-chips and                     [30]    K. Xu, D. Li, N. Cassimatis, and X. Wang, ‘‘LCANet:
       neuromorphic co-processors,’’ presented at the Pro-                            End-to-End Lipreading with Cascaded Attention-
       ceedings of SPAICE2024: The First Joint European                               CTC,’’ 2018 13th IEEE International Conference on
       Space Agency / IAA Conference on AI in and for                                 Automatic Face & Gesture Recognition (FG 2018),
       Space, Oct. 1, 2024, pp. 416–419.                                              pp. 548–555, 2018.

                                                                                                                                          11
                                                        L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




[31]    L. Qu, C. Weber, and S. Wermter, ‘‘LipSound: Neural                     General Staff, Athens, Greece. His research interests include interpretable
        Mel-Spectrogram Reconstruction for Lip Reading,’’ in                    machine learning, end-to-end development and deployment of AI systems,
                                                                                and AI applications in medical, industrial, and security domains.
        Interspeech, 2019.
[32]    W. Chen, X. Tan, Y. Xia, T. Qin, Y. Wang, and T.-Y.
        Liu, ‘‘DualLip: A System for Joint Lip Reading and
        Generation,’’ Proceedings of the 28th ACM Interna-
        tional Conference on Multimedia, 2020.                                                            PANAGIOTA MORAITI received the five-year
[33]    A. M. Sarhan, N. M. El-Shennawy, and D. M. Ibrahim,                                               (M.Eng. equivalent) degree in Electrical and Com-
        ‘‘HLR-Net: A Hybrid Lip-Reading Model Based on                                                    puter Engineering from the Democritus University
                                                                                                          of Thrace, in 2024. Her diploma thesis focused
        Deep Convolutional Neural Networks,’’ Computers,                                                  on Continual Test-Time Adaptation in the field of
        Materials & Continua, 2021.                                                                       autonomous driving. She is currently a Computer
[34]    F. Xue et al., ‘‘LCSNet: End-to-end Lipreading with                                               Vision Engineer at Tech Hive Labs, where she is
        Channel-aware Feature Selection,’’ ACM Transactions                                               involved in the development of AI-driven vision
                                                                                                          systems and robotic solutions. She has contributed
        on Multimedia Computing, Communications and Ap-                                                   to both research and industrial projects. Her re-
        plications, vol. 19, pp. 1–21, 2022.                                    search interests include computer vision, deep learning and robotics. She
[35]    L. Wu et al., ‘‘Landmark-guided cross-speaker lip                       has co-authored publications in the areas of Domain Adaptation, Continual
        reading with mutual information regularization,’’ in                    Learning, and Automated Quality Control.
        Proceedings of the 2024 Joint International Confer-
        ence on Computational Linguistics, Language Re-
        sources and Evaluation (LREC-COLING 2024), N.
        Calzolari, M.-Y. Kan, V. Hoste, A. Lenci, S. Sakti, and                                            ANTONIS PORICHIS received the Diploma de-
        N. Xue, Eds., Torino, Italia: ELRA and ICCL, May                                                   gree in Electrical and Computer Engineering
        2024, 10023–10033.                                                                                 from the National Technical University of Athens,
[36]    J. Salamon, C. Jacoby, and J. P. Bello, ‘‘A dataset and                                            Greece, in 2012, and the Ph.D. degree in Robotics
                                                                                                           and Artificial Intelligence from the University of
        taxonomy for urban sound research,’’ in Proceedings                                                Essex, U.K., in 2024. He is currently a Research
        of the 22nd ACM International Conference on Multi-                                                 Officer with the University of Essex. He has also
        media, 2014, pp. 1041–1044.                                                                        held leadership roles in industry as well as research
[37]    M. Gogate, K. Dashtipour, A. Adeel, and A. Hussain,                                                and development in data-efficient machine learn-
                                                                                                           ing and AI-driven product innovation. Earlier in his
        ‘‘CochleaNet: A robust language-independent audio-                      career, he held technical leadership positions in robotics, Internet-of-Things
        visual model for real-time speech enhancement,’’ In-                    systems, and intelligent software engineering. His research interests include
        formation Fusion, vol. 63, pp. 273–285, Nov. 1, 2020.                   machine learning, computer vision, robotic manipulation, and data-efficient
[38]    S. Kundu, M. Pedram, and P. A. Beerel, ‘‘HIRE-                          learning methods, with a particular focus on imitation learning and real-
                                                                                world robotic applications. He has co-authored several publications in these
        SNN: Harnessing the Inherent Robustness of Energy-                      areas, including work on robotic harvesting and learning from demonstration,
        Efficient Deep Spiking Neural Networks by Train-                        published in venues such as Robotics and IEEE conferences.
        ing with Crafted Input Noise,’’ 2021 IEEE/CVF In-
        ternational Conference on Computer Vision (ICCV),
        pp. 5189–5198, 2021.
[39]    Z. Yang, K. Adamek, and W. Armour, ‘‘Part-time
                                                                                                            PANOS CHATZAKOS received the Diploma,
        Power Measurements: Nvidia-smi’s Lack of Atten-
                                                                                                            M.Sc., and Ph.D. degrees in Mechanical Engi-
        tion,’’ in SC24: International Conference for High Per-                                             neering from the National Technical University of
        formance Computing, Networking, Storage and Anal-                                                   Athens, Greece. He is currently the Director of
        ysis, Nov. 2024, pp. 1–17.                                                                          the Essex Artificial Intelligence Innovation Centre
                                                                                                            at the University of Essex, U.K., a joint initiative
[40]    ‘‘Overview — akida examples documentation.’’
                                                                                                            with TWI Ltd., where he leads research and tech-
        Archived at: https : / / web . archive . org / web /                                                nology transfer activities in artificial intelligence
        20260522043609 / https : / / doc . brainchipinc . com/,                                             and robotics. He has extensive experience in both
        Accessed: May 22, 2026. [Online]. Available: https :                                                academia and industry, having established and led
                                                                                technology organizations and innovation initiatives across Europe, including
        //doc.brainchipinc.com/index.html
                                                                                senior leadership roles at TWI and as Executive Chairman of Tech Hive Labs.
                                                                                He has successfully managed and delivered numerous large-scale research
                                                                                and innovation projects, collaborating with industrial partners, SMEs, and
                                                                                academic institutions, and has led multidisciplinary teams developing AI-
                                                                                driven and robotic systems for real-world applications. His work spans data
LEONIDAS DELIMPASIS received the five-year (M.Eng. equivalent) degree           science, robotics, and intelligent systems integration, with a strong focus on
in Electrical and Computer Engineering from the National Technical Univer-      translating research into commercially viable technologies. Dr. Chatzakos
sity of Athens, Greece, in 2025, where his diploma thesis focused on Neuro-     has authored and co-authored several scientific publications and has received
Symbolic AI for Visual Question Answering. He has contributed to several        multiple international awards for his contributions to robotics and applied
European research projects in the areas of machine learning and computer vi-    research, including distinctions in industrial robotics and advanced manu-
sion. He was an ML Researcher at Tech Hive Labs. He is currently a Machine      facturing.
Learning Engineer at Plaixus and serves under the Hellenic National Defence

12
L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware




                           MICHAIL KARAMOUSADAKIS received the
                           five-year (M.Sc. equivalent) degree in Electri-
                           cal and Computer Engineering from the National
                           Technical University of Athens, Greece, in 2019,
                           and the M.Sc. degree in Rehabilitation Engineer-
                           ing from the National and Kapodistrian University
                           of Athens, Greece, in 2023. He has been involved
                           in the development of AI-driven systems and edge
                           computing solutions. He has also held software
                           engineering and research roles, contributing to the
design and implementation of intelligent systems and cyber-physical applica-
tions. His research interests include artificial intelligence, machine learning,
edge computing, DevOps/MLOps, and robotics, with a focus on deploying
scalable and efficient AI systems in real-world environments. He has co-
authored several publications in these areas, including works on edge AI
systems, cyber-physical security, and data-driven intelligent platforms.




                                                                                                    13

