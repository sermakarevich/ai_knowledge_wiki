> [[index|Wiki]] | [[summary|Summary]]

# HiGram — In Plain Language

## What is this about?

Picture an AI assistant that has been talking to you for months. It needs to remember thousands of small facts — what you said last Tuesday, that you changed jobs, that your dietary preference flipped from vegetarian to pescatarian last week — and to use the *right* facts when it answers a question, without dragging in a mountain of irrelevant history. Many current systems keep all these facts in one giant, ever-growing connected diagram (a "graph"), where each fact is a node linked to related facts. When the assistant needs to answer something or update a fact, it has to search through that whole sprawling diagram, which gets slower and messier the longer the relationship goes on.

HiGram is a different way to organize that memory diagram. Instead of one flat pile of facts, it builds a two-level filing system: a top level of broad folders (organized by subject, category, and context) and a bottom level of individual fact-cards (called MemoryUnits) that also know which other fact-cards they depend on. When something needs looking up or correcting, HiGram doesn't search the whole filing cabinet — it quickly zooms into one small, relevant drawer, picks out the one chain of connected fact-cards that actually matters, and only touches that chain.

## Why does it matter?

Two things go wrong without this kind of structure. First, cost: searching a huge, flat pile of memories to answer one question wastes a lot of computation (measured here in "tokens," roughly the units an AI model reads and writes) — HiGram's design cuts that cost dramatically. Second, and more subtly, correctness: when a fact changes ("I moved to Seattle"), everything that *depended* on the old fact ("I recommended restaurants near my old city") needs re-checking too. If the system only edits facts one at a time without tracing dependencies, those downstream conclusions quietly go stale and keep getting used as if they were still true. HiGram's mechanism is explicitly built to catch that.

## How does it work?

Think of it as a three-step pipeline, like a librarian handling a correction slip:

1. **Zoom in (localization).** Given the current question or the new piece of information, the system pulls out the relevant "drawer" — a small cluster of fact-cards sharing the same subject and rough category, called a MicroGraph. It picks a handful of the most relevant drawers, then within them finds the single connected chain of fact-cards ("the evidence path") that best matches what's being asked or updated.
2. **Update directly affected facts (intra-unit rewrite).** The librarian edits only the fact-cards on that chain: brand-new facts get filed as currently true ("active"); facts being corrected get their status updated while the old version is kept on file (not erased) for history.
3. **Check what depended on them (inter-unit rewrite).** For every fact-card that leaned on the ones just edited, the librarian re-checks: does this downstream conclusion still hold given the update? If yes, it's left alone. If no, it's stamped "outdated" rather than being silently reused later. Crucially, downstream facts don't automatically inherit validity from their source — each has to be re-earned.

Everything outside that one chain is left completely untouched, which is what keeps updates cheap and avoids repeatedly re-scanning the whole memory.

## Where can this be used?

- Long-running personal assistants or customer-support bots that accumulate a large history of user facts and need to stay both accurate and cheap to query as that history grows.
- Any agent memory system that has to reconcile *conflicting* information over time (e.g., "the meeting was moved," "the budget changed twice") without letting stale conclusions silently persist.
- More generally, any knowledge-graph-style memory (not limited to chat agents) where updates have downstream effects that current systems handle by brute-force re-search.

## Conclusions & takeaways

HiGram's core lesson, worth remembering: localize *before* you rewrite, and never let a fact's dependents automatically inherit its validity — re-check them explicitly. That combination is what buys both efficiency (smaller token footprint) and correctness (fewer stale facts surviving updates) at the same time. The honest limitation: it was tested on two benchmarks whose scope is long personal-conversation QA and synthetic conflict scenarios — it doesn't demonstrate that this approach handles memory needs outside that setting, such as facts that require external knowledge not already stored.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Graph memory | A memory system where facts are nodes connected by edges showing how they relate |
| MemoryUnit | One individual stored fact, with metadata like when it was true and its current status |
| MicroGraph | A small, localized slice of the whole memory graph, grouped by subject and rough category |
| Evidence path | The specific chain of connected facts that supports an answer or is affected by an update |
| Localization | Narrowing down to the small relevant part of memory before doing detailed work |
| Coordinated rewriting | Updating a fact and then explicitly re-checking (not assuming) whether facts that depended on it are still valid |
| Dependency edge | A link recording that one fact's validity relies on another fact |
| LLM-as-Judge (LLM-J) | Using a separate large language model to score whether an answer is correct, instead of only exact text matching |
| Token | A chunk of text an AI model reads or generates; more tokens = more compute cost |
| Ablation | An experiment where one component is removed to measure how much it was contributing |
