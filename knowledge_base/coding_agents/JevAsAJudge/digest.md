> [[index|Wiki]] | [[summary|Summary]]
# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv — Digest
## 1. [[wiki/01-abstract|Abstract]]
**In one sentence:** A cheap decision-only judge (TypeSafe JEV) stays within about three points of a state-of-the-art LLM judge on ordinary preference and factuality at 0.36% of its fee but falls far behind on derivation-checking and style-adversarial judgments, so a frozen cascade that accepts confident JEV verdicts and escalates uncertain ones retains ~99% of the stronger judge's accuracy at lower fee.
## Key points
- On ordinary preference (400-pair RewardBench sample), JEV scores 92.2% vs GPT-6 Astra 93.5% (paired difference −1.25 pp, 95% cluster interval [−3.8, 1.5]) at 0.36% of the comparator's fee.
- Gaps widen on demanding judgments: JudgeBench 78.6% vs 93.1%, and RM-Bench hard pairs (elaborately written wrong answers) 74.8% vs 94.6%.
- JEV returns a typed verdict plus probabilities over allowed labels; comparison is between complete configurations (JEV is proprietary, not compute-matched), and typed probabilities alone do not establish calibration.
- Routing signal is q = max probability over allowed labels: accept JEV's verdict above a threshold, otherwise escalate to a stronger LLM; pairwise uses both orders with order-aligned, averaged probabilities.
- GPT-6's advantage is concentrated in JEV's low-confidence cases (990 base-order judgments show accuracy generally rising across confidence bins), but confidence is less effective on style-adversarial RM-Bench pairs.
- Frozen offline cascade at τ=0.9 (JEV→GPT-6) accepts 53.7% of 510 held-out extension preference pairs, reaching 92.5% vs 93.1% for GPT-6 alone (~99%) at 56.8% of GPT-6's fee (62.2% conservative bound).
- Thresholds are workload-specific and do not transfer universally: selected on 96 pilot pairs (64 RewardBench + 32 JudgeBench) for max coverage within 2 points of fallback accuracy; e.g. frozen GPT-5.6 policy accepts 81.0% at τ=0.7 but loses 2.35 points; live latency not measured.
## The argument in five moves
1. LLM-as-a-judge is costly at scale with unreliable confidence, so the paper asks whether a cheap decision-only judge can serve as an economical first pass that flags when stronger evaluation is needed.
2. TypeSafe JEV (structured inputs + rubric in, typed verdict + probabilities out) nearly matches GPT-6 Astra on routine preference (92.2% vs 93.5% at 0.36% of the fee) but trails badly where judgments require checking a derivation or resisting an elaborately written wrong answer.
3. JEV's max-label probability q offers a routing signal — accept above a threshold, escalate below — with accuracy generally rising across confidence bins and the stronger judge's advantage concentrated in low-confidence cases, though the signal weakens on style-adversarial pairs.
4. A frozen offline cascade (threshold fit on 96 pilot pairs, tested on 510 held-out extension pairs) confirms the operating point: at τ=0.9 the JEV→GPT-6 cascade accepts 53.7% of pairs and reaches 92.5% vs 93.1% (~99%) at 56.8% of GPT-6's fee.
5. The result is an empirical operating profile, not a universal policy: thresholds must be validated locally per workload and fallback, since transferred policies can lose accuracy and live latency/token savings are unmeasured.
