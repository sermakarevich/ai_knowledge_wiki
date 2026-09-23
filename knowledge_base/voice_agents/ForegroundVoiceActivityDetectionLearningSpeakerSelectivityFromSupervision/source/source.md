# Foreground Voice Activity Detection: Learning Speaker Selectivity from Supervision
> PDF (not copied, >2 MB): https://arxiv.org/abs/2609.19856
Source: https://arxiv.org/abs/2609.19856
Kind: pdf
Fetched: 2026-09-22T08:13:12.005759+00:00
Tool: pdftotext

                                                  Foreground Voice Activity Detection: Learning
                                                      Speaker Selectivity from Supervision
                                                                     Guangzhao Yang* , Muhammad Huzaifah* , Yu Pan, Jinya Sakurai, Ningjie Bai†
                                                                                      R&D Team, Recho Inc., Tokyo, Japan
                                                                     {g.yang, m.huzaifah, y.pan, j.sakurai, n.haku}@recho-ai.com


                                              Abstract—Voice activity detection (VAD) fronts most voice-          a foreground speaker would seem to need much longer-range
                                           agent pipelines, yet production detectors treat all human speech,      modeling. In this paper, we test this directly: is the inability
                                           background talkers included, as valid activity; in crowded             to separate foreground from background speech caused by the
                                           settings this floods recognition, stalls turn-taking, and triggers




arXiv:2609.19856v1 [eess.AS] 17 Sep 2026
                                           false barge-in. We formalize Foreground VAD (FVAD): a frame-           limited context of recurrent architectures, or by training data
                                           synchronous, enrollment-free task in which only the dominant           and objectives that never require the distinction? Our results
                                           speaker, defined by sustained presence rather than instantaneous       strongly support the latter.
                                           loudness, is positive, and which reduces to conventional VAD              The limitation becomes severe in crowded settings such
                                           when a single speaker is present. We show that foreground              as restaurants, public squares, and meeting rooms, where
                                           selectivity is largely governed by training supervision: the crucial
                                           ingredient is an augmentation recipe pairing foreground-only           background conversation and babble are misclassified as valid
                                           labels with competing-speaker mixing, generated fully automat-         speech. For a voice agent this causes three failures: (1) Ir-
                                           ically without human annotation. To quantify selectivity we            relevant speech reaches downstream ASR, which modern far-
                                           introduce the Background False-Alarm Rate (BG-FAR), gated              field and noise-robust models [9], [10] transcribe into unrelated
                                           by foreground F1, and build a controlled benchmark, Mix-               content resulting in erroneous LLM responses; (2) Persistent
                                           Interference, complemented by an adapted VOiCES for real-
                                           world far-field evaluation. Across equal-size backbones, Mamba         background speech withholds the VAD falling edge that trig-
                                           and LSTM perform on par while a longer-context attention model         gers generation, leaving the agent in a perpetual listening state;
                                           is no better, suggesting that training supervision plays a substan-    (3) Background talkers falsely trigger barge-in [11], degrading
                                           tially larger role than temporal modeling capacity in achieving        the user experience.
                                           foreground selectivity. The resulting lightweight streaming model,        We formalize the underlying task as Foreground Voice
                                           Mamba-FVAD, outperforms commercial VADs and enrollment-
                                           based speaker-aware systems in foreground selectivity while            Activity Detection (FVAD): a frame-synchronous binary clas-
                                           staying competitive on conventional VAD, at 1–2 ms per-frame           sification in which a frame is positive if and only if it contains
                                           CPU latency.                                                           speech from the foreground speaker of the interaction. The
                                              Index Terms—voice activity detection, foreground speech de-         foreground role is defined by sustained presence and temporal
                                           tection, speaker selectivity, enrollment-free, streaming inference,    identity coherence, not instantaneous energy; the foreground
                                           on-device speech processing, competing-speaker robustness
                                                                                                                  speaker is the one with the greatest sustained speech presence,
                                                                      I. I NTRODUCTION                            and a momentarily louder competitor must not capture the role
                                                                                                                  (defining it by frame-wise loudness would otherwise collapse
                                              The rapid adoption of voice-based AI agents in customer
                                                                                                                  the task into energy-based VAD). Non-foreground speech is
                                           service, personal assistants, and human–AI collaboration has
                                                                                                                  therefore negative, and with a single speaker FVAD reduces
                                           raised the demand for natural, reliable spoken interaction.
                                                                                                                  to conventional VAD. Formally, for a stream x with per-frame
                                           Voice activity detection (VAD), which decides whether each
                                                                                                                  labels yτ , personal VAD (pVAD) models P (yτ | x, et ) over
                                           audio frame contains speech, is typically the first stage of such
                                                                                                                  three classes, target-speaker speech (tss), non-target-speaker
                                           pipelines, ahead of automatic speech recognition (ASR), and
                                                                                                                  speech (ntss), and non-speech (ns), given an exogenous en-
                                           its accuracy strongly shapes overall system performance.
                                                                                                                  rollment et of a known target. Instead, FVAD models the
                                              Modern VAD systems [1]–[3] achieve strong robustness,
                                                                                                                  binary posterior P (yτ =1 | x) for the foreground speaker F (x),
                                           ultra-low latency, and efficient CPU-only inference at 30 Hz
                                                                                                                  an endogenous function of the signal inferred online; a self-
                                           or higher, yet share a basic limitation: they classify all hu-
                                                                                                                  derived pseudo-enrollment the model forms from the audio
                                           man speech—background speakers included—as valid activity.
                                                                                                                  and keeps coherent over time. Equivalently, FVAD’s positive
                                           Methods that do distinguish speakers supply an explicit prior
                                                                                                                  class is the analogue of tss with a self-inferred target, while
                                           in the form of an enrolled embedding, as in personal [4], [5]
                                                                                                                  ns and ntss collapse into its negative class. In short, pVAD
                                           and target-speaker VAD [6], rather than expecting a plain VAD
                                                                                                                  is told who the target is, but FVAD must decide for itself
                                           to learn it. One might assume the limitation is architectural:
                                                                                                                  (we assume one foreground speaker per segment, the identity
                                           deployed VADs often use LSTMs or GRUs [7], [8] with only
                                                                                                                  the model commits to and tracks throughout). These choices
                                           a few hundred milliseconds of effective context, so isolating
                                                                                                                  distinguish FVAD from existing paradigms on three axes, ex-
                                             * Equal contribution.                                                panded in Section II: it strictly generalizes VAD (no separation
                                             † Corresponding author                                               front-end), it is enrollment-free yet identity-committed (unlike
pVAD or energy-following detection), and it runs in a single       the foreground role. For instance, foreground speech may be
streaming stage (unlike a VAD-plus-diarization cascade).           soft at utterance boundaries, whereas a background interjection
   Our central finding is that foreground focus is governed        can be momentarily loud, conditions our benchmark probes.
