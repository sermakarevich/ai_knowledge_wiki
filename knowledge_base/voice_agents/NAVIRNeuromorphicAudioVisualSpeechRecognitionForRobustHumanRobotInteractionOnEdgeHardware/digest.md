> [[index|Wiki]] | [[summary|Summary]]

# NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware — Digest

## 1. [[wiki/01-introduction-and-contributions|Introduction and Contributions]]

**In one sentence:** Industrial voice control fails under acoustic noise, so NAVIR builds an end-to-end audio-visual speech recognizer that fuses lip-motion with audio using only sequential 2D convolutions executable on the BrainChip Akida neuromorphic processor.

## Key points

- Audio-only ASR degrades sharply in industrial settings due to noise from machinery, ventilation, and ambient activity, forcing workers back to keypads, touchscreens, or physical switches that slow workflows and compromise hands-free safety.
- AVSR exploits the same redundancy as the human perceptual system (McGurk illusion [1]), integrating the visual appearance of the speaker's mouth to deliver robustness gains at low signal-to-noise ratios.
- State-of-the-art AVSR relies on 3D convolutions, recurrent units, attention/conformer encoders, and large transformer language models that assume GPU-class hardware and exceed typical edge-device budgets.
- NAVIR targets the BrainChip AKD1000 neuromorphic SoC, which natively supports only sequential 2D convolutional inference, factorizing encoding into a per-frame visual encoder, a temporal video encoder, and a spectrogram audio encoder fused by a lightweight predictor head with constrained beam-search decoding.
- Models are trained with connectionist temporal classification on noise-augmented audio, then fine-tuned with quantization-aware training.
- On GRID, the quantized audio-visual model reaches 14.0% WER under noise on the unseen-speaker split and 3.3% WER on the overlapped-speaker split, versus 22.5% and 11.8% for audio-only baselines; on the industrial-command corpus it attains 98.6% command accuracy at 1.5% WER.
- Operation-count analysis indicates a 13-fold energy advantage of the spiking formulation over its ANN counterpart at 27.6% mean firing rate; on-board measurements show ~5x lower energy per inference than a Raspberry Pi CPU on the lip-reading model and >100x lower than a laptop GPU, at 14.5 inferences per second.

## 2. [[wiki/02-neuromorphic-background|Neuromorphic Background: SNN Architectures and the AKD1000]]

**In one sentence:** SNNs replace energy-intensive MAC operations with sparse event-driven accumulate operations, and a lineage from surrogate-gradient training through residual and spike-driven transformers to prior AKD1000 deployments motivates NAVIR's strictly convolutional, spike-encoder- and firing-rate-driven design for the AKD1000.

## Key points

- SNNs use event-driven binary computation to replace dense multiply-accumulate (MAC) operations with sparse synaptic accumulate (AC) operations, cutting power consumption in principle.
- Wu et al.'s spatio-temporal backpropagation framework unrolled leaky integrate-and-fire dynamics across time and approximated the non-differentiable spike function with a smooth surrogate, making direct deep SNN training feasible.
- SEW-ResNet and MS-ResNet applied residual connections inside spiking networks, with membrane-shortcut designs guaranteeing strictly binary spike communication for efficient hardware deployment.
- Spikformer introduced spiking self-attention with binary query, key and value tensors, and the Spike-driven Transformer redesigned attention as a mask-and-add operation reducing all components to sparse addition.
- Prior audio-visual SNN work (S-CMRL cross-modal complementary attention with semantic-alignment loss, Tucker-fusion transformer coupling binary spike sequences with floating-point representations, DVS lip events as cross-modal attention cues) still grapples with keeping the full network spike-driven.
- The AKD1000 imposes a stricter regime supporting only sequential convolutional inference via the MetaTF/CNN2SNN toolchain, precluding recurrence and attention, so NAVIR builds on convolutional SNNs with spike encoder design and firing-rate control as the primary accuracy/energy levers.
- Prior AKD1000 results: Lunghi et al. report 0.63–1.38 mJ per frame at 0.66–1.41 ms latency for 4-bit-quantized CNNs on EuroSAT with a 911 mW idle floor; Chemnitz and Ermis report 99.5% lower energy and 76.7% lower latency vs an NVIDIA GTX 1080 on a GXNOR MNIST classifier; Lenz and McLelland cut total energy to less than a quarter via a two-stage AkidaNet/YOLOv5 pipeline.

## 3. [[wiki/03-related-work-akida-and-grid-sota|Related Work: AKD1000 Applications and GRID Lip-Reading State of the Art]]

