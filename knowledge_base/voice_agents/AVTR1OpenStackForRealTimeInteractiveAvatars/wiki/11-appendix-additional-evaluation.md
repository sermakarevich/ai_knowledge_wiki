> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix additional evaluation
**In one sentence:** The appendix adds qualitative listening comparisons (Figures 7–8), full SI-184 corpus processing statistics (184 videos → 1,457 scored segments, 3.46 hours), and ablations showing the motion-metric pattern holds across LivePortrait features (Table 8) and full-frame scoring (Tables 9–10).
## Key points
- Qualitative comparison (Appendix A, Figures 7–8): reactive-listening frames on the Seamless Interaction test set — recorded speaker and listener rows followed by each system's generated listener, columns anchored to speaker times with per-video timestamps.
- Corpus processing (Appendix B): SI configuration vendor V00, interaction_type ipc_conversation, label improvised, split test; broader selection holds 186 videos but two grounded_gesture videos (V00_S2050_I00001256, participants P1307A/P1308A, a physical performance rather than conversation) are excluded by the interaction_type filter.
- Frame accounting: 184 videos = 1,284,704 frames / 42,823 s (11.90 hours) at 30 fps, per-video 138–346 s (quartiles 212/233/233/257 s); listening segments from ground-truth voice activity (listener silent, speaker active ≥ once) with tracking-success, 0.2 s trim, ≥4 s, and history-masking filters leave 177 videos, 1,457 segments, 311,776 frames on the 25 fps grid = 3.46 hours, mean segment 8.6 s; seven videos contribute no valid segment.
- LivePortrait-feature VAD-masked repeat (Table 8): same pattern as EMOCA — talking-head generators among top ranks (SoulX Pro expression PFD 0.633, SoulX Lite expression rPCC 0.098); AVTR-1 expression PFD 0.671, rotation PFD 3.967; the motion-metric limitation is not representation-dependent.
- Full-frame EMOCA scoring (Table 9, all tracked frames): AVTR-1 leads dyadic systems with expression rPCC 0.063, PFD 19.85, SID 5.096, Var 1.432 — closest to ground truth (0/0/5.251/1.552) on most components.
- Full-frame LivePortrait scoring (Table 10): same protocol with LivePortrait features, extending the frame-set ablation across both representations.
---
## What the appendix proves
The headline limitation of motion-based metrics survives both ablations: changing features (EMOCA → LivePortrait) and changing frame sets (VAD-masked → full-frame) does not rescue motion similarity as a test of speech dependence — which is exactly the gap R-DGG is built to fill.
**Covers:** appendix tables and additional evaluation details.
