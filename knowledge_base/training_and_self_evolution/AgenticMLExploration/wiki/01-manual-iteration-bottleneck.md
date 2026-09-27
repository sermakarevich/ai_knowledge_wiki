> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The Manual ML-Iteration Bottleneck
**In one sentence:** Industrial ads ranking progress is limited mainly by how fast human engineers can complete full machine learning (ML) iteration cycles, not by model capacity or training compute.

## Key points
- A single end-to-end iteration on one ranking model takes days to weeks of senior engineer attention per model, stated in the paper as a qualitative range with no exact distribution given.
- A typical industrial ads ranking stack contains dozens of differentiated models, each with its own objective such as click, conversion, or view, plus its own surface, ad segment, training data, feature set, architecture, and infrastructure constraints.
- Because the engineering pool is finite, only a small subset of possible model-by-technique combinations is ever tried, so the long tail of models gets little exploration even when a proven technique already works on a neighboring model.
- Manual iteration has six phases: ideation and hypothesis generation, prioritization of candidates, implementation, training and failure recovery, evaluation triage, and proposal preparation.
- Automated machine learning (AutoML) and neural architecture search (NAS) do not solve this bottleneck because they search a narrow, well-defined space for a single objective, while real ads work needs open-ended code-level changes judged on metric gain, infrastructure feasibility, statistical significance, and launch quality together.
- Data-science agents built for Kaggle-style academic benchmarks do not solve this either because they optimize a leaderboard score on small datasets, while industrial work requires costly training on large datasets and small incremental gains on top of mature baselines with statistical rigor.
- Agentic ML Exploration (A-MLE) reframes the unit of optimization from improving one model architecture to improving the iteration loop itself, using an agent to carry hypotheses through planning, execution, analysis, and shared knowledge while humans act as reviewers at stage boundaries.

---
## Introduction
Industrial ads ranking is not one model. It is a portfolio of dozens of differentiated models. Each model is built for a different goal, surface, or ad segment, and each has different data, features, architecture, and infrastructure limits.

Because of this variety, moving a working idea from one model to another is surprisingly expensive. Code must be adapted, training must be rerun, and downstream users must not be broken.

The paper argues that progress is therefore controlled less by brilliant single-model ideas and more by iteration throughput: how many complete try-train-evaluate cycles the team can finish per month. Since every cycle costs days to weeks of senior engineer time per model — a qualitative estimate in the paper, not a measured average — a finite team can only test a small fraction of ideas. Proven techniques spread slowly and unevenly.

## Related work: AutoML and NAS
Automated machine learning (AutoML) means software that automates parts of model building, such as tuning settings or picking architectures. Neural architecture search (NAS) is a part of AutoML that automatically searches for good neural-network shapes.

Earlier work covered setting optimization, NAS, and end-to-end AutoML systems. These systems assume a fixed search space and one goal, for example best accuracy.

A-MLE differs in two ways. Its search space is open-ended: any code-level change to a complex ranking model. Its goal is composite: offline metric gain plus infrastructure feasibility, statistical significance, and whether the result is good enough to propose for launch.

## Related work: LLM agents and tool use
Large language model (LLM) means a large AI model trained on text and code that can follow instructions, write code, and use tools. Recent work shows LLMs with tools and feedback can do multi-step tasks, including code-generation agents that score well on software-engineering tests.

A-MLE extends this into ML engineering. Here the hard part is not only writing code. It is generating hypotheses, adapting training when runs fail, evaluating results, and picking high-value candidates under compute and infrastructure limits.

## Related work: ML engineering automation
Other agent projects target data science and end-to-end ML research. Most are tested on academic Kaggle-style benchmarks, meaning small public datasets where the winner is the highest leaderboard score.

A-MLE targets a different setting: many industry-scale models where each training run is expensive, datasets are large, and success means a small but reliable gain over a strong, mature baseline. The gate is statistical rigor and launch readiness, not just a higher leaderboard number.

## Related work: Ads ranking
Modern ads ranking uses cascaded multi-stage systems, meaning ads pass through several filtering and ranking stages with deep models at each stage. Recent progress includes self-supervised learning for sparse features, token-mixing architectures, and many embedding-based features.

A-MLE treats this literature as a menu of techniques to try. The agent's job is to decide which technique to test next on which model, given what has already been tried and what the evidence shows.

## The six manual phases and their per-phase bottlenecks
The paper lists six manual phases for one model iteration:

1. Ideation and hypothesis generation: the engineer reads papers, internal proposals, and training history to pick an idea. Bottleneck is how well the engineer knows both this specific model and the wider technique landscape.
2. Prioritization of candidates: the engineer decides which hypotheses deserve costly training runs and how many variants to try. Bottleneck is judging trade-offs between directions under a fixed training compute budget.
3. Implementation: the engineer writes or adapts code in a complex model codebase and training entry point. Bottleneck is codebase complexity and the difficulty of the technique, plus the need not to break other users.
4. Training and failure recovery: the engineer launches training on a shared compute pool, watches stability, and fixes failures. Bottleneck is infrastructure randomness, preemption by other jobs sharing the pool, data-pipeline incidents, and intermittent evaluation failures.
5. Evaluation triage: the engineer compares offline metrics against a moving baseline and breaks results down by ad and user segments. Bottleneck is metric variance and telling real improvement apart from baseline drift.
6. Proposal preparation: the engineer writes a proposal with experiment design, results, statistical analysis, and a launch recommendation. Bottleneck is the careful analysis and documentation needed for a launch decision.

All six phases need human judgment today, so delays add up.

## Why the portfolio math makes this the bottleneck
One iteration takes a multi-week span on one model — again a qualitative statement in the paper, not a precise measurement. Multiply that cost across a portfolio of dozens of models and many possible techniques.

The total number of model-by-technique pairs a team can explore in any period is therefore inherently small. Even if a technique is known to work somewhere, there is no time to port and validate it everywhere. That untested remainder is recoverable signal left on the table, especially in the long tail of models that rarely get expert attention. A-MLE is aimed directly at this gap: raise the number of cycles completed without adding engineers.

**Covers:** Paper Sections 1-3 (Abstract, Introduction, Related Work, The Manual ML Iteration Bottleneck).
