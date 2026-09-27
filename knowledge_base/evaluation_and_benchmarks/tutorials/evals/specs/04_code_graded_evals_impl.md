# Task: chapter 04 impl — code-graded evals, `metrics.json` writer and `just results` (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` ("Data contracts", "Results table columns"),
`project/src/evals_tutorial/helpdesk.py` (`load_traces` and the trace/ticket loaders only),
`project/src/evals_tutorial/llm.py` (`embed*`, `count_tokens` signatures) and
`research/SOURCES_practitioner.md` (section on "three levels of evaluation" / unit tests only). Do not
read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Nothing yet turns traces into numbers. The tutorial needs (a) the shared results plumbing every later
chapter uses — a `metrics.json` writer and `just results` → `project/runs/results.md` — and (b) the
cheapest tier of evals: pure code (no LLM). Level-1 evals (Hamel Husain: "unit tests") are deterministic
assertions: schema validity, classification metrics for `triage`, verifiable instructions (IFEval style:
"under 120 words", "cite a section", "no phone numbers"), exact/keyword/regex matches, plus the two classic
text-similarity metrics (ROUGE-L and embedding cosine to the gold answer points) so a later chapter can
show why they fail for free text.

## Fix

### `project/src/evals_tutorial/results.py` (Typer: `write`, `build`) — the shared plumbing
- `write_metrics(experiment, chapter, n, metrics: dict, ci: dict | None, llm_calls, seconds, details,
  predictions: list[dict], config: dict)` → writes `project/runs/<experiment>/{metrics.json,
  predictions.jsonl, config.json}` exactly per the `index.md` schema; also records `primary` (metric name)
  and `notes` (short string) inside `details`.
- `build` → scans `project/runs/*/metrics.json`, sorts by chapter then experiment and rewrites
  `project/runs/results.md`: one Markdown table with the `index.md` columns
  (`experiment | chapter | n | primary metric | 95 % CI | LLM calls | s/item | notes`), CI shown as
  `[lo, hi]` or `—` when absent, plus a generated header line with the timestamp and the count of
  experiments. Idempotent.
- justfile: `results` (= `build`).

### `project/src/evals_tutorial/code_evals.py` (Typer: `triage`, `checks`, `similarity`, `all`)
- `triage --run triage_v1 --split test`: from traces vs gold: accuracy, macro/micro F1 for `category`,
  accuracy for `priority` and `needs_escalation`, confusion matrix (12×12) saved as
  `runs/04_triage_v1/confusion.png` (matplotlib, ≤ 300 KB) and printed; JSON validity rate of the raw
  `output` (does it parse into the triage schema?). `n` = 60. Primary metric `f1_macro`. Experiment
  `04_triage_v1`. Also report the same on `dev` in `details` (not the table).
- `checks --run answer_v1 --split test`: a table-driven set of deterministic assertions over each reply,
  each a small pure function `(ticket, trace) -> bool` registered in a dict:
  `nonempty`, `max_words_150`, `mentions_section_name` (any gold section name or its title appears),
  `no_phone_or_email_invented` (regex: phone/email in output that is not in the handbook),
  `no_forbidden_promises` (regex list: "guarantee", "full refund immediately", …, from `prompts/`-free YAML
  `data/checks/forbidden_phrases.yaml`), `mentions_all_answer_point_keywords` (every gold answer point
  has ≥ 1 keyword — keywords = the 2 longest words of the point, lower-cased — in the reply; this is the
  keyword-assertion approximation of "covers the answer points"). Per-check pass rates + `all_checks_pass`
  rate; primary `all_checks_pass`. Experiment `04_checks_answer_v1`.
- `similarity --run answer_v1 --split test`: ROUGE-L F (implement the LCS-based ROUGE-L yourself, ≈ 30
  lines — no new dependency) and cosine similarity of `nomic-embed-text` embeddings between the reply and
  the concatenated gold answer points; report mean ± sd, and **the correlation (point-biserial / AUROC)
  of each similarity score with the chapter-03 `pass` label** — this is the number that shows whether
  similarity metrics track quality. 60 embeddings ≈ 60 cached calls. Primary `auroc_embed_vs_label`.
  Experiment `04_similarity_answer_v1`.
- `all` runs the three and then `results.build()`.

### `project/justfile`
`results`, `code-evals` (= `all`).

### Tests `project/tests/test_04_code_evals.py`
`write_metrics` + `build` round-trip in `tmp_path` (table has the exact column header from `index.md`,
CI rendering, `—` when absent); triage metrics on a 6-row synthetic set with a known confusion matrix;
every check function on hand-made pass/fail replies; ROUGE-L on two short strings with a hand-computed
value; similarity with `FakeEmbedder`. No network, no matplotlib window (`Agg`).

### Findings note `project/runs/04_findings.md` (REQUIRED)
The three new `results.md` rows (copy the lines); the confusion matrix as a small table (top confusions);
per-check pass rates; the AUROC/correlation of ROUGE-L and embedding similarity vs the pass label with a
one-line reading ("similarity does/does not separate pass from fail"); 2 concrete examples where a
high-similarity reply failed and a low-similarity reply passed (ticket id, scores, one quoted sentence);
LLM calls (embeddings) and seconds; anything skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/{results,code_evals}.py`,
`project/data/checks/forbidden_phrases.yaml`, `project/runs/04_triage_v1/**`, `project/runs/04_checks_answer_v1/**`,
`project/runs/04_similarity_answer_v1/**`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_04_code_evals.py`, `project/runs/04_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "04_triage_v1"` ≥ 1.

## Scope & constraints
No LLM judges (05), no confidence intervals yet (07 retrofits them; leave `ci` empty `{}`), no changes
to the SUT, prompts or traces. ≤ 100 LLM/embedding calls. Context budget ≈ 50k tokens. Do not run
`fleet serve restart` or `fleet run`.
