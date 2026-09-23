> [[index|Wiki]] | [[summary|Summary]]
# AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models — Digest
## 1. [[wiki/01-aura-overview|AURA: Uncertainty-Routed Activation Editing for Acoustic]]

**In one sentence:** The provided chunk is truncated mid-abstract and only establishes that AED speech foundation models hallucinate acoustically unsupported text under weak or missing speech, without reaching the AURA proposal details.

- The paper is titled "AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models".
- The authors are Natarajan Balaji Shankar, Zilai Wang, Zihan Wang, Mohan Shi, Kaiyuan Zhang, and Abeer Alwan, Department of Electrical and Computer Engineering, University of California Los Angeles.
- The chunk's central claim is that attention encoder-decoder (AED) speech foundation models achieve strong ASR performance but can generate acoustically unsupported text.
- Two stated failure conditions are inputs containing no speech and inputs with weak acoustic evidence; the sentence is cut off before any further conditions.
- A surviving fragment states the work concerns "specific internal computations that control whether the decoder remains grounded in the audio."
- A second surviving fragment states "This aligns with interpretability studies," but the referent and continuation are missing due to truncation.
- No AURA method, numbers, results, or operating-point claims are present in this chunk, so they are not covered here.

## 2. [[wiki/02-methodology-uncertainty-routed-editing|Methodology: Uncertainty-Routed Activation Editing]]

**In one sentence:** AURA freezes the pretrained AED speech model and applies sparse scale-and-shift edits to decoder cross-attention heads, with static Hard-Concrete gates selecting where to edit and a dynamic token-level gate routing edits by cross-attention uncertainty features.

- AURA targets decoder cross-attention heads where acoustic conditioning occurs, freezing all pretrained weights and learning only edits, to correct localized grounding failures without broad weight rewrites.
- Each head learns a scale vector `Ah` and bias vector `vh` with effective gates controlling additive/multiplicative/joint/no-op interventions, recovering the frozen output exactly when both gates are zero.
- Static Hard-Concrete gates with location parameter `log α` and stretch interval `(γ, ζ) = (−0.1, 1.1)` provide sparse head selection, initialized from `N(0, 0.012)` and driven to sparsity by an expected-L0 penalty.
- A dynamic per-head gate computed from three causal cross-attention features — Max-Prob (over-concentration), normalized Entropy (diffuse attention), and Shift (abrupt frame jumps) — modulates edits at every decoding step via a 4-scalar projection.
- The effective gate is the product of static and dynamic gates, separating where an edit may occur from when it should activate, so AURA stays mostly dormant during confident recognition and strengthens during unstable grounding.
- AURA is trained with standard ASR cross-entropy plus a ramped sparsity loss, adding only `2d + 6` scalars per decoder cross-attention head, keeping it in the ultra-efficient PEFT regime at roughly 500× fewer trainable parameters than LoRA.
- On non-speech audio AURA reduces hallucination rate from 89.18% to 1.94% without prior hallucination-head identification, and on imperfect-label corpora it approaches LoRA WER.

## 3. [[wiki/03-experimental-setup-and-baselines|Experimental Setup and Baselines]]

**In one sentence:** All models share an AdamW protocol with linear decay, 10% warmup, batch size 16 and up to 10k steps with swept PEFT learning rates and ramped Hard-Concrete sparsity, evaluated with greedy decoding and SCTK significance testing, where AURA's decoder cross-attention edits match or approach higher-capacity baselines with roughly 500× fewer parameters than LoRA while encoder-unfreezing diagnostics reveal capacity boundaries on child and disfluent speech.

