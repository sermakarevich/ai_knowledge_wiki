# DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events
Source: https://arxiv.org/abs/2609.12872
Kind: pdf
Fetched: 2026-09-22T09:29:47.304596+00:00
Tool: pdftotext

                                                 DUPLEXDRAMA: A SYNTHESIZED DIALOGUE DATASET WITH SCENARIOS,
                                                  FULL-DUPLEX BEHAVIORS, EXPRESSIVE SPEECH, AND SOUND EVENTS

                                         Qingxiang Guo∗ , Wenke Fan, Shuofeng Zhao, Dawei Yang, Zhiyang Zhou, Yingxin Shang, Hongwei Cai,
                                                           Zhou Wang, Weixu Wang, Lin Yang, Shuran Zhou, and Yang Song
                                                                  Zuoyebang Education Technology, Beijing, China


                                                                 ABSTRACT                                     Persona & Scenario
                                                                                                            Role 1 Lisa, 29, nurse · caring but tired                Role 2 Tom, 31, teacher · supportive




arXiv:2609.12872v1 [cs.CL] 11 Sep 2026
                                                                                                               home living · face to face · bedroom vs living room · 11:30 PM
                                         We present DuplexDrama, the first synthesized spoken dia-
                                         logue dataset that simultaneously covers four dimensions: (i)        Dialogue Script
                                                                                                            Role 1 “I’m so tired from the night shift.”
                                         complete persona and scenario settings; (ii) three full-duplex     Role 2 “<env: home living> I know, and my day was—” <user interrupt>
                                         behaviors (interruption, backchannel, incomplete); (iii) ex-       Role 1 “<evt: object hit> <emo: Surprised> Oh no, what happened?”

                                         pressive speech with persona-aligned emotion labels; and (iv)                                                                          overlap      event          environment
                                                                                                               Multi-Track Audio (4 audio files per dialogue)
                                         script-aware sound events. DuplexDrama is built via a 4-stage     Role 1 speech

                                         pipeline; quality validation on both scripts and synthesized      Role 2 speech
                                                                                                              Role 1 bg
                                         audio confirms its quality. We have produced more than 2,000         Role 2 bg

                                         hours audio data with a 64-voice timbre pool spanning 13 per-
                                         sonas and 5 age buckets; 3.8% of all turns carry at least one     Fig. 1. One DuplexDrama sample: persona and scenario
                                         full-duplex behavior. This data has been validated through        metadata, a tagged dialogue script, and four aligned audio
                                         internal full-duplex model training. We will release a curated    tracks in which tagged interruptions surface as real acoustic
                                         subset of 6,400 bilingual dialogues (800 h, Chinese ∼500 h        overlap. Swapping Role 1 and Role 2 yields two training sam-
                                         + English ∼300 h) to advance full-duplex spoken dialogue          ples per dialogue, doubling the usable data.
                                         model research. Data samples are available at our demo page1
                                         and LLM-judge evaluation prompts will be released with the
                                         dataset.                                                          data yet. To our knowledge, no public dataset jointly covers
                                             Index Terms— speech dataset, full-duplex dialogue, TTS        (i) complete persona and scenario annotations—which con-
                                         synthesis, sound event, multimodal dialogue training, LLM-        dition the model’s response style; (ii) systematic coverage of
                                         as-a-judge                                                        the three full-duplex behaviors (interruption, backchannel, in-
                                                                                                           complete); (iii) expressive speech with persona-aligned emo-
                                                                                                           tion labels; and (iv) script-aware sound event injection. Per-
                                                            1. INTRODUCTION                                sonaPlex [10] demonstrates persona-conditioned full-duplex
                                                                                                           conversational modeling; complementing this line of work,
                                         The emergence of large language models has enabled conver-
                                                                                                           DuplexDrama provides a fully open dataset covering all four
                                         sational AI systems that listen and speak simultaneously [1]—
                                                                                                           dimensions. We fill this gap with DuplexDrama, a synthe-
                                         ranging from open-source full-duplex models [2] to commer-
                                                                                                           sized spoken dialogue corpus. Fig. 1 shows one complete
                                         cial systems [3]. Yet training such systems requires full-
                                                                                                           sample.
                                         duplex dialogue data that is severely scarce. Existing TTS-
                                                                                                               DuplexDrama is built via a four-stage pipeline: (§2.1)
                                         synthesized dialogue corpora [4] are predominantly clean
                                                                                                           Persona and scenario generation with consistency constraints;
                                         read speech or simple turn-taking exchanges. Full-duplex
                                                                                                           (§2.2) Script generation with full-duplex behaviors, emotion
                                         benchmarks [5] target evaluation only and remain small in
                                                                                                           tags and sound event tags; (§2.3) IndexTTS2-based [11] ex-
                                         scale. Natural corpora spanning thousands of hours [6, 7, 8, 9]
                                                                                                           pressive speech synthesis with a 64-voice timbre pool span-
                                         ship authentic overlap and backchannel in the audio, yet ship
                                                                                                           ning 13 personas and 5 age buckets, followed by audio assem-
                                         without scripted scenarios, rich persona attributes, or full-
                                                                                                           bly; (§2.4) Script-aware event injection at the trigger word
                                         duplex behavior annotations. Recent persona-conditioned
                                                                                                           via word-level timestamps, with controlled SNR. A quality
                                         full-duplex models [10] target voice and role control, but do
                                                                                                           validator (§2.5) then discards low-quality dialogues, retaining
                                         not release public training corpora. Moreover, background
                                                                                                           only the high-quality subset for release.
                                         noise and sound events can provide multimodal information
                                                                                                               We make the following contributions:
                                         beyond speech, but they are not used in synthesizing dialogue
                                           ∗ Corresponding author: guoqingxiang@zuoyebang.com                    • A four-stage pipeline that constructs a synthesized spo-
                                           1 https://dunjie5465.github.io/duplexdrama-demo/                        ken dialogue dataset jointly covering persona and sce-
       nario, three full-duplex behaviors, persona-aligned ex-                 the LLM is prompted to produce spoken-style dialogue.
       pressive speech, and script-aware sound events, fol-                    Gemini-3.1-pro-preview [13] is used in this stage.
       lowed by a validator to assert quaility.
                                                                               2.3. Full-duplex Dialogue Synthesis
     • An evaluation protocol leveraging dual LLM judges
       (DeepSeek-v4.1-pro and Gemini-3.1-pro-preview) for                      We synthesize expressive speech via IndexTTS2 [11] since
       cross-checking, with evaluation prompts to be released                  it supports disentangled control of speaker timbre and emo-
       alongside the dataset, to enable reproducible script-                   tion. Our voice pool contains 64 speakers spanning 13 core
       rationality assessment (Section 3).                                     personas and 5 age buckets. Most prompt audios are gen-
                                                                               erated by MOSS-Audio [14], while a small fraction curated
     • A full open release of 6,400 bilingual dialogues (800 h),               from natural speech snippets. The seven-class emotion labels
       together with the audio asset bank (600 environmental                   are defined at Stage 2 (§2.2), where the LLM is constrained
       audios and 2,203 sound-event audios) and LLM-judge                      to draw only from these classes in scripts. A speaker prompt
       evaluation prompts, to support reproducible full-duplex                 audio and an emotion tag jointly condition IndexTTS2 at syn-
       spoken dialogue model research.                                         thesis time.
                                                                                   After obtaining per-utterance audio, we first run forced
                             2. PIPELINE                                       alignment (FA) [15] on all utterances to obtain word-level
                                                                               timestamps. We then assemble the utterances by turn order
