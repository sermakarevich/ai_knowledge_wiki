> [[index|Wiki]] | [[summary|Summary]]

# Design Docs Are All You Need — In Plain Language

## What is this about?

Imagine you own a bakery and you have a recipe book for predicting exactly how long each cake will take in each oven. Now imagine that every few months, someone invents a completely new kind of cake (with layers that rearrange themselves) and a completely new kind of oven (with different shelves and fans). Your recipe book's predictions keep going wrong, and every time you scribble a fix in the margins, the book gets messier and harder to use. Eventually the scribbles-on-scribbles are worse than starting over — but nobody ever wants to throw the book away and start fresh, because that feels like wasting all that work.

This paper is about a team that maintains exactly such a "recipe book" — except their cakes are AI models and their ovens are AI chips (Google TPUs). Their recipe book predicts how fast a model will run on a chip. And they made a radical decision: they threw away the code and kept only the recipes. Whenever something changes, they have a team of AI assistants rebuild the entire calculator from the recipes from scratch. It takes a couple of hours and costs about as much as a nice dinner — and the rebuilt calculator matches carefully hand-checked answers exactly.

## Why does it matter?

Anyone who maintains software in a fast-moving field knows this pain: the program works today, the world changes tomorrow, and each quick fix adds a layer of duct tape. Normally we accept this as the cost of doing business — rewriting from scratch is too expensive and too scary. What changed is that AI coding assistants made rebuilding cheap and fast. When rebuilding costs ~100 dollars and a few hours, the math flips: it can be cheaper to regenerate everything cleanly than to keep patching the duct tape. If true, it changes what a software project *is* — the permanent thing you curate is a set of human-readable documents, and the code is a disposable product squeezed out of them on demand, like printing a fresh copy from a master document.

## How does it work?

Step by step, using the bakery analogy:

1. **Write recipes, not code.** The team keeps ~50 documents describing every ingredient: the ovens (chip layout), the delivery trucks (network communication costs), the measuring system (number precision), and a catalog of cake types (AI model families).
2. **Draw the dependency map automatically.** Some recipes must be "baked" before others (you need to understand ovens before you can price delivery routes). Helper AIs read all the recipes and figure out this ordering by themselves — nobody maintains it by hand.
3. **Give each recipe to its own baker.** One AI assistant per document, working in dependency order, each with a small, focused job it can actually fit in its head. A supervisor watches where the bakers get confused and writes down exactly which recipes need clearer wording.
4. **Show every step on the board.** Each recipe includes a tiny worked example with real numbers ("on this small oven layout, the count is 3, not 6, so the delivery cost is..."), like a math teacher demonstrating a problem before assigning homework. Each recipe also ends with an answer key: a mini test with exact expected outputs.
5. **Rebuild on every change.** When anything in the world changes, a human edits only the recipe text, and the whole bakery is rebuilt from scratch — no patching, so no accumulated duct tape.

Under the hood, the recipes describe everything with one simple building block (a computation step with a symbolic cost formula, like "this step costs batch × length ÷ bandwidth") that nests inside itself like Russian dolls, and math software keeps all the formulas symbolic until the very last moment when real numbers are plugged in.

## Where can this be used?

- **Chip and model co-design:** quickly asking "what if" questions like "how would this new model run on next year's chip?" across thousands of options, then zooming in on the promising ones with a detailed schedule simulation.
- **Any software that rots fast:** tax software (laws change), integrations with third-party services (their interfaces change), data pipelines (formats change) — anywhere the rules churn faster than the code can comfortably absorb.
- **Team knowledge preservation:** when the durable artifact is plain-language documents with worked examples, a new engineer (or a new AI model) can understand and rebuild the system without archaeology through years of patches.

## Conclusions & takeaways

What to remember a month from now: when regeneration is cheap, treat human-readable design documents as the real product and code as a disposable build output — and make the documents regenerable by writing them as worked examples with exact numbers and built-in answer keys, not just rules and tests. Honest limitations: this is demonstrated on one system, one chip family, with cost figures from one AI vendor at one moment in time — and the paper never directly compares "worked-example docs" against "rules-and-tests docs" to prove the examples are the ingredient that matters.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Performance model | A calculator that predicts how fast a program will run without actually running it |
| Mixture-of-experts (MoE) | A model design where each piece of data is routed to only a few specialist sub-networks instead of using the whole model |
| Interconnect / topology | The "roads" connecting chips together and the map of those roads |
| Collective (AllGather, ReduceScatter, AllToAll) | Standardized group-message patterns chips use to share data, like "everyone send your piece to everyone" |
| Symbolic expression (SymPy) | A math formula kept as letters (cost = batch × length ÷ speed) instead of a single number, so you can reuse it with different inputs |
| Roofline bound | A simple optimistic speed limit for a chip: you can only go as fast as the slower of its math speed and its memory speed |
| Modulo scheduling / software pipelining | A careful timetable for overlapping repeated work steps, like an assembly line where the next item starts before the previous finishes |
| Reconciliation anchor | An answer key at the end of a recipe: exact expected outputs that the rebuilt code must reproduce |
| DAG / topological order | A map of "what depends on what" with no loops, read in an order where every prerequisite comes first |
| VMEM / MXU / ICI | Parts of a Google TPU chip: fast on-chip scratchpad memory, the matrix-multiplication engine, and the links between chips |
