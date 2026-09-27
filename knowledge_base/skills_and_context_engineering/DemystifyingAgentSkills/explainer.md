> [[index|Wiki]] | [[summary|Summary]]

# Demystifying Agent Skills: Why They Work-Until They Don't — In Plain Language

## What is this about?

Imagine hiring a new employee for a repetitive job — say, setting up a server. The first time, they fumble around, hit dead ends, and eventually succeed after a lot of trial and error. You could hand the next new hire either (a) a full diary of everything the first person did, mistakes and all, or (b) a clean one-page cheat-sheet distilled from that diary: "run these three commands in this order, watch out for this specific gotcha, verify with this command." Option (b) is what AI researchers call a "skill" for an AI coding agent — a short, standardized instruction file (called `SKILL.md`) that an AI reads before starting a task, distilled from its own or another agent's past attempts.

Everyone assumed cheat-sheets like this help, and they usually do. But nobody had carefully asked *why* they help, or when they quietly stop helping. This paper runs a scientific experiment: it takes the exact same raw diary of past attempts and gives it to an AI agent three different ways — as nothing at all, as the raw diary, or as the distilled cheat-sheet — then watches, blow-by-blow, what actually changes in how the AI behaves.

## Why does it matter?

AI coding assistants (and increasingly, AI agents doing all kinds of multi-step work) are being asked to get better over time by learning from their own history, instead of being retrained from scratch. Skills are the leading way people are packaging that learned experience today. If we don't understand *why* skills work, we're stuck writing and fixing them by trial and error — tweaking a skill file, seeing if scores go up, and not knowing if it will keep working on the next task or the next hundred cheat-sheets in a growing library. This paper gives a principled, mechanism-level explanation instead of guesswork, and flags a specific, measurable failure mode (retrieval breaking down as your skill library grows) that anyone building such a system needs to plan for.

## How does it work?

Think of the researchers as running a controlled science experiment, not just a benchmark leaderboard entry.

1. **Collect a diary.** For each task, they let an AI agent try it many times, keeping both the successful attempts and the failed ones — this is the raw "diary."
2. **Make two different cheat-sheets from the same diary.** One is "Workflow Memory" — a cleaned-up version of the raw diary, still close to the original blow-by-blow record. The other is a "Skill" — a fully distilled, standardized cheat-sheet (the `SKILL.md` file).
3. **Run the same task three ways: with nothing, with the diary, with the cheat-sheet.** Because both cheat-sheet versions come from the exact same diary entries, any difference in outcome must come from *how the information is packaged*, not from having more information.
4. **Have a judge read the transcripts, not just the score.** Instead of only checking "did it pass or fail," an AI judge reads what actually happened step by step and assigns it to one of 12 specific behavior categories — for example, "the agent set up its environment correctly" vs. "the agent got the algorithm wrong" vs. "the agent misapplied the cheat-sheet's advice." This is like a coach reviewing game tape instead of just the final score.
5. **Separately, stress-test "finding the right cheat-sheet."** In a library of 5 cheat-sheets, an AI can usually pick the right one. In a library of 100 — some of which look confusingly similar to the right one — it gets much worse at picking correctly. The researchers measure this directly, and separately from whether the task still gets done.

The headline result: the distilled cheat-sheet (Skill) wins mainly because it keeps the AI's *actions* on track — the right setup steps, the right order, the right checks — not because it teaches the AI new facts it didn't already know. But the same distillation that makes a cheat-sheet clean and short also makes it something the AI can misread or apply rigidly to the wrong situation — a brand-new kind of mistake that didn't exist before cheat-sheets were introduced.

## Where can this be used?

- **AI coding agents and DevOps automation**: any system (like Claude Code, Codex, or similar coding assistants) that reuses "how we solved this before" documentation as a skill or playbook.
- **Any agent with a growing library of reusable procedures**: customer-support bots with a knowledge base of "how to handle X," data-analysis agents with reusable query templates, or any RAG-style system where "the right document to retrieve" grows over time.
- **Skill-marketplace or skill-sharing platforms**: understanding that retrieval, not skill quality, may be the actual bottleneck as a library scales past a few dozen entries.
- **Any team designing "let the agent learn from experience" systems**: the paper's taxonomy (why a skill helped/failed) is a template for building your own diagnostic dashboard instead of just tracking pass/fail rates.

## Conclusions & takeaways

- A cheat-sheet works mainly by keeping actions consistent (procedural anchoring), not by teaching new facts — so don't expect a skill to fix an agent that fundamentally doesn't understand the problem.
- Skills relocate failure, they don't eliminate it: fewer "broke the environment" failures, but a new "misapplied or ignored the cheat-sheet" failure mode appears.
- As your skill library grows, the AI's ability to fetch the *exact right* cheat-sheet collapses fast — especially when several cheat-sheets look alike — but this often matters less for task completion than you'd expect, because a "close enough" cheat-sheet can still help.
- A month from now, remember this trade-off: skills give you more successes and fewer setup failures, at the cost of a new invocation-mistake class and a retrieval problem that gets worse, not better, as your library grows.
- Honest limitation: this was tested on terminal- and coding-style tasks specifically — it may not generalize to, say, long open-ended web browsing or negotiation-style agent tasks.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Skill | A short, standardized instruction file (e.g. `SKILL.md`) an AI agent reads before a task, distilled from past experience — like a cheat-sheet, not a diary |
| Workflow Memory | A cleaned-up but still detailed record of what happened in a past attempt — closer to a diary than a cheat-sheet |
| Procedural anchoring | A skill's main way of helping: keeping the AI's actions (steps, order, checks) consistent and correct, rather than teaching it new facts |
| Knowledge injection | The alternative way a skill *could* help: by telling the AI something it didn't already know — measured here as rare (4.5% of cases) |
| Trajectory | The full step-by-step record of everything an AI agent did during one attempt at a task |
| Skill-use Category (SC) | One of three top-level buckets the researchers sort every trajectory into: SC1 (it worked), SC2 (it broke during execution/verification), SC3 (guidance existed but was misused or blocked) |
| Open coding | A qualitative-research method: reading examples with no pre-set categories and inventing labels from what you actually see, before organizing them into a formal system |
| Hit@1 / top-1 precision | Out of the AI's top guess for "which cheat-sheet is the right one," the percentage of the time that guess is actually correct |
| Retrieval precision | Out of all the cheat-sheets the AI actually consulted or used, the fraction that were the genuinely correct one for the task |
| SKILL.md | The literal file format/name convention for a distilled skill artifact used in this research ecosystem (introduced by Anthropic) |
| Oracle-status success rate | Task success measured against the benchmark's official pass/fail verifier, not the agent's own self-assessment |
| Distractor | A decoy cheat-sheet included in a test library specifically to see if the AI can avoid picking the wrong one |
