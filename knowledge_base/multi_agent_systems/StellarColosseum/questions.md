---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science

### Q1. What is Stellar Colosseum, and what are its four workflow-level mechanisms plus its within-stage inference pattern?
> [!tip]- Answer
> Stellar Colosseum is a model-agnostic, many-agent harness that allocates inference across long-horizon mathematics and TCS (Theoretical Computer Science — the study of computation, algorithms, and complexity) research. At the workflow level it explores alternative strategies before proof construction, gates readiness, decomposes the proof into interdependent section-level subproblems, and routes verifier findings back to the affected part. Within each stage it generates candidates in parallel, attacks them with targeted falsification, and synthesizes them via overlapping random-sample tree aggregation. See [[wiki/01-overview-and-motivation|Stellar Colosseum: Overview and Motivation]].

### Q2. What are the four long-horizon research challenges that motivate Colosseum's design?
> [!tip]- Answer
> The four challenges are strategic uncertainty (the route to a proof is unclear and needs exploration), distributed technical difficulty (interdependent bottlenecks where fixing one exposes another), long outputs and error accumulation (single responses omit details and unsupported steps propagate), and failure with partial progress (failed attempts yield counterexamples or restrictions that must be recorded as specific claims, not generic failure). Each maps to a design choice: exploration, dependency-aware decomposition, sectioned construction, and critique-preserving memory. See [[wiki/02-strategy-exploration-and-readiness-gate|Strategy Exploration and Readiness Gate]].

### Q3. How does Colosseum's overlapping random-sample tree aggregation work, and what is the expected-reuse formula?
> [!tip]- Answer
> Each candidate bundled with its falsification records forms level C(0); each aggregation node at the next level independently draws k_l distinct inputs uniformly from the current population, with sampling without replacement inside a group but overlap allowed across groups. Each node synthesizes its subset while carrying critiques and disagreements forward, and the root returns one artifact plus unresolved objections. Expected reuse of a fixed node is E[R_i^(l)] = m(l+1) · k_l / m_l, targeting roughly two to three in contraction layers. See [[wiki/03-pipeline-context-and-shared-knowledge|Pipeline Context and Shared Knowledge]].

### Q4. What are the two complementary forms of cross-round memory, and what four kinds of entries does the knowledge curator record?
> [!tip]- Answer
> Across rounds Colosseum retains the full latest proof attempt (rejected draft plus verifier feedback, grounding the next round without endorsing its claims) and a shared knowledge directory of reusable findings that aggregation might otherwise discard. The curator records theorems and lemmas, failed approaches with precise failure points, references with needed statements and hypotheses, and observations with evidence and implications — each entry keeping its source and caveats. See [[wiki/03-pipeline-context-and-shared-knowledge|Pipeline Context and Shared Knowledge]].

### Q5. What aggregation tree configurations (widths and sample size) does Colosseum use for TCS-Bench, Codeforces, and the remaining stages?
> [!tip]- Answer
> Strategy exploration for TCS-Bench (Theoretical Computer Science Benchmark — a 300-task research-level theorem-proving suite) and Codeforces both use tree widths (32, 16, 8, 5, 1) with sample size k=5, while all remaining stages in all three settings use (16, 8, 5, 1) with k=5 and effective sample size min{k, m_l} at level l. Open-problem research uses varying exploration trees, some with slightly over 100 leaves, used only for exploration. These numbers fix population widths and fan-in, not total model calls. See [[wiki/04-inference-configs-and-research-results|Inference configs and research results]].

### Q6. Name two of the five new research results Colosseum runs contributed, with their key quantitative advances.
> [!tip]- Answer
> Any two suffice: l_p subspace approximation keeps the same sampling rule but cuts coreset size from O~(k^{p/2} ε^{-p}) to O~(k^{p/2} ε^{-2}); single-stage Hadamard quantization matches the 1/(d·4^b) error scaling with pairwise-independent dithers, removing the O(d)-bit residual payload and cutting the leading constant ~5.93x. Others include the sparse-least-squares condition-number barrier, the m^{c/ε^{2−2δ}} inner-product embedding lower bound, and the Ω(log^{3/2}n/(log log n)^{3/2}) prefix-matrix factorization bound. See [[wiki/04-inference-configs-and-research-results|Inference configs and research results]].

### Q7. How is TCS-Bench scored, what is the cross-model selection rule, and what accuracy does it reach?
> [!tip]- Answer
> TCS-Bench has 300 theorem-proving tasks from FOCS/STOC/SODA 2020–2026 papers, scored by a reference-assisted automated grader (given the ground-truth proof, >90% agreement on 100 expert-labeled proofs). Colosseum runs once with Gemini 3.1 Pro and once with Gemini 3.7 Flash; Flash samples eight critiques of the Pro proof and submits it only if at least five judge it correct, else the Flash proof. Cross-model selection reaches 71.0% (213 problems), above GPT-5.6 Pro (max) at 68.0% and each individual run (54.0%/55.0%). See [[wiki/05-tcs-bench-evaluation|Research-Level Evaluation on TCS-Bench]].

### Q8. What future adaptive inference controller does the paper propose, and what signals, actions, and evaluation discipline does it specify?
> [!tip]- Answer
> Because fixed population widths, fan-in, and sample counts waste compute where extra samples add little, a future controller would reuse workflow signals — strategy diversity, unresolved objections, repeated local failures, and agreement among independent candidates. It would expand uncertain branches, grant retries to unstable sections, and stop stabilized stages. Compute-matched evaluation is required to separate better allocation from merely more inference. See [[wiki/06-codeforces-limits-and-future-work|Adaptive Inference Allocation. The current configurations]].

### Q9. What are the Explorer, Exploration Falser, and Readiness Gate duties in Appendix A.1?
> [!tip]- Answer
> The Explorer develops one high-level strategy card (not a proof), with exactly one primary route and at most two backups. The Exploration Falser only attacks the card — testing weak lemmas, hidden assumptions, and bound directions — returning categorized objections and a survive/weaken-or-repair/reject/falsified verdict without rewriting it. The Readiness Gate neither solves nor repairs but audits fatal bridges, theorem uses, and code results, classifying the card as ready, eligible with explicit obligations, needing exploration, or rejected. See [[wiki/07-references-and-related-work|References and Related Work ([41]–[65]) plus Appendix Prompts]].

### Q10. Should a mathematics lab adopt Colosseum's full harness, or only its falsification-plus-critique-preserving aggregation, for long-proof projects?
> [!tip]- Answer
> Adopt the falsification-plus-aggregation discipline first, since critique-attached synthesis and the 71.0% TCS-Bench result with AUC (Area Under the Curve — a 0–1 score of how well critiques separate correct from incorrect proofs) 0.896 show it catches shared errors that flat voting misses. Take on the full harness — readiness gating, dependency DAGs (Directed Acyclic Graphs — dependency maps with no cycles), and global verification with local retry — only once long drafts with interdependent sections justify the orchestration and compute cost. See [[wiki/08-appendix-prompts-and-details|Appendix: Prompts and Details — A Strategy with an Unresolved Fatal]].
