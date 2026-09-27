> [[index|Wiki]] | [[summary|Summary]]

# Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code — Digest

## 1. [[wiki/01-context-engineering-multi-agent-code|Context Engineering for Multi-Agent LLM Code]]

**In one sentence:** Single-agent LLM coders fail on repository-level tasks for lack of task-specific context, so the paper proposes context engineering — a four-component workflow (GPT-5 intent clarification, Elicit retrieval, NotebookLM synthesis, Claude Code multi-agent execution) that improves single-shot accuracy and project-context adherence on a large real codebase.

## Key points

- Single-agent prompt-driven coders struggle on multi-file, repository-level tasks because of limited context windows and hallucinations on unfamiliar APIs or frameworks outside training data.
- A fixed static context such as one `CLAUDE.md` file cannot cover every task; in early experiments a default Claude Code agent with basic `CLAUDE.md` produced incomplete or incorrect solutions, missing distant-file edits or misusing unfamiliar libraries.
- Prior multi-agent and retrieval systems prove the mechanism: MASAI's specialized sub-agents reached 28.3% resolution on SWE-Bench Lite, HyperAgent's Planner/Navigator/Editor/Executor team reached 31.4% on SWE-Bench Verified, and AllianceCoder's retrieved API descriptions yielded up to 20% higher pass@1 accuracy.
- The proposed workflow has four components: (1) GPT-5 Intent Translator rewriting the request into a structured task specification, (2) Elicit-based semantic retrieval of documentation/research, (3) NotebookLM synthesis into a concise summary/table-of-contents with follow-up Q&A, and (4) a Claude Code multi-agent system (planner, coder, tester, reviewer) plus a vector database for code context with iterative refinement.
- Context engineering is defined as systematically constructing and supplying all relevant information for a task — clarified intent, high-level plans, external knowledge, repository-specific details — via a coordinated multi-agent process.
- The system was implemented on the RainMakerz Next.js application (~180K lines of code), where it implemented complex features in a single generation cycle — e.g. a new interactive visualization module spanning front-end and back-end — while a baseline single-agent Claude often omitted needed steps.
- The authors claim explicit context layering plus agent role decomposition fixes failure modes of earlier methods, matching or exceeding CodePlan and DARS on similar tasks, and outline a production path via CI integration (Claude Code in GitHub Actions for automated reviews) with cost, scalability, and safety safeguards.

## 2. [[wiki/02-planning-iterative-refinement|Planning and Iterative Refinement]]

**In one sentence:** Complex coding is treated as a planning problem where an explicit pseudocode/spec plan (CodePlan-style, via an Intent Translator/Planner) guides generation, test-feedback-driven iteration and branch-and-resample strategies (DARS, 47% pass@1 on SWE-Bench Lite) correct errors, and semantic retrieval plus agent tooling supply the external and repository context.

## Key points

