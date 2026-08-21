> [[index|Wiki]] | [[summary|Summary]]

# GraphPlanner — In Plain Language

## What is this about?

Imagine you run a small consulting firm with a dozen consultants of wildly different skill and price: some are cheap generalists, some are expensive specialists, and a couple are pricey experts who are only worth calling for the hardest problems. When a client brings you a complex question, you need to decide two things at once for every step of the work: *what kind of task is this step* (should someone break the question into smaller pieces? answer one of the pieces? stitch the answers together into a final report?) and *which consultant should do it*.

This paper is about building an automatic dispatcher for exactly that situation, except the "consultants" are different large language models (LLMs) — like GPT, Llama, or Mistral variants — and the "steps" are pieces of an AI agent's workflow. The dispatcher, called GraphPlanner, doesn't just pick one model per question; it decides a whole sequence of role-and-model pairs, learns from how well past decisions worked out, and gets better over time through trial and error (reinforcement learning).

## Why does it matter?

Companies increasingly build AI systems out of several LLM calls chained together — one model plans, another executes, another summarizes. Picking the wrong model for a step wastes money (using an expensive model for a trivial sub-task) or wastes quality (using a cheap model for something that needs real reasoning). Existing "routers" — the traffic-cop software that assigns queries to models — are either too simple (pick one model and stick with it for the whole request) or too shortsighted (pick models call-by-call without remembering how the team's previous jobs went). GraphPlanner shows you can get noticeably better accuracy *and* dramatically lower cost by giving the dispatcher a structured memory of who-did-what-and-how-well, both for the current job and for jobs completed before.

## How does it work?

Think of GraphPlanner's memory as two connected notebooks, both organized as graphs (webs of connected dots) rather than flat lists:

1. **The workflow notebook** (`G_workflow`) — tracks the current job in progress: which sub-questions have been created, who answered them, how accurate and how expensive each answer was.
2. **The history notebook** (`G_history`) — tracks past jobs the team has already finished, with the same kind of information.

Both notebooks connect to the same set of "consultant cards" — one card per (consultant, job-type) combination, e.g. "GPT-mini as a Summarizer," "Llama-70B as a Planner." This shared set of cards is the trick that lets information flow between the two notebooks without duplicating anything: a lesson learned in a past job (recorded in the history notebook) updates the same card that the current job (in the workflow notebook) reads from.

At each step:

1. GraphPlanner looks at the current unresolved question and the two notebooks.
2. A graph neural network (a kind of pattern-recognizer built to read connected-dot diagrams) reads both notebooks and scores every possible (role, consultant) pairing.
3. It picks the highest-scoring valid pairing — valid meaning, for instance, you can't summarize before anything has been answered.
4. That consultant does the job; the result gets written back into the workflow notebook, updating the picture for the next step.
5. The whole sequence keeps going until the original question is fully answered, at which point the system checks how good the final answer was and how much it all cost, and uses that as a training signal (reward) to make the dispatcher a little better next time.

The training method is PPO (Proximal Policy Optimization) — a well-established reinforcement-learning algorithm that nudges the dispatcher's decision-making toward higher rewards without destabilizing it, similar to how you'd coach an intern by giving steady, moderate feedback rather than wild swings in instruction.

## Where can this be used?

- **Multi-model AI platforms** — any product that already calls several different LLMs (cheap ones for routine work, expensive ones for hard cases) can use this kind of dispatcher to automatically balance quality against API cost.
- **Enterprise agent orchestration** — companies building internal "AI teams" (planner + coder + reviewer agents, for instance) could use a GraphPlanner-style router to decide dynamically which internal or external model handles each agent role per request, rather than hard-coding "always use model X for the planner."
- **Cost-sensitive deployments** — because the reward function explicitly trades off accuracy against cost, this approach is directly useful anywhere a fixed compute/API budget needs to stretch across many queries of varying difficulty.
- **Any setting with reusable task patterns** — since the historical-memory graph lets new queries benefit from patterns seen in past queries, it is a natural fit for organizations with high query volume and recurring task types (customer support triage, data analysis pipelines, coding assistants).

## Conclusions & takeaways

A month from now, remember this: **routing decisions in multi-agent LLM systems are themselves a sequential decision problem, not a one-shot classification problem** — and giving the router a shared, graph-structured memory of both the current job and past jobs measurably improves both accuracy and cost, and helps it generalize to new tasks, new models, and even new agent roles it has never seen. The honest limitation: everything here is evaluated in a controlled benchmark setting with fixed candidate LLM pools (12 models) and clearly defined roles; how this scales to open-ended production environments with dozens of rapidly-changing models, or how robust the shared history graph is to noisy or adversarial history, is not tested.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| LLM router | Software that decides which language model should handle a given request. |
| Agentic workflow | A multi-step AI process where different "agent roles" (planner, executor, summarizer) each do part of the job, often using different models. |
| MDP (Markov Decision Process) | A formal way of describing a sequence of decisions where each choice affects the state you're in next and how much reward you eventually get. |
| GARNet | The paper's custom graph neural network that reads the workflow and history notebooks and decides the next role/model pairing. |
| Heterogeneous graph | A graph (network of connected dots) where the dots and connections can be different types — here: queries, responses, and (LLM, role) hub cards. |
| PPO (Proximal Policy Optimization) | A reinforcement-learning training method that improves a decision-making policy gradually and safely, avoiding destabilizing over-corrections. |
| Role hub node | The shared "consultant card" for one (LLM, role) combination, reused across the current job and all past jobs to avoid duplicating information. |
| Pareto frontier | The set of "best possible trade-off" points between two competing goals (here, accuracy vs. cost) — you can't improve one without giving up the other along this curve. |
| Inductive vs. transductive inference | Inductive: make decisions using only the current information (cheap, no lookup). Transductive: also consult stored records from training-time interactions (more accurate, more expensive). |
| Zero-shot generalization | Performing well on tasks, models, or roles the system was never specifically trained on. |
| Ablation | An experiment that removes one component of a system to measure how much that component was actually contributing. |
