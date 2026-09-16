> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Primitives and production: filesystem to HaaS

**In one sentence:** Every harness component exists to deliver a specific desired behaviour, from filesystem and bash through memory, context management, hooks, and verification loops, and as models improve the scaffolding moves rather than disappears — converging on Harness-as-a-Service runtimes you configure instead of build.

## Key points

- Design working backwards from behaviour: behaviour wanted (or to fix) → harness piece that delivers it; any component without a named behavioural job should not exist.
- Filesystem plus Git is the foundational primitive — workspace for code/data/docs, offload for intermediate work, coordination surface for agents and humans — with versioning giving progress tracking, rollback, and branching.
- Bash plus code execution is the default general-purpose tool strategy (ReAct loop: reason → tool call → observe → repeat), because agents excel at shell and pre-building every tool is infeasible.
- Context rot is fought with four mechanisms: compaction (summarize/offload old context), tool-call offloading (head/tail in context, full 2,000-line outputs on disk), skills with progressive disclosure, and full context resets with a hand-off file for long jobs.
- Long-horizon work needs Ralph Loops (hook intercepts exit, re-injects original prompt into fresh context against a completion goal, state via filesystem), plan files plus self-verification, and generator/evaluator splits because self-grading skews positive.
- Hooks are the enforcement layer (run on lifecycle points: before tool call, after edit, before commit, session start) with the rule "success is silent, failures are verbose"; AGENTS.md stays short (HumanLayer: under 60 lines, earn each line) and ten focused tools beat fifty overlapping ones.
- Production proof is Claude Code (Fareed Khan breakdown): context injection, memory store, worktree isolator, permission gate with destructive-action hooks, subagent context firewalls, tool dispatch registry — and the Anthropic rule that every harness component encodes an assumption about what the model cannot do alone, so Opus 4.6 killed context-anxiety scaffolding but created need for multi-day memory and multi-agent coordination.
- The industry is moving from LLM APIs (give you a completion) to Harness-as-a-Service APIs (Claude Agent SDK, Codex SDK, OpenAI Agents SDK give you loop, tools, context, hooks, sandboxes); configure the four pillars (system prompt, tools, context, subagents) and iterate from a v0.1.

---

## Working backwards from behaviour

The framing from Viv: start from the behaviour you want and derive the harness piece that delivers it — behaviour we want (or want to fix) → harness design to help the model achieve this. Every harness component has a specific job; if you cannot name the behaviour a component exists to deliver, it probably should not be there.

## Filesystem and Git: durable state

The filesystem is the most foundational primitive, and it tends to be underrated because it is boring. Models can only directly operate on what fits in context. Without a filesystem, you are copy-pasting into a chat window, and that is not a workflow.

Once you have a filesystem, the agent gets:

| Capability | What it gives |
|---|---|
| Workspace | Read data, code, and docs |
| Offload | Place for intermediate work instead of holding it in context |
| Coordination surface | Shared files where multiple agents and humans coordinate |

Adding Git on top gives versioning for free: track progress, roll back errors, branch experiments. Most other harness primitives end up pointing at the filesystem for something.

## Bash and code execution: the general-purpose tool

The main agent loop today is a ReAct loop: the model reasons, takes an action via a tool call, observes the result, and repeats. But a harness can only execute the tools it has logic for. Two strategies:

- Pre-build a tool for every possible action.
- Give the agent bash and let it build the tools it needs on the fly.

Willison's take: agents already excel at shell commands; most tasks collapse to a few well-chosen CLI invocations. Harnesses still ship focused tools, but bash plus code execution has become the default general-purpose strategy for autonomous problem solving. It is the difference between teaching someone to use a single kitchen gadget and handing them a kitchen.

## Sandboxes and default tooling

Bash is only useful if it runs somewhere safe. Running agent-generated code on a laptop is risky, and a single local environment does not scale to many parallel agents.

Sandboxes give agents an isolated operating environment. Instead of executing locally, the harness connects to a sandbox to run code, inspect files, install dependencies, and verify work. Controls include allow-listed commands, network isolation, on-demand environment spin-up, and teardown when the task is done.

A good sandbox ships with good defaults: pre-installed language runtimes and packages, Git and test CLIs, a headless browser for web interaction. Browsers, logs, screenshots, and test runners are what let the agent observe its own work and close the self-verification loop. The model does not configure its execution environment — where the agent runs, what is available, and how it verifies output are all harness-level calls.

