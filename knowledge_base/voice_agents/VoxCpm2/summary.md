# Technical Analysis: OpenBMB/VoxCPM
**Repository:** https://github.com/OpenBMB/VoxCPM
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves
Multilingual text-to-speech must handle timbre control, style/emotion transfer, and high sample-rate output without per-language tokenizers or external vocoders/up samplers. Discrete-token pipelines add quantization error and language-tag plumbing; reference-based cloning systems typically need long prompts or separate enhancement stages.

VoxCPM addresses this with a tokenizer-free architecture that generates continuous speech representations end-to-end via a diffusion autoregressive process (01-overview.md:47). VoxCPM2 instantiates it as a 2B-parameter model on a MiniCPM-4 backbone trained on over 2 million hours of multilingual data, covering 30 languages plus 9 Chinese dialects with no language tag required (01-overview.md:49, 01-overview.md:53-60, 01-overview.md:63-65). Input reference audio is 16 kHz; output is 48 kHz via AudioVAE V2 asymmetric encode/decode with built-in super-resolution (01-overview.md:57). Three synthesis modes cover the control spectrum: Voice Design (new voice from description only), Controllable Cloning (short clip plus optional style guidance), and Ultimate Cloning (reference audio plus transcript continuation preserving timbre, rhythm, emotion, style) (01-overview.md:54-56). Streaming reaches RTF ~0.3 in PyTorch and ~0.13 via Nano-vLLM / vLLM-Omni on RTX 4090 (01-overview.md:59). Weights and code are Apache-2.0 (01-overview.md:60). The primary user is a developer or content producer integrating multilingual TTS, custom-voice creation, or short-clip cloning into an app, CLI batch job, or served endpoint.

## 2. High-Level Architecture
```
text (+ optional description/style prefix)
  │
  ▼
Gradio demos / CLI / Python API ──► VoxCPM.from_pretrained ──► MiniCPM-4 backbone (2B)
  │                                        │                          │
  │ reference wav (16 kHz)                 │ prompt transcript          ▼
  │                                        │ (ASR fallback)      diffusion autoregressive
  │                                        ▼                     core (cfg_value, timesteps)
  │                              iic/SenseVoiceSmall ────────────► AudioVAE V2 ──► 48 kHz wav
  │                                        │                          │
  ▼                                        ▼                          ▼
normalize / denoise flags            Nano-vLLM / vLLM-Omni /        output/ + Gradio playback
                                     llama.cpp-omni serving
```

Data flow:

1. Request assembly. Caller supplies `text` and, depending on mode, a voice description in parentheses, a `reference_wav_path`, or a `prompt_wav_path` plus `prompt_text`. The demo builds this dict in `app.py:275-312` (`_build_generate_kwargs` / `generate_tts_audio`).
2. Transcript recovery. When reference audio lacks a transcript, the demo runs SenseVoiceSmall ASR and strips the tag suffix before passing `prompt_text` (app.py:265-273).
3. Core synthesis. `voxcpm.VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)` loads the MiniCPM-4-based diffusion model; `model.generate(text=..., cfg_value=2.0, inference_timesteps=10, seed=42)` produces the waveform at `model.tts_model.sample_rate` (01-overview.md:113-126, README_zh.md:96-119).
4. Codec rendering. AudioVAE V2 decodes to 48 kHz directly from 16 kHz references with no external upsampler (01-overview.md:57).
5. Delivery. Results return as `(sample_rate, wav)` tuples for Gradio/file output, as streamed chunks via `generate_streaming` concatenated with `np.concatenate` (01-overview.md:206-211), or as 48000 Hz responses from Nano-vLLM / vLLM-Omni production serving (01-overview.md:285-299).
6. Adaptation loop. The LoRA WebUI loads a base checkpoint with an attached `LoRAConfig`, scans `lora/` for `lora_weights.safetensors`, and hot-swaps adapters for inference (lora_ft_webui.py:18-60, lora_ft_webui.py:149-252).

Persistent state lives outside version control and the Docker build context: `models/`, `data/`, `lora/`, `output/` are excluded by both `.dockerignore:1-35` and `.gitignore:1-14`; downloaded weights additionally live under `./pretrained_models/` (`.gitignore:1-14`) or `models/<repo__name>` (app_old.py:36-60, lora_ft_webui.py:18-20). Runtime configuration persists in `config.json:audio_vae_config.sample_rate` (lora_ft_webui.py:104-119) and `lora_config.json:base_model` (lora_ft_webui.py:255-315).

