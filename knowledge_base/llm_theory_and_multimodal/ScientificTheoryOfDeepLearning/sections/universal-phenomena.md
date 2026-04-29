> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Universal Phenomena Across Settings and Tasks

### Overview

Deep learning is not a single fixed recipe. Practitioners combine wildly different architectures (convolutional networks, transformers, U-Nets, recurrent models, graph networks), train on data spanning vision, language, speech, protein sequences, and games, and optimize with a variety of objectives -- contrastive, autoregressive, diffusion, supervised cross-entropy. The resulting model ecosystem is extraordinarily diverse. This diversity is what makes deep learning powerful in practice, but it also makes the project of building a scientific theory feel daunting: where does one even look for universal laws if every system seems different?

Section 2.5 of Simon et al. (2026) addresses this directly by marshaling a growing body of evidence that, beneath the surface variation, universal phenomena are at play. The argument is structurally analogous to a central episode in the history of physics: the theory of critical phenomena and universality classes. In that story, systems with completely different microscopic constituents -- magnets, fluids, alloys -- were found to exhibit identical behavior near phase transitions (the same critical exponents, the same scaling laws). This was unexpected and striking, and it forced theorists to realize that the fine-grained details of the constituents were irrelevant; what mattered was a much smaller set of aggregate features. The theoretical framework that made sense of this -- the renormalization group -- formalizes the idea that

> "as one examines a system from a more and more zoomed-out perspective, most details 'wash out' and only a handful of aggregate effects remain important."

The same logic applies to deep learning, the paper argues. If many very different neural network systems exhibit the same behaviors, there must be an underlying explanation that does not depend on the particulars of any one system. That explanation -- whatever it turns out to be -- is exactly the target of a learning mechanics theory. Universality thus plays a double role: it is empirical evidence that a coherent theory exists, and it provides guidance about what level of abstraction the theory should operate at.

The paper also invokes convergent evolution as an analogy from biology: species that solve similar problems tend to find similar solutions after many generations of selection pressure, regardless of their phylogenetic starting point. Deep learning systems, optimized by gradient descent on similar data distributions, may be doing something analogous.

The section organizes the universal phenomena into three distinct viewpoints:

1. Different architectures achieve comparable performance -- and sometimes identical input-output behavior -- on the same tasks.
2. Different datasets and modalities share common statistical structure.
3. The internal representations learned by different networks converge toward a common form.

Each of these is a different level at which universality manifests, and together they build a compelling case that deep learning is not a collection of independent engineering tricks but a coherent domain amenable to scientific theory.

---

### Universal Inductive Biases

The first and most practically visible form of universality is in performance: many architectural choices that look very different from the outside end up achieving similar results when given equivalent resources.

The clearest example is the long-running debate between convolutional networks (ConvNets) and vision transformers. For years after the transformer architecture was adapted for vision (Dosovitskiy et al., ViT), practitioners debated which class of model was fundamentally superior. Subsequent careful comparisons found that

> "after much debate [they] have been shown to obtain similar performance when matching compute, data size, and training recipes [Liu et al., 2022, Smith et al., 2023]."

The qualifier is important: "when matching compute, data size, and training recipes." Early comparisons failed to control for these confounders, which created the appearance of architectural differences that were really just differences in engineering effort applied to each family. Once experimental conditions were equalized, the gap largely disappeared.

But similar performance scores might still conceal different intermediate behaviors -- the models could be computing different functions and arriving at similar loss values for unrelated reasons. The case becomes much stronger when the functional similarity is demonstrated at the level of inputs and outputs. Zhang et al. (2024) provide exactly this for diffusion generative models: when transformers and U-Nets are trained as the denoising backbone of diffusion models and then fed with the same noise samples at inference time, they

> "generat[e] near-identical images when fed with the same noise samples [Zhang et al., 2024]."

This is a remarkable result. The two architectures have different inductive biases -- transformers operate via global self-attention; U-Nets combine local convolutions with a hierarchical encoder-decoder structure -- yet they converge to nearly the same input-output mapping. They have, in effect, learned the same function.

The paper interprets this as strong evidence that the architectures share similar inductive biases despite their surface differences. The relevant question then shifts from "which architecture is best?" to "what are those shared inductive biases, and why do they arise?"

