> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Six Months of Writing Code Exclusively With Agents - exe.dev blog — In Plain Language

## What is this about?

A software engineer set himself a rule in February: write no code by hand for six months.

He kept it almost perfectly — one lapse of three minutes — and used AI coding
agents for all real work instead. When an agent got stuck, he fixed the setup
around it (the instructions, tools, or environment) rather than typing the fix
himself.

The experiment started when models got clearly better. Early helpers like
Copilot autocomplete only drafted code. Then Claude Code plus stronger models
(GPT-5.3, Opus 4.6) could make larger changes across many files with less
hand-holding, so the results became good enough to build on.

Idle time did the rest. While one agent worked, he started another, then
another — until roughly 20 tasks were running at once, each on its own
disposable Linux cloud computer (VM), managed by a home-built tool called
botd that he could drive from his phone or laptop.

The punchline: making the code got easy. Deciding whether the code was worth
keeping became the real job.

## Why does it matter?

Before AI, this engineer's edge was a mental map of the whole system: how the
parts connect, which assumptions were never written down, and exactly which
line of code mattered. That map came from reading every change others made.

Hand-typing was his bottleneck. Even a small feature touched many layers
(buttons, database, tests, docs), with unequal risk — a bad button handler
reverts cleanly, a bad database change leaves a mess.

The experiment matters because it shows what changes when typing stops being
the limit:

- Output explodes: more gets built than ever, but so do dead ends — abandoned
  tasks, failed designs, even a collapsed tool (botd itself died).
- Failures get cheap: a trashed disposable computer costs almost nothing, so
  trying things and throwing them away becomes normal.
- Judgment becomes scarce: tests say "it works" but not "it belongs here."
  Small conveniences can mean years of maintenance, and once people rely on
  a behavior it is very hard to remove.
- Familiarity fades: he lost some line-by-line knowledge of the code, but
  gained something else — a saved, searchable history of every agent
  conversation that he can query later.

In short: code became cheap, so engineering judgment — what to build, what to
reject, how the pieces fit — became the valuable part.

## How does it work?

In plain terms, an AI agent is a language model running in a loop with tools:
send it a message, let it call a tool (run a command, read a file, search
logs), feed the result back, repeat. The loop is simple — the tools decide
what the agent is capable of. A coding agent needs a full computer: command
line, compilers, browsers, freedom to install things.

Growing from one agent to twenty required solving isolation step by step:

1. One shared computer failed — agents overwrote each other's files, fought
   over settings and network ports, and blocked each other.
2. Separate file checkouts (worktrees) fixed file clashes but not shared
   databases, ports, or stray processes.
3. Written rules ("use a random port, use a throwaway database") helped a
   little but wasted the agent's attention on avoiding neighbors.
4. Containers separated processes and local data, but the laptop still had to
   stay awake and approve commands.
5. One cloud computer per task won: fast to start, reachable over the network,
   and work survived closing the laptop.

The botd tool followed three rules: run off the laptop, work from a phone
(no terminal needed), and save every conversation. Agents ran in "do anything
locally" mode inside the throwaway computers, while secrets stayed outside:
passwords were added by a middleman service, never stored where the agent
could see them, and write access was limited to test systems.

Checking the work also scaled up. Agents ran tests, triggered the full
automatic test suite, opened the app in a browser, and sent screenshots.
Other agents reviewed the code, but the human still had to understand each
change before accepting it — an agent grading its own homework can confidently
build and test the wrong thing.

## Where can this be used?

The most useful agents in the story never wrote product code at all:

- **Investigators.** Given a customer's exact report plus access to system
  logs, the agent reconstructed what actually happened. The human then
  decided — and sometimes the right fix was a help page or an email, not code.
  Passing along the customer's exact words mattered: summarizing first would
  bake in the engineer's own blind spots.
- **Attackers.** A "try to break into our systems" agent found network paths
  everyone believed were closed and showed exactly how to reach them, so they
  were fixed before outsiders noticed.
- **Watchers.** A deployment-watcher called Athena babysits gradual rollouts,
  reading the change, the metrics, and the logs. Once it correctly diagnosed
  a failure as a broken server (not bad new code) and kept rolling out
  instead of panicking.

The same approach applies anywhere judgment plus tireless checking beats
typing: triaging bug reports against logs, probing your own security
assumptions, supervising risky rollouts, and digging through saved history to
reconstruct why a design decision was made.

The warning travels with it. Accepting agent-built systems without designing
them first produces a "brand-new legacy codebase" — code nobody understands
that is painful to change. The author calls that vibe coding; the alternative,
agentic engineering, means settling the architecture, interfaces, limits, and
tradeoffs with the agent before accepting the code.

## Conclusions & takeaways

- Code is cheap; systems carry weight. Data, running processes, and users
  mid-task must survive a change — moving them safely is the hard part.
- Test behavior, not implementation. Tests that describe what must stay true
  survive rewrites; tests that mirror the current code break every time an
  agent reshuffles it.
- Hygiene compounds. Agents copy whatever patterns they find, good or bad —
  every tolerated shortcut becomes the template for the next hundred changes.
- Small custom checks pay off. Since writing a one-off checker is now cheap,
  encode each lesson as a rule (a linter) so the mistake becomes impossible.
- Design first, code second. The review that matters happens in the design
  discussion, the contracts, and the validation — not line-by-line review.
- Keep the history. Saving every agent conversation proved as valuable as
  the code: when botd collapsed under its messy design, its saved history
  survived and another agent could still analyze what went wrong.
- The loop moved up a level. The old cycle was write, run, fail, fix on code.
  The new cycle is the same loop on prompts, designs, and whole features — a
  rewrite that used to cost a week now costs a conversation.

Final line of the story: he stopped writing code by hand, but he did not
stop engineering.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agent | An AI model running in a repeat loop: think, use a tool, read the result, repeat until done. |
| Model | The AI brain inside the agent (e.g. GPT-5.3, Opus 4.6); stronger models need less supervision. |
| VM (virtual machine) | A rented computer in the cloud used for one task, then thrown away; keeps tasks from interfering. |
| botd | The author's home-built dashboard: starts cloud computers, tracks agent tasks, works from a phone. |
| YOLO mode | Letting the agent run any command locally without asking first — safe only inside a throwaway computer. |
| CI (continuous integration) | An automatic service that runs the full test suite on every change before it can be merged. |
| Hyrum's Law | Once enough people use software, someone depends on every visible behavior — even accidental ones — so removing features is painful. |
| Vibe coding | Accepting AI-written code without understanding or designing it; fast now, painful to maintain later. |
| Agentic engineering | Designing the structure, interfaces, and tradeoffs with the agent first, so you understand the code you accept. |