- CodePlan [3] generates a high-level pseudocode plan outlining dependencies and subgoals before final code, improving multi-step reasoning; the system mirrors this with an Intent Translator and Planner agent.
- DARS (Aggarwal et al., 2025) adds dynamic action re-sampling — branching to an alternative strategy at decision points and using feedback such as test results to pick the best outcome — achieving 47% pass@1 on SWE-Bench Lite.
- The current system does not implement full branching but does iterate and self-correct inside the multi-agent loop (re-running tests, adjusting code), with adaptive branching left as future work.
- AllianceCoder (Gu et al., 2025) found in-context code plus API documentation gives significant gains while blindly retrieving similar code examples can hurt; it uses chain-of-thought to split queries into sub-tasks and retrieve per-sub-task API descriptions.
- The system retrieves two context kinds: (1) external knowledge (papers, guides) via Elicit and (2) internal codebase knowledge via a vector database plus search tools, then distills documents through NotebookLM instead of dumping long paragraphs.
- Claude Code supplies custom tools via Model Completion Protocol servers and multi-agent configurations (e.g., running tests, analyzing complexity); SeaView [6] is cited as a trajectory-visualization debugger for long agent runs of tens of thousands of tokens.
- Intent translation uses GPT-5 to turn an ambiguous request (e.g., "Add a calendar view to the scheduling page") into an explicit task list (update UI component X, fetch data Y, styling, unit tests), clarifying implicit requirements such as library choice and data needs.
- Repository retrieval on the large RainMakerz repo embeds code with a code-specialized embedding model (OpenAI's code-embedding model), chunks by function/class with tree-sitter AST parsing, queries ChromaDB/Zilliz semantically, and combines this with grep/file-path lexical search.

## 3. [[wiki/03-claude-multi-agent-architecture|Claude Multi-Agent Architecture: Specialist Sub-Agents, Isolated Contexts, and Delegation Loop]]

**In one sentence:** Claude Code uses an orchestrator that delegates to role-specialist sub-agents (e.g. backend-architect) with isolated context windows plus shared CLAUDE.md memory, layered context inputs, and a plan–delegate–test–review loop that completed 4/5 tasks (80%) versus 2/5 (40%) for a single-agent baseline.

## Key points

- The backend-architect profile is defined as `name: backend-architect`, `description: Design RESTful APIs, microservice boundaries, and database schemas`, `model: sonnet`, `tools: Read, Write, Edit, Bash`, and doubles as planner for backend-heavy tasks.
- Each sub-agent runs with an isolated context window containing only task-relevant information plus persistent project context, preventing cross-contamination between workflow phases.
- Shared background (architectural overviews such as the Figure 3 system design, coding style guidelines, known bugs and previous solutions for RainMakerz) is preloaded from a persistent CLAUDE.md file into every agent's context.
- Context is layered L1–L5 into each agent prompt: L1 Task Specification (Intent Translator), L2 External Knowledge (Elicit & NotebookLM), L3 Project Memory (CLAUDE.md, internal docs), L4 Retrieved Code Context (Vector DB, grep), L5 Execution Artifacts (diffs, logs, test results).
- The orchestration loop runs Planning → Task Delegation → Iterative Coding and Validation (`npm test` feedback, simple re-try rather than multi-trajectory branching as in DARS [4]) → Code Review and Refinement → Output and Deployment (unified diff, GitHub Actions CI, possible auto-merge).
- Dividing work reduces prompt tokens per agent and preserves coherence on large tasks; execution is currently sequential with parallel spawning of independent sub-tasks possible per Anthropic multi-agent research [7], unused here because steps had dependencies.
- On 5 RainMakerz tasks the multi-agent system achieved 4/5 single-shot successes (80%) with no human corrections versus 2/5 (40%) for the single-agent baseline, every generated function/class existed in the repo (e.g. correctly using `renewSession()` instead of hallucinated `refreshToken()`), and the one failure still made partial progress by identifying a misconfigured library.

## 4. [[wiki/04-results-discussion-efficiency-cost|Efficiency and Cost. The Richer Context]]

**In one sentence:** The richer multi-agent context costs roughly 3–5× more tokens (~100k vs 10k–20k baseline) but is justified by largely autonomous correct solutions, with gains traced to intent clarification plus retrieval augmentation and to role separation plus a reviewer agent, tempered by retrieval noise, brittle fixed sequencing, cost/scale, and test-suite dependence.

## Key points

- A single task exchanged around 30–40 messages across all agents and consumed roughly 100k tokens total (input + output), versus 10k–20k tokens for a few prompt-response turns in the single-agent approach — about 3–5× more tokens on successful tasks.
- The overhead is presented as justified: the baseline often needed multiple attempts or lengthy debugging chats that push its count closer to 50k tokens on a complex task, while the multi-agent system gets the job done largely autonomously, saving developer time.
- Intent translation (GPT-5) mattered because feeding the raw ambiguous query to code agents led them to focus on the wrong sub-problem or skip a requirement; a clarified spec up front produced more relevant searches and a more coherent plan.
- External knowledge injection (Elicit + NotebookLM) was validated where the fix needed concepts outside the codebase — e.g. a debounce mechanism for an API call, where a retrieved blog-post explanation guided correct implementation while the baseline attempted a simplistic fix that missed the root cause.
- Orchestration lessons: early runs had two agents editing the same file (e.g. frontend and backend agents on a shared config) or each assuming the other would handle a step; fixed by refining the Planner prompt to explicitly assign sub-tasks and adding a simple orchestrator lock against concurrent edits to the same file.
- The dedicated reviewer agent was invaluable, catching subtle issues coding agents overlooked — potential null pointer access and minor security concerns — supporting the claim that AI coders benefit from a second pair of eyes even when code "works".
- Limitations and outlook: irrelevant Elicit results add confusing noise; the plan → code → test → review sequence is brittle with no dynamic re-planning; cost may bite on very large projects; sparse test suites can cause false "complete" judgments and error tracing across agents is hard (SeaView [6] suggested); generality is claimed via the Next.js/TypeScript target plus a drop-in database-migrator agent, with future RL meta-control, search-based/graph planning (AllianceCoder), and human-in-the-loop plan approval.

## The argument in five moves

1. Single-agent coders fail on repository-level work because a fixed static context cannot supply task-specific intent, plans, external knowledge, and scattered repo details.
2. The fix is context engineering: a four-stage pipeline (GPT-5 intent spec → Elicit semantic retrieval → NotebookLM distilled synthesis → Claude Code multi-agent execution) grounded in CodePlan planning, DARS-style test-feedback iteration, AllianceCoder retrieval, and MASAI/HyperAgent role decomposition.
3. Execution uses a hub-and-spoke Claude orchestrator with isolated per-agent contexts, shared CLAUDE.md project memory, L1–L5 layered prompt inputs, AST-chunked hybrid vector-plus-lexical repo retrieval, and a plan–delegate–test–review–deploy loop.
4. On the ~180K-line RainMakerz Next.js app this yields 4/5 single-shot successes versus 2/5 for the single-agent baseline, with zero hallucinated APIs and end-to-end multi-file features completed autonomously.
5. The gain costs ~3–5× tokens (~100k vs 10k–20k) but saves developer time; it holds only with good retrieval ranking, dynamic re-planning, adequate test suites, and cost controls — the stated path to production and future work.
