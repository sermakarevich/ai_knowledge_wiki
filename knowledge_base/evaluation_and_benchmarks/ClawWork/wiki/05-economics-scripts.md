> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Economics pipeline scripts

**In one sentence:** Four offline scripts estimate task labor hours with GPT-5.2, convert hours to dollar values via BLS wages, validate the EconomicTracker payment/threshold system, and retroactively rescale old uniform-$50 agent payments to real task values.

## Key points

- `estimate_task_hours.py` estimates per-task professional hours with `MODEL = "gpt-5.2"` and streams results to `task_hour_estimates/task_hours.jsonl` (`scripts/estimate_task_hours.py:23`, `scripts/estimate_task_hours.py:25`).
- `calculate_task_values.py` computes `task_value = hours_estimate * hourly_wage` by matching each GDPVal occupation to a BLS `OCC_TITLE` with GPT-5.2 and writes `task_values.jsonl` (`scripts/calculate_task_values.py:26`, `scripts/calculate_task_values.py:261`).
- `recalculate_agent_economics.py` rescales paid entries with `new_payment = old_payment × (real_task_value / 50)` so the 0.6 evaluation cliff is preserved, writing a new `economic_real_value/` directory (`scripts/recalculate_agent_economics.py:120`, `scripts/recalculate_agent_economics.py:210`).
- `validate_economic_system.py` checks six required `EconomicTracker` methods, the `evaluation_score` parameter, per-channel cost separation, and threshold/date/task queries end to end (`scripts/validate_economic_system.py:237`, `scripts/validate_economic_system.py:404`).
- Payment gating is all-or-nothing at `min_evaluation_threshold=0.6`: scores below 0.6 pay $0, scores at or above pay the full amount, verified across nine boundary cases (`scripts/validate_economic_system.py:322`, `scripts/validate_economic_system.py:332`).
- Cost records distinguish four channels — `llm_tokens`, `search_api`, `ocr_api`, `other_api` — with per-task and per-day aggregation via `get_task_costs` and `get_daily_summary` (`scripts/validate_economic_system.py:433`, `scripts/validate_economic_system.py:127`).
- All three data scripts use append/streaming writes plus resume (`load_existing_estimates`, per-mapping saves) and 1-second rate limiting between LLM calls (`scripts/estimate_task_hours.py:195`, `scripts/calculate_task_values.py:227`, `scripts/estimate_task_hours.py:358`).

---

## Overview

The economics pipeline runs offline in three stages plus one validator (`scripts/estimate_task_hours.py:1`, `scripts/calculate_task_values.py:1`, `scripts/recalculate_agent_economics.py:1`, `scripts/validate_economic_system.py:1`):

1. Estimate hours per GDPVal task (`estimate_task_hours.py`).
2. Map occupations to BLS wages and multiply into dollar values (`calculate_task_values.py`).
3. Rescale historical agent ledgers from the legacy $50 cap to real values (`recalculate_agent_economics.py`).
4. Validate tracker behavior, integrations, and threshold logic (`validate_economic_system.py`).

No script runs the agent itself; they read/write JSONL/CSV/parquet artifacts and call `livebench.agent.economic_tracker.EconomicTracker` only inside the validator (`scripts/validate_economic_system.py:20`).

## Estimate task hours

Entry point and configuration (`scripts/estimate_task_hours.py:23`):

```python
MODEL = "gpt-5.2"
DATA_PATH = "../gdpval/data/train-00000-of-00001.parquet"
OUTPUT_DIR = "./task_hour_estimates"
OUTPUT_FILE = "task_hours.jsonl"
LOG_FILE = "./task_hour_estimation.log"
```

Flow:

- `load_gdpval_data()` reads the GDPVal parquet and logs task/occupation counts (`scripts/estimate_task_hours.py:37`).
- `create_hour_estimation_prompt(task_id, occupation, sector, task_prompt, reference_files)` builds the workforce-analyst prompt with conservative hour bands (0.25–1h quick, 1–3h standard, 3–6h moderate, 6–12h complex, 12+h rare) and a strict JSON output schema (`scripts/estimate_task_hours.py:44`, `scripts/estimate_task_hours.py:90`).
- Core call (`scripts/estimate_task_hours.py:130`):

```python
def estimate_hours_for_task(
    task_id: str,
    occupation: str,
    sector: str,
    task_prompt: str,
    reference_files: list
) -> Dict[str, Any]:
```

