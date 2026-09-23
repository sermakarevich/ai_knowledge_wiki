# Technical Analysis: herimor/voxtream

**Repository:** https://github.com/herimor/voxtream
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Zero-shot text-to-speech must clone an unseen voice from a short prompt while delivering audio with low latency and controllable prosody. Offline models buffer full utterances before emitting audio; fixed-rate streaming models cannot change speaking rate once generation starts, and cross-lingual voice prompts often degrade because the prompt transcript biases the acoustic model.

Voxtream (VoXtream2) addresses this as a full-stream zero-shot TTS model with dynamic speaking-rate control updatable mid-utterance (01-overview.md:3,01-overview.md:14). Rate control is implemented with distribution matching and classifier-free guidance for fine-grained adjustment during generation (01-overview.md:15,01-overview.md:24). Translingual prompting is supported by prompt text masking, allowing acoustic prompts in any language (01-overview.md:17,01-overview.md:26). Reported streaming performance is 4x faster than real-time with 74 ms first-packet latency in full-stream on a consumer GPU, 63 ms when compiled (01-overview.md:16,01-overview.md:25,01-overview.md:170-174).

The primary user is a developer integrating streaming voice synthesis into an interactive application (voice agent, dubbing/live narration, demo or websocket service), operating via CLI (`voxtream`), Python API (`SpeechGenerator.generate_stream`), Gradio demo (`voxtream-app`), or websocket server (`voxtream-server`) (01-overview.md:87-91,01-overview.md:117-138,01-overview.md:143-154).

## 2. High-Level Architecture

```text
prompt wav (3-10 s) ─► prompt preprocessing / enhancement ─► acoustic prompt cache ─┐
                                                                                    │
text (<=1000 chars) ─► text_generator / phonemizer (eSpeak NG) ─► text tokens ─► SynkAttention + Depth Transformer ─► Mimi codec frames ─► audio chunks ─► .wav / websocket / playback
                                                                                    ▲
speaking-rate schedule (syll/sec, e.g. repeat(2.0)) ─► speaking_rate.json ───────────┘
                                                                                    │
configs/generator.json + configs/speaking_rate.json ─► SpeechGenerator ──────────────┘

CLI (voxtream) │ Python API │ voxtream-app (Gradio) │ voxtream-server + client.py │ voxtream-benchmark
                                                              ▼
                                              local weights + HF dataset cache + ./experiments
```

Data flow:

1. Inputs are validated and normalized: prompt audio trimmed to max 20 s (target 3-10 s), text trimmed to max 1000 chars, optional speaking rate in syllables per second (01-overview.md:44-53).
2. `SpeechGenerator(config, spk_rate_config)` is constructed from `configs/generator.json` and `configs/speaking_rate.json`; first run downloads weights and warms up the model graph (01-overview.md:106-114,01-overview.md:52).
3. Text passes through `text_generator(...)` and the eSpeak NG phonemizer dependency; the acoustic prompt is optionally enhanced (`--prompt-enhancement`) and encoded into the SynkAttention cache (01-overview.md:24-35,01-overview.md:73-79,01-overview.md:130-134).
4. The autoregressive loop emits codec frames in either output-streaming (no rate control) or full-streaming (rate-controlled) mode; the rate schedule (e.g. `repeat(2.0)`) can vary mid-utterance via distribution matching and classifier-free guidance (01-overview.md:15,01-overview.md:63-70,01-overview.md:118-138).
5. The caller concatenates `audio_frame` chunks (`np.concatenate(audio_frames)`) and writes them at `config.mimi_sr` to wav, streams them over websocket for immediate playback, or measures them in `voxtream-benchmark` for RTF/FPL (01-overview.md:124-137,01-overview.md:147-154,01-overview.md:168-174).
6. Training and evaluation run offline: `train.py` in a devcontainer auto-downloads ~80 Gb of data to the HF cache and writes results to `./experiments`; metric reproduction is documented in `voxtream/utils/test/README.md` (01-overview.md:157-165,01-overview.md:154).