largely by supervision, not architecture. The decisive factor is   Furthermore, smoothing energy statistics over a longer analysis
the training-data recipe: clean utterances are pseudo-labeled by   window trades flicker for latency, and the gate’s hand-tuned
a of state-of-the-art VAD, then unlabeled interfering speakers     thresholds transfer poorly across devices and environments.
and babble are mixed into the target at controlled signal-to-      Speech enhancement front-ends [19], [20] raise SNR before
noise ratios (SNRs), level dynamics, and far-field reverbera-      VAD, but optimize perceptual quality over speaker selectivity.
tion, with the labels kept on the foreground alone. The model      Likewise, they are trained to preserve all speech; they denoise
is thereby supervised to treat competing speech as negative,       background speakers alongside the foreground and erase the
and a sustained foreground identity is encoded implicitly by       very level and reverberation cues that distinguish them, while
the supervision. Because selectivity is conferred by the data,     adding cascade latency in the single-speaker conditions that
the backbone is free to be chosen for deployment. Our primary      dominate real usage. By contrast, FVAD is a strict generaliza-
system, Mamba-FVAD, pairs a learnable LEAF front-end [12]          tion of VAD, reducing exactly to conventional detection when
with a Mamba state-space backbone [13] whose linear-time           one speaker is present and requiring no separation front-end.
recurrence gives constant per-frame computation and memory            A second line incorporates speaker identity. Streaming end-
for low-latency, CPU-only operation. Varying the backbone          to-end diarization [21], [22] attributes all speakers (“who
confirms architecture is not the bottleneck: an LSTM [14] (a       spoke when”) and typically needs look-ahead, leaving the
recurrent model with more limited context [15]) matches it,        foreground unchosen. Personal and target-speaker VAD [4]–
while a long-context attention model [16] yields no meaningful     [6] condition on an enrollment embedding, giving strong
gain.                                                              selectivity only for a pre-registered identity and failing when
   In summary, our key contributions are as follows:               the speaker is unknown or enrollment is mismatched. Post-
   • Task and metric. We give a formal definition of               VAD diarization [23] is accurate offline but introduces multi-
      enrollment-free foreground (dominant-speaker-selective)      stage latency. FVAD differs from previous paradigms in sev-
      VAD, and introduce the Background False-Alarm Rate           eral ways: the foreground is inferred endogenously from the
      (BG-FAR) metric: the probability of firing while only        signal (no enrollment), committed to as a single coherent
      competing speech is active and the foreground is silent,     identity (unlike diarization, which tracks everyone, or energy-
      gated by foreground F1, directly measuring the identity-     or saliency-following gates, which follow whoever is momen-
      commitment the task demands.                                 tarily loudest), and produced by one streaming detector (no
   • New benchmark. We introduce Mix-Interference, in              cascade).
      which the target foreground track is mixed with compet-                          III. M ETHODOLOGY
      ing speech at controlled SNRs, and adapt VOiCES [17]
      (real far-field television and babble noise) as a cross-     A. Interference-Aware Data Recipe
      check. We will release Mix-Interference to spur further         Training data. We propose a fully automatic pipeline
      work on FVAD.                                                for constructing large-scale VAD training data without hu-
   • Data recipe. We propose a fully automatic pipeline that       man annotation. Clean utterances are first pseudo-labelled by
      yields large-scale frame-level FVAD supervision without      Silero-v6 [1], then passed through an energy-adaptive edge
      human annotation, and show through controlled architec-      refinement that relocates each segment’s onset and offset to
      ture and data ablations that the recipe is what primarily    the local acoustic boundary. This places the decision threshold
      unlocks foreground focus.                                    a fixed fraction of the way from the local noise floor toward
   • State-of-the-art model. We develop Mamba-FVAD, a              speech energy, with separate onset/offset factors to absorb the
      lightweight streaming model that surpasses mainstream        asymmetric boundary lag of the base detector. The refinement
      commercial VADs and specialized speaker-aware systems        algorithm in effect tightens the labels without discarding
      on the proposed benchmark while remaining competitive        low-energy speech. The training corpus was assembled from
      on conventional VAD in clean and noisy conditions.           an in-house Japanese call-centre dataset of real conversa-
                                                                   tional speech (1,128 hours) and concatenated LibriSpeech read
                     II. R ELATED W ORK                            speech with inter-utterance silences, similar to the recipe used
   Production VADs, including Silero [1], TEN-VAD [2],             by LibriVAD [24].
