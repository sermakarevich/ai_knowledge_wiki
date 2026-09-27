# Technical Analysis: agentflow
**Repository:** https://github.com/abt0y/agentflow
**Version analyzed:** 0.1.0 (commit 1afc32ce70a4bbbe3058d51a9743b8b13302478c, 2026-03-31, branch master)
**Date:** 2026-09-09

## 1. Overview / What Problem It Solves
Agentflow runs teams of AI coding agents as a Python pipeline. You write a graph of steps, it runs them in order, in parallel, with retries (01-graph-dsl.md:3).
Problem: one agent call is not enough. Real work needs plan, then many workers, then merge, then review, then fix loops. Doing that by hand needs grouping and retry logic (targeted.md:18, targeted.md:20).
Solution: a Graph builder with edges (`>>`), parallel copies (`fanout()`), reducers (`merge()`), and failure loops (`on_failure`) (01-graph-dsl.md:5-11). An orchestrator runs nodes in dependency order, limits parallel work, checks success rules, and restarts failed work (02-orchestration-engine.md:3).
Each step can run locally or on cloud machines: local process, Docker container, SSH (SSH = Secure Shell, remote login protocol), EC2 (EC2 = Elastic Compute Cloud, rentable virtual machines on AWS), ECS (ECS = Elastic Container Service, running Docker containers on AWS) (04-remote-execution.md:3).

## 2. High-Level Architecture
```
pipeline.py (Graph DSL) ─ ► PipelineSpec ─ ► Orchestrator ─ ► Runner ─ ► Agent CLI
       │                          │                 │                │             │
       │                          ▼                 ▼                ▼             ▼
       │                   run.json + events.jsonl  semaphore   local/ssh/   codex/claude/
       │                   artifacts/output.txt                             kimi
       │                          │                 │
       └──────────────────────────┴── Jinja render ┴── success_criteria ─ ► merge/review
```
Jinja = a text template system with `{{ ... }}` placeholders. CLI = Command-Line Interface, a program you run in a terminal (03-agent-harness.md:3).
Data flow in 5 steps:
1. Define: `with Graph(...):` makes the graph active and node helpers register into it (`agentflow/dsl.py:114` per 01-graph-dsl.md:5). `DAG = Graph` is kept for old code (`agentflow/dsl.py:194` per 01-graph-dsl.md:14).
2. Render: prompts are plain strings with placeholders such as `{{ nodes.plan.output }}` and render before launch via a shared helper (`agentflow/context.py:231` per 03-agent-harness.md:9, `agentflow/context.py:212` per targeted.md:73).
3. Schedule: a node becomes ready only when every node in `depends_on` is completed, so execution is in topological order (`agentflow/orchestrator.py:871` per 02-orchestration-engine.md:5). Launches are async tasks queued per pass (`agentflow/orchestrator.py:879` per 02-orchestration-engine.md:11).
4. Execute: concurrency is bounded by one semaphore from `pipeline.concurrency` (`agentflow/orchestrator.py:783` per 02-orchestration-engine.md:7). Each node picks a runner with `target={"kind": ...}` for `local`, `container`, `ssh`, `ec2`, `ecs` (`agentflow/runners/registry.py:13` per 04-remote-execution.md:6).
5. Judge and loop: success rules decide pass or fail (`agentflow/success.py:43` per 02-orchestration-engine.md:9). Failed tail nodes with `on_failure_restart` reset targets back to pending until `max_iterations` (`agentflow/orchestrator.py:954`, `agentflow/orchestrator.py:961` per 02-orchestration-engine.md:8-10).
Persistent state: run record goes to `run.json` (`agentflow/store.py:64` per 02-orchestration-engine.md:12). Events such as `node_started`, `node_completed`, `node_cycle_restart` append to `events.jsonl` (`agentflow/store.py:71` per 02-orchestration-engine.md:12). Per-node `output.txt` and `result.json` are saved as artifacts (`agentflow/orchestrator.py:705` per 02-orchestration-engine.md:12). Each node id gets its own artifact folder (`agentflow/store.py:55` per 05-merge-and-cli.md:8).

