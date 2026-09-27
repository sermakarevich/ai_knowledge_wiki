> [[index|Wiki]] | [[summary|Summary]]

# Agent Skills Can Be Harmful — In Plain Language

## What is this about?

Picture an AI coding agent — a computer program that reads instructions written in plain English and then does the work itself: it explores a code project, writes and edits files, runs tests, and decides when the job is finished. Think of it as a new employee who can actually type the code, not just talk about it.

Now imagine handing that new employee a laminated "how-to card" before they start a task — a short cheat sheet titled something like "How to build a data-processing pipeline" or "How to add a search feature." In AI-agent land, this card is called a **skill** (usually a file named `SKILL.md`). It's meant to save time: instead of the agent figuring everything out from scratch, it gets pre-written steps, example code, checklists, and tips, written once by someone with experience and reused across many similar jobs.

Cheat sheets are usually helpful. But a cheat sheet written for "a typical version of this task" isn't guaranteed to fit the exact job in front of you today. Maybe the example on the card uses a slightly different file location, or it shows only some of the settings you actually need, or it insists on double-checking everything ten times when the task is trivial. This paper asks a simple but important question: when do these how-to cards quietly make the AI agent's work *worse* — either causing it to fail the task outright, or causing it to take much longer and cost much more money to finish — even when the card looked perfectly relevant on the surface?

## Why does it matter?

Companies are increasingly building marketplaces and shared libraries of these skill cards, the same way people share app plugins or recipe cards, so that AI agents don't have to relearn common tasks every time. If a shared skill silently steers the agent toward the wrong file path, an incomplete feature, or a bloated series of unnecessary checks, everyone who reuses that skill inherits the same problem — and it's hard to notice, because the agent still looks busy and confident while doing the wrong thing.

For anyone who builds, sells, or simply uses these AI coding assistants with plugin-like skill libraries, this matters in concrete ways: it tells you where to look when a "helpful" skill quietly breaks tasks or burns through budget, and it gives skill authors a checklist of common mistakes to avoid before publishing a skill for others to use.

## How does it work?

The researchers needed a way to prove that a specific skill — not bad luck, not a weak underlying AI model, not an unusually hard task — was the actual cause of a problem. Their method is essentially a controlled experiment, run twice:

1. **Run the same task twice, changing only the skill.** Everything else stays identical: the same task instructions, the same starting code, the same AI model, the same "grader" program (called a **verifier**) that checks whether the final result is correct. In one run (the "**target run**," the one being investigated) the agent uses the skill under suspicion. In the other run (the "**reference run**," acting like a stand-in answer key) the agent either gets no skill at all, or a different skill that covers a similar topic.
2. **Compare the two outcomes.** Because only the skill changed, any difference in the result can be blamed on the skill — this comparison approach is borrowed from a software-testing technique called **differential testing**, where you run two versions of something side by side and treat any difference as a clue.
3. **Only call it a "skill-induced failure" if the comparison proves harm.** Two kinds of harm are counted:
   - **The task straight-up fails.** The version *with* the skill fails the grader, while the reference version (no skill, or a different skill) passes. This is called a **functional failure** — the skill actively broke something that would otherwise have worked.
   - **It works, but costs way more.** Both versions pass the grader, but the skill-guided version uses far more **tokens** (tokens are the small chunks of text an AI model reads and writes — more tokens roughly means more computing cost and more money) or takes much longer to finish. The paper calls this an **efficiency regression**, and only counts it when the cost roughly doubles or more, to rule out ordinary day-to-day noise.

