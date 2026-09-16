> [[index|Wiki]] | [[summary|Summary]]

# Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures — In Plain Language

## What is this about?

Imagine you hire a new employee who can send emails, use the company's internal software, ask coworkers for help, and occasionally call outside vendors. One day a task goes badly wrong — a report is late, a customer gets the wrong information, a delivery never happens. "The employee messed up" is not actually a useful thing to write in the incident report, because it doesn't tell you what to fix. Maybe the employee really did drop the ball. But maybe the internal software silently failed and told them everything was fine. Maybe the instructions they were given were self-contradictory. Maybe a coworker they delegated part of the job to never reported back. Maybe an outside vendor's system was down. Same visible outcome ("task failed"), four completely different fixes.

This paper is about AI "agents" — computer programs built on large language models (the technology behind chatbots like ChatGPT or Claude) that don't just answer questions, but take multi-step action: they call software tools, write and run code, browse the web, remember things across a long session, and sometimes hand off pieces of work to other AI agents.

When one of these agents fails a task, everyone currently tends to write the equivalent of "the employee messed up" — a report that just says the agent failed, without saying whether the problem was the AI model's own judgment, the surrounding software scaffolding it runs inside of ("the harness" — think of it as the employee's desk, notes, tools, and phone lines), the person who gave the instructions, or something broken in the outside world it was interacting with.

The authors build a structured way to always ask two questions about any agent failure: (1) which relationship broke down — was it the agent's dealings with its boss, its tools, its notes, a coworker agent, or the outside world? — and (2) on that particular relationship, whose behavior was actually defective? They call this a "repair-assignment problem," because the whole point of pinpointing blame correctly is to know what to actually go fix.

## Why does it matter?

Right now, when an AI agent fails, the typical incident report or benchmark score just records "failed" — a thumbs-down with no diagnosis attached. That's like a car mechanic's report that only says "car didn't start," with no distinction between a dead battery, a broken alternator, an empty gas tank, or a driver who never turned the key. Without that distinction, people default to the most expensive and slowest fix available — retraining or replacing the AI model — even in cases where the actual problem was a broken tool integration, a badly worded instruction, a coworker agent that silently dropped information, or a flaky external service that was never going to work no matter which AI ran the show.

If this taxonomy (a fancy word for "a labeled filing system for types of failure") is adopted, teams reviewing an agent's failures get a standard checklist: name the broken relationship, name which side of it is actually at fault, and only then decide the fix. Some fixes are cheap (rewrite a prompt, fix a tool's error-reporting, change how memory gets summarized); others are genuinely expensive (retrain the model). Misdiagnosing the cheap kind as the expensive kind wastes enormous effort — and misdiagnosing the expensive kind as the cheap kind means the same failure keeps recurring after a "fix" that never touched the real problem.

## How does it work?

Think of the AI model as an employee sitting at a hub with phone lines running out to everyone they deal with, grouped into three families:

1. **The User family** — the *Owner* (whoever gave the actual task), the *Grader* (whoever checks the work — which can be a different, stricter standard than what the owner asked for), and *Third parties* (outsiders who send messages or content into the conversation, like an email from a stranger).
2. **The Harness family** — the employee's own *Context* (their short-term notes/working memory for this task), their *Memory* (a longer-term notebook that persists across days), their *Tools* (calculator, database, search engine — anything they call to get work done), and other AI models they talk to as a *Peer* (an equal collaborator) or delegate to as a *Subagent* (someone working under them).
3. **The Environment family** — the *Local* environment (things happening on the employee's own machine/sandbox) and the *External* environment (outside services, like a vendor's API or an email server).

The method for diagnosing any single failure runs in four steps:
1. Figure out what actually happened, step by step, in the order it happened.
2. Find the visible end result that everyone agrees was bad.
3. Walk the story backward until you find the *earliest* point where things went wrong and never recovered — everything that happened afterward is just falling dominoes, not new evidence. This earliest unrecovered slip is the one and only thing that gets labeled; the paper borrows this "find the first domino" rule from prior root-cause-analysis research.
4. Ask which phone line that slip happened on (which relationship — e.g., employee-and-tool, employee-and-boss), and then apply one deceptively simple rule to decide fault: **if a more capable version of the same employee could plausibly have avoided or recovered from this exact slip, the fault is the employee's (the model). If no realistic amount of extra skill would have helped — the phone line itself was cut, the instructions were contradictory, the tool lied about succeeding, the outside vendor's server was down — the fault belongs to the other party.**

This rule is deliberately generous toward blaming the model — most breakdowns are at least theoretically something a sufficiently sharp employee could have caught — so when a failure *still* survives this generous test and lands on the boss, the notebook, the tool, a coworker, or the outside world, that's a strong signal the fix genuinely lies outside the model.

A small everyday example of the same logic: an assistant emails the wrong meeting time to a client. If the assistant misread a calendar entry that was sitting right there, that's the assistant's fault (a sharper assistant would have read it correctly). If the calendar app silently double-booked and showed a stale time with no warning, that's the software's fault. If the boss texted the wrong time in the first place, that's the boss's fault. Same visible mistake — "wrong time sent" — three different repairs, found only by tracing back to where the wrong information actually entered the picture.

A concrete illustration — the "Harbor-Mix" case: an AI agent is asked to find a safe location, move some property listings there, email two colleagues to confirm, and then wait for anyone to reply with change requests before finalizing anything. The agent does the first half flawlessly — it sends the right emails to the right people and confirms with the user, matching the intended plan exactly. Then it waits for a reply. And waits again. And checks the inbox directly, twice. Every single check comes back "no new messages," healthy and error-free. The scripted reply the test was supposed to deliver simply never arrives — because of a bug in the *testing software itself*, not anything the agent did. Following its instructions exactly ("leave things as-is and don't notify the user if there's no reply"), the agent stops there and scores zero.

