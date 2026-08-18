# Extract wiki page 06 -- When to Graph, When Not To: Cost Data, Governance, and Frameworks

## Context

This is one worker task in a larger pipeline that turns a YouTube video transcript into an
English-language knowledge-base wiki entry. The source video is a Chinese-language tech
commentary titled "什么是图工程 | Graph Engineering | 循环工程 | Loop Engineering | ..." (English:
"What Is Graph Engineering? From Loop Engineering to Multi-Agent Orchestration"), published by
the channel 最佳拍档 (host: 大飞). It argues that "Graph Engineering" is the latest layer in a
five-layer evolution of AI agent engineering (prompt -> context -> harness -> loop -> graph
engineering), explains what a graph actually is, when to use which topology, and when NOT to
bother.

**IMPORTANT -- context is tight on this model. Read ONLY the one input file listed below. Do
NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for
style reference", and do NOT read the other chunk files. The format contract below is the only
convention you need. If this is a retry, do not try to diagnose the previous failure by reading
logs -- just re-read the input chunk and write the output directly.**

## Input

Read exactly this one file (a timestamped, Chinese-language transcript segment,
`[MM:SS] <text>` per line):

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/chunks/06.txt
```

## What this chunk covers

This chunk covers (in Chinese, with [MM:SS] timestamps) -- it is long and
covers several distinct but related closing arguments; give each its own subsection:
- **Don't graph for the sake of graphing.** Explicitly attributed to Anthropic, not the
  narrator's personal opinion: they have seen many teams spend months building complex
  multi-agent architectures only to later find that improving a single agent's prompt achieves
  the same result.
- **Anthropic's own cost/benefit numbers**: their multi-agent research system beat a
  single-agent system by 90.2% on an internal eval -- but multi-agent systems consume roughly
  15x the tokens of an ordinary chat conversation, and token usage alone explains about 80% of
  the performance variance. Conclusion: multi-agent is genuinely stronger, but that strength is
  bought with tokens, so it's only worth it for tasks whose value clears that cost.
- **Anthropic's three scenarios where multi-agent is clearly justified**:
  1. Context isolation -- when a subtask would generate a lot of information irrelevant to the
     main task, isolate it into a separate subagent to keep the main context clean.
  2. Parallelizable tasks -- work that splits into independent branches that can run
     simultaneously, exploring a larger search space than one agent could -- especially good
     for breadth-first research/search.
  3. Specialization -- different steps need different tools, prompts, or focus; splitting them
     up improves tool-selection accuracy and task focus.
  - The converse: if a task has one goal, one domain, and one clear stopping condition, a single
    clean loop is the optimal solution.
- **A governance red line**: while a graph's TASK structure (how work is split/merged) can be
  adjusted flexibly on the fly -- call this the "work graph", which can change quickly -- things
  like who has authority to modify a database or bypass an approval step are long-lived
  permissions that must NEVER be improvised by the model in the moment; call this the "role
  graph", which must change slowly and remain auditable. Otherwise what's been built is not an
  intelligent system but a production incident waiting to happen.
- **Framework landscape**: Graph engineering is not a paper concept -- LangGraph, Google ADK,
  and Microsoft AutoGen were already building agents with nodes/edges/shared state for two years
  before this term appeared. Quick comparison:
  - **LangGraph** (LangChain) -- directed graph plus conditional edges, built-in checkpointing
    and time-travel state management; good for long-running, auditable, rollback-capable
    production pipelines.
  - **CrewAI** -- role-based "crews", tasks/outputs passed in sequence; good for standardized
    role-based collaboration.
  - **Microsoft AutoGen** -- conversational GroupChat, driven mainly by conversation history;
    good for exploratory tasks needing multi-model dialogue coordination.
  - **Google ADK** -- structured graph architecture, hierarchical coordination plus the A2A
    protocol, code-first, enterprise-grade, deployable to Vertex AI.
  - A concrete efficiency detail: the same task costs LangGraph only ~2000 tokens versus
    AutoGen's ~8000 -- the difference comes from the graph structure itself, which turns
    inter-agent conversation into state transitions, eliminating the overhead of agents
    re-explaining background context to each other. This is offered as part of why LangGraph
    became the de facto enterprise production standard.
  - **LangGraph's signature feature, "durable execution"** (the term is from LangGraph's own
    docs): compiling the graph with a checkpointer attached snapshots the entire graph state at
    the end of every "super-step". This unlocks four capabilities: (1) human-in-the-loop --
    pause at any node for a human to inspect/edit/approve before resuming from that exact point;
    (2) memory -- context persists across multi-turn interactions; (3) time-travel debugging --
    rewind to any historical checkpoint to replay or even fork a new path; (4) fault tolerance --
    if a node fails, restart from the last successful step instead of from scratch. A related
    detail: "pending writes" -- if one node fails within a super-step, the outputs of other
    nodes that already succeeded in that same super-step are preserved, so recovery doesn't
    re-run the nodes that already succeeded. These engineering details are framed as exactly
    what turns agents from demoable prototypes into production-ready systems.
- **Is graph engineering just old pre-ReAct workflows again?** Answer: similar in form, not in
  substance. Old workflows had a fixed path and hard-coded node logic -- like a fixed assembly
  line that cannot bend when something unexpected happens. ReAct went to the opposite extreme --
  letting the model think-and-act the whole way through, which is flexible, but the entire
  control flow lives inside the model's repeated conversation turns, so afterward you can only
  "archaeologically" dig through a messy transcript to ask why it did something -- hard to
  reproduce, hard to audit, easy to lose control of. Graph engineering's cleverness is that it
  splits "stable" and "flexible" into two separate layers instead of forcing a choice: because
  the edges and overall structure are fixed, the system can be governed and audited, while nodes
  retain internal autonomy, so it stays flexible enough to handle real problems. This echoes
  Anthropic's own definitions: a workflow is a system orchestrated through predefined code
  paths; an agent is a system where the LLM dynamically decides its own process; a graph is
  precisely the fusion of the two -- predefined edges framing dynamic nodes. So it returns only
  to the SHAPE of old workflows; the core is completely different: old workflow nodes are dead
  code, graph nodes house agents capable of autonomous reasoning -- somewhat like packing
  ReAct's flexibility into a governable skeleton.
- **Final verdict on "hype or real"**: it is both a naming event and a genuine shift in vantage
  point. The naming part is hollow -- nodes, edges, state, directed-graph scheduling, state
  machines, multi-agent orchestration are decades-old computer science, and LangGraph/ADK/AutoGen
  have been doing this in practice for over two years; this particular term will likely be
  replaced by the next buzzword within months, just as happened to Loop Engineering. But the
  vantage-point shift is real: three things have now come together -- models strong enough to
  reliably act as autonomous nodes, frameworks mature enough to wire them together reliably, and
  a community large enough to have converged on shared vocabulary. Engineering focus has
  genuinely moved up a level, from programming ONE agent's behavior to programming the
  ORGANIZATION of a group of agents -- and that shift is real because it builds systems a single
  loop could never build. Closing observation: after all this AI effort, what we circle back to
  needing is the oldest discipline there is -- how to manage an organization (division of labor,
  defining authority/responsibility, separating doers from overseers, preventing total collapse
  when one part fails) -- questions human companies have wrestled with for centuries, now just
  asked again with a new set of "employees".
- **Three closing recommendations** (list all three as distinct key points):
  1. Don't graph for the sake of graphing -- if a clean loop can handle it, don't complicate it;
     first sketch a small graph simple enough to explain on a napkin (Anthropic's first
     principle, repeated).
  2. A graph's value comes from determinism, not from agent count -- let the model judge, let
     code backstop it, and add one independent pair of eyes whose whole job is to find fault.
  3. Most critical of all: a graph must stay grounded in reality with real-world anchors --
     otherwise no matter how precisely engineered, it's just a more organized hallucination
     factory.

## Output

Write the wiki page to:

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/wiki/06-when-to-graph-frameworks-and-governance.md
```

