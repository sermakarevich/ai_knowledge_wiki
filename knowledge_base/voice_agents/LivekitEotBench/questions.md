---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: livekit/eot-bench

### Q1. What per-pause decision does eot-bench evaluate, and what goes wrong when the decision fires too early versus too late?

> [!tip]- Answer
> Every silence pause forces the same live choice — is the user done talking — where firing early talks over the user (false cutoff on a mid-turn hesitation) and waiting late fills the conversation with dead air. eot-bench exists to measure exactly this tradeoff at real pauses in real human-to-agent turns. See [[wiki/01-overview|Overview]].

### Q2. What is the eot-bench dataset, and how is each user turn annotated?

> [!tip]- Answer
> It is the open dataset `livekit/eot-bench-data` of real task-oriented human-to-agent user turns with aligned audio and text context in 14 languages. Each row is one complete user turn annotated with every silence pause of at least 100 ms, where the final pause is the true end of turn and earlier pauses are mid-turn holds. See [[wiki/01-overview|Overview]].

### Q3. Why does eot-bench rank models by the false-cutoff vs. latency tradeoff instead of a single accuracy score, and what does "latency" mean here?

> [!tip]- Answer
> Either goal alone is trivial — wait forever to never interrupt, or fire instantly to never wait — so the benchmark sweeps the endpointing policy and reports best latency at fixed cutoff budgets, best cutoffs at fixed latency budgets, and the full Pareto frontier. Latency is conversational dead air after a true turn ending, not model inference or compute time. See [[wiki/01-overview|Overview]].

### Q4. How does the span-level evaluation work, and what three policy knobs are swept to produce operating points?

> [!tip]- Answer
> Each turn's silence spans of 100 ms or more are labeled `eot` for the final span and `hold` for earlier ones, and the adapter may use only audio, transcript, and messages available by time `t` for a causal prediction at `t`. The sweep varies `threshold` (confidence to end the turn), `action_delay` (minimum silence before acting), and `timeout` (maximum hold before forcing end-of-turn). See [[wiki/01-overview|Overview]].

### Q5. Which model leads the eot-bench leaderboard, and what role does the silence-only VAD baseline play?

> [!tip]- Answer
> LiveKit Turn Detector v1 posts the strongest overall results in English and across all 14 languages, for example 9.9% false cutoffs at a 300 ms latency budget in English, with reproducible artifacts committed under `output/`. The silence-only VAD baseline runs through the identical evaluation and policy grid so every learned and commercial detector is measured against what timing alone achieves. See [[wiki/01-overview|Overview]].

### Q6. What lives at the eot-bench repo top level, and what does each file exclude or pin?

> [!tip]- Answer
> The top level carries no executable code, only a 20-line `.gitignore` and a 14-line `requirements.txt`. The `.gitignore` excludes OS and Python byproducts, local virtualenvs, Hugging Face caches, secrets such as `.env` files, and generated trees like `eot_harness/output/` and `tmp/`, while `requirements.txt` pins the data, audio, and eval stack including `datasets`, `librosa`, `soundfile`, `scikit-learn`, and `websockets`. See [[wiki/02-top-level-files|top-level-files]].

### Q7. A voice-agent team must pick an eot-bench operating point for a customer-support bot where interruptions are costly: which budget should they optimize and why?

> [!tip]- Answer
> They should fix a strict low false-cutoff budget such as 5% and then minimize latency at that budget, accepting longer dead air to avoid talking over callers. This follows the benchmark's own framing that the right tradeoff depends on product cost, and its headline view reports dead air at a fixed interruption budget with lower-left Pareto positions preferred. See [[wiki/01-overview|Overview]].
