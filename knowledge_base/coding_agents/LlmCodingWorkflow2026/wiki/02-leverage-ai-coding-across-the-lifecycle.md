> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Leverage AI coding across the lifecycle
**In one sentence:** Use CLI and asynchronous AI coding agents in a supervised way across the SDLC — grounding them with plans/specs, verifying everything with tests and reviews, and containing their output with ultra-granular version control.
## Key points
- CLI agents (Claude Code, OpenAI Codex CLI, Google Gemini CLI) work inside the project directory, reading files, running tests, and performing multi-step fixes from chat commands.
- Asynchronous agents (Google Jules, GitHub Copilot Agent) clone the repo into a cloud VM, work in the background writing tests and fixing bugs, then open a PR — e.g. "refactor the payment module for X" returns later as a PR with code plus passing tests.
- Agents accelerate mechanical work (boilerplate, repetitive changes, automatic test runs) but need guidance: supply the plan/to-do list and load `spec.md` or `plan.md` into context before telling them to execute.
- Supervised use is the rule, not unattended full-feature generation: let agents generate and run code while watching each step; orchestration tools like Conductor can run 3–4 agents in parallel, but the author mostly sticks to one main agent plus a secondary reviewer because parallel threads are mentally taxing.
- Treat every AI snippet as junior-developer output and test it: instruct the agent to run the test suite after each task and debug failures, since agents with a good test suite as a safety net "fly" while agents without tests blithely claim "sure, all good!" while breaking things.
- Review AI code line by line with extra scrutiny, optionally spawning a second AI session or different model to critique the first (e.g. "Can you review this function for any errors or improvements?"), and only merge or ship code you understand — asking for explanatory comments or rewriting convoluted output.
- Commit early and often with clear messages as "save points in a game": finish task, run tests, commit, so any sideways AI change can be reverted or cherry-picked; small per-chunk commits (never one giant "AI changes" commit) make it possible to pinpoint which change broke something.
- Use git history and isolation to steer and sandbox AI work: paste diffs/commit logs into prompts and let the agent parse diffs and use `git bisect` across a tidy history, and spin up branches or fresh git worktrees per feature so parallel AI sessions don't interfere and failed experiments can be discarded.
---
## Leverage AI coding across the lifecycle
| Tool class | Examples | Mechanism |
|---|---|---|
| CLI agents in project directory | Claude Code, OpenAI Codex CLI, Google Gemini CLI | Chat in the project directory; read files, run tests, multi-step fix issues |
| Asynchronous cloud agents | Google Jules, GitHub Copilot Agent | Clone repo into a cloud VM, work in background (tests, bug fixes), then open a PR |
| Orchestration (parallel agents) | Conductor | Run multiple agents in parallel on different tasks; some engineers run 3–4 at once |

Grounding mechanism: supply the plan or to-do list from earlier steps, and where supported load `spec.md` or `plan.md` into context before executing, to keep the agent on track. Operating rule: "these are power tools - you still control the trigger and guide the outcome."

**Covers:** Context packing, model choice, and AI coding agents across the SDLC
## Keep a human in the loop - verify, test, and review everything
AI produces plausible-looking code but the author is responsible for quality: "never ... blindly trust an LLM's output." Verbatim characterization, attributed to Simon Willison: think of an LLM pair programmer as "over-confident and prone to mistakes" — it writes with complete conviction, including bugs or nonsense, and won't flag what's wrong unless caught.

Testing loop: the planning stage generates a test list or testing plan per step; the agent is instructed to run the test suite after implementing a task and debug failures (write code → run tests → fix). Practitioners with strong testing practices get the most from agents; without tests the agent may claim "sure, all good!" while having broken several things.

Review practice: pause and review generated code line by line; spawn a second AI session or different model to critique the first, e.g. have Claude write code then ask Gemini, "Can you review this function for any errors or improvements?" AI-written code needs extra scrutiny because it can be superficially convincing while hiding flaws.

Runtime debugging: Chrome DevTools MCP, built with the author's last team, bridges static analysis and live browser execution — it "gives your agent eyes" by granting AI tools access to the DOM, rich performance traces, console logs, and network traces, enabling automated UI testing and precise diagnosis from runtime data.

Cautionary case: one developer leaning heavily on AI generation for a rush project produced an inconsistent mess — duplicate logic, mismatched method names, no coherent architecture — after "building, building, building" without stepping back; the fix was a painful refactor. The author's stance: "I remain the accountable engineer," "the LLM is an assistant, not an autonomously reliable coder," "I am the senior dev; the LLM is there to accelerate me, not replace my judgment." Practical rule: only merge/ship understood code; ask for comments or rewrite convoluted output; staying in the loop keeps skills sharp "just at a higher velocity." Summary rule: "stay alert, test often, review always. It's still your codebase at the end of the day."

**Covers:** Context packing, model choice, and AI coding agents across the SDLC
## Commit often and use version control as a safety net. Never commit code you can't explain.
Frequent commits are save points for undoing AI missteps: "commit early and often, even more than I would in normal hand-coding" — after each small task or successful automated edit, with a clear message, so a buggy or messy next suggestion can be reverted (e.g. `git reset`) or cherry-picked without losing hours. Practitioner quote: commits as "save points in a game."

Git history as AI context: scan recent commits to brief the AI; paste `git diffs` or commit logs into prompts so the AI knows what is new; LLMs parse diffs well and can use `git bisect` with infinite patience to find where a bug was introduced — but only with a tidy history.

Review/debugging discipline: small commits with good messages document the process; five changes in separate commits let you pinpoint the breakage, versus one giant commit titled "AI changes". Cadence: "finish task, run tests, commit," with each small work chunk ending as its own commit or PR.

Isolation for experiments: use branches or worktrees (inspired by Jesse Vincent) — spin up a fresh git worktree per feature/sub-project so multiple AI sessions run in parallel without interference; discard a failed worktree at no cost to main, merge a successful one. Example: AI implements Feature A while the author or another AI works on Feature B simultaneously.

**Covers:** Context packing, model choice, and AI coding agents across the SDLC
