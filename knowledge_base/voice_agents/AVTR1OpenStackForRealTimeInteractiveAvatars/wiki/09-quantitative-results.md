> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Quantitative results
**In one sentence:** AVTR-1 leads the compared dyadic systems on visual quality (FID 14.3, FVD 76.8, CSIM 0.94) and most conventional listening metrics while staying competitive on lip sync, and its R-DGG interval sits above zero like the other dyadic systems and ground truth — unlike every talking-head generator — though the dyadic intervals overlap so no ranking among them is supported.
## Key points
- Visual quality + lip sync (Table 5a, SI-184): AVTR-1 FID 14.3 / FVD 76.8 / CSIM 0.94 / LSE-D 7.08 / LSE-C 3.28 — best among dyadic systems on all visual metrics (AvatarForcing* 14.4/85.8/0.77, DyStream 43.1/119.4/0.87) and competitive on lip sync (DyStream leads LSE-D 6.57, AVTR-1 leads LSE-C among dyadic), against talking-head bests (SoulX Pro FID 9.4/FVD 53.6, Ditto CSIM 0.95).
- Conventional listening, dyadic-only (Table 5b): AVTR-1 leads rPCC (0.083/0.140 exp/pose), PFD (25.98/6.417), expression SID (4.970) and expression Var (1.313) with pose Var 0.930 vs. ground truth 1.789 — closest-to-ground-truth on most components.
- Motion-metric limitation (Table 6, VAD-selected frames incl. talking-head generators): talking-head systems take both highlighted ranks on every rPCC/PFD component and on expression SID/Var; dyadic methods lead only pose SID/Var — motion similarity does not establish paired-speech dependence (LivePortrait-feature repeat in Appendix C.1 agrees).
- R-DGG (Table 7, ×10⁻⁴ nats): AVTR-1 0.57 [0.19, 0.98] p = 0.002; AvatarForcing* 0.32 [0.07, 0.56] p = 0.008; DyStream 0.48 [0.06, 0.93] p = 0.011; ground truth 0.72 [0.32, 1.12] p < 0.001; GT×other −0.11 [−0.56, 0.45] p = 0.659; Ditto 0.06, FLOAT 0.01, SoulX Lite −0.22, SoulX Pro 0.18 — all talking-head intervals include zero.
- Validation passes: ground-truth interval above zero, both negative-control types include zero, all three dyadic systems above zero — so R-DGG indicates speech dependence for dyadic outputs but not for talking-head or mismatched pairs; overlapping dyadic intervals admit no reliable ranking among the three.
- Bottom line per the paper: AVTR-1 combines visual/speaking quality comparable to evaluated systems with listening motion predictively related to the paired speaker's speech.
---
## Numbers to quote
Headline dyadic-leadership figures: FID 14.3, FVD 76.8, CSIM 0.94 (Table 5a); expression PFD 25.98 (Table 5b); R-DGG 0.57 [0.19, 0.98] ×10⁻⁴ nats, p = 0.002 (Table 7).
**Covers:** quantitative comparisons on visual quality, lip sync, and listening motion.
