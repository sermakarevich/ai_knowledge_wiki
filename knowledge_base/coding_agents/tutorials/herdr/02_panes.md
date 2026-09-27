# 02 · Panes: split, move, resize, zoom, swap, close

*What you will learn:* do **everything** to a pane three ways — with the **mouse**, with the **keyboard prefix**, and with the **CLI**. Every action below is given all three ways.

> Reminder: a **pane** is one rectangle of terminal (see [01_concepts.md](01_concepts.md)). A **tab** is the whole window a pane lives in; a **workspace** is the project.

## The verb → three-ways cheat-sheet

| verb | mouse | keyboard (prefix = `Ctrl+B`) | CLI (from any pane) |
|---|---|---|---|
| **split right** | right-click pane → *Split right* | `Ctrl+B v` | `herdr pane split --direction right` |
| **split down** | right-click pane → *Split down* | `Ctrl+B -` (minus) | `herdr pane split --direction down` |
| **move focus** | click the target pane | `Ctrl+B h/j/k/l` (left/down/up/right) | `herdr pane focus --direction <dir>` |
| **resize** | drag the split border | `Ctrl+B r` (enter resize mode, arrow to a border, size with arrows) | `herdr pane resize --direction <dir> [--amount 0.3]` |
| **zoom** | — | `Ctrl+B z` (toggle: one pane fills the tab) | `herdr pane zoom` (or `--on` / `--off`) |
| **swap** | — | `Ctrl+B Shift+h/j/k/l` (swap with neighbor in that direction) | `herdr pane swap --direction <dir>` |
| **close** | right-click pane → *Close* | `Ctrl+B x` (confirms in TUI) | `herdr pane close <pane_id>` |
| **move to new tab** | right-click pane → *Send to new tab* | — | `herdr pane move <pane_id> --new-tab` |
| **move to new workspace** | — | — | `herdr pane move <pane_id> --new-workspace` |

> `--current` targets the pane you're standing in; omit the pane id and Herdr uses the UI-focused pane. `<dir>` is one of `left|right|up|down`.

## Splitting

Start from one pane. Each split gives a **child** pane next to (or below) the focused one.

**Mouse.** Right-click the pane → *Split right* or *Split down*. The new pane appears and focus lands on it.

**Keyboard.**
```text
Ctrl+B v     # split right  (like tmux v)
Ctrl+B -     # split down   (minus key)
```

**CLI** (run inside any running pane — it splits the focused one):
```bash
herdr pane split --direction right
herdr pane split --direction down --ratio 0.7   # take 70% of the width
```

To open the new pane in a **different folder**: `herdr pane split --cwd ~/other/project`.

## Moving between panes

**Mouse.** Just click the pane you want.

**Keyboard** — the four `h j k l` keys (vim-style, where *h* = left, *j* = down, *k* = up, *l* = right):
```text
Ctrl+B h    # focus pane to the LEFT
Ctrl+B j    # focus pane BELOW
Ctrl+B k    # focus pane ABOVE
Ctrl+B l    # focus pane to the RIGHT
```

**CLI:**
```bash
herdr pane focus --direction right
herdr pane neighbor --direction up      # just report the neighbor, don't move
```

## Resizing

**Mouse.** Hover the split border until it highlights, click and drag. Done — this is the way most people resize.

**Keyboard.** First enter "resize mode":
```text
Ctrl+B r
```
Then use the arrow / `h j k l` keys to pick *which* border, and keep pressing in that direction to grow/shrink it; `Ctrl+C` or `Esc` exits resize mode.

**CLI** (non-interactive, scriptable):
```bash
herdr pane resize --direction right --amount 0.25   # move the right border 25%
```

## Zoom (focus one pane, full tab)

Zoom makes a single pane fill the whole tab; unzoom restores the layout. Great for reading a long log or agent output without distraction.

**Keyboard:**
```text
Ctrl+B z      # toggle zoom on the focused pane
```

**CLI:**
```bash
herdr pane zoom            # toggle
herdr pane zoom --on       # force zoom
herdr pane zoom --off      # force unzoom
```

## Swapping two panes

Reposition a pane without moving the *content* into a new pane (the process/agent stays in its pane — only the **position** changes).

**Keyboard** — swap the focused pane with its neighbor in a direction:
```text
Ctrl+B Shift+h     # swap with the pane on the LEFT
Ctrl+B Shift+j     # swap BELOW
Ctrl+B Shift+k     # swap ABOVE
Ctrl+B Shift+l     # swap with the pane on the RIGHT
```

**CLI** — three forms:
```bash
herdr pane swap --direction right
herdr pane swap --source-pane <idA> --target-pane <idB>      # swap two specific panes
```

## Moving a pane (to another tab / workspace)

Different from *swap*: **swap** keeps the same tab, **move** relocates the pane.

```bash
herdr pane move <pane_id> --tab <tab_id>            # into an existing tab
herdr pane move <pane_id> --new-tab                 # into a brand-new tab
herdr pane move <pane_id> --new-workspace           # into a brand-new workspace
```

> Moving a pane is a way to reorganize without losing the running process — the same agent follows it.

## Switching workspaces

A **workspace** is the project-level box (see [01_concepts.md](01_concepts.md)). To jump between workspaces — say, from the `api` project to the `data` one — you have three ways, same as everything else.

**Mouse.** Click the workspace's name in the **sidebar**. That's the fastest path most of the time.

**Keyboard** — open a picker and choose, rather than hunting for a specific hotkey:
```text
Ctrl+B w     # open the workspace navigation panel; pick with arrows, Enter to jump
Ctrl+B g     # goto picker — jump to any workspace, tab, or agent by typing its name
```

**CLI** (from any pane — scriptable, and great for "jump back to project X"):
```bash
herdr workspace list                          # see every workspace and its id
herdr workspace focus api                     # switch to the workspace named "api"
herdr workspace focus 2                       # …or by index (see the list above)
herdr workspace focus api --tab <tab_id>      # …and land on a specific tab there
```

> `focus` by **name** is the form to remember — index shifts as you add/remove workspaces, but a name you gave it (`herdr workspace rename api "api"`) is stable.

## Closing a pane

Closing a pane sends its process a hang-up (SIGHUP); the agent/shell inside is stopped. Confirm before you rely on it.

**Mouse.** Right-click → *Close*.

**Keyboard** (asks to confirm in the TUI):
```text
Ctrl+B x
```

**CLI** (no confirmation prompt — be sure you mean it):
```bash
herdr pane close <pane_id>
```

> Closing a tab's **last** pane closes the tab; closing a workspace's last tab closes the workspace.

## A 30-second exercise

Do these now, alternating mouse and keyboard, and notice both feel identical:

1. Split the current pane to the **right** (mouse).
2. Split the right pane **down** (`Ctrl+B -`).
3. Drag the border between the left and right panes to make the left bigger (mouse).
4. `Ctrl+B z` the bottom-right pane, read it, `Ctrl+B z` again to unzoom.
5. `Ctrl+B Shift+k` to swap the two bottom panes (there should be two — if not, split again).
6. `Ctrl+B x` the smallest pane. Done.

Next: the full keymap as a cheat-sheet in [03_shortcuts.md](03_shortcuts.md).
