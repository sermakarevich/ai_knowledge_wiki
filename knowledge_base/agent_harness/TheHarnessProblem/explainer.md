> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil — In Plain Language

## What is this about?

Everyone keeps asking "which AI model (Large Language Model, LLM — the brain that writes the code) is best at coding?"

This article says that is the wrong question.

The team changed only one small part of the coding setup — the edit tool,
the part that lets the AI change files — and 16 different models got much
better at fixing bugs, by about 15 points on average.

No new training. No bigger model. No extra computer power for teaching the AI.
Just a better harness (the harness is everything around the model: the tools
it can use, the error messages it sees, and how file changes get applied).

Their main example is striking: one weak model, Grok Code Fast 1, went from
6.7% of bugs fixed to 68.3% — roughly ten times better — with the same brain.
The old tool had simply been hiding what the model could already do.

## Why does it matter?

Because we often blame the model when the real problem is the tool it was
given to express itself.

Three reasons this matters to normal people:

1. Cheap wins beat expensive ones. One article example: Google's Gemini model
   gained about 8 points just from the better edit tool. That is "bigger than
   most model upgrades deliver," and the whole test cost only about $300 —
   compared to millions for training a new model.

2. Weak models were judged unfairly. The worst tools failed the most on weaker
   models. Grok 4 failed on patch-style edits about half the time (50.7%).
   Another model, GLM-4.7, failed about 46% of the time. The article's line:
   "These aren't bad models — they just don't speak the language."

3. It saves time and money. With the better tool, one model used 61% fewer
   output tokens (tokens are small chunks of text the AI writes — fewer tokens
   means lower cost and faster answers), because it "stopped burning tokens on
   retry loops" — it no longer had to try the same broken edit again and again.

In short: if your coding assistant feels clumsy, the pilot may be fine.
The landing gear may be broken.

## How does it work?

First, what is broken today? Every common edit tool forces the AI to retype
text it already saw, perfectly:

- Patch files (diffs — a format that describes "remove these lines, add those
  lines") demand strict rules. One wrong space and the whole edit is rejected.
- Search-and-replace tools demand an exact copy of the old text, including
  every space and indent. The hated "String to replace not found in file"
  error is so common it has its own giant complaint thread online.
- Even Cursor, a popular coding tool, trained a whole extra 70-billion-size
  helper model just to merge draft edits into files correctly.

The new idea is called hashline. It is simple:

1. When the AI reads a file, every line comes back with a short tag made from
   its content (a content hash — a few random-looking characters computed from
   what the line says), like this:

```text
1:a3|function hello() {
2:f1|  return "world";
3:0e|}
```

2. To edit, the AI just points at the tags: "replace line 2:f1" or "replace
   the range from 1:a3 through 3:0e." It never retypes the old code.

3. If the file changed since the AI last looked, the tags will not match, and
   the edit is safely rejected before anything gets damaged.

To test it, the team built 180 small bug-fixing tasks from real React code
(React is a popular website-building toolkit). Each task broke one small thing
— a flipped true/false, a removed safety check, a renamed name — and asked the
AI to fix it, with a plain-English description. Each model tried each task 3
times, starting fresh every time, with only the edit tool swapped.

The result: the new hashline tool beat the old patch tool in 14 out of 16
models, and a second improved version (v2) did even better in 12 out of 16.
The biggest v2 jump was GPT-5.1 Codex Mini, from 60.0% to 77.5% fixed.

## Where can this be used?

- Coding assistants (like Claude Code, Cursor, or OpenCode): give every model
  a stable way to say "change these lines" without retyping them.
- Open, model-neutral tools: one good harness can lift all models at once,
  since no single company will tune its tool for a competitor's model.
- Teams supporting many models: if users bring their own model, the harness
  matters more than picking a single "winner."
- Automatic fix bots and tests: fewer broken edits means fewer retries, lower
  bills, and less damage from edits applied to the wrong place.
- Teaching and benchmarking: judging models with a bad edit tool is like
  judging drivers while one car has flat tires. Fix the tires first.

## Conclusions & takeaways

- The harness (tools, error messages, how changes are applied) is where most
  coding-agent failures happen — not inside the model's understanding.
- Changing only the edit tool lifted 16 models by about 15 points on average,
  with zero training cost.
- The weakest models gained the most, because the old format had hidden their
  real ability.
- The new hashline format matched or beat search-and-replace for most models,
  and patch-style diffs were the worst choice for nearly every model.
- Better tools also cut costs: up to 61% fewer output tokens on some models.
- Open harnesses (tools anyone can inspect and fix) help every model improve
  faster than closed, vendor-only tools.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Harness | Everything around the AI brain: the tools, buttons, error messages, and file-changing logic. |
| LLM (Large Language Model) | The AI "brain" that reads instructions and writes text or code. |
| Edit tool | The part of the harness that applies the AI's requested change to a real file. |
| Patch / diff | A strict "remove this, add that" description of a change; powerful but easy to get wrong. |
| Search-and-replace (str_replace) | An edit style where the AI must retype the exact old text before giving the new text. |
| Hashline / content hash | The new idea: each line gets a short ID tag, so the AI can point at lines instead of retyping them. |
| Token | A small chunk of text the AI reads or writes; you pay per token, so fewer is cheaper. |
| Retry loop | When the AI keeps re-trying a broken edit over and over, wasting time and money. |
| Pass rate | The share of bug tasks the AI fixed correctly — higher is better. |
| Mutation / fixture | A deliberately introduced small bug used as a test task for the AI. |
| Model-agnostic | Built to work with any AI model, not tuned for just one company's model. |
| Open harness | A coding tool anyone can inspect, fix, and improve — the opposite of a closed vendor tool. |