MarbleNet [18], and related neural detectors [3], [7], [8], give      Dynamic Augmentation. Rather than pre-computing fixed
robust, low-latency frame-level detection but are trained to       mixtures, augmentations are applied stochastically per utter-
detect all speech. For example, competing speakers are treated     ance at load time, so every epoch presents new conditions. The
as positive examples rather than interference, so speaker selec-   selectivity-bearing component is competing-speaker mixing.
tion is therefore not naturally carried out—a gap we address       One to three interfering-speaker segments, sampled from a
with FVAD. A common deployment remedy gates a VAD by               held-out speech pool and covering 10–50% of the utterance,
signal energy, assuming the foreground is closest to the mi-       are mixed into the foreground at a target-to-interference ratio
crophone; but instantaneous energy is an unreliable proxy for      (measured over speech-active frames) of 0–15 dB, with a
probability p of 0.2. Each interfering segment is rendered as                                                            interference-aware (IA). As a control, we also train each
a background source via far-field simulation by convolving                                                               backbone under the conventional LibriVAD recipe [24] to
it with a room impulse response (RIR) sampled from the                                                                   isolate the recipe’s contribution.
DNS-Challenge [25] (50/50 simulated and real recorded RIRs)
and applying a random 1–4 kHz low-pass that models far-                                                                  C. Benchmark Creation
field high-frequency roll-off. The foreground labels are left                                                               Mix-Interference is a controlled benchmark that pits a
unchanged, so this competing speech is supervised as negative.                                                           single foreground speaker against one competing background
The remaining augmentations target general robustness, each                                                              speaker at known relative levels. Foreground utterances are
applied independently: environmental-noise mixing (p=0.45;                                                               drawn from concatenated LibriSpeech [26] test-other record-
scattered or full-length; bimodal SNR, easy [5, 20] dB / hard                                                            ings, with frame-level VAD labels (31.25 Hz) from an energy-
[-5, 5] dB), music mixing (p=0.15; [5, 20] dB), room rever-                                                              based labeler, where these labels define the foreground (target)
beration on the target (p=0.2), gain perturbation (±6 dB) with                                                           throughout. For each foreground clip we synthesize seven
per-segment level dynamics, hard non-speech negatives (noise-                                                            temporally-aligned 16 kHz variants: (1) the clean target;
, silence-, music- and far-field-speech-only clips, 1–2% each),                                                          (2) target + environmental noise, and (3–7) target + the
and telephone band-pass filtering (300–3400 Hz / 50–7000                                                                 same noise + a competing speaker at five fixed target-to-
Hz), sharpening rejection without eroding foreground recall.                                                             interference SNRs of 9, 11, 13, 15, 17 dB. The competing
                                                                                                                         speaker is a different test-other utterance, passed through a far-
B. Model Architecture and Experimental Setup                                                                             field simulation (random small/medium room, near/medium
                                                                                                                         distance, 4–8 kHz low-pass filter) and offset by a random
              512 sampling points, 32ms
                         ......                                                                                          temporal delay (±10 s) so it behaves as an intermittent
                                                                                                                New
                                                                                                                         background talker. All level ratios are computed over speech-
Frames:
                                                                                                               Frame
                                                                                                                         active frames (VAD-weighted RMS): noise is mixed at ≈15
                                                            LEAF              LEAF            LEAF             LEAF
                         LEAF Encoder
                                                           Encoder           Encoder         Encoder          Encoder    dB SNR for the interference variants and a harsher ≈6 dB for
 Model:
                        Temporal Decoder
                                                                    hidden
                                                           Temporal state
                                                                                      hidden         hidden
                                                                             Temporal state Temporal state    Temporal   the noise-only variant, and each mixture is peak-normalized to
                                                           Decoder           Decoder         Decoder          Decoder
                                                                                                                         0.95. Crucially, every variant retains the foreground-only VAD
Results: not-                               not-   not-      not-              not-
               speech    speech speech                                                        speech           speech
        speech                             speech speech    speech            speech                                     labels; the competing speaker is never labeled as speech so
                        a) Training                                                 b) Inference
                                                                                                                         the benchmark directly measures whether a model tracks the
Fig. 1: Overall architecture of the proposed Mamba-FVAD                                                                  foreground while rejecting background speech. Because the
framework.                                                                                                               five mixed variants share the same target, noise, and interferer
                                                                                                                         and differ only in the interferer’s level, the takes are frame-
   To train for FVAD, we pair a learnable acoustic front-                                                                locked, enabling paired per-frame contrasts.
end with a temporal backbone and a per-frame classification                                                                 VOiCES devkit [17] was adapted as an out-of-distribution
head, processing raw audio frame-wise (Fig.1). The front-                                                                FVAD benchmark to test whether foreground selectivity trans-
end is a LEAF encoder [12] adapted for streaming: temporal                                                               fers to physically recorded far-field speech. Unlike Mix-
pooling is removed and Gaussian pooling replaced by global                                                               Interference, nothing is mixed at conversion time: clean
average pooling to preserve frame-level resolution, operating                                                            LibriSpeech utterances are replayed through a loudspeaker
on pre-segmented 512-sample frames at a fixed 31.25 Hz.                                                                  and re-recorded by far-field microphones in real rooms, so
Because selectivity is conferred by the data (Sec.III-A), the                                                            reverberation, distance, and the distractor, categorized as none
backbone is free to be chosen for deployment. Our primary                                                                (clean), musi (music), or babb/tele (competing background
system, Mamba-FVAD (∼0.6M parameters), uses a Mamba                                                                      speech), are physically baked into the signal. We keep the
state-space decoder [13], whose linear-time recurrence gives                                                             distant recording as input and attach foreground-only labels
O(1) per-frame compute and memory and thus low-latency,                                                                  by keying the target speaker’s word-level timestamps from the
CPU-only real-time operation. To study how much temporal                                                                 original source forced alignments to each segment, while the
context foreground selectivity requires, we compare three                                                                recorded background talkers in babb/tele stay unlabeled, i.e.
iso-parameter backbones spanning context capacity under an                                                               negative. This makes the competitors real recorded speakers
identical recipe: the Mamba above; an LSTM [14], that is                                                                 rather than synthetic mixtures. Since every segment is recorded
a recurrent model with more limited effective context [15];                                                              under all conditions and frame-aligned, the matched none take
and a Transformer [16], with unbounded in-window context                                                                 serves as a per-frame clean reference for paired metrics like
but length-growing cost, serving as an offline upper bound.                                                              BG-FAR.
Mamba and the LSTM run at O(1) per-frame cost and stream;
the Transformer does not.                                                                                                D. Evaluation Metrics
   All backbones train with AdamW (lr 10−4 , weight decay                                                                   Conventional VAD scores, namely speech against non-
0.01, cosine schedule with linear warmup), batch size 16,                                                                speech F1 or ROC-AUC, cannot measure FVAD because they
dropout 0.3, and bf16 mixed precision; and the Transformer                                                               treat all speech as positive; a perfect foreground detector that
a reduced learning rate and longer warmup, for stable conver-                                                            suppresses a competing speaker would be charged with false
gence. We call models trained with our recipe (Sec. III-A)                                                               negatives. We therefore evaluate against foreground labels with
two complementary frame-level metrics that separate the two                                                                                 Mix-Interference
                                                                                                    1.0
