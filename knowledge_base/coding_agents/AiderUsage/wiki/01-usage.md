> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Usage

**In one sentence:** Run `aider <files>` to add editable files to the chat, ask for changes at the prompt, and aider edits, diffs, and git-commits them using your chosen LLM plus automatic repo context.

## Key points

- Run aider by naming the files to edit on the command line (`aider <file1> <file2> ...`); named files are "added to the chat session" so aider can see and edit them, including files to be created.
- At the `aider >` prompt, request code changes in natural language and aider edits the added files to fulfil the request.
- Add only the files that need editing: extra files overwhelm/confuse the LLM and cost more tokens; aider automatically pulls in content from related files and the rest of the repo.
- Files can also be added mid-chat with `/add`, and aider can run with no files at all, inferring which files need editing from the request.
- Best results come from deliberately adding just the files to edit while aider supplies relevant context from the rest of the repo.
- Aider works best with Claude 3.5 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o, but can connect to almost any LLM including local models.
- Select the model at launch with `aider --model XXX` (plus `--api-key` where needed) and switch mid-chat with the in-chat `/model` command.
- Aider shows diffs of its edits, git-commits all of its changes for easy tracking/undo, and `/undo` reverts unwanted AI changes.

---

## Running aider

Start aider with the source files to edit:

```text
aider <file1> <file2> ...
```

These files are "added to the chat session" so aider can see their contents and edit them; they may be existing files or names of files to create. Example session header (verbatim):

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

Use `/help <question>` to ask for help about using aider, customizing settings, troubleshooting, using LLMs, etc.

## Adding files

To edit files, "add them to the chat" by naming them on the aider command line or with the in-chat `/add` command. Only add files that need editing for the task — too many files overwhelm and confuse the LLM and cost more tokens. Aider automatically pulls in content from related files to understand the rest of the code base, so the guidance is: think about which files need editing, add just those, and aider includes relevant context from the rest of the repo. Aider can also run with no files added, figuring out which files need editing from the request.

## LLMs

Aider works best with "Claude 3.5 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o" and "can connect to almost any LLM, including local models". Launch commands (verbatim):

```text
# o3-mini
$ aider --model o3-mini --api-key openai=<key>

# Claude 3.7 Sonnet
$ aider --model sonnet --api-key anthropic=<key>
```

Or run `aider --model XXX` for another model; switch models during the chat with the in-chat `/model` command.

## Making changes

Ask aider to make changes to the code; it shows diffs of the changes it makes. "Aider will git commit all of its changes, so they are easy to track and undo." Unwanted AI changes can be reverted with the `/undo` command.

**Covers:** Usage: running aider with files, adding files to chat, LLMs, making changes
