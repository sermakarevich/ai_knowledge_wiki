# Build-Time vs. Run-Time: Why Dev Tools Fail in Production

**Video:** [Build-Time vs. Run-Time: Why Dev Tools Fail in Production](https://www.youtube.com/watch?v=9R--1tg45Jg&list=PLcfpQ4tk2k0X1DNKK3SyZ2Qbl3QxBfHr3) — AI Engineer (Averi Kitsch & Prerna Kakkar, Google), ~20 min

## Human Readable TL;DR

Two Google engineers explain a mistake teams make when they let an AI helper (agent) touch a database: they build a tool for a developer who is watching every step, then later plug that same tool into a customer-facing chatbot where nobody is watching — and the agent can be tricked into doing something destructive, like deleting a table. Their fix is to slowly take away the agent's freedom: hide the database connection details from it, stop letting it write its own raw database queries (SQL), and eventually stop letting it even know which user it's talking to. What's left is a small, safe, single-purpose action (like "cancel this order") that the agent cannot misuse no matter how cleverly someone tries to fool it. They also give plain rules for building any AI tool well: keep it focused, describe it clearly, separate "just looking" from "actually changing something," and give useful error messages.

## TL;DR

The talk (given at Google, covering MCP Toolbox for Databases — an open-source database connector server for AI agents) distinguishes build-time tools (developer-assistant, human-supervised, flexible — e.g., NL2SQL/"execute SQL" or admin tools) from runtime tools (end-user-facing, unsupervised, must be deterministic and narrow — e.g., a "cancel order" tool). A live failure demo showed an unsupervised build-time tool letting an agent delete a table. The security section frames the core risk as the "confused deputy" attack and Simon Willison's "lethal trifecta" (private data + untrusted content + an exfiltration path), and walks through hardening a tool step by step using MCP Toolbox's "source" primitive: hide connection details, add read-only/allowed-dataset/output-size limits, fix the SQL with typed prepared statements, move to semantic parameters, then strip user identity out via bound or authenticated parameters to reach a "zero trust" tool. It closes with tool-design best practices: outcome-focused tools, non-redundant descriptions, read/write separation, actionable errors, and simple flat inputs.

---

## Problem & Motivation

Teams building AI database tools often reuse the same tool in two very different situations: while a developer is actively watching and approving each step (build-time), and inside an unsupervised, end-user-facing application (runtime). A tool designed for the first case is usually too flexible and too powerful for the second — it can be talked into destructive or unauthorized actions because nothing outside the AI model's own judgment is stopping it. The talk addresses this gap directly: how to recognize which kind of tool you're building, and how to harden a tool so it stays safe even when a user tries to trick the agent behind it.

---

## Main Original Ideas

1. **Build-time vs. runtime tools** — Build-time tools (control-plane/admin tools and NL2SQL "execute SQL" tools) are made for a human-supervised developer-assistant setting: they are atomic and flexible, which is exactly why they're dangerous to leave unattended. Runtime tools are made for unsupervised, end-user-facing applications and must instead be deterministic, structured, and narrow (e.g., a "cancel order" tool with fixed logic).
2. **MCP Toolbox "source" primitive** — Google's MCP (Model Context Protocol) Toolbox for Databases secures a tool progressively: it first moves database connection details (host, port, credentials) into a preconfigured YAML file outside the agent's reach, then layers on read-only restrictions, allowed-dataset limits, and output-size caps.
3. **Confused deputy attack / lethal trifecta** — A confused deputy attack is when a user tricks a trusted agent into misusing its own privileges. Simon Willison's "lethal trifecta" names the three conditions that together cause a breach: an agent with simultaneous access to private data, untrusted content, and a way to leak that data back out.
4. **Bound vs. authenticated parameters** — To remove personally identifiable information (PII) like user identity from the agent's control, Toolbox supports bound parameters (the application authenticates the user and binds their identity directly to the tool call, never showing it to the agent) and authenticated parameters (the tool itself validates a signed identity token, such as an OpenID or JWT — JSON Web Token — and extracts the user's identity itself).
5. **Zero-trust tool design** — By repeatedly stripping capability away from the agent (connection details, raw SQL, then user identity), a tool ends up accepting only a simple, non-sensitive input (like a date), so the system — not the agent's judgment — stays in control of everything sensitive.

---

## Key Findings

- MCP Toolbox for Databases: ~15.7K GitHub stars, 132+ active contributors, support for 40+ databases.
- The self-managed toolbox plus Google-managed MCP handled 20 million tool calls last month.
- Failure demo: an unattended build-time tool let an agent be talked into deleting a database table with "no safeguard or guardrails."
- Planned (but not shown live due to a video load failure) runtime demo: a travel chatbot called "Similar" was designed to refuse booking a flight under another user's identity because its tools used authenticated identity binding.
- Salary-database example of the lethal trifecta: a malicious insider hid a request inside a support ticket; the trusted triage agent, holding database credentials, queried the salary database and posted all employee salaries back on the ticket — a full breach.
- The MCP Toolbox hardening sequence has roughly 7 stages, from a fully model-controlled tool (agent has raw DB credentials and writes SQL) down to a zero-trust tool with a single harmless parameter.

---

## Suggestions & Future Directions

1. Design tools around outcomes the user wants, not as a pile of atomic REST API (raw web service call) operations — this cuts the number of round trips the agent needs to make.
2. Write clear, non-redundant tool descriptions that guide the agent, without repeating information already visible in the input schema.
3. Separate read tools (auto-approvable) from write tools (should require human confirmation).
4. Return actionable error messages instead of generic HTTP status codes, so the agent can reason about and correct a failed call.
5. Keep tool inputs simple and flat rather than complex nested structures, since agents are less reliable at constructing complicated inputs correctly.
6. Use Eval Bench (Google's evaluation framework for agents, MCP tools, and skills) to validate that tools are actually working well.
7. Consult the MCP Toolbox for Databases documentation and GitHub repository for concrete implementation guidance.

---

## Authors & Institutions

Averi Kitsch (Staff Software Engineer, Google Cloud Databases; tech lead, MCP Toolbox for Databases), Prerna Kakkar (Senior Software Engineer, Google; tech lead, Eval Bench)