Persistent state lives on the local filesystem: downloaded model weights, HF dataset cache, `configs/*.json`, `assets/*.wav|*.csv`, and `./experiments` outputs. There is no database or remote state. Ephemeral runtime state is the SynkAttention prompt cache (subject to a 2026/04/30 cache-reset fix) and the caller-side frame list; `.gitignore` explicitly excludes `experiments/`, `assets/audio/*.npy`, `assets/benchmark/*.npy`, and `wavlm-large/` from version control (01-overview.md:19-22,02-top-level-files.md:13-27).

## 3. The Streaming Speech Generator

The central concept is the configured streaming generator: a `SpeechGenerator` bound to a generator config and a speaking-rate config, producing an iterator of `(audio_frame, metadata)` chunks from `(prompt_audio_path, text, speaking_rate)`.

Representation: `SpeechGeneratorConfig(**json.load(f))` loaded from `configs/generator.json`, plus `spk_rate_config` from `configs/speaking_rate.json`; synthesis output sample rate is `config.mimi_sr` (01-overview.md:106-114,01-overview.md:125). Generation modes are output-streaming (no rate control) and full-streaming (rate-controlled, `--full-stream` / `speaking_rate=repeat(2.0)`) (01-overview.md:63-70,01-overview.md:118-138).

Named kinds/types with file:line:

- `SpeechGenerator` in `voxtream/generator.py` — constructed as `SpeechGenerator(config, spk_rate_config)` (01-overview.md:104,01-overview.md:114,01-overview.md:177)
- `SpeechGeneratorConfig` in `voxtream/generator.py` — carries `mimi_sr` and `frame_repeat_counter` (recommended 12-25, added 2026/04/08 to reduce stuck-frame hallucinations) (01-overview.md:20-21,01-overview.md:104,01-overview.md:125)
- `generate_stream(prompt_audio_path=..., text=..., speaking_rate=...)` in `voxtream/generator.py` — returns iterable of `(audio_frame, _)` chunks (01-overview.md:119-134,01-overview.md:140)
- `text_generator(...)` and `set_seed()` in `voxtream/utils/generator.py` — text preparation and determinism (01-overview.md:100-107,01-overview.md:140)
- Acoustic prompt cache in SynkAttention — reset fix 2026/04/30 for noise from invalid prompt cache (01-overview.md:20)

Key query (verbatim, 01-overview.md:117-137): the canonical way to inspect generator behavior is to iterate the stream and concatenate:

```python
speech_stream = speech_generator.generate_stream(
    prompt_audio_path=Path('assets/audio/english_female.wav'),
    text=text_generator("Staff do not always do enough to prevent violence."),
    speaking_rate=repeat(2.0),
)

audio_frames = [audio_frame for audio_frame, _ in speech_stream]
sf.write('full_stream_2sps.wav', np.concatenate(audio_frames), config.mimi_sr)
```

## 4. LLM / External Service Integration

The repository calls no LLM or external inference API. All synthesis is local PyTorch inference after a one-time weight download and graph warmup (01-overview.md:52,01-overview.md:75-77). The only network-adjacent operations documented are local weight/dataset fetching (first-run weights download; training dataset auto-download to HF cache) and the self-hosted `voxtream-server` websocket transport with `voxtream/client.py` playback (01-overview.md:147-154,01-overview.md:157-164). No provider keys or LLM env vars are documented. Required system dependency is eSpeak NG as phonemizer (`apt-get install espeak-ng` / `yum install espeak-ng` / `brew install espeak-ng`) (01-overview.md:24-35). Optional runtime additions are acoustic prompt enhancement (`--prompt-enhancement`, +2 Gb VRAM) and compiled inference (`--compile` in `voxtream-benchmark`) (01-overview.md:49,01-overview.md:73-79,01-overview.md:168).

## 5. Prompt-Conditioned Streaming Synthesis Pipeline

