# LLM Reasoning Is Latent, Not the Chain of Thought

**Paper:** [LLM Reasoning Is Latent, Not the Chain of Thought (Wenshuo Wang, 2026)](https://arxiv.org/abs/2604.15726)

## Human Readable TL;DR

When a smart model "thinks out loud" before answering, it's easy to assume that the written-out steps are the actual thinking. This paper argues that's like reading someone's whispered notes and thinking that's their whole thought process -- the real reasoning often happens silently in the model's internal state, and the visible steps are more like a partial transcript. Through carefully controlled experiments, the author shows that which factor actually drives better answers (inner thoughts, written steps, or just having more time to think) depends heavily on the type of problem being solved.

## TL;DR

The paper argues that LLM "reasoning" has been conflated across three distinct objects -- surface chain-of-thought (S), latent-state trajectories (Z), and generic serial compute (B) -- and proposes a compute-audited experimental framework to disentangle them. Through controlled and naturalistic experiments across three models, the author shows a "substrate switch": latent dynamics (H1) dominate ordinary reasoning, surface CoT (H2) dominates constitutive regimes where visible structure is binding, and generic compute (H0) dominates search-heavy regimes. The central recommendation is to treat latent-state dynamics as the default object of study and to use factorized, compute-matched designs when evaluating reasoning.

---

## Problem & Motivation

LLM "reasoning" research is fragmented by three conflated interpretations: (1) explicit CoT *is* the reasoning, (2) gains come from extra serial compute regardless of form, or (3) reasoning is an unobservable latent process. Prior work rarely compares these within a unified, compute-matched framework, so claims about faithfulness, interpretability, benchmark validity, and inference-time interventions rest on unstated assumptions. Without resolving which object is primary, methodological choices (what to explain, where to intervene, how to monitor for safety) lack principled grounding.

---

## Main Original Ideas

1. **Three-Object Formalization (S, Z, B).** The paper introduces precise distinctions between Surface chain-of-thought (S, the verbalized trace), task-relevant latent-state trajectories (Z, hidden commitments distinct from arbitrary activations), and generic serial compute budget (B). This triad lets the field talk about reasoning without silently conflating representation with computation.

2. **Three Competing Testable Hypotheses (H1, H2, H0).** The author converts loose intuitions into three falsifiable hypotheses: H1 latent-trajectory mediation, H2 surface-CoT mediation, and H0 generic-serial-compute null. Each hypothesis yields asymmetric diagnostic predictions, enabling empirical adjudication rather than appeal to intuition.

3. **Compute-Audited Factorized Experimental Design.** A minimal six-arm design (baseline, surface manipulation + matched control, latent intervention + matched control, compute-only expansion) enforces that every comparison isolates one factor under a precise `B_eq` ledger accounting for decode, KV-cache, hooks, verifier calls, tools, and branch expansions.

4. **Regime Taxonomy and the "Substrate Switch".** The paper introduces four regimes -- ordinary, constitutive, search-dominant, and mixed -- and empirically demonstrates that the winning hypothesis switches across them. This reframes the question from "which hypothesis is true?" to "which substrate dominates under which task conditions?"

5. **Mediator Test Battery for Latent Reasoning.** For claims about Z, the author specifies a causal qualification pipeline -- temporal precedence, necessity (ablation), sufficiency (patching), specificity against shams, and direct Z-vs-S preservation contrast -- raising the bar above probe-only correlational evidence.

---

## Key Findings

**Frontier verdicts across regimes (accuracy-cost winners, 3 models: Qwen3-8B, Qwen3-32B, Llama-3.1-8B-Instruct):**

| Regime | Controlled Tier Winner | Gap | Naturalistic Benchmark | Winner | Gap |
|--------|------------------------|-----|------------------------|--------|-----|
| Ordinary | **Latent (H1)** | ~2.4% | GSM8K-Platinum | **Latent (H1)** | ~1.9% |
| Constitutive | **Surface (H2)** | ~2.1% | HotpotQA (gated) | **Surface (H2)** | ~2.3% |
| Search-dominant | **Compute (H0)** | ~3.2% | MATH-500 | **Compute (H0)** | ~3.4% |
| Mixed | No winner | ~0.5% | HumanEval+ | No winner | ~0.6% |

**Mediator tests for H1 in ordinary regimes:**

- Temporal precedence: Z* predictive early (Early AUC ~0.70--0.72)
- Necessity: ablating Z* drops accuracy by 8.6--9.4%
- Sufficiency: patching correct Z* rescues 6.3--7.0%
- Z-vs-S contrast: preserving Z* while corrupting S is +4.9% to +5.6% better than the inverse
- In constitutive regimes this contrast sharply contracts and reverses -- as predicted

---

## Suggestions & Future Directions

1. **Adopt latent-state dynamics as the default object of study.** Probe-only readouts should be complemented with mediator-qualifying causal follow-ups (ablation, patching, sham controls).

2. **Evaluate reasoning with factorized, compute-audited designs.** Disentangle S, Z, and B explicitly; use a precise `B_eq` budget ledger; pair targeted manipulations with compute-matched controls; pre-specify differential verdict rules.

3. **Refine safety monitoring beyond surface CoT.** Because latent reasoning can outrun or diverge from verbalization, safety protocols that rely only on reading visible traces may miss the actual decision substrate.

4. **Design benchmarks that resist substrate confounding.** Tasks that would credit H0 or H2 wins as reasoning may be measuring compute budget or surface fidelity rather than the intended capability.

5. **Extend the regime taxonomy.** Open questions include how substrate dominance shifts with scale, tool use, multi-agent settings, and long-horizon planning.

---

## Authors & Institutions

Wenshuo Wang (School of Future Technology, South China University of Technology, China).
