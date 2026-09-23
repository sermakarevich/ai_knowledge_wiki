---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: OpenMOSS/MOSS-TTS
### Q1. What is the MOSS-TTS Family and who builds it?
> [!tip]- Answer
> MOSS-TTS Family is an open-source speech and sound generation model family from MOSI.AI and the OpenMOSS team. It targets high-fidelity, high-expressiveness audio for complex real-world scenarios. Those scenarios span stable long-form speech, multi-speaker dialogue, voice design, environmental sound effects, and real-time streaming TTS. See [[wiki/01-overview|Overview]].
### Q2. Which model should you start with for each task in the MOSS-TTS chooser table?
> [!tip]- Answer
> Nano fits CPU or browser speech synthesis and voice cloning, while v1.5 / Local Transformer v1.5 fits multilingual long-form narration and cloning. TTSD fits multi-speaker dialogue, podcasts, and dubbing, and Realtime fits real-time streaming speech. Voice design or environmental sound effects start from the released-models overview or SoundEffect v2. See [[wiki/01-overview|Overview]].
### Q3. What were the headline MOSS-TTS releases in June 2026?
> [!tip]- Answer
> On 2026.6.18 the Local-Transformer-v1.5 4B checkpoint shipped with a Qwen3-4B backbone, Audio-Tokenizer-v2, and native 48 kHz stereo output. The same day brought Day-0 SGLang-Omni support with an OpenAI-compatible streaming endpoint and voice cloning. Earlier, on 2026.6.7, MOSS-Audio-Tokenizer-v2 shipped with 48 kHz stereo input/output. See [[wiki/01-overview|Overview]].
### Q4. What entry points and README structure orient a new MOSS-TTS user?
> [!tip]- Answer
> The landing page routes newcomers to Quickstart, Hugging Face model weights, the samples demo, fine-tuning, and serving backends. A demo video plus a Contents index (Introduction, Model Architecture, Released Models, Quickstart, Fine-Tuning, backends, Evaluation, Nano, Audio-Tokenizer, License, Citation) structures the README. The Introduction frames the family as five production-ready models because no single TTS model covers real-person quality, accuracy, style-switching, long stability, and interactive use. See [[wiki/01-overview|Overview]].
### Q5. What does the MOSS-TTS repo root ignore, and what single submodule does it declare?
> [!tip]- Answer
> The root `.gitignore` is a standard Python template covering bytecode, packaging, tests, envs, and IDE files, with project-specific tails ignoring `weights` and `outputs/*`. The `.gitmodules` file declares exactly one submodule, `moss_audio_tokenizer`, pointing at the MOSS-Audio-Tokenizer GitHub repo. Together they keep large weights and generated outputs out of git while pinning the shared codec dependency. See [[wiki/02-top-level-files|top-level-files]].
### Q6. What does MANIFEST.in include, graft, prune, and exclude when packaging MOSS-TTS?
> [!tip]- Answer
> It includes README.md, README_zh.md, LICENSE, and pyproject.toml, and grafts assets, docs, moss_tts_delay, moss_tts_local, moss_tts_realtime, and moss_audio_tokenizer. It prunes .git, .github, .vscode, and moss_tts.egg-info to keep VCS and build artifacts out of the sdist. Global excludes drop __pycache__, *.py[cod], .DS_Store, and *.so files. See [[wiki/02-top-level-files|top-level-files]].
### Q7. A team needs multilingual long-form narration plus a live streaming voice agent: which MOSS-TTS starting points would you recommend and why?
> [!tip]- Answer
> I would recommend v1.5 / Local Transformer v1.5 for the narration track because it is positioned for multilingual long-form stability at 48 kHz stereo, and Realtime for the agent track because it targets low-TTFB streaming with multi-turn context. Splitting the work this way matches the family's premise that one model cannot cover fidelity, long stability, and real-time interaction at once. Confirm against the chooser table and current backend support (SGLang-Omni / vLLM-Omni) before committing. See [[wiki/01-overview|Overview]].