**In one sentence:** Prior AKD1000 work shows strong energy advantages on lightweight sparse inference but is limited by single-node capacity, idle floor, and unsupported primitives, while GRID lip-reading SOTA (1.83–4.8% WER overlapped) relies on 3D convolutions, recurrence, or attention that AKD1000 does not support, leaving noisy-audio AVSR fusion on GRID an open gap.

## Key points

- Benoot et al. [15] integrate the AKD1000 (and forthcoming AKD1500) into a heterogeneous on-board satellite data-processing unit.
- Lutes et al. [16] exploit on-chip edge learning for individualised braking-intent EEG classification in the biomedical domain.
- Bråtman and Dow [17] characterise edge-learning hyperparameters for intracranial-pathology CT classification.
- Across these works, the AKD1000 consistently delivers strong energy advantages on lightweight, sparse inference, limited by single-node model capacity, the high idle floor, and constraints on architectural primitives.
- GRID [18] is the standard sentence-level lip-reading benchmark; LRW [19], LRS2 [20], LRS3 [21], TCD-TIMIT [22], AVSpeech [23], and ASPIRE [24] extend coverage to in-the-wild sentences and noisy conditions.
- On the SNN side, DVS-Lip-Audio [25] provides event-based audio-visual lip data, while SHD/SSC [26] and Speech Commands [27] provide audio-only benchmarks.
- GRID overlapped-speaker SOTA runs from LipNet 4.80% (2016) down to Wu et al. 1.83% (2024), with unseen-speaker results far worse (LipNet 11.40%, HLR-Net 9.70%, Wu et al. 10.21%).
- No published results exist for full AVSR fusion on GRID under noisy audio conditions, presenting both a literature gap and a comparison point for any neuromorphic approach.

## 4. [[wiki/04-architecture-and-decoding|Architecture Purpose-Designed for the BrainChip Akida]]

**In one sentence:** NAVIR factorises encoding into Akida-compatible per-frame spatial and temporal stages for video plus a parallel MFCC spectrogram encoder, fuses them through an MLP head, and decodes with grammar-constrained beam search under a hybrid 8/4/4 and 4/4/4 quantization scheme recovered by QAT.

## Key points

- Frames are processed individually rather than as a volumetric sequence because the AKD1000 does not support 3D convolutions, recurrent connections, or attention, so encoding is factorised into a spatial stage (per frame) and a temporal stage (across frames).
- Per-frame embeddings are stacked along the time axis into a 2D time × embedding-features representation, and a second Akida-compatible network applies temporal convolutions across the stack to yield a single video-clip embedding capturing motion and short-range dynamics.
- Audio is converted in parallel into Mel-frequency cepstral coefficients (MFCCs) and processed by a third AkidaNet-based encoder to yield an audio-clip embedding.
- Video-clip and audio-clip embeddings are concatenated into a joint audio-visual representation fed to a lightweight MLP predictor head outputting vocabulary logits, with per-token probabilities via softmax.
- At inference the head produces a T × V token-score matrix (clip windows × vocabulary) decoded by constrained beam search that restricts every per-frame transition to tokens forming a valid prefix of some legal sentence.
- Beam search maintains top-B hypotheses as partial token prefixes with accumulated scores, considering blank/silence emission, last-token repeat, or advance to a new legal-next token, with fallback extension or shortening guaranteeing a grammatically valid output.
- Training uses CTC loss marginalising over alignments via a blank label; WER is the primary metric plus sentence-level command accuracy on the industrial-command corpus.
- Quantization uses a win/w/a triple (first-layer weight bits / later-layer weight bits / activation bits): 8/4/4 for the image and spectrogram encoders on raw inputs, 4/4/4 for the video encoder and predictor head on intermediate embeddings, followed by quantization-aware training with only ℓ2 weight decay.

## 5. [[wiki/05-datasets-and-experimental-setup|Datasets and Experimental Setup]]

**In one sentence:** NAVIR is an internal 183-command / 366-recording audio-visual robot-command corpus augmented with industrial machinery noise from UrbanSound8K, evaluated alongside GRID under unseen- and overlapped-speaker protocols with flip/jitter augmentation and modality-specific QAT schedules.

## Key points

