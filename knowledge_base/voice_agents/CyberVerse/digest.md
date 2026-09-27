> [[index|Wiki]] | [[summary|Summary]]
# Sponsor — Digest

## 1. [[wiki/01-sponsor|Sponsor]]
**In one sentence:** CyberVerse thanks Compshare (优云智算), UCloud's AI cloud platform, for sponsoring the project with on-demand GPU rental and model API services.
## Key points
- The sponsor is Compshare (优云智算), identified in the chunk as UCloud's AI cloud platform offering on-demand GPU rental and model API services.
- Its core GPU rental service provides rapidly provisioned GPU instances with usage-based billing for model, algorithm, and application development.
- Compshare also provides one-stop access to domestic and international models, with support for Claude Code, Codex, and direct API use.
- Registration is directed through an invitation link carrying `referral_code=IBmJcGPVu1RF78dMihkQCX`.
- The sponsor block is presented as a two-column table with a 150px-wide Compshare logo linking to the same invitation URL.
- The sponsored project is CyberVerse, described as an open-source real-time digital-human Agent framework using WebRTC, persona memory, tools, RAG, and optional digital-human video capabilities.

## 2. [[wiki/02-configure-avatar-inference|Configure Avatar Inference]]
**In one sentence:** Avatar inference is enabled in `config/cyberverse.yaml` with per-model files under `config/avatar_models/`, optional FP4/SageAttention/FlashAttention acceleration, RTP log checks for stutter, and TURN/remote-access fixes.
## Key points
- Set `inference.avatar.enabled: true` in `config/cyberverse.yaml`, with `default: "flash_head"` or `"live_act"`, `idle_strategy: "silent_inference"`, `runtime.cuda_visible_devices: 0`, `runtime.world_size: 1`, and `model_config_dir: "avatar_models"`.
- Edit the active per-model file (`config/avatar_models/flash_head.yaml` or `config/avatar_models/live_act.yaml`); the Web UI also edits model parameters in those files, and model paths must match local checkpoints.
- Baidu Xiling is not an avatar inference model and must not be set as `inference.avatar.default`; it is selected per character in the Web UI with credentials in `config/env`, while CyberVerse still runs ASR/LLM/TTS/history and sends 16 kHz 16-bit mono PCM chunks to the browser driving the H5 iframe via `sendAudioData` / `AUDIO_STREAM_RENDER`.
- LiveAct FP4 GEMM is optional and requires building `lightx2v_kernel` from LightX2V with PyTorch 2.7+ and a CUTLASS checkout, then setting `fp8_gemm: false` and `fp4_gemm: true` under `live_act` and restarting inference.
- Diagnose stutter with RTP = `elapsed / (frames / fps)`: RTP < 1 means headroom, = 1 means exactly realtime, > 1 means inference is slower than playback; the chunk's examples are LiveAct `1.870 / 1.6 ≈ 1.17` (32 frames at 20 fps, 320×480) and FlashHead `2.100 / (33/20) ≈ 1.27` (33 frames at 20 fps, 512×512).
- When RTP > 1, lower resolution/quality (LiveAct `infer_params.size`, FlashHead `height`/`width`, or `model_type: "lite"` instead of `"pro"`), add compute (more GPUs, FP8/FP4, faster GPU), or match a resolution/FPS/GPU row marked Yes under Real-time; pure voice mode and cloud APIs (Baidu Xiling, Xunfei) do not use local avatar RTP.
- For `streaming_mode: direct` with the embedded TURN server, the browser must reach `8443/TCP` (check with `nc -vz <server-ip> 8443`, tunnel with `ssh -L 8443:127.0.0.1:8443 user@host -p port`, or set `pipeline.ice_public_ip` to the public IP/domain for direct access).

## The argument in five moves
1. CyberVerse is an open-source real-time digital-human Agent framework (WebRTC, persona memory, tools, RAG, optional video) whose compute needs are underwritten by sponsor Compshare (优云智算), UCloud's AI cloud platform.
2. Compshare's contribution is on-demand, rapidly provisioned GPU rental with usage-based billing plus one-stop domestic/international model and API access, reached via the invitation link carrying `referral_code=IBmJcGPVu1RF78dMihkQCX`.
3. Locally, avatar video is switched on in `config/cyberverse.yaml` (`flash_head`/`live_act`, `silent_inference`, shared GPU runtime) with per-model files under `config/avatar_models/`, while Baidu Xiling stays out of `inference.avatar.default` as a per-character cloud H5 figure driven by PCM audio.
4. Inference speed is bought optionally via LiveAct FP4 GEMM (LightX2V `lightx2v_kernel` build, PyTorch 2.7+, CUTLASS) and SageAttention/FlashAttention acceleration, and verified quantitatively with RTP = elapsed / (frames / fps) against the LiveAct (~1.17) and FlashHead (~1.27) worked examples.
5. When RTP exceeds 1 the remedy is lower resolution/quality, more or faster compute, or a Real-time Yes row — and when the embedded TURN path in `streaming_mode: direct` fails, the fix is network-level (reach 8443/TCP, SSH tunnel, or set `pipeline.ice_public_ip`).
