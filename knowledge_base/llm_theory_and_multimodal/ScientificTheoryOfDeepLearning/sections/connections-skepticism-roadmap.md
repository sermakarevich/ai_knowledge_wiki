> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Connections, Skepticism, and Roadmap

---

### 1. Relation to Other Perspectives

The authors of "There Will Be a Scientific Theory of Deep Learning" (Simon et al., 2026) situate learning mechanics within a landscape of ongoing theoretical efforts, arguing that these efforts are not competitors but are *essentially all complementary*: each perspective either directly pursues a mechanics of learning or would benefit from one symbiotically. The framing is explicitly pluralist -- different communities study the same system at different levels of abstraction, with different tools, and the field benefits from cross-pollination rather than consolidation under a single banner.

> "We believe that these perspectives are essentially all complementary: all either directly seek a mechanics of learning or would symbiotically benefit from one."

---

#### The Statistical Perspective

**Tradition and what it studies.** The classical learning theory tradition -- rooted in PAC learning, VC theory, and statistical generalization bounds -- asks how any prediction method can balance three fundamental desiderata: *expressivity* (representing rich real data), *complexity control* (making the most of finite training data), and *computational efficiency* (yielding practical algorithms). Bartlett et al. [2021] are cited as a lucid summary of this framing. The modern statistical viewpoint highlights two partial answers: (1) deep learning has an implicit inductive bias toward simple, well-generalizing functions (Wilson, 2025), and (2) overparameterization makes the highly nonconvex optimization landscape surprisingly tractable.

**Relation to learning mechanics.** The authors believe these two answers are "basically correct" but remain insufficiently precise. The statistical perspective thus arrives at the same destination as learning mechanics: to make these ideas precise requires a close look at the training process itself. The implicit bias cannot be characterized generically -- it must critically rely on specific properties of architectures and natural data. The authors write:

> "We do not believe these answers will be generic statements, but instead critically rely on important properties of deep learning and of natural data. The statistical perspective thus leads naturally to a serious scientific study of the mechanics of training."

**Specific institutions.** The Simons Institute for the Theory of Computing is credited with providing an important substrate for developing this statistical perspective through collaborations and seminars.

---

#### The Information-Theoretic Perspective

**Tradition and what it studies.** Closely related to the statistical perspective, the information-theoretic view treats learning as extraction of information from datasets. A learning system works when it extracts prediction-relevant information while discarding irrelevant information. In concrete terms, this becomes a compression hypothesis: learning compresses the dataset into either model parameters or hidden representations, and good generalization is the signature of successful compression. Key references include Shwartz-Ziv and Tishby [2017] and Xu and Raginsky [2017].

**Relation to learning mechanics.** The authors find this perspective "insightful" and regard it as likely correct in broad strokes. However, the same challenge applies as with the statistical perspective: the picture is compelling but not yet actionable. Making it concrete requires understanding how architecture, training process, and data interact to implement compression, and what factors modulate its success. The authors conclude:

> "The information-theoretic perspective thus also leads naturally to a serious scientific study of the mechanics of training."

**Distinction and complementarity.** This perspective is more of a high-level characterization (what learning achieves) than a mechanistic theory (how learning proceeds). Learning mechanics would provide the dynamical substrate that explains *how* compression actually occurs, making information-theoretic descriptions derivable rather than assumed.

---

#### Physics of Deep Learning

**Tradition and what it studies.** This community has a lineage reaching back to the origins of spin glass theory and neural network thermodynamics: Hopfield [1982], Amit et al. [1985], and Gardner [1988]. The modern incarnation (Zdeborovà, 2020; Bahri et al., 2020; Michaud, 2024; Ringel et al., 2025) seeks satisfying average-case theories of neural network learning -- not worst-case bounds, but typical-case descriptions that actually match observed behavior. The close relationship between physics and machine learning was recognized by the 2024 Nobel Prize in Physics. The community is mediated in part by recurring events at the Kavli Institute for Theoretical Physics, the Aspen Center for Theoretical Physics, and the Les Houches School of Physics, and through organizations such as the NSF AI Institute for Artificial Intelligence and Fundamental Interactions and the Simons collaboration on the physics of learning and neural computation.

