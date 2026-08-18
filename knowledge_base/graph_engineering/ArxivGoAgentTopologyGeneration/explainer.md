> [[index|Wiki]] | [[summary|Summary]]

# Plain-Language Explainer: GoAgent

## What is this about?

Imagine you hire a team of AI assistants (each one an instance of a large language model, or "LLM" — the technology behind tools like ChatGPT or Claude) to solve a hard problem together, like writing code or answering a tricky question. Somebody has to decide: who on the team talks to whom? Does everyone message everyone (expensive and noisy), or does information flow in a smart, structured way (a decomposer hands off to a solver, who hands off to a checker)?

This paper, GoAgent, is about automatically designing that "who talks to whom" map — called a **communication topology** — for a team of AI agents. Instead of deciding connections one AI agent at a time, GoAgent first groups agents into small sub-teams (like a "research group" or a "verification group"), and then decides how the *sub-teams* should connect to each other. It also has a smart filter that throws away irrelevant chatter between sub-teams so the team doesn't waste time and money passing around information nobody needs.

## Why does it matter?

Multi-agent AI systems (teams of AI agents working together) are becoming a standard way to tackle problems too big for one AI to solve alone. But teams that are wired up badly waste money (LLMs charge by the amount of text they read and write — "tokens") and can make worse decisions, because irrelevant noise crowds out the signal that actually matters. Prior methods design these communication maps agent-by-agent, which is like designing an org chart by deciding "does Employee 47 report to Employee 12?" one pair at a time — you never explicitly build the notion of a "team" or "department," so those useful groupings have to emerge by accident. GoAgent instead builds the org chart the way real organizations are built: first form the departments, then wire the departments together. The result is a system that answers questions more accurately, uses meaningfully fewer tokens (about 17% less than the best prior method), and holds up better if someone tries to sabotage one team member.

## How does it work?

1. **Propose candidate groups.** For a given problem, an LLM is asked to sketch out a pool of plausible sub-teams — e.g., a "Solver group," a "Verifier group," a "Knowledge group" — each with a name, area of expertise, member roles, and a fixed internal structure (how the members inside that one group talk to each other).
2. **Encode the task.** The specific question being asked is turned into a numeric summary (a "vector") that represents what this particular task needs.
3. **Build the map step by step (autoregressive generation).** "Autoregressive" just means "one step at a time, using what's been built so far to decide the next step" — the same way ChatGPT writes one word at a time based on the words before it. Here, at each step, the system picks the next sub-team to add and decides which earlier sub-teams it should connect to, always guided by the task's numeric summary.
4. **Filter with an information bottleneck.** An **information bottleneck** is a technique for deliberately squeezing information through a narrow "bottleneck" so that only the parts relevant to a goal survive — like summarizing a long meeting down to just the action items relevant to your job. GoAgent's version, the Conditional Information Bottleneck, does this squeeze *conditioned on the specific task* — so what counts as "relevant" changes depending on what question is being answered, rather than using one fixed rule for every task.
5. **Train without trial-and-error.** Instead of letting the system try random topologies and rewarding good outcomes (a slow, unstable process called reinforcement learning), GoAgent is shown collected examples of task-topology pairs that are known to have worked, and learns to imitate them directly (a technique called "Teacher Forcing," similar to how a piano student practices by playing along with a recording of the correct notes).

## Where can this be used?

Anywhere you're building a system of multiple AI agents that needs to divide a big task among specialized sub-teams — research assistants, coding pipelines with separate "write code" / "review code" / "run tests" roles, customer-support systems that route to different specialist bots, or automated analysis pipelines. It's most useful when: (a) the task naturally splits into sub-team-sized chunks, (b) token cost matters (you're paying per API call), and (c) you want some resilience if one agent in the pipeline gets compromised or produces bad output (e.g., via a prompt injection attack — a technique where malicious text tricks an AI into ignoring its instructions).

## Conclusions & takeaways

GoAgent shows that rethinking the *unit* you build a multi-agent system's wiring diagram out of — groups instead of individuals — pays off on three fronts at once: better accuracy, lower cost, and more robustness to attack. The tradeoff is that the candidate groups are fixed ahead of time by an LLM, so the system can't invent a brand-new kind of specialist team on the fly if a task needs one that wasn't in the original pool, and it's only been tested on static, one-shot reasoning and coding tasks — not on tasks that unfold interactively over time.

## Jargon decoder

- **LLM (large language model):** the AI technology (like GPT-4 or Claude) that understands and generates text; the "agent" in this paper is one LLM given a role and instructions.
- **Multi-agent system (MAS):** several LLM instances working together, each often playing a different role, coordinating to solve a task no single one handles as well alone.
- **Communication topology:** the map (a directed graph) of who sends information to whom in a multi-agent system.
- **Node-centric vs. group-centric:** node-centric designs the map one agent-connection at a time; group-centric first forms sub-teams (groups), then wires the sub-teams together.
- **Autoregressive generation:** building something step by step, where each new step is chosen based on everything built so far — the same mechanism LLMs use to generate text one word at a time.
- **Information bottleneck:** a method that compresses information down to only the part relevant to a specific goal, discarding the rest as noise.
- **Conditional Information Bottleneck (CIB):** an information bottleneck whose notion of "relevant" changes based on a condition — here, the specific task being solved.
- **Teacher Forcing:** a supervised training method where the model learns by directly imitating known-good example sequences, rather than learning through trial-and-error rewards.
- **Ablation study:** an experiment where you remove one piece of a system to measure how much that piece actually contributes to performance.
- **Prompt injection attack:** a security exploit where malicious text embedded in an AI's input tricks it into ignoring its original instructions or behaving unexpectedly.
- **Token:** the basic unit of text (roughly a word or word-fragment) that LLMs process and that API providers usually charge for — fewer tokens used means lower cost.
