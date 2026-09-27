> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Tech — LLM, RAG, Autonomous Agents

**In one sentence:** Workers are built on latest-generation language models plus RAG (Retrieval-Augmented Generation — the AI looks up your documents before answering) knowledge access and isolated per-tenant persistent memory, orchestrated through multi-agent workflows on open standards with logged, permissioned, human-approvable actions.

## Key points

- Workers run on the most advanced language models on the market, including the GPT, Claude, and Gemini families.
- New models are continuously evaluated on internal benchmarks covering reasoning quality, tool-calling accuracy, and safety.
- Workers automatically switch to the best available model for each type of task.
- The RAG architecture lets each worker access documents, knowledge bases, and business data (Notion, Google Drive, Confluence, Slack) at the moment of acting, reducing hallucinations.
- Persistent memory keeps interaction history, preferences, templates, and processes, and is isolated per tenant so data is never shared across organizations.
- Workers chain together in multi-agent workflows (for example marketing briefs design, then SEO optimizes), coordinated through open standards like MCP (Model Context Protocol — a standard for communication between AI agents and external tools).
- Each worker runs in an isolated environment with granular permissions; tool calls are logged for full audit, access is limited to explicitly granted resources, and sensitive actions can require human approval.
- The page sits in shared site navigation: 15 AI Workers, pricing, integrations (Slack, Teams, 3000+ tools), use cases, security and GDPR, build-a-team, clone-yourself, personality, blog, companion extension, and the five solution agents.

---

## Language models

Model choice is dynamic and benchmark-driven rather than fixed to one provider.

| Fact | Value from source |
|---|---|
| Model families | GPT, Claude, Gemini — most advanced on the market |
| Evaluation | Continuous, on internal benchmarks: reasoning quality, tool-calling accuracy, safety |
| Routing | Workers automatically switch to the best model per task type |

> "Our workers run on the most advanced language models on the market, including the GPT, Claude and Gemini families."

**Covers:** https://delos.so/tech

## RAG knowledge access

RAG grounds workers in the customer's own sources instead of training memory alone.

| Fact | Value from source |
|---|---|
| Sources | Documents, knowledge bases, business data: Notion, Google Drive, Confluence, Slack |
| Timing | Retrieved at the moment of acting |
| Effect | Drastically reduces hallucinations; keeps responses grounded in your reality |

> "Instead of relying only on what it learned during training, the worker retrieves relevant context from your own sources (Notion, Google Drive, Confluence, Slack…), which drastically reduces hallucinations and keeps responses grounded in your reality."

**Covers:** https://delos.so/tech

## Persistent memory

Memory makes workers learn processes and remember them across sessions.

| Fact | Value from source |
|---|---|
| Stored | Interaction history, preferences, templates, processes (e.g. brand voice learned last week is remembered today) |
| Isolation | Isolated per tenant; data never shared across organizations |

> "A worker that learned your brand voice last week still remembers it today. This memory is isolated per tenant: your data is never shared across organizations."

**Covers:** https://delos.so/tech

## Orchestration and security

Multi-agent coordination and locked-down execution are described as a pair.

| Fact | Value from source |
|---|---|
| Orchestration | Workers chain in multi-agent workflows; e.g. marketing briefs design, which produces visuals, then SEO optimizes |
| Standard | MCP (Model Context Protocol), standardizing agent-to-tool communication |
| Sandboxing | Each worker runs in an isolated environment with granular permissions |
| Oversight | Tool calls logged for full audit; access only to explicitly granted resources; sensitive actions can require human approval |

> "This coordination relies on open standards like the Model Context Protocol (MCP), which standardizes communication between AI agents and external tools."

**Covers:** https://delos.so/tech
