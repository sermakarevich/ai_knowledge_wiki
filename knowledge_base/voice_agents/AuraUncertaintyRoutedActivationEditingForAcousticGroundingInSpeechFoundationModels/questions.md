---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models

### Q1. What acoustic-grounding failure in AED speech foundation models motivates AURA?

> [!tip]- Answer
> Attention encoder-decoder speech foundation models achieve strong ASR yet can generate acoustically unsupported text when inputs contain no speech or only weak acoustic evidence. AURA targets the specific internal computations that control whether the decoder stays grounded in the audio. See [[wiki/01-aura-overview|AURA: Uncertainty-Routed Activation Editing for Acoustic]].

### Q2. How does AURA's head-level scale-and-shift editing backbone work, and what happens when both gates are zero?

> [!tip]- Answer
> AURA freezes all pretrained weights and learns a per-head scale vector Ah and bias vector vh on decoder cross-attention outputs, with effective gates selecting additive, multiplicative, joint, or no-op interventions. When both gates are zero the edited output recovers the frozen output exactly. Static head selection uses Hard-Concrete gates with stretch interval (−0.1, 1.1), initialized from N(0, 0.012) and sparsified by an expected-L0 penalty. See [[wiki/02-methodology-uncertainty-routed-editing|Methodology: Uncertainty-Routed Activation Editing]].

### Q3. What three cross-attention uncertainty features drive AURA's dynamic gate, and how do static and dynamic gates combine?

> [!tip]- Answer
> The per-head, per-step dynamic gate is computed from Max-Prob (over-concentration), normalized Entropy (diffuse attention), and Shift (abrupt frame jumps), projected through a zero-initialized 4-scalar projection. The effective gate is the product of the static gate (where an edit may occur) and the dynamic gate (when it should activate). Hence AURA stays mostly dormant during confident recognition and strengthens during unstable grounding. See [[wiki/02-methodology-uncertainty-routed-editing|Methodology: Uncertainty-Routed Activation Editing]].

### Q4. What is the shared training protocol, and what distinguishes AURA from AURA+Enc?

> [!tip]- Answer
> All models train with AdamW, linear decay, 10% warmup, batch size 16, up to 10k steps, PEFT learning rates swept over {1e-4, 3e-4, 5e-4}, full fine-tuning at 1e-5, greedy decoding, Whisper text normalization, and SCTK MAPSSWE testing at p < 0.05. AURA edits only decoder cross-attention heads with ~500x fewer parameters than LoRA (r=128, α=256), while AURA+Enc additionally fine-tunes all encoder parameters purely as a higher-capacity diagnostic, not an ultra-efficient PEFT method. See [[wiki/03-experimental-setup-and-baselines|Experimental Setup and Baselines]].

### Q5. What happens to hallucination rate and clean-speech WER when AURA adapts Whisper-Large-v3 on non-speech audio, and how does JoLA compare?

> [!tip]- Answer
> Zero-shot Whisper-Large-v3 hallucinates on nearly all UrbanSound8K inputs (89.18% HRnorm, 98.00% HRraw); AURA cuts HRnorm to 4.39% after 5 epochs and 0.93% after 25 epochs with no speech replay and no prior head identification. At 15 epochs AURA and JoLA reach similar HRnorm (1.94% vs 2.01%), but AURA better preserves LibriSpeech WER (2.29/3.65 vs 4.11/4.36), isolating the benefit of token-level uncertainty routing over static head editing. See [[wiki/03-experimental-setup-and-baselines|Experimental Setup and Baselines]].

### Q6. How does AURA perform on the MyST, TED-LIUM 3, and FluencyBank grounding stressors, and what does AURA+Enc reveal?

> [!tip]- Answer
> On MyST AURA is the strongest representation-editing method, beating full fine-tuning at Medium/Large-v3 (13.7%/14.2%) with significant gains; on TED-LIUM 3 it ties or leads ultra-efficient methods but with modest, non-significant differences. On FluencyBank AURA leads representation editing through Whisper-medium yet LoRA and full fine-tuning beat decoder-only AURA at every size. AURA+Enc consistently improves on MyST and FluencyBank, showing child and disfluent speech benefit from encoder adaptation when frozen acoustics are inadequate. See [[wiki/03-experimental-setup-and-baselines|Experimental Setup and Baselines]].

### Q7. What do the JoLA comparison, Table VII sensitivity analysis, and Figure 2 alignment plots jointly show?

> [!tip]- Answer
> AURA beats statically-gated JoLA in 13 of 15 dataset–model comparisons (tying in two), with its largest gains where the backbone has capacity for decoder-side correction. Table VII is a decode-time sensitivity check, not a training ablation: removing any routing feature degrades WER, with entropy dominant (+1.7 WER at Large-v3). Figure 2 is illustrative rather than corpus-level, showing AURA turning collapsed heads into cleaner monotonic alignments on three MyST utterances. See [[wiki/04-results-and-analysis|Results and Analysis: Operating Point, Gating Sensitivity, and Alignment]].

### Q8. For a new deployment with mostly clean adult speech plus some child and disfluent traffic, should you ship decoder-only AURA or add encoder capacity?

> [!tip]- Answer
> Ship decoder-only AURA as the default, since it suppresses non-speech hallucination and tracks LoRA on adult speech with roughly 500x fewer parameters and minimal clean-speech degradation. Add encoder capacity (AURA+Enc or LoRA/full fine-tuning) only for the child and disfluent slices, where decoder-only edits hit their capacity boundary and encoder adaptation yields significant gains. Monitor frozen-acoustic adequacy per slice rather than applying heavy adaptation everywhere. See [[wiki/04-results-and-analysis|Results and Analysis: Operating Point, Gating Sensitivity, and Alignment]].