Recent theoretical work has started to answer this. Kadkhodaie et al. (2024), Kamb and Ganguli (2025), and Niedoba et al. (2025) have shown that assuming inductive biases toward locality and adaptivity to geometric structures leads to accurate quantitative predictions about the behavior of diffusion generative models. In other words, the universal performance similarity is traceable to a specific abstract property -- a form of geometric adaptivity -- that both transformers and U-Nets instantiate, perhaps through different architectural mechanisms but to the same functional effect.

This is exactly the kind of theoretical progress the paper is advocating for. The universal phenomenon -- architectural interchangeability -- identifies something that calls for explanation, and the explanation, when it arrives, operates at the right level of abstraction (geometric inductive biases) rather than at the level of specific architectural details.

---

### Universal Structure in Data

The second viewpoint on universality concerns not the models but the data they are trained on. Here the argument draws on a fundamental constraint: the no-free-lunch theorem.

> "The no-free-lunch theorem states that generalization on completely arbitrary data with a common learning strategy is not possible [Wolpert, 1996]. Therefore, deep learning must rely on particular features of the data present across all datasets and modalities on which it succeeds."

This is a logical constraint, not just an empirical observation. If deep learning generalizes across vision, language, speech, protein sequences, and games, there must be structural properties shared by all of these data types that the learning algorithm is exploiting. The question is what those properties are.

The paper points to several well-documented regularities:

**Power-law spectral properties.** Many classes of images and audio signals share power-law spectral properties: the energy of the signal as a function of spatial or temporal frequency decays as a power law rather than being flat or exponential. This is a strong and specific statistical regularity. It is not obvious a priori that natural images should have this property, but they do -- robustly across different categories, photographers, and imaging conditions. Audio signals, including speech, exhibit similar properties. This means that a single linear analysis tool -- wavelet bases -- can provide compact, efficient representations of both (Olshausen and Field, 1996; Mallat, 1999). A learning algorithm that implicitly or explicitly discovers wavelet-like features will automatically be well-suited to both modalities.

**Sparsity and multiscale structure.** Related to power-law spectra is sparsity: natural signals, when transformed into the right basis (such as wavelets), have most of their energy concentrated in a small fraction of coefficients. This sparsity is what makes compression algorithms like JPEG and MP3 work, and it is also what makes deep networks with hierarchical representations effective -- they can discard most of the raw signal and retain the part that is informationally relevant.

**Zipf's law in text.** For language data, the analogous regularity is Zipf's law: the frequency of words in natural text follows a power-law distribution. The most common word is roughly twice as common as the second most common, three times as common as the third, and so on. This law

> "holds over many natural and artificial languages [Li, 2002, Piantadosi, 2014]"

and is a very strong constraint on the statistical structure of text. It implies that language is neither maximally redundant (every word equally likely) nor maximally unpredictable (every word equally rare) -- it occupies a specific statistical regime. A language model that correctly captures this structure at the token level has already learned something non-trivial about the domain.

**Hierarchical and compositional structure.** Perhaps the most theoretically important shared property is that both images and text are amenable to hierarchical, compositional models. Images have pixels that group into edges, edges into textures, textures into parts, parts into objects. Text has characters that group into morphemes, morphemes into words, words into phrases, phrases into sentences, sentences into discourse. This shared hierarchical structure is not a coincidence -- it reflects the fact that both vision and language encode information about a structured physical and social world. Recent work (Cagnetta et al., 2024; Sclocchi et al., 2025; Cagnetta et al., 2025) has shown that this hierarchical compositional structure can sometimes be related through a common formal model across the two modalities.

The implication for theory is significant. These shared statistical properties are

> "a partial explanation for the ability of a single learning algorithm (say, a transformer trained with SGD) to tackle seemingly unrelated datasets, leaving only the finer-grained differences between them to be learned."

In other words, the transformer + SGD combination is not a magical universal solver -- it is a system that is well-matched to the specific statistical regularities that are common across natural data. Understanding those regularities theoretically is part of understanding why deep learning works. The universality across modalities is a clue pointing toward the relevant structural properties of data.