**Relation to learning mechanics.** This perspective is described as "in line with (and has largely shaped) the perspective presented in this paper." The authors treat physics of deep learning as arguably the community already pursuing what they call learning mechanics. The primary challenge is then one of coordination: clarifying important open problems and organizing collective effort for efficient progress. The alignment is stronger here than with any other listed perspective -- the toolkit (statistical mechanics, random matrix theory, mean-field theory, replica methods), the questions (typical-case behavior, phase transitions, scaling), and the epistemological style (predict, measure, explain) match what the paper advocates.

---

#### Perspectives from Neuroscience

**Tradition and what it studies.** Neuroscience contributes at least two distinct approaches to the science of learning systems. The first starts from high-level hypotheses about neural computation -- for example, that the brain implements approximate probabilistic inference -- and derives predictions testable against both biological neural data and deep network behavior (Dayan et al., 1995; Friston, 2010). The second, *systems neuroscience*, aims to decompose subsets of the brain into interpretable circuits and reverse-engineer the structure of learned representations (Chung and Abbott, 2021; Bernardi et al., 2020; Kriegeskorte et al., 2008).

**Relation to learning mechanics.** The authors note that some predictions from high-level neuroscience hypotheses transfer remarkably well to deep networks: the classic case is edge-selective cells in the visual cortex (Olshausen and Field, 1996) and edge-selective receptive fields in convolutional networks (Zeiler and Fergus, 2014). Systems neuroscience resembles mechanistic interpretability -- the latter has explicitly adopted some of its methods and intuitions.

**Alignment and open questions.** The authors expect this dialogue to continue and regard it as plausible that some high-level neuroscience hypotheses will carry over to deep learning -- for instance, that networks admit partial decomposition into interpretable circuits and that local circuits implicitly solve inference tasks. Crucially, the *reasons* these facts hold, if they do, are bound up in the dynamical character of learning itself. A study of learning mechanics is therefore important to exploring these neuroscience-inspired ideas rigorously.

---

#### Developmental Interpretability / Singular Learning Theory

**Tradition and what it studies.** This approach grew out of the mechanistic interpretability community and seeks first-principles predictive theories of neural network learning grounded in the singular learning theory framework of Watanabe [2009]. It emphasizes a Bayesian perspective and frames training as a process of sequential phase transitions mediated by the geometry of the loss landscape. Key references include Hoogland et al. [2023]. The program explicitly aims for a rigorous foundation for interpretability rather than a qualitative catalog of mechanisms.

**Relation to learning mechanics.** The authors express strong alignment in *goals* -- developmental interpretability seeks the same fundamental mechanics of learning and the same rigorous foundation for interpretability that the paper advocates. The distinction is one of *toolkit*: singular learning theory draws on algebraic geometry, Bayesian model selection, and the mathematics of singular statistical models, whereas other learning mechanics approaches draw more on statistical physics, random matrix theory, and dynamical systems. The authors see "potential for fruitful cross-pollination and tool-sharing between these different approaches," treating the two as complementary routes toward the same destination.

---

#### Science of Deep Learning

**Tradition and what it studies.** The science of deep learning community starts from the recognition that ML practice is largely trial and error and aims to systematize it (Langley, 1988; Gal, 2015; Rahimi, 2017; Baraniuk et al., 2020). Much of the rapid empirical progress of the last decade has come from systematic organization around agreed-upon benchmarks (Donoho, 2024). Yet the authors observe that training and deploying large models "remains more alchemy than science."

**Relation to learning mechanics.** Learning mechanics is positioned as the *foundation* on which the science of deep learning must eventually be built. This is the most explicit statement of hierarchy in the paper: the science of deep learning community is asking the right applied questions, but without a mechanics of training, those questions can only be answered empirically, case by case. A mechanics of learning would provide the principled substrate that converts empirical practice into genuine scientific understanding -- analogous to how atomic theory underpins chemistry.

---

### 1.1 Learning Mechanics and Mechanistic Interpretability: A Symbiosis

Mechanistic interpretability (MI) receives dedicated subsection treatment (Sec 3.1) because, in the authors' view, it presents "a unique opportunity for cooperation" -- the most fully developed bilateral relationship described in the paper.

---

#### What Mechanistic Interpretability Studies

