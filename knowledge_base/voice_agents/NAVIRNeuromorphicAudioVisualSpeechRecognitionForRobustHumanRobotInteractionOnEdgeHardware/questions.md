---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware

### Q1. Why does NAVIR turn to audio-visual fusion, and what deployment tension motivates its neuromorphic design?
> [!tip]- Answer
> Audio-only ASR collapses under industrial machinery and ventilation noise, forcing workers back to keypads or switches that slow work and compromise hands-free safety. AVSR borrows the human McGurk-effect redundancy by adding lip-motion, which restores robustness at low SNR, but SOTA AVSR needs 3D convolutions, recurrence, attention, and large language models that exceed edge budgets. See [[wiki/01-introduction-and-contributions|Introduction and Contributions]].

### Q2. How do SNNs save energy in principle, and why does NAVIR restrict itself to convolutional SNNs on the AKD1000?
> [!tip]- Answer
> SNNs replace dense floating-point multiply-accumulate (MAC) operations with sparse event-driven accumulate (AC) operations over binary spikes, so energy scales with activity rather than nominal capacity. Direct deep training became feasible via surrogate-gradient spatio-temporal backpropagation, residuals, and spiking transformers, but the AKD1000 supports only sequential convolutional inference via MetaTF/CNN2SNN, precluding recurrence and attention. See [[wiki/02-neuromorphic-background|Neuromorphic Background: SNN Architectures and the AKD1000]].

### Q3. What does the GRID lip-reading SOTA table show, and what gap does NAVIR target?
> [!tip]- Answer
> Overlapped-speaker GRID SOTA improved from LipNet 4.80% (2016) to Wu et al. 1.83% (2024), while unseen-speaker results stay far worse (9.70–11.40%), and every baseline uses 3D convolutions, recurrence, or attention unsupported on the AKD1000. No published results exist for full AVSR fusion on GRID under noisy audio, which is both the literature gap and the comparison point for a neuromorphic approach. See [[wiki/03-related-work-akida-and-grid-sota|Related Work: AKD1000 Applications and GRID Lip-Reading State of the Art]].

### Q4. How is the NAVIR encoder pipeline factorised to stay AKD1000-compatible?
> [!tip]- Answer
> Because the AKD1000 lacks 3D convolutions, recurrence, and attention, each video frame is encoded individually by a per-frame spatial encoder, the embeddings are stacked into a 2D time-by-features map, and a second network applies temporal convolutions to yield one video-clip embedding. Audio runs in parallel through an MFCC spectrogram encoder, and both clip embeddings are concatenated into a joint representation for a lightweight MLP predictor head. See [[wiki/04-architecture-and-decoding|Architecture Purpose-Designed for the BrainChip Akida]].

### Q5. How do constrained beam-search decoding, CTC training, and hybrid quantization work in NAVIR?
> [!tip]- Answer
> Training uses CTC loss with a blank label to marginalise over frame-to-token alignments, and inference decodes the T-by-V score matrix with grammar-constrained beam search that only permits transitions forming valid sentence prefixes, with fallback extension or shortening guaranteeing grammatical output. Quantization uses a win/w/a triple with 8/4/4 on the raw-input image and spectrogram encoders and 4/4/4 on the video encoder and predictor head, recovered by quantization-aware training with only l2 decay. See [[wiki/04-architecture-and-decoding|Architecture Purpose-Designed for the BrainChip Akida]].

### Q6. What are the NAVIR corpus, the UrbanSound8K noise protocol, and the evaluation splits?
> [!tip]- Answer
> The internal NAVIR corpus holds 183 robot-manipulation commands from about 39 words in 5 categories, each with synonymous phrasings, spoken in full by 2 speakers for 366 recordings. Industrial noise comes only from the UrbanSound8K machinery subset (air conditioner, drilling, engine idling, jackhammer), mixed at SNRs of -15 to 0 dB in training and a fixed -10 dB at test, with the first fold held out. See [[wiki/05-datasets-and-experimental-setup|Datasets and Experimental Setup]].

### Q7. What do the GRID recognition results show about fusion under noise and quantization?
> [!tip]- Answer
> Clean-audio training collapses under noise (about 77–80% WER), while noisy-audio training plus video fusion cuts quantized noisy WER to 14.0% on the unseen-speaker split and 3.3% on the overlapped-speaker split, versus 22.5% and 11.8% audio-only. The AKD1000-constrained video-only model trails unconstrained SOTA on unseen speakers (35.3% vs 9.7–11.4%) but approaches it on overlapped speakers (6.7%), with QAT largely preserving accuracy. See [[wiki/06-grid-recognition-results|GRID Recognition Results: Visual Modality Anchors Recognition When Audio Degrades]].

### Q8. What does Table 8 report for quantized NAVIR results after QAT?
> [!tip]- Answer
> Clean-audio training scores 6.6% WER / 91.5% accuracy on clean audio but collapses to 98.7% / 0.0% under noise, and noisy-audio-only training stays weak at 43.1% / 47.9% noisy. Video-only holds 0.7% / 100% in both conditions, while noisy-audio-plus-video fusion holds 0.6% / 98.6% clean and 1.5% / 98.6% noisy, showing the visual stream anchoring recognition. See [[wiki/07-navir-results-and-energy-method|NAVIR results and energy method (Table 8, Section VII.A–VII.B)]].

