> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# ReAct: Synergizing Reasoning and Acting in Language Models — In Plain Language

## What is this about?

Think of a powerful racehorse and its tack — the saddle, bridle, and reins that channel all that strength in a useful direction. An AI (Artificial Intelligence) agent works the same way: the language model is the strong but unfocused horse, and everything around it — instructions, tools, checks, memory, permissions — is the tack. This guide calls that surrounding setup the harness, and says: Agent = Model + Harness.

The harness has two kinds of parts, borrowed from cybernetics (the science of control and feedback). Guides are feedforward controls: advice given before the agent acts, like a steering wheel. Sensors are feedback controls: checks run after the agent acts, like brakes. A car with a steering wheel but no brakes is dangerous, and the guide argues most teams today over-invest in guides and under-invest in sensors.

The big shift is this: writing clever prompts (Prompt engineering, the 2022–2024 fashion) was not replaced but absorbed. Prompting sits inside context engineering (giving the model the right information, 2025 fashion), which itself sits inside harness engineering (designing the whole system around the model, 2026 fashion). The model itself is treated as a commodity — interchangeable — while the harness is the real advantage.

## Why does it matter?

Because the numbers say the harness moves results far more than swapping models. On SWE-bench (a popular test where agents fix real software problems), changing the harness shifts scores by 22 points, while changing the model shifts scores by only about 1 point. LangChain kept the same model and gained 13.7 points on Terminal Bench 2.0 (a test of doing work in a computer terminal), from 52.8% to 66.5%, just by redesigning the harness. Princeton research reports harness setups improving solve rates by 64% over basic setups.

The same pattern shows up with business data. Atlan's data pipelines (automated flows that move and transform data) scored only 10–31% accuracy with a bare database description, but 94–99% with a properly governed harness. In other words, how you structure context beats how nicely you word the prompt. That matches a survey finding: 82% of IT (Information Technology) leaders say prompting alone is not enough for production agents.

It also matters because scale is now real. The idea spread in February 2026, and one OpenAI (a leading AI lab) case study describes 3 engineers shipping 1 million generated lines across 1,500 PRs (Pull Requests, proposed code changes) — about 3.5 PRs per engineer per day — with zero hand-written code. At that scale you cannot fix mistakes by hand; you must engineer each mistake away permanently.

## How does it work?

1. Start from one rule: every agent mistake is fixed in the harness, never in the output. The harness only tightens, never loosens. A bad answer is patched once so it can never happen again. This is called the ratchet principle.
2. Sort each mistake to the right fix. There are six standard routings: unknown rule goes into the project instruction file, violated rule becomes an automatic hook, missing information becomes a skill or MCP (Model Context Protocol, a standard way to plug tools and data into agents) tool, dangerous tool gets tighter permissions, polluted context gets a subagent (a helper agent that works in a clean, separate workspace), silent crash gets better monitoring.
3. Keep the instruction file lean and honest. Keep files like CLAUDE.md (a project instruction file the agent reads at startup) under 500 lines, with only things the model cannot guess: build and test commands, style rules, forbidden patterns, pointers to details. Every line must trace back to a real past failure; delete any rule you cannot link to a specific mistake.
4. Close the information gap. Anything a human teammate knows — docs, conventions, unwritten team habits — must be written into the harness. Otherwise the agent will make mistakes no human would make. This is called information parity.
5. Move must-hold rules from advice into enforcement. Instructions in CLAUDE.md are followed only about 70% of the time, while automatic hooks (small programs that run before or after agent actions) enforce at about 100%. So anything critical becomes a hook, not a polite request.
6. Load heavy knowledge on demand. Big references stay hidden behind skills that show only about 200 tokens (small chunks of text the model reads) at startup and load the rest when needed. After every edit, fast automatic sensors run: linters (programs that flag style and likely errors), tests, and type checkers (tools that verify data types line up).
7. Prefer fast, certain checks first. Use quick deterministic or computational sensors — tests, linters, type checkers, hooks — before slow LLM (Large Language Model) based judgment where another model grades the work. Wire these checks to run immediately after each edit for a tight feedback loop.
8. Separate thinking from doing. Split planning (deciding what to do) from generation (writing the code) and evaluation (checking it), because agents grade their own work too generously. Add recovery for overnight, unattended runs: handling crashes, running out of context (the model's working memory), and getting stuck.
9. Scale the same pattern to many agents. When you reach 10 or more agents, setup becomes an orchestration platform such as amux: tasks claimed from a Kanban board (a to-do / doing / done task board) over a REST API (Representational State Transfer Application Programming Interface, a standard way for programs to talk over the web), one isolated workspace per agent, a self-healing watchdog, messaging between sessions, an SSE (Server-Sent Events, a way to stream live updates to a web page) dashboard, and per-session token accounting.

## Where can this be used?

- Coding teams shipping software: several engineers running many agents in parallel to produce and review PRs (Pull Requests), with tests and linters catching errors after every edit.
- Terminal and computer-use tasks: agents that run commands, edit files, and run test suites, where a better harness lifted scores from 52.8% to 66.5% without changing the model.
- Data pipelines: company data flows where a governed harness lifted accuracy from 10–31% to 94–99%, by giving the agent structured, trustworthy context instead of a bare table list.
- Unattended overnight operation: agents that work while humans sleep, with crash recovery, stuck-state detection, and context-exhaustion handling so a failure does not silently stop the run.
- Multi-agent fleets: setups like 10+ agents coordinated through amux-style orchestration — task claiming, isolated workspaces, messaging, live dashboards — proven at scales such as 1 million LOC (Lines of Code) per day or over a thousand AI-assisted PRs per week.
- Self-improving setups: model-driven sensors such as plain-English self-report cards and event-driven subagent routines, which get better for free as the underlying models improve.

## Conclusions & takeaways

- The harness beats the model as an investment: 22 points versus 1 point on SWE-bench, +13.7 points with the same model, +64% in one study, and 10–31% versus 94–99% on data tasks.
- Fix the system, not the symptom: every mistake becomes a permanent harness fix, and every instruction line must earn its place by tracing to a real failure.
- Advice is weak, enforcement is strong: guides steer about 70% of the time, sensors enforce at about 100% — so critical rules belong in hooks, tests, and permissions.
- Keep it lean, then tighten: a short instruction file, on-demand skills, fast feedback after every edit, and planning kept separate from execution and evaluation.
- Honest limits: guides alone will fail about 3 times in 10; agents judge their own work too kindly, so outside checks are required; without encoded team knowledge the agent keeps making avoidable errors; and overnight or multi-agent runs need explicit recovery for crashes, full context, and stuck states — none of this removes the need for careful harness upkeep.

## Jargon decoder

| Term | What it means in plain language |
| --- | --- |
| Harness | Everything around the model — instructions, tools, checks, memory, permissions — that makes it reliable |
| Guide | Advice given before the agent acts, like a steering wheel; followed about 70% of the time |
| Sensor | Check run after the agent acts, like brakes; enforces at about 100% when automatic |
| Ratchet principle | Rule that every mistake is fixed permanently in the harness, which only tightens |
| CLAUDE.md / AGENTS.md | Project instruction file the agent reads at startup; keep short and tied to real failures |
| Hook | Small automatic program that runs before or after an action to enforce a rule |
| Skill / MCP tool | On-demand knowledge pack or plugged-in tool that loads details only when needed |
| Information parity | Making sure the agent knows everything a human teammate knows |
| Enforcement gap | The difference between advice followed ~70% and automatic checks enforced at ~100% |
| amux | Example orchestration setup for 10+ agents: task board, isolated workspaces, messaging, dashboard |