## 3. The Graph DSL
Core abstraction: `Graph` is a Python context manager that builds a DAG (DAG = Directed Acyclic Graph, a workflow with no loops). DSL = Domain-Specific Language, a mini-language for one job (01-graph-dsl.md:14).
Representation: constructor holds `name`, `working_dir`, `concurrency`, `fail_fast`, `max_iterations`, `scratchboard`, `use_worktree`, node/agent/target defaults (`agentflow/dsl.py:88` per 01-graph-dsl.md:11, `agentflow/dsl.py:81` per targeted.md:69). Exported spec is `PipelineSpec` with `name`, `concurrency`, `max_iterations`, node list (`agentflow/specs.py:1379` per 01-graph-dsl.md:168). Nodes carry `prompt`, `depends_on`, `on_failure_restart`, `success_criteria` in `NodeSpec` (`agentflow/specs.py:716` per 01-graph-dsl.md:168). Graphs export to runnable JSON (JSON = JavaScript Object Notation, a text data format) with `to_json` (`agentflow/dsl.py:156` per 05-merge-and-cli.md:10).
Node kinds: `codex`, `claude`, `kimi` forward to one shared builder (`agentflow/dsl.py:350`, `agentflow/dsl.py:354`, `agentflow/dsl.py:358` per 03-agent-harness.md:6). `python_node`, `shell`, `sync` are also re-exported at package root (`agentflow/__init__.py:3` per 01-graph-dsl.md:76).
Edge kinds: `a >> b` makes `b` depend on `a`; `plan >> [implement, review]` fans to two nodes; `[a, b] >> merge` joins them (`agentflow/dsl.py:48`, `agentflow/dsl.py:56` per 01-graph-dsl.md:6, 01-graph-dsl.md:76). `review.on_failure >> write` restarts `write` when `review` fails (`agentflow/dsl.py:72` per 01-graph-dsl.md:10). The proxy appends target ids to `on_failure_restart` (`agentflow/dsl.py:24` per 01-graph-dsl.md:171).
Key traversal (verbatim, `examples/iterative_impl.py:38-40` per targeted.md:43):
```python
    write >> review
    review.on_failure >> write  # loop until LGTM
    review >> summary           # proceed to summary on success
```
LGTM = Looks Good To Me, a human approval signal (02-orchestration-engine.md:9).
Knobs: `concurrency` for parallel workers, `max_iterations` for loop limit, validated as `concurrency >= 1` and `max_iterations >= 1` (`agentflow/dsl.py:88`, `agentflow/specs.py:1385` per 01-graph-dsl.md:11). `fanout()` source modes: `int` count, `list` values, `dict` matrix (`agentflow/dsl.py:247` per 01-graph-dsl.md:7). `merge()` needs exactly one of `by=[...]` or `size=N` (`agentflow/dsl.py:325` per 01-graph-dsl.md:8).

