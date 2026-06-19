# From AGI to ASI

**Paper:** [From AGI to ASI (Genewein, Franklin, Lerchner, Orseau, Albanie et al., 2026)](https://arxiv.org/abs/2606.12683)

## Human Readable TL;DR

Imagine a ladder of intelligence: today's AI is near the bottom, a typical human is somewhere in the middle, and at the top is a hypothetical AI that is smarter than all of humanity combined. Most discussions stop at "human-level AI" -- this report asks: what happens on the rungs above that? The authors map out four plausible routes to the top (keep making AI bigger, invent a totally new type of AI, let AI improve itself, or have millions of AIs cooperate like a super-organization) and six things that could stop the climb (running out of training data, too much energy, current AI designs hitting a wall, research getting too hard, AI being fundamentally unable to form genuinely new ideas, or governments deliberately hitting the brakes). The honest conclusion: nobody knows which route wins or whether any bottleneck is fatal -- but we need a lot more science to find out.

## TL;DR

Google DeepMind researchers formally characterize the post-AGI intelligence spectrum -- AGI (median human cognitive performance), ASI (outperforms large expert collectives across all domains), and Universal AI (the theoretically optimal AIXI agent as an upper bound) -- and analyze what it would take to traverse from one to the next. They enumerate four non-mutually-exclusive pathways (scaling compute/data, algorithmic paradigm shifts, recursive self-improvement, multi-agent collective formation) and six potential bottlenecks (data wall, resource demands, neural paradigm insufficiency, research difficulty growth, the "abstraction barrier," deliberate governance slowdown). Each bottleneck has potential counteracting factors, making their impact an open empirical question, and the paper closes with a 30+ item research agenda to quantify these uncertainties.

---

## Problem & Motivation

The past decade has moved AGI from science fiction to a concrete near-term target for major AI organizations. Yet essentially all serious analysis stops at the AGI horizon -- there is no structured framework for reasoning about what AI capability growth looks like *after* human parity. Extrapolations of compute growth (~10x effective compute per year combining hardware gains, investment, and algorithmic efficiency) suggest the post-AGI era may arrive soon and could itself be highly dynamic. Without a principled taxonomy of pathways and bottlenecks, researchers and policymakers are left with either naive extrapolation or pure speculation. This paper attempts to replace speculation with a structured, falsifiable research agenda.

---

## Main Original Ideas

1. **Three-tier intelligence taxonomy** -- The paper formally distinguishes AGI (roughly median individual human today), ASI (surpasses large well-coordinated human-expert collectives on virtually all tasks), and Universal AI / AIXI (the incomputable theoretical maximum defined by the Legg-Hutter score). The hierarchy is grounded in algorithmic information theory rather than informal intuition, providing a stable reference frame for discussing capability jumps.

2. **Four technological pathways to ASI** -- Rather than treating the AGI-to-ASI transition as a single event, the paper decomposes it into four independent (and composable) mechanisms: (i) continued scaling of compute, models, and data; (ii) algorithmic paradigm shifts that depart from pretraining+transformers; (iii) recursive self-improvement where AI accelerates AI R&D (analogized to genetic, cultural, and cooperative evolution); and (iv) superintelligence emerging from large multi-agent collectives or "virtual agent economies."

3. **Six structured bottlenecks** -- The paper catalogs the six most plausible brakes on AGI-to-ASI progress: the data wall (exhaustion of high-quality human-generated text), unsustainable economic/energy resource demands, neural paradigm insufficiency (hallucinations, robustness failures, reasoning limits), research compounding difficulty, the "abstraction barrier" (AI trained on human concepts may be fundamentally unable to form radically novel ones), and deliberate governance slowdowns. Each bottleneck is paired with candidate counteracting factors -- making the net effect an empirical question, not a foregone conclusion.

4. **Digital intelligence (dis)advantages table** -- The paper systematically enumerates where digital intelligence is categorically superior to biological (I/O speed, internal processing speed, lossless replication, high-bandwidth experience sharing, substrate independence) and where hard limits apply (speed of light, energy costs, real-time physical interaction, P vs. NP complexity, Gödelian incompleteness). This prevents both over- and under-estimation of ASI potential.

5. **Explosive growth is not ruled out** -- The report explicitly argues that the canonical "single transformative step change" narrative (AGI arrives, world changes once) may be wrong. Recursive improvement dynamics, if they activate, could produce a series of rapid compounding societal transformations rather than one discrete event, requiring governance frameworks designed for continuous, fast-moving change rather than a single threshold.

---

## Key Findings

| Aspect | Conclusion |
|--------|------------|
| **Effective compute growth** | ~10x per year (hardware + investment + algorithmic efficiency combined) |
| **ASI definition** | Outperforms large, well-coordinated human expert collectives on virtually all tasks |
| **UAI / AIXI** | Incomputable but serves as a formal upper bound; all practical ASIs are approximations from below |
| **Bottleneck severity** | All six bottlenecks have plausible counteracting forces; none is definitively fatal |
| **Pathway exclusivity** | All four pathways are non-mutually-exclusive; multiple could operate simultaneously |
| **Societal implication** | A series of compounding transformations is more likely than one discrete AGI step-change |

- Digital intelligence advantages amplify with scale: speed (orders of magnitude faster I/O and processing), lossless replication, and high-bandwidth weight/experience sharing have no biological equivalent.
- Fundamental limits (speed of light, energy, P≠NP, Gödel) mean ASI will not be omniscient or omnipotent even at the AIXI theoretical maximum.
- The "abstraction barrier" is identified as a novel and potentially decisive bottleneck: if AI systems are primarily trained on human abstractions, they may be limited to recombining human concepts rather than forming genuinely new ones.
- Benchmark stitching (converting heterogeneous performance metrics to a common scale via Rosetta Stone approaches) is highlighted as the key methodological enabler for quantitative forecasting of AGI-to-ASI progress.

---

## Suggestions & Future Directions

1. **Quantitative bottleneck forecasting** -- Develop rigorous empirical methods to measure the magnitude and timeline of each bottleneck (especially data wall and resource demand) rather than relying on qualitative arguments.
2. **ASI benchmarking infrastructure** -- Design benchmarks that can meaningfully measure capability beyond human level, including "benchmark stitching" approaches that remain valid as AI surpasses human baselines.
3. **Recursive improvement dynamics** -- Formalize and empirically study the feedback loops by which AI accelerates AI R&D; measure current rates of AI-assisted algorithmic efficiency gain.
4. **Multi-agent scaling laws** -- Establish whether collective intelligence of N AGI agents scales super-linearly, linearly, or sub-linearly with N, and identify the coordination mechanisms that determine this.
5. **Abstraction barrier characterization** -- Test whether current and near-future AI systems are genuinely limited to human-seeded concept spaces or can spontaneously form novel abstractions from raw interaction data.
6. **Governance and deliberate slowdown modeling** -- Model socio-political feedback loops between AI capability growth, public trust, and regulatory intervention to forecast plausible governance-driven trajectory changes.
7. **Massively interdisciplinary global effort** -- The paper explicitly calls for economists, sociologists, ethicists, AI scientists, and policymakers to collaborate on preparing societal infrastructure for a potentially rapid succession of transformative AI-enabled breakthroughs.

---

## Authors & Institutions

Tim Genewein (Google DeepMind), Matija Franklin (Google DeepMind), Alexander Lerchner (Google DeepMind), Laurent Orseau (Google DeepMind), Samuel Albanie (Google DeepMind), Adam Bales (Google DeepMind), Cole Wyeth (Google DeepMind / University of Waterloo), Stephanie Chan (Google DeepMind), Iason Gabriel (Google DeepMind), Joel Z. Leibo (Google DeepMind), Allan Dafoe (Google DeepMind), Marcus Hutter (Google DeepMind / Australian National University), Thore Graepel (Google DeepMind / University College London), Shane Legg (Google DeepMind)