Figure 2 overviews our four-stage pipeline. Stage 1 generates                  into two parallel tracks for both speakers. Each track only
persona and scenario tuples under consistency constraints.                     carries its own speaker; during the other speaker’s turns, si-
Stage 2 takes these validated tuples and generates dialogue                    lence is inserted to preserve speaker-switch boundaries. This
scripts annotated with three tag families—full-duplex behav-                   yields two long-form speech waveforms.
ior, emotion, and sound-event tags. Stage 3 synthesizes au-                        Full-duplex behaviors are jointly realized with the former
dio via IndexTTS2 [11] with voice–emotion conditioning and                     steps. Specifically, <user incomplete> tags are replaced
concatenates per-utterance segments in script order. Stage 4                   by literal “. . . ” inside sentence, which IndexTTS2 renders
constructs a background channel for each speech channel with                   as in-sentence pauses during synthesis. During audio assem-
both environmental noise and sound events. The pipeline pro-                   bly, for an <user interrupt> tag, the corresponding ut-
duces long-form dialogue audios. A quality validator then fil-                 terance fades out briefly while the other turn is brought in,
ters each dialogue; failures are discarded before release.                     producing acoustic overlap; for an <user backchannel>
                                                                               tag, the corresponding utterance is time-aligned and overlaid