distinct ways an FVAD model can fail, either by missing the                                                                                                           Mamb-FVAD (IA)
                                                                                                                                                                      LSTM-FVAD (IA)
target, or firing on a competitor.                                                                                                                                    Mamba VAD (libriVAD)




                                                                     BG-FAR ( rejects background)
                                                                                                    0.8                                                               LSTM VAD (libriVAD)
   Foreground F1 measures how well the model tracks the                                                                                                               Silero v6
                                                                                                                                                                      pVAD (enrolled)
target. With foreground-speech frames as positives, it is the                                                                                                         Standard VAD (pVAD arch)
                                                                                                    0.6                                                               Auditok
harmonic mean of precision and recall. Recall penalizes
missed foreground speech and precision penalizes activation                                         0.4
on any foreground-silent frame (silence, noise, or competing
speech). Reported together with its recall component, it acts                                       0.2
as a gate; a model cannot appear “selective” merely by being                                              marker size interferer loudness
                                                                                                          (big = 9 dB, small = 17 dB)
conservative as suppressing the target collapses recall and                                         0.0
hence F1.                                                                                                                                       VOiCES
                                                                                                    1.0
   Background False-Alarm Rate (BG-FAR) isolates the                                                         Distractor
                                                                                                               Music
behavior that defines the task, that is, firing on a competing                                                 Babble




                                                                     BG-FAR ( rejects background)
                                                                                                    0.8        Telephone
background speaker. It is the false-alarm rate computed only
over frames where the foreground is silent yet a background                                         0.6
source is active:
                                                                                                                       Model
BG-FAR = P (yτ = 1 | foreground-silent∧background-active)                                           0.4        Mamb-FVAD (IA)
                                                                                                               LSTM-FVAD (IA)
                                                                                                               Mamba VAD (libriVAD)
                                                                                                               LSTM VAD (libriVAD)
   Ordinary FAR over all silent frames is dominated by                                              0.2        Silero v6
                                                                                                               pVAD (enrolled)
easy true silence and dilutes this signal, by conditioning on                                                  Standard VAD (pVAD arch)
                                                                                                               Auditok
background-active frames, we target exactly the hard case. We                                       0.0
                                                                                                      0.55      0.60       0.65     0.70      0.75   0.80      0.85     0.90      0.95      1.00
obtain a frame-exact background-active mask without extra                                                          Foreground F1 (tracks target, penalizes over-firing )
annotation by exploiting paired, frame-aligned takes from
the benchmark datasets. Each clip has a matched reference         Fig. 2: BG-FAR vs. Foreground F1 for Mix-Interference
with the same foreground and environment but no competing         swept over SNR (9–17 dB) (top), and VOiCES by distractor
speaker (the noise-only take in Mix-Interference, the none        (bottom). The ideal FVAD model falls in the bottom-right.
take in VOiCES), and a foreground-silent frame is marked
background-active when its energy exceeds the reference by
more than a margin δ (6 dB in this paper). BG-FAR is bounded      yet collapse into this high-BG-FAR region, isolating the data
by 0 and 1, denoting complete rejection and complete accep-       recipe as the cause. Among baselines, only the enrolled
tance respectively. In our evaluation, BG-FAR is calculated at    pVAD keeps BG-FAR low at a flat ∼0.23 band, interferer-
an operating threshold of 0.5.                                    independent (as expected from an external speaker prior) but
   The two metrics are decisive only in combination. Genuine      at far lower Foreground F1. Removing that prior (Standard
foreground selectivity requires both high Foreground F1 (the      VAD) returns BG-FAR to the LibriVAD region.
target is detected and the model does not over-fire) and low
BG-FAR (competitors are rejected). Neither suffices alone, for       In VOiCES the distractors form a built-in control: music is
example, a silent model trivially attains BG-FAR = 0 but fails    non-speech, so its BG-FAR measures only generic non-speech
Foreground F1, whereas a generic VAD attains high recall but      suppression, whereas babble and telephone are competing
high BG-FAR. The full algorithms are described in Appendix        speech. The gap between babble/telephone and music thus
A and B.                                                          isolates false alarms specific to background speech; a true
                                                                  speaker-rejecter stays near its music floor, a generic “any-
               IV. R ESULTS AND A NALYSIS
                                                                  speech” detector does not. Mamba-FVAD behaves like the
A. Foreground VAD Performance                                     former: telephone (0.07) sits at the music floor (0.06) and
   Fig. 2 plots BG-FAR against Foreground F1 for our IA-          babble (0.12) only just above, a small speech-specific excess,
and LibriVAD-recipe models against baselines: production-         while Silero shows a much larger gap (music 0.12 vs. tele-
grade Silero-v6, a pretrained pVAD with speaker enrollment1 ,     phone 0.18, babble 0.27). On this out-of-distribution distant-
a Standard VAD (pVAD’s architecture, no enrollment), and          speech set Mamba-FVAD pays a small recall penalty (lower
energy-based Auditok. An ideal FVAD model sits bottom-            Foreground F1) yet rejects background speech as well as or
right with high foreground tracking, low BG-FAR. On Mix-          better than the enrolled pVAD—without enrollment.
Interference our IA models (Mamba-FVAD and its iso-                  Overall, varying the backbone (Mamba→LSTM) under the
parameter LSTM) occupy this region (Foreground F1 0.88-           IA recipe largely preserves the selective behavior, whereas
0.92; BG-FAR from 0.05 at 17 dB to at most 0.40 at 9 dB),         varying the recipe (IA→LibriVAD) collapses it to that of a
while every other system drifts up the BG-FAR axis as the         conventional VAD. We thus attribute foreground selectivity to
interferer becomes louder, exceeding 0.8 at the loudest. Criti-
cally, the LibriVAD-recipe models share the same architectures      1 https://github.com/pirxus/personalVAD
                        TABLE I: Conventional VAD Performance Benchmark, scored by ROC-AUC / F1@0.5
                                                  Ten-VAD                                                                        LibriVAD concat
