> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Merge reducers and CLI surface
**In one sentence:** Agentflow combines parallel branches with a reducer (a step that combines many parallel outputs into one) and runs graphs from the command line, using Jinja (a Python template language using {{ }} placeholders) to read branch outputs.

## Key points
- Batch reducers split one fanout into fixed-size groups with `merge(..., size=N)`, while group reducers make one reducer per field value with `merge(..., by=[field])` (`agentflow/dsl.py:272`, `agentflow/dsl.py:329`, `agentflow/dsl.py:331`).
- Reducer prompts loop over branch outputs with Jinja templates like `{% for r in fanouts.review.nodes %}` to build a combined summary (`examples/code_review.py:41`, `agentflow/dsl.py:322`).
- Branches avoid clobbering because each node id gets its own artifact folder and its own workspace folder from `derive` (`agentflow/store.py:55`, `agentflow/context.py:11`, `examples/airflow_like_fuzz_batched.py:76`).
- Users run a graph with `agentflow run pipeline.py --output summary`, where `--output` picks summary or json output (`agentflow/cli.py:2161`, `agentflow/cli.py:2165`, `docs/cli.md:59`).
- Python graphs export to runnable JSON with `to_json`, and the loader runs the Python file and parses its printed JSON (`agentflow/dsl.py:156`, `agentflow/loader.py:20`).
- Worktree isolation gives each local node its own git worktree folder and branch so file edits do not collide (`agentflow/worktree.py:9`, `agentflow/orchestrator.py:499`, `agentflow/dsl.py:92`).
- Doctor and preflight checks test tools, login, and keys before a run, and `inspect` shows the launch plan without running anything (`agentflow/cli.py:2290`, `agentflow/cli.py:2170`, `agentflow/inspection.py:989`).

---
## Batch versus group reducers
`merge()` needs exactly one mode. Batched mode cuts shards into equal chunks. Grouped mode cuts by field value, such as target family.

```python
def merge(
    node: NodeBuilder,
    source: NodeBuilder,
    *,
    by: list[str] | None = None,
    size: int | None = None,
    derive: dict[str, Any] | None = None,
) -> NodeBuilder:
```

```python
    if by is not None:
        mode: dict[str, Any] = {"group_by": {"from": source.id, "fields": list(by)}}
    elif size is not None:
        mode = {"batches": {"from": source.id, "size": size}}
```

The docs state the same rule in plain words:

```
`merge(node, source_node)` requires exactly one of `by=` or `size=`:

- `by=["field", ...]` -- one reducer per unique field combination
- `size=N` -- one reducer per N-item batch
```

Batched example uses 16 shards per reducer:

```python
        fuzzer,
        size=16,
```

Grouped example uses target and corpus fields:

```python
        fuzzer,
        by=["target", "corpus"],
```

## Scoped reduce loop
A batch or group reducer sees only its own members through `item.scope`. This loop lists only members with output.

```python
                "{% for shard in item.scope.with_output.nodes %}\n"
                "### {{ shard.node_id }} (status: {{ shard.status }})\n"
                "Workspace: {{ shard.workspace }}\n"
                "{{ shard.output or '(no output)' }}\n\n"
                "{% endfor %}"
```

## Full-graph reduce loop
A final node can read the whole fanout group through `fanouts.<name>`. This pattern comes from the simple code review example.

```python
            "{% for r in fanouts.review.nodes %}\n"
            "## {{ r.file }}\n"
            "{{ r.output }}\n\n"
            "{% endfor %}"
```

## Branch isolation
Each parallel copy gets its own workspace folder from `derive`, and its own run folder for logs. That is how branches avoid overwriting each other.

```python
            target={"cwd": "{{ item.workspace }}"},
```

```python
        derive={"workspace": "agents/agent_{{ item.suffix }}"},
```

Each node id gets its own artifact directory:

```python
    def node_artifact_dir(self, run_id: str, node_id: str) -> Path:
        return ensure_dir(self.run_dir(run_id) / "artifacts" / node_id)
```

Artifact paths are built per node id:

```python
def _artifact_paths_context(*, run_id: str, artifacts_base_dir: Path, node_id: str) -> dict[str, Any]:
    artifact_dir = artifacts_base_dir.expanduser().resolve() / run_id / "artifacts" / node_id
```

## Run and inspect commands
The `run` command takes a pipeline path plus output format controls:

```python
def run(
    path: str,
    runs_dir: str = typer.Option(".agentflow/runs", envvar="AGENTFLOW_RUNS_DIR"),
    max_concurrent_runs: int = typer.Option(2, envvar="AGENTFLOW_MAX_CONCURRENT_RUNS"),
    output: RunOutputFormat = typer.Option(
        RunOutputFormat.AUTO,
        "--output",
        help="Result output format. Defaults to `summary` on a terminal and `json` otherwise.",
    ),
```

Common usage from the docs:

```bash
agentflow run examples/pipeline.yaml
```

Output rule from the docs:

```
On a terminal, `run` and `inspect` default to a compact summary. When stdout is redirected, they fall back to JSON-oriented output. You can always force a format with `--output`.
```

## Export and load
A Python graph prints runnable JSON. The loader executes that Python file and reads the printed text.

```python
    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_payload(), indent=indent)
```

```python
def _load_pipeline_from_python(path: Path) -> PipelineSpec:
    resolved = path.resolve()
    result = subprocess.run(
        [sys.executable, str(resolved)],
        capture_output=True,
        text=True,
        cwd=str(resolved.parent),
    )
    if result.returncode != 0:
        raise ValueError(f"pipeline script `{path}` failed:\n{result.stderr.strip()}")
    return load_pipeline_from_text(result.stdout, base_dir=path.parent.resolve())
```

## Worktrees and doctor
Worktree isolation creates one folder and branch per node id:

```python
def create_worktree(repo_dir: Path, node_id: str, run_id: str) -> Path:
    """Create a git worktree for a node. Returns the worktree path."""
    safe_id = node_id.replace("/", "_")
    worktree_dir = repo_dir / ".agentflow" / "worktrees" / run_id / safe_id
    worktree_dir.parent.mkdir(parents=True, exist_ok=True)

    branch_name = f"agentflow/{run_id[:8]}/{safe_id}"
```

**Covers:** merge paths in agentflow/dsl.py, examples/airflow_like_fuzz_*.py, examples/code_review.py, agentflow/cli.py, agentflow/loader.py, agentflow/defaults.py, agentflow/inspection.py, agentflow/worktree.py, docs/cli.md, docs/pipelines.md
