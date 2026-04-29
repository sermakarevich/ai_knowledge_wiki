> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Simple Empirical Laws

### Overview

Section 2.3 of Simon et al. (2026) presents the third line of evidence for a coming scientific theory of deep learning: the existence of simple empirical laws that govern macroscopic, aggregate statistics of neural networks. This is the "top-down" complement to the bottom-up first-principles work described in earlier sections. Rather than deriving behavior from mathematical assumptions, top-down theorizing begins by noticing that certain measurable quantities obey strikingly clean relationships -- and then asks why.

The section identifies a handful of such laws, spanning test loss (neural scaling laws), weight dynamics (edge of stability), and the internal geometry of representations and weights (neural collapse, the neural feature ansatz, and gradient flow conservation laws). Each law is reproducible across architectures and datasets, which the authors take as strong evidence that a simple underlying mechanism is responsible -- and therefore that a theoretical explanation is tractable.

---

### The General Idea: Macroscopic Statistics and Their Laws

Deep learning systems are highly measurable. During and after training, one can track an enormous range of quantities: individual weight values, activations for specific inputs, gradient norms, loss on every batch, Hessian eigenvalues, representation geometry, and more. The measurement problem is not access -- it is selection. Which of the countless measurable quantities are the lawful ones?

The paper's answer is that the most lawful quantities tend to be **aggregate, macroscopic statistics** -- quantities that summarize many weights or many samples simultaneously. The train loss and test loss are canonical examples: each is an average over many data points, and this averaging is precisely what enables regularity to emerge.

> "While any quantity can be measured, the most lawful are typically aggregate, macroscopic statistics over many weights and samples."

This observation has an important methodological implication. The loss landscape at the level of individual weights is famously complicated -- visualizations such as those in Li et al. (2018) reveal a high-dimensional surface with seemingly chaotic structure. Yet when you zoom out and track the sharpness (a scalar summary of the Hessian) or the total test loss (a scalar summary of performance across thousands of examples), clean patterns emerge. Macroscopic aggregation filters noise.

#### The Kepler Analogy

The authors situate this pattern within the broader history of science:

> "This pattern has ample precedent in the quantitative sciences. Many important physical and chemical laws were first discovered as empirical regularities and only later understood in terms of deeper principles, including laws due to Kepler, Snell, Boyle, Hooke, Faraday, Ohm, Poiseuille, and Planck."

Kepler's laws of planetary motion are the paradigm case. Kepler did not derive his three laws from Newtonian mechanics -- Newton had not yet formulated it. Instead, Kepler fit the observational data of Tycho Brahe and found that orbits are ellipses, that a line from the planet to the sun sweeps equal areas in equal times, and that the square of the orbital period is proportional to the cube of the semi-major axis. These were purely empirical regularities. Newton's theory of gravitation then explained all three as consequences of a single inverse-square force law.

The analogy to deep learning is precise: we are at the Kepler stage. We have discovered that certain macroscopic statistics of neural networks obey clean power laws, threshold conditions, and geometric constraints. We do not yet have the "Newton" -- the unified underlying theory that explains them all from first principles. The authors argue that the existence of such clean empirical laws is itself evidence that such a theory exists and is findable.

#### Why Empirical Laws Matter for Theory-Building

Empirical laws serve two purposes in a maturing science. First, they are **predictive tools** even before they are explained. A practitioner who knows the neural scaling laws can extrapolate model performance to larger compute budgets without running the experiment. A practitioner who knows about the edge of stability can anticipate instability when setting a learning rate. Second, empirical laws are **targets for theoretical explanation** -- they constrain what any complete theory must account for, and the simplicity of the law hints at the simplicity of its cause.

The authors note:

> "The fact that test loss is so predictable strongly suggests that a simple underlying explanation remains to be found."

And they conclude the section with an explicit methodological recommendation:

> "We encourage theorists of deep learning to proactively use experiments to look for lawful regularities in neural networks."