Model                 KAIST       Voxconverse                     In-house
                                                    test
                                                                                   clean           SNR=-5            SNR=0           SNR=5             SNR=10         SNR=15                SNR=20

webRTC1               – / 0.688     – / 0.433     – / 0.891       – / 0.587       – / 0.930        – / 0.288     – / 0.332          – / 0.332        – / 0.465        – / 0.564         – / 0.675
Auditok2              – / 0.586     – / 0.941     – / 0.886       – / 0.614       – / 0.938        – / 0.802     – / 0.802          – / 0.803        – / 0.807        – / 0.834         – / 0.899
SpeechBrain [27]    0.966 / 0.831 0.858 / 0.960 0.677 / 0.840   0.842 / 0.560   0.874 / 0.916    0.808 / 0.870 0.823 / 0.886      0.821 / 0.893    0.816 / 0.896    0.811 / 0.898     0.808 / 0.899
Pyannote VAD [23]     – / 0.945     – / 0.975     – / 0.917       – / 0.655       – / 0.950        – / 0.890     – / 0.909          – / 0.917        – / 0.923        – / 0.928         – / 0.934
FSMN-VAD [28]         – / 0.932     – / 0.972     – / 0.871       – / 0.705       – / 0.918        – / 0.847     – / 0.895          – / 0.901        – / 0.902        – / 0.903         – / 0.904
Ten VAD [2]         0.989 / 0.927 0.930 / 0.949 0.942 / 0.928   0.969 / 0.851   0.980 / 0.955    0.835 / 0.807 0.882 / 0.880      0.912 / 0.904    0.932 / 0.918    0.948 / 0.927     0.960 / 0.934
MarbleNet [18]      0.994 / 0.947 0.962 / 0.966 0.920 / 0.912   0.973 / 0.616   0.979 / 0.955    0.890 / 0.895 0.919 / 0.912      0.935 / 0.919    0.945 / 0.925    0.953 / 0.929     0.958 / 0.933
Silero-v5 [1]       0.992 / 0.926 0.947 / 0.946 0.925 / 0.903   0.966 / 0.728   0.979 / 0.952    0.846 / 0.809 0.909 / 0.905      0.943 / 0.922    0.963 / 0.932    0.971 / 0.941     0.975 / 0.949
Silero-v6 [1]       0.992 / 0.947 0.952 / 0.952 0.957 / 0.939   0.966 / 0.862   0.981 / 0.960    0.846 / 0.831 0.918 / 0.914      0.946 / 0.930    0.963 / 0.937    0.972 / 0.944     0.976 / 0.953
Mamba-FVAD (IA)     0.986 / 0.910 0.933 / 0.929 0.910 / 0.890   0.982 / 0.884   0.979 / 0.960    0.830 / 0.712 0.916 / 0.884      0.958 / 0.933    0.970 / 0.947    0.974 / 0.953     0.976 / 0.956




interference-aware training, not architectural inductive bias.                                  Section IV-A: it leads on the real-world in-house benchmark,
                                                                                                leads from 5 dB SNR upward on LibriVAD-concat, and stays
B. Conventional VAD Performance                                                                 within a few points of specialist VADs elsewhere. Because
   Foreground selectivity must not cost ordinary detection:                                     the IA recipe pairs competing-speech mixing with standard
with no competing speaker, an FVAD model should reduce                                          noise augmentation, selectivity and general noise-robustness
to a conventional VAD rather than suppress single-talker                                        coexist—the speaker-selective objective adds the former with-
speech. We verify this on three public sets: KAIST3 , Vox-                                      out sacrificing the latter.
Converse [29], Ten-VAD test4 ; and two deployment-relevant
                                                                                                C. Ablations
conditions: a human-annotated in-house benchmark and long-
form LibriVAD-concat. The in-house set is 9.8 h of con-                                            For ablation experiments, all models were trained on the
versational Japanese from real voice-agent interactions in                                      same IA recipe as Mamba-FVAD but on a fixed budget limited
noisy venues (restaurants, meeting rooms, open-plan offices)                                    to 5 epochs.
where background speech and babble are prevalent. Following                                        Competing-speaker mixing. Table II isolates the
FVAD, frame-level human labels mark only the intended                                           selectivity-bearing augmentation via three variants that
speaker as speech, whereas background/overlapping talkers                                       differ only in how overlapping speech is generated: the
and non-speech are negative. Because such calls interleave                                      reference (On) renders each interferer as far-field background;
clean single-talker and competing-speech stretches, it jointly                                  Off completely removes competing-speaker mixing; Nearfield
tests conventional detection and foreground selectivity under                                   keeps the overlap but skips far-field simulation. Off is by far
one label set. For LibriVAD-concat we follow [24], concate-                                     the most damaging. BG-FAR rises across the board, widening
nating LibriSpeech recordings under clean and additive-noise                                    as the interferer grows louder and largest on the real-recorded
(SNR −5 to 20 dB) conditions. As not all baselines expose                                       VOiCES. Never exposed to competing speech, the model
per-frame posteriors, we report ROC-AUC where available and                                     tends to fire on any speech (hence its marginally higher
F1@0.5 threshold as a secondary measure (Table I).                                              foreground recall). This confirms that supervised exposure to
   On the public sets, Mamba-FVAD is broadly competitive,                                       unlabeled competing speech, not generic noise augmentation,
