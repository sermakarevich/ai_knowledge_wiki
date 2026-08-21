> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prompt Templates & Worked Examples

**In one sentence:** Appendix K exposes the literal prompt templates behind GraphPlanner's five agent roles (Planner, Executor, Summarizer, plus the appendix-introduced Thinker and Verifier) and the agent/model role descriptions, alongside three fully traced Phase-2 workflows showing how the same prompt family drives single-step, flat multi-step, and nested hierarchical decompositions.

## Key points

- Five prompt templates are given verbatim: **Planner** (sub-query decomposition), **Executor** (query answering), **Summarizer** (parent-query synthesis), **Thinker** (step-by-step draft reasoning), and **Verifier** (approve/revise gate) — each sharing a common Inputs/Instructions/Output format contract.
- All templates are context-passing templates: they thread `{QUERY}`, `{ROOT QUERY}`, `{PARENT QUERIES}`, `{SIBLING RESPONSES}` (and `{SUMMARY}`/`{CHILD ANSWERS}` for summarization) so any node in the workflow graph receives its position's context.
- The Planner is limited to 1–3 atomic, non-overlapping, self-contained sub-queries, with the number adapted to complexity and redundancy suppressed via sibling responses.
- The Thinker/Verifier pair forms a draft-then-verify sub-loop: the Thinker must produce numbered Reasoning Steps plus a Draft Answer "as [its] response will be verified by a Verifier Agent," and the Verifier must emit `[APPROVED/REVISED]`, Issues Found, and a Verified Response.
- Worked example 1 (math QA) shows the flat path: Planner (LLaMA-3.1-8B) → Q1/Q2 executors (Qwen2.5-7B, Gemma-2-9B) → executor merging subtotals (LLaMA-3.1-8B) → summarizer (LLaMA-3-70B-ChatQA) → final executor (Qwen2.5-14B) answering "$18".
- Worked example 2 (code task, `remove_digits`) shows nested planning: after Q1/Q2, a second Planner pass decomposes Q2 into Q2a (filtering logic, CodeGemma-7B: `not ch.isdigit()`) and Q2b (string construction, Qwen2.5-7B), then two summarizer passes and a final Qwen2.5-14B executor produce the Python function.
- Worked example 3 (natural QA, "Who painted the Mona Lisa?") shows the degenerate path: the planner selects an executor-only route — a single Qwen2.5-14B step, Acc 1, cost 85 — demonstrating adaptive skipping of decomposition.
- The appendix also fixes per-role duties (Tables 24–28) and a model catalog with pricing (Tables 29–40), plus a compact LLM-role→function table (Table 41); all models in the examples are routed at $0.10–$0.90 per million tokens.

---

## Prompt Templates

### Planner (sub-query decomposition) — Table 19

> You are a query decomposition assistant. Your task is to decompose the user's query into atomic and independent sub-queries.
>
> **Inputs:**
> - Original query: `{QUERY}`
> - Parent queries: `{PARENT QUERIES}`
> - Previous sibling responses: `{SIBLING RESPONSES}`
>
> **Instructions:**
> - Determine the optimal number of sub-queries (1–3).
> - Ensure each sub-query is self-contained and non-overlapping.
> - Avoid redundancy by considering `{SIBLING RESPONSES}`.
> - Adjust the number of sub-queries depending on complexity.
>
> **Output format:**
> - List 1–3 sub-queries.
> - One sub-query per line.
> - No numbering or extra commentary.

### Executor (query answering) — Table 20

> You are a helpful assistant. Answer the given (sub-)query with support from full context.
>
> **Inputs:**
> - Current sub-query: `{QUERY}`
> - Original query: `{ROOT QUERY}`
> - Parent queries: `{PARENT QUERIES}`
> - Previous sibling responses: `{SIBLING RESPONSES}`
> - If final execution: summary of sub-query responses `{SUMMARY}`
>
> **Instructions:**
> - Interpret the sub-query with reference to full context.
> - Align the answer with prior responses to ensure consistency.
> - If this is the final step, synthesize everything into a complete final answer.
>
> **Output format:**
> - Direct, complete answer in the format required by the task.
> - No extra commentary.

### Summarizer (parent query synthesis) — Table 21

