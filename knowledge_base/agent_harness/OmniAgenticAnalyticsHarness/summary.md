# Building the Best Agentic Analytics Harness: Powered by Claude, Built with Claude Code

**Video:** [Building the best agentic analytics harness: Powered by Claude, built with Claude Code (Chris Merrick, Omni Analytics, 2026)](https://www.youtube.com/watch?v=K4-flzsPraE)
**Source:** Claude YouTube channel (Anthropic "Code with Claude" series)
**Published:** May 21, 2026

---

## Human Readable TL;DR

Imagine you have a super-smart data analyst who not only answers your questions but also knows which filing cabinet to look in, can fetch the exact right folder, and then writes up a full report -- without you telling it every step. That's what Omni built. They created an AI system called "Blobby" that can handle complex business questions by breaking them into steps, running the right database queries in sequence, and summarizing the results -- all while enforcing the same data security rules as a human analyst. And they built nearly all of it using Claude Code as their coding assistant.

## TL;DR

Omni's co-founder & CTO Chris Merrick presents the architecture behind their production agentic analytics system -- a multi-agent harness built entirely on Claude that moves beyond single-query text-to-SQL into true multi-step reasoning over enterprise data. The system features a coordinator agent that selects specialized tools (topic picker, field values lookup, summarization sub-agent) in sequence, grounds all AI actions in Omni's semantic layer for governance and accuracy, and handles the engineering challenges of conversation memory and security at scale. 99% of the platform's code was written using Claude Code.

---

## Problem & Motivation

Text-to-SQL AI rarely survives contact with production. Demos look impressive but enterprise data is messy: questions span multiple datasets, field values need exact matches, context windows overflow on large result sets, and access controls must be enforced per-user. Omni's customers were asking broad, open-ended questions through their MCP server in tools like Cursor and Claude -- the same way people talk to general LLMs. A single-query AI couldn't handle that. They needed an agent that could think, plan, and act across multiple steps while remaining as reliable and governed as the rest of their platform.

---

## Main Original Ideas

1. **Coordinator-first architecture.** Rather than a single monolithic agent, Omni's system uses a coordinator LLM that observes the question, the accumulated results, and prior tool calls to decide what to do next -- continue, retry, switch tools, or stop. This enables adaptive multi-step analysis instead of a fixed pipeline.

2. **Semantic layer as intelligence backbone.** Omni's pre-existing semantic layer (business metrics definitions, field relationships, governance rules, access permissions) is surfaced to the agent as structured context. This grounds the AI's actions in institutional knowledge -- the agent knows what "active customer" means to the business -- rather than relying on the LLM's training data.

3. **Specialized, right-sized tools.** Instead of one large all-capable tool, the agent has a small set of purpose-built tools:
   - **Topic Picker:** Scans metadata across curated datasets (Topics) to select the right data source before generating SQL -- prevents the agent from querying the wrong table.
   - **Field Values Tool:** Fetches valid field values from the database to ensure exact matches, fixing the classic AI hallucination of inventing field names or values.
   - **Summarization Sub-agent:** A separate agent with its own context window processes large query result sets independently, preventing the main context window from overflowing while distilling findings into the running summary.

4. **Prompt-cache-efficient conversation memory.** Full conversation history (including prior queries and results) is reconstructed each turn. Apache Arrow result sets are serialized to CSV before storage so they can be re-injected as text without breaking prompt caching, keeping latency and cost under control as conversations grow.

5. **99% Claude Code development.** The entire platform -- including the agentic system itself -- was built with Claude Code as the primary coding tool, demonstrating that AI coding assistants are production-viable for complex systems engineering.

---

## Key Findings

| Area | Approach |
|------|----------|
| Multi-step reasoning | Coordinator agent breaks questions into sub-tasks, runs queries iteratively |
| Dataset selection | Topic Picker examines metadata before SQL generation |
| Field accuracy | Field Values Tool fetches live valid values from the database |
| Context management | Summarization sub-agent has its own context window; Arrow → CSV serialization |
| Governance | All queries execute under user-specific permissions from the semantic layer |
| Development velocity | 99% of codebase written with Claude Code |
| Business scale | Omni raised $120M Series C at $1.5B valuation (April 2026) |

- Multi-dataset analytical questions are handled by breaking them into parts, querying each dataset, then synthesizing
- The coordinator can retry, change tools, or stop early when useful insights emerge -- not a rigid pipeline
- Integration with external tools (Claude Desktop, Cursor, VS Code, ChatGPT) via MCP server with the same governed context

---

## Suggestions & Future Directions

1. **Expand tool surface.** As more analytical patterns are identified, additional specialized tools can be added to the coordinator's toolset without restructuring the core architecture.
2. **Evaluation rigor.** The talk explicitly covers evaluating agent effectiveness -- building reliable evals for multi-step agentic systems remains an open engineering challenge in the space.
3. **Broader MCP ecosystem.** Omni's governed semantic context is already available via MCP; exposing richer agent skills (not just query execution) is a natural next step.
4. **Agent skills for internal workflows.** Omni uses their own agentic system for customer support tooling, demonstrating dogfooding as a validation strategy.

---

## Authors & Institutions

**Chris Merrick** (Co-founder & CTO, Omni Analytics) -- presented at Anthropic's "Code with Claude" event, May 2026. Omni was co-founded by ex-Looker executives Colin Zima, Jamie Davidson, and Chris Merrick.
