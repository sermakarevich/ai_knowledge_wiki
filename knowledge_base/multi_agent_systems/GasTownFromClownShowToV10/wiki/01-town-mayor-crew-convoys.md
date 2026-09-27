> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Town: Roles, Convoys, and the Daily Loop

**In one sentence:** Gas Town runs 20–30 coding agents as a self-managing factory town with seven worker roles, per-project rigs, mail-based messaging, and delivery-tracking convoys driven through tmux.

## Key points

- The Town (`~/gt`, Go binary `gt`) is HQ; each managed git repo beneath it is a Rig, and the human is the Overseer — the eighth role with their own identity and inbox.
- Seven worker roles split the labor: Mayor (concierge/chief-of-staff), Polecats (ephemeral per-rig task swarm), Refinery (single serializer owning the merge queue), Witness (per-rig babysitter that un-sticks polecats and hustles the Refinery), Deacon (daemon-pinged patrol preacher), Dogs incl. Boot (Deacon's helper crew and its watcher), and Crew (long-lived named personal agents).
- Every unit of slung work is wrapped in a Convoy bead — a delivery-tracking wrapper with a Charmbracelet TUI (Text User Interface, graphics made of text) expanding-tree dashboard — and a convoy can absorb multiple swarm attacks before it lands.
- The core verbs are `gt sling` (hang work on a hook), `gt nudge` (tmux poke that kicks a polite idling agent into reading hook+mail), `gt handoff` (tidy + restart in place), and `gt seance` (revive a predecessor via `/resume` using the session ID saved in the nudge title).
- GUPP (Gastown Universal Propulsion Principle — "if there is work on your hook, YOU MUST RUN IT") plus the nudge hack plus the Deacon's hierarchical heartbeat keep convoys starting, completing, and landing unattended overnight.
- The daily loop is tmux-native (`C-b s` list/snoop, `C-b n/p` cycle crew, `C-b [` scroll, `C-b a` activity feed) and degrades gracefully: no-tmux mode and naked sessions still work, just slower.
- Opinionated cute names are deliberate compression: they make the org chart legible to humans and to the agents themselves.

---

## 1. Town, rigs, and the Overseer

The Town is the operator's home directory (Yegge's is `~/gt`): a separate repo holding Gas Town configuration plus all project rigs beneath it (`gastown`, `beads`, `wyvern`, `efrit`, …). The `gt` Go binary manages and orchestrates workers across every rig.

A **Rig** is one git repo placed under Gas Town management (`gt rig add`). Some roles are per-rig (Witness, Polecats, Refinery, Crew); others are town-level (Mayor, Deacon, Dogs). Rig-level workers can still go cross-rig when needed via `gt worktree`, which grabs them their own clone of another project so they stop stepping on each other's feet.

The **Overseer** is the human — explicitly the eighth role, with a persistent identity and inbox in the system, able to send and receive town mail. The social design note is blunt: "Mayors are there to get yelled at" — close enough to yell at, powerful enough to act.

## 2. The seven worker roles

| Role | Scope | Job |
|------|-------|-----|
| Mayor | town | Concierge/chief-of-staff; kicks off most convoys, gets pinged on landing, reads worker output so you don't have to, holds context/dreams |
| Polecats | per-rig | Ephemeral swarm workers spun up on demand; produce MRs (Merge Requests, proposed code changes), then are fully decommissioned (names recycled) |
| Refinery | per-rig | Owns merging: intelligently merges every change one at a time to main, reimagining changes when the base moved too far |
| Witness | per-rig | Babysitter: hustles polecats to file MRs, hustles Refinery to drain them, peeks at Deacon for stuckness, runs rig-level plugins |
| Deacon | town | Daemon beacon: runs a patrol loop, pinged every couple minutes with "do your job" (DYFJ), propagates the signal downward |
| Dogs (+ Boot) | town | Deacon's personal crew for maintenance and plugin runs; Boot wakes every 5 minutes with the single job of checking the Deacon |
| Crew | per-rig | Long-lived named agents working directly for the Overseer (design partners, back-and-forth work); not managed by the Witness |

