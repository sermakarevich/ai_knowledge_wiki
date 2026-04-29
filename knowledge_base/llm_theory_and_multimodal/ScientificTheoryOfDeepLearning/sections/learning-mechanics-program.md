> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## The Learning Mechanics Program

This file covers Sections 1.1--1.3 of Simon et al. (2026), "There Will Be a Scientific Theory of Deep Learning" (arXiv:2604.21691). The paper is a position and synthesis piece whose central thesis is stated plainly in its introduction:

> "This paper makes the case that, yes, there will be a scientific theory of deep learning; that we can see pieces of this theory starting to emerge; and that this theory will take the form of a mechanics of the learning process."

---

### Background: From Mathematical Questions to a Scientific Endeavor

Before articulating what learning mechanics is, the paper traces how deep learning theory arrived at this inflection point. The historical arc matters for understanding why "mechanics" is the right framing.

**Early questions were about expressivity and generalization.** Deep learning theory shares roots with the McCulloch--Pitts neuron and the perceptron. The earliest theoretical questions asked what functions simple models can represent and how they can be learned from data. As learning came to be understood as a statistical problem, the focus shifted to: when does learning from finite samples generalize? This produced classical learning theory -- statistical and computational/PAC learning theory -- paired with classical optimization theory. These frameworks gave clean end-to-end guarantees for simple, convex, parsimonious models. In parallel, statistical physics contributed satisfying theories of average-case behavior for simple models.

**The rise of deep learning broke those frameworks.** Neural networks are complex, nonconvex, and overparameterized -- in direct contrast with the regime where classical learning theory excels. They optimize and generalize better than classical approaches can guarantee or explain. More importantly, it became clear that neural networks were not merely fitting data; they were learning structured internal representations and displaying striking regularities across tasks and scales.

**A new kind of scientific tension emerged.** The paper explicitly frames the current situation in terms borrowed from the philosophy of science:

> "New scientific endeavors often start with an empirical tension in which nature presents something interesting we cannot predict or explain with existing tools, and although neural networks are artificial computational systems, this same scientific tension is present here."

This shift -- from a largely mathematical study of what is possible to a truly scientific effort to describe, explain, and ultimately predict the behavior of complex empirical systems -- is the defining transition. The authors argue it calls for the methods and sensibility of science, not just mathematics:

> "We should thus approach this task as scientists, embracing empirics, seeking unifying principles, and identifying recurring motifs. We should also expect the path forward to look more like the development of a scientific field than the development of a mathematical one."

---

### 1.1 What's in a Mechanics?

#### The Core Analogy

The name "learning mechanics" is not merely evocative branding. The authors construct a careful structural analogy between the physics of mechanics and the process of neural network training.

**Mechanics in physics** is the branch studying how forces acting on objects determine their movement through space and time. The paper maps each element of this definition onto deep learning:

| Physics | Deep Learning |
|---|---|
| Object moving through physical space | Model moving through parameter space via discrete updates |
| Forces from interactions between components | Interactions between parameters, dataset, task, and learning rule |
| Forces mediated by fields | Updates mediated by gradients |
| Systems settle at local minima of a potential | Networks converge to local minima of a loss landscape |

The authors are explicit that these are not superficial metaphors:

> "While the systems under study are very different, since the key problems of both are essentially about movement and interaction, we might expect some features of the resulting sciences to be shared."

#### Analogy Grounded in Actual Research Practices

The authors go further, showing that the analogy is already reflected in the five lines of evidence they identify:

- **Solvable settings:** All branches of mechanics develop a library of analytically solvable settings to gain intuition (e.g., the harmonic oscillator, the hydrogen atom). Learning mechanics does the same, with deep linear networks and kernel regression serving an analogous role.

- **Simplifying limits:** All branches of mechanics use limits as simplifying tools (e.g., the thermodynamic limit n, V → ∞; the classical limit ℏ → 0). Learning mechanics uses infinite-width and infinite-depth limits in the same way.

