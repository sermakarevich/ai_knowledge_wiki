# Neural Computers

**Paper:** [Neural Computers (Zhuge, Zhao, Liu, Zhou, et al., 2025)](https://arxiv.org/abs/2604.06425)

## Human Readable TL;DR

Imagine if instead of running software on a traditional computer with a processor, memory, and screen as separate parts, you could train a single "brain" that handles all three at once -- computing, remembering, and displaying -- just by watching recordings of people using computers. That's what this paper proposes: a "Neural Computer" that learns to simulate interactive computer interfaces (terminals and desktops) purely from video recordings of screen activity. It works surprisingly well for rendering what things look like, but still struggles with actual math and logic -- it can mimic the appearance of computing better than the substance.

## TL;DR

This paper introduces Neural Computers (NCs) -- neural systems that unify computation, memory, and I/O into a single learned runtime state, instantiated as video generation models. Two prototypes are built: NC_CLIGen for terminal interfaces and NC_GUIWorld for GUI desktop environments, both trained solely on I/O trace data. Results show strong rendering fidelity (PSNR 40.77 dB for CLI) and cursor control accuracy (98.7% with explicit visual supervision), but native symbolic reasoning remains weak (4% arithmetic accuracy), revealing that current video models learn interface "physics" far better than computational logic.

---

## Problem & Motivation

Current AI systems separate computation, memory, and I/O across different subsystems: conventional computers rely on explicit programs, AI agents delegate execution to external environments, and world models merely predict dynamics without acting. No existing paradigm internalizes all three functions within a single neural system. The authors ask whether a single set of weights can learn to serve as the computer itself -- updating an internal runtime state from user inputs and rendering coherent outputs -- purely by observing input/output traces of interactive computing sessions, without access to internal program state.

---

## Main Original Ideas

1. **Neural Computer (NC) Formalism** -- A formal definition of NCs as learned latent-state systems described by an initial state h_0, an update function F_theta, and a decoder G_theta, where the model's latent state serves simultaneously as persistent memory, computation engine, and I/O pathway.

2. **Video-as-Runtime Instantiation** -- Implementing NC prototypes as video generation models (built on Wan2.1 diffusion transformers) where video latents z_t realize the runtime state, screen frames are observations, and user actions are conditioning inputs.

3. **NC_CLIGen Data Pipeline** -- A two-tier data engine: (a) general data from public asciinema recordings rendered into terminal frames, and (b) clean data from deterministic vhs-scripted Docker executions, with LLM-generated captions at multiple granularity levels serving as control channels.

4. **NC_GUIWorld Action Conditioning Architecture** -- A systematic study of four action injection strategies (external, contextual, residual, internal) and two encoding granularities (raw events vs. meta-actions), with explicit SVG cursor rendering and per-frame masks for visual supervision of cursor state.

5. **Completely Neural Computer (CNC) Roadmap** -- A vision for mature NCs characterized by Turing completeness, universal programmability, behavior consistency, and machine-native semantics operating directly on distributed representations.

---

## Key Findings

### CLI Results (NC_CLIGen)

| Metric | Value | Notes |
|---|---|---|
| **PSNR** | **40.77 dB** | At 13px font size |
| **SSIM** | **0.989** | High-fidelity terminal rendering |
| OCR Character Accuracy | 0.54 | Up from 0.03 at initialization |
| Exact Line Match | 0.31 | At 60k training steps |
| Arithmetic Accuracy (native) | 4% | Severe symbolic reasoning limitation |
| Arithmetic Accuracy (reprompted) | **83%** | Gains from specification, not reasoning |
| PSNR (semantic captions) | 21.90 dB | Baseline conditioning |
| PSNR (detailed captions) | **26.89 dB** | Literal captions significantly improve alignment |

### GUI Results (NC_GUIWorld)

| Metric | Best Model | Notes |
|---|---|---|
| **FVD** | **14.5** | Internal injection mode |
| **SSIM** | **0.863** | Internal injection, meta-action v2 |
| **LPIPS** | **0.138** | Residual injection |
| Cursor Accuracy (coordinates only) | 8.7--13.5% | Without visual supervision |
| Cursor Accuracy (SVG + masks) | **98.7%** | With explicit visual supervision |

### Key Qualitative Findings

- **Data quality over scale**: 110 hours of goal-directed trajectories outperformed 1,400 hours of random exploration across all metrics (FVD 14.72 vs. 20.37--48.17)
- **Deeper action injection wins**: Internal and residual injection modes consistently beat shallow external conditioning for post-action visual consistency
- **Reprompting exposes a ceiling**: The jump from 4% to 83% on arithmetic via reprompting shows the model faithfully renders conditioned content rather than performing actual computation
- **Global metrics plateau early**: PSNR/SSIM saturate around 25k steps on clean data, while character-level accuracy continues to improve

---

## Suggestions & Future Directions

1. **Robust Symbolic Processing** -- Current NCs fail at native arithmetic and logic; future work must develop mechanisms for reliable symbolic computation within the neural runtime, potentially through hybrid architectures or specialized training objectives.

2. **Stable Routine Reuse** -- CNCs require the ability to install, invoke, and compose learned routines that persist across tasks, moving beyond relearning capabilities each session toward compositional neural programs.

3. **Behavior Consistency and Runtime Governance** -- A clear separation between executing installed capabilities and explicitly updating them is needed for trust and reliability, possibly via gating mechanisms that distinguish "run mode" from "reprogram mode."

4. **Turing Completeness via Unbounded Memory** -- Achieving general computation requires progressively growing effective memory (model parameters or context), moving beyond the fixed-capacity latent states of current prototypes.

5. **Beyond Video Models** -- Future NCs should explore machine-native neural architectures optimized for reasoning and state manipulation rather than frame-level video generation, which imposes unnecessary visual rendering overhead.

6. **Leveraging the Data Advantage** -- Every digital interaction produces structured I/O traces; scaling NC training to this continuously generated data source could enable end-to-end learning of interface conventions and task semantics far beyond curated datasets.

---

## Authors & Institutions

Mingchen Zhuge, Changsheng Zhao, Haozhe Liu, Zijian Zhou, Shuming Liu, Ernie Chang, Gael Le Lan, Junjie Fei, Wenxuan Zhang, Zhipeng Cai, Zechun Liu, Yunyang Xiong, Yining Yang, Yuandong Tian, Yangyang Shi, Vikas Chandra (Meta AI); Wenyi Wang, Yasheng Sun, Jurgen Schmidhuber (KAUST)
