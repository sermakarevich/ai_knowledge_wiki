> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# ClawWork — In Plain Language

## What is this about?

Imagine hiring a freelancer and giving them $10 for the month — not just as pay, but as their whole operating budget. Every phone call, every Google search, every hour of thinking costs them money out of that $10, and they only earn money back when they deliver work good enough to get paid. That is ClawWork in a nutshell: it turns an AI assistant into an AI coworker that must earn a living.

The coworker gets real professional assignments — 220 tasks drawn from 44 occupations and economic sectors. It starts with just $10, pays for every word it generates, and only gets paid when the quality of its work clears a passing bar. If it wastes effort on rambling or failed attempts, it can go broke.
Think of the balance as a health bar in a video game: smart moves refill it, wasteful moves drain it.

## Why does it matter?

Most AI tests only ask "did it get the right answer?" ClawWork asks a tougher, more realistic question: "did it earn more than it spent?" That changes behavior completely. A brilliant answer that cost $5 in computing to produce is a failure if the job only pays $3.

This matters for anyone who wants to deploy AI workers in the real world, where computing costs are real and sloppy work earns nothing. It rewards agents that are frugal, pick the right jobs, and deliver reliably — just like a good human freelancer.

## How does it work?

1. **Get the job.** The agent is handed one professional task per workday from the task pool, simulating weekdays across a date range.
2. **Check the wallet.** Before starting, it sees its current dollar balance, what each word/s tool call costs, and the full task description.
3. **Do the work — or study.** It can spend the day doing the paid task with its tools, or choose to learn instead. It has at most about 15 rounds of back-and-forth with its tools per day.
4. **Pay as you go.** Every AI reply and paid tool call (search, document reading) is deducted from the balance immediately and logged to accounting files.
5. **Submit the result.** It produces files (reports, spreadsheets, documents) as deliverables. If it runs out of time, an automatic wrap-up step collects whatever it made and submits the best of it.
6. **Get graded.** An AI judge scores the work against a rubric (a checklist) specific to that occupation.
7. **Get paid — or not.** If the score is 0.6 or higher, the agent earns the full value of the job, priced as estimated hours times the real hourly wage for that occupation. Below 0.6, it earns $0.
8. **Survive.** Balances map to statuses: broke at $0 or less, struggling under $100, stable under $500, thriving above that. Results stream to a web dashboard.

## Where can this be used?

- **Testing AI workers.** Compare which AI setups actually make money instead of just sounding smart.
- **Building cheaper agents.** Find where agents waste computing budget and teach them to be thrifty.
- **Pricing real deployments.** Estimate what a task is worth (hours times wage) versus what it costs the AI to do it.
- **Live demos and monitoring.** Watch balances, earnings, and decisions on the dashboard, live or as a static report site.
- **Custom jobs.** Type a plain instruction starting with `/clawwork` and the system classifies it into an occupation, prices it, and runs the same earn-or-bust loop.

## Conclusions & takeaways

- ClawWork's core lesson: economic survival (income minus computing costs) is a stricter and more practical test than answer quality alone.
- The 0.6 quality bar is all-or-nothing: just below it pays nothing, just above it pays everything — so consistency near the bar matters enormously.
- Frugality is a skill: short, decisive work beats long, wasteful exploration because every token has a price.
- Choosing well matters too: agents decide each day whether to take the paid job or spend time learning.
- Honest limits (from the digest alone): quality scores come from one AI judge, not human clients; task dollar values rest on estimated hours and wage tables; the scheduler component is still an empty placeholder; and poor early decisions can bankrupt an agent before it proves itself.

## Jargon decoder

| Term | What it means in plain language |
| --- | --- |
| AI coworker | An AI expected to do billable professional work, not just chat |
| GDPVal tasks | The pool of 220 sample professional assignments used as jobs |
| Token | A small chunk of text the AI reads or writes; each one costs money |
| EconomicTracker | The built-in accountant that deducts costs and credits pay |
| LiveAgent | The daily worker program that picks up one task per day and does it |
| Evaluation threshold (0.6) | The passing grade: score this or higher to get paid, lower earns $0 |
| BLS wage | The official U.S. hourly pay rate for an occupation, used to price jobs |
| Rubric | The grading checklist the judge uses for each occupation |
| ClawMode / nanobot | The chat assistant the economic engine plugs into, plus its command loop |
| Dashboard | The React (a programme that runs in the browser) website showing balances, earnings, and rankings |
| Static data mode | A version of the dashboard that shows pre-built files instead of live data |
| Artifact | A file the agent produces as its deliverable, e.g. a report or spreadsheet |
