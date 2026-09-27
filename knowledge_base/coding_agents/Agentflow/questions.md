---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Agentflow

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. `fanout()` takes one node and a source. What are the three source modes, and what does each one select?

> [!tip]- Answer
> `fanout()` expands one node into many parallel copies, and the source argument selects the mode. An `int` means a plain count of copies, a `list` means one copy per explicit value, and a `dict` means a cartesian matrix over fields. Each copy receives an `item` variable carrying its index, number, count, suffix, node id, and value. See [[wiki/01-graph-dsl|Graph DSL]].

### Q2. `merge()` requires exactly one of two modes. What does each mode produce?

> [!tip]- Answer
> `merge()` reduces a fanout group in exactly one of two ways. `by=[...]` makes one reducer per unique field combination (grouped reduce), while `size=N` makes one reducer per N-item batch (batched reduce). Each reducer sees only its own members through `item.scope` with member outputs. See [[wiki/05-merge-and-cli|Merge Reducers and CLI]].

### Q3. How is a write-review loop wired so that failure retries the worker while success moves forward, and what does the orchestrator reset on failure?

> [!tip]- Answer
> Normal edges run on success while `on_failure` edges run on failure, so `review.on_failure >> write` restarts the worker when review fails and `review >> summary` continues on success. When a node with `on_failure_restart` fails, the orchestrator resets that node plus its restart targets and the nodes between them back to pending so they re-execute. Nodes whose dependencies failed without such a path are instead marked skipped. See [[wiki/02-orchestration-engine|Orchestration Engine]].

### Q4. What does a `success_criteria` rule of `output_contains` with value LGTM check, and what are the other rule kinds?

> [!tip]- Answer
> After a worker finishes, success rules decide pass or fail, and all configured rules must pass. `output_contains` checks whether the node output holds a value such as LGTM (Looks Good To Me, an approval signal), so a review node passes only when its output contains LGTM. The other kinds check the work folder: `file_exists`, `file_contains`, and `file_nonempty`. See [[wiki/02-orchestration-engine|Orchestration Engine]].

### Q5. Each node picks its machine with `target={"kind": ...}`. Which kinds exist, and what does each run on?

> [!tip]- Answer
> The registry maps `local`, `container`, `ssh`, `ec2`, and `ecs` to a runner class per node. Local runs the command directly while container wraps the same logic in a `docker run` call, and ssh (Secure Shell, a remote-login protocol) shells out to the system `ssh` binary. EC2 (Elastic Compute Cloud, rentable virtual machines) launches cloud machines per node or one shared machine, while ECS (Elastic Container Service, containers on AWS) builds and pushes a Docker image, then polls logs until the task stops. See [[wiki/04-remote-execution|Remote Execution]].

### Q6. Two parallel branches run at the same time and both write files. Why don't they overwrite each other?

> [!tip]- Answer
> Each node renders with its own separate result dict plus a scoped `item.scope` view for the current member, so one branch never sees another branch's variables. Each copy also gets its own workspace folder from the fanout `derive` map and its own artifact folder keyed by node id. Parallel agents share findings only through an explicit shared scratchboard file merged line by line, never through shared working files. See [[wiki/03-agent-harness|Agent Harnesses]].

### Q7. What breaks if `max_iterations` is removed from a pipeline with a review-write cycle?

> [!tip]- Answer
> Cycles are capped by `max_iterations`: each failed tail node counts its restarts and only re-queues while the count stays below the limit, otherwise it emits `node_cycle_exhausted`. Without the cap, a never-passing review-write loop would reset and re-queue forever instead of terminating. Per-attempt retries with backoff sit one level below inside node execution and cannot stop the cycle on their own. See [[wiki/02-orchestration-engine|Orchestration Engine]].

### Q8. Contrast Agentflow's graph paradigm with fleet's queue model. What does each make easy, and what does each leave to the operator?

> [!tip]- Answer
> Agentflow builds workflows as programmatic Python: one `Graph` owns the whole run with explicit edges, fanout and merge points, and dependency-ordered scheduling. Fleet is a queue model with YAML workflows and task entries: items sit in a queue, workers pick them up, and no single DAG (Directed Acyclic Graph, a workflow with no loops) object owns the run. The graph makes the full pipeline visible with declarative grouping, merging, and retry loops, while the queue keeps single tasks independent and flexible but leaves grouping, merging, and retry loops to the operator. See [[wiki/targeted|Targeted Comparison for Fleet]].

### Q9. Sketch how you would add a cycle-until-LGTM loop to a fleet YAML workflow for a write step and a review step.

> [!tip]- Answer
> Give the fleet review step a `success_criteria` gate of `output_contains` with value LGTM plus an `on_failure` restart pointing at the write step with a `max_iterations` cap such as 5. Wire the review output back into the worker prompt with `{{ nodes.review.output }}` templating so each retry fixes the listed issues. Failed reviews then loop the worker until LGTM or the cap, mirroring the on-failure proxy and cycle cap. See [[wiki/targeted|Targeted Comparison for Fleet]].

### Q10. Across these wiki pages, what is the weakest evidence link in the case being made?

> [!tip]- Answer
> The weakest link is the fleet-transfer proposal: the fanout plus merge, cycle-until-LGTM, workspace, templating, and runner borrowings mirror verified Agentflow mechanisms but cite no fleet-side implementation, test, or measurement, so they stand as sketches rather than demonstrated integrations. Treat them as design hypotheses to prototype and measure, which is the [[critical_thinking|Critical Analysis]] habit of separating verified mechanism from asserted consequence. See [[wiki/targeted|Targeted Comparison for Fleet]].
