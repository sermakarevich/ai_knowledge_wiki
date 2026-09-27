# Source

- **Hub:** [Orkes Documentation — Agentic Workflow Engine](https://www.orkes.io/content/) (canonical URL; tracking params `_gl`, `gclid`, `gbraid` stripped — they are ad-click noise)
- **What it is:** the full Orkes Conductor documentation site (Conductor = open-source workflow orchestration engine originated at Netflix; Orkes = commercial cloud/enterprise distribution positioning it as an "Agentic Workflow Engine")
- **Retrieved:** 2026-09-08
- **Scope analyzed:** hub navigation + Getting Started, Workflows, Agents, AI Cookbook, Design Patterns cookbook, SDK, Integrations, Reference (operators / system tasks / API), Platform concepts

Key pages consulted (canonical URLs, all under `https://orkes.io/content`):

- `/` — docs home / navigation map
- `/quickstart`, `/quickstart/first-worker`, `/quickstart/workflows`, `/quickstart/tasks`, `/quickstart/workers`
- `/devguide/workflows`, `/documentation/configuration/workflowdef`, `/developer-guides/write-workflows-using-code`
- `/devguide/ai`, `/devguide/concepts/agents`, `/devguide/ai/conductor-agents`, `/devguide/ai/agent-framework-recipes`, `/devguide/ai/multi-agent-architecture`
- `/ai-cookbook/durable-agents`, `/ai-cookbook/why-conductor`, `/ai-cookbook/production-agent-architecture`, `/ai-cookbook/failure-semantics`, `/ai-cookbook/human-in-the-loop`
- `/devguide/cookbook`, `/cookbook/microservice-orchestration`, `/cookbook/dynamic-parallelism`, `/cookbook/wait-and-timers`, `/cookbook/task-timeouts-and-retries`, `/devguide/cookbook/saga-compensation`, `/cookbook/event-driven`, `/cookbook/dynamic-workflows`
- `/devguide/integrations`, `/devguide/how-tos/event-bus`, `/developer-guides/event-handler`, `/developer-guides/mcp-gateway`, `/developer-guides/api-gateway`
- `/category/reference-docs/operators`, `/category/reference-docs/system-tasks`, `/category/reference-docs/ai-tasks`
- `/agentic-workflow-engine`, `/devguide/concepts`
- SDK index: `/sdks/sdk-index` (Java, Python, Go, JavaScript, C#, Ruby, Rust)

Note: the live docs site was read via web fetch rather than mirrored — mirroring the whole site into `source/` would bloat the auto-synced KB git repo. The wiki pages in `wiki/` are the durable capture.
