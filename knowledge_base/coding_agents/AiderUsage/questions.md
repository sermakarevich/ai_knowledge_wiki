---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Usage | aiderLinkMenuExpand(external link)DocumentSearchCopyCopied

### Q1. How do you start aider with files to edit, and what does adding files to the chat mean?

> [!tip]- Answer
> Start aider with `aider <file1> <file2> ...`, naming existing files or files to be created. Named files are "added to the chat session" so aider can see their contents and edit them when you request changes. See [[wiki/01-usage|Usage]].

### Q2. What do you do at the aider prompt to make changes, and what does aider show and record afterward?

> [!tip]- Answer
> At the `aider >` prompt, request code changes in natural language and aider edits the added files to fulfil the request. It shows diffs of the changes it makes and git-commits all of its changes for easy tracking and undo. See [[wiki/01-usage|Usage]].

### Q3. Which files should you add to the chat, and why does adding too many hurt?

> [!tip]- Answer
> Add only the files that need editing for the task, since too many files overwhelm and confuse the LLM and cost more tokens. Aider automatically pulls in content from related files and the rest of the repo, so deliberately adding just the edit targets gives the best results. See [[wiki/01-usage|Usage]].

### Q4. How can you add files mid-chat, and can aider run with no files added?

> [!tip]- Answer
> Files can be added mid-chat with the in-chat `/add` command, in addition to naming them on the command line at launch. Aider can also run with no files added, in which case it figures out which files need editing from the request. See [[wiki/01-usage|Usage]].

### Q5. Which LLMs work best with aider, and how do you select or switch models?

> [!tip]- Answer
> Aider works best with Claude 3.5 Sonnet, DeepSeek R1 and Chat V3, and OpenAI o1, o3-mini and GPT-4o, but can connect to almost any LLM including local models. Select the model at launch with `aider --model XXX` plus `--api-key` where needed, and switch mid-chat with the in-chat `/model` command. See [[wiki/01-usage|Usage]].

### Q6. How do you get help inside aider and revert unwanted AI changes?

> [!tip]- Answer
> Use `/help <question>` to ask for help about using aider, customizing settings, troubleshooting, and using LLMs. Revert unwanted AI changes with the `/undo` command, since aider's automatic git commits make every change easy to track and undo. See [[wiki/01-usage|Usage]].

### Q7. Should a developer adopt aider's add-just-the-edit-targets plus auto-commit workflow for everyday coding tasks?

> [!tip]- Answer
> Yes for small scoped edits with a strong model, because naming only the files to edit keeps context focused and cheap while automatic repo context, diffs, and git commits plus `/undo` make iteration safe. Avoid it as a hands-off whole-repo workflow, since over-adding files confuses the model and costs tokens, so large refactors still need deliberate file scoping and diff review. See [[wiki/01-usage|Usage]].
