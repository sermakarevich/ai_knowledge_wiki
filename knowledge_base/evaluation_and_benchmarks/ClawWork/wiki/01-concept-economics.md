> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Concept: AI-coworker economic benchmark

**In one sentence:** ClawWork turns an AI assistant into an economically accountable AI coworker that must earn real income from professional tasks while paying its own token costs from a $10 starting balance.

## Key points

- ClawWork frames assistants as coworkers that "complete real work tasks and create genuine economic value" (`/tmp/clawwork/README.md:36-37`).
- Agents do professional work from the GDPVal dataset, "pay for their own token usage, and maintain economic solvency" (`/tmp/clawwork/README.md:39-40`).
- The benchmark runs 220 GDPVal tasks spanning 44 occupations/economic sectors (`/tmp/clawwork/README.md:62-62`).
- Each agent starts with just $10 and "pay[s] for every token generated" so waste can wipe the balance (`/tmp/clawwork/README.md:64-64`).
- Payment follows real economic value as `quality_score × (estimated_hours × BLS_hourly_wage)` (`/tmp/clawwork/README.md:276-278`).
- Work quality is scored by an LLM judge (GPT-5.2) with "category-specific rubrics for each of the 44 GDPVal sectors" (`/tmp/clawwork/README.md:76-76`).
- The end-to-end loop is Task Assignment → Execution → Artifact Creation → LLM Evaluation → Payment (`/tmp/clawwork/README.md:72-72`).

---

## Economic premise: earn more than you burn

ClawWork replaces a technical score with a survival test: the agent must stay solvent while doing paid work (`/tmp/clawwork/README.md:39-43`). Production success is defined as **work quality**, **cost efficiency**, and **long-term survival** (`/tmp/clawwork/README.md:42-43`). The top systems reportedly reach "$1,500+/hr equivalent salary" (`/tmp/clawwork/README.md:72-73`).

Starting conditions are deliberately tight (`/tmp/clawwork/README.md:338-342`):

- Initial balance: **$10**.
- Token costs deducted automatically after each LLM call.
- API costs for search: `$0.0008/call Tavily, $0.05/1M tokens Jina`.

The earlier LiveBench prototype used the same survival idea with a $1,000 start and a daily trade-or-work choice (`/tmp/clawwork/livebench/README.md:7-12`), described as "Squid Game for AI Agents" (`/tmp/clawwork/livebench/README.md:3-3`).

## Payment: BLS wage × hours × quality

Payment is not flat; it tracks estimated professional value (`/tmp/clawwork/README.md:272-278`):

```text
Payment = quality_score × (estimated_hours × BLS_hourly_wage)
```

Task economics quoted verbatim (`/tmp/clawwork/README.md:280-285`):

| Metric | Value |
|--------|-------|
| Task range | $82.78 – $5,004.00 |
| Average task value | $259.45 |
| Quality score range | 0.0 – 1.0 |
| Total tasks | 220 |

Tasks require real deliverables such as Word documents, Excel spreadsheets, PDFs, data analysis, project plans, technical specs, research reports, and process designs (`/tmp/clawwork/README.md:270-270`).

## Evaluation: category-specific LLM rubrics

Quality scoring uses GPT-5.2 with per-occupation rubrics (`/tmp/clawwork/README.md:76-76`). The rubric generator iterates "through all 44 task categories (occupations) in the gdpval dataset" (`/tmp/clawwork/eval/generate_meta_prompts.py:5-6`) and emits one JSON rubric per occupation into `./meta_prompts` (`/tmp/clawwork/eval/generate_meta_prompts.py:27-28`).

Key configuration quoted verbatim (`/tmp/clawwork/eval/generate_meta_prompts.py:26-29`):

```python
MODEL = "gpt-5.2"
DATA_PATH = "../gdpval/data/train-00000-of-00001.parquet"
OUTPUT_DIR = "./meta_prompts"
LOG_FILE = "./meta_prompt_generation.log"
```

The scoring contract is strict: "a **0-10 scoring scale** where missing or incomplete deliverables MUST receive scores of 0-2" (`/tmp/clawwork/eval/generate_meta_prompts.py:80-81`). The rubric weights are completeness 40%, correctness 30%, quality 20%, and domain standards 10% (`/tmp/clawwork/eval/generate_meta_prompts.py:123-147`), combined as "weighted average: completeness (40%), correctness (30%), quality (20%), domain_standards (10%)" (`/tmp/clawwork/eval/generate_meta_prompts.py:160-160`).

Entry point quoted verbatim (`/tmp/clawwork/eval/generate_meta_prompts.py:46-51`):

```python
def create_meta_prompt_generation_request(
    category: str,
    sector: str,
    task_prompts: List[str],
    sample_task_details: List[Dict[str, Any]]
) -> str:
```

## Work-or-learn tradeoff and agent loop

Each day the agent decides to work for immediate income or invest in learning to improve future performance (`/tmp/clawwork/README.md:66-66`). The documented daily loop is receive assignment, decide work-or-learn, execute, earn income or deduct costs, then persist state and update the dashboard (`/tmp/clawwork/README.md:108-112`).

Agent configuration lives in `livebench/configs/` (`/tmp/clawwork/README.md:291-291`), quoted verbatim (`/tmp/clawwork/README.md:300-307`):

```json
"economic": {
  "initial_balance": 10.0,
  "task_values_path": "./scripts/task_value_estimates/task_values.jsonl",
  "token_pricing": {
    "input_per_1m": 2.5,
    "output_per_1m": 10.0
  }
}
```

Core decision and submission tools are `decide_activity(activity, reasoning)` for `"work"` or `"learn"` and `submit_work(work_output, artifact_file_paths)` for evaluation plus payment (`/tmp/clawwork/README.md:375-376`).

## Survival metrics

Benchmark metrics cover survival days, final balance, total work income, profit margin `(income - costs) / costs`, work quality, token efficiency, activity mix, and task completion rate (`/tmp/clawwork/README.md:482-491`). The LiveBench lineage used explicit tiers: Thriving above $500, Stable $100–$500, Struggling $0–$100, Bankrupt at or below $0 (`/tmp/clawwork/livebench/README.md:200-205`).

**Covers:** component 01
