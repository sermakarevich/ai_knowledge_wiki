> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Targeted: Agentflow graph orchestration vs fleet queue model
**In one sentence:** Agentflow is programmatic Python graph orchestration whose DAG (Directed Acyclic Graph, a workflow with no loops) paradigm contrasts with fleet's queue model, and fleet can borrow fanout/reduce parallelism, cycle-until-LGTM loops, and pluggable remote-execution targets.
## Key points
- Borrow fanout (splitting one task into many parallel copies) plus merge reducers for map-reduce over beads tasks.
- Borrow cycle-until-LGTM (LGTM means Looks Good To Me, a human approval signal) loops: a review node with a success rule plus an on_failure back-edge to the worker.
- Borrow batch versus group reducers: one reducer per N-item batch, or one reducer per field combination.
- Borrow per-branch workspaces from fanout derive maps so parallel workers do not clobber shared files.
- Borrow node templating (`{{ nodes.x.output }}`, `{{ item.scope }}`, `{{ fanouts.name.nodes }}`) so later steps can read earlier outputs.
- Borrow success_criteria as pass/fail gates (`output_contains`, `file_exists`, `file_contains`, `file_nonempty`) instead of exit-code-only checks.
- Borrow pluggable runners per step (local, container, SSH, EC2, ECS) with shared cloud machines for sequential steps.
---
## Design principles
Agentflow builds workflows as Python code, not as static config files. You write a `Graph` block, create nodes with helpers, and wire them with `>>` edges. The graph is then validated and run by an orchestrator that respects dependencies, limits concurrency, and handles loops.

Fleet works the opposite way. Fleet is a queue-model orchestrator with YAML workflows and beads tasks: work items sit in a queue, workers pick them up, and scheduling is driven by task state rather than by a fixed graph of edges. There is no single DAG (Directed Acyclic Graph, a workflow with no loops) object that owns the whole run.

The scale difference shows in the 94-node pipeline example: 1 plan node, then a fanout (splitting one task into many parallel copies) to 64 workers, then 8 batch merges with `size=8`, then a second fanout to 16 reviews, then 4 review merges grouped by field, then 1 final synthesis node. Total is 1 + 64 + 8 + 16 + 4 + 1 = 94. In Agentflow this is five lines of wiring: `>>` from plan to workers, `merge(..., size=8)` for batches, a second `fanout()` for reviewers, `merge(..., by=[...])` for grouped reviews, and a final `>>` to synthesis. In a queue model the same shape would need 94 task rows plus manual grouping logic.

The contrast: Agentflow makes the whole pipeline visible as code with explicit fanout and merge points, while fleet makes each task independent and flexible but leaves grouping, merging, and retry loops to the operator.
## Worker restart handling
Agentflow restarts workers with three cooperating pieces: `max_iterations` loops, `success_criteria` gates, and on_failure back-edges.

`max_iterations` caps how many times a cycle may repeat (`agentflow/dsl.py:90`). The orchestrator counts restarts per failed tail node and only re-queues while the count is below the limit, otherwise it emits `node_cycle_exhausted` (`agentflow/orchestrator.py:981`).

`success_criteria` decides pass or fail after each run. Four rule kinds exist and all must pass: `output_contains` checks node output text, plus `file_exists`, `file_contains`, and `file_nonempty` checks on the work folder (`agentflow/success.py:43`). The classic example is a review node that passes only when its output contains LGTM (LGTM means Looks Good To Me, a human approval signal):

```python
    review = claude(
        task_id="review",
        prompt=(
            "Review this implementation for correctness and completeness.\n\n"
            "{{ nodes.write.output }}\n\n"
            "If the implementation is complete and correct, respond with exactly: LGTM\n"
            "Otherwise, list specific issues that must be fixed."
        ),
        success_criteria=[{"kind": "output_contains", "value": "LGTM"}],
    )
```

Verbatim from `examples/iterative_impl.py:19-28`.

`on_failure` edges wire the loop. A normal edge runs on success; an on_failure edge restarts targets on failure (`agentflow/dsl.py:73`). The proxy appends target ids to `on_failure_restart` (`agentflow/dsl.py:27`). Verbatim wiring from `examples/iterative_impl.py:38-40`:

