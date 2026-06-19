# Claude Code Worktrees Guide

**Source:** [Claude Code Worktrees Guide](https://claudefa.st/blog/guide/development/worktree-guide)
**Type:** Developer Guide (Claude Code v5.2, optimized for Claude Opus 4.7)

## Human Readable TL;DR

Imagine you're working on a big puzzle, but you need two people to work on different sections at the same time without bumping into each other. Normally they'd fight over the same pieces. Git worktrees are like giving each person their own identical copy of the puzzle to work on simultaneously -- then merging the results at the end. This guide explains how Claude Code uses this trick so that multiple AI "helpers" can work on your code at the same time without accidentally overwriting each other's work.

## TL;DR

Git worktrees enable filesystem-level branch isolation so that multiple Claude Code sessions (or sub-agents) can operate on the same repo concurrently without merge conflicts. The `--worktree` flag creates isolated working directories under `.claude/worktrees/`, each with its own branch. The Desktop app applies this automatically per session; the CLI requires explicit opt-in. Agents can be configured with `isolation: worktree` frontmatter to always run in isolation.

---

## Problem & Motivation

Running multiple Claude Code sessions simultaneously against a shared working directory causes merge conflicts and lost context -- two agents that rewrite the same file silently clobber each other. The worktree feature solves this by giving each session (or sub-agent) its own isolated branch and directory, making parallel AI-driven development safe.

---

## Main Original Ideas

1. **`--worktree` CLI flag** -- Three usage patterns: named worktrees (`claude --worktree feature-auth` → dedicated branch + directory), auto-named throwaway worktrees (`claude --worktree`), and mid-session worktree creation on demand.

2. **Desktop auto-isolation** -- The Desktop app automatically places each new session into `.claude/worktrees/` with customizable branch prefixes; no manual flag required.

3. **Sub-agent worktree isolation** -- When Claude spawns parallel sub-agents, each can receive its own worktree. This is the critical enabler for safe batch code migrations where multiple agents rewrite identical files concurrently.

4. **Agent frontmatter `isolation: worktree`** -- Agents defined in `.claude/agents/` can opt into automatic isolation on every execution via a single config field, making it a per-agent policy rather than a per-invocation flag.

5. **Smart cleanup logic** -- Worktrees with no changes are removed automatically; worktrees with changes prompt the user to keep or remove. Supports non-Git VCS via custom hooks (Mercurial, Perforce, SVN).

---

## Key Findings

| Scenario | Use Worktree? |
|---|---|
| Multi-agent parallel work | Yes |
| Feature + bugfix combination | Yes |
| Experimental / throwaway sessions | Yes |
| Single-file fix, focused session | No |

- Core heuristic: "If you'd normally create a separate branch to avoid conflicts, use a worktree instead."
- Parallel agents rewriting identical files is the primary failure mode that worktrees eliminate.
- The Desktop app removes the opt-in friction entirely by defaulting to isolation.

---

## Suggestions & Future Directions

1. Add `.claude/worktrees/` to `.gitignore` to keep the repo clean.
2. Use `git worktree list` and `git worktree prune` for routine maintenance.
3. Configure `isolation: worktree` in agent frontmatter for any agent intended to run in parallel.

---

## Authors & Institutions

Claude Fast (claudefa.st) -- Developer tooling guide, no individual author credited.
