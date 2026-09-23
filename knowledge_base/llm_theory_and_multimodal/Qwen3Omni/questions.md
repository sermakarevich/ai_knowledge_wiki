---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: QwenLM/Qwen3-Omni

### Q1. What is Qwen3-Omni, and what inputs and outputs does it handle?

> [!tip]- Answer
> Qwen3-Omni is described as a natively end-to-end multilingual omni-modal foundation model. It processes text, images, audio, and video inputs and delivers real-time streaming responses in both text and natural speech. Low-latency streaming with natural turn-taking plus system-prompt control makes it suited to interactive voice/video use. See [[wiki/01-overview|Overview]].

### Q2. How was Qwen3-Omni trained, and what benchmark claims does the repo make?

> [!tip]- Answer
> It uses early text-first pretraining plus mixed multimodal training, which is claimed to give native multimodal support without regressing unimodal text/image performance. The repo claims SOTA on 22 of 36 audio/video benchmarks and open-source SOTA on 32 of 36, with ASR, audio understanding, and voice conversation comparable to Gemini 2.5 Pro. These figures frame it as breadth without a unimodal quality cost. See [[wiki/01-overview|Overview]].

### Q3. What architecture, language coverage, and captioner variant does Qwen3-Omni offer?

> [!tip]- Answer
> Its architecture is an MoE-based Thinker–Talker design with AuT pretraining and a multi-codebook design aimed at minimum latency. It supports 119 text languages, 19 speech-input languages, and 10 speech-output languages, with the exact lists enumerated in the README. A dedicated open-source Qwen3-Omni-30B-A3B-Captioner variant targets detailed, general-purpose, low-hallucination audio captioning. See [[wiki/01-overview|Overview]].

### Q4. What usage demos do the `cookbooks/` notebooks cover, and what setup do they assume?

> [!tip]- Answer
> The cookbooks cover audio tasks (speech recognition, speech translation, music, sound, caption, mixed-audio analysis), visual tasks (OCR, grounding, image QA, image math, video description, navigation, scene transitions), and audio-visual tasks. Each notebook ships with execution logs showing expected outputs. They are run locally after QuickStart model download and environment setup. See [[wiki/01-overview|Overview]].

### Q5. How does `web_demo.py` load models, and what voices and vLLM constraints apply?

> [!tip]- Answer
> It loads either `Qwen3OmniMoeForConditionalGeneration` via transformers or a vLLM `LLM` plus a `Qwen3OmniMoeProcessor`, selected by `args.use_transformers`, and forces `VLLM_USE_V1='0'` with `VLLM_WORKER_MULTIPROC_METHOD='spawn'` before importing vLLM. It offers three TTS voices `['Chelsie', 'Ethan', 'Aiden']` with `DEFAULT_VOICE='Chelsie'`. Audio generation is unsupported under the vLLM path, which is text-output only. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. How does `web_demo.py` handle conversation history and run inference?

> [!tip]- Answer
> It reformats Gradio history into chat messages, mapping uploads by mimetype to `image`/`video`/`audio` items with `.webm`-to-`.mp4` conversion, and evicts old turns beyond image 1 / video 5 / audio 5 limits. The transformers branch runs `processor.apply_chat_template` plus `process_mm_info(messages, use_audio_in_video=True)` plus `model.generate` with `thinker_max_new_tokens=32768` and the chosen speaker, emitting 24 kHz WAV output. The vLLM branch instead uses `SamplingParams(temperature, top_p, top_k, max_tokens=16384)`. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. When should you choose `web_demo_captioner.py` over `web_demo.py`, and how is it configured?

> [!tip]- Answer
> Choose the captioner demo for single-audio detailed captioning and the chat demo for full multimodal text/image/audio/video conversation with voice output. The captioner defaults to `Qwen/Qwen3-Omni-30B-A3B-Captioner` on port `8901`, limits its vLLM path to one audio per prompt with `max_model_len=65536`, and exposes upload/microphone input with temperature/top_p/top_k sliders behind `generate_caption_from_audio` / `on_submit`. Its transformers branch generates with `thinker_max_new_tokens=32768` while the vLLM branch allows up to 32768 output tokens. See [[wiki/02-top-level-files|Top-level-files]].
