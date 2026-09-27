# Jev (TypeSafe) tutorial

**Jev** is the model behind [TypeSafe](https://docs.typesafe.ai/introduction). It is a *System One* model: it does not generate text. You send it **state** (any text or JSON — a message, a record, a source file) plus **typed questions**, and it returns **numbers your code can use directly**. Three question types exist:

| Type | You ask | You get |
|---|---|---|
| `Choice` | pick one option from a labelled list | `choice`, `probabilities` per option, `confidence` |
| `Score` | rate the state on an ordered rubric | `score` (may land between levels), `probabilities`, `confidence` |
| `Noul` | is this statement true? | `noul`, a number 0 (no) … 1 (yes) |

Because there is no text generation the calls are fast (whole notebook including a 200-file scan runs in ~30 s), cheap (~$0.04 per million input tokens; the whole notebook costs about 2 cents) and every question in a request is evaluated in parallel against the same state.

Abbreviations: **API** = Application Programming Interface (the HTTP service); **SDK** = Software Development Kit (the `typesafe-sdk` Python package); **JSON** = JavaScript Object Notation; **ADR** = Architecture Decision Record.

## What this project contains

- `jev_tutorial.ipynb` — how to *use* Jev (36 cells, outputs saved so it can be read without running).
- `jev_eval_tutorial.ipynb` — how to *test* Jev's accuracy and sensitivity before trusting it (37 cells, outputs saved).
- `build_notebook.py` / `build_eval_notebook.py` — generate the two notebooks with `nbformat`; edit these, then `just build` / `just build-eval`. Keeping the source in `.py` files makes diffs readable.
- `justfile` — recipes (below). `pyproject.toml` — `uv` project (`typesafe-sdk`, `jupyterlab`, `pandas`, `nbconvert`).
- `fleet_cache/` (gitignored) — one JSON file per API answer for section 4 of `jev_tutorial.ipynb`.
- `eval_cache/` (gitignored) — one JSON file per API answer for `jev_eval_tutorial.ipynb`, keyed by a hash of the request.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) and [`just`](https://github.com/casey/just).
- A TypeSafe API key from https://console.typesafe.ai/settings/keys exported as `TYPESAFE_API_KEY` (already set in Sergii's shell). The SDK also reads `TYPESAFE_BASE_URL`, `TYPESAFE_DEFAULT_MODEL` (default `jev-latest`) and `TYPESAFE_LOG_LEVEL`.
- `~/git/fleet` checked out (only for section 4).

## Run it

```bash
cd ~/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/jev
just install     # uv sync
just check-key   # fails if TYPESAFE_API_KEY is missing
just models      # lists models: jev-latest, jev-preview
just jupyter     # JupyterLab on http://localhost:8899, notebook opened
just run         # execute headless (nbconvert --execute --inplace)
just clean       # strip outputs
just build       # regenerate jev_tutorial.ipynb from build_notebook.py

just jupyter-eval  # JupyterLab with jev_eval_tutorial.ipynb opened
just run-eval      # execute jev_eval_tutorial.ipynb headless
just clean-eval    # strip its outputs
just build-eval    # regenerate jev_eval_tutorial.ipynb from build_eval_notebook.py
```

## Notebook walkthrough

**1. Setup** — imports, key check, a shared `USAGE` counter, `TypeSafeClient(retry=RetryPolicy(...))`, `client.models.list()`.

**2. Basic examples (straight from the docs)**
- 2.1 Quick-start ticket: one call, `Choice` (department) + `Score` (frustration) + `Noul` (urgency).
- 2.2 Inside an answer: `probabilities`, `confidence`, `legend`, `request_id`, `usage`; the typed views `response.choices/scores/nouls`.
- 2.3 State as a dict: conversation + order + policy in one state; questions that compare parts of it.
- 2.4 Structured instructions/criteria (`{"what": ..., "not_for": ..., "examples": [...]}`) to sharpen option boundaries.
- 2.5 Raw dict questions (`{"type": "noul", ...}`), `extra_body`, per-call `RetryPolicy`, catching `TypeSafeAPIError` (`.status`, `.request_id`), logging.
- 2.6 `AsyncTypeSafeClient` with `asyncio.gather` (top-level `await` works in Jupyter).

**3. Patterns**
- 3.1 Confidence-gated routing: below a floor → human; above it, the threshold to act automatically scales with the stakes.
- 3.2 Composite scoring: one `Score` per factor, combine in code with explicit weights (`senior_ic` vs `eng_manager` weightings).
- 3.3 Speculative fan-out: ask every possibly-needed question in one request, let code pick which answers matter.

**4. Advanced — "Jev, how should I improve `fleet`?"**
Jev cannot write advice, so the question is rephrased so Jev is the *judge* and we supply the *candidates*:
- 4.1 **Scorecard**: state = README + OVERVIEW + ARCHITECTURE (trimmed) + ADR list + lines-of-code per package (~47k chars). Nine `Score` dimensions on one 0–4 rubric plus five risk `Noul`s. Result on 2026-09-16: strongest = modularity 3.99, failure_handling 3.91, docs 3.80; weakest = scalability 1.70, security_posture 1.79, cost_control 1.98. `hard_bd_dependency` 0.97 true; `single_machine_limit` 0.49 (undecided).
- 4.2 **Which area first?**: one `Choice` over nine improvement areas. Top pick `ui_security` 0.42, then `multi_machine` 0.29, `smarter_retries` 0.13 — with confidence 0.34, i.e. it is a close call, so read the distribution rather than the top pick.
- 4.3 **Ranked backlog**: 12 hand-written improvement ideas, each judged on `impact`, `effort`, `risk` (0–4 → 0–1), `fits_philosophy` and `already_exists` (Nouls); `priority = 0.45·impact + 0.25·(1−effort) + 0.15·(1−risk) + 0.15·fits`. Top 3: evaluation harness (0.64), per-attempt cost tracking (0.61), Slack integration (0.59). Bottom: splitting the two biggest files (0.33, low impact).
- 4.4 **Per-file scan**: all 199 `.py` files under `src/fleet` (skipping `__pycache__`, `node_modules`), 8 concurrent requests, questions taken from fleet's own ADR 0006 rules (function > ~40 lines, if-chain dispatch, mixed abstraction levels, hard to test) plus `refactor_need`, `readability` and a `biggest_issue` Choice. Top files by refactor need: `orchestrator/supervisor.py`, `state/archive.py`, `schedules/firing.py`, `state/journal.py`, `orchestrator/triage.py`. Most common "biggest issue": `error_handling` (74 files), then `none` (49), `duplication` (36), `coupling` (30).
- 4.5 **Hand-off**: prints a ready `fleet bd create ...` command that turns the top-5 files into a fleet task, so the loop "Jev ranks → coder fixes → tests validate" can run unattended.

**5. Cost** — `USAGE` totals and an estimated dollar cost (price constant hard-coded from the TypeSafe cookbook; check the pricing page).

## `jev_eval_tutorial.ipynb`: testing accuracy and sensitivity

Answers two questions the docs and public write-ups (see below) explicitly leave open: is Jev
*accurate* when the correct answer is objectively known, and is it *sensitive* the right amount —
stable under meaning-preserving edits, responsive to real changes?

**1. Setup + noise floor** — same client pattern, plus a disk cache keyed by a hash of the request. Repeats the exact same call 8× to measure how much an answer jitters with **zero** change to the input, so later drift can be judged against a real baseline instead of against zero.

**2. Accuracy**, on tasks with a *computable* ground truth (no human labelling):
- 2.1 Numeric comparison (`Noul`): "is A bigger than B" for random number pairs.
- 2.2 Unambiguous keyword routing (`Choice`): the ticket names its own department; a floor test.
- 2.3 Rule-following (`Score`): the scoring rule is stated in the instructions and the state gives an exact count, isolating instruction-following from judgment.
- 2.4 Negation trap (`Noul`): matched affirmative/negated sentence pairs, to check Jev does not invert on "does NOT".

**3. Calibration** — pools (confidence, correctness) from the tasks above that carry a `confidence`, bins by confidence, and reports a reliability table plus an expected calibration error. On the run baked into the notebook (2026-09-19): 100% accuracy on all four tasks, ECE 0.001 — but with only ~50 pooled points this is a demonstration of the method, not a production audit; widen `N_PER_TASK` for a tighter read.

**4. Invariance** — one clear-cut example per primitive, perturbed with paraphrase, irrelevant preamble/suffix, reordered `Choice` criteria dict, casing, and a distractor sentence. None moved the answer or exceeded 2× the noise floor in the baked run — but note the caveat in the notebook: a base case already at `p = 1.0` is at a ceiling and cannot show drift even if it exists.

**5. Discrimination**:
- 5.1 A controlled dial (0–5 anger markers inserted into a fixed template) → frustration `Score`; Spearman correlation 0.94 in the baked run.
- 5.2 A decision-boundary sweep mixing a billing sentence and a technical sentence in five ratios; `p(technical)` climbs from 0.00 to 0.98 and confidence dips near the 50/50 mix.
- 5.3 A distractor-flood test: the same signal sentence buried in 0/2k/8k/20k characters of filler; the correct answer survived in the baked run.

**6. Scorecard** — one table combining every check above with a pass/fail bar.

Two bugs found and fixed while building this notebook, worth knowing if you extend it: an early version of the routing test (2.2) paired every department's template with every detail regardless of topic, producing self-contradictory tickets and a false 44% "accuracy"; and an early negation-trap instruction (2.4) was itself phrased with a confusing double negative, which looked like a genuine 50% negation-blindness finding until the wording was cleaned up (both now 100%). Neither was a real Jev weakness — a reminder that a badly designed test produces a confident, wrong verdict just as easily as a well-designed one does.

### Why this notebook exists

Public reviews after Jev's September 2026 launch converge on the same gap. TypeSafe's own 711-case dashboard reports 67.8% aggregate accuracy against a reference built from averaging two other LLMs' answers, not human ground truth — describing agreement, not correctness. [pearpages.com's review](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim) states plainly that "the documentation contains no calibration curves, no Brier scores and no reliability diagrams," and that sensitivity to input changes is "completely unknown" outside TypeSafe's own four workflows. A hands-on test at [paddo.dev](https://paddo.dev/blog/thirty-cent-judge) ran Jev over 9,081 real low-confidence product-matching pairs and manually checked 50 verdicts (48 held up), but explicitly stopped short of a calibration claim for the same reason — one small hand-checked sample cannot establish that a 0.9 is right 90% of the time. `jev_eval_tutorial.ipynb` builds the missing pieces using synthetic tasks with a computable ground truth, so accuracy and calibration can be measured at a sample size a human cannot label by hand.

