> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** PaddleSpeech is an open-source PaddlePaddle-based toolkit for speech and audio tasks (ASR, TTS, translation, speaker verification, and more) with training, inference, and deployment support.
## Key points
- PaddleSpeech is an open-source toolkit on the PaddlePaddle platform for speech and audio tasks using state-of-the-art models (README.md:38).
- The project won the NAACL2022 Best Demo Award with paper at `https://arxiv.org/abs/2205.12007` (README.md:40).
- Demonstrated tasks include Speech Recognition (EN/ZH examples, README.md:58, README.md:65), English-to-Chinese Speech Translation (README.md:88), Text-to-Speech in multiple languages/dialects (README.md:106, README.md:113, README.md:134, README.md:141), and Punctuation Restoration (README.md:165-README.md:166).
- Stated vision is easy-to-use, efficient, flexible, scalable implementation empowering industrial application and academic research across training, inference/testing, and deployment (README.md:176).
- Entry points for quick start are CLI, Server, and Streaming Server, plus production-ready streaming ASR and streaming TTS systems (README.md:177, README.md:179).
- The Chinese frontend is rule-based with Text Normalization and G2P including polyphone and tone sandhi plus self-defined linguistic rules (README.md:180).
- Task coverage spans ASR, TTS synthesis, Speaker Verification, Keyword Spotting, Audio Classification, and Speech Translation, integrated with mainstream datasets such as LibriSpeech, LJSpeech, AIShell, and CSMSC (README.md:182-README.md:183).
---
## Demonstrated capabilities
Audio-in/text-out and text-in/audio-out demos from `README.md`:

| Capability | Example input | Example output |
|---|---|---|
| Speech Recognition (README.md:42) | EN audio `en.wav` (README.md:55) | `I knocked at the door on the ancient side of the building.` (README.md:58) |
| Speech Recognition (README.md:42) | ZH audio `zh.wav` (README.md:62) | `我认为跑步最重要的就是给我带来了身体健康。` (README.md:65) |
| Speech Translation EN→ZH (README.md:72) | EN audio `en.wav` (README.md:85) | `我 在 这栋 建筑 的 古老 门上 敲门。` (README.md:88) |
| Text-to-Speech (README.md:95) | `Life was like a box of chocolates, you never know what you're gonna get.` (README.md:106) | `tacotron2_ljspeech_waveflow_samples_0.2/sentence_1.wav` (README.md:108) |
| Text-to-Speech (README.md:95) | `早上好，今天是2020/10/29，最低温度是-3°C。` (README.md:113) | `tn_g2p/parakeet/001.wav` (README.md:115) |
| Text-to-Speech (README.md:95) | Cantonese inputs, e.g. `宜家唔系事必要你讲，但系你所讲嘅说话将会变成呈堂证供。` (README.md:134) | `chengtangzhenggong.wav` (README.md:137) |
| Punctuation Restoration (README.md:154) | `今天的天气真不错啊你下午有空吗我想约你一起去吃饭` (README.md:165) | `今天的天气真不错啊！你下午有空吗？我想约你一起去吃饭。` (README.md:166) |

More TTS samples are referenced at `https://paddlespeech.readthedocs.io/en/latest/tts/demo.html` (README.md:152).

## Features
Verbatim feature list from `README.md:176-README.md:184`:
- `Ease of Use`: `low barriers to install, [CLI](#quick-start), [Server](#quick-start-server), and [Streaming Server](#quick-start-streaming-server) is available to quick-start your journey.` (README.md:177)
- `Align to the State-of-the-Art`: `we provide high-speed and ultra-lightweight models, and also cutting-edge technology.` (README.md:178)
- `Streaming ASR and TTS System`: `we provide production ready streaming asr and streaming tts system.` (README.md:179)
- `Rule-based Chinese frontend`: `our frontend contains Text Normalization and Grapheme-to-Phoneme (G2P, including Polyphone and Tone Sandhi). Moreover, we use self-defined linguistic rules to adapt Chinese context.` (README.md:180)
- `Cascaded models application`: `as an extension of the typical traditional audio tasks, we combine the workflows of the aforementioned tasks with other fields like Natural language processing (NLP) and Computer Vision (CV).` (README.md:184)

Project metadata from `README.md:13-README.md:23`: license `Apache 2` (README.md:14), supports `linux, win, mac` (README.md:15), requires `python-3.8+` (README.md:16), distributed via PyPI as `paddlespeech` (README.md:21-README.md:22).

## Recent updates (selected)
Selected verbatim entries from `README.md:187-README.md:215`:
- `2025.09.01: Add [Whisper large v3 and turbo model](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/whisper).` (README.md:187)
- `2025.08.11: Add [code-switch online model and server demo](./examples/tal_cs/asr1/).` (README.md:188)
- `2023.05.31: Add [WavLM ASR-en](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/examples/librispeech/asr5), WavLM fine-tuning for ASR on LibriSpeech.` (README.md:189)
- `2022.11.18: Add [Whisper CLI and Demos](https://github.com/PaddlePaddle/PaddleSpeech/pull/2640), support multi language recognition and translation.` (README.md:206)
- `2022.11.07: Add [U2/U2++ C++ High Performance Streaming ASR Deployment](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/runtime/examples/u2pp_ol/wenetspeech).` (README.md:209)

## Component map
The chunk's macro-component list contains only:
- `top-level-files/` (chunk 01-overview.md:219)

No other macro components are listed in this chunk; detailed coverage of `top-level-files/` belongs to page `02-top-level-files.md`.

**Covers:** README.md, README_cn.md (linked at chunk 01-overview.md:7), docs/images/PaddleSpeech_logo.png (chunk 01-overview.md:9)
