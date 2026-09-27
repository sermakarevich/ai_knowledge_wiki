# Task: chapter 03 impl — look at your data: trace viewer, open coding, axial coding, the label set (code + data, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` ("Data contracts"), `research/hamel_field-guide-rapidly-improving-ai-products.md`
(only the sections on error analysis / open and axial coding — search for "open coding"), and
`project/src/evals_tutorial/helpdesk.py` (`load_traces`). Do not read chapter markdown
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
80 `answer_v1` traces exist but nobody has looked at them. The methodology says: read traces, write a
free-text note per failure (open coding), cluster the notes into a failure taxonomy (axial coding), and
only then build graders. We also need a **label set** (`pass`/`fail` + failure modes per ticket) that
chapters 05 and 07 align judges against. A human domain expert would label these; here the labels are
produced by a *reference-aware grader* (the LLM given the gold answer points, gold sections and the
handbook — information the app itself never sees) plus a manual review of a sample. Be explicit about
this in the findings note.

## Fix

### `project/src/evals_tutorial/viewer.py` (Typer: `html`, `show`)
- `html --run answer_v1 --out runs/viewer/answer_v1.html`: one static HTML page (no server, no JS
  framework; inline CSS; ≤ 200 lines of Python) listing every trace: ticket text, gold labels, retrieved
  sections with scores, the reply, latency, and — when a labels file exists — the label, failure modes
  and note, with keyboard-free filters implemented as `<details>` groups per failure mode. Hamel's point:
  a viewer built for *your* trace schema, that shows everything on one screen.
- `show <ticket_id> --run answer_v1`: the same for one trace, in the terminal with `rich`.

### `project/src/evals_tutorial/labels.py` (Typer: `grade`, `code`, `stats`)
- `grade --run answer_v1`: for every trace, `chat_json` with the **reference-aware rubric** prompt
  `prompts/reference_grader_v1.txt` (inputs: ticket, gold answer points, gold section texts, the reply;
  output schema `{pass: bool, missing_points: list[str], unsupported_claims: list[str],
  wrong_tone_or_promise: bool, did_not_answer: bool, note: str}` where `note` is ONE free-text sentence
  describing what is wrong — this is the open-coding note). 80 calls. Write
  `project/data/labels/answer_v1.jsonl` per the `index.md` contract, with `failure_modes` filled in the
  next step and the raw grader fields under `raw`.
- `code`: **axial coding**. Print all `note`s of failing traces (expect 20–40 short sentences) and
  cluster them into 4–7 failure modes with stable snake_case ids. Do this yourself as the worker (read
  the printed notes, decide the clusters, write them into `project/data/labels/taxonomy.yaml`:
  `id, name, definition, example_ticket_ids`) — do NOT ask the LLM to cluster. Then map each failing
  trace to ≥ 1 mode: `failure_modes` in the labels file. Expected modes typically include
  `missing_required_fact`, `unsupported_claim`, `wrong_section_retrieved`, `over_promise`,
  `did_not_answer`, `format_or_citation`; use what the notes actually show.
- **Manual review**: pick 12 traces (6 pass, 6 fail, seeded) and review them yourself by reading them
  with `viewer show`; record agree/disagree per trace in `project/data/labels/review_answer_v1.md` and
  flip a label only when the grader is clearly wrong (say so in the file).
- `stats`: pass rate, counts per failure mode, per topic and per scenario (Markdown tables).
- Also `grade --run triage_v1`: code-only — compare each trace's `category`/`priority`/
  `needs_escalation` with gold → `project/data/labels/triage_v1.jsonl` (`pass` = all three correct;
  `failure_modes` ∈ {`wrong_category`, `wrong_priority`, `wrong_escalation`}). No LLM calls.

### `project/justfile`
`viewer run`, `labels run`, `labels-stats`.

### Tests `project/tests/test_03_labels.py`
`FakeLLM` grading → labels file with contract fields; taxonomy YAML loads and every `failure_modes`
id in the committed labels exists in it; triage grading is pure code (table-driven); the HTML viewer
renders a synthetic trace and contains its ticket id. No network.

### Findings note `project/runs/03_findings.md` (REQUIRED)
Pass rates (answer, triage); the taxonomy with definitions, counts and one real example per mode
(ticket id, the note, the offending sentence of the reply); the per-topic and per-scenario tables; the
manual-review result (n agree / disagree, and what the disagreements were); 3–5 observations (e.g. which
scenario fails most, whether retrieval or generation is the bigger problem); LLM calls and time; the
explicit caveat about reference-aware grading standing in for human labels.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/{viewer,labels}.py`,
`project/src/evals_tutorial/prompts/reference_grader_v1.txt`, `project/data/labels/{answer_v1,triage_v1}.jsonl`,
`project/data/labels/taxonomy.yaml`, `project/data/labels/review_answer_v1.md`, `project/runs/viewer/*.html`,
`project/data/cache/**`, `project/justfile`, `project/tests/test_03_labels.py`, `project/runs/03_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/data/labels/taxonomy.yaml | grep -c "id:"` ≥ 4.

## Scope & constraints
No reference-free judges (chapter 05), no metrics.json/results.md (chapter 04), no statistics. Do not
change the SUT or the `v1` traces. ≤ 100 LLM calls. Context budget ≈ 50k tokens. Do not run `fleet serve
restart` or `fleet run`.
