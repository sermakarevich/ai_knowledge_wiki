---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Agora: Git as Shared Memory for Collective AutoResearch

### Q1. What coordination problem does Agora solve, and what is its core data structure?

> [!tip]- Answer
> Parallel coding-agent sessions each start from scratch, so adding workers produces duplicated search rather than more discovery, with failures and lineage stuck in transcripts or temp worktrees. Agora answers with an append-only DAG (directed acyclic graph — a graph of nodes and "builds on" edges with no cycles) stored in Git, where every result, insight, hypothesis, verification, and report is an immutable commit whose parent edges say what it builds on. See [[wiki/01-agora-overview|Agora Overview]].

### Q2. How does Agora differ from existing multi-agent frameworks and autonomous research agents?

> [!tip]- Answer
> Frameworks like role-play, programmed conversations, and orchestrators coordinate a team inside one application or episode, and single-agent researchers automate one end-to-end pipeline. Agora is complementary: it prescribes no researcher, role graph, manager, runtime, or shared filesystem, and instead keeps durable shared state — negative results, lineage, verification — across independently scheduled, asynchronous participants. See [[wiki/01-agora-overview|Agora Overview]].

### Q3. How is node quality computed in Agora's contribution graph, and why is it not a "truth signal"?

> [!tip]- Answer
> Each node v = (h, a, T, d, x, m, P, τ) carries its commit hash, account, tags, description, metadata, metric, parents, and timestamp, and its evidence score S(u) sums tag weights of follow-on work from other accounts: +5 for setup/result/insight/hypothesis/report, +20/+10/−20 for verification confirmed/partial/failed, 0 for endorsed/wip, with self-citations excluded and only the newest verification verdict counting. It is not a truth signal but an actionability signal: work others reproduced or built on is more actionable than work merely voted for. See [[wiki/02-exploration-quality-diversity|Exploration and Quality Diversity]].

### Q4. What does the analyze call return, and why is "a leaderboard a good exploitation signal and a poor map"?

> [!tip]- Answer
> A leaderboard pulls every worker toward the same parent, hides negative results, and makes a saturated basin look like progress, so analyze returns many views at once: metric leaders, most built-on nodes, leaves, underexplored/unverified/contested results, open hypotheses, activity, tags, and contributors. Once embedding coverage reaches 50%, it adds single-link clusters (cosine threshold 0.90, capped at 5,000 recent contributions) with cluster counts, top-cluster share, entropy-based effective count, evenness, metric histogram, and a small-cluster frontier. See [[wiki/02-exploration-quality-diversity|Exploration and Quality Diversity]].

### Q5. What goes into the diversity-aware UCB (upper-confidence-bound) score, and what are the three attention slots?

> [!tip]- Answer
> The candidate score U(v) combines quality percentile Q(v), follow-on-work count n(v) out of N overall, near-duplicate count ρ(v), and an exploration constant C that grows when the metric distribution bunches near its best. Candidates appear in three slots — exploit (reproduce/refine leaders), explore known (extend promising work in a thin cluster), explore novel (inspect untouched nodes in singleton or tiny clusters) — because the split matters more than the exact score for exposing the explore–exploit trade-off and monoculture collapse. See [[wiki/03-diversity-ucb-attention|Diversity-aware UCB]].

### Q6. What was the weight-transfer task, how was it scored, and who did the work?

> [!tip]- Answer
> The task asked how much predictive quality could be recovered in a frozen 119.6M-parameter 14-layer attention-SSM (state-space model) hybrid matching no donor, using only weights and forward passes of 141 donor models, with no training corpus and no gradient update. The evaluator seeds all RNGs (random-number generators) with 42, runs the submitted transfer() function, and scores 200 FineWeb-Edu texts as summed next-token loss divided by UTF-8 byte count (random init 3.3923 bpb, trained GPT-2 124M ~1.0, aspirational target below 2.5). Thirteen worker accounts wrote 1,699 of 1,703 contributions over 11 days 19 hours (April 26–May 8), sustaining ~170 contributions/day with 233 new bests. See [[wiki/03-diversity-ucb-attention|Diversity-aware UCB]].

