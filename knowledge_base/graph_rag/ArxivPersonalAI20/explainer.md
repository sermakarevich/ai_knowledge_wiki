> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# PersonalAI 2.0 — Plain-Language Explainer

## The problem this paper is solving

Imagine you want an AI assistant that remembers everything about you and can answer complicated questions by connecting facts — like "which of my colleagues worked on the same project as the person who introduced me to my current job?" That kind of question needs several hops of reasoning: colleague → project → introduction → job. A large language model (LLM, the kind of AI behind ChatGPT-style assistants) is good at fluent, common-sense answers but bad at remembering huge amounts of specific fact and easily makes things up ("hallucinates") if it doesn't have the right facts in front of it.

One popular fix is **GraphRAG**: store all the known facts as a graph (a network of "nodes" — things like people, places, projects — connected by "edges" — relationships like "worked on" or "introduced"), and when a question comes in, pull the relevant part of that graph into the LLM's prompt before it answers. This is a form of Retrieval-Augmented Generation (RAG) — augmenting the LLM's answer with retrieved facts instead of relying purely on what it memorized during training.

## Why a flat retriever isn't good enough

Most GraphRAG systems retrieve information in one shot: look up the nodes mentioned in the question, grab their neighborhood, and hand it to the LLM. That works fine for a simple one-hop question ("what team is Alice on?") but falls apart for multi-hop questions (needing several linked facts), because the system doesn't know in advance which parts of the graph it will need — it only discovers that as it goes. A rigid, pre-planned graph structure ("static ontology") and inefficient traversal make this worse: the retriever either grabs too little (missing the answer) or too much (drowning the LLM in irrelevant facts).

## PAI-2's idea: let the LLM plan its own search, and revise the plan as it learns

PersonalAI 2.0 (PAI-2) treats retrieval like a mini research task instead of a single lookup. Here's the flow, in plain terms:

1. **Break the question apart.** A complicated question is split into independent sub-questions that can be answered separately, then combined.
2. **Write a search plan.** For each sub-question, the LLM writes out, in plain English, the steps it thinks it needs to take to find the answer — like a to-do list for research.
3. **Find the entry points.** From each plan step, the LLM pulls out the important named things (entities) and matches them to nodes ("vertices") in the graph.
4. **Ask focused follow-up questions.** For each matched node, the LLM generates a "clue-query" — a narrower question aimed at that specific part of the graph.
5. **Walk the graph.** The system traverses ("hops through") the graph starting from those nodes, following the clue-query, and collects the raw facts (triples — small subject-predicate-object statements, like "Alice — worksOn — ProjectX") it finds along the way.
6. **Filter for relevance.** Not every fact collected is useful, so irrelevant ones are filtered out, keeping only the closest matches to what's actually being asked.
7. **Summarize what was learned.** The kept facts are turned into a short summary of "what we now know" for that plan step.
8. **Check: do we know enough yet?** The LLM looks at everything learned so far and decides: can I answer the sub-question now, or do I need to search more?
9. **If not enough — revise the plan.** The plan gets updated based on what was just learned (a new lead might point somewhere unexpected), and the loop repeats from step 3, up to a maximum number of tries.
10. **Give up gracefully if truly stuck.** If the search limit is hit without enough information, the system returns an honest "no answer" instead of guessing.
11. **Combine the pieces.** Once all sub-questions have answers, they're stitched together into one final answer to the original question.

The key insight is step 9: the plan isn't fixed in advance — it adapts as new facts come in, the same way a person doing research follows up on unexpected leads instead of sticking rigidly to their first search plan.

## How they tested it

The authors ran PAI-2 against three well-known GraphRAG competitors — LightRAG, RAPTOR, and HippoRAG 2 — plus their own earlier system, PAI-1, on six standard question-answering benchmark datasets covering different difficulty levels of multi-hop reasoning. Since there's no perfect automatic way to grade "is this answer correct," they used an **LLM-as-a-Judge**: a separate LLM scores each answer as correct or incorrect, and the authors checked that this judge agrees closely with real human graders before trusting it.

They also tested a separate skill: how much information survives when raw text is turned into a knowledge graph and then reconstructed (the **MINE-1** benchmark) — a measure of whether the "memorizing" step itself loses facts.

## What they found

- PAI-2 beats the three competitor systems on average, and the planning mechanism (not the graph-search algorithm) is responsible for the largest share of that improvement.
- Giving the system more attempts at generating "clue-queries" per plan step (up to a point) also helps.
- PAI-2's graph-construction step keeps more of the original information intact than rival methods, setting a new best result on MINE-1.

## What could go wrong / open issues

The authors are upfront that their memory-graph design still has rough edges: dates are stored as plain text rather than structured time fields (risking loss in long contexts — the well-known **"Lost in the Middle"** problem where LLMs pay less attention to the middle of a long input), the category structure of the graph is too simple for efficient filtering, ambiguous names (e.g., "Apple" the company vs. the fruit) aren't formally disambiguated, and duplicate facts aren't merged unless they're worded identically.

## Why this matters

This paper is evidence for a broader lesson in personalized AI agents: for questions that require multiple connected facts, *how the AI decides where to look next* — adapting mid-search based on what it's already found — matters more than which graph-traversal algorithm it uses to actually walk the graph. That's a useful design principle for anyone building an AI assistant that needs to reason over a large, structured memory of facts about a person, organization, or knowledge base.

## Jargon decoder

- **GraphRAG** — Retrieval-Augmented Generation where the retrieved knowledge lives in a graph (nodes + relationships) instead of plain text chunks.
- **Knowledge graph** — a network of facts represented as nodes (entities) connected by edges (relationships).
- **LLM-as-a-Judge** — using one LLM to automatically grade the correctness of another LLM's (or system's) answers, in place of slower/costlier human grading.
- **BeamSearch** — a graph-traversal algorithm that keeps only the most promising few paths at each step, instead of exploring everything.
- **Multi-hop QA** — questions whose correct answer requires chaining together two or more separate facts (hops), rather than a single lookup.
- **Clue-query** — a narrower, reformulated question PAI-2 generates for a specific matched graph node, used to focus the next round of graph traversal.
- **MINE-1** — a benchmark measuring how much factual information is preserved when text is converted into a knowledge graph and then read back out.
- **Triple** — a single fact expressed as subject–predicate–object (e.g., "Alice — worksOn — ProjectX").
- **Ablation** — an experiment where a component is switched off (or removed) to measure how much it was contributing.
- **Lost in the Middle** — the tendency of LLMs to pay less attention to information placed in the middle of a long input context.
- **RAGAS metrics (Context Relevance, Faithfulness, Groundedness)** — automated scores that check whether retrieved context is relevant, whether the answer sticks to what the context actually supports, and whether claims are backed by evidence.