## 3. The Voice-Conditioning Request
The central concept is a single generation request that encodes text plus optional voice conditioning, dispatched to one of three cloning/design behaviors without changing the model call shape.

Representation: a `generate_kwargs` dict with `text`, `reference_wav_path`, `cfg_value`, `inference_timesteps`, `normalize`, `denoise`, `seed`, plus conditional `prompt_wav_path` / `prompt_text` (app.py:275-312). The underlying model object is `voxcpm.VoxCPM` constructed via `from_pretrained`, with output rate read from `model.tts_model.sample_rate` (01-overview.md:113-126, app_old.py:80-113).

Named kinds:

- Voice Design — voice specified only by a natural-language description in parentheses at the start of `text`, e.g. `"(your voice description)The text to synthesize."` (01-overview.md:153-157). No reference audio is passed.
- Controllable Cloning — `text` plus `reference_wav_path`, with an optional style prefix in `text`, plus `cfg_value`, `inference_timesteps`, `seed` (01-overview.md:170-183). Timbre comes from the clip; style is steerable.
- Ultimate Cloning — `text` plus `prompt_wav_path` and `prompt_text`, with optional `reference_wav_path`; passing the same clip in both audio paths maximizes similarity (01-overview.md:191-197). This continues from reference audio plus transcript and reproduces rhythm, emotion, and style (01-overview.md:56).

Key query — kwargs builder (verbatim, `app.py:275-312`):

```python
generate_kwargs = dict(
    text=final_text,
    reference_wav_path=audio_path,
    cfg_value=float(cfg_value_input),
    inference_timesteps=inference_timesteps,
    normalize=do_normalize,
    denoise=denoise,
    seed=seed,
)
if prompt_text_clean and audio_path:
    generate_kwargs["prompt_wav_path"] = audio_path
    generate_kwargs["prompt_text"] = prompt_text_clean
return generate_kwargs
```

Presence or absence of `prompt_text`/`prompt_wav_path` is what switches Controllable versus Ultimate behavior in the demo path.

## 4. LLM / External Service Integration
No remote LLM or paid inference API is called at synthesis time. The "LLM" is the local MiniCPM-4 backbone inside the VoxCPM2 weights (01-overview.md:49, README_zh.md:43). External network use is limited to model-weight download and locally run auxiliary models:

- Providers: Hugging Face Hub (`openbmb/VoxCPM2`, `openbmb/VoxCPM1.5`, `iic/SenseVoiceSmall`) via `snapshot_download` and `VoxCPM.from_pretrained` (app_old.py:36-60, app.py:227-263); ModelScope mirror via `snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2')` (01-overview.md:136-140).
- Required calls: one checkpoint fetch (HF or ModelScope) plus local `VoxCPM.generate` / `generate_streaming`; ASR fetch of `iic/SenseVoiceSmall` for transcript recovery when `prompt_text` is absent (app.py:265-273).
- Optional calls: OpenAI-compatible serving via `vllm serve openbmb/VoxCPM2 --omni --port 8000` with `/v1/audio/speech` (README_zh.md:179-260) — a local server exposing an OpenAI-shaped endpoint, not the OpenAI API.
- Env vars: `HF_REPO_ID` (defaults to `openbmb/VoxCPM1.5` in the legacy demo when empty, app_old.py:11-18). No API keys are documented in the visible wiki portions.

## 5. The Text-to-Speech Synthesis Pipeline
Primary workflow: text (plus optional voice conditioning) to 48 kHz waveform through demo, core model, and optional served_decoder paths.

