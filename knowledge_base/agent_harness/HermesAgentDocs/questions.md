---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Hermes Agent Documentation

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What is the one-command install for Linux/macOS/WSL2, and what must you do after it finishes?

> [!tip]- Answer
> Run `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`, then reload the shell (`source ~/.bashrc` or `source ~/.zshrc`) before starting with `hermes`. See [[wiki/01-installation-and-quickstart|Installation and Quickstart]].

### Q2. Where do secrets vs settings live, and which command routes values automatically?

> [!tip]- Answer
> Secrets in `~/.hermes/.env`, settings in `~/.hermes/config.yaml`; `hermes config set <KEY> <value>` routes each to the right file, with CLI args overriding both. See [[wiki/02-configuration-providers-cli|Configuration, Providers, and CLI]].

### Q3. What are the two built-in memory files, their sizes, and why is the snapshot frozen?

> [!tip]- Answer
> MEMORY.md (agent notes, 2,200 chars) and USER.md (user profile, 1,375 chars) in `~/.hermes/memories/`; injected once at session start and frozen to preserve the LLM prefix cache, with disk writes visible next session. See [[wiki/03-memory-skills-learning-loop|Memory, Skills, and the Learning Loop]].

### Q4. When should the agent use session search instead of memory, and why?

> [!tip]- Answer
> Session search (FTS5 over all past sessions, ~20ms, free) answers "did we discuss X?" specifics on demand; memory (~1,300 tokens, paid every prompt) holds only facts that must always be in context. See [[wiki/03-memory-skills-learning-loop|Memory, Skills, and the Learning Loop]].

### Q5. What does the background review do, and name two ways to make it cheaper or safer?

> [!tip]- Answer
> After each turn it replays the conversation and may save memories or patch skills; run it on a cheaper model, defer it on local GPUs, disable it, or gate writes with `write_approval` staging (`/memory pending`, `/skills pending`). See [[wiki/03-memory-skills-learning-loop|Memory, Skills, and the Learning Loop]].

### Q6. How do Bot Mode group chats coordinate, and when does a human get pulled in?

> [!tip]- Answer
> 2–6 Bots coordinate in serial rounds via @mentions (plus direct `message_agent` calls), escalate with @user, and surface a needs-you badge when human judgment is required. See [[wiki/04-messaging-gateway-bot-mode|Messaging Gateway and Bot Mode]].

### Q7. What is a toolset, and how do you limit one run to web + terminal tools only?

> [!tip]- Answer
> A toolset is a named group of tools enabled/disabled together; run `hermes chat --toolsets "web,terminal"` to scope that session, with per-platform presets and per-MCP-server `mcp-<server>` sets. See [[wiki/05-tools-integrations-mcp|Tools, Integrations, and MCP]].

### Q8. How is an MCP server declared, and how do you control which of its tools the agent sees?

> [!tip]- Answer
> Under `mcp_servers` in config.yaml as stdio (`command`+`args`+`env`) or HTTP (`url`+`headers`+`auth: oauth`), registered as `mcp_<server>_<tool>`; control with `enabled`, `tools.include` whitelists vs `tools.exclude` globs (include wins), plus prompts/resources toggles. See [[wiki/05-tools-integrations-mcp|Tools, Integrations, and MCP]].

### Q9. Why can unattended cron work be trusted — what makes it reviewable and undoable?

> [!tip]- Answer
> Jobs run in fresh isolated sessions on a 60-second tick with validation and delivery control, destructive work is covered by shadow-git checkpoints with rollback, and a hardline command blocklist holds even in YOLO/headless modes. See [[wiki/06-automation-security-architecture|Automation, Security, and Architecture]].

### Q10. What is the weakest link in the docs' case for Hermes, and what evidence would change your mind?

> [!tip]- Answer
> Operator-scale evidence is missing: no cost/latency numbers for always-on gateway + reviews, no quality data on agent-authored skills across model sizes, thin multi-user boundaries — a measured month-long deployment report would settle it. See [[critical_thinking|Critical Analysis]].