trailing the strongest specialist on each (MarbleNet on KAIST,                                  is the causal ingredient for background-speech rejection.
Pyannote on VoxConverse, Silero-v6 on TEN-VAD) only                                             TABLE II: Competing-speaker augmentation ablation: BG-
slightly and with no categorical failure, while leading on the                                  FAR and foreground recall (fgRec) on Mix-Interference and
in-house benchmark, whose labeling mirrors the FVAD objec-                                      VOiCES.
tive. On LibriVAD-concat it is strong from 5 dB SNR upward,
reflecting the conventional noise/music/RIR augmentation the                                    Speaker
                                                                                                                             Mix-Interference                                 VOiCES

IA recipe includes for robustness. The one weak spot is −5 dB                                   mixing                    BG-FAR ↓                      fgRec ↑           BG-FAR ↓            fgRec ↑

speech-shaped noise (SSN: ROC-AUC 0.70, vs ≥0.93 for                                                        S17     S15    S13      S11    S9 (loud)      S9       musi     babb     tele      babb

non-speech noise). This represents the boundary case of the                                     On (ref)    0.059   0.088 0.140    0.226     0.357       0.946     0.141   0.270 0.183         0.848
                                                                                                Off         0.076   0.112 0.184    0.300     0.462       0.957     0.231   0.342 0.235         0.877
selectivity prior, whose training interferers are always quieter                                Nearfield   0.065   0.091 0.134    0.219     0.359       0.962     0.193   0.313 0.230         0.858
than the target, so a louder, sustained speech-like masker
inverts the dominance cue and the model suppresses the now-                                        Nearfield shows that how the overlap is rendered governs
quietest true foreground.                                                                       real-world transfer. On synthetic Mix-Interference near- and
   In sum, Mamba-FVAD trades a small, localized amount of                                       far-field are nearly indistinguishable, but on VOiCES, where
generic-VAD accuracy for the strong foreground selectivity of                                   competitors are physically distant and reverberant, the far-
  1 https://github.com/wiseman/py-webrtcvad
                                                                                                field reference wins at every distractor, its training interferers
  2 https://github.com/amsehili/auditok                                                         matching real background acoustics. For only a one to two
  3 https://github.com/jtkim-kaist/VAD                                                          point recall cost, far-field competing-speaker mixing both
  4 https://github.com/TEN-framework/ten-vad/tree/main/testset                                  rejects background speech and generalizes.
   Architecture. Table III compares the three iso-parameter          form for representative multi-talker clips (Fig.3). The model’s
temporal decoder backbones under the identical IA recipe on          behavior tracks whether a foreground speaker has been estab-
the conventional VAD benchmarks. Mamba only very slightly            lished. Before the primary speaker enters (first ∼3 s of Fig.3c),
edges out the LSTM, differing by at most ∼2 points of ROC-           no dominant speaker yet exists, so the model falls back to
AUC, with each leading on some sets (Mamba on KAIST                  conventional VAD and marks the preceding speech-plus-noise
0.962 and TEN-VAD 0.910, the LSTM on VoxConverse                     as active. Once the primary speaker appears, it locks onto that
0.930), at comparable parameter count. The Transformer trails        target, and when the speaker stops (∼4 s later) it returns to
on every benchmark despite its larger context. However, we           silence even though background speech continues. Because
acknowledge that the Transformer trained less stably on this         the background spectrum is nearly identical before and after
data regime despite hyperparameter tuning and also required          the target’s turn, this switch cannot be explained by acoustic
chunking on long clips; hence we treat its scores as a floor.        change alone; it reflects learned contextual selection.
                                                                        Selection is not driven by loudness. Near the end of an ut-
TABLE III: Architecture ablation: ROC-AUC across bench-              terance (∼31 s), the target is quiet yet still detected, indicating
marks. LibriVAD-concat is frame-weighted over all noises and         the model holds a stable latent representation of the foreground
SNRs.                                                                rather than tracking instantaneous amplitude. Background talk-
                                                                     ers are consistently suppressed with clean segment boundaries,
                       Vox Ten   In- LibriVAD
Decoder KAIST                                 Params                 and because FVAD carries no explicit speaker-embedding
                      conv. VAD house concat
                                                                     module, it follows speaker changes without re-enrollment,
Transf.      0.893    0.746 0.858 0.927            0.876   615,369   keeping the model lightweight. When no primary speaker is
LSTM         0.953    0.930 0.891 0.977            0.922   662,657   present (Figs. 3(a),(b)), it gracefully reverts to conventional
Mamba        0.962    0.922 0.910 0.978            0.923   615,297   VAD, marking all speech active. Overall, Mamba-FVAD be-
                                                                     haves like human auditory attention—focusing on a target,
   Together with the matched Mamba/LSTM selectivity in               suppressing competitors, and falling back to general-purpose
Section IV-A and the competing-speaker ablation in Sec-              VAD when no target is established—at 1–2 ms per-frame
tion IV-C, the results suggest that foreground selectivity is        latency on an AWS t2.micro instance, confirming real-time
driven primarily by the proposed supervision strategy, while         CPU-only deployment.
the choice of backbone appears to play a secondary role under
                                                                                  V. C ONCLUSION AND L IMITATIONS
the evaluated settings. The backbone is therefore a deployment
choice: we adopt Mamba for its O(1) streaming recurrence,               We formalized Foreground VAD (FVAD), an enrollment-
with the LSTM a near-equivalent, lighter alternative.                free, frame-synchronous task that tracks a single dominant
                                                                     speaker and reduces to conventional VAD when only one
