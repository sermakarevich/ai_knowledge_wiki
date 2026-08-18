---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: What Is Graph Engineering?

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What is the one-line division of labor between Loop Engineering and Graph Engineering?

> [!tip]- Answer
> Loop Engineering solves how to make a *single* agent keep working reliably (discover → plan → execute → verify, in a closed loop). Graph Engineering solves how to organize *multiple* agents, tools, and humans into an observable, recoverable, scalable system. See [[wiki/01-five-layer-evolution|The Five-Layer Evolution]].

### Q2. Name the five inherent flaws of a loop, and the sixth, more insidious one. Why can't a "bigger, stronger loop" fix any of them?

> [!tip]- Answer
> The five: context rot (accumulated reasoning buries the original goal), error cascades (the same broken chain that erred is asked to diagnose itself), tool overload (accuracy collapses past ~15-20 tools), coarse control granularity (all-or-nothing execution, no mid-run pause/checkpoint), and poor observability (you see *what* happened, not *why* it branched). The sixth is goal blindness / Goodhart's Law — optimizing one metric to the point of betraying its intent (e.g. a support AI that raised ticket-resolution rate for 5 months while doubling churn). None are fixable by scaling the loop because their root cause is *relational* — it lives between steps/agents, not inside any single loop, the same way one disciplined employee can't substitute for a team that needs division of labor and mutual review. See [[wiki/01-five-layer-evolution|The Five-Layer Evolution]].

### Q3. What are the four formal parts of a graph (V/E/S/P), and what two things is this kind of graph explicitly *not*?

