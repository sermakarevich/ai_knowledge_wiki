> [[index|Wiki]] | [[summary|Summary]]

# Hermes Agent Documentation — In Plain Language

## What is this about?

Imagine hiring an assistant who sits at your computer, remembers how you like things done, writes down instructions for recurring chores so they never have to ask twice, and can text you on Telegram or Slack when something needs your eyes. That is Hermes Agent: a computer program by Nous Research you talk to in plain language, and it can run commands, browse files, search the web, and message you wherever you already chat.

The clever part is that it improves with use. Every conversation teaches it something — your preferences, your projects, the right way to do a task — and it files that away for next time, either as a short note it always remembers or as a step-by-step guide it pulls out only when relevant.

## Why does it matter?

Most chatbots are goldfish: every conversation starts from zero, they live in one browser tab, and they cannot actually do anything on your computer. Hermes is closer to a colleague with a desk, a notebook, and a phone: it remembers, it acts, it reaches you, and it keeps working on a schedule even when you are away. If that works reliably, routine computer chores — reports, monitoring, triage, follow-ups — stop needing your hands.

## How does it work?

Step by step, in everyday terms:

1. **You install it** with one command, like installing any app, and log in once to connect it to an AI brain (the easiest path needs no secret key).
2. **You chat with it** in your terminal (the text window programmers use) or in a nicer desktop app.
3. **It keeps two tiny notebooks**: one about the world (your computer, your projects, lessons learned) and one about you (how you like answers, your timezone, pet peeves). Small on purpose — only the essentials.
4. **It keeps a full diary too**: every past conversation is searchable in milliseconds, for free, when it needs to recall specifics.
5. **After each chat it reflects**: a background pass asks "what should I remember from that?" and files notes or updates its how-to guides — with your approval if you want it.
6. **It writes its own guidebook**: when it figures out a tricky multi-step task, it saves the recipe as a "skill" it can reuse, share, or download from a library others publish.
7. **It moves into your chat apps**: one background process connects Telegram, Discord, Slack, WhatsApp, and 15+ more, so you can talk to it from your phone.
8. **It can hire specialists**: you can create named helper personalities (a coder, a researcher) that collaborate in group chats and tap you only when human judgment is needed.
9. **It works while you sleep**: scheduled jobs run on their own in isolated sessions, and risky work can be undone thanks to automatic checkpoints.
10. **It asks before doing anything dangerous**, hides your secrets, and some destructive commands are simply never allowed — no matter what mode it is in.

## Where can this be used?

- A developer's daily driver: coding help, PR workflows, testing, and repo chores from the terminal.
- A phone-accessible assistant: check on long tasks, approve actions, or ask questions from Telegram or WhatsApp.
- A small team's helper crew: specialist bots for triage, monitoring, and reporting across Slack or Discord.
- A learning machine for repeated workflows: expense filing, deployment steps, research routines — learned once via `/learn`, reused forever.
- A research platform: recorded agent runs become training data for making future agents smarter.

## Conclusions & takeaways

Hermes' bet is that the durable value of an agent is what it accumulates — memory, skills, routines — not any single clever answer. The design keeps always-loaded memory tiny and cheap, loads procedures only when needed, and puts humans in the approval loop for what gets learned. Honest limits: it needs a capable model (large context), always-on operation costs tokens and attention, and self-written guides vary in quality — so gate the learning loop until trust is earned.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agent | A program that takes actions (runs commands, sends messages), not just answers |
| LLM (Large Language Model) | The AI brain that understands and writes text |
| CLI (Command Line Interface) | Talking to the computer by typing commands in a text window |
| TUI (Terminal User Interface) | A fancier text-window app with panels and mouse support |
| MCP (Model Context Protocol) | A standard plug for giving the agent new tools from outside apps |
| Memory (MEMORY.md / USER.md) | Two tiny notebooks: facts about the world, and facts about you |
| Skill | A reusable how-to guide the agent loads only when relevant |
| Gateway | The background process connecting the agent to chat apps |
| Bot Mode | Named helper personalities with their own memory and jobs |
| Cron | A scheduler that runs chores automatically on a timetable |
| Toolset | A bundle of tools switched on/off per task |
| Checkpoint / rollback | An undo point for computer work |
| FTS5 full-text search | Fast keyword search inside saved conversations |
| YOLO mode | Auto-approve everything (still with hard safety limits) |