1. `VoxCPMDemo.__init__` — `app.py:227-263`. Resolves device via `resolve_runtime_device(device, "cuda")`, sets `self.optimize` on CUDA, records `asr_model_id="iic/SenseVoiceSmall"`, and lazily loads `voxcpm.VoxCPM.from_pretrained(self._model_id, optimize, device)`.
2. `VoxCPMDemo.get_or_load_asr_model` + transcript strip — `app.py:265-273`. Runs `asr.generate(input=prompt_wav, language="auto", use_itn=True)` and returns `res[0]["text"].split("|>")[-1]`.
3. `VoxCPMDemo._build_generate_kwargs` — `app.py:275-312`. Assembles the `generate_kwargs` dict above, adding `prompt_wav_path`/`prompt_text` only when a cleaned transcript and audio path coexist.
4. `VoxCPMDemo.generate_tts_audio` — `app.py:275-312` (signature visible to line 312 of 607). Accepts `text_input`, `control_instruction`, `reference_wav_path_input`, `prompt_text`, `cfg_value_input=2.0`, `do_normalize=True`, `denoise=True`, `inference_timesteps=10`, `seed`; returns `(int, np.ndarray, Optional[int])`. Body past the signature is truncated in the chunk.
5. `VoxCPM.from_pretrained` — `app.py:57-62`, `README_zh.md:96-119`, `lora_ft_webui.py:221-252`. Canonical form `VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)`; demo passes `optimize`/`device`; LoRA path additionally passes `lora_config` and `lora_weights_path`.
6. `VoxCPM.generate` — `app_old.py:80-113`, `01-overview.md:113-126`. Takes `text`, `prompt_text`, `prompt_wav_path`, `cfg_value`, `inference_timesteps`, `normalize`, `denoise`; legacy wrapper returns `(current_model.tts_model.sample_rate, wav)`.
7. `VoxCPM.generate_streaming` — `01-overview.md:206-211`. Yields chunks the caller concatenates with `np.concatenate`.
8. Legacy `app_old.py` equivalents — `app_old.py:11-70`. `HF_REPO_ID` defaulting, `resolve_local_model_dir` (local dir check then `snapshot_download` into `models/<repo__name>`), eager `AutoModel` ASR construction, old-style `voxcpm.VoxCPM(voxcpm_model_path=model_dir)`.
9. `lora_ft_webui.run_inference` — `lora_ft_webui.py:255-315` (visible part). Reuses `current_model` when loaded; otherwise resolves base path from UI field, then `lora_config.json:base_model`, then default path; on LoRA rank mismatch reloads from the checkpoint's base model. Training loop and Gradio wiring are past the truncation point.

## 6. Key Files
| File | Lines | What It Does |
|---|---|---|
| `app.py` | 607 (visible through `generate_tts_audio` signature ~312) | Current VoxCPM2 Gradio demo; `VoxCPMDemo`, lazy model/ASR load, kwargs builder, bilingual UI (`app.py:26-312`) |
| `app_old.py` | 288+ (launch at 279-288) | Legacy VoxCPM1.5 demo; HF fallback, eager ASR, `(sample_rate, wav)` return, port 7860 UI (`app_old.py:11-288`) |
| `lora_ft_webui.py` | 1332 (visible through ~315) | LoRA train/infer WebUI; checkpoint preference, sample-rate read, LoRA scan/config, hot-swap inference (`lora_ft_webui.py:18-315`) |
| `README_zh.md` | 260+ visible (version table onward cut) | Chinese README; install, Python API, CLI, demo, Nano-vLLM/vLLM-Omni/llama.cpp-omni paths (`README_zh.md:43-260`) |
| `01-overview.md` (wiki) | 301 (README excerpt, truncated mid-sentence) | Capability matrix, language list, Python/CLI/streaming/deploy quick start (`01-overview.md:47-301`) |
| `.dockerignore` | 27 lines (refs as 1-35) | Excludes `models/ data/ lora/ output/`, `.git/`, caches/venvs, docker/nginx docs, IDE files |
| `.gitignore` | 14 lines | Excludes `launch.json`, `.venv/`, `voxcpm.egg-info`, `./pretrained_models/`, `app_local.py`, `models/ data/ lora/ output/` |
| `config.json` (model config) | referenced at `lora_ft_webui.py:104-119` | Supplies `audio_vae_config.sample_rate` for resampling decisions |
| `lora/lora_weights.safetensors` | scanned at `lora_ft_webui.py:149-218` | LoRA adapter checkpoints discovered by directory walk |
| `lora_config.json` | referenced at `lora_ft_webui.py:255-315` | Stores `base_model` fallback for inference path resolution |
| `models/openbmb__VoxCPM2` / `models/openbmb__VoxCPM1.5` | referenced at `lora_ft_webui.py:18-20` | Preferred local checkpoint dirs, V2 first with V1.5 fallback |
| `examples/example.wav` | referenced at `app_old.py:152-268` | Default prompt-audio upload/mic example for the legacy demo |
| `examples/input.txt` | referenced at `README_zh.md:132-163` | Sample batch input for `voxcpm batch` |
| `docker/docker-compose.yml`, `docker/nginx.conf`, `docker/README.md` | listed in `.dockerignore` | Deploy/docs artifacts excluded from image build context |

