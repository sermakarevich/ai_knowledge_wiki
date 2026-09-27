> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Hi, my name is Lauren — trust thesis behind 2,000 PRs a month
**In one sentence:** Lauren Tan (Potato on X), working on Grokbot at SpaceX AI, argues that shipping ~2,000 pull requests to production in a month is possible by building trust in agents through environment setup — verification skills, engineer-like skills, and an agent-friendly codebase — organized like a Michelin kitchen rather than a software factory.
## Key points
- Lauren Tan identifies as Potato on X and works on Grokbot at SpaceX AI, and reports shipping 2,000 pull requests to production last month.
- Her thesis is that a well-set-up agent environment creates a personal or team-scale production system for high-quality code at much greater rates, enabled by trusting agents to produce quality work unsupervised.
- She prefers the Michelin kitchen analogy over "software factory": agents are line cooks/sous-chefs/dishwashers, leaders set up equipment, training, and ratios, and humans remain responsible for the final creative outcome.
- Six months earlier she joined Cursor (before it was part of SpaceX AI) to work on the replacement for the Cursor IDE (agents window), which had performance issues, and found manual Chrome DevTools traces and heap snapshots could not keep up with the wall of incoming PRs.
- That frustration led to verification skills: her first skill, Control Glass, uses the Chrome DevTools Protocol with a reusable CLI plus a stored "feature map" (materialized memory of features, navigation, shortcuts, DOM elements) maintained by automation.
- She describes a trust continuum from 1–5 agents (constant babysitting and course-correction) toward ~100 agents, warning that scaling without trust produces slop PRs, regressions, and bugs.
- The core prescription is a five-layer trust stack in priority order: codebase/architecture (make bad patterns categorically impossible), static analysis (linters, compiler diagnostics, CI), rules/Bugbot/skills (guidance agents may forget), and style guides/human review as the weakest last resort.
- For the Grokbot codebase she cites Dune, an agent-friendly framework with strict conventions (co-located features, entry points/routes, transcript cards, host on the Grokbot VM, client separation, main/renderer thread import boundaries enforced via the dependency graph), including a ban on code comments to stop agents copying workaround justifications.
---
## Intro and thesis
Lauren Tan introduces herself as Potato on X, working on Grokbot at SpaceX AI:

> "Hi, my name is Lauren. You might know me as Potato On X. And I work on Grockbot at SpaceX AI. So, last month I did something pretty crazy. I shipped 2,000 pull requests to production."

Her stated argument:

> "if you set up your environment for your agents really really well, you can end up with something that looks more like a personal or even team software factory where you're producing very high quality code at much greater rates than before."

She rejects the "software factory" term in favor of a Michelin kitchen: technologists are not mass-producing on an assembly line; the work is creative/art, agents no longer "cook the individual components" but humans own the final outcome via kitchen setup (line cooks, sous-chefs, equipment, training, dishwasher ratios).

## Origin story: Cursor performance work
- Joined Cursor six months ago (before SpaceX AI), with no agent skills, fresh codebase and product.
- Tasked by her manager with performance issues in the Cursor agent window (replacement for the Cursor IDE), drawing on prior React team experience.
- Early work was manual Chrome DevTools performance traces and heap snapshots against an "insurmountable wall of pull requests" with no signal on regressions.
- Realization: "wait we have agents what am I doing?" — leading to verification skills where the agent runs the app, takes traces, understands them, finds hotspots, and hill-climbs performance automatically.
- She stresses she never set out to ship 2,000 PRs/month; skills, tools, and codebase changes compounded into trust, driven by the thought "I am the bottleneck" and the need to impart engineer knowledge into a team of agents.

## The trust graph: 1–5 agents vs 100 agents
- Starting state (1 to 1–5 agents): babysitting every chat, constantly intervening and correcting; without supervision nothing happens or agents do the wrong thing.
- She calls this the hardest phase to escape because the exit path is unclear.
- Scaling to ~100 sub-agents/cloud agents without trust yields "a ton of slop pull requests" plus regressions and bugs.
- Verification is presented as the starting lever: lower end = verification skills (teach agent to run the app, use Chrome DevTools Protocol, take traces/heap snapshots); opposite end = formal verification (formal methods, Lean, TLA+, business-logic invariants), which is harder and still an open question, and few can use — but verification skills alone go "very far."