- It calls `client.chat.completions.create` with `response_format={"type": "json_object"}` and attaches usage metadata plus `estimated_at` and `model` (`scripts/estimate_task_hours.py:158`, `scripts/estimate_task_hours.py:177`).
- `load_existing_estimates(output_file)` enables resume by skipping already-written task IDs; `save_estimate(estimate, output_file)` appends one JSON object per line immediately after each success (`scripts/estimate_task_hours.py:195`, `scripts/estimate_task_hours.py:210`).
- `main()` iterates all parquet rows, normalizes `reference_files` to a list, sleeps 1 second between requests, and tracks processed/skipped/failed counts (`scripts/estimate_task_hours.py:316`, `scripts/estimate_task_hours.py:358`).
- `generate_summary_report(output_file)` writes `summary.json` with total/average/min/max hours, token usage, `estimated_cost_usd` at `$5.00 per 1M tokens`, and per-occupation breakdown sorted by total hours (`scripts/estimate_task_hours.py:215`, `scripts/estimate_task_hours.py:260`).

## Calculate task values

Configuration (`scripts/calculate_task_values.py:26`):

```python
MODEL = "gpt-5.2"
TASK_HOURS_FILE = "./task_hour_estimates/task_hours.jsonl"
HOURLY_WAGE_FILE = "./task_value_estimates/hourly_wage.csv"
OUTPUT_DIR = "./task_value_estimates"
OCCUPATION_MAPPING_FILE = "occupation_to_wage_mapping.json"
TASK_VALUES_FILE = "task_values.jsonl"
SUMMARY_FILE = "value_summary.json"
LOG_FILE = "./task_value_calculation.log"
```

Flow:

- `load_task_hours()` reads `task_hours.jsonl` line by line (`scripts/calculate_task_values.py:43`).
- `load_wage_data()` parses the tab-delimited wage CSV with `csv.DictReader(f, delimiter='\t')`, drops rows where `H_MEAN` is empty or `'*'`, and keeps `{'occ_title', 'h_mean'}` pairs (`scripts/calculate_task_values.py:57`, `scripts/calculate_task_values.py:62`).
- `get_unique_occupations(tasks)` pulls distinct `metadata.occupation` values from the hour estimates (`scripts/calculate_task_values.py:79`).
- `create_occupation_matching_prompt(gdpval_occupation, wage_occupations)` asks GPT-5.2 to return the single best BLS title with `confidence` and `reasoning`, requiring a character-for-character BLS title match (`scripts/calculate_task_values.py:89`, `scripts/calculate_task_values.py:133`).
- Core matcher (`scripts/calculate_task_values.py:142`):

```python
def match_occupation_to_wage(
    gdpval_occupation: str,
    wage_data: List[Dict[str, str]]
) -> Optional[Dict[str, Any]]:
```

- It stores `gdpval_occupation`, `bls_occupation`, `hourly_wage`, `confidence`, `reasoning`, `matched_at`, and `model`, and logs each hit such as `Matched 'X' -> 'Y' ($Z/hr)` (`scripts/calculate_task_values.py:182`, `scripts/calculate_task_values.py:191`).
- `create_occupation_mappings(occupations, wage_data, output_dir)` reloads existing mappings and saves the JSON list after every new mapping with a 1-second sleep (`scripts/calculate_task_values.py:201`, `scripts/calculate_task_values.py:227`).
- Valuation (`scripts/calculate_task_values.py:237`):

```python
def calculate_task_values(
    tasks: List[Dict[str, Any]],
    occupation_mappings: Dict[str, Dict[str, Any]],
    output_dir: Path
) -> List[Dict[str, Any]]:
```

- Each output record holds `task_id`, `occupation`, `hours_estimate`, `hourly_wage`, `task_value_usd`, `bls_occupation`, `confidence`, `sector`, and `task_summary`, computed as `task_value = hours_estimate * hourly_wage` and rounded to cents (`scripts/calculate_task_values.py:261`, `scripts/calculate_task_values.py:263`).
- `generate_value_summary(task_values, output_dir)` writes `value_summary.json` with totals, averages, min/max, and an occupation breakdown sorted by total value descending (`scripts/calculate_task_values.py:292`, `scripts/calculate_task_values.py:354`).
- `main()` requires `OPENAI_API_KEY` and runs match → value → summary in that order (`scripts/calculate_task_values.py:374`, `scripts/calculate_task_values.py:381`).

## Recalculate agent economics

Purpose: fix historical ledgers that paid a uniform $50 cap by scaling only actually-paid amounts to real task values (`scripts/recalculate_agent_economics.py:1`).

Usage (`scripts/recalculate_agent_economics.py:9`):

```text
python recalculate_agent_economics.py <agent_data_dir>
```

Key functions:

- `load_task_values(task_values_path)` reads `task_value_usd` per `task_id` from JSONL and logs the price range and average (`scripts/recalculate_agent_economics.py:31`, `scripts/recalculate_agent_economics.py:51`).
- `load_tasks(agent_dir)` reads `work/tasks.jsonl`; `load_balance_history(agent_dir)` reads `economic/balance.jsonl` (`scripts/recalculate_agent_economics.py:55`, `scripts/recalculate_agent_economics.py:74`).
- `create_date_to_task_mapping(tasks)` maps `date → task_id` from `tasks.jsonl` (`scripts/recalculate_agent_economics.py:93`).
- Core rescale (`scripts/recalculate_agent_economics.py:108`):

