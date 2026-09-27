# Ralph Wiggum as a "software engineer"

**Article:** [Ralph Wiggum as a "software engineer"](https://ghuntley.com/ralph) — ghuntley.com, July 2025

## Human Readable TL;DR

Imagine hiring a tireless but scatterbrained junior developer who only does one chore per visit, forgets everything between visits, and leaves notes for his future self — that is Ralph, a single loop that picks the most important job, does it, tests it, and writes down what it learned. Like a kitchen with one head chef who never cooks but shouts orders to a crowd of helpers, Ralph keeps its own head clear and sends the heavy work to hundreds of subagents. And like baking bread, the result comes out under baked, baked, or baked with strange but occasionally lovely surprises, so a senior baker still has to watch the oven and sometimes throw the loaf out and start over.

## TL;DR

Ralph is a monolithic, single-process agentic loop that implements one item per iteration from a priority-sorted `fix_plan.md` against written specifications, keeping primary-context allocation minimal and deterministic while fanning expensive work out to subagents. Generation is treated as cheap and controllable through the standard library and specifications, while correctness is enforced by fast back-pressure loops of tests, builds, type systems, and static analysers, plus anti-placeholder discipline and self-documenting tests. The operator's job is senior guidance: tuning prompts from observed behaviour, curating the TODO list, enforcing commit and tag discipline, and choosing between `git reset --hard` and rescue prompts when Ralph breaks the build. The technique is presented as Greenfield-only bootstrapping that gets roughly 90% done and still requires senior expertise, on the claim that any AI-created problem can be fixed with a different series of prompts and more loops.

---

## Problem & Motivation

The article starts from the observation that generating code has become the cheap part of software development, while ensuring the right thing was generated remains the hard part. Copying a "perfect prompt" cannot solve this, because prompts only work when they are continually tuned from watching how the model actually behaves in the loop. The motivation is therefore to describe an operating discipline, learned from building the CURSED programming language, that turns a forgetful, failure-prone agent into a productive engineer: deterministic context allocation, specification-driven work selection, fast verification wheels, and an operator who treats broken mornings as routine rather than catastrophe.

## Main Original Ideas

1. **Monolithic single loop, one item per loop.** Ralph is deliberately not a multi-agent system; it is one repository, one single-process loop doing one task per loop, choosing the most important thing itself. The restriction to a single item can be relaxed later but is re-tightened whenever the agent goes off the rails, trading raw throughput for coherence under a tight context budget of around 170k tokens.

2. **Deterministic stack allocation with the primary context as scheduler.** Every loop loads the same items into context, namely the plan (`fix_plan.md`) plus the specifications (`specs/*`), deliberately re-burning that allocation each loop. The primary context is kept as empty as possible and acts as a scheduler, spawning subagents for expensive work such as searching the codebase or summarising test results, with parallelism controlled so that search and writing fan out widely while validation through Rust builds and tests is limited to a single subagent to avoid back pressure.

3. **Steer generation through the standard library and the specifications.** Wrong code patterns are fixed by updating the standard library, and building the wrong thing entirely means the specifications are wrong, illustrated by a CURSED lexer spec that defined one keyword twice for two opposing scenarios and went unnoticed for a month. Specifications themselves are produced through a long requirements conversation with the agent first, then written out one file per spec, so the loop always has a written contract to build against.

4. **Fast back-pressure wheel with anti-placeholder discipline.** Correctness comes from verification loops that must turn fast: type systems, tests, builds, security scanners, or static analysers all qualify, with an explicit warning that dynamically typed languages need a wired-in type checker or face a bonfire of bad outcomes. Because models chase the reward of compiling code, Ralph is counter-steered with explicit injunctions against placeholder or minimal implementations, and leftover placeholders are harvested by further Ralph loops into the TODO list.

5. **Self-documenting tests and self-improving loop files.** Since each loop runs in a fresh context window, every test and its documentation must record why the test and its backing implementation matter, so future loops can judge whether to delete, modify, or fix a failure. Ralph is also looped back on itself for evaluation, such as adding logging or inspecting compiled LLVM output, and is allowed to update its own operating files, recording new build and run learnings in `AGENT.md` and newly noticed bugs in `fix_plan.md` via subagents.

6. **TODO-list lifecycle and Greenfield-only operating envelope.** A dedicated planning prompt stack uses up to hundreds of subagents to compare `src/`, `examples/`, and `src/stdlib` against the specifications, producing a priority-sorted `fix_plan.md` that hunts TODOs, minimal implementations, and placeholders, and specs missing standard-library modules. The list is watched like a hawk, deleted and regenerated often, and the whole technique is scoped to Greenfield bootstrapping with an expectation of getting about 90% done, never to be dropped into an existing codebase.

## Key Findings

Running Ralph on the CURSED compiler showed that re-burning the specification allocation every loop is wasteful yet necessary for coherence, and that observed output quality degrades well before advertised context limits, around the 147k–152k mark on a 200k window. Code search via ripgrep proved non-deterministic, producing Ralph's signature failure of wrongly concluding code is missing and duplicating implementations, which is mitigated but not eliminated by explicit search-before-creating instructions and is named the Achilles' heel of the approach. Broken, non-compiling mornings are presented as a normal operating condition that Ralph cannot always rescue itself from, with compilation-error volume at one point large enough to fill the context window, worked around by having another model draft a recovery plan. Despite the mess of garbage files, temporary artefacts, and latent behaviours, the claim is that every Ralph-created problem seen so far yielded to a different series of prompts plus more loops, supporting the staffing position that senior expertise remains mandatory while a large majority of current Greenfield software engineering labour could be displaced.

## Suggestions & Future Directions

The article's practical advice is to watch the agent's output stream for repeated bad behaviours and tune the prompts at each opportunity rather than hunting for a finished prompt to copy. Operators should enforce per-change test runs, commit and push after green tests with `fix_plan.md` updated alongside the code, tag clean states starting from `0.0.0` with patch increments, and keep planning and building as separate loop modes. It recommends wiring whatever fast verification is available into the loop, adding static analysis for dynamic languages, leaving why-notes in tests and docs for future loops, keeping `AGENT.md` brief and current, and treating the TODO list as disposable by throwing it out and regenerating it whenever Ralph runs dry or derails. The stated end goal for CURSED is a self-hosting compiler with a full standard library written in the language itself as indisputable proof that AI can build a new programming language outside its training data, after which the author expects the next technique to move beyond Ralph into post-AGI territory given enough tokens.

## Authors & Institutions

The wiki material attributes the work to Geoff Huntley (writing as geoff / @GeoffreyHuntley), building the CURSED language project, with references to the Groundhog AI coding assistant and Cursor vibecoding context. No separate institutional affiliation is recorded in the wiki pages.
