---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: siddsachar/row-bot

### Q1. What does the Row-Bot name stand for, and what kind of application is it?
> [!tip]- Answer
> The name defines the operating model: Reason through messy context, Orchestrate tools and model providers, and Work inside user-chosen files, repos, workflows, and channels.
> It is a local-first desktop AI assistant for doing real work with models, memory, and tools, keeping durable app data on the user's machine. See [[wiki/01-overview|Overview]].

### Q2. How does Row-Bot orchestrate larger tasks across parent and child agents?
> [!tip]- Answer
> A larger task runs through a focused Agent Profile with a visible goal, while the parent orchestrates scoped child agents for research, review, implementation, or follow-up work and joins required results.
> Durable checkpoints preserve approvals, steering, retries, stops, and recovery, and checkpoint-safe work budgets plus delegation limits bound long runs. See [[wiki/01-overview|Overview]].

### Q3. How do parallel Developer workspaces stay safe, and what happens to tool calls on restart?
> [!tip]- Answer
> Parallel writers target distinct existing local folders as separate Developer workspaces, with folder-scoped locks allowing concurrency while keeping one writer per shared folder.
> On restart, Row-Bot closes unanswered tool calls without replaying them and resumes the saved parent when required child results are ready. See [[wiki/01-overview|Overview]].

### Q4. How do Recommended Auto capability loading and rolling compaction manage context?
> [!tip]- Answer
> Recommended Auto keeps permitted core tools directly available and searches enabled MCP, plugin, Custom Tool, and channel capabilities only when a request needs them.
> Long conversations are metered and compacted into durable untrusted reference context preserving the newest turn and atomic tool-call/result groups, failing with an exact capacity message when the prompt cannot fit. See [[wiki/01-overview|Overview]].

### Q5. What model paths and privacy guarantees define Row-Bot's local-first stance?
> [!tip]- Answer
> Model paths span local Ollama models, provider keys, ChatGPT/Codex and Claude/Grok subscriptions or OAuth, and custom OpenAI-compatible endpoints, all behind explicit provider identity and reasoning controls.
> There is no account system, no hosted inference server, and no first-party telemetry; keys live in the OS credential store and calls go only to the chosen provider. See [[wiki/01-overview|Overview]].

### Q6. What rules does AGENTS.md impose on coding agents, and what do the root launchers contain?
> [!tip]- Answer
> AGENTS.md is canonical and ranks protecting local data/secrets above all else, forbidding first-party telemetry, secret commits, live-dependent default tests, hand-edited requirements.txt, and runtime code in root wrappers.
> The root app.py and launcher.py contain no application logic and only prepend src/ to sys.path before delegating to row_bot.app and row_bot.launcher.main. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Should a privacy-sensitive team doing local development work adopt Row-Bot, and what caveats apply?
> [!tip]- Answer
> Yes for teams that want local-first data, explicit provider choice, approval gates, and bounded orchestration, since secrets stay local and long runs are checkpointed and budget-limited.
> Caveats are the opt-in Computer Use beta's separately disclosed upstream telemetry, email-only vulnerability reporting with latest-stable-only support, and time-bound OSV exceptions expiring 2026-09-30. See [[wiki/02-top-level-files|top-level-files]].