2.1. Persona and Scenario Generation                                           onto the other track which continues speaking, yielding si-
                                                                               multaneous speech.
We first construct two complementary seed pools via
DeepSeek-v4.1-pro [12]: a persona pool covering 24 macro
                                                                               2.4. Background Channel Realization
categories and 134 sub-types organized by social function,
and a topic pool covering 46 macro categories and 404 sub-                     Stage 2 (§2.2) already places environmental noise and sound-
types organized by narrative scenario. From each pool we                       event tags at semantically meaningful positions in the script.
draw a seed, then DeepSeek-v4.1-pro expands the seed into                      Stage 4 realizes those tags into audio.
a dialogue setup that couples two persona tuples2 with a sce-                      We construct two background channels per dialogue, each
nario specification3 under consistency constraints.                            paired with one speech channel and combining environmen-
                                                                               tal noise and sound events. Environmental noise is drawn
2.2. Dialogue Script Generation                                                from a self-built bank of 7 scene categories and 600 long-
                                                                               duration clips. Each noise instance persists for several turns,
In Stage 2, the LLM follows the validated persona–scenario                     which is decided at script generation time. Sound events
tuple and generates the dialogue script annotated with                         are drawn from a separate bank of 52 categories and 2,203
three orthogonal tag families: (i) full-duplex behavior                        short-duration clips. Each event tag is matched to an asset
tags (<user interrupt>, <user backchannel>,                                    and inserted at the FA-aligned trigger position (Fig. 3). Both
<user incomplete>);          (ii) proper emotion tags                          background noise and sound-event loudness are controlled by
([Neutral],        [Happy],        [Angry],       [Sad],                       configurable SNR. Finally, each speech channel pairs with a
[Whispering],         [Hesitant],         [Surprised])                         time-aligned background channel. In general, training a full-
aligned with IndexTTS2; (iii) environmental noise and                          duplex model only requires the background channel at the in-
sound event tags referencing the audio bank. In addition,                      put (HM) side.
   2 name, gender, age, occupation, personality, role.                             All audio assets are drawn from publicly accessible
   3 scene, tone, narrative type, scene medium, an event chain of three pro-   sources and processed strictly for non-commercial, academic
gressing events, and a segmented emotional arc.                                research purposes.
                                                                     Build Stage




                                                        Scripts w.                                                                                                                                   Long-form
 Seed Topic                                                                                                            Construct
                        Persona &                       Behavior,                   TTS & Audio                                                           Quality                                     Dialogue
                                                                                                                      background
                         Scenario                        Emotion                     Assemble                                                            Validator
                                                                                                                        channel
                                                         & Event