## Memory and search: continual learning

Models have no additional knowledge beyond their weights and what is currently in context. Without the ability to edit weights, the only way to add knowledge is through context injection.

The filesystem is again the primitive. Harnesses support memory file standards like AGENTS.md that get injected on every start. As the agent edits that file, the harness reloads it, and knowledge from one session carries into the next — a crude but effective form of continual learning.

For knowledge that did not exist at training time (new library versions, current docs, today's data), web search and MCP tools like Context7 bridge the cutoff. These are useful primitives to bake into the harness rather than leaving to the user.

## Battling context rot

Context rot is the observation that models get worse at reasoning and completing tasks as the context window fills up. Context is scarce, and harnesses are largely delivery mechanisms for good context engineering.

Three techniques show up repeatedly:

- **Compaction.** When the window gets close to full, something has to give. Letting the API error is not an option for a production harness, so the harness intelligently summarizes and offloads older context so the agent can keep working.
- **Tool-call offloading.** Large tool outputs (think 2,000-line log files) clutter context without adding much signal. The harness keeps the head and tail tokens above a threshold and offloads the full output to the filesystem, where the agent can read it on demand.
- **Skills with progressive disclosure.** Loading every tool and MCP into context at startup degrades performance before the agent takes a single action. Skills let the harness reveal instructions and tools only when the task actually calls for them.

Anthropic's harness post adds one more technique for really long jobs: full context resets, where the harness tears the session down and rebuilds it from a compact hand-off file. They are explicit that compaction alone was not sufficient for long tasks; sometimes you need to start fresh with a structured brief. This is closer to how humans onboard a new engineer than to how we usually think about "memory."

## Long-horizon execution: Ralph Loops, planning, verification

Autonomous long-horizon work is the holy grail and the hardest thing to get right. Today's models suffer from early stopping, poor decomposition of complex problems, and incoherence as work stretches across multiple context windows. The harness has to design around all of that.

**Ralph Loop:** a hook intercepts the model's attempt to exit and re-injects the original prompt into a fresh context window, forcing the agent to continue against a completion goal. Each iteration starts clean but reads state from the previous one through the filesystem. A surprisingly simple trick for turning a single-session agent into a multi-session one, and the kind of primitive you would never derive from "just use a smarter model."

**Planning plus self-verification:** the model decomposes a goal into a sequence of steps, usually into a plan file on disk. The harness supports this with prompting and reminders about how to use the plan file. After each step, the agent checks its work via self-verification: hooks run a pre-defined test suite and loop failures back to the model with the error text, or the model reviews its own output against explicit criteria.

**Planner / generator / evaluator splits:** Anthropic's long-running harness work is explicit that separating generation from evaluation into distinct agents outperforms self-evaluation, because agents reliably skew positive when grading their own work. It is GANs for prose. The related pattern is the sprint contract, where the generator and evaluator negotiate what "done" actually means before code gets written. Writing down the done-condition before starting catches more scope drift than any prompt change.

## Hooks: the enforcement layer

Hooks are what separate "I told the agent to do X" from "the system enforces X."

A hook is a script that runs at a specific lifecycle point: before a tool call, after a file edit, before commit, on session start. They are the right place for things the agent should never forget but often does:

- Run typecheck and lint and tests after every edit and surface failures.
- Block destructive bash (`rm -rf`, `git push --force`, `DROP TABLE`).
- Require approval before opening a PR or pushing to main.
- Auto-format on write so the agent does not waste tokens on whitespace.

The principle HumanLayer highlights: success is silent, failures are verbose. If typecheck passes, the agent hears nothing. If it fails, the error text gets injected into the loop and the agent self-corrects. That makes the feedback loop almost free in the common case and directly actionable when something goes wrong.

## AGENTS.md and tool choice

The flat markdown rulebook at the root of the repo is still the single highest-leverage configuration point, because it lands in the system prompt every turn. Conventions go here: package manager, test framework, formatting, "never touch /legacy," "always use our logger." Two hard-won lessons:

- **Keep it short.** HumanLayer keeps theirs under 60 lines. Every line is competing for attention, and more rules make each rule matter less. Pilot's checklist, not style guide.
- **Earn each line.** Rules should trace to a specific past failure or a hard external constraint. If they do not, they are noise. Ratchet; do not brainstorm.

Same discipline applies to tools. Each tool's name, description, and schema gets stamped into the prompt every request. Ten focused tools outperform fifty overlapping ones because the model can hold the menu in its head. HumanLayer also flags a real security concern: tool descriptions populate the prompt, so any MCP server you install is trusted text the model will read. A sloppy or malicious MCP can prompt-inject your agent before you have typed anything.

## What this looks like in production

The clearest public picture of a mature harness is Fareed Khan's (estimated) breakdown of Claude Code's architecture. Almost every concept from the previous section shows up as a named component:

- Context injection is the knowledge layer.
- Loop state lives in the memory store and the worktree isolator.
- Destructive-action hooks sit behind the permission gate.
- Subagent context firewalls are the entire multi-agent layer.
- The tool dispatch registry is where MCP servers and bash both plug in.

Khan's argument is the same as Viv's, just worked through a shipping product: Claude Code's trajectory is about the harness at least as much as about the model underneath it.

## Harnesses don't shrink, they move

One of the better observations in the Anthropic write-up is that as models improve, the space of interesting harness combinations does not shrink. It moves.

The naive story is that better models make harnesses obsolete. If the model can plan, no planner. If the model is coherent at long horizons, no context resets. And yes, Opus 4.6 largely killed the context-anxiety failure mode (Sonnet 4.5 used to wrap up work prematurely as it approached what it thought was its context limit), which means a whole class of anxiety-mitigation scaffolding from six months ago is now dead code.

But the ceiling moved with the model. Tasks that were unreachable are in play, and they have their own failure modes. The anxiety scaffolding goes away, and in its place you need a multi-day memory policy, or a harness that coordinates three specialized agents, or evaluators for design quality in generated UIs. The assumptions shift, and so does the scaffolding that encodes them.

Anthropic puts it cleanly: "every component in a harness encodes an assumption about what the model can't do on its own." When the model gets better at something, that component becomes load-bearing for nothing and should come out. When the model unlocks something new, new scaffolding is needed to reach the new ceiling.

## The model-harness training loop

A feedback loop exists between harness design and model training. Today's agent products are post-trained with harnesses in the loop. The model gets specifically better at the actions the harness designers think it should be good at: filesystem operations, bash, planning, subagent dispatch. That is why Opus 4.6 feels different inside Claude Code than inside someone else's harness, and why changing a tool's logic sometimes causes strange regressions. A genuinely general model would not care whether you used `apply_patch` or `str_replace`, but co-training creates overfitting.

The practical implication is twofold. A harness is a living system, not a config file you set up once. And the "best" harness is not necessarily the one the model was trained inside; it is the one designed for your task. Viv's Top 30 to Top 5 Terminal Bench jump is the clearest proof point.

## Harness-as-a-Service

Viv's other contribution is the HaaS framing: Harness-as-a-Service. The observation is that we are moving from building on LLM APIs (which give you a completion) to building on harness APIs (which give you a runtime). The Claude Agent SDK, the Codex SDK, and the OpenAI Agents SDK all point in the same direction. You get the loop, the tools, the context management, the hooks, and the sandbox primitives out of the box, and you customize them.

The shift matters because the default path used to be: build your own loop, wire up your own tool-calling, handle your own conversation state, invent your own approval flow. Now the default path is: pick a harness framework, configure it along the four pillars (system prompt, tools, context, subagents), and put the rest of your effort into domain-specific prompt and tool design.

That is what makes "skill issue" tractable. You are not rebuilding an agent from scratch every time something goes wrong. You are tuning a configuration surface that is already well-factored.

Viv's line on this is also the best argument for starting messy: "good agent building is an exercise in iteration. You can't do iterations if you don't have a v0.1."

## Where this is going

Look at the top coding agents side by side (Claude Code, Cursor, Codex, Aider, Cline) and they look more like each other than their underlying models do. The models are different. The harness patterns are converging — the industry slowly finding the load-bearing pieces of scaffolding that turn a generative model into something that can ship.

Viv's framing of the open problems: orchestrating many agents working in parallel on a shared codebase; agents that analyze their own traces to identify and fix harness-level failure modes; harnesses that dynamically assemble the right tools and context just-in-time for a given task instead of being pre-configured at startup. That last one feels like where harnesses stop being static config and start becoming something closer to a compiler.

**Covers:** chunk 02
