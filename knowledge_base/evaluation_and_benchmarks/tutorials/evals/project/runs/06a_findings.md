# Chapter 06a — MT-Bench: qwen3.8:27b as a pairwise judge (first half)

## What this is

The first half of chapter 06. We treat the local model `qwen3.8:27b` as a
pairwise judge and test it against the real MT-Bench crowd-sourced votes:
over a fixed seed-0 sample of 150 turn-1 non-tie pairs, we (1) measure the
human–human ceiling, (2) have qwen judge each pair in **both orderings**
(`ab` and `ba`, 300 calls) so position can be controlled, and (3) score
qwen's agreement with humans and its position/verbosity bias. GPT-4's
agreement on the same 150 pairs is reported as a reference.

This is the **qwen half** of task `fleet-uo3ez`; the **other half**
(06b) runs gemma4 + a purpose-built judge (selene-mini), adds a PoLL-style
panel, and fits Bradley–Terry ratings.

## Method

- **Sample**: 150 turn-1 pairs from
  `data/public/mt_bench_human_votes.jsonl`, `winner` not a tie, ≤ one vote per
  `(question_id, model_a, model_b)`, seed 0 → `runs/06_pairs.jsonl`.
- **Human–human ceiling**: over every `(question, pair)` with ≥2 human votes,
  the fraction of vote-pairs that pick the same winner — reported with and
  without ties in the denominator.
- **Judge**: `llm.chat` with `prompts/pairwise_judge_v1.txt` (short
  explanation, then a final `Judge: A` / `Judge: B` / `Judge: tie` line),
  seeded deterministically. Run in order `ab` then order `ba` so each pair is
  judged twice with the answers swapped.
- **Agreement** (primary `agreement_with_humans`): a pair agrees when the
  majority of the two orderings (after mapping a position back to a model)
  matches the human winner. A tie in either order, or the two orders picking
  different models, leaves no consistent winner and counts as a miss.
- **Bias** (primary `position_flip_rate`):
  - *position* = share of both-definite pairs whose model-pick flips when the
    order is swapped, plus the share of the 300 calls won by the first position
    (50% = no bias);
  - *verbosity* = P(judge wins the longer answer) vs P(humans pick the longer).
- **Self-preference**: not measurable — none of the 6 MT-Bench models is a
  Qwen family model, so there is no "own-family" row to compare against.

## Headline numbers (150 pairs)

| metric | qwen3.8:27b | human–human ceiling | GPT-4 |
|---|---|---|---|
| agreement with humans | **0.613** (92/150) | 0.826 (no ties) / 0.642 (with ties) | **0.680** (102/150) |
| position-flip rate | **0.207** (31/150) | — | — |
| first-position win share (of 300) | 0.573 (172/300) | — | — |
| P(judge picks the longer answer) | 0.373 | 0.713 (humans) | — |

## Observations

- **qwen is *below* the GPT-4 reference and slightly below the "with ties"
  human–human ceiling.** 0.613 vs GPT-4's 0.680 vs human 0.642/0.826. Against
  the no-tie ceiling (0.826) qwen trails by more than 20 points — meaning a
  non-trivial share of qwen's misses are pairs humans themselves would agree
  on. The gap to GPT-4 (≈ 7 points) is the more useful read: it is a
  competent but clearly second-tier judge on this task.
- **Position anchoring is the single biggest bias, and it's large.** 1 in 5
  both-definite pairs (31/150) reverse their model-pick purely by the order
  the two answers appear in. Every one of those 31 flips has the *same* A/B
  label in both orderings — qwen locked onto the first position, so which
  model it "picks" changes with the swap. That's textbook position bias.
- **First position wins 57.3% of the 300 calls** (172/300), a 14-point
  asymmetry over the 50% no-bias line. Consistent with the high flip rate:
  qwen is not position-neutral.
- **qwen has essentially no verbosity bias — in fact it leans the *other*
  way.** Humans pick the longer answer 71.3% of the time; qwen picks the
  longer answer only 37.3% of the time. Where the crowd skews to "longer is
  better", qwen is close to a coin-flip and even slightly under-weights length.
  So a large share of qwen's misses vs the human ceiling come from *not*
  adopting the human length heuristic, on top of the position anchoring.
- **One concrete flipped pair** (both orders picked the same position, so the
  model flipped):
  - `question_id=82`, `alpaca-13b` vs `vicuna-13b-v1.2`, human → **vicuna**.
    order `ab`: qwen→ **A (alpaca)**. order `ba` (answers swapped): qwen→
    **A (now vicuna)**. qwen judged position 1 both times, so it landed on
    different models — a pure order effect.
- **Robustness fix made during the run**: early on one `ba` reply hit
  `max_tokens` mid-explanation and ended without a `Judge:` line. `parse_verdict`
  previously raised `ValueError`, which would have aborted a 300-call batch.
  It now degrades that one unparseable reply to a `tie` (treated as "no
  confident pick") instead of killing the run. The affected reply is in the
  LLM cache and re-parsed cleanly on resume — no extra calls.

## Cost

- 300 new/total chat calls (150 `ab` + 150 `ba`); on resume, 28 `ba` were served
  from the local LLM cache and 122 were new.
- Wall time for the two-order judging pass ≈ 758 s (ab + ba, single GPU).

## Reproducing

```
cd project
just mtbench-sample            # -> runs/06_pairs.jsonl + human–human ceiling
just mtbench-judge qwen3.8:27b ab
just mtbench-judge qwen3.8:27b ba
just mtbench-agreement qwen3.8:27b   # -> runs/06_agreement_qwen3.8_27b/
just mtbench-bias      qwen3.8:27b   # -> runs/06_bias_qwen3.8_27b/
just results
```

Artifacts: `runs/06_pairs.jsonl` (150 pairs w/ attached answers),
`runs/06_verdicts/qwen3.8:27b/{ab,ba}.jsonl` (verdicts, 150 each),
`runs/06_agreement_qwen3.8_27b/metrics.json`, `runs/06_bias_qwen3.8_27b/metrics.json`
(demo `flipped_pairs`, `first_position_win_share`, verbosity rates).

## What 06b still needs

- Run the same `judge`/`agreement`/`bias` for `gemma4:latest` (cheaper) and,
  if the pull succeeds, `atla/selene-mini` (the one allowed `ollama pull`),
  recording whether a purpose-built judge beats qwen.
- Add the **PoLL panel** and **Bradley–Terry** ratings from judge votes, and
  check they reproduce the human ranking; then write the final `06_findings.md`.