- NAVIR is a custom, internal (not publicly released) audio-visual dataset of robot-manipulation commands used to fine-tune and evaluate the deployed system.
- NAVIR contains 183 distinct commands from ~39 words in 5 categories, each with synonymous phrasings, produced in full by 2 speakers for 366 recordings total.
- UrbanSound8K (8,732 excerpts, ≤4 s, 10 classes, 10 folds) is used solely as a noise source; only the mechanical/machinery subset (air conditioner, drilling, engine idling, jackhammer) is mixed into GRID and NAVIR.
- Noise mixing uses SNRs sampled from {−15, −10, −5, 0} dB during training and a fixed −10 dB SNR for the noisy-audio test condition; the first predefined fold is held out for evaluation.
- GRID is reported under both the LipNet unseen-speaker protocol and an overlapped-speaker protocol, while NAVIR uses an 80/20 sentence-level split holding out random commands across both speakers (only 2 speakers, so it tests unseen sentences, not unseen speakers).
- Both runs apply horizontal-flip augmentation (p = 0.5) and temporal jitter (p = 0.05); after float training, hybrid quantization plus QAT fine-tuning runs 15 epochs (GRID unseen-speaker), 100 epochs (GRID overlapped), 200 epochs (NAVIR).
- Under the GRID unseen-speaker split, clean-trained audio models collapse to ~77–80% WER in noise, noisy-audio training brings this to 21.0% float / 22.5% quantized, and noisy-audio + video fusion reduces it further to 16.6% float / 14.0% quantized.

## 6. [[wiki/06-grid-recognition-results|GRID Recognition Results: Visual Modality Anchors Recognition When Audio Degrades]]

**In one sentence:** On GRID and NAVIR, fusing video with audio sharply lowers WER under noise — with quantization largely preserved and occasional small QAT gains — while clean-audio-only models collapse under noise and the AKD1000-constrained video-only model trails unconstrained SOTA on GRID unseen speakers but approaches baselines on overlapped speakers and saturates near 0% WER on NAVIR.

## Key points

- In the fused noisy condition the quantized model is marginally better than its float counterpart, but the effect is small and not consistent across all configurations.
- The GRID video-only model reaches 34.0% (float) and 35.3% (quantized) WER on the unseen-speaker split, versus a 9.7–11.4% SOTA range whose baselines use 3D convolutions, attention-augmented decoders, and large-scale pre-training that are not AKD1000-compatible.
- On the GRID overlapped-speaker split, video-only reaches 9.1% (float) and 6.7% (quantized) WER, approaching the 1.83–4.8% unconstrained ANN baseline range, with QAT improving video-only by 2.4 absolute points over float.
- Under GRID overlapped-speaker noise, noisy-audio + video fusion reaches 2.8% (float) and 3.3% (quantized) WER versus 10.4%/11.8% for noisy audio alone and 9.1%/6.7% for video alone; under clean audio fusion reaches 0.7%/0.8%, below both single-modality baselines.
- Training on clean audio alone collapses under noise: 77.1–79.8% WER across the four clean-audio-trained configurations on GRID overlapped split (and 97.5% float / 98.7% quantized on NAVIR), whereas training on noisy audio reduces noisy-test WER substantially.
- On NAVIR, video-only retains 0.5% to 0.7% WER with 100% command accuracy preserved through quantization, and noisy-audio + video fusion degrades only from 0.3% to 0.6% WER clean and 0.9% to 1.5% noisy; the 200-epoch QAT schedule is described as well matched to the small corpus size.
- The Pareto analysis in Section VII-C uses both the overlapped- and unseen-speaker video-only stats for cross-method comparison.

## 7. [[wiki/07-navir-results-and-energy-method|NAVIR results and energy method (Table 8, Section VII.A–VII.B)]]

**In one sentence:** After quantization-aware training, NAVIR's accuracy collapses on audio-only training but the video-anchored noisy-audio+video model holds 1.5% WER / 98.6% command accuracy under noisy audio, and the operation-count energy model (Horowitz 45 nm constants, 27.55% firing rate) gives a 13.17× SNN-over-ANN gain at 314.92 µJ per sentence.

## Key points

