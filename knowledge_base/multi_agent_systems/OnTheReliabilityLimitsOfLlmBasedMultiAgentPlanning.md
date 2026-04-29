# On the Reliability Limits of LLM-Based Multi-Agent Planning

**Paper:** [On the Reliability Limits of LLM-Based Multi-Agent Planning (Ao, Gao, Simchi-Levi, 2026)](https://arxiv.org/abs/2603.26993)

## Human Readable TL;DR

Imagine a game of telephone where each person rephrases a message before passing it on -- by the end, the message is garbled. This paper proves mathematically that the same thing happens when you chain multiple AI agents together: each handoff loses information, and the final answer is always worse than if a single agent had just handled the whole task with the same information. The only way to actually improve the chain is to give later agents genuinely new information (like access to a search engine), not just let them re-read what was already said. The paper also shows that structured, number-based communication between agents degrades much more slowly than free-form prose.

## TL;DR

This paper formalizes LLM-based multi-agent planning as a delegated decision problem over finite acyclic networks. The core result (Proposition 6) proves that any delegated network is decision-theoretically dominated by a centralized Bayes decision maker with access to the same exogenous signals. Communication loss is characterized via expected posterior divergence under proper scoring rules (Theorem 8), reducing to conditional mutual information under log loss. Experiments on MMLU confirm that relay chains degrade monotonically -- from 90.7% (single agent) to 22.5% (5-agent relay) -- and that only genuinely new exogenous signals improve reliability.

---

## Problem & Motivation

LLM-based multi-agent systems are widely deployed for tasks requiring decomposition, tool use, and verification. Yet there is no theoretical framework explaining when and why adding more agents helps or hurts. Empirical benchmarks compare architectures without controlling for information structure, making it impossible to distinguish gains from architecture versus gains from additional data. This paper fills that gap by providing decision-theoretic bounds on what multi-agent delegation can and cannot achieve.

---

## Main Original Ideas

1. **Delegated Decision Network Model** -- Formalizes multi-agent LLM systems as finite acyclic DAGs where nodes process a shared context signal, communicate through bandwidth-limited language interfaces, and optionally escalate to human review. Maps real system components (planners, workers, critics, tool calls) onto formal primitives.

2. **Centralized Dominance Result (Proposition 6)** -- Proves that without new exogenous signals, any delegated network is dominated by a centralized Bayes decision maker with access to the same information. Delegation alone cannot improve decision quality -- it can only lose information.

3. **Budget-Constrained Signal Design Equivalence (Theorem 7)** -- Shows that in the common-evidence regime (all agents share the same context), optimizing over multi-agent DAG architectures under a communication budget is equivalent to choosing a budget-constrained stochastic encoder on the shared signal.

4. **Posterior Divergence Characterization of Communication Loss (Theorem 8)** -- Under proper scoring rules, the gap between centralized and delegated performance equals expected posterior divergence. Under log loss this reduces to conditional mutual information I(Y; H|M); under Brier score to expected squared posterior error. Serial chains decompose additively.

5. **Redundancy and Verification Bounds (Corollary 9)** -- A verifier signal improves reliability only if it is not Blackwell-redundant given existing communication. Self-critique (re-reading the same message) provably cannot help; only executable tests or external validators add value.

6. **Optimal Human Review Policy (Theorem 10)** -- Characterizes optimal selective review as a pointwise comparison of automated posterior risk against review cost, yielding a threshold escalation rule.

---

## Key Findings

### Main Experimental Results (200 MMLU Questions, gpt-4.1-mini / o4-mini)

| Condition | Description | Accuracy (95% CI) |
|-----------|-------------|-------------------|
| A (centralized) | Single agent, direct answer | **90.7%** |
| B2 (2-agent relay) | 2-agent prose relay | 41.2% |
| B (3-agent relay) | 3-agent prose relay | 43.5% |
| B5 (5-agent relay) | 5-agent prose relay | 22.5% (below chance) |
| B_post (3-agent posterior) | 3-agent structured posterior relay | 75.2% |
| C (single + Wikipedia) | Single agent + Wikipedia tool | 87.2% |
| D (Wiki + Scholar) | Single agent + Wikipedia + Scholar | 89.8% |
| S (synthetic, no tool) | Synthetic KB, no tool access | 24.3% |
| S (synthetic, with tool) | Synthetic KB + tool access | **82.7%** |

- **Relay degradation is monotonic**: accuracy drops ~8.5 percentage points per stage with prose relay, but only ~2.8 points per stage with structured posterior relay
- **KL divergence correlates with accuracy loss**: r=0.72 for 3-agent chains, r=0.44 for 5-agent chains, validating Theorem 8's posterior distortion characterization
- **Redundant signals don't help**: Wikipedia + Wikipedia performs identically to Wikipedia + Scholar on MMLU (89.8% both), confirming Corollary 9 -- only genuinely new information improves decisions
- **Tool access is transformative when information is missing**: on synthetic KB tasks, tool access jumps accuracy from 24.3% to 82.7% (+58.4 pts)
- Total API cost for all experiments: ~$70--95

---

## Suggestions & Future Directions

1. **Matched-signal evaluation protocol** -- Future benchmarks of multi-agent architectures should compare systems under matched exogenous signals and communication capacity, treating retrieval or additional context as a change in information structure rather than a pure architecture effect.

2. **Posterior distortion as communication quality metric** -- Recommends measuring communication quality via posterior distortion rather than proxies like transcript length or token count.

3. **Risk-based human review triggers** -- Human review should be triggered by posterior risk comparisons (automated risk vs. review cost) rather than fixed stage counts or workflow heuristics.

4. **Extensions to richer settings** -- The framework provides foundations for future work on communication-constrained planning, tool-mediated decision support, and human-AI systems with structured recourse beyond the common-evidence regime studied here.

5. **Practical architecture implications** -- Results suggest that adding agents to a pipeline without adding new information sources is counterproductive; system designers should focus on information acquisition (tools, retrieval) rather than delegation depth.

---

## Authors & Institutions

Ruicheng Ao (Operations Research Center & IDSS & Dept. of Civil and Environmental Engineering, MIT), Siyang Gao (Dept. of Systems Engineering, City University of Hong Kong), David Simchi-Levi (Operations Research Center & IDSS & Dept. of Civil and Environmental Engineering, MIT)