> You are a professional summarizer. Your task is to synthesize multiple child answers into a coherent response to the parent query.
>
> **Inputs:**
> - Parent query: `{PARENT QUERY}`
> - Child answers: `{CHILD ANSWERS}`
>
> **Instructions:**
> - Combine all child answers into a complete, coherent response.
> - Preserve all important details.
> - Resolve overlap or conflicts among child answers.
> - Ensure the response directly addresses `{PARENT QUERY}`.
>
> **Output format:**
> - A single, well-structured paragraph answering the parent query.

### Thinker (sub-query reasoning) — Table 22

> You are a Thinker Agent in a multi-agent workflow system. Your task is to generate detailed reasoning responses for sub-queries.
>
> **Inputs:**
> - Sub-query: `{SUB QUERY}`
> - Original query: `{ROOT QUERY}`
> - Parent queries: `{PARENT QUERIES}`
> - Previous sibling responses: `{SIBLING RESPONSES}`
>
> **Instructions:**
> - Understand the sub-query in context of the original query.
> - Think step-by-step through the problem with detailed reasoning.
> - Consider information from previous sibling responses to maintain consistency.
> - Show your reasoning process clearly before reaching conclusion.
>
> **Output format:**
> - **Reasoning Steps:** List numbered reasoning steps.
> - **Draft Answer:** Your reasoned response to the sub-query.
> - Be thorough as your response will be verified by a Verifier Agent.

### Verifier (response verification) — Table 23

> You are a Verifier Agent in a multi-agent workflow system. Your task is to verify draft responses and produce refined, verified outputs.
>
> **Inputs:**
> - Sub-query: `{SUB QUERY}`
> - Original query: `{ROOT QUERY}`
> - Draft response from Thinker: `{DRAFT RESPONSE}`
> - Previous sibling verified responses: `{VERIFIED SIBLING RESPONSES}`
>
> **Instructions:**
> - Verify accuracy, completeness, consistency, and logical soundness.
> - If draft response is correct: approve and format cleanly.
> - If issues found: correct errors and improve the response.
> - Ensure consistency with other verified sibling responses.
>
> **Output format:**
> - **Verification Result:** [APPROVED/REVISED]
> - **Issues Found:** List specific problems identified (if any).
> - **Verified Response:** Final verified answer to the sub-query.

### Agent role descriptions (Tables 24–28)

- **Planner** — the decomposition agent: "analyze a complex user query and break it down into a set of clear, atomic sub-questions that can be addressed independently. This ensures that each sub-query targets a specific aspect of the original request, reducing ambiguity and overlap."
- **Executor** — the answering agent: generates responses "either directly or by incorporating additional background context when necessary"; "It can operate in both raw query execution mode or in a final, context-aware answering mode, depending on the task's stage and goal."
- **Summarizer** — the condensation agent: distills long/complex input into "a concise, coherent, and fluent summary... rewriting the original input into a well-structured passage that captures the essential meaning."
- **Thinker** — the reasoning agent: "process sub-queries through systematic step-by-step analysis, generating detailed reasoning chains that lead to well-founded conclusions... the core analytical component that transforms sub-queries into thoroughly reasoned draft answers for subsequent verification."
- **Verifier** — the quality assurance agent: "critically evaluate draft responses from Thinker agents, checking for accuracy, completeness, logical consistency... either approve correct drafts or provide refined corrections. It acts as the final quality gate."

### LLM catalog (Tables 29–40)

| Model | Notes (abridged) | $/M tokens (in/out) |
|---|---|---|
| Qwen2.5 (7b) | upgraded Qwen series, strong multilingual | 0.20 / 0.20 |
| CodeGemma (7b) | Gemma variant specialized for code generation | 0.20 / 0.20 |
| Mistral (7b) | open-weight, fast inference | 0.20 / 0.20 |
| LLaMA-3.1 (8b) | Meta Llama-3 series, conversational AI + complex reasoning | 0.20 / 0.20 |
| LLaMA-3 ChatQA (8b) | NVIDIA fine-tuned, QA/reasoning-optimized | 0.20 / 0.20 |
| Gemma-2 (9b) | Google instruction-tuned, general text | 0.10 / 0.10 |
| Mistral-Nemo (12b) | Mistral + NeMo hybrid | 0.30 / 0.30 |
| LLaMA-3.3 Nemotron Super (49b) | high-accuracy for demanding applications | 0.90 / 0.90 |
| LLaMA-3.1 Nemotron (51b) | NVIDIA alignment model, safe/helpful/accurate | 0.90 / 0.90 |
| Mixtral (8x7b) | 56B MoE, eight 7B experts, creative text | 0.60 / 0.60 |
| LLaMA-3 ChatQA (70b) | conversational AI/chat-optimized | 0.90 / 0.90 |
| Mixtral (8x22b) | 176B MoE, eight 22B experts | 1.20 / 1.20 |