Fig. 2. DuplexDrama pipeline generating persona, behavior/emotion/event-tagged scripts, dual-track long-form speech wave-
forms with full-duplex behaviors surfaced as acoustic overlap, and script-aware event mixing, followed by a quality validator.


      Audio Assets                       Dialogue Script                  Output
                              Turn 4 (HM, A)
                                                                                                    Table 1. Dataset overview of the released corpus.
    doorbell
    page turn
                              “. . . the pen slipped
                              out and hit the floor.”
                                                                                                                         Metric                                              Value
    footstep          match                                     inject
    object hit                event class: object hit                     mixed audio                                    Dialogues                                          6,400
    cup glass                 FA onset:        2.34 s                    speech + event                                  Total audio (hours)                                  800
                                                                                                                         Avg. dialogue length (s)                             460
                                                                                                                         Turns                                             ∼362k
Fig. 3. Sound-event realization: assets from the audio
                                                                                                                         Avg. turn length (s)                                   8
bank are matched against the event class tag emitted by                                                                  Voice timbres                                         64
Stage 2 (§2.2), aligned to the trigger word’s onset by forced
alignment of the synthesized speech, and mixed in at the con-
figured SNR.                                                                               Table 2. Full-duplex behavior tag counts and shares across
                                                                                           all turns.
                                                                                                             Behavior Tag                                        Count                   Share
2.5. Quality Validation
                                                                                                             <user interrupt>                                       8,996                    2.4%
We employ a dual-LLM (DeepSeek-v4.1-pro [12] and                                                             <user backchannel>                                     2,455                    0.6%
                                                                                                             <user incomplete>                                      2,271                    0.7%
Gemini-3.1-pro-preview [13]) framework to evaluate scripts
on three dimensions: asset rationality of the manually curated
audio bank (judged by the single Gemini-3.1-pro-preview
multimodal model), tag rationality in scripts, and script-                                 3.2. Data Quality Validation
scenario consistency, with the latter two cross-checked by                                 We evaluate each generated dialogue on the four objective
both LLMs. The synthesized audio is then evaluated along                                   audio metrics defined in Section 2.5; script-tag rationality is
four objective metrics: WER (Qwen3-ASR [15]), audio qual-                                  reported separately in Section 3.2.2. The results are listed as
ity via UTMOSv2 [16] and NISQA [17] (MOS), and SpkCons                                     follows.
via SpeechBrain [18] cosine similarity. Dialogues with Sp-
kCons below 0.9 are discarded following [4].                                               3.2.1. Objective Audio Quality Metrics
                                                                                           Note that both Word Error Rate (WER) and speaker consis-
                     3. DATASET ANALYSIS                                                   tency (SpkCons) are performed on clean TTS audio (without
                                                                                           background), since those two metrics evaluate speech itself
In this section, we analyse the dataset through intrinsic met-
rics organized into three sub-sections. Section 3.1 reports                                   40%
                                                                                                            32.55%
dataset statistics; Section 3.2 reports quality validation; Sec-                              30%
                                                                                                                              23.68%
tion 3.3 compares with prior corpora.                                                         20%
                                                                                                                                       19.52%

                                                                                                                                                        11.40%
                                                                                              10%                                                                          5.60%
                                                                                                                                                                                             3.69%            3.56%

3.1. Dataset Statistics                                                                                      in   g      ti
                                                                                                                           nd          of
                                                                                                                                          e             oor                bb y              ur
                                                                                                                                                                                               nt
                                                                                                                                                                                                          in
                                                                                                                                                                                                               e
                                                                                                            liv              oo          fic          ou               lo                       a           sid
                                                                                                        e                       r                       td       pu
                                                                                                                                                                                         sta             e
                                                                                                     ho                  ie                      ee                bl                   re           vehi
                                                                                                        m               qu                          t                 ic            fe                   cl
We summarize the released corpus through four views: an                                                                                         str                                ca