## Key concepts

- **System One model** — a model that answers typed questions with probabilities instead of generating text. Think "panel of judges", not "writer".
- **State** — the material to judge. Prefer a dict with descriptive keys; keep *content* in state and *judgment* in questions.
- **Confidence** — a single 0–1 number derived from the shape of `probabilities` (Choice/Score only). Low confidence is a signal ("I don't know"), not noise.
- **Request budget** — about 32,000 tokens (~150,000 characters) shared by state + questions per request. The notebook's `fit()` helper truncates to stay under it.
- **Judge vs. writer** — for open questions ("how do I improve X?"), a text LLM (or you) brainstorms candidates and rubrics; Jev ranks them consistently and cheaply, and the numbers can be tracked over time.

## Gotchas / notes

- `model` in the response reports the concrete version (`jev-1.13.0`) even when you asked for `jev-latest`.
- `Score.criteria` is an ordered list: index 0 is level 0. The `legend` field on the answer maps indices back to text.
- Questions with only a `Noul` answer have no `confidence`; use the distance from 0.5 as a rough proxy if you need one.
- Wrong model name → `TypeSafeBadRequestError` (HTTP 400), not a 404.
- nbconvert executes top-level `await` fine; running the generator with plain `python` would not (it only writes cells, so that is fine).
- `fleet_cache/` and `eval_cache/` pin results; delete a file there (or the folder) to re-judge.