- Table 8 reports quantized (post-QAT) NAVIR results as WER (%) / command accuracy (%): clean-audio training gives 6.6 / 91.5 on clean audio but 98.7 / 0.0 on noisy audio.
- Noisy-audio training alone is weak: 12.1 / 77.5 on clean audio and 43.1 / 47.9 on noisy audio.
- Video-only training holds 0.7 / 100.0 on both clean and noisy audio test conditions.
- Noisy audio + video training holds 0.6 / 98.6 on clean audio and 1.5 / 98.6 on noisy audio, showing the visual modality anchoring recognition.
- Clean audio + video training gives 4.3 / 93.0 on clean audio but collapses to 95.7 / 4.2 on noisy audio.
- Energy methodology: E_ANN = MACs × E_MAC with E_MAC ≈ 3.7 pJ, and E_SNN = MACs × r̄ × E_AC with E_AC ≈ 0.9 pJ, using Horowitz 45 nm primitive costs; Horowitz reports only primitive-cost numbers, not a model-level methodology.
- Measured average firing rate r̄ is 27.55% (72.45% sparsity) across spiking layers on GRID, yielding a theoretical 13.17× ANN/SNN gain, 314.92 µJ per-sentence SNN inference versus a 4.15 mJ ANN baseline for the video-only model.

## 8. [[wiki/08-power-measurements-and-pareto|Table 11: Video-only model per-inference power]]

**In one sentence:** On the video-only model the AKD1000 reaches 14.55 it/s at 0.0165 mWh per inference, making it 4.9× more efficient than the same SNN on Pi CPU, 26× better than the Pi float-Keras baseline, and over 100× better than laptop GPU.

## Key points

- Video-only Akida backend: 14.55 it/s at 462.0 mWh per 5 min, i.e. 72.0 mWh attributable draw and 0.0165 mWh per inference.
- Same SNN on Pi CPU under the Akida backend (strongest CPU baseline): 15.55 it/s at 0.0810 mWh per inference, so the AKD1000 is 4.9× more energy-efficient per inference.
- Pi CPU Keras float baseline: 1.10 it/s at 0.4306 mWh per inference, a 26× gap versus the AKD1000.
- Laptop GPU Keras baseline: 2.54 it/s at 1.6913 mWh per inference, more than a 100× gap versus the AKD1000.
- Idle baselines adopted are 390 mWh / 5 min for the Pi and 1,280 mWh / 5 min for the GPU; Pi figures are total system draw (FNB58) while GPU figures are GPU-only draw via nvidia-smi normalised to a 5-minute window.
- The video-only pipeline uses 5 AKD1000 passes per inference: image encoder (75 NPs, 1 sequence), temporal encoder (41 NPs, 3 sequences), predictor head (2 NPs, 1 sequence).
- The audio-video extension (Table 12 preview) totals 22 passes per inference and raises Akida energy to 0.0894 mWh per inference at 2.61 it/s, still 37× less than laptop GPU but broadly comparable to the Pi-CPU Akida backend (0.0866 mWh/inf. at 13.36 it/s).

## 9. [[wiki/09-robot-demonstration|Robot Demonstration and Closed-Loop Validation]]

**In one sentence:** A self-contained edge system couples the neuromorphic AVSR pipeline on Raspberry Pi + AKD1000 to a uFactory xArm 6 arm, dispatching recognised voice commands to physical action in real time with ~5× lower energy per inference than the strongest CPU baseline and >100× lower than a laptop GPU.

## Key points

- A uFactory xArm 6 robotic arm is connected directly to the Pi, closing the loop from voice command to physical action.
- Video and audio are captured, processed through the neuromorphic pipeline, and recognised commands are dispatched to the arm in real time.
- The complete system is self-contained, edge-deployable, and runs entirely on commodity embedded hardware augmented by the AKD1000.
- The chunk contains the fragment "command accuracy and 1.5% WER" and separately states a task-specific industrial-command corpus "reaches 98.6%".
- On the deployment platform the system sustains real-time throughput at approximately 5× less energy per inference than the strongest CPU baseline, identified as the SNN-converted model running on the Akida software backend.
- The same deployment point uses over 100× less energy per inference than a laptop GPU on the video-only model.
- The authors state this is, to the best of their knowledge, the first end-to-end multimodal AVSR system demonstrated on neuromorphic hardware of this class.
- The remaining gap to unconstrained SOTA accuracy is attributed to the chip's deliberate architectural simplicity, with sparsity-aware fine-tuning named as the concrete path to close the video-only vs audio-video deployment gap.

## 10. [[wiki/10-limitations-future-work-appendices|Limitations, Future Work and Appendices]]

**In one sentence:** A small threshold before quantization or ℓ1-penalised fine-tuning is proposed to equalise audio-video and video-only hardware mappings (a generic AKD1000-toolchain property), and Appendix B specifies the AkidaNet image/spectrogram encoders, the NAVIR-specific temporal-video encoder, and the predictor head with exact layers, dimensions, and quantization.

## Key points

