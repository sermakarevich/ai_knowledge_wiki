# Towards Org-Level Agent Harnesses

**Source:** [X thread by Lance Martin (@RLanceMartin), Anthropic (2026)](https://x.com/RLanceMartin/status/2070571422913876182)

## Human Readable TL;DR

Imagine every employee at a company used to bring their own personal AI assistant, configured only for themselves. Now the company gives everyone access to one shared assistant that lives in the team chat (Slack), already knows the shared context, and can be looped into conversations by name. This post explains why that shift happened at Anthropic, what it unlocked (new employees ramp up faster, less duplicated work, the AI can join a live incident call), and how the assistant went from needing constant hand-holding to running long tasks on its own and proactively pinging people when something needs attention.

## TL;DR

Lance Martin describes three shifts behind Anthropic's internal "Claude Tag" (an org-level Claude agent harness surfaced in Slack): (1) single-player → multi-player, where identity, connectors, and skills move from the individual to the org, enabling shared-context benefits and inline multi-engineer collaboration (incident response, postmortems); (2) synchronous → asynchronous, enabled by rising model task-length (doubling ~every 4 months) and security improvements (prompt-injection resistance, auto-mode classifiers reviewing actions), paired with a "goal" primitive that lets Claude run, self-measure, and self-correct on open-ended instructions; (3) reactive → proactive, enabled by channel-based memory that lets Claude retain per-channel proactivity preferences (always respond, respond to a trigger, alert on a condition) so it can come to the user rather than wait to be asked.

---

## Problem & Motivation

Prior to Claude Tag, Claude Code usage at Anthropic was fragmented: each person ran their own harness with personal connectors, tying agent identity to the individual. This limited onboarding speed, caused duplicated work, and left the agent unable to participate in team-level workflows (shared incident channels, group discussions). Separately, early Slack-bot-style deployments of Claude required constant human steering (check-ins, nudges, approvals) because the model couldn't sustain long autonomous stretches of work, and lacked the security guarantees needed to trust it with delegated, unsupervised tasks.

---

## Main Original Ideas

1. **Org-level agent harness (Claude Tag)** -- gives Claude its own identity, connectors, and skills scoped to the organization (via Slack) rather than to an individual user, so anyone in the org gets the same baseline capability from day one.
2. **"Claude is a light source, the product is the lens"** -- a framing for why product surfaces must change as underlying model capability grows: the same underlying capability gets refocused into different UX shapes (CLI vs. inline Slack agent) as task-length and autonomy increase.
3. **The "goal" primitive** -- a way of instructing Claude with an end-state and a self-correction loop rather than a fixed procedure, e.g. "find opportunities to improve latency, check results, and profile," letting the agent run, measure against the goal, and iterate.
4. **Channel-based memory for proactivity preferences** -- letting users configure, per Slack channel, how proactive Claude should be (always respond, respond only to a specific request type, or respond only on a defined trigger/schedule), turning "when should the agent interrupt me" into a steerable, persistent setting rather than a global default.
5. **HTML as a communication surface** -- using rendered HTML dashboards/visualizations as the output format for long-horizon or data-heavy work, instead of plain chat text, as task complexity and duration grow.

---

## Key Findings

- Model task length has been doubling roughly every 4 months, which the author identifies as the key capability driver making asynchronous delegation viable.
- Security improvements cited as prerequisites for trusting async delegation: increased resistance to prompt injection, "auto-mode" classifiers that review agent actions, and a dedicated Claude Tag security model.
- Observed multi-player use cases: Claude joins a live incident Slack thread to help find root cause alongside multiple engineers; Claude is tagged into a long discussion thread to produce a postmortem with timeline and action items.
- Observed proactive use cases: long-running experiment monitoring with Claude keeping the run alive; proactive searching of channels to surface prior work/best practices before a task starts; a "channel watcher" pattern where Claude @-mentions the user once a stated condition is met.
- The author reports still switching back to the Claude Code CLI for tasks needing a "more hands-on UX," positioning Claude Tag as complementary to the CLI rather than a replacement.

---

## Suggestions & Future Directions

1. Claude Tag is framed as the first of several planned org-level surfaces beyond Slack.
2. The author points to companion write-ups (linked in the thread) for deeper coverage of: general Claude Tag capabilities, agent identity design, and multi-player coordination mechanics -- suggesting these are the natural next areas to dig into.
3. Implicit open question: as proactivity and autonomy increase further, channel-based memory/preference systems will likely need to keep expanding to stay the primary steering mechanism between full autonomy and constant check-ins.

---

## Authors & Institutions

Lance Martin (@RLanceMartin), Anthropic. Thread also credits @trq212 and @lydiahallie for related videos/write-ups referenced inline.
