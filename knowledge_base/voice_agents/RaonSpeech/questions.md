---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: krafton-ai/Raon-Speech

### Q1. What are the two Raon-Speech tracks and what do they share?
> [!tip]- Answer
> The repo holds Raon-Speech (offline SpeechLM: TTS, STT, SpeechChat, TextQA) and Raon-SpeechChat (offline/realtime full-duplex), which share one core model family and processor stack under `src/raon/`. Both tracks are served by a single shared `RaonModel` backbone with model types `raon` and `raon_duplex`. See [[wiki/01-overview|Overview]].

### Q2. What scale of data and benchmark coverage underpins Raon-Speech?
> [!tip]- Answer
> Raon-Speech is a 9B bilingual English/Korean SpeechLM trained on 1M+ hours of curated speech-text data and evaluated across 42 speech and text benchmarks, while Raon-SpeechChat is continually trained on 116K hours of time-aligned dialogue data. It covers ASR, speech generation, spoken QA, audio understanding, and text QA, plus three Korean benchmarks (KVoiceBench, KOpenAudioBench, KMMAU). See [[wiki/01-overview|Overview]].

### Q3. How does Raon-SpeechChat enable real-time full-duplex conversation?
> [!tip]- Answer
> It extends Raon-Speech with causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, and text lookahead. These mechanisms give it strength in turn-taking, backchanneling, interruption handling, overlap robustness, and multi-turn dialogue with pause handling. See [[wiki/01-overview|Overview]].

### Q4. How do you load the models and what distinguishes the two execution modes?
> [!tip]- Answer
> Every entry point accepts a local checkpoint directory or a Hub `repo_id` (e.g. `KRAFTON/Raon-Speech-9B`, `KRAFTON/Raon-SpeechChat-9B`) via `RaonPipeline(..., device="cuda", dtype="bfloat16")`, `bash scripts/infer.sh` / `duplex_infer.sh`, or `AutoModel.from_pretrained(..., trust_remote_code=True)`. With `raon` installed all entry points work (scripts, demos, `from raon import RaonPipeline`), while without install only the Hub-remote-code Gradio demo and pure-Transformers flow work since `python -m raon.*` and the realtime duplex runtime import `raon.*`. See [[wiki/01-overview|Overview]].

### Q5. What SpeechLLM tasks, data format, and pipeline calls does the offline track support?
> [!tip]- Answer
> The offline track supports four channels — `tts`, `stt`, `speech-chat`, `textqa` — with JSONL samples carrying `conversations`, `audios`, optional `speaker_ref_audios`, `channel`, and `system`, evaluated from data under `data/speechllm/eval`. Inference runs via `bash scripts/infer.sh` (defaults from `config/infer.yaml`, `--attn_implementation sdpa` or `fa`) or the pipeline API (`pipe.stt`, `pipe.tts`, `pipe.speech_chat`, `pipe.textqa`, `pipe.tts_continuation`). Streaming TTS is faster than real time at RTF 0.27 / 617 ms TTFT / 135 ms TBT on RTX 6000 Pro Blackwell and RTF 0.45 / 887 ms TTFT / 233 ms TBT on L40S. See [[wiki/01-overview|Overview]].

### Q6. What do the three top-level files define and what must you watch when installing?
> [!tip]- Answer
> The root carries no model logic, only hygiene, attribution, and runtime: a 217-line stock Python `.gitignore` (bytecode, packaging outputs, envs/secrets, coverage/lint/IDE artefacts), a 40-line `NOTICE` crediting Transformers, Qwen3/Qwen3OmniMoe, Mimi codec, SpeechBrain ECAPA-TDNN (all Apache-2.0) plus PyTorch (BSD 3-Clause), and an 18-line 14-package `requirements.txt`. Only five packages are pinned (`accelerate`, `pydantic`, `soundfile`, `transformers>=4.57.1,<5.0`, `datasets`), so `torch`, `torchaudio`, and `speechbrain` float and you must match PyTorch/Torchaudio to your CUDA plus Python >=3.11 yourself. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Your team needs a bilingual English/Korean voice assistant with natural interruption handling and low streaming latency: which track would you recommend and why?
> [!tip]- Answer
> I would recommend Raon-SpeechChat over the offline Raon-Speech track because it is continually trained on 116K hours of time-aligned dialogue specifically for turn-taking, backchanneling, and interruption handling, with streaming TTS at 3.7x real time on a Blackwell-class GPU. The tradeoff is operational cost: you take on the full-duplex training/inference pipeline, `raon_duplex` model type, and stereo dialogue data contract instead of the simpler single-turn STT/TTS calls. See [[wiki/01-overview|Overview]].
