> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Top-Level Files

**In one sentence:** The repo root exposes the user-facing entry points — a VoxCPM2 Gradio demo (`app.py`), a legacy VoxCPM1.5 demo (`app_old.py`), a LoRA fine-tune/inference WebUI (`lora_ft_webui.py`), the Chinese README, and ignore rules that keep weights/data out of Docker and git.

## Key points

- `.dockerignore` (27 lines) excludes runtime weight/data dirs (`models/`, `data/`, `lora/`, `output/`), `.git/`, Python caches/venvs, Docker compose/nginx docs, and IDE files from the image build context (`.dockerignore:1-35`).
- `.gitignore` (14 lines) ignores `launch.json`, `.venv/`, `voxcpm.egg-info`, `./pretrained_models/`, `app_local.py`, plus the same large user-specific dirs `models/`, `data/`, `lora/`, `output/` (`.gitignore:1-14`).
- `app.py` is the current VoxCPM2 Gradio demo: `VoxCPMDemo(model_id="openbmb/VoxCPM2", device="auto")` resolves the runtime device, lazily loads `voxcpm.VoxCPM` and a `iic/SenseVoiceSmall` ASR model, and synthesizes via `generate_tts_audio` with defaults `cfg_value=2.0`, `inference_timesteps=10`, `normalize=True`, `denoise=True` (`app.py:227-312`).
- `app.py` ships inline bilingual UI strings (`en` + `zh-CN`, with `zh-Hans`/`zh` aliased to `zh-CN`) wired through `gr.I18n`, covering the three modes — Voice Design, Controllable Cloning, Ultimate Cloning — plus CFG/steps/seed/denoise/normalize labels (`app.py:26-160`).
- `app_old.py` is the legacy VoxCPM1.5 demo: it defaults `HF_REPO_ID` to `openbmb/VoxCPM1.5`, eagerly loads SenseVoiceSmall, resolves a local checkpoint dir with HF-download fallback, and returns `(sample_rate, wav)` from `generate_tts_audio` (`app_old.py:11-113`).
- `lora_ft_webui.py` is a bilingual (en/zh) LoRA training + inference WebUI that prefers `models/openbmb__VoxCPM2` (falling back to `models/openbmb__VoxCPM1.5`), reads the resampling rate from `config.json:audio_vae_config.sample_rate`, scans `lora/` for `lora_weights.safetensors`, and supports LoRA hot-swapping with rank-mismatch reload (`lora_ft_webui.py:18-60`).
- `README_zh.md` documents install (`pip install voxcpm`), Python API (`VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)` + `generate(cfg_value=2.0, inference_timesteps=10, seed=42)`), CLI (`voxcpm design/clone/batch`), Web Demo (`python app.py --port 8808 --device auto`), and Nano-vLLM / vLLM-Omni / llama.cpp-omni deployment paths (`README_zh.md:96-260`).
- Truncation notice: the chunk cuts `app.py` just after the `generate_tts_audio` signature (~line 312 of 607), `lora_ft_webui.py` mid-`run_inference` (~line 315 of 1332), and `README_zh.md` mid version/model table — claims above cover only the visible portions.

---

## Ignore rules (.dockerignore, .gitignore)

Both files keep the same four heavy dirs out of builds and version control:

```python
# .dockerignore:1-5 / .gitignore:8-13
models/
data/
lora/
output/
```

Full listing:

| file | entries |
|---|---|
| `.dockerignore` (`.dockerignore:1-35`) | `models/ data/ lora/ output/`, `.git/`, `__pycache__/ *.pyc *.pyo *.egg-info/ .venv/ venv/ .venv-bench/`, `docker/docker-compose.yml docker/nginx.conf docker/README.md`, `.DS_Store .vscode/` |
| `.gitignore` (`.gitignore:1-14`) | `launch.json`, `.venv/`, `__pycache__`, `voxcpm.egg-info`, `.DS_Store`, `./pretrained_models/`, `app_local.py`, `models/ data/ lora/ output/` |

`.gitignore`-only entries (`launch.json`, `./pretrained_models/`, `app_local.py`, `voxcpm.egg-info`) are local-dev artifacts with no Docker equivalent in the chunk.

## Current demo (app.py)

Entry class and lazy model loading (verbatim, `app.py:227-263`):

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