D. Performance Analysis                                              is present, and introduced BG-FAR and Foreground F1 to
                                                                     measure it. Our central finding is that foreground selectivity
                                                                     primarily comes from supervision: a fully automatic recipe
                                                                     pairing foreground-only labels with competing-speaker mixing
                                                                     turns an ordinary streaming VAD selective, and iso-parameter
                                                                     Mamba, LSTM, and Transformer backbones confirm that
                                                                     temporal-modeling capacity is at most a secondary factor. The
                                                                     resulting model, Mamba-FVAD, surpasses commercial VADs
                                                                     and enrollment-based speaker-aware systems on selectivity
     a) Segment A of example          b) Segment B of example        while staying competitive on conventional VAD and main-
                                                                     taining 1–2 ms per-frame CPU latency. The Mix-Interference
                                                                     benchmark will be released to support further study.
                                                                        The selectivity that drives these gains also bounds the
                                                                     method. Because the model commits to a dominant fore-
                                                                     ground, it under-fires when the target is not the domi-
                                                                     nant source: recall falls at extreme negative SNR on all-
                                                                     speech-positive benchmarks, and on out-of-distribution far-
                     c) Whole segment of example
                                                                     field speech (VOiCES) selectivity transfers but foreground
Fig. 3: Mamba-FVAD inference on a multi-talker recording:            recall drops under the acoustic shift. We also assume a single
the model locks onto the dominant speaker (c) while gracefully       foreground speaker per segment, leaving turn-taking and co-
degrading to standard VAD in the absence of a primary speaker        equal speakers to future work.
(a, b).

 To visualize the learned selectivity qualitatively, we overlay
Mamba-FVAD’s frame-level predictions on the input wave-
                               R EFERENCES                                         [20] A. Défossez, G. Synnaeve, and Y. Adi, “Real time speech enhancement
                                                                                        in the waveform domain,” in Interspeech, 2020, pp. 3296–3300.
 [1] S. Team, “Silero VAD: Pre-trained enterprise-grade voice ac-                  [21] D. Liang, N. Shao, and X. Li, “Frame-wise streaming end-to-end speaker
     tivity detector (VAD), number detector and language classifier,”                   diarization with non-autoregressive self-attention-based attractors,” in
     https://github.com/snakers4/silero-vad, 2024.                                      IEEE International Conference on Acoustics, Speech and Signal Pro-
 [2] T. Team, “TEN VAD: A low-latency, lightweight and high-performance                 cessing (ICASSP), 2024, pp. 10 521–10 525.
     streaming voice activity detector (VAD),” https://github.com/TEN-             [22] D. Liang and X. Li, “LS-EEND: Long-form streaming end-to-end
     framework/ten-vad.git, 2025.                                                       neural diarization with online attractor extraction,” IEEE Transactions
 [3] S. Zhang, M. Lei, Z. Yan, and L. Dai, “Deep-FSMN for large vocabulary              on Audio, Speech and Language Processing, vol. 33, pp. 3568–3581,
     continuous speech recognition,” in IEEE International Conference on                2025.
     Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2018, pp.             [23] H. Bredin, R. Yin, J. M. Coria, G. Gelly, P. Korshunov, M. Lavechin,
     5869–5873.                                                                         D. Fustes, H. Titeux, W. Bouaziz, and M.-P. Gill, “Pyannote.Audio:
 [4] S. Ding, Q. Wang, S.-Y. Chang, L. Wan, and I. Moreno, “Personal                    Neural building blocks for speaker diarization,” in IEEE International
     VAD: Speaker-conditioned voice activity detection,” in The Speaker and             Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020,
     Language Recognition Workshop (Odyssey 2020), 2020, pp. 433–439.                   pp. 7124–7128.
 [5] S. Ding, R. Rikhye, Q. Liang, Y. He, Q. Wang, A. Narayanan,                   [24] I. Stylianou, A. kr. Sarkar, N. Dawalatabad, J. Glass, and Z.-
     T. O’Malley, and I. McGraw, “Personal VAD 2.0: Optimizing personal                 H. Tan, “LibriVAD: A scalable open dataset with deep learning
     voice activity detection for on-device speech recognition,” in Inter-              benchmarks for voice activity detection,” 2025. [Online]. Available:
     speech, 2022, pp. 3744–3748.                                                       https://arxiv.org/abs/2512.17281
 [6] D. Wang, X. Xiao, N. Kanda, T. Yoshioka, and J. Wu, “Target speaker           [25] H. Dubey, V. Gopal, R. Cutler, A. Aazami, S. Matusevych, S. Braun,
     voice activity detection with transformers and its integration with end-to-        S. E. Eskimez, M. Thakker, T. Yoshioka, H. Gamper, and R. Aichner,
     end neural diarization,” in IEEE International Conference on Acoustics,            “ICASSP 2023 deep noise suppression challenge,” IEEE Open
     Speech and Signal Processing (ICASSP), 2023, pp. 1–5.                              Journal of Signal Processing, vol. 5, pp. 725–737, 2023. [Online].
 [7] P. R. R. Gudepu, J. M. Koroth, K. Sabu, and M. A. B. Shaik, “Dynamic               Available: https://www.microsoft.com/en-us/research/publication/icassp-
     encoder RNN for online voice activity detection in adverse noise                   2023-deep-noise-suppression-challenge/
     conditions,” in Interspeech, 2023, pp. 5052–5056.                             [26] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, “Librispeech: An
 [8] M. Sharma, S. Joshi, T. Chatterjee, and R. Hamid, “A                               ASR corpus based on public domain audio books,” in EEE International
     comprehensive empirical review of modern voice activity                            Conference on Acoustics, Speech and Signal Processing (ICASSP), 2015,
     detection approaches for movies and tv shows,” Neurocom-                           pp. 5206–5210.
     puting, vol. 494, pp. 116–131, 2022. [Online]. Available:                     [27] M. Ravanelli, T. Parcollet, P. Plantinga, A. Rouhe, S. Cornell, L. Lu-
     https://www.sciencedirect.com/science/article/pii/S0925231222004635                gosch, C. Subakan, N. Dawalatabad, A. Heba, J. Zhong, J.-C. Chou,
 [9] X. Shi, X. Wang, Z. Guo, Y. Wang, P. Zhang, X. Zhang, Z. Guo, H. Hao,              S.-L. Yeh, S.-W. Fu, C.-F. Liao, E. Rastorgueva, F. Grondin, W. Aris,
     Y. Xi, B. Yang, J. Xu, J. Zhou, and J. Lin, “Qwen3-ASR technical                   H. Na, Y. Gao, R. D. Mori, and Y. Bengio, “SpeechBrain: A general-
     report,” 2026. [Online]. Available: https://arxiv.org/abs/2601.21337               purpose speech toolkit,” 2021, arXiv:2106.04624.
