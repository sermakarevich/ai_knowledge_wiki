# 00 · Installing and starting Herdr

*What you will learn:* install Herdr the quick (and the "proper") way, verify it works, start it from a real project, and learn that Herdr is **mouse-first** — the keyboard is optional.

## What Herdr is

Herdr is a **terminal multiplexer for coding agents**, in the tradition of `tmux` but built around running agents:

- It is a **background session server** plus one or more **terminal clients**. Your panes live in the server; you attach a client, work, detach, and the panes (and any agents inside them) **keep running**.
- Inside a session you get **workspaces** → **tabs** → **panes**. Each pane can run a shell, a server, tests, or a long-running coding agent (`claude`, `codex`, `opencode`, `pi`, …).
- It is **mouse-native**: you can split, resize, switch, and close things with the mouse. Keyboard shortcuts exist and are convenient, but they are **optional** — never required.

> If the names "workspace / tab / pane" feel small, that is intentional — we unpack the full model in [01_concepts.md](01_concepts.md).

## Prerequisites
- A terminal (macOS, Linux, or Windows).
- A coding agent you already use (not required for this chapter, but handy for `02_panes.md`).

## Install

### The quick way (recommended)
On Linux or macOS:

```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

On Windows, in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://herdr.dev/install.ps1 | iex"
```

The installer drops a single `herdr` binary on your PATH.

### The "proper" ways (use the one you already use)
| method | command |
|---|---|
| Homebrew (macOS) | `brew install herdr` |
| mise | `mise use -g herdr` |
| Nix (builds from source) | `nix profile install github:herdrdev/herdr/v0.8.2` (replace `v0.8.2` with the latest tag) |
| Manual | download the `herdr-<platform>` asset from the GitHub releases, `chmod +x` it, move it to `~/.local/bin/herdr` |

> Pick ONE installer and then update through that same tool (e.g. `brew upgrade herdr`). Mixing installers leads to confusing duplicate binaries.

## Verify

```bash
herdr --version
```

You should see something like `herdr 0.8.2`. If your shell says `herdr: command not found`, open a new terminal (so the PATH refreshes) or check the install directory is on your PATH.

## Start it from a real project

Run it **in the directory where your code lives** — that directory becomes the starting workspace's project root:

```bash
cd ~/your/project
herdr
```

What happens:
- Herdr **launches (or attaches to) your default background session** automatically. You never touch sockets yourself.
- Because the session has no workspaces yet, it opens **one workspace** automatically, containing **one tab** with **one pane** running your shell.
- You are "in" it: the shell prompt is there, and the mouse can already click things.

## The "just use the mouse" tour (2 minutes)

Do these with the **mouse only** — no keyboard shortcuts needed:

1. **Click any tab, workspace, pane, or agent** in the UI to focus it.
2. **Drag the split border** between two panes to resize.
3. **Right-click a pane** → context menu → `Split right` / `Split down` / `Close`.
4. **Drag-select text** to copy it to your clipboard. **Double-click a token** to copy just that token. (No `Ctrl+Shift+C` needed.)

> That's the whole mental model. The keyboard layer is a convenience for people who want a `tmux`-like flow — we cover it in [02_panes.md](02_panes.md) and [03_shortcuts.md](03_shortcuts.md).

## Detach (and the surprise)

Press `Ctrl+B q` — or **just close your terminal window**. Herdr's server and every pane/agent inside keep running. Come back any time:

```bash
herdr
```

You reattach to the same session, same panes, same agents mid-thought.

> To *end* a session (stop it and its panes), use `herdr server stop` from a shell. We cover this in [04_features.md](04_features.md).

## Where to find more help inside Herdr

| want … | do this |
|---|---|
| every active keybinding | press `Ctrl+B ?` in-pane — a binding list appears |
| a specific command | run the equivalent `herdr …` CLI subcommand (e.g. `herdr panes --help`) |
| the online doc | <https://herdr.dev/docs/> (this tutorial's source of truth) |

## What to do next

Split your first pane, resize it, close it, and detach. You already know enough to work — we'll cover the full vocabulary (workspace/tab/pane/agent/session) in [01_concepts.md](01_concepts.md).
