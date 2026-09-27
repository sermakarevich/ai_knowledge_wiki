> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Usage | aiderLinkMenuExpand(external link)DocumentSearchCopyCopied — In Plain Language

A plain-language guide to starting and running an aider session:
which files to give it, what to type, how it edits safely, and how to pick the AI model behind it.

## What is this about?

Aider is a command-line helper that edits your code for you while you chat with it.

You start it by naming the files you want changed, for example `aider factorial.py`.

Those files are "added to the chat session," which simply means aider can read and rewrite them.

You then type a request in everyday language at the `aider >` prompt, such as
"make a program that asks for a number and prints its factorial."

Aider rewrites the files, shows you exactly what changed, and saves each round
of changes with git so you can review or undo them.

You can also add files in the middle of a conversation with `/add`,
run aider with no files at all and let it guess what to touch,
and switch AI models with flags or the `/model` command.

## Why does it matter?

Most AI coding tools either edit too blindly or force you to paste code back and forth.

Aider's usage pattern solves three everyday problems at once.

First, focus: you tell it exactly which files are allowed to change,
so it does not wander across your whole project.

Second, cost and clarity: every file you add is sent to the AI model,
so adding only what matters keeps answers sharper and token bills lower.

Third, safety: because every edit comes with a visible diff plus an automatic
git commit and an `/undo` command, experimenting feels low-risk.

In short, the way you launch and talk to aider is what makes it fast,
cheap, and trustworthy instead of chaotic.

## How does it work?

Think of one aider session as four steps: launch, ask, review, adjust.

**1. Launch with the files you want to change.**

```text
aider <file1> <file2> ...
```

The names can be files that already exist or files you want aider to create.
Aider opens, reports its version, which models it is using,
how many files are in your git repo, and how much repo context it holds.
Then it waits at the prompt.

```text
$ aider factorial.py

Aider v0.37.1-dev
Models: gpt-4o with diff edit format, weak model gpt-3.5-turbo
Git repo: .git with 258 files
Repo-map: using 1024 tokens
Use /help to see in-chat commands, run with --help to see cmd line args
───────────────────────────────────────────────────────────────────────
> Make a program that asks for a number and prints its factorial
```

**2. Ask for the change in plain words.**

Type what you want at the `aider >` prompt. No special syntax is needed.
Aider reads the added files, gathers background from related files on its own,
and rewrites the added files to match your request.

If you forgot a file, add it mid-chat:

```text
/add other_file.py
```

You can also start with no filenames. Aider then infers which files need edits
from your words, which is handy for small questions and explorations.

**3. Pick the brain behind the tool.**

Aider works best with strong models such as Claude 3.5 Sonnet,
DeepSeek R1 and Chat V3, or OpenAI o1, o3-mini, and GPT-4o,
but it can connect to almost any model, including ones running locally.

Choose at startup:

```text
aider --model o3-mini --api-key openai=<key>
aider --model sonnet --api-key anthropic=<key>
aider --model XXX
```

Or switch without restarting, inside the chat:

```text
/model sonnet
```

Stuck? Ask `/help <question>` about settings, models, or troubleshooting.

**4. Review diffs and rely on automatic saves.**

Every edit appears as a diff, so you see added and removed lines.
Aider git-commits its changes automatically, which makes them easy to track.
If you dislike the last AI edit, revert it with:

```text
/undo
```

Then ask again with clearer instructions.

## Where can this be used?

- Creating a brand-new script by naming a file that does not exist yet and describing what it should do.
- Fixing or extending one or two known files without pasting code into a browser chatbot.
- Exploring an unfamiliar repo: start with no files, describe the goal, and let aider propose which files to edit.
- Iterating quickly on a feature: keep the chat focused on the same few files while aider pulls background from the rest.
- Switching models mid-task: start cheap or local, then switch to a stronger model for a tricky edit.
- Recovering safely from bad AI output using diffs, git history, and `/undo` instead of manual repair.

## Conclusions & takeaways

- Name only the files that need editing; aider fetches the surrounding context by itself.
- Talk to aider like a junior teammate: short, concrete requests work better than huge vague ones.
- Keep an eye on diffs and commits rather than blindly accepting output; the safety net only helps if you review it.
- Choose a capable model for hard work and switch freely; the usage pattern stays the same.
- When in doubt, ask `/help`, add one more file with `/add`, or undo with `/undo` and try again.

## Jargon decoder

| Term | What it really means |
|------|----------------------|
| Chat session | The current conversation with aider, including the files it is allowed to see and edit. |
| Add to the chat | Give aider permission to read and rewrite a file, via the command line or `/add`. |
| Repo-map | A short automatic summary of your whole project that helps the AI find relevant code. |
| Token | A small chunk of text the AI reads; more files means more tokens and higher cost. |
| Model | The AI engine doing the thinking, e.g. GPT-4o, Claude Sonnet, DeepSeek, o3-mini. |
| API key | A secret password that lets aider use a paid AI model. |
| Diff | A side-by-side view of what changed: lines added versus lines removed. |
| Git commit | A saved snapshot of your files, so you can review history or roll back. |
| `/undo` | A chat command that reverses aider's most recent AI edit. |
| Local model | An AI that runs on your own computer instead of a company's server. |
