# Native Python Object-Oriented Agents

**Paper:** [Native Python Object-Oriented Agents (Furgale et al., NVIDIA, 2026)](https://arxiv.org/abs/2607.20709)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine hiring a new employee and, instead of scattering their job description across sticky notes, side-channel emails, and a separate rulebook nobody reads, you just hand them one well-organized employee handbook: here are your duties, here is your labeled filing cabinet, here is what "done" looks like for each task. NOOA does exactly that for AI assistants: it turns an "agent" into an ordinary piece of computer code (a Python class) where the assistant's jobs are its methods, its notes are tidy labeled fields instead of a messy diary, and it can reach directly into real files, spreadsheets, or game boards rather than hearing about them second-hand through garbled text descriptions. Because the AI already "speaks" ordinary computer code fluently from its training, this handbook style turns out to make it dramatically better and cheaper at real jobs -- fixing software bugs, finding security holes, playing an unfamiliar video game -- than the messier, ad-hoc styles used by most other AI-agent tools today.

## TL;DR

NOOA (NVIDIA Object-Oriented Agents) represents an LLM agent as an ordinary Python object: methods are actions (docstring = prompt, type signature = enforced contract), fields are durable state, and a method whose body is just `...` is completed at runtime by a strategy-driven agent loop (a single-shot `PredictStrategy` or an iterative CodeAct REPL loop), while normal-bodied methods stay deterministic Python. The paper claims this is the first design to combine six model-facing capabilities on one surface -- typed I/O, pass-by-reference over live objects, code-as-action, programmable loop engineering, explicit object state, and model-callable harness APIs for context/events/memory -- and backs the claim with a 14-framework survey (none combine all six), 88 capability tests across 10 models (97.9% pass rate), and benchmark results on SWE-bench Verified (82.2%), Terminal-Bench 2.0 (73.0%), CyberGym L1 (86.8%, best open-source entry), and ARC-AGI-3, where a single agent running a 50-line skill replaces a six-agent, ~150k-line world-model system and pushes the benchmark's score-cost Pareto frontier to 85.1% RHAE with GPT-5.6-sol -- a 6.4x improvement over the raw model.

---

## Problem & Motivation

Agent development has fragmented into many agent development kits (ADKs), each inventing its own developer-facing and model-facing abstractions. As a result, agent source code ends up split across prompt templates, schemas, callbacks, configuration files, and orchestration code -- mature primitives (tools, memory, workflows, code execution) exist, but not as one coherent surface. Learning a new agent framework typically means learning a new bespoke programming model for capabilities -- typed interfaces, variable scoping, control flow, async execution, object state -- that ordinary programming languages already solved. This is wasteful twice over: these abstractions are already familiar to human developers, *and* they are heavily represented in the data LLMs were trained on, so reinventing them as a domain-specific language (DSL) throws away both kinds of familiarity. Taking direct inspiration from PyTorch (a powerful runtime behind a simple Python programming model), NOOA's thesis is that wherever Python already has the right abstraction, the framework should use it directly rather than invent a new one -- eliminating the human learning curve while maximizing "agent readiness," since models already know ordinary Python.

---

## Main Original Ideas

1. **Agent-as-a-Python-object programming model.** An agent is simply a Python class: its methods are the actions the model can take, its fields are its state, its docstrings are its prompts, and its type annotations are enforced contracts. A method with a real body executes as deterministic code; a method whose body is the ellipsis (`...`) becomes an "agentic method" completed at runtime by an LLM-driven loop -- so developers and agents share literally the same interface, testable and refactorable like any other software.
2. **Typed I/O as an enforced loop contract.** Agentic methods have typed inputs and a typed return value that the harness actively validates before returning control to the caller, retrying with an error message on failure. This makes the type contract binding rather than advisory, unlike frameworks where typing covers only an inner tool call or a bolt-on output schema.
3. **Pass by reference over live objects.** Arguments and return values cross the model boundary as live Python objects, not serialized text. For large arguments, the model sees only a bounded head/tail preview (type, true length, a few elements) while the full object remains bound and fully usable in code -- so the amount of data an agent can process is bounded by the execution environment, not by the prompt.
4. **Code as action (the CodeAct loop).** The model acts by writing and executing real Python -- with control flow, helper calls, and inline method/tool calls -- inside a restricted, Jupyter-like REPL against the live agent object, rather than emitting one JSON tool call per turn.
5. **Programmable loop engineering.** There is no separate workflow DSL: outer orchestration loops are ordinary Python methods a developer writes, and inner loops are ordinary Python code the model writes inside a CodeAct turn (e.g., fanning out subagents with `asyncio.gather`) -- both using the same object model and calling convention.
6. **Explicit, model-visible object state.** Durable state lives as typed fields on `self` rather than only in conversation history, and is rendered fresh into a bounded per-turn context block on every LLM call -- so state survives independent of transcript length or compaction.
7. **Model-callable harness APIs.** Structured static/dynamic context blocks and a queryable, typed event history are exposed as explicit Pythonic APIs (`self.context[...]`, `self.events.query(...)`) to both the developer and the model, rather than being hidden host machinery.
8. **Agent-authored long-term memory subsystem.** An optional, fully reversible add-on (`MemoryManager.install(agent)`) gives the model seven tools to author its own memories, retrieves via ACT-R activation (relevance/recency/importance) over a typed memory graph, supports "pass-by-reference" memories resolved against live agent state, consolidates asynchronously, and stores everything in one inspectable SQLite file.

---

## Key Findings

**Table -- headline benchmark results**

| Benchmark | NOOA best result | Key comparisons |
|---|---|---|
| Capability tests (88 tests x 10 models x 5 runs) | 97.9% overall pass rate | Stress-test subset (batching, error recovery, refinement) drops to 84.7%; small/frontier gap widens from 3.2 to 23 points |
| SWE-bench Verified (500 tasks) | 82.2% (GPT-5.5, xhigh reasoning); 79.8% (Opus 4.6, high) | vs. OpenCode 78.6%/75.2%, PI 78.2%/75.8%; specialized closed systems: Codex 88.7%, Claude Code 80.8% |
| Terminal-Bench 2.0 (89 tasks) | 73.0% (GPT-5.5, high/xhigh); 65.2% (Opus 4.6, high) | vs. OpenCode 60.7%/43.8%, PI 68.5%/58.4% (PI's xhigh peak of 75.3% edges NOOA's 73.0%) |
| CyberGym L1 (vulnerability discovery) | 86.8% (GPT-5.5), network blocked | Top open-source agent; behind closed Microsoft MDASHv2 (95.6%) and Crystalline/Opus 4.6 (89.6%); ahead of OpenAI Codex+skill (83.5%) |
| ARC-AGI-3 (RHAE, 2-hour fleet cap) | 50.2% (GPT-5.5); 85.1% (GPT-5.6-sol, <$20/game) | vs. hypothesis-driven baseline 41.7% (+8.5 pts); markdown-file memory ablation 38.4% (+11.8 pts for memory subsystem); raw GPT-5.6-sol scores 13.3% on ARC Prize's own eval -- a 6.4x harness effect |

- **SWE-bench score-cost Pareto frontier:** at GPT-5.5 xhigh, NOOA hits 82.2% using ~28 calls and ~1.1M tokens/task, versus OpenCode's ~1.3M tokens for 78.6% and PI's 66 calls/~2.2M tokens for 78.2% -- NOOA sits at or above the other harnesses' accuracy at every comparable token budget (Figure 6).
- **Termination discipline matters:** OpenCode stops whenever the model responds without a tool call (77% of its failed GPT-5.5 Terminal-Bench trials end within 10 steps); NOOA instead requires a validated, evidence-bearing `TaskResult`, preventing unsupported "done" claims.
- **Reasoning effort as capability equalizer:** on the capability suite, reasoning-mode gains grow monotonically as model size falls -- Nemotron 3 Nano improves 52.5%->84.8% (off->on) versus Opus 4.8's already-saturated 100.0%/99.5%.
- **Stress-test case studies (Appendix B):** sophistication and success are orthogonal -- Claude Opus 4.8 correctly fanned out a batch classification but then failed by hand-transcribing its own printed results (dropping one item), while GPT-5.5 passed with a fully manual, no-subagent approach purely through disciplined bookkeeping.
- **14-framework survey (Sec. 5, Table 7):** across LangGraph/LangChain, LangChain Deep Agents, Microsoft Agent Framework, OpenAI Agents SDK, Google ADK, PydanticAI, smolagents, Claude Agent SDK, OpenAI Codex, OpenHands, PI, Hermes, OpenCode, and OpenClaw, **no framework scores "Strong/Supported" on all six axes**; most score "typed output only" (not input) for typed I/O, files/paths rather than live objects for pass-by-reference, and tool-mediated (not live) state for object state. NOOA self-scores "Strong" on all six. Several of the newest, strongest competing capabilities (Microsoft's Monty CodeAct provider, Pydantic's CodeMode, OpenAI Codex's code mode) shipped only as experimental/flag-gated features during the survey window -- read by the authors as the field converging toward NOOA's six ideas.
- **ARC-AGI-3 world-model compression:** one NOOA agent plus a 50-line skill reproduces the DreamTeam system's methodology (six roles, 1,821 lines of prompts, a 4,690-line retrodiction engine, ~150k lines total) in ~6.1k lines, with the memory subsystem replacing DreamTeam's per-role carry-forward ledgers.
- **Sandbox red-team audit:** 18 scans of the live 25-game ARC-AGI-3 fleet found zero rule violations (no network calls, no game-source leakage, no cross-game reads) across 13,335 agent logs; one escape attempt was blocked pre-execution by the cell guard.

---

## Suggestions & Future Directions

1. **Rewrite the whole agent, not just the prompt.** The authors argue optimization should extend beyond prompt search to rewriting prompts, docstrings, typed signatures, helper code, tool descriptions, context policies, and retry/decomposition structure together, citing GEPA-style reflective optimization as a starting point but framing the real target as the whole agent object and harness.
2. **Turn skills into full software packages.** Today's "skills" across most harnesses are text snippets or informal procedures; the authors expect skills to evolve into typed libraries with documentation, tests, examples, subagents, dependencies, and versioned interfaces that agents can inspect, call, repair, and extend themselves.
3. **Use reinforcement learning to teach inductive, harness-level reasoning.** Citing DeepSeek-R1 as precedent for outcome-driven RL inducing reasoning behavior, the authors propose training over complete agent trajectories so models learn what context to reveal, which variables to preserve, when to write deterministic helpers, and when to decompose tasks -- turning the harness itself into a learned action space rather than a passive execution environment.
4. **Acknowledged limitation -- no host sandboxing.** NOOA executes model-written code in the agent's own process; its validator protects the agent loop (type-checks return values) but is explicitly *not* a security sandbox and makes no claim about what arbitrary generated code can do to the host machine -- this is the same isolation posture as any harness with a shell tool. The authors' recommended mitigation is external, OS-level isolation (their own OpenShell system) placed around the process, since in-process execution is also precisely what preserves pass-by-reference.
5. **Open technical work flagged in the text.** Better bounded-preview formats for pass-by-reference (the current `pprint`-style format was chosen empirically and may not be optimal for all models) and extending preview support to more data types remain unresolved; the companion "workspace optimization" line of work also leaves cross-task transfer only partially solved outside of the memory subsystem.

---

## Authors & Institutions

Paul Furgale, Severin Klingler, James Nolan, Matt Staats, Gaia Di Lorenzo, Elisa Martinez Abad, Christian Schuller, Razvan Dinu, Alessio Devoto, Pascal Berard, Gal Kaplun, Elad Sarafian, Riccardo Roveri, Leon Derczynski, Ricardo Silveira Cabral -- all NVIDIA.

## Figures

![The CodeAct strategy loop within an agentic method: each turn renders context from live Python state, calls the LLM, optionally executes a model-written Python action, and updates events and state, repeating until a type-validated result is returned to the caller.](wiki/images/fig2-codeact-loop.png)

![SWE-bench Verified pass rate plotted against mean prefill+output tokens per task, across NOOA, OpenCode, and PI at multiple backends and reasoning-effort levels: NOOA's points sit at or above the accuracy of the other two harnesses at every comparable token budget, occupying most of the score-cost Pareto frontier.](wiki/images/fig6-swebench-pareto.png)

![Fleet-mean RHAE over time and spend on ARC-AGI-3 under the two-hour competition cap for the world-model-plus-memory skill (GPT-5.5 and GPT-5.6-sol), a markdown-file memory ablation, and a hypothesis-driven baseline, showing the memory subsystem's contribution and the score achieved once game mechanics have been encoded and can be predicted.](wiki/images/fig7-arcagi3-rhae.png)
