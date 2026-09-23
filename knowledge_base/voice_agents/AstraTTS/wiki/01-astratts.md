[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AstraTTS
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
---
## Project features
**Covers:** chunk sections "项目特性" (features), v1.2.2 / v1.2.1 changelog

- High-performance inference: ONNX Runtime, CPU instruction-set optimized, "远快于传统的 Python 推理".
- High concurrency: built-in inference pool (Inference Pool), multi-channel concurrent synthesis using multi-core CPU.
- Streaming output: millisecond-level first-packet latency, play-while-synthesizing.
- Visual management: WebUI panel covering voice management, model conversion, parameter tuning (light/dark themes: synthesis lab, voice library, control center, model converter).
- Multi-platform: native Windows 10/11; Linux (Ubuntu, Arch, WSL) and macOS (Apple Silicon / Intel) fully compatible.
- Multi-language: complete Chinese/English and Chinese/Japanese bilingual mixed reading ("三语混合尚在开发中").
- Hot reload: config items take effect immediately while the service runs.
- v1.2.2: "新增MacOS支持，来自 #3", crediting Domination888.
- v1.2.1 additions: native Docker support (minimal optimized Dockerfile on `.NET 10 (Ubuntu Noble)` + native Python, one-click start, Tsinghua mirrors for China by default); WebUI one-click reset; Linux CLI audio fallback `pw-play` -> `paplay` -> `aplay`; retained/optimized GPT-SoVITS V2ProPlus parallel model loading and concurrent synthesis.

## Installation and deployment
**Covers:** chunk sections "安装与部署指南" (bundle / Docker / LAN)

Bundle (integrated package) via Quark: `https://pan.quark.cn/s/416fa9f65f3b`, extraction code `y8Wx`.

| OS | Package | Steps (verbatim) |
| :--- | :--- | :--- |
| Windows | `-win64.zip` | Download and extract; run `astra-server.exe`; open `http://localhost:5000`; import SoVITS models on "模型转换" page; upload reference audio on "音色库管理" page; single-shot local playback via `astra-cli.exe`. |
| Linux | `-linux64.tar.gz` | `tar -xzvf AstraTTS-v*-linux64.tar.gz`; init converter env with `./init-env.sh` (builds lightweight venv under `tools/converter/.venv`); start with `chmod +x astra-server && ./astra-server`; CLI via `./astra-cli --text "测试"`. |
| macOS | `-macOS-arm64.dmg` / `-macOS-x64.dmg` or `.tar.gz` | Apple Silicon (M1/M2/M3/M4) and Intel supported, v1 engine only. DMG (recommended): download matching arch, drag `AstraTTS.app` to `Applications`, right-click → Open on first launch to bypass Gatekeeper, optional `brew install ffmpeg` for low-latency streaming. tar.gz: `tar -xzvf AstraTTS-v*-macOS-arm64.tar.gz`, `xattr -dr com.apple.quarantine .`, optional `./init-env-mac.sh`, then `./astra-server` (`http://localhost:5000`) or `./astra-cli --text "你好世界"`. |

> "注意：macOS 版仅启用 **v1 推理引擎**，v2 / v2ProPlus 暂未在 macOS 上启用。"

Docker deployment (recommended for servers):

```bash
git clone https://github.com/Blackwood416/AstraTTS.git
cd AstraTTS

wget https://github.com/Blackwood416/AstraTTS/releases/latest/download/resources-minimal.zip
unzip resources-minimal.zip
rm resources-minimal.zip

docker build -t astratts-server:latest .

docker run -d --name astratts \
  -p 5000:5000 \
  -v ./resources:/app/resources \
  astratts-server:latest
```

Notes: download `resources-minimal.zip` from GitHub Releases into `resources-minimal` at the source root; Docker image uses the Dudooniao mirror node `https://docker.aityp.com/` with apt/pip defaulting to Tsinghua sources; after start, open `http://localhost:5000` with hot-reload, voice management, and model conversion working in-container.

LAN access: Windows `.\astra-server.exe --urls "http://0.0.0.0:5000"`, Linux `./astra-server --urls "http://0.0.0.0:5000"`, then visit e.g. `http://192.168.1.100:5000` from other devices.

Resource note (verbatim): "由于核心模型体积较大且 Git LFS 开销较高，项目现已**停止使用 Git LFS**。核心资源（`resources-minimal`）现已移至 [GitHub Releases](https://github.com/Blackwood416/AstraTTS/releases) 独立托管。**从源码构建或使用 Docker 的用户，请务必手动下载资源包并解压至项目根目录。**"

## Project structure and engine comparison
**Covers:** chunk sections "项目结构", "引擎版本对比", "模型与资源目录"

- **AstraTTS.Core**: core SDK with hybrid G2P engine, RoBERTa/Hubert feature extractors, and high-performance inference engines for each version.
- **AstraTTS.CLI**: CLI tool; Windows supports low-latency WASAPI playback; Linux pipes to `aplay`/`paplay`/`pw-play` audio backends.
- **AstraTTS.Web**: backend web service with full WebUI management, supports headless deployment on Linux servers.

Default engine is **V1 (recommended)**; V2 is low-maturity.

| 特性 | V1 引擎 (推荐) | V2 引擎 (实验性) |
| :--- | :--- | :--- |
| **项目来源** | 基于 [Genie-TTS](https://github.com/High-Logic/Genie-TTS) | 基于 [GPT-SoVITS-Minimal](https://github.com/GPT-SoVITS_minimal) |
| **状态** | ✅ 稳定，支持 **V2ProPlus** 模型克隆 | 🚧 开发中 (WIP) |
| **语种能力** | ✅ 中日混读 / 中英混读 (双语) | ⚠️ 仅中英 |
| **采样参数** | ❌ 确定性生成 (不支持 TopK/Temp) | ✅ 支持 TopK / Temp / NoiseScale |
| **并发能力** | ✅ 支持 (Inference Pool) | ✅ 支持 |

Resource layout (version 1.1.x+):

```text
resources/
├── models_v1/                   # V1 引擎模型 (扁平化)
│   └── {avatarId}/              # 核心 vits.onnx 存放处
├── models_v2/                   # V2 引擎模型
│   └── {avatarId}/              # sovits.onnx 等
├── shared/                      # 基础库
│   ├── g2p/                     # 日语/中/英字典及模型
│   ├── v1_extra/                # 通用 Bert/Hubert 组件
├── avatars/                     # 角色音色库
│   └── {avatarId}/              # 参考音频目录
```

## Configuration and developer build
**Covers:** chunk sections "配置文件说明 (`config.yaml`)", "开发者快速开始", "许可证", "致谢", "贡献者"

Config has moved fully to YAML; core example (see `config.template.yaml` for full reference):

```yaml
ResourcesDir: "resources"      # 资源位置
DefaultAvatarId: "default"     # 默认音色

# 性能配置
IntraOpNumThreads: 0           # 0 为自动线程数
InterOpNumThreads: 1           # 算子间并行

# 引擎与推理
UseEngineV2: false             # 默认使用 V1 
Speed: 1.0                     # 默认语速
StreamingMode: true            # 开启流式

# 音色定义
Avatars:
- Id: default
  Name: "我的音色"
  References:
  - Id: normal
    AudioPath: "ref.wav"
    Language: "zh"             # 指定参考音频语种
```

Build environment: .NET 10.0 SDK; Windows 10/11 (x64/arm64); Linux x86_64 or ARM64 mainstream distros (Ubuntu 22.04+, Arch Linux, WSL2) requiring `dotnet-runtime-10.0`, with CLI playback via `alsa-utils` (`aplay`) or `pulseaudio` (`paplay`); macOS 11 (Big Sur)+ on Apple Silicon (arm64) and Intel (x64), v1 engine only, CLI streaming playback via `brew install ffmpeg` (`ffplay`) while stock `afplay` supports non-streaming only.

Build/publish scripts: Windows `publish.ps1`; Linux `publish-linux.sh`; macOS `publish-mac.sh` (auto-detects arch, optional `arm64` / `x64` arg); tarball via `./pack-release.sh`; DMG via `./pack-mac-dmg.sh` (must run on a macOS host).

License: MIT License. Acknowledgements: Genie-TTS (V1 core architecture reference), GPT-SoVITS (V2 algorithm source), GPT-SoVITS_minimal_inference (V2 C# reference), ONNX Runtime (inference backend), NAudio (.NET audio), wasapi_relink (WASAPI low-latency helper), BreakingBad (AI-Hobbyist) (built-in default model source). Contributor: Domination888.
