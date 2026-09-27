> [[index|Wiki]] | [[summary|Summary]]
# Critical Analysis: Agentflow
## Claims vs. evidence
- 94-node scale (1 plan + 64 workers + 8 batch merges + 16 reviews + 4 review merges + 1 synthesis): suggestive.
- The sources show the arithmetic and the five wiring steps (`>>` from plan to workers, `merge(size=8)` for batches,
- a second `fanout()` for reviewers, `merge(by=[...])` for grouped reviews, final `>>` to synthesis).
- What is missing: no run logs, wall-clock time, per-node LLM (Large Language Model, the AI engine) spend, or failure-rate data for a real 94-way run.
- The closest concrete shapes are smaller: a 128-shard fuzz example (`fuzzer_000` to `fuzzer_127`) and 8 batch reducers from `size=16`.
- Zero-config remote (EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) / ECS (Elastic Container Service, running containers on AWS)
- auto-discovery of AMI (Amazon Machine Image, a virtual-machine template), key pair, VPC (Virtual Private Cloud, private network section in AWS)): weak as "zero-config", strong as "fewer fields".
- The same source lists what you still need: AWS (Amazon Web Services, the cloud provider) credentials, boto3 (Python library for AWS),
- a default VPC with port 22 open, Docker for ECS image builds, and local agent logins forwarded to the remote box.
- EC2 discovery picks newest Ubuntu 24.04 AMI, creates an `agentflow` SSH (Secure Shell, remote login protocol) key under `~/.agentflow/keys/`,
- and reuses one security group; ECS reuses the same VPC discovery when subnets are empty.
- Iterative LGTM (Looks Good To Me, a human approval signal) loops (`success_criteria=[output_contains: LGTM]`
- + `review.on_failure >> write` + `max_iterations` cap): strong on mechanism, weak on effectiveness.
- The path is fully traced: DSL (Domain-Specific Language, a mini-language for one job) proxy appends restart targets,
- `evaluate_success` in `success.py` judges output, the orchestrator resets node plus targets to pending and counts iterations,
- emitting `node_cycle_restart` or terminal `node_cycle_exhausted`.
- Missing: convergence data, false-LGTM rate for a substring gate, and cost per extra iteration.
- Small-repo signals temper all three claims: version 0.1.0, single-maintainer smell,
- README (readme file, the project's front-page docs)-driven claims with worked examples rather than measured results.
## Genuinely new vs. repackaged
- Vs Airflow (a DAG (Directed Acyclic Graph, a workflow with no loops) scheduler for data pipelines): Agentflow borrows the DAG plus fanout idea
- but targets short-lived agent runs, not scheduled data tables. The `airflow_like.py` example is naming, not parity.
- Vs LangGraph (a Python library for agent workflows as graphs): the graph, conditional edges, and retry loops overlap heavily.
- Agentflow's distinct bit is batch/group reducers with `item.scope` views (member ids, statuses, outputs, `with_output` subset)
- plus per-node cloud targets (`local`, `container`, `ssh`, `ec2`, `ecs`) in one small package.
- Vs Claude Squad (multi-agent coding setups): multi-harness mixing (`codex`, `claude`, `kimi` nodes sharing one `NodeBuilder`,
- e.g. plan with Codex, implement with Claude, review with Kimi, wired by `{{ nodes.<id>.output }}`) is convenient packaging, not a new coordination theory.
- Net: a useful combination (Python graph + map-reduce fanout/merge + LGTM gates + pluggable runners), not a new primitive.
## Weaknesses and blind spots
- Code health: `local_shell.py` at 2636 lines is a god file (one oversized file doing too much),
- `cli.py` at 2327 lines is a second one. The local runner imports only three small helpers (render `shell_init`,
- check `{command}` placeholder, detect interactive bash), leaving most of that surface as unreviewed risk for adopters.
- Failure-mode gaps: shared files (crash registry, shared notes) rely on prompt-contract locking, not engine locking.
- A failed dependency without an `on_failure` path just marks downstream `skipped (upstream_failure)`,
- which can silently drop branches in a wide fanout. Controller-requested reruns add a second reset path worth auditing.
- Cost and scale questions: default EC2 mode launches one fresh virtual machine per node, so a 64-worker fanout means 64 launches
- unless every node sets the same `shared` name with reference-counted cleanup. No source discusses per-shard LLM spend,
- boot and SSH-wait time, log volume (`run.json`, `events.jsonl`, per-node artifacts), or CloudWatch (AWS log storage) polling delays at that width.
- AWS prerequisites sit behind the label: region access, default VPC, `boto3` installed, local Docker for ECS builds,
- agent keys (`~/.codex/auth.json`, Claude credentials) present locally for forwarding, and an `agentflow` security group with SSH open.
## Applicability
- Works when: embarrassingly parallel agent sweeps (fuzz shards, file reviews, multi-target scans)
- where each copy owns its workspace via `derive={"workspace": "agents/agent_{{ item.suffix }}"}` and `target={"cwd": ...}`.
- Works when: merges stay batch-scoped (one reducer per N items, looping `item.scope.with_output.nodes`)
- or grouped by field, with a final synthesis node reading `fanouts.<name>.nodes`.
- Works when: local-first iteration loops (write, review, fix until LGTM) with `max_iterations` as the safety cap,
- per-node artifact folders, and optional git worktree isolation per node id.
- Fails when: reducers need cross-batch reasoning (each reducer sees only its own scope),
- shared mutable state needs real transactions, or the team cannot absorb EC2/ECS setup and per-node LLM cost.
- Fails when: success needs semantic judgment (real correctness, security review) rather than substring match on "LGTM",
- `file_exists`, `file_contains`, or `file_nonempty` checks.
## Relevance to my work
- Trial the fanout plus merge-reducer pattern for agentic sweeps (parallel workers, batch synthesis): it maps directly onto batch code-review and eval harnesses without adopting the whole repo.
- Trial cycle-until-LGTM loops with `success_criteria` gates for code agents: cheap to copy into fleet YAML (YAML, a config file format) as `success_criteria` plus `on_failure: restart` with a `max_iterations` cap.
- Ignore the EC2-per-node remote layer for the Elisity data platform (Elisity's data lake on AWS): default one-machine-per-node plus forwarded agent keys does not fit platform-grade isolation, cost control, or audit needs; container or shared-machine modes only if a concrete need appears.
- Watch the repo (0.1.0, god files, README-driven): revisit only if maintainers split the shell/CLI core, publish real large-fanout run data, and harden shared-state handling.
## What this changes
- It confirms map-reduce over agent outputs (fanout with `derive`, scoped reducers, full-group reads) beats flat parallel task lists for review-and-synthesize workloads.
- It confirms LGTM-gated restart edges are a smaller, clearer primitive than free-form retry logic, provided the gate stays cheap and the iteration cap is explicit.
- It confirms per-step runner choice (local now, container or cloud later) is worth copying, while per-node cloud machines are opt-in rather than default.
- It does not change the build-vs-borrow call: borrow the two patterns, do not adopt the runner fleet yet.
## Verdict
Agentflow's mechanism is well-specified and readable, but its big claims rest on examples rather than measurements.
The god files, prompt-contract locking, and per-node cloud cost make the repo itself too young to adopt.
Fleet-style queue systems can still borrow the merge-reducer and LGTM-loop shapes at low cost.
Strongest reason to stay engaged is that both patterns are directly reusable in near-term agent work, so my verdict is trial.
