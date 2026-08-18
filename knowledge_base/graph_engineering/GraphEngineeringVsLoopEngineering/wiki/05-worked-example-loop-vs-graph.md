> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worked Example: Daily Research Brief, Loop vs. Graph

**In one sentence:** A single concrete task — producing a verified daily research brief — is built two ways (one self-reviewing agent loop vs. a three-node graph with clean state flow), to show that the graph buys real, repeatable quality gains, but only pays off when the task runs repeatedly.

## Key points

- The example is a daily research brief, a canonical scenario borrowed from Anthropic and the community precisely because it is small enough to hold in your head yet typical enough to be representative [11:19].
- The task spec: every morning, read the latest content on a given topic from a few sources, condense it into a one-page summary, and verify accuracy before it lands in the user's inbox [11:25].
- Built as a single loop, the agent dumps all raw search results into one shared context, drafts the brief, then reviews that same draft — the author grading their own exam, which "almost always stamps pass" [12:03].
- By the time the loop-agent reaches its review step, its context is a "mush": raw scraped pages, half-written sentences, and its own earlier reasoning all mixed together [11:53].
- A loop is inherently sequential, so it reads sources one at a time; the same task is therefore also slower in loop form [12:08].
- The graph version is a three-node diagram — researcher → writer → reviewer — where state flows cleanly between nodes: the researcher fans out to multiple sources in parallel and returns only structured notes; the writer receives only those clean notes, never the raw web pages; the reviewer works in a fresh context seeing only the brief and the acceptance criteria, and bounces the brief back to the writer if it fails [12:13].
- The graph's observable benefits: separate clean contexts, a writer never drowned in search noise, a genuine independent review instead of self-certification, faster parallel gathering, and a flow readable as a clear path rather than something to reverse-engineer from a long transcript [12:35].
- The honest costs of the graph: you maintain three prompts instead of one, you must design the state structure between nodes, and you inherit a new set of failure modes [12:55].
- The decision rule: for a brief that runs every day, the overhead is repaid by real, repeated quality improvement — worth it; for a task that runs only once, that overhead is pure tax with no repeated payoff. This repeated-value-versus-one-off-cost tradeoff is presented as the entire decision of whether to upgrade from loop to graph [13:04].

---

## Setup: one task, two architectures

This section ties the whole concept stack together — nodes, edges, fan-out/fan-in, validators — onto a single concrete workload and runs a head-to-head comparison against the loop [11:10].

The example is deliberately borrowed from a scenario Anthropic and the community keep reusing [11:19], chosen for being "small enough yet typical enough" [11:23]. The task:

1. Every morning, read the latest content on a given topic from several sources [11:27].
2. Compress it into a one-page summary [11:31].
3. Check accuracy before it reaches the user's inbox [11:32].

On paper it sounds simple [11:36]. That is the point: the value of the example lies in what the two ways of building it expose, not in the difficulty of the task.

## Built as a single loop: the self-critique illusion

The most intuitive architecture is one agent doing everything in one loop [11:40]:

- dump the raw search results from all sources into the context,
- draft the brief,
- then review its own draft [11:43].

The failure mode is structural, not incidental:

- **Context rot:** by the time the review step begins, the context is a soup — the original search pages, half-written sentences, and the agent's own earlier reasoning all smeared together [11:53].
- **Author grading their own exam:** the draft is reviewed inside the same context in which it was written [12:00]. The agent is effectively its own examiner, so it almost always stamps a "pass" [12:03].
- **Inherent serialization:** a loop is inherently sequential, so the agent reads sources one at a time — the same task is simply slower in loop form [12:08].

None of these follow from a weak model or a bad prompt; they follow from the single-shared-context shape of the loop.

## Built as a graph: the three-node brief pipeline

The same task as a graph is a small three-node diagram with state flowing cleanly between the nodes [12:13]:

| Node | Input | What it does | Output |
|---|---|---|---|
| Researcher | task/topic | fans out to multiple sources and gathers in parallel [12:19] | only structured notes — never raw pages [12:22] |
| Writer | clean structured notes (never sees the messy raw web pages) [12:26] | writes the brief | the one-page brief [12:28] |
| Reviewer | only the brief + acceptance criteria, in a fresh context [12:29] | checks quality; if it fails, bounces the brief back to the writer [12:33] | accept / send-back |

### Why this shape behaves differently

- **Contexts stay separate and clean** — each node owns its own context, so the search noise never contaminates the writing or the review [12:37].
- **The writer is never drowned in search garbage** — it receives only the clean, structured notes the researcher node produced [12:40].
- **The review is a genuine independent check** — a fresh context seeing only the brief and the acceptance criteria, rather than self-certification by its author [12:42].
- **Parallel gathering is faster** — the researcher node fans out to multiple sources simultaneously, where the loop could only read them one by one [12:45].
- **The flow is readable as a clear path** — you can look at the diagram and see the pipeline, instead of reverse-engineering intent from a long transcript of one agent talking to itself [12:48].

## The honest costs of the graph

The page is explicit that the graph is not free [12:55]:

- you maintain **three prompts instead of one** [12:57] — each node needs its own well-written instruction set;
- you must **design the state structure** that flows between nodes [13:00] — the contract between researcher notes, writer input, and reviewer criteria is now a surface you own;
- you inherit **a new set of failure modes** [13:02] — e.g., the researcher returning bad-structured notes, the writer ignoring the notes, the reviewer bouncing good briefs.

## The verdict: repeated value vs. one-off cost

The final judgment turns on the run cadence of the task [13:04]:

- **Daily brief:** something that runs every day amortizes the overhead — the extra prompts, state design, and new failure modes buy real, repeated quality improvements. Verdict: **worth it** [13:05].
- **One-off task:** the same overhead attached to a task that runs only once is "pure tax" with no repeated payoff [13:12].

The closing line frames this as the whole decision: the loop-to-graph upgrade reduces to a single calculation — is the task repeated enough that the one-off cost is repaid, or is there no repetition to repay it [13:16].

**Covers:** [11:08]-[13:16] of the source video transcript
