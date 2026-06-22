# Loop Engineering

**Source:** [Loop Engineering (Addy Osmani, Jun 9 2026)](https://x.com/addyosmani/status/2064127981161959567)

## Human Readable TL;DR

Instead of constantly typing instructions to AI coding assistants yourself, you can build a small automated system that does the instructing for you. Think of it like setting up an automated assembly line -- you design the line once, and it keeps producing results on its own. The system discovers what work needs doing, hands tasks to AI agents, checks their results, and keeps a record of progress. Your job shifts from factory worker to factory designer.

## TL;DR

Loop engineering is the practice of replacing yourself as the person who prompts coding agents by designing automated systems that do the prompting instead. It is built on five primitives -- automations, worktrees, skills, plugins/connectors, and sub-agents -- plus a persistent external memory store. Both Claude Code and OpenAI Codex now ship all five, making the pattern tool-agnostic. The paradigm shift: from turn-by-turn prompting to designing autonomous loops with verifiable stopping conditions.

---

## Problem & Motivation

For two years, working with coding agents meant writing a prompt, reading the result, then writing the next prompt -- the agent as a hand-held tool, one turn at a time. That model has a ceiling: the human is the bottleneck, present for every step.

The emerging alternative is to build a small control system that finds work, hands it to agents, checks results, and decides what comes next -- without the human in the loop for each turn. @steipete summarized it as: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." @bcherny (head of Claude Code at Anthropic) stated it directly: "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

---

## Main Original Ideas

1. **Loop engineering as a discipline** -- The explicit framing that "loop engineering" sits one floor above agent harness engineering and the factory model. You define a recursive goal; the AI iterates until complete, with the human absent from individual turns.

2. **Five-primitive model** -- A loop requires exactly five building blocks, now present in both major tools:
   - **Automations** -- Scheduled discovery and triage; runs that find nothing archive themselves; runs that find something surface to an inbox. Can call skills to stay maintainable.
   - **Worktrees** -- Isolated git working directories per agent; prevents parallel agents from colliding on the same files.
   - **Skills** -- Project knowledge written down once in a folder (SKILL.md + assets); the agent reads it every run instead of re-deriving context from scratch. "Skills compound; no skills re-derive from zero every cycle."
   - **Plugins and connectors (MCP)** -- Let the loop reach outside the filesystem: issue trackers, databases, Slack, CI. The difference between "here is the fix" and "the loop opened the PR, linked the ticket, and pinged the channel when CI went green."
   - **Sub-agents** -- Separate the maker from the checker. The model that wrote the code is too lenient grading its own work; a second agent with different instructions (sometimes a different model) catches what the first rationalized away.

3. **The sixth thing: external memory** -- A markdown file or Linear board outside the conversation that persists what has been done and what is next. The model forgets between runs; the repo does not. This is the spine of any long-running loop.

4. **Tool-agnostic shape** -- The five primitives map almost exactly onto both Codex and Claude Code under different names. Once you recognize the shape, loop design transfers across tools without re-learning.

5. **/goal as the loop's stop condition** -- Both tools implement a `/goal` primitive that keeps running across turns until a verifiable condition holds, checked by a fresh model separate from the one doing the work -- the maker/checker split applied to termination itself.

---

## Key Findings

- **Practical loop anatomy**: An automation runs on a schedule, calls a triage skill, writes findings to a state file, opens an isolated worktree per finding, dispatches a maker sub-agent and a checker sub-agent, lets connectors open the PR and update the ticket, and surfaces anything it cannot handle to a human inbox.
- **The leverage point moved** -- The hard skill is no longer prompt engineering; it is loop design. Same loop, two engineers: one uses it to move faster on work they understand deeply; the other uses it to avoid understanding the work at all.
- **Token cost is the main practical constraint** -- Sub-agents burn tokens proportionally to the number of concurrent threads; usage patterns vary wildly between token-rich and token-poor situations.
- **Quality risk is real** -- "Slop" concerns are valid. A loop running unattended is also a loop making mistakes unattended.

---

## Suggestions & Future Directions

1. **Verification remains a human responsibility** -- Even with a verifier sub-agent, "done" is a claim, not a proof. Osmani's standing rule: "Your job is to ship code you confirmed works."
2. **Guard against comprehension debt** -- The faster a loop ships code you did not write, the larger the gap between what exists and what you actually understand. Read what the loop made.
3. **Avoid cognitive surrender** -- Designing a loop to avoid thinking rather than with judgment is the same action with the opposite result. "Build the loop. Stay the engineer."
4. **Token awareness** -- Spend sub-agent calls where a second opinion is worth the cost; not every step warrants a separate checker.
5. **Balance direct prompting and loops** -- Directly prompting agents is still effective; loops are not a wholesale replacement, just a shift in leverage point.

---

## Authors & Institutions

Addy Osmani -- Director, Google Cloud AI; former engineering lead, Google Chrome.
