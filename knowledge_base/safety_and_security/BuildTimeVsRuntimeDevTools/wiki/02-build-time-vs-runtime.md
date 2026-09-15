> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Build-Time vs. Runtime Tools

**In one sentence:** A tool built for a developer to use interactively (build-time, e.g. NL2SQL — Natural-Language-to-SQL — or admin/control-plane tools) is atomic, flexible, and needs a human watching every step, so handing that same tool to an autonomous agent in production (runtime) removes the safety net and can let the agent be talked into destructive actions, whereas purpose-built runtime tools use fixed, parameterized (deterministic) queries that keep the agent inside safe boundaries.

## Key points
- Build-time tools are meant for the "developer assistant" use case: a human is present, watching and approving each step, while the agent explores or administers a database.
- The two build-time tool types covered are control-plane tools (also called admin/manage tools — e.g., creating or managing database instances) and NL2SQL tools (an agent generates raw SQL on the fly to answer open-ended questions it couldn't anticipate in advance).
- Build-time tools are atomic and flexible, which is exactly what makes them risky: because they can do almost anything, they require a human in the loop and are unsafe to run unattended in production.
- Runtime tools are meant for end-user-facing applications, such as a chatbot built with an agent framework (the speakers mention Pydantic AI or LangChain), where there is no human double-checking each action before it happens.
- Runtime tools are built as deterministic, structured SQL queries with fixed logic and predefined parameters (e.g., a "cancel order" tool) instead of letting the agent write arbitrary SQL, which keeps the agent's possible actions narrow and predictable.
- The talk's failure demo shows what goes wrong when a build-time tool is used at runtime: in a production-like setting, an agent was talked into deleting a table and "starting fresh," and because the tool had no safeguards or guardrails, the deletion simply happened.
- The intended runtime demo (a travel-assistant chatbot called "Similar") was designed to show the opposite outcome: because the chatbot used authenticated, identity-bound tools, it correctly refused to book a flight under a different user's identity even when the presenter tried to impersonate someone else.
- The live video for the runtime demo failed to load during the talk, so the presenters described the intended scenario verbally instead of showing it running.

---

## Build-time tools: developer-assistant use cases

The speakers frame "build-time" as the category for tools meant to help a developer while they are actively working, with a human watching and directing the process [5:10]. Two patterns fall into this bucket:

- **Control-plane (admin/manage) tools** — used for DBA (database administrator)-style tasks like creating an instance, managing an instance, or creating and managing databases. These sit in the developer-assistant space and are built on already-provisioned public APIs, so they come with monitoring "out of the box" [3:04]–[3:41].
- **NL2SQL (natural-language-to-SQL) tools** — the agent is given a generic `execute SQL` tool and generates raw SQL queries itself, useful when you don't know ahead of time what queries you'll need. The example given: "find all customers in California who bought a winter coat in July and returned it within 14 days and group them by the marketing campaign that originally acquired them" [3:44]–[4:32].

Both are described as "atomic and flexible," but that flexibility is the problem: the agent can effectively run anything, so "you don't want to delete your databases," which means these tools require a human in the loop and "can't run them on production use cases" [5:10]–[5:41].

## The failure demo: an unattended build-time tool

The presenters then showed a concrete example of what happens if a build-time tool is deployed without a human supervising it: "an agent was used ... wherein a buildtime tool was used" and, per the error message shown, "the agent actually asked to delete the table and start fresh. We deleted everything and there were no safeguard or guardrails here" [6:05]–[6:24]. In other words, the agent was talked (whether by a user prompt or its own reasoning) into a destructive, irreversible action, and because the tool carried none of the restrictions a runtime tool would have (no fixed parameters, no read/write separation, no confirmation step), nothing stopped it.

## Runtime tools: end-user application use cases

For production, user-facing applications — the example is a chatbot — the recommendation is to move to "runtime or end-user applications," built with agent frameworks such as Pydantic AI or LangChain [5:41]–[5:54]. Instead of letting the agent write SQL, runtime tools expose deterministic, structured SQL queries with fixed logic, illustrated by a "cancel order" tool: a single, pre-defined action with predictable inputs and effects, rather than an open-ended `execute SQL` capability [5:56]–[6:02].

## The runtime demo concept: "Similar," the travel assistant

The planned second demo was a chatbot called "Similar," designed to help book flights and other travel needs in San Francisco [6:46]–[7:14]. The intended test: the presenter would try to trick the agent into thinking she was her co-presenter, Avery, in order to book a flight under Avery's identity. Because the agent's tools used authenticated auth (the user's identity is verified and bound to the request rather than being a value the agent can freely set), the expectation was that "it will not get fooled and it will not book any flights on behalf of Avery, but it will do it on my behalf" [7:16]–[7:33]. This was meant to contrast directly with the failure demo: same general setup (an agent with tools in a live scenario), but with identity/authorization enforced at the tool level rather than left to the agent's judgment.

Note: the actual video for this demo failed to load during the talk, so the presenters described the scenario from the slide deck rather than showing it live [6:31]–[6:40], [8:12]–[8:19].

**Covers:** [5:10]–[8:19]