This is a call for what the authors term top-down theorizing -- a strategy that has been enormously productive throughout physics and chemistry, and which the field of deep learning is only beginning to pursue systematically.

---

### Neural Scaling Laws

#### The Basic Finding

The single most important scalar measurement of any machine learning system is its test loss -- the average error on unseen data. Given the enormous complexity of large language models and other large-scale systems, it might seem that test loss would be an intractable function of the many hyperparameters, architectural choices, and training decisions involved. The neural scaling laws say otherwise.

Studies by Kaplan et al. (2020) and Hestness et al. (2017) established that, within a fixed architectural family, the final test loss follows a **power law** in each of three scalar variables: compute, dataset size, and parameter count. Specifically:

> "studies of neural scaling laws [Kaplan et al., 2020, Hestness et al., 2017] demonstrate that, within an architectural family, the final loss follows a predictable power law function governed by only three scalar variables: compute, the amount of data, and the network's size."

When plotted on log-log axes, the relationship between test loss and each of these variables is approximately linear -- the hallmark of a power law. This is shown in Figure 3 of the paper, which reproduces the Kaplan et al. results: three separate log-log plots, one for dataset size in tokens, one for parameters (non-embedding), and one for compute in PF-days (non-embedding). In each case the loss decays along a straight line on the log-log plot.

The structural form of the scaling law is:

```
L ~ C^(-alpha_C)   (as a function of compute C)
L ~ D^(-alpha_D)   (as a function of dataset size D)
L ~ N^(-alpha_N)   (as a function of parameter count N)
```

where `alpha_C`, `alpha_D`, and `alpha_N` are empirically measured exponents. These exponents are not small -- they indicate that a tenfold increase in compute, data, or parameters each produce a meaningful, predictable reduction in loss. The precise values of the exponents depend on the architectural family and the dataset domain, but the power-law form is remarkably consistent.

#### What Has and Has Not Been Explained

The existence of power-law scaling is striking enough. The deeper question -- why do these specific functional forms and these specific exponents arise -- remains largely open.

Several candidate frameworks have been proposed:

- **Data manifold dimensionality** -- Sharma and Kaplan (2022) and Bahri et al. (2024) suggest that if the true data distribution lies on a low-dimensional manifold, the decay rate of the loss as a function of model size or data should be set by the intrinsic dimensionality of that manifold.
- **Feature superposition** -- Liu et al. (2025) propose that the way features are superposed in neural network representations may account for the observed scaling behavior.
- **Power laws in task structure** -- Cui et al. (2021), Bordelon et al. (2024a), Michaud et al. (2023), Ren et al. (2025), and Defilippis et al. (2025) explore how power-law structure latent in the task or data-generating process propagates into the scaling law exponents.
- **Architecture and optimizer dependence** -- Barkeshli et al. (2026) argue that the exponents may depend not only on data structure but also on details of the architecture and optimizer, complicating any purely data-driven explanation.

Despite this activity, the authors are candid about the state of the art:

> "At present, no framework can robustly predict the observed exponents a priori from dataset and architectural properties across realistic settings (see Open Direction 7), though recent progress has begun to move in this direction [Cagnetta et al., 2026]."

This admission is itself theoretically informative. The power-law form is robust; the exponents are not yet derived from first principles in realistic settings. This gap -- between the observed regularity and its theoretical grounding -- is exactly the kind of gap that historical precedent suggests will eventually be closed by a deeper theory.

#### Why the Scaling Laws Are Important

Beyond their practical utility for extrapolation, the scaling laws carry a theoretical message: the test loss is not a chaotic function of training decisions, but rather a smooth, low-dimensional function of a handful of aggregate variables. This "effective low-dimensionality" of the loss surface -- at the macroscopic level -- is itself a non-trivial fact about deep learning that any theory must explain.

The Hestness et al. (2017) results, predating the LLM era, showed that this power-law behavior was not an artifact of transformer architectures or language modeling. It appears across domains and architectural families, which strengthens the case that it reflects a deep property of the learning process rather than a domain-specific accident.

