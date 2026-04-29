> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Analytically Solvable Settings

### Overview and Motivation

The first line of evidence for an emerging scientific theory of deep learning is the existence of a rich landscape of analytically solvable minimal models. The core argument is methodological: science routinely builds understanding of complex systems by first studying pared-down, representative settings where quantitative calculation is tractable. The paper draws an explicit analogy to physics:

> "physics uses representative solvable settings like the harmonic oscillator and the hydrogen atom as sources of intuition for much broader classes of system."

Deep learning appears unusually amenable to this approach. Scientists have identified many minimal models where learning dynamics simplify enough that quantities of interest -- loss landscapes, generalization error, training trajectories -- can be computed in closed form or reduced to low-dimensional dynamical systems.

The paper's framing has two complementary faces. First, solvable settings are *exploratory*: they reveal phenomena and mechanisms to look for when studying realistic deep learning. Second, they are *constitutive*: any eventual complete theory of deep learning must encompass these simplified cases. Their solutions may serve as "nucleation sites from which a more general theory crystallizes."

The unifying technical strategy highlighted in Section 2.1 is **linearization** -- and the section develops two distinct instantiations of the idea, followed by a discussion of progress beyond linearization.

---

### Linearization in the Data: Deep Linear Networks

#### What a Deep Linear Network Is

A deep linear network is obtained by stripping all nonlinearities from a neural network architecture. The result is a composition of linear maps:

```
f(x; θ) = W_L · W_{L-1} · ... · W_1 · x
```

where `θ := {W_ℓ}_{ℓ=1}^{L}`, each `W_ℓ` is a real matrix (a linear transformation), and `L ≥ 2`. This is equation (1) in the paper.

The model is **linear in its inputs x** but remains **highly nonlinear in its parameters θ** because the weight matrices are multiplied together. This nonlinearity in parameters is what makes deep linear networks interesting: they are not trivially equivalent to shallow linear regression, and they preserve many structural features of deep learning while discarding others.

#### Why Deep Linear Networks Are a Useful Proxy

Despite their simplicity, deep linear networks retain a striking set of hallmark behaviors of real deep learning. The paper lists:

- **Saddle-point-dominated loss landscapes** -- the loss surface is non-convex and contains many saddle points, not just global minima. This was identified early by Baldi and Hornik [1989].
- **Sharp phase transitions and separation of timescales** during training -- different components of the task are learned at very different rates, leading to step-function-like dynamics [Gissin et al., 2019; Atanasov et al., 2021].
- **Edge-of-stability oscillations with gradient descent** -- when learning rates are large, gradient descent exhibits oscillations at the edge of numerical stability even in these linear settings [Even et al., 2023].
- **Strong initialization-dependent inductive biases** -- what the network learns and how quickly depends sensitively on how the weights are initialized [Woodworth et al., 2020; Kunin et al., 2024].

The survival of these phenomena in a tractable linear setting is what makes deep linear networks scientifically valuable: they can be studied exactly, yet the lessons transfer to the nonlinear case.

#### The Gradient Flow Framework

Analysis of deep linear networks is typically carried out using the **gradient flow** learning rule -- the continuous-time limit of gradient descent, where the parameter update at each infinitesimal time step is proportional to the negative gradient of the loss. This eliminates the discrete step-size parameter and yields a system of ordinary differential equations (ODEs) governing the parameter trajectories.

Two additional simplifying assumptions are standard in the literature:

1. A specific choice of **data distribution** -- typically whitened inputs, `x ~ N(0, I)`, so the input covariance is the identity. This decouples the dynamics across different directions in input space.
2. A specific choice of **initialization** -- often what the paper calls a "task-aligned initialization" `θ^(0)`, meaning the initial weight matrices are arranged to align with the singular structure of the input-output correlation matrix.

Under these conditions, the paper reports that:

> "the learning dynamics can often be solved exactly or reduced to low-dimensional dynamical systems."

The key references for rigorous analysis under these assumptions are: Fukumizu [1998], Saxe et al. [2014], Tarmoun et al. [2021], and Dominé et al. [2025].

