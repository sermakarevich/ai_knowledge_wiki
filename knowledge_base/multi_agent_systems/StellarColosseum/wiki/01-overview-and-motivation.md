> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Stellar Colosseum: Overview and Motivation
**In one sentence:** Stellar Colosseum is a model-agnostic, many-agent harness that allocates inference across long-horizon mathematics and theoretical computer science research by exploring strategies, gating readiness, decomposing proofs into interdependent sections, and routing verifier feedback back to the affected parts.
## Key points
- Language models can produce plausible short proofs but remain unreliable on long-horizon research problems where progress depends on a sequence of uncertain, interdependent decisions.
- Colosseum is model-agnostic and organizes inference at two levels: a stage-level research workflow and within-stage parallel sampling plus synthesis (Figure 1).
- At the workflow level it explores alternative strategies before proof construction, uses a readiness gate to decide when a route is mature enough to decompose, represents the proof plan as interdependent section-level subproblems, and routes verifier findings back to the affected part of the argument.
- Within each stage it generates candidates in parallel, attacks them with targeted falsification, and combines candidates and their critiques into a single research artifact through overlapping random-sample tree aggregation.
- The workflow has been integrated into Google Antigravity's Teamwork framework as the Long Proof pattern [7].
- It builds on and substantially extends the parallel exploration and iterative verification architecture of Woodruff et al. [56], adding explicit stage control, dependency-aware proof construction, and critique-preserving aggregation.
- Demonstrated with Gemini 3.1 Pro (plus Gemini 3.7 Flash on TCS-Bench): several new results on open problems from FOCS and JMLR papers, 71.0% accuracy on TCS-Bench, and 218 of 222 solved in a Codeforces evaluation with execution feedback.
---
## Abstract: what Colosseum is
**Covers:** Title block, authors, arXiv:2609.15983v2 [cs.AI] 15 Sep 2026, Abstract

Paper: "Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science" by Honghao Lin*, David P. Woodruff*, Yuan Deng, Jieming Mao, Song Zuo, Vahab Mirrokni (Google Research; Woodruff also Carnegie Mellon University; * co-first authors).

Verbatim core claim from the abstract:

> "We introduce Stellar Colosseum, a model-agnostic harness for allocating inference across research in mathematics and theoretical computer science."

Mechanisms named in the abstract, in order:

1. Explores alternative strategies before proof construction.
2. Uses a readiness gate to decide when a route is mature enough to decompose.
3. Represents the proof plan as interdependent section-level subproblems.
4. Routes verifier findings back to the affected part of the argument.
5. Across stages: generates candidates in parallel, attacks them with targeted falsification, and combines candidates and critiques via "overlapping random-sample tree aggregation."

Integration fact: "The Colosseum workflow has been integrated into Google Antigravity's Teamwork framework as the Long Proof pattern [7]."

Reported results (abstract):

| Evaluation | Result as stated |
|---|---|
| Open-ended research with Gemini 3.1 Pro | Several new results addressing open problems from papers published at venues such as FOCS and JMLR |
| TCS-Bench [15] (research-level theorem proving from FOCS, STOC, SODA papers) | 71.0% accuracy using Gemini 3.1 Pro and Gemini 3.7 Flash |
| Codeforces, proof-oriented pipeline with execution feedback, Gemini 3.1 Pro | Solves 218 of 222 problems |

## Introduction: why long-horizon research needs a harness
**Covers:** Section 1 Introduction (opening through two-level organization statement), Figure 1

Context: language models have made substantial progress in mathematical reasoning, including olympiad-level problems [52, 29], and recent studies describe new mathematics and TCS results obtained with their help [21, 56].

Research workflow as described: work often starts with literature search and small examples; researchers try several representations and conjectures before finding lemmas worth proving; even a promising approach can fail if a key lemma is false or a later step exposes a missing assumption; as the proof grows, definitions and assumptions must stay consistent across dependent lemmas; changing one part may alter what later sections must establish; a failed approach may still yield a useful restriction, counterexample, or alternative formulation.

Decision problem stated: "Progress depends on deciding what to develop, what to repair, and when to change direction, using the evidence gathered along the way."

On inference-time scaling: more opportunities to explore solutions and check them; sampling multiple reasoning paths, searching over intermediate states, and iteratively critiquing an answer can improve reasoning quality [55, 60, 44]. Limitation stated: "Agreement among candidates can still hide a shared error, so a flat vote over final answers offers limited guidance for proofs." The stated challenge: "use this computation to choose between approaches, uncover specific gaps, and preserve what remains useful after an attempt fails."

System statement: "We introduce Stellar Colosseum (Colosseum for short), a model-agnostic system for long-horizon research in mathematics and theoretical computer science." It keeps track of proposed strategies, partial proofs, and verification findings as shared research state, so exploration, proof construction, and revision build on one another.

Architecture (Figure 1):

- Panel (a), Stage-Level Research Workflow, five stages: Stage 1 Strategy Exploration ("Develops and challenges research routes"), Stage 2 Readiness Gate ("Decides whether a route supports a proof plan"), Stage 3 Proof Decomposition ("Builds a sectioned dependency graph"), Stage 4 Subproblem Solving (Section 1 … Section k, Section 2), Stage 5 Global Verification ("Evaluates the assembled proof as a whole"), with loops for local retry, revise / re-verify ("Patch sections or outline"), re-explore, and continue exploring.
- Panel (b), Within-Stage Sampling and Synthesis: "Each synthesis node aggregates a random subset of candidates and their associated critiques", e.g. S1: 1,2,3 → Synth. A1; S2: 3,4,5 → Synth. A2; S3: 4,5,6 → Synth. A3; S4: 6,7,8 → Synth. A4; then T1: A1,A2,A3 → Synth. B1; T2: A2,A3,A4 → Synth. B2; then R: B1,B2 → Stage Output; each synthesis paired with a falsifier; side store of Shared Research Knowledge: prior attempts and feedback, knowledge directory, pitfalls and objections.
