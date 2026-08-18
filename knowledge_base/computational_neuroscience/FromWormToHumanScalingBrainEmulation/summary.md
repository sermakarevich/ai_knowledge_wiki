# From Worm to Human: Scaling Brain Emulation

**Paper:** [From Worm to Human: Scaling Brain Emulation (Isaak Freeman, 2026)](https://pdf.isaak.net/scaling-emulations)

## Human Readable TL;DR

Imagine making a working copy of a brain inside a computer -- like a flight simulator, but for thinking. This thesis adds up everything we'd need (microscope photos of every wire, recordings of every neuron firing, and enormous computer power) and shows the numbers are surprisingly close to what big AI data centers already have. The author suggests we start with simple animals (a worm, a baby fish, a fruit fly) where we can actually finish the job, and use what we learn to climb the ladder toward mouse and eventually human brains. The total bill would land somewhere between the Human Genome Project and the Manhattan Project -- big, but not impossible.

## TL;DR

A monograph synthesizing progress across connectomics, functional imaging, neural simulation, and AI hardware into a single feasibility roadmap for whole-brain emulation. Under pessimistic assumptions, real-time human brain emulation needs ~6e20 FLOP/s, ~700 GB/GPU memory, and ~24 GB/s interconnect -- within one order of magnitude of mid-2020s AI clusters (4e20 FLOP/s, 180 GB/GPU). Cost-per-neuron in EM connectomics has fallen from ~$16,500 to ~$100 over a decade, and the complete adult fruit fly connectome (139,255 neurons) was finished in 2024. The paper proposes *C. elegans*, larval zebrafish, and *Drosophila* as the most compelling near-term targets, with a full human-scale program estimated at $5--50B over 10--25 years.

---

## Problem & Motivation

Neuroscience progresses far more slowly than software-based AI, while brain diseases affect over 3.4 billion people. No prior work translates progress in connectomics, functional imaging, simulation, and AI hardware into a unified, quantitative engineering roadmap. The thesis argues that whole-brain emulation could (a) accelerate neuroscience via fast in-silico experiments, (b) enable new treatments for brain disorders, (c) advance consciousness research, (d) provide a path to "aligned AI by construction" (an emulated human inherits human values), (e) enable longevity / digital continuity, and (f) inspire new AI architectures. The gap is the absence of a feasibility synthesis bridging four otherwise siloed fields.

---

## Main Original Ideas

1. **Cross-domain feasibility synthesis.** First monograph to translate progress across connectomics, functional imaging, neural simulation, and AI hardware into common quantitative units (FLOP/s, GB/GPU, GB/s bandwidth), exposing interdependencies and bottlenecks across fields that rarely talk to each other.

2. **Fermi estimates for whole-brain hardware requirements.** Derives concrete lower and upper bounds: LIF neurons fit on a single H100-class GPU (~3.4 PFLOP/s), while a Hodgkin-Huxley model with 1,000 compartments per neuron requires ~6e20 FLOP/s -- comparable to a 100,000-GPU AI cluster.

3. **Organism ladder ("from worm to human").** Identifies *C. elegans*, larval zebrafish, and *Drosophila* as the most compelling near-term end-to-end targets, with larval zebrafish singled out as the strongest vertebrate validation platform combining structural, functional, and behavioral data.

4. **Benchmarking framework for emulation quality.** Proposes a multi-tier taxonomy (deterministic metrics, stochastic distribution matching, behavioral metrics, benchmark suites) to evaluate brain emulations quantitatively against experimental observables -- analogous to CASP for protein folding.

5. **Cost trajectory analysis for connectomics.** Documents the >100x drop in cost-per-neuron (~$16,500 → ~$100) and identifies human proofreading (>90% of project budgets) as the dominant cost driver, with ML-based automation as the primary lever for further reduction.

6. **Mega-project scoping.** Estimates a full human-scale connectomics + simulation effort at $5--50B over 10--25 years -- between the Human Genome Project (~$5B) and Manhattan Project (~$30B), and far less than Apollo (~$257B).

---

## Key Findings

| Domain | Quantity | Value |
|--------|----------|-------|
| Connectomics cost | Per-neuron, recent (zebrafish larvae) | **~$100** (down from ~$16,500) |
| Connectomics scale | Fruit fly complete brain (2024) | 139,255 neurons, 54.5M synapses |
| Functional imaging | Larval zebrafish (ZAPBench) | >70,000 neurons at ~1 Hz |
| Functional imaging | Mouse cortex (light-beads microscopy) | **~1M neurons at 2 Hz** (13x prior SOTA) |
| Simulation scale | Lu et al. 2024, human-scale | 86B neurons on 14,012 GPUs (60--120x slower than real time) |
| Simulation scale | Yamazaki et al. 2021, cerebellum | ~68B neurons at 600x slower than real time |
| Hardware target (pessimistic) | Real-time human emulation | **~6e20 FLOP/s, ~700 GB/GPU, ~24 GB/s interconnect** |
| Hardware available (mid-2020s) | AI cluster | 4e20 FLOP/s, 180 GB/GPU, 1.8 TB/s interconnect |
| Storage | Human brain raw at 10 nm isotropic | ~1.4 zettabytes (compressible ~128x → 10--100 PB) |

- **Connectome-only Drosophila LIF simulations** (Shiu et al., 2024) reproduced circuit-level feeding and grooming behaviors validated in vivo, using ground-truth wiring with no molecular data -- evidence that minimal connectome data can partially reproduce behavior.
- ***C. elegans* model** (Creamer et al., 2024): connectome-constrained linear model fit to whole-brain recordings achieved relative correlations up to 0.92 for held-out neurons.
- **The binding bottleneck is memory and interconnect, not compute.** Over 20 years, FLOPS improved ~60,000x while DRAM bandwidth grew only ~100x and interconnect bandwidth ~30x.
- **Proofreading dominates connectomics cost** (>90% of project budgets); ML automation is the single largest future cost-reduction lever.

---

## Suggestions & Future Directions

1. **Standardized benchmark competitions** for brain emulation, analogous to CASP for protein folding, to make "how good is our simulation?" empirically answerable.
2. **Scale functional datasets** in *C. elegans* and larval zebrafish to pair with completed or near-complete connectomes.
3. **AI-assisted automated proofreading pipelines** as the primary cost-reduction lever for moving beyond *Drosophila*-scale connectomes (mouse is ~1,000x larger; *Drosophila* alone consumed 33 person-years of proofreading).
4. **Scale expansion microscopy and molecular labeling** to close the molecular-data gap -- connectomes capture wiring but not receptor types, ion channel densities, or neuromodulator concentrations.
5. **Investigate the "glass ceiling" of optical imaging.** Single-neuron functional imaging beyond ~1--2 mm depth is currently impossible in mammals; adult mouse, monkey, and human brains require new modalities.
6. **Empirically determine the minimum structural vs. functional data** required for accurate emulation -- the field's central open question.
7. **Settle "emulation in the strong sense":** whether connectome-based simulations reproduce functional dynamics and emergent properties, not just connectivity.
8. **Sustained mega-project investment of $5--50B** over 10--25 years to reach human-scale capability.

Acknowledged limitations: the thesis explicitly excludes non-connectomics emulation paradigms, X-ray microscopy and other emerging modalities, structure-to-function inference methods, and the ethical / legal / philosophical dimensions of creating digital minds.

---

## Authors & Institutions

Isaak Freeman (MIT Program in Media Arts and Sciences, School of Architecture and Planning; B.A. Applied Mathematics/Neuroscience, UC Berkeley). Thesis supervisor: Edward S. Boyden (Y. Eva Tan Professor in Neurotechnology, MIT). Committee readers: Kevin M. Esvelt (Associate Professor of Media Arts and Sciences, MIT); George M. Church (Robert Winthrop Professor of Genetics, Harvard Medical School). Master of Science thesis, submitted January 23, 2026; March 2026.
