> [[index|Wiki]] | [[summary|Summary]]
# MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini - Firethering — Digest

## 1. [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]]

**In one sentence:** MOSS-TTS-Nano is a 100M-parameter model that streams good-sounding speech on a regular CPU, and it is the entry point to a five-model Apache 2.0 MOSS-TTS family whose dialogue model beats Gemini 2.5 Pro and ElevenLabs on speaker similarity.

- MOSS-TTS-Nano has 100M parameters and streams audio in real time on 4 CPU cores, removing the GPU/VRAM requirement that blocks local TTS adoption.
- Nano outputs 48kHz stereo audio, supports 20 languages including Chinese, English, Arabic, Japanese, and Korean, and clones voices from a reference audio file with automatic chunking of long text.
- Nano setup is clone the repo, install requirements, pass a reference audio file plus text, via CLI, local FastAPI web demo, or Python API; a demo is live on Hugging Face.
- The MOSS-TTS family from MOSI.AI and the OpenMOSS team (dropped April 13th per the article) has five distinct models sharing one audio backbone, all Apache 2.0: flagship MOSS-TTS (8B and 1.7B), MOSS-TTSD dialogue, MOSS-VoiceGenerator, MOSS-TTS-Realtime, MOSS-SoundEffect.
- MOSS-TTS-Realtime targets voice agents with 180ms time-to-first-byte after warmup, designed to respond in under half a second and stay coherent across a full conversation.
- The 8B flagship fits on an 8GB GPU, with a fully torch-free path (llama.cpp backbone + ONNX Runtime audio tokenizer) and four configs: Default ONNX, TensorRT, low-memory 8GB, and fully CPU-only.
- On English speaker similarity, MOSS-TTSD-v1.0 scored 0.7893 vs Gemini 2.5 Pro 0.6786 and ElevenLabs V3 0.6730; on Chinese it scored 0.7949 vs Doubao Podcast 0.8034 — self-reported, team-evaluated numbers the article flags as such.

## The argument in five moves

1. Local TTS faces an access problem: good-sounding models need serious hardware while models that run anywhere sound robotic.
2. Nano is the entry point that breaks the tradeoff — a 100M-parameter model streaming real-time speech on 4 CPU cores with 48kHz stereo, 20 languages, and reference-audio cloning.
3. The family is the story: five models sharing one audio backbone, each built for a different problem (flagship quality, dialogue, voice generation, realtime agents, sound effects), all Apache 2.0.
4. Running light is practical, not just promised — the 8B flagship fits on an 8GB GPU with a torch-free llama.cpp + ONNX path and four configs, plus community tooling around it.
5. The credibility anchor is the dialogue benchmark, with MOSS-TTSD beating Gemini 2.5 Pro and ElevenLabs on English speaker similarity and near-tying Doubao on Chinese, flagged as self-reported but documented and public.
6. The close is a picker: Nano for any-hardware local voice AI today, 8B for best quality with a GPU, TTSD for two-voice conversation, VoiceGenerator for text-described voices, Realtime for live agents.
