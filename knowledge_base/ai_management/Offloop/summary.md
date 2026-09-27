# Offloop

**Source:** [Offloop -- Scale your team's work without scaling headcount](https://offloop.org/?from=x)

## Human Readable TL;DR

Offloop sells a shared "workplace" where AI agents do recurring office chores -- following up with customers, writing launch posts, watching competitors, summarizing feedback -- instead of a human doing them in a chat window. Think of it like hiring a small ops team, except the workers are AI agents that live in channels with memory, permissions, and an audit trail, so a 3-person startup can run like a 10-person one without adding headcount.

## TL;DR

Offloop is a B2B SaaS product (private beta) that packages agentic workflows -- goal + context + tools + approvals -- into persistent "channels" rather than one-off chat sessions. It targets small teams that need continuous operational work (customer follow-up, launches, growth, research, feedback loops) done by agents connected to tools like GitHub, Notion, Sentry, Supabase, and Vercel, with visible progress and audit trails instead of hidden chat logs. Three tiers: Operator (individual, private beta, macOS app), Team Pilot (shared team channels), Enterprise (SSO, custom connectors).

---

## Problem & Motivation

Small teams lack the headcount to keep operational loops running -- follow-ups, research, feedback triage, launch coordination -- even though the individual tasks are well within an LLM's capability. Generic chat-based AI assistants don't solve this because the work is recurring and stateful (it needs memory, handoffs, and follow-through across days/weeks), not a single prompt-response. Offloop's framing: teams need "help keeping work moving," not just help answering a prompt.

---

## Main Original Ideas

1. **Agents as workplace occupants, not chatbots** -- agents are given goals, context, files, tasks, approvals, and signals, and are expected to produce artifacts, follow up, and hand off work, mirroring how a human employee operates rather than how a chat assistant responds once.
2. **Channels as the unit of work** -- instead of ephemeral chat threads, work happens in persistent channels with team memory, roles, and audit trails, making agent activity visible and reviewable rather than buried in DMs.
3. **Connector-based tool grounding** -- agents act through integrations (GitHub, Notion, Sentry, Supabase, Vercel, etc.) scoped by workspace membership and connector grants, rather than freeform API access.
4. **Model-agnostic routing with disclosure** -- the platform routes requests to configured LLMs and exposes routing decisions rather than abstracting/hiding which model handled a task.

---

## Key Findings

No quantitative benchmarks, user counts, or performance metrics are published on the site -- this is a product marketing page, not a research artifact. Qualitative claims only:
- Positions itself against "another chat box" as the wrong interface for recurring operational work.
- Claims governance features (permissions, data scoping, credential management, audit-friendly runtime) are built in rather than bolted on.

---

## Suggestions & Future Directions

1. Product is in **private beta** (Operator tier) -- roadmap implies broader team/enterprise rollout (Team Pilot is "custom," Enterprise is "contact sales").
2. Open questions the FAQ addresses but doesn't fully resolve: exact data retention scope, and how prompts are "prepared at runtime" before being sent to underlying LLM providers.

---

## Pricing / Tiers

| Tier | Status | Target | Key Features |
|------|--------|--------|--------------|
| **Operator** | Private beta | Individuals | Channel workspace, macOS app, files, schedules, visible progress |
| **Team Pilot** | Custom | Small teams | Shared channels, team memory, connector setup, onboarding |
| **Enterprise** | Contact sales | Organizations | Custom connectors, SSO, audit-friendly runtime, support |

## Authors & Institutions

No individual authors credited. Content attributed to "Offloop Team" / "Loopie Research" (in-house blog byline).
