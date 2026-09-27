[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Algorithm 1 Donor-Behavior Transfer, As Committed
**In one sentence:** Without training data or a single gradient update on the target, the community's best `transfer()` initializes the frozen 119.6M hybrid to 1.899044 bpb (from 3.3923 random, toward ~1.0 for a trained GPT-2 124M, closing 62% of the gap) by compressing donor behavior into a low-rank bigram transition operator (Stage A) plus structured attention/SSM/feed-forward routes (Stage B), with the first 18 scored contributions delivering ~98% of the total reduction.
## Key points
- Stage A builds a V×V bigram log-prob table M from 6 donors (D1..D6, weights αⱼ) over 28 contexts P: clipped (±25) log-softmax per donor/context/token, weighted by clipped variance and naturalness factors, then mean-centers M and takes a randomized SVD (rank d−1, oversample 32, 1 power iteration, fixed seed) to set the embedding E and output head H.
- Stage B wires fixed routes without learning: even attention layers {0,2,...,12} get zeroed Wq/Wk (uniform causal attention) with Wv/Wo reading/writing band Bk; layer-0 SwiGLU is 0.009 × SVDProject(GPT-2 small MLP0); odd SSM layers {1,3,...,13} copy read band Rℓ with recurrence off (Wx, Wdt ← 0), depthwise kernel ← κℓ, and Wout writes bands with per-band scalars.
- Trajectory: slice-copying GPT-2/Mamba weights scored 4.68 (worse than random, published as a negative result); 30 minutes later a unigram prior scored 2.52; within six hours four accounts reached bigram statistics under 3/6/12/24 prefixes (1.93); those 18 scored contributions account for ~98% of the total reduction, and the remaining 1,106 found the next 0.03.
- Milestones (Table 4, same development evaluator): 1.9319 (24 prefixes, geometric-mean aggregation, Apr 27), 1.9228 (second donor Cerebras-GPT 111M + variance/naturalness weights, Apr 28), 1.9136 (six donors, 28 single-token contexts, Apr 29), 1.9062 (one SVD power iteration, May 1), 1.9028 (first SSM edit, May 3), 1.8995 (layer-0 FFN projection, May 5), 1.8990 (cross-band SSM writes, May 8).
- Negative results are first-class records (53 tagged): doubling prefixes to 48 (four controlled variants), flattening the singular-value spectrum, transplanting native Mamba blocks, copying GPT-2's embedding directly, and building the prior from a different-tokenizer donor (Pythia) all regressed and were published with scores.
- Lineage/reproduction: best contribution has 145 commits by 15 of 17 accounts with 115/144 parent edges crossing accounts; 165 verification contributions cover 95 distinct targets (verifier ≠ author, zero reported failures); same-hardware reproductions are bit-identical, cross-hardware (A100 vs H100) differ ≤ 1.3×10⁻³ bpb; 40 of the winner's 144 scored ancestors were independently reproduced.
- Coordination/human/verification context: graph has 1,703 nodes, 1,894 edges, 149 multi-parent nodes, one component holding 98.9%; first 8 improvements ≈ 70% of descent; 63% of 696 equal-score cross-account pairs land within an hour (80% within six); one human intervention (May 2 diversity views → first sub-1.90 next morning); record verified by recomputing all counts from a server export, algebraic score check, and code-level import-chain reading (no eval-data touch, no gradient updates).
---
## Stage A — Transition prior (Algorithm 1, lines 1–9)
**Covers:** Algorithm 1, Stage A (lines 1–9)

Require: frozen target (d=672, 14 layers, vocabulary V); donors D1..D6 with weights αⱼ; contexts P (|P|=28); temperatures Tb, Tu; routes (Table 3).

- Line 1–4: for each donor j, context p, token v (streamed in batches): ℓⱼ,ₚ(v,·) ← clip(log softmax Dⱼ(p,v), ±25); wⱼ,ₚ(v) ← clipped variance × naturalness factors ([0.5, 1.5] range, normalized over p).
- Line 5: M(v,·) ← Σⱼ αⱼ Σₚ wⱼ,ₚ(v) ℓⱼ,ₚ(v,·) — "V × V bigram log-prob table".
- Line 6: u ← Σᵥ M(v,·); C ← M − 1u⊤.
- Line 7: (U, S, V⊤) ← RandSVD(C; rank d−1, oversample 32, 1 power iteration, fixed seed).
- Line 8: E:,0 ← 1; E:,1: ← U/√d; H:,0 ← u/(√d Tu); H:,1: ← VS/Tb.
- Line 9: embedding ← E; output head ← H; all sublayer weights ← 0; norms ← identity.

## Stage B — Structured context routes (Algorithm 1, lines 10–19)
**Covers:** Algorithm 1, Stage B (lines 10–19)

- Lines 10–13: for each attention layer ℓ ∈ {0, 2, ..., 12}, band k = ℓ/2: Wq, Wk ← 0 ("uniform causal attention"); Wv reads Bk scaled 1/√d; Wo writes Bk scaled aℓ.
- Line 14: layer-0 SwiGLU (Wgate, Wup, Wdown) ← 0.009 · SVDProject(GPT-2 small MLP0).
- Lines 15–18: for each SSM layer ℓ ∈ {1, 3, ..., 13}: Win copies read band Rℓ into 96 channels and their gates; Wx, Wdt ← 0 ("recurrence off"); depthwise kernel ← κℓ; Wout writes each band in Wℓ with its scalar.
- Line 19: return target.

## Evidence and trajectory (Figure 3, Table 4)
**Covers:** §4.5 Evidence (Figure 3, Table 4)

- Verbatim: "Figure 3: Every scored contribution at its server timestamp on a log bpb axis, with parent edges as faint lines; colour follows the score from magenta (at or above random) to green (below 1.96), and orange rings mark the leaders after May 2."
- Verbatim: "The first day's statistical priors deliver almost the whole reduction; donor ensembling and a better SVD sketch reach 1.904 by May 1; the first sub-1.90 scores follow the May 2 deployment of the landscape views. The rendering runs through May 9; all numbers in this report use the first 1,703 contributions, ending May 8."
- Verbatim trajectory: "The first scored attempt copied parameter slices from GPT-2 and Mamba into matching shapes and scored 4.68, worse than random; its author published it as a negative result with an explanation. Thirty minutes later the same account replaced copying with a unigram prior read off GPT-2's predictions (2.52), and within six hours four accounts had extended the idea to bigram statistics under 3, 6, 12, and 24 prefixes (1.93)."

Table 4 — Milestones on the ancestry of the best contribution at cutoff (times UTC; "selected on the same development evaluator, so adjacent rows are stages of a search, not a controlled ablation"):

| When | Account | bpb | Change introduced |
|---|---|---|---|
| — | — | 3.3923 | Random initialization |
| Apr 27 00:24 | worker1 | 4.6784 | Slice-copy GPT-2 and Mamba weights (worse than random) |
| Apr 27 00:57 | worker1 | 2.5151 | Unigram prior from GPT-2 predictions; residual sublayers zeroed |
| Apr 27 01:50 | worker1 | 2.1284 | Bigram transition matrix, randomized SVD into embedding and head |
| Apr 27 06:55 | worker2 | 1.9319 | 24 prefixes, geometric-mean aggregation |
| Apr 27 13:30 | worker2 | 1.9304 | Per-prefix log-softmax before averaging (18th scored) |
| Apr 28 04:31 | slurm_worker_4 | 1.9228 | Second donor (Cerebras-GPT 111M), variance and naturalness weights |
| Apr 29 11:04 | slurm_worker_2 | 1.9136 | Six donors, 28 single-token contexts |
| May 1 05:10 | worker2 | 1.9062 | One power iteration in the randomized SVD |
| May 1 10:28 | slurm_worker_3 | 1.9043 | Layer-0 attention as uniform causal mean-pool |
| May 3 00:13 | slurm_worker_3 | 1.9028 | First SSM edit: layer-1 band mean-pool, chosen after a landscape read |
| May 5 17:34 | slurm_worker_6 | 1.8995 | Layer-0 feed-forward projection from GPT-2 small |
| May 8 13:24 | slurm_worker_1 | 1.8990 | Cross-band SSM output-projection writes on layers 1, 3, 7 |

## Negative results, lineage, and primary result
**Covers:** §4.5 Negative results, Lineage and reproduction, Primary result

- Verbatim (negative results): "Doubling the prefix set to 48 made the recipe worse, documented with four controlled variants. Flattening the singular-value spectrum, transplanting native Mamba blocks from hybrid donors, copying GPT-2's embedding matrix directly, and building the prior from a donor with another tokenizer (Pythia) all regressed and were published with their scores. The window contains 53 contributions explicitly tagged as negative results."
- Lineage: best contribution has 145 commits in its ancestry by 15 of 17 accounts; 115 of 144 parent edges cross account boundaries. 165 verification contributions cover 95 distinct targets; each names its target, each verifier differs from the author, none reports a failure. Same-hardware reproductions bit-identical; cross-hardware (A100 vs H100) ≤ 1.3×10⁻³ bpb. 40 of the winner's 144 scored ancestors independently reproduced.
- Verbatim (primary result): "Without training data or a single gradient update on the target, the community's best transfer() initializes the frozen 119.6M hybrid to 1.899044 bpb, against 3.3923 for random initialization and about 1.0 for a trained GPT-2 124M, closing 62% of that gap."
- Caveat, verbatim: "the number to trust is the improvement from 3.39 to about 1.90 rather than the final decimal places; the last recorded change moved the score by 9×10⁻⁶, below cross-hardware variation."
- Verbatim mechanism claim: "Donor behavior, compressed into a low-rank transition operator, transfers across architectures where donor parameters do not, and every step of the search that found this is a reproducible commit in a shared graph."

## Coordination dynamics, human intervention, verification (§§4.6–4.8)
**Covers:** §§4.6–4.8 (Figures 4–5)

- Graph: 1,703 nodes, 1,894 edges, 149 multi-parent nodes, one component holding 98.9% of all nodes (Figure 4 force-directed layout; highlighted spine is the ancestry of the eventual leader).
- Four observations: (1) fast exploitation — first 8 improvements ≈ 70% of total descent, first 18 scored ≈ 98%; (2) narrow spine — one lineage collects most follow-on work, side branches short and quickly abandoned; (3) parallel rediscovery — of 696 pairs of different accounts posting identical scores, 63% within an hour, 80% within six (Figure 5); (4) community-level diagnosis — families pile up near 1.90 bpb with a shared explanation that the evaluator is globally linear and sublayers are underused (agents' interpretive claims reported as theirs).
- Verbatim assessment: "This is what the mechanism is supposed to produce: a frontier that moves quickly, later workers building on visible leaders, and cross-branch insight into a common ceiling. It is also a picture of its weaknesses. A shared leaderboard did not stop duplicate work, and the graph is heavily exploitation-biased."
- Human intervention at two points: before the run (task, donor zoo, target architecture, evaluator, brief, project, worker launch) and one change during the run — on May 2, "when the analysis views showed that more than a third of all activity sat in a single semantic cluster and the leaderboard had stalled, we deployed the clustering, diversity summary, and diversity-aware UCB"; workers adopted the views immediately and the first sub-1.90 result came the next morning "by a worker that chose to follow the thin state-space cluster rather than extend the dominant one."
- Verification at three levels: trace (exported full contribution stream and graph from the server, recomputed every count/statistic/figure — no number from agent summaries or leaderboard display); result (checked best score algebraically against reported loss, token count, byte count; confirmed independent cross-hardware reproductions within brief tolerance); method (followed winning commit's import chain back to base module, read code at each step, confirmed no eval-data touch and no gradient-descent update; "Algorithm 1 and Table 3 were written from that reading, not from the agents' prose"). The winning method was not rerun; the primary result is the archived evaluator output corroborated by cross-hardware reproductions.
