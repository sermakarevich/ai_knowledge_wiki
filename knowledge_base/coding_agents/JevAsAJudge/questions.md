---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv
### Q1. What problem does the paper set out to solve, and what role does it propose for a decision-only judge?
> [!tip]- Answer
> Large-scale LLM-as-a-judge evaluation is costly and generative judges give unreliable confidence, so routine pairs waste money on the strongest judge. The paper asks whether a cheap decision-only judge can serve as an economical first pass that both renders verdicts and flags when stronger evaluation is needed. This frames the contribution as an empirical operating profile of accuracy, confidence, and cost together rather than a compute-matched architectural comparison. See [[wiki/01-abstract|Abstract]].
### Q2. How does TypeSafe JEV perform against GPT-6 Astra on ordinary preference, and at what relative cost?
> [!tip]- Answer
> On a 400-pair RewardBench sample of ordinary preference, JEV scores 92.2% versus 93.5% for GPT-6 Astra, a paired difference of −1.25 points with a 95% cluster interval of [−3.8, 1.5]. That keeps JEV within about three points of the state-of-the-art comparator at roughly 0.36% of its fee. The chunk stresses this covers routine preference only, not harder judgment types. See [[wiki/01-abstract|Abstract]].
### Q3. Where does the cheap judge fall far behind, and what limit does the paper place on that finding?
> [!tip]- Answer
> Gaps widen sharply on derivation-checking JudgeBench (78.6% vs 93.1%) and on RM-Bench hard pairs with elaborately written wrong answers (74.8% vs 94.6%). These are the cases that motivate escalation rather than cheap acceptance. The paper cautions this does not support a blanket claim that all difficult tasks fail in the same way. See [[wiki/01-abstract|Abstract]].
### Q4. What exactly is the routing signal q, and how is it applied to pairwise comparisons?
> [!tip]- Answer
> The signal q is the largest probability JEV assigns to any allowed label: accept JEV's verdict when q is above a threshold, otherwise escalate to the stronger LLM and use its verdict. For pairwise comparisons both candidate orders are judged, probabilities are aligned to the same semantic response, and then averaged before gating. Thresholds are fit on pilot data and are not assumed to transfer universally. See [[wiki/01-abstract|Abstract]].
### Q5. What evidence supports confidence as a routing signal, and what are its stated caveats?
> [!tip]- Answer
> Across 990 base-order judgments JEV accuracy generally rises across confidence bins, and GPT-6's advantage is concentrated in JEV's less-confident cases — exactly the property a cascade needs. The caveats are that typed probabilities alone do not establish calibration and confidence is a useful ranking signal, not a certificate of correctness. On style-adversarial RM-Bench pairs, JEV's confidence is notably less effective at identifying its own errors. See [[wiki/01-abstract|Abstract]].
### Q6. What does the frozen offline cascade test show at τ=0.9?
> [!tip]- Answer
> Thresholds are selected per fallback model on 96 pilot pairs (64 RewardBench + 32 JudgeBench) to maximize coverage while staying within two points of fallback accuracy, with invalid JEV outputs deferring to fallback. Evaluated on 510 held-out extension preference pairs, the JEV→GPT-6 cascade at τ=0.9 accepts 53.7% of pairs and reaches 92.5% versus 93.1% for GPT-6 alone (~99%) at 56.8% of GPT-6's fee (62.2% conservative bound). Live sequential latency and generated-token savings were not measured. See [[wiki/01-abstract|Abstract]].
### Q7. (Evaluation) Should a team deploy the paper's τ=0.9 cascade policy directly on a new workload? Justify your recommendation.
> [!tip]- Answer
> No — the team should refit and revalidate the threshold locally on its own workload and fallback model rather than importing τ=0.9. Thresholds are workload-specific and transfer can fail, as shown by a frozen GPT-5.6 policy that accepts 81.0% at τ=0.7 but loses 2.35 points. The honest contribution is an empirical operating profile whose policy must be validated locally, with live latency still unmeasured. See [[wiki/01-abstract|Abstract]].
