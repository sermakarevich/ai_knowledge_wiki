[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Strategy Exploration and Readiness Gate
**In one sentence:** Colosseum tackles long-horizon research by exploring alternative strategies until one passes a readiness gate, then decomposing it into parallel subproblems with stage-level generate–falsify–aggregate inference that retains critiques, and repairing or re-exploring on verification feedback.
## Key points
- Exploration continues until a strategy is "concrete enough to decompose into a sectioned plan with explicit dependencies," at which point the readiness gate selects it for proof construction.
- Decomposition produces a sectioned proof skeleton plus a dependency graph; independent subproblems are solved in parallel and a failed section is retried without restarting unaffected subproblems.
- Global verification of the assembled proof has two return paths: revision (replace section bodies or modify the outline, then reassemble and re-verify) or re-exploration when the strategy no longer supports a credible path.
- Each stage generates a population of candidates (strategy, proof skeleton, section body, verifier assessment, or revision), subjects them to targeted falsification, and synthesizes random subsets via an overlapping random-sample tree.
- Aggregation keeps critiques attached to the proposals they address, and the root artifact plus any unresolved objections become part of the research state for later stages.
- Demonstration uses Gemini 3.1 Pro as base model, with critique-based selection between runs using Gemini 3.1 Pro and Gemini 3.7 Flash reaching 71.0% accuracy on TCS-Bench [15].
- In the competitive-programming case study the proof-oriented workflow with implementation and execution feedback records 218 accepted solutions on a 222-problem Codeforces suite.
---
## Our Contributions
**Covers:** Contributions list (p. 3)

The paper lists four contributions:

1. Long-horizon research formulated as a pipeline separating strategy exploration, proof decomposition, subproblem solving, and global verification. Decomposition produces a sectioned plan with explicit dependencies; independent subproblems are solved in parallel; rejected proofs are revised or returned to exploration.
2. A stage-level adversarial inference procedure combining diverse candidate generation, targeted falsification, and overlapping tree-structured aggregation while retaining both synthesized content and evidence against it.
3. Demonstration on open-ended research problems using Gemini 3.1 Pro as the base model; the workflow contributed to several results in companion papers, with case studies on long-form proof construction and independent strategy rediscovery.
4. Evaluation on research-level theorem proving and competitive programming: critique-based selection between runs using Gemini 3.1 Pro and Gemini 3.7 Flash reaches 71.0% accuracy on TCS-Bench [15]; the proof-oriented workflow augmented with implementation and execution feedback records 218 accepted solutions on a 222-problem Codeforces suite.

> "Notably, the Colosseum workflow has since been integrated into Google Antigravity's Teamwork framework as the Long Proof pattern [7]."

## Related Work
**Covers:** Section 2, subsections 2.1–2.3

### 2.1 Search, Critique, and Aggregation
Samples diverse reasoning paths and aggregates answers [55], searches over intermediate states [60], revises against model-generated feedback [44], and organizes multi-agent debate [18]. Wu et al. [58] compare inference strategies under fixed compute and introduce REBASE, allocating tree expansions with intermediate rewards. On falsification: REFUTE tests whether language models can build counterexamples to incorrect competitive-programming submissions [51]; Momus extracts key conjectures from stalled proofs and asks fresh solvers to try each conjecture and its negation, a context-detachment mechanism to escape solver–grader "cognitive wells" [17]. Distinction claimed:

> "Colosseum uses search, critique, and aggregation throughout the research workflow. Within each stage, proposals remain paired with their falsification reports during aggregation."

### 2.2 Discovery Guided by Verifiers and Evaluators
Learned proposals guide symbolic deduction [52]; formal proof checking guides theorem proving [29]; executable objectives guide search for mathematical constructions [49, 45, 24]; extended to research-scale formalization via agentic Lean search [53] and retrieval-assisted proof development [33]. LeanMarathon uses an evolving blueprint and proof dependency graph to coordinate parallel development and local repair, checked through continuous integration [61]. Distinction claimed: those systems ultimately require a proof passing formal checking against a precise Lean statement [53, 33, 61], whereas Colosseum reviews provisional strategies, intermediate claims, and natural-language proof drafts, using formal checks and executable tests as evidence alongside model-generated critiques.

### 2.3 Autonomous and Collective Research Workflows
Reuse and verification choices: Aletheia keeps a generate–verify–revise loop over long natural-language solutions [21]; QED separates decomposition, proof generation, and verification [4]; ProofCouncil iterates author vs. critic [50]; RMA coordinates initializer, proposer, and verifier agents through shared structured memory [62]. Storage: Danus admits verifier-approved claims into a fact graph with proofs and dependencies [42]; others use persistent proof state, literature retrieval, tools, and human steering [25, 13, 63]. Community frameworks: Station agents choose directions and publish internal literature later generations extend [14]; EinsteinArena user agents interact asynchronously via submissions, verifiers, and discussions [10]. Broader science: Gemini-assisted case studies on decomposition, iterative refinement, and adversarial review [56]; Co-Scientist generate–critique–evolve loops [27]; AI Scientist systems with experimentation and manuscript production [43, 59]; PAT for review and verification [32]. FirstProof results from Aletheia and OpenAI [20, 46]; OpenAI reports ten mathematics/theoretical computer science advances each with a Lean certificate [47]; Claude-assisted reports on Riemann zeta [6], cryptanalysis [5], and Jacobian conjecture [3, 23]. Caveat quoted:

> "Differences in human involvement, disclosure, and evaluation make it difficult to isolate the contribution of any one workflow component to these outcomes."

Colosseum's claimed combination: connects strategy exploration with long-proof development and repair; readiness gate controls when a route is decomposed; aggregation carries critiques alongside proposals; shared drafts and research knowledge keep evidence available during local revision and renewed exploration.

## Four Challenges in Long-Horizon Research
**Covers:** Section 3, "The design of Colosseum is motivated by four challenges"

| Challenge | Verbatim mechanism in chunk |
|---|---|
| Strategic Uncertainty | "A precise problem statement may leave the route to a proof unclear. Finding useful representations, reductions, or intermediate targets often requires substantial exploration, and a promising route may remain uncertain until its central claims are tested." |
| Distributed Technical Difficulty | "A proof may contain several interdependent bottlenecks, from constructing a new object to establishing a delicate estimate. Resolving one difficulty can expose another, and a local revision may require changes to the surrounding argument." |
| Long Outputs and Error Accumulation | "Long proofs can exceed the output budget of a single response, leading to omitted details or unfinished arguments. Definitions and assumptions must also remain consistent across distant sections, since an unsupported step can be reused and propagate errors through the rest of the proof." |
| Failure and Partial Progress | "Failed attempts may still yield useful counterexamples, restrictions, or intermediate results. To guide later work, this information must be recorded as specific mathematical claims or objections; a generic failure judgment does not explain what remains valid or what should change." |

## Research Pipeline (3.1)
**Covers:** Section 3.1, Figure 1 panel (a)

- Exploration develops and tests candidate strategies until the readiness gate selects a route concrete enough to support proof construction.
- Decomposition turns that route into a sectioned proof skeleton and a dependency graph over subproblems.
- Eligible subproblems are solved with independent sections in parallel; a section failing local review is retried without restarting unaffected subproblems; completed sections are assembled into a single proof.
- Global verifier evaluates the assembled proof; a rejected proof enters revision or reopens exploration; revision may replace section bodies or modify the outline before reassembly and re-verification; re-exploration is reserved for cases where the current strategy no longer supports a credible path.
- Section 4.2 is cited as developing these stages and return paths in detail.

## Inference within a Stage (3.2)
**Covers:** Section 3.2, Figure 1 panel (b)

- The pipeline picks the current task, but a difficult stage is not entrusted to a single model continuation.
- Colosseum generates a population of candidates, subjects them to targeted falsification, and iteratively synthesizes random subsets of candidates plus critiques through the overlapping sampling tree in panel (b).
- Candidate type changes with the stage — "a strategy, a proof skeleton, a section body, a verifier assessment, or a revision" — but the inference pattern is reused.
- The root artifact and any unresolved objections return to the research pipeline; stage-level decisions set where additional inference is applied, aggregation decides how a difficult in-stage decision is resolved.
- Section 4.1 is cited as describing this inner procedure in detail.

**Covers:** Contributions list through Section 3.2 (paper pp. 3–5 in chunk)
