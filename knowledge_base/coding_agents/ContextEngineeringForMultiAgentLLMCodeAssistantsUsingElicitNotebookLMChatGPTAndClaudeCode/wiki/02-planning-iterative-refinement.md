> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Planning and Iterative Refinement
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
---
## Planning and iterative refinement
**Covers:** CodePlan planning; DARS re-sampling; iteration in this system

| Approach | Mechanism | Reported result |
|---|---|---|
| CodePlan [3] | High-level pseudocode plan followed step-by-step; outline dependencies and subgoals before final code | Improved multi-step reasoning (no numeric claim in chunk) |
| DARS (Aggarwal et al., 2025) [4] | Dynamic action re-sampling: branch at decision points, try alternative strategy, use feedback (e.g., test results) to choose best outcome | 47% pass@1 on SWE-Bench Lite |
| This system | Intent Translator and Planner decompose the problem; multi-agent loop re-runs tests and adjusts code; no full branching yet | Adaptive branching noted as future enhancement |

> "DARS achieved a 47% pass@1 on SWE-Bench Lite with this method, indicating the value of exploring multiple solution trajectories."

## Retrieval-augmented code generation
**Covers:** Traditional search vs semantic retrieval; AllianceCoder; this system's two-source retrieval

- Traditional code search (keyword or AST-based) finds relevant context, but recent work uses semantic retrieval over unstructured information.
- AllianceCoder (Gu et al., 2025) [5]: chain-of-thought breaks a query into sub-tasks and retrieves pertinent API descriptions for each; conclusion — in-context code and API documentation yield significant gains, whereas blindly retrieving similar code examples can sometimes hurt performance.
- This system retrieves (1) external knowledge (papers, guides) related to the task via Elicit and (2) internal codebase knowledge via a vector database and search tools.
- RAG agents augmenting prompts with repository snippets and commit history show improved bug-fixing accuracy; this work extends that by engaging documents through NotebookLM to extract distilled insights.
- Figure 1 (p. 3): end-to-end pipeline — intent translation, retrieval and synthesis, orchestrated multi-agent coding with tools and memory (Intent Translator GPT-5, Semantic Retrieval Elicit, Knowledge Synthesis NotebookLM, Claude Orchestrator, backend/frontend/devops/reviewer sub-agents, VectorDB, MCP tools, repository, CI/CD).

## Agent tooling and debugging
**Covers:** Tool-use frameworks; Claude Code MCP tools; SeaView trajectory inspection

| Item | Role per chunk |
|---|---|
| LangChain Agents, HuggingGPT | Enable LLMs to invoke tools and other models; tailoring to software engineering remains active research |
| Claude Code | Built-in custom tools via Model Completion Protocol servers and multi-agent configurations; used here for running tests and analyzing code complexity |
| SeaView [6] | Visualizes and inspects trajectories of software-engineering agents; motivates better debugging interfaces for long action sequences (often tens of thousands of tokens) |
| This work | Relies on logs and intermediate results; SeaView-style visualization could aid future development and evaluation |

## Methodology: Intent Translation with GPT-5
**Covers:** Section 3 workflow start; disambiguation into a structured spec

- Input: ambiguous natural-language query for a code change or feature.
- GPT-5 Intent Translator reformulates it into a structured specification/task outline via a step-by-step-breakdown prompt that clarifies implicit requirements (e.g., which calendar library, what data to display).
- Worked example: "Add a calendar view to the scheduling page" becomes "update UI component X to include a calendar widget; fetch data Y from the backend API; adjust styling and add unit tests".
- Purpose stated: front-load clarification to reduce the burden on coding agents to interpret fuzzy instructions — "similar in spirit to the planning step in CodePlan but performed by a distinct, specialized model."

## Semantic literature retrieval with Elicit; knowledge synthesis with NotebookLM
**Covers:** External retrieval (top-k) and NotebookLM distillation

- Elicit performs semantic (not keyword) search over papers, documentation, and Q&A for algorithm descriptions, API usage examples, and best-practice guidelines (e.g., React calendar library docs, scheduling UI design paper), fed by key terms from the task spec such as "calendar widget React TypeScript library".
- Top-k results fetched as PDFs or text: k = 3–5.
- NotebookLM receives all retrieved documents and is prompted for a concise table-of-contents (TOC) summary of each plus answers to implementation questions (e.g., "What are the steps to integrate the chosen calendar library?", "What pitfalls or edge cases are noted?").
- Output is structured as key bullet points or Q&A pairs rather than long paragraphs; NotebookLM's multi-document synthesized overview maintains a high signal-to-noise ratio.
- Figure 2 (p. 4): retrieval pipeline — code-aware chunking (AST chunker, embedder) and dual-index backend (Chroma, Zilliz) with a unified adapter, query → rerank → snippets for agent generation.

## Repository context retrieval
**Covers:** RainMakerz codebase indexing: embeddings, chunking, hybrid search

| Choice | Detail from chunk |
|---|---|
| Target repo | RainMakerz (large; full codebase infeasible as prompt context) |
| Vector DB | ChromaDB and Zilliz both experimented with |
| Embeddings | Code-specialized embedding model (OpenAI's code-embedding model) into high-dimensional vectors |
| Chunking | By function or class definitions using an AST parser (tree-sitter) |
| Query | Refined task spec → top relevant fragments by embedding proximity |
| Lexical fallback | grep and file-path search for exact identifier matches via Claude agents |
| Example | SchedulerPage component or CalendarService class fragments retrieved with file names and relevant lines as supplementary context |

## System architecture and agent orchestration (4 / 4.1)
**Covers:** Claude multi-agent design: hub-and-spoke orchestrator and specialist roles

- Centralized orchestrator-worker (hub-and-spoke): a primary Claude "Manager" coordinates specialist sub-agents, each with its own context and role.
- Roles created: backend-architect (senior back-end engineer with file read/write, edit, bash access), frontend-specialist, devops-engineer, code-reviewer, reflecting a development team.
- Agent definitions are YAML/Markdown files under `.claude/agents/` (Listing 1 excerpt), auto-loaded so the orchestrator can invoke any agent by name.
- Figure 3 (p. 5): orchestrator delegates to backend/frontend/devops/reviewer sub-agents acting via Liveblocks, Supabase, API routes, frontend, CI/CD, Vector DB, and MCP tools (runtime and tooling layer).
