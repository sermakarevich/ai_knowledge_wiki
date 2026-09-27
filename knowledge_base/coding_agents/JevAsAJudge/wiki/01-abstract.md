> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure — Abstract
**In one sentence:** A cheap decision-only judge (TypeSafe JEV) stays within about three points of a state-of-the-art LLM judge on ordinary preference and factuality at 0.36% of its fee but falls far behind on derivation-checking and style-adversarial judgments, so a frozen cascade that accepts confident JEV verdicts and escalates uncertain ones retains ~99% of the stronger judge's accuracy at lower fee.
## Key points
- On ordinary preference (400-pair RewardBench sample), JEV scores 92.2% vs GPT-6 Astra 93.5% (paired difference −1.25 pp, 95% cluster interval [−3.8, 1.5]) at 0.36% of the comparator's fee.
- Gaps widen on demanding judgments: JudgeBench 78.6% vs 93.1%, and RM-Bench hard pairs (elaborately written wrong answers) 74.8% vs 94.6%.
- JEV returns a typed verdict plus probabilities over allowed labels; comparison is between complete configurations (JEV is proprietary, not compute-matched), and typed probabilities alone do not establish calibration.
- Routing signal is q = max probability over allowed labels: accept JEV's verdict above a threshold, otherwise escalate to a stronger LLM; pairwise uses both orders with order-aligned, averaged probabilities.
- GPT-6's advantage is concentrated in JEV's low-confidence cases (990 base-order judgments show accuracy generally rising across confidence bins), but confidence is less effective on style-adversarial RM-Bench pairs.
- Frozen offline cascade at τ=0.9 (JEV→GPT-6) accepts 53.7% of 510 held-out extension preference pairs, reaching 92.5% vs 93.1% for GPT-6 alone (~99%) at 56.8% of GPT-6's fee (62.2% conservative bound).
- Thresholds are workload-specific and do not transfer universally: selected on 96 pilot pairs (64 RewardBench + 32 JudgeBench) for max coverage within 2 points of fallback accuracy; e.g. frozen GPT-5.6 policy accepts 81.0% at τ=0.7 but loses 2.35 points; live latency not measured.
---
## Abstract
The paper frames LLM-as-a-judge as costly at scale with unreliable confidence, and asks whether a decision-only judge can serve as an economical first pass that flags when stronger evaluation is needed. Tested against sixteen generative and reward-model judges with blinded human adjudication, JEV lands "within three percentage points of a state-of-the-art LLM judge, our strongest comparator, on ordinary preference and evidence-grounded factuality at 0.36% of the comparator's fee", while "[l]arger gaps arise when judgments require checking a derivation or resisting an elaborately written wrong answer." The gap to the comparator "is concentrated in low-confidence decisions", and "[a] frozen cascade that accepts confident verdicts and escalates uncertain ones retains 99% of the comparator's accuracy at lower cost."

**Covers:** paper abstract (alphaXiv page header + Abstract section)
## A cheap first pass, with limits
The first judge is TypeSafe JEV: structured inputs + rubric in, typed verdict + probabilities over allowed labels out. The chunk stresses this is an empirical test of accuracy, confidence, and operating cost together — not a compute-matched architectural comparison, since JEV is proprietary.

| Workload | JEV | GPT-6 (Astra) | Gap |
|---|---|---|---|
| RewardBench sample (400 pairs, ordinary preference) | 92.2% | 93.5% | −1.25 pp, 95% cluster interval [−3.8, 1.5] |
| JudgeBench (derivation-checking) | 78.6% | 93.1% | −14.5 pp |
| RM-Bench hard pairs (elaborately written rejected answer) | 74.8% | 94.6% | −19.8 pp |

Takeaway stated in chunk: cheap first pass suffices for routine preference; derivation-checking and misleading-style cases support escalation, but "do not support a claim that all difficult tasks fail in the same way."

**Covers:** "A cheap first pass, with limits" subsection
## Confidence as a routing signal
Mechanism: q = largest probability JEV assigns to any allowed label. Rule: if q above threshold → accept JEV verdict; else → ask stronger LLM and use its verdict. Pairwise comparisons judge both candidate orders, align probabilities to the same semantic response, and average before gating. Threshold is fit on pilot data, "not assumed to transfer universally."

Evidence for the signal: on 990 base-order judgments JEV accuracy generally rises across confidence bins, and "GPT-6's advantage is concentrated in JEV's less-confident cases." Caveats: "confidence is a useful ranking signal, but it is not a certificate of correctness", and "[o]n style-adversarial RM-Bench pairs, JEV's confidence is less effective at identifying errors."

**Covers:** "Confidence as a routing signal" subsection
## What the frozen test shows
The main cascade evidence is a frozen, offline test:

- Threshold selection: per fallback model, on 96 pilot selection pairs (64 RewardBench + 32 JudgeBench), seeking maximum coverage while keeping selection accuracy within two points of that fallback; invalid JEV outputs defer to fallback.
- Evaluation: two-order policy on 510 extension preference pairs not used for fitting.
- Result: at τ=0.9, JEV→GPT-6 cascade accepts 53.7% of pairs, reaches 92.5% accuracy vs 93.1% for GPT-6 alone (≈99%), at 56.8% of GPT-6's reported fee (62.2% under conservative bound).
- Limits: thresholds are workload-specific — "one policy does not transfer as intended" (frozen GPT-5.6 policy accepts 81.0% at τ=0.7 but loses 2.35 points); live sequential latency not measured; measurements do not establish reduced generated tokens or live cascade latency.

Established contribution per chunk: "an empirical operating profile of a cheap, decision-only judge paired with confidence-based escalation" whose threshold "must be validated locally for each workload and fallback."

**Covers:** "What the frozen test shows" subsection + AI Overview two-step framing