---

### Universality in Representations

The third and perhaps most striking form of universality goes inside the networks themselves: the internal representations learned by different networks tend to converge, even when the networks differ substantially in their architecture, initialization, training data, or objective.

#### The Basic Phenomenon

The observation that differently trained networks learn similar internal representations has been accumulated gradually over the past decade. Raghu et al. (2017) and Kornblith et al. (2019) established early quantitative methods for comparing representations across networks. The accumulating evidence shows convergence across multiple axes:

- **Random initializations:** Two networks with identical architecture and training procedure but different random seeds learn representations that are more similar to each other than chance would predict, and this similarity is computable and substantial.

- **Architecture variations:** Networks with different widths, depths, or architectural families (e.g., convolutional vs. fully-connected) can still learn representations that are measurably similar (Raghu et al., 2017; Kornblith et al., 2019; Bansal et al., 2021).

- **Training datasets:** Networks trained on different image datasets (e.g., ImageNet vs. Places-365) learn similar representations (Lenc and Vedaldi, 2015), even though the specific objects and scenes in the two datasets differ substantially.

- **Training objectives:** Networks trained with supervised objectives (cross-entropy on class labels) and self-supervised objectives (contrastive learning, masked autoencoding) learn similar representations (Bansal et al., 2021). This is particularly striking because the supervision signal is completely different in the two cases.

- **Modalities:** Networks trained on vision data and networks trained on language data learn representations that are surprisingly similar (Huh et al., 2024). This cross-modal convergence is perhaps the most surprising of all, since the input spaces are entirely different.

#### The Platonic Representation Hypothesis

The pattern across all these axes of variation points toward what Bansal et al. (2021) and Huh et al. (2024) call the "Platonic representation" hypothesis: there is a single, universal representation of reality toward which neural networks converge as they become larger and more capable.

> "this similarity grows as model size and performance increase, hinting that neural activations converge towards a universal ('Platonic') representation [Bansal et al., 2021, Huh et al., 2024]."

The name is apt: just as Plato's theory of forms posited that particular physical instances are imperfect reflections of universal ideal forms, the hypothesis posits that particular trained networks are imperfect approximations to a universal representation that is determined by the structure of the world (or more precisely, by the structure of the data distribution that reflects the world).

This hypothesis has a strong implication: if true, it means that studying any sufficiently large, well-trained network tells you something about this universal representation -- and therefore about the structure of the world that generated the data. The choice of specific architecture or training procedure becomes a detail, not a fundamental constraint.

#### Theoretical Grounding

Several theoretical results provide mechanistic grounding for the convergence phenomenon, at different levels of idealization:

**Random feature representations** (Rahimi and Recht, 2007; Guth et al., 2024): In simplified settings where the network's internal features are random (not learned), convergence of the kernel induced by those features follows from the law of large numbers. As the number of random features grows, the kernel concentrates around its expectation, making different random feature models increasingly similar to each other. This is a mathematically precise result that explains a limiting case.

**Deep linear networks** (Ziyin and Chuang, 2025): In networks where all nonlinearities are removed (a popular theoretical idealization), representational convergence can be proven to arise from the implicit regularization of SGD. The optimizer itself, independent of the specific loss landscape, drives different initializations toward the same solution. This is a cleaner statement than the random feature case because it involves learning rather than fixed random features.

**Identifiability theory** (Hyvärinen et al., 2024 and related work): A separate line of theory, coming from the study of independent component analysis and its nonlinear generalizations, has established conditions under which learned representations are provably unique (identifiable) -- meaning that any two models trained on the same data generating process must learn the same representation (up to trivial symmetries). Results have been established for unsupervised objectives (Klindt et al., 2020), self-supervised objectives (Zimmermann et al., 2021), and supervised objectives (Reizinger et al., 2024), under suitable assumptions on the data generating process (Reizinger et al., 2025). These identifiability results provide perhaps the strongest theoretical backing for representational convergence: they say that convergence is not merely an empirical tendency but a provable consequence of the objective and the data.

