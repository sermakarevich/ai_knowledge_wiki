# The Power of Agentic Loops: Implementing Flexbox Layout in 3 Hours

**Article:** [The Power of Agentic Loops (Colin Eberhardt, 2025)](https://blog.scottlogic.com/2025/12/22/power-of-agentic-loops.html)
**Source:** Scott Logic Blog | **Published:** 2025-12-22 | **Reading time:** ~10 min

## Human Readable TL;DR

Imagine hiring a tireless intern who writes code, runs tests, reads the error messages, fixes the mistakes, and repeats -- all without you having to look over their shoulder. That's what Colin Eberhardt did to rebuild a notoriously tricky layout algorithm in just three hours, a job that took a seasoned developer two weeks a decade ago. The secret wasn't a smarter AI -- it was setting up the right feedback loop so the AI could check its own work and keep going until it got it right.

## TL;DR

Colin Eberhardt demonstrates that LLM-powered agents with automated feedback loops can compress multi-week algorithm implementations into hours. He implemented a ~800-line flexbox layout engine against a ~350-test suite in roughly three hours using VS Code Copilot agent mode, a browser-based reference implementation for ground-truth diffing, and a self-updating instruction file that let the agent accumulate lessons across increments. The key finding: the quality of the feedback mechanism matters more than prompt engineering.

---

## Problem & Motivation

One-shot AI code generation has a ceiling -- the model writes code, the human verifies it, the cycle repeats manually. For complex algorithms this is slow and error-prone. Eberhardt wanted to test whether an agentic loop (model + tools + automated verification + iteration) could eliminate the human-in-the-loop for a well-scoped, non-trivial implementation task. He chose flexbox as the benchmark because it is algorithmically demanding (Vjeux took two weeks in 2015) yet fully specifiable through a test suite and a reference browser implementation.

---

## Main Original Ideas

1. **Agentic loop as first-class engineering pattern** -- Supply an LLM with a goal, provide tools to evaluate progress toward that goal, then let it iterate. The loop mirrors the human software development cycle: think, write, execute, verify, repeat. The key shift is that the agent drives this cycle autonomously rather than waiting for human feedback at each step.

2. **Feedback mechanism over prompt quality** -- Eberhardt argues that for agentic systems "an effective feedback mechanism is probably more important than a well-crafted prompt." He built a CLI tool that ran the agent's output against both a JSON-driven test suite and a browser reference implementation, giving the agent a binary pass/fail signal it could act on immediately.

3. **Self-improving instructions via reflection** -- When the agent repeatedly failed tests because the test harness hadn't been updated for new flexbox properties, Eberhardt prompted it to update `copilot-instructions.md` with lessons learned after each increment. This created an evolving coaching document -- a form of persistent memory layered on top of a stateless model.

4. **Incremental problem decomposition** -- Rather than handing the agent the full flexbox spec, the task was broken into ten increments of increasing complexity. Each increment had a focused scope, reducing the search space and making the feedback loop tight enough for the agent to converge quickly.

5. **Human role shifts from coder to loop designer** -- The critical human skill is no longer writing the code but designing the conditions under which the agent can verify and improve its own output: choosing the decomposition, building the reference implementation, and deciding when autonomous iteration is safe.

---

## Key Findings

| Metric | Value |
|---|---|
| Total implementation time | ~3 hours |
| Algorithm size | ~800 lines of code |
| Test suite size | ~350 tests |
| Original human time (2015 reference) | ~2 weeks |
| Number of increments | 10 |

- The agent independently diagnosed and fixed a floating-point precision issue in increment #2, proposing "approximately equal" comparisons with a ~0.02 px tolerance to match browser sub-pixel rendering.
- In increment #3, the agent discovered the test harness was missing properties rather than that its implementation was wrong -- a non-trivial root-cause distinction.
- Debugging behaviour felt "very familiar" to human problem-solving: pursuing dead ends, backing up, trying new approaches, without explicit instruction to do so.
- After initial observation and loop tuning, the author concluded the agent ran well enough unattended that "you shouldn't sit and watch -- you should get on with something more worthwhile."

---

## Suggestions & Future Directions

1. **Legacy migration loops** -- Apply the same pattern to automated migration of codebases between frameworks or language versions, where a reference implementation and automated tests can be constructed upfront.
2. **UI automation via MCP** -- Use browser-control tools (MCP) to close the feedback loop on visual/UI tasks, removing the last manual step for front-end work.
3. **Automating human validation** -- Invest engineering effort in automating the verification step that humans currently perform manually; this is where the highest leverage lies for future agentic workflows.
4. **Honest scope assessment** -- The author cautions that flexbox had near-ideal conditions (well-documented in training data, trivially constructable reference implementation, constrained problem domain). Most real projects will require "creativity and engineering expertise" to build equivalent feedback mechanisms.

---

## Authors & Institutions

Colin Eberhardt -- Scott Logic (Technology Director)
