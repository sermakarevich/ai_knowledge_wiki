> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Spec-Driven Development with Coding Agents - DeepLearning.AI — In Plain Language

This is a plain-language guide to a short DeepLearning.AI course,
built with JetBrains and taught by Paul Everitt, a Developer Advocate there.
It is a beginner course of about 1 hour 16 minutes, with 15 video lessons.
You only need basic familiarity with a programming language
and some experience with AI coding tools to follow it.

## What is this about?

Imagine you ask an AI coding assistant to "build me a login page"
and it quickly writes lots of code — but the code does something
different from what you actually wanted.
That fast, loose style has a nickname: "vibe coding".
It feels productive, but the result often drifts away from your intent.

This course teaches the opposite habit: spec-driven development.
Before the AI writes any code, you write down a clear description
— called a "spec" — of what you want built.
The spec is just a markdown text file, the same simple format
used for notes and documentation.
The coding agent then reads that spec and implements it.

The course walks you through this on a small practice project.
You start by writing a "project constitution": a short document
covering the mission of the project, the tech stack you will use,
and the roadmap of what to build.
Then you write a spec for your first feature, build it,
check the result, replan, build a second feature,
and end up with a small working product (an MVP).
It also shows how to bring the same habit
to an older, existing codebase, and how to package
your personal workflow so you can reuse it.

## Why does it matter?

AI coding agents are fast, but speed is not the same as accuracy.
When you only chat with the agent in short back-and-forth messages,
important details live only in your head or in the chat history.
When the chat ends or a new session starts, that context is lost,
and the agent starts guessing — that is when the code stops
matching what you asked for.

A written spec fixes this by moving your intent out of your head
and into a file the agent can re-read every time.
Three practical benefits follow from that:

- Fewer misunderstandings: the agent has a stable reference
  for what "done" looks like, instead of piecing it together
  from scattered chat messages.
- Memory across sessions: each new agent session can pick up
  the constitution and the specs and continue where the last one stopped.
- Less mental burden: you no longer have to hold every decision
  in your head or re-explain the project each time —
  the documents carry that weight for you.

In short, the course argues that detailed specs produce software
that is closer to what you meant and easier to maintain,
while keeping you in control of complex projects.

## How does it work?

The course teaches one repeatable loop with three steps:
plan, implement, verify. You use it for every feature.

Step 1 — Plan. You and the agent discuss the feature
and write (or refine) its spec in small iterative rounds.
You check the plan before any code is written,
so mistakes are cheap to fix while they are still just words.

Step 2 — Implement. The agent writes the code,
using the spec as its guide.
Your job shifts from typing code to steering:
pointing the agent at the spec and keeping it on track.

Step 3 — Verify. You check what was built against the spec,
with yourself in the loop — reviewing, testing, asking for fixes.
Nothing is accepted blindly; the human confirms each feature is done.

Around that loop sit three supporting habits the course demonstrates:

1. Start with a constitution. Collaborate with the agent to write down
   the mission, tech stack, and roadmap first, so every later feature
   has shared ground rules to build on.
2. Replan between features. After the first feature is validated,
   update the plan, then build the second feature the same way —
   feature by feature until you reach a minimum viable product.
3. Reuse your workflow. At the end, you package the way you like
   to work into a portable "agent skill" — a reusable recipe
   you can carry across different agents and editors.

For older projects, the order is flipped: instead of starting blank,
you use the existing documentation to generate the first specs,
and then join the same plan-implement-verify loop from there.

## Where can this be used?

- Starting a brand-new side project or prototype with an AI assistant,
  where you want the first version to actually match your idea.
- Building a second and third feature on top of the first,
  without losing track of earlier decisions.
- Taking over or improving an older codebase:
  generating specs from existing docs gives the agent
  something solid to work from instead of guesswork.
- Working across tools: because the spec and the workflow
  are plain files, you can carry them from one agent or editor to another
  rather than starting over each time.
- Learning a disciplined team habit: writing things down explicitly
  is the same skill that helps human teammates stay aligned,
  not just AI ones.

The prerequisite is modest — basic coding familiarity plus some
experience with AI coding tools — so the habit is aimed at everyday
developers, not just specialists.

## Conclusions & takeaways

- Write it down first: a short markdown spec beats a long chat thread
  when it comes to getting what you asked for from an AI agent.
- Keep the human in charge: plan carefully, let the agent implement,
  then verify every result yourself before moving on.
- Ground each project in a constitution — mission, tech stack, roadmap —
  so context survives from one agent session to the next.
- Build feature by feature, replanning as you go;
  small validated steps compound into a working MVP.
- Old code is not excluded: existing docs can seed the first specs.
- Make the discipline portable by saving your workflow as a reusable skill.

The big picture: vibe coding optimizes for speed, spec-driven development
optimizes for staying aligned with your intent — and alignment is what
makes AI-written code actually usable.

## Jargon decoder

| Term | What it really means |
|---|---|
| Spec-driven development (SDD) | Writing a clear description of what to build first, then letting the AI implement exactly that. |
| Vibe coding | Chatting loosely with the AI and accepting fast code without a written plan — quick but often off-target. |
| Spec | A markdown file describing one feature: what it should do and what "finished" looks like. |
| Project constitution | A short founding document for the project: its mission, tech stack, and roadmap. |
| Plan-implement-verify | The course's three-step loop: agree on the plan, build it, then check the result. |
| Human-in-the-loop | The rule that a person reviews and approves each step instead of letting the AI run alone. |
| Intent fidelity | How closely the built code matches what you actually meant — the thing specs protect. |
| Cognitive debt | The confusion and rework that pile up when decisions live only in your head or in lost chats. |
| Greenfield codebase | A brand-new project started from a blank slate. |
| Legacy codebase | An older, existing project you now want to improve or extend. |
| MVP (minimum viable product) | The smallest working version that proves the idea — here, reached after two planned features. |
| Agent skill | Your personal workflow saved as a reusable, portable recipe for AI agents and editors. |