[10] M. Rouvier and M. Mohammadamini, “Far-field speaker recognition               [28] Z. Gao et al., “FunASR: A fundamental end-to-end speech recognition
     benchmark derived from the DiPCo corpus,” in Proceedings of the                    toolkit,” in Interspeech, 2023.
     Thirteenth Language Resources and Evaluation Conference (LREC),               [29] J. S. Chung, J. Huh, A. Nagrani, T. Afouras, and A. Zisserman, “Spot
     N. Calzolari, F. Béchet, P. Blache, K. Choukri, C. Cieri, T. Declerck,            the conversation: Speaker diarisation in the wild,” in Interspeech, 10
     S. Goggi, H. Isahara, B. Maegaard, J. Mariani, H. Mazo, J. Odijk,                  2020, pp. 299–303.
     and S. Piperidis, Eds. Marseille, France: European Language
     Resources Association, 2022, pp. 1955–1959. [Online]. Available:                       A PPENDIX A: F OREGROUND F1 ALGORITHM
     https://aclanthology.org/2022.lrec-1.209/
[11] J. Chen, Y. Hu, J. Li, K. Li, K. Liu, W. Li, X. Li, Z. Li,
     F. Shen, X. Tang, M. Wei, Y. Wu, F. Xie, K. Xu, and K. Xie,                    Algorithm 1: Foreground F1. Positives are foreground-
     “FireRedChat: A pluggable, full-duplex voice interaction system                speech frames; precision penalizes any activation on a
     with cascaded and semi-cascaded implementations,” 2025. [Online].
     Available: https://arxiv.org/abs/2509.06502
                                                                                    foreground-silent frame (silence, noise, or competing
[12] N. Zeghidour, O. Teboul, F. de Chaumont Quitry, and M. Tagliasacchi,           speech), recall penalizes missed foreground speech.
     “LEAF: A learnable frontend for audio classification,” International            Input: model f ; threshold θ = 0.5; clips (x, y) with
     Conference on Learning Representations (ICLR), 2021.
[13] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling                                 foreground labels y
     with selective state spaces,” 2024. [Online]. Available:                        Output: Foreground F1
     https://arxiv.org/abs/2312.00752                                                TP ← 0, FP ← 0, FN ← 0;
[14] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural
     Computation, vol. 9, no. 8, pp. 1735–1780, 1997.                                foreach clip (x, y) do
[15] Q. Zhang, M. Chen, Z. Song, H. Liu, X. Zhang, and H. Li, “Long-context              p ← f (x);          // per-frame foreground
     modeling networks for monaural speech enhancement: A comparative                     posteriors
     study,” in IEEE Workshop on Applications of Signal Processing to Audio
     and Acoustics (WASPAA), 2025, pp. 1–5.                                              for t ← 1 to T do
[16] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,                 ŷt ← [ pt ≥ θ ]; // 1 if pt ≥ θ, else 0
     L. Kaiser, and I. Polosukhin, “Attention is all you need,” Advances in                  if ŷt = 1 and yt = 1 then
     Neural Information Processing Systems, vol. 30, 2017.
[17] C. Richey, M. A. Barrios, Z. Armstrong, C. Bartels, H. Franco,
                                                                                                  TP ← TP + 1
     M. Graciarena, A. Lawson, M. K. Nandwana, A. Stauffer, J. van Hout,                     else if ŷt = 1 and yt = 0 then
     P. Gamble, J. Hetherly, C. Stephenson, and K. Ni, “Voices Obscured                           FP ← FP + 1
     in Complex Environmental Settings (VOiCES) Corpus,” in Interspeech,                     else if ŷt = 0 and yt = 1 then
     2018, pp. 1566–1570.
                                                                                                  FN ← FN + 1
[18] F. Jia, S. Majumdar, and B. Ginsburg, “MarbleNet: Deep 1D time-
     channel separable convolutional neural network for voice activity de-
     tection,” in IEEE International Conference on Acoustics, Speech and              P ← TP/(TP + FP), R ← TP/(TP + FN);
     Signal Processing (ICASSP), 2021, pp. 6818–6822.                                 return 2P R/(P + R);
[19] S. Zhao, Z. Pan, and B. Ma, “Clearervoice-studio: Bridging advanced
     speech processing research and practical deployment,” 2025. [Online].
     Available: https://arxiv.org/abs/2506.19398
           A PPENDIX B: BG-FAR ALGORITHM

 Algorithm 2: Background False-Alarm Rate (BG-
 FAR). L OG E NERGY   PH returns per-frame log-energy
 Et = 10 log10 ( H1 i=1 x2(t−1)H+i ) on the 31.25 Hz
 grid (H=512); the reference xr is the noise_only
 take (Mix-Interference) or the none take (VOiCES).
   Input: model f ; threshold θ = 0.5; margin δ = 6 dB;
           clips paired as (xc , xr , y) – condition xc
           (foreground + competing speaker), matched
           reference xr (same scene, no competing
           speaker), foreground labels y
   Output: BG-FAR
   n ← 0;                          // false alarms on
    background-active frames
   d ← 0;             // total background-active
    frames
   foreach paired clip (xc , xr , y) do
       p ← f (xc );       // per-frame foreground
        posteriors
       E c ← L OG E NERGY(xc ),
        E r ← L OG E NERGY(xr );
       for t ← 1 to T do
           if yt = 0 and Etc − Etr > δ then
               d ← d + 1;
               if pt ≥ θ then n ← n + 1;

  return n/d;


            G ENERATIVE AI U SE D ISCLOSURE
   Generative AI tools (ChatGPT, Claude) were used for
grammar checking and polishing the English writing of this
manuscript. All technical content, experimental design, and
scientific conclusions were produced entirely by the authors.

