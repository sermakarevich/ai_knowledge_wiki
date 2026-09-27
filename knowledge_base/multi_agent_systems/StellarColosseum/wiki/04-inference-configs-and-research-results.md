[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Inference configs and research results
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
---
## Exploration vs. shared configurations
**Covers:** Section 4 tail / Table 1

> "exploration, some with slightly over 100 leaf nodes. These larger trees are used only for exploration; all remaining stages share a fixed configuration with 16 leaf nodes."

| Setting | Stage | Tree widths m | Sample size k |
|---|---|---|---|
| Open-problem research | Strategy exploration | Varies | Varies |
| TCS-Bench | Strategy exploration | (32, 16, 8, 5, 1) | 5 |
| Codeforces | Strategy exploration | (32, 16, 8, 5, 1) | 5 |
| All three settings | All remaining stages | (16, 8, 5, 1) | 5 |

Table 1: Stage-level aggregation configurations for open-problem research, TCS-Bench, and Codeforces. At level l, the effective sample size is min{k, m_l}.

> "These configurations specify population widths and aggregation fan-in rather than the exact total number of model calls, which also depends on the number of proof sections, local retries, and global revision rounds."

## Selected research results
**Covers:** Section 5 intro

> "We summarize five research results to which runs of the workflow contributed. Each subsection states the motivating question and principal advance; the cited papers provide complete definitions, attribution, and proofs."

## Strong coresets for l_p subspace approximation when p > 2
**Covers:** Section 5.1

- Problem: given A in R^{n x d}, find low-dimensional subspace minimizing aggregate distance of rows of A; strong coreset samples/rescales few rows to form SA preserving simultaneously for every subspace F of dimension at most k: ||SA(I-P_F)||_{p,2}^p = (1 +/- epsilon)||A(I-P_F)||_{p,2}^p.
- Prior: Woodruff and Yasuda obtained coreset size O~(k^{p/2} epsilon^{-p}) via recursive ridge-leverage-score sampling; unclear whether epsilon^{-p} was intrinsic or from analysis of recursive row-count recurrence.
- New: same sampling rule supports O~(k^{p/2} epsilon^{-2}) with O~(nnz(A) + d^omega) running time; key step keeps truncation in sampling probabilities when bounding surviving rows, changing fixed point of recurrence from epsilon^{-p} to epsilon^{-2} dependence.

## The condition-number barrier in sparse least squares
**Covers:** Section 5.2

- Prior: for objectives with restricted condition number kappa, known algorithms need output sparsity with essentially linear dependence on kappa; Axiotis and Sviridenko gave such an algorithm and conjectured it could not be improved by polynomial-time algorithms.
- New: for least-squares, barrier holds conditional on randomized exact-volume Small-Set Expansion Hypothesis: for every fixed gamma in (0,1], no randomized polynomial-time algorithm can with probability >= 2/3 return x with s = ||x||_0 satisfying ||Ax-b||_2^2 <= min_{||z||_0 <= k} ||Az-b||_2^2 + epsilon and s = O(k kappa^{1-gamma} / (s+k)), where kappa_r is restricted condition number at sparsity level r; thus no fixed sublinear power of kappa can replace linear dependence.

## Dimension lower bounds for maximum inner product embeddings
**Covers:** Section 5.3

- Setup: multi-vector embeddings compare point clouds via Chamfer similarity; single-vector embeddings compare one vector per item by inner product; for singleton queries Chamfer reduces to maximum inner product.
- Prior: upper bound m^{O(1/epsilon^2)} for representing point clouds of size at most m by single vectors; earlier lower bound (epsilon^2 m)^{Omega(1/epsilon)} left gap between 1/epsilon and 1/epsilon^2 in exponent of m.
- New: for every fixed delta in (0,1) and sufficiently large m, there are unit query vectors and document point clouds where any single-vector representation approximating all maximum inner products to additive error epsilon must have dimension D >= m^{c_delta / epsilon^{2-2delta}} for constant c_delta > 0; holds even for fully data-dependent representations and extends to Chamfer similarity.

## Single-stage Hadamard quantization
**Covers:** Section 5.4

- Prior: unbiased dithered quantizer with sharp mean-squared-error guarantees; finer 1/d-scale inner-product estimator used second randomized transform plus residual quantization stage, adding communication and larger leading constant.
- New: second stage unnecessary for same 1/(d 4^b) mean-squared-error scaling; pairwise-independent dithers across Hadamard coordinates yield unbiased single-stage estimator using b bits per coordinate.
- Removes residual-stage O(d)-bit payload and reduces leading constant in proved upper bound by ~5.93x.

## Lower bounds for prefix-matrix factorizations
**Covers:** Section 5.5

- Setup: Q is n x n lower-triangular all-ones matrix mapping vector to prefix sums; for Q = AB, gamma_{2,1}(Q) = inf_{Q=AB} ||A||_{2->inf} ||B||_{1->1} governs space bounds for factorization-based rank/quantile estimation in turnstile streams and error bounds for matrix mechanisms in continual counting.
- New: gamma_{2,1}(Q) = Omega(log^{3/2} n / (log log n)^{3/2}) over real factorizations of arbitrary finite inner dimension; dyadic factorization gives O(log^{3/2} n), so bounds differ only by (log log n)^{3/2}; proof combines right-sided Haar projections with scale-dependent numerical-sparsity decomposition, aggregated across dyadic scales.

## Case study: long-form proof construction for Knuth's cycles
**Covers:** Section 5.6

- Problem: for integer m > 2, can directed edges of Cayley graph Gamma_m = Cay(Z_m^3, {e1,e2,e3}) be partitioned into three directed Hamiltonian cycles; odd case has simple construction with complete proof, even case harder.
- History in chunk: earlier intricate even-case construction generated by GPT-5.3-Codex with complete proof via GPT-5.4 Pro; later multi-agent search produced much simpler even-m construction verified computationally through m <= 2000 but lacking rigorous symbolic proof for arbitrary even m; subsequent note introduced second simple construction and reports full-length AI-generated proof drafts for both.
- Difficulty: compact local routing rules depending on parity plus exceptional boundary cases; must show every directed edge assigned exactly once and each color class traverses all m^3 vertices in single cycle rather than shorter cycles.
- Output: 46-page proof draft for earlier construction and 75-page proof draft for new one; shows proof far beyond typical single model response developed as persistent revisable document with explicit dependency structure.

## Case study: independent rediscovery of the Erdos unit-distance breakthrough
**Covers:** Section 5.7

- Background: u(n) = max unit-distance pairs among n planar points; Erdos grid gives n^{1+Omega(1/log log n)}, conjectured u(n) = n^{1+o(1)}; OpenAI reports internal model generated 2026 counterexample, distilled/simplified/human-verified to show infinitely many sets with >= n^{1+delta} pairs for fixed delta > 0.
- Colosseum run: Gemini 3.1 Pro as base model, internet disabled; 22-page draft developed number-theoretic approach based on unramified towers and relative unit groups, independently arriving at central architecture of OpenAI solution and pursuing u(n) >= n^{1+epsilon_0} for infinitely many n with explicit epsilon_0 > 0.
- Process signal: run proceeded through 15 exploration rounds; accumulated-knowledge layer carried partial results, objections, failed attempts forward, letting strategy-selection loop synthesize evidence into subsequent directions; concrete example of sustained coherent long-horizon research.
**Covers:** Sections 4-tail/Table 1 through 5.7