MI aims to understand trained neural networks by identifying the internal mechanisms -- features, circuits, and learned algorithms -- that give rise to their behavior. Its guiding belief is that neural networks admit a human-understandable, mechanistic description that can be uncovered through careful empirical reverse engineering. The community operates under several working assumptions (informally):

1. Neural networks encode the state of internal computational variables in their activations, often called "features."
2. Successive layers transform and combine these features in structured "circuits."
3. Taken together, these circuits implement algorithms that admit some level of human-understandable description.

The field has produced striking results in large models: Olah et al. [2020], Templeton et al. [2024], Engels et al. [2024], Gurnee et al. [2025], Lindsey et al. [2025]. It is deeply associated with Anthropic and the AI safety / Effective Altruism communities, though increasingly pursued in academic labs. The authors also note that mechanistic interpretability has recently bifurcated into (a) an ambitious camp hoping to develop full explanatory scientific theory and (b) a pragmatic camp focused on targeted interventions for particular cases.

---

#### The Physics-Biology Analogy

The authors frame the learning mechanics -- mechanistic interpretability relationship through the analogy of *physics and biology*:

> "These approaches study the same system -- i.e., deep learning -- at different levels of abstraction, and so of course they can (and should) work together for mutual gain."

Learning mechanics is to MI as physics is to biology -- or, using the paper's explicit three-level framing drawn from Marr's levels of analysis:

- **Learning mechanics** = the physics of deep learning (implementation level, quantitative, low-level)
- **Mechanistic interpretability** = the biology of deep learning (algorithmic level, structural, intermediate)
- **Model psychology** = capabilities, personality, and goals of the model (computational level, highest abstraction)

The paper notes that learning mechanics is "the farthest from model psychology, with mechanistic interpretability (the biology) lying in the middle and connecting the two." A consequence is that neither level alone is sufficient: learning mechanics cannot answer questions of semantic meaning on its own (it is too low-level), and MI remains largely qualitative without the mathematical backbone that learning mechanics can provide.

> "At time of writing, mechanistic interpretability remains largely a qualitative science, more reliant on human-judged empirics than on compact mathematical principles or simple governing laws."

> "On the other hand, a mechanics of learning would be quantitative by definition, but by the same token will be too low-level to answer important questions of semantic meaning on its own."

Calls for rigorous foundations for interpretability have been steadily growing (Sharkey et al., 2025; Joshi et al., 2026; Greenspan et al., 2026), and the authors regard this as a primary service that learning mechanics can and should provide.

---

#### How Learning Mechanics Formalizes Core MI Assumptions

The paper identifies four core assumptions that guide MI research, all of which are currently implicit or incompletely justified. Learning mechanics can make these explicit, formalize them, and, where necessary, challenge them:

1. **Linear representability** -- features correspond to meaningful directions in activation space. The representational geometry of neural networks is approximately linear at the level of semantically meaningful variables (Mikolov et al., 2013; Park et al., 2023a; Nanda et al., 2023b; Marks and Tegmark, 2023; Jiang et al., 2024; Csordás et al., 2024).

2. **Locality** -- features and circuits are localizable to particular subsets of model components. Causal effects of computation are concentrated in identifiable, relatively small subsets of weights or neurons (Meng et al., 2022; Wang et al., 2022; Conmy et al., 2023; Arora et al., 2025).

3. **Sparsity** -- individual features and circuits are activated or functionally relevant on only a small fraction of inputs. Any given mechanism fires rarely relative to the full input distribution (Cunningham et al., 2023; Bricken et al., 2023).

4. **Compositionality** -- complex network representations and computations arise from the composition of simpler, modular sub-mechanisms (Thorpe, 1989; Smolensky, 1990; Lepori et al., 2023; Schug et al., 2023; Ramesh et al., 2023).

The paper notes that learning mechanics offers the tools to clarify:
- the *regimes* in which each assumption holds,
- the *conditions* under which it fails, and
- the *derivation* of each assumption from training dynamics and data statistics.

This is directly connected to Open Direction 4 (defining features formally) discussed below.

---

#### How Learning Mechanics Explains the Dynamical Emergence of Mechanisms

MI has prioritized the question of *what* mechanisms trained networks contain; learning mechanics addresses the complementary question of *how* and *why* such mechanisms form through training. This dynamical perspective is already attracting substantial interest within parts of the interpretability community:

