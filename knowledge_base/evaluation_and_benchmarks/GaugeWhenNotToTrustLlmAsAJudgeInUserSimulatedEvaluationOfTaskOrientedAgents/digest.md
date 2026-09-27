> [[index|Wiki]] | [[summary|Summary]]
# GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents — Digest

## 1. [[wiki/01-gauge-overview|GAUGE: When Not to Trust LLM-as-a-Judge]]
**In one sentence:** This chunk contains only the paper's title block (title, authors Umesh Bodhwani, Thanh Tran, Kai Wei, Amazon affiliation) and no substantive claims, so no argument can be extracted from it.
## Key points
- The chunk provides the paper title "GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents" and nothing beyond the header.
- The listed authors are Umesh Bodhwani, Thanh Tran, and Kai Wei, affiliated with Amazon.
- Contact emails listed are {bodhwani, tdt, kaiwe}@amazon.com.
- The abstract body is absent from the chunk, so no thesis, method, or result claims can be stated.
- Fragmentary tokens (e.g. "SimArena/", "LostInSim", "ECom-", "Bench", "Judge-", "eval") appear but form no complete claim and are not reported as findings.

## 2. [[wiki/02-introduction-and-positioning|Introduction and Positioning]]
**In one sentence:** GAUGE audits the low-cost offline gate in which persona-driven LLM (Large Language Model) user-simulators talk to candidate task-oriented agents and an LLM-as-a-judge scores the transcripts, and finds the gate is human-validated yet mis-anchored — its ranking matches a verifiable non-LLM (Large Language Model) reward broadly but satisfaction is decorrelated from task success and close-pair decisions disagree 31% of the time.
## Key points
- The de facto release gate audited is: persona-conditioned simulators converse with each candidate, an LLM-judge scores transcripts, and the higher-scoring agent is promoted, run in CI (Continuous Integration) at a few cents per transcript with no labeled production data.
- GAUGE (Grounded Audit of User-simulator-and-judge Gate Evaluation) is a reusable, fully offline protocol that separates two validities release practice conflates: ranking validity (ordering agents like the verifiable reward) and construct validity (certification against human satisfaction).
- Satisfaction–success gap: 57.5% of conversations the blind human panel rated satisfied (≥5/7) had failed the customer's task, with correlation ρ=−0.147, holding across five rater populations, both benchmarks, and every subjective dimension rated.
- Ranking holds broadly but fails where it matters: aggregate gate-versus-reward ranking correlation is ρ=0.94, yet the decision-disagreement rate jumps from <1% on wide-reward pairs to 31% on close (near-equal strong) agent pairs.
- Scale of the audit: 25 agents from six providers, four judges, two substrates (τ2-bench oracle DB-state/action checks and SimulatorArena human-graded correctness), ≈3,700 transcripts.
- Same-family judge self-preference is isolated at +0.75/7, and an accept/reject threshold anchored on satisfaction admits agents that fail 48–60% of the time.
- Remedy is a calibrate-then-trust cadence: run the verifiable audit once on a representative benchmark to learn the gate's trusted operating region, then use the cheap gate in CI (Continuous Integration) within that region; a judge-free completion bit is a zero-cost tripwire for truncation regressions (ρ=0.87 vs. 0.80 on broken-vs-working), while out-of-sample recalibration does not transfer.