```python
def recalculate_balance_history(
    balance_history: List[Dict[str, Any]],
    date_to_task: Dict[str, str],
    task_values: Dict[str, float],
    default_max_payment: float = 50.0
) -> tuple[List[Dict[str, Any]], Dict[str, Dict[str, float]]]:
```

- Formula preserved verbatim from the docstring (`scripts/recalculate_agent_economics.py:120`):

```text
Formula: new_payment = old_payment × (real_task_value / 50)
```

- Zero-income days (below the 0.6 cliff) are left at $0; only `old_work_income > 0` entries are scaled, and each correction records `old_payment`, `new_payment`, `real_task_value`, and `scaling_factor` (`scripts/recalculate_agent_economics.py:161`, `scripts/recalculate_agent_economics.py:167`).
- Corrected entries add `work_income_delta_old`, `total_work_income`, `total_token_cost`, `balance`, `net_worth`, `correction_applied`, `task_id`, and `real_task_value`; the `initialization` row is carried over unchanged (`scripts/recalculate_agent_economics.py:136`, `scripts/recalculate_agent_economics.py:186`).
- `save_corrected_data(agent_dir, new_balance_history, payment_corrections)` creates `economic_real_value/` with corrected `balance.jsonl`, `correction_summary.json` (old/new final balance, income deltas, per-task corrections), and an unchanged copy of `token_costs.jsonl` (`scripts/recalculate_agent_economics.py:202`, `scripts/recalculate_agent_economics.py:214`).
- `main()` hardcodes the task-value source as `./scripts/task_value_estimates/task_values.jsonl` and runs load → map → rescale → save → print (`scripts/recalculate_agent_economics.py:344`, `scripts/recalculate_agent_economics.py:358`).

## Validate economic system

`validate_economic_system.py` is a demo plus four validators run from `__main__` (`scripts/validate_economic_system.py:588`, `scripts/validate_economic_system.py:597`).

- `demo_new_format()` builds a temp-dir `EconomicTracker` with `signature="demo-agent"`, `initial_balance=1000.0`, and `min_evaluation_threshold=0.6`, then runs three tasks scoring 0.85 (paid), 0.45 (rejected), and 0.65 (paid) through `start_task` / `track_tokens` / `track_api_call` / `add_work_income` / `end_task` / `save_daily_state` (`scripts/validate_economic_system.py:32`, `scripts/validate_economic_system.py:61`).
- It prints a daily summary (`tasks_completed`, `tasks_paid`, per-channel costs, net profit, final balance), per-task cost breakdowns, and seven sample record shapes: `llm_tokens`, search `api_call`, OCR `api_call`, awarded `work_income`, rejected `work_income`, `task_summary`, and daily balance (`scripts/validate_economic_system.py:127`, `scripts/validate_economic_system.py:151`, `scripts/validate_economic_system.py:164`).
- `validate_integration_points()` asserts six tracker methods exist — `start_task`, `end_task`, `add_work_income`, `get_task_costs`, `get_daily_summary`, `get_cost_analytics` — plus the `evaluation_score` parameter, four-value `evaluate_artifact` returns, and `start_task`/`end_task`/`actual_payment` wiring in `live_agent.py` with `evaluation_score` passthrough in `direct_tools.py` (`scripts/validate_economic_system.py:237`, `scripts/validate_economic_system.py:254`, `scripts/validate_economic_system.py:272`).
- `validate_threshold_logic()` runs nine score cases from 0.0 to 1.0 against a $50 base, expecting $0 below 0.6 and $50 at/above, then audits every `work_income` record for `payment_awarded == (score >= threshold)` (`scripts/validate_economic_system.py:326`, `scripts/validate_economic_system.py:378`).
- `validate_cost_channel_separation()` mixes `JINA_Search`, `OCR_Input`, `OCR_Output`, and a custom API call and asserts per-channel totals match within `tolerance = 0.000001` (`scripts/validate_economic_system.py:425`, `scripts/validate_economic_system.py:443`).
- `validate_query_capabilities()` writes six tasks across three dates with alternating 0.7/0.5 scores and asserts per-task cost, per-date counts (2 tasks, 1 paid each), and global analytics (6 tasks, 3 paid, 3 rejected, 3 dates, 6 tasks in `by_task`) (`scripts/validate_economic_system.py:489`, `scripts/validate_economic_system.py:520`, `scripts/validate_economic_system.py:535`).
- `check_backward_compatibility_notes()` documents breaking changes: `add_work_income()` now requires `evaluation_score`, `evaluate_artifact()` returns four values, and callers must bracket work with `start_task()`/`end_task()` (`scripts/validate_economic_system.py:568`, `scripts/validate_economic_system.py:575`).

**Covers:** component 05
