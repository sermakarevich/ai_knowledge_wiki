[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Table 9: Decision-disagreement rate by signal
**In one sentence:** The judge gate picks the worse agent (lower verifiable reward) in 31.0% of near-equal pairs but only 0.9% of wide pairs, and no cheaper or combined signal fixes this because the errors are specific to each signal, not shared noise.
## Key points
- Table 9 measures "fraction of pairs where the gate promotes the lower-reward agent," split into near-equal pairs (reward gap |ΔR| (absolute reward difference) < 0.1, n=87) versus wide pairs (|ΔR| ≥ 0.1, n=211), with 2 exact-tie pairs excluded from 300 total.
- The main judge (Opus-4.8) has a near-equal disagreement rate of 31.0%, with a base-model cluster-bootstrap 95% CI (confidence interval, the uncertainty range) of [11.6, 50.0].
- Even the low end of that range (11.6%) is still about 13× the wide-pair rate of 0.9%, so close pairs are far more error-prone than clearly separated pairs.
- The result survives removing the least-independent pairs: on the 75 cross-base-model pairs only, the rate is 32.0% (24/75).
- The errors are signal-specific, not one shared ranking mistake: of 60 near-equal pairs flipped by at least one of five signals, only 4 are flipped by all five and 22 by exactly one, with mean pairwise Jaccard (overlap between flip sets) 0.40.
- Section G tests 21 cheaper candidate signals — single judges, the process-blind proxy, the completion bit, and unweighted and confidence-weighted judge ensembles — and none beats the best single judge on near-equal pairs.
- Averaging all four judges gives exactly 31.0% (27/87), identical to the best single judge, because the judges are highly correlated (pairwise ρ (rank correlation) 0.67–0.98) and flip the same close pairs.
---
## What Table 9 counts
Table 9 reports the decision-disagreement rate by signal: "fraction of pairs where the gate promotes the lower-reward agent, on near-equal (|∆R| < 0.1, n=87) vs. wide (|∆R| ≥ 0.1, n=211) pairs; the 2 exact-tie pairs of the ... 300 are excluded."
## Main rate and uncertainty
The chunk "puts the primary Opus-4.8 near-equal rate at 31.0%, 95% CI [11.6, 50.0], its lower bound still ∼13× the 0.9% wide-pair rate."
The CI (confidence interval) is described as "Base-model cluster-bootstrap 95% CI on the Opus-4.8 near-equal rate: [11.6, 50.0]."
## Robustness to pair independence
"dropping the least-independent same-base-model temperature pairs leaves 32.0% on the 75 cross-base-model pairs (24/75)."
## Signal-specific, not shared noise
"The disagreement is also signal-specific rather than shared ordering noise: of the 60 near-equal pairs flipped by at least one of the five signals, only 4 are flipped by all five and 22 by exactly one (mean pairwise Jaccard 0.40), so the 31% is a population-level, signal-specific property, not shared reference-ranking noise."
## Cheap signals do not fix it
"We test whether any cheaper signal removes the near-equal decision error of §4.2 without the paid audit. Across 21 candidate signals, spanning single judges, the process-blind proxy, the completion bit, and unweighted and confidence-weighted judge ensembles, none outperforms the best single judge on near-equal pairs."
"Averaging all four judges gives exactly 31.0% (27/87), identical to the best single judge, because the judges are highly correlated (pairwise ρ 0.67–0.98) and flip the same close pairs."
**Covers:** Decision-disagreement (near-equal pair) rates broken down by evaluation signal
