# One Developer, Two Dozen Agents, Zero Alignment

**Source:** [One Developer, Two Dozen Agents, Zero Alignment (Maggie Appleton, 2026)](https://maggieappleton.com/zero-alignment)
**Author:** Maggie Appleton -- Staff Research Engineer, GitHub Next
**Context:** First public demo of the Ace research prototype

---

## Human Readable TL;DR

Imagine you gave every worker in an office a magic copy machine that could finish paperwork in seconds. You'd expect to get more done, right? But if nobody agrees on *what* paperwork to file, you just end up with a mountain of the wrong forms done very quickly. That's the problem with today's AI coding tools -- they make individual programmers faster, but software is a team sport. The real bottleneck was never typing the code; it was everyone agreeing on what to build. This talk introduces a new tool called Ace that treats AI-assisted coding as a shared, multiplayer activity, so the whole team -- developers, designers, product managers -- can steer together in real time.

## TL;DR

Appleton argues that current AI coding agents optimize for individual developer throughput, but the actual constraint in modern software teams is *alignment*: agreeing on what to build, why, and in what order. As agent velocity compresses implementation from weeks to minutes, traditional synchronization touchpoints (planning meetings, early reviews, shared context gathering) are lost. Ace is a multiplayer coding workspace -- combining Slack-style chat, sandboxed cloud VMs, and shared agent sessions -- designed to restore alignment at agentic speed.

---

## Problem & Motivation

The prevailing "one developer, many agents" vision treats faster implementation as the primary goal. Appleton challenges this with a core observation: **implementation is no longer the bottleneck -- agreement is**. When individual output accelerates, teams lose the incidental coordination that traditional slow workflows provided (planning discussions, incremental feedback, shared context). The result is wasted work: features built without stakeholder input, critical feedback arriving only after completion, merge conflicts from parallel uncoordinated agent runs, and PR queues that no one can review fast enough.

---

## Main Original Ideas

1. **The Alignment Cost of Speed** -- When agents compress implementation from weeks to minutes, teams lose the pre-implementation alignment checkpoints baked into traditional workflows. Speed trades throughput for synchronization, pushing coordination dangerously late (post-implementation review instead of pre-implementation planning).

2. **The Nine Women / One Baby Fallacy Applied to Software** -- Individual productivity gains do not compose into team productivity. Believing otherwise mirrors the logical error of thinking nine women can produce a baby in one month -- parallelism doesn't help when the bottleneck is coordination, not capacity.

3. **Existing Tools Are Misfit for Agentic Velocity** -- GitHub, Slack, Jira, and Linear were designed for human-paced development. Forcing agentic output volumes through these platforms creates coordination debt rather than eliminating it.

4. **Quality as the New Differentiator** -- In a world of fast, cheap software, quality becomes the competitive moat. Reclaiming time from implementation should fund deeper user research, more rigorous architecture decisions, and better design thinking -- not just more output.

5. **Multiplayer Coding Workspaces** -- The architectural response: shared sessions backed by sandboxed cloud VMs, collaborative prompting (multiple people steering one agent), real-time plan editing, and a context dashboard that surfaces what teammates are building and deciding.

---

## Key Findings

| Problem | Traditional Workflow | Agentic (Current) | Ace Approach |
|---|---|---|---|
| Planning alignment | Synchronous meetings | Lost / compressed | Real-time collaborative plans |
| Feedback timing | Mid-implementation reviews | Post-implementation only | Live preview + shared session |
| Context sharing | Stand-ups, PRs | Overwhelming PR queues | Context dashboard with summaries |
| Tool access | Developer-only | Developer-only | Designers & PMs share interface |
| Environment parity | "Works on my machine" | Still fragmented | Shared sandboxed cloud VMs |

- Shared sessions allow non-developers to participate directly: designers and PMs prompt the same agent and see real-time code previews.
- Backwards compatibility is preserved -- PRs still push to GitHub; VS Code integration is available for complex work.

---

## Suggestions & Future Directions

1. **Shift the success metric** from lines of code / PRs merged to alignment quality and decision throughput.
2. **Design agentic tools as team interfaces first**, individual tools second.
3. **Invest recovered implementation time** in upstream activities: user research, design, architecture -- not additional feature volume.
4. **Mobile support** for Ace is in development, enabling async input from non-desktop team members.
5. **Open question:** How do you measure and incentivize alignment in engineering organizations that currently reward individual output?

---

## Authors & Institutions

Maggie Appleton -- GitHub Next (Staff Research Engineer)
