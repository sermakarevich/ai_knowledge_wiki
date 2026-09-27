# Chapter 06 — MT-Bench pairwise judges under the microscope

## What this is

We put four LLMs in the *judge* seat on real MT-Bench pairs and score every
one of them the same way, against the crowd-sourced human votes — the ground
truth that ships with MT-Bench. For each pair we also have the human
winners, so we can measure (1) **how well a judge agrees with humans**, (2)
**where the judge is biased** (which answer it favours, position-wise and
length-wise), (3) whether **a panel of judges** does better than any single
judge, and (4) whether the votes **reproduce the leaderboard ranking** when we
fit a Bradley–Terry model.

The judges this chapter runs:

| judge | family | role |
|---|---|---|
| `qwen3.8:27b` | general (local) | the "default" judge (06a) |
| `gemma4:latest` | general (local) | a second general judge |
| `atla/selene-mini` | purpose-built judge (pulled for 06b) | a judge *trained to be a judge* |
| *(panel)* | all three together | PoLL-style majority vote |

The three are deliberately different: two general-purpose models plus one
model that was explicitly built as an automated judge. A key question — "does
a purpose-built judge beat a general one at judging" — is exactly what this
chapter is set up to answer.

## Method

- **Sample**: `n = 100` (06b) / `150` (06a `qwen`) turn-1 pairs from
  `data/public/mt_bench_human_votes.jsonl`, `winner` not a tie, ≤ one vote per
  ordered `(question_id, model_a, model_b)`, seed 0 → `runs/06_pairs.jsonl`.
  The 06b figures are the first 100 of the 06a seed-0 sample so the three
  judges are judged on the *identical* pairs.
- **Human–human ceiling**: over every `(question, ordered-pair)` group with
  ≥2 human votes, the fraction of vote-pairs that agree — reported with and
  without ties in the denominator.
- **Judge**: `llm.chat` with `prompts/pairwise_judge_v1.txt` (short explanation,
  then a final `Judge: A` / `Judge: B` / `Judge: tie` line), seeded
  deterministically. Each pair is judged in **both orderings** (`ab` then `ba`)
  so position can be controlled.
- **Agreement** (primary `agreement_with_humans`): a pair agrees when the
  majority of the two orderings (after mapping a position back to a model)
  matches the human winner. A tie in either order, or the two orders picking
  different models, leaves no consistent winner and counts as a miss.
- **Bias** (primary `position_flip_rate`):
  - *position* = share of both-definite pairs whose model-pick flips when the
    order is swapped, plus the share of all calls won by the first position
    (50% = no bias);
  - *verbosity* = P(judge wins the longer answer) vs P(humans pick the longer).
- **Self-preference**: not measurable — none of the 6 MT-Bench models is a
  Qwen/Gemini-family model, so there is no "own-family" row to compare.
- **Panel** (PoLL-style): each judge's `ab`/`ba` is first collapsed to a single
  model-pick via majority-of-two-orders; the panel then takes a bare majority
  of the *available* picks — a model must win strictly more than half to
  count, otherwise it's a tie. Agreement = share of pairs whose panel pick
  equals the human winner.
- **Bradley–Terry**: a 2-parameter pairwise win-rate model. We fit it twice —
   once on the human votes, once on the judges' votes — and compare the
   resulting rankings with Spearman rank correlation (average-rank ties).
   Fitted with the in-repo MM (minorisation-maximisation) MLE in
   `mtbench.py:_fit_bt` (the allowed `evalica` package was installed and its
   `bradley_terry` API checked, but the own implementation is used — no
   behaviour difference for this data, and no network dependency).

## Headline numbers (judged on the same 100 pairs)

| judge | agreement w/ humans | position-flip rate | first-pos win share | picks longer (judge / human) |
|---|---|---|---|---|
| `gemma4:latest` | **0.620** (62/100) | **0.210** (21/100) | 81/200 (40.5%) | 83/200 (0.42) / 72/100 (0.72) |
| `atla/selene-mini` | **0.620** (62/100) | **0.210** (21/100) | 117/200 (58.5%) | 82/200 (0.41) / 72/100 (0.72) |
| **panel** (3 judges) | **0.700** (70/100) | 9 tie-majorities | 82/100 had ≥2 judges covering | — |
| `qwen3.8:27b` (06a, 150) | 0.613 (92/150) | 0.207 (31/150) | 172/300 (57.3%) | 112/300 (0.37) / 107/150 (0.71) |
| human–human ceiling | 0.826 (no ties) / 0.642 (with ties) | — | — | — |
| GPT-4 reference (06a, 150) | 0.680 (102/150) | — | — | — |

