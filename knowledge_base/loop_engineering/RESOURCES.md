# Loop Engineering — Curated Resources

> **Scope (strict):** resources whose *primary subject* is **engineering the agentic loop** — the
> "stop prompting, design the loop that prompts the agent" idea: loop architecture, triggers,
> verifiable goals, **stop/exit conditions**, loop safety (YOLO + sandbox), self-correction as loop
> design, and the **Ralph loop** technique.
>
> **Deliberately excluded** (off-topic for this list): generic "what/future/state of agents",
> agent harness/scaffolding, context engineering, tool-writing, prompt engineering, model
> comparisons, and framework tutorials. Foundational loop-*pattern* papers (ReAct, Reflexion,
> Self-Refine) are also excluded as upstream/"past" — available on request.

All links verified working (June 2026). Ranked within each section by **topic centrality first, then
source reliability**.

---

## 📝 Articles & Posts

1. **The Art of Loop Engineering** — Sydney Runkle, *LangChain* (Jun 16, 2026)
   <https://www.langchain.com/blog/the-art-of-loop-engineering>
   Defines the discipline as a four-layer nested loop stack — agent loop → verification loop →
   event-driven loop → hill-climbing loop. *"give the LLM context and let it call tools in a loop
   until it's done."*

2. **Loop Engineering** — Addy Osmani, *Google Chrome* (Jun 7, 2026)
   <https://addyosmani.com/blog/loop-engineering/>
   The post that named/popularized the discipline. *"Loop engineering is replacing yourself as the
   person who prompts the agent. You design the system that does it instead."*

3. **Designing Agentic Loops** — Simon Willison (Sep 30, 2025)
   <https://simonwillison.net/2025/Sep/30/designing-agentic-loops/>
   Earliest clear treatment of loop design as *the* skill: tool/loop design, YOLO-mode safety,
   sandboxing. *"an LLM agent is something that runs tools in a loop to achieve a goal."*

4. **Ralph Wiggum as a "software engineer"** — Geoffrey Huntley (Jul 14, 2025)
   <https://ghuntley.com/ralph/>
   The originating spec of the Ralph loop: the bash-loop-as-agent — `while :; do cat PROMPT.md |
   claude-code ; done` — one task per iteration, backpressure via tests.

5. **everything is a ralph loop** — Geoffrey Huntley (Jan 17, 2026)
   <https://ghuntley.com/loop/>
   Argues the loop is the primitive unit of software development. *"Ralph works autonomously in a
   single repository as a single process that performs one task per loop."*

6. **Loop Engineering** — Cobus Greyling, *Medium* (Jun 2026)
   <https://cobusgreyling.medium.com/loop-engineering-62926dd6991c>
   Practitioner breakdown of the core mechanics (triggers, verifiable goals, guardrails); companion
   to the author's `loop-engineering` repo below.

7. **The Power of Agentic Loops — Implementing Flexbox Layout in 3 Hours** — Colin Eberhardt, *Scott Logic* (Dec 22, 2025)
   <https://blog.scottlogic.com/2025/12/22/power-of-agentic-loops.html>
   A concrete iterate-until-done case study. *"supply a reasoning LLM with a goal, provide tools to
   evaluate progress, then allow it to iterate until the goal is met."*

8. **Loop Engineering, Continued: From One Governed Loop to an Operable Fleet** — Boyu Wang, *TrueFoundry* (Jun 17, 2026)
   <https://www.truefoundry.com/blog/loop-engineering-fleet-runtime>
   Takes loop engineering into multi-loop territory: *"a collection of loops, running for a year, is
   a production system-of-systems"* — lifecycle, isolation, versioning.

9. **A Brief History of Ralph** — *HumanLayer* (2026)
   <https://www.humanlayer.dev/blog/brief-history-of-ralph>
   Traces how the Ralph loop technique emerged and evolved — focused on the loop itself, not general
   agent history.

---

## 🎥 YouTube Videos (captions available)

1. **Inventing the Ralph Wiggum Loop — w/ Geoffrey Huntley** — *Dev Interrupted #256* (Jan 2026)
   <https://www.youtube.com/watch?v=C1YNGy6qusg>
   The loop's creator on its mechanics, stop conditions, and managing context-rot inside the loop.

2. **The Ralph Wiggum Loop from 1st Principles (by the creator of Ralph)** — Geoffrey Huntley
   <https://www.youtube.com/watch?v=4Nna09dG_c0>
   Builds the loop / orchestrator pattern up from scratch.

3. **Agent Loops: Complete Guide (Claude Code + Codex)**
   <https://www.youtube.com/watch?v=RVEaDvh6f5A>
   Taxonomizes loop types with side-by-side implementations and stop conditions.

---

## 💻 GitHub Repos

1. **ghuntley/how-to-ralph-wiggum** — Geoffrey Huntley · ⭐ ~1.7k
   <https://github.com/ghuntley/how-to-ralph-wiggum>
   Canonical Ralph-loop reference: `IMPLEMENTATION_PLAN.md` as persistent state across loop
   iterations, one task per cycle, backpressure via tests.

2. **snwfdhmp/awesome-ralph** — community · ⭐ ~0.9k
   <https://github.com/snwfdhmp/awesome-ralph>
   Curated list of Ralph / agentic-loop resources — "runs AI coding agents in automated loops until
   specifications are fulfilled."

3. **ralph-loop (official Claude Code plugin)** — *Anthropic* · in `anthropics/claude-plugins-official`
   <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop>
   Implements the Ralph technique via a **Stop hook** that intercepts Claude's exit and re-loops
   until a completion promise fires. *(Installed locally — `/ralph-loop`.)*

4. **vercel-labs/ralph-loop-agent** — Vercel · ⭐ ~0.8k
   <https://github.com/vercel-labs/ralph-loop-agent>
   Wraps the AI SDK tool-call loop in an outer iteration that runs until a `verifyCompletion`
   callback passes; composable stop conditions (iterations / tokens / cost).

5. **cobusgreyling/loop-engineering** — Cobus Greyling · ⭐ ~0.6k
   <https://github.com/cobusgreyling/loop-engineering>
   Seven production loop patterns (Daily Triage, PR Babysitter, CI Sweeper…) plus CLI scaffolding
   (`loop-init` / `loop-audit` / `loop-cost`) and a safety/failure-modes doc.

---

## 🐦 Social / Origin Threads

1. **Addy Osmani — Loop Engineering thread** — *X*
   <https://x.com/addyosmani/status/2064127981161959567>

2. **Simon Willison — designing agentic loops (safely, in YOLO mode)** — *X*
   <https://x.com/simonw/status/1973046549597847714>

---

### Note on your example video

`https://youtu.be/OaRhpwz_TGM` = **"The Future of AI Agents with Andrew Ng | Interrupt"** — a broad
"future of agents" fireside, **not** specifically loop engineering. It fails the strict scope above,
so it's excluded. Say the word if you want it kept anyway.
