# 05 · Alternatives & competitors (open source)

*What you will learn:* which other tools solve the same problem, what each is best at, and when **Herdr** is the better pick. Only **open source** tools make the table; the last section lists the notable **closed-source** ones so you know they exist.

> **Open source** here means the license is OSI-approved and the source is publicly available (MIT, ISC, AGPL-3.0, etc.). Tools with a "custom" / `NOASSERTION` / "Other" license are called out separately — they may still be free to use, but they are not *open source* in the strict sense.
>
> **AGPL-3.0** means the code is open source, but if you modify it and expose it over a network, you must offer the same source to users of your modified copy. For local/personal use of a terminal this clause rarely matters; it does matter for anyone commercializing a fork that clients connect to.

## Quick table (open source only)

| Tool | License | What it is | One-line "when to pick this instead" | Best fit |
|---|---|---|---|---|
| **tmux** | ISC | The classic (since 2008) terminal multiplexer; sessions, windows, panes, hooks, scripting — no UI, no agents, config in `.tmux.conf`. | You want the most portable, best-documented, most-hackable base to script and you do **not** want a mouse UI. | Remote boxes, Linux servers, heavy scripting |
| **Zellij** | MIT | Rust multiplexer, same job as tmux, nicer default layout, key hints on screen; still no agent awareness. | You want a tmux replacement that is friendlier out of the box and you're OK with keyboard-driven. | Local dev, tmux refugees who don't want plugins |
| **opencode** | MIT | A **coding agent** (the kind of process you run inside a pane). Not a multiplexer at all, but you'll pair it with one. | You need the agent itself (CLI LLM assistant), not a shell manager. | Agent of choice for Herdr / tmux / any terminal |
| **Warp** | AGPL-3.0 | "Agentic development environment, born out of the terminal" — a full GUI terminal product that wraps shells in a Rust UI and can run agents. | You want a polished all-in-one desktop terminal with built-in AI features, and you're OK with a GUI app rather than a `Ctrl+B` prefix model. | Users who want a single vendor's all-in-one; teams that don't care about strict terminal parity |
| **cmux** | GPL-3.0-or-later (self-reported; GitHub parses it as `NOASSERTION`, so confirm before depending on it) | Ghostty-based macOS terminal with vertical tabs + notifications tuned for AI coding agents. | You live on macOS, you like Ghostty, and you want vertical tabs + notifications without a full multiplexer layer. | macOS power users; Ghostty fans |

## Capability matrix (what Herdr's own comparison page claims)

From `herdr.dev/compare/` — read "yes" as first-class support. Where a cell says **n/a** the product is a different kind of thing (agent, IDE, macOS app), so the row doesn't apply meaningfully.

| Capability | Herdr | tmux · zellij | cmux · warp | solo | conductor · emdash · superset |
|---|---|---|---|---|---|
| kind | terminal multiplexer | terminal multiplexer | terminal / IDE | terminal app | agentic IDE |
| work survives UI close | ✓ | ✓ | ✓ | ✗ | varies |
| runs in a terminal | ✓ | ✓ | ✓ | ✓ | ✗/partial |
| **semantic agent state** (working / blocked / done, in the sidebar) | ✓ | ✗ | ✓/partial | ✗ | ✗ |
| detach / SSH handoff | ✓ | ✓ | partial | ✗ | ✗ |
| direct `herdr agent …` commands (read/prompt/wait) | ✓ | ✗ | ✗ | ✗ | ✗ |
| API for agents to call (herdr as a tool) | ✓ | ✗ | ✗ | ✗ | ✗ |
| worktree / diff review | ✗ | ✗ | ✗ | ✗ | ✓ |

Take the "solo / conductor / emdash / superset" column with a grain of salt — those products are **closed source** (next section) so Herdr's matrix is describing them from outside; treat them as a hint at their positioning, not a verified claim.

## "When to pick Herdr"

- **vs tmux / zellij** — You already live in the terminal. Herdr gives you the same *survives UI close* guarantee **plus** a mouse-first UI, an **agent sidebar** that knows when Claude/Codex/opencode is `working` vs `blocked`, and `herdr agent prompt/wait` so scripts can actually drive the agent. If you just want the shell and don't care about agents, tmux is fine.
- **vs Warp** — Warp is a GUI terminal that *wraps* shells; you can't script it the same way, it's not in a standard terminal, and AGPL-3.0 matters if you fork it into a SaaS. Herdr is a plain terminal program: run it inside Warp, iTerm2, or a bare shell; script it with `herdr pane/run/send-keys/agent`.
- **vs cmux** — cmux is a macOS app that *replaces* your terminal. Herdr is a multiplexer that *renders on top of* any terminal, works on Linux/Windows too, and exposes the agent layer (state tracking + automation) that cmux doesn't. Pick cmux if you want the Ghostty look on a Mac; pick Herdr if you need portability or want to drive agents by CLI.
- **vs opencode** — Not the same job. opencode is the **agent** (the process), Herdr is the **container** that hosts it. Use them together.
- **vs the closed-source "agentic IDEs" (solo, conductor, emdash, superset)** — These promise to *drive* a lot of agents for you inside a GUI. If you prefer a standard terminal where the **same shell commands** work as they always did, and you want to script it rather than buy it, Herdr is the open, terminal-native pick.

## Not open source (listed for completeness)

| Tool | Status | Why it's not in the table |
|---|---|---|
| **solo** (soloterm.com) | Closed macOS app | No public source found |
| **conductor** | Closed (likely) | No public repo identified under the "conductor" name Herdr compares against |
| **emdash** | Closed | No standalone public source found |
| **superset** (`superset-sh/superset`) | License **"Other" / NOASSERTION** on GitHub (no standard OSI license) | "Source-available" but **not open source** under the OSI definition |

## A fair summary

**Herdr** is the only tool in this chapter that hits three boxes at once: *runs as a plain terminal program* (so it works in SSH / any shell / any OS), *survives closing the UI* (server/client split like tmux), and **knows agents exist** (sidebar state + `herdr agent` automation). Pick the other tool the moment one of those boxes stops mattering to you — that's when you don't need Herdr.
