> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions — In Plain Language

## What is this about?

Think of an ontology as a precise map of ideas for a subject area: the important things (like "Plant" or "Sensor"), how they relate (like "eats" or "measures"), and the rules that connect them.

Competency questions, or CQs, are the plain-English questions that map is supposed to answer — for example, "Which plants eat animals?"

Building such maps by hand is slow and needs experts. Large language models (LLMs) can draft them quickly, but until now there was no fair, shared test for how good those AI-made drafts really are.

CQ4OE is that shared test. It takes six existing subject areas — wine, African wildlife, digital rights (ODRL), water sensors (SAREF4WATR), video games, and software — and turns them into a carefully checked exam for AI systems.

The exam starts from 255 published questions, keeps 110 good ones, adds 8 new ones to fill gaps, and ends with 118 questions in total. Each question is linked to exactly the vocabulary and rules needed to answer it — nothing more, nothing less.

It offers two levels of challenge. The easier one, called CQ2Term (99 questions), asks: did the AI find the right words mentioned in each question? The harder one, called CQ2Onto (all 118 questions), asks: did the AI build a complete, working mini-map — with hierarchies, property meanings, and logical rules — that actually answers each question?

## Why does it matter?

Older tests had three problems this work fixes. First, everyone tested something slightly different, so results could not be compared fairly.

Second, reference maps often contained extra knowledge beyond what the questions asked for. An AI could then look bad for leaving out irrelevant detail, or look good for copying background knowledge that had nothing to do with the questions.

Third, old scores mostly counted matching words. They missed deeper mistakes: wrong connections between ideas, missing parent-child links, or broken logic that a computer reasoner would choke on.

CQ4OE matters because it grades what counts: does the generated map satisfy the stated requirements, question by question, rule by rule? Every score can be traced back to the specific question and the specific rule that passed or failed, through automatic reports the benchmark produces.

## How does it work?

Building the benchmark took four steps. First, the authors picked the core vocabulary of each subject by ranking ideas by how connected they are, then checking by hand with diagrams and official documents.

Second, they filtered the 255 published questions, throwing out ones that needed outside knowledge, could not be answered from the source, or were about single examples rather than general rules. Each surviving question was labelled with three kinds of words: explicit (written in the question), implicit (synonyms), and derived (not mentioned but needed for the answer).

For "Which plants eat animals?", for instance, "CarnivorousPlant" is derived — plus the rules that it is a kind of Plant and that it eats some Animal.

Third, they wrote just 8 new questions to cover core ideas no old question touched. Fourth, they built the two gold standards: a word list per question for CQ2Term, and a small rule set per question for CQ2Onto, where a rule is kept only if removing it would make the question unanswerable.

One annotator plus two expert reviewers had to agree on every item; about 86% passed without changes.

Grading has to cope with renaming: one AI may write `hasPart`, another `containsComponent`, for the same idea. So CQ4OE first aligns wordings using five similarity checks — exact match, two spelling-based measures, a sequence comparison, and an AI-embedding meaning check — combined into one score with stricter cutoffs for properties than for classes.

Then it computes scores for words, property features (like "symmetric"), connections, full logical rules, and inferred hierarchies checked with the HermiT reasoner. Nine popular LLMs were tested as baselines, using one-shot, step-by-step, and repair-agent approaches, producing 54 word-list runs and 162 full maps.

## Where can this be used?

Anyone building a knowledge map with AI help can use CQ4OE to pick the right model for their subject: one model may shine on wildlife but stumble on water sensors.

Teams can test a single skill (just finding words) or the full job (building answer-ready structure), benchmark a brand-new model with one script, or add a new subject area by following the same four steps.

Because every failure is labelled — missing word, shaky property, flat hierarchy, incomplete question — engineers know exactly what to fix by hand instead of re-checking everything.

The resources are open: parallel folders for each task, persistent identifiers for each metric, and a public leaderboard for comparing new methods.

It also fits human-in-the-loop workflows, where an engineer drafts with an LLM and uses the per-question report as a checklist for review.

## Conclusions & takeaways

The headline result: AI is decent at finding words but weak at assembling them into working maps. Word-level scores run about 59–67%, with classes (around 67%) clearly beating properties (around 55%).

But only about 24% of questions get all their words, and only about 2% get all their rules. Hierarchy scores average just 17%.

Typical failures: missing parent-child chains (e.g. WaterMeter → Meter → Sensor → Device collapses to a single flat link), unstable property names, and maps that mention the right ideas somewhere but not under the question that needs them.

Giving questions one at a time yields denser hierarchies; adding automatic repair tools lifts per-question rule coverage from about 18% to 24%. Results vary more by subject than by model — no single model wins everywhere.

Limits to keep in mind: all structure scores depend on the word-alignment step, only hierarchy-type rules get second chances through reasoning, and public sources may already sit in model training data. Future work plans more subjects, better alignment, and private, contamination-free test areas.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Ontology | A machine-readable map of ideas, relations, and rules for one subject |
| Competency question (CQ) | A plain-English question the map must be able to answer |
| Class | A category of things, e.g. Plant or Sensor |
| Property | A named relation or attribute, e.g. eats or hasPart |
| TBox axiom | A general rule about categories, e.g. every carnivorous plant is a plant |
| Provenance | A record linking each word and rule back to the question that needs it |
| CQ2Term | The easier sub-test: did the AI list the right words per question? |
| CQ2Onto | The harder sub-test: did the AI build a complete answer-ready map? |
| Alignment | Matching AI wordings to reference wordings that mean the same thing |
| Hierarchy closure | All parent-child links, including ones a reasoner infers indirectly |
