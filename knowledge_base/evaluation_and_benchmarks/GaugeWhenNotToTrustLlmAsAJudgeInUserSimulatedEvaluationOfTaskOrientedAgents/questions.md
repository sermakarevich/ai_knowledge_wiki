---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents

### Q1. What does the opening chunk of the GAUGE paper actually contain, and what substantive claim can be extracted from it?

> [!tip]- Answer
> It contains only the title block: the title, authors Umesh Bodhwani, Thanh Tran, and Kai Wei with Amazon affiliation, and contact emails. No abstract, method, or result claims are present, so no argument can be extracted from it — fragmentary tokens like "SimArena/" form no complete claim. See [[wiki/01-gauge-overview|GAUGE: When Not to Trust LLM-as-a-Judge]].

### Q2. Describe the de facto offline release gate that GAUGE audits.

> [!tip]- Answer
> Persona-conditioned user-simulators converse with each candidate task-oriented agent, an LLM (Large Language Model)-as-a-judge scores the transcripts, and the higher-scoring variant is promoted. It runs in CI (Continuous Integration) at a few cents per transcript with no labeled production data, and rests on one rarely measured assumption: that the gate ranks variants the way a grounded evaluation would. See [[wiki/02-introduction-and-positioning|Introduction and Positioning]].

### Q3. What does "a gate can be human-validated yet mis-anchored" mean, and why do the paper's three reasons make ranking validity alone insufficient?

> [!tip]- Answer
> It means the judge reproduces human satisfaction scores closely (Opus-4.8 at ρ=0.846 against the panel) while satisfaction itself is decorrelated from task success (ρ=−0.147), so matching humans certifies the wrong construct. Ranking validity alone is insufficient because release decisions live on near-equal pairs where the gate mis-promotes 31% of the time, teams optimizing a satisfaction anchor trigger Goodhart-style divergence, and a satisfaction-anchored accept/reject bar admits agents that fail 48–60% of the time. See [[wiki/02-introduction-and-positioning|Introduction and Positioning]].

### Q4. State GAUGE's formal release-decision quantities and the two validities it separates.

> [!tip]- Answer
> At the release-decision unit (agent a, aggregated over personas p and domains d): agent-level gate G(a) = Ep,d[gate(τ)], verifiable reward R(a) = Ep,d[r(τ)] ∈ [0,1], plus proxy Sproxy(a) and human Shum(a) satisfaction aggregates. Ranking validity is ρ(G, R) — whether the gate orders agents like the verifiable reward — while construct validity is the satisfied-but-failed rate, P(task failed | rated satisfied), with satisfied meaning ≥5/7 or ≥8/10. See [[wiki/03-judge-biases-and-method|Judge Biases and Method]].

### Q5. Why are the policy-aware gate and the process-blind proxy deliberately disjoint, and what does that separation buy the audit?

> [!tip]- Answer
> The gate is an operations-supervisor rubric reading the full transcript including tool calls and goal, scoring policy adherence and task resolution first; the proxy is a first-person shopper seeing only user-visible spoken turns, rating how the conversation felt. Disjoint in role, evidence, and vocabulary, they cannot agree by shared-rubric artifact — so when the gate halves failure risk (AUC 0.73) and the proxy tracks satisfaction into uninformativeness (AUC 0.49), the audit proves evidence access, not model capability, determines reliability. See [[wiki/03-judge-biases-and-method|Judge Biases and Method]].

### Q6. Why is satisfaction "uninformative rather than merely weak" about task success?

> [!tip]- Answer
> Because 57.5% of conversations the blind human panel rated satisfied (≥5/7) had failed the task — statistically indistinguishable from the stratified sample's own 57.3% base failure rate, with transcript-level AUC 0.44, so conditioning on "satisfied" does not lower failure at all. By contrast the policy-aware gate roughly halves failure risk (20.0% of accepted conversations fail vs. 40.2% base, AUC 0.73) while the process-blind proxy behaves like satisfaction (32.7%, AUC 0.49). See [[wiki/04-satisfaction-success-gap|Satisfaction Matches the Base — Only the Policy-Aware Gate Helps]].

### Q7. Why is the satisfaction–success gap not an artifact of the word "satisfaction" or of one rater?

> [!tip]- Answer
> All five blind-panel dimensions (satisfaction, respect, clarity, helpfulness, would-return) are decorrelated from verifiable success (|ρ| ≤ 0.17, overall ρ=−0.147, flat dose-response), so the gap reflects subjective approval in general. It survives dropping any single annotator (56.4–60.5%), holds across five rater populations (47.6–59.5%), and replicates per domain (retail 24.1%, airline 62.1%, math tutoring 38.7%). See [[wiki/04-satisfaction-success-gap|Satisfaction Matches the Base — Only the Policy-Aware Gate Helps]].

### Q8. What is the measured magnitude of same-family judge self-preference, and does it change the agent ranking?

> [!tip]- Answer
> The Opus-4.8 judge inflates Claude agents over GPT-5.5 by a scale-invariant diff-in-diff of +0.75/7 (Sonnet-4.5 shows +0.67/7 against GPT-5.4), yet it leaves the ranking intact: all four judges recover the verifiable-reward ordering (ρ=0.84–0.94) and agree with one another (ρ=0.90–0.98). The ordering is also not a capability artifact — the weakest judge-as-agent (GPT-5.4, reward 0.77) is tied-best as a ranker (ρ=0.94) — and GPT-5.5 grades ≈0.8/7 lower in absolute level while agreeing on order. See [[wiki/05-judge-robustness-and-self-preference|Judge robustness and self-preference]].

