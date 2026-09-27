> [[index|Wiki]] | [[digest|Digest]]

# ReAct: Synergizing Reasoning and Acting in Language Models — In Plain Language

## What is this about?

Think of cooking a new dish. You do not just chop blindly, and you do not just sit and think about food. You pause between steps: check the fridge, realize there is no salt, decide soy sauce plus pepper could work, and look up a dough recipe in a cookbook. Then you act again with this new plan.

ReAct (short for Reasoning + Acting) gives a language-model agent (an AI program built on a Large Language Model, a system trained on huge amounts of text, that can take actions like searching or clicking) this same loop. The agent writes down short inner thoughts between its actions. The thoughts do not change the outside world — they only organize the plan. The actions do change things: they fetch facts from somewhere outside, like a Wikipedia search, or move objects in a simulated house or shop. Thinking guides acting, and acting feeds fresh facts back into thinking.

The digest presents this as one combined method. Pure thinking without acting can invent facts. Pure acting without thinking acts blindly and cannot keep track of a longer goal. ReAct interleaves the two so each side covers the other's weakness.

## Why does it matter?

Before ReAct, there were two common styles, and each had a clear failure.

The first style is step-by-step reasoning alone (called CoT, short for chain-of-thought). It thinks through a problem in words but never checks the outside world, so it can sound confident while inventing facts, and one early mistake spreads into everything after it.

The second style is acting alone (earlier planners that only pick actions). It can click and search, but it has no working memory for the bigger goal, so it behaves short-sightedly — repeating dead actions or never connecting what it just saw to what to do next.

ReAct matters because, according to the digest, it fixes both at once with very little teaching (just 1–6 examples): answers stay competitive on question-answering tests while being more grounded in retrieved facts, and success jumps on decision-making tasks. Its step-by-step traces are also easier for a person to read, check, and even correct by editing a thought.

## How does it work?

1. The agent starts with a goal, for example answering a tricky question or putting a clean knife on a counter.
2. It writes a thought: break the goal into smaller steps and make a plan (find the knife, take it, clean it, put it down).
3. It takes an action in the world, such as searching Wikipedia or opening a drawer.
4. It reads the observation — what the world sent back (a search result, "nothing happens", an item found).
5. It writes the next thought: pull out the useful bit of what it just saw, track progress, and decide whether to continue, switch steps, or handle a surprise.
6. If something goes wrong (no exact search hit, a missing item, a blocked path), it adjusts the plan in words instead of repeating the same action.
7. Steps 3–6 repeat, with dense thinking-and-checking for question answering and sparser, occasional thinking for long control tasks, until the agent gives a final answer or finishes the task.
8. A person can step in and edit a thought — for example deleting one invented sentence and adding a hint — which changes what the agent believes and what it does next, rescuing a run that would otherwise fail.

## Where can this be used?

- Fact-checking and multi-step questions answered with live lookup, such as encyclopedia-style questions where the answer may have changed since the training data was written (the digest's hotel-size example).
- Claim checking, where the agent must search, read what it found, and label a claim as supported, refuted, or not provable (the digest's Bermuda Triangle, Soyuz, and film examples).
- Household-style simulated tasks where an agent must find, clean, and place objects across rooms, cabinets, and sinks.
- Online shopping tasks where the agent must compare several products and options (scent, size, pack count, price) and buy exactly the right one — the digest's banana-chips example where careful reasoning picks the correct pack for a perfect score while acting alone buys the wrong item.
- Any setting where a human supervisor wants to inspect or steer behavior by reading and editing short thoughts rather than rewriting code.

## Conclusions & takeaways

- The core idea is simple: alternate thinking and doing so plans stay flexible and facts stay fresh.
- Reported headline results from the digest: competitive grounded question answering plus about +34 points on household tasks and +10 points on shopping tasks over systems trained on thousands to hundreds of thousands of examples, and the method works across different large models.
- Human editing of thoughts is a real lever: a two-thought fix can turn many wasted actions into a success.
- Honest limits from the digest: ReAct still fails. Reasoning can slip, searches can miss (no exact hit), the model can still invent facts, and some test labels themselves are ambiguous. A stripped-down version with only vague thoughts even skips needed steps (like cleaning the knife) and then loops forever — so explicit, specific subgoal tracking matters.
- Practical lesson: if you use this style, make thoughts concrete (what subgoal, what was just learned, what changes), connect every claim to something actually observed, and keep a human-readable trace so failures can be diagnosed and corrected.

## Jargon decoder

| Term | Plain meaning |
| ---- | ------------- |
| ReAct | The method: alternate written reasoning with real actions so each guides the other. |
| LLM (Large Language Model) | An AI system trained on vast text that predicts and writes language; the "brain" of the agent. |
| Thought / reasoning trace | A short written note to self with no effect on the world; used to plan, track, and adjust. |
| Action | Something the agent does that affects or queries the world: search, look up, click, take, clean, buy. |
| Observation | What comes back after an action: a search snippet, a page fact, or "nothing happens". |
| CoT (chain-of-thought) | Thinking step by step in words without acting; powerful but can invent facts. |
| Act-only planner | An agent that only picks actions without explicit reasoning; can act blindly or repeat failures. |
| Grounding | Tying statements to facts actually retrieved from outside instead of memory alone. |
| Hallucination | Confidently stating something false or invented, e.g. a wrong collaboration story or date. |
| In-context example | A worked demonstration shown in the prompt so the model copies the pattern. |
| Human-in-the-loop editing | A person fixes the agent by rewriting one of its thoughts, changing later actions. |
