> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Study Design: LiveCodeBench and SWE-bench Verified Datasets
**In one sentence:** The study uses LiveCodeBench release_v6 (1,055 Python problems from May 2023–April 2025, plus Self-Repair, Code Execution, and Test Output Prediction variants) alongside human-validated SWE-bench Verified issue-fix pairs, and operationalizes seven IBQ-G influence tactics (nine scenarios with Pressure Alternative and Neutral control) with dataset-adapted, tone-controlled prompts across five open-weight models.
## Key points
- LiveCodeBench contains Python coding challenges similar to LeetCode, AtCoder, and CodeForces.
- Beyond code generation, LiveCodeBench adds Self-Repair (fixing incorrect code using execution info and failed tests; debugging ability), Code Execution (predicting program output; comprehension ability), and Test Output Prediction (predicting expected outputs from a description plus test input; test generation ability).
- Experiments use LiveCodeBench release_v6 with 1,055 problems released between May 2023 and April 2025.
- SWE-bench consists of issue-fix pairs mined from real-world GitHub repositories, answered in diff format and often requiring multi-file edits; SWE-bench Verified is its human-validated subset filtering out overly difficult or impossible tasks so tests are scoped and descriptions clear.
- Eleven IBQ-G tactics were narrowed to seven by excluding Apprising (personal gain implausible for LLMs), Collaboration (implies pausing for user input), Consultation (implies partial guidance), and Coalition (overlap with legitimating tactics plus multi-entity complexity).
- Each of the seven tactics was operationalized from its four IBQ-G behavioural items (e.g. Inspirational Appeals "You have the opportunity to do something exciting and worthwhile."), plus a Pressure Alternative interpretation and a Neutral baseline, for nine tactic scenarios total.
- Prompts were dataset-adapted (developer solving self-contained challenges for LiveCodeBench; professional/collaborative setting with roles and policies for SWE-bench Verified) with consistent semi-formal tone so effects reflect tactics, not tone or sentiment.
- Five open-weight models via Groq API (Llama 3.1 8B, Llama 3.3 70B, Llama 4 Maverick 17B 128e, DeepSeek R1 Distill Llama 70B, Qwen 3 32B non-reasoning), each prompt-task combination run three times with mean and variance recorded.
---
## LiveCodeBench
**Covers:** Section 3.1.1 (LiveCodeBench dataset)

The LiveCodeBench dataset contains Python coding challenges similar to those found on competitive coding platforms such as LeetCode, AtCoder, and CodeForces. Beyond code generation, three additional problem types are constructed from the curated samples:

| Problem type | Task | Ability evaluated |
|---|---|---|
| Self-Repair | Fixing existing incorrect code from information about its execution and failed test cases | Debugging ability |
| Code Execution | Predicting the output of a given Python program | Code comprehension ability |
| Test Output Prediction | Given a natural language problem description (including any example input-output pairs) and a specific test input, predicting the expected outputs | Test generation ability |

> "For our experiments, we use the release_v6 version of LiveCodeBench, containing 1,055 problems released between May 2023 and April 2025."

## SWE-bench Verified
**Covers:** Section 3.1.2 (SWE-bench Verified)

The SWE-bench dataset consists of issue-fix pairs mined from real-world GitHub repositories. Rather than focusing on the creation of a single function or file, responses must be written in diff format, with correct patches often requiring edits to multiple files. SWE-bench Verified is a human-validated subset of SWE-bench, created in response to some SWE-bench tasks which were overly difficult or impossible to solve. Using human annotators, every instance from the original SWE-bench test set was filtered to ensure that unit tests were appropriately scoped and problem descriptions were clearly specified.

## Operationalizing influence tactics in prompt design
**Covers:** Section 3.2 (Operationalizing Influence Tactics in Prompt Design)

Each psychological influence tactic was operationalized into a reproducible prompt template, drawing directly from the item descriptions in Yukl et al.'s IBQ-G. Starting from the 11 tactics, round-table discussion excluded four as less applicable or ambiguous in one-shot developer-LLM problem solving:

| Excluded tactic | Reason given |
|---|---|
| Apprising | Framing a task as personally beneficial was conceptually difficult and ambiguous for an LLM given the benchmark tasks |
| Collaboration | Offering to assist or provide resources implied the AI should pause for user input instead of delivering a complete solution independently |
| Consultation | Asking the target for improvements or help planning implies receipt of partial guidance rather than a full solution |
| Coalition | Enlisting aid from others overlaps conceptually with legitimating tactics (external validation) and adds unnecessary multi-entity coordination complexity |

This resulted in seven tactics. Prompt design followed the per-tactic IBQ-G items: each tactic has four associated behaviours treated as requirements, with IBQ-G items referenced by number only to respect the copyright holder. Example verbatim requirement mapping:

> "one requirement for the 'Inspirational Appeal' tactic is to frame a proposed activity or change as an opportunity to do something really exciting and worthwhile. As such, our corresponding prompt includes the sentence 'You have the opportunity to do something exciting and worthwhile.'"

While designing the Pressure prompt, two interpretations of the IBQ-G were found, so an alternative formulation (Pressure Alternative) was designed and used; with a Neutral baseline (no influence tactics) there are nine tactic scenarios for evaluation in total.

Prompts were prefixed to problem descriptions and adapted per dataset: LiveCodeBench prompts written from the perspective of a developer solving self-contained programming challenges; SWE-bench Verified prompts implying a professional or collaborative software development setting, sometimes invoking roles, responsibilities, and policies. A consistent semi-formal tone was maintained across all prompts to convey the tactic clearly, controlling for tone and emotional expressiveness so observed effects could be attributed to the influence tactics themselves. Prompts were reviewed and refined through a three-round author discussion process for conceptual validity and consistency, with Figure 2 showing prompt structure and Table 2 giving per-dataset tactic examples.

## Studied models
**Covers:** Section 3.3 (Studied Models)

Five open-weight LLMs accessed via the Groq API, chosen for diverse architectures, scales, and reasoning capabilities:

| Model | Description given |
|---|---|
| Llama 3.1 8B | Small-scale, dense transformer; accessibility and representative architecture |
| Llama 3.3 70B | Larger Llama variant; scaling effects and parameter sensitivity |
| Llama 4 Maverick 17B 128e | Recent MoE model with sparse activation and routing; efficient large-scale training advances |
| DeepSeek R1 Distill Llama 70B | Reasoning-optimized variant; effects of reasoning-tuned optimization |
| Qwen 3 32B (non-reasoning) | Non-Llama-family MoE for diversity; non-reasoning variant used due to API issues with reasoning mode |

The Llama-family-heavy pool was intentional for reproducibility, transparent inspection, and uniform deployment under a single API; commercial models such as GPT-4o or Claude were excluded for reproducibility and cost feasibility. Each prompt-task combination was executed three times per model, with mean and variance of performance metrics recorded.

**Covers:** Sections 3.1.1–3.3 (LiveCodeBench release_v6; SWE-bench Verified; tactic operationalization; studied models)
