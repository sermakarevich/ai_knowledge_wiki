# Herdr tutorial

A short, hands-on tutorial for **Herdr**, a *terminal multiplexer for coding agents*: instead of a bunch of separate terminal windows, you get **workspaces** holding **tabs**, each tab holding **panes**, and each pane can host a long-running coding agent (Claude, Codex, opencode, pi, …) that keeps running in a background **session** even when you close your terminal. Herdr is **mouse-first** — you can do everything by clicking and dragging — and the keyboard shortcuts are optional.

Retrieve chapters with `ai show research_topics/coding_agents/tutorials/herdr/<chapter>`.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — install Herdr (one-liner, Homebrew, Nix), start it for the first time, and learn that it is mouse-native.
- [01_concepts.md](01_concepts.md) — the mental model in two minutes: workspace, tab, pane, agent, session, client/server, and modes.
- [02_panes.md](02_panes.md) — the main focus: splitting, moving, resizing, zooming, swapping, and closing panes, by mouse and by keyboard.
- [03_shortcuts.md](03_shortcuts.md) — a cheat-sheet of the `Ctrl+B` prefix commands, grouped by task, plus copy mode and prefix-free control.
- [04_features.md](04_features.md) — the power features: detach/reattach, session restore, agent states, the sidebar, remote access (SSH and phone), and notifications.
- [05_alternatives.md](05_alternatives.md) — open-source comparison: tmux, Zellij, opencode, Warp (AGPL-3.0), cmux, plus a "not open source" list (solo, conductor, emdash, superset) and a one-line "when to pick Herdr instead".

## How chapters fit together
`00_setup` gets Herdr running on your machine. `01_concepts` gives you the vocabulary. From there the chapters are standalone — you can jump to `02_panes` when you want to manage splits, `03_shortcuts` for a quick reference, or `04_features` to learn detach, restore, and remote access. Close with [05_alternatives.md](05_alternatives.md) once you want to know *why* Herdr instead of tmux, Warp, cmux, or one of the closed agentic IDEs.

## Local settings (shared by all chapters)
| setting | value |
|---|---|
| binary | `herdr` on your PATH |
| platform | macOS (Apple silicon), Linux, Windows x86_64 |
| install | `curl -fsSL https://herdr.dev/install.sh \| sh` (or `brew install herdr`) |
| launch | `herdr` from the directory where your project lives |
| prefix key | `Ctrl+B` (the keyboard prefix; the mouse covers everything) |
| default session | `herdr` launches or attaches to your local background session automatically |

## Notes
- There is no runnable project in this folder: Herdr is a single binary and a live TUI (text user interface), not a codebase, so there is no Docker/`uv`/`justfile` here. You "run" the tutorials by opening real Herdr panes and trying each command against a real agent.
- Verify a chapter's commands with `herdr --help`, `herdr panes --help`, and inside Herdr with `Ctrl+B ?` (lists every active keybinding).

Verified on: Herdr 0.8.2, macOS, 2026-09-01.
