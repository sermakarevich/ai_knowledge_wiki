> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Theories of Hyperparameters

### Overview

Training a deep neural network involves a surprisingly large number of numerical knobs. The paper groups these into two broad families:

- **Optimization hyperparameters** -- learning rate, batch size, momentum, weight-decay, initialization variance, and the choice of optimizer algorithm itself.
- **Architecture hyperparameters** -- width, depth, output multiplier, and related structural choices.

The proliferation of these knobs is a double burden. For practitioners, it means extensive and expensive tuning to reach peak performance. For researchers, it means that every empirical result comes entangled with a choice of hyperparameters, making it hard to isolate the causal effect of any single variable. Simon et al. argue that this situation is not irreducible -- it is, rather, a sign that the right theoretical language has not yet been applied.

> "It is only in the last few years that the theory community has come to realize that hyperparameters can be disentangled and understood, and that the resulting mathematics is often both useful for practitioners and clarifying for theorists."

The analogy drawn in the paper is to dimensional analysis and dimensionless numbers in classical physics. In fluid dynamics, the Reynolds number Re = ρvL/μ (density × velocity × length scale / viscosity) distills four separate physical quantities into one dimensionless ratio that determines whether flow is laminar or turbulent. You do not need to solve the full Navier-Stokes equations to answer many practical questions -- you just need to know where Re sits relative to the critical threshold. Similarly, the right theoretical framework for deep learning hyperparameters can give a coarse but reliable picture of how the system behaves as you vary its knobs, without requiring a complete solution of the optimization dynamics.

> "While solving the optimization dynamics of a neural network is very difficult, it is often very helpful to quickly obtain a coarse picture of how things change if you change one or more hyperparameters."

The section surveys two interconnected lines of work that have made this program concrete: theories of optimization hyperparameters (principally learning rate and batch size) and theories of architecture hyperparameters (principally width scaling under the Tensor Programs framework).

---

### Optimization Hyperparameters

#### The Linear Scaling Rule for SGD

Stochastic gradient descent has two primary hyperparameters: the learning rate η and the batch size B. A fundamental empirical observation -- formalized as the **linear scaling rule** by Goyal et al. [2017] -- is that the training trajectory is approximately invariant under the joint rescaling:

```
η  →  k · η
B  →  k · B
T  →  T / k   (steps, keeping total examples seen fixed)
```

That is, if you multiply both the learning rate and the batch size by the same factor k, and simultaneously reduce the number of optimizer steps by k (so that the total number of training examples consumed remains constant), the loss curve and final model quality stay nearly the same. In practice this means that a learning rate tuned for a small batch can be transferred to a larger batch simply by scaling it proportionally -- a highly practical result for distributed training, where large batch sizes are natural.

The theoretical underpinning comes from interpreting SGD as a discretization of an underlying **stochastic differential equation (SDE)**. In continuous time, SGD with learning rate η and batch size B approximates a Langevin-type SDE:

```
dθ = -∇L(θ) dt  +  (η/B)^{1/2} · σ(θ) dW
```

where σ(θ) captures gradient noise and W is a Wiener process. In this formulation, the noise magnitude is proportional to η/B. Holding η/B fixed while scaling both η and B by k therefore keeps the SDE identical -- explaining why the trajectory is invariant. Several parallel theoretical works converged on this picture: Mandt et al. [2017], Jastrzebski et al. [2017], Chaudhari and Soatto [2018], and Li et al. [2019, 2021b] each derived the linear scaling rule from the SDE perspective.

#### Adaptive Optimizers and the Square-Root Scaling Rule

The SDE analysis is clean for vanilla SGD but requires extension for the adaptive optimizers (Adam, RMSProp, Adagrad) that dominate modern practice. Malladi et al. [2022] carried out this extension and found a different scaling relationship: for adaptive optimizers, the learning rate should scale with the **square root** of the batch size:

```
η_adaptive  ∝  B^{1/2}
```