## Further reading

- [TypeSafe docs](https://docs.typesafe.ai/introduction) · [Quick start](https://docs.typesafe.ai/introduction/quickstart) · [Python SDK usage](https://docs.typesafe.ai/sdk/python/usage) · [Confidence](https://docs.typesafe.ai/confidence) · [Patterns](https://docs.typesafe.ai/patterns) · [Cookbooks](https://docs.typesafe.ai/cookbooks/parallel_questions) · full index: https://docs.typesafe.ai/llms.txt
- Claude Code skill: `claude plugin marketplace add typesafe-ai/skills && claude plugin install typesafe@typesafe-ai`
- fleet docs: `~/git/fleet/docs/OVERVIEW.md`, `docs/ARCHITECTURE.md`, `docs/adr/`

## Command-line tool

The same calls are available from the shell via `jev` (source `~/git/ai_tools/jev`, install with `uv tool install --editable ~/git/ai_tools/jev`):

```
jev choose "Which team?" -o billing -o tech -s "invoice is wrong"          # Choice
jev score  "How severe?" -l "cosmetic" -l "blocks a task" -l "data loss" -s @bug.txt   # Score
jev check  "Is this spam?" -s -                                          # Noul, state from stdin
jev ask    questions.json -s '{"post": "...", "reply": "..."}'          # many questions, one request
```

JSON on stdout; `--format md` for a summary; `--min-confidence 0.7` exits 2 when Jev is unsure.
