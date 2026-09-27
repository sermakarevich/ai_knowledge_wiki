# 04 · The power features

*What you will learn:* the things that make Herdr more than "tmux with a mouse": named **sessions**, **agents** it drives directly, **remote** access (SSH and phone), **notifications**, and **plugins**.

> The mouse covers all the day-to-day layout work (see [02_panes.md](02_panes.md)). This chapter is about the deeper layer: keeping work **alive**, **watching** agents, and **reaching in from anywhere**.

## Sessions: work that outlives your terminal

A **session** is the background server that owns everything. You usually just run `herdr` and it attaches to your **default** session. Named sessions let you keep several projects separated:

```bash
herdr --session api          # launch/attach a session called "api"
herdr session list           # see running sessions
herdr session attach api     # attach to it from another terminal
herdr session stop api       # stop it (and its panes/agents)
herdr session delete api     # remove its state
```

**Detach and come back.** `Ctrl+B q` — or just close your terminal — leaves every pane and agent running. Re-run `herdr` (or `herdr --session api`) and you're dropped back in mid-thought. That single idea is most of why people switch from raw terminal windows to a multiplexer.

> `herdr server stop` ends the **server itself** (all sessions). Use it when you're truly done on this machine, not between tasks.

## The agent layer

Herdr *knows* an agent is running in a pane and can act on it — not just watch it. Start a supported CLI (`claude`, `codex`, `opencode`, `pi`, …) in a pane and Herdr detects it, labels it, and exposes it:

```bash
herdr agent list                       # every detected agent
herdr agent read <target> --lines 40   # read an agent's output
herdr agent prompt <target> "fix the flaky test" [--wait]
herdr agent wait <target> --until done # block until it settles
herdr agent rename <target> refactorer # give it a name
herdr agent attach <target>            # jump into that agent
```

`--wait` on `agent prompt` blocks until the agent produces a settled state, then continues your script. This is the automation seam: Herdr scripts the **agents**, while `pane run`/`send-keys` script plain terminals.

| agent state (sidebar) | means |
|---|---|
| `working` | thinking / running a turn |
| `blocked` | waiting on you (approval or a question) |
| `done` / `idle` | finished / ready for input |
| `unknown` | agent present but Herdr can't classify it |

## Notifications

Have Herdr ping you (a toast on the client, optionally a sound) instead of you polling the sidebar:

```bash
herdr notification show "Build finished" --body "3 failed" --sound done
```

Pair it with an agent that finishes long work and you get a "needs you" ping the moment it's `blocked` or `done`.

## Remote: same server, other place

Because the server and the client are separate, you can drive the **same** session from elsewhere:

```bash
herdr --remote workbox                       # attach over SSH, using YOUR local keybindings
herdr --remote workbox --remote-keybindings server   # use the server's keymap instead
herdr --remote workbox --handoff             # seamless client handoff
```

- **Remote SSH box:** run the server on the GPU box; attach from your laptop. Detach and the box keeps cooking.
- **Phone / tablet:** SSH in with any terminal app that speaks a pty; the client just renders the server. No extra install.
- **Local terminal, different screen:** `herdr server` on the machine, `herdr session attach <name>` from the other one.

> `--handoff` swaps a live pane from one client to another without dropping it — handy for "walk to the desk".

## Plugins and integrations

- **Extensions:** `herdr plugin link <path>` (local dev) or `herdr plugin install <owner>/<repo>` (GitHub); `herdr plugin action list`. Plugins add tools Herdr can launch from the UI.
- **Office integrations** (Slack, GitHub, etc.) live under `herdr integration …` — they let agents or scripts call external services by name.
- **Config:** `[keys]` remaps any binding, `[ui.toast]` controls notification delivery. See the [config reference](https://herdr.dev/docs/config-reference/).

## A final mental map

```
            herdr  (client — your terminal; detach/reattach freely)
                │
herdr server  ─┬─  session "api"      ── workspace ── tab ── panes ── agents (watched in sidebar)
                │
                └─  session "data"    ── workspace ── tab ── panes ── agents
                │
      --remote  ─► the SAME server, rendered from another machine / your phone
```

Everything in this tutorial reduces to that picture: a **client** rendering a **session** (the server), that holds **workspaces → tabs → panes**, each pane possibly running an **agent** you can watch, prompt, or reach from anywhere.

That's it — you now have the full mental model, the pane verbs, the whole keymap, and the power features. Re-open [03_shortcuts.md](03_shortcuts.md) whenever your muscle memory needs a nudge.
