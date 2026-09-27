> [[index|Wiki]] | [[summary|Summary]]

# Portal by Spotify Cut My Claude Code Token Usage by 90% — In Plain Language

## What is this about?

Imagine you hire a top lawyer at $500 an hour.
Then you ask her to spend the whole day photocopying papers.
She can do it, but you are wasting money.
It would be smarter to hire a cheap assistant for the photocopying
and save the lawyer for hard legal thinking.

That is exactly what this approach does for coding with Artificial Intelligence (AI).
The smart and expensive model (Claude Code) is the lawyer.
It keeps doing the hard thinking.
The cheap and fast model (Gemini Flash) is the assistant.
It does the boring reading and writing jobs.

The tool that makes this possible is called Portal by Spotify.
It lets you create small helpers that run on demand
and take over the grunt work.
You just write down what the helper should do,
pick the cheap model, and Portal runs it for you.
No servers or keys to manage.

## Why does it matter?

When a coding assistant works, most of its time is not smart thinking.
It is reading big files and writing routine text like tests or configs.

Every word the smart model reads or writes costs tokens
(small pieces of text the model charges for).
Reading five large files just to answer one question
can burn thousands of tokens with almost no reasoning.
The pain is not the seat license. It is the tokens.

This is why the bill grows so fast.
A research firm (Gartner, June 2026) expects AI coding costs by 2028
to pass the average developer salary.
Already a quarter of team leaders spend $200-500 per developer per month on tokens,
and some spend over $2,000.
Cutting that waste by 90% means the smart model uses only about one tenth
of the tokens for reading jobs.

## How does it work?

1. Declare two helpers in Portal. One is called bulk-reader.
Its job is: read many large files and answer one question with short bullets.
The other is called code-writer.
Its job is: write tests, configs, or stubs by copying existing patterns.

2. Set strict rules for each helper.
Bulk-reader must output bullets only, no greetings, no extra talk.
Each bullet must start with the exact name, type, or line number.
Code-writer must output only code, no explanations, no extra formatting.
This keeps answers short and clean, so no tokens are wasted on cleanup.

3. Install an automatic redirector called the shunt plugin.
First they tried writing rules in a notes file, but the smart model could ignore them.
Each project also needed its own copy.
The plugin instead enforces the rules, so redirecting happens on its own.

4. Block big reading jobs automatically.
If the smart model tries to open a file longer than 350 lines (you can change this limit),
the read is stopped.
Small exact reads still go through, so fixing one line is not blocked.
Tricks like using shell commands to read big files are also stopped,
but filtered searches still pass because they are also targeted reads.

5. Send the big job to the cheap assistant.
For reading, the files plus your question are packed with labels and sent to bulk-reader.
It is a one-time call, nothing is stored.
The big text goes only to the cheap model, never into the smart model's memory.
A follow-up simply sends the files again.
For writing, a task description plus a required example file are sent to code-writer.
The example is required so the result matches your style instead of generic code.
The result is written straight to disk, so the smart model never even sees it.

6. Keep the hard thinking with the expert.
The block message tells the smart model exactly which helper to call and how.
So even if the smart model never read the guide, the costly read still stays blocked.
The smart model gets back only a short summary,
then continues with reasoning, edits, and decisions.

## Where can this be used?

- Any coding team with large code stores.
The test was on a Java monorepo (one big shared code store) with four scenarios,
comparing direct reads against helper summaries.
- Answering questions that span many files, like "what does this service do",
without opening each file with the expensive model.
- Writing routine output: tests, config scaffolding, type stubs,
and other predictable code that follows existing patterns.
- Outside Spotify and outside coding: the same pattern fits docs writing,
code reviews, and translations.
Helpers are reusable, shareable company-wide as public helpers,
and can be combined into new helpers like a doc writer, reviewer, or translator.
- Any tool that can call the Portal command line and enforce checks can copy this pattern.
You do not need Spotify's setup, only the idea:
one part decides when to redirect, another part does the cheap work.
You can swap the model, instructions, or tools without changing the redirector.

## Conclusions & takeaways

- What to remember in a month: let the cheap model read and write in bulk,
let the smart model think and edit.
The saving comes from the fact that big files go to the cheap model
and only a short summary reaches the smart model.
- The headline result is about 90% fewer tokens used by the smart model
for bulk reading on average.
No per-scenario numbers were published,
and this was an author-run test on one repo, not an independent lab test.
It also did not measure quality or speed, only token drop.
- Honest limits: you cannot delegate editing,
because helper summaries do not include line numbers you can trust.
Claude must still do small exact reads before changing code.
You cannot delegate deep thinking — the helper once missed a subtle thread-safety bug
that the smart model found in seconds.
So debugging, design choices, and safety-critical code stay with the smart model.
- Added waiting time: each redirect adds 10 to 30 seconds of network delay,
and one call is capped at 30 seconds, so large jobs must be split.
Small files are not worth redirecting, which is why the 350-line limit exists.
- To try it yourself you install two plugins, run a setup command to log in,
and use the public helpers with no extra setup.
If you copy a public helper, your copy wins automatically.

## Jargon decoder

| Term | Plain meaning |
| --- | --- |
| Token | A small chunk of text the model reads or writes. You pay for how many it handles. |
| Frontier model | The smartest, most expensive model. Here it is Claude Code, saved for hard thinking. |
| Worker model | The cheap, fast model. Here it is Gemini Flash, used for boring reading and writing. |
| Mode | A small declared helper in Portal, with written instructions, a chosen model, and settings. |
| Hook | An automatic check that runs before an action and can stop it, e.g. stop opening a huge file. |
| Skill | A short guide that tells the smart model when and how to call a helper. |
| Ephemeral runtime | A short-lived computer that runs one job then disappears, like AWS Lambda (Amazon's on-demand compute service) but for agents. No servers to manage. |
| MCP | Model Context Protocol — a standard way to plug extra tools into the helper. |
| CLI | Command-Line Interface — a text-based way to run commands, here the Portal command line. |
| Monorepo | One large shared code store for many parts of a project, here a Java one used for testing. |
| Temperature | A setting for how creative vs strict the model is. Low value like 0.2 means strict and predictable. |