- Formation of induction heads (Elhage et al., 2021; Olsson et al., 2022)
- Grokking and progress measures (Nanda et al., 2023a)
- Sudden phase transitions in circuit formation (Elhage et al., 2022; Chen et al., 2023; Gopalani et al., 2024; Park et al., 2024)
- The developmental interpretability research program (Hoogland et al., 2023, 2025)

The authors invoke Saphra [2022]'s vision that learning mechanics could play a role analogous to evolution in biology:

> "Echoing Saphra [2022], we hope that learning mechanics can play a role analogous to evolution in biology: just as 'nothing in biology makes sense except in the light of evolution,' the internal mechanisms of trained networks may be most naturally understood in the light of the processes that give rise to them."

The goal is not to replace MI efforts but to foster deeper engagement between mechanistic interpretability and the mathematical framework of learning mechanics -- making the emergence of mechanisms not merely an observed fact but an explained consequence of training dynamics.

---

#### What MI Provides Back to Learning Mechanics

The relationship is explicitly bidirectional. MI has deeply influenced learning mechanics by providing concrete, well-defined empirical phenomena that invite first-principles explanation.

A key epistemological contribution: MI places the structure of data at the center of its analyses, revealing settings where the relationship between input structure and learned mechanisms is especially transparent (Nanda et al., 2023a; Shai et al., 2024). Classical deep learning theory has instead relied on highly simplified data models, leaving a persistent gap between theoretical predictions and observed behavior. MI helps bridge this gap by giving theorists concrete targets -- specific phenomena to explain rather than generic bounds to derive.

Specific MI observations that have already proven influential in stimulating learning mechanics work:

- **Emergence of induction heads for in-context learning:** Bietti et al. [2023], Reddy [2023], Nichani et al. [2024]
- **Role of Fourier features in algebraic tasks:** Morwani et al. [2023], Kunin et al. [2025], Marchetti et al. [2026]
- **Geometry of features arising from correlations in data:** Engels et al. [2024], Prieto et al. [2025], Karkada et al. [2026]

> "Just as the development of physics was often driven by empirical discoveries in adjacent fields, we expect progress in learning mechanics to be driven by theorists who take seriously empirical phenomena, including those uncovered by the mechanistic interpretability community, and seek to explain them."

In summary: MI offers learning mechanics a rich and growing tableau of empirical phenomena ripe for mathematical theory -- well-defined targets, controlled settings, and structured data environments that make the development of theory tractable.

---

### 2. Reasons for Skepticism and Responses

The authors devote Section 4 to addressing common counterarguments in an explicitly intellectually honest way. Rather than dismissing skepticism, they enumerate each objection and provide a detailed response. Five main skeptical positions are treated.

---

#### Objection 1: "Competent researchers have been trying for decades and we don't have a theory. Surely if there was one, we would have found it."

**The objection in full:** Machine learning theory has a long history. Many avenues have been thoroughly explored. Why should now be different?

**The response.** The authors offer three reasons for optimism:

1. **The empirical landscape has fundamentally changed.** The practical success of deep learning is comparatively recent. There is now a wealth of new empirical systems to study and mine for explainable phenomena. Some of the most important phenomena -- for example, the apparent convergence to universal representations discussed in Section 2.5 -- were only revealed by recent years of model scaling. These developments have transformed the search for a theory from a purely mathematical exercise into an empirical science with no shortage of interesting things to measure and a tight feedback loop for checking hypotheses.

2. **The field is much larger and more diverse.** Empirical successes have attracted researchers from physics, mathematics, neuroscience, and other adjacent fields. More minds, and more diverse ones, are working on the problem than ever before.

3. **Major sciences take decades.** The development of thermodynamics, quantum mechanics, and evolutionary biology each required several decades of sustained effort. The authors argue we should not be discouraged that we do not yet have all the answers -- the timescale expectation should be calibrated accordingly.

---

#### Objection 2: "The objects currently understood theoretically are very primitive compared to LLMs. First-principles understanding of large models is too heavy a lift."

**The objection in full:** Existing solvable models (deep linear networks, kernel methods) bear little resemblance to the transformer architectures running state-of-the-art systems. The gap seems unbridgeable.

