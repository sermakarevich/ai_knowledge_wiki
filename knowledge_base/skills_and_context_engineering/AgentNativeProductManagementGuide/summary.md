# A Guide to Agent-native Product Management

**Article:** [A Guide to Agent-native Product Management (Marcus Moretti, Every, 2025)](https://every.to/guides/ai-product-management-guide)

## Human Readable TL;DR

Imagine a project manager whose paperwork, status reports, and meeting prep are all handled by an AI assistant -- leaving them free to do the actual interesting thinking. This guide shows exactly how to set that up: one AI skill that interviews you to build a clear product strategy document, and another that automatically pulls together a daily health report from your product's data. The tedious admin of product management becomes automated, and the PM gets to focus on decisions, creativity, and talking to users.

## TL;DR

Marcus Moretti's guide introduces an agent-native PM workflow built on two Claude Code skills (`ce:strategy` and `ce:product-pulse`) from Every's open-source compound-engineering plugin. The `strategy` skill conducts a guided interview to generate a structured strategy doc (problem → approach → personas → metrics → tracks). The `pulse` skill auto-generates a daily one-page report by querying analytics, tracing, payments, and database tools via MCP. Together they close the Plan → Ship → Review loop with minimal manual overhead.

---

## Problem & Motivation

Modern PMs manage 100+ software subscriptions and split attention across design, diplomacy, analytics, and execution. The administrative and data-gathering burden consumes time that should go to strategy and user insight. LLM agents can now handle that drudgery, but there's no standard playbook for wiring them into a PM's actual workflow.

---

## Main Original Ideas

1. **Agent-conducted strategy interview** -- Instead of writing a strategy doc from scratch, the `ce:strategy` skill interviews the PM conversationally, drilling into vague answers (based on Rumelt's "Good Strategy Bad Strategy" framework). Output is a `strategy.md` covering target problem, approach, personas, S.M.A.R.T. metrics, and work tracks.

2. **Product Pulse as living product memory** -- `/ce:product-pulse` generates a 30-40 line on-demand report by querying four tool categories (analytics, tracing, payments, DB) via MCP. Reports are saved as dated Markdown files in `~/pulse-reports/`, building longitudinal memory. Scheduled daily via Claude Code Routines.

3. **Strategy-grounded pulse analysis** -- The agent evaluates pulse data relative to the declared strategy metrics rather than hard-coded thresholds, using common-sense comparison to prior periods and preemptively answering likely follow-up questions.

4. **Ticket abolition** -- The guide recommends eliminating traditional detailed ticket-writing; agents write and manage issues. Status tracking shifts to now/next/later (Kanban) rather than sprint-based planning.

---

## Key Findings

| Component | Details |
|-----------|---------|
| Strategy doc sections | Target problem, approach, personas, 3-5 S.M.A.R.T. metrics, 2-4 tracks |
| Pulse report length | ~30-40 lines, single page |
| Pulse data sources | PostHog/Mixpanel/Amplitude, Datadog/Sentry/Logfire, Stripe/Paddle, DB read-only |
| Scheduling | Claude Code Routines, author runs daily at 8am |
| Plugin install | `github.com/EveryInc/compound-engineering-plugin` |

- The PM loop simplifies to: **Plan → Ship → Review → Repeat**, with AI handling the Review generation and much of the Plan documentation
- Strategy documents feed companion skills: `ce-ideate`, `ce-brainstorm`, `ce-plan` -- creating a coherent pipeline from strategy through specs to shipped code
- Data quality prerequisite: product must be instrumented and logging must be established before pulse tracking is useful

---

## Suggestions & Future Directions

1. Add cross-pulse metric comparison and aggregation (not yet implemented)
2. Per-stack customization guides for niche tools
3. Prioritization workflow integration (author uses a custom `/prioritize` command, not yet published)
4. Revisit strategy every few months as shipping data accumulates -- reinterviewing yourself is recommended

---

## Authors & Institutions

Marcus Moretti -- Every (every.to)
