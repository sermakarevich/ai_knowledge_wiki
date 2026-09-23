> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# News
**In one sentence:** VoxServe announced its Qwen3-TTS at-scale serving blog post and streaming-centric SpeechLM paper in [2025-02], alongside 8 supported TTS/STS models, a 40 ms TTFA demo, LLM voice-chatbot integration, and a web playground.
## Key points
- In [2025-02] VoxServe published the blog post "Light-Speed Qwen3-TTS Serving at Scale with VoxServe".
- In [2025-02] VoxServe released the paper "VoxServe: A Streaming-Centric Serving System for Speech Language Models" (arXiv:2602.00269).
- VoxServe supports 6 TTS models (`chatterbox`, `cosyvoice2`, `csm`, `orpheus`, `qwen3-tts`, `zonos`) and 2 STS models (`glm`, `step`).
- An ultra-low-latency TTS demo achieves **40 ms** Time-To-First-Audio (TTFA) on an NVIDIA H100 GPU with `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`.
- Qwen3-TTS supports incremental text input, enabling seamless integration with local LLMs for voice chatbots with low end-to-end latency.
- VoxServe includes a web-based playground UI to manage servers, generate audio, and view real-time logs.
- VoxServe delivers low-latency, high-throughput inference for Speech Language Models (SpeechLMs), including text-to-speech (TTS) and speech-to-speech (STS) models.
---
## News announcements
- **[2025-02]** Blog post: [Light-Speed Qwen3-TTS Serving at Scale with VoxServe](https://vox-serve.github.io/2026/02/09/qwen3-tts-support.html)
- **[2025-02]** Paper released: [VoxServe: A Streaming-Centric Serving System for Speech Language Models](https://arxiv.org/abs/2602.00269)

## Supported Models
VoxServe supports the following TTS and STS models:

| Model | Type | Link |
|-------|------|------|
| `chatterbox` | TTS | [Chatterbox TTS](https://huggingface.co/ResembleAI/chatterbox) |
| `cosyvoice2` | TTS | [CosyVoice2-0.5B](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B) |
| `csm` | TTS | [CSM-1B](https://huggingface.co/sesame/csm-1b) |
| `orpheus` | TTS | [Orpheus-3B](https://huggingface.co/canopylabs/orpheus-3b-0.1-ft) |
| `qwen3-tts` | TTS | [Qwen3-TTS-1.7B](https://huggingface.co/collections/Qwen/qwen3-tts) |
| `zonos` | TTS | [Zonos-v0.1](https://huggingface.co/Zyphra/Zonos-v0.1-transformer) |
| `glm` | STS | [GLM-4-Voice-9B](https://huggingface.co/zai-org/glm-4-voice-9b) |
| `step` | STS | [Step-Audio-2-Mini](https://huggingface.co/stepfun-ai/Step-Audio-2-mini) |

See the [models documentation](https://vox-serve.github.io/vox-serve/models.html) for detailed information. More models coming soon.

## Demos
### Ultra-Low Latency
VoxServe is optimized for real-time speech synthesis. The demo below shows a TTS request achieving **40 ms** Time-To-First-Audio (TTFA) on an NVIDIA H100 GPU with `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`.

### Real-Time LLM Integration
Qwen3-TTS supports incremental text input, enabling seamless integration with LLMs for voice chatbots. The demo below shows VoxServe connected to a local LLM with low end-to-end latency.

## Playground
VoxServe includes a web-based playground for interactive testing. Use the browser UI to manage servers, generate audio, and view real-time logs.

**Covers:** News announcements: Qwen3-TTS blog post, VoxServe paper release, supported TTS/STS models, demos, and playground
