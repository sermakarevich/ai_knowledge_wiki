# Skill Retrieval Augmentation for Agentic AI

**Paper:** [Skill Retrieval Augmentation for Agentic AI (Su et al., 2026)](https://arxiv.org/abs/2604.24594)

## Human Readable TL;DR

Imagine you're a contractor who could theoretically use any tool ever invented, but your truck only holds a few tools at once. The old approach is cramming as many tools as possible into the truck -- but as warehouses grow to millions of tools, this breaks down. This paper proposes a smarter approach: keep tools in a giant warehouse, and retrieve exactly the right one for each job on demand. The twist they discover is that even when the right tool is fetched, workers often grab it whether or not they actually need it -- and sometimes don't grab it even when they do. The real bottleneck isn't finding tools; it's knowing when and whether to use them.

## TL;DR

This paper formalizes Skill Retrieval Augmentation (SRA) -- a paradigm where LLM agents dynamically retrieve executable capability packages ("skills") from large external corpora rather than relying on a fixed, pre-enumerated skill set. The authors build SRA-Bench (5,400 instances, 636 gold skills, 26,262 total skills) to evaluate the full pipeline across three stages: skill retrieval, skill incorporation, and skill application. Experiments on six LLMs reveal that retrieval-based skill augmentation substantially improves performance, but the dominant bottleneck is not retrieval quality -- it is the agent's failure to exhibit need-aware and relevance-aware skill-loading behavior.

---

## Problem & Motivation

Current agent systems equip LLMs with skills via explicit in-context enumeration: all available skills are summarized and injected into the prompt. This approach collapses under scale -- platforms like SkillsMP already host over 1 million distinct skills (as of April 2026), context budgets are exhausted, and accuracy in identifying the right skill degrades sharply.

SRA addresses this by treating skills as entries in a large external corpus to be retrieved on demand, analogous to how RAG addresses knowledge at scale -- but with a fundamentally different retrieval target: executable capability packages rather than declarative passages.

---

## Main Original Ideas

1. **Skill Retrieval Augmentation (SRA) paradigm** -- A three-stage pipeline formalization: (1) a retriever maps the user query to a ranked candidate list from a corpus of N skills; (2) the agent's incorporation module selects and adapts relevant candidates into its active context; (3) the agent applies incorporated skills during task solving. Crucially, the incorporated set S̃ may be empty if the agent judges its parametric capability sufficient.

2. **Skill as a typed artifact** -- A skill s_i is formally defined as (name, description, content, executable_payload): a natural-language interface coupled with invocable resources (code, tools). This distinguishes skills from both RAG documents (declarative only) and standalone APIs (no usage guidance).

3. **SRA-Bench** -- The first benchmark designed for decomposed SRA evaluation. Built by curating 5,400 capability-intensive instances from six source benchmarks (TheoremQA, LogicBench, ToolQA, MedCalc-Bench, CHAMP, BigCodeBench), constructing 636 gold skills via LLM drafting + expert revision, and mixing them into 25,626 web-crawled distractor skills to form a realistic 26,262-skill corpus.

4. **Gold skill construction via LLM-draft + expert revision** -- Three hard quality constraints: *generality* (skills describe reusable methods, not instance-specific answers), *correctness* (formulas, tool workflows, and code verified against authoritative references), and *leakage control* (worked examples use newly constructed instances, not benchmark inputs). Expert revision consistently adds recognition patterns, multi-branch edge cases, and tool-chaining workflows absent from LLM drafts.

5. **SR-Agents baseline family** -- Three practical skill-use strategies studied against Oracle and no-skill baselines: Full-Skill Injection (inject top-k BM25 results directly), LLM Selection (model chooses one skill from a top-50 catalog), and Progressive Disclosure (OpenClaw-style LOAD_SKILL action, model fetches on demand during reasoning).

6. **Discovery of the incorporation gap** -- Agents load skills at nearly identical rates regardless of (a) whether the gold skill is actually in the retrieved candidate set and (b) whether the task actually requires external capability. Skill-loading behavior is model-dependent with no monotonic scaling trend, revealing that scalable skill augmentation requires advances beyond retrieval.

---

## Key Findings

### End-task performance (%) -- representative results from Table 2

| Model | LLM Direct | Oracle Skill | LLM Selection | Full-Skill Injection |
|---|---|---|---|---|
| Llama-3.1-8B | 29.8 | **44.5** | 37.0 | 32.7 |
| Llama-3.3-70B | 47.8 | **64.4** | _59.2_ | 52.7 |
| Mistral-3.1-24B | 43.4 | **63.2** | _56.6_ | 48.5 |
| Qwen3-235B-A22B | 53.3 | **67.5** | _62.8_ | 56.2 |
| Qwen3-32B | 50.8 | **67.2** | 55.3 | 54.3 |
| Qwen3-4B | 38.8 | **61.6** | 53.3 | 45.5 |

Averages computed over all 5,400 instances. Bold = best; underlined = second best.

- SRA provides real gains: Oracle Skill consistently and substantially beats LLM Direct across all models and benchmarks.
- LLM Selection is the most reliable practical strategy -- it narrows the gap to Oracle Skill more consistently than the other retrieval-based strategies.
- Progressive Disclosure is theoretically ideal (the agent should load skills only when needed) but exhibits the least stable performance in practice.
- Retrieval-based methods remain well below the Oracle upper bound in most settings, confirming the headroom left by incorporation and application failures.
- Performance improvements are highly uneven across benchmarks: some tasks (e.g., BigCodeBench, MedCalc) benefit strongly; others less so.
- Agents load skills at similar rates regardless of whether the gold skill is in the retrieved set (RQ5: relevance-unawareness).
- Agents show no preference for loading skills on tasks that genuinely require external capability vs. tasks solvable from parametric knowledge alone (RQ6: need-unawareness).
- No monotonic trend with model size in skill-loading rationality -- larger models are not necessarily more need-aware.

---

## Suggestions & Future Directions

1. **Need-aware skill incorporation training** -- Current LLMs lack the ability to distinguish when external skill loading is actually necessary. Dedicated training signal for this decision is an open research need.
2. **Relevance-aware selection** -- Agents should load skills at higher rates when the gold skill is present and at lower rates when it is absent; this discrimination currently does not emerge from scale alone.
3. **Skill indexing and organization** -- New methods for organizing heterogeneous skill corpora to support both lexical and semantic retrieval beyond BM25/dense baselines.
4. **Quality control for web-crawled skills** -- The 25,626 distractor skills in SRA-Bench were scraped from GitHub, Skills.sh, and Hugging Face; noisy and malformed skills represent a practical challenge in deployed systems.
5. **Lifelong skill accumulation** -- Agents that autonomously identify capability gaps, request new skills, and integrate them into a growing personal corpus.
6. **Feedback-driven skill debugging and refinement** -- Using task execution outcomes to iteratively improve skill quality.
7. **Multi-skill coordination** -- CHAMP and BigCodeBench already require multiple concurrent gold skills; robust multi-skill retrieval and orchestration remains underexplored.

---

## Authors & Institutions

Weihang Su, Jianming Long, Qingyao Ai, Yichen Tang, Changyue Wang, Yiteng Tu, Yiqun Liu -- Department of Computer Science and Technology, Tsinghua University
