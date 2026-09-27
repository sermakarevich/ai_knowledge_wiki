> [[index|Wiki]] | [[summary|Summary]]
# Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science — Digest

## 1. [[wiki/01-overview-and-motivation|Stellar Colosseum: Overview and Motivation]]
**In one sentence:** Stellar Colosseum is a model-agnostic, many-agent harness that allocates inference across long-horizon mathematics and theoretical computer science research by exploring strategies, gating readiness, decomposing proofs into interdependent sections, and routing verifier feedback back to the affected parts.
## Key points
- Language models can produce plausible short proofs but remain unreliable on long-horizon research problems where progress depends on a sequence of uncertain, interdependent decisions.
- Colosseum is model-agnostic and organizes inference at two levels: a stage-level research workflow and within-stage parallel sampling plus synthesis (Figure 1).
- At the workflow level it explores alternative strategies before proof construction, uses a readiness gate to decide when a route is mature enough to decompose, represents the proof plan as interdependent section-level subproblems, and routes verifier findings back to the affected part of the argument.
- Within each stage it generates candidates in parallel, attacks them with targeted falsification, and combines candidates and their critiques into a single research artifact through overlapping random-sample tree aggregation.
- The workflow has been integrated into Google Antigravity's Teamwork framework as the Long Proof pattern [7].
- It builds on and substantially extends the parallel exploration and iterative verification architecture of Woodruff et al. [56], adding explicit stage control, dependency-aware proof construction, and critique-preserving aggregation.
- Demonstrated with Gemini 3.1 Pro (plus Gemini 3.7 Flash on TCS-Bench): several new results on open problems from FOCS and JMLR papers, 71.0% accuracy on TCS-Bench, and 218 of 222 solved in a Codeforces evaluation with execution feedback.

## 2. [[wiki/02-strategy-exploration-and-readiness-gate|Strategy Exploration and Readiness Gate]]
**In one sentence:** Colosseum tackles long-horizon research by exploring alternative strategies until one passes a readiness gate, then decomposing it into parallel subproblems with stage-level generate–falsify–aggregate inference that retains critiques, and repairing or re-exploring on verification feedback.
## Key points
- Exploration continues until a strategy is "concrete enough to decompose into a sectioned plan with explicit dependencies," at which point the readiness gate selects it for proof construction.
- Decomposition produces a sectioned proof skeleton plus a dependency graph; independent subproblems are solved in parallel and a failed section is retried without restarting unaffected subproblems.
- Global verification of the assembled proof has two return paths: revision (replace section bodies or modify the outline, then reassemble and re-verify) or re-exploration when the strategy no longer supports a credible path.
- Each stage generates a population of candidates (strategy, proof skeleton, section body, verifier assessment, or revision), subjects them to targeted falsification, and synthesizes random subsets via an overlapping random-sample tree.
- Aggregation keeps critiques attached to the proposals they address, and the root artifact plus any unresolved objections become part of the research state for later stages.
- Demonstration uses Gemini 3.1 Pro as base model, with critique-based selection between runs using Gemini 3.1 Pro and Gemini 3.7 Flash reaching 71.0% accuracy on TCS-Bench [15].
- In the competitive-programming case study the proof-oriented workflow with implementation and execution feedback records 218 accepted solutions on a 222-problem Codeforces suite.

## 3. [[wiki/03-pipeline-context-and-shared-knowledge|Pipeline Context and Shared Knowledge]]
**In one sentence:** Information produced earlier in the pipeline stays available to later stages — within a round (strategy, proof plan, section bodies, verifier findings), across rounds (rejected draft plus verifier feedback, plus a shared knowledge directory of reusable results), and Section 4.3 describes these two forms of cross-round memory.
## Key points
- Within a round, later stages can use the current strategy, the sectioned proof plan, completed section bodies, and verifier findings.
- Across rounds, a rejected proof draft and its verifier feedback are passed directly into the next attempt, so the next round does not start from the original problem alone.
- Cross-round memory has two complementary forms: the full latest proof attempt (grounds the next round in what was actually tried) and a shared knowledge directory (preserves reusable findings that aggregation might otherwise discard).
- The decomposer produces a numbered, sectioned proof skeleton with dependency edges forming a directed acyclic graph (DAG); document order controls exposition while the dependency graph controls the order work can proceed.
- A subproblem becomes eligible once its dependencies are completed, independent sections are solved in parallel, and each retry is local — completed work elsewhere in the dependency graph is preserved.
- Global verification reads the original problem plus the completed document as one argument, uses local subproblem reviews as audit context, and rejects on a single concrete fatal defect (not a majority vote).
- The knowledge curator records four reusable kinds: (1) theorems and lemmas, (2) failed approaches, (3) references, (4) observations — each entry retaining its source and caveats, updated across rounds.

