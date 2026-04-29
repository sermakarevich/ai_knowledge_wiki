# There Will Be a Scientific Theory of Deep Learning

**Paper:** [There Will Be a Scientific Theory of Deep Learning (Simon et al., 2026)](https://arxiv.org/abs/2604.21691)
**Deep dive:** [[details]]

## Human Readable TL;DR

Today, building large AI models is more like cooking with vague recipes than running a chemistry experiment -- engineers tweak settings until things work, but nobody can fully explain why. This paper argues we are on the verge of a "physics" of deep learning: a real scientific theory, like the one that turned steam-engine tinkering into thermodynamics, that can predict how networks behave instead of just describing what happens. The authors gather scattered research findings -- simple patterns, predictable scaling, and behaviors that appear in very different models -- as evidence that this theory is already starting to take shape. They name this emerging field "learning mechanics" and lay out a roadmap for building it.

## TL;DR

This is a position/synthesis paper advocating for an emerging scientific framework for deep learning, which the authors term "learning mechanics." Rather than presenting new empirical results, it consolidates five lines of evidence -- analytically solvable settings, insightful asymptotic limits, simple empirical laws, theories of hyperparameters, and universal phenomena -- to argue that a physics-style, first-principles theory of training dynamics, representations, and generalization is feasible and partially in place. The work draws explicit analogies to physics (NTK as harmonic oscillator, μP-style scaling as analogous to dimensionless physical parameters, neural scaling laws as Kepler-style empirical laws), and frames learning mechanics as the foundational "physics" complementary to mechanistic interpretability's "biology." It concludes with seven desiderata for the theory and ten open research directions, deliberately targeting newcomers to coordinate community progress.

---

## Problem & Motivation

Modern deep learning systems are nonconvex, overparameterized, and exhibit phenomena (structured internal representations, edge-of-stability training, neural collapse, smooth scaling laws) that classical learning theory -- PAC learning, statistical learning, convex optimization theory -- cannot predict or explain. Engineering progress has dramatically outpaced theoretical understanding, leaving practitioners reliant on trial-and-error. The authors argue this gap creates three pressures:

- **Scientific:** complex empirical systems with reproducible regularities are exactly what scientific theories are supposed to capture, analogous to how thermodynamics emerged from steam engines.
- **Practical:** model design, hyperparameter tuning, and scaling waste enormous compute because we lack predictive theory.
- **Safety-related:** governing increasingly powerful AI requires principled descriptions of behavior, not just black-box benchmarking.

The paper's motivation is to argue that the transition from "alchemy to science" is feasible and already underway, and to coordinate the field around a shared agenda.

---

## Main Original Ideas

1. **"Learning Mechanics" as a unifying frame.** The authors coin "learning mechanics" as a name for the emerging mathematical, first-principles theory of deep learning, deliberately analogizing to physics' classical and statistical mechanics. The frame consolidates fragmented theoretical efforts into a single research program.

2. **Seven desiderata for the theory.** It should be (1) fundamental (first-principles), (2) mathematical (quantitative statements), (3) predictive (empirically verifiable), (4) comprehensive (covering training, representations, weights, and performance), (5) intuitive (simple and illuminating), (6) useful (foundational for applied DL), and (7) humble (explicit about its regime of applicability).

3. **Five lines of evidence framework.** The paper organizes existing theoretical results into five categories that mirror established scientific methodologies: solvable settings (deep linear nets, NTK), insightful limits (infinite width/depth), simple empirical laws (scaling laws, edge of stability, neural collapse), theories of hyperparameters (linear scaling rule, μP), and universality (across architectures, data, representations).

4. **Discretization hypothesis.** A conceptual proposal that finite neural networks should be understood as noisy, finite approximations of infinite-sized continuous systems -- with finite width, depth, learning rate, and batch size acting as discretization errors of ideal continuous limits.

5. **Symbiosis with mechanistic interpretability.** Learning mechanics is positioned as the "physics" providing first-principles, quantitative explanations for the empirical "biology" studied by mechanistic interpretability -- formalizing assumptions like linear representability, locality, and sparsity, and explaining how mechanisms emerge dynamically during training.

6. **Research roadmap and outreach.** Ten concrete open directions are outlined, and the paper deliberately targets newcomers to lower barriers to entry and coordinate community effort.

---

## Key Findings

This is a synthesis/position paper rather than an empirical work, so "findings" take the form of consolidated evidence that a scientific theory is emerging:

- **Solvable models capture real behaviors.** Deep linear networks reproduce key DL phenomena (saddle points, phase transitions, edge-of-stability oscillations, initialization-dependent low-rank biases). The Neural Tangent Kernel (NTK) accurately predicts generalization error, double descent, and aspects of scaling laws in the lazy regime.
- **Limits illuminate structure.** The lazy/rich (kernel vs. feature-learning) dichotomy at infinite width is controlled by initialization scaling. Maximal Update Parameterization (μP) preserves feature learning at scale and enables hyperparameter transfer across model sizes. Infinite-depth limits split into smooth-flow vs. diffusive regimes for residual networks.
- **Empirical laws are robust.** Power-law neural scaling laws (Kaplan et al. 2020), edge-of-stability sharpness stabilizing near 2/η (Cohen et al. 2021), neural collapse to a regular simplex (Papyan et al. 2020), and the neural feature ansatz (Radhakrishnan et al. 2024) reproduce across architectures and datasets.
- **Hyperparameters obey rules.** The linear scaling rule for learning rate and batch size (and adaptive-optimizer extensions) is derivable from SDE models. Optimizers implicitly regularize loss-landscape curvature, simplifying their effective dynamics.
- **Universality is real.** Different architectures (e.g., transformers vs. UNets in diffusion models) can produce nearly identical input-output mappings when matched on resources. Representations across initializations, architectures, datasets, and even biological systems converge with scale ("Platonic representations").

---

## Suggestions & Future Directions

The authors outline a research agenda with roughly ten open directions:

1. **Build a unified framework for nonlinear feature learning** that goes beyond isolated toy models (multi-index, quadratic activation, teacher-student) into a coherent theory.
2. **Derive scaling laws from first principles**, rather than fitting them empirically.
3. **Develop the discretization hypothesis quantitatively**, treating finite networks as discretizations of continuous infinite-size systems.
4. **Extend μP-style hyperparameter transfer** to more architectural and training axes (depth, context length, attention heads).
5. **Formalize the assumptions of mechanistic interpretability** (linear representability, locality, sparsity) within learning mechanics.
6. **Explain the dynamical emergence** of learned mechanisms and circuits during training.
7. **Characterize universal data statistics** (power-law spectra, hierarchical structure, Zipf's law, sparsity) that underpin DL's cross-modal success.
8. **Bridge to neuroscience and cognitive science** via shared representational and learning principles.
9. **Develop predictive tools** for dataset design, optimizer choice, and resource allocation.
10. **Coordinate community effort** and lower barriers to entry for new researchers from diverse backgrounds.

The authors are explicit about humility: the theory should announce its regime of applicability and not overclaim. Key phenomena -- genuine nonlinear feature learning at scale, optimizer-specific effects, full transformer dynamics -- remain open challenges.

---

## Authors & Institutions

Jamie Simon (UC Berkeley, Imbue), Daniel Kunin (UC Berkeley), Alexander Atanasov (Harvard), Enric Boix-Adserà (University of Pennsylvania), Blake Bordelon (Harvard), Jeremy Cohen (Flatiron Institute), Nikhil Ghosh (Flatiron Institute), Florentin Guth (NYU & Flatiron Institute), Arthur Jacot (NYU), Mason Kamb (Stanford), Dhruva Karkada (UC Berkeley), Eric J. Michaud (Astera Institute), Berkan Ottlik (University of Pennsylvania), Joseph Turnbull (UC Berkeley).