Intuitively, adaptive methods normalize gradients element-wise, which changes how gradient noise scales with batch size compared to the vanilla SGD case. The SDE framework again provides the language to make this precise: the effective noise term in the adaptive SDE scales differently, leading to the square-root rather than linear relationship.

This result matters because in large-scale training -- LLMs, vision transformers -- Adam variants are nearly universal. Having a principled rule for transferring the learning rate across batch sizes (rather than re-tuning from scratch) directly reduces the computational cost of distributed training experiments.

#### The Batch Size Tradeoff and the Critical Batch Size

The invariance perspective tells you how to translate a hyperparameter setting from one batch size to another, but it does not tell you which batch size to use in the first place. Choosing B involves a genuine tradeoff between two resources:

- **Serial time** -- the number of sequential optimizer steps required to reach a target loss.
- **Compute** -- the total number of floating-point operations (closely tied to wall-clock cost and financial cost).

At the extremes: a practitioner who cares only about serial time should use the full dataset as a single batch (gradient descent), since each step is then as informative as possible. A practitioner who cares only about cost should use batch size 1, since each example provides a noisy but unbiased gradient at minimal compute per step. Real practitioners face both constraints simultaneously.

McCandlish et al. [2018] formalized this tradeoff with a simple model showing that the **Pareto frontier** between serial time and compute takes the form of a **hyperbola**. The concept of a **critical batch size** B_crit characterizes the point on this hyperbola where you begin sacrificing one resource meaningfully to gain the other. Below B_crit, adding parallelism (more compute per step) gives roughly proportional reductions in steps. Above B_crit, adding more compute gives diminishing returns on serial time -- you are in the "compute-wasteful" regime.

Work by Ma et al. [2018], Jain et al. [2018], and Shallue et al. [2019] contributed complementary analyses of this tradeoff. Together they provide a framework for deciding batch size based on the relative value placed on the two resources -- a much more principled basis than brute-force grid search.

#### Implicit Regularization of Loss Curvature

Beyond governing the speed and cost of training, optimization hyperparameters also affect the **trajectory** that training follows through parameter space, and therefore properties of the learned network such as:

- **Generalization performance** (Keskar et al. [2016], Schulman and Lab [2025])
- **Compressibility / pruning behavior** (Catalan-Tatjer et al. [2025], Barsbey et al. [2025])

A rich line of work has sought to explain these implicit effects through a single unifying hypothesis: **many of the side-effects of optimizer hyperparameters can be understood as implicit regularization of loss-function curvature (i.e., the Hessian of the loss).**

The empirical observation came first. Keskar et al. [2016] and Jastrzebski et al. [2017, 2020] and Cohen et al. [2021a] all found that first-order optimizers (SGD, Adam) implicitly regularize the trace or eigenvalues of the Hessian, with:

- Larger learning rates → stronger curvature regularization (flatter minima)
- Smaller batch sizes → stronger curvature regularization (flatter minima)

This aligned with the empirical finding that large-batch training tends to converge to sharper, less-generalizing minima unless the learning rate is scaled up correspondingly.

The theoretical explanation came from Taylor-expanding the loss objective to third order. Standard gradient flow minimizes a first-order approximation; the second-order (Hessian) term is what curvature regularization controls. When the optimizer dynamics oscillate or fluctuate -- as they do with finite step sizes, stochastic batches, or adaptive learning rates -- a third-order calculation reveals that these oscillations automatically induce an **effective curvature penalty** on the trajectory. Theoretical works in simplified settings that established this mechanism include Blanc et al. [2020], Li et al. [2021c], Damian et al. [2021], Wen et al. [2022], and Li et al. [2025].

The paper notes a suggestive analogy to **Ito's correction** in stochastic calculus: after a nonlinear transformation, noise contributes an additional deterministic drift term. Similarly, stochastic or oscillatory optimization dynamics may be described by an effective flow on a modified loss.

> "As a result, we now have a mathematical understanding of the learning rate in full-batch gradient descent, and are mostly free to instead study the simpler dynamics of gradient flow plus a loss curvature penalty."

