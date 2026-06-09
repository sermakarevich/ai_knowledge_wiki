# Claude Code Routines: Building Proactive Agent Workflows

**Source:** [Claude Code Routines Workshop -- Code with Claude Conference](https://youtu.be/eSP7PLTXNy8)  
**Speaker:** Maya, Applied AI Team, Anthropic  
**Event:** Code with Claude (Day 1 Workshop Session)

---

## Human Readable TL;DR

Imagine instead of reminding a colleague every Monday to update the team docs, they just... do it automatically when code changes. That's what Claude Code Routines do -- they let Claude act like a proactive teammate that notices changes, runs on a schedule or reacts to events (like a GitHub issue), and takes action without anyone having to press a button. You don't need to set up servers or cron jobs; Anthropic handles all the plumbing.

---

## TL;DR

Claude Code Routines is a managed automation feature that transforms Claude Code from an interactive tool into a proactive coding agent. Users define a prompt, connected repositories, available connectors (Slack, GitHub, etc.), and a trigger (time-based schedule or event-based webhook/GitHub events). Anthropic handles hosting, session state, and infrastructure. Sessions remain interactive and steerable via web, CLI, or desktop -- bridging full automation with human-in-the-loop oversight.

---

## Problem & Motivation

Running Claude Code proactively today requires significant infrastructure work: deciding where agents run (not on a local laptop), managing hosting and data persistence, building cron jobs or endpoints to trigger sessions, and dealing with opaque headless sessions that offer no visibility or steerability. The result is high boilerplate cost for every proactive use case.

The internal motivating example: Anthropic's Claude Code engineering velocity grew 200% in PR volume YTD, overwhelming the single engineer responsible for keeping documentation in sync.

---

## Main Original Ideas

1. **Managed Proactive Agents (Routines)** -- A Claude Code session defined entirely by prompt + repos + connectors + trigger, with zero infrastructure managed by the user. Anthropic handles hosting, state persistence, and connector authentication.

2. **Dual Trigger Model** -- Routines support two trigger types:
   - *Time-based:* weekly, daily, or any cron-style schedule (e.g., every Monday at 10am)
   - *Event-based:* native GitHub events (PR opened, issue created, label applied) or arbitrary custom events via POST to a managed webhook endpoint, with the event payload passed as context into the session

3. **Interactive & Steerable Sessions** -- Every routine is a full Claude Code session under the hood, accessible in real time via web, CLI, and desktop. Users can observe the running session, ask follow-up questions mid-run, steer Claude toward a different direction, or resume past sessions -- identical to an interactive terminal session.

4. **Agent-on-Agent Review (Generator-Critiquer Pattern)** -- One routine generates output (e.g., opens a docs PR); a second routine triggers on that PR's creation to leave review comments before any human sees it. Reduces reliance on synchronous human review without sacrificing quality.

5. **Three-Decision Framework for Routine Design:**
   - *Trigger:* when and how should the agent be initiated?
   - *Context:* what repos, files, and connectors does Claude need to succeed?
   - *Steerability:* how will output quality be monitored and maintained?

---

## Key Findings

| Challenge Today | Routines Solution |
|---|---|
| Agent must run on user's machine | Managed cloud infrastructure, no laptop dependency |
| Manual cron/endpoint setup required | Native schedule + GitHub event triggers built in |
| Opaque headless sessions | Full session visibility and real-time steering via web/CLI |
| Connector auth management | Connectors (Slack, GitHub, Drive) configured once per routine |

**Real-world result:** Anthropic's documentation engineer used Routines to automate:
- Weekly diff of Claude Code source vs. docs repo → auto-PR for outdated docs
- Event-triggered routine on GitHub issue creation → auto-investigation + PR + Slack ping

**Entry point:** `/schedule` command inside Claude Code initiates routine creation via conversational setup.

---

## Suggestions & Future Directions

1. Expand event-based connectors beyond GitHub to other developer platforms (Jira, Linear, PagerDuty, etc.)
2. Apply Routines to common developer workflows: deploy verifiers that monitor Datadog/Grafana post-deploy and optionally auto-rollback; on-call investigators; backlog triage agents
3. Evolve the human-in-the-loop model: start with Claude providing go/no-go recommendations, progressively delegate full actions (e.g., auto-rollback) as trust is established
4. Use the `/schedule` command as the lowest-friction entry point -- one command away from creating a first routine

---

## Authors & Institutions

Maya (Anthropic, Applied AI Team) -- presented at Code with Claude conference, Day 1 workshop session
