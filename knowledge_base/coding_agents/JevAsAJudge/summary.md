# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv

**Article:** [JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://www.alphaxiv.org/abs/2609.26550) — alphaXiv, September 2026

## Human Readable TL;DR

Imagine a junior triage nurse who handles all the routine checkups cheaply and quickly but sends anything that looks uncertain to a senior doctor. That is what TypeSafe JEV does here: it judges easy preference comparisons almost as well as a far more expensive AI judge at a tiny fraction of the fee, but it stumbles on trickier cases like checking step-by-step derivations or resisting a beautifully written but wrong answer. The paper's fix is a simple confidence rule: when JEV's own confidence is high, keep its verdict, and when it is unsure, escalate to the stronger model. With that frozen rule in place, the combined system keeps about 99% of the strong judge's accuracy while sending only about half the cases upstairs, cutting the bill substantially.

## TL;DR

The paper tests TypeSafe JEV, a cheap decision-only judge that returns a typed verdict plus probabilities over allowed labels, against sixteen generative and reward-model judges with blinded human adjudication, using GPT-6 Astra as the strongest comparator. On ordinary preference (a 400-pair RewardBench sample) JEV reaches 92.2% versus 93.5% for GPT-6, a gap of about 1.25 points, at roughly 0.36% of the comparator's fee, but the gap widens sharply on derivation-checking JudgeBench and style-adversarial RM-Bench hard pairs. Because GPT-6's advantage concentrates in JEV's low-confidence decisions, a frozen offline cascade that accepts confident JEV verdicts and escalates the rest retains about 99% of GPT-6's accuracy at lower cost. Thresholds are workload-specific and must be validated locally rather than assumed to transfer.

---

## Problem & Motivation

Large-scale LLM-as-a-judge evaluation is expensive, and the confidence signals of generative judges are often unreliable, so running the strongest judge on every pair wastes money on routine cases that a cheaper judge could handle. The paper asks whether a decision-only judge can serve as an economical first pass that both renders verdicts and flags when stronger evaluation is actually needed. This frames the contribution as an empirical operating profile of accuracy, confidence, and cost together, rather than a compute-matched architectural comparison, since JEV itself is proprietary. The practical goal is a cascade policy that maximizes the share of cases decided cheaply while staying within a small accuracy tolerance of the strong fallback judge.

## Main Original Ideas

1. **Decision-only judge as first pass.** The paper treats TypeSafe JEV, which takes structured inputs plus a rubric and returns only a typed verdict with probabilities over allowed labels, as a complete economical configuration to be profiled against full generative judges on accuracy, confidence quality, and operating cost rather than on matched compute.

2. **Confidence-gated escalation with two-order averaging.** The routing signal is q, the maximum probability JEV assigns to any allowed label, and the rule is to accept JEV's verdict above a threshold and otherwise defer to the stronger LLM. For pairwise comparisons both candidate orders are judged, the probabilities are aligned to the same semantic response, and then averaged before gating, with invalid JEV outputs deferring to the fallback.

3. **Frozen pilot-fitted cascade evaluated on held-out pairs.** Thresholds are selected per fallback model on a small pilot set, seeking maximum coverage while keeping selection accuracy within two points of that fallback, and the resulting fixed policy is then evaluated on disjoint extension pairs. This frozen offline design is presented as the honest test of whether confidence-based routing survives contact with unseen data rather than merely fitting the pilot.

## Key Findings

On routine preference the cheap judge is nearly interchangeable with the strong one: JEV scores 92.2% against GPT-6 Astra's 93.5% on the 400-pair RewardBench sample, a paired difference of −1.25 points with a 95% cluster interval of [−3.8, 1.5], at about 0.36% of the comparator's fee. The picture changes on demanding judgments, where JEV falls to 78.6% versus 93.1% on JudgeBench derivation-checking and to 74.8% versus 94.6% on RM-Bench hard pairs with elaborately written wrong answers. The chunk stresses that these results support escalation for derivation-checking and misleading-style cases but do not support a blanket claim that all difficult tasks fail the same way.

Confidence proves to be a useful but imperfect routing signal. Across 990 base-order judgments, JEV accuracy generally rises across confidence bins, and GPT-6's advantage is concentrated in JEV's less-confident cases, which is exactly the property a cascade needs. At the same time, typed probabilities alone do not establish calibration, confidence is described as a ranking signal rather than a certificate of correctness, and on style-adversarial RM-Bench pairs JEV's confidence is notably less effective at identifying its own errors.

The frozen cascade test delivers the headline cost result. With the threshold fitted on 96 pilot selection pairs (64 RewardBench plus 32 JudgeBench) and evaluated on 510 held-out extension preference pairs, the JEV-to-GPT-6 cascade at τ=0.9 accepts 53.7% of pairs and reaches 92.5% accuracy versus 93.1% for GPT-6 alone, or roughly 99%, at 56.8% of GPT-6's reported fee (62.2% under a conservative bound). The limits are stated plainly: thresholds are workload-specific and one policy does not transfer as intended, as shown by a frozen GPT-5.6 policy that accepts 81.0% at τ=0.7 but loses 2.35 points, and live sequential latency and generated-token savings were not measured.

## Suggestions & Future Directions

The clearest direction from the chunk is local validation: because thresholds are workload-specific, any deployment should refit and revalidate the confidence threshold on its own workload and fallback model rather than importing the paper's τ=0.9. Further work should probe calibration and ranking quality of JEV confidence more rigorously, especially on style-adversarial cases where the signal weakens, and test whether richer routing features beyond the top probability improve escalation decisions. Finally, the cost story needs live-system confirmation, including sequential latency, token savings, and fee bounds under production conditions, before the offline fee ratios can be read as deployment savings.

## Authors & Institutions

The wiki chunk used for this summary does not record author names or institutional affiliations, so they are omitted here rather than inferred. The comparison configurations named in the chunk are TypeSafe JEV as the cheap decision-only judge and GPT-6 Astra (alongside a GPT-5.6 fallback policy) as the stronger comparators, evaluated with blinded human adjudication across sixteen judge configurations.
