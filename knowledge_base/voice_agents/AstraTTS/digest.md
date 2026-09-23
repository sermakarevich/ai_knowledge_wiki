> [[index|Wiki]] | [[summary|Summary]]

# AstraTTS — Digest

## 1. [[wiki/01-astratts|AstraTTS]]

**In one sentence:** AstraTTS is an ONNX Runtime-based, cross-platform TTS engine offering CPU-optimized inference with an inference pool for concurrency, millisecond-level streaming output, voice/model management via WebUI, and V1 (stable, recommended) plus V2 (experimental) engines deployable on Windows, Linux, macOS, and Docker.

## Key points
- High-performance inference is built on ONNX Runtime with deep CPU instruction-set optimization, claimed to be far faster than traditional Python inference, plus an inference-pool design for multi-channel concurrent synthesis across multi-core CPUs.
- Streaming output offers millisecond-level first-packet latency so synthesis plays while generating; configuration supports runtime hot-reload with no restart.
- Platform coverage is Windows 10/11 natively plus Linux (Ubuntu, Arch, WSL) and macOS (Apple Silicon / Intel); macOS builds use only the v1 inference engine.
- Language support covers Chinese/English and Chinese/Japanese bilingual mixed reading, with trilingual mixing still in development.
- v1.2.2 added macOS support via PR #3 from Domination888; v1.2.1 added native Docker support, one-click WebUI config reset, Linux audio fallback (`pw-play` -> `paplay` -> `aplay`), and v2ProPlus parallel loading plus concurrent synthesis.
- Core resources (`resources-minimal`) are no longer hosted via Git LFS and must be downloaded from GitHub Releases and extracted to the project root (source/Docker users).
- Engine choice defaults to V1 (stable, supports V2ProPlus model cloning, deterministic generation without TopK/Temp); V2 (from GPT-SoVITS-Minimal) is work-in-progress, Chinese/English only, but supports TopK / Temp / NoiseScale sampling.
- Default service endpoint is `http://localhost:5000`, with LAN access via `--urls "http://0.0.0.0:5000"` and builds requiring .NET 10.0 SDK.

## The argument in five moves
1. AstraTTS positions itself as a CPU-optimized, ONNX Runtime-based TTS engine that beats traditional Python inference on speed.
2. It makes synthesis interactive through millisecond-level streaming output that plays while generating.
3. It scales to concurrent use through an inference-pool design exploiting multi-core CPUs.
4. It stabilizes delivery on the recommended deterministic V1 engine with bilingual mixed reading, keeping sampling-capable V2 experimental.
5. It ships as a manageable product via WebUI voice/model management with hot-reload config across Windows, Linux, macOS, and Docker.
6. It sustains that footprint with manual `resources-minimal` distribution via GitHub Releases and .NET 10.0 builds served on `localhost:5000`.
