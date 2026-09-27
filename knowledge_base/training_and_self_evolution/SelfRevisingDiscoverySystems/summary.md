# Self-Revising Discovery Systems for Science: A Categorical Framework for Agentic Artificial Intelligence

**Paper:** [Self-Revising Discovery Systems for Science: A Categorical Framework for Agentic Artificial Intelligence (Wang & Buehler, 2026)](https://arxiv.org/abs/2606.01444)

## Human Readable TL;DR

Imagine a scientist who not only finds new answers but also invents new words to describe what they found -- changing the very language of science, not just filling in the blanks. This paper builds a mathematical rulebook for AI scientists that can do the same: not just get better answers within an existing framework, but recognize when the framework itself is broken and upgrade it. Like a mechanic who not only fixes a car but redesigns the engine when needed -- and keeps a precise paper trail of every change so anyone can audit exactly what was discovered and why.

## TL;DR

This paper introduces a category-theoretic framework that formally distinguishes three operations in agentic scientific AI: *retrieval* (finding existing artifacts), *search* (exploring within a fixed schema), and *discovery* (changing the schema itself). Artifact states are modeled as copresheaves over a schema category; provenance is the category of elements; and discovery is a verified regime transition with left Kan extension transporting old evidence into the new vocabulary. The framework is instantiated in two systems -- Builder/Breaker (protein mechanics, MDL-gated symbolic model revision) and CategoryScienceClaw (proof-carrying categorical layer over ScienceClaw) -- demonstrating both quantitative world-model revision and auditable, typed scientific workflows.

---

## Problem & Motivation

Current AI scientists are highly capable at recombining and optimizing within a *fixed* scientific vocabulary (types, operations, verifiers). But genuine scientific progress often requires *changing* that vocabulary -- introducing new effective variables, admissible operations, new verifiers, or new artifact types. There is no formal, operational definition of when an agentic system is merely searching within a fixed regime vs. enlarging the regime itself. Without such a definition, verifiers can't be properly designed, provenance can't be rigorously audited, and progress can't be meaningfully measured. This paper extracts an operational formalization of scientific regime change from the philosophical tradition (Popper, Kuhn, Lakatos) and provides a mathematical substrate for engineering self-revising AI discovery systems.

---

## Main Original Ideas

1. **Discovery Regime as a Categorical Tuple** -- A regime `b = (S_b, Γ_b, V_b, L_b)` consists of a schema category of artifact types and operations, a grammar for composition, a verifier/gate, and an optional description-length functional. This formalizes what a scientific AI "knows how to talk about" at any given moment.

2. **Artifact State as a Copresheaf** -- The system's state at time `t` is a copresheaf `I_t : S_b → Set`, mapping each artifact type to the set of actual artifacts of that type. The category of elements `∫ I_t` is the realized, typed provenance graph -- every artifact with its causal lineage.

3. **Fixed-Regime Updates as Endofunctors** -- Operations within a fixed regime are endofunctors that must preserve provenance-preserving refinements (injective natural transformations). This enforces an audit contract: operations can add or annotate artifacts, but never silently merge distinct accepted artifacts.

4. **Discovery as Verified Regime Transition + Kan Extension** -- Discovery is a schema functor `u : S_b → S_b'`. Old artifacts are transported into the new regime via the left Kan extension `Lan_u I_t`. The *residual content* -- artifacts in the new state not reachable by transport -- is the objective, quantifiable measure of what was genuinely discovered.

5. **Retrieval / Search / Discovery Triptych** -- Three structurally distinct operations are cleanly separated: retrieval adds already-representable artifacts; search finds new paths within a fixed schema; discovery changes the schema. This separation drives verifier design, provenance auditing, and progress measurement.

6. **Kan-Transport Audit** -- A post-hoc diagnostic classifying new artifact types as "generator-reachable" (unary transform of an old type) vs. "composite-reachable" (requiring new multi-input operations) -- distinguishing feature engineering from a deeper change in compositional grammar.

---

## Key Findings

### Builder/Breaker Protein Mechanics (MDL-Gated Symbolic Revision)

| Iteration | Evidence (residues) | R² | Accepted Description Length (bits) |
|-----------|--------------------|----|--------------------------------------|
| 0 | 122 | 0.48 | baseline |
| 1 | 263 | 0.68 | reduced |
| 2 | 691 | 0.54 | further reduced |
| 3 | 1171 | 0.41 | 2016.5 (−337.6 from start of inner search) |

- The system discovered a **mode-conditioned compliance** relation: `B̂(z)_pi = α + β ϕ_pi ψ_pi`, where `ϕ_pi` is log-compliance and `ψ_pi` is ReLU-mode participation. This emerged as a *new interaction type* (product operation), not an additive term.
- `LogCompliance` and `ReLUModeAmplitude` were generator-reachable; `ModeConditionedCompliance` was only composite-reachable -- requiring the newly admitted product morphism. This confirms a true regime change.
- Non-monotonic R² (0.48 → 0.68 → 0.54 → 0.41) reflects expanding adversarial evidence sets, not failure; MDL acceptance remains valid because it accounts for evidence breadth and model complexity together.
- Rejected edits and retractions remain first-class audit objects.

### CategoryScienceClaw Fiber-Network Mechanics

- Candidate models compared: isotropic fiber-count descriptor `M_0` vs. orientation-tensor anisotropic stiffness surrogate `M_1`.
- AIC gate accepted `M_1` with **ΔAIC = 123.87**.
- Recovered: dominant orientation S = 0.673, principal axis 47.88°, stiffness E = 119.4 kPa, R² = 0.999989.
- Residual content (not obtainable by transporting old inputs): orientation tensor, principal axis, anisotropic stiffness surrogate, gate record, perturbation stress test.
- Rejected model `M_0` retained as inspectable provenance -- not discarded.

---

## Suggestions & Future Directions

1. **Convergence on growing regimes** -- Under what conditions does a sequence of regime transitions `b_0 → b_1 → b_2 → ...` converge in an appropriate colimit? When is non-convergence productive exploration vs. unproductive oscillation?
2. **Scaling laws for discovery** -- How do discovery rates (rate, quality, and accepted value of regime enlargements) scale with model size, tool diversity, simulator fidelity, evidence heterogeneity, and verifier strength?
3. **Verification tooling for agentic loops** -- Practical tooling is needed to replay artifact chains, check approximate naturality, account for description-length or pressure scores, and record retractions without deleting provenance.
4. **Learning the base schema category** -- Currently schema categories are engineered by hand. A major open problem is learning `S_b` and `L_b` from corpora, tool signatures, code, figures, and lab protocols at working scientific scale.
5. **Multicategorical discovery** -- Learning the typed multicategory or colored-operadic schema `M_b` from traces and artifact lineages, and estimating artifact and operation components of discovery cost at scale.

---

## Authors & Institutions

**Fiona Y. Wang** (Laboratory for Atomistic and Molecular Mechanics, Dept. of Biological Engineering, MIT) · **Markus J. Buehler** (Laboratory for Atomistic and Molecular Mechanics, Dept. of Civil and Environmental Engineering, Dept. of Mechanical Engineering, Center for Computational Science and Engineering, Schwarzman College of Computing, MIT)
