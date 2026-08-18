# Task: write wiki page 01 — Graph Engineering Defined

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read this exact file, nothing else):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/source/chunks/01.txt`

This is a transcript segment (timestamps `[00:00-04:15]`) from the YouTube video "What Is Graph Engineering?" by KGP Talkie. It covers: why graph engineering is presented as "not a new technique" (LangGraph, Google ADK, Microsoft AutoGen already do this), the stack of agentic-AI techniques (prompt engineering → context engineering → harness engineering → loop engineering → graph engineering), how loop engineering (agent-evaluates-agent, never self-prompting) composes into graph engineering when multiple such loops/solutions are coordinated together, and the "node" concept (a node is an agent, a self-prompting loop solution, or a direct LLM call, orchestrated together to reach a goal).

**Output (write exactly this file; if it already exists — a retry — overwrite it completely):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/wiki/01-graph-engineering-defined.md`

**Write the page using exactly this structure:**

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering Defined

**In one sentence:** <one sentence stating the chapter's whole argument>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (not "discusses X") — cover: the agentic-technique stack and where each layer applies (inside vs outside the agent), the definition of loop engineering as agent-evaluates-agent self-prompting, why an agent cannot self-prompt itself directly, the definition of graph engineering as multiple coordinated loop-engineering solutions, the node concept and what a node can be>

---

## The agentic-technique stack

<hierarchical prose covering prompt/context/harness engineering (input side of an agent), loop engineering (outside the agent), and graph engineering (coordinating multiple loop-engineering solutions together)>

## Loop engineering recap: self-prompting via evaluation, not self-reference

<explain: agent one produces a response, agent two evaluates it and re-prompts agent one; this two-agent arrangement is a "self-prompting solution"; a single agent cannot self-prompt itself>

## From loop to graph: nodes and orchestration

<explain: arranging multiple self-prompting solutions (e.g., named as solution one/two/three, such as a "viewer agent") in a coordinated manner produces a graph; each node in that graph can be an agent, a loop-engineering solution, or a direct LLM call; nodes are orchestrated to achieve a goal; note the presenter's framing that this is not a new technique — LangGraph, Google ADK, and Microsoft AutoGen have used this for years, it is only a new name>

---

**Covers:** 00:00-04:15
```

**Scope:** touch ONLY the one output file listed above. Do not run any fleet commands other than `bd close`.

**DoD:** output file written → `bd close <own-id> --reason "chunk 01 extracted"`. No git commands — `.kb` auto-syncs.