### Q9. How is the theoretical 13.17x SNN-over-ANN energy gain derived?
> [!tip]- Answer
> ANN energy is estimated as MACs times 3.7 pJ per MAC and SNN energy as MACs times the 27.55% mean firing rate times 0.9 pJ per AC, using Horowitz 45 nm primitive costs, giving a gain of 3.7 / (0.9 x r-bar) = 13.17x. This yields 314.92 uJ per-sentence SNN inference against a 4.15 mJ ANN baseline, stated as roughly 62.8x below LipNet and 497x below Wu et al. as ANN comparison points. See [[wiki/07-navir-results-and-energy-method|NAVIR results and energy method (Table 8, Section VII.A–VII.B)]].

### Q10. What does Table 11 show for per-inference power of the video-only model across backends?
> [!tip]- Answer
> The AKD1000 reaches 14.55 inferences/s at 0.0165 mWh per inference, making it 4.9x more efficient than the same SNN on Pi CPU (0.0810 mWh), 26x better than the Pi float-Keras baseline (0.4306 mWh), and over 100x better than laptop GPU (1.6913 mWh). Adopted idle baselines are 390 mWh per 5 min for the Pi (total system draw) and 1,280 mWh for the GPU (GPU-only via nvidia-smi), with the video-only pipeline using 5 AKD1000 passes per inference. See [[wiki/08-power-measurements-and-pareto|Table 11: Video-only model per-inference power]].

### Q11. What does the closed-loop robot demonstration prove, and what novelty is claimed?
> [!tip]- Answer
> A uFactory xArm 6 arm connected directly to the Raspberry Pi closes the loop from voice command to physical action, with video and audio captured, processed through the neuromorphic pipeline, and recognised commands dispatched in real time on self-contained commodity embedded hardware plus the AKD1000. The authors claim it is the first end-to-end multimodal AVSR system demonstrated on neuromorphic hardware of this class, sustaining real-time throughput at roughly 5x less energy than the strongest CPU baseline. See [[wiki/09-robot-demonstration|Robot Demonstration and Closed-Loop Validation]].

### Q12. What fix is proposed for the audio-video mapping slowdown, and what does Appendix B specify?
> [!tip]- Answer
> A small threshold before quantization or fine-tuning under an added l1 penalty would reduce incoming connections per convolutional layer and equalise the 22-pass audio-video mapping with the 5-pass video-only mapping, a generic AKD1000-toolchain property. Appendix B specifies the AkidaNet image/spectrogram encoders (4 full plus 10 separable blocks, filters 32 to 1024 scaled by alpha), the temporal-video encoder stacking (T, 1, 128) embeddings with 3x3 convs and pooling to D dimensions, and the MLP predictor head emitting vocabulary logits including the CTC blank. See [[wiki/10-limitations-future-work-appendices|Limitations, Future Work and Appendices]].

### Q13. Which references ground the SNN training lineage and the speech corpora?
> [!tip]- Answer
> SNN training foundations are Wu et al. spatio-temporal backpropagation [3], SEW-ResNet and MS-ResNet residual learning [4][5], Spikformer and the spike-driven transformer [6][7], plus audio-visual SNN fusion works [9]–[11] and AKD1000 hardware studies [12]–[17]. Speech data rest on the GRID corpus [18], in-the-wild extensions LRW/LRS2/LRS3/TCD-TIMIT/AVSpeech/ASPIRE [19]–[24], and SNN-side benchmarks DVS-Lip-Audio, SHD/SSC, and Speech Commands [25]–[27]. See [[wiki/11-references-part-1|References Part 1: Energy, SNN, and Hardware References]].

### Q14. Which references cover the lip-reading baselines, noise sources, and measurement caveats?
> [!tip]- Answer
> Lip-reading baselines run LipNet [28] through WLAS, LCANet, LipSound, DualLip, HLR-Net, LCSNet, and Wu et al. [29]–[35], while the noise methodology rests on the UrbanSound8K dataset [36] and CochleaNet enhancement [37]. Power claims are caveated by the HIRE-SNN robustness study [38] and the nvidia-smi measurement critique [39], with Akida implementation details pinned to the archived BrainChip documentation [40]. See [[wiki/12-references-part-2|References Part 2 and Author Biographies]].

### Q15. For a battery-powered factory robot needing reliable voice commands in heavy machinery noise, which NAVIR configuration would you deploy and why?
> [!tip]- Answer
> I would deploy the noisy-audio-plus-video fusion model on the Pi plus AKD1000, since it holds 98.6% command accuracy at 1.5% WER under -10 dB noise while audio-only collapses to 0% accuracy, and the on-board demo proves real-time closed-loop xArm 6 control. I would accept the slower 22-pass audio-video mapping (2.61 inferences/s, still real-time for commands) over video-only, and apply the proposed threshold or l1 sparsity fine-tuning to recover the per-inference energy edge. See [[wiki/08-power-measurements-and-pareto|Table 11: Video-only model per-inference power]].