## 4. LLM / External Service Integration
The repo shells out to CLIs, it does not call model APIs directly. Three harnesses (harness = wrapper that launches an AI agent) build command lines (03-agent-harness.md:3):
- Codex: `CodexAdapter.prepare()` picks sandbox `read-only` vs `workspace-write` from `tools=` (`agentflow/agents/codex.py:31`, `agentflow/agents/codex.py:70` per 03-agent-harness.md:7).
- Claude: `ClaudeAdapter.prepare()` builds streaming JSON call with permission bypass (`agentflow/agents/claude.py:37`, `agentflow/agents/claude.py:52` per 03-agent-harness.md:8). `tools=` switches read-only list vs read-write list adding `Write`, `Edit`, `Bash` (`agentflow/agents/claude.py:13`, `agentflow/agents/claude.py:26`, `agentflow/agents/claude.py:52` per 03-agent-harness.md:8).
- Kimi: `KimiAdapter.prepare()` builds print-mode streaming call with auto-approve (`agentflow/agents/kimi.py:14`, `agentflow/agents/kimi.py:16` per 03-agent-harness.md:11).
Providers: each adapter reads `node.provider` via `provider_config(node.provider, node.agent)` (03-agent-harness.md:29, 03-agent-harness.md:60, 03-agent-harness.md:88). Wiki does not list provider names or endpoints.
Required vs optional per wiki: agent CLIs must exist (`node.executable or "codex" / "claude" / "kimi"` per 03-agent-harness.md:30, 03-agent-harness.md:61, 03-agent-harness.md:89). Local agent logins such as `~/.codex/auth.json` or `~/.claude/.credentials.json` are needed so keys can be forwarded to remote machines (`agentflow/cloud/aws.py:126`, `agentflow/cloud/aws.py:154` per 04-remote-execution.md:75). AWS (AWS = Amazon Web Services, the cloud provider) credentials plus `boto3` are required for EC2/ECS; Docker is required for ECS image builds (04-remote-execution.md:13, 04-remote-execution.md:75).
Env vars in wiki: only runner/CLI vars `AGENTFLOW_RUNS_DIR`, `AGENTFLOW_MAX_CONCURRENT_RUNS` (05-merge-and-cli.md:109-112); no model API-key names are listed.
Cost points: wiki lists no prices or token accounting. Cost drivers visible in wiki are parallel copy count (e.g. 128 shards per 01-graph-dsl.md:111), `timeout_seconds` (e.g. 3600 per 01-graph-dsl.md:87), per-node `retries=2` (01-graph-dsl.md:88), and EC2 per-node machines vs shared machines (`agentflow/runners/ec2.py:25` vs `agentflow/runners/ec2.py:234` per 04-remote-execution.md:8-9).

## 5. The Fanout-Merge-Review Pipeline
Main pipeline: plan ─ ► fanout ─ ► merge ─ ► review ─ ► synthesis (02-orchestration-engine.md:150-159).
1. `fanout(node, source)` expands one node into many copies (`agentflow/dsl.py:247` per 01-graph-dsl.md:7). Each copy gets `item` with `index`, `number`, `count`, `suffix`, `node_id`, `value` (`agentflow/dsl.py:229` per 01-graph-dsl.md:79). Example: `int` mode with `128` makes `fuzzer_000` to `fuzzer_127` (`tests/test_dsl.py:392` per 01-graph-dsl.md:111).
2. `merge(node, source, by=|size=)` reduces the group (`agentflow/dsl.py:325` per 01-graph-dsl.md:8). It auto-adds dependency on the source group (`agentflow/dsl.py:340` per 01-graph-dsl.md:114). Batch mode `size=16` turns 128 shards into 8 reducers; group mode `by=["target","corpus"]` groups by field values (`tests/test_dsl.py:340` per 01-graph-dsl.md:142).
3. Reducer sees only its members through `item.scope` plus `member_ids`, `source_group`, `source_count` (`agentflow/dsl.py:307` per 01-graph-dsl.md:142). Full-group reads use `fanouts.<name>.nodes`, e.g. `{% for r in fanouts.review.nodes %}` (`examples/code_review.py:41` per 05-merge-and-cli.md:6).
4. Orchestrator `run()` loops over `remaining` and `in_progress`, skips blocked nodes, launches ready ones (`agentflow/orchestrator.py:811` per 02-orchestration-engine.md:15). Ready means all `depends_on` completed, except cycle members which allow completed or failed (`agentflow/orchestrator.py:867` per 02-orchestration-engine.md:16).
5. `evaluate_success(node, result, ...)` judges each result (`agentflow/orchestrator.py:627` per 02-orchestration-engine.md:47). Four rule kinds, all must pass: `output_contains`, `file_exists`, `file_contains`, `file_nonempty` (`agentflow/success.py:34` per 02-orchestration-engine.md:51, `agentflow/success.py:43` per targeted.md:26). Classic gate: review passes only when output contains LGTM (`examples/iterative_impl.py:19-28` per targeted.md:41).
6. On tail failure with `on_failure_restart`, scheduler counts the iteration and re-queues failed node plus restart targets and nodes between them (`agentflow/orchestrator.py:954` per 02-orchestration-engine.md:71). Reset sets status to pending and clears output (`agentflow/orchestrator.py:112` per 02-orchestration-engine.md:88). Cap is `pipeline.max_iterations`, else emits `node_cycle_exhausted` (`agentflow/orchestrator.py:961` per 02-orchestration-engine.md:8). Upstream failures without a failure path mark downstream skipped with `upstream_failure` (`agentflow/orchestrator.py:834` per 02-orchestration-engine.md:6).

