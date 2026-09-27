[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Adaptive Inference Allocation. The current configurations
**In one sentence:** Current runs fix population widths, aggregation fan-in, and sample counts up front even though the value of extra samples or rounds varies, so future work proposes an adaptive controller driven by workflow signals with compute-matched evaluation, plus using validated research trajectories as post-training data despite a credit-assignment challenge.
## Key points
- Current configurations fix population widths, aggregation fan-in, and sample counts before a run begins.
- The value of an additional sample or round varies across stages and subproblems, so fixed allocation can be inefficient.
- A future controller could reuse signals already produced by the workflow: strategy diversity, unresolved objections, repeated local failures, and agreement among independently generated candidates.
- The controller would expand uncertain branches, grant additional retries to unstable sections, and stop stages whose outputs have stabilized.
- Compute-matched evaluation would be needed to distinguish improved allocation from simply using more inference.
- The harness records structured research trajectories rather than only final answers: candidate strategies, falsifier critiques, aggregation decisions, dependency graphs, intermediate drafts, and revision histories.
- A natural direction is to use trajectories from runs with externally validated outcomes as post-training data, where intermediate states supervise strategy selection, decomposition, objection handling, and revision, while rejected routes and verifier feedback supply negative and corrective signals, distilling inference-time orchestration into the base model and improving the starting point for later runs.
- The main challenge is credit assignment, since a successful final result does not reveal which intermediate strategies, critiques, or revisions caused progress; the harness branching structure may help by comparing candidates sharing the same context but leading to different downstream outcomes.
---
## Adaptive inference allocation
**Covers:** Adaptive Inference Allocation section (p. 16)

> "Adaptive Inference Allocation. The current configurations fix population widths, aggregation fan-in, and sample counts before a run begins."

> "The value of an additional sample or round, however, can vary across stages and subproblems."

Proposed controller inputs already produced by the workflow:
- strategy diversity
- unresolved objections
- repeated local failures
- agreement among independently generated candidates

Proposed controller actions:
- expand uncertain branches
- grant additional retries to unstable sections
- stop stages whose outputs have stabilized

> "Compute-matched evaluation would be needed to distinguish improved allocation from simply using more inference."

## Learning from research trajectories
**Covers:** Section 8.2 (pp. 16-17)

> "The harness records structured research trajectories rather than only final answers: candidate strategies, falsifier critiques, aggregation decisions, dependency graphs, intermediate drafts, and revision histories."

> "A natural direction is to use trajectories from runs with externally validated outcomes as post-training data for the base model."

- Intermediate states could provide supervision for strategy selection, decomposition, objection handling, and revision.
- Rejected routes and verifier feedback could supply negative and corrective signals.
- Goal: distill some benefits of inference-time orchestration into the underlying model and improve the starting point for later runs.

> "The main challenge is credit assignment: a successful final result does not by itself reveal which intermediate strategies, critiques, or revisions were responsible for progress."

> "The branching structure of the harness may help identify useful training signals by comparing candidates that share the same context but lead to different downstream outcomes."
**Covers:** Adaptive Inference Allocation through Section 8.2 (pp. 16-17); references [1]-[40] tail in chunk not summarized