1. Install prerequisites with `apt-get install espeak-ng` (Debian) in `README.md:45-56` — provides the phonemizer backend required before any synthesis (01-overview.md:24-35).
2. Install package with `pip install "voxtream>=0.2.3"` in `README.md:63-64` — pins the 0.2.x inference entry points (01-overview.md:36-39).
3. Seed RNG with `set_seed()` in `voxtream/utils/generator.py:107` — establishes deterministic generation (01-overview.md:100-107).
4. Load `SpeechGeneratorConfig(**json.load(f))` from `configs/generator.json` in `voxtream/utils/generator.py:108-109` — binds model, codec (`mimi_sr`), and `frame_repeat_counter` settings (01-overview.md:106-110).
5. Load `spk_rate_config` from `configs/speaking_rate.json` in `voxtream/utils/generator.py:111-112` — binds rate-control schedule (01-overview.md:111-112).
6. Construct `SpeechGenerator(config, spk_rate_config)` in `voxtream/generator.py:114` — downloads weights and warms up the graph on first run (01-overview.md:114,01-overview.md:52).
7. Prepare text with `text_generator(...)` in `voxtream/utils/generator.py:133` — wraps raw text for the full-stream path (plain string accepted in output-streaming path) (01-overview.md:119-134).
8. Invoke `generate_stream(prompt_audio_path=..., text=..., speaking_rate=...)` in `voxtream/generator.py:119-134` — output-streaming omits `speaking_rate`; full-streaming passes `speaking_rate=repeat(2.0)` adjustable mid-utterance (01-overview.md:118-138).
9. Drain iterator with `[audio_frame for audio_frame, _ in speech_stream]` in caller code `:124,136` — collects codec-decoded chunks (01-overview.md:124,01-overview.md:136).
10. Write `sf.write(path, np.concatenate(audio_frames), config.mimi_sr)` in caller code `:125,137` — materializes the stream to wav (01-overview.md:125,01-overview.md:137).
11. Serve or measure via `voxtream-app` in `voxtream/app.py:170-171`, `voxtream-server` plus `python voxtream/client.py` in `voxtream/server.py:179-187`, or `voxtream-benchmark [--compile]` in `voxtream/benchmark.py:221` for RTF/FPL (01-overview.md:143-154,01-overview.md:168-174).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | model statement, features, updates, install, usage, training, benchmark | Primary specification for VoXtream2 behavior and contracts |
| `voxtream/generator.py` | `SpeechGenerator`, `SpeechGeneratorConfig`, `generate_stream` | Core streaming synthesis abstraction |
| `voxtream/utils/generator.py` | `set_seed`, `text_generator` | Text preparation and RNG seeding for the pipeline |
| `voxtream/client.py` | websocket client playback path | Sends prompt path + text, plays output stream immediately |
| `voxtream/train.py` | `batch_size`, `GPU_IDS` launch | Training entry point run inside devcontainer |
| `configs/generator.json` | generator hyperparameters incl. `mimi_sr`, `frame_repeat_counter` | Static inference configuration |
| `configs/speaking_rate.json` | rate-control hyperparameters | Static speaking-rate configuration |
| `voxtream/utils/test/README.md` | evaluation metric reproduction | Defines how reported metrics are reproduced |
| `voxtream/utils/dataset/README.md` | custom dataset preparation | Defines training data contract |
| `.devcontainer/docker-compose.yaml` | `voxtream` service build/run | Reproducible training container |
| `requirements.txt` | ~331-353 pinned stack | Training/inference/demo dependency manifest |
| `MANIFEST.in` | 301-306 include rules | Packaging list for README, VERSION, assets, configs |
| `ATTRIBUTION.md` | 51-64 dataset attribution | CC BY 4.0 credit for Emilia and HiFiTTS-2 weights basis |
| `NOTICE` | 312-316 Depth Transformer credit | Attributes SesameAI component under Apache 2.0 |
| `assets/audio/` | prompt wav fixtures | Sample acoustic prompts (e.g. english_male/female) |
| `voxtream/VERSION` | version marker packaged by MANIFEST.in | Single source of packaged version |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `torch` | `>=2.4,<2.9` | Model inference and training tensor runtime |
| `torchaudio` | `>=2.4,<2.9` | Audio I/O and preprocessing |
| `torchtune` | `==0.4.0` | Transformer training recipes |
| `torchao` | `==0.9.0` | Quantization/optimization for torch |
| `lightning` | `==2.4.0` | Training loop orchestration |
| `transformers` | `==4.50.0` | Pretrained model/tokenizer utilities |
| `moshi` | `>=0.2.13` | Streaming audio codec (Mimi) lineage |
| `huggingface_hub` | `==0.28.1` | Weight/dataset download and caching |
| `hydra-core` | `==1.3.2` | Training configuration (`train.py batch_size=...`) |
| `gradio` | `==4.44.1` | Interactive demo (`voxtream-app`) |
| `gradio_client` | `==1.3.0` | Demo client support |
| `openai-whisper` | `==20250625` | ASR utility (evaluation/transcription) |
| `silero-vad` | `==6.2.0` | Voice activity detection for audio handling |
| `espeak-ng` (system) | unpinned OS package | Phonemizer backend required before pip install works |
| `black` (pre-commit) | `25.9.0` | Formatting hook |
| `isort` (pre-commit) | `6.0.1` | Import sorting hook |
| `ruff` (pre-commit) | `v0.13.1` | Lint hook (`--fix --exit-non-zero-on-fix`) |
| `mypy` (pre-commit) | `v1.18.2` | Type-checking hook |