**The response.** The authors concede that building up to LLMs "will be a heavy lift and take considerable time." But they argue the near-term value of learning mechanics does not require a complete constructive theory of any large model. The hope is instead that understanding basic building blocks proves useful even without full coverage. This is already happening in isolated pockets:

- **Empirical scaling laws** (Section 2.3): useful for predicting loss as a function of compute even without a full model theory.
- **Mathematical prescriptions for hyperparameter scaling** (Section 2.4): µP and related frameworks allow optimal hyperparameters to be transferred across scale.
- **Neural-tangent-kernel-based methods for data attribution** (Park et al., 2023b): provide useful data selection tools from a theoretical substrate.
- **Theoretically motivated optimizers** (Gupta et al., 2018; Jordan et al., 2024): emerged from principled analysis of optimization geometry.

These "local theories" of small pieces of the deep learning stack are already useful for large model training without being comprehensive theories. The authors draw an analogy to atomic theory: understanding that matter is made of atoms underlies virtually all basic science, even before one can simulate a protein from scratch. Similarly, learning mechanics can offer foundational tools that MI and other applied communities can use in their work, bridging toward large models without requiring a complete top-down theory.

---

#### Objection 3: "What matters is a model's high-level behavior. Microscopic theories are too zoomed in to be relevant."

**The objection in full:** Practitioners and safety researchers care about what models do -- their capabilities, failure modes, and alignment properties. A microscopic theory of training dynamics is too far removed from these concerns to matter.

**The response.** The authors explicitly acknowledge the importance of high-level behavior, then argue that deep learning can and should be studied at multiple levels simultaneously:

- **Physics level (learning mechanics):** training dynamics, optimization, representation formation -- the implementation.
- **Biology level (mechanistic interpretability):** features, circuits, learned algorithms -- the algorithm.
- **Psychology level:** capabilities, personality (Betley et al., 2026), and goals of the model -- what is computed.

They note that this hierarchy maps roughly onto Marr's three levels of analysis of a computational system: physical implementation, algorithmic description, and computational specification. The microscopic level is not the only relevant one, but it is the foundation. Without it, the higher levels lack explanatory grounding. Mechanistic interpretability is explicitly positioned as the bridge connecting physics to psychology, making the low-level work directly relevant to high-level questions about behavior.

---

#### Objection 4: "We don't need a theory of deep learning. We need a theory of data."

**The objection in full:** The bottleneck to understanding deep learning is our poor formal understanding of the structure of natural data (images, text, audio). A theory of data would be more valuable than a theory of learning dynamics.

**The response.** The authors argue we need *both*, and that both are part of the same project. A unified mechanics of learning must encompass a theory of how a parameterized model learns from data, and this requires a characterization of the structure of data that the model exploits. These are not competing research programs but jointly necessary components. The paper touches on this explicitly in Section 2.5 (universality of representations and what they reveal about data structure) and Open Direction 2 (developing a theory capable of capturing natural data).

---

#### Objection 5: "AI will understand itself before we do. Why bother building human theory?"

**The objection in full:** AI systems may soon be capable of advancing deep learning theory faster and more effectively than human researchers. If so, the human effort to build theory is either redundant or will quickly be superseded.

**The response.** The authors give a three-part answer:

1. **Theory is already useful and will become more impactful.** The work being done now contributes to near-term practical impact -- it is not merely speculative future-proofing. Investing in theory is not premature even in the current AI landscape.

2. **AI will not suddenly and separately "solve" deep learning theory.** Breakthrough progress in the near term is more likely to come from human scientists *using or working with* AI than from AI operating in isolation. Expert humans will remain in the loop during this transitory period.

3. **Human-parseable theory is essential for AI safety.** If one's goal is AI safety, some degree of human oversight of AI systems will be necessary (unless one trusts AIs to fully police themselves). A human-understandable theory of deep learning gives researchers and oversight bodies "a foot in the door" -- a principled language for understanding and intervening in AI behavior that does not require trusting the system to explain itself.

---

### 3. Open Directions in Learning Mechanics

Section 5 presents a curated list of open directions that the authors expect a mechanics of learning to address within the next decade. The directions are loosely ordered by their connection to the lines of evidence introduced in Section 2. For a longer catalog and community discussion, the authors point to `learningmechanics.pub/openquestions`.

---