**Data structure as the origin** (Huh et al., 2024; Karkada et al., 2026): In more diverse settings, recent evidence suggests that the universality of representations ultimately traces its origins to the universal structure in data discussed in the previous section. The representations converge because the data distributions, despite appearing very different at the surface level, share deep statistical regularities. This connects the second and third viewpoints on universality: universal data structure drives universal representations.

#### Convergence at the Level of Individual Neurons

The convergence is not only at the level of global representational geometry. Several works have shown empirically that individual neurons in different networks can be matched to specific neurons in other networks:

> "Several works have also shown empirically that this similarity can extend to the level of individual neurons [Li et al., 2015, Dravid et al., 2023, Khosla et al., 2024]."

This is a stronger claim: not only do the overall representation spaces align, but the specific features computed by individual units are replicable. Different networks, trained independently, discover the same individual features -- curve detectors, frequency-selective cells, multimodal neurons. This is a striking form of reproducibility that would be very difficult to explain if the representations were arbitrary or random.

#### Connection to Biological Neural Networks

The convergence of artificial network representations with biological neural representations is a separate but related thread that the paper acknowledges cautiously:

> "In some cases, similar representations have been found in both artificial neural networks and biological neural networks [Olshausen and Field, 1996, Yamins et al., 2014, McIntosh et al., 2016], though the extent of this correspondence remains controversial [Bowers et al., 2023]."

The early observation by Olshausen and Field (1996) that sparse coding of natural images produces Gabor-like filters -- similar to the simple cells found in primary visual cortex -- was one of the first hints that artificial and biological representations might converge. Yamins et al. (2014) extended this to deeper network layers and higher visual areas, showing that networks trained to classify objects develop intermediate representations that predict the responses of neurons in areas V4 and IT. McIntosh et al. (2016) showed similar alignment in the retina. These results suggest that the convergence is not just among artificial systems but extends to biological systems that evolved to process the same natural data distributions.

The paper is appropriately cautious here: the extent of the correspondence is contested (Bowers et al., 2023), and there are many ways in which artificial and biological visual systems differ. But the partial correspondence is at least consistent with the view that representation convergence is driven by data structure, since both artificial and biological systems are shaped by the statistics of natural images.

#### Caveats and Open Questions

The paper is careful to note that the universality of representations is not fully established:

> "it should be noted that the range of settings in which this convergence is observed, and its extent, are not fully known (see Open Direction 10). In particular, recent work has shown that this apparent convergence to universal representations depends crucially on the chosen comparison metric across similarities [Gröger et al., 2026]."

This is an important qualification. Representational similarity is not a primitive observable -- it is measured using specific metrics (centered kernel alignment, linear regression R², canonical correlation analysis, and others), and different metrics can give different answers. Gröger et al. (2026) show that the apparent universality depends on which metric is used, which raises the question of which metric, if any, captures the "true" similarity of representations. A growing literature is devoted to this question (Sucholutsky et al., 2023; Klabunde et al., 2025) and to identifying cases where different metrics agree (Harvey et al., 2024; Williams, 2024).

This is not a fatal objection to the universality thesis -- even if the extent of convergence depends on the metric, the qualitative phenomenon is real -- but it is a reminder that the phenomenon is not fully understood and that theoretical work remains to be done.

---

### What This Line of Evidence Establishes

The three viewpoints on universality -- in inductive biases, in data structure, and in representations -- converge on a common conclusion that the paper articulates directly:

> "If the mechanisms learned by large models are indeed universal, this is very encouraging for theory: behavior shared across many systems should depend primarily on the features common to all such systems, and thus admit a description simpler than any particular model in isolation."

This is the core logic connecting universality to the possibility of scientific theory. A description of behavior that is universal -- that holds across ConvNets and transformers, across vision and language, across supervised and self-supervised training -- cannot depend on the specifics of any one system. It must depend only on what those systems have in common. The theory that captures it will therefore be simpler, more general, and more explanatory than any account that is tied to a specific architecture or training procedure. This is exactly the situation in physics: the renormalization group description of critical phenomena is simpler and more general than any microscopic model of a specific material.

The second implication goes deeper still:

> "if the internal structure of trained neural networks primarily reflects the structure of data, then in studying neural networks we may ultimately be studying the structure of data and its generating processes."

