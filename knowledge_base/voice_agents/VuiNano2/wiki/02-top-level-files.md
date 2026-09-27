> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** Top-level files define how Vui is cloned, installed, edited, ignored by git, demoed as TTS, and fed example texts.
## Key points
- `AGENTS.md` orients AI coding agents: Vui is a streaming conversational voice assistant (ASR → LLM → TTS) built around a 305M speech transformer over the Qwen3-TTS-12Hz codec (AGENTS.md:3-5).
- Setup is `uv`-only on Python 3.12 (`uv sync`, `--extra mlx`, `--extra claude`) with setuptools-layout imports (`from vui.x import y`), because `pip` ignores `[tool.uv.sources]` and source-builds flash-attn (AGENTS.md:10-15).
- Entry points are `python -m vui.serving.stream` on `:8080`, `python -m vui.serving.claude_server` on `:8642`, `python demo.py` (Gradio) with `demo.py --render --prompt` CLI rendering, and `docker compose up -d`; no test suite is committed, so changes are verified end-to-end via the entry point (AGENTS.md:21-27).
- `bootstrap.sh` is hosted at `https://install.fluxions.ai` (`curl -fsSL https://install.fluxions.ai | bash`), clones Vui into `$VUI_HOME` (default `~/vui`) at `$VUI_REF` (default `main`), then execs `install.sh` forwarding all args (bootstrap.sh:2-13).
- `demo.py` auto-detects platform (MLX on Apple Silicon arm64/darwin, CUDA elsewhere), parses `checkpoint`, `--render`, `--text/-t`, `--prompt/-p` (default `prompts/harry.wav`), `--temperature`, `--n-codebooks`, `--max-secs`, `--eos-threshold`, and exits early into `vui.demo.cli.run` in render mode (demo.py:1-71).
- `install.sh` never uses sudo, validates it runs inside a Vui checkout (`pyproject.toml` + `src/vui` + `name = "vui"`), resolves the LLM backend (explicit flag > `VUI_LLM_BACKEND` > live Ollama > live vLLM > default `vllm`), picks docker vs native, pins the torch CUDA build from GPU compute capability, and fetches ffmpeg shared libs for torchcodec when needed (install.sh:28-30, install.sh:97-100, install.sh:135-148, install.sh:217-231, install.sh:244-294).
- `.gitignore` excludes Python/Docker/venv/IDE artifacts plus repo-specific outputs: `*.pt`, `*.wav`, `*.mp3`, `*.tar.gz`, `*.safetensors`, `*.opus`, `*.log`, `*.json` (with `!sample_texts.json` exception), `checkpoints/`, `scratch/`, `debug_dump/`, `outputs/`, `prompts/`, `todo.md`, and generated `cpu/*.onnx`, `cpu/*.onnx.data`, `cpu/*.bin`, `cpu/vui_tts` (`.gitignore`:165-187).
---
## .gitignore
Standard Python gitignore plus Vui runtime exclusions (`.gitignore`:1-187):
```gitignore
*.pt
*.wav
*.mp3
*.tar.gz
*.safetensors
*.opus
*.log
*.json
!sample_texts.json
checkpoints/
```
```gitignore
# Local scratch / dumps / outputs
scratch/
debug_dump/
outputs/
prompts/
todo.md

# cpu/ inference artifacts (large, generated)
cpu/*.onnx
cpu/*.onnx.data
cpu/*.bin
cpu/vui_tts
```
- The `!sample_texts.json` negation keeps the demo-text fixture tracked while ignoring other JSON outputs (`.gitignore`:173).
## AGENTS.md
Agent orientation header, verbatim (AGENTS.md:3-5):
> "Orientation for AI coding agents working on Vui — a streaming conversational voice assistant (ASR → LLM → TTS) built around a 305M speech transformer over the Qwen3-TTS-12Hz codec."
> "For end-user setup (Docker, voices, hardware), read `README.md`. This file is for editing the code."
Setup, verbatim (AGENTS.md:10-15):
```sh
uv sync                    # base + flash-attn prebuilt wheel (Linux/CUDA)
uv sync --extra mlx        # add Apple Silicon backend
uv sync --extra claude     # add Claude task-server deps
```
| Command | What it does (AGENTS.md:21-25) |
|---|---|
| `python -m vui.serving.stream` | Streaming server on `:8080` (browser UI at `/`) |
| `python -m vui.serving.claude_server` | Optional Claude task sidecar on `:8642` |
| `python demo.py` | Gradio TTS playground |
| `python demo.py --render --prompt prompts/abraham.wav` | CLI render with a preset voice |
| `docker compose up -d` | Full stack via compose (see `docker-compose.yml`, `docker/`) |
- No test suite is committed; UI/streaming changes are verified in the browser UI and model changes via `demo.py` rendering (AGENTS.md:27).
- Repo-layout tables name `src/vui/model.py` (768 dim, 22 layers, 8 heads, `sq_proj`/`wps_proj` conditioning), `engine.py` (`Engine`/`GenConfig`/`Row`, WPS estimation), `inference.py`, `qwen_codec.py` (16 codebooks × 2048, 12.5 Hz, 24 kHz), `qwen_spk_enc.py`, `rope.py`/`sampling.py`, `tokenizer.py`, `align.py`, `prompt_utils.py`, `streaming.py`, `hf.py`, `config.py`, `demo/cli.py`; `src/vui/mlx/tts/` and `mlx/asr/`; the three-process `serving/stream/` tree (`__main__.py`, `server.py` with `DEFAULT_SETTINGS`/`n_codebooks`, `connection.py`, `voice_turn.py`, `tts_worker.py`, `tts_worker_mlx.py`, `asr_worker.py`, `audio_in_worker.py`, `vad.py`, `playback.py`, `drains.py`, `llm.py`/`llm_backend.py`, `thoughts.py`, `tools/`, `memories.py`, `tasks.py`, `protocol.py`, `prompts.py`/`prompt_routes.py`, `model_routes.py`, `voice_note_routes.py`, `test_routes.py`, `realtime/`, `asr/`, browser UI, helpers); `claude_server.py` on `:8642` with `discover_mcp_tools()` and `MODEL`; and other top-level `demo.py`, `prompts/`, `docs/` (`configuration.md`, `realtime-api.md`, `memory-budget.md`, `thoughts-tools.md`), `docker/` (`Dockerfile.stream`, `Dockerfile.claude`), `docker-compose.yml`, `pyproject.toml` (AGENTS.md:33-103).
- Conventions: no emojis; modern typing (`list[str]`, `dict[str, X]`, `str | None`); minimal why-comments; flat imports (`from vui.engine import Engine`); `VUI_`-prefixed env vars read once at startup; single-tenant assumption; main ↔ TTS worker ↔ ASR worker crossing only via `torch.multiprocessing.Queue` with small picklable payloads; `tts_worker.py`/`voice_turn.py` are latency-sensitive with buffer reuse and CUDA-graph boundaries (AGENTS.md:107-114).
## bootstrap.sh
Full 44-line script shown without truncation; header, verbatim (bootstrap.sh:2-13):
```sh
# Vui bootstrap — hosted at https://install.fluxions.ai
#
#     curl -fsSL https://install.fluxions.ai | bash
#     curl -fsSL https://install.fluxions.ai | bash -s -- --docker
#
# Clones Vui into $VUI_HOME (default ~/vui), then execs ./install.sh inside it.
# All args after `--` are forwarded to install.sh — see `./install.sh --help`.
```
| Env knob | Default (bootstrap.sh:10-19) |
|---|---|
| `VUI_HOME` | `$HOME/vui` |
| `VUI_REPO` | `https://github.com/fluxions-ai/vui` |
| `VUI_REF` | `main` |
- Requires `git`, refuses a non-repo `$VUI_HOME`, fetches/checks out/pulls an existing clone after a clean-tree check, otherwise `git clone --branch "$VUI_REF"`, then `cd "$VUI_HOME"` and `exec bash "$VUI_HOME/install.sh" "$@"` (bootstrap.sh:24-43).
## demo.py
Truncated in the chunk: 1492-line file, excerpt ends after the MLX model loader with 39617 more characters cut, so Gradio UI wiring, CUDA generation path, and render helpers below that point are not covered here.
- Module docstring, verbatim (demo.py:1-8): "TTS demo with training-style text chunking. Auto-detects platform: uses MLX on Apple Silicon, CUDA elsewhere."
- CLI surface, verbatim arg names (demo.py:28-51): positional `checkpoint`, `--render`, `--text/-t`, `--prompt/-p` default `prompts/harry.wav`, `--temperature`, `--n-codebooks`, `--max-secs`, `--eos-threshold`.
- Render mode exits early via `from vui.demo.cli import run as cli_run` with `checkpoint_path = _args.checkpoint or "vui-nano-1.1.safetensors"` plus temperature/n_codebooks/max_secs/eos_threshold overrides (demo.py:56-71).
- Platform detection, verbatim (demo.py:78-80): `IS_APPLE_SILICON = platform.machine() == "arm64" and sys.platform == "darwin"`; `HAS_CUDA = not IS_APPLE_SILICON and torch.cuda.is_available()`; `USE_MLX = IS_APPLE_SILICON`.
- MLX-only helpers shown: KV disk cache at `~/.cache/vui/kv` keyed by prompt hash + checkpoint stem + precision (`_kv_cache_path`), `_save_kv_to_disk`/`_load_kv_from_disk` round-tripping decoder `kv_caches` with an `offset` metadata, `_prefill_segments_mlx` prefilling `[spk] [text_i] [audio_i]` per segment, and `generate_chunked_mlx` matching the CUDA `generate_chunked` interface via `chunk_text(text, sentence_only=True, single_speaker=True)` with per-turn cache rewind to `prompt_offset` (demo.py:109-268).
- Settings persistence: `CACHE_DIR = ~/.cache/vui`, `SETTINGS_FILE = demo_settings.json`, `DEFAULTS` table below, `_load_settings`/`_save_settings` merging stored JSON over defaults (demo.py:276-317).
| `DEFAULTS` key | Value (demo.py:280-299) |
|---|---|
| `temperature` | `0.7` |
| `top_k` | `50` |
| `use_top_p` | `False` |
| `top_p` | `1.0` |
| `max_duration` | `120` |
| `sq_dns_sig` / `sq_dns_bak` / `sq_nq_noi` / `sq_nq_disc` / `sq_nq_col` | `0.0` |
| `sq_nq_loud` | `5.0` |
| `wps_score` | `0.0` |
| `rep_penalty` | `1.1` |
| `rep_window` | `24` |
| `chunk_words` | `20` |
| `n_codebooks` | `0` |
| `eos_threshold` | `0.45` |
| `compile_rq` | `False` |
- Checkpoint resolution via `from vui.hf import download` with `checkpoint_path = download(checkpoint_path)`; MLX loader `load_quantized(ckpt_path, precision)` reads `max_secs` from config (default `15.0`), calls `compile_forward()`, and reports parameter megabytes (demo.py:320-342).
## install.sh
Truncated in the chunk: 476-line file, excerpt covers arg parsing through ffmpeg fetching with 7460 more characters cut, so launch/docker-compose/native tail steps are not covered here.
- Header modes, verbatim (install.sh:7-16): `./install.sh` (setup + launch), `--docker`, `--native`, `--upgrade`, `--no-claude`, `--no-launch`, `--llm vllm`, `--model qwen3:8b`, `--dry-run`, `--help`.
| Env knob | Default/meaning (install.sh:18-26) |
|---|---|
| `VUI_REF` | git ref for `--upgrade` (default `main`) |
| `OLLAMA_HOST` | remote Ollama endpoint (e.g. `gpu-box.lan:11434`) |
| `VUI_VLLM_URL` | vLLM endpoint (default `http://localhost:8000`) |
| `VUI_TASK_PORT` | Claude task server port (default `8642`) |
| `VUI_MODE` | `native` or `docker`, same as flags |
| `VUI_FFMPEG_DIR` | ffmpeg shared-lib cache (default `~/.cache/vui/ffmpeg`) |
| `VUI_FFMPEG_VERSION` | ffmpeg major line (default `7.1`) |
- Never uses sudo; native path needs no root (install.sh:28-30).
- Arg parsing accepts `--model/--no-launch/--no-claude/--docker/--native/--llm/--upgrade/--dry-run/-h/--help` and rejects unknown args with exit 2 (install.sh:73-86); helpers are `log`/`warn`/`die`/`run` with `run` echoing `   $ ...` under dry-run (install.sh:88-91).
- Refuses to run outside a checkout (`pyproject.toml` + `src/vui` + `^name = "vui"`); `--upgrade` requires `.git`, a clean tree, then fetch + checkout + `--ff-only` pull (install.sh:97-112).
- Backend resolution order in `resolve_llm_backend()`: explicit `--llm` > `VUI_LLM_BACKEND` > reachable Ollama (`/api/version`) > reachable vLLM (`/v1/models`) > die if `OLLAMA_HOST` set-but-unreachable, else `vllm`; neither backend up is still fine since TTS/ASR serve regardless (install.sh:118-148).
- Docker-vs-native: forced `MODE`/`VUI_MODE` wins, else prompt when interactive with Docker usable, else non-interactive Docker default, else native (install.sh:159-175).
- GPU handling: `detect_gpu()` reads compute capability via `nvidia-smi --query-gpu=compute_cap`; `resolve_torch_backend()` respects explicit `UV_TORCH_BACKEND`, exports `auto` on capability ≥ 7.5, else pins `cu126` with an SDPA/fp32 warning (install.sh:190-231).
- ffmpeg handling: torchcodec dlopens one `libtorchcodec_core` per ffmpeg major and needs shared sonames (a static ffmpeg binary is insufficient, so readiness is tested by importing `vui.ffmpeg_libs`); `ensure_ffmpeg_libs()` fetches the BtbN `ffmpeg-n<VER>-latest-<linux64|linuxarm64>-lgpl-shared` tarball into a temp dir and moves it into place (install.sh:233-294).
## sample_texts.json
Truncated in the chunk: excerpt ends mid-value at `"Sarcy: meeting hell": "Oh wonderful another meeting that coul` with 33565 more characters cut, so remaining entries after that point are not covered here.
- JSON dict of named demo/render texts mixing single-speaker monologues, two-speaker dialogues, assistant-style briefings, and disfluency-marked reads using `[laugh]`, `[sigh]`, `[hesitate]` tokens (sample_texts.json:1-36).
- Shown keys include `Podcast intro (2-speaker)`, `Excited voicemail`, `Short frustrated`, `Bad toastie (2-speaker)`, `Neural networks lecture`, `Old friends catch up (2-speaker)`, `Risotto monologue`, `Breaking news`, `Tech debate (2-speaker)`, `Assistant: morning briefing`, `Assistant: contract analysis`, `Assistant: flight delay`, `Assistant: build failure`, `Assistant: budget warning`, `Assistant: supplier comparison`, `Assistant: focus timer`, `Hesitant: planning discussion/nervous presentation/confused directions/stuttering apology/job interview/forgot something/bad idea/asking for help`, `Supportive: tough time/listening/reassurance/checking in/not your fault/take your time/proud of you/you're not alone/it's okay to cry`, `Hesitant: overwhelmed parent`, and the cut-off `Sarcy: meeting hell` (sample_texts.json:2-36).
**Covers:** `.gitignore`, `AGENTS.md`, `bootstrap.sh`, `demo.py` (truncated per note above), `install.sh` (truncated per note above), `sample_texts.json` (truncated per note above)
