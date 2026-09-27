# Task: chapter 02 impl — the system under test: handbook, ticket generator, `triage`, `answer`, traces (code + data only, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` (especially "Data contracts") and `project/src/evals_tutorial/llm.py`
(the API you must use). Do not read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Every later chapter evaluates one application on one ticket set. Neither exists. Build the fictional
shop's handbook, generate tickets whose labels are gold *by construction*, implement `triage` and
`answer` with versioned prompts, and record a trace for every call.

## Fix

### `project/src/evals_tutorial/handbook.py` (Typer: `generate`, `stats`)
- `generate`: for each of the 12 section ids in `index.md`, ask the LLM (through `llm.chat`, temperature
  0, cached) for a 200–400-word policy document for *Northwind Outdoor* (bikes and camping gear) in
  Markdown with 4–6 numbered rules containing concrete numbers (days, percentages, amounts, thresholds)
  → `project/data/handbook/<section_id>.md`. Ask for a short `## Key facts` bullet list at the end of
  each (3–5 facts) — chapter tickets are built from these facts. 12 calls.
- `load() -> dict[section_id, text]`, `key_facts(section_id) -> list[str]` (parse the bullets).
- `stats`: table section | words | facts.

### `project/src/evals_tutorial/tickets.py` (Typer: `generate`, `stats`)
- Grid: `personas` (6: e.g. hurried commuter, polite retiree, angry first-time buyer, small-business
  buyer, non-native English speaker, teenager) × `topics` = the 12 section ids × `scenarios` (4:
  `simple_question`, `problem_report`, `urgent_blocker`, `out_of_policy_request`). Pick 80 combinations
  with a seeded RNG, every topic ≥ 5 times, every scenario ≥ 15 times.
- For each: choose 1–2 key facts of the topic section; the label is set BEFORE generation:
  `category = topic`; `priority` from scenario (`simple_question`→`low`/`normal`, `problem_report`→
  `normal`/`high`, `urgent_blocker`→`urgent`, `out_of_policy_request`→`normal`); `needs_escalation` =
  scenario is `out_of_policy_request` or (`urgent_blocker` and topic in {`payments`, `privacy`,
  `damaged_items`}); `sections = [topic]` (+ one related section for 20 % of tickets, chosen from a fixed
  map, e.g. returns↔shipping, warranty↔damaged_items, discounts↔gift_cards); `answer_points` = the
  chosen key facts rewritten as the points a reply must state.
- Then ask the LLM (`chat_json`, schema `{text: str}`) to write the customer's message (60–160 words) in
  the persona's voice, about the chosen facts and scenario, WITHOUT naming the section. 80 calls.
- `split`: seeded, 20 `dev` / 60 `test`, stratified by topic. Write `project/data/tickets/tickets.jsonl`
  with exactly the fields of the `index.md` contract. `stats`: counts per topic/scenario/priority/split.

### `project/src/evals_tutorial/prompts/`
`triage_v1.txt` (system prompt: the 12 categories with one-line descriptions, the 4 priorities, the
escalation rule *as the model should apply it*, output JSON), `answer_v1.txt` (system prompt: "You are
the Northwind Outdoor support assistant … answer ONLY from the handbook excerpts below … cite sections
as [section_id] … if the handbook does not cover it, say so and offer escalation"; placeholders
`{context}`, `{ticket}`). Deliberately keep `v1` plain (no few-shot, no formatting rules) — later
chapters improve it.

### `project/src/evals_tutorial/helpdesk.py` (Typer: `triage`, `answer`, `run`)
- `Triage(BaseModel)`: `category: Literal[...12]`, `priority: Literal[...]`, `needs_escalation: bool`,
  `reason: str`. `triage(ticket_text, version="v1") -> Triage` via `llm.chat_json`.
- Retrieval: `embed_documents` over the 12 sections (split each into ≤ 120-word chunks, keep
  `section_id`), `embed_query(ticket)`, cosine top-k chunks (k=4), collapse to sections in score order →
  `retrieved: [{section, score}]`; context = the full text of the top-2 sections.
- `answer(ticket_text, version="v1") -> Reply(text, citations: list[str])` (citations parsed from
  `[section_id]` tokens).
- `run --task triage|answer --version v1 --split all`: for every ticket write
  `project/runs/traces/<task>_<version>/<ticket_id>.json` exactly per the `index.md` trace contract
  (include `latency_s` and `usage` from `llm.py`). Run BOTH tasks for `v1` on all 80 tickets (160 calls;
  `just gpu-check` first; run in background with a log per COMMON).
- `load_traces(run) -> list[dict]` helper for later chapters.

### `project/justfile`
`handbook`, `tickets`, `run-triage version`, `run-answer version`.

### Tests `project/tests/test_02_sut.py`
With `FakeLLM`/`FakeEmbedder`: grid picks 80 combos with the coverage guarantees; labels derive from
scenario as specified (table-driven test); `Triage` schema rejects a bad category; retrieval returns
sections in score order and the context has ≤ 2 sections; trace file has every contract field;
`tickets.jsonl` (committed) has 80 rows, 20 dev / 60 test, every category present. No network.

### Findings note `project/runs/02_findings.md` (REQUIRED)
Handbook stats table; ticket stats tables; 3 example tickets (one per split/scenario) with their gold
labels; 2 example `answer_v1` traces (ticket → retrieved → reply) and 1 `triage_v1` trace; how many
triage outputs match the gold category (a quick count, no CI yet); total LLM calls and wall time;
anything that differed from the spec.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/{handbook,tickets,helpdesk}.py`,
`project/src/evals_tutorial/prompts/{triage_v1,answer_v1}.txt`, `project/data/handbook/*.md`,
`project/data/tickets/tickets.jsonl`, `project/runs/traces/{triage_v1,answer_v1}/*.json`,
`project/data/cache/**`, `project/justfile`, `project/tests/test_02_sut.py`, `project/runs/02_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/data/tickets/tickets.jsonl | wc -l` = 80.

## Scope & constraints
No grading, no metrics, no `results.md` yet (chapter 04). No agent (chapter 10). Do not edit `index.md`
or the `v1` prompts after the traces are recorded. ≤ 260 LLM calls total. Context budget ≈ 50k tokens.
Do not run `fleet serve restart` or `fleet run`.
