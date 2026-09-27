PDF: https://aider.chat/docs/usage.html (no source.pdf in run; use Source URL)
# Usage | aiderLinkMenuExpand(external link)DocumentSearchCopyCopied
Source: https://aider.chat/docs/usage.html
Kind: article
Fetched: 2026-09-24T04:58:35.283932+00:00
Tool: urllib
Topic: coding_agents

Usage | aiderSkip to main content

  aider

#  Usage

Run aider with the source code files you want to edit.
These files will be “added to the chat session”, so that
aider can see their
contents and edit them for you.
They can be existing files or the name of files you want
aider to create for you.

aider <file1> <file2> ...

At the aider > prompt, ask for code changes and aider
will edit those files to accomplish your request.

$ aider factorial.py

Aider v0.37.1-dev
Models: gpt-4o with diff edit format, weak model gpt-3.5-turbo
Git repo: .git with 258 files
Repo-map: using 1024 tokens
Use /help to see in-chat commands, run with --help to see cmd line args
───────────────────────────────────────────────────────────────────────
> Make a program that asks for a number and prints its factorial

...

Use /help <question> to
ask for help about using aider,
customizing settings, troubleshooting, using LLMs, etc.

##  Adding files

To edit files, you need to “add them to the chat”.
Do this
by naming them on the aider command line.
Or, you can use the in-chat
/add command to add files.

Only add the files that need to be edited for your task.
Don’t add a bunch of extra files.
If you add too many files, the LLM can get overwhelmed
and confused (and it costs more tokens).
Aider will automatically
pull in content from related files so that it can
understand the rest of your code base.

You can use aider without adding any files,
and it will try to figure out which files need to be edited based
on your requests.

You’ll get the best results if you think about which files need to be
edited. Add just those files to the chat. Aider will include
relevant context from the rest of your repo.

##  LLMs

Aider works best with Claude 3.5 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o. Aider can connect to almost any LLM, including local models.

# o3-mini
$ aider --model o3-mini --api-key openai=<key>

# Claude 3.7 Sonnet
$ aider --model sonnet --api-key anthropic=<key>

Or you can run aider --model XXX to launch aider with
another model.
During your chat you can switch models with the in-chat
/model command.

##  Making changes

Ask aider to make changes to your code.
It will show you some diffs of the changes it is making to
complete you request.
Aider will git commit all of its changes,
so they are easy to track and undo.

You can always use the /undo command to undo AI changes that you don’t
like.

## Table of contents

Tips

In-chat commands

Chat modes

Tutorial videos

Voice-to-code with aider

Images & web pages

Prompt caching

Aider in your IDE

Notifications

Aider in your browser

Specifying coding conventions

Copy/paste with web chat

Linting and testing

Editing config & text files
