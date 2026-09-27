> [[index|Wiki]] | [[summary|Summary]]
# [2608.10878] X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction — Digest

## 1. [[wiki/01-computer-science-computation-and-language|Computer Science > Computation and Language]]
**In one sentence:** The arXiv Computation and Language listing identifies [2608.10878] X2-Turn as a frame-synchronous dual-head method for joint streaming ASR and turn state prediction, built on Voxtral Realtime and evaluated on bilingual EasyTurn and Full-Duplex-Bench.
## Key points
- The listed title is "X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction" under arXiv ID 2608.10878 (cs).
- The listed authors are Kaiqi Fu, Rime Wen, Altman Lin, Shawn Qin, Roy Gan, Hao Wang, and Qian Wang (7 authors).
- The abstract states the method adds a frame-synchronous turn state head operating in parallel with the ASR head on shared streaming representations, jointly predicting ASR tokens and fine-grained turn states at the frame level.
- The abstract frames the problem as real-time distinction between user interruptions, backchannels that should be ignored, and utterance completion in spoken dialogue systems.
- The abstract claims experiments on bilingual EasyTurn and Full-Duplex-Bench show an effective trade-off between turn state accuracy and decision latency.
- The listed subjects are Computation and Language (cs.CL) and Audio and Speech Processing (eess.AS), cited as arXiv:2608.10878 [cs.CL].
- The version history lists v1 submitted 11 Aug 2026 (1,280 KB), v2 on 19 Aug 2026 (943 KB), and v3 last revised 8 Sep 2026 (923 KB).

## The argument in five moves
1. Spoken dialogue systems need accurate, responsive turn-taking that distinguishes in real time between user interruptions, ignorable backchannels, and utterance completion.
2. Prior modular approaches predict turn state at the utterance or fixed-chunk level and often depend on an auxiliary ASR model, creating a mismatch with the continuous turn state estimate while limiting responsiveness and increasing complexity.
3. X2-Turn answers with frame-synchronous dual-head modeling via delayed-stream modeling: building on pretrained Voxtral Realtime, a turn state head runs in parallel with the ASR head on shared streaming representations.
4. The two heads jointly predict ASR tokens and fine-grained turn states at the frame level, aligning recognition and turn estimation in the streaming frame loop.
5. Bilingual EasyTurn and Full-Duplex-Bench experiments are claimed to show an effective trade-off between turn state accuracy and decision latency, with the listing carried as arXiv:2608.10878 [cs.CL] (cs.CL + eess.AS) across v1–v3 revisions.
