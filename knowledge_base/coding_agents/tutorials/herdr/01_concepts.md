# 01 · The mental model: workspace, tab, pane, agent, session

*What you will learn:* the six nouns you'll use for the rest of this tutorial, and how they fit together in a three-level containment.

## The three-level containment

```
Session (a background server + its state)
 └─ Workspace (a project: the top folder you care about)
     └─ Tab (a top-level view inside a workspace)
         └─ Pane (a rectangle of terminal you can run a command in)
```

Think of it as: **a session is a running server; a workspace is a project; a tab is a workspace window; a pane is one split in that window**.

## The six nouns

### 1. Session
The **background thing that owns all your work**. It is a server process that:

- keeps running after you detach or close your terminal;
- holds every workspace, tab, pane and agent;
- is re-entered by simply running `herdr` again (no sockets, no port management);
- is *named* — there is a "default" session, and you can also have named sessions (`herdr session start alpha`, `herdr session attach alpha`) and *remote* sessions you connect to over SSH.

Stop it only when you're done with the work it holds: `herdr server stop`.

### 2. Workspace
A **project-level container**, the "big box" around a set of related work. Give each active project its own workspace so the sidebar's per-agent state stays readable.

- A workspace owns **tabs** and **agents running inside it**.
- A new workspace opens with one tab and one shell pane.
- Rename it to reflect the actual project (see `herdr workspace rename <id> <name>` in [04_features.md](04_features.md)).

### 3. Tab
A **top-level view inside a workspace** — like a browser tab. Each tab has its own layout of panes.

- `Ctrl+B c` creates a new empty tab.
- `Ctrl+B n` / `Ctrl+B p` go to the next / previous tab.
- `Ctrl+B 0..9` jumps to a tab by number.
- A tab is NOT the same as a pane: a tab is a *whole window*, a pane is *one split inside that window*.

### 4. Pane
A **single rectangle of terminal** you can run anything in — your shell, a test suite, a server, or a coding agent.

This is the unit you'll use most in [02_panes.md](02_panes.md):

| verb | meaning |
|---|---|
| **split** | divide one pane into two (a *child* pane) |
| **move** | focus a different pane |
| **resize** | change a pane's size (drag a border) |
| **zoom** | temporarily fill the tab with one pane; press again to unzoom |
| **swap** | exchange two panes' positions |
| **close** | end a pane (the process inside gets a SIGHUP) |

**Mouse first.** Every one of those can be done by clicking and dragging. The keyboard layer is for speed.

### 5. Agent
A **long-running coding agent process** running in some pane. Supported: `claude`, `codex`, `opencode`, `pi`, and other CLIs listed in the Herdr [agents](https://herdr.dev/docs/agents/) doc.

- Herdr **detects** the agent as soon as it starts in a pane.
- The **sidebar** shows its state across every workspace: `working` (thinking), `blocked` (needs you), `done`, `idle` (awaiting input).
- You can start one by typing `claude` (or `codex`, or …) into a fresh pane.

### 6. Client / server
- **Server** = the Herdr session itself (`herdr server …`). Lives on one machine, runs forever.
- **Client** = a terminal that *renders* the server's UI. Detach one client, others can still attach.

This is what makes `herdr --remote` and phone-over-SSH work — the client on your phone just renders the same server.

## Modes (a short detour)

Herdr has three "modes" that change how keyboard input is handled:

| mode | how you get there | what it does |
|---|---|---|
| **normal** | (default) | keystrokes go to the pane's process |
| **prefix** | `Ctrl+B` then a key | keys are consumed by Herdr (`v` = split right, `q` = detach, …) |
| **copy (read-only)** | scroll wheel, or `Ctrl+B [` | navigate/select text without touching the pane's scrollback or process input |

You can go **prefix-free**: configure a "prefix-free" binding directly on an action key (e.g. `ctrl+a v = split-h`) — see [03_shortcuts.md](03_shortcuts.md).

## The sidebar

The sidebar is always on and shows, per agent:

- which **workspace** it lives in,
- which **tab/pane** it is in,
- its **state** (working / blocked / done / idle),

…so at a glance you know which project needs your attention.

## A 60-second recap

1. A **session** runs in the background.
2. Inside it, a **workspace** is a project.
3. A workspace has **tabs**; a tab holds **panes**.
4. Any pane can host an **agent**, whose state you watch in the sidebar.
5. Your terminal is a **client** — detach it, and the server keeps running.
6. **Modes** (normal / prefix / copy) decide where keystrokes go.

Now the chapter this tutorial is mostly about: [02_panes.md](02_panes.md).
