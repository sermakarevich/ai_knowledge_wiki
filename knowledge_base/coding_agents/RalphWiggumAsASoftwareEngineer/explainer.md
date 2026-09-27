> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Ralph Wiggum as a "software engineer" — In Plain Language

## What is this about?

Ralph Wiggum as a "software engineer" is a technique for letting an AI coding assistant build software on its own, in loops, overnight.

The name comes from The Simpsons character Ralph Wiggum — cheerful, literal-minded, and unreliable. The joke is honest: the loop is simple and a bit clumsy, but if you supervise it well, it gets a surprising amount done.

In practice, "Ralph" means one AI agent working in one project folder, doing one small task per loop, then starting over with a fresh memory. Each loop it reads a to-do list (`fix_plan.md`) and a set of written requirements (specs), picks the most important item, implements it, runs the tests, updates the to-do list, and saves its work with git.

The example behind these notes is CURSED, a brand-new programming language and compiler. The operator set Ralph loose on it for weeks, watching its behaviour and steadily tuning the instructions.

The headline result: roughly 90% of a brand-new project built this way, under senior guidance — with the frank warning that some mornings you wake up to a codebase that no longer compiles.

## Why does it matter?

Writing code has become the cheap part. The expensive parts are deciding what to build and proving it actually works.

Ralph matters because it offers a working answer to both:

- **Deciding what to build:** instead of one giant prompt, you keep plain-written requirements (specs) plus a living to-do list. The agent reads them every loop, so it stays pointed at the right work.
- **Proving it works:** instead of trusting the AI's word, you wire in fast automatic checks — builds, tests, type checkers, scanners. Anything that fails gets rejected and becomes the next loop's work.

It also matters as a reality check. The claim here is not "AI replaces all engineers." It is narrower: for starting brand-new projects from scratch, a supervised loop like this can displace a large share of routine implementation work — but a senior person is still needed to steer, judge, and rescue it.

Anyone saying a tool does 100% of the work with no engineer involved is, in the source's words, "peddling horseshit."

## How does it work?

Think of Ralph as a diligent but forgetful worker who starts each shift with no memory. You make that work by keeping everything important written down.

**1. One loop, one job, same starting point.**

Every loop the agent gets the same pack: the to-do list (`fix_plan.md`) plus the requirements folder (`specs/`). It picks the single most important item and does only that. If it starts going off the rails, you tighten back to one item per loop.

Keep the starting pack small. The usable thinking space is around 170k tokens, and bigger packs mean worse results. Re-reading the same specs each loop is deliberately "wasteful" — it keeps the worker pointed the same way every time.

**2. The main worker schedules; helpers do the heavy lifting.**

The main agent should not burn its own thinking space reading huge test logs. Instead it acts like a scheduler: it fans out helper agents (subagents) to search code, write files, and summarise results.

One caution: only one helper at a time should run builds and tests. Hundreds of helpers all building at once creates back pressure and gridlock.

**3. Requirements first, code second.**

Before any building, you have a long conversation about what the software should do, then write that down as one file per requirement in the specs folder. Later steering is simple:

- Agent writes the wrong kind of code? Fix the shared code library (stdlib) so the right pattern is the easy one.
- Agent builds the wrong thing entirely? Fix the specs — one CURSED wording bug defined a keyword twice and wasted a month.

**4. Fast checks reject bad work.**

After every change, the agent runs the tests for just that piece of code. Type systems, builds, and scanners all count as checks. The loop must turn fast: strict languages (like Rust) catch more mistakes but build slowly and need more attempts; simpler languages need an added type checker or results become "a bonfire."

**5. Leave notes for your future forgetful self.**

Because each loop starts fresh, every test and doc must say *why* it exists, not just what it does. That note lets a future loop decide: keep it, fix it, or delete it as outdated.

**6. Fight the standard failure modes with written signs and more loops.**

