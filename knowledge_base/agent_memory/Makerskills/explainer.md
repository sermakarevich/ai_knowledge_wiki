> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# coreyhaines31/makerskills — In Plain Language

## What is this about?

Think of makerskills as a toolbox of about 20 ready-made assistants
that live inside your AI coding helper (Claude Code, Codex, Cursor, and similar tools).

Each "skill" is really just a well-written instruction document
that tells the AI how to handle one everyday founder job:
thinking through a hard decision, researching a topic,
organising notes, drafting posts or slides,
checking company money, or finding a website name.

You trigger one by typing a short command like `/decide`,
and the AI walks you through the steps and saves the result to disk.

The whole project is summed up in one line from its own docs:
"AI agent skills for the personal operator's craft" —
in other words, helpers for the small team or solo founder
who does a bit of everything.

## Why does it matter?

Founders and independent operators repeat the same tricky workflows
over and over: decisions, research, note-taking, content, money check-ins.

Without help, that work is slow, inconsistent, and easy to lose.
A decision made in chat disappears. Research has no sources.
Meeting notes never reach the knowledge base.

Makerskills matters because it turns those one-off chats
into repeatable routines with saved results:
decisions get a revisit date, research gets citations,
notes get filed in a vault, money gets a regular cadence.

It also keeps things shareable: the instruction documents are public
and generic, while your personal details stay in a private folder
on your own machine, so updating the toolbox never wipes your data.

## How does it work?

The core idea is simple: a skill IS a document.

Each skill is a file called `SKILL.md` — plain text with steps
the AI follows when you call it. There is no app to build
and no compile step; improving a skill means editing text.

Working with it follows the same rhythm every time:

1. You state what you want ("I need to think through a decision").
2. A routing list points you to the right skill
   (a table of about 21 "I want to..." rows, e.g. decision → `/decide`,
   stuck → `/unstuck`, video → `/watch-video`, messy terminal output → `/paste`).
3. The skill asks structured questions, does the work,
   and writes a tidy result to disk — input becomes output becomes archive.
4. Skills call each other by name instead of duplicating work,
   so a video summary can flow into your notes,
   or a business idea can flow into a domain-name search.

A good first try is `/decide`: it needs no setup,
asks a handful of questions picked from a 38-question decision list,
and saves your answer with a date to revisit it.

Setup has two halves: install the plugin with two commands
(add the marketplace, then install makerskills),
then point one setting at your private folder
(`MAKERSKILLS_CONFIG`, usually `~/.config/makerskills`).
Extra tools and keys are optional and only needed
for the skills you actually use.

## Where can this be used?

Anywhere a founder or small team leans on an AI assistant:

- **Big choices:** weigh a hire, a product fork, or a purchase
  (`decide`), brainstorm a business idea on 9 dimensions
  (`business-brainstorm`), or get a mock board of famous founders
  to argue it out (`maker-council`).
- **Getting unstuck:** when something feels impossible,
  classify the blockage and brainstorm at least 10 fresh angles (`unstuck`).
- **Learning and memory:** research with citations (`deep-research`),
  pull notes from books (`read-book`) or videos (`watch-video`),
  file everything in a personal vault (`second-brain`)
  or a shared team vault (`company-brain`).
- **Making things:** plan social posts across accounts (`jab-hook`),
  build branded slide decks (`slide-deck`),
  turn a call transcript into tasks and a reply draft (`ingest`).
- **Running the business:** track projects across tools (`pm`),
  model household money scenarios (`personal-cfo`),
  run a monthly or weekly company money check (`company-cfo`),
  clean pasted output for Slack or LinkedIn (`paste`).
- **Extending the system:** make a new skill (`skillify`),
  connect an outside service or API (`toolify`),
  or put a job on a schedule (`loopify`).

Skills come in personal/team pairs
(personal notes vs. team notes, household money vs. company money),
so the same habit scales from solo work to team work.

## Conclusions & takeaways

- Makerskills is documentation first, automation second:
  the written workflow is the product, and the AI just runs it.
- Its power comes from routine, not magic:
  structured questions, saved outputs, revisit dates, regular cadences.
- Skills are meant to combine, so set up the busy hubs first
  (video, notes, skill-making, slide decks) and the rest plugs in.
- The public/private split is the safety net:
  shared instructions stay public, personal data stays on your disk.
- Start small: install, run `/decide`, read one `SKILL.md`,
  then adopt one skill that replaces a chore you already do by hand.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Skill | A saved instruction document the AI follows to do one job |
| Plugin | The bundle of all the skills, installed into your AI tool at once |
| SKILL.md | The actual file containing a skill's steps; editing it changes the skill |
| Agent Skills host | The AI app the skills run in (Claude Code, Codex, Cursor, etc.) |
| Routing table | The "I want to..." list that points you to the right skill |
| Compose by name | Skills handing work to each other instead of redoing it |
| Vault | A folder of plain-text notes that acts as your searchable memory |
| Private config layer | Your personal settings and saved results, kept outside the shared repo |
| Semver / versioning | Numbering that tracks changes, separately for the bundle and each skill |
| Cadence | A repeating rhythm, e.g. a weekly money check or nightly data pull |
