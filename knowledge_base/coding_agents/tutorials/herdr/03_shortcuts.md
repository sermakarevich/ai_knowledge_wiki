# 03 · Keyboard shortcuts (cheat-sheet)

*What you will learn:* the full default `Ctrl+B` keymap **grouped by task**, copy mode (scroll and select text), how to change the prefix itself, and how to bind actions to direct chords with no prefix at all.

> In this chapter **`prefix` means `Ctrl+B`**. So `prefix+v` = press `Ctrl+B`, release, then press `v`. Herdr is still mouse-first — these are for speed, not required.
>
> Can't remember a binding? Press `Ctrl+B ?` inside Herdr and it lists **every active binding**; type `/` to filter.

## Learn these five first

These cover most daily movement. Everything else can stay on the mouse.

| action | key |
|---|---|
| New tab | `prefix+c` |
| Split right / down | `prefix+v` / `prefix+minus` |
| Move between panes | `prefix+h` `prefix+j` `prefix+k` `prefix+l` (left / down / up / right) |
| Workspace navigation | `prefix+w` |
| Detach (leave everything running) | `prefix+q` |

## The rest, by task

### Panes

| action | key |
|---|---|
| Zoom the focused pane (fill the tab) | `prefix+z` |
| Close pane | `prefix+x` |
| Swap panes | `prefix+shift+h/j/k/l` |
| Resize mode | `prefix+r` |
| Copy mode | `prefix+[` |

(See [02_panes.md](02_panes.md) for what each pane verb does.)

### Tabs

| action | key |
|---|---|
| Next / previous tab | `prefix+n` / `prefix+p` |
| Jump to tab 1–9 | `prefix+1` … `prefix+9` |
| Rename tab | `prefix+shift+t` |
| Close tab | `prefix+shift+x` |

### Workspaces and session

| action | key |
|---|---|
| New workspace | `prefix+shift+n` |
| Rename workspace | `prefix+shift+w` |
| Close workspace | `prefix+shift+d` |
| Workspace navigation panel | `prefix+w` |
| Goto picker (jump anywhere) | `prefix+g` |
| Toggle sidebar | `prefix+b` |

> Keyboard switching of workspaces is picker-based (`prefix+w` / `prefix+g`); there is no `next/prev workspace` hotkey. The CLI equivalent is `herdr workspace focus <name|index>` — see the "Switching workspaces" section in [02_panes.md](02_panes.md).

## Copy mode (scroll and select)

Press `prefix+[` to enter copy mode on the focused pane. Your scrollback becomes a read-only, navigable surface — the pane's process keeps running and output stays live at the bottom.

| action | keys |
|---|---|
| Navigate | `h/j/k/l`, `w`/`b`/`e` (word), `W`/`B`/`E` (big word), `{`/`}` (paragraph), `PageUp`/`PageDown`, `ctrl+f`/`ctrl+b`, `ctrl+d`/`ctrl+u` (half/full page) |
| Search literal text | `/` (forward), `?` (backward); `n`/`N` to repeat |
| Start a selection | `v` or `Space` |
| Copy the selection | `y` or `Enter` |
| Leave without copying | `q` or `Esc` (`Esc` first clears an active selection/search) |

> Easiest of all: **mouse drag-select copies directly to your clipboard** without ever entering copy mode. Use copy mode when you want to page far back through a log.

## Change anything

Every binding is configurable, including the prefix key itself. In your Herdr config:

```toml
[keys]
prefix = "ctrl+a"
```

That swaps the whole keymap off `Ctrl+B` onto `Ctrl+A` so it doesn't fight other apps.

## Going prefix-free (chords, no prefix)

You can also bind a Herdr action to a **direct chord** that needs no prefix at all — e.g. `ctrl+alt+h` to move focus left. Any chord works, but it has to survive three layers (your OS, your outer terminal like iTerm2/Ghostty, and the program in the pane) before Herdr sees it. `ctrl+alt+…` is almost always a safe family because terminals leave it free.

This keeps the prefix bindings **and** adds direct chords on top:

```toml
[keys]
focus_pane_left    = ["prefix+h", "ctrl+alt+h"]
focus_pane_down    = ["prefix+j", "ctrl+alt+j"]
focus_pane_up      = ["prefix+k", "ctrl+alt+k"]
focus_pane_right   = ["prefix+l", "ctrl+alt+l"]
next_tab           = ["prefix+n", "ctrl+alt+]"]
previous_tab       = ["prefix+p", "ctrl+alt+["]
new_tab            = ["prefix+c", "ctrl+alt+c"]
split_vertical     = ["prefix+v", "ctrl+alt+d"]
split_horizontal   = ["prefix+minus", "ctrl+alt+shift+d"]
zoom               = ["prefix+z", "ctrl+alt+z"]
```

If a direct chord does nothing, your terminal or desktop swallowed it — free the chord in the terminal's settings or pick a different one here.

## Where to see the whole thing

- Inside Herdr: `Ctrl+B ?` (live, filtered with `/`).
- Config + binding syntax: the [keybinding reference](https://herdr.dev/docs/configuration/#keybindings).
- The online keymap page: <https://herdr.dev/docs/keyboard/>.

Now the last chapter — the power features (detach/restore, agent states, remote, notifications) — in [04_features.md](04_features.md).