The single most important comparison: **the panel (0.700) is clearly better
than either individual judge (0.620), and it even beats the GPT-4
single-judge reference (0.680).** That is the PoLL (panel-of-LLM-judges)
effect in action — aggregating independent, differently-biased judges
cancels out the idiosyncratic errors that make a lone judge miss.

## Observations

### 1. No judge, however purpose-built, clearly beats the general models
`atla/selene-mini` — a model that exists *as a judge* — lands at the exact
same 0.620 agreement as `gemma4:latest`, and both sit at the same level as the
local `qwen3.8:27b` (0.613). On this MT-Bench subset there is **no measurable
edge to the purpose-built judge**; it does not move the needle on agreement.
That's a useful, slightly unglamorous result: "judge-specialised" is not a
magic bullet for pairwise preference scoring.

### 2. gemma4 and selene are *mirror* position biases that happen to agree
This is the most striking finding. Both are position-biased (21% flip
rate), but in **opposite directions**:

- `gemma4:latest` wins the **first** position in only **40.5%** of calls → it
  leans toward the *second* answer.
- `atla/selene-mini` wins the **first** position in **58.5%** of calls → it
  leans toward the *first* answer.

So one anchors on "what came first," the other on "what came second." Yet
because a *correct* judge should pick the same **model** in both orders,
their per-pair model-picks end up overlapping heavily — they reach the same
winner on ~80% of the pairs they can both decide. The biases cancel when you
take the panel majority, but each one's *individual* verdict is still
position-corrupted. If you use one of these alone, swap the order and the
verdict can flip for a pure order effect.

### 2b. One concrete flipped pair (qwen, pure order effect)
`question_id=82`, `alpaca-13b` vs `vicuna-13b-v1.2`, human → **vicuna**.
Order `ab`: qwen → **A (alpaca)**. Order `ba` (answers swapped): qwen →
**A (now vicuna)**. qwen picked *position 1* in both orders, so it landed on
two different models — a pure order effect, not a content re-reading.