**Open Direction 1: What are simple, solvable models of genuinely deep, nonlinear learning?**

Deep linear networks and kernel methods are the two main workhorse solvable models of learning mechanics. Deep linear networks capture the nonlinear dynamics of parameters through training, while kernel methods capture nonlinear function learning from data. However, these tools are complementary rather than unified: no existing solvable model captures *both* forms of nonlinearity simultaneously. A few special cases with both are known, but no general framework has emerged.

The research question: Can we find a class of solvable models that captures both deep, nonlinear dynamics *and* nonlinear function learning, while maintaining some level of generality? Can such models illuminate feature learning, the role of depth, optimization phenomena (such as progressive sharpening), and architectural innovations (normalization layers, residual streams, self-attention, gated nonlinearities)? Can the framework usefully extend to modern learning paradigms -- self-supervised learning, reinforcement learning, denoising diffusion?

---

**Open Direction 2: What would a theory capable of capturing natural data look like?**

Deep neural networks find and exploit structure in natural data, which means that data structure must enter into our theories. Despite data complexity, models often appear to derive their learning signal from a small set of sufficient statistics. What are these minimal data statistics? How do they enter into a predictive theory of what the model learns? Are the relevant statistics different for different models or at different stages of training? Can the relevant structure of a dataset be described by a model with free parameters found via empirical fit?

This direction is motivated by the observation (Section 2.5) that representations trained across vastly different settings converge, suggesting that the relevant structure of natural data is in some sense identifiable and universal. A theory of data and a theory of learning must be developed in concert.

---

**Open Direction 3: Does deep learning implicitly minimize some notion of functional complexity?**

Deep networks trained by conventional optimizers are widely believed to have a bias toward simple functions. This idea appears under many names -- implicit regularization, maximum margin bias, simplicity bias, spectral bias -- but has only been characterized precisely in highly specific settings, and no general picture has emerged.

The questions: Do deep neural networks broadly seek to minimize a precise notion of complexity among functions with low loss? If so, what is the appropriate notion -- Kolmogorov complexity, circuit complexity, weight norm, or something else? In what settings is this minimization exact, and when only approximate? Do the sparse features and circuitry studied by mechanistic interpretability naturally emerge as the solution to such a minimization problem?

---

**Open Direction 4: How do we formally define the features learned by neural networks?**

Mechanistic interpretability seeks to identify features, circuits, and mechanisms in trained networks, but these concepts currently lack precise mathematical definitions grounded in first principles. Can such definitions be developed? What formal structures naturally emerge? Can these notions be used to evaluate and formalize the central assumptions of mechanistic interpretability -- linear representability, locality, sparsity, and compositionality (as discussed in Section 3)?

This direction also asks how formal feature definitions connect with the rich-vs.-lazy picture of feature learning (Section 2.2) -- a distinction that is mathematically sharper but semantically less meaningful. Bridging these two framings would be a significant unification.

---

**Open Direction 5: Are finite neural networks properly understood as approximations to infinite limits?**

The paper articulates the *Discretization Hypothesis*: finite neural networks are simply discretized approximations to infinite networks, analogous to how a spatiotemporal discretization numerically approximates the solution to a differential equation. For width, the limiting continuous object is the measure of neuron activity in hidden layers. For depth in residual networks, finite depth can be viewed as a discretization of a neural SDE or ODE. Small step sizes can render stochastic optimization algorithms approximately equivalent to some kind of flow.

In this view, increasing model size (and decreasing learning rate while commensurately increasing step count) improves performance by decreasing discretization error, at the cost of additional computation. The questions: Is this the right way to understand width, depth, learning rate, and other finite hyperparameters? What does the limiting continuum system look like?

---

**Open Direction 6: Can we understand and eliminate all hyperparameters?**

Sections 2.2 and 2.4 outline a research program in which hyperparameters are systematically analyzed, disentangled, and in some cases removed by taking appropriate limits (e.g., infinite-width limits naturally eliminate certain width-dependent hyperparameters). How far can this program go? Can we reach zero hyperparameters, or are some irreducible? If all hyperparameters could be eliminated, what would remain -- and would the resulting system be more interpretable or more predictable?

---

**Open Direction 7: Can we predict scaling law exponents a priori?**