Generation kwargs builder and TTS signature (verbatim, `app.py:275-312`):

```python
def _build_generate_kwargs(
    self,
    *,
    final_text: str,
    audio_path: Optional[str],
    prompt_text_clean: Optional[str],
    cfg_value_input: float,
    do_normalize: bool,
    denoise: bool,
    inference_timesteps: int = 10,
    seed: Optional[int] = None,
) -> dict:
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

```python
def generate_tts_audio(
    self,
    text_input: str,
    control_instruction: str = "",
    reference_wav_path_input: Optional[str] = None,
    prompt_text: str = "",
    cfg_value_input: float = 2.0,
    do_normalize: bool = True,
    denoise: bool = True,
    inference_timesteps: int = 10,
    seed: Optional[int] = None,
) -> Tuple[int, np.ndarray, Optional[int]]:
```

Reference-transcript ASR strips the SenseVoice tag (verbatim, `app.py:265-273`):

```python
res = self.get_or_load_asr_model().generate(
    input=prompt_wav,
    language="auto",
    use_itn=True,
)
return res[0]["text"].split("|>")[-1]
```

UI chrome in the visible portion: `gr.themes.Soft(primary_hue="blue", secondary_hue="gray", neutral_hue="slate", font=[GoogleFont("Inter"), "Arial", "sans-serif"])` plus custom toggle-switch CSS (`app.py:166-221`); default target text is `"VoxCPM2 is a creative multilingual TTS model from ModelBest, designed to generate highly realistic speech."` (`app.py:162-164`). The remainder of `generate_tts_audio` and the Blocks layout are cut in the chunk (file has 607 lines; chunk stops at the signature).

## Legacy demo (app_old.py)

HF default and device selection (verbatim, `app_old.py:11-18`):

```python
if os.environ.get("HF_REPO_ID", "").strip() == "":
    os.environ["HF_REPO_ID"] = "openbmb/VoxCPM1.5"
```

```python
self.device = "cuda" if torch.cuda.is_available() else "cpu"
```

Model-dir resolution order — local dir, then HF snapshot download, then `models` fallback (verbatim, `app_old.py:36-60`):

```python
if os.path.isdir(self.default_local_model_dir):   # "./models/VoxCPM1.5"
    return self.default_local_model_dir
repo_id = os.environ.get("HF_REPO_ID", "").strip()
...
target_dir = os.path.join("models", repo_id.replace("/", "__"))
snapshot_download(repo_id=repo_id, local_dir=target_dir, local_dir_use_symlinks=False)
```

Unlike `app.py`, ASR is constructed eagerly in `__init__` and the TTS model via the old constructor (`app_old.py:23-70`):

```python
self.asr_model: Optional[AutoModel] = AutoModel(
    model=self.asr_model_id,   # "iic/SenseVoiceSmall"
    disable_update=True,
    log_level="DEBUG",
    device="cuda:0" if self.device == "cuda" else "cpu",
)
self.voxcpm_model = voxcpm.VoxCPM(voxcpm_model_path=model_dir)
```

Generation returns a plain `(sample_rate, wav)` pair with no seed passthrough (verbatim, `app_old.py:80-113`):

```python
wav = current_model.generate(
    text=text,
    prompt_text=prompt_text,
    prompt_wav_path=prompt_wav_path,
    cfg_value=float(cfg_value_input),
    inference_timesteps=int(inference_timesteps_input),
    normalize=do_normalize,
    denoise=denoise,
)
return (current_model.tts_model.sample_rate, wav)
```

UI controls (`create_demo_interface`, `app_old.py:152-268`): Quick-Start and Pro-Tips accordions, prompt-audio upload/mic (default `./examples/example.wav`), and these widgets:

| widget | config |
|---|---|
| CFG slider (`app_old.py:228-235`) | min 1.0, max 3.0, default 2.0, step 0.1 |
| Inference timesteps (`app_old.py:236-243`) | min 4, max 30, default 10, step 1 |
| Text normalization checkbox | default False (`DoNormalizeText`) |
| Prompt enhancement checkbox | default False (`DoDenoisePromptAudio`, ZipEnhancer) |
| Launch (`run_demo`, `app_old.py:279-288`) | `server_name="localhost"`, `server_port=7860`, queue `max_size=10, default_concurrency_limit=1` |

## LoRA fine-tune WebUI (lora_ft_webui.py)

Default checkpoint preference (verbatim, `lora_ft_webui.py:18-20`):

```python
_v2_path = project_root / "models" / "openbmb__VoxCPM2"
_v15_path = project_root / "models" / "openbmb__VoxCPM1.5"
default_pretrained_path = str(_v2_path if _v2_path.exists() else _v15_path)
```

Sample-rate detection reads the encoder rate from the model config (verbatim, `lora_ft_webui.py:104-119`):

```python
with open(config_file, "r", encoding="utf-8") as f:
    cfg = json.load(f)
