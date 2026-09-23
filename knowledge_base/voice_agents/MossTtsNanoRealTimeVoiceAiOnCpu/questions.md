---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini - Firethering

### Q1. What access problem does MOSS-TTS-Nano solve, and what are its headline specs?
> [!tip]- Answer
> Nano breaks the tradeoff where good-sounding TTS needs serious hardware and models that run anywhere sound robotic, streaming real-time speech on 4 CPU cores with a 100M-parameter model. It outputs 48kHz stereo audio, supports 20 languages including Chinese, English, Arabic, Japanese, and Korean, and clones voices from a reference audio file with automatic chunking of long text. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q2. What are the five models in the MOSS-TTS family, and what problem is each built for?
> [!tip]- Answer
> The family shares one audio backbone and is all Apache 2.0: flagship MOSS-TTS (8B and 1.7B) for best quality and long-form zero-shot cloning, MOSS-TTSD for two-speaker dialogue, MOSS-VoiceGenerator for text-described voices with no reference audio, MOSS-TTS-Realtime for live voice agents, and MOSS-SoundEffect for environmental audio from text. Each was built for a different problem rather than being five versions of the same thing. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q3. How do you set up and run MOSS-TTS-Nano locally?
> [!tip]- Answer
> Setup is clone the repo, install requirements, and point it at a reference audio file plus text, with three interfaces: CLI, a local FastAPI web demo, and a Python API. A live demo also runs on Hugging Face for trying it without installing anything. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q4. How does the 8B flagship run light, and what are its four deployment configs?
> [!tip]- Answer
> The 8B flagship fits on an 8GB GPU and offers a fully torch-free path using llama.cpp for the backbone plus ONNX Runtime for the audio tokenizer, so no PyTorch install is required. The four llama.cpp configs are Default ONNX, TensorRT for maximum throughput, low-memory mode tuned for 8GB GPUs, and fully CPU-only with no GPU. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q5. What community tooling exists around the MOSS-TTS family?
> [!tip]- Answer
> Community contributions include a ComfyUI extension, an OpenAI-compatible TTS API wrapper, and AnyPod, a podcast generation tool using MOSS-TTS plus MOSS-TTSD as its backend. A Tosee developer also contributed a Norwegian LoRA adapter fine-tuned on the NST Norwegian speech dataset. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q6. What are the MOSS-TTSD speaker-similarity benchmark numbers, and what caveat applies?
> [!tip]- Answer
> On English speaker similarity, MOSS-TTSD-v1.0 scored 0.7893 versus Gemini 2.5 Pro at 0.6786 and ElevenLabs V3 at 0.6730, where the metric is whether multi-speaker audio sounds like the right person talking. On Chinese it scored 0.7949 versus Doubao Podcast at 0.8034, essentially a coin flip in practice. These are the team's own self-reported evaluations with documented methodology and a public benchmark, so they are specific enough to be meaningful but should be treated as such. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].

### Q7. Which MOSS model would you recommend for a CPU-only laptop demo today, a GPU-backed quality build, and a live voice agent — and why?
> [!tip]- Answer
> Recommend Nano for the CPU-only laptop demo since it streams in real time on 4 CPU cores with minutes-long setup, the 8B flagship for the GPU quality build since it fits an 8GB GPU with the low-memory config, and MOSS-TTS-Realtime for the live agent with its 180ms time-to-first-byte after warmup and conversation-long coherence. All five are on Hugging Face and ModelScope under Apache 2.0, so the choice turns on hardware and latency rather than licensing. See [[wiki/01-moss-tts-nano-real-time-voice-ai-on-cpu|MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini]].