## 7. Dependencies
| Package | Version constraint | Purpose |
|---|---|---|
| Python | `≥ 3.10 (<3.13)` | Runtime interpreter range (01-overview.md:99-103) |
| PyTorch | `≥ 2.5.0` | Model execution, CUDA device check (01-overview.md:99-103, app_old.py:11-18) |
| CUDA | `≥ 12.0` | GPU acceleration requirement (01-overview.md:99-103) |
| `voxcpm` | unspecified (installed via `pip install voxcpm`) | Core package: `VoxCPM.from_pretrained`, `generate`, CLI (01-overview.md:99-103) |
| `voxcpm[timestamps]` | unspecified (installed via `pip install "voxcpm[timestamps]"`) | Word/char timestamp support for CLI (01-overview.md:219-266) |
| `nano-vllm-voxcpm` | unspecified (installed via `pip install nano-vllm-voxcpm`) | Production serving path, RTF ~0.13 (01-overview.md:285-299) |
| Gradio (`gr`) | unspecified | Demo UI, `gr.I18n`, `gr.themes.Soft`, Blocks layout (app.py:26-221) |
| NumPy (`numpy` as `np`) | unspecified | Waveform typing/concatenation (`np.ndarray`, `np.concatenate`) (app.py:95-107, 01-overview.md:206-211) |
| SenseVoice (`iic/SenseVoiceSmall` + `AutoModel`) | unspecified (`disable_update=True` in legacy path) | Reference-transcript ASR (app.py:227-273, app_old.py:23-70) |
| `huggingface_hub` (`snapshot_download`) | unspecified | Checkpoint download fallback into `models/` (app_old.py:36-60) |
| ModelScope SDK (`snapshot_download`) | unspecified | Alternate checkpoint mirror into `./pretrained_models/` (01-overview.md:136-140) |
| ZipEnhancer (via denoise prompt flag) | unspecified | Optional prompt-audio enhancement (`DoDenoisePromptAudio`) (app_old.py:236-243) |

## 8. CLI / Usage Surface
Entry points: `voxcpm` CLI, `VoxCPM` Python class, `python app.py` / `python app_old.py` demos, `lora_ft_webui.py` WebUI, `voxcpm2-cli` (llama.cpp-omni), `vllm serve` (vLLM-Omni).

| Command | Key flags / args |
|---|---|
| `voxcpm design --text "..." --output out.wav` | `--control`, `--seed` for description-guided design (01-overview.md:219-266, README_zh.md:132-163) |
| `voxcpm clone --text "..." --reference-audio path/to/voice.wav --output out.wav` | Controllable clone; add `--prompt-audio` + `--prompt-text` for Ultimate mode (01-overview.md:219-266) |
| `voxcpm batch --input examples/input.txt --output-dir outs` | File-driven batch synthesis (README_zh.md:132-163) |
| `voxcpm ... --timestamps --timestamp-level word\|char --timestamp-language en\|zh` | Timestamp output; needs `voxcpm[timestamps]` extra (01-overview.md:219-266) |
| `python app.py --port 8808 --device auto\|cpu\|mps\|cuda\|cuda:N` | Current demo; `auto` uses MPS on Apple Silicon (01-overview.md:272-281, README_zh.md:168-177) |
| `python app_old.py` (via `run_demo`) | Legacy demo on `localhost:7860`, queue `max_size=10, default_concurrency_limit=1` (app_old.py:279-288) |
| `voxcpm2-cli -t/-o/-r/--prompt-wav/--prompt-text/--cfg/--timesteps/--seed/--temperature/--stream` | On-device llama.cpp-omni CLI (README_zh.md:179-260) |
| `vllm serve openbmb/VoxCPM2 --omni --port 8000` | Served `/v1/audio/speech` endpoint (README_zh.md:179-260) |

