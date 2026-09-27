> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# smixs/agent-second-brain — In Plain Language

## What is this about?
Think of it as a personal assistant that lives inside your chat app
and keeps your notes tidy for you.

You send it everyday stuff — a voice memo recorded while walking,
a quick text, a forwarded post, a photo of a whiteboard.
It turns that raw material into neat, connected notes
inside your own digital notebook (an Obsidian vault).

The big idea is simple: "you talk, the agent files."
You never open a separate app, learn commands,
or sort things into folders yourself.

It runs day and night on a small rented computer (a VPS),
paid for with a flat monthly fee of about $25.
There is no per-message meter running in the normal case,
because it reuses one long-running chat session
instead of starting a fresh billed request every time.

A concrete example: you say "Call with Alisher — they want
the pilot pushed to July, remind me Friday to send the contract."
The assistant updates the client card, links it to the project,
sets the Friday reminder, and on Friday it pings you
with the reminder plus the background context.

## Why does it matter?
Most note-taking systems fail for the same boring reason:
keeping them organized takes more effort than doing the work.

Voice memos pile up unheard. Good ideas drown in chat history.
Note folders grow into a mess nobody can search.

This project removes the organizing step entirely.
Capture becomes almost free — a five-second voice note —
and the assistant does the filing, linking, and reminding.

It also matters where your notes live.
Everything is stored as plain text files on your own server,
so you can read them forever, with or without the assistant.
Nothing depends on a third-party app that might shut down
or change its prices.

Finally, the flat price matters.
Instead of a surprise bill that grows with every message,
you pay roughly $20 for the assistant subscription,
$5 for the small server, and nothing extra for voice transcription
on the free tier. The cost stays the same
whether you send ten notes or a hundred.

## How does it work?
In five everyday moves:

1. **You talk in Telegram.** That is the whole interface.
   No categories, no commands, no extra app to open.
   Voice, text, photos, documents, and forwards all count,
   and nothing you send is quietly ignored.

2. **One long-lived helper does the filing.**
   Instead of waking up a new helper for every message,
   the system keeps one assistant session open around the clock
   and feeds it your messages. That session writes plain notes
   into your notebook and connects related cards together.

3. **Your memory is organized like a garden, not a pile.**
   Every note gets a type (idea, client, project, lesson, goal).
   Important things stay front and center; older things slowly
   fade through stages — active, warm, cold, archived —
   the way human memory fades. Touching a note brings it back.
   Old notes can even resurface next to new ones
   to spark unexpected connections.

4. **The garden tends itself.**
   The system builds index pages, fixes broken links,
   merges duplicates, and gives the whole notebook
   a health score, so the collection stays navigable
   instead of rotting over time.

5. **Reminders and night shifts run separately.**
   A second helper session handles scheduled reminders
   and a nightly review, so a reminder never interrupts
   an ongoing conversation. A watchdog plus a daily
   green-or-red health report keep the whole thing honest:
   broken jobs switch themselves off and tell you.

Getting started is deliberately ordinary:
make a private copy of the project, get two keys
(one for the chat bot, one for voice transcription),
then run one install command. The installer asks
a few questions, sets up background services,
and messages you when the bot is alive.

## Where can this be used?
- **Busy founders and freelancers:** speak client updates
  on the go, get client cards, follow-ups, and reminders
  without evening admin work.
- **Students and researchers:** dictate ideas and lessons,
  ask "what did I write about this last week?",
  and turn a rough idea into a structured project note.
- **Anyone with a messy notebook:** forward articles,
  photos, and files, and get back filed summaries
  instead of an ever-growing inbox.
- **Privacy-minded note-takers:** keep journals, goals,
  contacts, and finances on your own machine
  as plain files you fully control.
- **Routine-driven people:** say "remind me Friday at 3pm"
  or "every weekday at 6:30pm check my inbox folder"
  and let plain-language schedules replace a task-manager app.
- **Nightly reviewers:** get an evening report of what
  the day meant — what was classified, which goals moved,
  what is worth remembering tomorrow.

## Conclusions & takeaways
The core trick is not fancy: make capturing cheaper
than forgetting, and make organizing someone else's job.

By combining a chat app you already use, a notebook
you already own, one always-on session, and a memory
layer that forgets on purpose, the project turns
a stream of voice and text into knowledge you can reuse.

If you remember three things, remember these:
your notes stay yours as plain files; your costs stay flat;
and your memory stays alive because it is allowed to fade,
resurface, and repair itself.

## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Second brain | A trusted place outside your head where ideas, notes, and reminders live |
| Obsidian vault | A folder of plain-text notes that link to each other like a personal wiki |
| Telegram bot | The chat contact you talk to; it is the only screen you ever need |
| Persistent session | One helper that stays logged in all day instead of being rehired per message |
| Headless call | A one-off background request; this project avoids them to avoid extra billing |
| Knowledge graph | Notes connected by links, so clients, projects, and ideas point at each other |
| Ebbinghaus decay | A rule for forgetting: unused memories fade over time, reused ones last longer |
| Memory tiers | Fading stages (core, active, warm, cold, archive) that decide how visible a note is |
| MOC (Map of Content) | An auto-made index page that gathers links on one topic |
| Watchdog / doctor | A babysitter and a daily checkup that restart stuck parts and report green or red |
| VPS | A small rented computer on the internet that runs your assistant 24/7 |
| Cron / ticker | A scheduler that fires reminders and nightly jobs at the right time |
