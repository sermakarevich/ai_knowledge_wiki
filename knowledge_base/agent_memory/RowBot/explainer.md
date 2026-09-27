> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# siddsachar/row-bot — In Plain Language

Row-Bot is a desktop assistant that helps you do real work with AI models,
your own notes and memory, and practical tools — while keeping your data
on your own computer instead of sending it to someone else's server.

Its name is also its job description: Reason, Orchestrate, Work.

## What is this about?

Row-Bot is a program you install on your Windows, Mac, or Linux computer.

Instead of chatting with an AI on a website, you chat with it in a desktop
app that can also look at your files, remember things for you, run
repetitive jobs on a schedule, and connect to messaging apps.

Think of it like a helpful office assistant who sits at your desk, learns
where everything is, and can call in specialists when a job gets big.

It works with many different AI models: ones running on your own machine,
big commercial ones you access with a key, monthly subscriptions you log
into, or models your company hosts itself.

There is no Row-Bot account, no Row-Bot cloud computer doing the thinking,
and no built-in tracking of what you do.

## Why does it matter?

Most AI assistants live on the web, which means your files, messages,
and secret keys travel to someone else's computers.

Row-Bot flips that around: your files, passwords, and memories stay on
your machine by default, and only the question you ask goes to whichever
AI provider you chose.

That matters for privacy, for working without an internet connection,
and for people who handle sensitive documents, code, or client work.

It also matters for control. You pick the model for each task, you see
the goal it is working toward, and you set limits on how long it can run
and how many helpers it can call before it must stop and ask you.

For bigger projects, that combination of privacy plus visible,
limited teamwork is hard to find in a single tool.

## How does it work?

You start by talking to Row-Bot in its chat window, much like any chatbot.

Behind the scenes, here is what happens, step by step:

1. You give it a job, for example "turn my inbox into an action plan"
   or "prepare a report from these spreadsheets."
2. Row-Bot picks a focused role for the job, called an Agent Profile,
   and shows you the goal so you can see what it is aiming for.
3. For a small job it just answers. For a big job, the main assistant
   splits the work and hands pieces to smaller helper assistants.
4. The main assistant stays in charge: it collects the helpers' results,
   asks you for approval when something is risky, and saves checkpoints
   so it can recover if something goes wrong.
5. Helpers that write code each get their own folder to work in. Only one
   writer is allowed in the same folder at a time, so they do not
   overwrite each other's work, but different folders can proceed in parallel.
6. Row-Bot does not load every tool at once. It keeps a small set of core
   tools ready and searches for extra abilities only when your request
   needs them, which keeps things fast and safe.
7. Long conversations are measured against the model's memory limit. Older
   turns are squeezed down into a saved summary, while the newest message
   and unfinished tool steps are kept whole, so nothing breaks halfway.
8. When it needs an AI model, it sends your request only to the provider
   you selected — a local model, a key-based service, a subscription
   login, or your own custom address — and labels clearly which is which.
9. Your keys and login tokens are kept in your computer's built-in
   password storage, not in plain files. Restarting the app safely closes
   unfinished steps instead of repeating them blindly.

Installing it is meant to be simple: a one-click installer on Windows
and Mac, or a single install command on Linux.

## Where can this be used?

- Everyday productivity: sorting email, planning from an inbox, writing
  reports, or turning rough notes into polished documents and slides.
- Coding help: connecting a local code folder, reviewing changes, writing
  tests, preparing branches and pull requests, with approvals before
  anything risky runs.
- Design and presentations: drafting slide decks, mockups, landing pages,
  and storyboards, with templates, charts, and image generation built in.
- Repeating jobs: scheduled tasks, alerts, and step-by-step pipelines that
  run in the background and notify you when done.
- Messaging on the go: connecting Telegram, WhatsApp, Discord, Slack, or
  text messages so you can ask Row-Bot things and approve steps remotely.
- Research and learning: searching the web, reading papers, transcripts,
  and documents, while building a personal knowledge collection that
  remembers people, projects, and ideas over time.
- Private or offline work: using local models for sensitive material, so
  documents never have to leave your machine to get summarized or organized.

## Conclusions & takeaways

Row-Bot is best understood as a private, do-the-work assistant rather
than just a chat window.

Its three big ideas are simple: think carefully through messy information,
coordinate the right tools and models, and do the work where your files
already live.

The local-first design is its strongest promise: no account, no central
server doing the thinking, and secrets kept in your system's own safe.

The trade-off is responsibility. You choose the models, approve risky
actions, and manage budgets and limits — the app gives you the dials,
but you still drive.

If you want one desktop place to chat, remember, automate, code, design,
and message with your choice of AI behind it, Row-Bot is built for that.

## Jargon decoder

| Term | What it means in plain language |
|------|---------------------------------|
| Local-first | Your data and settings live on your computer first, not on a company's server. |
| Agent Profile | A preset role, like "researcher" or "coder," that tells the assistant how to behave for this job. |
| Goal Mode | A visible statement of what the assistant is trying to achieve, so you can check its aim. |
| Child agent | A temporary helper the main assistant creates for one piece of a bigger task. |
| Checkpoint | A saved snapshot of progress and approvals, so work can pause and safely resume. |
| Work budget | A limit on time, steps, or helpers that keeps long jobs from running forever. |
| Capability loading | Picking only the tools needed for this request instead of loading everything at once. |
| Context compaction | Squeezing older chat history into a shorter summary so long talks still fit the model's memory. |
| Provider | The company or local program supplying the AI brain, such as OpenAI, Anthropic, or Ollama. |
| MCP / plugin / skill | Extra add-on abilities, like connecting a new app or teaching Row-Bot a repeatable trick. |
| Computer Use | An optional feature that lets the assistant click and type on screen for you, with extra permission. |
| Worktree / workspace | A separate folder copy where a coding helper can work without disturbing your main files. |
