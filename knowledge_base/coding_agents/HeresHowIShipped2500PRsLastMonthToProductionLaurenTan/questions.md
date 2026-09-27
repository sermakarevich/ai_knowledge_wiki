---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: here's how i shipped 2,500 PRs last month to production - Lauren Tan https://x.com/poteto

### Q1. What is Lauren Tan's central thesis for shipping ~2,000 PRs to production in a month?

> [!tip]- Answer
> Her thesis is that high-volume shipping comes from building trust in agents through environment setup, not from working faster: verification skills, engineer-like skills, and an agent-friendly codebase let agents produce quality work unsupervised. She frames the result as a personal or team-scale production system for high-quality code at much greater rates. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q2. Why does Tan prefer the Michelin kitchen analogy over the "software factory"?

> [!tip]- Answer
> She rejects the assembly-line image because the work is creative: agents act as line cooks, sous-chefs, and dishwashers while leaders set up equipment, training, and ratios, and humans own the final creative outcome. The kitchen setup — not mass production — is what makes high output possible. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q3. What bottleneck at Cursor led Tan to build verification skills?

> [!tip]- Answer
> Working on performance in the Cursor agent window (the IDE replacement), she faced a wall of incoming PRs with no regression signal, and manual Chrome DevTools traces and heap snapshots could not keep up. Her realization — "wait we have agents what am I doing?" — led to skills where the agent runs the app, takes traces, and hill-climbs performance itself. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q4. What are the two components of Control Glass and its feature map, and why do they matter?

> [!tip]- Answer
> Control Glass pairs a reusable CLI in the skill directory (reproducible app runs, trace and evidence collection, performance-bar checks) with a stored feature map (materialized memory of features, navigation, shortcuts, and DOM elements, maintained by automation). Together they let agents reproducibly control the app and understand intent instead of guessing from vague reports. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q5. What is the five-layer trust stack, and in what order should corrections be pushed up it?

> [!tip]- Answer
> In priority order the layers are: codebase/architecture (make bad patterns categorically impossible), static analysis (linters, compiler diagnostics, CI), rules/Bugbot/skills (guidance agents may forget), with style guides and human review as the weakest last resort. When correcting an agent, push the fix up the stack toward architecture first so the default path becomes the right one. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q6. Why does Tan call the codebase "the best form of memory," and what follows from the garden and virus analogies?

> [!tip]- Answer
> LLMs extend existing patterns in their context window rather than refactoring, so whatever agents read and copy becomes the de facto pattern across PRs. One workaround or comment spreads "like a virus" into codebase-wide tech debt, so workarounds are weeds needing a "gardener" role: write a lint rule first to stop the bleeding, delete tech debt, ban comment-justified band-aids, and keep the codebase in a state you would be happy for an agent to copy. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].

### Q7. Should your team adopt Tan's trust-stack approach (Dune-style conventions, lint-first weed-pulling, verification skills) to scale agent output?

> [!tip]- Answer
> Recommend it where agent-written code dominates and regressions are the bottleneck: locked-down conventions plus lint rules and verification skills compound into unsupervised trust, while style guides and human review alone cannot scale past a handful of agents. Reject or defer it where the codebase is small, human-authored, or highly exploratory, since the framework, feature-map, and automation investment only pays off at volume. Judge by failure cost: adopt the layers that make your most expensive failure class categorically impossible first. See [[wiki/01-hi-my-name-is-lauren-you|Hi, my name is Lauren]].
