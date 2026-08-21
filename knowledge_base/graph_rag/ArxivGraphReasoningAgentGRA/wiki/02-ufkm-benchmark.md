[[../index|Wiki]] | [[../summary|Summary]]

# The UFK-M benchmark, question generation, and the experimental setup

**In one sentence:** The paper builds and evaluates a synthetic bicycle-factory benchmark (UFK-M) where every question is generated answer-first — SQL written and validated against the database before the natural-language question exists — and tests seven backbone LLMs across four providers under three agentic baselines with deterministic scoring and bootstrap uncertainty.

## Key points

- UFK-M is a fully synthetic bicycle-assembly factory inspired by real client factories; a founding text states its operational rules, KPIs and industry concepts in prose, backed by a SQL data layer (DuckDB tables) and a semantic layer (a knowledge graph that distills the founding text and maps it onto the tables).
- The benchmark has two nested tiers (large and xlarge) that scale without removing information; baselines are evaluated mostly on xlarge.
- Questions are generated in reverse: an LLM writes a SQL program over sampled schema cards, it is executed and kept only if non-empty, non-degenerate, and ≤10 rows, and only then is a natural-language question written that the result answers.
- Because the SQL is validated before questioning, every question is demonstrably answerable, and the gold answer is the actual output of a run program rather than model-generated text.
- The frozen xlarge set holds 258 questions: 116 table answers, 84 single values, 48 booleans, 10 lists; 147 need at most one join, 45 need two, 66 need three or more; 34 additionally require the semantic layer (a named rule or KPI whose resolved value or formula stays hidden).
- Correctness is decided by a deterministic matcher, not an LLM judge: numerics compared with rounding tolerance, percentages scale-free (fraction vs. percentage independent), tables scored by recall of required gold rows.
- Seven backbone configurations across four providers are tested: DeepSeek V4-Flash (non-thinking, the reference), DeepSeek V4-Pro and V4-Pro-Think (same weights, reasoning off vs. on), GPT-5 Nano (low/high reasoning effort), GLM-4.5-Air, and Qwen3-Coder-Flash.
- Each backbone runs under three agentic baselines: GRA and RSA get 45 LLM-call turns (retrieving via the local embedder multilingual-e5-large-instruct), while SQA gets 6 turns and the full schema in its prompt with no retrieval; SQL tools cap results at 50 rows.
- All models decode greedily (temperature 0), completions capped at 1,024 tokens (8,192 for thinking configurations); primary results use the validated 258-question xlarge set, and uncertainty is quantified via paired bootstrap over questions (B = 104) with 95% percentile intervals.
- The chunk ends with the opening of the Results section: DeepSeek models are most accurate for all systems (8–18 pp gaps under GRA/RSA but only 2–9 pp under SQA), and full-context (SQA) inference is more robust when tool use is unreliable, leading with Qwen3-Coder-Flash (+2.3 pp over GRA) and GPT-5 Nano (+5.5 pp).

## Detail

### The UFK-M benchmark

UFK-M is a fictional bicycle-assembly factory: it is inspired by real client factories but is entirely synthetic. A founding text states the factory's operational rules, KPIs and industry concepts in prose. Two coordinated layers then make that world machine-readable: a data layer of DuckDB tables, and a semantic layer — a knowledge graph that distills the founding text and maps it onto the tables. Two nested tiers scale the benchmark without removing information (the smaller tier is a reduction of the larger one), and the paper evaluates its baselines mostly on the xlarge tier:

| Tier   | Tables | Rows    | KG nodes | KG edges | Founding words | Questions |
|--------|--------|---------|----------|----------|----------------|-----------|
| large  | 32     | 157 953 | 125      | 268      | 4 278          | 148       |
| xlarge | 64     | 174 006 | 235      | 513      | 6 933          | 258       |

(Reproduced from Table 2, "The two nested tiers of UFK-M".)

### Answer-first question generation

Questions are generated in reverse: the answer is fixed before the question exists. For each question, an LLM receives a sample of schema cards (table and column descriptions) and writes a SQL program over them. The program is executed against the database and kept only if its result is non-empty, non-degenerate, and contains at most ten rows. Only then does the LLM write a natural-language question that the retained result answers.

This order matters. Because the SQL is written and validated before the question, every question in the set is answerable from the data, and its gold answer is the output of a program that has actually run rather than text produced by a model.

The frozen xlarge set holds 258 such questions: 116 table answers, 84 single values, 48 booleans and 10 lists. By join complexity, 147 need at most one join, 45 need two, and 66 need three or more; 34 additionally require the semantic layer — a named operational rule or KPI whose resolved value or formula stays hidden.

### Deterministic scoring

Correctness is decided by a deterministic matcher rather than an LLM judge. Numeric answers are compared with tolerance for rounding precision, percentage answers are compared scale-free (i.e., the comparison is independent of whether the answer is expressed as a fraction or as a percentage), and table answers are scored by recall of the gold rows they must contain.

### Experimental setup

The authors evaluate seven backbone configurations across four providers:

- DeepSeek V4-Flash (non-thinking, used as the reference),
- DeepSeek V4-Pro and DeepSeek V4-Pro-Think (same weights, reasoning off vs. on),
- GPT-5 Nano (low/high reasoning effort),
- GLM-4.5-Air,
- Qwen3-Coder-Flash.

Each backbone runs under the three described agentic baselines, with GRA/RSA given 45 LLM-call turns and SQA 6 turns. SQL tools cap results at 50 rows; GRA/RSA retrieve context via a local embedder, multilingual-e5-large-instruct, while SQA instead receives the full schema in its prompt with no retrieval. All models decode greedily (temperature 0), with completions capped at 1,024 tokens (8,192 for thinking configurations) to avoid truncating answers; otherwise the harness is identical across systems. Evaluation uses the UFK-M benchmark, with primary results reported on the validated 258-question xlarge set.

Uncertainty is quantified via paired bootstrap over questions (B = 104), reported as 95% percentile intervals.

### Opening of the results (section 6.1, present in this chunk)

The chunk closes with the first part of the results: comparing the three systems across the model grid (in their Table 3), DeepSeek models achieve the highest accuracy for all systems — leading by 8–18 pp under GRA and RSA but only 2–9 pp under SQA. Among lower-cost models, Qwen3-Coder-Flash significantly outperforms GPT-5 Nano for every system. The ranking of agentic vs. full-context methods depends on the backbone: GRA performs best with the DeepSeek and GLM models, whereas SQA performs best with Qwen3-Coder-Flash (+2.3 pp over GRA) and GPT-5 Nano (+5.5 pp). The authors conclude from this that full-context inference is more robust when tool use is unreliable.
