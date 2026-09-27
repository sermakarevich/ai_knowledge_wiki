[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Computer Science > Computation and Language
**In one sentence:** The arXiv Computation and Language listing identifies [2608.10878] X2-Turn as a frame-synchronous dual-head method for joint streaming ASR and turn state prediction, built on Voxtral Realtime and evaluated on bilingual EasyTurn and Full-Duplex-Bench.
## Key points
- The listed title is "X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction" under arXiv ID 2608.10878 (cs).
- The listed authors are Kaiqi Fu, Rime Wen, Altman Lin, Shawn Qin, Roy Gan, Hao Wang, and Qian Wang (7 authors).
- The abstract states the method adds a frame-synchronous turn state head operating in parallel with the ASR head on shared streaming representations, jointly predicting ASR tokens and fine-grained turn states at the frame level.
- The abstract frames the problem as real-time distinction between user interruptions, backchannels that should be ignored, and utterance completion in spoken dialogue systems.
- The abstract claims experiments on bilingual EasyTurn and Full-Duplex-Bench show an effective trade-off between turn state accuracy and decision latency.
- The listed subjects are Computation and Language (cs.CL) and Audio and Speech Processing (eess.AS), cited as arXiv:2608.10878 [cs.CL].
- The version history lists v1 submitted 11 Aug 2026 (1,280 KB), v2 on 19 Aug 2026 (943 KB), and v3 last revised 8 Sep 2026 (923 KB).
---
## Paper identity
**Covers:** chunk lines 15–37 (arXiv ID, title, authors, subjects, citation)

| Field | Value |
|---|---|
| arXiv ID | 2608.10878 (cs) |
| Title | X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction |
| Authors | Kaiqi Fu, Rime Wen, Altman Lin, Shawn Qin, Roy Gan, Hao Wang, Qian Wang |
| Subjects | Computation and Language (cs.CL); Audio and Speech Processing (eess.AS) |
| Cite as | arXiv:2608.10878 [cs.CL] (or arXiv:2608.10878v3 [cs.CL] for this version) |
| DOI | https://doi.org/10.48550/arXiv.2608.10878 |

## Abstract (verbatim claim)
**Covers:** chunk line 29

> "Accurate and responsive turn-taking is essential for spoken dialogue systems, which must distinguish in real time between user interruptions, backchannels that should be ignored, and the completion of an utterance. Prior modular approaches typically optimize turn state prediction at the utterance or fixed-chunk level, creating a mismatch with the continuous turn state estimate, and often depend on an auxiliary ASR model, which limits responsiveness and increases overall system complexity. Therefore, we present X2-Turn, a frame-synchronous turn state prediction method via delayed-stream modeling. Specifically, building on the pretrained Voxtral Realtime model, we introduce a frame-synchronous turn state head that operates in parallel with the ASR head on shared streaming representations, jointly predicting ASR tokens and fine-grained turn states at the frame level. Experiments on bilingual EasyTurn and Full-Duplex-Bench demonstrate that the proposed method achieves an effective trade-off between turn state accuracy and decision latency."

## Submission history
**Covers:** chunk lines 45–56

| Version | Date (UTC) | Size |
|---|---|---|
| v1 | Tue, 11 Aug 2026 12:54:52 | 1,280 KB |
| v2 | Wed, 19 Aug 2026 03:16:50 | 943 KB |
| v3 (this version) | Tue, 8 Sep 2026 12:28:34 | 923 KB |

From: Kaiqi Fu. Submitted 11 Aug 2026 (v1), last revised 8 Sep 2026 (v3).

## Browse and access context
**Covers:** chunk lines 58–90 (full-text links, browse context)

- Full-text links listed: PDF, HTML (experimental), TeX Source, view license.
- Current browse context: cs.CL (prev | next; new | recent | 2026-08).
- Change-to-browse options listed: cs, eess, eess.AS.
- No paper results, methods, numbers, or figures beyond the abstract claim are present in this chunk.
