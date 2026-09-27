> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani — In Plain Language

## What is this about?

This is a short practical rule from engineer Arpit Bhayani for teams letting AI agents write a lot of code.

The rule is simple: you cannot have both maximum AI speed and full human understanding everywhere. So you must choose, file by file and module by module, which one you want.

His post drew wide attention — about 1,258 reactions and 41 comments — because it names a tension many teams feel but rarely state openly: the agent can write 400 lines in ninety seconds, but then nobody really knows whether those lines are correct.

The fix he proposes is to sort every module into one of two buckets before handing anything to an agent.

Bucket one is where speed wins. Bucket two is where understanding wins. You decide up front, and you treat the two buckets very differently.

## Why does it matter?

AI agents change the failure mode of coding.

A normal bug breaks loudly and you notice. A runaway or subtly wrong AI change can look perfectly reasonable, pass a quick glance, and quietly ship — while costing real money and attention.

The source material gives concrete stakes. Agent runs average about $27 per shipped task, versus about $5.50 when they succeed on the first try. One team lost about $3,200 in a single month to tasks that retried themselves into the ground, including one task with 100+ retries costing about $940 and producing nothing.

There are also hard limits: examples cited include a 2,000,000-token-per-day cap plus a 25,000-token per-request cap, where the AI simply stops answering once the cap is hit.

At the same time, human attention is scarce. If you try to deeply review every AI-generated line, you lose the speed benefit. If you review nothing, you ship code nobody understands — especially dangerous in auth, payments, or anything touching data.

The per-module tradeoff matters because it tells you where to spend your limited attention so you get speed where it is safe and safety where it counts.

## How does it work?

The method has three steps: sort, delegate differently, and reinvest the savings.

Step 1 — Sort each file or module into one of two buckets:

- Bucket one: speed matters more than knowing every line. Examples: one-off scripts, internal tooling, throwaway prototypes.
- Bucket two: failure is expensive or hard to reverse. Examples: auth, payments, anything touching data integrity.

Step 2 — Treat agent output differently by bucket:

- In Bucket one, let the agent own the code fully. Do not waste time re-deriving understanding you will never need again.
- In Bucket two, treat agent output as only a first draft. Read the diff line by line, trace how it touches the rest of the system, and make the agent explain its own reasoning before you merge.

Step 3 — Move the time you saved:

Take the hours saved by shipping Bucket one fast, and spend them reading deeply — but only where it counts, in Bucket two. That reallocation is, in Bhayani's words, the whole tradeoff.

Two refinements from the discussion make it work better in practice:

- Use the time while the agent is working productively. Read important code or think through the plan instead of waiting, so you catch expensive mistakes early.
- Expect Bucket one to shrink over time. As the codebase matures and you write better instructions for agents, more code earns Bucket-two-level care or better guardrails.

The surrounding discussion adds one big warning: guardrails, not model choice, decide outcomes. Tests, CI, contracts, linters, and clean transaction handling must push back on wrong code, because the model alone will not.

## Where can this be used?

You can apply this anywhere an AI agent writes code that a human must later maintain.

- Greenfield prototypes: put scaffolding, seed scripts, and demo UI in Bucket one so the agent can move fast.
- Internal tools: admin dashboards, migration scripts, and reporting helpers are classic Bucket-one candidates.
- Core product code: put login, signup, sessions, permissions, billing, and payment webhooks firmly in Bucket two.
- Data layers: schema migrations, data pipelines, and anything that writes to the database of record belong in Bucket two.
- Agent workflows themselves: use Bucket-two review for the prompts, permissions, and automation that let agents run, since a mistake there multiplies.
- Team process: use a short per-module label or code-ownership note so every contributor knows which bucket a file is in before asking the agent to change it.

A simple starting question for any file is: "If the agent gets this subtly wrong, do we lose money, leak data, or corrupt records?" If yes, it is Bucket two.

## Conclusions & takeaways

- You cannot have both AI speed and deep understanding everywhere. Trying to get both means getting neither properly.
- Decide the tradeoff per file or module, before the agent starts — not after the code arrives.
- Let the agent fully own low-stakes code: scripts, tooling, and throwaways.
- Treat high-stakes agent output as a first draft: review line by line, trace side effects, and ask the agent to explain itself.
- Spend speed savings on understanding where it counts, rather than spreading review thinly everywhere.
- Use agent run time for high-value thinking: read core code and sharpen the plan.
- Shrink Bucket one over time as instructions, tests, and guardrails improve.
- Put guardrails outside any single model: passing tests, CI blocks, API contracts, transaction-safe persistence, and vendor separation matter more than which model you pick.

## Jargon decoder

| Term | Plain definition |
|---|---|
| AI agent | A program that writes or changes code on its own from your instructions, often across many files at once. |
| Tradeoff | A choice where gaining one good thing means giving up another — here, speed versus understanding. |
| Module | A separate chunk of the codebase with one job, such as login, billing, or reporting. |
| Bucket one (speed bucket) | Low-risk code where shipping fast matters more than knowing every line. |
| Bucket two (high-stakes bucket) | Important code where a mistake is costly, so a human must review deeply. |
| Diff | The line-by-line list of what changed in the code, which you read during review. |
| Guardrails | Automatic checks — tests, CI, linters, contracts — that block bad code before it ships. |
| CI | An automatic check that runs tests every time code is proposed, blocking merges that fail. |
| Token cap | A hard limit on how much AI text can be used per day or per request, which stops runaway cost. |
| Retry loop | When an agent keeps retrying a failing task on its own, burning time and money without progress. |