## 3. [[wiki/03-judge-biases-and-method|Judge Biases and Method]]
**In one sentence:** Known LLM-judge biases (position, self-preference, inconsistency) plus a misaligned satisfaction anchor motivate GAUGE, an end-to-end audit that compares a policy-aware LLM-judge gate against a verifiable non-LLM reward at the agent release-decision unit.
## Key points
- The chunk lists known LLM-judge biases: position (Wang et al., 2024), self-preference (Panickssery et al., 2024), and inconsistency (Stureborg et al., 2024), alongside benchmarks of LLM judges and reward models (Tan et al., 2025; Lambert et al., 2025).
- A complementary line calibrates model confidence to signal when to trust an LLM output versus defer to a human (Bodhwani et al., 2025a; Jung et al., 2025), but for customer agents this anchor is misaligned because human satisfaction is decorrelated from task success.
- The core delta claim is that a judge can be "human-validated" yet mis-rank agents, and that the satisfaction–success decorrelation misleads humans too, not only simulators that are over-cooperative or ranking-divergent (Mind-the-Sim2Real (Zhou et al., 2026), SimulatorArena (Dou et al., 2025)).
- GAUGE is defined at the release-decision unit (agent a, aggregated over personas p and domains d): agent-level gate G(a) = Ep,d [gate(τ)], verifiable reward R(a) = Ep,d [r(τ)] ∈ [0, 1], plus Sproxy(a) and Shum(a); it measures ranking validity ρ(G, R) and the construct (satisfaction–success) gap.
- The construct gap is the rate at which the task failed (r(τ)=0) among transcripts a signal rated satisfied, where satisfied means ≥5 on a 7-point or ≥8 on a 10-point scale; a gate can be human-validated (ρ(Shum, G) high) yet mis-anchored (ρ(Shum, R) low) because satisfaction itself does not track success.
- The primary substrate is τ2-bench (Barres et al., 2026) retail and airline with a non-LLM oracle reward — fully deterministic on airline (DB-state and communicate checks), predominantly deterministic on retail (deterministic DB check gates an LLM-scored natural-language assertion) — plus SimulatorArena (Dou et al., 2025) math tutoring for replication.
- The cross-provider ladder spans 14 models from six providers (Anthropic, Meta, Mistral, Qwen, DeepSeek, OpenAI) at two temperatures on 114 retail and 50 airline tasks, yielding 25 scored model-temperature configurations and about 3,700 transcripts; the controlled-degradation set has 12 Sonnet-4.5 configurations over 6 strata × 2 domains (144 cells, 720 transcripts), degraded only via inference-time hyperparameters with no prompt or code edits.
- Four judges apply the gate rubric to the full grid (Claude Sonnet-4.5 and Opus-4.8, GPT-5.4 and GPT-5.5), with Opus-4.8 the primary judge and GPT-5.5 its out-of-family counterpart; on a stratified 150-transcript τ2 sample with a blind 3-person panel (150×3 design, Krippendorff's α=0.79, human–human ceiling ρ=0.85), Opus-4.8 reproduces human satisfaction at ρ=0.846 and GPT-5.5 at ρ=0.827.

## 4. [[wiki/04-satisfaction-success-gap|Satisfaction Matches the Base — Only the Policy-Aware Gate Helps]]
**In one sentence:** Satisfaction ratings are uninformative about task success because the satisfied-but-failed rate (57.5%) matches the base failure rate (57.3%), and only the policy-aware gate that checks whether the task resolved halves failure risk and discriminates success.
## Key points
- The human panel rated 57.5% of satisfied (≥5/7) conversations as failed, statistically indistinguishable from the stratified sample's own 57.3% base failure rate.
- Conditioning on satisfied does not lower failure, so satisfaction is uninformative rather than merely weak, with transcript-level AUC 0.44.
- The policy-aware gate roughly halves failure risk: 20.0% of gate-accepted conversations fail against a 40.2% base rate on the natural task mix, with AUC 0.73.
- The process-blind proxy, which never sees tool calls or task, behaves like satisfaction not the gate: 32.7% vs. 40.2% base, AUC 0.49.
- Separating these two signals — one uninformative (proxy/satisfaction) and one informative (policy-aware gate) — is the core contribution of this work.
- The panel result is robust to dropping any single annotator (56.4–60.5% leave-one-annotator-out).
- The satisfied-but-failed rate is concordant across five rater populations (human panel plus gate and proxy scorings from two LLM providers; 47.6–59.5%).
- The gap reflects subjective approval in general: all five subjective dimensions (satisfaction, respect, clarity, perceived helpfulness, would-return) are decorrelated from success (|ρ| ≤ 0.17), with overall ρ = −0.147.

## 5. [[wiki/05-judge-robustness-and-self-preference|Judge robustness and self-preference]]
**In one sentence:** The judge's agent ranking is robust — it holds with an out-of-family judge and is not a capability artifact — but same-family judges inflate their own provider's agents by about 0.7/7 without changing the ranking.
## Key points
- Opus-4.8 and GPT-5.5 agree at ρ=0.92, so the ordering is "not a single-provider artifact."
- All four judges recover the verifiable-reward ordering (ρ=0.84–0.94) and agree with one another (ρ=0.90–0.98).
- GPT-5.5 grades ≈0.8/7 lower in absolute level, even though its ranking agrees.
- The ordering is not a capability artifact: as agents on the same τ 2 pool, Opus-4.8 scores 0.82 and GPT-5.5 scores 0.84 versus pool-best Opus-4.6 (t.7) at 0.87, with overlapping 95% CIs.
- The weakest judge-as-agent, GPT-5.4 (0.77), is tied-best as a ranker (ρ=0.94), so ranking ability does not require outclassing the agents.
- The near-equal limit holds for every judge (top-11 ρ=0.25–0.51, all n.s.), confirming "genuine agent near-equality rather than mis-ranking by a weak judge."
- Same-family self-preference is isolated by a scale-invariant diff-in-diff of +0.75/7 for the Opus-4.8 judge inflating Claude agents over GPT-5.5 (Sonnet-4.5 shows +0.67/7 against GPT-5.4), and it "leaves the ranking intact."
- Ranking is stable against judge noise across two reruns: test–retest ICC=0.87 and rank stability ρ=0.92.

## 6. [[wiki/06-reliability-methods-and-references|Reliability methods, references, and appendix evidence]]
**In one sentence:** The appendices show the satisfied-but-failed gap is not a single-rater, single-dimension, single-degradation, or single-simulator artifact, because every rater population, every subjective dimension, the controlled-degradation set, and both simulator providers fail the same 20% false-accept ceiling.
## Key points
- Every rater population exceeds the lenient 20% false-accept ceiling: on τ (tau)-bench the human panel scores 23/40 (57.5%), Opus-4.8 gate 30/63 (47.6%), Opus-4.8 proxy 50/84 (59.5%), GPT-5.5 gate 29/57 (50.9%), GPT-5.5 proxy 75/126 (59.5%), all at p (p-value) < 10⁻⁶, and SimulatorArena human ratings score 12/31 (38.7%) at p=0.013.
- The headline does not depend on any single human annotator: removing any one of the three panel raters keeps the satisfied-but-failed rate within 56.4–60.5% (4.1-point spread around 57.5%), with per-annotator rates of 58.1%, 63.5%, and 59.5%.
- All five blind-panel subjective dimensions are decorrelated from verifiable success (n=150, all |ρ| ≤ 0.17, where ρ means Spearman rank correlation): satisfaction ρ=-0.147, respect/tone ρ=-0.118, clarity ρ=+0.085, helpfulness ρ=-0.129, would-return ρ=-0.168 (p=0.04, the only nominal hit, consistent with chance among five correlated tests).
- High ratings invert at 56–64% on every dimension (satisfaction 57.5%, respect/tone 63.6%, clarity 56.5%, helpfulness 63.3%, would-return 61.7%), while inter-annotator agreement measured by Krippendorff's α (alpha, an agreement statistic) stays high at 0.76–0.83, so raters agree with each other but not with task success.
- The controlled-degradation set (12 configurations of one model, Claude Sonnet-4.5, perturbing only inference-time flags: temperature, max_tokens output cap, max_steps conversation cap, max_errors tolerance) confirms a clean positive control: degraded-tier mean verifiable reward 0.05 versus 0.65 for good/medium tiers, yet every subjective signal still rates degraded configs mid-scale.
- The sharpest inversion is config D7 (step-starved, st6): verifiable reward 0.00 but human-panel satisfaction 4.64 on a 1–7 scale, the highest of any degraded config, because a step-capped trajectory is cut off mid-task while reading as helpful turn-by-turn.
- The gap persists under a controlled simulator swap (same 12 variants, personas, tasks, rubrics, judge, and oracle; only the user-simulator provider changes): satisfied-but-failed rates are Sonnet-4.5 43.6% (gate) / 52.9% (proxy) versus GPT-5.4 66.7% (gate) / 69.8% (proxy), all p < 10⁻⁷ against 20%.

## 7. [[wiki/07-simulator-swap-control|Controlled second-provider simulator swap (Table 7)]]
**In one sentence:** Swapping the user simulator from Sonnet-4.5 to GPT-5.4 leaves the satisfied-but-failed gap large and highly significant and preserves the 25-agent ranking, so neither finding is a Sonnet-simulator artifact.
## Key points
- Controlled swap design: identical 12 variants × 6 strata × task ids (n=216 each) on the retail degradation grid, same Sonnet-4.5 agent, only the user-simulator provider differs.
- "Satisfied" means ≥5/7 and "failed" means verifiable reward = 0; the satisfied-but-failed (false-accept) rate stays far above the 20% null under both simulators.
- The two simulators steer the same agent into different trajectories: mean verifiable reward is GPT-5.4 0.21 vs. Sonnet 0.32, with the harsher simulator surfacing more task failures.
- Because mean reward differs, compare each false-accept rate to the null, not to each other — the reward shift mechanically shifts the absolute false-accept rate.
- Full 25-agent ranking grid re-run under the GPT-5.4 user simulator: 114 tasks per agent, 2,850 transcripts, holding agent, tasks, rubrics, judge, and oracle fixed.
- Agent ordering is preserved across simulators: Spearman ρ=0.93 (Pearson 0.97; base-model cluster-bootstrap 95% CI [0.71, 0.98]) vs. 0.94 under Sonnet-4.5.
- The near-equal top-11 degradation reproduces under GPT-5.4 (top-11 ρ=0.51), so same-family simulator–agent affinity does not account for the ranking result (§4.2).

## 8. [[wiki/08-decision-disagreement-rate|Table 9: Decision-disagreement rate by signal]]
**In one sentence:** The judge gate picks the worse agent (lower verifiable reward) in 31.0% of near-equal pairs but only 0.9% of wide pairs, and no cheaper or combined signal fixes this because the errors are specific to each signal, not shared noise.
## Key points
- Table 9 measures "fraction of pairs where the gate promotes the lower-reward agent," split into near-equal pairs (reward gap |ΔR| (absolute reward difference) < 0.1, n=87) versus wide pairs (|ΔR| ≥ 0.1, n=211), with 2 exact-tie pairs excluded from 300 total.
- The main judge (Opus-4.8) has a near-equal disagreement rate of 31.0%, with a base-model cluster-bootstrap 95% CI (confidence interval, the uncertainty range) of [11.6, 50.0].
- Even the low end of that range (11.6%) is still about 13× the wide-pair rate of 0.9%, so close pairs are far more error-prone than clearly separated pairs.
- The result survives removing the least-independent pairs: on the 75 cross-base-model pairs only, the rate is 32.0% (24/75).
- The errors are signal-specific, not one shared ranking mistake: of 60 near-equal pairs flipped by at least one of five signals, only 4 are flipped by all five and 22 by exactly one, with mean pairwise Jaccard (overlap between flip sets) 0.40.
- Section G tests 21 cheaper candidate signals — single judges, the process-blind proxy, the completion bit, and unweighted and confidence-weighted judge ensembles — and none beats the best single judge on near-equal pairs.
- Averaging all four judges gives exactly 31.0% (27/87), identical to the best single judge, because the judges are highly correlated (pairwise ρ (rank correlation) 0.67–0.98) and flip the same close pairs.

## 9. [[wiki/09-annotation-and-prompt-instructions|Annotation and Prompt Instructions: Entire Conversation, Personas, and Evaluation Substrates]]
**In one sentence:** This chunk supplies the rater/simulator instruction to read the entire conversation while keeping all task facts unchanged, the persona overlays S1–S5 and S8, the Table 11 dataset statistics across three substrates, the two-part oracle patch with its robustness argument, and the verbatim process-blind prompts for the experience rater, human panel, and user simulator.
## Key points
- The persona overlay instruction requires keeping all facts of the request unchanged — only tone, cooperativeness, pacing, and assertiveness vary, while task facts (reason_for_call, known_info, evaluation_criteria) are untouched so the verifiable reward is unaffected.
- Six exercised personas are defined (S1 Cooperative, S2 Impatient/rude, S3 Distracted, S4 Anxious/low-trust, S5 Terse, S8 Skeptical negotiator), with S6 chatty over-sharer and S7 indecisive perfectionist defined-but-unexercised, accounting for the gap between S5 and S8.
- The cross-provider ladder covers 3,691 scorable transcripts (non-null reward: 2,487 retail / 1,204 airline), 25 scored agent configurations, a task pool of 114 retail / 50 airline tasks, averaging 31 messages, 8.6 tool calls, and 7.6 user turns per conversation.
- The 25 scored configurations are 28 (model, temperature) cells minus three excluded for infrastructure reasons (Llama-3.1-405B at both temperatures, throttle-limited; and the GPT-5.5 temperature-0.7 cell, as GPT-5.5 fixes its sampling setting); the 14 base models span Anthropic Opus-4.6/Sonnet-4.6/Haiku-4.5, Meta Llama 405B/70B/8B, Mistral Large-3/Small/Ministral-3B, Qwen3 235B/32B, DeepSeek-V3.2, and OpenAI GPT-5.4/5.5, each run at two temperatures.
- The controlled-degradation positive-control set has 720 transcripts in 144 cells (12 configs × 6 strata × 2 domains, 5 transcripts per cell) with tiers of 3 good / 5 medium / 4 degraded configs; the human panel has 150 transcripts / 3 annotators (85 retail / 65 airline stratification, 86 failed / 64 succeeded) with Krippendorff's α of 0.79 for satisfaction; SimulatorArena (math tutoring) has 9 models / 50 graded conversations with a 31-conversation high-satisfaction (≥8/10) subset.
- The only modification to the τ2-bench evaluator is a bug-fix in two disjoint parts — (A) backend swap repointing four DEFAULT_LLM_* constants from gpt-4.1 to bedrock/...claude-sonnet-4-5 with temperatures staying at 0 and no scoring logic touched, and (B) a tolerant verdict parser (loads_tolerant) that recovers fenced/wrapped JSON without rewriting verdicts — validated by a 16-case unit test and by the argument that airline (reward_basis = (DB, COMMUNICATE)) is fully deterministic and patch-independent while retail changed outcome in only 113 of 2,537 applicable simulations (4.5%).
- Experience/human raters are process-blind by construction: they see only user-visible spoken turns (tool calls and task stripped out), rate satisfaction, respect/tone, clarity, perceived helpfulness, and would-return on 1–7 based purely on how the conversation felt, not on policies, tools, or behind-the-scenes actions — which is why the satisfaction–success gap does not depend on the patched component, with the process-blind proxy still false-accepting 62.1% of satisfied airline conversations (325/523).

## 10. [[wiki/10-release-gate-judge-rubric|Release-gate judge (policy-aware) and three satisfied-but-failed cases]]
**In one sentence:** A policy-aware release-gate judge scores only the assistant on a 1–7 scale with policy adherence first, and three τ 2 cases show satisfaction signals passing (7/7) while verifiable reward is 0.0 because the task actually failed.
## Key points
- The release-gate judge role-plays an operations supervisor deciding whether an agent variant is safe to ship, evaluating ONLY the assistant.
- It scores four dimensions in priority order: (1) policy adherence, (2) task resolution, (3) efficiency, and (4) professionalism, on a 1–7 scale with a final `SCORE: <1-7>` line.
- Policy adherence requires authenticating before acting, explicit confirmation before any database write, one tool call per turn, and no fabrication.
- The retail τ 2 case scores Gate 7/7, proxy 7/7, human panel 5.5/7, but verifiable reward 0.0, with 12 of 13 tool calls correct and one pending order never modified.
- The airline τ 2 case scores proxy 7/7 but reward 0.0 because the rebooking did not match the required end-state, flagged by the cross-provider judge (GPT-5.4 gate 1/7).
- The SimulatorArena math-tutoring case scores human 10/10 and proxy 7/7 yet is verifiably incorrect: shown work implies 330 passes but the tutor states 165, caught by the policy-aware gate (Opus-4.8 1/7).
- The common mechanism is satisfied-but-failed: the user ends satisfied (###STOP### / thanks) while the task end-state is wrong.

## The argument in five moves
1. The de facto release gate — persona simulators conversing with candidates plus an LLM-judge scoring transcripts — is cheap and widely used, but its core assumption that it ranks agents like grounded evaluation was unmeasured.
2. GAUGE audits that gate at the release-decision unit against a verifiable non-LLM reward and a blind human panel, separating ranking validity from construct validity.
3. Satisfaction is uninformative about success (57.5% satisfied-but-failed, ρ=−0.147, all dimensions |ρ|≤0.17), so a gate can be human-validated yet mis-anchored; only the policy-aware gate that checks task resolution halves failure risk.
4. Ranking validity holds broadly (ρ≈0.94, robust across judges, simulators, and reruns, with isolated +0.75/7 self-preference) yet collapses exactly where release decisions live — 31% wrong promotions on near-equal pairs, unfixable by ensembling or cheaper signals.
5. Controls rule out artifacts: the gap and ranking limit survive annotator ablations, five rater populations, two substrates, controlled degradation (including the D7 step-starved inversion), a second-provider simulator swap, and a deterministic oracle patch.
6. Therefore trust the gate only inside a calibrated operating region: audit once against verifiable reward, use the cheap gate in CI (Continuous Integration) within that region, use the judge-free completion bit as a truncation tripwire, and re-audit on configuration change.
