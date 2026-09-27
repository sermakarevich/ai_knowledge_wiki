---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Sponsor

### Q1. Who sponsors CyberVerse and what does the sponsor provide?
> [!tip]- Answer
> CyberVerse is sponsored by Compshare (优云智算), described as UCloud's AI cloud platform. Its core offering is on-demand GPU rental with rapidly provisioned instances and usage-based billing for model, algorithm, and application development. It also provides one-stop access to domestic and international models and APIs. See [[wiki/01-sponsor|Sponsor]].

### Q2. How is the Compshare sponsorship presented and how does a reader register through it?
> [!tip]- Answer
> The sponsor block is a collapsible `<details open>` section with a single-row, two-column table pairing a 150px-wide Compshare logo with thank-you text. Both the logo and the "Register through this invitation link" text point to the Compshare passport URL carrying `referral_code=IBmJcGPVu1RF78dMihkQCX`. Registration therefore flows exclusively through that invitation link. See [[wiki/01-sponsor|Sponsor]].

### Q3. How do you enable local avatar inference in CyberVerse?
> [!tip]- Answer
> Set `inference.avatar.enabled: true` in `config/cyberverse.yaml` with `default` as `"flash_head"` or `"live_act"`, plus `idle_strategy: "silent_inference"` and the shared GPU runtime (`cuda_visible_devices`, `world_size`) with `model_config_dir: "avatar_models"`. Then edit the matching per-model file under `config/avatar_models/` (Web UI edits land in the same files) and make sure model paths match local checkpoints. See [[wiki/02-configure-avatar-inference|Configure Avatar Inference]].

### Q4. Why must Baidu Xiling never be set as `inference.avatar.default`, and how does it actually work?
> [!tip]- Answer
> Baidu Xiling is a cloud H5 digital human, not a local avatar inference model, so it is selected per character in the Web UI with credentials (`BAIDU_XILING_APP_ID/APP_KEY`, optional `CAMERA_ID`) in `config/env`. CyberVerse still runs ASR, LLM, TTS, and history through the orchestrator, then sends 16 kHz 16-bit mono PCM chunks to the browser. The frontend embeds the Baidu H5 iframe and drives it with the official `sendAudioData` / `AUDIO_STREAM_RENDER` message format. See [[wiki/02-configure-avatar-inference|Configure Avatar Inference]].

### Q5. What is required to enable optional LiveAct FP4 GEMM acceleration?
> [!tip]- Answer
> FP4 acceleration requires building and installing `lightx2v_kernel` from LightX2V using PyTorch 2.7+ and a CUTLASS checkout on the build machine. After installing the built wheel with `--force-reinstall --no-deps`, set `fp8_gemm: false` and `fp4_gemm: true` under `live_act` in `config/avatar_models/live_act.yaml` (or the Web UI). Restart the inference service after changing these flags. See [[wiki/02-configure-avatar-inference|Configure Avatar Inference]].

### Q6. How do you diagnose avatar stutter with RTP, and what do you do when RTP exceeds 1 or remote video never connects?
> [!tip]- Answer
> Compute RTP as `elapsed / (frames / fps)` from the inference logs: below 1 means headroom, exactly 1 means realtime, and above 1 (e.g. LiveAct `1.870/1.6 ≈ 1.17`, FlashHead `2.100/(33/20) ≈ 1.27`) means inference is slower than playback so video lags. When RTP exceeds 1, lower resolution or quality, add compute such as more or faster GPUs or FP8/FP4, or pick a resolution/FPS/GPU row marked Yes under Real-time. When `streaming_mode: direct` video never connects, check `8443/TCP` reachability with `nc -vz`, use an SSH `-L` tunnel, or set `pipeline.ice_public_ip` for direct access. See [[wiki/02-configure-avatar-inference|Configure Avatar Inference]].

### Q7. Should a GPU-poor team planning a CyberVerse demo use Compshare's sponsored GPU rental for local avatar video, or ship pure voice / a cloud avatar API instead?
> [!tip]- Answer
> Prefer pure voice mode or a cloud avatar API (Baidu Xiling, Xunfei) unless the demo truly needs the local-video "one photo" effect and the team can hold RTP below 1. Local avatar inference demands tuned GPU rows, optional FP4/SageAttention/FlashAttention builds, and TURN/WebRTC networking fixes, which is heavy for a GPU-poor team. Using the Compshare invitation link for a short on-demand GPU rental is justified only to validate one realtime configuration before deciding. See [[wiki/02-configure-avatar-inference|Configure Avatar Inference]].
