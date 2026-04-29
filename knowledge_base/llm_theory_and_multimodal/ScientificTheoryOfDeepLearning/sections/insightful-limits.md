> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Insightful Limits

### Overview and Motivation

Modern deep learning systems are staggeringly large. State-of-the-art models regularly involve hundreds of architectural components, hundreds of billions of parameters, and are trained on trillions of tokens. Constructing a detailed microscopic theory that tracks individual parameters in such systems seems essentially hopeless. The sheer number of interacting degrees of freedom rules out any brute-force analytical treatment.

The paper's second line of evidence for an emerging scientific theory of deep learning is the repeated success of **asymptotic (infinite) limits** in taming this complexity. The strategy is to approximate the system as effectively infinite in some dimension, derive exact results in that limit, and then rely on the (empirically and theoretically supported) intuition that those results remain informative for the original finite system.

This is a thoroughly proven strategy in physics and chemistry:

> "complex systems often simplify when approximated as effectively infinite in size, revealing simple mathematical structure that remains informative even for the original finite system. This strategy is well established in statistical and chemical physics: for example, the ideal gas law, PV = nRT, is derived in a limit of infinite number of particles (often termed the thermodynamic limit) yet accurately describes real parcels of gas of finite volume."

The central claim of this section is that **limits are a central mathematical tool for managing the complexity of deep learning, and their recurring success in doing so provides strong evidence for an emerging theory.**

---

### The Infinite Width Limit and the Lazy/Rich Dichotomy

#### Why Width?

The most extensively developed infinite limit in deep learning theory is the **infinite width limit**: sending the number of neurons in every hidden layer to infinity. This limit generally leads to **mean-field behavior**, in which one only needs to describe the evolution of the neuron population as a whole -- for instance, as a probability distribution over neuron states -- rather than tracking each individual neuron.

However, taking this limit non-trivially requires care about initialization. As width grows, activations in deeper layers can diverge unless the initialization scale is shrunk to compensate. The rate of this shrinkage turns out to determine the qualitative character of training dynamics, giving rise to one of two fundamentally distinct behaviors.

#### Initialization Scaling and the Central Issue

The first works to study infinite-width statistics (rather than training dynamics) found that, for inputs to hidden neurons to neither vanish nor explode as width grows, the parameter scale at initialization must decay as [width]^{-1/2} [Neal, 1996; Poole et al., 2016]. This is simply the **LeCun initialization rule** [LeCun et al., 1998], derivable from the central limit theorem -- nothing exotic.

The subtlety appears when one tries to actually train these infinite-width networks with their LeCun-scaled initialization. The result is surprising:

> "the network's weights and hidden representations change only negligibly, yet these small changes accumulate to produce substantial changes in the output function."

In other words, the network's behavior is governed almost entirely by its value at initialization -- the parameters barely move -- yet the output function changes substantially. This is the **lazy** or **kernel** or **linearized regime**.

---

#### The Lazy / Kernel / NTK Regime

In this regime, training dynamics are **linear in the parameters** (in the sense discussed in Section 2.1 of the paper on linear dynamics). The evolution of the target function can be expressed entirely in terms of the **Neural Tangent Kernel (NTK)** [Jacot et al., 2018; Lee et al., 2019].

The NTK is the kernel k(x, x') = nabla_theta f(x) · nabla_theta f(x'), where the gradient is evaluated at initialization and -- crucially in this limit -- stays approximately constant throughout training. Because the kernel is fixed, the function class is fixed: this is equivalent to kernel regression with a particular kernel determined by the architecture and initialization.

The analytical tractability of the NTK regime is remarkable:
- Training dynamics reduce to a linear system, solvable in closed form.
- Generalization can be analyzed using classical kernel learning theory.
- The fixed kernel means exact results are obtainable about convergence, overfitting, and implicit bias.

The fatal limitation, however, is that the NTK regime **fails to exhibit feature learning**:

> "the fact that its hidden representations do evolve only negligibly means that it fails to exhibit feature learning. While the definition of feature learning is much debated (see Open Direction 4), all agree that at minimum it requires the network's hidden activations on a given data sample to change from their values at initialization, which does not happen in this limit."

Networks in this linearized regime were later given the name **"lazy"** by Chizat et al. [2019]. The NTK infinite-width limit, while beautiful, is thus the **wrong limit** for understanding real, performant networks.