overview table (Table 1), a full-duplex behavior-tag table (Ta-
ble 2), and two bar charts depicting the distributions of envi-                            Fig. 4. Distribution of environment background tags across
ronment background and sound-event tags (Fig. 4, Fig. 5).                                  the seven scene categories.
  15%
                12.44%
                                                                                                                                                  Table 4. LLM validation results including asset rational-
  10%                          8.92%           8.48%
                                                                                                                                                  ity score of audio asset, tag plausibility score and rationality
                                                            8.10%
                                                                         6.26%                                                                    score between dialogue settings and scripts. All scores range
                                                                                      5.20%
      5%
                                                                                                 4.68%          4.67%      4.37%          4.22%   from 0 to 5. (Env. for environment noise and Evt. for sound
                                                                                                                                                  event.)
                    ct         fl
                                   e           on           ve           or           ng         an
                                                                                                     d
                                                                                                              hi
                                                                                                                 t
                                                                                                                           ac
                                                                                                                              e           le                       Asset rationality Tag rationality        Script
                je            uf              ti         mo           do           pi           st                       rf            st
            ob                            ra            h           in           ty                        ct                        ru
                          sh                                                                                          su
       pu
           t
                     pe
                         r
                                       vi
                                          b
                                                    ot
                                                   cl         st
                                                                 ep
                                                                           oa
                                                                              rd
                                                                                        r
                                                                                            t
                                                                                           si         ob
                                                                                                         je
                                                                                                                 oc
                                                                                                                     k          ot
                                                                                                                                   h              Model            Env       Evt       Env       Evt        consist.
  ck             pa                or           t           ot           yb           ai                        kn            cl
 pi                            p              if                                   ch
               or             ta          sh             fo           ke
           rn             e
                         on             dy                                                                                                        DeepSeek [12] —             —        4.77      4.57        4.43
       tu                           bo
  ge
 pa
                     ph
                                                                                                                                                  Gemini [13]   4.10         4.61      4.86      4.94        4.16


Fig. 5. Top-10 sound-event tags across five macro-classes,
sorted descending by share.                                                                                                                       Table 5. Comparison with prior corpora: Dur. (hr) total au-
                                                                                                                                                  dio duration in hours; Type (natural / synthesized); ① persona
and should not be affected by additive background noise. UT-                                                                                      + scenario; ② full-duplex status; ③ sound event. SDF abbre-
MOSv2 and NISQA are predicted on both the clean TTS au-                                                                                           viates SpeechDialogueFactory. Legend: ✗ absent, ✓ present.
dio and the mixed (with background) audio as comparison.                                                                                               Dataset            Dur. (hr)    Type      ①      ②    ③
Table 3 reports the per-dialogue scores; the middle column                                                                                             Fisher [6]           2,000      natural   ✗      ✗    ✗
flags whether each metric is evaluated on clean, mixed, or                                                                                             CANDOR [7]            850       natural   ✗      ✗    ✗
both audio. As expected, mixing the background costs UT-                                                                                               Open-Yap-1K [9]      1,000      natural   ✗      ✗    ✗
MOSv2 only 0.05 but NISQA-MOS 0.47, since UTMOSv2                                                                                                      DuplexConv [8]       2,000      natural   ✗      ✓    ✓
targets the naturalness of synthetic speech while NISQA also                                                                                           SDF [4]               146       synth.    ✓      ✗    ✗
penalises additive noise; the speech itself is therefore left in-                                                                                      Ours                  800       synth.    ✓      ✓    ✓
tact. We attribute the lower-than-typical UTMOSv2 scores
primarily to the diverse persona stylings and emotion injec-
tion in our synthesized audio.
                                                                                                                                                  sational speech as acoustic baselines but ship without any of
Table 3. Per-dialogue audio-side objective metrics: WER                                                                                           our four annotation dimensions. Open-Yap-1K [9] and Du-
/ SpkCons / UTMOSv2 / NISQA. Middle column: ✗ clean                                                                                               plexConv [8] ship large-scale natural conversational record-
speech, ✓ mixed audio.                                                                                                                            ings with speaker overlap, yet both lack scripted scenarios,
                                                                                                                                                  persona attributes, and sound-event annotations. SpeechDi-
                               Metric                                         w. bg                   Value
                                                                                                                                                  alogueFactory [4] is a synthesized corpus that provides per-
                               WER                                               ✗                  1.8%                                          sona and scenario annotations but does not cover full-duplex
                               SpkCons                                           ✗                 97.3%                                          scenarios. Our proposed DuplexDrama is the only corpus that
                               UTMOSv2                                          ✗/✓              2.57 / 2.52                                      jointly covers all four annotation dimensions, with the script-
                               NISQA — MOS                                      ✗/✓              3.65 / 3.18                                      aware sound event tags being unique to our work.