#### The Saxe et al. 2014 Result: Decoupled Bernoulli ODEs

The canonical result in this line of work is due to Saxe et al. [2014]. Under the task-aligned initialization and whitened inputs, the gradient flow dynamics of a deep linear network **decouple** into a set of independent, one-dimensional ODEs -- one for each singular mode of the input-output correlation matrix.

Each such ODE has the form of a **Bernoulli ODE**, which is exactly solvable. The solution describes a sigmoid-shaped trajectory: each singular mode remains near zero for a while, then rapidly switches on and saturates near its target value. This is the mathematical origin of the "sharp phase transitions and separation of timescales" listed above.

The consequence is a **sequential learning** phenomenon: singular modes associated with **larger singular values** are learned first, and modes associated with smaller singular values emerge later. Figure 1(a) in the paper (reproducing Figure 3 of Saxe et al. [2014]) shows the gradient flow dynamics of the singular values of the product matrix `W_2 W_1` as a function of training time, with exact theoretical curves matching experiment.

#### The Greedy Low-Rank Bias

The sequential learning result generalizes to a broader principle: deep networks exhibit a **greedy low-rank bias** -- they acquire components of the task in order of importance (as measured by singular value magnitude), rather than learning everything at once.

> "Canonical work by Saxe et al. [2014] first showed how deep linear networks learn singular vectors of the input–output correlation sequentially during training, with learning prioritized toward modes associated with the largest singular values."

This bias has a proposed functional significance: by learning the high-singular-value (high signal-to-noise) components first, the network effectively separates signal from noise during training [Lampinen and Ganguli, 2018]. The paper notes that this closely mirrors behavior in nonlinear networks, where "simpler functions are often learned before more complex ones" [Kalimeris et al., 2019; Simon et al., 2023b].

The greedy low-rank bias is also amplified by several factors studied in the literature:

- **Small initializations**: scaling down initial weights strengthens the low-rank bias [Gidel et al., 2019; Li et al., 2021a; Jacot et al., 2021; Pesme and Flammarion, 2023].
- **Increased depth**: adding more layers further concentrates learning on the dominant singular modes [Gunasekar et al., 2018; Arora et al., 2018, 2019b].
- **Stronger mini-batch noise**: stochastic gradient descent with larger batch noise pushes toward lower-rank solutions [Pesme et al., 2021; Chen et al., 2024].
- **Explicit `ℓ_2` regularization**: weight decay independently promotes low-rank solutions [Ziyin et al., 2022; Wang and Jacot, 2024].

The convergence of so many distinct mechanisms toward the same qualitative bias suggests it is a robust, structurally deep feature of deep learning, not an artifact of any one setting.

---

### Linearization in the Parameters: NTK and Kernel Methods

#### The Taylor Expansion Construction

A complementary linearization strategy operates in parameter space rather than data space. Given a neural network `f(x; θ)` with parameters `θ`, one can form its **first-order Taylor expansion around the initial parameters** `θ_0`:

```
f_lin(x; θ) = f(x; θ_0) + ∇_θ f(x; θ_0)^T (θ - θ_0)
```

where `∇_θ f(·; θ_0)` is the gradient of the network output with respect to parameters, evaluated at initialization. This is equation (2) in the paper.

The resulting model `f_lin` is **linear in the parameters** `θ -- θ_0` but remains **highly nonlinear in the data x** through the fixed feature map `∇_θ f(·; θ_0)`. This is the opposite of the deep linear network construction, which is linear in x and nonlinear in θ.

#### When the Linearization Is Accurate

The paper emphasizes that this is not merely a mathematical device:

> "This is not some contrived construction: in fact, there are settings in which a model is well-approximated throughout training by its linearization, i.e., ∀t, f(x; θ_t) ≈ f_lin(x; θ_t)."

Concretely, this approximation holds when:

