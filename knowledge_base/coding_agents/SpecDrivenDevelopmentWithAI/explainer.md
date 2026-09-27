> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Spec-driven development with AI: Get started with a new open source toolkit - The GitHub BlogLinkedIn iconInstagram iconYouTube iconX iconTikTok iconTwitch icon — In Plain Language

## What is this about?

This post introduces spec-driven development: a way of building software
with an AI coding agent where you write down what you want first, in plain
words, and let the AI do most of the typing.

The star of the show is an open source toolkit called Spec Kit. You describe
your idea, and it helps turn that description into a specification, then a
technical plan, then a list of small tasks, and finally working code.

Think of it like building a house. Instead of telling the builders "just
start laying bricks," you first agree on the blueprint, the materials, and
the order of work. The AI is the construction crew; you are the architect
who checks the blueprint before anyone pours concrete.

The big shift is this: the specification is no longer a document you write
once and forget. It becomes the living center of the project — the shared
source of truth that the AI keeps reading while it works.

## Why does it matter?

Anyone who has asked an AI to "build my app" has seen what happens without
a spec: you get a giant dump of code that almost works, is hard to review,
and misses the edge cases you actually care about.

Spec-driven development fixes that by forcing clarity up front. When you
write down who the software is for, what problem it solves, and what success
looks like, the AI has something solid to aim at instead of guessing.

It also changes your job for the better. You spend less time writing
boilerplate and more time thinking: is this really what I want? Did the AI
miss a constraint, like an old system it must connect to or a privacy rule
it must follow? Catching those mistakes on paper is cheap; catching them in
a thousand lines of generated code is painful.

In short, it makes AI-generated code more reliable, more reviewable, and
easier to change later — because there is always a spec to return to when
something stops making sense.

## How does it work?

The process has four phases, and you check the AI's work before moving from
one phase to the next.

**1. Specify — describe the what and why.** You give a high-level idea: who
uses this, what problem it solves, how people interact with it, and what a
good outcome looks like. The agent turns that into a detailed spec of user
journeys and success criteria. No talk of tech stacks yet — just the goal.

**2. Plan — decide the technical how.** You add your constraints: the stack
you want, the architecture, company standards, legacy systems, compliance
rules, performance targets. The agent writes a full technical plan around
those constraints. You can even ask for several plan variations to compare,
or feed it your internal docs so it follows house patterns.

**3. Tasks — break it into small chunks.** The agent combines the spec and
the plan into a list of small, isolated tasks. Instead of "build
authentication," you get items like "create a registration endpoint that
rejects badly formatted emails." Each task is small enough to build and test
on its own, which gives the agent a tight test-and-check loop.

**4. Implement — build task by task.** The agent works through the list, one
task at a time or several in parallel. Because it already knows the what
(spec), the how (plan), and the order (tasks), each change is small and
focused instead of one overwhelming code dump.

Your role at every checkpoint is to steer and verify. Read what the AI
produced, ask "does this capture what I actually want?" and "what edge cases
did it miss?", then correct course before moving on. As the post puts it,
the AI generates the artifacts — you make sure they are right.

In practice you steer with simple commands: you initialize a project, then
run one command for the spec, one for the plan, and one for the task list,
and the agent implements from there. Named assistants that work with this
flow include GitHub Copilot, Claude Code, and Gemini CLI.

## Where can this be used?

This approach fits anywhere you would otherwise hand a big, fuzzy request to
an AI and hope for the best.

A few examples: starting a brand-new project or feature where the shape is
still unclear; adding to an existing codebase with strict standards, legacy
integrations, or compliance rules the AI must respect; teams that want every
AI change to be small and reviewable rather than one giant pull request; and
situations where requirements keep evolving, since the living spec gives you
one place to update and re-derive the plan and tasks.

It is less useful for throwaway experiments where speed matters more than
correctness — if you just want a quick sketch, writing a full spec first is
overkill.

Note: the page this explainer is based on also linked to related posts (for
example, a podcast episode and a Copilot-to-Rust migration story), but those
were just teasers and newsletter boilerplate, not part of this method.

## Conclusions & takeaways

- Put the spec first. A clear, living specification beats a clever prompt:
  it is what the AI builds from, checks against, and updates as you learn.
- Keep the four phases in order — Specify, Plan, Tasks, Implement — and do
  not skip the checkpoints. Validating each step is what prevents big,
  expensive mistakes later.
- Describe outcomes before technology. Nail down users, journeys, and
  success criteria before you argue about stacks and frameworks.
- Break work into small, testable chunks. Small tasks mean small diffs,
  easier reviews, and an agent that can check its own work as it goes.
- Remember your job: steer and verify. The agent writes the bulk of the
  material, but you own the judgment — spot the gaps, name the edge cases,
  and insist on fixes before moving forward.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Spec-driven development | Building software by writing a clear spec first and letting the AI generate code from it, instead of prompting for code directly. |
| Spec Kit | The free, open source toolkit from the post that guides you through the Specify → Plan → Tasks → Implement flow. |
| Specification (spec) | A written description of what the software should do and why, including users, journeys, and success criteria. |
| Living artifact | A document that stays active and gets updated as the project grows, rather than being filed away and forgotten. |
| Technical plan | The "how" behind the spec: stack, architecture, constraints, and standards the implementation must follow. |
| Task breakdown | Splitting the spec and plan into small, isolated jobs that can each be built and tested on their own. |
| Checkpoint / validation | A pause between phases where you review the AI's output and fix problems before letting it continue. |
| Steer and verify | Your role in the loop: guide the AI with inputs and check every artifact for gaps and mistakes. |
| Coding agent | An AI assistant (like Copilot, Claude Code, or Gemini CLI) that writes and edits code from your instructions. |
| Testable chunk | A task small enough that you (or the agent) can confirm it works in isolation before moving on. |
