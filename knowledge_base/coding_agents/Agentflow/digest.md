> [[index|Wiki]] | [[summary|Summary]]
# Agentflow — Digest
Six pages condensed to one line and key points each.

## 1. [[wiki/01-graph-dsl|Graph DSL: programmatic orchestration]]
**In one sentence:** The Graph DSL is the Python code layer that builds agent pipelines with nodes, edges, parallel copies, and retry loops, then converts them to a validated specification for execution.
## Key points
- `Graph` is a Python context manager: `with Graph(...):` makes the graph active, node helpers register into it, and exit restores the previous context (`agentflow/dsl.py:114`).
- Edges use the `>>` operator: `a >> b` makes `b` depend on `a`, `plan >> [implement, review]` fans to two nodes, and `[a, b] >> merge` joins them (`agentflow/dsl.py:48`).
- `fanout()` expands one node into many parallel copies with three source modes: `int` for count, `list` for explicit values, `dict` for cartesian matrix (`agentflow/dsl.py:247`).
- `merge()` reduces a fanout group in exactly one of two ways: `by=[...]` for one reducer per field combination, `size=N` for one reducer per N-item batch (`agentflow/dsl.py:325`).
- Prompts use Jinja templating (Jinja = a text template system with `{{ ... }}` placeholders): `{{ nodes.plan.output }}` inserts the output of node `plan` (`examples/airflow_like.py:13`).
- Failure loops use `on_failure` edges: `review.on_failure >> write` restarts `write` when `review` fails, while `review >> summary` continues on success (`agentflow/dsl.py:72`).
- `Graph` run knobs are `concurrency` for parallel workers and `max_iterations` for loop limit, validated as `concurrency >= 1` and `max_iterations >= 1` (`agentflow/dsl.py:88`, `agentflow/specs.py:1385`).

## 2. [[wiki/02-orchestration-engine|Orchestration engine: scheduling, cycles, and restarts]]
**In one sentence:** The orchestrator runs pipeline nodes in dependency order, limits how many run at once, checks success rules, and retries or restarts failed work until the run completes, fails, or is cancelled.
## Key points
- Nodes run in dependency order: a node becomes ready only when every node in its `depends_on` list is completed, so the graph executes in topological order (`agentflow/orchestrator.py:871`).
- Upstream failure blocks downstream work: nodes whose dependencies failed, were skipped, or were cancelled are marked skipped with reason `upstream_failure` (`agentflow/orchestrator.py:834`).
- Concurrency is bounded by a semaphore: the run loop creates one semaphore from `pipeline.concurrency` and each launch runs inside it (`agentflow/orchestrator.py:783`).
- Cycles are capped by `max_iterations`: each failed tail node counts its restarts, and only restarts while the count is below `pipeline.max_iterations`, otherwise it emits `node_cycle_exhausted` (`agentflow/orchestrator.py:961`).
- Success rules decide pass or fail: `output_contains` checks whether the node output holds a value such as LGTM (LGTM = Looks Good To Me, a human approval signal), alongside `file_exists`, `file_contains`, and `file_nonempty` checks (`agentflow/success.py:43`).
- Failure edges re-queue work: when a node with `on_failure_restart` fails, the orchestrator resets that node plus its restart targets and the nodes between them back to pending (`agentflow/orchestrator.py:954`).
- Worker failure and restarts are handled at two levels: per-attempt retries with backoff inside `_execute_node`, plus scheduler-level re-queue of finished nodes requested by a periodic controller (`agentflow/orchestrator.py:540`, `agentflow/orchestrator.py:986`).
- State survives in the store and traces: run state is written to `run.json`, events are appended to `events.jsonl`, and per-node output plus trace events are saved as artifacts (`agentflow/store.py:64`, `agentflow/store.py:71`, `agentflow/orchestrator.py:705`).

