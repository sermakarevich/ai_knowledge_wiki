[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** DuplexSLA is a native full-duplex Speech–Language–Action foundation model that jointly decodes assistant audio and a structured action stream on a shared 160 ms chunk timeline (README.md:36).
## Key points
- DuplexSLA unifies listening, speaking, in-conversation planning, and tool calling on a single conversational clock, decoding assistant audio with a structured action stream on a shared 160 ms chunk timeline (README.md:36).
- It uses a dual-stream three-channel formulation to close the gap where duplex backbones lacked a native channel for in-conversation planning and tool calling (README.md:38).
- The user audio channel carries continuous user audio features at an 80 ms stride (README.md:40).
- The assistant audio channel carries discrete assistant speech tokens in a TA4 layout — 1 text anchor + 4 audio tokens at 40 ms stride per chunk (README.md:41).
- The action channel is a rate-limited textual stream carrying delayed transcripts, planning text, interaction-control labels, and structured tool calls at ≤10 tokens per chunk (README.md:42).
- All three channels are decoded jointly by a single backbone initialised from Step-Audio-2-mini (~7B parameters) and adapted via continued pretraining and post-training on duplex dialogue, turn-taking, and tool-call data (README.md:44).
- Turn-taking (`pause`, `interrupt`, `backchannel`) is emitted internally from semantic state rather than an external semantic VAD, and planning/tool calls are emitted on the action channel without halting assistant audio (README.md:48, README.md:50).
---
## News
Release status as stated in the repo (README.md:20, README.md:22, README.md:23):
- **2026/05**: Released the DuplexSLA technical report.
- Inference code, model checkpoints, and DuplexSLA-Bench are coming soon.

## Open-source plan
Checklist verbatim from the repo (README.md:25, README.md:27, README.md:28):

| Artefact | Status |
|---|---|
| DuplexSLA technical report (PDF) (`DuplexSLA.pdf`) | Done (`[x]`) |
| DuplexSLA-Bench evaluation code and data | Pending (`[ ]`) |

## Introduction — dual-stream three-channel formulation
Verbatim formulation (README.md:38, README.md:40, README.md:41, README.md:42):
- **User audio channel** — continuous user audio features at an 80 ms stride.
- **Assistant audio channel** — discrete assistant speech tokens in a *TA4* layout (1 text anchor + 4 audio tokens at a 40 ms stride per chunk).
- **Action channel** — a rate-limited textual stream carrying delayed transcripts, planning text, interaction-control labels, and structured tool calls (≤10 tokens per chunk).

Joint decoding and backbone (README.md:44):

| Config | Value |
|---|---|
| Shared chunk timeline | 160 ms |
| User stride | 80 ms |
| Assistant layout | TA4 (1 text anchor + 4 audio tokens, 40 ms stride per chunk) |
| Action rate limit | ≤10 tokens per chunk |
| Backbone init | Step-Audio-2-mini (~7B parameters) |
| Adaptation | Continued pretraining (CPT) + post-training on duplex dialogue, turn-taking, tool-call data |

Architecture figure referenced in the repo (README.md:32):
- `assets/architecture.png` — "DuplexSLA chunk-level architecture", displayed at 92% width.

## Highlights
1. **Semantic-driven turn-taking control** (README.md:48): emits `pause`, `interrupt`, and `backchannel` decisions internally based on its own semantic state, rather than relying on an external semantic VAD.
2. **In-conversation planning and tool calling** (README.md:50): planning text and structured tool calls are emitted on the action channel without halting assistant audio; tool calls are anchored to their own chunks and can run in semantic order along the user's request; covers multi-action and backchannel-triggered tool use interleaved with ongoing speech.
3. **DuplexSLA-Bench** (README.md:52): duplex benchmark covering `pause`, `interrupt`, and `backchannel` turn-taking plus three in-conversation tool-calling styles — single-action, multi-action, and backchannel-triggered tool calls.

## Model usage
> 🚧 Inference code, deployment recipes, and model checkpoints are not yet released. This section will be updated once the artefacts land on Hugging Face. (README.md:56)

Planned release artefacts (README.md:60, README.md:61, README.md:62):
- Pretrained DuplexSLA checkpoint on Hugging Face.
- Reference inference / streaming server.
- DuplexSLA-Bench evaluation harness and data.

## Citation
Verbatim citation block from the repo (README.md:68, README.md:69):

```bibtex
@article{zhang2026duplexsla,
  title   = {{DuplexSLA}: A Full-Duplex Spoken Language Model with Synchronized Speech, Language, and Action},
  author  = {Zhang, Haoyang and Chen, Jun and Wu, Donghang and Li, Yuxin and Zhang, Yuxin and Zhang, Xiangyu Tony and Liu, Che and Lin, Qingjian and Peng, Yizhou and Liu, Hexin and Chng, Eng Siong and Yan, Chao and Wu, Boyong and Huang, Yechang and Yang, Xuerui and Yu, Gang and Tian, Fei},
  journal = {arXiv preprint},
  year    = {2026}
}
```

## License
This project is released under the MIT License (`LICENSE`) (README.md:79).

**Covers:** `README.md`, `DuplexSLA.pdf`, `LICENSE`, `assets/architecture.png`