Cohen et al. [2025] pushed this program to its logical conclusion for the full-batch setting. They showed that for **several optimizers** applied to **realistic neural networks**, the entire training trajectory is well-modeled by:

```
gradient flow on [L(θ) + λ · C(θ)]
```

where L(θ) is the original loss, C(θ) is a curvature penalty (whose form depends on the optimizer), and λ is a strength parameter that depends on the hyperparameters (learning rate, momentum, etc.). The role of the hyperparameters is thus reduced to two quantities: the form of C and the magnitude λ. This is a substantial conceptual simplification -- instead of reasoning about the hyperparameters directly, one can reason about their effect on the curvature landscape.

There is an additional, though apparently weaker, implicit regularization effect: regularization of the **gradient norm** itself (Barrett and Dherin [2020], Smith et al. [2021]).

For stochastic settings and adaptive optimizers, analogous characterizations have been developed in more specialized contexts by Pesme et al. [2021] and Chen et al. [2024], but a fully unified treatment remains an important open direction (Open Direction 8 in the paper).

> "Fully extending this characterization to stochastic and adaptive optimizers would give us a common language for reasoning about the implicit effects of optimization hyperparameters on the training trajectory."

The research program then breaks into two connected questions: (1) characterize how hyperparameters determine the effective curvature penalty, and (2) understand how the curvature penalty in turn determines properties of the learned network. The first question is now substantially answered for the full-batch case; the second remains open.

---

### Architecture Hyperparameters: The Tensor Programs Framework and μP

#### The Problem of Width Scaling

Width is the most obvious architecture hyperparameter for a neural network. Practitioners routinely double, quadruple, or multiply by orders of magnitude the hidden dimension of transformer layers or residual blocks. But width interacts non-trivially with the learning rate, initialization scale, and output multiplier. Under "standard" parameterization (the default in most frameworks), as width increases:

- The optimal learning rate **shifts** -- wider networks require smaller learning rates.
- Hyperparameters tuned on narrow proxy models do **not** transfer reliably to wide target models.
- Wider networks do not always outperform narrower ones if hyperparameters are not re-tuned.

This fragility is a serious practical problem in the era of large-scale neural network development, where running a full hyperparameter sweep on a billion-parameter model is prohibitively expensive.

#### Tensor Programs: A Systematic Framework

The **Tensor Programs** framework, developed by Yang and collaborators (Yang and Hu [2021], Yang and Littwin [2023]), provides a systematic language for analyzing how neural network computations behave as width goes to infinity. The key move is to write hyperparameters explicitly as functions of width. For example, the learning rate takes the form:

```
η = η_0 · width^c
```

where η_0 is a scale-independent coefficient and c is an exponent to be determined by theory. Similarly, initialization variance and output multipliers are written with their own width-dependent exponents.

The Tensor Programs framework then asks a sharp question: for what choices of these exponents does the infinite-width limit retain **non-trivial, non-explosive** training behavior? The analysis tracks feature evolution -- how the representations in each layer change during training -- as width grows.

A remarkable finding is that all valid (non-trivial, non-explosive) choices of exponents yield one of exactly **two limiting behaviors**:

1. **Neural Tangent Parameterization (NTP)** -- features are **frozen** during training. The network behaves like a linear model in function space. This corresponds to the lazy regime described in the paper's Section 2.2.

2. **Maximal Update Parameterization (μP)** -- features **evolve** during training. The network genuinely learns new representations, corresponding to the rich regime.

This dichotomy is the architecture-hyperparameter analog of the rich/lazy dichotomy identified through the study of feature learning (Section 2.2 of the paper). The two analyses converge on the same fundamental distinction from different starting points.

#### Maximal Update Parameterization (μP)

Since feature learning is essential for performance on most real tasks, the analysis directly resolves a key question: **μP is the correct parameterization to use when scaling width.** NTP, by freezing features at infinite width, fails to capture the behavior of realistic trained networks.