## Control Glass and the feature map
| Component | What it does |
|---|---|
| CLI inside the skill directory | Reproducible app runs, trace/evidence collection, performance-bar checks; avoids per-session ad-hoc scripts; invested in to handle many use cases |
| Feature map | Materialized memory of how the app works: features, how users reach them (keyboard shortcuts, DOM elements to click), what features do; stored in the skill directory in the codebase with maintaining automation |

- Motivation: vague Slack reports (small UI slice screenshot plus "three question marks") left agents able to run the app but guessing at intent; CLI + feature map together let agents reproducibly control the app and understand internal/external requests.
- Result: control/verification skills became "critical infrastructure" the team constantly maintains; an agent verifying its own work with empirical evidence is "extremely powerful" for trust.

## Beyond correctness: PAC skills and code quality
- Verification covers correctness ("does the checkout button actually check out the cart?") with empirical evidence, but not performance or code quality.
- Response: PAC plugin (collection of skills/playbooks for debugging, feature development, prototyping) encoding her personal software-engineering workflows to teach agents to write code the way she wants.
- Senior engineers should contribute a team repository of such skills; combined with verification skills, agents verify correctness and produce high quality, plus real performance metrics/statistics/telemetry.

## Codebase as memory; garden and virus analogies
- Claim: refactor/rewrite architecture to be agent-friendly, possibly the most important investment if agents will write all future code — design codebases so the default is the right thing.
- Mechanism: codebase is "the best form of memory" because LLMs extend existing patterns in their context window (files agents read/open); they extend rather than refactor each PR.
- Anti-patterns spread "like a virus": one workaround/comment gets copied by agents across the codebase in days/weeks into a de facto pattern; garden analogy: workarounds are weeds needing a "gardener" role to nip them early.
- Example: banning agent-written code comments in Dune, because agents used surrounding comments to justify papering over problems with band-aids instead of real fixes.
- Dune principles: delete existing tech debt; enforce a single paved/blessed path with conventions plus CI/lint guidance so agents need not guess; on seeing bad patterns, first write a lint rule to "stop the bleeding" even before cleanup; keep the codebase in a state you would be happy for an agent to copy.

## Dune example and Michelin-kitchen operations
- Dune is the client framework powering Grokbot, born from Cursor agent-window performance lessons on the premise that "agents love taking shortcuts" — so make the easy path the right path, even if locked-down and "annoying for humans," suited to minimal-context contributors (designers, PMs, CEOs).
- Conventions cited: features co-located in a single folder, entry points (like routes) in the React code, transcript cards in the Grokbot app, host on the Grokbot VM, client powering the application, with strict boundaries (e.g., main-process/Electron main-thread code barred from the renderer thread) enforced through the import/dependency graph to protect 60fps (16ms) / 120fps (8ms) renderer budgets.
- Broader point: an agent-friendly framework encodes tribal knowledge of the best engineers, moving it out of style-guide/human-review comments into the framework and codebase as materialized memory.
- Operations: Grokbot provides the "outer loop" via connectors (Slack, Datadog, Sentry, PlanetScale) aggregating signals ("company brain" term noted but deemed unnecessary since agents use tools well); Grokbot routines subscribe to Slack threads/Sentry alerts and auto-kick-off cloud agents, plus Cursor automations/SDK bots reusing the same agent infra for tasks like automatic bug-report reproduction and PR opening.
- Closing prescription: when correcting/intervening on an agent, work the five layers in order — codebase/architecture (categorically impossible via data structures/algorithms), static analysis, then rules/Bugbot/skills — until the environment is trusted enough that agents "can just be free"; contact: X handle "potato with an E."

**Covers:** Full-talk single chunk 01 (intro and trust thesis behind shipping ~2,000 PRs to production with agents; Lauren Tan talk).