- **Infinite width (or related overparameterization) limits** are taken -- any neural network architecture can be driven into the linearized regime by taking suitable limits [Jacot et al., 2018; Lee et al., 2019; Chizat et al., 2019; Liu et al., 2020]. This is further discussed in Section 2.2 of the paper (the mean-field and infinite-width limits, corresponding to Line of Evidence #2).
- **Fine-tuning of large language models** -- recent empirical evidence suggests that LLM fine-tuning occurs in a near-linearized regime, where parameter changes are small enough that the Taylor approximation remains accurate throughout [Malladi et al., 2023; Ren and Sutherland, 2025].

#### The Neural Tangent Kernel

Because a linearized network is linear in its parameters, its training dynamics under gradient descent on least-squares loss reduce exactly to **kernel ridge regression** -- but with a kernel determined by the network's architecture and initialization rather than by the raw data geometry.

The key object is the **neural tangent kernel (NTK)**, defined as:

```
K_NTK(x, x') := ∇_θ f(x; θ_0)^T ∇_θ f(x'; θ_0)
```

This is the inner product between the gradient feature maps at two data points. It measures how similarly the network's output at x and x' respond to a perturbation in parameters from initialization.

The contrast with ordinary linear regression is instructive: linear regression on features x uses the **Gram kernel** `K_Gram(x, x') = x^T x'`. The NTK replaces raw data geometry with gradient-space geometry. Since the gradient `∇_θ f(·; θ_0)` is shaped by the network architecture (depth, width, activation functions, etc.), the NTK encodes architectural inductive bias.

The NTK was introduced by Jacot et al. [2018], who showed that in the infinite-width limit the NTK is deterministic (does not depend on the random initialization) and remains constant throughout training, making the analysis exact.

#### What the NTK Framework Predicts

The paper identifies several concrete predictions that fall out of the NTK / linearized network analysis:

**1. Generalization error on arbitrary targets.** Because the NTK determines the learned predictor exactly (via kernel ridge regression), one can analytically compute the expected test error for any target function `f*`, given knowledge of the data distribution. This requires:

- The eigenstructure of the NTK (its eigenfunctions and eigenvalues, which encode what the network finds easy vs. hard to learn).
- The spectral decomposition of the target function in the NTK eigenbasis.
- The statistics of the input distribution.

This is made precise in work by Jacot et al. [2020], Canatar et al. [2021], Loureiro et al. [2021], Hastie et al. [2022], Wei et al. [2022], and Simon et al. [2023a]. Figure 1(b) in the paper (based on Figure 2 of Simon et al. [2023a]) shows this framework applied to realistic data (binarizations of CIFAR-5m), with theoretical predictions for test MSE matching experimental curves across a wide range of training set sizes.

**2. Inductive bias from architecture.** The NTK feature map `∇_θ f(·; θ_0)` is fully determined by the network architecture, so one can trace how architectural choices (depth, width, skip connections, convolutional structure, etc.) translate into the kernel's geometric properties and thus into which functions the model prefers to learn. This is studied in Arora et al. [2019c] and Geifman et al. [2020].

**3. Tendency to learn simple, generalizing functions.** Applying the NTK framework to realistic data distributions (not just toy Gaussian inputs) uncovers a mechanism by which linearized models preferentially learn low-frequency, smooth functions [Basri et al., 2020; Karkada et al., 2025]. This gives a theoretical grounding for the empirical observation that neural networks generalize despite being heavily overparameterized.

**4. Double descent.** The NTK / kernel framework can reproduce the "double descent" phenomenon -- the non-monotonic behavior of test error as a function of model size or training dataset size, where error first decreases, then increases (overfitting), then decreases again (interpolation regime) [Belkin et al., 2019; Advani et al., 2020].

**5. Scaling laws.** The NTK framework can also make predictions about how test error scales with dataset size n or model size -- the "scaling laws" that have become a central empirical regularity in large-scale deep learning [Caponnetto and de Vito, 2007; Pillaud-Vivien et al., 2018; Cui et al., 2023; Atanasov et al., 2024].

#### Limitations of Linearized Networks

Despite their theoretical power, linearized networks have recognized failure modes that the paper is explicit about:

> "However, despite these theoretical merits, linearized networks are unrealistic in a few critical ways."

The two most important limitations are:

**1. Absence of feature learning.** Real neural networks learn internal representations -- they transform inputs through a sequence of layers, and these intermediate representations change substantially during training. A linearized network, by construction, has a *fixed* feature map `∇_θ f(·; θ_0)` that does not change. It cannot discover new features; it can only reweight a fixed basis.

This leads to overly pessimistic predictions for sample complexity. Fully nonlinear networks can outperform kernel methods (including NTK) by factors that grow with problem dimension, because they exploit structure in the target function to learn task-relevant features with far fewer samples [Ghorbani et al., 2020; Vyas et al., 2022]. The NTK framework, being blind to feature learning, misses this advantage entirely.

**2. Avoidance of nonconvex optimization.** By reducing training to a tractable linear problem (kernel ridge regression), the linearized framework sidesteps the nonconvex loss landscape and the complex geometry of gradient descent trajectories in that landscape. These are intrinsic features of deep learning that the NTK analysis cannot illuminate.

These limitations motivate the next frontier: analytically tractable models that are genuinely nonlinear in both the data and the parameters.

---

### Beyond Linearization: Nonlinear Toy Models

#### The Frontier and Why It Is Hard

The paper frames the development of nonlinear solvable models as "an important frontier for theory":

> "An important frontier for theory lies in developing analytically tractable toy models that remain genuinely nonlinear in both the data and the parameters."

The core difficulty is that, once both data-nonlinearity and parameter-nonlinearity are present, the data distribution plays a much more complex role, making it hard to obtain unified, general frameworks. Existing work has proceeded by isolating specific nonlinear mechanisms and making them solvable under structured assumptions -- typically Gaussian inputs with structured target functions.

#### Gaussian Inputs and Multi-Index Models

One productive line works with **Gaussian inputs** `x ~ N(0, I)` and **structured target functions**. A particularly important family is **multi-index models**, where the target function depends on the input only through a small number of linear projections:

```
f*(x) = g(v_1^T x, v_2^T x, ..., v_k^T x)
```

for some low-dimensional link function g and directions `v_1, ..., v_k`. These targets have latent low-dimensional structure.

The key theoretical result in this line is a **separation theorem**: fully nonlinear neural networks provably outperform any kernel method (including NTK) in sample complexity, specifically because they can exploit the low-dimensional structure of multi-index targets to learn the relevant directions `v_1, ..., v_k` from data. This is proven in Abbe et al. [2022], Damian et al. [2022b], Bietti et al. [2022], Ba et al. [2022], and Dandi et al. [2023].

Complementarily, methods from **statistical physics** -- in particular, replica methods and cavity methods -- enable computing **exact asymptotics** for Bayes-optimal inference and for learning dynamics in these models. This means one can, in principle, compute the exact minimum achievable test error and how network dynamics evolve over training, in the limit of large n and d with fixed ratio. References include Barbier et al. [2019], Aubin et al. [2018], and Mignacco et al. [2020].

#### Quadratic Activation Networks

A related class of solvable nonlinear models uses **quadratic activation functions** `σ(z) = z^2` in two-layer networks. Quadratic activations make the network nonlinear in both x and θ, but the polynomial structure enables exact asymptotic analysis.

Recent results have characterized:
- **Exact asymptotics** of test error in the large-n, large-d limit [Erba et al., 2025; Defilippis et al., 2025].
- **Training dynamics** -- how the network evolves during gradient descent [Ben Arous et al., 2025].
- **Scaling laws** -- how test error scales with model and data size in this nonlinear setting [Ren et al., 2025].

These results provide a rare case where nonlinear feature learning is both present and analytically controllable.

#### Teacher-Student Models

A classical framework for studying nonlinear learning dynamics is the **teacher-student model**: a "teacher" network with fixed, random parameters generates the training labels, and a "student" network of the same architecture is trained to match the teacher's outputs.

In certain regimes, the high-dimensional training dynamics of the student can be **reduced to a low-dimensional system of ODEs** for a small set of summary statistics -- order parameters that capture the overlap between student and teacher weight vectors. This reduction makes the dynamics exactly solvable.

The foundational work is Saad and Solla [1995]. More recent analyses include Goldt et al. [2019], Ben Arous et al. [2022], Veiga et al. [2022], and Zavatone-Veth et al. [2025]. The teacher-student framework has been productive precisely because it isolates the difficulty of nonlinear learning (the student must discover the teacher's hidden structure) while providing enough symmetry to make the dynamics tractable.

#### Other Isolated Nonlinear Phenomena

The paper lists a number of other lines of work that isolate and make tractable specific nonlinear phenomena in deep learning:

- **Max-margin solutions (implicit bias of gradient descent on classification).** For homogeneous networks (networks satisfying `f(x; cθ) = c^k f(x; θ)` for some k) trained with logistic loss, gradient descent converges to the maximum-margin classifier in the direction space, even without explicit regularization [Soudry et al., 2018a; Lyu and Li, 2020]. This is a fully nonlinear result about the implicit regularization of gradient descent.

- **Memorization and associative memory.** The capacity of neural networks to memorize specific patterns -- and the dynamics by which they do so -- is studied through exactly solvable associative memory models [Nichani et al., 2025].

- **Modular arithmetic and grokking.** Transformers trained on modular arithmetic tasks (e.g., learning `(a + b) mod p`) exhibit a dramatic learning transition -- rapid generalization after a long period of near-zero generalization. Recent work derives exact solutions for the network's learned algorithmic structure in this setting [Morwani et al., 2023; Gromov, 2023; Kunin et al., 2025].

- **Nonlinear solvable models of attention.** The attention mechanism -- central to transformers -- has been studied in analytically tractable settings [Zhang et al., 2025; Boncoraglio et al., 2025].

- **Improved scaling laws from nonlinear feature learning.** Beyond the NTK scaling law predictions, recent work characterizes how nonlinear feature learning changes the scaling behavior, typically improving sample efficiency [Bordelon et al., 2025].

#### The Collective Picture: Promise and Limitation

The paper is candid about both the promise and the current limitations of the nonlinear solvable models literature:

> "Taken together, these approaches illustrate both the promise and the limitations of current nonlinear toy models: each captures a slice of fully nonlinear learning dynamics, yet no unified framework has emerged."

Each result is a self-contained island of tractability -- a specific mechanism made solvable under specific assumptions. What is missing is a unified theoretical framework that can interpolate between these islands and make predictions for arbitrary architectures, data distributions, and tasks. The paper explicitly designates this as "an open and rapidly evolving area" and returns to it in Section 5 (Open Problems, Open Direction 1).

---

### Limitations of Solvable Settings as a Whole

Solvable settings are powerful but not without systematic blind spots. Drawing together the limitations flagged across the section:

**1. Restricted data assumptions.** Most exact results require either Gaussian inputs (enabling concentration-of-measure arguments) or whitened inputs (decoupling the dynamics). Real data distributions are structured, heavy-tailed, and high-dimensional in ways that break these assumptions. Extending solvable analyses to structured data remains largely open.

**2. Restricted architecture and initialization assumptions.** The exact Saxe et al. [2014] solutions require task-aligned initializations that do not match standard training practice (random Gaussian initialization). Results for arbitrary initializations are much harder.

**3. Absence of feature learning in the linear-parameter setting.** As discussed above, the NTK / linearized framework fundamentally cannot describe the feature learning that is arguably the most important capability of deep networks.

**4. Isolation of nonlinear mechanisms, not synthesis.** The nonlinear solvable models each handle one phenomenon at a time. Real deep learning involves the simultaneous interaction of many mechanisms -- feature learning, implicit regularization, memorization dynamics, attention-based routing -- and no current toy model captures more than a few of these at once.

**5. Finite-size and finite-time effects.** Many asymptotic results (from statistical physics, random matrix theory, etc.) are exact only in the infinite-width or infinite-data limit. Corrections for finite width or finite training time are often non-trivial and can be qualitatively important in practice.

Despite these limitations, the paper's argument is that solvable settings have already proven their scientific value: they have identified phenomena (low-rank bias, double descent, implicit max-margin regularization, grokking) that were subsequently confirmed in realistic settings. The existence of this growing zoo of exactly solvable models -- each capturing something real about deep learning -- is itself evidence that a unified theory is within reach.

---

### Summary of Key References

| Result / Framework | Key References |
|---|---|
| Saddle-point landscapes in deep linear networks | Baldi and Hornik [1989] |
| Phase transitions and timescale separation | Gissin et al. [2019]; Atanasov et al. [2021] |
| Edge-of-stability oscillations | Even et al. [2023] |
| Initialization-dependent inductive biases | Woodworth et al. [2020]; Kunin et al. [2024] |
| Gradient flow analysis of deep linear networks | Fukumizu [1998]; Tarmoun et al. [2021]; Dominé et al. [2025] |
| Sequential singular mode learning (Bernoulli ODE) | Saxe et al. [2014] |
| Low-rank bias and generalization | Lampinen and Ganguli [2018] |
| Simpler-first learning in nonlinear networks | Kalimeris et al. [2019]; Simon et al. [2023b] |
| Small init strengthens low-rank bias | Gidel et al. [2019]; Li et al. [2021a]; Jacot et al. [2021]; Pesme and Flammarion [2023] |
| Depth strengthens low-rank bias | Gunasekar et al. [2018]; Arora et al. [2018, 2019b] |
| Mini-batch noise and low-rank bias | Pesme et al. [2021]; Chen et al. [2024] |
| ℓ_2 regularization and low-rank bias | Ziyin et al. [2022]; Wang and Jacot [2024] |
| Neural Tangent Kernel | Jacot et al. [2018] |
| Infinite-width limit and NTK | Lee et al. [2019]; Chizat et al. [2019]; Liu et al. [2020] |
| Fine-tuning in near-linearized regime | Malladi et al. [2023]; Ren and Sutherland [2025] |
| Generalization error predictions from NTK | Jacot et al. [2020]; Canatar et al. [2021]; Loureiro et al. [2021]; Hastie et al. [2022]; Wei et al. [2022]; Simon et al. [2023a] |
| Inductive bias from architecture via NTK | Arora et al. [2019c]; Geifman et al. [2020] |
| Tendency to learn simple functions | Basri et al. [2020]; Karkada et al. [2025] |
| Double descent | Belkin et al. [2019]; Advani et al. [2020] |
| Scaling laws (kernel / linear setting) | Caponnetto and de Vito [2007]; Pillaud-Vivien et al. [2018]; Cui et al. [2023]; Atanasov et al. [2024] |
| NTK pessimism on sample complexity | Ghorbani et al. [2020]; Vyas et al. [2022] |
| Nonlinear networks outperform kernels (multi-index) | Abbe et al. [2022]; Damian et al. [2022b]; Bietti et al. [2022]; Ba et al. [2022]; Dandi et al. [2023] |
| Stat physics asymptotics for Gaussian models | Barbier et al. [2019]; Aubin et al. [2018]; Mignacco et al. [2020] |
| Quadratic activation networks -- asymptotics | Erba et al. [2025]; Defilippis et al. [2025] |
| Quadratic activation networks -- dynamics | Ben Arous et al. [2025] |
| Quadratic activation networks -- scaling laws | Ren et al. [2025] |
| Max-margin implicit bias | Soudry et al. [2018a]; Lyu and Li [2020] |
| Teacher-student dynamics | Saad and Solla [1995]; Goldt et al. [2019]; Ben Arous et al. [2022]; Veiga et al. [2022]; Zavatone-Veth et al. [2025] |
| Memorization / associative memory | Nichani et al. [2025] |
| Grokking / modular arithmetic | Morwani et al. [2023]; Gromov [2023]; Kunin et al. [2025] |
| Nonlinear attention models | Zhang et al. [2025]; Boncoraglio et al. [2025] |
| Scaling laws from nonlinear feature learning | Bordelon et al. [2025] |
