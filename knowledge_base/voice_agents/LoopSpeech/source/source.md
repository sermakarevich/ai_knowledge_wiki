> PDF/original location (no source.pdf bundled, <2 MB rule N/A): https://github.com/FreedomIntelligence/LoopSpeech
# FreedomIntelligence/LoopSpeech
Source: https://github.com/FreedomIntelligence/LoopSpeech
Kind: repo
Fetched: 2026-09-22T14:16:35.009079+00:00
Tool: git-clone

# FreedomIntelligence/LoopSpeech

Commit: 613deb05c2aa26bac37bbf32171690500c5512de

## README

# LoopSpeech

Official repository for **"What Did I Just Say? Self-Listening for Full-Duplex Speech Models"**.

> **Status:** Preprint. Code, models, data, and the public paper link will be added as they become available.

<p align="center">
  <img src="assets/self-listening-overview.png" alt="Self-Listening overview: human self-monitoring and model self-listening" width="100%">
</p>

<p align="center"><em>Self-Listening feeds the model speech already played to the user back into the listening pathway, mirroring human speech self-monitoring.</em></p>

## Overview

Full-duplex speech models can listen and speak at the same time, enabling interruptions and backchannels. Yet text generation, speech synthesis, and audio playback run asynchronously: a model may have generated content that the user has not actually heard.

This creates an **anchoring gap** between what the model believes it has said and what was really played to the user. The gap becomes critical when a user interrupts with requests such as:

- "What did you just say?"
- "Repeat the last item."
- "Where did you stop?"
- "Continue from there."

LoopSpeech introduces **Self-Listening**, a playback-grounded approach that lets a full-duplex model track its own realized speech and recover consistently after interruptions.

## Method

<p align="center">
  <img src="assets/self-listening-architecture.png" alt="Three-channel Self-Listening architecture" width="100%">
</p>

<p align="center"><em>The three-channel architecture interleaves user speech, played model speech, and model text on a shared timeline while handling overlap and interruption control.</em></p>

Self-Listening organizes an interaction as three time-aligned streams:

1. **User speech** - the incoming audio from the user.
2. **Played model speech** - only the model waveform that has already reached user-side playback.
3. **Model text** - response tokens and full-duplex control tokens.

The streams are interleaved on a shared 40 ms timeline. Played model speech is fed back through the model's speech-input pathway, giving the model a causal record of what the user has actually heard without delaying generation or playback.

The system is built on the Thinker branch of **Qwen2.5-Omni-7B** and uses a frozen **MOSS-TTS-Realtime** model for streaming synthesis. Native control tokens support overlap handling, interruption stopping, backchannel continuation, waiting, and silence.

## AnchorSpeech

The paper also introduces **AnchorSpeech**, a time-aligned collection for training and evaluating anchoring-sensitive interruptions.

AnchorSpeech-test measures whether a model's response after an interruption is consistent with the last completed item that was actually played, rather than with text that may only have been generated internally.

## Main Results

On AnchorSpeech-test:

| Model | Anchoring accuracy | Stop latency | Response latency |
|---|---:|---:|---:|
| GPT-Realtime-2.1 | 43.8% | 0.296 s | 1.548 s |
| Two-channel full-duplex model | 7.8% | 0.425 s | 0.567 s |
| **Three-channel Self-Listening model** | **73.0%** | **0.434 s** | **0.564 s** |

Self-Listening improves anchoring accuracy by:

- **65.2 percentage points** over the matched two-channel model.
- **29.2 percentage points** over GPT-Realtime-2.1, the strongest evaluated commercial baseline.

The nearly unchanged stopping and response latencies in the controlled two-channel/three-channel comparison indicate that the improvement comes from playback-grounded context rather than a slower interruption strategy.

Experiments on Full-Duplex-Bench v1.5 further show sub-second response latency in interruption and backchannel scenarios, while revealing a trade-off between anchoring and conventional turn-management performance.

## Authors

Xuanning Zhou*, Junyi Ao*, Xiaotong Liu, Tom Ko†, Benyou Wang, and Haizhou Li

- Shenzhen Loop Area Institute, China
- The Chinese University of Hong Kong, Shenzhen, China

\* Equal contribution.  
† Corresponding author.

## Citation

If you find this work useful, please cite:

```bibtex
@misc{zhou2026loopspeech,
  title        = {What Did I Just Say? Self-Listening for Full-Duplex Speech Models},
  author       = {Zhou, Xuanning and Ao, Junyi and Liu, Xiaotong and Ko, Tom and Wang, Benyou and Li, Haizhou},
  year         = {2026},
  note         = {Preprint}
}
```

The citation will be updated when a permanent paper identifier or venue record becomes available.

## Repository Roadmap

- [ ] Paper link
- [ ] Inference and training code
- [ ] Model checkpoints
- [ ] AnchorSpeech data and evaluation scripts
- [ ] Reproducible examples and demos

## Contact

Please open an issue in this repository for questions and updates.


## Top-level layout

- assets/ (dir, 2 files, ~0 lines)
- README.md (~104 lines)

