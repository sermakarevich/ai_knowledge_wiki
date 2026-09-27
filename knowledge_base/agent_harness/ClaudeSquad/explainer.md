> [[index|Wiki]] | [[summary|Summary]]

# Claude Squad — In Plain Language

## What is this about?

Imagine a restaurant kitchen where instead of one cook, you have ten robot cooks all working at once. If they all shared one counter and one copy of the recipe, they would bump into each other, spill things, and overwrite each other's work.

Claude Squad is like the kitchen pass — the central counter where the head chef watches every dish — combined with air-traffic control. Each robot cook gets its own separate counter with its own clean copy of the recipe. The head chef (you) stands at one screen, sees all ten counters at a glance, and switches attention with a single keypress.

In real terms, it is a terminal app that runs several AI coding assistants in parallel. Each assistant works in its own isolated copy of your code, and you manage them all from one keyboard-driven screen.

## Why does it matter?

The everyday problem is simple: AI coding assistants are useful, but running more than one at a time is messy. Put two of them in the same folder and they overwrite each other's files. Put them in background windows and you lose track of who is doing what — who is stuck, who finished, who needs approval.

Normally you would juggle this by hand: copy folders, open extra windows, remember which window was which task, clean up afterwards. That is slow and error-prone, and one mistake can wipe out good work.

If this works, one person can supervise many assistants the way one chef supervises many cooks. You start several attempts at once, pause one, check another's work, push a third's result for review, and shut down the ones that went wrong — all without leaving your keyboard and without manual cleanup.

## How does it work?

Think of opening a new counter for each robot cook:

1. You walk into the kitchen (you open the app inside your project folder) and pick which kind of robot cook to use.

2. You press one key to hire a new cook. The kitchen builds a fresh counter for them — a separate copy of the recipe book (your code) so they cannot mess up anyone else's dish.

3. Each cook is put in their own glass booth with a camera. You can watch any booth live from the central screen, even while all the others keep cooking.

4. The central screen refreshes on a timer, showing who is busy, who is waiting for your approval, and what each cook has changed so far.

5. When a dish looks good, you press one key to send it upstairs for tasting (save and share the changes). When a dish goes wrong, you press one key to close that counter and send the cook home.

6. When you leave for the night, the booths and counters stay exactly as they were. When you come back, everything is still there — unless you order a full cleanup, which tears everything down at once.

No cook talks to another cook. There is no master plan or task list. It is just: create, watch, pause, resume, share, shut down — capped at ten cooks at a time.

That is the whole trick: separate counters prevent messes, glass booths let you watch, and one control screen keeps ten cooks manageable.

## Where can this be used?

- Trying three different fixes for the same bug at once, then keeping the best one.

- Running one assistant on documentation, one on tests, and one on a new feature — all in parallel.

- Testing different AI assistants side by side on the same task to see which does better.

- Reviewing work safely: each assistant's changes stay in its own copy until you approve them, so the main code stays clean.

- Outside coding: any work where several AI helpers need their own isolated copy of some files — for example, drafting several versions of a report, a lesson plan, or a legal memo from the same starting template, then comparing the results.

- Brainstorming alternatives: asking several assistants to solve the same problem in different ways, then mixing the best ideas.

- Teaching or demos: showing a group how parallel AI workers behave, with every worker visible on one screen.

## Conclusions & takeaways

What to remember a month from now: Claude Squad is a simple control tower for parallel AI coding assistants — one isolated workspace plus one isolated terminal session per assistant, all visible in one keyboard-driven screen. Its strength is isolation plus visibility, not smart coordination.

The big idea travels well: give every AI worker its own sandbox, keep the controls in one place, and make start, watch, pause, and share each a single action. You do not need a complex scheduler to get most of the benefit of parallel assistants.

Honest limitations: it does not plan tasks, split work between assistants, or let assistants talk to each other. It holds at most ten assistants at once.

It only works inside a code project folder, needs extra tools installed to run, and one broken saved record can hide all the others on restart. It is a single-person console, not a team orchestration system — there is no task queue, no dependencies, and no multi-machine support.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| tmux | A tool that runs several separate terminal sessions in the background, like glass booths each cook works inside |
| git worktree | A separate folder copy of your code project, so each assistant edits its own copy without collisions |
| worktree / branch | A worktree is the folder copy; a branch is the labeled line of changes that copy belongs to |
| TUI (Terminal User Interface) | An app you control with the keyboard inside a text-only terminal window, with panels and menus but no mouse windows |
| Bubble Tea | A toolkit for building keyboard-driven terminal screens in the Go programming language |
| PTY (Pseudo-Terminal) | A fake terminal screen that lets a program run as if a person were typing, even when it runs in the background |
| autoyes | An automatic "yes, keep going" mode so the assistant does not stop to ask permission at every step |
| gh CLI (GitHub Command Line Interface) | The official text-command tool for sending code to GitHub (GitHub CLI) and opening review requests |
| daemon | A quiet helper program that keeps running in the background, here used to auto-approve waiting assistants |
| profile | A saved preset naming which AI assistant to launch and with what command |