## 3. [[wiki/03-agent-harness|Agent harnesses: codex, claude, kimi nodes]]
**In one sentence:** Three small wrappers (a harness = the wrapper that launches an AI agent with a prompt and tools) turn pipeline nodes into command-line calls to the Codex, Claude, and Kimi CLIs (CLI = Command-Line Interface, a program you run in a terminal).
## Key points
- You create nodes with `codex(task_id=..., prompt=..., **kwargs)`, `claude(task_id=..., prompt=..., **kwargs)`, and `kimi(task_id=..., prompt=..., **kwargs)`, which all forward to one shared node builder (`agentflow/dsl.py:350`, `agentflow/dsl.py:354`, `agentflow/dsl.py:358`).
- The `tools=` knob defaults to read-only and switches Codex between `read-only` and `workspace-write` sandboxes (`agentflow/agents/codex.py:31`, `agentflow/agents/codex.py:70`).
- The same `tools=` knob switches Claude between a read-only tool list and a longer read-write list that adds `Write`, `Edit`, and `Bash` (`agentflow/agents/claude.py:13`, `agentflow/agents/claude.py:26`, `agentflow/agents/claude.py:52`).
- Prompts can reuse earlier outputs with placeholders such as `{{ nodes.claude_solve.output }}`, as shown in the debate example (`examples/multi_agent_debate.py:18`, `examples/multi_agent_debate.py:26`), and they are rendered with a shared template helper (`agentflow/context.py:231`).
- A registry maps each agent kind to its adapter class (`CodexAdapter`, `ClaudeAdapter`, `KimiAdapter`) and lets you replace one with `register()` (`agentflow/agents/registry.py:13`, `agentflow/agents/registry.py:22`).
- Parallel branches stay isolated because the render context builds a separate result dict per node and a scoped `item.scope` view for the current member (`agentflow/context.py:157`, `agentflow/context.py:190`).
- Parallel agents can still share findings through a shared scratchboard file, merged line by line with de-duplication or appended under a `## From <node_id>` header (`agentflow/scratchboard.py:30`, `agentflow/scratchboard.py:48`, `agentflow/scratchboard.py:59`).
- Named skills are loaded from local files and prepended to the prompt as a `Selected skills:` prelude, or listed as unresolved names when no file is found (`agentflow/skills.py:27`, `agentflow/context.py:232`).

## 4. [[wiki/04-remote-execution|Remote execution: SSH, EC2, ECS runners]]
**In one sentence:** Agentflow can run an agent step on your own machine, in a local Docker container, or on AWS cloud machines using SSH (Secure Shell, remote login protocol), EC2 (Elastic Compute Cloud, rentable virtual machines on AWS), and ECS (Elastic Container Service, running Docker containers on AWS).
## Key points
- Each node picks its machine with `target={"kind": ...}`; the registry maps `local`, `container`, `ssh`, `ec2`, and `ecs` to a runner class (`agentflow/runners/registry.py:13`).
- SSH (Secure Shell, remote login protocol) execution shells out to the system `ssh` binary with no extra Python dependency, using `BatchMode=yes` and `StrictHostKeyChecking=accept-new` (`agentflow/runners/ssh.py:23`, `agentflow/runners/ssh.py:34`).
- EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) by default launches one fresh virtual machine per node, waits for SSH (Secure Shell, remote login protocol), runs the command, then terminates the machine (`agentflow/runners/ec2.py:25`, `agentflow/runners/ec2.py:76`, `agentflow/runners/ec2.py:250`).
- Nodes that set the same `shared` name reuse one EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) machine; the manager launches on first use, returns the same address on later use, and terminates only after the last user releases it (`agentflow/runners/ec2.py:234`, `agentflow/cloud/shared.py:54`, `agentflow/cloud/shared.py:96`).
- EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) auto-discovery fills in a missing AMI (Amazon Machine Image, a template for a virtual machine), SSH (Secure Shell, remote login protocol) key pair, and VPC (Virtual Private Cloud, your private network section in AWS) network when you omit them (`agentflow/runners/ec2.py:109`, `agentflow/cloud/aws.py:67`, `agentflow/cloud/aws.py:85`, `agentflow/cloud/aws.py:11`).
- ECS (Elastic Container Service, running Docker containers on AWS) Fargate builds a Docker image with the agent tools, pushes it to ECR, registers a task definition, and polls CloudWatch logs until the task stops (`agentflow/runners/ecs.py:25`, `agentflow/runners/ecs.py:133`, `agentflow/runners/ecs.py:199`).
- Local runs the command directly as a child process while container wraps the same local logic in a `docker run --rm` call with mounted work folders; container is a subclass of the local runner (`agentflow/runners/local.py:278`, `agentflow/runners/container.py:18`, `agentflow/runners/container.py:11`).
- Zero-config is partial: you can omit AMI (Amazon Machine Image), key, subnets, and cluster, but you still need AWS credentials, boto3, a default VPC (Virtual Private Cloud), Docker for ECS (Elastic Container Service) builds, and agent login keys forwarded from your machine (`agentflow/cloud/aws.py:22`, `agentflow/runners/ec2.py:37`, `agentflow/runners/ecs.py:48`, `agentflow/runners/ec2.py:143`).