The practical consequence is significant. Yang and Hu [2021] and Yang et al. [2022] showed that under μP, the optimal learning rate **remains nearly constant across widths**:

> "Under μP, by contrast, the optimal learning rate remains nearly constant across widths, making it possible to predict the learning rate for wide networks from experiments on narrower, cheaper models. Reproduced from Yang et al. [2022]."

This is illustrated in Figure 5 of the paper (reproduced from Yang et al. [2022]), which shows transformer training loss as a function of learning rate for models of varying width (128 to 8192):

- **Standard parameterization (left panel):** The optimal learning rate shifts systematically as width increases. A learning rate tuned at width 128 is badly suboptimal at width 4096.
- **μP (right panel):** The optimal learning rate is nearly identical across all widths. The loss curves align, and the optimum is stable.

The caption from the paper's source material is explicit: under standard practice, "different widths do not share the same optimal hyperparameter; wider networks do not always perform better than narrower ones; in fact they underperform the same-width networks in our technique even after tuning learning rate."

This unlocks a new **hyperparameter transfer paradigm** (called μTransfer by Yang et al. [2022]):

1. Express your target model in μP.
2. Tune hyperparameters on a small, cheap proxy model.
3. Transfer those hyperparameters directly to the large, production-size model -- no retuning required.

The paper's source material describes the verification: μTransfer was applied to Transformer and ResNet architectures, matching published numbers for BERT-large (350M parameters) by tuning on a 13M-parameter model, and matching published numbers for GPT-3 (6.7B parameters) by tuning on a much smaller model -- in each case at a tiny fraction of the full pretraining compute cost. A PyTorch implementation is publicly available at github.com/microsoft/mup.

#### The Gap Between Theory and Practice

The theoretical underpinning of μP is asymptotic -- it holds exactly only in the limit of infinite width. Real models are trained at widths far smaller than the dataset size, and the empirical success of μTransfer depends on how quickly the optimal hyperparameters stabilize as width grows.

The paper acknowledges this gap directly:

> "At the same time, the theory underpinning this result is asymptotic and does not fully account for its empirical effectiveness."

Recent work has begun to close this gap. Noci et al. [2024], Ghosh et al. [2025], and Hayou [2025] provide evidence that a small set of **spectral statistics** of the weight matrices stabilize rapidly across widths under μP, and that these statistics approximately govern the optimal hyperparameters. This suggests that the effective dimension of the hyperparameter space -- the set of quantities that actually determine behavior -- is low, and that this low-dimensional structure emerges quickly even at finite width.

#### Extending to Depth and Other Scaling Dimensions

The width-scaling analysis has been extended to **depth scaling** by Yang et al. [2023b], Bordelon et al. [2023], and Dey et al. [2025]. Depth introduces additional complications because the relevant quantities (e.g., per-layer learning rate scales, residual connection magnitudes) interact in more complex ways than width alone.

The paper identifies extending this scaling-centric approach to other architectural dimensions -- such as the number of attention heads, the size of the key/query dimension, or mixture-of-experts routing parameters -- as an important future direction (Open Direction 6).

---

### Synthesis: What This Line of Evidence Shows

The two bodies of work surveyed in this section -- theories of optimization hyperparameters and theories of architecture hyperparameters -- share a common structure and a common lesson.

**Common structure.** In each case, the theoretical advance consists of identifying a principled parameterization under which hyperparameters decouple or become transferable:

- For SGD, the SDE perspective reveals that η and B appear only through their ratio η/B in the noise magnitude, so they are not independent degrees of freedom -- the ratio is the effective parameter.
- For adaptive optimizers, an analogous (but different) combination governs the noise.
- For width scaling under μP, the exponents c governing each layer's learning rate and initialization scale are fixed by the requirement of non-trivial infinite-width dynamics, leaving only scale-independent coefficients as free parameters -- and those coefficients transfer across widths.

**Common lesson.** With the right parameterization, the effective dimensionality of the hyperparameter space collapses. What looked like a high-dimensional tuning problem -- learning rate, batch size, momentum, width, initialization -- turns out to be a lower-dimensional problem once the correct invariances are identified.

