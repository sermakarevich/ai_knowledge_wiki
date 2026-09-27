# extract chunk 01: MechanicsOfSwarm

Write ONE wiki page from your chunk only.

## Input
- Your chunk: `/Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/source/chunks/01.txt` (read it fully)
- Whole-source orientation (do NOT read other chunks):
- 01.txt: The Mechanics of a Swarm: A Reproducible External Reconstruction of an Unintended Agent-Coordination Episode on a Third-...
- 02.txt: 5.2 Population: of the order of 900 episodes, not 3103 names The archive records 1,035 names carrying exactly one valid ...
- 03.txt: 5.9 Behaviour: measurement instead of work, and three fuzzy types The centre of gravity moves to self-measurement. Under...
- 04.txt: 41 Copy-loop rule: same name, identical normalised delta within 60 min, or a line of ≥80 characters previously written b...

## Task
Write `/Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/01-<kebab-topic-from-your-chunk>.md` where <kebab-topic> names what YOUR chunk covers.

Wiki-page contract (follow exactly):
- First line: backlink `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`
- `# <page title>` (topic, not "Chapter N")
- `**In one sentence:**` + one sentence capturing the chunk
- `## Key points`: 5-8 bullets, each a COMPLETE claim (numbers, mechanisms, conclusions) — never "discusses X"
- `---`
- Hierarchical `##` detail subsections covering the chunk fully: exact numbers, tables, verbatim prompts/algorithms
- Last line: `**Covers:** <what part of the source>`
- Flowing paragraphs. NEVER one sentence per line. Abbreviations expanded on first use only, no dictionary parentheticals.

## Tests
- `test -s /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/01-*.md`
- `grep -c '^\*\*In one sentence:\*\*' /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/01-*.md` >= 1
- `grep -c '^- ' /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/01-*.md` >= 3

## DoD (close-out shape c — shared tree)
1. Tests green (exact commands above).
2. `git add` ONLY the files named above (never `git add -A` / `.` / `-a`; never reset/checkout/stash/restore — shared tree).
3. `git commit -m "<msg>"`.
4. Verify: `git show HEAD:<path> | grep -c "<token>"` >= 1.
5. `bd close <your-own-id> --reason "<done>"`. Close ONLY your own bead. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai. Touch ONLY the paths named above.
- Do not run `fleet serve restart` / `fleet run`. No live-LLM tests.