3.2.2. Script Rationality Validation via Dual LLM Judges
We employ LLM judges to evaluate three dimensions:                                                                                                                     4. CONCLUSION
(i) asset rationality, (ii) rationality of background tags, and
(iii) script-scenario consistency. Dimensions (i) and (iii) are
cross-checked by both DeepSeek-v4.1-pro [12] and Gemini-                                                                                          We present DuplexDrama, the first TTS-synthesized spoken
3.1-pro-preview [13]; dimension (ii) is judged by the single                                                                                      dialogue dataset jointly covering persona and scenario anno-
Gemini-3.1-pro-preview multimodal model since the audio                                                                                           tations, full-duplex behaviors, expressive speech, and sound
bank is manually curated. Table 4 reports average scores after                                                                                    events. The corpus is built through a four-stage pipeline and
filtering.                                                                                                                                        evaluated along four objective audio metrics, with dual-LLM
                                                                                                                                                  cross-checking of script rationality. We will release approxi-
                                                                                                                                                  mately 800 hours of data to facilitate research on full-duplex
3.3. Comparison with Other Datasets
                                                                                                                                                  spoken dialogue modeling. Future work will pursue more re-
Table 5 compares our released DuplexDrama with five prior                                                                                         alistic duplex label distributions, paralinguistic phenomena in
corpora. Fisher [6] and CANDOR [7] supply natural conver-                                                                                         TTS output, and more flexible sound-event label matching.
Acknowledgement                                                    [10] R. Roy, J. Raiman, S.-g. Lee, T.-D. Ene, R. Kirby,
                                                                        S. Kim, J. Kim, and B. Catanzaro, “PersonaPlex: Voice
