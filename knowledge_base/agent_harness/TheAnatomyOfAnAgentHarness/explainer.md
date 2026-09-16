> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# The Anatomy of an Agent Harness — In Plain Language

## What is this about?

Think of an Artificial Intelligence (AI) model as a very smart brain in a jar.
It can read text, images, and video, and it can write text back. That is all it does.

It cannot remember things between chats. It cannot run code. It cannot browse
files or install software. On its own, it is not an agent — just a brain with
no hands, no desk, and no notebook.

An agent harness is everything around that brain that lets it actually do work.
Simple formula from the article:

> Agent = Model + Harness

The harness is all the code (programs), settings, and running logic that is
not the model itself. It gives the model a desk to work at, tools to use,
a way to check its own work, and rules it must follow.

The article walks through each harness part by asking: "What do we want the
agent to do, and what must we build around the model to make that possible?"

## Why does it matter?

A raw model is clever but helpless. Without a harness it forgets everything,
cannot touch the real world, and cannot finish big jobs alone.

A good harness turns that cleverness into useful work:

- It gives the agent lasting memory, so work survives after one chat ends.
- It lets the agent act safely — run programs, edit files, use a browser —
  without breaking your computer.
- It keeps the agent sharp over long jobs instead of getting confused.
- It lets the agent check its own work with tests and fix its own mistakes.

The second half of the story matters just as much. Models are trained
(a process called post-training, meaning extra training after the main
training) together with a specific harness, so they become experts at their
own tools but clumsy with different ones. That means picking or tuning the
harness for your task can matter more than picking a smarter model — the
authors jumped from Top 30 to Top 5 on a coding test just by improving
the harness, changing nothing else.

## How does it work?

Here are the building blocks, in plain terms:

1. **A desk with drawers: the file system.** Instead of pasting everything
   into the chat, the agent gets files and folders. It reads data, saves
   drafts, and picks up where it left off. Git (a version tracker for files)
   adds undo history and lets it try risky ideas on a side copy.

2. **Hands: code execution.** Rather than building one button for every
   possible action, the harness gives the agent one universal tool — a way
   to write and run computer code. It works in a loop: think, act with a
   tool, look at the result, repeat. This loop is called ReAct
   (Reason + Act, meaning reason, then act, then observe).

3. **A safe workshop: the sandbox.** Agent-written code runs in an isolated
   (separate, locked-off) mini-computer, not on your laptop. It comes with
   the basics pre-installed: programming languages, file tools, a web
   browser, logs (records of what happened), screenshots, and test runners
   (programs that check whether code works). The agent writes code, runs
   the tests, reads the errors, and fixes things itself.

4. **Notes and fresh news: memory and search.** Since nobody can rewrite the
   model's weights (its built-in knowledge) during a chat, new facts must be
   pasted into its short-term reading window, called context. Memory files
   like AGENTS.md are auto-loaded at the start of each session, and search
   tools fetch new facts (for example, a new software version released after
   the model was trained). MCP (Model Context Protocol, a standard plug for
   connecting AI to outside data) tools like Context7 supply that fresh info.

5. **Fighting tiredness: beating context rot.** As the reading window fills
   up, the model reasons worse — this fading is called context rot. Three
   fixes: compaction (summarize and tidy up when the window gets full),
   tool-call offloading (save huge tool outputs to a file, keep only a
   short preview in view), and Skills with progressive disclosure (load only
   a short summary of each skill first, reveal details on demand).

6. **Stamina for long jobs.** Big tasks need all of the above plus planning
   and double-checking: a plan file listing the steps, hooks (automatic
   triggers that run checks) that run tests after each change, and loops
   that refuse to quit early. One pattern, the Ralph Loop, catches the
   agent when it tries to stop and sends it back with a clean slate and the
   original goal until the job truly passes.

7. **Training and harness grow up together.** Makers of tools like Claude
   Code train their models inside their own harness, rewarding skills like
   file handling and splitting work across helper agents (subagents). Each
   generation gets better inside its home harness — but overfits (memorizes
   one setup too well) to it, so the same model can score much worse in a
   different harness. Smarter models will absorb some harness jobs, but a
   well-built workshop will always help any brain work better.

## Where can this be used?

- **Coding helpers.** An agent that edits a project, runs the test suite,
  reads the failures, and keeps fixing until tests pass.
- **Team-of-agents setups.** Several agents share one file system as a
  common notebook, splitting a big project into parallel pieces.
- **Research and support bots.** Agents that look up fresh documentation
  and library versions instead of guessing from outdated training data.
- **Long-running automation.** Jobs that span many sessions — migrations,
  reports, data cleanup — where files plus version history keep every step
  traceable and resumable.
- **Your own tuned setup.** When an off-the-shelf tool underperforms, build
  a task-specific harness (right tools, clean starting files, strict checks)
  instead of only buying a bigger model.

## Conclusions & takeaways

- The model holds the smarts; the harness makes those smarts useful.
- Build backwards from the behavior you want: need memory, action,
  safety, freshness, focus, and stamina — then add one harness piece
  for each need.
- Files plus version tracking are the foundation; code execution plus safe
  sandboxes give hands; memory, search, and anti-rot tricks keep the mind
  fresh; planning plus testing give staying power.
- Models overfit to the harness they trained in, so the default harness is
  rarely the best one for your task — tuning the harness is high-leverage work.
- Harness engineering is here to stay: even as models improve, a good
  environment, the right tools, lasting state, and verification loops make
  every model faster and more reliable.

## Jargon decoder

| Term | What it means in plain words |
|---|---|
| Harness | All the code, settings, and running logic around the AI model that lets it act |
| Agent | The model plus its harness, working as one helpful unit |
| ReAct loop | Repeat cycle: think, do something with a tool, look at the result |
| Sandbox | A separate, safe mini-computer where risky code can run without harm |
| Context | The short-term reading window the model can see right now |
| Context rot | The model getting worse at thinking as that window fills up |
| Compaction | Tidying up: summarize old chat to free space so work can continue |
| MCP (Model Context Protocol) | A standard plug that connects the agent to outside data and tools |
| Skill | A reusable how-to pack the agent can load only when needed |
| Ralph Loop | A rule that sends the agent back to work when it tries to quit too early |
| Post-training | Extra training after the main training, often inside a specific harness |
| Overfitting (to a harness) | Getting so used to one tool setup that a different setup confuses the model |
