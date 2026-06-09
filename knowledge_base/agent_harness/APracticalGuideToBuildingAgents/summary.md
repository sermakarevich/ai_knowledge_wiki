# A Practical Guide to Building Agents

**Guide:** [A Practical Guide to Building Agents (OpenAI, 2025)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

## Human Readable TL;DR

Think of a traditional app like a vending machine -- you press a button, you get one specific thing. An AI agent is more like a personal assistant: you give it a goal, and it figures out the steps, uses whatever tools it needs (calendar, email, search), and keeps going until the job is done. This guide from OpenAI explains when to hire that assistant vs. just pressing a button, how to give it the right tools and instructions, how to keep it from going off the rails, and when to build a team of assistants instead of just one.

## TL;DR

OpenAI's 34-page practical guide (April 2025) defines agents as LLM-powered systems that autonomously manage multi-step workflows via tool use and decision-making. It covers the three core building blocks (model, tools, instructions), two orchestration patterns (single-agent loops and multi-agent manager/decentralized graphs), and a layered guardrails framework. The key recommendation is to start with a single capable agent and evolve complexity only when that agent demonstrably fails.

---

## Problem & Motivation

Traditional rule-based automation breaks down on workflows requiring nuanced judgment, handling unstructured data, or managing frequently-changing rule sets. The guide addresses the gap between simple LLM chatbots (no workflow control) and agents that autonomously execute end-to-end workflows -- and gives teams a concrete path to build them safely.

---

## Main Original Ideas

1. **Agent definition as two invariants** -- An agent must (a) use an LLM to manage workflow execution and self-correct on failure, and (b) dynamically select tools within defined guardrails. Chatbots and single-turn classifiers explicitly do not qualify.

2. **Three-signal "build vs. don't build" test** -- Agents are appropriate when the workflow has complex decision-making (nuanced judgment), difficult-to-maintain rules (brittle rulesets), or heavy reliance on unstructured data. If none apply, deterministic automation suffices.

3. **Model selection via performance-then-optimization** -- Build first with the most capable model to get a baseline, then swap in smaller/cheaper models per task to find acceptable tradeoffs. Don't prematurely cap capability.

4. **Tool taxonomy: Data / Action / Orchestration** -- Tools are categorized by purpose: Data (read context), Action (write/send/update), Orchestration (call sub-agents). Each tool needs a standardized definition reusable across many agents.

5. **Prompt templates over per-case prompts** -- Use a single flexible base prompt with policy variables instead of many individual prompts. This dramatically simplifies maintenance as use cases multiply.

6. **Single-agent-first orchestration principle** -- Always maximize one agent's capabilities before introducing multiple agents. Multi-agent adds complexity and overhead; split only when prompts have too many conditionals or tools overlap confusingly.

7. **Manager vs. Decentralized multi-agent patterns** -- Manager: one orchestrating LLM calls specialized agents as tools, retaining context. Decentralized: agents hand off execution to peers via one-way transfers, no central controller. Edges in the graph are tool-calls (manager) vs. handoffs (decentralized).

8. **Optimistic execution for guardrails** -- The primary agent generates output concurrently while guardrails run in parallel. Guardrails raise exceptions only on violations rather than blocking the main flow -- better latency while maintaining safety.

9. **Human intervention as a designed component** -- Two explicit triggers: exceeding retry/failure thresholds, or reaching high-risk/irreversible actions. Human-in-the-loop is treated as a first-class architectural element, not an afterthought.

---

## Key Findings

### When to Build an Agent

| Signal | Example |
|--------|---------|
| Complex decision-making | Refund approval in customer service |
| Difficult-to-maintain rules | Vendor security reviews |
| Heavy unstructured data | Processing home insurance claims |

### Orchestration Patterns

| Pattern | Structure | Best For |
|---------|-----------|----------|
| Single agent | Loop with tools until exit condition | Most workflows; start here |
| Manager | Central LLM calls sub-agents as tools | Need central control + synthesis |
| Decentralized | Peer agents hand off to each other | Triage workflows, no central synthesis needed |

### Guardrail Types

| Type | Mechanism |
|------|-----------|
| Relevance classifier | Flags off-topic queries |
| Safety classifier | Detects jailbreaks / prompt injection |
| PII filter | Vets model output for personal data |
| Moderation | Flags harmful content (hate, harassment) |
| Tool safeguards | Risk-rate tools (low/medium/high); gate high-risk calls |
| Rules-based | Blocklists, regex, input length limits |
| Output validation | Brand-alignment content checks |

### Tool Splitting Heuristics

- Too many **conditional branches** in prompts → split agents by logic segment
- **Tool overlap** (not just count) causes failures -- even <10 overlapping tools can break; >15 distinct tools can work fine

---

## Suggestions & Future Directions

1. **Start small, validate, then scale** -- Deploy a single-agent MVP with real users before building multi-agent systems. Treat agent evolution as iterative, not big-bang.

2. **Establish evals before optimizing** -- Build benchmarks against the best model first; use them to safely downgrade to cheaper models per task.

3. **Layer guardrails incrementally** -- Begin with data privacy and content safety; add new guardrails as real-world edge cases surface rather than trying to anticipate all risks upfront.

4. **Use computer-use models for legacy systems** -- For systems without APIs, agents can use UI-based computer-use models as a fallback to interact with applications as a human would.

5. **Declarative vs. code-first orchestration** -- The guide implicitly advocates for code-first (Agents SDK style) over declarative graph frameworks (LangGraph-style), arguing declarative approaches become brittle as workflows grow dynamic.

---

## Authors & Institutions

OpenAI (no individual authors listed -- organizational publication, April 2025)
