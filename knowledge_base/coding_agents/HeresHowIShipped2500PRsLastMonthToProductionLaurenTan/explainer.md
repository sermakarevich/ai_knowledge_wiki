> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# here's how i shipped 2,500 PRs last month to production - Lauren Tan https://x.com/poteto — In Plain Language

## What is this about?

This is a talk by Lauren Tan (known as Potato on X), who works on Grokbot at SpaceX AI.

Her headline claim: she shipped around 2,000 pull requests to production in a single month — not by typing faster, but by setting up AI coding agents so well that they could do good work without constant supervision.

The big idea is trust. Right now most people use 1 to 5 agents and have to babysit every step. Lauren argues that if you invest in the environment around the agents — the tools, checks, and codebase — you can scale to dozens or ~100 agents producing high-quality work, like running a professional kitchen instead of a factory assembly line.

## Why does it matter?

Anyone who has tried AI coding agents knows the painful starting phase: you ask for a change, the agent does the wrong thing, you correct it, repeat. That babysitting is the bottleneck.

Lauren's story makes this concrete. Six months earlier she joined Cursor to fix performance problems in the new agents window (the replacement for the Cursor IDE). There was a wall of incoming pull requests and no clear signal about what caused slowdowns. Manual checking with browser developer tools and memory snapshots could not keep up.

Her conclusion: "I am the bottleneck." Instead of working harder herself, she taught the agents to do what a good engineer does — run the app, measure it, check their own work, and follow team conventions. That shift is what unlocked volume without a collapse in quality.

Without that trust, she warns, scaling up just produces piles of low-quality changes, regressions, and bugs.

## How does it work?

Three layers build on each other: verification skills, engineer-like skills, and an agent-friendly codebase, wrapped in kitchen-style operations.

**1. Verification skills: let agents check their own work.**

The first skill she built was called Control Glass. In plain terms:

- It gives the agent a reusable command tool that launches the app, drives it through the browser automation protocol, and collects evidence (traces, snapshots, performance numbers).
- It keeps a "feature map": a stored guide to what the app does, how users reach each feature (shortcuts, buttons), and which parts of the page matter. Automation keeps this guide up to date.

Before this, a vague bug report (a tiny screenshot plus "???") left agents guessing. After this, agents can reproduce the problem, test their fix, and show proof — which builds trust fast.

**2. Engineer-like skills: teach taste, not just correctness.**

Verification answers "does the button work?" It does not answer "is the code clean and fast?"

So she built a second collection (the PAC plugin): step-by-step playbooks for debugging, building features, and prototyping that capture how she personally likes to work. The suggestion is that every senior engineer should contribute their own playbooks, so the team of agents writes code the way the team wants it — plus real metrics and telemetry, not vibes.

**3. Codebase as memory: make the easy path the right path.**

Her strongest claim: the codebase itself is the best memory for agents, because agents copy whatever patterns they see open in front of them.

That cuts both ways. One workaround or misleading comment gets copied everywhere within days, "like a virus." So someone has to garden: pull the weeds early, delete tech debt, and enforce one clear blessed path with conventions and automatic checks.

Her example is Dune, the framework behind Grokbot. It is deliberately strict — features kept together in one folder, clear entry points, enforced boundaries between fast and slow parts of the app — even if that strictness annoys humans. The payoff is that an agent with almost no context (a designer, a PM, even a CEO) still lands on the right pattern by default. One memorable rule: a ban on agent-written code comments, because agents were reading old comments as permission to paper over problems.

**4. The trust stack and the outer loop.**

When something goes wrong, she fixes it in this order:

1. Codebase and architecture — make the bad pattern impossible.
2. Static analysis — linters, compiler checks, CI.
3. Rules, bots, and skills — guidance agents can forget.
4. Style guides and human review — weakest, last resort.

Around all of this sits an "outer loop": connectors to Slack, error trackers, and databases, plus routines that watch for alerts and automatically start an agent to reproduce the bug and open a fix. Human corrections get pushed up the stack so the same mistake cannot happen again — until agents "can just be free."

## Where can this be used?

- Any team using AI coding agents that feels stuck babysitting 1–5 agents and wants to scale without drowning in bad PRs.
- Performance work: agents that run the app themselves, take measurements, find hotspots, and improve step by step.
- Bug triage: auto-reproduce vague reports (screenshot + "???") into a tested fix with evidence attached.
- Codebases agents will mostly write from now on: strict conventions, one paved path, lint-first fixes.
- Cross-functional teams: locked-down frameworks that let non-engineers ship safely with minimal context.
- On-call and maintenance: routines that turn alerts into reproduction attempts and draft PRs automatically.

## Conclusions & takeaways

- Volume comes from trust, not speed. Setup first, then scale.
- Start with verification: if agents can run the app and prove their work, everything else gets easier.
- Encode taste as playbooks. Senior engineers should write down how they debug and build so agents copy the good habits.
- Treat the codebase as memory. Keep it so clean you would be happy for an agent to copy any part of it.
- Fix problems from the strongest layer down: architecture first, human review last.
- Think Michelin kitchen, not factory: leaders set up equipment, training, and ratios; agents do the cooking; humans own the final dish.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Pull request (PR) | A proposed code change packaged up for review before it goes live. |
| Production | The real app real users touch, as opposed to a test copy. |
| Agent | An AI assistant that can read code, run commands, and make changes on its own. |
| Verification skill | A reusable tool that lets an agent run the app and collect proof its change works. |
| Chrome DevTools Protocol | A remote-control interface for the browser used to inspect, measure, and drive web pages. |
| Feature map | A stored guide to what each part of the app does and how to reach it. |
| Static analysis / linter | Automatic checkers that scan code for mistakes and style violations without running it. |
| CI (continuous integration) | Automatic tests and checks that run on every proposed change. |
| PAC plugin | Her collection of step-by-step engineering playbooks given to agents. |
| Dune | The strict, convention-heavy app framework behind Grokbot designed to be easy for agents to copy correctly. |
| Outer loop | Background routines and connectors that turn alerts and messages into agent tasks automatically. |
| Trust stack | Her priority order for fixes: architecture first, then automatic checks, then guidance, then human review. |
