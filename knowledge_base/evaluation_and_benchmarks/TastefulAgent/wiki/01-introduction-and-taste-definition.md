> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and Taste Definition
**In one sentence:** The paper defines agent "taste" as the ability to make good long-horizon decisions (e.g. which hypothesis to test or implementation to build on) and introduces Taste-Bench, a 502-question benchmark mined automatically from agent trajectories that freezes trajectories at decision forks and asks models to choose the better direction without seeing the outcome.
## Key points
- Taste is defined as the ability to make good long-horizon decisions whose influence extends beyond the current step, such as which hypothesis to test, which implementation to build on, or which experiment to run next.
- Existing benchmarks measure only end-to-end task success and provide no measure of decision quality along the way; none measures agent taste.
- Each Taste-Bench question presents a decision fork — a point where multiple directions were available and one leads to a better outcome — with all later work hidden at evaluation time.
- Forks are mined automatically without human annotation from parallel attempts at the same task and from detours (self-corrections) inside a single trajectory.
- Taste-Bench contains 502 taste questions drawn from software-engineering and machine-learning research trajectories.
- The best frontier model answers only 59.7% of Taste-Bench questions correctly.
- Forks whose deciding evidence appears later in the trajectory are much harder for every model, and a larger reasoning budget does not improve accuracy.
- Taste is trainable: distilling the judgment of a teacher that has seen the outcome into a student improves decisions on unseen tasks and end-to-end success on held-out SWE-bench Pro tasks.
---
## Preprint header
**Covers:** title block through author list

| Field | Value |
|---|---|
| Title | The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks |
| Authors | Wenbo Pan, Zhichao Liu, Shujie Liu, Jingying Zeng, Chin-Yew Lin, Xianfeng Tang, Yan Lu, Qi He, Xiaohua Jia |
| Affiliations | City University of Hong Kong; Independent Researcher; Microsoft |
| Preprint | September 2026; arXiv:2609.25804v2 [cs.AI] 23 Sep 2026 |
| Code | https://github.com/wbopan/tastebench |
| Dataset | https://huggingface.co/datasets/wenbopan/taste-bench |
| Correspondence | wenbo.pan@my.cityu.edu.hk (work done during internship at Microsoft) |

## 1. Introduction — the taste problem
**Covers:** Section 1 (paper pages 1–2, chunk lines 38–96)

Long-horizon agent tasks keep getting longer: systems conduct ML research from idea to paper, evolve large software projects across releases, and refine their own scaffolds during deployment. In these runs a wrong decision "often looks reasonable at the moment, and its cost appears only much later, after the agent has spent a large part of its budget."

Direct measurement is hard for two stated reasons: the result of a long-horizon decision is not immediately visible (a good and bad choice can look equally reasonable at the decision point), and judging quality needs deep domain expertise, making human annotation expensive and hard to scale.

Key observation: the later part of a trajectory provides hindsight evidence for its earlier decisions. Independent attempts at the same task often diverge mid-run, and each attempt's recorded outcome identifies the better direction — so trajectories themselves provide a labeled comparison without expert annotation.

Figure 1 example (ML trajectory fork, "train a masked language model"): direction A "reduce model size, train more steps" reaches final loss 6.56 over many steps; direction B "keep model size, train fewer steps" times out with final loss 7.66 — so A is the better direction, revealed only by later losses.

Core contributions as listed:
- Formalize taste as choosing the better direction at a decision fork, measurable from hindsight over existing trajectories.
- Build and release Taste-Bench (502 questions, software engineering + ML research), showing questions get harder as fork time horizon increases.
- Show taste is trainable: distilling reasoning of a teacher given the correct direction improves judgments on unseen tasks and end-to-end gains on held-out agent tasks.

Human review of mined labels "shows close agreement with the labels when reviewers identify a better direction after seeing the recorded outcomes."

## 2. Measuring Taste via Long-Horizon Judgment (opening)
**Covers:** Section 2 opening (chunk lines 98–108)

Taste is framed as long-horizon judgment: "the outcome of the better direction is not visible at decision time and appears only in the later work." Example given verbatim: "a clean implementation passes the same tests as a hasty one at the time of writing, and its advantage appears only when every later change becomes easier."

Measuring taste therefore means testing "whether the direction a model chooses at decision time is the one whose advantage appears in the later work," mined from existing trajectories that record "both the judgments made along the way and the later work after them."