---

#### The Rich / Active / Feature-Learning Regime

Several authors identified an alternative infinite-width limit in which training does induce feature learning. The key insight is a different scaling of the output layer:

> "The key insight was essentially to downscale the final-layer weights by a factor of [width]^{-1}, rather than the earlier [width]^{-1/2}, thereby forcing the network weights to change more to compensate."

With this more aggressive suppression of the output, the network function is trivially zero at initialization (in the infinite-width limit), but it **grows by an order-one amount upon each gradient step**, meaning that the weights and hidden representations must change substantially during training. The network is no longer lazy -- it is actively learning features.

This "downscale the output" idea has a lineage:

- **Shallow networks:** Mei et al. [2019], Rotskoff and Vanden-Eijnden [2018], and Chizat and Bach [2018] developed "mean-field networks" in the shallow case.
- **Arbitrary depth:** Geiger et al. [2020] and Yang and Hu [2021] showed the same idea works for networks of arbitrary depth, bundling the resulting hyperparameter scaling factors into what is now known as the **Maximal Update Parameterization (muP)** (discussed more extensively in Section 2.4 of the paper).

It is now widely accepted that infinite-width neural networks can learn features when appropriately parameterized.

---

#### What Rich Networks Actually Do

Wide networks in the rich regime display qualitatively distinct behaviors compared to their lazy counterparts. These are not minor quantitative differences -- they are differences in kind.

**Feature adaptation:** The hidden representations of rich networks change over the course of training, adapting to the structure of the input data and altering the internal geometry of representations [Bordelon and Pehlevan, 2022].

**Neuron specialization:** Subpopulations of neurons specialize, learning to attend to different latent features in the data [Aubin et al., 2018; Goldt et al., 2019; Ren et al., 2025].

**Low-dimensional structure discovery:** When the optimal predictions involve low-dimensional subspaces of high-dimensional data, the distribution over first-layer weights evolves to amplify directions in the relevant subspace [Mei et al., 2018; Abbe et al., 2022; Moniri et al., 2023; Cui et al., 2024; Defilippis et al., 2025; Erba et al., 2025; Montanari and Wang, 2026].

**Greedy low-rank bias:** When the initialization scale is made even smaller than the rich regime, networks often exhibit the greedy low-rank bias discussed in Section 2.1 of the paper, acquiring some components of the task before others [Saxe, 2015; Atanasov et al., 2021, 2025].

---

#### The Lazy--Rich Dichotomy as a Structural Finding

The lazy--rich dichotomy, and its dependence on initialization scale, is described as a **central finding** of infinite-width analyses. Importantly, it generalizes beyond the infinite-width limit:

> "Subsequent work has shown that analogous behavior appears even at finite width: scaling down the network output promotes feature learning, pushing models toward the rich regime, whereas increasing the output scale tends to linearize training dynamics and induce lazy behavior [Chizat et al., 2019]."

This sensitivity to initialization scale connects to a broader literature on inductive bias, where "seemingly small changes to the learning setup can steer training toward fundamentally different solution classes" [Maennel et al., 2018; Woodworth et al., 2020].

The physical analogy offered by the paper is instructive: the lazy vs. rich dichotomy is conceptually similar to **elastic vs. plastic deformation in materials**. A material deforms linearly (elastically) in response to a small force, with its internal atomic structure unchanged. Under a larger force it deforms nonlinearly (plastically), and its internal structure changes permanently.

---

#### Parameterization Taxonomy: NTP vs. NTK vs. muP

Understanding the lazy--rich dichotomy requires distinguishing several parameterizations:

- **NTP (naive/standard parameterization):** The default parameterization that naive application of LeCun initialization gives. Parameters are initialized at scale [width]^{-1/2} at every layer. Training in the infinite-width limit with NTP produces the **NTK / lazy regime**.

