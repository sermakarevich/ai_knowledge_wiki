[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Turn-Completion Evaluation — The Detectors Do Not Score

**In one sentence:** Detectors are compared as complete causal policies at their native gates rather than on identical silence, where the locked V1 test shows historical Voice-Light step 3,500 with low false cutoffs but only 12.53% EOT recall, and V2 validation fails its joint gate so its test split remains sealed.

## Key points

- Voice-Light emits its boundary score at 80 ms, Smart Turn at 240 ms, LiveKit at 320 ms, and Silero updates a silence proxy on 32 ms chunks, so comparisons evaluate complete causal policies at native gates rather than isolating model quality under identical acoustic evidence.
- Implementations are pinned to Silero VAD 6.2.1, Pipecat Smart Turn v3.2, and LiveKit v1-mini, with possible training-source overlap making Smart Turn contextual only.
- In the locked real-conversation V1 test under the original yield-target protocol, Voice-Light (historical step 3,500) had 2.70% false cutoffs (1/37 HOLD errors), 12.53% EOT recall, and 770 ms mean latency including timeout actions, at threshold 0.90, 560 ms minimum delay, and 800 ms timeout.
- Baselines on the same locked V1 test reached 95.60% EOT recall (Silero) and 91.50% (LiveKit) at the same 2.70% false-cutoff rate and lower mean latencies (656 ms and 654 ms), while Smart Turn had 13.51% false cutoffs (5/37) with 20.72% recall and 684 ms mean latency.
- The V2 semantic-completion validation inventory contains 1,005 soft targets and 789 clean hard labels (134 HOLD and 655 EOT), with 216 ambiguous cases excluded from hard scoring.
- Historical step 3,500 achieved AUROC 0.6866, 65.80% recall, 3.73% false cutoffs, and 2.0 s p95 latency on V2 validation, but its BCE of 0.6719 and Brier score of 0.1843 were worse than the constant soft-prior baseline (0.5847 and 0.1453) despite above-chance ranking.
- No swept detector met the joint gate of at most 5% false cutoff, at least 70% recall, and at most 800 ms p95 latency, so the V2 test split remained sealed; a completion-primary retrain improved calibration but still missed the gate, and longer training reduced recall.

---

## Native gates, not identical silence

The detectors do not score after identical amounts of silence. Per the chunk:

> "Voice-Light emits its boundary score at 80 ms, Smart Turn at 240 ms, LiveKit at 320 ms, and Silero updates a silence proxy on 32 ms chunks."

> "Comparisons therefore evaluate complete causal policies at their native gates rather than isolating model quality under identical acoustic evidence."

The implementations are pinned to Silero VAD 6.2.1, Pipecat Smart Turn v3.2, and LiveKit v1-mini [21, 22, 23].

## Locked V1 test (Table 4)

Table 4: Locked real-conversation test under the original V1 yield-target protocol. Mean latency includes timeout actions. VL is historical Voice-Light step 3,500; policy values are threshold, minimum delay, and timeout. Possible training-source overlap makes Smart Turn contextual only.

| Metric | VL | Silero | Smart | LiveKit |
|---|---|---|---|---|
| False cutoff | 2.70% | 2.70% | 13.51% | 2.70% |
| HOLD errors (𝑛 = 37) | 1 | 1 | 5 | 1 |
| EOT recall | 12.53% | 95.60% | 20.72% | 91.50% |
| Mean latency | 770 ms | 656 ms | 684 ms | 654 ms |
| Threshold | 0.90 | 0.05 | 0.95 | 0.15 |
| Minimum delay | 560 ms | 640 ms | 80 ms | 640 ms |
| Timeout | 800 ms | 800 ms | 800 ms | 800 ms |

## V2 semantic-completion validation and the sealed test

The V2 semantic-completion validation inventory contains 1,005 soft targets and 789 clean hard labels: 134 HOLD and 655 EOT examples, with 216 ambiguous cases excluded from hard scoring.

Historical step 3,500 achieved AUROC 0.6866, 65.80% recall, 3.73% false cutoffs, and 2.0 s p95 latency. Its BCE of 0.6719 and Brier score of 0.1843 were worse than the constant soft-prior baseline (0.5847 and 0.1453), despite above-chance ranking.

No swept detector met the joint gate of at most 5% false cutoff, at least 70% recall, and at most 800 ms p95 latency, so the V2 test split remained sealed. A completion-primary retrain improved calibration but still missed the gate; longer training reduced recall.

**Covers:** §4 native gates (VL 80 ms, Smart Turn 240 ms, LiveKit 320 ms, Silero 32 ms chunks; Silero VAD 6.2.1, Smart Turn v3.2, LiveKit v1-mini); Table 4 locked V1 test (false cutoff, HOLD errors, EOT recall, mean latency, threshold, minimum delay, timeout); V2 validation inventory (1,005 soft / 789 hard: 134 HOLD + 655 EOT, 216 ambiguous), step-3,500 AUROC/recall/calibration vs. soft-prior baseline, joint gate and sealed test.
