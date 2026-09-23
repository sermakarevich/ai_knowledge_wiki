> [[index|Wiki]] | [[summary|Summary]]
# QwenLM/Qwen3-Omni — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Qwen3-Omni is a natively end-to-end multilingual omni-modal foundation model that takes text, image, audio, and video input and streams back text plus natural speech in real time.
## Key points
- Qwen3-Omni processes text, images, audio, and video inputs and delivers real-time streaming text and natural-speech responses (README.md:22).
- Early text-first pretraining plus mixed multimodal training gives native multimodal support without regressing unimodal text/image performance (README.md:74).
- It reaches SOTA on 22 of 36 audio/video benchmarks and open-source SOTA on 32 of 36, with ASR, audio understanding, and voice conversation comparable to Gemini 2.5 Pro (README.md:74).
- It supports 119 text languages, 19 speech-input languages, and 10 speech-output languages, with the exact language lists enumerated in the README (README.md:76-78).
- Its architecture is an MoE-based Thinker–Talker design with AuT pretraining and a multi-codebook design for minimum latency (README.md:80).
- It supports low-latency streaming audio/video interaction with natural turn-taking, system-prompt control, and a dedicated open-source captioner variant Qwen3-Omni-30B-A3B-Captioner (README.md:82-86).
- Usage is demonstrated through `cookbooks/` notebooks with execution logs covering audio, visual, and audio-visual tasks, run locally after QuickStart model download and environment setup (README.md:96).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repo's top level provides two Gradio demo entry points — a multimodal chat demo (`web_demo.py`) and an audio-captioning demo (`web_demo_captioner.py`) — each loadable via transformers or vLLM.
## Key points
- `web_demo.py` loads either `Qwen3OmniMoeForConditionalGeneration` (transformers path) or `vLLM LLM` (vLLM path) plus a `Qwen3OmniMoeProcessor`, selected by `args.use_transformers` (web_demo.py:27-51).
- `web_demo.py` forces `VLLM_USE_V1='0'` and `VLLM_WORKER_MULTIPROC_METHOD='spawn'` before importing vLLM (web_demo.py:5-6).
- `web_demo.py` offers three TTS voices `['Chelsie', 'Ethan', 'Aiden']` with `DEFAULT_VOICE='Chelsie'`, and warns audio generation is unsupported under vLLM (web_demo.py:56-63).
- `web_demo.py` reformats Gradio history into chat messages, converting uploads by mimetype to `image`/`video`/`audio` items with `.webm`-to-`.mp4` conversion, and evicts old turns beyond image 1 / video 5 / audio 5 limits (web_demo.py:92-187).
- `web_demo.py` runs transformers inference via `processor.apply_chat_template` + `process_mm_info(messages, use_audio_in_video=True)` + `model.generate(..., thinker_max_new_tokens=32768, speaker=voice_choice, ...)` with 24 kHz WAV output, or vLLM inference via `SamplingParams(temperature, top_p, top_k, max_tokens=16384)` (web_demo.py:189-224).
- `web_demo_captioner.py` is an audio-only captioning demo whose vLLM path is limited to `limit_mm_per_prompt={'audio': 1}` and `max_model_len=65536` (web_demo_captioner.py:12-42).
- `web_demo_captioner.py` exposes a single-audio Gradio UI (upload/microphone, temperature/top_p/top_k sliders, Submit/Clear) backed by `generate_caption_from_audio` / `on_submit`, with defaults `DEFAULT_CKPT_PATH="Qwen/Qwen3-Omni-30B-A3B-Captioner"` and server port `8901` (web_demo_captioner.py:286-414).

## The system in five moves
1. Qwen3-Omni is framed as a natively end-to-end multilingual omni-modal foundation model taking text, image, audio, and video in and streaming text plus natural speech out in real time.
2. Native multimodal breadth is claimed to cost nothing on unimodal quality via early text-first pretraining plus mixed multimodal training, reaching SOTA on 22 of 36 and open-source SOTA on 32 of 36 audio/video benchmarks.
3. That capability is packaged as a MoE-based Thinker–Talker architecture with AuT pretraining and multi-codebook low-latency design, plus a dedicated Qwen3-Omni-30B-A3B-Captioner variant and cookbook demos.
4. The repo's top level exposes this through two Gradio entry points — full multimodal chat (`web_demo.py`) and audio-only captioning (`web_demo_captioner.py`) — each loadable via transformers or vLLM.
5. Both demos converge on the same inference pattern (`apply_chat_template` → `process_mm_info` with `use_audio_in_video=True` → `generate`/`SamplingParams`) with voice selection, turn/media limits, and vLLM constraints (no audio generation in chat demo, single-audio 64k context in captioner) controlling the interaction.
