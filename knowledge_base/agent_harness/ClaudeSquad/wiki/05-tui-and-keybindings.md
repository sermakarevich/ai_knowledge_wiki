> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# TUI Views and Keybindings
**In one sentence:** The interface is a Bubble Tea Elm-architecture TUI (`app/app.go:51,183,196,1045`) that pairs a left session list (`ui/list.go:56`) with a right tabbed pane for live tmux preview, git diff, and shell terminal (`ui/tabbed_window.go:33-37,46`), plus centered modal overlays and a bottom keybinding menu, all driven by a single keyboard dispatch.
## Key points
- Elm structure lives in `app/app.go`: `home` struct holds all panes (`app/app.go:51`), `Init` starts spinner plus preview/metadata ticks (`app/app.go:183`), `Update` routes timer/mouse/key/window messages (`app/app.go:196`), `View` joins list + tabbed window + menu + error box and layers overlays via `PlaceOverlay` (`app/app.go:1045`).
- List view (`ui/list.go:56`) stores instances, selection index, and repo counts (`ui/list.go:56-66`), renders status icon + title + branch + `+added/-removed` stats per row (`ui/list.go:117`), and mutates selection via `Up`/`Down` with wraparound (`ui/list.go:266,312`), `Kill` (`ui/list.go:278`), and `MoveUp`/`MoveDown` swap (`ui/list.go:385,395`).
- Terminal embedding (`ui/terminal.go:30`) caches one detached tmux session per instance title (`ui/terminal.go:33,125`), polls visible output with `CapturePaneContent` in `UpdateContent` (`ui/terminal.go:73`), attaches fullscreen via `Attach` (`ui/terminal.go:186`), and implements scrollback with a `viewport` plus `ScrollUp`/`ScrollDown`/`ResetToNormalMode` (`ui/terminal.go:324,334,346`).
- Preview and diff are separate tabs inside `TabbedWindow` (`ui/tabbed_window.go:46`): tab ids are `PreviewTab`/`DiffTab`/`TerminalTab` (`ui/tabbed_window.go:33-37`), only the active tab updates (`ui/tabbed_window.go:107,114,122`), preview shows tmux output or centered `FallBackText` states (`ui/preview.go:53,119`), diff shows colorized `git diff` plus stats in a viewport (`ui/diff.go:43,111`).
- Overlay system centers modal dialogs over a faded background with `PlaceOverlay` (`ui/overlay/overlay.go:47`): `TextInputOverlay` hosts textarea + branch/profile pickers + enter button (`ui/overlay/textInput.go:35`); `BranchPicker` filters git branches with debounced async results (`ui/overlay/branchPicker.go:15,63`); `ProfilePicker` selects harness left/right (`ui/overlay/profilePicker.go:13,44`); `ConfirmationOverlay` gates kill/push on `y`/`n`/`esc` (`ui/overlay/confirmationOverlay.go:9,42`); `TextOverlay` shows help text closed by any key (`ui/overlay/textOverlay.go:9,30`).
- Keybindings are a two-level map: raw strings to `KeyName` in `GlobalKeyStringsMap` (`keys/keys.go:38`) dispatched by `handleKeyPress` switch (`app/app.go:609`): `n` new, `N` new-with-prompt, `D` kill, `enter`/`o` attach, `tab` cycle tab, `c` checkout/pause, `r` resume, `p` push (no `s` binding exists; `s` in older docs maps to current `p`), `q`/`ctrl+c` quit, `?` help, `up`/`k`/`down`/`j` navigate, `K`/`J` reorder, `shift+up`/`shift+down` scroll, `esc` exits scroll/input states, `ctrl-q` is tmux-detach inside attached sessions only (`app/help.go:49,90`).
- Help and menu are data-driven: `Menu` rebuilds its option list from state + instance status + active tab (`ui/menu.go:78,84,98,123`) and renders `GlobalkeyBindings` help text (`ui/menu.go:162`); `app/help.go:36,64,86,95` defines four help screens (general, instance-start, attach, checkout) shown once via bitmask state except general which always shows (`app/help.go:131`), dismissed by any key (`app/help.go:166`).
---
## Elm wiring in app.go
`home` aggregates every pane; no sub-model has its own `Update` (`app/app.go:51`).
```go
// app/app.go:51-104
type home struct {
	ctx context.Context
	program string
	autoYes bool
	storage *session.Storage
	appConfig *config.Config
	appState config.AppState
	state state
	newInstanceFinalizer func()
	promptAfterName bool
	keySent bool
	instanceStarting bool
	startingInstance *session.Instance
	list *ui.List
	menu *ui.Menu
	tabbedWindow *ui.TabbedWindow
	errBox *ui.ErrBox
	spinner spinner.Model
	textInputOverlay *overlay.TextInputOverlay
	textOverlay *overlay.TextOverlay
	confirmationOverlay *overlay.ConfirmationOverlay
}
```
States are `stateDefault/stateNew/statePrompt/stateHelp/stateConfirm` (`app/app.go:40-48`). `Init` (`app/app.go:183`) batches spinner tick, 100ms preview tick, and metadata tick. `Update` (`app/app.go:196`) switches on `hideErrMsg`, `previewTickMsg`, `keyupMsg`, `instanceStartDoneMsg`, `metadataUpdateDoneMsg`, `tea.MouseMsg` (wheel scroll only, `app/app.go:261`), branch-search debounce/result, `tea.KeyMsg` → `handleKeyPress` (`app/app.go:293-294`), `tea.WindowSizeMsg` → `updateHandleWindowSizeEvent` with 30/70 width split and 90/10 height split (`app/app.go:156-181`), `spinner.TickMsg`.
`handleKeyPress` (`app/app.go:387`) order is fixed: menu-highlight echo (`app/app.go:353`), `stateHelp` (`app/app.go:393`), `stateNew` inline title editor (`app/app.go:397`), `statePrompt` overlay delegate (`app/app.go:483`), `stateConfirm` delegate (`app/app.go:568`), `esc` exits preview/terminal scroll mode (`app/app.go:581`), `ctrl+c`/`q` quit (`app/app.go:600`), then `GlobalKeyStringsMap` lookup and `switch name` (`app/app.go:604-609`):
```go
// app/app.go:604-613
	name, ok := keys.GlobalKeyStringsMap[msg.String()]
	if !ok {
		return m, nil
	}

	switch name {
	case keys.KeyHelp:
		return m.showHelpScreen(helpTypeGeneral{}, nil)
	case keys.KeyPrompt:
```
`View` (`app/app.go:1045`) joins padded list + tabbed window horizontally, then menu + error box vertically (`app/app.go:1046-1055`), and conditionally layers exactly one overlay centered (`app/app.go:1057-1072`).
## List view
`List` (`ui/list.go:56`) holds `items`, `selectedIdx`, dimensions, `InstanceRenderer`, `autoyes`, and repo-count map (`ui/list.go:56-66`). `SetSize` propagates width to renderer (`ui/list.go:78`); `SetSessionPreviewSize` resizes each live tmux capture (`ui/list.go:86`). `InstanceRenderer.Render` (`ui/list.go:117`) builds prefix ` %d. `, status glyph (spinner for `Running`/`Loading`, `●` for `Ready`, `⏸` for `Paused`, `ui/list.go:131-139`), truncates title by `runewidth` (`ui/list.go:143-146`), and composes a second line with branch icon `Ꮧ` (`ui/list.go:115`), optional `(repo)` suffix in multi-repo mode (`ui/list.go:188-195`), and green `+N` / red `-M` diff stats (`ui/list.go:154-172`). `String` (`ui/list.go:228`) draws ` Instances ` header plus ` auto-yes ` badge when enabled (`ui/list.go:240-250`), then one entry per instance. Navigation wraps (`ui/list.go:266-275,312-321`); `Kill` kills tmux, decrements repo counts, splices the slice (`ui/list.go:278-304`); `AddInstance` returns a finalizer that registers the repo name after start (`ui/list.go:344-356`).
## Terminal preview
`TerminalPane` (`ui/terminal.go:30`) maps instance title to cached `tmuxSession` (`ui/terminal.go:33`) under mutex (`ui/terminal.go:31`). `UpdateContent` (`ui/terminal.go:73`) returns fallback text for nil/paused/unstarted instances (`ui/terminal.go:77-88`), skips refresh while scrolling (`ui/terminal.go:91-93`), ensures a session (`ui/terminal.go:96`), then `CapturePaneContent` (`ui/terminal.go:106`). `ensureSessionLocked` (`ui/terminal.go:125`) reuses live sessions, drops dead entries, creates `term_<title>` with `$SHELL` or `/bin/sh` (`ui/terminal.go:146-152`), restores or starts it in the worktree (`ui/terminal.go:155-168`), and applies detached size (`ui/terminal.go:177-180`). `String` (`ui/terminal.go:240`) renders scroll viewport (`ui/terminal.go:251-253`), vertically centered fallback (`ui/terminal.go:259-284`), or last-`height` lines of capture padded to fill (`ui/terminal.go:287-299`). Scroll mode captures full history with `CapturePaneContentWithOptions("-","-")` and a footer (`ui/terminal.go:304-321`).
## Preview/diff tabs
`TabbedWindow` (`ui/tabbed_window.go:46`) owns `preview`, `diff`, `terminal`, and `instance` (`ui/tabbed_window.go:53-56`); constructor fixes tab order Preview/Diff/Terminal (`ui/tabbed_window.go:59-70`). `SetSize` shrinks width to 90% via `AdjustPreviewWidth` (`ui/tabbed_window.go:77-79,82`) and subtracts tab bar plus window frame for content height (`ui/tabbed_window.go:89-95`). `Toggle` cycles `activeTab` (`ui/tabbed_window.go:102`). Updates are gated: `UpdatePreview` no-ops unless `PreviewTab` (`ui/tabbed_window.go:107-112`), `UpdateDiff` calls `SetDiff` only on `DiffTab` (`ui/tabbed_window.go:114-119`), `UpdateTerminal` only on `TerminalTab` (`ui/tabbed_window.go:122-127`). `ScrollUp`/`ScrollDown` fan out per tab (`ui/tabbed_window.go:135-165`); predicates `IsInPreviewTab/IsInDiffTab/IsInTerminalTab` drive `esc` handling in `app.go` (`ui/tabbed_window.go:168-180`, `app/app.go:581-597`). `String` (`ui/tabbed_window.go:217`) renders tab headers with active/inactive borders (`ui/tabbed_window.go:229-255`) and switches content (`ui/tabbed_window.go:259-266`).
`PreviewPane` (`ui/preview.go:15`) keeps `previewState{fallback,text}` (`ui/preview.go:24-29`). `UpdateContent` (`ui/preview.go:53`) maps nil → "Spin up a new instance with 'n'" (`ui/preview.go:56`), `Loading` → "Setting up workspace..." (`ui/preview.go:58`), `Paused` → resume hint plus branch clipboard notice (`ui/preview.go:61-75`); otherwise it calls `instance.Preview()` in normal mode or `PreviewFullHistory()` on first scroll entry (`ui/preview.go:83-113`). `String` (`ui/preview.go:119`) centers fallback (`ui/preview.go:124-155`), returns viewport in scroll mode (`ui/preview.go:158-160`), else truncates to `height-1` lines plus `...` (`ui/preview.go:164-182`).
`DiffPane` (`ui/diff.go:18`) wraps a `viewport` plus `diff`/`stats` strings (`ui/diff.go:18-24`). `SetDiff` (`ui/diff.go:43`) shows "No changes" for nil/unstarted (`ui/diff.go:44-55`), "Setting up worktree..." when stats are nil (`ui/diff.go:57-69`), error text on `stats.Error` (`ui/diff.go:71-82`), else green/red counts plus `colorizeDiff` output (`ui/diff.go:88-94`). `colorizeDiff` (`ui/diff.go:111`) paints `@@` hunks cyan, `+` green, `-` red, skips `+++`/`---` metadata (`ui/diff.go:117-129`).
## Overlays
All modals render through `PlaceOverlay(x,y,fg,bg,shadow,center)` (`ui/overlay/overlay.go:47`), which fades background ANSI colors to gray (`ui/overlay/overlay.go:73-94`), centers or clamps coordinates (`ui/overlay/overlay.go:97-127`), and splices foreground lines over background (`ui/overlay/overlay.go:136-171`). `View` (`app/app.go:1045`) calls it for prompt, help, and confirm states (`app/app.go:1061,1066,1071`).
`TextInputOverlay` (`ui/overlay/textInput.go:35`) composes `textarea` + optional `profilePicker` + optional `branchPicker` + enter button, with `FocusIndex` over `numStops` focus stops (`ui/overlay/textInput.go:36-47,70-73`). `HandleKeyPress` (`ui/overlay/textInput.go:180`) routes `tab`/`shift+tab` cycling (`ui/overlay/textInput.go:182-187`), `esc` cancel (`ui/overlay/textInput.go:188-190`), `enter` submit or focus-advance (`ui/overlay/textInput.go:191-213`), other keys to the focused stop (`ui/overlay/textInput.go:215-230`). `Render` (`ui/overlay/textInput.go:298`) stacks profile picker, title + textarea, branch picker, divider lines, and Enter button (`ui/overlay/textInput.go:315-338`).
`BranchPicker` (`ui/overlay/branchPicker.go:15`) holds `results/filter/filterVersion/cursor` (`ui/overlay/branchPicker.go:16-23`); `HandleKeyPress` (`ui/overlay/branchPicker.go:63`) handles up/down/filter typing and reports `filterChanged` for debounced `git.SearchBranches` (`app/app.go:561,891`); `SetResults` drops stale versions (`ui/overlay/branchPicker.go:98-101`); `Render` shows max 5 windowed rows plus `New branch (from HEAD)` (`ui/overlay/branchPicker.go:10,185-209`).
`ProfilePicker` (`ui/overlay/profilePicker.go:13`) holds profiles + cursor (`ui/overlay/profilePicker.go:14-18`), moves on left/right (`ui/overlay/profilePicker.go:44-58`), renders horizontal `name | name` list (`ui/overlay/profilePicker.go:87-109`).
`ConfirmationOverlay` (`ui/overlay/confirmationOverlay.go:9`) defaults to width 50, `y` confirm, `n` cancel, red border (`ui/overlay/confirmationOverlay.go:29-38`); `HandleKeyPress` fires `OnConfirm`/`OnCancel` and returns close flag (`ui/overlay/confirmationOverlay.go:42-60`); `Render` appends "Press y to confirm, n or esc to cancel" (`ui/overlay/confirmationOverlay.go:63-78`). `TextOverlay` (`ui/overlay/textOverlay.go:9`) closes on any key (`ui/overlay/textOverlay.go:30-38`) and renders bordered content at set width (`ui/overlay/textOverlay.go:41-51`).
## Keybinding reference table
Canonical definitions in `keys/keys.go:38-58`:
```go
// keys/keys.go:38-58
var GlobalKeyStringsMap = map[string]KeyName{
	"up":         KeyUp,
	"k":          KeyUp,
	"down":       KeyDown,
	"j":          KeyDown,
	"shift+up":   KeyShiftUp,
	"shift+down": KeyShiftDown,
	"J":          KeyMoveDown,
	"K":          KeyMoveUp,
	"N":          KeyPrompt,
	"enter":      KeyEnter,
	"o":          KeyEnter,
	"n":          KeyNew,
	"D":          KeyKill,
	"q":          KeyQuit,
	"tab":        KeyTab,
	"c":          KeyCheckout,
	"r":          KeyResume,
	"p":          KeySubmit,
	"?":          KeyHelp,
}
```
Dispatch arms in `app/app.go:609-814`; scroll/quit guards precede the map (`app/app.go:581-607`).

