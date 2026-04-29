# Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents

**Paper:** [Agent Behavioral Contracts (Varun Pratap Bhardwaj, 2026)](https://arxiv.org/pdf/2602.22302)

## Human Readable TL;DR

Imagine hiring a new employee and only giving them a rough job description -- you'd quickly find them slowly drifting from what you wanted, sometimes in invisible ways. AI agents have the same problem: prompts are too informal to guarantee good behavior over long conversations. This paper proposes "behavioral contracts" -- like a written agreement that specifies what an agent must always do, what it should usually do, and how to course-correct when it slips. The system watches the agent in real time, catches drift before it causes harm, and even works across teams of agents passing tasks to each other.

## TL;DR

Agent Behavioral Contracts (ABC) brings the Design-by-Contract paradigm to LLM agents by formalizing a contract `C = (P, I, G, R)` of preconditions, invariants, governance policies, and bounded recovery, with a probabilistic `(p, δ, k)`-satisfaction notion to handle LLM non-determinism. The authors prove that recovery transforms exponentially-decaying compliance into linear decay (Lemma 3.10) and that drift modeled as an Ornstein–Uhlenbeck process is bounded to `D* = α/γ` whenever recovery rate exceeds natural drift (Theorem 4.3). They ship a YAML DSL (ContractSpec) and Python runtime (AgentAssert) with sub-10ms overhead, and validate across 7 LLMs and 1,980 sessions, showing contracted agents catch 5.2–6.8 soft violations/session that uncontracted baselines miss entirely while keeping hard-constraint compliance at 88–100%.

---

## Problem & Motivation

LLM-based autonomous agents are deployed using **informal natural-language prompts**, which provide no formal guarantees and degrade silently over multi-turn interactions. The paper identifies three concrete failure modes:

1. **Behavioral drift** -- agents gradually deviate from spec (a support agent becomes unprofessional, a research agent fabricates sources, a financial agent exceeds authority) and the deviation is invisible until harm is done.
2. **Governance failures** -- no runtime mechanism to enforce regulatory or organizational policies (PII leakage, unauthorized actions, spending limits).
3. **Silent degradation** -- without formal verification, projects fail in production after passing prototype testing.

Existing alternatives are insufficient: training-time alignment (Constitutional AI, RLHF) cannot adapt to deployment-specific constraints; output guardrails (NeMo Guardrails, Guardrails AI) are stateless and per-response with no temporal awareness or compositionality. Theoretical impossibility results imply passive safety cannot govern self-evolving agents -- active runtime enforcement is required.

---

## Main Original Ideas

1. **Formal contract structure `C = (P, I_hard, I_soft, G_hard, G_soft, R)`** -- generalizes Design-by-Contract to multi-turn agent behavior by separating zero-tolerance hard constraints from recoverable soft constraints, and elevating bounded recovery `R` to a first-class contract component with a maximum `k`-step recovery horizon.

2. **`(p, δ, k)`-satisfaction probabilistic compliance** -- a runtime-enforceable notion of compliance that handles LLM non-determinism: hard constraints hold with probability `p`, and soft deviations of magnitude `δ` recover within `k` steps with probability `p`.

3. **Stochastic drift model and Drift Bound Theorem** -- behavioral drift `D(t)` is modeled as an Ornstein–Uhlenbeck process `dD = (α − γD)dt + σdW`. Theorem 4.3 proves drift is bounded to `D* = α/γ` in expectation whenever the contract recovery rate `γ` exceeds natural drift rate `α`, giving designers a closed-form criterion.

4. **Recovery linearizes compliance (Lemma 3.10)** -- without recovery, multi-turn compliance probability decays as `q^T` (exponential); with recovery rate `r`, it decays as `1 − T(1−q)(1−r)` (linear). This is what makes long sessions feasible to govern.

5. **Compositionality theorem for multi-agent chains** -- formal sufficient conditions (interface compatibility, assumption discharge, governance consistency, recovery independence) under which per-agent contracts compose. The probabilistic extension quantifies that reliability degrades multiplicatively (`p_chain ≥ Π p_i`) while drift accumulates additively (`δ_chain ≤ Σ δ_i`) -- the "broken telephone" effect.

6. **ContractSpec DSL + AgentAssert runtime** -- a YAML DSL for declarative contract specification and a modular Python runtime that parses contracts, evaluates predicates against observed state, tracks drift, orchestrates LLM re-prompting for recovery, and integrates into agent platforms with `O(k + |A|)` per-action overhead.

7. **AgentContract-Bench** -- 200 synthetic scenarios across 7 domains (financial advisory, customer support, code generation, research synthesis, healthcare triage, governance stress, composition) with adversarial stress profiles and explicit compositionality tests.

8. **The "transparency effect" empirical finding** -- contracts do not change underlying agent behavior so much as make previously invisible deviations measurable, reframing the value of runtime enforcement around observability rather than just correction.

---

## Key Findings

### Live LLM Experiments (7 models, 6 vendors, 1,980 sessions)

| Experiment | Metric | Uncontracted | Contracted |
|---|---|---|---|
| **E1: Transparency** | Soft violations detected per session | 0.0 – 0.3 | **5.2 – 6.8** |
| **E1: Hard compliance** | Frontier models (GPT-5.2, GPT-4o-mini) | varies | **100%** |
| **E1: Hard compliance** | All models range | -- | **88 – 100%** |
| **E1: Hard compliance lift** | Mistral Large 3, Claude Opus 4.6 | baseline | **up to +4.5 pp** |
| **E2: Drift over 12 turns** | Mean `D(t)` | unbounded | **0.139 (max < 0.27)** |
| **E2: Recovery success** | Frontier models | -- | **100%** |
| **E2: Recovery success** | Other models | -- | 17 – 50% |
| **E3: Adversarial stress** | Min hard compliance under attack | -- | **≥ 0.911** |
| **E3: Adversarial stress** | Combinations holding 100% hard | -- | **7 / 12** |
| **E4: Ablation** | ΔΘ per removed component (recovery, soft) | -- | **≈ −0.20** |
| **Runtime overhead** | Per-action latency | -- | **< 10 ms (<1% of LLM call)** |

- **Transparency effect** is the headline result: contracted agents surface 5.2–6.8 soft violations/session that baselines miss entirely. Statistical effect is enormous (`p < 0.0001`, Cohen's `d = 6.7 – 33.8`).
- **Hard-constraint enforcement works:** 88–100% hard compliance across all models, with frontier models perfect; runtime catches residuals that training-time alignment missed.
- **Drift is bounded empirically**, matching the OU mean-reversion model -- contracts prevent runaway divergence over long sessions.
- **Adversarial resilience:** under prompt injection, conflicting advice, and boundary-push, hard compliance never falls below 0.911.
- **All ABC components are necessary:** ablating recovery or soft constraints individually each costs ≈ 0.20 in overall reliability score Θ.
- **Practical wrinkle:** overly aggressive platform guardrails (Azure DefaultV2) blocked 40–60% of legitimate multi-turn sessions, indicating coordination is needed between platform-level and application-level governance layers.

---

## Suggestions & Future Directions

1. **Tighter integration with feature extraction** -- ABC currently assumes a state dictionary of pre-computed features (`tone_score`, `pii_detected`); future work should integrate feature extraction pipelines into the framework.
2. **Adaptive reference distributions** -- the JS-divergence drift component relies on a manually calibrated reference distribution; needs adaptive mechanisms for non-stationary environments.
3. **Reusable recovery strategy library** -- the default recovery is just event emission, leaving deployers to write corrective actions; a shared library of recovery patterns would help adoption.
4. **Beyond `k`-window stationarity** -- the drift bound assumes stationary approximation that may be optimistic on very short sessions; need analysis under non-stationary regimes.
5. **Correlated-failure compositionality** -- probabilistic composition assumes conditional independence between agents; multi-agent systems sharing the same underlying LLM violate this and need correlation-aware bounds.
6. **End-to-end benchmark fidelity** -- AgentContract-Bench evaluates the enforcement engine on synthetic traces; future benchmarks should run the full pipeline including raw LLM-output feature extraction.
7. **Automated contract inference** -- learning contracts from logs/specifications rather than hand-authoring them.
8. **Extension to richer multi-agent topologies** -- compositionality theorem currently covers serial chains; needs extension to DAGs, broadcast, and dynamic spawning.
9. **Integration with resource-governance frameworks** -- ABC focuses on behavior; combining with works like "Agent Contracts" (Ye and Tan, 2026) could yield full-stack governance.
10. **Longitudinal real-world studies** -- empirical validation in production deployments over months, not just controlled 1,980-session experiments.

---

## Authors & Institutions

Varun Pratap Bhardwaj (Senior Manager & Solution Architect, Accenture; LL.B.) -- single-author paper with patent pending. Reference implementation and benchmark suite available subject to intellectual property clearance.