- **Coarse aggregate statistics:** Continuum and statistical mechanics -- the branches most directly dealing with large numbers of interacting components -- describe zoomed-out summary statistics rather than the motion of every particle. This approach has proven equally useful for dealing with the complexity of deep learning.

- **System parameters:** Every physical system has characteristic scales and coupling constants affecting its behavior, and techniques for treating these are essentially the same as those used to study hyperparameters in deep learning.

- **Universal behavior:** Physics is full of cases in which the same phenomena appear in very different settings (critical phenomena, renormalization group flow). Deep learning similarly exhibits universal behaviors across architectures and training settings.

#### Why "Mechanics" Specifically

The choice of the word "mechanics" is deliberate. The authors invoke the specific family: classical mechanics, continuum mechanics, statistical mechanics, and quantum mechanics. Each of these theories:
- Proceeds from first principles
- Makes quantitative predictions
- Uses limiting approximations as productive tools
- Focuses on aggregate or average-case behavior rather than tracking every degree of freedom
- Has a defined regime of applicability outside which it breaks down

The emerging science of deep learning, the authors argue, shares all these traits. The name encodes a research program, not just a description.

---

### The Seven Desiderata

Section 1.1 closes with a set of seven desiderata -- properties that a mature learning mechanics should satisfy. These are presented as the result of assessing how mature branches of mechanics were motivated, developed, and succeeded. Each desideratum is worth examining in full.

#### 1. Fundamental

> "Learning mechanics should be fundamental, proceeding logically from a first-principles description of neural network training. Interim assumptions about network weights, dynamics, and performance will be useful tools, but they should ultimately be explained from first principles."

The distinction here is important: the theory will use approximations and simplifying assumptions as scaffolding, but these are means to an end, not the end itself. A fully mature learning mechanics would derive the behavior of realistic networks from basic facts about architecture, data, and gradient-based optimization -- not from ad hoc assumptions introduced to make the math tractable. This desideratum sets learning mechanics apart from purely phenomenological or descriptive approaches.

#### 2. Mathematical

> "Learning mechanics should be mathematical, making unambiguous quantitative statements about important properties of neural networks. No mechanics is a qualitative science; neither will be learning mechanics."

The emphasis on "unambiguous quantitative statements" rules out vague intuitions or order-of-magnitude reasoning as the terminal product. The paper here invokes the comparison to physics directly: classical mechanics does not say "heavier objects fall faster under gravity" -- it says F = ma. Learning mechanics must aspire to the same precision. Verbal descriptions of phenomena are starting points, not conclusions.

#### 3. Predictive

> "Learning mechanics should be predictive, making claims supported by simple, repeatable empirical measurements. We have excellent experimental control of our system, and every major development should be unambiguously verified in experiment."

This desideratum reflects the authors' strong empiricist commitment. A key advantage of deep learning as a scientific domain -- one the authors highlight in Section 2 -- is that the "equations of motion" are fully known and every weight, activation, gradient, and loss value can be recorded. The system is unusually transparent and measurable. A theory that cannot make predictions verifiable against this rich experimental data is not a scientific theory in the intended sense. The bar is explicit: "unambiguously verified in experiment."

#### 4. Comprehensive

> "Learning mechanics should be comprehensive, describing aspects of neural networks' training process, hidden representations, and final weights in a single picture."

The scope covers three distinct aspects of neural networks: (a) the dynamics of training, (b) the structure of hidden representations, and (c) the statistics of final weights. A theory that accounts for only one of these -- say, training loss dynamics but not representation geometry -- falls short of comprehensiveness.

The authors are equally explicit about what comprehensiveness does not mean:

> "It is worth emphasizing that this theory will not -- and should not -- aim to describe everything. A map at the full resolution of the world would be the size of the world and thus of little use. What we seek instead is a theory that operates at the right level of resolution -- one that sacrifices detail in favor of insight."

This is a key philosophical commitment. The theory's value comes precisely from its ability to identify the right coarse-grained variables -- to know what to ignore as well as what to track.

#### 5. Intuitive