## 8. CLI / Usage Surface

Entry points (01-overview.md:87-91,01-overview.md:143-158,01-overview.md:168-187,01-overview.md:199-215):

- `voxtream` — file synthesis, output-streaming and full-streaming
- `voxtream-app` — interactive Gradio demo with dynamic rate control
- `voxtream-server` + `python voxtream/client.py` — websocket synthesis with immediate playback
- `voxtream-benchmark` — RTF/FPL measurement
- `python voxtream/train.py` (via docker-compose) — training

Commands:

```bash
voxtream --prompt-audio assets/audio/english_male.wav --text "..." --output "output_stream.wav"
voxtream --prompt-audio assets/audio/english_female.wav --text "..." --output "full_stream_2sps.wav" --full-stream --spk-rate 2.0
voxtream --prompt-audio assets/test/english_male.wav --text "..." --output "output_enhanced.wav" --prompt-enhancement
voxtream-app
voxtream-server
python voxtream/client.py
voxtream-benchmark [--compile]
GPU_IDS=0,1 docker-compose -f .devcontainer/docker-compose.yaml run voxtream python voxtream/train.py batch_size=12
```

| CLI flag | Meaning |
|---|---|
| `--prompt-audio` | Path to prompt wav (3-10 s ideal, max 20 s trimmed) |
| `--text` | Text to synthesize (max 1000 chars trimmed) |
| `--output` | Output wav path |
| `--full-stream` | Enable full streaming mode |
| `--spk-rate` | Target speaking rate in syllables/sec (e.g. `2.0`) |
| `--prompt-enhancement` | Enable acoustic prompt enhancement (+2 Gb VRAM) |
| `--compile` (benchmark) | Compile model for faster inference at cost of compile time |

| Env var / config | Role |
|---|---|
| `GPU_IDS` | Container-visible GPUs for `train.py` launch |
| `batch_size` | Training batch size (default 64 on H200; 12 fits RTX3090) |
| `configs/generator.json` | `SpeechGeneratorConfig` incl. `mimi_sr`, `frame_repeat_counter` (12-25) |
| `configs/speaking_rate.json` | `spk_rate_config` for rate-control schedule |
| `speaking_rate` / `repeat(2.0)` (Python) | Per-call rate schedule, variable mid-utterance |

## 9. Extensibility Points

- New speaking-rate policy: pass a different `speaking_rate` iterable to `SpeechGenerator.generate_stream` in `voxtream/generator.py`; tune defaults in `configs/speaking_rate.json` (01-overview.md:129-134).
- Hallucination/stability tuning: adjust `frame_repeat_counter` (12-25) in `SpeechGeneratorConfig` / `configs/generator.json` (01-overview.md:20-21).
- Prompt conditioning: modify prompt preprocessing or enhancement path behind `--prompt-enhancement` in `voxtream/generator.py` and translingual masking behavior (01-overview.md:17,01-overview.md:73-79).
- Transport and UX: extend `voxtream/client.py` + server entry (`voxtream-server`) for new streaming protocols, or the Gradio app behind `voxtream-app` for new controls (01-overview.md:143-154).
- Training data: follow `voxtream/utils/dataset/README.md` to add a custom dataset for `voxtream/train.py` (01-overview.md:165,01-overview.md:157-164).
- Evaluation: add metrics under `voxtream/utils/test/README.md` workflow (01-overview.md:154).
- Packaging: extend `MANIFEST.in` includes and `requirements.txt` pins for new assets or dependencies (02-top-level-files.md:66-89).

## 10. Limitations and Gotchas

