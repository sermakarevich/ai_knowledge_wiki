> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# An Empirical Study on the Code Refactoring Capability of Large Language Models — In Plain Language

## What is this about?

Imagine hiring a very fast junior programmer to tidy up messy code — then checking whether a senior developer still does it better. That is what this study does.

The researchers took an AI coding model called StarCoder2 and asked it to refactor (clean up without changing what the code does) Java code from 30 open-source projects. They then compared the AI's cleanups against cleanups human developers had actually made to the same code.

Three questions drove the work: does the AI or the human produce cleaner code, what kinds of messes is each one better at fixing, and can better instructions (prompting) make the AI's cleanups safer and more effective?

To keep the test fair, they picked projects the model had never seen during training, used only commits that were pure cleanups (no new features mixed in), and judged every result the same way: fewer known bad patterns ("code smells"), better structural measurements, and whether the existing tests still pass.

A few details behind the fair setup are worth knowing. The model, StarCoder2, was chosen partly because its training data is public, so the team could deliberately select projects outside it and avoid the AI simply remembering answers. Each test focused on a single file's worth of cleanup per commit, fed to the model on a powerful GPU. And when the AI produced several candidate cleanups, the team kept the best one — the one removing the most bad patterns — mirroring how a developer would pick their strongest attempt.

## Why does it matter?

Cleaning up code eats a large share of every development team's time. Done well, it makes software easier to understand, safer to change, and cheaper to maintain. Done badly, it breaks things.

This study matters because it replaces hype with numbers. It shows exactly where today's AI genuinely helps with cleanup — and where it still falls short of a human. That lets teams decide which cleanup jobs to hand to the AI, which to keep with developers, and how much checking AI output needs.

It also matters for tool builders: the finding that showing the model just one good example sharply improves its results is a cheap, practical recipe for better AI refactoring assistants.

Concretely, the payoff shows up in four places:

- **Time savings.** Routine tidying that developers postpone for lack of time can be drafted by the AI in seconds.
- **Safer delegation.** Knowing the AI wins on pattern-based messes but loses on architecture tells teams exactly where human review must be strictest.
- **Better benchmarks.** Future AI coding tools can reuse this head-to-head method — same code, same scoring — to prove they really improved.
- **Realistic expectations.** The test-pass gap (57% vs 100%) is a vivid reminder that AI cleanup is a draft, not a done deal.

## How does it work?

The setup is a head-to-head contest on identical starting code:

1. **Collect the before-and-after pairs.** From each project the team gathered commits where developers only refactored — about 5,194 in total — and saved the code from before and after each cleanup.
2. **Ask the AI to clean the "before" code.** StarCoder2 received the original messy snippet and a short instruction to refactor it, with no hints about what the human did.
3. **Score all three versions.** Each version — original, human cleanup, AI cleanup — was checked three ways: a smell detector counted remaining bad patterns, a structural analyzer measured complexity and modularity, and the project's own unit tests verified nothing broke.
4. **Compare with statistics, not vibes.** Gaps were tested for significance, so "the AI wins here" means a real, repeatable difference rather than noise.

The headline scores: the AI's cleanups removed about 44% of bad patterns versus about 24% for humans, and improved structural measurements slightly more on average (roughly 19% vs 17%). The catch: only about 57% of the AI's cleanups passed all tests even when it got five tries, while the humans' passed essentially 100% of the time.

The team then split the wins by category. The AI dominated routine, pattern-based messes — overlong statements, magic numbers (unexplained constants), empty error handlers, overlong names — winning 10 of 16 smell types. Humans won the architecture-heavy ones: broken modularization, weak encapsulation, and classes trying to do too many jobs at once.

Finally, they tested better instructions. Showing the model one example cleanup ("one-shot") lifted test success from about 28% to 35% and smell removal by roughly 3.5 points. Asking it to explain its reasoning step by step ("chain-of-thought") helped nearly as much and unlocked seven new cleanup styles it had never attempted unprompted. Generating five candidate cleanups per snippet and keeping the best also beat generating just one.

## Where can this be used?

- **Everyday code cleanup bots.** Let the AI handle the boring, repetitive tidying — renaming, simplifying long statements, replacing magic numbers, removing dead abstractions — then have a human review and run the tests.
- **Code review assistants.** Flag pattern-based smells automatically and suggest a concrete fix before a human reviewer looks at the deeper design issues.
- **Legacy code triage.** Scan an old codebase for the smell types the AI fixes reliably, and route the architecture-level problems (modularization, encapsulation) to senior developers.
- **Prompt templates for AI tools.** Always include at least one good before-and-after example in the instruction, and generate several candidate cleanups instead of one — both are low-cost wins this study validates.
- **Training and onboarding.** Show new developers side-by-side AI vs human cleanups to teach which refactorings are mechanical and which demand whole-system thinking.
- **CI quality gates.** Add smell-count checks to continuous integration so AI-generated cleanups must measurably reduce bad patterns before merging.
- **Research reuse.** The leakage-controlled project selection is a template any team can copy when evaluating a new model fairly.

## Conclusions & takeaways

- AI refactoring is already strong at the routine work: it removes far more surface-level bad patterns than developers do on the same code.
- Humans still own the deep work: design, architecture, and dependency reasoning remain developer territory.
- AI output cannot be trusted blindly: with barely half of cleanups passing tests, every AI refactoring needs automated tests plus human review.
- Small process tweaks pay off: one example in the prompt and multiple candidate generations produce the best results.
- The winning formula is partnership, not replacement: use the AI for fast, systematic tidying and developers for structural judgment.
- Caveats apply: results come from one model and Java open-source projects, so treat them as strong evidence, not a universal guarantee.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Refactoring | Tidying code so it is easier to read and change, without altering what it does. |
| Code smell | A recognizable bad pattern (e.g., a giant method, an unexplained number) hinting the code needs cleanup. |
| Implementation smell | A surface-level mess inside one piece of code, usually fixable with a simple rule. |
| Design smell | A deeper structural problem in how classes and modules are organized. |
| Cohesion | How well the parts of one class belong together; higher is better. |
| Coupling | How tangled classes are with each other; lower is better. |
| Cyclomatic complexity | A count of how many decision paths run through code; lower means easier to follow and test. |
| Unit test pass rate | The share of cleanups that still pass the project's automated checks — a safety score. |
| Zero-shot / one-shot prompting | Asking the AI with no examples (zero-shot) versus showing it one example first (one-shot). |
| Chain-of-thought prompting | Asking the AI to reason step by step before answering, which improves harder tasks. |
| Data leakage | When a model is tested on code it already saw in training, inflating its score; this study avoids it by design. |
| Effect size | A number saying how big a measured difference is in practice, not just whether it is real. |