> "Learning mechanics should be intuitive, being simple, illuminating, and satisfying in its demystification of deep learning. Like physics, learning mechanics should strive for simple insight over technical complexity."

The word "satisfying" is notable here. The authors are not content with a theory that is merely correct but impenetrable. The goal is demystification -- the kind of "aha" clarity that, in physics, comes from understanding why a pendulum's period depends on length but not mass, or why entropy always increases. Technical complexity is a means to this end, not a virtue in itself.

#### 6. Useful

> "Learning mechanics should be useful, serving as the scientific foundation for applied deep learning as physics does for other forms of engineering. Concrete goals should include greatly reducing the need for hyperparameter tuning, giving predictive tools for dataset design, and providing rigorous foundations for AI safety work."

The analogy to physics-as-engineering-foundation is central to the paper's practical argument. Just as thermodynamics and electromagnetism enable chemical engineering and electrical engineering respectively, a mature learning mechanics should enable principled AI engineering. The paper names three concrete use cases:

- **Reducing hyperparameter tuning.** Currently, practitioners rely heavily on trial-and-error search over learning rates, batch sizes, weight decay, and other hyperparameters. Theory should replace this with principled prescriptions.

- **Predictive tools for dataset design.** Rather than assembling training data empirically and testing the results, theory should allow practitioners to reason in advance about what data will be beneficial.

- **Rigorous foundations for AI safety work.** The connection to safety is elaborated in Section 1.2 and Section 3.

#### 7. Humble

> "Finally, learning mechanics should be humble, being solid in what it describes and explicit about what it cannot. Every branch of physical science has a regime of applicability outside of which it breaks down, and these boundaries are taught together with the science so that it may be used reliably. We anticipate the mechanics of learning applicable to realistic deep learning will break down in many small-scale, handcrafted, or otherwise special cases, and this is the price we will pay for the right simple picture in the regimes we care about."

This is perhaps the most philosophically sophisticated desideratum. Classical mechanics breaks down at relativistic speeds; thermodynamics breaks down for very small systems; both are still extraordinarily useful because their regimes of applicability are clearly understood. Learning mechanics is expected to break down for small-scale, handcrafted, or otherwise special-case networks -- and this is explicitly accepted as a feature, not a bug. A theory that claims applicability everywhere is almost certainly wrong; a theory that knows its own limits can be trusted within them.

The paper notes that the seven desiderata together -- fundamental, mathematical, predictive, comprehensive, intuitive, useful, and humble -- would make learning mechanics "transformative, paradigm-setting" and capable of resolving "important open questions that have long remained out of reach."

---

### 1.2 Why Learning Mechanics Matters

The authors acknowledge that building learning mechanics will require "sustained effort, both intellectual and institutional" and therefore justify the investment across three categories of reasons.

#### Scientific Reasons: Understanding Intelligence and the Natural World

The scientific motivation rests on the observation that the striking engineering success of large neural networks implies they are exploiting deep principles of learning and representation that we do not yet understand.

The authors ground this in historical precedent:

> "This has historical precedent: technology has often preceded scientific theory, as was the case with steam engines' role in motivating thermodynamics, which went on to explain much more than engine efficiency."

The steam engine example is telling: practitioners built functional steam engines before Carnot or Clausius had any theory of heat. When thermodynamics finally arrived, it did not just explain why steam engines work -- it revealed the fundamental nature of energy, entropy, and equilibrium, with consequences far beyond engineering.

A second historical example is offered:

> "A similar story played out in flight: the development of airplanes through trial and error and inspiration from the natural world helped motivate aerodynamic theory, which in turn enabled both better aircraft design and a deeper understanding of how birds themselves fly."

By analogy, the principles that govern learning in artificial neural networks may shed light on biological intelligence:

> "In our case, the principles that govern learning in artificial neural networks may also shed light on our own biological intelligence, with potentially important implications for neuroscience and cognitive science."

This is a claim about the scope of learning mechanics extending beyond the artificial systems that motivated it -- just as thermodynamics extends beyond the steam engine.

#### Practical Reasons: Replacing Trial and Error with Principles