- Either a small threshold before quantization or fine-tuning under an additional ℓ1 penalty would directly reduce `incoming_conn` for every convolutional layer and is expected to equalise the audio-video and video-only mappings without further architecture changes.
- The mapping behaviour is described as a generic property of the AKD1000 toolchain, relevant to any work deploying multiple checkpoints of the same architecture on this hardware.
- Image and spectrogram encoders reuse the standard AkidaNet ImageNet model (`akida_models.akidanet_imagenet`, one-channel input) with the dropout + 1000-way dense head removed and replaced by a single dense projection with ReLU bounded at 6.0.
- The AkidaNet backbone has four full convolution blocks (conv_0–conv_3, strided at conv_0 and conv_2) plus ten separable blocks (separable_4–separable_13, strided at 4, 6, 12), with filters doubling from 32 to 1024 scaled by width multiplier α (0.50 on GRID, 0.25 on NAVIR for both encoders).
- The temporal-video encoder stacks per-frame embeddings into a (T, 1, F=128) tensor so the AKD1000 2D convolution acts as an effective 1D temporal convolution, using 3×3 conv blocks with ⌊64α⌋ / ⌊96α⌋ / ⌊128α⌋ filters, global average pooling, dropout 0.03, and a dense projection to D (256 on GRID, 128 on NAVIR).
- On NAVIR the temporal conv blocks are conv → batch normalisation → ReLU while on GRID batch normalisation is omitted (conv → ReLU), with α = 0.5 on NAVIR and 1.0 on GRID, padding `same`, stride 1, and the same ℓ2 weight decay as AkidaNet.
- The predictor head consumes the concatenated fused embedding (768-dim = 256 + 512 on GRID with two hidden layers of 512 and 256 units; 640-dim = 128 + 512 on NAVIR with one hidden layer of 256 units), all hidden activations ReLU bounded at 6.0, outputting V raw logits (including CTC blank) for CTC loss and constrained beam-search decoding, quantized to 4-bit weights/activations and fine-tuned jointly in QAT.

## 11. [[wiki/11-references-part-1|References Part 1: Energy, SNN, and Hardware References]]

**In one sentence:** This page catalogs bibliography entries [2]–[30] cited by the NAVIR paper, spanning computing-energy motivation, SNN training and architectures, neuromorphic hardware studies, and audio-visual speech datasets.

## Key points

- [2] M. Horowitz, "1.1 Computing's energy problem (and what we can do about it)," 2014 IEEE ISSCC Digest of Technical Papers, pp. 10–14, 2014.
- [3]–[5] cover SNN training foundations: spatio-temporal backpropagation (Wu et al., Front. Neurosci., vol. 12, 2017), deep residual learning in SNNs (Fang et al., NeurIPS 2021), and advancing SNNs toward deep residual learning (Hu et al., IEEE TNNLS, vol. 36, pp. 2353–2367, 2021).
- [6]–[8] cover SNN transformer and forecasting variants: Spikformer (Zhou et al., ICLR 2023), spike-driven transformer (Yao et al., NeurIPS 2023), and time-series forecasting with SNNs (Lv et al., ICML 2024).
- [9]–[11] cover audio-visual SNN fusion work: semantic-alignment and cross-modal residual learning (He et al., 2025, arXiv:2502.12488), spiking Tucker fusion transformer (Li et al., IEEE TIP, vol. 33, pp. 4840–4852, 2024), and human-inspired AVSR computing (Liu et al., IEEE Trans. Computers, vol. 74, pp. 2950–2961, 2025).
- [12]–[17] cover neuromorphic energy/hardware evidence: SNN energy-efficiency for space (Lunghi et al., Astrodynamics, vol. 9, pp. 909–932, 2025), Akida vs. NVIDIA GPU comparison (Chemnitz and Ermis, 2025), low-power ship detection (Lenz and McLelland, 2024, arXiv:2406.11319), onboard processing with COTS SoCs and neuromorphic co-processors (Benoot et al., SPAICE2024, pp. 416–419), braking-intent few-shot transfer (Lutes et al., J. Neural Eng., vol. 22, 2024), and Akida on-edge medical imaging training (Bråtman and Dow, 2023).
- [18]–[24] cover audio-visual speech corpora: GRID audio-visual corpus (Cooke et al., JASA, vol. 120, pp. 2421–2424, 2006, PMID: 17139705), Lip Reading in the Wild (Chung and Zisserman, ACCV 2016), deep AVSR (Afouras et al., IEEE TPAMI, vol. 44, pp. 8717–8727, 2018), LRS3-TED (Afouras et al., 2018, arXiv:1809.00496), TCD-TIMIT (Harte and Gillen, IEEE Trans. Multimedia, vol. 17, pp. 603–615, 2015), looking-to-listen cocktail party (Ephrat et al., ACM TOG, vol. 37, pp. 1–11, 2018), and ASPIRE noisy AV enhancement corpus (Gogate et al., 2020).
- [25]–[30] as visible in the chunk cover event-based lip-reading (Tan et al., CVPR 2022, pp. 20062–20071), Heidelberg spiking datasets (Cramer et al., IEEE TNNLS, vol. 33, pp. 2744–2757, 2019), Speech Commands dataset (Warden, 2018, arXiv:1804.03209), LipNet sentence-level lipreading (Assael et al., 2016, arXiv:1611.01599), lip reading sentences in the wild (Chung et al., CVPR 2017, pp. 3444–3453), and LCANet cascaded attention-CTC lipreading (Xu et al., FG 2018, pp. 548–555).