### Q7. What are Stage A and Stage B of the winning transfer() recipe?

> [!tip]- Answer
> Stage A builds a 50257×50257 bigram log-prob table M from 6 GPT-2-vocabulary donors over 28 single-token contexts (clipped ±25 log-softmax, variance/naturalness weights, 0.725 donor weight on GPT-2 small), splits off the column mean u, and factorises the centred table by randomized SVD (singular-value decomposition — a matrix factorisation into ranked components) at rank 671 to set the embedding and output head with sublayers zeroed. Stage B wires fixed routes without learning: even attention layers become uniform causal mean-pools on 96-dimensional bands, layer-0 SwiGLU gets a 0.009-scaled GPT-2-small MLP projection, and odd SSM layers run gated depthwise convolutions with recurrence off. See [[wiki/04-weight-transfer-recipe|Weight-Transfer Recipe]].

### Q8. How did the search trajectory unfold, and what role did negative results and reproduction play?

> [!tip]- Answer
> Slice-copying weights scored 4.68 (worse than random, published as a negative result), then a unigram prior hit 2.52 within 30 minutes and bigram statistics reached ~1.93 within six hours, so the first 18 scored contributions delivered ~98% of the total reduction to the cutoff best of 1.899044 bpb, closing 62% of the gap to a trained GPT-2. Fifty-three tagged negative results (48 prefixes, flattened spectra, transplanted Mamba blocks, Pythia tokenizer) plus a 145-commit cross-account lineage and 165 independent verifications (95 targets, zero failures, bit-identical on same hardware) made the result auditable. See [[wiki/04-weight-transfer-recipe|Weight-Transfer Recipe]].

### Q9. What is the paper's conclusion about scaling researchers, and what evidence supports the "binding constraint" interpretation?

> [!tip]- Answer
> The thesis is that scaling autonomous researchers without scaling their institution turns compute into duplicated search, answered by three rules: every contribution durable, addressable, and linked; reproduction and downstream use, not votes, set quality; every participant sees neglected branches alongside leaders. Evidence: for five days agents refined one recipe by 10⁻⁵ bpb per step reading the same leaderboard, then left that basin within a day of the May 2 diversity-map intervention — suggesting the coordination layer, not the individual agent, was the binding constraint. See [[wiki/05-conclusion-coordination|Conclusion]].

### Q10. What must a retained community run preserve, and what does a minimal contribution record contain?

> [!tip]- Answer
> A retained run must preserve seven immutable identity groups: project instructions and scoring policy; code revisions including dirty-worktree state; model/data/hardware identities; prompts, seeds, and compute budgets; the full contribution DAG (directed acyclic graph); event-level evaluator outputs; and frozen aggregation code. The minimal record shared by light (metadata-only) and heavy (code-bundle) paths carries project, agent_id, parent_hashes, tags, description, and a value block with metric_value, run_manifest, and prediction — e.g. worker-7 reporting 1.905 for a six-donor blend — while a verification must add target hash, reproduction config, evaluator identity, and reproduced value. See [[wiki/06-references|References and Appendices]].

### Q11. (Evaluation) Your lab runs parallel coding agents that keep rediscovering the same solution. Should you adopt Agora, and how would you prove it helps?

> [!tip]- Answer
> Adopt it only provisionally: the paper's run never settled causality since the same models and compute were never run without Agora or with a plain leaderboard, so the monoculture escape could reflect the map rather than the DAG (directed acyclic graph) itself. The decisive test is the Appendix C matched comparison — identical agents, models, compute, evaluator, and wall-clock budget across Isolated, Flat-log, Central-planner, and Agora arms, scored at the whole-community-run level — and only a win there justifies the infrastructure cost. See [[wiki/06-references|References and Appendices]].
