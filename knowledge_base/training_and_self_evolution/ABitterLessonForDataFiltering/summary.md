# A Bitter Lesson for Data Filtering

**Paper:** [A Bitter Lesson for Data Filtering (Mohri, Duchi, Hashimoto, 2026)](https://arxiv.org/abs/2605.19407)

## Human Readable TL;DR

Imagine you're teaching someone by giving them books: most people would carefully hand-pick only the best, clearest books and throw out the trashy ones. This paper finds that if you're a big enough brain (a large AI model) and have enough study time (compute), it's actually better to read everything -- even garbage. Sorting through books to pick only the "good" ones is expensive and ultimately wasteful: a smart enough student can figure out on their own what's worth learning and what isn't.

## TL;DR

This paper empirically challenges the standard practice of filtering pretraining data for large language models. Training Llama-style transformers at sufficient scale (330M+ parameters) on raw, unfiltered Common Crawl outperforms all tested filtered variants, including DCLM-Baseline. Large models are also surprisingly robust to deliberately injected junk data (random strings, shuffled words). Scaling law extrapolations predict the full 240T-token Common Crawl becomes optimal at ~1e+30 FLOPs.

---

## Problem & Motivation

Data filtering is near-universal in LLM pretraining: pipelines like DCLM-Baseline keep only ~2% of raw Common Crawl, discarding the rest as "low quality." But filtering removes data, which conflicts with scaling trends that demand ever-increasing token counts. At frontier model sizes (1T+ parameters), even heavily filtered datasets like DCLM's 3.8T tokens fall short of the Chinchilla-optimal token budget. The authors ask: is data filtering actually necessary, or is it a compute-constrained heuristic that breaks down at scale?

---

## Main Original Ideas

1. **No-filter as the asymptotically optimal strategy** -- For sufficiently large models and compute budgets, training directly on raw Common Crawl (no filtering at all) outperforms every tested filtering strategy. This frames data filtering as another instance of Sutton's "bitter lesson": human-designed heuristics that work at small scale get overtaken by simpler, compute-scalable methods.

2. **Compute-performance Pareto frontier analysis** -- Instead of comparing datasets at fixed compute, the authors find the best achievable loss $L^*(D) = \min_{M,N} \ell(A(D,M,N))$ for each dataset, constructing Pareto frontiers that reveal crossing points where unfiltered CC overtakes filtered variants.

3. **Junk data injection experiments** -- Synthetic low-quality data (random strings from a 10k-word vocabulary; CC documents with shuffled word order) is deliberately mixed into training sets at up to 800% of the base pool size. Results show large models absorb this noise without catastrophic degradation.

4. **Scaling laws for when unfiltered data wins** -- The authors derive scaling laws predicting $N^*(M, m)$ -- the minimum training steps for the raw CC pool to beat RefinedWeb -- across model and pool sizes, then extrapolate to the full 240T-token DCLM-Pool.

5. **Theoretical grounding via linear matrix factorization** -- A toy model with orthogonal inputs shows that when model rank $\geq$ number of distinct tasks, noise distributions are absorbed without performance loss. This explains empirically why model capacity is the critical threshold.

---

## Key Findings

| Setting | Result |
|---|---|
| 330M+ param models, 670M-token CC pool | Raw CC outperforms all 5 filtered variants (English, Repetition, Stop Words, RefinedWeb, DCLM-Baseline) |
| Compute-Pareto frontier | Raw CC goes from worst (low compute) to best (high compute); repetition filter never appears on the Pareto frontier |
| Junk injection: shuffled words, +400% pool | 330M model trained on shuffled-augmented data *surpasses* pure CC (unigram signal preserved) |
| Junk injection: random strings | Performance gap vs. pure CC closes as model size increases |
| Full 240T-token DCLM-Pool extrapolation | Raw CC becomes optimal at ~1e+30 FLOPs (~reachable near-future compute by some forecasts) |
| Initial token prediction | Shuffled data degrades prediction of first 1/4/16 tokens (distribution shift), but negligible for typical LM use |
| Factual content in CC (MMLU-related docs, GPT-4o-mini analysis) | Supporting content outnumbers refuting by >10x -- actively harmful misinformation is relatively rare |

- The crossing point (where raw CC overtakes filtered) comes earlier (fewer total tokens) as model size grows.
- Smaller models (80M params) never show a crossing point on the 10B-token pool, confirming a minimum capacity threshold.
- Epoch count required for raw CC to win *decreases* with larger models but *increases* super-linearly with larger pool sizes.

---

## Suggestions & Future Directions

1. **Explore non-dense architectures** -- Results focus on vanilla dense transformers. Mixture-of-Experts models may respond differently to unfiltered data and warrant dedicated scaling studies.
2. **Include data curricula and post-training** -- This work studies pretraining in isolation. Filtering effects may interact non-trivially with supervised fine-tuning, RLHF, and instruction tuning stages.
3. **AI-generated content in web crawls** -- As synthetic text increasingly populates the web, the assumption that CC is merely noisy (but human-generated) may break down. Future work should study model-generated contamination.
4. **Rare adversarial or toxic content** -- While factually refuting content is rare in aggregate, concentrated harmful data pockets could still degrade targeted capabilities and deserve further investigation.
5. **Push to frontier compute** -- The ~1e+30 FLOP prediction is a concrete experimental target; direct validation at scale would settle the question empirically rather than by extrapolation.

---

## Authors & Institutions

Christopher Mohri (Stanford CS), John Duchi (Stanford Statistics & EE), Tatsunori Hashimoto (Stanford CS)