Using this method across two existing test collections (one with 84 varied tasks — cooking, finance, healthcare-style problems — and one with 490 real software-engineering tasks), and pulling in real skill cards shared online, the researchers ran thousands of these paired comparisons. After filtering out weak or ambiguous cases, they confirmed 307 genuine skill-caused problems: 125 outright failures and 182 costly-but-passing runs. They then read through the step-by-step "trajectory" (the agent's full sequence of actions — what it read, what it typed, what commands it ran) for each case to work out *why* it went wrong, and organized the reasons into a small set of repeatable categories (a **taxonomy**).

They also built a follow-up tool, **SkillTriage**, that automates this "why did it go wrong" diagnosis using another AI model, so that future teams don't have to manually re-read every trajectory by hand.

## Where can this be used?

- **Vetting a skill or plugin marketplace.** Before publishing a shared skill card, run it through this before/after comparison on a handful of representative tasks to see if it ever makes things fail or balloon in cost.
- **Code review for AI-agent instruction files.** When someone submits a new `SKILL.md`-style file, reviewers can specifically check for the failure patterns this paper found most common: does the card confuse its own examples for hard requirements? Does it specify the wrong file location? Does it demand excessive re-checking?
- **Cost auditing of AI coding assistants.** Teams paying for AI-agent usage can use the token/time comparison idea to spot which loaded skills are quietly driving up bills without improving results.
- **Designing better skill-authoring guidelines.** The paper's findings translate directly into house rules for writing skills: keep the always-loaded text short, separate "this is just an example" from "this is a strict requirement," and don't demand more verification than the task actually needs.

## Conclusions & takeaways

The single most important finding: skills essentially never fail because they're the wrong topic for the job — that happened in only 2 of 125 failure cases. Instead, skills fail because they mislead the agent on the *details* of an on-topic task: filling in a required piece incorrectly, leaving a required piece out entirely, quietly changing the working setup so the final check doesn't match what was actually graded, or writing the result to the wrong location. And when a skill wastes money rather than causing outright failure, the main cause usually isn't a bloated wall of instruction text — it's the skill talking the agent into extra, unnecessary work, especially excessive double-checking after the job is already done.

The practical message for a month from now: treat "load this skill" as a decision with a real cost and a real risk of breaking things, not as a free bonus. Before trusting a shared skill card, ask whether its examples might be mistaken for requirements, whether it assumes a setup that might not match yours, and whether it insists on more verification than the task warrants.

Honest limits: the evidence comes from two specific benchmarks, one agent framework (OpenCode), and one AI model (Claude Opus 4.6), plus skills pulled from two particular skill-sharing websites. The authors themselves note that some patterns might be specific to this setup and may not carry over perfectly to other AI models, other agent tools, or other skill libraries. Also, deciding "why" something failed still involves human judgment calls, even though the team tried to reduce bias through group agreement and a second independent automated check.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| LLM agent | An AI program (built on a large language model) that doesn't just chat — it can act: browsing files, running commands, editing code, and deciding when a task is done. |
| Agent skill / SKILL.md | A reusable "how-to card" of written instructions, examples, and checklists that gets loaded into the agent's context to guide it on a specific kind of task. |
| Verifier | An automated grader — a program that checks whether the agent's finished work is actually correct (pass or fail), instead of a human judging it. |
| Token | A small chunk of text (roughly a word-piece) that an AI model reads or writes; more tokens used means more computing cost. |
| Differential testing | A comparison technique: run two versions of the same thing side by side and treat any difference in outcome as evidence about what caused it. |
| Target run / reference run | The "target run" is the run being investigated (with the skill in question); the "reference run" is the comparison run (no skill, or a different skill) used as a stand-in answer key. |
| Functional failure | A case where the skill-guided run fails the grader while the comparison run passes — the skill broke something that otherwise would have worked. |
| Efficiency regression | A case where both runs pass, but the skill-guided run costs far more time or tokens (here, roughly double or more) than the comparison run. |
| Trajectory | The full, step-by-step record of everything the agent did during a run — what it read, typed, ran, and decided. |
| Taxonomy | An organized set of labeled categories used to group similar causes of failure together, so patterns can be spotted and discussed consistently. |
| SkillTriage | The paper's own automated tool (built on another AI model) that reads a target/reference pair of runs and predicts which failure category applies, mimicking the human analysis. |