Large models exhibit robust power-law scaling of loss with respect to model size, data, and compute (Section 2.3). The observed exponents are nontrivial -- they do not appear to be simple fractions that might result from elementary dimensionality arguments. It is widely believed that these values are driven largely by structure latent in the dataset, though they may also depend on architecture and optimizer details.

Many explanations for scaling laws have been proposed, but a decisive test of any such theory is its ability to predict the exponents *quantitatively from first principles*. No framework currently does this robustly across realistic settings. The questions: Can we develop a theory that both explains why power laws arise and predicts their exponents a priori? What measurements of the dataset, architecture, and optimization are required?

---

**Open Direction 8: How does loss curvature interplay with architecture, features, and generalization?**

A significant feature of deep learning optimization is that the optimizer implicitly regularizes curvature along its trajectory, steering toward regions of the loss landscape with lower curvature. Progress has been made formalizing this using curvature-penalized gradient flows (Sections 2.3 and 2.4), but the implications remain unclear.

Open questions: Why does curvature tend to rise in the absence of implicit regularization ("progressive sharpening"), and can this be attributed to specific architectural or data distribution properties? How does implicit curvature regularization affect the features that are learned? Why does it sometimes lead to improved generalization? What is the mechanistic link between curvature dynamics and representation structure?

---

**Open Direction 9: What makes for a good optimizer in deep learning?**

It remains fundamentally unclear why some optimizers work better than others. Why do adaptive methods -- Adam, Muon -- consistently outperform simpler alternatives like SGD when training large language models? How does adaptive preconditioning interact with network architecture and the loss landscape to yield faster, more stable training? Can we identify fundamental principles that explain the success of modern optimizers, predict when they will fail, and guide the design of new ones?

This direction bridges optimization theory and learning mechanics, asking for principled explanations rather than empirical comparisons of optimizer performance.

---

**Open Direction 10: In what sense do large models trained differently learn similar representations?**

Evidence discussed in Section 2.5 suggests that large models trained from different random seeds -- and sometimes with different widths, architectures, data, or objectives -- tend to learn similar internal representations. A precise version of this claim would be powerful: it would give theorists confidence that theory developed for one model and setting transfers broadly.

The central methodological challenge is defining "similarity" for high-dimensional representations. Metrics based on kernel alignment, nearest-neighbors, model stitching, and more compare different aspects of representation geometry. Which are stable across training regimes? What is the appropriate metric to quantify similarity? What is the largest range of experimental settings under which convergence is observed -- what are the *representation universality classes*?

---

### 4. How to Get Involved + Tenets

#### Encouragement for Newcomers

Section 6 extends an explicit invitation to researchers who want to contribute to learning mechanics, paired with the observation that no single academic background is required. The authors note:

> "There is no specific academic background required to do useful work in this field. Well-regarded researchers in deep learning theory come from backgrounds in physics, mathematics, computer science, neuroscience, statistics, and more."

The authors argue that knowing another field well is an asset -- established ideas from other fields can be applied to deep learning in some form, as the diversity of perspectives surveyed in Section 3 demonstrates. Cross-pollination is explicitly valued over specialization. The stated prerequisites are deliberately minimal: a firm grasp of undergraduate mathematics, a familiarity with deep learning, and a desire to learn.

The community infrastructure mentioned includes:
- The `learningmechanics.pub` website (with open questions, introductory material, and community discussion in comments)
- The *Physics Meets ML* talk series
- The *Physics of Learning* talk series

The authors close with an explicit call to action:

> "We encourage taking a crack at the open directions in Section 5. Work hard, have fun, and best of luck -- we hope to see a great deal more fundamental science of deep learning in the next few years!"

---

#### 6.1 Tenets for Getting Started

The authors compile six guiding principles for doing research in learning mechanics. These are explicitly not intended to maximize short-term citation counts or to follow the path of least academic resistance. They are intended to maximize long-term impact and community integration.

> "These tenets are not intended to maximize your number of citations in the short term, and following them may involve some swimming against the current of academia. Instead, they are intended to maximize your impact in the long term and your ability to integrate and contribute to the community."

---

**Tenet 1: Do experiments frequently.**

