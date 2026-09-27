> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Give your agent a laboratory — In Plain Language

Imagine you hire a cook but lock them out of the kitchen: no tasting, no smelling, no timer. They have to ask you "is this done yet?" every two minutes. That is what most people do to AI coding assistants. This piece says: stop writing cleverer instructions, and instead build the cook a kitchen — a small setup where the assistant can see, measure, and check its own work.

## What is this about?

- The quality of an AI coding assistant depends mostly on its feedback loop, not on the exact words in your request.
- A "laboratory" is any setup that lets the assistant view and verify what it just did, without asking you to check manually.
- Vague requests like "make it faster" or "clean up the code" usually fail: the assistant does a little work, asks you to confirm, or fixes one thing while quietly breaking another.
- The fix: before any real work starts, set up tools and steps so the assistant can measure a baseline, try changes, and compare results by itself.
- Two worked examples show the pattern: one for speeding up slow software, one for matching a design mockup pixel by pixel.
- The core rule is simple: if the assistant ever asks you to do something by hand, stop and figure out how to give it the tool to do that step itself.
- Over time, prompting skill becomes less about long wordy requests and more about knowing how much checking-setup each kind of job needs.

## Why does it matter?

- It flips the focus from prompt wording to working conditions. A mediocre instruction plus a good checking setup beats a brilliant instruction with no way to check.
- It removes you as the bottleneck. Every time the assistant asks "can you run this / look at this / tell me if this looks right?", that is a signal something is missing from its setup.
- It makes results trustworthy. Numbers (timings, test results, screenshots) replace opinions about whether something got "better."
- It saves repeat effort. Once a checking setup works, you can save it and reuse it instead of re-explaining the process every time.
- It matches how these tools actually behave today: they work in short bursts and need tight, fast feedback to stay on track.
- It scales with model progress: as models get better you can slim the instructions down, but the checking setup keeps paying off regardless.

## How does it work?

The general recipe has four moves: set up measurement, figure out what is wrong, fix things one at a time, then write up what changed.
Think of it like a science experiment: measure first, change one variable, measure again, and only believe improvements you can see in the numbers or side-by-side pictures.

**Example A: the speed laboratory.** Say your app is slow.

1. **Set up instruments.** Build a small speed test (a benchmark script) that measures the slow parts right now. Record those numbers as the baseline.
2. **Diagnose.** Study the numbers, pick the 3–5 biggest slowdowns, and write down a guess for each one: what causes it, and what might fix it.
3. **Improve step by step.** Change one thing, re-run the speed test, and compare with the baseline. Keep it only if it is faster and nothing breaks. Save each win separately so you can undo or pick individual fixes later. Skip anything that would need a giant rewrite — just flag it.
4. **Report.** Produce a simple page with before-and-after charts showing where time went and how much was saved.

**Example B: the design-matching laboratory.** Say you have a design mockup and want the code to match it.

1. **Read the source of truth.** Pull the design file directly (using a connector tool) and study the layout, parts, and visual details before writing any code.
2. **Build a rough first draft.** Expect it to be wrong — that is normal and part of the plan.
3. **Compare and polish in a loop.** Take a screenshot of your version, put it next to the design, list every visible difference (spacing, colors, text style, corner roundness, shadows, borders, alignment, behavior on small screens), fix them one by one, and re-check each fix. Repeat until you cannot spot any differences.
4. **Ask when stuck.** If the design is unclear or impossible to build as drawn, ask the human instead of guessing.

**Make it reusable.** When a workflow like one of these works well, save it as a named reusable recipe (called a skill, command, or subagent) so the assistant can run it again later. But do not rush this: try it a few times first so you learn how much instruction each kind of job really needs.

## Where can this be used?

- **Speeding up software:** any "it feels slow" complaint becomes a measure-first project with before/after proof.
- **Bug hunts:** instead of "find the bugs," give the assistant failing tests or a reproduction script it can re-run after each fix.
- **Code cleanups:** pair a vague "simplify this" with automated checks (tests, style checks) so simplifications cannot silently break behavior.
- **Design implementation:** turning mockups into web pages, where screenshots replace human eyeballing.
- **Data or writing tasks:** anywhere the assistant can compare its output against an example, a checklist, or a scoring script.
- **Team habits:** whenever you catch yourself doing manual checking for the assistant, treat it as a to-do item to automate that check next time.
- **Learning new libraries:** pair exploration with small test scripts so the assistant can confirm its understanding instead of guessing from memory.
- **Reports and demos:** end with a visual before/after summary so other people can see the improvement without re-running everything themselves.

## Conclusions & takeaways

- Wording matters less than working conditions: give the assistant a way to check itself.
- If it asks you to do something by hand, pause and ask: "how can I give it the tool to do this itself?"
- Start every fuzzy job by building measurement first — a speed test, a screenshot loop, a test script.
- Change one thing at a time, measure, and keep only what helps.
- Match the effort to the job: small jobs need light checklists; big jobs deserve the full laboratory.
- Practice first, save templates later: get a few repetitions in before turning a workflow into a permanent reusable recipe.
- The gap between "close enough" and "correct" is where quality lives — and only a checking loop can close it.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Feedback loop | The cycle of trying something, checking the result, and adjusting — the assistant's way of tasting its own cooking. |
| Laboratory | A small setup of tools and steps that lets the assistant measure and check its own work. |
| Benchmark / baseline | A speed test run before any changes, so later results have something to compare against. |
| Bottleneck | The slowest part of the system — the narrow bit that holds everything else up. |
| Hypothesis | An educated guess ("I think X is slow because of Y, and doing Z should help") tested one at a time. |
| Instrumentation | Adding timers, logs, or measuring tools so you can see what is actually happening. |
| MCP (connector) | A plug-in that lets the assistant use an outside tool directly, e.g. read a design file or control a browser. |
| Figma | A popular design app where designers draw what screens should look like; used here as the target picture. |
| Screenshot loop | Repeatedly photographing the assistant's output and comparing it with the target until they match. |
| Skill / command / subagent | A saved, named recipe that teaches the assistant to re-run a workflow on its own later. |
| Cherry-picking | Choosing individual saved fixes to keep while leaving others out. |
| Scaffolding | Extra instructions and structure you add around a task to keep the assistant on track. |