**LLM role → function (Table 41):** Planner — "Decomposes a complex query into atomic sub-queries and organizes the workflow." Executor — "Generates answers for sub-queries with or without contextual grounding." Summarizer — "Aggregates multiple intermediate outputs into a coherent final response." Thinker — "Performs systematic reasoning to produce detailed draft analyses before execution." Verifier — "Evaluates the correctness and quality of generated content before finalization."

## Worked Example 1: Multi-step arithmetic QA (Table 16)

**Original task (Step 1):** "A notebook costs $3 and a pen costs $2. What is the total cost of 4 notebooks and 3 pens?"

1. **Step 1 — Planner (LLaMA-3.1-8B):** decomposes into three sub-queries — Q1 "Compute the subtotal for 4 notebooks at $3 each." (Q2) pen subtotal; (Q3) "Using the subtotals ($12 and $6), prepare the combined information for final reasoning." (Acc 0, cost 110)
2. **Step 2 — Executor (Qwen2.5-7B):** Q1 → computes 4 × 3 = 12. (Acc 0, cost 95)
3. **Step 3 — Executor (Gemma-2-9B):** Q2 → computes 3 × 2 = 6. (Acc 0, cost 125)
4. **Step 4 — Executor (LLaMA-3.1-8B):** Q3 → returns structured summary: "Notebook subtotal = 12; Pen subtotal = 6." (Acc 0, cost 140)
5. **Step 5 — Summarizer (LLaMA-3-70B-ChatQA):** "Summarize all intermediate results into a concise final reasoning context." → generates "Total = 12 + 6." (Acc 0, cost 480)
6. **Step 6 — Executor (Qwen2.5-14B):** "Given the original question and the summarized reasoning (12 + 6), compute the final result." → "The total cost is $18." (Acc 1, cost 260)

## Worked Example 2: Code task with nested planning (Table 17)

**Original task (Step 1):** "Implement `remove~~d~~igits(s: str) -> str`."

1. **Step 1 — Planner (LLaMA-3.1-8B):** produces two sub-queries — Q1 "Describe the rule for removing digits from a string." (Q2) "Outline the implementation steps for `remove~~d~~igits`." (Acc 0, cost 120)
2. **Step 2 — Executor (Qwen2.5-7B):** Q1 → returns rule: iterate over characters and keep only non-digit characters. (Acc 0, cost 95)
3. **Step 3 — Planner (LLaMA-3.1-8B) — second planning round:** decomposes Q2 into (Q2a) "Describe filtering logic for keeping non-digit characters." (Q2b) "Describe how to construct the final output string." (Acc 0, cost 115)
4. **Step 4 — Executor (CodeGemma-7B):** Q2a → explains: check each character with `not ch.isdigit()`. (Acc 0, cost 200)
5. **Step 5 — Executor (Qwen2.5-7B):** Q2b → describes: collect filtered characters and join them into a new string. (Acc 0, cost 95)
6. **Step 6 — Summarizer (LLaMA-3-70B-ChatQA):** "Summarize Q2a and Q2b into a unified implementation plan." → concise plan: filter non-digit characters → join into result. (Acc 0, cost 480)
7. **Step 7 — Summarizer (LLaMA-3-70B-ChatQA):** "Combine Q1's rule with the summarized plan from Step 6." → merged reasoning: removal rule + full implementation steps. (Acc 0, cost 480)
8. **Step 8 — Executor (Qwen2.5-14B):** "Using the initial query and merged summary, produce the final Python function." → returns final function: "remove~~d~~igits". (Acc 1, cost 260)

## Worked Example 3: Single-step natural QA (Table 18)

**Original task (Step 1):** "Who painted the Mona Lisa?"

- **Step 1 — Executor (Qwen2.5-14B), only step:** receives the original query directly and immediately produces "The Mona Lisa was painted by Leonardo da Vinci." (Acc 1, cost 85)

This is the simplest execution path: the planner classifies the query as needing no decomposition and routes it through an executor-only step, illustrating GraphPlanner's adaptive decision to skip workflow construction for easy queries.

**Covers:** Appendix K (Prompt Usage)