---

### Weight Dynamics at the Edge of Stability

#### Motivation: The Loss Landscape Is Complicated, But Aggregates Are Not

Understanding the trajectory of network weights during training is fundamental to understanding why networks converge to good solutions. In simple, analytically tractable cases (see Section 2.1 of the paper), the weight dynamics can be solved exactly. In realistic, large-scale settings, exact solutions are out of reach. The loss landscape itself -- as visualized by Li et al. (2018) -- appears immensely complicated, with no obvious global structure.

Yet certain coarse, aggregate properties of the weight trajectory do obey simple laws. The most prominent of these is the behavior of the **sharpness** -- defined as the largest eigenvalue of the Hessian of the training loss with respect to the parameters.

> "While there are simple cases where these dynamics are exactly solvable (see Section 2.1), this is usually well out of reach. The loss landscape dictates the network's dynamics, but a direct visualization of the loss, as is done in Li et al. [2018], suggests an immensely complicated landscape that is unlikely to have lawful regularities. Nonetheless, some robust patterns in the coarse, aggregate properties of weight trajectories have been found."

#### Progressive Sharpening and the 2/η Threshold

When a neural network is trained using full-batch gradient descent with learning rate `η`, the sharpness undergoes two distinct, reproducible phases:

1. **Progressive sharpening** -- the sharpness increases gradually over the course of training, even as the training loss decreases.
2. **Edge of stability** -- the sharpness eventually plateaus near the value `2/η`, where it remains for the rest of training.

This two-phase pattern was documented systematically by Cohen et al. (2021a) across multiple architectures and learning rates. Figure 4 of the paper shows the effect for three architectures (a fully-connected network, VGG, and ResNet) trained on CIFAR-10, each with multiple learning rates. In every case, the sharpness rises and then hovers at or just above the dashed horizontal line marking `2/η`.

The threshold `2/η` is not arbitrary. In convex optimization, `2/η` is the maximum sharpness compatible with stability of gradient descent:

> "2/η is the maximum stable sharpness achieved in convex optimization -- any sharpness larger than 2/η would cause parameter oscillations of increasing magnitude."

This gives the edge of stability its name. The sharpness rises until it reaches the boundary of the stability region, then is held there by a dynamical balance between the loss-minimizing descent direction and the destabilizing effect of large curvature.

#### Third-Order Curvature and the Mechanism of Stabilization

Understanding why the sharpness stabilizes near `2/η` -- rather than simply exceeding it and diverging -- requires going beyond second-order analysis. Damian et al. (2022a) identified the mechanism: coarse properties of the **third-order loss curvature** cause the second-order sharpness to self-regulate at the stability boundary.

> "Damian et al. [2022a] showed how coarse properties of the third-order loss curvature can cause the (second-order) sharpness to stabilize at 2/η."

Intuitively, when the sharpness exceeds `2/η`, gradient descent steps cause oscillations in the direction of the sharpest curvature. These oscillations interact with the third-order structure of the loss surface in a way that reduces the sharpness -- restoring stability. The result is a self-regulating feedback loop that keeps the sharpness hovering near the threshold.

#### Decomposition of Dynamics at the Edge of Stability

Subsequent work by Cohen et al. (2025) further refined this picture. The loss dynamics at the edge of stability can be decomposed into two components:

1. **Smooth, time-averaged gradient flow** -- a slow, steady descent that follows the gradient flow in a time-averaged sense.
2. **Oscillations in unstable directions** -- rapid oscillations in the directions corresponding to eigenvalues of the Hessian near or above `2/η`.

> "Follow-up work reveals that loss dynamics at the edge of stability can be decomposed as smooth, time-averaged, gradient flow dynamics plus oscillations in unstable directions [Cohen et al., 2025]. These works make quantitative predictions about the parameter trajectory which closely match experiment."

