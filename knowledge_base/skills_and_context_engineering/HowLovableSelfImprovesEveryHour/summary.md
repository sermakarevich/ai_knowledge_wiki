# How Lovable Self-Improves Every Hour

**Talk:** [How Lovable self-improves every hour — Benjamin van Beek, Lovable](https://www.youtube.com/watch?v=KA5kPbdkK2E)
**Speaker:** Benjamin van Beek, Member of Technical Staff, Lovable
**Source:** YouTube conference talk

---

## Human Readable TL;DR

Imagine a customer service team that writes down every time a customer had to ask the same question twice, figures out the real answer, and then trains every future rep with that knowledge so no customer ever hits that wall again. That is what Lovable built for its AI coding assistant -- and as a bonus, they gave the AI a "complaint box" where it can vent directly to the engineering team when something in the system is broken, which turned out to be a surprisingly good bug detector.

## TL;DR

Lovable built two complementary continuous-learning loops to reduce user friction at scale (200k+ projects/day). The first -- a "Stack Overflow for Lovable" -- detects when users are stuck, captures sessions that go stuck→unstuck, clusters them into reusable knowledge entries, injects them contextually into the agent, and A/B tests their effectiveness with production traffic. The second gives the agent a `vent_send_feedback` tool to self-report tooling or platform failures directly to Slack, which doubles as an early-warning incident detector and drives automated PR creation.

---

## Problem & Motivation

Non-technical users (the "99% who can't code") abandon AI-assisted product creation the moment they hit a hard technical block. Unlike technical users who can diagnose and work around friction, non-technical users simply give up -- permanently failing to experience successful AI. At 200,000 projects/day, even small friction rates translate to massive abandonment. The goal: make mistakes happen once and never again.

---

## Main Original Ideas

1. **Stuck Detection via LLM Judge** -- A lightweight model monitors sessions for signals of being stuck: repeated requests for the same thing, explicit complaints, failed resolution attempts, and premature session abandonment. It classifies whether a block is solvable-with-prompting, easy-to-fix (bugs/missing features), or genuinely hard.

2. **Lovable Stack Overflow (Knowledge Injection Loop)** -- When a session transitions from stuck→unstuck (user was blocked, then succeeded), the system captures the high-signal sample. It clusters similar cases to avoid one-off overfitting, generates a generalizable knowledge entry, validates it with an agent-as-eval (optionally human-reviewed), and stores it in a continuously updated knowledge bank. A lightweight model then injects relevant entries as context into the main agent when it detects a matching situation.

3. **Blank Injection A/B Testing** -- For a small fraction of cases where an injection would normally fire, the system deliberately injects nothing. This creates a clean comparison group to measure whether each knowledge entry is genuinely improving outcomes. Entries that don't improve the metric are demoted or removed.

4. **Knowledge Staleness Management** -- The knowledge bank is continuously rebalanced. Entries become stale after model updates or feature changes; the system actively prunes deprecated context to avoid "context rot" that degrades agent performance.

5. **Agent Vent Tool (`vent_send_feedback`)** -- The agent is given a tool to emit structured complaints when it encounters broken tooling, missing capabilities, confusing docs, or unexpected platform behavior. The tool is calibrated to only fire when the agent is genuinely frustrated, keeping signal-to-noise high. Reports go straight to a Slack channel and an automation agent triages, deduplicates, and creates PRs.

6. **Incident Detection via Vent Spikes** -- Platform incidents (broken sandboxes, server outages) cause sharp spikes in vent events. This has proven to be an earlier and more descriptive signal of what went wrong than traditional monitoring alone.

---

## Key Findings

| Metric | Result |
|--------|--------|
| Projects per day | 200,000+ (up from a few thousand a year prior) |
| "Fixing intent" messages | Significant and sustained decline after Stack Overflow injection |
| Project deployment rate | Measurable increase (key success metric) |
| Vent tool: first bug found | File copy tool silently failing on filenames with spaces (including non-breaking spaces from WhatsApp/Mac screenshots) |
| Models using Stack Overflow context | All top-ranked models in internal leaderboard |

- All top-performing models in Lovable's internal benchmark use Stack Overflow injection context.
- Vent tool spikes reliably correlated with production incidents and provided faster, more specific diagnosis than traditional monitoring.
- Agent meta-feedback emerged organically: the agent complained that the vent tool was too easy to trigger and offered no way to retract a message.
- Automated triage agent now monitors vent events, deduplicates, investigates, and opens PRs -- engineers only review and merge.

---

## Suggestions & Future Directions

1. **Fully close the loop** -- Automate the entire path from vent event → root cause analysis → PR → deploy → eval confirmation, reducing manual engineer review to zero.
2. **Finer stuck taxonomy** -- Distinguish solvable-with-prompting from easy-to-fix cases programmatically so routing (knowledge injection vs. engineering fix) is automatic.
3. **Model-aware knowledge versioning** -- Explicitly version knowledge entries against model releases so staleness detection is proactive rather than reactive.
4. **Broader adoption of inline feedback** -- Using the agent's in-context intelligence for self-reporting is cheaper and more signal-rich than external LLM reviewers on every turn; the pattern generalizes to any agentic platform.

---

## Authors & Institutions

Benjamin van Beek -- Member of Technical Staff, Lovable (formerly: satellites, particle physics, fusion reactor research)
