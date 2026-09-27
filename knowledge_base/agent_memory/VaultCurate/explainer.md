> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# notoriouslab/vault-curate — In Plain Language
## What is this about?
Vault Curate is an add-on (plugin) for Obsidian, the popular note-taking app.
Its motto is simple: "Find, connect, and rediscover your notes."
It solves a familiar problem: after months of note-taking, your vault becomes
an attic of boxes — you know something useful is inside, but keyword search
misses it and you forgot half of what you wrote.
Vault Curate adds three tools that work immediately, with no setup:
1. **Find** — search by meaning, not just exact words.
2. **Connect** — see which notes are related, even if you never linked them.
3. **Rediscover** — get reminded of old, forgotten notes that matter right now.
A fourth tool, **AI curation** (auto-writing descriptions and tags),
stays switched off until you deliberately turn it on.
A core promise: **nothing leaves your machine by default.** The built-in
language model is about 110 MB, downloads once, needs no API key,
and runs entirely on your own computer.
## Why does it matter?
Three everyday frustrations motivated this project:
- **Keyword search fails.** You search "car" but the note says "automobile",
  so you miss it. Or the idea is phrased differently than you remember.
- **Related notes stay scattered.** Two notes on the same topic sit alone
  because you never linked them by hand.
- **Old notes become lost memories.** Good ideas quietly rot because
  you never stumble across them again.
Vault Curate attacks all three at once — without becoming an autopilot
that rewrites your notes. Its ground rules are deliberately reassuring:
- It never edits notes on its own; every connection is a suggestion.
- You say yes (one click makes a real link) or no (dismiss it for good).
- Dismissed pairs stay dismissed, even across renames or index rebuilds.
- It is especially strong in Chinese — names, proper nouns, everyday
  phrasing — a gap in many search tools.
- It works on your phone too: build the index once on desktop, let your
  sync tool carry it over, and search on mobile with no second download.
## How does it work?
Think of it as a librarian who has read every note and remembers
what each one is really about.
**Step 1: It reads everything, locally.** The built-in model reads your
notes — long ones included, up to about 60,000 characters each — and builds
a private index on your device. Traditional Chinese is matched as Simplified
behind the scenes while stored text and snippets stay Traditional.
**Step 2: Search runs three engines at once.** Every search blends three
approaches into one ranked list: *keyword* (exact phrases), *meaning*
(same idea, different wording), and *fuzzy title* (typos and variants).
Results show the matching passage highlighted; clicking jumps to it.
A Hot / Cold / All filter narrows to active notes, neglected notes, or all.
**Step 3: It draws maps of how notes relate.** Instead of a plain list,
you get an editable Obsidian Canvas file, freshly timestamped each run:
- *Relation graph:* your note centered, closest meaning-neighbours around
  it, each line labelled with a similarity score.
- *Semantic path:* a chain of stepping-stone notes between any two notes,
  with an honest "not really connected" verdict when no strong chain exists.
- *Expand in place:* grow an existing map with a node's neighbourhood
  without wrecking your layout.
Colours carry meaning: purple is "related but unlinked", gray is "already
linked", cyan marks forgotten notes, green marks query relevance.
Every purple line is a question: tick a checkbox to write a real link into
a "Related" section, or dismiss the pair everywhere.
**Step 4: It sorts notes into Hot and Cold.** Notes that are linked or
recently created/edited count as Hot; orphans untouched for a while count
as Cold. Merely opening a note does not count — only editing does.
The cutoff in days is tunable under Advanced settings.
Two Discover views resurface Cold notes: one tied to the open note, one
global view of forgotten notes near your recent focus, grouped by folder.
One click exports a topic-grouped overview note (a "Map of Content").
**Step 5 (optional): AI curation, only if you ask.** Enabled in settings
and pointed at a model of your choice, it drafts descriptions and tags
into a note's frontmatter. This is the only part that can send data out —
and only because you configured it that way.
## Where can this be used?
- **Personal vaults:** reconnect reading, project, and journal notes
  without manual tagging marathons.
- **Study and research:** find the half-remembered passage, trace a path
  between two topics, or collect the top dozen hits on one canvas.
- **Writing:** open a draft and see related forgotten notes surface
  at the moment you need them.
- **Chinese-language vaults:** meaning-aware search tuned for names,
  nouns, and colloquial phrasing where many tools stumble.
- **Phone-plus-desktop setups:** index once on a computer, then search
  the same vault from a phone via iCloud, Obsidian Sync, or Syncthing.
- **Shared vaults:** the synonym list (e.g. "Amy = Amy Chen") smooths
  over different people spelling the same name differently.
## Conclusions & takeaways
- Vault Curate is a **finder, not a thinker**: it surfaces candidates,
  you make the calls.
- Its strength is **recall**: meaning search plus visual maps plus
  deliberate rediscovery of neglected notes.
- **Privacy is the default**, not a toggle: local model, local index,
  no account, no background network calls.
- Hot/Cold reframes note hygiene: **editing is attention**, and attention
  is what keeps a note alive.
- Honest limits are part of the design: it admits weak connections,
  and AI features stay off until invited.
- In short: a librarian who knows every box in your attic —
  but still asks before moving anything.
## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Obsidian plugin | An add-on that gives the Obsidian notes app an extra feature |
| Semantic search | Finding by meaning ("car" matches "automobile"), not identical words |
| Wikilink | A clickable link from one note to another, in double brackets |
| Canvas | Obsidian's whiteboard where notes appear as cards joined by lines |
| Relation graph | A map with one note centered and its closest relatives around it |
| Semantic path | A chain of notes bridging topic A to topic B, like connecting flights |
| Hot / Cold notes | Recently used notes (Hot) vs orphaned, untouched notes (Cold) |
| Map of Content (MOC) | An overview note grouping related notes by topic |
| Frontmatter | A small settings block atop a note holding tags and descriptions |
| Embedding model | The local ~110 MB reader turning text into meaning fingerprints |