## 6. Key Files
| File | Lines | What It Does |
|------|-------|--------------|
| agentflow/local_shell.py | 2636 | Shell-command helpers; local runner imports only 3 helpers from it (`agentflow/runners/local.py:9`, `agentflow/local_shell.py:131,138,2118` per 04-remote-execution.md:18) |
| agentflow/cli.py | 2327 | `run`, `inspect`, doctor commands; `run` output-format options (`agentflow/cli.py:2161,2165,2170,2290` per 05-merge-and-cli.md:9, 05-merge-and-cli.md:12) |
| agentflow/doctor.py | 2233 | Doctor and preflight checks for tools, login, keys before a run (per 05-merge-and-cli.md:12) |
| agentflow/specs.py | 1529 | Validated specs: `FanoutSpec`, `NodeSpec`, `PipelineSpec`; validates `concurrency >= 1` (`agentflow/specs.py:557,716,1379,1385` per 01-graph-dsl.md:111, 01-graph-dsl.md:168, 01-graph-dsl.md:11) |
| agentflow/inspection.py | 1334 | `inspect` launch plan without running (`agentflow/inspection.py:989` per 05-merge-and-cli.md:12) |
| agentflow/orchestrator.py | 1015 | Scheduling loop, semaphore, retries, cycle restarts, artifact writes (`agentflow/orchestrator.py:540,627,705,783,811,954,986` per 02-orchestration-engine.md) |
| agentflow/defaults.py | 387 | Default settings store (cited as merge/CLI coverage per 05-merge-and-cli.md:167) |
| agentflow/runners/ecs.py | 382 | ECS Fargate runner: cluster/log/role setup, image build, task poll (`agentflow/runners/ecs.py:74,86,95,133,199,234` per 04-remote-execution.md:11, 04-remote-execution.md:48-52) |
| agentflow/dsl.py | 379 | `Graph`, `>>` edges, `fanout()`, `merge()`, `codex/claude/kimi` constructors (`agentflow/dsl.py:48,72,114,247,325,350` per 01-graph-dsl.md, 03-agent-harness.md) |
| agentflow/runners/local.py | 338 | Local runner: spawns prepared command as child process (`agentflow/runners/local.py:270,271,278` per 04-remote-execution.md:12, 04-remote-execution.md:67) |
| agentflow/runners/ec2.py | 277 | EC2 runner: per-node or shared machines, UserData, spot, SSH delegate (`agentflow/runners/ec2.py:25,39,76,153,234,250` per 04-remote-execution.md:8-9, 04-remote-execution.md:26-27) |
| agentflow/traces.py | 276 | Per-agent trace parser factory for codex/claude/kimi (`agentflow/traces.py:268` per 02-orchestration-engine.md:129) |
| agentflow/context.py | 235 | Jinja render context, per-node dicts, `item.scope` view (`agentflow/context.py:157,190,212,231` per 03-agent-harness.md:9-11) |
| agentflow/app.py | 194 | App wiring (web/service entry; structural, no wiki line — listed for size context) |
| agentflow/cloud/aws.py | 175 | EC2/ECS auto-discovery: AMI, key, VPC subnets, security group (`agentflow/cloud/aws.py:11,27,54,67,85` per 04-remote-execution.md:10, 04-remote-execution.md:73) |
| agentflow/runners/ssh.py | 142 | SSH runner via system `ssh` binary, `BatchMode=yes`, timeout/cancel codes (`agentflow/runners/ssh.py:23,34,109,135` per 04-remote-execution.md:7, 04-remote-execution.md:23) |