## Wiki page format contract (follow exactly)

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# <Topic Title>

**In one sentence:** <the page's whole argument, one sentence>

## Key points

- <5-8 bullets, each a COMPLETE, standalone claim with real content -- numbers,
  mechanisms, named concepts, conclusions. NOT topic labels like "discusses X".
  Someone who reads only these bullets must have the substance of this page.>

---

## <First subsection mirroring the source's own structure>

<full detail: hierarchical ## subsections, exact numbers/terms/named concepts,
tables where useful, quotes attributed to the people named in the chunk (e.g.
Peter Steinberger, David Khourshid, Boris Cherny, Anthropic). Cite timestamps
like [03:24] next to major points so a reader can jump to that moment in the
source video.>

## <More subsections as needed>

...

**Covers:** [<start MM:SS>-<end MM:SS>] of the source video transcript
```

Rules:
- Output MUST be written in English, even though the source chunk is in Chinese --
  translate and synthesize, do not leave any Chinese text in the output file.
- Every named concept, framework, number, or person in the chunk must appear in the
  page (e.g. "90.2%", "15x tokens", "2000 vs 8000 tokens", "Boris Cherny", "Peter
  Steinberger", "LangGraph", "AutoGen", "CrewAI", "Google ADK", "Anthropic").
- No line limit. Be thorough -- this is the deep rung of the wiki, not a summary.
- If this file already exists (a retry), overwrite it completely.


## Scope & constraints

- Touch ONLY the one output file listed above. Do not edit or create any other file.
- Do not run any git commands -- this KB directory auto-syncs on its own.
- Do not run `fleet serve restart` / `fleet run` or any other fleet supervisor command.

## Definition of Done

1. The output file above exists and is written in English, following the format contract.
2. `bd close <own-task-id> --reason "wiki page 06 extracted"`