## 4. [[wiki/04-inference-configs-and-research-results|Inference configs and research results]]
**In one sentence:** Strategy-exploration trees use larger widths (some with over 100 leaves, TCS-Bench/Codeforces use (32, 16, 8, 5, 1) with k=5 while all later stages use (16, 8, 5, 1) with k=5), and runs of the workflow contributed five new results plus two long-horizon case studies.
## Key points
- Exploration trees can exceed 100 leaf nodes and are used only for exploration; all remaining stages share a fixed 16-leaf configuration.
- TCS-Bench and Codeforces strategy exploration both use tree widths (32, 16, 8, 5, 1) with sample size k=5, while all remaining stages use (16, 8, 5, 1) with k=5 and effective sample size min{k, m_l} at level l.
- For l_p subspace approximation with p > 2, the Colosseum-obtained proof shows the same sampling rule supports coreset size O~(k^{p/2} epsilon^{-2}) instead of O~(k^{p/2} epsilon^{-p}), keeping O~(nnz(A) + d^omega) running time by keeping truncation in sampling probabilities when bounding surviving rows.
- For sparse least squares, no randomized polynomial-time algorithm can achieve error min_{||z||_0 <= k} ||Az-b||_2^2 + epsilon with sparsity s = O(k kappa^{1-gamma} / (s+k)) for every fixed gamma in (0,1], conditional on the randomized exact-volume Small-Set Expansion Hypothesis with success probability at least 2/3.
- For maximum inner-product embeddings, any single-vector representation approximating all maximum inner products to additive error epsilon must have dimension D >= m^{c_delta / epsilon^{2-2delta}} for every fixed delta in (0,1) and large m, nearly closing the gap between 1/epsilon and 1/epsilon^2 in the exponent.
- Single-stage Hadamard quantization attains the same 1/(d 4^b) mean-squared-error scaling with b bits per coordinate using pairwise-independent dithers, removing the residual-stage O(d)-bit payload and reducing the leading constant by ~5.93x.
- The prefix-matrix factorization lower bound is gamma_{2,1}(Q) = Omega(log^{3/2} n / (log log n)^{3/2}), near-optimal against the dyadic O(log^{3/2} n) upper bound, via right-sided Haar projections plus scale-dependent numerical-sparsity decomposition.
- Case studies show long-horizon behavior: 46-page and 75-page proof drafts for Knuth's cycles even-m constructions, and a 22-page independent rediscovery draft of the Erdos unit-distance breakthrough (u(n) >= n^{1+epsilon_0}) over 15 exploration rounds with internet disabled.

## 5. [[wiki/05-tcs-bench-evaluation|Research-Level Evaluation on TCS-Bench]]
**In one sentence:** Colosseum is tested for breadth on the 300-task research-level TCS-Bench, where cross-model selection between Gemini 3.1 Pro and Gemini 3.7 Flash runs reaches 71.0% accuracy, beating all direct-model baselines and each individual Colosseum run.
## Key points
- TCS-Bench contains 300 theorem-proving tasks derived from papers published at FOCS, STOC, and SODA between 2020 and 2026, each supplying the mathematical context and asking for a self-contained proof of a target theorem.
- Candidate proofs are scored by a reference-assisted automated grader that also receives the benchmark's ground-truth proof; its prompt was optimized on a separate set of 100 expert-labeled proofs, on which it reported more than 90% accuracy.
- Colosseum is run separately with Gemini 3.1 Pro and Gemini 3.7 Flash, producing one candidate proof from each run for every problem.
- Selection rule: Gemini 3.7 Flash produces eight independently sampled critiques of the Gemini 3.1 Pro proof; if at least five judge that proof correct it is submitted, otherwise the Gemini 3.7 Flash proof is submitted; the benchmark grader only scores the selected proof and plays no role in selection.
- Individual Colosseum runs score 54.0% (with Gemini 3.1 Pro) and 55.0% (with Gemini 3.7 Flash), far above direct Gemini 3.1 Pro evaluation at 30.3% and above Gemini 3.1 DeepThink at 52.0%.
- Cross-model selection reaches 71.0%, above GPT-5.6 Pro (max) at 68.0%, solving 213 problems — an improvement of 48 problems over the stronger individual run — and is the highest accuracy among evaluated non-oracle methods.
- The two runs have nearly identical accuracy but complementary errors: the critique signal distinguishes grader-labeled correct vs. incorrect proofs with an AUC of 0.896, while routing with Gemini 3.1 Pro's internal verifier alone yields only 64.7%; the oracle best-of-two (fraction solved by at least one run) is 77.3% and is an upper bound rather than an achievable selection rule.

## 6. [[wiki/06-codeforces-limits-and-future-work|Adaptive Inference Allocation. The current configurations]]
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