## 12. [[wiki/12-references-part-2|References Part 2 and Author Biographies]]

**In one sentence:** This closing chunk contains bibliography entries [31]–[40] on lip reading, audio-visual enhancement, SNN robustness, and power measurement plus Akida documentation, followed by author biographies and the paper's closing page footers.

## Key points

- Ref [31] is L. Qu, C. Weber, and S. Wermter, "LipSound: Neural Mel-Spectrogram Reconstruction for Lip Reading," in Interspeech, 2019.
- Ref [32] is W. Chen et al., "DualLip: A System for Joint Lip Reading and Generation," Proceedings of the 28th ACM International Conference on Multimedia, 2020.
- Refs [33]–[35] cover hybrid and end-to-end lip-reading models: HLR-Net (Computers, Materials & Continua, 2021), LCSNet (ACM TOMM vol. 19, pp. 1–21, 2022), and landmark-guided cross-speaker lip reading (LREC-COLING 2024, pp. 10023–10033).
- Refs [36]–[37] cover audio datasets and enhancement: Salamon et al. urban-sound dataset/taxonomy (ACM Multimedia 2014, pp. 1041–1044) and CochleaNet audio-visual speech enhancement (Information Fusion, vol. 63, pp. 273–285, Nov. 1, 2020).
- Refs [38]–[39] cover SNN robustness and power measurement: HIRE-SNN (IEEE/CVF ICCV 2021, pp. 5189–5198) and Nvidia-smi power-measurement critique (SC24, Nov. 2024, pp. 1–17).
- Ref [40] is "Overview — akida examples documentation," archived at the web.archive.org URL for doc.brainchipinc.com, accessed May 22, 2026.
- The chunk closes with biographies for Delimpasis, Karamousadakis, Moraiti, Porichis, and Chatzakos, plus the running footers "12" / "13" and "L. Delimpasis et al: NAVIR: Neuromorphic AVSR for Robust Human–Robot Interaction on Edge Hardware".

## The argument in five moves

1. Industrial voice control fails because acoustic noise collapses audio-only ASR, while SOTA AVSR fixes robustness with 3D, recurrent, and attention machinery that edge hardware cannot afford.
2. NAVIR therefore constrains the whole design to what the BrainChip AKD1000 supports — factorised per-frame spatial plus temporal 2D convolutions for video, a parallel MFCC spectrogram encoder, MLP fusion, and grammar-constrained beam search trained with CTC and hybrid quantization plus QAT.
3. Evaluated on GRID with UrbanSound8K machinery noise and on the internal 183-command NAVIR robot corpus, clean-audio training collapses under noise while noisy-audio plus video fusion anchors recognition (GRID 14.0% unseen / 3.3% overlapped quantized noisy WER; NAVIR 1.5% WER / 98.6% accuracy).
4. The same constrained model converts sparsity into energy savings — 27.55% firing rate giving 13.17× theoretical SNN-over-ANN gain at 314.92 µJ per sentence, and on-board 14.55 it/s at 4.9× better than Pi-CPU SNN, 26× better than Pi float, and >100× better than laptop GPU.
5. A Pi + AKD1000 + xArm 6 closed-loop demo proves self-contained real-time edge deployment as the first end-to-end multimodal AVSR on this neuromorphic class, with the residual SOTA gap and slower 22-pass audio-video mapping attributed to deliberate chip simplicity and left to sparsity-aware (threshold/ℓ1) fine-tuning.
