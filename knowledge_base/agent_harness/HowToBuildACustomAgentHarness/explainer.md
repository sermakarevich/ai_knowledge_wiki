> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# How to Build a Custom Agent Harness — In Plain Language

## What is this about?

This article answers one question: once you have a smart language model,
how do you turn it into a useful helper that can actually do work?

The answer it gives is a short formula:

`agent = model + harness`

The model is the brain. It can think and write text, but on its own it
cannot look things up, run code, or remember yesterday.
The harness is everything around the brain: the scaffolding
(supporting frame) that connects the model to the real world: the tools
it can use, the instructions it follows, and the information it sees
at each step.

The article shows how to build that scaffolding with LangChain's
`create_agent` function. You start with a very small, simple loop —
the model thinks, calls a tool, looks at the result, and repeats until
the job is done — and then you add small add-on pieces called middleware
to shape that loop for your exact job.

## Why does it matter?

A strong model with a bad setup still fails. If it gets too much
information, it gets confused. If it gets too little, it guesses.
If nobody handles errors or safety rules, one bad tool call can break
a whole run.

How well the harness fits the task decides how useful the helper is.
A customer-support helper needs fast answers, strict safety rules, and
access to order records. A coding helper that runs for hours needs
memory, the ability to run and test code, and a way to split big jobs
into smaller ones. The same brain needs a different support frame
for each job.

Starting from a minimal (bare-bones) base instead of a big pre-made
package matters because every task needs different context,
failure handling, rules, and environment. A small base you extend
is easier to shape than a big rigid one you must fight.

## How does it work?

Think of the harness as a work routine with helpers standing at
checkpoints along the way.

Step 1: Start with the smallest working loop.
You call `create_agent` with three things: which model to use, which
tools it may call, and a system prompt (the standing instructions like
"you are a helpful assistant"). That gives you the core loop only:
think, act with a tool, observe the result, repeat.

Step 2: Plug in middleware at the checkpoints.
Middleware (middle-layer software, here small add-on pieces)
hooks into the loop at six points: before and after the model thinks,
before and after a tool runs, and when the whole run starts and ends.
Each piece handles one concern, and pieces can be mixed and matched.

There are four levers (ways to change behavior) a piece of middleware
can pull:

1. Deterministic logic (fixed rules, not AI guesses). For example: use
   a cheap model for easy steps and a strong model for hard ones, adjust
   the instructions on the fly, or tidy up the conversation history.
2. Tool management. Set tools up, clean up after them, and hand the
   model a clean, correct set of tools for this run.
3. Custom state (shared notes the run keeps). Counters, flags, and
   shared data that persist across steps so different pieces can
   coordinate, like "steps used so far: 12".
4. Stream handlers (output routers). Watch the flow of events as they
   happen and send each type where it belongs: word-by-word updates
   to the screen, tool calls to an audit log (record of actions),
   timing data to monitoring.

Step 3: Cover the real-world needs.

A production helper, one that real users rely on, usually needs most
of these eight abilities, each delivered by ready-made reusable pieces:

- Keep the conversation from overflowing the model's memory by
  summarizing or trimming old messages.
- Load knowledge at the start and save what was learned at the end,
  so the helper improves over time.
- Act in an environment: read files, run shell commands (text orders
  to the computer), or run code, instead of only answering in words.
- Split work: hand hard sub-tasks to subagents (smaller helper copies
  with a clean workspace) and track progress with a to-do list.
- Survive hiccups: retry failed tool or model calls with backoff
  (waiting longer between tries) or switch to a backup model.
- Enforce rules every time: hide personal data, check compliance
  (following laws and company rules), and require approvals. These live
  in code, not just in the prompt, so the model cannot talk its way
  around them.
- Let a human steer: pause before a risky action so a person can
  approve, reject, or redirect it.
- Control cost: reuse repeated prompt parts from cache (short-term
  storage) and set limits on how many calls one run may make.

The article's proof is reuse: every helper the LangChain team itself
built — a sales helper, a long-running coding helper, a no-code
builder (a tool that lets non-programmers make helpers) — is the same
small base plus a different stack of these pieces.

## Where can this be used?

- Customer support: fast answers grounded in order and help-center
  data, with strict privacy and approval rules on every call.
- Coding assistants: long sessions that read files, run tests, split
  work across subagents, and keep history short through summarization.
- Sales and marketing helpers: load account notes at startup, draft
  outreach, save outcomes back to memory for next time.
- Data and office work: helpers that read documents, run calculations
  in a code sandbox (a safe isolated space), and ask a human before
  sending anything important.
- Any team building many helpers: write a safety or cost-control piece
  once, then reuse it across every helper in the company.

## Conclusions & takeaways

- Usefulness comes from fit. The model is only half the story; the
  harness around it decides whether it works for your task.
- Start small, then shape. Begin with the minimal think-act-observe
  loop and add one focused piece at a time.
- One concern per piece. Small composable (mix-and-match) pieces are
  easier to test, share, and reuse than one giant custom script.
- Give the right context at the right time. That is the whole job of
  the harness: not more information, but the right information at
  each step.
- Put rules in code, not wishes in prompts. Safety, privacy, approvals,
  retries, and cost limits must fire automatically.
- If you remember one line: build the smallest loop that works, then
  tailor it with middleware until the harness fits the task.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agent | A language model plus its support setup, looping over tools until a job is done. |
| Harness | The scaffolding around the model: tools, instructions, memory, rules, and error handling. |
| `create_agent` | LangChain's starter function that builds the minimal loop from a model, tools, and instructions. |
| Middleware | A small add-on piece that runs at checkpoints in the loop and changes what happens there. |
| System prompt | The standing instructions the model always sees, like its job description. |
| Context window | How much text the model can consider at once; old messages must be trimmed or summarized. |
| Subagent | A smaller helper copy that handles one sub-task with a clean workspace and reports back. |
| Human in the loop | A pause where a person approves, rejects, or redirects before a risky action runs. |
| Prompt caching | Reusing repeated instruction text from fast storage to save time and money. |
| Backoff and fallback | On failure, wait longer between retries, or switch to a backup model or tool. |