The fact that these quantitative predictions match experiment is notable: this is not merely a qualitative story but a framework that makes falsifiable, quantitative claims about the weight trajectory. It represents a partial success of top-down theorizing -- an empirical law (progressive sharpening followed by stabilization at `2/η`) has been given a mechanistic explanation in terms of third-order curvature, and that explanation makes quantitative predictions.

#### What Remains Open

The theoretical picture is incomplete in one important direction. Progressive sharpening -- the first phase -- has been proven to occur in **deep linear networks** (Even et al., 2023; Yoo et al., 2025), but:

> "a quantitative explanation suitable to realistic nonlinear networks remains to be found (see Open Direction 8)."

The linear-network proof provides structural intuition, but deep learning practitioners do not train linear networks. Extending the progressive sharpening result to realistic nonlinear architectures -- transformers, ResNets, CNNs -- remains an open problem flagged by the authors as a priority direction.

---

### Coarse Properties of Hidden Representations and Weights

Beyond the test loss and the sharpness, there are several empirical laws governing the internal geometry of trained networks -- how the hidden representations of different classes are arranged, how the first-layer weights are structured, and what quantities are conserved throughout training. The paper briefly describes three such laws.

---

#### Neural Collapse (Papyan et al., 2020)

**The observation.** Consider a neural network classifier trained to distinguish among `C` classes. Papyan et al. (2020) observed a striking geometric phenomenon in the final hidden layer:

> "Papyan et al. [2020] found that, at the end of training, the final-hidden-layer representations of samples from each class tend to cluster tightly around their class mean. Furthermore, the C class mean vectors form a regular simplex."

In other words, if you take all the final-layer representations of, say, all cat images in the training set, they cluster together -- their mean is a representative vector, and the within-class spread is small. More remarkably, the `C` class means (one per class) arrange themselves in a maximally symmetric geometric configuration: a **regular simplex** in representation space.

For `C` classes, a regular simplex is the unique configuration of `C` points that are mutually equidistant and have equal angle to a common center. For two classes it is a line segment (the two endpoints are equidistant from the midpoint); for three classes it is an equilateral triangle; for four classes it is a regular tetrahedron; and so on. This configuration maximizes the angular separation between class means, making it the natural geometry for a classifier that wants to be maximally discriminative.

**Why it matters.** Neural collapse is remarkable for several reasons. It is architecture-agnostic -- it has been observed across fully-connected networks, convolutional networks, and other architectures. It occurs at the end of training, after the network has been trained to convergence, not during early or intermediate training. And it is a structural claim about the geometry of representations, not just a scalar statistic.

**The theoretical explanation.** Later theoretical work (Zhu et al., 2021) explained neural collapse as the energy-minimizing configuration under two conditions:

> "Later theoretical work has explained this geometric arrangement as the natural energy-minimizing configuration when (a) the loss used is cross-entropy and (b) a small amount of weight decay is applied [Zhu et al., 2021]."

This is a clean example of an empirical law receiving a theoretical explanation that reduces it to more basic principles (the loss function and the regularizer). The explanation identifies the two ingredients that produce the simplex structure and predicts that it should break down when those ingredients are absent -- a testable, falsifiable prediction.

Neural collapse is also conceptually interesting because it suggests that the final-layer representation geometry is not arbitrary -- it is strongly constrained by the optimization objective. A theory of deep learning representations must account for this constraint.

---

#### The Neural Feature Ansatz (Radhakrishnan et al., 2024)

**The observation.** At the other end of the network, there are regularities in the **first-layer weights**. Radhakrishnan et al. (2024) identified a relationship between the first-layer weight matrix `W_1` and the network's input-output Jacobian. Specifically, they found that after training, the Gram matrix of the first-layer weights aligns with the average gradient outer product:

$$W_1^\top W_1 \propto \mathbb{E}_{x \sim P_{\text{data}}} \left[ \nabla_x f(x; \theta) \nabla_x f(x; \theta)^\top \right]$$

where `nabla_x f(x; theta)` is the Jacobian of the network output with respect to the input `x`.

The paper states this as equation (3):