```python
    write >> review
    review.on_failure >> write  # loop until LGTM
    review >> summary           # proceed to summary on success
```

When the tail node fails, the scheduler resets that node plus its on_failure restart targets and the nodes between them back to pending (`agentflow/orchestrator.py:954`). Reset clears output and status (`agentflow/orchestrator.py:112`). Nodes whose dependencies failed without an on_failure path are marked skipped with reason `upstream_failure` (`agentflow/orchestrator.py:844`). Per-attempt retries with backoff sit one level below, inside node execution (`agentflow/orchestrator.py:540`).
## Conflict resolution
Parallel fanout branches avoid clobbering (overwriting each other's files) through isolation, not through locks. Each copy gets its own workspace folder from a `derive` map and its own artifact folder keyed by node id.

Verbatim shard contract from `examples/airflow_like_fuzz_batched.py:55-56` and `examples/airflow_like_fuzz_batched.py:76`:

```python
            target={"cwd": "{{ item.workspace }}"},
```

```python
        derive={"workspace": "agents/agent_{{ item.suffix }}"},
```

Each node id gets its own artifact directory (`agentflow/store.py:55`), and artifact paths are built per node id (`agentflow/context.py:11`). An optional worktree mode gives each local node its own git worktree folder and branch (`agentflow/worktree.py:9`). Shared files such as crash registries are append-only with locking, by prompt contract rather than by the engine.

Merging is done by a reducer (a step that combines many parallel outputs into one). `merge()` needs exactly one mode: `size=N` for one reducer per N-item batch, or `by=[fields]` for one reducer per field combination (`agentflow/dsl.py:272`, `agentflow/dsl.py:329`, `agentflow/dsl.py:331`). A batch reducer sees only its own members through `item.scope` (`agentflow/dsl.py:307`), and reducer prompts loop over member outputs with Jinja (a text template system with `{{ ... }}` placeholders) such as `{% for shard in item.scope.with_output.nodes %}` (`examples/airflow_like_fuzz_batched.py:92`). A final node can read the whole fanout group through `fanouts.<name>`, for example `{% for r in fanouts.review.nodes %}` (`examples/code_review.py:41`).
## Workflow abstraction
Workflows are plain Python. A `Graph` context manager makes the graph active, node helpers register into it, and exiting the block restores the previous context (`agentflow/dsl.py:114`). The constructor holds pipeline settings such as `concurrency` and `max_iterations` (`agentflow/dsl.py:81`, `agentflow/dsl.py:88`, `agentflow/dsl.py:90`). `DAG = Graph` is kept for old code (`agentflow/dsl.py:194`). Graphs export to runnable JSON with `to_json` (`agentflow/dsl.py:156`).

Edges use the `>>` operator: `a >> b` makes `b` depend on `a`, `plan >> [implement, review]` fans out to two nodes, and `[a, b] >> merge` joins them. Failure loops use on_failure edges: `review.on_failure >> write` restarts `write` when `review` fails (`agentflow/dsl.py:73`, `agentflow/dsl.py:27`).

Node templating connects steps without code plumbing. Prompts are plain strings with placeholders: `{{ nodes.plan.output }}` inserts the output of node `plan`, `{{ item.workspace }}` inserts the per-copy workspace of a fanout member, and `{{ fanouts.review.nodes }}` lists a whole fanout group. Templates render before launch via a shared helper (`agentflow/context.py:212`).

The two scaling primitives are fanout and merge. `fanout()` expands one node into many parallel copies with int, list, or dict sources (`agentflow/dsl.py:213`). `merge()` reduces a fanout group in exactly one of two ways: `by=[...]` for grouped reducers or `size=N` for batched reducers (`agentflow/dsl.py:272`). Each reducer sees `item.scope` with member outputs, plus `member_ids`, `source_group`, and `source_count` (`agentflow/dsl.py:293`).
## Multi-harness support
A harness is the wrapper that launches an AI agent with a prompt and tools. Agentflow ships three small node constructors: `codex`, `claude`, and `kimi`. Each takes a task id, a prompt, and optional settings, and all forward to one shared node builder (`agentflow/dsl.py:350`, `agentflow/dsl.py:354`, `agentflow/dsl.py:358`):

```python
def codex(*, task_id: str, prompt: str, **kwargs: Any) -> NodeBuilder:
    return _node(AgentKind.CODEX, task_id=task_id, prompt=prompt, **kwargs)
```

Verbatim from `agentflow/dsl.py:350-351`. The `claude` and `kimi` constructors have the same shape (`agentflow/dsl.py:354`, `agentflow/dsl.py:358`).

Each harness builds a CLI (Command-Line Interface, a program you run in a terminal) call in its adapter `prepare()` step: Codex picks `read-only` versus `workspace-write` sandbox from the `tools=` knob (`agentflow/agents/codex.py:67`), Claude builds a streaming-JSON call with permission bypass (`agentflow/agents/claude.py:37`), and Kimi builds a print-mode streaming call with auto-approve (`agentflow/agents/kimi.py:14`). A registry maps each agent kind to its adapter class and lets you replace one with `register()` (`agentflow/agents/registry.py:13`). Because all three share the same `NodeBuilder`, a single graph can mix them freely, for example plan with Codex, implement with Claude, review with Kimi, with cross-outputs wired by `{{ nodes.<id>.output }}` templating (`examples/multi_agent_debate.py:18`).
## What fleet can borrow
1. fanout plus merge reducers for YAML workflows. Add a `fanout:` step that expands one task template into N beads tasks, plus a `merge:` step with `size=N` or `by=[field]` modes. Mirrors `fanout()` (`agentflow/dsl.py:213`) and `merge()` batch/group modes (`agentflow/dsl.py:329`, `agentflow/dsl.py:331`).
```yaml
  # fleet-sketch proposal (not agentflow code):
- step: review
  fanout: {count: 8, derive: {workspace: "agents/agent_{{ item.suffix }}"}}
- step: batch_merge
  merge: {from: review, size: 4}
```
2. Cycle-until-LGTM (LGTM means Looks Good To Me, a human approval signal) loops for workers. Add `success_criteria: [{kind: output_contains, value: LGTM}]` plus an `on_failure: restart <step>` edge with a `max_iterations` cap. Mirrors the on_failure proxy (`agentflow/dsl.py:73`), the restart-target wiring (`agentflow/dsl.py:27`), and the cycle cap (`agentflow/orchestrator.py:981`).
```yaml
  # fleet-sketch proposal (not agentflow code):
- step: review
  success_criteria: [{kind: output_contains, value: LGTM}]
  on_failure: {restart: write, max_iterations: 5}
```
3. Scoped reduce context for merge steps. Give each reducer an `item.scope` view (member ids, statuses, outputs, `with_output` subset) plus `fanouts.<name>.nodes` for full-group reads. Mirrors the scope contract (`agentflow/dsl.py:307`) and the artifact-per-node layout (`agentflow/store.py:55`).
4. Per-branch workspace isolation by default. Stamp each fanned-out beads task with its own `workspace` and `cwd` derived from `item.suffix`, so parallel fanout copies never share an output folder. Mirrors the derive pattern (`examples/airflow_like_fuzz_batched.py:76`) and per-node cwd targeting (`examples/airflow_like_fuzz_batched.py:55`).
5. Node output templating between steps. Let fleet YAML prompts reference `{{ nodes.<id>.output }}`, `{{ item.scope.with_output.nodes }}`, and `{{ fanouts.<name>.nodes }}` with Jinja rendering before launch. Mirrors the shared render helper (`agentflow/context.py:212`) and the review-merge loop (`examples/code_review.py:41`).
6. Pluggable per-step runners with shared cloud machines. Let each YAML step set `target: {kind: local|container|ssh|ec2|ecs}` with a `shared:` name for reusing one machine across sequential steps. Mirrors the runner-per-kind design (`agentflow/runners/container.py:11`, `agentflow/runners/local.py:16`) and shared-machine cleanup (`agentflow/cloud/shared.py:96`), plus per-node worktree isolation (`agentflow/worktree.py:9`).
**Covers:** wiki/01-graph-dsl.md, wiki/02-orchestration-engine.md, wiki/03-agent-harness.md, wiki/04-remote-execution.md, wiki/05-merge-and-cli.md, examples/
