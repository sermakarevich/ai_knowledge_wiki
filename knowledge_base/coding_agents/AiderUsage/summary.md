# Usage | aiderLinkMenuExpand(external link)DocumentSearchCopyCopied

**Article:** [Usage](https://aider.chat/docs/usage.html) — aider.chat, n.d.

## Human Readable TL;DR

Aider is like a pair programmer who lives in your terminal: you point it at the files you want changed, tell it what you want in plain English, and it rewrites the code, shows you the diff, and saves the work as a git commit. The trick is to hand it only the files that actually need editing, the way you would hand a chef only the ingredients for tonight's dish, because dumping your whole pantry on the counter just confuses things and runs up the bill. Behind the scenes aider quietly reads the rest of your repo for context and can talk to almost any large language model, so you pick your favourite brain and let it do the typing.

## TL;DR

Aider is a terminal-based AI pair-programming tool launched as `aider <file1> <file2> ...`, where named files are added to the chat session for viewing and editing, with mid-chat file management via `/add` and support for starting with no files while aider infers edit targets. The documented workflow is to add only files needing edits while aider automatically pulls related repo context, request changes at the `aider >` prompt, review shown diffs, and rely on automatic git commits with `/undo` for reverts. Model selection happens at launch via `aider --model XXX` (plus `--api-key` where needed) or mid-chat via `/model`, with best results reported on Claude 3.5 Sonnet, DeepSeek R1 and Chat V3, and OpenAI o1, o3-mini and GPT-4o, alongside support for almost any LLM including local models.

---

## Problem & Motivation

Editing code through a general chat interface forces developers to shuttle context back and forth by hand, pasting files in and copying changes out, which is slow and error-prone on real repositories. The usage page addresses this by presenting aider as a chat loop grounded in the actual codebase: the developer declares which files are in play, aider sees and edits them directly, and every change lands as a tracked git commit with a visible diff. The underlying concern is focus versus context, since giving the model too many files wastes tokens and degrades its judgement, while giving it too few leaves it blind, so the page teaches a deliberate middle path where the user scopes the edit set and aider fills in the surrounding repository understanding automatically.

## Main Original Ideas

1. **Chat session as edit scope.** Files named on the command line (including names of files to be created) become the shared working set that aider can both read and modify, turning the chat into a concrete editing session rather than a detached Q&A.
2. **Minimal explicit context with automatic repo awareness.** The guidance to add only files needing edits, paired with aider's automatic retrieval of related-file content, splits responsibility cleanly: the human decides intent and scope while the tool supplies background context.
3. **Model-agnostic launch and mid-chat switching.** Model choice is treated as a runtime option (`--model`, `--api-key`, `/model`) rather than a fixed dependency, with named best performers alongside broad support for other hosted and local models.
4. **Diff-first, commit-backed editing loop.** Every AI change is shown as a diff and automatically git-committed, with `/undo` as the safety net, so tracking and reverting AI work uses the same mechanism as ordinary development.

## Key Findings

The core command shape is `aider <file1> <file2> ...`, optionally empty, with `/add` extending the working set during a session and `/help <question>` available for usage, configuration, troubleshooting, and LLM questions. Verbatim launch examples cover `aider --model o3-mini --api-key openai=<key>` and `aider --model sonnet --api-key anthropic=<key>`, plus the general `aider --model XXX` form, and the example session header shows aider reporting its version, model pair, git repo file count, and repo-map token budget at startup. The page stresses that overloading the session with unnecessary files confuses the model and inflates token cost, and it documents that aider can operate file-less by inferring edit targets from the request. On the safety side, the combination of visible diffs, automatic commits, and the `/undo` command is presented as the standard way to review, track, and roll back AI-made changes.

## Suggestions & Future Directions

The wiki material summarised here covers only the basics of running aider, adding files, choosing models, and making changes, so natural extensions would be the in-chat command reference, configuration and customisation, troubleshooting, and deeper LLM setup that the `/help` system points toward. Open questions left by this page include how aider selects related-file context, how repo-map budgets scale on large monorepos, and how teams should standardise model choice and file-scoping conventions. A useful follow-up would be worked examples of scoping strategies for common tasks such as refactors, new features, and bug fixes, along with guidance on commit hygiene when every AI edit auto-commits.

## Authors & Institutions

No authors or institutions are named in the wiki material summarised here; the page documents usage of the aider project (aider.chat documentation).