### Q9. What is config D7 in the controlled-degradation set, and why is it the sharpest inversion in the paper?

> [!tip]- Answer
> D7 is a step-starved Sonnet-4.5 configuration (max_steps capped at 6) with verifiable reward 0.00, yet it scores the highest human-panel satisfaction of any degraded config (4.64/7) because a trajectory cut off mid-task still reads as helpful turn-by-turn. It sits inside a clean positive control: degraded-tier mean reward 0.05 versus 0.65 for good/medium tiers, while every subjective signal still rates degraded configs mid-scale. See [[wiki/06-reliability-methods-and-references|Reliability methods, references, and appendix evidence]].

### Q10. How can inter-annotator agreement be high while satisfaction inverts success at 56–64% on every dimension?

> [!tip]- Answer
> Krippendorff's α (alpha, an agreement statistic) stays high at 0.76–0.83, so raters agree with each other — but the five dimensions correlate pairwise at 0.61–0.97, meaning they measure roughly one latent "this interaction felt good" factor that is orthogonal to task success. High agreement plus high inversion is therefore consistent: the panel reliably measures felt experience, which simply does not track whether the customer's task got done. See [[wiki/06-reliability-methods-and-references|Reliability methods, references, and appendix evidence]].

### Q11. What does the second-provider simulator swap prove, and what is the correct way to compare its two false-accept rates?

> [!tip]- Answer
> Swapping the user simulator from Sonnet-4.5 to GPT-5.4 (same 12 variants, strata, task ids, rubrics, judge, oracle) keeps the satisfied-but-failed rate far above the 20% null under both simulators (all p < 10⁻⁷), and the full 25-agent re-run preserves ordering (Spearman ρ=0.93, near-equal top-11 ρ=0.51) — so neither finding is a Sonnet-simulator artifact. Each rate must be compared to the null, not to each other, because the harsher GPT-5.4 simulator steers the same agent to lower mean reward (0.21 vs. 0.32), which mechanically shifts the absolute rate. See [[wiki/07-simulator-swap-control|Controlled second-provider simulator swap (Table 7)]].

### Q12. State Table 9's headline result and explain why averaging four judges does not fix it.

> [!tip]- Answer
> The main Opus-4.8 judge promotes the lower-reward agent in 31.0% of near-equal pairs (|ΔR| < 0.1, n=87; 95% CI [11.6, 50.0]) versus only 0.9% of wide pairs — and the low end of that range is still ~13× the wide-pair rate. Averaging all four judges gives exactly 31.0% again because the judges are highly correlated (pairwise ρ 0.67–0.98) and flip the same close pairs; across 21 cheaper candidate signals none beats the best single judge, and flip sets are signal-specific (mean Jaccard 0.40). See [[wiki/08-decision-disagreement-rate|Table 9: Decision-disagreement rate by signal]].

### Q13. You are designing a new persona for the simulator pool. What constraint must it satisfy so the verifiable reward stays valid, and what existing personas model this?

> [!tip]- Answer
> The persona may vary only tone, cooperativeness, pacing, and assertiveness — task facts (reason_for_call, known_info, evaluation_criteria) must stay untouched so the oracle reward is unaffected. Existing models include S1 Cooperative through S5 Terse plus S8 Skeptical negotiator, which adversarially challenges fees and probes loopholes without ever changing the underlying request facts (S6/S7 are defined but unexercised). See [[wiki/09-annotation-and-prompt-instructions|Annotation and Prompt Instructions: Entire Conversation, Personas, and Evaluation Substrates]].

### Q14. The retail τ2 case scores Gate 7/7 with reward 0.0, while the math-tutoring case scores human 10/10 with the gate at 1/7. What do these two cases jointly demonstrate?

> [!tip]- Answer
> Both show the satisfied-but-failed mechanism — the user ends satisfied (###STOP### / thanks) while the end-state is wrong — but from opposite sides: in retail, 12 of 13 correct tool calls and one never-modified pending order produce a flawless-feeling interaction the gate misses, while in math tutoring the policy-aware gate catches an arithmetic error (shown work implies 330, tutor states 165) the human rater missed. Jointly they show the rubric's priority order — policy adherence first, then task resolution, efficiency, professionalism, scoring only the assistant — makes the gate evidence-driven rather than infallible, succeeding exactly where transcript-only feel fails. See [[wiki/10-release-gate-judge-rubric|Release-gate judge (policy-aware) and three satisfied-but-failed cases]].

### Q15. Your team wants to ship the simulator-plus-judge gate as the sole CI release criterion for a customer-service agent. What should you recommend?

> [!tip]- Answer
> Recommend calibrate-then-trust instead of blind trust: run the verifiable audit once on a representative benchmark to learn the gate's trusted operating region, then use the cheap gate in CI only inside that region, since aggregate ρ≈0.94 coexists with 31% wrong promotions on the near-equal pairs release decisions actually turn on. Add the judge-free completion bit as a zero-cost tripwire for truncation regressions (ρ=0.87 vs. 0.80 broken-vs-working), never anchor accept/reject on satisfaction (it admits 48–60% failures), and re-audit on any configuration change because out-of-sample recalibration does not transfer. See [[wiki/02-introduction-and-positioning|Introduction and Positioning]].
