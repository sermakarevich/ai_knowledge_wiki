> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code — In Plain Language

## What is this about?

This paper asks a simple question: why do AI coding assistants fail on real, large codebases, and how can we fix that?

A single AI coder works fine for small snippets. But on a real repository — hundreds of files, scattered logic, unfamiliar libraries — it misses edits in distant files, invents functions that do not exist, or misunderstands a vague request.

The authors' answer is "context engineering": instead of giving one agent one big prompt, systematically build the right information for each task and deliver it through a team of specialist agents.

Their pipeline has four stages:

1. A GPT-based Intent Translator rewrites a vague request ("add a calendar view") into a concrete task list (which UI component, which API, which tests).
2. Elicit retrieves external knowledge — docs, papers, guides — relevant to the task.
3. NotebookLM compresses those documents into a short summary with Q&A, not a pile of long text.
4. A Claude Code team (planner, coders, tester, reviewer) executes the plan, pulling repository context from a vector database plus ordinary search.

The test bed is RainMakerz, a ~180K-line Next.js app, where the team implemented multi-file features in a single automated run.

## Why does it matter?

Because repository-level coding is the real job, and single agents are measurably bad at it.

On five RainMakerz tasks, the multi-agent system succeeded on 4 out of 5 (80%) with no human fixes, versus 2 out of 5 (40%) for a single-agent baseline. Every function it used actually existed in the repo — for example it called the real `renewSession()` where the baseline invented a nonexistent `refreshToken()`.

Prior work points the same way: specialist teams (MASAI, HyperAgent) beat single agents on SWE-Bench, retrieved API docs boost accuracy by up to 20%, and explicit plans plus test-feedback iteration (CodePlan, DARS) fix multi-step errors.

The practical payoff is fewer half-finished features, fewer hallucinated APIs, and less developer babysitting — at the cost of more tokens per task.

## How does it work?

Think of it as a small software team with a research assistant attached.

**Step 1 — Clarify the request.** The Intent Translator turns ambiguity into a spec. "Add a calendar view to the scheduling page" becomes: update component X, fetch data Y from the backend, adjust styling, add unit tests. This prevents agents from solving the wrong sub-problem.

**Step 2 — Fetch outside knowledge.** Elicit does semantic search (top 3–5 results) for things like "calendar widget React TypeScript library". NotebookLM then distills those documents into bullet points and answers questions such as "what are the integration steps and pitfalls?" One real example: a retrieved explanation of debouncing guided a correct API-call fix the baseline got wrong.

**Step 3 — Fetch inside knowledge.** The repo is indexed by function/class chunks (parsed with tree-sitter), embedded with a code-specific model, and stored in ChromaDB/Zilliz. Agents query it semantically and fall back to grep and file-path search for exact names.

**Step 4 — Plan, delegate, test, review.** A central orchestrator runs a loop: Planner writes a file-by-file plan, frontend/backend specialists implement steps, tests run via `npm test` with failures fed back for fixes, and a dedicated reviewer checks type safety, performance, and security. Output is a summary plus a unified diff, ready for CI and pull requests.

Two design details matter. Each agent gets an isolated context (only its task plus shared project memory) so phases do not contaminate each other. And every prompt is layered: task spec, external knowledge, project memory, retrieved code, and execution artifacts like diffs and logs.

## Where can this be used?

- Large web codebases (the demonstrated case: Next.js/TypeScript) where features span frontend, backend, types, and registries.
- Bug fixes needing outside concepts — rate limiting, debouncing, unfamiliar library APIs — where docs matter as much as repo code.
- Teams wanting AI-assisted CI: Claude changes re-tested in GitHub Actions, with possible auto-merge when checks pass.
- Other stacks by swapping parts: the authors added a database-migrator agent for SQL changes without touching the orchestrator, and suggest Java microservices or data-science notebooks as next targets.
- Human-in-the-loop setups where a person approves the plan before code is written.

It fits less well where tests are sparse (the system may wrongly declare victory), retrieval is noisy, or token budgets are tight.

## Conclusions & takeaways

The core claim: give models not more information, but the right information in the right form, split across manageable subtasks.

What the evidence supports: clarified intent plus retrieved docs plus role separation plus a reviewer reliably beats a single agent with a static prompt on complex, multi-file work.

What tempers it: the richer context costs ~100K tokens per task versus 10–20K for the baseline (about 3–5x), irrelevant retrieved papers can confuse the planner, the fixed plan-code-test-review sequence cannot yet re-plan from scratch, and debugging a wrong answer across agents is hard.

Future directions named in the paper: smarter retrieval ranking, dynamic or RL-based orchestration, search-based planning, caching and smaller specialist models for cost, and structured human checkpoints.

Bottom line: a coordinated team of narrow, well-briefed agents can do in one shot what a single clever agent fumbles — if you engineer what each one sees.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Context engineering | Deliberately assembling exactly the info an AI needs for one task, instead of one fixed prompt. |
| Intent translation | Rewriting a vague user request into an explicit step-by-step task spec. |
| Retrieval-augmented generation (RAG) | Pulling relevant docs or code into the prompt at generation time to ground the answer. |
| Semantic retrieval | Finding documents by meaning, not just matching keywords. |
| Vector database | A store of code or text as numeric embeddings so similar-meaning items can be searched quickly. |
| AST chunking | Splitting code by function or class boundaries (using a syntax tree) before indexing. |
| Sub-agent / specialist agent | A separate AI worker with one role, e.g. planner, frontend coder, backend coder, reviewer. |
| Orchestrator | The manager agent that assigns steps, passes context, and runs the test-review loop. |
| CLAUDE.md | A persistent project memory file with architecture, style rules, and known fixes shared by all agents. |
| Single-shot success | Producing working code that passes tests on the first automated attempt, with no human fixes. |
| Pass@1 | The share of tasks solved correctly on the very first try. |
| Hallucination | The model inventing a function, API, or fact that does not exist in the repo. |
