> [[index|Wiki]] | [[summary|Summary]]

# Orkes Conductor — In Plain Language

## What is this about?

Imagine you order food online. Behind one tap, a chain of small jobs runs: the restaurant confirms, the kitchen cooks, a courier is assigned, you get a text, the payment clears. If any step fails — the courier cancels, the card declines — someone has to notice, retry, or undo the earlier steps (refund you, free the kitchen slot).

Orkes Conductor is the "someone" for software. It is a central coordinator that runs such multi-step jobs across different services, keeps a written record after every step, and knows what to do when something breaks: try again, wait, ask a human, or undo what already happened. Recently the same coordinator learned to run AI helpers: asking a language model a question, letting it look things up or use tools, and pausing for a person to approve before anything important happens — all recorded step by step.

## Why does it matter?

Without a coordinator, every service has to handle failures itself: "what if the next service is down? what if I already charged the customer?" That logic gets copied everywhere, breaks quietly, and nobody can answer "where exactly did my order get stuck?"

With a coordinator, the whole process is written down in one place as a recipe (called a *workflow*), every step's result is saved, and a crash or restart just resumes from the last finished step. For AI helpers this matters even more: a helper that can act on its own needs the same safety rails — limited retries, approval gates, and a full log of what it did and why.

## How does it work?

Step-by-step, using the food-order analogy:

1. **Write the recipe.** You describe the process as a list of steps with rules: do A then B, do C and D at the same time, if the answer is "yes" go one way otherwise the other, repeat until done. The recipe is stored with a version number, like a cookbook edition.
2. **Start a run.** Each real order creates a *run* of the recipe. The coordinator hands out steps one at a time and writes down each result before handing out the next.
3. **Helpers do the work.** Small programs called *workers* pick up steps they know how to do (charge a card, send a text), do them, and report back. Common chores — calling a web address, waiting a while, asking a human — are built in, so no custom code is needed for them.
4. **React to trouble.** Each step declares its own safety policy: retry 3 times with growing pauses, give up after 2 minutes, or mark the step optional and continue. If the whole run fails, a backup recipe (*failure workflow*) undoes finished steps in reverse — refund, cancel, notify.
5. **Pause and resume freely.** A step can wait hours for a human approval or an outside event. Waiting costs nothing; the run's state sits safely stored until the signal arrives.
6. **Watch everything.** Every run is searchable — by status, time, customer, or custom labels — with the full history of inputs, outputs, and retries for each step.

## Where can this be used?

- **Online shops and bookings:** order → pay → ship, with refunds if any step fails.
- **Approvals:** expense reports, document sign-offs, loan applications that wait days for a human.
- **Data chores:** nightly jobs that fan out to thousands of parallel copies and collect the results.
- **AI assistants:** question-answering helpers that search documents, call tools, and ask a person before acting.
- **Alerts and automation:** "when this event arrives, start that process" — e.g. a payment signal triggers provisioning.

## Conclusions & takeaways

- One coordinator with a written record beats scattered retry logic hidden in every service.
- Saving progress after every step is what makes long, failure-prone processes safe — for both classical services and AI helpers.
- AI output is treated as a *suggestion*: the recipe checks it, limits what tools it may use, and asks a human before risky actions.
- Honest limitation: you must run the coordinator itself reliably, and very chatty high-frequency jobs may fit simpler tools better.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Workflow | The recipe: the full multi-step process written down once |
| Task | One step in the recipe (charge card, send text, ask the AI) |
| Worker | A small helper program that performs steps it knows how to do |
| Operator | A recipe instruction about *flow* (do in parallel, choose a branch, repeat) |
| System task | A built-in chore needing no custom code (call a URL, wait, publish an event) |
| Durable execution | Progress is saved after every step, so crashes never lose work |
| Saga / compensation | The undo plan: reverse finished steps when the run fails |
| Event handler | A rule: "when this outside signal arrives, start or advance a run" |
| Human-in-the-loop | The recipe pauses and waits for a person to approve or decide |
| MCP (Model Context Protocol) | A standard way for AI helpers to discover and call outside tools |
| A2A (agent-to-agent) | A standard way for one AI helper to delegate to another |
| RAG (retrieval-augmented generation) | The helper looks up documents first, then answers using them |
