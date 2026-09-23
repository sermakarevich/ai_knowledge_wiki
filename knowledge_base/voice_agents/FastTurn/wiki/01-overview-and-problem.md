> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# FastTurn: Unifying Acoustic and Streaming Semantic
**In one sentence:** Recent AudioLLM advances push spoken dialogue toward real-time full-duplex turn-taking, where existing voice-activity and ASR-based approaches leave a gap that FastTurn addresses by unifying acoustic and streaming semantic cues for low-latency robust turn detection — though this chunk truncates before stating the full contribution.
## Key points
- Recent advances in AudioLLMs moved spoken dialogue beyond turn-based interaction toward real-time full-duplex communication.
- In full-duplex operation the agent must decide when to speak, yield, or interrupt while the user is still talking.
- In practical deployments, existing full-duplex spoken dialogue systems [9, 10] rely on turn detection as a controllable interface between speech processing and response generation.
- Current turn detection approaches fall broadly into two groups, per this chunk's introduction fragment.
- The first group relies on voice activity detection (VAD) and infers interruption timing from acoustic energy or activity patterns [11, 12, 13].
- VAD-based methods are described as lightweight and fast, but as primarily capturing speech presence (sentence truncated here); voice-activity cues are separately described as lacking semantic understanding.
- The second alternative is only named as "ASR-based" before the chunk cuts off, so its stated properties and no numbers, tables, or mechanisms are available in this chunk.
---
## Title block (verbatim as present)
Full title as printed in the chunk:
> "FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection"
Authors as printed: Chengyou Wang, Hongfei Xue, Mingchen Shao, Chunjiang He, Jingbin Hu, Shuiyuan Wang, Bo Wu, Yuyu Ji, Jimeng Zheng, Ruofei Chen, Zhou Zhu, Lei Xie; affiliations: Audio, Speech and Language Processing Group (ASLP@NPU), Shengwang, QualiaLabs; contacts: asd6404112a@mail.nwpu.edu.cn, lxie@nwpu.edu.cn.
## Abstract fragment (verbatim, truncated)
> "Recent advances in AudioLLMs have enabled spoken dialogue systems to move beyond turn-based interaction toward real-time full-duplex communication, where the agent must decide when to speak, yield, or interrupt while the user is still talking. Existing full-duplex approaches either rely on voice activity cues, which lack semantic understanding, or on ASR-based"
No tables, numbers, or equations are present in this chunk.
## Introduction fragment (verbatim, truncated)
> "In practical deployments, existing full-duplex spoken dialogue systems [9, 10] often rely on turn detection to provide a controllable interface between speech processing and response generation. Current turn detection approaches can be broadly categorized into two groups. The first group relies on voice activity detection (VAD) and infers interruption timing from acoustic energy or activity patterns [11, 12, 13]. These methods are lightweight and fast, but primarily capture speech presence"
The chunk ends mid-sentence here ("speech presence" with no continuation); no further claims, numbers, or citations are available in this chunk.
**Covers:** Paper framing: full-duplex turn-taking problem, VAD vs ASR baselines, FastTurn contribution summary (chunk 01-fastturn-unifying-acoustic-and-streaming-semanti; source text truncated as noted above)