The practical motivation concerns the design and development of real-world AI systems. The current state is characterized by extensive trial and error:

> "Neural networks are still trained using methods discovered largely through trial and error rather than first principles, and theory plays little role in the day-to-day practice of deep learning."

A mature theory could replace this with principled guidance for model design, optimization, scaling, and deployment. The paper is careful to note that theory has already begun playing this role in limited cases:

- **Empirical scaling laws** (Section 2.3) -- allowing practitioners to predict model performance at scale before committing compute.
- **Mathematical prescriptions for hyperparameter scaling** (Section 2.4) -- particularly the maximal update parametrization (muP) and related frameworks.
- **Theoretically motivated optimizers and methods for data attribution** (Section 4).

The implicit argument is that these early successes are a proof of concept: if limited theory already reduces practical waste, more complete theory will do so more broadly and more reliably.

#### Safety-Related Reasons: The Governance Problem

The safety motivation is distinct from and arguably more urgent than the practical one:

> "The safety reasons concern our ability to describe, characterize, and govern increasingly powerful AI systems. Some form of regulation will likely be necessary, but it is difficult to regulate a technology that we cannot clearly describe."

The logic here is that regulation requires description. You cannot write meaningful regulations about properties you cannot characterize, measure, or predict. A theory that identifies the relevant variables, mechanisms, and organizing principles of large models would provide the descriptive basis needed for reliability, oversight, and control.

The paper also identifies a specific avenue:

> "One avenue by which fundamental theory might aid in AI safety is by supporting mechanistic interpretability, a point to which we return in Section 3."

The relationship between learning mechanics and mechanistic interpretability is described as potentially symbiotic -- a point the paper returns to in detail in Section 3. The brief framing offered in the abstract positions them as complementary disciplines:

> "Where mechanistic interpretability aims to be the biology of deep learning, learning mechanics should aspire to be its physics, mirroring the complementary relationship between biology and physics in the natural sciences."

Biology and physics are mutually supporting sciences: physics provides the foundational laws; biology explains the organization and behavior of complex systems built from those laws. The vision is that learning mechanics provides the physics layer -- the first-principles dynamical theory -- on which mechanistic interpretability (the biology layer) can build and from which it can draw rigorous support.

---

### 1.3 Plan for the Paper (Section Structure)

Section 1.3 lays out the paper's architecture, which is also useful as a map of what the authors consider the major components of the emerging field.

**Section 2 -- Five lines of evidence.** The core evidential argument. For each of the five research threads, the authors "motivate each line of evidence with an intuitive explanation and highlight examples of research successes that illustrate the underlying principle." (Detail on each line is covered in sibling section files.)

**Section 3 -- Relationship to other perspectives.** The paper situates learning mechanics relative to competing or complementary approaches: statistical and information-theoretic perspectives, and especially mechanistic interpretability. This is where the physics/biology symbiosis argument is developed.

**Section 4 -- Addressing objections.** The paper reviews and addresses "common arguments that fundamental theory will not be possible." This is an explicit engagement with skeptics -- an acknowledgment that the thesis is contested and an attempt to meet objections head-on.

**Section 5 -- Open directions.** A "portrait of ten important open directions in learning mechanics, from predicting scaling laws to eliminating hyperparameters, where we expect to see major progress in the coming years."

**Section 6 -- Advice for beginners.** The paper closes with practical guidance for young researchers and introductory resources, with a companion site at learningmechanics.pub.

**Intended audiences.** The paper explicitly identifies four audiences it hopes to reach:

1. **Veteran scientists of deep learning** -- the paper aims to synthesize useful approaches and results and to depict an emerging science in a galvanizing way.
2. **Deep learning practitioners** -- the paper aims to convince them that theory is on a path to practical utility and to encourage scientific observation of their systems.
3. **AI safety and mechanistic interpretability researchers** -- the paper aims to convince them that white-box, first-principles theory is difficult but possible, and that communities should collaborate.
4. **Young students and newcomers** -- the paper explicitly aims to lower the barrier to entry, articulating "deep intuitions about this science [that] have been percolating inside the theory community for a while."

