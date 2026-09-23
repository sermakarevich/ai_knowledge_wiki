# Plan — NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities

Source: https://arxiv.org/abs/2609.21967 (kind: pdf via pdftotext)
Run dir: /Users/sergii/.fleet/workflows/summary_get/wfr-6816papv
Paper dir: /Users/sergii/.ai/knowledge/research/NemotronLabsVoiceChat

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-2026-9-21-nemotronlabs-voicechat-an-open-full-du | 01-overview-architecture.md | Covers paper intro, abstract, full-duplex motivation and architecture overview. |
| 02-2-1-speech-to-text-stt-the-stt-component | 02-speech-to-text.md | Covers the STT component: streaming encoder, LLM backbone and auxiliary transcription branch. |
| 03-component-wise-training-the-full-duplex-stt-back | 03-training-recipes.md | Covers component-wise training of the full-duplex STT backbone, RNN-T branch and TTS. |
| 04-respond-resume-uncertain-unknown-model | 04-backchannel-evaluation.md | Covers backchannel behavior classes (Respond/Resume/Uncertain/Unknown) and model comparison. |
| 05-4-bandhav-veluri-benjamin-n-peloquin | 05-references-background.md | Covers cited prior work on full-duplex speech models starting at reference [4]. |
| 06-sft-data-construction-like-the-cpt | 06-sft-data-construction.md | Covers SFT data construction following the CPT approach. |
| 07-we-evaluate-the-voicechat-tts-speech-decoder | 07-tts-decoder-evaluation.md | Covers evaluation of the VoiceChat-TTS speech decoder. |