## 7. [[wiki/07-references-and-related-work|References and Related Work ([41]–[65]) plus Appendix Prompts]]
**In one sentence:** This chunk lists references [41]–[65] and opens Appendix A with the shortened prompt templates for strategy exploration (explorer, falser, aggregator, readiness gate).
## Key points
- Lists 25 references numbered [41]–[65], spanning NeurIPS 2023 through arXiv preprints dated 2024, 2025, and 2026.
- Reference [41] is Honghao Lin, Vahab Mirrokni, and David P. Woodruff, "Pairwise-independent dithering for single-stage Hadamard quantization," arXiv:2608.02564, 2026.
- Appendix A states its templates are "shortened versions of the prompts used by the harness" with "items in braces filled in by the harness at runtime" and repeated instructions omitted.
- The Explorer must "Develop one promising high-level solution strategy before decomposition" and "Return one strategy card, not a proof, section plan, or LaTeX document," keeping exactly one primary route and at most two backup routes.
- The Exploration Falser must "Attack the supplied strategy card. Do not rewrite, polish, or defend it, except to name a minimal weakening," returning categorized objections, cheap tests, and a survive / weaken-or-repair / reject / falsified verdict.
- The Exploration Aggregator must "Produce one new strategy card, not a list and not a decomposition," preserving the narrowest repairable primary route and at most two backups while addressing every serious falser objection.
- The Readiness Gate does not solve or repair but audits fatal bridge claims, cited theorems, equivalences, invariants, bound directions, and code results, classifying the card as ready, eligible with explicit obligations, needing further exploration, or rejected.

## 8. [[wiki/08-appendix-prompts-and-details|Appendix: Prompts and Details — A Strategy with an Unresolved Fatal]]
**In one sentence:** A strategy with an unresolved fatal bridge can only proceed to decomposition under strict stability and explicit-obligation conditions, after which fixed prompts govern decomposition into a LaTeX skeleton with a dependency DAG, parallel subproblem solving with falser critique and aggregation, and global verification with conservative revision.
## Key points
- A strategy with an unresolved fatal bridge cannot be marked ready, but may proceed to decomposition only if the route and proof architecture are stable and every remaining obligation has a concrete proof or verification path.
- Minor obligations must each be assigned to an explicit proof or certificate section in the proof plan, while a major obligation — one that could force changing the route, reduced target, or core mechanism, or that has no clear repair path — sends the strategy back for further exploration.
- Decomposition output must return blocking issues, fatal bridge claims, theorem and criterion audits, hidden hard steps, minimal remaining obligations, obligation severity, whether decomposition is allowed, and the recommended next action.
- The decomposer produces a standalone LaTeX master-document skeleton (title, concise abstract, one section per subproblem with a specific roadmap and a reserved body location) plus an ordered subproblem list in topological order with dependency indices, and must not silently build on unresolved attacked claims.
- Each subproblem is solved by multiple solvers, critiqued by paired falsers, and combined through a tree aggregator, with retries supplied with the previous attempt and its criticism so progress is retained without hiding unresolved objections.
- Only an executed code probe counts as computational evidence; an unexecuted certificate may only be stated as a reduction, conditional result, or certificate plan with the stronger claim kept as an open obligation.
- A subproblem falser never repairs or rewrites: it classifies sections as ready (later assembly may rely on the result), conditional (useful progress but an explicit bridge or obligation is unresolved), or rejected (wrong target, false or constraint-dropping bridge), since any explicit gap precludes a ready verdict.
- The global verifier reads the entire assembled proof against the original problem (hypotheses, scope, conclusion, theorem uses, citations, computations, boundary cases, attacked/conditional claims), accepts only complete proofs, otherwise writes standalone actionable feedback localizing every material defect; revision is conservative (outline cleanup cannot add sections, reorder the plan, or introduce a new strategy) and code probes are adversarial checks only, never repairs.

## The argument in five moves
1. Long-horizon mathematics and TCS research fails under single-shot inference because routes are uncertain, proofs have interdependent bottlenecks, long outputs accumulate errors, and failed attempts carry usable partial progress that must be preserved.
2. Colosseum therefore separates the workflow into stages — strategy exploration, readiness gating, decomposition into a dependency-graph of section subproblems, parallel subproblem solving, and global verification — with local retry, revision, or re-exploration as the return paths.
3. Within every difficult stage the same adversarial inference pattern applies: generate diverse candidates in parallel, attack each with targeted falsification, and synthesize overlapping random subsets through a tree that carries critiques and unresolved objections forward to the root artifact.
4. Memory across rounds makes the process cumulative rather than restart-based: the latest rejected draft plus verifier feedback grounds the next attempt, while a curated knowledge directory (theorems/lemmas, failed approaches, references, observations) preserves reusable findings with sources and caveats.
5. Breadth and depth evaluations support the design: cross-model critique selection over two Colosseum runs reaches 71.0% on the 300-task TCS-Bench (AUC 0.896 critique signal, 77.3% oracle best-of-two), the proof-oriented pipeline solves 218/222 Codeforces problems, and open-ended runs contribute new results plus long coherent drafts (46/75-page Knuth cycles proofs, 22-page Erdos unit-distance rediscovery over 15 rounds).
6. The harness is completed by fixed, auditable prompts (explorer, falser, aggregator, readiness gate, decomposer, solver, verifier, conservative reviser) and a forward agenda: adaptive inference allocation driven by workflow signals with compute-matched evaluation, and distilling validated research trajectories into post-training data despite the credit-assignment challenge.
