> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini
**In one sentence:** MOSS-TTS-Nano is a 100M-parameter model that streams good-sounding speech on a regular CPU, and it is the entry point to a five-model Apache 2.0 MOSS-TTS family whose dialogue model beats Gemini 2.5 Pro and ElevenLabs on speaker similarity.
## Key points
- MOSS-TTS-Nano has 100M parameters and streams audio in real time on 4 CPU cores, removing the GPU/VRAM requirement that blocks local TTS adoption.
- Nano outputs 48kHz stereo audio, supports 20 languages including Chinese, English, Arabic, Japanese, and Korean, and clones voices from a reference audio file with automatic chunking of long text.
- Nano setup is clone the repo, install requirements, pass a reference audio file plus text, via CLI, local FastAPI web demo, or Python API; a demo is live on Hugging Face.
- The MOSS-TTS family from MOSI.AI and the OpenMOSS team (dropped April 13th per the article) has five distinct models sharing one audio backbone, all Apache 2.0: flagship MOSS-TTS (8B and 1.7B), MOSS-TTSD dialogue, MOSS-VoiceGenerator, MOSS-TTS-Realtime, MOSS-SoundEffect.
- MOSS-TTS-Realtime targets voice agents with 180ms time-to-first-byte after warmup, designed to respond in under half a second and stay coherent across a full conversation.
- The 8B flagship fits on an 8GB GPU, with a fully torch-free path (llama.cpp backbone + ONNX Runtime audio tokenizer) and four configs: Default ONNX, TensorRT, low-memory 8GB, and fully CPU-only.
- On English speaker similarity, MOSS-TTSD-v1.0 scored 0.7893 vs Gemini 2.5 Pro 0.6786 and ElevenLabs V3 0.6730; on Chinese it scored 0.7949 vs Doubao Podcast 0.8034 — self-reported, team-evaluated numbers the article flags as such.
---
## Meet the Family
**Covers:** flagship / dialogue / generator / realtime / soundeffect roles

The family "isn't five versions of the same thing. Each model was built for a different problem."

- MOSS-TTS (flagship): best voice quality, zero-shot voice cloning, long-form speech stable across minutes, fine-grained pronunciation control; two sizes, 8B and 1.7B.
- MOSS-TTSD (dialogue): two speakers back and forth with natural pacing and expressiveness; "the one that beat Gemini 2.5 Pro and ElevenLabs."
- MOSS-VoiceGenerator: describe a voice in plain text (age, tone, accent, character) and it creates one from scratch with no reference audio needed.
- MOSS-TTS-Realtime (voice agents): 180ms time-to-first-byte after warmup.
- MOSS-SoundEffect: generates environmental audio (rain, traffic, crowd noise, mechanical sounds) from text descriptions with controllable duration, for games/videos/interactive experiences.

> "Five models, one shared audio backbone, all Apache 2.0."

## MOSS-TTS-Nano: The One That Changes the Access Problem
**Covers:** 100M params, CPU deployment, quality/languages, setup

The article's framing quote:

> "Most text-to-speech AI fall into two camps. The ones that sound good need serious hardware. The ones that run on anything sound robotic. MOSS-TTS-Nano is trying to be neither."

> "Nano is the entry point. The family is the story."

- 100M parameters; runs on a regular CPU, streaming in real time on 4 CPU cores — no GPU spec needed for local-app users, no cloud compute needed for tests, usable on a modest laptop.
- 48kHz stereo output ("higher than most TTS models output by default"); 20 languages including Chinese, English, Arabic, Japanese, Korean and more.
- Voice cloning via reference audio file; long text handled automatically by chunking.
- Setup: clone repo, install requirements, point at reference audio + text; CLI, local web demo via FastAPI, Python API.

## Running Light, Building Fast
**Covers:** 8B deployment paths and community tooling

- 8B flagship fits on an 8GB GPU; torch-free path uses llama.cpp for the backbone and ONNX Runtime for the audio tokenizer — no PyTorch install required.
- Four llama.cpp configs: Default ONNX, TensorRT for maximum throughput, low-memory mode tuned for 8GB GPUs, fully CPU-only with no GPU.
- Community tooling: ComfyUI extension; OpenAI-compatible TTS API wrapper; AnyPod podcast generation tool (MOSS-TTS + MOSS-TTSD backend); Norwegian LoRA adapter fine-tuned on the NST Norwegian speech dataset (contributed by a Tosee developer).

## The Number Worth Knowing
**Covers:** TTSD speaker-similarity benchmarks vs Gemini 2.5 Pro / ElevenLabs / Doubao

Article caveat, verbatim in spirit:

> "These are the team's own evaluations so treat them as self-reported. But the methodology is documented, the benchmark is public, and the numbers are specific enough to be meaningful."

| Model | EN SIM | ZH SIM |
|---|---|---|
| MOSS-TTSD-v1.0 | 0.7893 | 0.7949 |
| Gemini 2.5 Pro | 0.6786 | — |
| ElevenLabs V3 | 0.6730 | 0.6970 |
| Doubao Podcast | — | 0.8034 |

- English speaker similarity: MOSS-TTSD 0.7893 vs Gemini 2.5 Pro 0.6786 vs ElevenLabs V3 0.6730 — the metric is "does it actually sound like the right person is talking" for multi-speaker audio.
- Chinese speaker similarity: MOSS-TTSD 0.7949 vs Doubao Podcast 0.8034 ("close enough that the gap is essentially a coin flip in practice").

## Which One Is Right for You
**Covers:** model picker and availability

- Try local voice AI today on any hardware: Nano (setup takes minutes; demo live on Hugging Face).
- Best voice quality with a GPU: 8B flagship (GGUF weights ready, llama.cpp path, 8GB GPU enough with low-memory config).
- Two voices in natural conversation: MOSS-TTSD (article calls it the strongest open-source option in that space).
- New voice from text description with no reference audio: MOSS-VoiceGenerator.
- Live voice agent needing fast response + conversation consistency: MOSS-TTS-Realtime.
- Availability: all five on Hugging Face and ModelScope; main repo on GitHub under OpenMOSS; whole family Apache 2.0 — "build, fine-tune & use commercially."

**Covers:** Nano 100M CPU real-time model plus the 5-model MOSS-TTS family, TTSD benchmarks vs Gemini/ElevenLabs, and which-model picker