This mirrors the Reynolds number story in fluid dynamics. The Reynolds number Re = ρvL/μ is not merely a convenient summary -- it is the natural variable in which the physics is simple. Below a critical Re, flow is laminar regardless of which individual parameter (speed, pipe size, viscosity) you vary. Above it, flow is turbulent. The physics does not care about the four individual parameters; it cares about their combination. The Tensor Programs framework and the SDE-based scaling rules play an analogous role for deep learning: they identify the natural variables in which training dynamics are simple and transferable.

The paper frames this as one of five converging lines of evidence that a scientific theory of deep learning is within reach. The evidence is not merely that empirical scaling rules exist -- it is that those rules are **explained** by mathematics, that the explanatory theories are **predictive** (they correctly anticipate μTransfer, the square-root scaling for Adam, the curvature-regularization picture), and that the theories **reduce** the complexity of the phenomena (from many hyperparameters to a few effective quantities).

> "It is only in the last few years that the theory community has come to realize that hyperparameters can be disentangled and understood, and that the resulting mathematics is often both useful for practitioners and clarifying for theorists."

The remaining open challenge -- noted explicitly in the paper -- is to complete this program for stochastic and adaptive optimizers in the implicit-regularization story (Open Direction 8), and to extend the Tensor Programs architecture analysis to dimensions beyond width and depth (Open Direction 6). But the existence of a coherent framework, with concrete predictions already validated at scale, is itself strong evidence that the theoretical program is on the right track.

---

### Key References

The following works are cited in Section 2.4 of Simon et al. [2026] and are central to the lines of evidence described here:

**Linear scaling rule and SGD SDE theory**
- Goyal et al. [2017] -- original linear scaling rule for distributed training
- Mandt et al. [2017] -- SDE perspective on SGD
- Jastrzebski et al. [2017, 2020] -- SDE analysis and curvature observations
- Chaudhari and Soatto [2018] -- entropy-SGD / SDE connection
- Li et al. [2019, 2021b] -- theoretical derivation of linear scaling from SDE

**Adaptive optimizer scaling**
- Malladi et al. [2022] -- square-root scaling rule for Adam from SDE analysis

**Batch size tradeoffs**
- Ma et al. [2018], Jain et al. [2018] -- theoretical batch size tradeoff analyses
- McCandlish et al. [2018] -- critical batch size and hyperbola Pareto frontier
- Shallue et al. [2019] -- empirical study of batch size tradeoffs

**Implicit curvature regularization**
- Keskar et al. [2016] -- sharp vs. flat minima in large-batch training
- Cohen et al. [2021a] -- empirical curvature regularization by optimizers
- Blanc et al. [2020], Li et al. [2021c], Damian et al. [2021], Wen et al. [2022], Li et al. [2025] -- theoretical explanations via Taylor expansion
- Cohen et al. [2025] -- curvature-penalized gradient flow model for full training trajectory
- Barrett and Dherin [2020], Smith et al. [2021] -- implicit gradient norm regularization
- Pesme et al. [2021], Chen et al. [2024] -- stochastic settings

**Generalization and compressibility effects**
- Schulman and Lab [2025] -- generalization effects of hyperparameters
- Catalan-Tatjer et al. [2025], Barsbey et al. [2025] -- compressibility effects

**Tensor Programs and μP**
- Yang and Hu [2021] -- Tensor Programs framework, introduction of μP
- Yang and Littwin [2023] -- further Tensor Programs theory
- Yang et al. [2022] -- μTransfer: hyperparameter transfer across widths (verified on Transformer, ResNet, BERT-large, GPT-3)
- Noci et al. [2024], Ghosh et al. [2025], Hayou [2025] -- finite-width stabilization of spectral statistics under μP

**Depth scaling extensions**
- Yang et al. [2023b], Bordelon et al. [2023], Dey et al. [2025] -- Tensor Programs extended to depth scaling