return int(cfg["audio_vae_config"]["sample_rate"])
```

Checkpoint scan + default LoRA config (verbatim, `lora_ft_webui.py:149-218`):

```python
for root, dirs, files in os.walk(root_dir):   # root_dir="lora"
    if "lora_weights.safetensors" in files:
        rel_path = os.path.relpath(root, root_dir)
```

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

Model load always carries a LoRA config so checkpoints can hot-swap later (verbatim, `lora_ft_webui.py:221-252`):

```python
current_model = VoxCPM.from_pretrained(
    hf_model_id=pretrained_path,
    load_denoiser=False,
    optimize=False,
    lora_config=lora_config,
    lora_weights_path=lora_weights_path,
)
```

`run_inference` (visible part, `lora_ft_webui.py:255-315`): reuses `current_model` when loaded, otherwise resolves the base path from the UI field → saved `lora_config.json:base_model` → default path; on rank mismatch (`model r` vs `checkpoint r`) it reloads from the checkpoint's base model. Training-loop, subprocess launch, and Gradio tab wiring live past the truncation point (file has 1332 lines; chunk stops ~line 315).

## Chinese README (README_zh.md)

Positioning statement (verbatim, `README_zh.md:43`): **VoxCPM2** is built on MiniCPM-4, 2B params, trained on 2M+ hours, supports 30 languages + 9 Chinese dialects, native 48 kHz output. Feature bullets in the visible portion: 30-language TTS, voice design, controllable cloning, ultimate (continuation) cloning, 48 kHz via AudioVAE V2 asymmetric codec, context-aware prosody, streaming (RTF ~0.3, ~0.13 via Nano-vLLM/vLLM-Omni), Apache-2.0 (`README_zh.md:45-54`).

Minimal Python API (verbatim, `README_zh.md:96-119`):

```python
model = VoxCPM.from_pretrained(
  "openbmb/VoxCPM2",
  load_denoiser=False,
)
wav = model.generate(
    text="VoxCPM2 是目前推荐使用的多语言语音合成版本。",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
```

CLI surface (verbatim flags, `README_zh.md:132-163`):

```bash
voxcpm design --text "..." --output out.wav
voxcpm design --text "..." --control "年轻女声，温暖温柔，略带微笑" --seed 42 --output out.wav
voxcpm clone --text "..." --reference-audio path/to/voice.wav --output out.wav
voxcpm clone --text "..." --prompt-audio path/to/voice.wav --prompt-text "参考音频转录文本" --reference-audio path/to/voice.wav --output out.wav
voxcpm batch --input examples/input.txt --output-dir outs
```

Web Demo and device flag (verbatim, `README_zh.md:168-177`):

```bash
python app.py --port 8808
python app.py --device auto   # auto | cpu | mps | cuda | cuda:N
```

Production/on-device pointers in the visible portion: `pip install nano-vllm-voxcpm` (RTF ~0.13 on RTX 4090), `vllm serve openbmb/VoxCPM2 --omni --port 8000` with `/v1/audio/speech`, and `llama.cpp-omni` `voxcpm2-cli -t/-o/-r/--prompt-wav/--prompt-text/--cfg/--timesteps/--seed/--temperature/--stream` (`README_zh.md:179-260`). Version table, fine-tune, docs, and risk sections are past the chunk's cut point.

**Covers:** `.dockerignore`, `.gitignore`, `app.py` (visible through `generate_tts_audio` signature; rest truncated), `app_old.py`, `lora_ft_webui.py` (visible through `run_inference` LoRA hot-swap; rest truncated), `README_zh.md` (visible through deployment sections; version table onward truncated)
