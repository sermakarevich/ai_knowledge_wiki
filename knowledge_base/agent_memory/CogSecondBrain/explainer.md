> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# huytieu/COG-second-brain — In Plain Language

Think of COG as a notebook that thinks with you. You talk to an AI
assistant in plain English, and it files, connects, and checks your
notes for you — using only simple text files and version history.

## What is this about?

COG stands for Cognition + Obsidian + Git. In plain terms: smart
helpers (Cognition) + a folder of notes (Obsidian) + a time machine
for those notes (Git).

There is no database and no vendor lock-in. Everything is just
Markdown text files (`.md`) inside folders. Any AI that can read
text — Claude Code, Cursor, Gemini CLI, Kiro, Codex, and others —
can work with the same brain.

Setup takes about two minutes: copy the project, open it in your
AI tool, and say "Run onboarding." The assistant then personalizes
your profiles, interests, and folders, and you are ready to go.

## Why does it matter?

Most notes go stale: links rot, meeting notes get lost, team updates
live in four different apps. COG matters because it turns scattered
notes into a living memory.

For individuals, it captures braindumps, daily news briefs, saved
links, weekly reviews, and journals — then consolidates them into
reusable frameworks instead of piles of forgotten files.

For teams, it cross-references GitHub, Linear, Slack, and PostHog
into one daily team brief, processes meeting recordings into
decisions and action items, and maintains a people directory so
context about collaborators builds up over time.

Because everything is plain files under version control, updates
are safe: framework improvements arrive file-by-file without
overwriting your personal notes.

## How does it work?

The flow is simple: You → AI Agent → Skills → Notes → Git.

1. You speak in natural language ("Give me my daily brief").
2. The agent runs one of 33 skills — small playbooks for jobs
   like onboarding, braindump, daily brief, saving URLs,
   weekly check-in, product specs, release notes, or publishing.
3. For heavy lifting, the main assistant delegates to cheap
   helper workers (6 of them: data collection, web research,
   file operations, approved updates, publishing, people
   profiles). Helpers write results to temporary files and
   return only a short status plus a file path.
4. Notes land in numbered folders: inbox, daily, personal,
   professional, projects, knowledge, and templates.
5. Git (plus iCloud if you want) syncs and versions everything,
   and selected results are pushed out to GitHub, Linear,
   Slack, Confluence, or Notion.

Cost control is built in: helpers run on the cheaper, faster
model (Sonnet) for gathering facts, while the lead session uses
the stronger model (Opus) for reasoning and writing.

Rigor is opt-in, never forced. Only when you ask for a verified
run (words like "closed loop" or a `verification_harness: on`
setting) does work walk a V-shape: break the goal into checkable
criteria, build, then verify each claim against the real artifact.
Four read-only checkers observe files directly and never grade
their own homework — they get file paths, not summaries, so
they cannot be fooled by a nice story.

## Where can this be used?

- Personal knowledge: daily briefs with 7-day-fresh news,
  braindumps with automatic filing, saved links with extracted
  insights, weekly pattern reviews, memory audits.
- Team leadership: daily team briefs, meeting transcript
  processing, deep weekly or board-prep analysis.
- Product management: research → spec → user stories →
  release notes → knowledge base, plus issue audits and
  publishing to Confluence or Notion.
- Content and craft: announcement scouting with deduplication
  and volume caps, plain-language writing checks, charts and
  diagrams, illustrated essays, guided journals.
- High-stakes builds: phased goals that span sessions, gated
  checkpoints from intake (CP-0) through shipping (CP-6) and
  retro (CP-7), with evidence logged per requirement.

It works wherever Markdown-reading agents work: Claude Code is
first-class, Antigravity mirrors it, Cursor / Kiro / Gemini CLI
cover core workflows, and a universal `AGENTS.md` file covers
everything else.

## Conclusions & takeaways

COG's big idea: files that think. Keep knowledge as plain text,
let AI helpers do the filing and checking, and keep history in
Git so nothing is lost and upgrades never clobber your content.

The practical takeaways: start with onboarding; talk in plain
language; let cheap workers gather and the lead assistant reason;
ask for verification only when the stakes justify it; and cite
notes with path, date, and confidence so future-you can trust
past-you.

The limit is also clear: it is only as good as what you feed it.
Empty folders mean an empty brain — capture first, consolidate
later, and review weekly.

## Jargon decoder

| Term | What it really means |
|---|---|
| Second brain | A trusted external memory: notes + helpers that remember for you |
| Skill | A named playbook you trigger with plain words, e.g. "Weekly review" |
| Worker | A cheap helper that gathers facts and hands back a file path |
| Verifier | A read-only checker that looks at the real file, not a summary |
| Vault | Just a folder tree of notes, numbered `00` through `06` |
| Braindump | Dumping raw thoughts so the assistant can sort and file them |
| Harness / V-model | Optional strict mode: define checks first, build, then prove each one |
| Checkpoint (CP-0–CP-7) | Named gates from intake to retro; some block, some only advise |
| People CRM | Auto-built contact notes that get richer the more someone is mentioned |
| Anti-slop set | Paired writing/design rules that keep output plain and human |