> [!tip]- Answer
> V = nodes (one-in/one-out units of work — an agent or a deterministic step), E = edges (routing: pass-through, conditional branch, fan-out, fan-in, loop-back), S = state (the shared read/write object that welds independent agents into one system), P = policy (constraints on who can create nodes, call tools, or modify the graph). It is explicitly not a slide-deck flowchart (which only *describes* an intended path for humans, without enforcing it) and not a knowledge graph (which organizes what the system *knows*, not who it's made of and how work flows). See [[wiki/02-anatomy-of-a-graph|Anatomy of a Graph]].

### Q4. A team wants to build "the diamond" (fan-out/fan-in) pattern for a research task. What specifically must the fan-in step be, and why does that matter?

> [!tip]- Answer
> The fan-in step must be a deterministic, programmatic merge (e.g. dedup + classify) that runs *before* any model call writes the final draft — not "just concatenate the outputs" and not a model deciding how to combine them. This matters because the value of the diamond (and of a graph generally) comes from the certainty you build into the merge point; letting a model do an undefined "combine" step reintroduces the same self-referential judgment problem a graph is meant to avoid. See [[wiki/03-graph-topologies|Graph Topologies]].

### Q5. When would you use Routing vs. Evaluator-Optimizer, and what is Anthropic's "simplicity-first" caveat that applies before reaching for either?

> [!tip]- Answer
> Routing: use it when input types vary enough that one prompt tuned for one type would drag down performance on another — classify first, then send to specialized handling. Evaluator-Optimizer: use it when there's a clear evaluation standard and iterating (generate → score → refine) measurably improves quality. The simplicity-first caveat: find the simplest solution first — many applications are fully served by a single model call plus retrieval and don't need an agent at all, let alone a graph or any of these topologies. See [[wiki/03-graph-topologies|Graph Topologies]].

### Q6. What is the root cause of most agent-system failures, according to the video, and what two mechanisms (beyond just "add a Verifier") does the graph use to fix it?

> [!tip]- Answer
> The root cause: the same model acts as both the athlete (producer of a conclusion) and the referee (judge of that same conclusion) — it approves its own work with no independent standard. Beyond the Verifier (a separate adversarial node that only tries to overturn conclusions), the graph adds a Router that calibrates check intensity to the stakes of the task (like hospital triage), and — most critically — anchors conclusions to code (deterministic chores handed to ordinary code, not another agent) and reality (a test that passed, a user who stayed, money that landed), since agent-only cross-checking without any real anchor is "a more elaborate self-congratulation machine." See [[wiki/04-verification-and-determinism|Verification as the Real Lever]].

### Q7. Contrast the "Adversarial" and "Judge panel" verification patterns. What question does each answer, and how do they treat the losing/failing candidates differently?

> [!tip]- Answer
> Adversarial sends multiple independent skeptics to attack the *same single* conclusion; it stands only if a majority fail to refute it — the question answered is "does it survive attack?" and failed refutations are just evidence, nothing is salvaged from them. Judge panel scores *multiple candidate solutions* in parallel, picks a winner, and then enriches the winner by absorbing good ideas from the losing candidates — the question answered is "which of these is best?", and losers are mined as assets rather than simply discarded. See [[wiki/04-verification-and-determinism|Verification as the Real Lever]].

### Q8. In the daily-research-brief worked example, why did the single-loop version's self-review "almost always stamp pass," and what specifically prevents that failure in the three-node graph version?

> [!tip]- Answer
> In the loop version, the same agent that wrote the draft reviews it inside the same shared context — it is effectively grading its own exam, with no independent standard. In the graph version, the reviewer node works in a *fresh* context that sees only the brief and the acceptance criteria (never the raw research or the writer's reasoning), making it a genuinely independent check rather than self-certification. See [[wiki/05-worked-example-loop-vs-graph|Worked Example: Daily Research Brief]].

### Q9. What decision rule determines whether the loop-to-graph "upgrade" is worth its costs in the worked example, and what are those costs?

> [!tip]- Answer
> The decision rule is repeated value vs. one-off cost: if the task runs repeatedly (e.g. daily), the overhead is amortized and repaid by real, repeated quality gains — worth it. If the task runs only once, the same overhead is pure tax with no repeated payoff — not worth it. The costs: three prompts to maintain instead of one, a state structure to design between nodes, and a new set of failure modes (e.g. bad structured notes, a writer ignoring notes, a reviewer wrongly bouncing good work). See [[wiki/05-worked-example-loop-vs-graph|Worked Example: Daily Research Brief]].

### Q10. What are Anthropic's three specific numbers on multi-agent vs. single-agent performance and cost, and what conclusion do they support?

> [!tip]- Answer
> Multi-agent beats single-agent by 90.2% on an internal eval, but consumes roughly 15x the tokens of an ordinary chat conversation, and token usage alone explains about 80% of the performance variance. The conclusion: multi-agent genuinely is stronger, but that strength is bought with tokens — so it's only worth it when the task's value clearly exceeds that token cost, not as a default upgrade. See [[wiki/06-when-to-graph-frameworks-and-governance|When to Graph, When Not To]].

### Q11. What is the difference between a "work graph" and a "role graph," and why does conflating them create a production incident risk rather than "a smarter system"?

> [!tip]- Answer
> The work graph is how tasks are split and merged — it can be adjusted flexibly on the fly, since it's just code and state. The role graph is long-lived permissions (who can modify a database, who can bypass an approval step) — it must change slowly and remain auditable and human-owned. If a model is allowed to improvise role-graph changes the way it improvises work-graph changes, you haven't built a smarter system — you've built a production incident waiting to happen, because permission changes have real-world, hard-to-reverse consequences that task-routing changes don't. See [[wiki/06-when-to-graph-frameworks-and-governance|When to Graph, When Not To]].

### Q12. Evaluation question: Is the 90.2%-improvement-for-15x-tokens figure strong enough evidence to justify multi-agent adoption broadly? What's the weakest link in that evidence, and how does that shape when you should trust "graph engineering" claims in general?

> [!tip]- Answer
> It's a single internal Anthropic evaluation on their own research-agent benchmark, not an externally replicated, peer-reviewed, or task-general result — so it should be read as "multi-agent can substantially beat single-agent on breadth-first research-style tasks in Anthropic's own setting," not as a universal multiplier applicable to any task or domain. The weakest link is generalizability: no external benchmark, no comparison against a well-tuned single-agent baseline outside Anthropic's own system, and token cost as a single variable explaining 80% of variance suggests the "improvement" may partly just be "spend more compute," which a well-optimized single loop given more compute budget might partially match. This shapes a general skepticism habit for the whole "graph engineering" pitch: treat vendor-reported multi-agent wins as directional evidence for a narrow class of tasks (parallelizable, context-isolating, specialized work), not as proof that graphs beat loops in general. See [[critical_thinking|Critical Analysis]].
