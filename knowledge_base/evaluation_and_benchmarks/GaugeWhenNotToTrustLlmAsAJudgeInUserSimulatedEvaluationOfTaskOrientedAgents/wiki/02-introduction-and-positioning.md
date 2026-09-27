> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and Positioning
**In one sentence:** GAUGE audits the low-cost offline gate in which persona-driven LLM (Large Language Model) user-simulators talk to candidate task-oriented agents and an LLM-as-a-judge scores the transcripts, and finds the gate is human-validated yet mis-anchored — its ranking matches a verifiable non-LLM (Large Language Model) reward broadly but satisfaction is decorrelated from task success and close-pair decisions disagree 31% of the time.
## Key points
- The de facto release gate audited is: persona-conditioned simulators converse with each candidate, an LLM-judge scores transcripts, and the higher-scoring agent is promoted, run in CI (Continuous Integration) at a few cents per transcript with no labeled production data.
- GAUGE (Grounded Audit of User-simulator-and-judge Gate Evaluation) is a reusable, fully offline protocol that separates two validities release practice conflates: ranking validity (ordering agents like the verifiable reward) and construct validity (certification against human satisfaction).
- Satisfaction–success gap: 57.5% of conversations the blind human panel rated satisfied (≥5/7) had failed the customer's task, with correlation ρ=−0.147, holding across five rater populations, both benchmarks, and every subjective dimension rated.
- Ranking holds broadly but fails where it matters: aggregate gate-versus-reward ranking correlation is ρ=0.94, yet the decision-disagreement rate jumps from <1% on wide-reward pairs to 31% on close (near-equal strong) agent pairs.
- Scale of the audit: 25 agents from six providers, four judges, two substrates (τ2-bench oracle DB-state/action checks and SimulatorArena human-graded correctness), ≈3,700 transcripts.
- Same-family judge self-preference is isolated at +0.75/7, and an accept/reject threshold anchored on satisfaction admits agents that fail 48–60% of the time.
- Remedy is a calibrate-then-trust cadence: run the verifiable audit once on a representative benchmark to learn the gate's trusted operating region, then use the cheap gate in CI (Continuous Integration) within that region; a judge-free completion bit is a zero-cost tripwire for truncation regressions (ρ=0.87 vs. 0.80 on broken-vs-working), while out-of-sample recalibration does not transfer.
---
## 1. The offline gate under audit
**Covers:** Introduction — de facto evaluation gate and its unmeasured assumption

Developers of agentic task-oriented LLM (Large Language Model) agents for customer service, tool-use assistants, and tutoring face three constraints: no clean held-out test set capturing live user experience, prohibitively slow per-candidate human studies, and a fast-changing config space (model, prompt, policy, tools).

The field's answer is the composite simulator-plus-judge gate: drive each candidate against persona-conditioned user-simulators, score transcripts with an LLM-judge, promote the higher-scoring variant. It rests on one assumption teams almost never measure: that this gate ranks variants the way a grounded evaluation would.

Known judge biases (self-preference, position bias) are documented; what was not quantified is their magnitude at the release-decision unit against a verifiable reward: a 57.5% false-accept rate on the blind human panel, a gap persisting across five rater populations and altering agent-selection decisions.

## 2. GAUGE positioning (Table 1)
**Covers:** Table 1 — positioning against prior evaluation work

| Criterion | Prior columns (∼/✗) | GAUGE |
|---|---|---|
| Ranking validity vs. reward | ∼ / ∼ / ✗ / ∼ | ✓ |
| Release-decision unit | ∼ / ✓ / ✗ / ∼ | ✓ |
| Satisfaction ≠ task success | ✗ / ✗ / ✗ / ∼ | ✓ |
| Cross-provider scale | ∼ / ✗ / ∼ / ✗ | ✓ |
| Grounded in real human ratings | ✓ / ✗ / ✓ / ✓ | ✓ |
| Judge-free cost decomposition | ✗ / ✗ / ✗ / ✗ | ✓ |

> Table caption (verbatim): "Positioning against prior evaluation work. Only GAUGE tests whether the simulator+judge gate ranks agents like a verifiable non-LLM reward and quantifies the satisfaction–success gap. ✓ fully addresses the criterion; ∼ partial; ✗ not."

## 3. Why the satisfaction anchor misleads
**Covers:** Introduction — three reasons ranking validity is not enough