> "As discussed in Section 2.3, deep learning is a field where the cost of doing experiments is relatively low, with a fast turnaround time. Use that to your advantage! Experiments serve to check assumptions, inform theoretical models, reveal the limitations of a theory, peer beyond the cases that a theory covers, and surface interesting phenomena to study in the first place. Try to include experiments in every paper, and make them as simple and revealing as possible."

The emphasis on experiments is distinctive for a field nominally oriented toward mathematical theory. The authors treat experimentation not as supplementary validation but as an integral part of the research loop -- the mechanism by which theory stays grounded and by which new phenomena worth explaining are discovered.

---

**Tenet 2: Simplicity and insight matter more than technical complexity.**

> "If you want to do work that is useful for others, they need to understand it, not merely be impressed by it. Take the time to simplify your findings, identify the underlying intuition, and check with simple experiments. A useful idea for thinking about a type of problem is generally more valuable than a difficult theorem or a solution to any particular problem, so emphasize these useful ideas when you present your work. This will make your results more accessible and easier for others to extend and apply."

The authors explicitly acknowledge the tension with academic incentives:

> "Your conference reviewers may disagree with this philosophy -- the conference system tends to reward technical complexity and undervalue simplicity -- but it will make your work more impactful in the long run."

---

**Tenet 3: Value scientific understanding over state-of-the-art performance.**

> "Applied deep learning is a field of engineering whose progress is measured by benchmarks. For scientists of deep learning, the game is different: your contribution is gauged by your contribution to collective understanding. It is easy to feel pressure to tack on some engineering benefit in a scientific paper to make the paper seem more relevant and timely, but doing so usually dilutes the paper's scientific contribution without really affecting practice."

The authors do not say performance improvements are worthless -- they note that "fundamental science should eventually improve state-of-the-art performance, and when this naturally falls out of the science, it is a powerful way to demonstrate what has been understood." But when it does not naturally arise, they counsel:

> "Set benchmarks aside for the time being and seek understanding on its own terms."

---

**Tenet 4: Don't try to do it alone.**

> "Deep learning is a field with a lot of history and many known results, and guidance from a live human will help you. You can get pretty far from reading material online and talking to AI, but it doesn't replace human collaboration and mentorship. You should seek out other people interested in this area, ask for their feedback, and ask to work with them."

A practical corollary is added: when a talk version of a paper exists, watch it in addition to reading the paper. The authors observe that "a great deal more of the nuance of a project is conveyed through a live presentation." The *Physics Meets ML* and *Physics of Learning* series are cited as good sources for such talks on learning mechanics.

---

**Tenet 5: Try a few different problems before going deep into one.**

> "Deep learning theory has so many open questions that you probably won't know where to start. That's okay -- just jump in, and feel free to change problems a few times early on. Knowing multiple areas is essential to having high-level ideas anyways, and working in an area is the best way to learn it."

This tenet counsels against premature commitment. The field is young and fast-moving, and early breadth is presented as both epistemically valuable (cross-area knowledge generates high-level ideas) and practically healthy (early pivots are low-cost and high-information).

---

**Tenet 6: Invest in fundamental tools and techniques.**

> "Compared to more established fields of science, mathematics, and engineering, deep learning is very young. These other fields have identified deep ideas and developed powerful tools applicable to broad classes of problem. Learning these fundamental tools comes in handy when similar problems arise in deep learning."

Specific tools highlighted:

- **Statistical physics and random matrix theory:** powerful for thinking about high-dimensional interacting systems; directly applicable in learning mechanics when taking infinite limits.
- **Classical optimization theory:** central ideas make regular appearances in neural network optimization analysis.
- **Statistical signal processing** (wavelet decompositions, graphical models, information theory): comparatively underutilized in learning mechanics but potentially valuable and complementary tools.

The investment in fundamental tools is framed as a long-term bet: deep learning is young enough that the right mathematical frameworks have not yet been identified, and researchers who bring tools from adjacent mature fields are disproportionately likely to find new purchase on hard problems.

---

#### Summary of the Invitation

The section closes with the authors putting as much useful introductory material as possible on `learningmechanics.pub` and encouraging discussion in comments there. The spirit is explicitly welcoming and collaborative -- the field is open, the problems are important and tractable, and the authors want it to grow. The six tenets collectively describe a research style that is empirically grounded, mathematically substantive, socially integrated, and intellectually humble -- biased toward genuine understanding over apparent sophistication.
