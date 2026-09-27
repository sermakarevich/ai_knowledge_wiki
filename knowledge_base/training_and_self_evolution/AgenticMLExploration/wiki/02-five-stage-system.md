> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The Five-Stage A-MLE System
**In one sentence:** A single tool-using LLM (Large Language Model) agent orchestrates five stages over a shared skill library and sandboxed execution layer, with each session parameterized by a (model, objective, compute) triple and terminating in either a proposal or a documented null result.

## Key points
- A-MLE has five stages — hypothesis generation, exploration strategy, experiment execution, result analysis, and shared substrate — all driven by one tool-using agent.
- Each exploration session is parameterized by a (model, objective, compute) triple, which fixes what is being improved, what goal counts as success, and how much budget is available.
- Hypotheses are grounded in the live state of the model (current config, baseline metrics, and history of tried techniques) and scored by an LLM (Large Language Model) critic for novelty and feasibility.
- The exploration plan interleaves exploration (testing single hypotheses in isolation) with exploitation (combining the best candidates and pushing them harder), and the plan is negotiated with the user.
- Experiment execution runs as a sandboxed loop: edit code or config in a copy, typecheck and unit-test, build an image, run a short smoke test, launch full training, then monitor and retry or fix at code or config level.
- Result analysis compares against a rolling baseline rather than a frozen snapshot, decomposes metrics by segment to catch localized regressions, and auto re-runs jobs whose within-run variance is too high.
- The shared substrate is long-lived, versioned markdown (a simple text format) trees kept in source control, with eligibility annotations for matching techniques to similar models and Track Record write-back of new outcomes at session end.
- Every stage boundary is a HITL (human-in-the-loop) checkpoint where an engineer can approve, request changes, or stop the session, which limits the blast radius of any single bad agent decision.

---
## How the system fits together
A single agent walks the session from input to output. All stages read from and write to the same shared substrate below them, and results can loop back for another round of strategy.

![A-MLE orchestration: one agent walks four gated stages over a shared substrate, with multi-round feedback into strategy](images/fig1-orchestration.png)

The diagram shows Model+Objective+Compute input, Hypothesis Generation → Exploration Strategy → Experiment Execution → Result Analysis (each with an H checkpoint circle), Proposal/Null Result output, multi-round feedback arrow back into strategy, and all stages reading/writing the Shared Knowledge Substrate (Skill Library + Code-Execution Sandbox) bar below.

## 4.1 Hypothesis Generation
The agent starts by reading the live state of the model: recent training config, baseline metrics, and the rolling history of already-tried techniques. From this it proposes a small set of candidate techniques, each with an explicit reason why it fits the current model state. Candidates can come from internal generators such as model-state analyzers, training-efficiency analyzers, and recent-literature retrievers. An LLM (Large Language Model) critic then scores each idea for novelty and feasibility. Grounding in live state matters because a hypothesis that fit the old baseline often fails after a baseline refresh.

## 4.2 Exploration Strategy
Given the candidate set and limits on number of runs, total compute, or wall-clock time, the agent orders and plans the sequence of model iterations. Plans mix exploration (validating single hypotheses alone) with exploitation (combining the most promising ones and pushing them harder). The agent negotiates this plan with the user at the checkpoint, because the trade-off between an aggressive plan and compute cost should be an explicit, reviewed choice.

## 4.3 Experiment Execution
The agent works in a sandboxed copy of the codebase, meaning an isolated copy where mistakes cannot harm production code. The loop is: edit the training config or model architecture, run type checks and unit tests, build an image with the updated code, run a short smoke pass to verify it starts correctly, then submit the full training job. After submit, the agent monitors progress, tells infrastructure errors apart from genuine training divergence, and either retries, fixes code or config, or reports the run. Across a multi-experiment plan it adapts: if one branch proves infeasible, it reroutes remaining compute instead of abandoning the session.

## 4.4 Result Analysis
After each run, the agent checks statistical significance against a rolling baseline (a continuously updated reference, not a frozen snapshot that would drift out of date). It breaks metrics down by segment to surface localized regressions that an average would hide, and triggers an automatic re-run when within-run variance passes a threshold. At the end of a round it builds a structured leaderboard of candidates, then either feeds it back into the strategy stage for another round or assembles the final proposal.

## 4.5 Shared Substrate
Each session both reads from and writes to a shared, long-lived knowledge store. Knowledge gained on one model becomes usable on another model. In practice this is versioned markdown trees in source control, holding per-technique and per-model knowledge from the past. At session start, the agent matches the target model's context against structured eligibility annotations to surface techniques with prior evidence on architecturally similar models. At session end, new outcomes are committed back to the relevant Track Record, reviewable like any other source-control change.

## 4.6 Human-in-the-Loop Checkpoints
The agent acts on its own inside each stage, but every stage boundary is a checkpoint. Here a human engineer can approve continuation, ask for changes, or end the session. The split of labor is simple: the agent covers a wide search space fast, while the engineer reviews findings for edge cases and gaps using practical judgment about trade-offs. This structure limits the blast radius of any single agent mistake — for example a hallucinated (made-up) code change is caught before training launch, and a miscalibrated evaluation is caught before proposal writing.

## Skill library categories (Appendix A)
The skill library is the reusable half of the substrate: the shared collection of tools and how-to knowledge the agent draws on. Categories include model-state analyzers for reading current configs and metrics, training-efficiency analyzers for spotting compute or speed issues, and literature retrievers for pulling in recent external techniques. The code-execution sandbox is the other half: the isolated layer where edits, checks, builds, smoke tests, and training launches happen safely.

## Phase boundary conventions (Appendix B)
The convention is simple and uniform: four gated stages lead to one of two terminal outputs, and there is a checkpoint at every boundary. Each checkpoint offers the same three options — approve and continue, request modifications, or terminate. Feedback can flow forward through the gates or loop back over multiple rounds into strategy. A session always ends with a recorded artifact: either a proposal or a documented null result, so negative outcomes also enrich the substrate.

**Covers:** Paper Section 4 (4.1-4.6) plus Appendices A (skill library) and B (checkpoint conventions).
