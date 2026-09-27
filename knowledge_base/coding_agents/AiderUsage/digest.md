> [[index|Wiki]] | [[summary|Summary]]

# Usage | aiderLinkMenuExpand(external link)DocumentSearchCopyCopied — Digest

## 1. [[wiki/01-usage|Usage]]

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

## The argument in five moves

1. Start by naming the files to edit on the command line so aider can see and change them.
2. Ask for the change in natural language at the `aider >` prompt and let aider perform the edits.
3. Keep the chat focused on only the files that need editing to avoid confusing the model and wasting tokens.
4. Rely on aider to pull in related-file and repo-wide context automatically, or to infer target files when none are named.
5. Choose a capable model at launch or switch mid-chat, then review diffs and rely on automatic git commits plus `/undo` for safe iteration.