## 7. Dependencies
| Package | Constraint | Notes per wiki |
|---------|------------|----------------|
| boto3 | >=1.35.0 | AWS calls for EC2/ECS; still required even with auto-discovery (`agentflow/cloud/aws.py:22` per 04-remote-execution.md:13) |
| fastapi | >=0.116.0 | Manifest entry (no wiki behavior line) |
| httpx | >=0.28.1 | Manifest entry (no wiki behavior line) |
| jinja2 | >=3.1.6 | Prompt templating `{{ nodes.x.output }}`, loops, conditions (01-graph-dsl.md:9, 01-graph-dsl.md:145-166) |
| pydantic | >=2.11.0 | Spec/store models e.g. `record.model_dump_json` (`agentflow/store.py:64` per 02-orchestration-engine.md:115) |
| typer | >=0.16.0 | CLI options e.g. `typer.Option` for runs dir, output format (`agentflow/cli.py` per 05-merge-and-cli.md:108-118) |
| uvicorn | >=0.35.0 | Manifest entry (no wiki behavior line) |
Entry point: `pyproject.toml` scripts `agentflow=agentflow.cli:app`. Requires Python (the programming language): `>=3.11`.

## 8. CLI / Usage Surface
Entry points: `agentflow run`, `agentflow inspect`, doctor checks (05-merge-and-cli.md:9, 05-merge-and-cli.md:12).
```bash
agentflow run pipeline.py --output summary
agentflow run examples/pipeline.yaml
```
`--output` picks summary or json output (`agentflow/cli.py:2161`, `agentflow/cli.py:2165` per 05-merge-and-cli.md:9). On a terminal default is compact summary; when redirected default is JSON; `--output` forces a format (`docs/cli.md:59` per 05-merge-and-cli.md:9, 05-merge-and-cli.md:126-130). Python graphs export with `to_json` and the loader runs the Python file and parses printed JSON (`agentflow/dsl.py:156`, `agentflow/loader.py:20` per 05-merge-and-cli.md:10).
| Env var | Default | Purpose |
|---------|---------|---------|
| AGENTFLOW_RUNS_DIR | .agentflow/runs | Where run folders go (`agentflow/cli.py` per 05-merge-and-cli.md:108-112) |
| AGENTFLOW_MAX_CONCURRENT_RUNS | 2 | Outer cap on whole runs; orchestrator holds a thread semaphore of this size (`agentflow/orchestrator.py:87` per 02-orchestration-engine.md:45, 05-merge-and-cli.md:108-112) |
Config files: pipeline files are Python (`pipeline.py`) or YAML (YAML = YAML Ain't Markup Language, a text config format) (`agentflow run examples/pipeline.yaml` per 05-merge-and-cli.md:122). No extra config-file path is named in wiki beyond pipeline path plus runs dir.
Safety nets: worktree isolation gives each local node its own git worktree folder and branch (`agentflow/worktree.py:9`, `agentflow/orchestrator.py:499`, `agentflow/dsl.py:92` per 05-merge-and-cli.md:11). Doctor/preflight test tools, login, keys; `inspect` shows launch plan without running (`agentflow/cli.py:2290`, `agentflow/cli.py:2170`, `agentflow/inspection.py:989` per 05-merge-and-cli.md:12).

## 9. Extensibility Points
- New harness: add an `AgentAdapter` subclass with `prepare()` like `CodexAdapter` / `ClaudeAdapter` / `KimiAdapter` (`agentflow/agents/codex.py:67`, `agentflow/agents/claude.py:37`, `agentflow/agents/kimi.py:14` per 03-agent-harness.md), then map it in the registry which maps each agent kind to its class and allows replace via `register()` (`agentflow/agents/registry.py:13`, `agentflow/agents/registry.py:22` per 03-agent-harness.md:10). Add a `codex()`-style constructor forwarding to `_node()` (`agentflow/dsl.py:350` per 03-agent-harness.md:17-22).
- New runner: add a runner class (see `agentflow/runners/local.py:278`, `agentflow/runners/ssh.py:44`, `agentflow/runners/ec2.py:39`, `agentflow/runners/ecs.py:74` per 04-remote-execution.md) and register `local|container|ssh|ec2|ecs`-style kind in the runner registry (`agentflow/runners/registry.py:13` per 04-remote-execution.md:6). Container pattern is subclass of local runner (`agentflow/runners/container.py:11` per 04-remote-execution.md:12).
- New reducer: no separate reducer class in wiki; reuse `merge(node, source, by=|size=)` modes (`agentflow/dsl.py:272`, `agentflow/dsl.py:329`, `agentflow/dsl.py:331` per 05-merge-and-cli.md:6). Custom grouping = new `by` fields; custom batching = new `size`; scoped reads come from `item.scope` (`agentflow/dsl.py:307` per targeted.md:67).

## 10. Limitations and Gotchas
- `local_shell.py` is very large (2636 lines) while the local runner imports only 3 helpers from it (`agentflow/runners/local.py:9`, `agentflow/local_shell.py:131,138,2118` per 04-remote-execution.md:18). Big file, small use = hard to review and easy to break.
- Zero-config remote is partial. You can omit AMI (AMI = Amazon Machine Image, a template for a virtual machine), key, subnets, cluster, but you still need AWS credentials, boto3, a default VPC (VPC = Virtual Private Cloud, your private network section in AWS), Docker for ECS builds, and agent login keys forwarded from your machine (`agentflow/cloud/aws.py:22`, `agentflow/runners/ec2.py:37`, `agentflow/runners/ecs.py:48`, `agentflow/runners/ec2.py:143` per 04-remote-execution.md:13).
- CLI surface is very large (`cli.py` 2327 lines, `doctor.py` 2233 lines, `inspection.py` 1334 lines). `run` alone mixes path loading, runs-dir, concurrency, output-format controls (`agentflow/cli.py` per 05-merge-and-cli.md:108-118). Expect many flags to learn.
- Origin naming: template notes a duplicate `shouc/agentflow` vs `abt0y/agentflow` origin naming gotcha. Wiki pages read for this summary do not give a file:line for it, so verify in git remotes before citing or scripting.
- Shared files need care: parallel branches are isolated by workspace and artifact folders, but shared notes are append-only by prompt contract with locking, not by the engine (`examples/airflow_like_fuzz_batched.py:76`, `agentflow/store.py:55` per targeted.md:62-65). A bad prompt can still cause clobbering (overwriting each other's files).

## 11. How It Compares to Alternatives
- LangGraph: LangGraph is also graph-based agent orchestration, but Agentflow shells out to existing Codex/Claude/Kimi CLIs instead of wiring model calls in Python.
- Apache Airflow: Airflow schedules static data tasks with workers; Agentflow copies that shape (`examples/airflow_like.py:13` per 01-graph-dsl.md:9) but prompts and outputs are Jinja-linked AI steps with LGTM loops.
- Claude Squad / tmux orchestration: tmux (tmux = terminal multiplexer, a tool that splits one terminal into many sessions) tools run parallel terminal agents; Agentflow replaces manual session juggling with `fanout()` copies plus per-branch workspaces and merge reducers.
- Fleet queue model: fleet queues YAML workflows and beads tasks picked by workers with no single DAG object, while Agentflow owns the whole run as Python code with explicit fanout/merge points (targeted.md:16, targeted.md:20); the 94-node shape is five lines of wiring in Agentflow vs 94 task rows plus manual grouping in a queue model (targeted.md:18).

## Appendix
A. Codex harness command (`agentflow/agents/codex.py:67` per 03-agent-harness.md:25):
```python
    def prepare(self, node: NodeSpec, prompt: str, paths: ExecutionPaths) -> PreparedExecution:
        provider = self.provider_config(node.provider, node.agent)
        executable = node.executable or "codex"
        sandbox = "read-only" if node.tools == ToolAccess.READ_ONLY else "workspace-write"
        command = [
            executable,
            "exec",
            "--json",
            "--skip-git-repo-check",
```
B. Merge mode switch (`agentflow/dsl.py` per 05-merge-and-cli.md:29-34):
```python
    if by is not None:
        mode: dict[str, Any] = {"group_by": {"from": source.id, "fields": list(by)}}
    elif size is not None:
        mode = {"batches": {"from": source.id, "size": size}}
```
C. Cycle restart emit (`agentflow/orchestrator.py:954` per 02-orchestration-engine.md:71):
```python
                    if (
                        record.nodes[node_id].status == NodeStatus.FAILED
                        and node.on_failure_restart
                        and not self._should_cancel(run_id)
                    ):
                        iteration_key = (run_id, node_id)
                        iteration_counts[iteration_key] = iteration_counts.get(iteration_key, 0) + 1
```