## 5. [[wiki/05-merge-and-cli|Merge reducers and CLI surface]]
**In one sentence:** Agentflow combines parallel branches with a reducer (a step that combines many parallel outputs into one) and runs graphs from the command line, using Jinja (a Python template language using {{ }} placeholders) to read branch outputs.
## Key points
- Batch reducers split one fanout into fixed-size groups with `merge(..., size=N)`, while group reducers make one reducer per field value with `merge(..., by=[field])` (`agentflow/dsl.py:272`, `agentflow/dsl.py:329`, `agentflow/dsl.py:331`).
- Reducer prompts loop over branch outputs with Jinja templates like `{% for r in fanouts.review.nodes %}` to build a combined summary (`examples/code_review.py:41`, `agentflow/dsl.py:322`).
- Branches avoid clobbering because each node id gets its own artifact folder and its own workspace folder from `derive` (`agentflow/store.py:55`, `agentflow/context.py:11`, `examples/airflow_like_fuzz_batched.py:76`).
- Users run a graph with `agentflow run pipeline.py --output summary`, where `--output` picks summary or json output (`agentflow/cli.py:2161`, `agentflow/cli.py:2165`, `docs/cli.md:59`).
- Python graphs export to runnable JSON with `to_json`, and the loader runs the Python file and parses its printed JSON (`agentflow/dsl.py:156`, `agentflow/loader.py:20`).
- Worktree isolation gives each local node its own git worktree folder and branch so file edits do not collide (`agentflow/worktree.py:9`, `agentflow/orchestrator.py:499`, `agentflow/dsl.py:92`).
- Doctor and preflight checks test tools, login, and keys before a run, and `inspect` shows the launch plan without running anything (`agentflow/cli.py:2290`, `agentflow/cli.py:2170`, `agentflow/inspection.py:989`).

## 6. [[wiki/targeted|Targeted: Agentflow graph orchestration vs fleet queue model]]
**In one sentence:** Agentflow is programmatic Python graph orchestration whose DAG (Directed Acyclic Graph, a workflow with no loops) paradigm contrasts with fleet's queue model, and fleet can borrow fanout/reduce parallelism, cycle-until-LGTM loops, and pluggable remote-execution targets.
## Key points
- Borrow fanout (splitting one task into many parallel copies) plus merge reducers for map-reduce over beads tasks.
- Borrow cycle-until-LGTM (LGTM means Looks Good To Me, a human approval signal) loops: a review node with a success rule plus an on_failure back-edge to the worker.
- Borrow batch versus group reducers: one reducer per N-item batch, or one reducer per field combination.
- Borrow per-branch workspaces from fanout derive maps so parallel workers do not clobber shared files.
- Borrow node templating (`{{ nodes.x.output }}`, `{{ item.scope }}`, `{{ fanouts.name.nodes }}`) so later steps can read earlier outputs.
- Borrow success_criteria as pass/fail gates (`output_contains`, `file_exists`, `file_contains`, `file_nonempty`) instead of exit-code-only checks.
- Borrow pluggable runners per step (local, container, SSH, EC2, ECS) with shared cloud machines for sequential steps.

## The system in five moves
1. Plan writes the task plan.
2. Fanout splits the plan into parallel workers.
3. Merge combines worker outputs into a draft.
4. Review cycles the draft until LGTM.
5. Synthesis writes the final output.