Implementation-wise each role is a composition: a Role bead (job description/priming) + an Agent bead (persistent identity) + a Hook bead + an inbox (beads) + a tmux session + daemon supervision.

## 3. Mail and two-tier beads

Town mail and messaging (events) use Beads. There are two levels that mostly don't matter day-to-day — workers route sensibly even given work "from the wrong rig":

- **Rig-level work** is project work: features, bug fixes, split between polecats and crew.
- **Town-level work** is orchestration: patrols (long step-chains encoded as linked beads) and one-shot workflows like releases or cross-rig code-review waves.

Beads has cross-rig routing: `bd create` / `bd show` pick the right database by issue prefix (`bd-`, `wy-`). A mail-budget table caps chatter per role (Polecat 0–1 mails per run, others protocol-only, Dogs zero-mail, nudges for the rest) — because unbounded mail used to mean unbounded commits and races.

## 4. Convoys: the ticketing unit

Everything rolls up into a Convoy: a special bead wrapping a unit of work for delivery tracking. It deliberately does **not** use the Epic (parent/child) structure, because the tracked issues mostly already have another parent — the convoy tracks them by reference.

Flow: `gt sling` hangs work on a worker's hook and a Convoy bead is created around it — from a single polecat fix to a giant swarm. The convoy dashboard (Charmbracelet TUI with expanding trees per convoy) shows each tracked issue. "Landed/finished" means done. A convoy can take several swarm attacks before finishing; whoever manages it (e.g. the Witness) keeps recycling polecats onto its issues. Gate-state trick: a polecat vanishes while waiting on a GH (GitHub) Action / CI (Continuous Integration, automatic checks), and a Gate bead wakes a fresh polecat to continue when the gate triggers.

Why convoys exist: hearing "issue `wy-a7je4` just finished" is meaningless without the larger block it belonged to. The convoy is that block.

## 5. The propulsion loop: GUPP, nudge, handoff, seance

**GUPP** ("if there is work on your hook, YOU MUST RUN IT") is the answer to the core Claude Code problem: sessions end, context fills, work stops. Because agent, hook, and workflow are all persistent beads, any fresh session can resume. Workers are prompted with "physics over politeness": read hook + mail on startup, start working without waiting.

**The nudge** exists because Claude Code is "miserably polite" and often idles waiting for input. `gt nudge` sends a tmux notification that looks like the user typed something, ~30–60s after startup (always within ~5 min while the town runs). That kicks the worker into reading mail and hook.

**Handoff** (`gt handoff` / `/handoff` / "let's hand off"): the worker tidies, optionally mails itself next steps, and restarts its session in place in tmux. GUPP resumes the hooked work automatically.

**Seance** (`gt seance`): fixes lost handoff notes. Because every nudge title carries the Claude Code `session_id`, a successor can spin up a subprocess, `/resume` its predecessor, and ask "where is my stuff?" — talking to dead ancestors.

## 6. The tmux daily loop

tmux is the primary UI and Yegge recommends learning a handful of bindings: `C-b s` (list/snoop/switch sessions), `C-b b` (cursor back), `C-b [` (copy/scroll mode, `ESC` exits), `C-b C-z C-z` (suspend to shell), `C-b n/p` (cycle to next worker, e.g. next Crew member), `C-b a` (activity feed view). Agents themselves can customize tmux on request (views, key rebinds, popups). Remote cloud workers and future GUI/Emacs/web UIs build on the same session substrate.

## 7. Planning throughput: feeding the factory

With 12–30 workers a backlog evaporates in one sitting — so the hardest problem becomes **keeping the factory fed**. Inputs are epics, issues, and molecules (pre-built workflows); outputs include freshly generated plans (Spec Kit / BMAD plans converted to Beads epics, swarmed per-part inside a big convoy). Formulas generate work at scale: the Rule-of-Five formula (every step reviewed 4 extra times with different focus) turns one workflow into hours or days of autonomous hooked work.

**Covers:** Welcome essay roles/convoys/GUPP/workflow sections (Figs 5–8, 14–15) + targeted.md sections 2, 4.
