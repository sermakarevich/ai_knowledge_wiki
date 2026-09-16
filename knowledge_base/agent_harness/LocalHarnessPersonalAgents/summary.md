# Statistical Priors for Implicit Preferences: Decoupling Skill Selection as a Local Harness in Personal Agents

**Paper:** [Statistical Priors for Implicit Preferences: Decoupling Skill Selection as a Local Harness in Personal Agents (Gan, Tang, Liu, 2026)](https://arxiv.org/abs/2606.05828)

## Human Readable TL;DR

Imagine you have a digital assistant that can order coffee from any of a dozen apps. You always prefer one particular app, but you never say so explicitly -- you just use it habitually. The assistant currently has no way to learn this preference because it relies on a cloud AI that forgets your habits between chats. This paper proposes a simple fix: keep a small, local scoreboard that tracks which apps you actually reward, and let the cloud AI step in only when you give an explicit instruction like "order from HouseBrew today." That split turns out to dramatically improve satisfaction with far fewer wrong guesses.

## TL;DR

This paper identifies a core architectural flaw in memory-augmented personal agents: forcing a single remote LLM to jointly handle statistical preference learning and semantic intent parsing leads to high regret and poor preference recovery. The proposed LOCAL HARNESS decouples these responsibilities -- a lightweight local bandit (LinUCB) serves as the primary decision-maker modeling implicit user habits, while the remote LLM is reserved exclusively as a semantic exception handler for explicit overrides. Evaluated on the new TOOLBENCH-60 benchmark across three LLM backbones, BANDIT-AS-OVERRIDE achieves the lowest cumulative regret and highest test accuracy, validated by a formal regret-improvement theorem.

---

## Problem & Motivation

Personal agents (e.g., Claude Code, Codex, Pi Agent) rely on large pools of locally installed external skills. When multiple skills can serve the same request, the optimal choice is governed not by the query's explicit text but by the user's latent preferences -- habits built through repeated daily interactions. Current agents inject per-user history into the LLM prompt (memory-augmented agents), forcing a single high-latency remote model to simultaneously track statistical frequencies and parse query semantics. This conflation causes context overflow, high API latency, multi-turn reasoning failures, and poor mathematical interpretability of preferences. The privacy constraints of local deployment rule out complex centralized recommendation systems, creating a need for a lightweight, on-device preference harness.

---

## Main Original Ideas

1. **LOCAL HARNESS Architecture** -- A strict physical and logical decoupling of statistical preference learning from semantic intent parsing. A local, computationally cheap statistical module acts as the primary, default decision-maker; the remote LLM is removed from the high-frequency execution path and invoked only as a narrow semantic exception handler for explicit lexical overrides.

2. **Two Statistical Priors** -- Two concrete local estimators are proposed and evaluated:
   - *Freq-as-Override*: maintains a per-(user, domain, skill) success-rate table and greedily selects the highest empirical frequency; ties are broken by round-robin initialization.
   - *Bandit-as-Override*: runs LinUCB over the (user, domain, skill) state space, computing UCB scores per skill to balance exploration and exploitation for nuanced preference recovery.

3. **Three-Step Decision Procedure** -- (1) A shared domain classifier restricts candidates to K skills in domain d. (2) The local statistical prior selects the default action ã_t. (3) An override probe -- a single binary LLM call -- checks whether the query explicitly names a skill; if yes, the named skill supersedes the prior, otherwise ã_t is executed. This makes the LLM call strictly conditional and eliminates it from standard-query execution paths.

4. **TOOLBENCH-60 Benchmark** -- A new simulation sandbox for preference-driven skill selection, filling a gap where no existing environment existed. It covers 10 functional domains with 6 skills each (60 total), 50 simulated users, and Dirichlet-parameterized preference distributions swept from one-hot (deterministic) to uniform (stochastic) to test multiple preference regimes.

5. **Formal Regret-Improvement Theorem** -- Theorem 4.1 proves that under mild consistency assumptions on the local prior, LOCAL HARNESS achieves strictly lower expected per-round regret than the LLM-only baseline after a finite number of interactions T_0. A quantitative bound shows two-phase convergence: an early O(t^{-1/2}) exploration term and a long-horizon plateau at λ·|R(P) - R(Q)| -- a strict (1-λ)× reduction over the LLM-only baseline.

---

## Key Findings

| Agent | Regime | Regret ↓ | Acc. ↑ | R.R. ↑ | SRC ↑ |
|---|---|---|---|---|---|
| Bandit-as-Override | one-hot | **135.7** | **84.3%** | **100.0%** | 0.539 |
| Freq-as-Override | one-hot | 126.3 | 82.5% | 92.5% | 0.288 |
| Profile-Memory | one-hot | 269.5 | 53.4% | 70.9% | 0.271 |
| InContext-Memory | one-hot | 363.9 | 27.2% | 62.5% | 0.282 |
| ZeroShot-LLM | one-hot | 377.2 | 23.9% | 15.9% | 0.000 |
| Bandit-as-Override | soft-0.3 | **264.8** | **46.2%** | **100.0%** | **0.539** |
| Profile-Memory | soft-0.3 | 344.2 | 32.9% | 70.9% | 0.271 |
| InContext-Memory | soft-0.3 | 372.7 | 25.4% | 62.5% | 0.282 |

*(Qwen3-30B-Instruct backbone; results consistent across DeepSeek-V4-Flash and GPT-5.2)*

- **Neither semantics nor statistics alone suffices.** Zero-shot LLMs cannot deduce latent habits; purely statistical agents (Pure-Bandit, Freq-Greedy) fail on explicit override queries (~10% accuracy on explicit queries vs. ~95% for LOCAL HARNESS).
- **Decoupling beats prompt-injected memory.** Profile-Memory -- the most faithful analogue of production agents (OpenClaw, Claude Code) -- consistently underperforms all LOCAL HARNESS variants across all three backbones and all preference regimes.
- **Exploration outperforms frequency counting.** The gap between Bandit-as-Override and Freq-as-Override widens monotonically as preference distributions become more stochastic (increasing Dirichlet α), with cumulative regret delta growing from 9.4 (one-hot) to 38 (α=0.3).
- **Backbone-invariant ranking.** The relative ordering of all nine agents is preserved across Qwen3-30B, DeepSeek-V4-Flash, and GPT-5.2, consistent with the theory which depends on the LLM only through a scalar miscalibration constant.
- **LLM override channel preserves bandit posterior.** Bandit-as-Override and Pure-Bandit show indistinguishable Spearman rank correlation (~0.53) across all backbones, confirming the override channel does not corrupt the local estimator.

---

## Suggestions & Future Directions

1. **Non-stationary user preferences** -- TOOLBENCH-60 currently models stationary profiles; extending the benchmark and harness to handle temporal shifts in user habits is an identified next step.
2. **Sparse, delayed, or noisy rewards** -- The current formulation assumes immediate binary feedback; relaxing to realistic feedback (ratings, implicit signals, delays) is needed for production deployment.
3. **Richer local feature representations** -- The harness uses deterministic feature hashing for lightweight operation; replacing or augmenting with dense neural text embeddings could capture finer syntactic preference variations at higher compute cost.
4. **On-device LLM for the override probe** -- The framework still relies on a capable remote model for the semantic exception handler; evaluating viability with small on-device models (e.g., sub-3B parameter) is an important open question for fully private local deployment.
5. **Broader benchmark coverage** -- Extending evaluation beyond TOOLBENCH-60 to existing tool-retrieval benchmarks (MassTool, ToolBench) to validate generalization.

---

## Authors & Institutions

Zeyu Gan, Huayi Tang, Yong Liu* (corresponding) -- Gaoling School of Artificial Intelligence, Renmin University of China, Beijing, China.