AI Disclosure. LLMs were used solely to polish English dur-             and role control for full duplex conversational speech
ing manuscript preparation; all technical content is authored           models,” in Proc. ICASSP, 2026, arXiv:2602.06053.
and verified by the human authors, who take full responsi-
bility for the final text. Compliance with Ethical Standards.      [11] S. Zhou, Y. Zhou, Y. He, X. Zhou, J. Wang, W. Deng,
DuplexDrama is constructed from TTS synthesis and publicly              and J. Shu, “IndexTTS2: A breakthrough in emotionally
available audio; no human subject data was used; ethical ap-            expressive and duration-controlled auto-regressive zero-
proval was not required. Conflicts of Interest. None.                   shot text-to-speech,” in Proc. AAAI, 2026, pp. 35139–
                                                                        35148.

                     5. REFERENCES                                 [12] DeepSeek-AI,     “DeepSeek-V4: Towards highly
                                                                        efficient million-token   context intelligence,”
 [1] J. Lu, Y. Wang, J. Luo, Y. Chen, T. Liang, S. Ji, Z. Jiang,        https://huggingface.co/deepseek-ai/
     X. Yang, Y. Zhang, X. Cheng, C. Wen, C. Pan, H. Wang,              DeepSeek-V4, 2026.
     C. Ye, J. Wu, X. Jiang, G. Jiang, and Z. Zhao, “A survey
     of full-duplex spoken dialogue systems: Architectural         [13] Google DeepMind, “Gemini 3.1 Pro Preview,”
     hierarchy, interaction ontology, and decision state ma-            https://ai.google.dev/gemini-api/
     chine,” arXiv preprint, 2026, arXiv:2606.19453.                    docs/models/gemini-3.1-pro-preview,
                                                                        2026.
 [2] A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez,
     H. Jégou, E. Grave, and N. Zeghidour, “Moshi: a              [14] C. Yang, C. Yu, H. Chen, J. Zhu, J. Chen, K. Chen,
     speech-text foundation model for real-time dialogue,”              W. Wang, Y. Wang, Y. Jiang, Y. Jiang, Z. Lin, Z. Chen,
     arXiv preprint, 2024, arXiv:2410.00037.                            Z. Fei, C. Liu, D. Yu, J. Zhan, K. Yu, K. Huang, L. Fan,
                                                                        M. Chen, Q. Cheng, R. Li, S. Li, S. Wang, X. Zhao,
 [3] OpenAI, “GPT-4o system card,” arXiv preprint, 2024,                Y. Gao, Y. Gong, Y. Zhang, Z. Xu, and X. Qiu, “MOSS-
     arXiv:2410.21276.                                                  Audio Technical Report,” 2026, arXiv:2606.01802.

 [4] M. Wang, Y. Bai, Y. Wang, T.-T. Vu, E. Shareghi, and          [15] X. Shi, X. Wang, Z. Guo, Y. Wang, P. Zhang, X. Zhang,
     G. Haffari, “SpeechDialogueFactory: A framework for                Z. Guo, H. Hao, Y. Xi, B. Yang, J. Xu, J. Zhou, and
     natural speech dialogue generation,” in Proc. Inter-               J. Lin, “Qwen3-ASR technical report,” arXiv preprint,
     speech, 2025.                                                      2026, arXiv:2601.21337.

 [5] G.-T. Lin, S.-Y. S. Kuan, Q. Wang, J. Lian, T. Li,            [16] K. Baba, W. Nakata, Y. Saito, and H. Saruwatari, “The
     S. Watanabe, and H.-y. Lee, “Full-Duplex-Bench v1.5:               t05 system for the VoiceMOS Challenge 2024: Transfer
     Evaluating overlap handling for full-duplex speech                 learning from deep image classifier to naturalness MOS
     models,” in Proc. ICASSP, 2026, arXiv:2507.23159.                  prediction of high-quality synthetic speech,” in Proc.
                                                                        IEEE Spoken Language Technology Workshop (SLT),
 [6] C. Cieri, D. Miller, and K. Walker, “The Fisher corpus:            2024, pp. 818–824.
     a resource for the next generations of speech-to-text,” in
                                                                   [17] G. Mittag, B. Naderi, A. Chehadi, and S. Möller,
     Proc. LREC, 2004.
                                                                        “NISQA: A deep CNN-self-attention model for multidi-
 [7] A. Reece, G. Cooney, P. Bull, C. Chung, B. Dawson,                 mensional speech quality prediction with crowdsourced
     C. Fitzpatrick, T. Glazer, D. Knox, A. Liebscher, and              datasets,” in Proc. Interspeech, 2021, pp. 2117–2121.
     S. Marin, “The CANDOR corpus: insights from a large           [18] M. Ravanelli, T. Parcollet, P. Plantinga, A. Rouhe,
     multimodal dataset of naturalistic conversation,” Sci-             S. Cornell, L. Lugosch, C. Subakan, N. Dawalatabad,
     ence Advances, vol. 9, no. 13, pp. eadf3197, 2023.                 A. Heba, J. Zhong, J.-C. Chou, S.-L. Yeh, S.-W. Fu, C.-
 [8] C. Wang, C. He, Z. Zhu, and L. Xie, “DuoConv:                      F. Liao, E. Rastorgueva, F. Grondin, W. Aris, H. Na,
     Large-scale chinese full-duplex speech datasets for                Y. Gao, R. De Mori, and Y. Bengio, “SpeechBrain: A
     conversational AI,” https://huggingface.co/                        general-purpose speech toolkit,” arXiv preprint, 2021,
     datasets/qualialabsAI/DuplexConv, 2026.                            arXiv:2106.04624.

 [9] The Agentic Data Company,            “Open yap 1k:
     Channel-separated english natural two-speaker conver-
     sations,” https://theagenticdatacompany.
     com/open-yap-1k, 2026.

