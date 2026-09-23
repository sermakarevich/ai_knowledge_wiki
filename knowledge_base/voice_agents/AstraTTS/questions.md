---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AstraTTS

### Q1. What is AstraTTS in one sentence, and which platforms and languages does it cover?
> [!tip]- Answer
> AstraTTS is an ONNX Runtime-based, cross-platform TTS engine with CPU-optimized inference, an inference pool for concurrency, millisecond-level streaming, WebUI voice/model management, and V1 (stable) plus V2 (experimental) engines. It runs natively on Windows 10/11 plus Linux (Ubuntu, Arch, WSL) and macOS (Apple Silicon/Intel), though macOS builds use only the v1 engine. It supports Chinese/English and Chinese/Japanese bilingual mixed reading, with trilingual mixing still in development. See [[wiki/01-astratts|AstraTTS]].

### Q2. How do AstraTTS's performance, concurrency, streaming, and management features work together?
> [!tip]- Answer
> High-performance inference rests on ONNX Runtime with deep CPU instruction-set optimization, claimed to be far faster than traditional Python inference. Concurrency comes from a built-in inference pool that synthesizes multiple channels at once across multi-core CPUs, while streaming output delivers millisecond-level first-packet latency so audio plays while later chunks still generate. Management is visual via a WebUI (voice library, synthesis lab, control center, model converter) with runtime hot-reload so config changes apply without restart. See [[wiki/01-astratts|AstraTTS]].

### Q3. What changed in v1.2.2 and v1.2.1?
> [!tip]- Answer
> v1.2.2 added macOS support via PR #3 from Domination888. v1.2.1 added native Docker support (minimal optimized Dockerfile on .NET 10 Ubuntu Noble with native Python, one-click start, Tsinghua mirrors by default), a WebUI one-click config reset, a Linux CLI audio fallback chain (`pw-play` -> `paplay` -> `aplay`), and retained plus optimized GPT-SoVITS V2ProPlus parallel model loading with concurrent synthesis. See [[wiki/01-astratts|AstraTTS]].

### Q4. How do you install and run the AstraTTS bundle on Windows, Linux, and macOS?
> [!tip]- Answer
> Windows downloads the `-win64.zip`, extracts it, runs `astra-server.exe`, opens `http://localhost:5000`, and uses `astra-cli.exe` for single-shot local playback. Linux unpacks the `-linux64.tar.gz`, runs `./init-env.sh` to build a lightweight venv under `tools/converter/.venv`, then starts `./astra-server` and synthesizes via `./astra-cli --text`. macOS uses the matching-arch DMG (drag `AstraTTS.app` to Applications, right-click Open once to bypass Gatekeeper) or tarball with `xattr -dr com.apple.quarantine .`, optionally installs ffmpeg for low-latency streaming, and runs only the v1 engine. See [[wiki/01-astratts|AstraTTS]].

### Q5. How does Docker deployment, LAN access, and the resources-minimal move work?
> [!tip]- Answer
> Docker users clone the repo, download `resources-minimal.zip` from GitHub Releases, extract it to the project root, then `docker build -t astratts-server:latest .` and run with `-p 5000:5000` plus a `-v ./resources:/app/resources` mount. This manual step is required because core resources left Git LFS for independent GitHub Releases hosting due to model size and LFS overhead. LAN access rebinds the server with `--urls "http://0.0.0.0:5000"` and visits the host's LAN address such as `http://192.168.1.100:5000`. See [[wiki/01-astratts|AstraTTS]].

### Q6. How do the V1 and V2 engines differ, and what is the default engine?
> [!tip]- Answer
> V1 (recommended, based on Genie-TTS) is stable, deterministic without TopK/Temp sampling, supports Chinese/Japanese and Chinese/English bilingual mixing plus inference-pool concurrency, and supports V2ProPlus model cloning. V2 (experimental work-in-progress, based on GPT-SoVITS-Minimal) supports TopK / Temp / NoiseScale sampling but handles Chinese/English only. The default is V1 (`UseEngineV2: false`); V2 is for cases needing its sampling controls. See [[wiki/01-astratts|AstraTTS]].

### Q7. What are the three code components, the resource layout, and the config/build essentials?
> [!tip]- Answer
> The three components are AstraTTS.Core (hybrid G2P engine, RoBERTa/Hubert feature extractors, per-version inference engines), AstraTTS.CLI (low-latency WASAPI playback on Windows, `aplay`/`paplay`/`pw-play` pipes on Linux, ffplay via ffmpeg for streaming on macOS), and AstraTTS.Web (backend web service with full WebUI, headless-capable on Linux servers). Resources flatten into `models_v1/{avatarId}/vits.onnx` and `models_v2/{avatarId}/sovits.onnx` plus `shared/` (g2p dictionaries, v1_extra Bert/Hubert) and `avatars/{avatarId}/` reference audio. Config is fully YAML (`ResourcesDir`, `DefaultAvatarId`, `IntraOpNumThreads: 0` for auto, `InterOpNumThreads: 1`, `Speed: 1.0`, `StreamingMode: true`, `Avatars` with reference audio paths), built with the .NET 10.0 SDK via `publish.ps1` / `publish-linux.sh` / `publish-mac.sh` plus `pack-release.sh` / `pack-mac-dmg.sh`, under an MIT License. See [[wiki/01-astratts|AstraTTS]].

### Q8. Would you recommend AstraTTS for a CPU-only, cross-platform app needing low-latency bilingual Chinese-English TTS, and why?
> [!tip]- Answer
> Yes, conditionally: its ONNX Runtime CPU optimization, millisecond-level streaming, inference-pool concurrency, and stable deterministic V1 engine with Chinese/English mixing plus Windows/Linux/macOS bundles fit that need well. Caveats are the manual `resources-minimal` download from Releases, macOS limited to the v1 engine, and trilingual mixing still in development. Pilot the V1 engine on the target CPU with the intended voices before committing. See [[wiki/01-astratts|AstraTTS]].