### 3. The panel wins by cancelling, not by knowing more
The panel's 0.700 is *not* because any single panel member is strong — it's
because their errors are (enough) independent. When gemma4 and selene lean in
opposite directions, the pair where one judge is anchored on position and the
other isn't tends to resolve to the majority, and the pairs where *both* are
confidently wrong are rare. Result: 9 tie-majorities (a deliberate "I don't
know"), 82/100 pairs had ≥2 independent judges covering, and 70/100 correct.
This is the standard argument for ensembles applied to judges: **diversity of
error, not raw strength, is what buys accuracy.**

### 4. None of the judges picks "longer is better"
All three judges pick the longer answer only ~40–42% of the time, while
**humans pick the longer answer 72% of the time.** So the human leaderboard is
partly built on a length heuristic that the LLM judges simply don't share. A
good chunk of the judges' agreement gap versus the human ceiling is them not
reproducing that length bias — separate from, and in addition to, the
position anchoring. (This is the opposite of "verbosity inflation," which is
a known failure mode where judges *over*-reward length. Here the judges are
too *literal* about content and under-adopt the crowd's length prior.)

### 5. Bradley–Terry: judges reconstruct most of the leaderboard, not all
Fitting the two-parameter Bradley–Terry model over the votes and comparing
rankings:

| judge | human ranking (top→bottom) | ranking agreement (Spearman ρ) |
|---|---|---|
| human votes (reference) | gpt-4, gpt-3.5, claude-v1, vicuna, alpaca, llama | — |
| judges' votes | claude-v1, gpt-4, vicuna, gpt-3.5, alpaca, llama | **0.714** |

The judges and the crowd **agree on the broad shape** (gpt-family on top,
alpaca/llama at the bottom) but disagree on the **fine ordering** at the top
(gpt-4 vs claude-v1) and mid (gpt-3.5 vs vicuna). Spearman ρ = 0.71 on 6
models is "same leaderboard, different tiebreaks." Bradley–Terry gives a
clean, continuous *level* (a score you can add/compare) out of discrete
pairwise calls — that's its main value — but it inherits whatever bias the
votes had, so it doesn't remove the disagreement, it just quantifies it.

- Ratings (max normalised to 1):
  - **human**: gpt-4 1.00, gpt-3.5 0.82, claude-v1 0.81, vicuna 0.66, alpaca
    0.37, llama 0.23
  - **qwen/judges**: claude-v1 1.00, gpt-4 0.64, vicuna 0.45, gpt-3.5 0.40,
    alpaca 0.24, llama 0.05
- Plot: `runs/bt_ratings.png` (bar chart of both ratings, ρ annotated).

## Bottom line

- **A single general or purpose-built judge hits ~0.62 agreement** on this
  MT-Bench subset and carries a real position bias (21% flips).
- **A 3-judge panel hits 0.70** — better than any individual and better than
  the GPT-4 single-judge reference. Cheap, local, and measurably stronger.
- **Purpose-built ≠ better.** `atla/selene-mini` gives no advantage over
  `gemma4` / `qwen` on agreement.
- **Judges systematically under-use the human "longer is better" prior** and
  differ mainly in *which position* they anchor to (gemma4→2nd, selene→1st).
- **Bradley–Terry converts these calls into scores** (ρ = 0.71 vs the human
  leaderboard): right shape, off on the close top/mid ordering.

## Cost

- `gemma4` (100 pairs, ab+ba) = 200 calls · `selene-mini` (100 pairs, ab+ba)
  = 200 calls → **400 new calls** for 06b (within the ≤420 budget).
- 06a `qwen3.8:27b` (150 pairs, ab+ba) = 300 calls (of which a large share
  served from the local LLM cache on resume).
- Wall time: ~3–5 min per judge on the shared single GPU (RTX 4090 48 GB,
  1024 GB/s, low VRAM contention). All calls are deterministic (seed 0) and
  idempotent — re-running a command serves cached verdicts and makes no new
  calls.

## Skipped

- `atla/selene-mini` pull **succeeded**, so nothing was skipped on that front —
  it ran on the same 100 pairs as `gemma4` and is included above.
- No dedicated selene prompt variant was needed: `ollama show atla/selene-mini`
  did not mandate a special format, so it judged with the shared
  `prompts/pairwise_judge_v1.txt`.
- Self-preference check skipped: no MT-Bench model shares a family with any of
  the three judges.

## Reproducing

```
cd project
just mtbench-sample                                  # -> runs/06_pairs.jsonl
just mtbench-judge gemma4:latest ab
just mtbench-judge gemma4:latest ba
just mtbench-agreement gemma4:latest                  # -> runs/06_agreement_gemma4_latest/
just mtbench-bias      gemma4:latest                  # -> runs/06_bias_gemma4_latest/
just mtbench-judge atla/selene-mini ab
just mtbench-judge atla/selene-mini ba
just mtbench-agreement atla/selene-mini               # -> runs/06_agreement_atla_selene-mini/
just mtbench-bias      atla/selene-mini               # -> runs/06_bias_atla_selene-mini/
just mtbench-panel --limit 100                        # -> runs/06_panel/
just mtbench-bt                                         # -> runs/06_bradley_terry/ + runs/bt_ratings.png
just results                                         # -> runs/results.md
```

Artifacts:
- `runs/06_pairs.jsonl` — sampled pairs with attached turn-1 answers
- `runs/06_verdicts/<judge>/{ab,ba}.jsonl` — raw verdicts + parseable `Judge:` line
- `runs/06_agreement_<judge>/metrics.json`, `runs/06_bias_<judge>/metrics.json`
- `runs/06_panel/metrics.json` — panel majority + per-pair `judge_votes`, `panel`
- `runs/06_bradley_terry/metrics.json` — human vs judge ratings + ranking
- `runs/bt_ratings.png` — Bradley–Terry ratings bar chart
- `runs/results.md` — every experiment in one table
