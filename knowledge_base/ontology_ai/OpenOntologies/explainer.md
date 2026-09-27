> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment — In Plain Language

## What is this about?

Imagine two hospitals that each keep their own catalogue of body parts.

One calls it "Heart", the other calls it "Cardiac structure" — same thing, different words.

An ontology is just a careful, machine-readable catalogue like that: it lists the
things in a domain (classes such as Heart, Lung), how they relate (a HeartValve
is part of a Heart), and the rules they must obey (every Pizza must have a base).

The problem: large language models (LLMs) are good at writing such catalogues,
but bad at checking them. They produce text that looks right yet contains
contradictions, mix up similar-sounding entries, or misread the raw file format.

Open Ontologies is a helper system that sits between the LLM and the catalogue.

It is a single fast program (written in Rust, no extra setup needed) that gives
the LLM a set of proper tools: build entries, check logic, compare two catalogues,
and manage versions over time. The LLM asks for things through structured queries
instead of staring at raw files.

Two headline results from the digest and wiki:

- Matching two anatomy catalogues (mouse vs. human, 2,737 vs. 3,304 classes)
  reaches F1 = 0.832 with record precision 0.963 — up from F1 = 0.182 before
  the key matching fix.
- Letting the LLM use structured tools to read a catalogue (F1 = 0.717) far beats
  pasting the raw file into its context (F1 = 0.323) — which is even worse than
  giving it no file at all (F1 = 0.431).

## Why does it matter?

Three everyday frustrations motivate this work.

First, more information is not always better. You would expect that showing the
LLM the full file helps. It does not: on 9 test catalogues with 3,042 checked
facts, the raw-file LLM scored 25% worse than the LLM working from memory alone.
The raw syntax actively confuses it, especially on statements like "this property
applies to that class" (domain/range triples scored 0.0 on 4 of 9 catalogues).

Second, clever scoring matters less than a simple fairness rule. The team tried
five different ways of weighting match signals (names, parents, properties, and
so on). Once the fairness rule was in place, all five scored within 0.004 of each
other. Without the rule, all scored an identical 0.728. Effort spent fine-tuning
weights was nearly wasted; the rule did the real work.

Third, speed plus checking makes LLM-built catalogues practical. Using the tool
pipeline, an LLM rebuilt the classic 91-class Pizza teaching catalogue in under
5 minutes with 96% class coverage, versus about 4 hours of manual work. Fast
built-in checking (15 ms on 50,000 facts, versus ~24 seconds for a full academic
reasoner) makes that loop interactive.

## How does it work?

Think of the system as four cooperating parts plus a matchmaker.

1. A store and search desk. All facts live in a fast in-memory triple store
   with a standard query language (SPARQL). Instead of reading the whole file,
   the LLM asks precise questions: "list all classes", "what are the properties
   of X?", "what breaks if I change Y?"
2. A logic checker. A fast rule engine fills in implied facts (if A is a kind of
   B, and B is a kind of C, then A is a kind of C), a consistency checker looks
   for contradictions, a shape validator checks required patterns, and a pattern
   enforcer keeps house style. Lifecycle tools — plan, enforce, apply, monitor,
   drift — work like infrastructure-as-code for catalogues, with every change logged.
3. A matchmaker with six clues. To decide whether class A in catalogue 1 equals
   class B in catalogue 2, it combines six similarities: name (weight 0.25),
   properties (0.20), parents (0.15), examples (0.15), logical restrictions
   (0.15), and neighbourhood (0.10). If only the name matches and everything else
   is empty, the score is penalised by 15% so weak guesses do not pass the bar.
4. The fairness rule: stable 1-to-1 matching. Sort all candidate pairs by score,
   then keep only the best partner for each side. No class gets two spouses.
   That single step cut candidates from 12,557 noisy guesses (precision 0.102)
   down to 1,154 clean pairs (precision 0.963).

Why the rule wins: on the anatomy catalogues most pairs share no properties or
examples, so five of the six clues are zero. Reweighting zeroes changes nothing.
Picking exactly one best partner per class removes thousands of spurious
many-to-many matches regardless of the exact formula.

The same method struggles where names do not overlap. On 15 conference-organisation
catalogue pairs with very different modelling styles, it reaches only F1 = 0.438
(precision 0.693, recall 0.320) — respectable precision, but it misses many true
matches that need background knowledge to recognise.

## Where can this be used?

- Merging medical or biological vocabularies. Two anatomy catalogues that use
  different labels for the same organ can be aligned with very high precision,
  leaving only the low-name-similarity cases for expert review.
- Catalogues-as-code teams. Versioned editing with diffs, blast-radius scoring,
  watchers, and drift checks fits teams that maintain product, food, or
  supply-chain catalogues the way they maintain software.
- Fast teaching and prototyping. A 91-class teaching catalogue built in minutes
  at 96% coverage shows how beginners or domain experts could draft a first
  version quickly, then fix the last few percent by hand.
- Any LLM-plus-data workflow. The broader lesson travels: when the LLM must read
  structured data, give it query tools, not a raw dump. Raw Turtle files varied
  wildly (0.69 on simple files, below 0.16 on complex ones), while tool access
  was consistently better (+122% over raw-file reading).
- Choosing where to invest. If your catalogues have little shared structure,
  invest in the matching constraint and background dictionaries first, not in
  ever-more-elaborate similarity scores.

## Conclusions & takeaways

- Tools beat text dumps. Structured access (F1 = 0.717) is a qualitatively
  different way of reading, not just "more context". Raw syntax can hurt.
- Constraints beat cleverness. One-to-one matching lifted F1 from 0.182 to 0.832;
  weight tuning moved it by less than 0.004.
- Precision is the strength, recall the gap. Best-in-class precision (0.963) on
  anatomy comes with recall 0.733 — true matches with very different names are
  still missed without external background knowledge.
- Heterogeneity is the open challenge, alongside independent evaluation (not yet
  submitted to the official matching campaign) and testing beyond a single LLM.
- Practical upshot: pair a fast, checking-heavy catalogue tool with an LLM
  orchestrator, query it instead of pasting files, enforce one-to-one matches,
  and spend your remaining budget on domain dictionaries.

## Jargon decoder

| Term | What it really means |
|---|---|
| Ontology | A machine-readable catalogue of things, relations, and rules in one domain. |
| OWL | The standard language for writing such catalogues so computers can reason over them. |
| Triple store / SPARQL | A database of subject–predicate–object facts plus a query language for asking precise questions about them. |
| OWL-RL reasoning | A fast, rule-based way to fill in implied facts; quick but not exhaustive. |
| SHACL validation | An automatic shape check, e.g. "every product must have exactly one price". |
| Ontology alignment | Deciding which entries in two catalogues mean the same thing. |
| Stable 1-to-1 matching | Each entry gets at most one partner — the best-scoring one — so duplicates are removed. |
| Precision / recall / F1 | Of the pairs you proposed, how many were right / of the true pairs, how many you found / the balance of the two. |
| MCP (Model Context Protocol) | A standard plug that lets an LLM call external tools instead of guessing from text. |
| Turtle syntax | A compact text format for catalogue facts that is easy for machines but confusing for LLMs to read raw. |