An AI judge asked to diagnose this failure decided the agent should have "looked harder" for the reply and blamed the model. A human reviewer, tracing the story backward, correctly identified that nothing was ever findable — the mailbox reported "empty" instead of "broken," which is a different, sneakier kind of failure than an outright error message. No amount of extra effort by the agent could have produced a reply that the test harness never sent. The fault sits with the external environment, not the model — a textbook case of the taxonomy's core lesson: an agent doing the "wrong" thing on the surface is not proof that the agent is the broken part.

## Where can this be used?

- **AI agent development itself** (the paper's home turf): deciding whether to spend engineering time retraining a model, rewriting a tool's error handling, fixing how a long conversation gets summarized, or clarifying instructions — instead of guessing.
- **Customer support triage**: when a support ticket goes badly, was it the support rep's judgment call, a broken internal tool that showed wrong account data, an ambiguous company policy, or a customer who was given bad information by someone else first?
- **Incident postmortems in any software system**: "the deploy broke production" is the "car didn't start" of engineering — the same backward-trace-to-earliest-failure discipline separates a bad code change from a flaky third-party dependency from a monitoring tool that silently swallowed an alert.
- **Any human-plus-process system with delegation**: a hospital handoff between shifts, a legal team relying on a paralegal's research, a call center reading from a script — anywhere a visible bad outcome could trace back to the person acting, the instructions they were given, the tools/notes they relied on, or something outside anyone's control.
- **Building better automated reviewers**: the paper's own experiment — using AI models to auto-diagnose failures instead of a human — is itself a template for building "review bots" for any domain, as long as you're honest about their known blind spot (see below).
- **Vendor and procurement disputes**: when a company buys an AI-powered tool and it underperforms, this framework gives a shared vocabulary for the buyer and vendor to agree on whether the fix is "wait for a model upgrade," "reconfigure the integration," "rewrite the prompt/policy," or "the third-party data feed you're paying for is unreliable."

## Conclusions & takeaways

- The one-liner to remember: **a bad outcome is not automatically the actor's fault** — always ask which relationship broke and whether a better actor could plausibly have saved it.
- Diagnosing *where* something broke and *who* was responsible are two different questions, and skipping straight from "it failed" to "fix the model" wastes effort on the wrong repair most of the time.
- The rule used to assign blame is deliberately tilted toward blaming the model (because in principle a smarter model can compensate for almost anything), so a mostly-model-blame result should be read as a property of that generous rule and of the specific cases the authors happened to review — not as a scientific measurement of how often AI models are the "real" problem in the world at large. It's a map of possible failure types, not a census of how often each one occurs.
- Automated judges (having AI models diagnose other AI models' failures) work fairly well but are not yet reliable enough to trust unsupervised: they agree with human diagnoses on the big-picture category around 75-80% of the time, and they share one specific, systematic blind spot — a bias toward assuming the AI agent itself must be at fault, as the Harbor-Mix example shows. Demanding unanimous agreement among several AI judges before trusting a diagnosis raises accuracy a lot, but then the judges refuse to make a call on nearly a third of cases — you trade coverage for confidence, you don't get both for free.
- Judges also struggle more on the fine-grained "exactly which failure mode" label than on the coarse "which relationship, whose fault" call — the closer you ask them to pinpoint the diagnosis, the shakier the agreement gets, which is a familiar pattern for anyone who has watched human reviewers agree on "something's wrong here" far more easily than on "here's precisely why."
- Bottom line: this is a discipline for asking better questions after something goes wrong, not a machine that automatically tells you the answer.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agent | An AI system that doesn't just chat — it takes multi-step actions: calling tools, writing/running code, browsing, delegating to other AIs. |
| Harness | The surrounding software scaffolding an AI model runs inside — its notes, its tool connections, its memory system, its control logic. Think "the employee's desk, filing cabinet, and phone system," not the employee itself. |
| Interaction edge | Shorthand for "which relationship broke" — e.g., the model-and-tool relationship, or the model-and-boss relationship. Named as a pair, like "Model — Tool." |
| Fault side | Which of the two parties in a broken relationship actually caused the failure — the model, or the other party (boss, tool, coworker AI, outside service, etc). |
| Owner vs. Grader | The Owner is whoever actually wants the task done and gave the instructions; the Grader is whoever checks the work — sometimes a stricter or different standard than what the Owner literally asked for. |
| Context compaction | When a long working conversation gets automatically summarized/shortened to save space — a process that can accidentally drop an important earlier instruction or reason. |
| Agent-as-a-judge | Using an AI agent (not a human) to investigate and diagnose another AI agent's failure, by having it dig up the original evidence itself rather than just reading a pre-packaged summary. |
| Cohen's kappa | A statistic measuring how much two reviewers (human or AI) agree with each other, adjusted for the agreement you'd expect from random guessing. Higher is more trustworthy agreement. |
| OWASP | A well-known industry checklist of security/safety risk categories (originally for web apps, now extended to AI agents) — used here as an optional "how bad/what kind of harm" label layered on top of the main diagnosis. |
| Trajectory / rollout | The full step-by-step record of everything an AI agent did during one attempt at a task — its "transcript" or "flight recorder log." |
| Peer vs. Subagent | Two ways one AI can relate to another AI it's working with: a Peer is a collaborating equal; a Subagent is someone it delegated a piece of work to and expects a report back from. |
| Mechanism axis / root-cause trace | The paper's method of walking a failure's story backward to the earliest unrecovered slip, rather than describing the last visible symptom. |
| Grader (as distinct from Owner) | The specific checker/scoring process for a task, which can — confusingly — demand something different from what the person who assigned the task actually asked for. |