---

### 1.4 Five Lines of Evidence (Preview)

Section 1.2 of the paper gives a preview list of the five bodies of evidence for an emerging mechanics of learning. Each has a dedicated subsection in Section 2; the preview here is one-sentence per line.

1. **Solvable idealized settings (Section 2.1).** A growing number of analytically solvable settings -- including deep linear networks, kernel methods, and multi-index models -- fully capture learning with simple mathematics, providing the intuition-building "toy models" that every mature mechanics requires.

2. **Tractable limits (Section 2.2).** Useful limits -- including the lazy vs. rich learning distinction, and limits of infinite width and depth -- reveal fundamental learning behaviors in the same way that the thermodynamic limit, the classical limit (ℏ → 0), or the hydrodynamic limit simplify physical systems.

3. **Simple empirical laws (Section 2.3).** In many cases, simple empirical laws suffice to capture meaningful macroscopic statistics, including test-time performance (neural scaling laws), loss-landscape sharpness (edge of stability), and representation structure (neural feature ansatz); these play the role of Kepler's laws or Boyle's law -- precursors to deeper first-principles derivation.

4. **Theories of hyperparameters (Section 2.4).** Many of the hyperparameters governing optimization can be disentangled and understood -- for instance, step size as a sharpness-regularizing parameter, and muP as a width-scaling prescription -- leaving behind simpler effective dynamical systems amenable to analysis.

5. **Universal behaviors (Section 2.5).** As applied deep learning has scaled up and converged on best practices, universal phenomena have increasingly appeared across settings and tasks -- common inductive biases, shared representations, and cross-architecture regularities that echo critical phenomena and renormalization group flow in statistical physics.

The authors also highlight the shared character of these five lines:

> "These lines of research broadly share several overarching characteristics: they are concerned with the dynamics of the training process; they primarily seek to describe coarse aggregate statistics of learning; and they emphasize accurate average-case predictions over rigorous worst-case bounds."

This shared character is precisely what makes them converge toward a coherent mechanics rather than a collection of disconnected results.

---

### Terminological and Conceptual Notes

**"Learning mechanics" vs. "theory of deep learning."** The authors use the phrase "scientific theory" throughout, but settle on "learning mechanics" as the proper name for the specific kind of theory they envision. "Theory" is too broad and does not capture the dynamics-centric, first-principles, average-case character of the emerging work. "Mechanics" encodes all of these properties by analogy to physics.

**"Alchemy to science."** The paper's framing of deep learning's current state as pre-theoretic or "alchemical" -- practitioners achieving results through trial and error without understanding why -- is implicit throughout the introduction, though the specific "alchemy" framing appears more explicitly in discussions of the field's culture (see Section 4). The introduction's description of "methods discovered largely through trial and error rather than first principles" and theory playing "little role in the day-to-day practice" captures the same idea.

**Complexity as the central challenge, not opacity.** Section 2 makes a point that is anticipated in Section 1's framing: the obstacle to a scientific theory of deep learning is not that the system is hidden or inaccessible, but that it is complex. Unlike many physical or biological systems where the governing equations must be inferred from observation, deep learning "directly exposes its 'equations of motion.'" Every weight, activation, gradient, and loss value is measurable. The challenge is that the interaction of architecture, data, task, and learning rule produces dynamics that are nonlinear, coupled, and high-dimensional. This reframing -- from mystery to complexity -- is central to the optimism of the paper: complexity can, in principle, be tamed by the right theoretical tools.

**The physics/biology analogy for the broader field.** The paper's vision of the relationship between learning mechanics and mechanistic interpretability deserves emphasis as a key conceptual contribution of Section 1. Rather than viewing interpretability and theory as competing or redundant, the paper proposes a complementary structure: learning mechanics is the physics (foundational, dynamical, first-principles); mechanistic interpretability is the biology (organizational, functional, higher-level). Each supports and constrains the other. This positions learning mechanics as a necessary substrate for safety-relevant interpretability work, not merely a parallel academic track.