| Key | Action | File:line |
|---|---|---|
| `n` | New instance (enter title in `stateNew`) | `keys/keys.go:50`, `app/app.go:641` |
| `N` (shift-n) | New instance with prompt/branch/profile flow | `keys/keys.go:47`, `app/app.go:612` |
| `D` (shift-d) | Confirm then kill selected session | `keys/keys.go:51`, `app/app.go:677` |
| `enter` / `o` | Attach to selected tmux session (terminal tab attaches terminal session) | `keys/keys.go:48-49`, `app/app.go:779` |
| `ctrl-q` | Detach from attached tmux session (tmux-level, not Bubble Tea map) | `app/help.go:49,90` |
| `p` | Push branch (confirm-gated; historic `s` no longer bound) | `keys/keys.go:56`, `app/app.go:716` |
| `c` | Checkout: commit, copy branch, pause session | `keys/keys.go:54`, `app/app.go:739` |
| `r` | Resume paused session | `keys/keys.go:55`, `app/app.go:770` |
| `tab` | Cycle Preview → Diff → Terminal | `keys/keys.go:53`, `app/app.go:673` |
| `q` / `ctrl+c` | Save instances and quit | `app/app.go:600`, `keys/keys.go:52` |
| `?` | General help overlay | `keys/keys.go:57`, `app/app.go:610` |
| `up` / `k`, `down` / `j` | Move selection | `keys/keys.go:39-42`, `app/app.go:661,664` |
| `K` / `J` | Reorder selected instance up/down | `keys/keys.go:45-46`, `app/app.go:754,762` |
| `shift+up` / `shift+down` | Scroll active preview/diff/terminal pane | `keys/keys.go:43-44`, `app/app.go:667,670` |
| `esc` | Exit scroll mode; cancel title input; close confirm | `app/app.go:581,468`, `ui/overlay/confirmationOverlay.go:50` |
| mouse wheel | Scroll active pane when selection is live | `app/app.go:261-278` |