Python API defaults: `VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)`; `generate(text=..., cfg_value=2.0, inference_timesteps=10, seed=42)`; `generate_streaming(text=...)` with `np.concatenate` (01-overview.md:113-126, 01-overview.md:206-211). Voice Design passes the description parenthesized at the start of `text` (01-overview.md:153-157).

| Env var | Default / effect |
|---|---|
| `HF_REPO_ID` | Empty means `openbmb/VoxCPM1.5` in `app_old.py:11-18`; selects Hub repo for snapshot download into `models/<repo__name>` |

| Config | Keys / effect |
|---|---|
| `config.json` | `audio_vae_config.sample_rate` determines resampling rate (lora_ft_webui.py:104-119) |
| `lora_config.json` | `base_model` fallback when UI field is empty (lora_ft_webui.py:255-315) |
| `LoRAConfig` | `enable_lm=True, enable_dit=True, r=32, alpha=16, target_modules_lm/dit=["q_proj","v_proj","k_proj","o_proj"]` (lora_ft_webui.py:149-218) |
| Gradio launch | `server_name="localhost"`, `server_port=7860`, queue limits (legacy); `--port 8808`, `--device` (current) |

## 9. Extensibility Points
- New synthesis mode or conditioning logic: extend `VoxCPMDemo._build_generate_kwargs` and `generate_tts_audio` in `app.py:275-312`; the conditional injection of `prompt_wav_path`/`prompt_text` is the mode switch.
- Device and optimization policy: modify `VoxCPMDemo.__init__` device resolution (`resolve_runtime_device`) and `self.optimize` flag in `app.py:227-263`; legacy path hard-codes `cuda`-if-available in `app_old.py:11-18`.
- ASR replacement: swap the `iic/SenseVoiceSmall` model ID and the `split("|>")` tag-strip in `app.py:265-273`, or the eager `AutoModel(...)` block in `app_old.py:23-70`.
- Checkpoint sourcing: change `default_pretrained_path` preference (`models/openbmb__VoxCPM2` vs `VoxCPM1.5`) in `lora_ft_webui.py:18-20` or the local-dir-then-`snapshot_download` order in `app_old.py:36-60`.
- Adapter coverage: adjust `LoRAConfig` (`enable_lm`, `enable_dit`, `r`, `alpha`, `target_modules_lm/dit`) constructed in `lora_ft_webui.py:149-218` and threaded through `VoxCPM.from_pretrained(..., lora_config=..., lora_weights_path=...)` in `lora_ft_webui.py:221-252`.
- UI/localization: add strings to the inline `en` + `zh-CN` dict (with `zh-Hans`/`zh` aliases) wired through `gr.I18n` in `app.py:26-160`, or widgets in `create_demo_interface` in `app_old.py:152-268`.
- Served deployment: add a backend alongside the Nano-vLLM (`VoxCPM.from_pretrained(model=..., devices=[0])` + `generate(target_text=...)`), vLLM-Omni, and llama.cpp-omni paths in `01-overview.md:285-299` / `README_zh.md:179-260`.

## 10. Limitations and Gotchas
- **Wiki coverage is truncated; several bodies are unverified.** `app.py` stops at the `generate_tts_audio` signature (~312/607), `lora_ft_webui.py` stops mid-`run_inference` (~315/1332), `README_zh.md` stops before the version/model table, and the production-serving sentence cuts off mid-link at `01-overview.md:301` — claims about Blocks layout, training loop, and batching behavior rest only on the visible portions (02-top-level-files.md:16, 01-overview.md:285-301).
- **Python ceiling excludes 3.13+.** Requirement is `Python ≥ 3.10 (<3.13)` with `PyTorch ≥ 2.5.0` and `CUDA ≥ 12.0` (01-overview.md:99-103); newer interpreters are out of the documented range.
- **Character timestamps are best-effort.** Derived from word alignment rather than independent char alignment (01-overview.md:257), and timestamp CLI use needs the separate `pip install "voxcpm[timestamps]"` extra (01-overview.md:219-266).
- **Sample-rate asymmetry is load-bearing.** References are 16 kHz while output is 48 kHz via AudioVAE V2 (01-overview.md:57); feeding other rates without the `config.json:audio_vae_config.sample_rate` resampling read (lora_ft_webui.py:104-119) risks quality or shape errors.
- **Legacy and current demos diverge silently.** `app.py` lazily loads models with `optimize` on CUDA and passes `seed`/`normalize=True`/`denoise=True` defaults (app.py:227-312), while `app_old.py` eagerly constructs ASR, uses the old `VoxCPM(voxcpm_model_path=...)` constructor, defaults normalization and denoise to False, and returns no seed (app_old.py:23-113, app_old.py:228-243). Copying flags between them changes output.
- **LoRA rank mismatch forces a reload.** `run_inference` detects model-rank versus checkpoint-rank mismatch and reloads from the checkpoint's base model (lora_ft_webui.py:255-315); hot-swap is not free when ranks differ.

