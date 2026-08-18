> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Topologies and When to Use Them

**In one sentence:** A handful of proven node arrangements — the diamond (fan-out/fan-in), Orchestrator-Workers, Pipeline, plus Anthropic's Routing and Evaluator-Optimizer — are composable, nestable building blocks you should assemble only as far as the task truly needs, rather than reaching for vocabulary or frameworks first.

## Key points

- The industry has settled on a small set of proven topologies, and recognizing those shapes is far more useful than memorizing terminology [06:48–06:51].
- The highest-frequency shape is the **diamond** (split → parallel → merge), also called **fan-out/fan-in**: fan-out is multiple branches starting at once with no one blocking another; fan-in is the program deduplicating and classifying the results before handing them to a final drafter [06:54–07:20].
- **Orchestrator-Workers** puts a central supervisor agent in the middle, dispatching to specialized workers (research, coding, review) while handling planning and aggregation itself; it is the core pattern behind **Anthropic's** research system, where the lead agent sets strategy and spawns subagents that act as parallel "intelligent filters" [07:23–07:43].
- A **Pipeline** is a fixed sequence of steps where each step consumes the previous step's output, with optional programmatic checkpoints to keep the flow on track; it trades latency for higher accuracy because every model call becomes a simpler task [07:46–08:02].
- These three are not mutually exclusive framework choices but **composable, nestable blocks** — real production systems often wrap several diamonds inside an orchestrator, and a pipeline inside the diamond [08:04–08:13].
- Anthropic's *Building Effective Agents* adds two shapes: **Routing** (classify the input first, then route to specialized handling — separation of concerns when one prompt optimized for one input type would drag down another) and **Evaluator-Optimizer** (one node generates, another scores it, loop until the bar is met — when there is a clear evaluation standard and iteration demonstrably improves quality) [08:15–08:38].
- Anthropic's **simplicity-first** stance: find the simplest solution first and only add complexity when truly needed — many applications work with a single model call plus retrieval, needing no agent at all, let alone a graph [08:41–08:52].
- Frameworks like **LangGraph**, **Bedrock**, and **Rivet** simplify raw-call plumbing, tool parsing, and call-chaining so you start fast, but they add an abstraction layer that hides the underlying prompts and responses (making debugging harder) and tempt you to over-complicate a system a simple solution would have solved — so start from the raw model API and, if you use a framework, make sure you understand the code underneath it [08:53–09:18].

---

## Proven topologies beat vocabulary

The section opens on the practical question of how to arrange the graph [06:47]. Rather than a list of buzzwords, the industry has settled on a few topologies that have survived real use [06:48]. The explicit advice: recognizing these shapes is far more useful than memorizing the terms [06:51]. Everything that follows is catalogued as a shape you can recognize and place, not a concept to recite.

## Diamond — fan-out / fan-in

The single most frequent shape is the **diamond**: split the work, run the branches in parallel, then merge [06:54–06:56]. In more precise terms it is **fan-out / fan-in**, the canonical shape of a parallel workflow [06:58–07:01].

**Worked example from the video's own production** [07:03–07:20]: When the host wrote the very article being discussed, three agents were launched at once:

| Branch | Role | Fan direction |
| --- | --- | --- |
| Agent 1 | Reads the original X post | part of fan-out |
| Agent 2 | Translates the official documentation | part of fan-out |
| Agent 3 | Reviews community discussion | part of fan-out |

All three branches start simultaneously and no one waits for another — this is **fan-out** [07:11–07:12]. When the material comes back, the program first deduplicates and classifies it [07:15], and only then is it handed to a final drafting agent — this is **fan-in** [07:17–07:19]. The two actions chained together are what make the diamond [07:20].

> Key mechanic: the fan-in merge is not "stitch the three outputs together" — it is a **programmatic** step (dedup + classify) that runs *before* any model call writes the final draft. That is the certainty the section keeps returning to: determinism is inserted at the merge, not left to the model.

## Orchestrator-Workers

The second shape is the **Orchestrator-Workers** pattern [07:23–07:25]. A supervisor agent sits in the middle and dispatches tasks to specialized workers — research, coding, review — while it itself is responsible for planning and aggregation [07:25–07:31].

This is explicitly identified as the **core pattern behind Anthropic's research system** [07:32–07:36]. Its dynamics [07:36–07:43]:

- the lead agent analyzes the problem, sets strategy, and spawns subagents;
- the subagents behave like **intelligent filters**, gathering information **in parallel**;
- the results are then reported back to the lead agent, which synthesizes them into the final answer [07:43].

The distinction from the diamond is where the decision-making sits: in Orchestrator-Workers the central agent owns the plan and the aggregation (planning + synthesis), whereas in the diamond the join is a fixed programmatic merge step.

