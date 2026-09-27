# Evaluation & Benchmarks

Benchmarks, evaluation methodologies, verifiers, and empirical head-to-head comparisons of LLMs and agent systems.

## Papers

- [[AskEarlyAskLateAskRight/summary]] — Forced-injection framework across 3 benchmarks/4 models shows clarification value decays dimension-specifically: goal-clarification window closes by 10% trajectory, input by ~50%; no frontier model asks within the optimal window.

## Tutorials

- [[tutorials/evals/index|evals]] — How to measure whether an LLM app actually works: product evals (error analysis, code-graded checks, LLM-as-judge + human alignment, statistics with error bars, RAG metrics, hallucination detectors, agent evals) and model benchmarks (GSM8K, IFEval, prompt sensitivity), all run locally on one helpdesk app and public human-labeled sets, with every result in one table.
- [[tutorials/jev/index|jev]] — TypeSafe **Jev**, a "System One" model that answers typed questions (Choice / Score / Noul) with probabilities instead of text: notebook with the docs' basic examples, confidence-routing / composite-scoring / fan-out patterns, and an advanced section that scores `~/git/fleet`'s architecture, ranks an improvement backlog and scans all source files against fleet's own ADR rules.
