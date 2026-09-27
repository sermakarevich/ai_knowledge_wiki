> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Orchestration engine: scheduling, cycles, and restarts
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
---
## How scheduling works
The main loop in `run()` keeps two sets: `remaining` nodes and `in_progress` tasks. Each pass it skips blocked nodes, collects ready nodes, and launches them as background tasks (`agentflow/orchestrator.py:811`).
Ready means all dependencies are completed. Cycle members are the exception: they may proceed when dependencies are completed or failed, so a back-edge can loop (`agentflow/orchestrator.py:867`):
```
                # Cycle nodes can proceed when deps are COMPLETED or FAILED
                if node_id in cycle_nodes or node.on_failure_restart:
                    terminal = {NodeStatus.COMPLETED, NodeStatus.FAILED}
                    if not all(record.nodes[dep].status in terminal for dep in node.depends_on):
                        continue
                elif not all(record.nodes[dep].status == NodeStatus.COMPLETED for dep in node.depends_on):
                    continue
```
Launches are queued as async tasks and collected as they finish (`agentflow/orchestrator.py:879`):
```
            for node_id in ready:
                if node_id not in in_progress:
                    remaining.remove(node_id)
                    record.nodes[node_id].status = NodeStatus.QUEUED
                    in_progress[node_id] = asyncio.create_task(launch(node_id))
```
## Concurrency limit
Concurrency (how many things run at the same time) uses an asyncio semaphore (a counter that blocks extra work until a slot frees). One semaphore is built per run from the pipeline setting (`agentflow/orchestrator.py:783`):
```
        semaphore = asyncio.Semaphore(pipeline.concurrency)
```
Every node launch enters that semaphore, so no more than `pipeline.concurrency` nodes execute at once. Periodic nodes reuse the same path but add a tick number first (`agentflow/orchestrator.py:791`):
```
        async def launch(node_id: str) -> _NodeExecutionOutcome:
            async with semaphore:
                node = node_map[node_id]
```
A second, outer limit caps whole runs: the orchestrator holds a thread semaphore sized by `max_concurrent_runs`, and each submitted run waits for a slot before its loop starts (`agentflow/orchestrator.py:87`).
## Success checks
After a worker finishes, the orchestrator calls one function to judge the result (`agentflow/orchestrator.py:627`):
```
            success_ok, success_details = evaluate_success(node, result, paths.host_workdir)
```
That function has four rule kinds, and all of them must pass (`agentflow/success.py:34`):
```
        if isinstance(criterion, OutputContainsCriterion):
            haystack = output if criterion.case_sensitive else output.lower()
            needle = criterion.value if criterion.case_sensitive else criterion.value.lower()
            ok = needle in haystack
            messages.append(f"output_contains({criterion.value!r})={ok}")
```
The other kinds check the work folder: `file_exists` tests presence (`agentflow/success.py:48`), `file_contains` reads the file and searches for a string (`agentflow/success.py:51`), and `file_nonempty` requires non-blank content (`agentflow/success.py:58`). With no rules configured, the node passes with `no success criteria configured` (`agentflow/success.py:36`).
## Retries, cycles, and restarts
Per-node retries are a simple for-loop over attempts. `retries=2` means up to three tries (`agentflow/orchestrator.py:540`):
```
        for attempt_number in range(1, node.retries + 2):
```
Between attempts the worker sleeps longer each time (backoff = waiting longer after each failure) (`agentflow/orchestrator.py:700`):
```
            if attempt_number <= node.retries:
                await asyncio.sleep(max(node.retry_backoff_seconds, 0.0) * attempt_number)
                continue
```
Graph cycles use `on_failure_restart` edges. When the tail node fails, the scheduler counts the iteration and re-queues the failed node, its restart targets, and nodes between them (`agentflow/orchestrator.py:954`):
```
                    if (
                        record.nodes[node_id].status == NodeStatus.FAILED
                        and node.on_failure_restart
                        and not self._should_cancel(run_id)
                    ):
                        iteration_key = (run_id, node_id)
                        iteration_counts[iteration_key] = iteration_counts.get(iteration_key, 0) + 1
                        if iteration_counts[iteration_key] < pipeline.max_iterations:
                            await self._publish(
                                run_id, "node_cycle_restart",
                                node_id=node_id,
                                iteration=iteration_counts[iteration_key],
                                restart_targets=node.on_failure_restart,
                            )
```
Reset means status back to pending with output cleared (`agentflow/orchestrator.py:112`):
```
    @staticmethod
    def _reset_node_for_cycle(record: "RunRecord", node_id: str, remaining: set[str]) -> None:
        """Reset a node to PENDING so it can be re-executed in a cycle."""
        node_result = record.nodes.get(node_id)
        if node_result is None:
            return
        node_result.status = NodeStatus.PENDING
        node_result.finished_at = None
        node_result.output = None
        node_result.exit_code = None
        node_result.success = None
        node_result.success_details = []
        remaining.add(node_id)
```
A separate path handles controller-requested reruns: a periodic node can ask for cancel or rerun of watched fanout members (fanout = splitting one task into many parallel copies), and finished targets go back to pending with a `node_rerun_queued` event (`agentflow/orchestrator.py:986`):
```
                    if (
                        node_id in self._pending_node_reruns.setdefault(run_id, set())
                        and record.nodes[node_id].status in _TERMINAL_NODE_STATUSES
                        and not self._should_cancel(run_id)
                    ):
                        self._pending_node_reruns[run_id].discard(node_id)
                        record.nodes[node_id].status = NodeStatus.PENDING
```
## State, traces, and paths
Every state change is persisted (saved to disk) through `RunStore`. The run record goes to `run.json` (`agentflow/store.py:64`):
```
    async def persist_run(self, run_id: str) -> None:
        record = self._runs[run_id]
        run_dir = self.run_dir(run_id)
        lock = self._locks[run_id]
        with lock:
            (run_dir / "run.json").write_text(record.model_dump_json(indent=2), encoding="utf-8")
```
Events such as `node_started`, `node_completed`, and `node_cycle_restart` are appended to `events.jsonl` and fanned out to subscribers (`agentflow/store.py:71`). Node output and result files are written after execution (`agentflow/orchestrator.py:705`):
```
        await self.store.write_artifact_text(run_id, node_id, "output.txt", result.output or "")
        await self.store.write_artifact_json(run_id, node_id, "result.json", result.model_dump(mode="json"))
```
Trace lines from workers are normalized per agent type so the UI sees one event shape. The factory picks the parser by agent (`agentflow/traces.py:268`):
```
def create_trace_parser(agent: AgentKind, node_id: str) -> BaseTraceParser:
    match agent:
        case AgentKind.CODEX:
            return CodexTraceParser(node_id=node_id, agent=agent)
        case AgentKind.CLAUDE:
            return ClaudeTraceParser(node_id=node_id, agent=agent)
        case AgentKind.KIMI:
            return KimiTraceParser(node_id=node_id, agent=agent)
    return GenericTraceParser(node_id=node_id, agent=agent)
```
File locations for each node come from `build_execution_paths`, which separates the host work folder from the per-node runtime folder (`agentflow/prepared.py:48`):
```
    resolved_base_dir = base_dir.expanduser().resolve()
    host_runtime_dir = resolved_base_dir / run_id / "runtime" / node_id
    if create_runtime_dir:
        host_runtime_dir = ensure_dir(host_runtime_dir)
```
## Data flow
```
plan ─ ► fanout ─ ► merge ─ ► review ─ ► synthesis
 │         │          │          │             │
 │         ▼          ▼          ▼             ▼
 │      worker-A   merged     LGTM?         final
 │      worker-B    draft     check          output
 │         │          │          │
 └─────────┴──────────┴──── pass? ─ ► retry loop
                                  ─ ► on_failure restart
```
In words: the plan node fans out into parallel workers, their outputs merge into one draft, a review node checks success rules such as `output_contains LGTM`, and synthesis writes the final answer. A failed review retries the node with backoff, and a failed tail node with an `on_failure_restart` edge resets its targets for another cycle until `max_iterations` is hit.
**Covers:** agentflow/orchestrator.py, agentflow/success.py, agentflow/store.py, agentflow/traces.py, agentflow/prepared.py
