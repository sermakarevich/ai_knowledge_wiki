> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science — In Plain Language

## What is this about?

Stellar Colosseum (Colosseum for short) is an organizer for Artificial Intelligence (AI) research teams.

Instead of asking one AI model (a single large language model) to solve a hard math problem in one go, it runs many AI agents — small specialist roles like explorer, critic, builder, and checker — that work together over many rounds.

Think of it like running a research lab: some agents suggest routes, others try to break them, others write parts of the proof (a step-by-step logical argument), and others check the whole thing. The system keeps every draft, critique, and fix so later rounds build on earlier work instead of starting over.

It is model-agnostic, meaning it can work with different underlying AI models (here Gemini 3.1 Pro and Gemini 3.7 Flash). It has been added to Google Antigravity's Teamwork framework as the "Long Proof" pattern.

It organizes computing effort at two levels: a big-picture workflow (which stage runs next, and whether to fix, retry, or change direction) and a within-stage contest (many candidates compete, get criticized, and get merged). Figure 1 in the paper shows both levels side by side.

## Why does it matter?

Long math proofs are hard for AI for four plain reasons:

1. The right route is unclear at the start — you must try several ideas before one looks workable.
2. A proof has several linked hard parts — fixing one part can break another.
3. Long outputs accumulate errors — definitions drift, a weak step gets reused, details get skipped.
4. Failed tries still contain value — a counterexample (an example that disproves a claim), a partial lemma (a helper result), or a warning about a dead end.

Single-shot answers and simple majority votes do not fix this: several agents can agree and still share the same hidden mistake. Colosseum matters because it turns inference (the computing effort spent at answer time) into an organized process: explore routes, check readiness, split the work, verify the whole, and repair only what broke.

A familiar analogy: writing a book by first testing several outlines, having an editor approve one, assigning chapters to different authors with a shared style guide, and then proofreading the whole book — instead of asking one person to write it perfectly in a single sitting.

The headline evidence: 71.0% accuracy on the 300-task TCS-Bench (a research-level test set from FOCS, STOC, and SODA papers — top conferences in theoretical computer science), several new results on open problems from FOCS and JMLR (Journal of Machine Learning Research) papers, and 218 of 222 solved Codeforces programming problems with execution feedback.

## How does it work?

The work runs in five stages, with a shared memory across all of them.

A shared rule applies inside every hard stage: generate a diverse population, attack each member with critics, then combine random overlapping groups through a tree. Random overlapping groups matter because the same draft gets mixed with different partners, so minority insights survive instead of being voted out early.

**Stage 1 — Strategy exploration.** Many explorers each propose one "strategy card": one main route plus at most two backup routes, with the mechanism, needed helper results, expected bottleneck, and a testable check. Paired falsifiers (adversarial critics) attack each card: counterexamples, hidden assumptions, wrong inequality directions, misused theorems. An aggregator then merges overlapping random groups of cards-plus-critiques through a tree until one improved card comes out. Exploration repeats until a route looks solid.

**Stage 2 — Readiness gate.** A gatekeeper agent audits the best card but does not solve or repair it. It asks: is the central idea stable, are the remaining gaps precise enough to hand to writers, and is there any fatal gap that would force a new route? Verdicts are ready, eligible with explicit obligations (small gaps assigned to specific sections), needs more exploration, or rejected.

**Stage 3 — Proof decomposition.** The approved route becomes a LaTeX (a document format for math writing) skeleton: title, short abstract, one section per subproblem, each with a roadmap and a placeholder for the body. A dependency graph (a map of which section needs which earlier section, with no cycles — a DAG, or Directed Acyclic Graph) controls the order of work, while document order controls how it reads.

**Stage 4 — Subproblem solving.** Independent sections are solved in parallel by many solvers, each critiqued by a paired falser (verdicts: ready, conditional meaning useful but gappy, or rejected). A tree aggregator merges candidates without hiding objections. A failed section is retried locally with its old draft plus criticism — the rest of the proof is kept.

**Stage 5 — Global verification.** A global verifier reads the whole assembled proof against the original problem, using local reviews only as audit context. One concrete fatal defect is enough to reject — this is not a vote. Rejection has two return paths: revision (replace section bodies or tidy the outline, then re-verify) or re-exploration when the whole route no longer looks credible.

**Memory across rounds.** Two things carry forward: the full latest draft plus its verifier feedback, and a shared knowledge directory curated into theorems and lemmas, failed approaches, references, and observations — each with its source and caveats (warnings).

Typical tree sizes make the scale concrete: strategy exploration uses wider trees (32, 16, 8, 5, 1) with sample size 5, sometimes over 100 starting leaves, while all later stages use a fixed (16, 8, 5, 1) setup. Only an executed code probe (actually run code) counts as computational evidence — an unrun calculation stays an open obligation, not proof.

## Where can this be used?

- Open-ended math and theoretical computer science research: the runs contributed five new results (smaller coresets for subspace approximation, a condition-number barrier for sparse least squares, dimension lower bounds for embeddings, simpler Hadamard quantization, prefix-matrix lower bounds) plus long drafts — 46-page and 75-page proofs for Knuth's cycles constructions, and a 22-page independent rediscovery of the Erdos unit-distance breakthrough over 15 rounds with internet disabled.
- Research-level benchmark proving: the TCS-Bench setup (300 tasks, reference-assisted automated grader scoring above 90% on expert-labeled proofs) is a template for testing any long-proof system.
- Competitive programming with checks: the same proof-shaped pipeline plus code execution reached 218/222 on Codeforces.
- Picking the better of two runs: for TCS-Bench the system ran once with each model, then asked one model for eight independent critiques of the other's proof and kept it only if at least five judged it correct. The benchmark grader only scored the final pick and played no role in choosing it.
- Future reuse: validated runs record full trajectories (strategies, critiques, dependency graphs, revision histories) that could become training data for the next model — with the open challenge of credit assignment (figuring out which intermediate step actually caused success), and a planned adaptive controller that spends extra effort only on uncertain branches.

## Conclusions & takeaways

- Split long research into stages (explore, gate, decompose, solve, verify) and repair locally instead of restarting.
- At every hard stage: generate diverse candidates in parallel, attack them with dedicated critics, and merge them through a tree that keeps critiques attached.
- Never let a vote overrule a concrete counterexample: one fatal defect rejects.
- Keep two memories: the last full draft with its feedback, and a curated directory of reusable findings with sources and caveats.
- The numbers support the design: individual runs scored 54.0% and 55.0%, smart cross-model selection reached 71.0% (213 problems, 48 more than the stronger single run), with critique quality at AUC (Area Under the Curve — a score where 1.0 is perfect separation) 0.896 and an oracle upper bound of 77.3%.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Harness | The organizer software that assigns tasks to AI agents and passes results between them. |
| Long-horizon research | Work that takes many linked steps over many rounds, where early choices shape later work. |
| Inference | Computing effort a model spends when producing an answer (as opposed to training). |
| Strategy card | A one-route plan: main idea, needed helper results, expected hard part, and a testable check — not yet a proof. |
| Readiness gate | A checkpoint that decides whether a plan is concrete enough to split into writing tasks. |
| Falsifier / falsification | A critic role that tries to break a proposal with counterexamples and hidden-assumption checks. |
| Tree aggregation | Merging overlapping random groups of drafts-plus-critiques level by level until one combined draft remains. |
| Dependency graph (DAG) | A map showing which proof sections depend on which earlier ones, with no circular dependencies. |
| Global verifier | The final checker that reads the whole assembled proof against the original problem. |
| Knowledge directory | A shared notebook of reusable theorems, failed routes, references, and observations with sources and warnings. |