## 11. How It Compares to Alternatives
- MiniCPM-4 (https://github.com/OpenBMB/MiniCPM): the backbone VoxCPM2 builds on (01-overview.md:49, README_zh.md:43). Using it directly would mean a text LLM without the diffusion-autoregressive speech head and AudioVAE V2 codec; VoxCPM is the speech-specialized derivative.
- SenseVoiceSmall (`iic/SenseVoiceSmall`): the auxiliary ASR used for transcript recovery (app.py:227-273, app_old.py:23-70). It is a complement, not a TTS competitor — VoxCPM depends on it when `prompt_text` is missing.
- Nano-vLLM (`nano-vllm-voxcpm`) / vLLM-Omni: served-inference options for the same weights, trading plain-PyTorch simplicity (RTF ~0.3) for PagedAttention throughput (RTF ~0.13) and an OpenAI-compatible API (01-overview.md:59, 01-overview.md:285-299, README_zh.md:179-260).
- llama.cpp-omni (`voxcpm2-cli`): the on-device/CLI alternative to server GPUs, exposing `-t/-o/-r/--prompt-wav/--prompt-text/--cfg/--timesteps/--seed/--temperature/--stream` flags for local execution (README_zh.md:179-260).

Positioning: VoxCPM2 competes as a tokenizer-free, end-to-end 48 kHz multilingual synthesizer with description-driven voice design and two tiers of reference cloning, where the cited alternatives are its backbone, its ASR helper, and its three serving runtimes rather than independent TTS models.

## Appendix: Selected Code Snippets
1. Demo construction and lazy load (`app.py:227-263`):

```python
class VoxCPMDemo:
    def __init__(self, model_id: str = "openbmb/VoxCPM2", device: str = "auto") -> None:
        self.device = resolve_runtime_device(device, "cuda")
        logger.info(f"Running VoxCPM on device: {self.device}")
        self.optimize = self.device.startswith("cuda")

        self.asr_model_id = "iic/SenseVoiceSmall"
        self.asr_device = "cuda:0" if self.device.startswith("cuda") else "cpu"
```

```python
self.voxcpm_model = voxcpm.VoxCPM.from_pretrained(
    self._model_id,
    optimize=self.optimize,
    device=self.device,
)
```

2. ASR tag strip (`app.py:265-273`):

```python
res = self.get_or_load_asr_model().generate(
    input=prompt_wav,
    language="auto",
    use_itn=True,
)
return res[0]["text"].split("|>")[-1]
```

3. Legacy checkpoint resolution (`app_old.py:36-60`):

```python
if os.path.isdir(self.default_local_model_dir):   # "./models/VoxCPM1.5"
    return self.default_local_model_dir
repo_id = os.environ.get("HF_REPO_ID", "").strip()
...
target_dir = os.path.join("models", repo_id.replace("/", "__"))
snapshot_download(repo_id=repo_id, local_dir=target_dir, local_dir_use_symlinks=False)
```

4. LoRA default config and load (`lora_ft_webui.py:149-252`):

```python
return LoRAConfig(
    enable_lm=True,
    enable_dit=True,
    r=32,
    alpha=16,
    target_modules_lm=["q_proj", "v_proj", "k_proj", "o_proj"],
    target_modules_dit=["q_proj", "v_proj", "k_proj", "o_proj"],
)
```

```python
current_model = VoxCPM.from_pretrained(
    hf_model_id=pretrained_path,
    load_denoiser=False,
    optimize=False,
    lora_config=lora_config,
    lora_weights_path=lora_weights_path,
)
```
