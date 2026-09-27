> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Models, Cost, and Code Extraction

**In one sentence:** The study evaluates three OpenAI models spanning low-cost to state-of-the-art, plans API costs with tiktoken estimates and Batch-API savings, and extracts syntactically valid code via a regex plus AST-validation loop that preserves the original prompts.

## Key points

- GPT-4o was OpenAI's state-of-the-art model at study time, while GPT-4o-mini had replaced GPT-3.5-turbo as the best lightweight model with better performance and cost-efficiency.
- Evaluating three models captures a range from low-cost to most advanced, showing how sensitivity to prompt variations scales with model capability.
- API cost is billed by input and output tokens, estimated per prompt with OpenAI's tiktoken module plus a margin factor on unknown response length, and a 50% reduction assumed for the Batch-API.
- Running all attempts on GPT-4o-mini cost USD 28, versus an estimated USD 3080 on GPT-4 assuming the same output length, with cost scaling linearly in sample size and details in the repository.
- Security scanners require syntactically correct code, but ChatGPT responses intermix code with natural language, so code-only instructions are deliberately avoided in the original prompts to preserve real-world usage and result validity.
- Extraction finds markdown code blocks delimited by ``` with a regular expression: no block may mean pure code, one block is taken as-is, and multiple blocks trigger a follow-up.
- Validity is confirmed with `ast.parse` building the Abstract Syntax Tree with no errors and AST height above two; failures or multiple blocks append the follow-up "Only output the python code and nothing else, so that when I copy your answer into a file, it will be a valid python file", retried up to two times before reporting an error and regenerating the sample from scratch (max 3 times).

---

## Models under test

GPT-4o was the state-of-the-art model at study execution time; GPT-4o-mini replaced GPT-3.5-turbo as the best lightweight option, offering improved performance and cost-efficiency. Testing three models spans low-cost to most advanced, providing insight into how prompt-variation sensitivity scales with capability.

| Model | Role in study |
|---|---|
| GPT-4o | State-of-the-art / most advanced |
| GPT-4o-mini | Lightweight successor to GPT-3.5-turbo, improved performance and cost-efficiency |
| Third model (context: GPT-3.5-turbo / GPT-4 family) | Low-cost end of the range |

## Cost planning

A budget script estimates OpenAI API cost (billed by input and output tokens) using `tiktoken` for prompt tokens, prior-response lengths plus a margin factor for unknown output length, and a 50% Batch-API discount.

| Estimate | Value |
|---|---|
| All attempts on GPT-4o-mini | USD 28 |
| All attempts on GPT-4 (same output length as 4o-mini) | USD 3080 |
| Batch-API effect | 50% cost reduction |
| Sample-size scaling | Linear |

Detailed results are available in the authors' repository.

## Code extraction (Figure 2 workflow)

Security scanners need syntactically correct code, but responses mix code with natural-language text. Adding a code-only instruction would alter responses "and could invalidate our results", so the authors "maintain the original prompts and perform code extraction separately."

1. Find markdown code blocks (delimited by ```) with a regular expression.
2. If no block is found, the response may consist entirely of code; if one block is found, take its contents.
3. Validate with `ast.parse`: no errors and AST height above two means valid code that continues to the code security scan.
4. If validation fails, or the response contains multiple code blocks, append the follow-up prompt to the original conversation:

> "Only output the python code and nothing else, so that when I copy your answer into a file, it will be a valid python file"

5. "Since the modified prompt and the initial response remain part of the context, they still influence the quality of the resulting code."
6. The new response is evaluated with the same steps and re-tried unless the limit of two re-tries is reached.
7. "If two code extraction attempts fail, an error is reported, and the original prompt is re-generated from scratch by returning to Response Generation (max. 3 times)."

## Validity and metrics notes (bridging fragment)

Scanners "found considerably fewer vulnerabilities than the manual search, but the relative difference in the results between the two LLMs stayed in proportion", so the benchmark supports relative comparison of vulnerability counts but "should not be considered an absolute measure of the security quality of LLM-generated code." Metrics start from Semgrep and CodeQL per-sample results, filtered to the suspected CWE of the prompt, computing values for both raw and CWE-filtered results, including scanner agreement on the suspected CWE and the average vulnerability count from both scanners combined.

**Covers:** Models under test, API cost planning, and code-extraction workflow.