- **NTK parameterization:** Sometimes distinct from NTP, this refers explicitly to the parameterization studied in Jacot et al. [2018] and related work, in which the kernel K(x, x') remains constant during training, giving rise to kernel gradient descent.

- **muP (Maximal Update Parameterization):** The parameterization identified by Yang and Hu [2021] that suppresses the output (or, equivalently, scales learning rates by layer-dependent factors) so that every layer makes an O(1) update per gradient step in the infinite-width limit. muP is the parameterization that **preserves feature learning** at infinite width. Crucially, muP also enables **hyperparameter transfer**: learning rates and other optimizer settings found optimal at small width transfer to large width, a practical consequence of theoretical importance (discussed further in Section 2.4).

- **Mean-field parameterization:** The parameterization used in the shallow mean-field network literature (Mei et al., Chizat and Bach, Rotskoff and Vanden-Eijnden), conceptually aligned with muP for shallow networks.

---

#### The Bayesian Perspective (Footnote)

The paper notes a parallel line of work studying feature learning from a Bayesian perspective. Naively, infinite-width networks have simple Bayesian statistics given by **Gaussian processes** [Lee et al., 2017] -- analogous to the lazy limit for conventionally trained networks. This Gaussian process limit serves as a solvable reference point [Cohen et al., 2021b; Lavie et al., 2024]. Researchers then reintroduce finite width, using mean-field and variational techniques to characterize feature adaptation to data [Cohen et al., 2021b; Seroussi et al., 2023; Rubin et al., 2023, 2025a, 2025b]. One may also induce feature learning in this Bayesian setting by rescaling the total likelihood [Yang et al., 2023a], which is analogous to the final-layer downscaling that gives the rich limit in conventional training.

---

### The Infinite Depth Limit

#### Taking Depth to Infinity

By analogy with width, one can also ask what happens as the **depth** of a network goes to infinity. The natural setting for this is **residual networks** (ResNets), where each layer adds a "residual" contribution to the forward pass:

x_{l+1} = x_l + alpha_l * F_l(x_l)

For the residual stream to remain well-behaved as depth grows, each layer's contribution must be suppressed by a factor that shrinks with depth. As with width, the precise rate of suppression determines the qualitative character of the resulting dynamics, and again two qualitatively distinct limits emerge.

#### Smooth-Flow Limit: Suppression by [depth]^{-1}

Suppressing each layer by a factor of [depth]^{-1} results in limiting dynamics in which the residual stream **changes smoothly over depth** [Bordelon et al., 2024b; Chizat, 2025; Chaintron et al., 2026]. This is reminiscent of **Neural ODEs** [Chen et al., 2018]: as depth goes to infinity, the discrete residual updates become infinitesimally small, and the forward pass converges to the solution of an ordinary differential equation in the depth variable. The dynamics are smooth and continuous.

#### Diffusive Limit: Suppression by [depth]^{-1/2}

Suppressing each layer by a factor of [depth]^{-1/2} results in a different limit in which the residual stream **diffuses as if driven by a stochastic differential equation** [Bordelon et al., 2023; Yang et al., 2023b]. This is more like a Brownian motion or random walk in depth -- the increments are larger (relative to total depth) than in the smooth case, and the cumulative effect resembles diffusion rather than smooth flow.

These two limits are not just mathematically different -- they lead to **qualitatively different solutions** in realistic architectures such as transformers [Dey et al., 2025]. Which limit is more important for understanding practical deep networks remains an open question:

> "It is not yet clear which is the more important limit to study."

---

### Other Limits: Recurrent Architectures and Transformers

#### Recurrent Architectures

Not all architectures are naturally analyzed in terms of width or depth as distinct orthogonal dimensions. Recurrent architectures (RNNs, SSMs, etc.) repeat the same transformation over time steps. Their infinite limits can be analyzed using similar mean-field ideas, but the relevant limit involves the number of recurrent steps or the hidden state dimension [Clark et al., 2026; Bauer et al., 2026].

#### Transformer-Specific Limits

State-of-the-art transformer models have **multiple internal scaling dimensions** that each admit their own infinite limit. These include:

**Multi-head self-attention layers:**
- Number of attention heads
- Head size (dimension per head)
- Context length (sequence length)

Limits along these axes have been studied by Hron et al. [2020] and Bordelon et al. [2024b].

**Mixture-of-expert (MoE) MLPs:**
- Expert count
- Expert size (parameters per expert)
- Sparsity (fraction of experts activated per token)

These limits have been studied by Malasnicki et al. [2025] and Jiang et al. [2026].

The interplay among these multiple limits is not fully understood. Clarifying this interplay is important both for making theoretical contact with modern practice and for disentangling initialization and optimization hyperparameters in large models (see Section 2.4 of the paper).

#### Optimization Hyperparameter Limits

Most optimization hyperparameters have a natural associated limit:

- **Batch size -> infinity:** Recovers **population gradient descent** (full-batch gradient descent on the true data distribution), eliminating stochastic noise.
- **Learning rate -> 0:** Recovers **gradient flow** (continuous-time gradient descent), eliminating discretization artifacts of gradient steps.
- **Weight decay -> 0, training time -> infinity:** First optimizes the loss to convergence, then performs **parameter norm minimization** conditioned on the final loss value -- a double limit that recovers a specific implicit regularization bias.

The paper notes that understanding the finite corrections induced by deviating from these limits (finite batch size, finite learning rate, finite training) is addressed in Section 2.4 on the discretization hypothesis.

---

### Joint Scaling Limits

#### When Limits Commute

Sometimes two scaling limits can be taken in either order and give the same result -- the limits **commute**. For example, the infinite width and infinite depth limits in residual networks commute, as long as a sensible parameterization is used [Hayou and Yang, 2023].

When limits commute, life is simple: one can take them in whatever order is most convenient, and the result is unambiguous.

#### When Limits Do Not Commute

In many theoretical machine learning settings, different scaling dimensions **do not commute**, and the limiting behavior depends on the **ratio** of the two variables. This gives rise to **joint** or **proportional scaling limits**, where one takes both variables to infinity but holds their ratio fixed.

Joint limits are common in random matrix theory. A canonical example: the singular value distribution of a random matrix with P rows and N columns depends, in the large-N, large-P limit, on the ratio P/N, not on P and N individually (the Marchenko--Pastur law). The relevant limit is N, P -> infinity with P/N = c held constant.

#### Machine Learning Joint Limits

The paper identifies several important joint scaling limits in machine learning:

**Data--model joint limits:** Neural networks trained with random data can often be described by a joint limit where both **dataset size** and **parameter count** go to infinity, but one or more of the ratios

[data] / [input dim], [data] / [width], [data] / [parameters]

is held at a finite value [Seung et al., 1992; Saad and Solla, 1995; Zdeborova and Krzakala, 2016; Li and Sompolinsky, 2021; Maillard et al., 2024; Martin et al., 2024; Barbier et al., 2025].

> "This joint scaling is likely necessary in the study of compute-optimal neural scaling laws where the training horizon (i.e. dataset size) is scaled linearly with the total parameters [Hoffmann et al., 2022] and to theoretically characterize hyperparameter transfer phenomena [Bordelon and Pehlevan, 2025]."

The reason joint data--model limits matter specifically for scaling laws is that:

> "infinite parameter limits at fixed dataset size are capable of perfect interpolation and do not capture scaling law behaviors across model sizes (see Section 2.3)."

A model with infinite parameters can always interpolate any fixed finite dataset, so any interesting scaling behavior (power-law decrease in loss with model size) only appears when the dataset also grows.

**Width--depth joint limit:** In non-residual networks, the ratio [width] / [depth] can be a relevant joint scaling variable [Hanin and Nica, 2019; Li et al., 2022; Noci et al., 2023; Hanin and Jiang, 2025].

**Learning rate--output multiplier joint limit:** In the rich regime, the ratio [learning rate] / [output multiplier] is a relevant joint scaling variable that controls the balance between feature learning and lazy behavior [Atanasov et al., 2025].

**SGD noise temperature:** The ratio [learning rate] / [batch size] controls the effective temperature of stochastic gradient descent noise, often called the **SGD noise temperature** [Mandt et al., 2017; Jastrzebski et al., 2017]. This ratio determines how much stochastic gradient noise the system experiences and therefore how much implicit regularization SGD provides relative to full-batch gradient descent.

---

### The Discretization Hypothesis

#### The Core Idea

Having catalogued the many insightful limits available in deep learning theory, the paper synthesizes them under a single conceptual framework:

> "the widespread use of limits to manage the complexity of deep learning reflects a recurring theme across scientific disciplines: appropriate asymptotic perspectives often render otherwise intractable systems analytically tractable."

The key heuristic belief that underpins this entire program is stated explicitly:

> "Many theorists share a heuristic belief that most practical neural networks can be understood as noisy, finite approximations to models of infinite size."

This is formalized as the **Discretization Hypothesis**.

#### The Physical Analogy

The analogy is to numerical solution of partial differential equations:

> "By analogy, one numerically solves a partial differential equation by discretizing over space and time, and the finer the discretization, the smaller the numerical error from the desired continuum process. This is very possibly also true of deep neural networks, with width and depth taking the place of space and time."

Just as a coarser grid introduces numerical error relative to the true continuum PDE solution, a narrower or shallower network introduces "discretization error" relative to the infinite-width, infinite-depth ideal. And just as increasing the grid resolution reduces numerical error at the cost of more computation, increasing network width or depth reduces these finite-size deviations at the cost of more parameters and compute.

Crucially, the analogy extends beyond just width and depth:

> "Other finite hyperparameters, such as the learning rate, batch size, and dataset size, might also be understood in this way."

- Finite **learning rate** is a discretization of continuous-time gradient flow.
- Finite **batch size** is a discretization of full population gradient descent.
- Finite **dataset size** is a discretization of the full data distribution.

#### What the Hypothesis Claims

The Discretization Hypothesis has a precise empirical content:

> "The Discretization Hypothesis amounts to the statement that finite-size corrections from limits typically worsen performance while saving costs in data, time, memory, and compute."

In other words: being finite (in width, depth, dataset size, etc.) generally hurts performance, but it is a necessary concession to cost. If you had infinite compute, you'd use infinite-width, infinite-depth models trained on infinite data with infinitesimally small learning rates and infinite batch sizes -- and they'd perform better.

#### The Falsification Criterion

The paper provides an explicit way to falsify the hypothesis:

> "Showing that these finite-size effects deliver a general benefit that cannot be achieved any other way would falsify this hypothesis."

That is, if it were demonstrated that finite width, finite depth, or finite learning rate provides a **systematic advantage** -- not just a cost--performance tradeoff, but a genuine inductive bias benefit that cannot be replicated by any infinite-limit model -- then the Discretization Hypothesis would be false.

This would be a surprising finding. The hypothesis is consistent with the practical observation that, given fixed compute, practitioners prefer larger models to smaller ones -- suggesting that finite-size effects are indeed primarily costs, not benefits.

#### Status: Implicit but Unproven

Despite its foundational role, the Discretization Hypothesis has not been formally proven:

> "While it has yet to be made precise or proven (see Open Direction 5), this hypothesis has implicitly underpinned much important work, and little in the analytical study of large models makes sense without it."

This is an important epistemic claim. The entire infinite-limits research program rests on this hypothesis -- without it, there would be no reason to expect that results derived in the infinite limit are relevant to practical finite networks. The fact that infinite-limit results do match finite-network behavior in practice is strong empirical support, but a rigorous theoretical grounding remains an open problem.

---

### Summary and Connections

The insightful limits line of evidence assembles the following picture:

1. **Infinite width** reveals a fundamental dichotomy between lazy (kernel/NTK) and rich (feature-learning/muP) regimes, determined by how aggressively the output is suppressed relative to the initialization. This dichotomy is a genuine, qualitative structural finding -- not merely a quantitative difference.

2. **Infinite depth** in residual networks similarly yields two qualitatively distinct limits (smooth ODE-like flow vs. diffusive SDE-like dynamics), with the right limit for practical architectures still under investigation.

3. **Architecture-specific limits** (attention heads, context length, expert count, recurrent steps) each provide their own simplifying infinite limit, and their interplay is a frontier area.

4. **Optimization hyperparameter limits** (infinite batch size, zero learning rate, infinite training time) each recover idealized processes whose finite corrections can be analyzed perturbatively.

5. **Joint scaling limits** -- taking multiple variables to infinity simultaneously with fixed ratios -- are necessary for describing scaling laws and hyperparameter transfer phenomena. The SGD noise temperature, width/depth ratio, and data/parameter ratio are examples.

6. **The Discretization Hypothesis** synthesizes all of the above: practical finite networks are noisy approximations to infinite-limit ideals. Finite hyperparameters introduce "discretization errors" analogous to those in numerical PDE solvers. This hypothesis is implicit in nearly all theoretical work on large models, and making it precise and proving it (or finding counterexamples) is a major open problem.

These limits are not merely mathematical conveniences -- the paper argues they reveal genuine structure in deep learning that persists at finite scale. Their recurring success, across so many different architectures, hyperparameters, and training settings, constitutes strong evidence that a coherent scientific theory of deep learning is possible.
