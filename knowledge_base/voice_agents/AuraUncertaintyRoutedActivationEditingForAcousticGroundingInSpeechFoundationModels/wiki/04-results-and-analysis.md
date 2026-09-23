> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Results and Analysis: Operating Point, Gating Sensitivity, and Alignment

**In one sentence:** AURA's decoder-only uncertainty-routed edits beat statically-gated JoLA in 13 of 15 comparisons with entropy as the dominant routing signal, and qualitative alignment plus the conclusion frame decoder editing as sufficient when frozen acoustics are adequate but needing encoder capacity for child and disfluent speech.

## Key points

- AURA beats JoLA (same head-level scale-and-shift backbone with only static gates) with lower WER in 13 of 15 dataset–model comparisons and ties in two at reported precision (Tables III–V).
- AURA's largest gains over JoLA appear when the backbone has sufficient representational capacity for decoder-side corrections.
- Table VII decode-time routing-feature analysis is not a feature-necessity ablation since models were trained with all features present; it tests whether the trained router remains sensitive to each feature at inference.
- Removing any routing feature at decode time degrades WER, with entropy dominant: largest degradation of +1.7 WER at Whisper-Large-v3.
- Figure 2 visualizes decoder cross-attention on three MyST test utterances at the same layer-head positions for full fine-tuning vs AURA; it is illustrative of behavior type, not a corpus-level alignment metric.
- AURA uses sparse scale-and-shift edits to decoder cross-attention heads with 500× fewer trainable parameters than LoRA, freezing the pretrained model.
- Stated operating point: ultra-efficient decoder editing is most effective when the frozen acoustic representation is adequate, while child and disfluent speech may benefit from substantially higher-capacity encoder updates (AURA+Enc).

---

## Operating point

**Covers:** Results and analysis: hallucination reduction, grounding-stressor adaptation, ablations, and operating point (chunk 04/4, §§ D–E, Conclusion, Acknowledgements, disclosures, references tail).

> "Together, these results sharpen AURA's intended operating point: ultra-efficient decoder editing is most effective when the frozen acoustic representation is adequate, while child and disfluent speech may benefit from substantially higher-capacity encoder updates."

## D. Sensitivity of uncertainty-routed gating

Comparing AURA with JoLA gives the closest test of uncertainty-routed dynamic gating, since JoLA uses the same head-level scale-and-shift backbone with only static gates. Under this matched setup:

- AURA achieves lower WER than JoLA in 13 of 15 dataset–model comparisons and ties in two at the reported precision (Tables III–V).
- AURA's largest gains appear when the backbone has sufficient representational capacity for decoder-side corrections, consistent with the AURA+Enc finding that child speech and disfluent speech can benefit from additional encoder capacity when decoder-only edits are insufficient.

Table VII provides a decode-time sensitivity analysis of the three routing features:

- Because the models are trained with all features present, this experiment should not be interpreted as a feature-necessity ablation; it asks whether the trained router remains sensitive to each feature at inference.
- Removing any feature degrades WER in this experiment, but the effect is not uniform: entropy is the dominant signal, with the largest degradation of +1.7 WER at Whisper-Large-v3.
- The chunk interprets this as larger models exposing more informative cross-attention uncertainty patterns, making uncertainty-routed activation editing especially effective at larger scales.
- Interpretation stated in chunk: the learned gate uses all uncertainty features, with entropy contributing most strongly, rather than proof that all features are equally necessary during training.

## E. Cross-attention alignment

Figure 2 shows decoder cross-attention on three MyST test utterances; the y-axis denotes decoder query position j and the x-axis denotes encoder key position i, with color intensity as attention weight A_ji. For each utterance, the same layer-head positions are plotted for full fine-tuning and AURA, with reference and decoded hypotheses.

- The illustrated cases are explicitly not intended as a corpus-level alignment metric but to show the type of behavior the uncertainty-routed edits can induce.
- First utterance: AURA recovers the reference exactly, while full fine-tuning deletes most of the phrase and outputs "girl." This coincides with a much cleaner diagonal under AURA, especially in head L11H5.
- Third utterance: both systems append the final spurious word "kill," but full fine-tuning additionally inserts the unrelated phrase "cold air and warm air and change" in the middle of the sentence; AURA instead stays aligned with the reference until the final over-extension, visible in heads such as L14H15 where AURA exhibits a stronger monotonic source-to-token pattern than full fine-tuning.
- Across these examples, AURA turns collapsed or off-diagonal heads under full fine-tuning into more monotonic cross-attention alignments.
- Caveat stated in chunk: this does not by itself prove a corpus-wide alignment shift, but it supports the proposed mechanism — AURA routes head-level edits according to cross-attention uncertainty, and in these cases cleaner alignment coincides with more grounded decoding.

## V. Conclusion (as stated in chunk)

- AURA is an ultra-efficient activation-editing method for reducing hallucination and improving acoustic grounding in AED speech foundation models.
- It freezes the pretrained model and applies sparse scale-and-shift edits to decoder cross-attention heads, using orders of magnitude fewer trainable parameters than LoRA — stated as 500× fewer trainable parameters than LoRA.
- Unlike static representation-editing methods, AURA routes each edit with cross-attention uncertainty features, intervening when decoder grounding becomes unstable.
- Across four datasets spanning non-speech audio, imperfect-label child and adult speech, and disfluent speech, AURA provides a parameter-efficient alternative to higher-capacity adaptation.
- On non-speech audio, AURA reduces hallucination without prior head identification; on unfiltered MyST it approaches LoRA at larger model sizes, while on TED-LIUM 3 it closely tracks LoRA across model sizes.
- The instability of some text-oriented representation-editing baselines highlights that AED models require interventions respecting the frame-token acoustic grounding path; AURA edits decoder cross-attention heads and routes edits using cross-attention uncertainty.
- AURA+Enc further shows that child speech and disfluent speech can still benefit from additional encoder adaptation capacity.
- Future work stated: extend analysis of uncertainty-routed editing to speech LLMs, code-switched ASR, and long-form decoding.

## Acknowledgements and disclosures (as stated in chunk)

- Supported in part by the National Science Foundation (NSF) and the Institute of Education Sciences (IES), U.S. Department of Education, through Grant R305C240046 to the U. at Buffalo; opinions are the authors' own.
- Generative AI use disclosure: ChatGPT (GPT-5.5) used for language editing (proofreading, clarity/readability) only; all technical content, experimental design, results, and conclusions produced and verified by the authors, who take full responsibility; AI tools not used for a significant portion of the manuscript and not listed as authors.

**Covers:** Results and analysis: hallucination reduction, grounding-stressor adaptation, ablations, and operating point.
