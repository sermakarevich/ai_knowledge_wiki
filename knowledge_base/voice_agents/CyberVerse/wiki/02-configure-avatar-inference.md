> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Configure Avatar Inference
**In one sentence:** Avatar inference is enabled in `config/cyberverse.yaml` with per-model files under `config/avatar_models/`, optional FP4/SageAttention/FlashAttention acceleration, RTP log checks for stutter, and TURN/remote-access fixes.
## Key points
- Set `inference.avatar.enabled: true` in `config/cyberverse.yaml`, with `default: "flash_head"` or `"live_act"`, `idle_strategy: "silent_inference"`, `runtime.cuda_visible_devices: 0`, `runtime.world_size: 1`, and `model_config_dir: "avatar_models"`.
- Edit the active per-model file (`config/avatar_models/flash_head.yaml` or `config/avatar_models/live_act.yaml`); the Web UI also edits model parameters in those files, and model paths must match local checkpoints.
- Baidu Xiling is not an avatar inference model and must not be set as `inference.avatar.default`; it is selected per character in the Web UI with credentials in `config/env`, while CyberVerse still runs ASR/LLM/TTS/history and sends 16 kHz 16-bit mono PCM chunks to the browser driving the H5 iframe via `sendAudioData` / `AUDIO_STREAM_RENDER`.
- LiveAct FP4 GEMM is optional and requires building `lightx2v_kernel` from LightX2V with PyTorch 2.7+ and a CUTLASS checkout, then setting `fp8_gemm: false` and `fp4_gemm: true` under `live_act` and restarting inference.
- Diagnose stutter with RTP = `elapsed / (frames / fps)`: RTP < 1 means headroom, = 1 means exactly realtime, > 1 means inference is slower than playback; the chunk's examples are LiveAct `1.870 / 1.6 ≈ 1.17` (32 frames at 20 fps, 320×480) and FlashHead `2.100 / (33/20) ≈ 1.27` (33 frames at 20 fps, 512×512).
- When RTP > 1, lower resolution/quality (LiveAct `infer_params.size`, FlashHead `height`/`width`, or `model_type: "lite"` instead of `"pro"`), add compute (more GPUs, FP8/FP4, faster GPU), or match a resolution/FPS/GPU row marked Yes under Real-time; pure voice mode and cloud APIs (Baidu Xiling, Xunfei) do not use local avatar RTP.
- For `streaming_mode: direct` with the embedded TURN server, the browser must reach `8443/TCP` (check with `nc -vz <server-ip> 8443`, tunnel with `ssh -L 8443:127.0.0.1:8443 user@host -p port`, or set `pipeline.ice_public_ip` to the public IP/domain for direct access).
---
## Configure Avatar Inference
From the chunk:
```yaml
inference:
  avatar:
    enabled: true
    default: "flash_head"               # use "flash_head" or "live_act"
    idle_strategy: "silent_inference"
    runtime:
      cuda_visible_devices: 0      # shared GPU ID(s), e.g. 0,1 for multi-GPU
      world_size: 1                # shared GPU count, set to 2 for dual-GPU
    model_config_dir: "avatar_models"
```
Model-specific settings live in one file per model under `config/avatar_models/`; update those paths to match local checkpoints. Edit the active model file, e.g. `config/avatar_models/flash_head.yaml` or `config/avatar_models/live_act.yaml`.
## Baidu Xiling H5 Digital Human
Credentials in `config/env`:
```env
BAIDU_XILING_APP_ID="your-app-id"
BAIDU_XILING_APP_KEY="your-app-key"


# Optional when the figure needs a fixed camera.
BAIDU_XILING_CAMERA_ID="0"
```
Verbatim: "Baidu Xiling is selected per character in the Web UI. It is not an avatar inference model and should not be configured as `inference.avatar.default`." CyberVerse still runs "ASR/LLM/TTS/history through the orchestrator, then sends 16 kHz 16-bit mono PCM chunks to the browser. The frontend embeds the Baidu H5 iframe and drives it with the official `sendAudioData` / `AUDIO_STREAM_RENDER` message format."
## LiveAct FP4 GEMM (Optional)
"FP4 acceleration requires building and installing `lightx2v_kernel` from [LightX2V](https://github.com/ModelTC/LightX2V). Use PyTorch **2.7+** and a CUTLASS checkout on the build machine."
Preparation:
```bash
pip install scikit_build_core uv
```
Build wheel:
```bash
git clone https://github.com/NVIDIA/cutlass.git
git clone https://github.com/ModelTC/LightX2V.git
cd LightX2V/lightx2v_kernel


# Replace /path/to/cutlass with the absolute path to your cutlass clone.
MAX_JOBS=$(nproc) && CMAKE_BUILD_PARALLEL_LEVEL=$(nproc) \
uv build --wheel \
    -Cbuild-dir=build . \
    -Ccmake.define.CUTLASS_PATH=/path/to/cutlass \
    --verbose \
    --color=always \
    --no-build-isolation
```
Install:
```bash
pip install dist/*.whl --force-reinstall --no-deps
```
Enable in `config/avatar_models/live_act.yaml` (or the web UI), under `live_act`:
```yaml
fp8_gemm: false
fp4_gemm: true
```
"Restart the inference service after changing these flags."
## SageAttention and FlashAttention (Optional)
SageAttention source build:
```bash
# SageAttention (source build)
git clone https://github.com/thu-ml/SageAttention.git
cd SageAttention
export EXT_PARALLEL=4 NVCC_APPEND_FLAGS="--threads 8" MAX_JOBS=32 # Optional
python setup.py install
```
FlashAttention:
```bash
# FlashAttention (optional)
wget -O flash_attn-2.8.1+cu12torch2.8cxx11abiTRUE-cp312-cp312-linux_x86_64.whl \
  "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.1/flash_attn-2.8.1%2Bcu12torch2.8cxx11abiTRUE-cp312-cp312-linux_x86_64.whl"

pip install flash_attn-2.8.1+cu12torch2.8cxx11abiTRUE-cp312-cp312-linux_x86_64.whl
```
## QA — Self-Check
"Use this section when avatar video **stutters, freezes, or falls behind** audio. The first step is to confirm whether inference can keep up with playback."
### Check RTP from inference logs
"**RTP** (real-time performance factor) compares how long a chunk took to generate versus how long that chunk lasts at the configured FPS:"
```text
RTP = elapsed / (frames / fps)
```
| RTP | Meaning |
|-----|---------|
| **< 1** | Inference is faster than playback — headroom for realtime streaming |
| **= 1** | Exactly realtime |
| **> 1** | Inference is slower than playback — production cannot keep up with consumption; video will lag or stutter |
"Watch the inference terminal (`make inference`) while the character is speaking. Look for **LiveAct** or **FlashHead** chunk lines."
LiveAct example (RTP > 1):
```text
INFO:inference.plugins.avatar.live_act_plugin:LiveAct chunk: idx=2 frames=32 320x480 fps=20 iter=2 elapsed=1.870s is_final=False
```
- Playback duration: `32 / 20 = 1.6` s
- RTP: `1.870 / 1.6 ≈ 1.17` (**> 1** → too slow for 320×480 @ 20 fps on this GPU)
FlashHead example:
```text
INFO:...FlashHead video chunk generated: chunk_index=1 num_frames=33 512x512 fps=20 ... elapsed=2.100s
```
"Here RTP = `2.100 / (33/20) ≈ 1.27` — also above realtime."
### What to do when RTP > 1
1. "**Lower resolution or quality** — e.g. LiveAct `infer_params.size`, FlashHead `height` / `width`, or FlashHead `model_type: "lite"` instead of `"pro"`."
2. "**Add compute** — more GPUs (`runtime.world_size`, `cuda_visible_devices`), enable FP8/FP4 GEMM or compile options where supported, or use a faster GPU."
3. "**Match the support list** — for local GPU models, pick a resolution/FPS/GPU row marked **Yes** under **Real-time?** in [Realtime Digital Human Video Interaction](#realtime-digital-human-video-interaction) above."
Verbatim: "Pure voice mode (`inference.avatar.enabled: false`) does not use avatar RTP. Baidu Xiling and Xunfei digital humans are cloud APIs and do not use local avatar RTP either; stutter there is usually network/WebRTC or upstream voice latency — see [Remote Access Notes](#remote-access-notes)."
## Remote Access Notes
"When `streaming_mode: direct` uses the embedded TURN server, the browser must be able to reach the server's `8443/TCP`. If the page loads but audio/video never connects, or the server logs show `ICE connection state: failed` or `publish timeout waiting for connection`, first check whether your machine can reach port `8443` on the server:"
```bash
nc -vz <server-ip> 8443
```
"If `8443` is not reachable, the usual cause is a cloud security group, firewall, or NAT restriction. In that case, you can forward your local `8443` to the server through an SSH tunnel:"
```bash
ssh -L 8443:127.0.0.1:8443 user@host -p port
```
"After the tunnel is established, the browser will access the remote TURN service through local `127.0.0.1:8443`." "If you want the browser to connect to the remote server directly instead of through an SSH tunnel, set `pipeline.ice_public_ip` in `config/cyberverse.yaml` to the server's public IP or domain. If you are using an SSH tunnel, you can keep the default value (`127.0.0.1`)."
## Trailing sections in chunk
Roadmap is maintained in Yuque ("Roadmap 已迁移至语雀"): CyberVerse Requirements Management link in chunk. Community: WeChat `wx_dsd2077` with CyberVerse note, invite to CyberVerse Digital Human Technology Group. License: "GNU General Public License v3.0 — see [LICENSE](LICENSE)." Acknowledgements list in chunk: SoulX-FlashHead, SoulX-LiveAct, MuseTalk, Pion, Linux.do.
**Covers:** Configuring avatar inference settings and model paths (Configure Avatar Inference through Acknowledgements tail in chunk).
