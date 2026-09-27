> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — Framing and Proposal
**In one sentence:** Iterative harness-level recursive self-improvement overfits its evolve set, so RRSI regularizes candidate proposal and selection to favor reusable mechanisms, gaining up to 14.1 points in-distribution and up to 4.7 points on five out-of-distribution benchmarks while using 30% fewer policy tokens.
## Key points
- An LLM agent's capability is largely magnified by its harness: the prompts, control flow, tooling, memory, and context management surrounding the frozen backbone model.
- Recent methods automate harness engineering by iteratively proposing and selecting component-wise edits, practically establishing recursive self-improvement (RSI) at the agent-system level.
- Such recursive evolution overfits by memorizing training tasks, showing large in-distribution gains that shrink or even vanish on out-of-distribution benchmarks.
- The RRSI proposer operates with a temporally annealed budget limiting how many edits a candidate can bundle, and encourages unexplored trajectories based on evolution history.
- The RRSI selector uses a critic that screens benchmark-specific proposals and a pruner that removes changes that are too small, too expensive, or no longer useful.
- Across eight benchmarks spanning coding, agentic workspace, and engineering design tasks, RRSI gains up to 14.1 points on the split it evolves against and up to 4.7 points on the five out-of-distribution benchmarks.
- The resulting harness runs on 30% fewer policy tokens than the unregularized evolution.
- Figure 1 shows prior methods retain little of their evolve-set gain on the agentic workspace benchmark and several end below H0, the initial harness, while RRSI generalizes the improvements.
---
## Paper header
Paper dated 2026-09-22: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses" by Peng Xia (1,2), Rujun Han (1), Zifeng Wang (1), Yanfei Chen (1), Yufan Zhang (1), Yoonho Lee (3), Chengsong Huang (4), Han Yu (1), Zhongying CuiZhu (1), Yifei Ming (1), Huaxiu Yao (2), Burak Gokturk (1), Tomas Pfister (1) and Chen-Yu Lee (1); affiliations: 1 Google Cloud AI Research, 2 UNC-Chapel Hill, 3 Stanford University, 4 Washington University in St. Louis; arXiv:2609.24972v1 [cs.LG] 21 Sep 2026.
## Abstract claim
> "An LLM agent's capability is largely magnified by its harness, namely the prompts, control flow, tooling, memory, and context management surrounding the frozen backbone model."
> "However, such recursive evolution may overfit by memorizing the training tasks, showing large in-distribution gains that shrink or even vanish on out-of-distribution benchmarks."
> "Together these constraints favor reusable agent mechanisms over benchmark-specific ones or even noises."
## 1. Introduction (opening)
- Modern LLM agents are systems rather than standalone models: a frozen backbone wrapped in a harness of prompts, control flow, tool interfaces, memory and context management.
- The harness decides whether the same model reads the right file before editing it, recovers from a failed command, manages efficient working context, and writes findings into deliverables; much recent agent-product progress came from harness engineering rather than new model weights.
- Manual harness engineering relies on humans inspecting failed trajectories and tweaking the scaffold by hand, so progress is limited by how many trajectories an engineer can read.
- Automated loop uses LLMs to optimize harness components from task feedback, giving a practical RSI at the agent-system level "where feedback from the current system is used to improve the harness that shapes its subsequent behavior."
- Test-time harness evolution "repeatedly proposes and selects edits using feedback from a finite evolve set, creating an adaptive overfitting risk: evolve-set performance may improve without corresponding gains on unseen tasks"; recent studies show substantial evolution vs held-out gaps and that apparent improvements can arise from task-specific fitting.
## Figure 1
Caption verbatim: "Figure 1 | Evolution overfits on the split it is scored on whereas RRSI generalizes the improvements. (a) Gains on the evolve split against gains out of distribution for the agentic workspace benchmark. Prior methods retain little of their evolve-set gain and several end below H0, the initial harness. (b-d) Out-of-distribution held-out score for H0, average of the four baseline methods and our RRSI on SWE-bench Verified, the mean of JobBench, GDPval and APEX-Agents, and Frontier-Eng." Figure panels (b-d) themselves are garbled/unreadable in this chunk extraction, so no panel numbers are quoted.
**Covers:** 2026-09-22 paper header + abstract + Section 1 Introduction opening + Figure 1 caption