## Pipeline

The third shape is the **Pipeline** [07:46–07:48]. The task is broken into a fixed sequence of steps, where each step processes the output of the previous step [07:48–07:50]. You can additionally insert **programmatic checkpoints** between steps to keep the process from drifting [07:52–07:54].

**When to use it and what it costs:**

- It fits scenarios that can be **cleanly decomposed into fixed subtasks** [07:56].
- It **trades latency for higher accuracy**, because each model call becomes a simpler task [07:59–08:02].

> A pipeline is a degenerate graph: a single straight line. Its value comes entirely from the checkpoints you can put *between* the LLM calls — again, deterministic control points rather than more models.

## Composable, nestable building blocks

The three shapes are **not mutually exclusive framework choices**; they are composable, nestable blocks [08:04–08:07]. Real production systems routinely nest them [08:09–08:13]:

- the orchestrator pattern wrapping several diamonds;
- and a pipeline inside the diamond.

The point is that "which topology?" is the wrong framing in production: instead you combine a supervisor that plans, a parallel fan-out it delegates to, and a fixed pipeline inside each branch — all at once.

### Two more shapes from Anthropic's *Building Effective Agents*

Beyond the three core shapes, Anthropic's *Building Effective Agents* adds two more [08:15–08:19]:

**1. Routing** [08:21–08:30]
Classify the input first, then direct it to specialized downstream handling. It achieves **separation of concerns**. Use it when there are many kinds of input and a single prompt tuned for one type would be a drag on another.

**2. Evaluator-Optimizer** [08:32–08:38]
One node **generates**, another **evaluates and scores** it, and the pair **loops until the output meets the bar**. Use it when there is a **clear evaluation standard** and iteration demonstrably brings a visible improvement.

### The five shapes at a glance

| Shape | Core mechanic | Use it when… | Watch out for… |
| --- | --- | --- | --- |
| **Diamond** (fan-out/fan-in) [06:54] | Split → parallel → programmatic merge (dedup + classify) | Independent branches that don't depend on each other; high-frequency case | Merge step must be deterministic code, not "just concatenate" |
| **Orchestrator-Workers** [07:23] | Central supervisor plans + dispatches + synthesizes; workers are parallel filters | Problem that needs a lead agent to set strategy and aggregate dynamic sub-results (Anthropic's research system) | The supervisor is the single point of intelligence — it must be good at planning |
| **Pipeline** [07:46] | Fixed linear sequence; each step consumes the previous; checkpoints between | Task that decomposes cleanly into fixed subtasks | Adds latency; buys accuracy by making each call simpler |
| **Routing** [08:21] | Classify input → route to specialized handling | Input types vary enough that one prompt for one type hurts another | Classifier quality sets the ceiling of the downstream specialists |
| **Evaluator-Optimizer** [08:32] | Generator + scorer loop until bar is met | Clear evaluation standard and iteration measurably improves quality | Needs a real, reliable evaluator; otherwise you loop on noise |

## Simplicity first (Anthropic's stance)

Anthropic is called out for emphasizing a particular attitude [08:41–08:45]: **find the simplest solution first, and only add complexity when it is truly needed**. The concrete claim: a large number of applications are adequately served by a **single model call plus retrieval** [08:48] — they do not need an agent at all, let alone a graph [08:51–08:52].

This is the section's governing heuristic: topologies are a tool you reach for only after the simple thing has been shown insufficient, not a default architecture you decorate.

## A caution on frameworks: LangGraph, Bedrock, Rivet

The final part is a pointed caveat about agent frameworks such as **LangGraph**, **Bedrock**, and **Rivet** [08:53–08:56]. Their own guidance is described as apt:

- **What they buy you** [08:58–09:02]: they simplify the low-level plumbing — making the model calls, parsing tool calls, and chaining calls together — which lets you **start fast**.
- **What they cost** [09:04–09:12]: they tend to add a layer of **abstraction** that **covers up the underlying prompts and responses**, which makes **debugging harder**, and they can **tempt you to over-complicate** a system when a simple solution would have been enough.

**The recommendation** [09:14–09:18]:
1. Start directly with the **raw model API** — many of these patterns can be implemented in **a few lines of code**.
2. If you do reach for a framework, **make sure you understand the code underneath it**.

> The thread tying this section together is determinism, not scale. A pipeline earns its latency with checkpoints; a diamond earns its parallelism with a programmatic merge; Orchestrator-Workers earns its delegation with a lead agent that plans and synthesizes. The value of a graph is measured by how much certainty you can build around the result — and the frameworks are a convenience that risks hiding exactly the prompts and responses where that certainty lives.

**Covers:** [06:47]–[09:18] of the source video transcript