- *Assuming instead of searching:* code search can be flaky, so the agent sometimes declares code "missing" and writes a duplicate. The fix is a blunt written rule: search with helpers first, never assume.
- *Placeholder shortcuts:* models love minimal stubs because "compiling code" feels like success. The fix is an equally blunt rule — full implementations only — plus extra loops that hunt TODOs and stubs and add them back to the to-do list.
- *Drifting to-do list:* a planning loop with hundreds of helpers compares the code against the specs and rebuilds the priority-sorted to-do list. Watch it "like a hawk," delete it when it rots, regenerate it.
- *Self-improvement:* the agent is allowed to update its own runbook (`AGENT.md`, how to build and run things) and log newly spotted bugs into the to-do list, even unrelated ones.

**7. Expect breakage; keep rescue discipline.**

Some mornings the project will not compile and Ralph cannot fix it. The human then judges: wipe back to the last good state (`git reset --hard`) and restart, or write a fresh set of rescue instructions. Strict habits — update the to-do list, commit, push, tag clean states starting at `0.0.0` — make either choice cheap.

## Where can this be used?

Use it for **starting new projects from nothing** — a fresh language, library, prototype, or bootstrap codebase where there is little existing code to respect.

Concretely, it fits:

- Greenfield prototypes where 90%-done fast beats perfect.
- Repetitive implementation against clear specs (standard libraries, example programs, test coverage).
- Overnight progress: queue the loop, review and re-steer in the morning.
- Teams with a senior person available to write specs, watch behaviour, tune instructions, and judge reset-versus-rescue calls.

Do not use it as described inside a large existing codebase. The source is blunt: "no way in heck" — the loop does not understand your history, conventions, and hidden constraints well enough, and will break things.

It also only works where fast automatic checks exist. No tests, no type checker, no build, no scanner — no Ralph. Set up the checking wheel first.

## Conclusions & takeaways

- There is no magic prompt to copy. The instructions only work because they were tuned by watching the agent fail. Your job is observing and tuning, not one-shot prompt writing.
- Keep the loop boring on purpose: one folder, one worker, one job per loop, same starting pack, fresh memory each time.
- Steering is upstream (fix the shared library for wrong patterns, fix the specs for the wrong thing) and enforcement is downstream (fast checks reject bad work).
- Failure is routine and handled with more loops, not fewer: search-first rules, anti-shortcut rules, regenerated to-do lists, self-updating runbooks.
- Budget for breakage and bound the scope: Greenfield bootstrapping to ~90% under senior guidance, with reset-or-rescue judgment calls and strict commit habits.
- The provocative tail: if code is cheap and checks are fast, "maintainability by humans" stops being the only frame — future loops can adapt code when needed. That idea is unproven at scale, so treat it as a bet, not a fact.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Ralph loop | One full round: read the to-do list and specs, do one job, test it, update the list, save. Then forget everything and start again. |
| Specs (specifications) | Plain-written descriptions of what the software must do, one file per topic. The source of truth the agent reads every loop. |
| fix_plan.md | The living to-do list: what is missing or broken, sorted by importance. Rebuilt often, deleted when it goes stale. |
| AGENT.md | The runbook: how to build, test, and run this project. The agent is allowed to correct it when it learns something. |
| Subagent | A helper copy of the AI spun up for one chore (search, write, summarise) so the main worker's thinking space stays clear. |
| Back pressure / fast wheel | Any automatic check (tests, builds, type checker, scanner) that rejects bad work quickly and forces another try. |
| Placeholder implementation | A fake shortcut — empty function, stub, or TODO — that looks done but does nothing real. Explicitly banned. |
| Greenfield | A brand-new project with no old code to work around. The only setting where this technique is recommended. |
| Self-hosting compiler | A compiler good enough to build itself — the end goal used for the CURSED example. |
| Context window / budget | How much text the AI can think about at once (~170k usable tokens here). Spend it sparingly or results get worse. |