If representations converge to a universal form that is determined by data structure, then a theory of learned representations is simultaneously a theory of natural data distributions. And since language data comes directly from humans expressing their thoughts, goals, and experiences:

> "since language data comes directly from humans, understanding its structure may teach us something new and fundamental about ourselves."

This is a remarkable claim to close the section with. It suggests that the project of developing a scientific theory of deep learning is not merely a technical enterprise aimed at understanding a class of algorithms -- it is potentially a window into the structure of human cognition and communication.

#### The Role of Universality in the Broader Argument

Within the structure of the paper's five lines of evidence, universality plays a specific logical role. The other lines of evidence establish that:

1. Empirical phenomena in deep learning have a definite structure (scaling laws, double descent, grokking, neural collapse).
2. Mathematical theory can make quantitative, falsifiable predictions about these phenomena.
3. Simplified settings (mean-field theory, infinite-width networks) exhibit the same phenomena as practical systems.
4. Training dynamics are ordered and predictable.

Universality (line 5) establishes that these phenomena are not accidents of particular experimental setups. The same phenomena appear across architectures, datasets, scales, and modalities. This is what justifies calling them fundamental phenomena of deep learning rather than artifacts of specific choices. It also identifies the right level of abstraction for a theory: not the level of specific architectural decisions, but the level of shared inductive biases, shared data structure, and shared representation geometry.

Together, the five lines of evidence make the case that deep learning is ready for the same kind of theoretical treatment that was eventually applied to thermodynamics, fluid mechanics, and critical phenomena -- a "learning mechanics" that captures the essential regularities of how learning systems behave, abstracted away from the details of any particular implementation.

---

### Key References in This Section

| Reference | Contribution |
|---|---|
| Wolpert (1996) | No-free-lunch theorem -- motivation for universal data structure |
| Olshausen and Field (1996) | Sparse coding, wavelet bases, connection to V1 simple cells |
| Mallat (1999) | Wavelet analysis of natural signals |
| Li (2002); Piantadosi (2014) | Zipf's law across natural and artificial languages |
| Lenc and Vedaldi (2015) | Representational similarity across ImageNet and Places-365 |
| Raghu et al. (2017) | Early quantitative methods for comparing network representations |
| Kornblith et al. (2019) | Centered kernel alignment for representational similarity |
| Yamins et al. (2014) | Alignment of CNN representations with primate visual cortex |
| McIntosh et al. (2016) | Alignment with retinal processing |
| Klindt et al. (2020) | Identifiability for unsupervised objectives |
| Zimmermann et al. (2021) | Identifiability for self-supervised objectives |
| Liu et al. (2022); Smith et al. (2023) | ConvNet vs. transformer parity in vision |
| Bansal et al. (2021) | Cross-objective representational convergence; Platonic hypothesis |
| Moschella et al. (2022) | Cross-architecture representational alignment |
| Rahimi and Recht (2007); Guth et al. (2024) | Convergence of random feature kernels |
| Cagnetta et al. (2024; 2025); Sclocchi et al. (2025) | Hierarchical compositional structure across images and text |
| Kadkhodaie et al. (2024); Kamb and Ganguli (2025); Niedoba et al. (2025) | Geometric inductive biases in diffusion models |
| Zhang et al. (2024) | Transformers and U-Nets generate identical images in diffusion |
| Huh et al. (2024) | Cross-modal representational convergence; Platonic representation hypothesis |
| Reizinger et al. (2024; 2025) | Identifiability for supervised objectives |
| Hyvärinen et al. (2024) | Identifiability theory overview |
| Bowers et al. (2023) | Critical perspective on ANN-brain correspondence |
| Li et al. (2015); Dravid et al. (2023); Khosla et al. (2024) | Individual neuron correspondence across networks |
| Sucholutsky et al. (2023); Klabunde et al. (2025) | Representational similarity metric comparison |
| Harvey et al. (2024); Williams (2024) | Unification of similarity metrics |
| Ziyin and Chuang (2025) | SGD implicit regularization drives convergence in deep linear networks |
| Karkada et al. (2026) | Data structure as origin of representational universality |
| Gröger et al. (2026) | Metric-dependence of apparent representational universality |