- All models are trained with AdamW, linear learning-rate decay, 10% warmup, batch size 16, and up to 10k steps; PEFT learning rates are swept over {1 × 10−4, 3 × 10−4, 5 × 10−4} with checkpoint selection on development-set performance, while full fine-tuning uses 1 × 10−5.
- LoRA uses r = 128 and α = 256 as a high-capacity baseline, and the reported ~500× parameter reduction refers to this setting; with the same placement, ranks 8/16/32 would still use approximately 31/61/122× AURA's trainable parameters.
- For JoLA and AURA, Hard-Concrete gates use temperature τ = 0.33 and stretch interval (−0.1, 1.1), with sparsity weight λt linearly ramped from 0.0 to 0.1 over the first 10% of training; LoReFT is swept over prefix/suffix positions p2+s2 and p7+s7.
- AURA edits decoder cross-attention heads and learns sparse head selection plus token-level uncertainty routing without a prior head-identification stage, while AURA+Enc additionally fine-tunes all encoder parameters only as a higher-capacity diagnostic, not as an ultra-efficient PEFT method.
- All experiments use Hugging Face Transformers with greedy decoding (30 s chunking for non-speech), Whisper English text normalization for WER, NIST SCTK MAPSSWE significance testing (p < 0.05), and a single NVIDIA RTX A6000 GPU.
- Non-speech adaptation uses only AudioSet, DEMAND, and MUSAN clips with empty transcripts and no speech replay, evaluating hallucination rate on UrbanSound8K and WER on LibriSpeech test-clean/test-other; zero-shot Whisper-Large-v3 has 89.18% HRnorm and 98.00% HRraw, while AURA reaches 4.39% HRnorm after 5 epochs and 0.93% after 25 epochs.
- On speech grounding stressors AURA is the strongest representation-editing method on MyST and TED-LIUM 3 ultra-efficient comparisons and reaches statistically significant gains on MyST (e.g. Medium 13.7%, Large-v3 14.2%) and FluencyBank Small/Medium, but LoRA and full fine-tuning outperform decoder-only AURA at every FluencyBank model size.

## 4. [[wiki/04-results-and-analysis|Results and Analysis: Operating Point, Gating Sensitivity, and Alignment]]

**In one sentence:** AURA's decoder-only uncertainty-routed edits beat statically-gated JoLA in 13 of 15 comparisons with entropy as the dominant routing signal, and qualitative alignment plus the conclusion frame decoder editing as sufficient when frozen acoustics are adequate but needing encoder capacity for child and disfluent speech.

- AURA beats JoLA (same head-level scale-and-shift backbone with only static gates) with lower WER in 13 of 15 dataset–model comparisons and ties in two at reported precision (Tables III–V).
- AURA's largest gains over JoLA appear when the backbone has sufficient representational capacity for decoder-side corrections.
- Table VII decode-time routing-feature analysis is not a feature-necessity ablation since models were trained with all features present; it tests whether the trained router remains sensitive to each feature at inference.
- Removing any routing feature at decode time degrades WER, with entropy dominant: largest degradation of +1.7 WER at Whisper-Large-v3.
- Figure 2 visualizes decoder cross-attention on three MyST test utterances at the same layer-head positions for full fine-tuning vs AURA; it is illustrative of behavior type, not a corpus-level alignment metric.
- AURA uses sparse scale-and-shift edits to decoder cross-attention heads with 500× fewer trainable parameters than LoRA, freezing the pretrained model.
- Stated operating point: ultra-efficient decoder editing is most effective when the frozen acoustic representation is adequate, while child and disfluent speech may benefit from substantially higher-capacity encoder updates (AURA+Enc).

## The argument in five moves

1. AED speech foundation models hallucinate acoustically unsupported text under weak or missing speech, motivating interventions on the internal computations that keep the decoder grounded in the audio.
2. AURA freezes the pretrained model and learns sparse head-level scale-and-shift edits on decoder cross-attention heads, with static Hard-Concrete gates selecting where to edit and a dynamic gate routing edits token-by-token from cross-attention uncertainty (Max-Prob, Entropy, Shift).
3. Under a shared AdamW/greedy-decoding/SCTK protocol, AURA trains only thousands of parameters — roughly 500x fewer than LoRA (r=128) — and needs no prior hallucination-head identification, unlike head-targeted CALM-style baselines.
4. On non-speech audio AURA collapses hallucination rate (89.18% to ~1-4% HRnorm) while preserving LibriSpeech WER, and on imperfect-label/disfluent speech (MyST, TED-LIUM 3, FluencyBank) it beats statically-gated JoLA in 13 of 15 comparisons with entropy as the dominant routing signal.
5. Decoder-only editing reaches its capacity boundary on child and disfluent speech, where the AURA+Enc diagnostic shows encoder adaptation still helps — fixing the operating point: use ultra-efficient uncertainty-routed decoder edits when frozen acoustics suffice, add encoder capacity when they do not.
