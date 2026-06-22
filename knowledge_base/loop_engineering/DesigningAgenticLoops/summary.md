# Designing Agentic Loops

**Article:** [Designing Agentic Loops (Simon Willison, 2025)](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/)

## Human Readable TL;DR

Imagine having an assistant who can not only follow your instructions but also try things out, see if they work, and keep adjusting until the job is done -- like a handyman who keeps testing different screws until the shelf is sturdy. This article explains how to set up AI tools to work that way safely: give them a small, isolated workspace, limit how much money they can spend, point them at problems that have a clear "right answer" (like passing tests), and let them iterate. The main lesson is that AI agents shine when they can try, fail, and retry -- but only if you've built guardrails so a mistake doesn't take down your whole system.

## TL;DR

Simon Willison defines agentic loops as LLM systems that run tools in a loop to achieve a goal, exemplified by coding agents like Claude Code. The piece outlines practical safety mitigations for "YOLO mode" (auto-approving all agent commands), recommends `AGENTS.md` files over MCP for exposing CLI tools, and argues that tightly scoped credentials (test environments, small spending caps) are the critical enabler. Agentic loops yield the most value on iterative, measurable tasks -- debugging, performance tuning, dependency upgrades -- especially when automated test suites provide clear success signals.

---

## Problem & Motivation

LLM-based agents capable of executing shell commands and code have matured rapidly (Claude Code launched February 2025), but best practices for designing and running them safely remain underdeveloped. Developers face a real tension: maximum productivity requires trusting the agent to act autonomously ("YOLO mode"), but unrestricted autonomy creates meaningful risks -- data exfiltration, corrupted files, or the host machine being used as an attack proxy. The article attempts to distill early practitioner wisdom into actionable patterns.

---

## Main Original Ideas

1. **YOLO Mode as a calculated risk** -- Automatically approving all agent tool calls is both dangerous and practically necessary for productivity. The mitigations are environmental (sandboxes, containers, remote compute) rather than behavioral -- you constrain the blast radius rather than trying to review every command.

2. **`AGENTS.md` over MCP** -- Rather than setting up Model Context Protocol servers, Willison recommends a simple markdown file listing available CLI tools and how to use them. Quality LLMs already know tools like Playwright and FFmpeg; documenting them in `AGENTS.md` is sufficient, and the agent learns the rest through trial-and-error.

3. **Tightly scoped credentials as a first-class design concern** -- Agents should receive credentials restricted to test/staging environments and with hard spending caps. The concrete example: isolated Fly.io organizations with $5 budgets for performance investigation work. Spending-capable credentials (cloud APIs, LLM calls) are the highest-risk surface.

4. **Clear success criteria as the selection criterion** -- Not all tasks suit agentic loops. The best candidates have an objective "done" signal: tests pass, a benchmark improves by X%, a Docker image shrinks. Tasks without measurable success criteria are poor fits because the agent cannot self-evaluate progress.

5. **Automated test suites as force multipliers** -- Comprehensive test coverage dramatically amplifies agent effectiveness on debugging and refactoring tasks. The agent can run tests, read the output, and iterate without human checkpoints.

---

## Key Findings

- **High-value agentic task types:** debugging failing tests, SQL/query performance optimization, container image size reduction, dependency upgrades, Docker configuration tuning.
- **Three principal risk categories in YOLO mode:** (1) shell commands corrupting important files, (2) data exfiltration via stolen source code or environment secrets, (3) using the host machine as a proxy for external attacks.
- **Recommended sandboxing options:** Docker containers without internet access (Anthropic's own recommendation paired with `--dangerously-skip-permissions`), GitHub Codespaces, ChatGPT's Code Interpreter.
- **Field maturity:** as of the article's writing (September 2025), agentic loop design is a nascent discipline -- Claude Code itself only launched in February 2025, roughly seven months prior.

---

## Suggestions & Future Directions

1. Continue developing community best practices -- the author explicitly frames this as an open, evolving space.
2. Explore further use cases that fit the "clear success criteria + trial-and-error" profile beyond the examples given.
3. Standardize `AGENTS.md` conventions across projects to reduce per-project setup friction.
4. Invest in better sandboxing tooling to lower the barrier to running agents safely without full Docker setups.

---

## Authors & Institutions

Simon Willison -- independent developer, co-creator of Django, author of simonwillison.net.
