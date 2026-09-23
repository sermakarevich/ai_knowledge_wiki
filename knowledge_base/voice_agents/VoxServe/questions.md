---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: News
### Q1. What two artifacts did VoxServe announce in [2025-02], and what is each one about?
> [!tip]- Answer
> VoxServe published the blog post "Light-Speed Qwen3-TTS Serving at Scale with VoxServe" on its GitHub Pages site, focused on serving Qwen3-TTS at scale. It also released the paper "VoxServe: A Streaming-Centric Serving System for Speech Language Models" (arXiv:2602.00269), which presents VoxServe as a streaming-centric serving system for SpeechLMs. See [[wiki/02-news|News]].
### Q2. Which six TTS models does VoxServe support?
> [!tip]- Answer
> The supported TTS models are `chatterbox` (Chatterbox TTS), `cosyvoice2` (CosyVoice2-0.5B), `csm` (CSM-1B), `orpheus` (Orpheus-3B), `qwen3-tts` (Qwen3-TTS-1.7B), and `zonos` (Zonos-v0.1), each linked to its upstream HuggingFace checkpoint. The models documentation page holds detailed per-model information, and more models are noted as coming soon. See [[wiki/02-news|News]].
### Q3. Which two STS models does VoxServe support?
> [!tip]- Answer
> VoxServe supports two speech-to-speech models: `glm` (GLM-4-Voice-9B) and `step` (Step-Audio-2-Mini), each linked to its upstream HuggingFace checkpoint. Together with the six TTS models this makes eight supported models spanning both TTS and STS modalities. See [[wiki/02-news|News]].
### Q4. What latency result does the ultra-low-latency demo claim, and under what setup?
> [!tip]- Answer
> The demo claims 40 ms Time-To-First-Audio (TTFA) for a single TTS request running on an NVIDIA H100 GPU. The model used is `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, and the result is presented as evidence that VoxServe is optimized for real-time speech synthesis. See [[wiki/02-news|News]].
### Q5. How does Qwen3-TTS incremental text input enable real-time LLM voice-chatbot integration?
> [!tip]- Answer
> Qwen3-TTS accepts incremental text input, so text can be fed piece by piece as it arrives instead of waiting for the complete response. This enables seamless integration with LLMs for voice chatbots, as demonstrated by VoxServe connected to a local LLM with low end-to-end latency. See [[wiki/02-news|News]].
### Q6. What can you do in the VoxServe web-based playground?
> [!tip]- Answer
> The playground is a browser UI for interactive testing of VoxServe. You use it to manage servers, generate audio, and view real-time logs, which lowers adoption friction by making the system operable without custom tooling. See [[wiki/02-news|News]].
### Q7. Would you recommend VoxServe for a team building a real-time voice chatbot, and why?
> [!tip]- Answer
> Yes, for teams needing streaming speech output with minimal time-to-first-audio: it unifies six TTS and two STS models behind one serving story, supports incremental text input for live LLM voice-chatbot loops, offers a browser playground for quick iteration, and reports a 40 ms TTFA headline on H100 hardware. The main caveats are reproducing the latency figure on your own GPUs and confirming your target voice model is among the eight currently supported. See [[wiki/02-news|News]].
