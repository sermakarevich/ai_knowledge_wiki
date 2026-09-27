> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work: Long-Horizon Agents, Pre-Outcome Judgment, Process Evaluation, and Distillation
**In one sentence:** The paper positions Taste-Bench against four literatures — long-horizon agent benchmarks that test task completion rather than direction choice, pre-outcome idea judgment on standalone ideas rather than in-trajectory forks, process/step-level evaluation that scores steps or whole trajectories rather than outcome-labeled direction choice made blind, and distillation methods whose recipe it adapts — and concludes that taste is measurable from existing trajectories (502 questions), distillable into weights, and transferable to end-to-end success.
## Key points
- Long-horizon benchmarks (AgentBench [9]; SWE-bench and SWE-bench Pro [10, 11]; MLAgentBench and RE-Bench [12, 13]) test whether an agent completes a long task, whereas Taste-Bench tests whether the agent chooses the better direction inside the task.
- Prior work on judging research directions before outcomes — predicting which of two ideas performs better [33], preferring one of two ML solutions before executing them [34], choosing the better of two AI-safety proposals against expert ratings [35] — judges standalone ideas or solutions, whereas Taste-Bench judges forks inside executed trajectories carrying the agent's situation and recorded outcome labels.
- Judgments of ideas before execution often flip after execution [36], which motivates Taste-Bench's use of recorded trajectory outcomes as labels.
- Process supervision scores steps with human labels [37] or rollout outcomes from each step [38]; agent work has trained policies from explored-vs-expert trajectory preferences [39] and verified alternatives at critical steps [40], plus test-time process reward models scoring candidate actions [41] — while Taste-Bench instead labels the better direction with the outcome the trajectory later records and evaluates the model choosing before seeing it.
- Whole-trajectory judges (Agent-as-a-Judge, AgentRewardBench [42, 43]) and failure-attribution methods (Who&When, AgenTracer [44, 45], which models localize poorly) differ from Taste-Bench's blind, outcome-labeled direction choice.
- The distillation recipe follows SDPO [32] but replaces environment feedback with a demonstration of the supported candidate and samples targets from the teacher rather than the student [51], transferring in-context judgment into weights; advisor models similarly steer an executor with advice from a small trained model [52].
- The paper's conclusion restates the arc: taste (choosing the better direction before the outcome is visible) is measurable from existing trajectories; Taste-Bench has 502 outcome-labeled questions; distilling teacher reasoning given the supported candidate transfers to unseen tasks; injecting the student's judgment as advice improves end-to-end success.
---
## 6. Related Work — long-horizon agent evaluation
**Covers:** Section 6, paragraph 1 (chunk lines 5–9)

AgentBench evaluates multi-step interaction [9]; SWE-bench and SWE-bench Pro evaluate software agents on repository tasks [10, 11]; MLAgentBench and RE-Bench extend evaluation to ML experimentation and AI R&D [12, 13].

Positioning verbatim: "These benchmarks test whether an agent completes a long task, whereas Taste-Bench tests whether the agent chooses the better direction inside the task."

## 6. Related Work — judging research directions before the outcome
**Covers:** Section 6, paragraph 2 (chunk lines 11–17)

| Prior work | What it judges | Citation |
|---|---|---|
| Predicting which of two ideas performs better | Standalone ideas, before outcome known | [33] |
| Preferring one of two ML solutions before executing them | Standalone solutions, pre-execution | [34] |
| Choosing the better of two AI-safety research proposals against expert ratings | Standalone proposals, expert-rated | [35] |
| Ideation-execution gap: judgments before execution often flip after execution | Idea judgments vs execution outcomes | [36] |

Contrast verbatim: "These works judge standalone ideas or solutions, whereas Taste-Bench judges forks inside executed trajectories, so each question carries the situation of the agent and the recorded outcome labels it."

## 6. Related Work — process evaluation and step-level judgment
**Covers:** Section 6, paragraph 3 (chunk lines 19–26)

| Line of work | Mechanism | Citation |
|---|---|---|
| Process supervision | Score steps with human labels | [37] |
| Process supervision | Score steps with outcomes of rollouts from each step | [38] |
| Agent policy training | Preferences between explored and expert trajectories | [39] |
| Agent policy training | Verified alternatives at critical steps | [40] |
| Test-time scoring | Process reward model scores candidate actions | [41] |
| Whole-trajectory judging | Agent-as-a-Judge; AgentRewardBench | [42, 43] |
| Failure attribution | Who&When; AgenTracer attribute a failure to its decisive step, which models localize poorly | [44, 45] |

Taste-Bench difference verbatim: "Taste-Bench instead labels the better direction with the outcome the trajectory later records, and the evaluated model chooses before seeing it."

## 6. Related Work — distillation and internalizing context
**Covers:** Section 6, paragraph 4 (chunk lines 28–34)

| Method | Teacher / signal | Citation |
|---|---|---|
| Knowledge distillation | Student matches teacher's output distribution | [46] |
| Context distillation | Same model conditioned on extra context as teacher | [47, 48] |
| STaR | Same model with the correct answer | [49] |
| LEAP | Privileged state | [50] |
| SDPO | Environment feedback | [32] |

Own recipe verbatim: "Our recipe follows SDPO but replaces the feedback with a demonstration of the supported candidate and samples the targets from the teacher rather than from the student [51], so it transfers in-context judgment into the weights." Advisor models "similarly steer an executor with advice from a small trained model [52]."

## 7. Conclusion (as stated in this chunk)
**Covers:** Section 7 (chunk lines 36–43)

Verbatim core: "In this work, we study taste, the ability of an agent to choose the better direction before the outcome is visible. We show that this ability can be measured from existing trajectories, and we build Taste-Bench, a benchmark of 502 taste questions labeled by recorded outcomes."

Further verbatim: "Distilling the reasoning of a teacher given the supported candidate transfers judgment to questions from unseen tasks, and injecting the student's judgment as advice improves end-to-end success." Closing hope: "We hope Taste-Bench provides a practical basis for measuring and training the judgment of long-horizon agents."

## Reproducibility, ethics, and AI-use statements (as stated in this chunk)
**Covers:** statements block (chunk lines 45–67)

- Reproducibility: one fixed benchmark version; appendix specifies constructions, prompts, over-long-trajectory handling, and scoring; every figure generated directly from recorded results; every reported run complete over released questions; distillation runs fix base-model version, random seeds, fold splits, inference settings. Releases: benchmark at `https://huggingface.co/datasets/wenbopan/taste-bench`; evaluation code, protocol, and recorded results of every evaluated model at `https://github.com/wbopan/tastebench`.
- Ethics: benchmark consists of technical agent trajectories plus a separate human review collecting judgments from two reviewers; credential strings removed before sending trajectories to any model; measuring long-horizon judgment has dual-use risk; only aggregate capability results reported, no domain-specific harmful instructions.
- AI use: generative AI tools assisted with synthetic data generation, experimental and methodological design, method implementation, interpretation of results, translation, language editing, manuscript drafting, figure creation, code editing, and literature searches; authors take full responsibility; designs, conclusions, and artifacts are original contributions.
- References in this chunk span [1]–[37] (entries [38]+ are cut off mid-list at Lightman et al. "Let's verify step by step").

**Covers:** §6 Related Work through §7 Conclusion plus reproducibility/ethics/AI-use statements and references [1]–[37] (chunk 05/13, lines 1–203)