> "Radhakrishnan et al. [2024] show that, after training, the Gram matrix of the first-layer weights W_1^T W_1 aligns with the average gradient outer product."

**What this means.** The Gram matrix `W_1^T W_1` captures the "directions" that the first layer is sensitive to -- its top eigenvectors are the input directions that the first layer responds to most strongly. The average gradient outer product `E[nabla_x f nabla_x f^T]` captures the input directions that matter most for changing the network output. The ansatz says that these two quantities align: the first layer learns to be sensitive to precisely the input directions that the network's overall input-output mapping depends on.

This is an elegant statement about what the first layer learns -- it learns to extract the features that are most relevant to the network's behavior, as measured by the gradient of the output with respect to the input.

**Scope and theoretical status.** The authors are careful about the scope of this result:

> "While this rule is heuristic and inexact, it often makes strikingly accurate predictions for quantities like the top eigenvectors of W_1^T W_1."

It is a heuristic, not a theorem. But it is a productive heuristic -- it predicts the leading eigenvectors of the first-layer Gram matrix, which correspond to the most important input directions the first layer represents. Similar heuristics hold at deeper layers, suggesting that a principle of "feature alignment with task-relevant gradients" may be a general property of trained networks.

Theoretical explanations for the neural feature ansatz are partial at the time of writing, with contributions from Ziyin et al. (2024) and Boix-Adsera et al. (2025). Like progressive sharpening for nonlinear networks, this remains an area where the empirical observation is ahead of the theory.

---

#### Gradient Flow Conservation Laws (Kunin et al., 2021)

**The linear network discovery.** The third structural regularity concerns quantities that are **conserved** throughout training under gradient flow -- quantities that do not change as the weights evolve, regardless of how the loss changes.

The discovery originated in the analysis of linear networks (Saxe et al., 2014; Du et al., 2018; Arora et al., 2019a), where it was observed that a specific quantity remains constant under gradient flow. For consecutive linear layers with weight matrices `W_l` and `W_{l+1}`, the difference between the covariance matrix and the Gram matrix of consecutive layers is conserved:

$$W_l W_l^\top - W_{l+1}^\top W_{l+1}$$

is constant under gradient flow throughout training. This means that no matter how the weights change, the difference between these two matrix quantities remains fixed at its initial value.

> "the difference between the covariance and Gram matrices of consecutive layers W_l W_l^T - W_{l+1}^T W_{l+1} is conserved under gradient flow [Saxe et al., 2014, Du et al., 2018, Arora et al., 2019a]."

**The Noether connection.** Initially this appeared to be a curiosity specific to linear networks. The key insight came when Kunin et al. (2021) and Tanaka and Kunin (2021) recognized that this conserved quantity arises from a **continuous symmetry of the parameterization** -- an instance of Noether's theorem from classical mechanics.

> "What initially appeared to be a curiosity of linear networks was later shown to follow from continuous symmetries of the parameterization -- an instance of the Noether principle -- and thus could be used to identify similar conserved quantities in nonlinear networks [Kunin et al., 2021, Tanaka and Kunin, 2021, Marcotte et al., 2024a,b]."

Noether's theorem states that every continuous symmetry of the action of a physical system corresponds to a conserved quantity. In deep learning, the "action" is replaced by the gradient flow dynamics, and the symmetries are symmetries of the parameterization -- transformations of the weights that leave the network's input-output function unchanged.

**A taxonomy of symmetries and their conserved quantities.** Once the Noether connection was made, a systematic taxonomy became possible. The paper lists several concrete examples of symmetries in standard architectures and their corresponding conserved quantities:

