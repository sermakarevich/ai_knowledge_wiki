> [[index|Wiki]] | [[summary|Summary]]

# Gas Town: From Clown Show to v1.0 — In Plain Language

## What is this about?

Imagine a restaurant kitchen during the dinner rush with 25 cooks, no head chef, no ticket rail, and everyone's recipes written on napkins that blow away. That was AI coding help in 2025: each robot assistant worked alone, forgot things when its shift ended, and bumped into the others.

Steve Yegge built the missing kitchen: a "town" where every cook has a job title (one greets customers, some just chop vegetables in bursts, one plates every dish, one watches the others, one walks around shouting "keep cooking!"), every order hangs on a ticket rail nobody can lose, recipes are written as step-by-step cards that survive cooks quitting mid-shift, and scratch notes get thrown away instead of filed forever. At first the kitchen was a disaster — the fire alarm sprayed the good cooks, the ticket rail caught fire 22 times, and dirty dishes piled up. This is the story of fixing all that until the kitchen ran itself for over a month: version 1.0.

## Why does it matter?

One AI helper is like one employee: manageable. Twenty-five is a company, and companies need management — otherwise work vanishes, people redo each other's jobs, and nobody knows what's done. Anyone who wants AI to do big jobs (rewrite a whole app, keep a codebase healthy overnight) hits this wall the moment they go from one helper to many.

If this works, a single person can direct a whole factory of helpers the way a chef runs a kitchen: dreaming up dishes while the line cooks execute. If it fails the way it first failed, you get the worst of both worlds — paying for 25 cooks and getting food slower than cooking alone.

## How does it work?

The kitchen runs on five simple habits:

1. **Everything goes on the ticket rail.** Every task, message, worker name, and recipe step is a "bead" — a little ticket pinned where everyone can see it and stored permanently. Cooks come and go; tickets stay.
2. **Everyone has a hook with their name on it.** Giving someone work means hanging a ticket on their personal hook and poking them ("you must cook what's on your hook!"). If they quit mid-dish, the next cook reads the same hook and continues.
3. **Recipes are cards, not memory.** Big jobs are pre-written as chains of small ticket-steps (a "molecule"), so a cook just walks the chain: do step, check it off, next. The chain survives crashes because it's on the rail, not in anyone's head.
4. **One plater, one babysitter, one shouter.** A single "Refinery" cook plates every dish one at a time (no fighting over the pass); a "Witness" watches the choppers and un-sticks them; a "Deacon" patrols shouting "keep working," with helper "Dogs" for dirty jobs.
5. **Scratch paper goes in the bin.** Quick coordination scribbles ("still alive?", "checked, nothing to do") are written on disappearing tickets ("wisps") that get burned daily instead of clogging the permanent files — because at factory speed, paperwork was burying the kitchen.

## Where can this be used?

- **Running many coding helpers at once** — the original job: one person directing overnight swarms that file, review, and merge code while they sleep.
- **Any team of AI workers** — support bots, research assistants, data-cleaning crews: anywhere parallel helpers need a shared to-do list that outlives any single worker.
- **Personal memory for one helper** — the ticket rail alone (called Beads) works with almost any AI assistant: your notes, plans, and history survive between chats even without the whole town.
- **Workflow marketplaces** — pre-written recipe cards ("release a new version," "review everything five times") can be shared and reused like apps in a store (the planned "Mol Mall").
- **Our own fleet of task workers** — the direct takeaway: wrap each batch of work in a tracking ticket, give every worker a persistent hook list, burn control chatter instead of archiving it, and serialize all merges through one gatekeeper.

## Conclusions & takeaways

Remember this a month from now: **make the work outlive the worker.** If every task, message, and recipe step lives in a shared permanent place, individual helpers can crash, quit, or be replaced without losing anything — and that single property unlocks everything else (overnight runs, 25 parallel cooks, workflows that survive disasters).

Honest limits: this kitchen is expensive (multiple paid AI accounts), needs an experienced chef (someone already juggling many helpers by hand), tolerates mess (some dishes get cooked twice, some get lost), and only runs a handful of AI brands today. Version 1.0 means "it holds together," not "anyone can run it."

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agent / worker | One AI helper doing a job, like one cook |
| Bead | A ticket on the rail: a task, message, or name tag that is saved permanently |
| Rig | One project kitchen under the town's management (one recipe book) |
| Convoy | A food order ticket bundling everything for one delivery, tracked until it lands |
| GUPP | The house rule: "if there's food on your hook, cook it — no waiting to be asked" |
| Nudge | A poke ("hey!") that wakes up a helper politely idling instead of working |
| Molecule / formula | A recipe: chained step-cards (molecule) written from a reusable template (formula) |
| Wisp | A disappearing sticky note for quick coordination chatter — burned, not filed |
| Refinery / merge queue | The single cook allowed to plate dishes, serving orders one at a time |
| Dolt | The filing cabinet: a database that versions everything like code history |
| tmux | A tool showing many text windows on one screen — the kitchen's pass where you watch all cooks |
| NDI | "Messy path, sure finish": the order still arrives even if cooks improvise along the way |
