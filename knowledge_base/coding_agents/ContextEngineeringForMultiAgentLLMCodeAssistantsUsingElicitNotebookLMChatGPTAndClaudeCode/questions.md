---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code

### Q1. Why do single-agent LLM coders fail on repository-level tasks, and why can't a fixed static context like one CLAUDE.md file fix it?

> [!tip]- Answer
> Single-agent coders struggle on multi-file tasks because limited context windows and hallucinations on unfamiliar APIs cause them to miss distant-file edits or misuse libraries. A fixed static context cannot cover every task's needs, so the baseline Claude Code agent with basic CLAUDE.md produced incomplete or incorrect solutions on non-trivial features. See [[wiki/01-context-engineering-multi-agent-code|Context Engineering for Multi-Agent LLM Code]].

### Q2. What are the four components of the proposed context-engineering workflow, and which prior results motivate role decomposition and retrieval?

> [!tip]- Answer
> The workflow is (1) GPT-5 Intent Translator producing a structured task spec, (2) Elicit semantic retrieval of docs/research, (3) NotebookLM synthesis into a concise summary/TOC with Q&A, and (4) a Claude Code multi-agent team (planner, coder, tester, reviewer) with a vector DB and iterative refinement. It is motivated by MASAI's 28.3% on SWE-Bench Lite via sub-agent specialization, HyperAgent's 31.4% on SWE-Bench Verified with a Planner/Navigator/Editor/Executor team, and AllianceCoder's ~20% pass@1 gain from retrieved API descriptions. See [[wiki/01-context-engineering-multi-agent-code|Context Engineering for Multi-Agent LLM Code]].

### Q3. How do CodePlan-style planning and DARS-style iteration differ, and what does this system borrow from each?

> [!tip]- Answer
> CodePlan generates an explicit high-level pseudocode plan of dependencies and subgoals before coding, which the system mirrors with its GPT-5 Intent Translator and Planner agent. DARS adds dynamic action re-sampling — branching to alternative strategies at decision points and using test feedback to pick the best — reaching 47% pass@1 on SWE-Bench Lite. See [[wiki/02-planning-iterative-refinement|Planning and Iterative Refinement]].

### Q4. How do the Elicit/NotebookLM external pipeline and the repository retrieval pipeline work?

> [!tip]- Answer
> Elicit semantically retrieves top-k (k = 3–5) papers, docs, and guides from task-spec key terms, and NotebookLM distills them into a high-signal TOC summary plus Q&A pairs instead of dumping long paragraphs. Repository retrieval embeds the RainMakerz codebase with a code-specialized embedding model, chunks by function/class via tree-sitter AST parsing into ChromaDB/Zilliz, and combines semantic search with grep/file-path lexical fallback. See [[wiki/02-planning-iterative-refinement|Planning and Iterative Refinement]].

### Q5. What are the L1–L5 context layers, and how do isolated sub-agent contexts plus shared CLAUDE.md memory work together?

> [!tip]- Answer
> Each agent prompt receives L1 Task Specification, L2 External Knowledge (Elicit/NotebookLM), L3 Project Memory (CLAUDE.md, internal docs), L4 Retrieved Code Context (vector DB, grep), and L5 Execution Artifacts (diffs, logs, tests). Each sub-agent (e.g. backend-architect: sonnet model, Read/Write/Edit/Bash tools) runs in an isolated window with only task-relevant data plus preloaded CLAUDE.md background (architecture overviews, style rules, known bugs), preventing cross-phase contamination. See [[wiki/03-claude-multi-agent-architecture|Claude Multi-Agent Architecture: Specialist Sub-Agents, Isolated Contexts, and Delegation Loop]].

### Q6. How does the plan–delegate–test–review loop run, and what did the CustomBlock case study and 5-task evaluation show?

> [!tip]- Answer
> The orchestrator plans (steps mapped to files), delegates per-step slices with code snippets to specialists, validates via `npm test` with re-try on failure, runs a reviewer checklist (type safety, performance, security), then outputs a unified diff for GitHub Actions CI. On 5 RainMakerz tasks the multi-agent system scored 4/5 (80%) single-shot with zero hallucinated APIs (e.g. using real `renewSession()` over invented `refreshToken()`), versus 2/5 (40%) for the single-agent baseline that skipped registry and type updates. See [[wiki/03-claude-multi-agent-architecture|Claude Multi-Agent Architecture: Specialist Sub-Agents, Isolated Contexts, and Delegation Loop]].

### Q7. What does the richer context cost in tokens, and which two mechanisms were credited with the gains?

> [!tip]- Answer
> A successful multi-agent task used ~30–40 messages and ~100k tokens versus 10k–20k for a few single-agent turns (~3–5× overhead), partly offset because complex baselines balloon toward 50k tokens with retries and debugging chats. Gains were traced to intent clarification plus retrieval augmentation (e.g. a retrieved debounce explanation fixing an API-call bug the baseline patched superficially) and to role separation plus the reviewer agent catching null-pointer and security issues. See [[wiki/04-results-discussion-efficiency-cost|Efficiency and Cost. The Richer Context]].

### Q8. Should a team with a large codebase but sparse tests and tight token budgets adopt this workflow as-is?

> [!tip]- Answer
> No — adopt it only with safeguards, because sparse tests risk false "complete" judgments, irrelevant Elicit hits add confusing noise, the fixed plan → code → test → review sequence cannot dynamically re-plan, and the ~3–5× token cost bites at scale. The justified path is piloting where tests are strong, adding retrieval ranking/filtering, human plan approval, and cost controls (caching, compression, smaller sub-agent models) before production CI use. See [[wiki/04-results-discussion-efficiency-cost|Efficiency and Cost. The Richer Context]].