- **Silent input truncation:** prompt audio longer than 20 s and text longer than 1000 chars are trimmed, and generation caps at 1 minute — long-form input loses content without error (01-overview.md:44-53).
- **VRAM and stack brittleness:** 2.2 Gb required (+2 Gb with enhancement); tested only on Ubuntu 22.04 / CUDA 12 / PyTorch 2.4, with known CUDAGraphs issues tracked in `https://github.com/herimor/voxtream/issues/8` (01-overview.md:49-53).
- **First-run cost:** weights download plus model graph warmup delays initial synthesis; benchmark `--compile` further trades startup time for lower FPL/RTF (01-overview.md:52,01-overview.md:168).
- **Stuck-frame hallucinations:** streaming loop can repeat frames; mitigation is the `frame_repeat_counter` heuristic (12-25), not a structural fix (01-overview.md:20-21).
- **Training hardware floor:** dataset auto-downloads ~80 Gb to HF cache, loads into RAM (~80 Gb RAM per GPU), default `batch_size=64` targets H200 with 12 as the RTX3090 fallback; results only land in local `./experiments` (01-overview.md:157-164).
- **Missing finetuning path:** finetuning instructions are an open TODO, and misuse (non-consensual voice cloning) is explicitly disclaimed (01-overview.md:175).

## 11. How It Compares to Alternatives

- **Coqui XTTS v2:** zero-shot multilingual voice cloning with strong speaker similarity, but file-oriented synthesis without Voxtream's mid-utterance speaking-rate schedule or 74 ms full-stream first-packet path.
- **Microsoft VALL-E / VALL-E X:** prompt-conditioned neural codec TTS establishing the zero-shot paradigm including translingual prompts, but research-oriented and non-streaming versus Voxtream's 4x real-time streaming loop.
- **Suno Bark:** fine-grained prosody and non-speech vocalization control in an offline generation model, without Voxtream's low-latency streaming or syllables-per-second rate interface.
- **F5-TTS / E2-TTS family:** fast non-autoregressive diffusion/flow synthesis with naturalness focus, but fixed-rate utterance generation rather than dynamically adjustable streaming rate.

Positioning: Voxtream occupies the interactive-streaming niche — sub-100 ms first-packet, mid-utterance rate control, and translingual acoustic prompting — trading long-form capacity (1-minute cap, input trimming) and training accessibility for live controllable synthesis.

## Appendix: Selected Code Snippets

1. Output-streaming CLI (`README.md:87-91`, via 01-overview.md:55-62):

```bash
voxtream \
    --prompt-audio assets/audio/english_male.wav \
    --text "In general, some method is then needed to evaluate each approximation." \
    --output "output_stream.wav"
```

2. Full-streaming CLI with fixed rate (`README.md:95-101`, via 01-overview.md:63-71):

```bash
voxtream \
    --prompt-audio assets/audio/english_female.wav \
    --text "Staff do not always do enough to prevent violence." \
    --output "full_stream_2sps.wav" \
    --full-stream \
    --spk-rate 2.0
```

3. Python streaming API (`README.md:117-138`, via 01-overview.md:91-138):

```python
speech_generator = SpeechGenerator(config, spk_rate_config)

# Output streaming, no speaking rate control
speech_stream = speech_generator.generate_stream(
    prompt_audio_path=Path('assets/audio/english_male.wav'),
    text="In general, however, some method is then needed to evaluate each approximation.",
)

audio_frames = [audio_frame for audio_frame, _ in speech_stream]
sf.write('output_stream.wav', np.concatenate(audio_frames), config.mimi_sr)


# Full streaming & fixed speaking rate control (2 syllables per second)
speech_stream = speech_generator.generate_stream(
    prompt_audio_path=Path('assets/audio/english_female.wav'),
    text=text_generator("Staff do not always do enough to prevent violence."),
    speaking_rate=repeat(2.0),
)

audio_frames = [audio_frame for audio_frame, _ in speech_stream]
sf.write('full_stream_2sps.wav', np.concatenate(audio_frames), config.mimi_sr)
```

4. Packaging includes (`MANIFEST.in:301-306`, via 02-top-level-files.md:66-74):

```text
include README.md
include voxtream/VERSION
include requirements.txt
recursive-include assets *.wav
recursive-include assets *.csv
recursive-include configs *.json
```
