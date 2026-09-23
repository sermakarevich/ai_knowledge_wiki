> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Qwen3-Omni is a natively end-to-end multilingual omni-modal foundation model that takes text, image, audio, and video input and streams back text plus natural speech in real time.
## Key points
- Qwen3-Omni processes text, images, audio, and video inputs and delivers real-time streaming text and natural-speech responses (README.md:22).
- Early text-first pretraining plus mixed multimodal training gives native multimodal support without regressing unimodal text/image performance (README.md:74).
- It reaches SOTA on 22 of 36 audio/video benchmarks and open-source SOTA on 32 of 36, with ASR, audio understanding, and voice conversation comparable to Gemini 2.5 Pro (README.md:74).
- It supports 119 text languages, 19 speech-input languages, and 10 speech-output languages, with the exact language lists enumerated in the README (README.md:76-78).
- Its architecture is an MoE-based Thinker–Talker design with AuT pretraining and a multi-codebook design for minimum latency (README.md:80).
- It supports low-latency streaming audio/video interaction with natural turn-taking, system-prompt control, and a dedicated open-source captioner variant Qwen3-Omni-30B-A3B-Captioner (README.md:82-86).
- Usage is demonstrated through `cookbooks/` notebooks with execution logs covering audio, visual, and audio-visual tasks, run locally after QuickStart model download and environment setup (README.md:96).
---
## Introduction
Verbatim definition (README.md:72):

> `Qwen3-Omni is the natively end-to-end multilingual omni-modal foundation models. It processes text, images, audio, and video, and delivers real-time streaming responses in both text and natural speech.`

Key features (README.md:74-86):
- **State-of-the-art across modalities**: text-first pretraining + mixed multimodal training; SOTA 22/36, open-source SOTA 32/36 audio/video benchmarks.
- **Multilingual**: 119 text languages; 19 speech-input languages (`English, Chinese, Korean, Japanese, German, Russian, Italian, French, Spanish, Portuguese, Malay, Dutch, Indonesian, Turkish, Vietnamese, Cantonese, Arabic, Urdu`); 10 speech-output languages (`English, Chinese, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean`).
- **Novel Architecture**: `MoE-based Thinker–Talker` + `AuT pretraining` + `multi-codebook design`.
- **Real-time Audio/Video Interaction**: low-latency streaming, natural turn-taking, immediate text or speech responses.
- **Flexible Control**: behavior customization via `system prompts`.
- **Detailed Audio Captioner**: `Qwen3-Omni-30B-A3B-Captioner`, general-purpose, detailed, low-hallucination.
## Model Architecture
The README architecture section (README.md:88-92) is a diagram placeholder only — no prose, parameters, or layer/config details are present in this chunk:

> `<img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/overview.png" width="80%"/>`

No weights, dimensions, codebook counts, or training hyperparameters are stated here.
## Cookbooks for Usage Cases
Cookbooks under `cookbooks/` demonstrate audio, image, video, and audio-visual tasks with execution logs (README.md:96). Representative entries (README.md:109-174):

| Category | Cookbook | Description |
| --- | --- | --- |
| Audio | `speech_recognition.ipynb` | Speech recognition, multiple languages and long audio |
| Audio | `speech_translation.ipynb` | Speech-to-Text / Speech-to-Speech translation |
| Audio | `music_analysis.ipynb` | Music style, genre, rhythm analysis |
| Audio | `sound_analysis.ipynb` | Sound effects and audio signals |
| Audio | `audio_caption.ipynb` | Detailed description of any audio input |
| Audio | `mixed_audio_analysis.ipynb` | Mixed speech, music, environmental sounds |
| Visual | `ocr.ipynb` | OCR for complex images |
| Visual | `object_grounding.ipynb` | Target detection and grounding |
| Visual | `image_question.ipynb` | Arbitrary image QA |
| Visual | `image_math.ipynb` | Math problems in images (Thinking model) |
| Visual | `video_description.ipynb` | Detailed video description |
| Visual | `video_navigation.ipynb` | Navigation commands from first-person video |
| Visual | `video_scene_transition.ipynb` | Scene-transition analysis |

Truncation note: this chunk is cut mid-row at the Audio-Visual cookbook table (README.md:177, `audio_visual_q...`), so Audio-Visual entries and everything after the Overview section (QuickStart, interaction, Docker, evaluation, citation) are not covered here.
**Covers:** `README.md` (Overview / Introduction / Model Architecture / Cookbooks for Usage Cases)
