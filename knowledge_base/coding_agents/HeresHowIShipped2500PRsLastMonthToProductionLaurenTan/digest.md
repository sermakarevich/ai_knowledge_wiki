> [[index|Wiki]] | [[summary|Summary]]
# here's how i shipped 2,500 PRs last month to production - Lauren Tan https://x.com/poteto — Digest

## 1. [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren — trust thesis behind 2,000 PRs a month]]
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

## The argument in five moves
1. High-volume shipping (~2,000 PRs/month) is framed not as working faster but as building trust so agents can produce quality work unsupervised.
2. The bottleneck is human verification: manual DevTools traces and heap snapshots could not keep up with the wall of PRs on the Cursor agent window.
3. The first lever is verification skills (Control Glass CLI + feature map) that let agents run the app, reproduce behavior, and check their own work with empirical evidence.
4. The second lever is engineer-like skills and codebase-as-memory: PAC playbooks plus an agent-friendly architecture (Dune conventions, single paved path, lint-first weed-pulling) so the default pattern agents copy is the right one.
5. These compound into Michelin-kitchen operations — trusted environment, connectors/routines/auto-repro outer loop, corrections pushed up the five-layer trust stack — until agents "can just be free."
