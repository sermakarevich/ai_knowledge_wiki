> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# mateaix/mateclaw — In Plain Language

## What is this about?
MateClaw is a self-hosted "second brain": one deployment that bundles
an AI assistant's reasoning, knowledge, memory, tools, and chat channels
together, instead of scattering them across separate services.

In practice, you run it on your own server and get "digital employees" —
named assistants with a role, goal, and backstory (for example, a Research
Analyst or a Customer Support agent). Six ready-made templates ship with
the product, so you can start without designing an agent from scratch.

It is built for teams, not just one person: multiple users share
workspaces, sensitive actions need approval, and everything is logged for
audit. The pitch is simple: "$0 · No tokens metered. No seats billed.
Your server. Your data. Your keys."

You can reach the same assistant through many doors: a web admin console,
a desktop app, an embeddable website chat widget, IM channels (DingTalk,
Feishu, WeChat, Telegram, Discord, QQ, Slack), and a plugin SDK for
developers.

## Why does it matter?
Most AI assistants break when something goes wrong: an API key expires,
a vendor has an outage, quota runs out, or the server restarts mid-task
and hours of work are lost.

MateClaw's answer has three parts. First, it keeps a list of backup AI
providers (DashScope, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Ollama,
and others) and automatically retries with the next healthy one when the
primary fails. A health tracker parks sick providers in a cooldown window
so the system stops hammering them.

Second, long work is made recoverable. "Persistent Goals" save the
checklist, progress, attempts, and intermediate files to the database, so
after a restart the system picks up where it left off instead of starting
over. "Team Runs" do the same for multi-step jobs split across workers,
linking the objective, task graph, worker runs, and deliverables under
one stable ID.

Third, knowledge stays trustworthy. The built-in "LLM Wiki" turns messy
raw material (PDFs, markdown files, scraped pages) into structured,
interlinked pages with traceable citations, and the most relevant pages
are automatically fed into the assistant's instructions.

## How does it work?
Think of it in five steps:

1. **Pick an employee, pick an engine.** Each digital employee's identity
   (role, goal, backstory) is kept separate from the engine that runs it.
   You can use the built-in ("native") engine or an external managed loop
   called DSH, which runs as an authenticated side process and streams
   thinking, answers, tool calls, and usage back as standard events.

2. **Survive provider failures.** Providers are ordered in
   Settings → Models. When one fails (bad key, 401, network blip, empty
   quota), the request moves to the next healthy provider. You only see
   an error when the whole chain is exhausted.

3. **Work in recoverable chunks.** Big jobs become Goals with checklists
   and checkpoints. Workers append small verifiable units of progress and
   keep a progress ledger; a supervisor reconciles interrupted attempts
   after restarts. One caveat: exactly-once is not promised for outside
   side effects (payments, sends, publishes), which need extra care.

4. **Coordinate teams on a shared board.** One request creates one Team
   Run: chat shows the outcome, a live view shows workers in real time,
   and a Teams view keeps history. Underneath, a shared board handles
   task dependencies, parallel dispatch, execution leases, cancellation,
   and human approval gates.

5. **Grow knowledge and skills safely.** The Wiki digests documents into
   linked pages; workspace memory files (`AGENTS.md`, `MEMORY.md`, daily
   notes) plus scheduled consolidation remember context. New abilities
   arrive as SKILL.md packages, MCP tool connections, or bridged coding
   tools (Claude Code, Codex) — all fenced by a Tool Guard with roles,
   approvals, and path protection. Routine business flows can be scripted
   as linear workflows and fired by triggers (schedules, webhooks,
   channel messages).

Deployment itself is deliberately boring: a lean Docker setup over
PostgreSQL 16, a copy-and-rename `.env.example` template where missing
required values stop startup instead of silently using defaults, and an
Admin Runtime Console with health monitoring and one-click restart.

## Where can this be used?
- **Team assistant hubs:** one self-hosted deployment serving many users
  across web, desktop, and chat apps, with approvals and audit trails.
- **Long research or data jobs:** multi-hour analyses that must survive
  restarts, keep evidence, and cite sources from the Wiki.
- **Customer support and operations:** agents on the website widget or IM
  channels, with human approval gates before sensitive actions.
- **Recurring business routines:** scheduled or event-triggered workflows
  (e.g. digest incoming messages, draft reports, update memory) that are
  replayable and rate-limited against loops.
- **Developer and analyst teams:** code review, data analysis, and custom
  tool packs added via skills, MCP servers, or the plugin SDK.
- **Regulated or privacy-sensitive settings:** organizations that need
  data on their own servers, per-channel error isolation, and full logs
  rather than a third-party SaaS black box.

## Conclusions & takeaways
MateClaw is less "a chatbot" and more "an office in a box": employees,
memory, knowledge base, tools, channels, and team coordination in one
self-hosted package.

Its most distinctive ideas are the separation of employee identity from
the execution engine, automatic failover across AI vendors with health
cooldowns, and durability by default — Goals and Team Runs that persist
progress so long work survives failures.

The trade-off is operational: you gain control of data, cost, and audit,
but you run the infrastructure (database, models, sidecars) yourself.
And durability covers internal progress, not the outside world — actions
that spend money or publish content still need idempotency or human
review.

If you want a team-grade, self-hosted agent platform with linked
knowledge and approval-gated teamwork, this is what MateClaw is trying
to be.

## Jargon decoder
| Term | Plain definition |
|---|---|
| Agent runtime | The engine that actually runs an assistant's think-act-observe loop. |
| Native vs. DSH engine | Built-in engine versus an external helper process plugged in over a standard connection. |
| Provider failover | Automatically retrying with a backup AI vendor when the first one fails. |
| Health tracker / cooldown | A scoreboard that benches a failing AI vendor for a while before trying it again. |
| Persistent Goal | A long task saved step-by-step so it can resume after crashes or restarts. |
| Team Run (`runId`) | One multi-worker job tracked under a single ID from goal to deliverables. |
| Task DAG / shared board | The dependency map and task list that coordinates which worker does what, and when. |
| LLM Wiki | A knowledge base that converts raw documents into linked, citable pages for the AI to use. |
| SKILL.md package | A plug-in bundle of instructions and tools that teaches an agent a new ability. |
| MCP / ACP | Standard ways to connect outside tools or coding assistants into the agent. |
| Tool Guard | The permission system: who may use which tool, what needs approval, which files are off-limits. |
| Workflow / trigger | A reusable script of steps, plus the schedule or event that launches it automatically. |