Verbatim central claim: "A gate can be human-validated yet mis-anchored."

Three reasons given:

1. Capability dominance only: among near-equal strong agents — the comparisons real release decisions make — the gate promotes the lower-reward agent on 31% of close pairs (the decision-disagreement rate), up from <1% where rewards are far apart.
2. Optimization hazard: teams optimize against gates, and tuning to a satisfaction anchor raises a metric known to diverge from the objective once optimized (Strathern, 1997; Skalse et al., 2022).
3. Bad absolute bar: an accept/reject threshold anchored on satisfaction admits agents that fail 48–60% of the time (§4.1).

The anchor thus governs exactly the decisions a gate exists to make: promoting near-equal candidates, serving as an optimization target, and setting the absolute accept/reject bar.

The user-simulator is a component of the gate audited here; every central claim is anchored on the simulator-independent verifiable reward and human panel.

## 4. Related work deltas
**Covers:** Section 2 Related Work

- User-simulator reliability: from satisfaction-driven simulation (Sun et al., 2021) to LLM-based simulators (Davidson et al., 2023; Sekulic et al., 2024) and "agents evaluating agents" (Zhuge et al., 2025); SimulatorArena (Dou et al., 2025) and Lost-in-Simulation (Seshadri et al., 2026) test simulators as human proxies via absolute rating correlation or single-agent reliability. Delta: this work audits the composite gate's agent-ranking validity at the release-decision unit against a non-LLM verifiable reward, and shows its optimized satisfaction signal is decorrelated from task success.
- Agent and customer-agent benchmarks: tool-using agents evaluated by recent benchmarks (Zhou et al., 2024; Qin et al., 2024; Liu et al., 2024); ECom-Bench (Wang et al., 2025) reports persona-simulator pass-rates, while τ-bench (Yao et al., 2025) and τ2-bench (Barres et al., 2026) provide a verifiable substrate. Delta: tests whether such pass-rates rank agents like a grounded reward, and surfaces the satisfied-but-failed inversion.
- LLM-as-a-judge calibration to humans: literature validates LLM-judges against human preference/satisfaction (Zheng et al., 2023; Liu et al., 2023; Gu et al., 2024) and documents judge biases including self-preference and position bias (Panickssery et al., 2024; Wang et al., 2024).

## 5. Contributions and Figure 1
**Covers:** Contributions (1)–(4), Key Findings list, Figure 1 caption

Four contributions as stated:

1. GAUGE, a reusable protocol validating simulator-plus-judge gates against a verifiable non-LLM reward at the release-decision unit: 25 agents, six providers, four judges, two substrates, ≈3,700 transcripts (§3).
2. Satisfaction–success gap: satisfaction carries essentially no information about task success — 57.5% of satisfied conversations failed the task (ρ=−0.147) across five rater populations and two substrates (§4.1).
3. Separating ranking from construct validity on the six-provider ladder: robust ranking (ρ=0.94) yet 31% wrong promotions on close pairs; same-family judge self-preference +0.75/7 (§4.2, §4.3).
4. Calibrate-then-trust recipe: judge-free completion bit as zero-cost tripwire for truncation regressions (ρ=0.87 vs. 0.80 broken-vs-working; §4.5); negative result that out-of-sample recalibration does not transfer (§4.6).

Key Findings (verbatim bullets):

- "Subjective approval is decorrelated from task success across all dimensions, so an evaluation gate can be human-validated yet mis-anchored to the outcome."
- "High aggregate ranking validity coexists with unreliable resolution of near-equal candidates, precisely the comparisons release decisions depend on."
- "Evaluator reliability is determined by evidence access, not model capability: outcome-grounded judging succeeds where transcript-only satisfaction fails."
- "The gate is valid only within a bounded operating region, requiring re-auditing on configuration change rather than on a fixed schedule."

Figure 1 (verbatim caption): "GAUGE measures whether the LLM-as-a-Judge and user-simulator evaluation gate ranks agents the way a grounded, verifiable reward would. Left to right: an agent and a persona simulator converse on a substrate, and four evaluators score each transcript: three subjective satisfaction signals (the LLM-as-a-Judge gate, an LLM human-proxy, and a blind 3-person human panel) and one objective non-LLM reward. Aggregating over all 25 agents, the gate's agent ranking matches the reward's (ρ=0.94), yet satisfaction is decorrelated from success."
