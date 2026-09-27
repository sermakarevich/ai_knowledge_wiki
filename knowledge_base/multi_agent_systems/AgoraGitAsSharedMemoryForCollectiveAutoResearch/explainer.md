> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Agora: Git as Shared Memory for Collective AutoResearch — In Plain Language

## What is this about?
Imagine hiring 13 smart research assistants and telling them all to solve
the same hard puzzle, but each one works in a separate room with no phone.
That is what happens today when we run many AI coding agents in parallel:
each session starts from zero, repeats the same dead ends, and loses
what it learned when it shuts down.
Agora is a fix for that problem. It is a shared notebook the whole
group of agents (and humans) can read and write.
Technically it is a growing family tree of research steps stored in Git
(Git is the version-control tool programmers use to track code changes).
Every try, idea, guess, check, and summary becomes one permanent entry
(a "commit") that says exactly what it built on.
Nobody shares a chat, a boss, or a computer. The shared history file
is the only connection between workers.
In the paper's test, 13 AI workers with no assigned tasks and no central
planner worked for nearly 12 days on one task and posted 1,703 entries.
They moved the score from 3.39 down to 1.899 bits per byte
(bits per byte is a text-prediction error score — lower is better).

## Why does it matter?
One AI agent alone can already improve a setup by itself while nobody watches.
But just adding more agents does not add more discovery — it mostly adds
repeated work. Everyone chases the same leaderboard leader, failures vanish,
and nobody knows which result was actually re-checked.
Science in real life avoids this with shared journals, citations, and
reproduction (re-running someone else's experiment to confirm it).
Agora gives AI agent groups the same basics: a public frontier
(what is currently best), a permanent family tree (who built on what),
saved failures, independent checks, and a way to spread attention
instead of everyone piling onto one idea.
Without something like this, more computers just mean more duplicated
searching, not faster science.

## How does it work?
Think of three simple rules plus one tool that keeps everyone honest.
Rule 1: everything is saved and linked. Each entry records its parents,
meaning "this builds on that." Results, ideas, untested guesses,
re-checks, and summaries all get the same treatment. Nothing can be
rewritten — history only grows.
Rule 2: quality comes from use, not votes. A result earns trust when other
workers (not the same author) build on it or independently reproduce it.
A failed re-check hurts the score. Simply saying "nice work" adds nothing.
The newest check replaces the old one, but both stay in the history.
Rule 3: show the neglected paths next to the popular ones. A leaderboard
(a ranked list of best scores) is a good signal for what works now but a
bad map of what is unexplored. So Agora also shows leaves (entries nobody
continued), untested guesses, unchecked or disputed results, and groups
of similar ideas (clusters). Candidates are shown in three boxes:
exploit (copy or polish the leaders), explore-known (extend a promising
but thin area), and explore-novel (look at ideas nobody touched).
Under the hood, Git stores the permanent entries and a simple database
(SQLite, a small file-based database) builds the searchable views.
The database can always be rebuilt from Git, so Git is the single source
of truth.
The test task was deliberately hard: fill a fresh 119.6-million-parameter
hybrid language model using only the weights and example outputs of 141
ready-made donor models — no training texts, no gradient updates
(gradient updates are the usual step-by-step learning adjustments).
The winning recipe copied donor word-pattern statistics (a bigram table,
meaning "which word likely follows which") into the new model's input
and output layers, then added small fixed patches to its attention,
feed-forward, and state-space parts (the parts that mix word context).
The family tree of that winner spans 145 entries across 15 accounts,
with 165 independent re-checks and zero reported failures.

## Where can this be used?
Anywhere several AI agents (AI is artificial intelligence) work on the
same open problem over days or weeks without a shared chat.
Examples: tuning model setups, hunting for better prompts or settings,
materials or drug-candidate screening with a shared score, software
teams of agents fixing bugs across a big codebase.
It also fits mixed human-plus-agent groups: people can post guesses or
summaries, agents test them, and everyone sees the same map.
The reproducibility appendices (appendices are extra sections proving
the work can be re-run) even list what a serious run must archive:
instructions, code versions, model and hardware names, prompts and seeds
(seeds are fixed random starting numbers), the full entry tree, raw
scores, and the scripts that made every table.
That makes it useful for labs, companies, or open communities that want
an audit trail (a complete record anyone can inspect later).

## Conclusions & takeaways
The big lesson: when many AI researchers share no memory, extra computers
turn into extra repetition. A shared, permanent, linked memory changes
what the group can do.
In this run the group found a no-training starting recipe that closed 62%
of the gap toward a trained model, re-checked each other 165 times, and
jointly diagnosed why they were stuck near 1.90.
It also showed a weakness: for five days everyone polished one recipe in
tiny steps while staring at the same leaderboard. After a single human
showed them a diversity map on May 2, they left that rut within a day.
So the coordination layer (how the group shares memory and attention),
not the smarts of any single agent, was the bottleneck.
One caution: there was no matched control group (the same agents and
computers running without Agora or with only a plain leaderboard), so we
cannot prove Agora caused the win. The paper's own next step is exactly
that fair comparison.

## Jargon decoder
| Term | Plain meaning |
|---|---|
| DAG (directed acyclic graph) | A family tree of entries with arrows for "builds on"; loops are impossible because history only grows. |
| Git commit | One permanent saved snapshot with an ID number (hash) that anyone can open and re-run. |
| Bits per byte (bpb) | Error score for predicting text; lower means the model guesses text better. |
| Donor model | A ready-made trained model whose weights and answers you borrow from. |
| Weight transfer | Filling a new model with useful starting weights taken from other models, without normal training. |
| Verification | An independent re-run of someone else's entry to confirm the score; you may never verify your own work. |
| Leaderboard | Ranked list of best scores; useful for exploiting winners, bad at showing unexplored ideas. |
| Monoculture | Everyone crowding onto the same idea while other paths sit empty. |
| UCB (upper-confidence bound) | A ranking score balancing "this looks good" with "we have not tried this much yet." |
| Quality-diversity | Keeping many different good solutions instead of one single champion. |
| Embedding / cluster | A numeric fingerprint of each entry's text, used to group near-duplicates into clusters. |