- **Rescaling symmetries in networks with homogeneous nonlinearities** (e.g., ReLU networks) -- if you scale up the weights of one layer and scale down the weights of the next, the function computed by the network is unchanged. This rescaling symmetry gives rise to conservation laws about the relative norms of consecutive layers' weight matrices.
- **Scale symmetries preceding normalization layers** (e.g., batch normalization) -- the network function is invariant to rescaling the weights before a batch normalization layer, since the normalization layer removes that scale. This gives rise to conservation laws involving those weights.
- **Translation symmetries in the logits preceding a softmax** -- adding a constant to all logits before a softmax leaves the output probabilities unchanged. This yields a conservation law on the sum of the logit weights.
- **Rotation symmetries between key and query matrices in attention** -- in the attention mechanism `softmax(QK^T / sqrt(d)) V`, there is a rotation symmetry between the key and query projections. This produces conservation laws involving those matrices.

**Behavior under SGD.** The conservation laws hold exactly under **gradient flow** (continuous-time gradient descent). Under **stochastic gradient descent** (SGD), the symmetries are broken by the stochasticity of mini-batch sampling, but in a predictable, controlled way:

> "symmetry-specific statistics of the parameters that are conserved under gradient flow and weakly broken by SGD in predictable ways."

This "weakly broken" behavior means that even under SGD, these quantities do not drift arbitrarily -- they remain close to their initial values, with deviations that are predictable from the SGD noise structure. This is a quantitative prediction that can be tested experimentally, and the framework of Kunin et al. (2021) provides the tools to make and test such predictions.

**Why this matters.** The conservation laws identify hidden structure in the weight trajectory that is invisible when you look at individual weights. They also constrain the space of solutions that gradient descent can reach: a network initialized at a particular point in weight space can only reach points where the conserved quantities match their initial values. This constrains the implicit bias of gradient descent and connects the conservation laws to questions about generalization.

The Noether principle approach is particularly powerful because it is systematic -- once you identify the symmetries of your architecture, you automatically know what is conserved. This makes it a general tool for analyzing new architectures, not just the specific examples studied so far.

---

### What Ties These Laws Together

The five empirical laws described in this section -- neural scaling laws, the edge of stability, neural collapse, the neural feature ansatz, and gradient flow conservation laws -- are superficially unrelated. They concern different quantities (test loss, Hessian sharpness, final-layer geometry, first-layer weights, and conserved quantities under gradient flow), different aspects of the network (external behavior, training dynamics, internal representations), and different points in the training process (end of training, during training, and continuously throughout training).

What ties them together is a set of structural features they share:

**1. They are aggregate, macroscopic statistics.**
Each law concerns a quantity that summarizes many weights or many samples. The test loss averages over many data points. The sharpness is the largest eigenvalue of the Hessian -- a global summary of the loss curvature. Neural collapse is a statement about the mean representation of each class across all training examples. The neural feature ansatz is a statement about the Gram matrix of the first-layer weights -- a summary of all first-layer features. The conservation laws concern matrix-valued quantities that aggregate over all weights in a layer. Individual weights or individual examples do not obey such clean laws; the aggregation is essential.

**2. They are reproducible across architectures and datasets.**
Each of these laws has been observed across multiple architectural families and multiple data domains. Neural scaling laws hold for language models, vision models, and other domains. The edge of stability has been observed in fully-connected networks, VGG, and ResNet (as shown in Figure 4 of the paper). Neural collapse has been observed across multiple architectures. The conservation laws hold by construction for any architecture with the relevant symmetries. This cross-architecture, cross-dataset reproducibility is a strong signal that the laws reflect properties of the learning process itself, not of any particular architecture or domain.

**3. They admit (partial or complete) theoretical explanations.**
None of these laws is merely an empirical curiosity -- each has attracted theoretical work that has explained at least part of the observed behavior. Neural scaling law exponents have candidate explanations in terms of data manifold dimensionality and task structure. The edge of stability threshold of `2/η` is understood in terms of convex optimization stability theory, and the stabilization mechanism has been explained by Damian et al. (2022a) through third-order curvature. Neural collapse has been explained as an energy minimizer under cross-entropy loss and weight decay (Zhu et al., 2021). The conservation laws follow from Noether's theorem applied to the symmetries of the parameterization (Kunin et al., 2021). The neural feature ansatz remains the least theoretically grounded, but even there, partial explanations exist (Ziyin et al., 2024; Boix-Adsera et al., 2025).