Notes: `ctrl+c` in `stateNew` kills the draft instance (`app/app.go:399`); `ctrl+c` in `statePrompt` cancels the prompt overlay (`app/app.go:485`); `KeyReview`/`KeyPush` enums exist but are unbound (`keys/keys.go:16-17`); menu underline echo skips `shift+up/down` and paused-`enter` (`app/app.go:369-374`).
## Help
General help (`app/help.go:36`) groups Managing (`n/N/D`, arrows, `J/K`, `enter/o`, `ctrl-q`), Handoff (`p/c/r`), Other (`tab`, `shift-up/down`, `q`) (`app/help.go:42-60`). Instance-start help shows branch worktree + program (`app/help.go:64-84`); attach help states the `ctrl-q` detach rule (`app/help.go:86-93`); checkout help explains local commit + clipboard branch + resume (`app/help.go:95-108`). Each type has a seen-bitmask (`app/help.go:109-121`); `showHelpScreen` (`app/help.go:131`) always shows general help but shows others once, storing bits in app state (`app/help.go:144-148`); `handleHelpState` (`app/help.go:166`) closes on any key via `TextOverlay.HandleKeyPress` and resizes (`app/help.go:168-177`). Bottom `Menu` (`ui/menu.go:45`) switches option sets for empty/default/new/prompt states (`ui/menu.go:104-121`); instance rows show `n/D + enter/p/c-or-r + tab/?/q`, collapsing diff/terminal scroll hint and paused-vs-active `r` vs `c` (`ui/menu.go:123-154`); `String` (`ui/menu.go:162`) renders `GlobalkeyBindings` help pairs with group separators and underline on the pressed key (`ui/menu.go:176-226`). Errors surface in `ErrBox` (`ui/err.go:10`), auto-cleared after 3s via `hideErrMsg` (`app/app.go:986-996`); list/preview fallback art is `FallBackText` ASCII logo (`ui/consts.go:5`).
**Covers:** ui/list.go, ui/terminal.go, ui/preview.go, ui/tabbed_window.go, ui/menu.go, ui/diff.go, ui/overlay/*.go, app/help.go, app/app.go (TUI wiring only)
