> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Start with a clear plan (specs before code)

**In one sentence:** Before any code generation, iteratively brainstorm a comprehensive spec.md with the LLM and refine an AI-generated bite-sized project plan, then implement it one small tested chunk at a time to keep human and model aligned and avoid wasted cycles.

## Key points

- Don't dive into codegen on a vague prompt; first define the problem and plan the solution with the AI, treating the LLM as a pair programmer needing clear direction, context, and oversight rather than autonomous judgment.
- Describe the idea and ask the LLM to iteratively ask questions until requirements and edge cases are fleshed out, then compile a comprehensive spec.md containing requirements, architecture decisions, data models, and testing strategy.
- Feed the spec into a reasoning-capable model to generate a project plan of logical, bite-sized tasks or milestones (a mini "design doc"), iterating and asking the AI to critique or refine it until coherent and complete before coding.
- Upfront planning pays off enormously: as Les Orchard put it, it's like doing a "waterfall in 15 minutes" — a rapid structured phase that makes subsequent coding much smoother and forces human and AI onto the same page.
- Implement one focused piece at a time (e.g. prompt "Okay, let's implement Step 1 from the plan", test it, then move to Step 2), since LLMs do best on contained tasks and large monolithic requests produce confusion or a "jumbled mess".
- Asking for huge swaths of an app at once yields inconsistency and duplication — "like 10 devs worked on it without talking to each other" — so stop, back up, and split the problem, carrying forward built context incrementally, which also fits test-driven development (tests generated per piece).
- Use a structured "prompt plan" file with a sequence of per-task prompts (executable one by one by tools like Cursor) to enforce small loops, reduce catastrophic errors, and allow quick course-correction.

---

## Start with a clear plan (specs before code)

Don't just throw wishes at the LLM — begin by defining the problem and planning a solution, since diving straight into code generation with a vague prompt is a common mistake. The workflow is: brainstorm a detailed specification with the AI, outline a step-by-step plan, and only then write code. Concretely, describe the idea and have the LLM iteratively ask questions until requirements and edge cases are fleshed out, compiling the result into a comprehensive spec.md with requirements, architecture decisions, data models, and even a testing strategy. Next, feed that spec into a reasoning-capable model to break implementation into logical, bite-sized tasks or milestones — essentially a mini "design doc" or project plan — and iterate on it, including asking the AI to critique or refine it, until coherent and complete. Verbatim payoff quote from Les Orchard: it's like doing a "waterfall in 15 minutes". Context from the chunk's intro: at Anthropic, engineers adopted Claude Code so heavily that today "~90% of the code for Claude Code is written by Claude Code itself", yet LLM programming is "difficult and unintuitive" and requires critical thinking plus clear direction, context, and oversight.

## Break work into small, iterative chunks

Scope management is everything: feed the LLM manageable tasks, not the whole codebase at once. After planning, prompt the codegen model with something like "Okay, let's implement Step 1 from the plan" — code it, test it, then move to Step 2, each chunk small enough to fit context and stay understandable. Asking for too much in one go risks confusion or a "jumbled mess" that is hard to untangle; developers report huge single-shot generations produced inconsistency and duplication — "like 10 devs worked on it without talking to each other". The fix is to stop, back up, and split into smaller pieces, carrying forward built context incrementally. This pairs with test-driven development (write or generate tests for each piece as you go) and with tooling such as a structured "prompt plan" file containing a sequence of prompts per task for tools like Cursor to execute one by one. The principle: avoid huge leaps, iterate in small loops to reduce catastrophic errors and course-correct quickly, exploiting the LLM's strength at quick, contained tasks.

**Covers:** Spec-first planning and breaking work into small iterative chunks