The pattern -- empirical law discovered, theoretical explanation found -- is precisely the pattern that characterizes maturing scientific fields. The authors expect this pattern to continue:

> "Given how often scientific fields have developed in this way, it seems likely that deep learning will continue to yield empirical laws as its science matures."

**4. They suggest underlying mechanisms ripe for theoretical explanation.**
The most powerful aspect of these empirical laws is not their practical utility (though that is real) but their theoretical implications. A law as clean as "sharpness stabilizes at `2/η`" cannot be coincidental -- it must reflect a robust feature of the gradient descent dynamics. A phenomenon as geometric as neural collapse -- class means forming a regular simplex -- cannot be arbitrary -- it must follow from the optimization objective. The simplicity of the law is evidence for the simplicity of the cause.

This is the core argument of Section 2.3: the measurability of deep learning, combined with the simplicity of the empirical laws that have been found, creates an unusually favorable environment for theoretical progress. Unlike many complex systems in science, where measuring the relevant quantities is expensive or impossible, deep learning allows rapid experimentation and iteration. The challenge is not measurement but selection -- identifying which of the many measurable quantities obey simple laws.

---

### Methodological Takeaway: Top-Down Theorizing

Section 2.3 closes with an explicit methodological recommendation for theorists:

> "Theory can be built 'bottom-up,' starting from first-principles math as in Sections 2.1 and 2.2, or 'top-down,' starting from empirical observations and attempting to explain them. In this section we have highlighted a few notable examples of top-down theories. We expect more to come."

The top-down approach -- start with the empirical law, then find the mechanism -- has been productive throughout physics and chemistry. Kepler's laws preceded Newton's mechanics by decades. Ohm's law preceded the electron theory of conduction. The Planck radiation law preceded quantum mechanics. In each case, the empirical law was precise enough to constrain and eventually guide the development of the underlying theory.

The authors are careful to note that not all macroscopic statistics obey simple laws:

> "Of course, some caution is necessary: most macroscopic statistics don't obey a simple and general mathematical law -- or at least don't seem to until plotted against the right quantity -- and so the challenge is to find those that do."

This is a real challenge. The space of possible statistics to measure is enormous, and most of them are not lawful. The skill required is not just measurement but insight -- the ability to identify which statistics are likely to be lawful before running the experiments, or to recognize lawfulness in data once collected. The examples highlighted in this section -- loss vs. compute, sharpness vs. training step, class mean geometry, first-layer Gram matrix alignment, conserved matrix differences -- were not obvious a priori. They were found by researchers who combined theoretical intuition with empirical exploration.

The recommendation to "proactively use experiments to look for lawful regularities" is a call for this kind of empirically-driven theory-building. In the current moment, with deep learning systems highly measurable and the space of potential laws largely unexplored, this strategy seems particularly likely to be productive.

---

### Summary of Empirical Laws Covered

| Law | Quantity | Key Reference | Status |
|---|---|---|---|
| Neural scaling laws | Test loss vs. compute, data, parameters | Kaplan et al. 2020; Hestness et al. 2017 | Exponents not yet derived from first principles in realistic settings |
| Edge of stability | Hessian sharpness during training | Cohen et al. 2021a; Damian et al. 2022a | Threshold `2/η` explained; progressive sharpening in nonlinear networks open |
| Neural collapse | Final-layer class mean geometry | Papyan et al. 2020; Zhu et al. 2021 | Explained as energy minimizer under cross-entropy + weight decay |
| Neural feature ansatz | First-layer Gram matrix vs. gradient outer product | Radhakrishnan et al. 2024 | Partial theoretical explanations (Ziyin et al. 2024; Boix-Adsera et al. 2025) |
| Gradient flow conservation laws | Matrix quantities conserved under gradient flow | Saxe et al. 2014; Kunin et al. 2021 | Explained via Noether's theorem applied to parameterization symmetries |
