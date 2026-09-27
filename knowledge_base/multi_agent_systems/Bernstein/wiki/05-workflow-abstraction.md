> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Workflow Abstraction: Task Graphs, Roles, and Artifact Contracts
**In one sentence:** Bernstein runs work as a task graph (a set of tasks linked by dependencies) where phases limit which roles can act, edges control order, and each phase or file deliverable must match a written contract before the run moves on.
## Key points
- Bernstein has two workflow formats: a YAML manifest (YAML = a human-readable config file format) with `nodes` as a list, and a DSL (DSL = Domain-Specific Language, a small config language for one job) with `phases` plus `nodes` as a mapping; the CLI tells them apart by structure (`src/bernstein/cli/commands/workflow_cmd.py:28`, `src/bernstein/cli/commands/workflow_cmd.py:51`).
- A YAML manifest node sets exactly one of `command` or `agent`, with `depends_on`, `when`, `loop`, `fresh_context`, and `timeout_seconds` as options (`src/bernstein/core/workflows/workflow_spec.py:141`, `src/bernstein/core/workflows/workflow_spec.py:176`).
- Nodes form a DAG (DAG = Directed Acyclic Graph, a graph with no loops); the loader rejects unknown dependencies and cycles, and the runner groups nodes into parallel layers in topological order (`src/bernstein/core/workflows/workflow_spec.py:263`, `src/bernstein/core/workflows/workflow_spec.py:310`).
- A governed phase lists `allowed_roles`; an empty set means all roles pass, and only tasks whose role matches count toward phase completion (`src/bernstein/core/planning/workflow.py:56`, `src/bernstein/core/planning/workflow.py:265`).
- A DSL edge is either plain (`depends_on: [decompose]`) or guarded (`source` plus `condition`, for example `status == 'failed'`), and the guard is checked with a safe AST (AST = Abstract Syntax Tree, the parsed form of an expression) evaluator without `eval()` (`src/bernstein/core/planning/workflow_dsl.py:648`, `src/bernstein/core/planning/workflow_dsl.py:126`).
- A non-code deliverable (report, dataset, action log, ops result) completes on the signed lineage entry hash of its canonical bytes, and the receipt is only written after all declared checks pass (`src/bernstein/core/tasks/artifact_completion.py:11`, `src/bernstein/core/tasks/artifact_completion.py:31`).
- A recipe is a workflow plus a typed `params` block; rendering substitutes `{param}` in `prompt`, `command`, and `loop.until` only, leaves `{goal}` for the runner, and then validates as a normal workflow (`src/bernstein/core/workflows/recipe_spec.py:335`, `src/bernstein/core/workflows/recipe_spec.py:291`).
- A registered recipe is identified by the SHA-256 hash (SHA-256 = a function that maps bytes to a fixed 256-bit fingerprint) of its canonical bytes; register, supersede, rollback, pause, and resume are receipts on the HMAC (HMAC = Hash-based Message Authentication Code, a keyed checksum) chain (`src/bernstein/core/workflows/recipe_registry.py:288`, `src/bernstein/core/workflows/recipe_registry.py:943`).
---
## YAML shape (phases, nodes, depends_on, conditions, retry)
A YAML manifest has `name`, `description`, `version`, and `nodes`, where `nodes` is a list (`src/bernstein/core/workflows/workflow_spec.py:242`). Each list item carries `id`, `depends_on`, and either `command` or `agent` (`src/bernstein/core/workflows/workflow_spec.py:141`). The docstring example shows the shape:
```yaml
      - id: research
        agent: manager
        prompt: "Research {goal} and produce a one-page brief."
      - id: plan
        depends_on: [research]
        agent: architect
        prompt: "Turn the brief into a concrete plan."
```
The source of this excerpt is `src/bernstein/core/workflows/workflow_spec.py:16`. The DSL format instead has `name`, `version`, `phases` (a list), and `nodes` (a mapping keyed by node id) (`src/bernstein/core/planning/workflow_dsl.py:465`, `src/bernstein/core/planning/workflow_dsl.py:472`). Each DSL node sets `phase` and `role`, with optional `depends_on`, `retry`, `activity`, `description`, and `estimated_minutes` (`src/bernstein/core/planning/workflow_dsl.py:536`). The canonical DSL example is `.bernstein/workflows/audit-evidence-pack.yaml:9` for `name` and `version`, `.bernstein/workflows/audit-evidence-pack.yaml:12` for `phases`, and `.bernstein/workflows/audit-evidence-pack.yaml:21` for `nodes`. The CLI sniffs the kind without parsing: presence of top-level `phases` means DSL, list-form `nodes` without `phases` means manifest (`src/bernstein/cli/commands/workflow_cmd.py:51`).
## Phases and allowed_roles
A governed phase is a named step in an ordered list with `allowed_roles`, `completion_statuses`, `requires_approval`, and `entry_guard_description` (`src/bernstein/core/planning/workflow.py:51`). An empty `allowed_roles` means no role restriction (`src/bernstein/core/planning/workflow.py:265`). The built-in sequence is plan, implement, verify, review, merge (`src/bernstein/core/planning/workflow.py:120`). Its role limits are: plan allows manager and architect, implement allows all roles, verify allows qa and security, review allows manager and architect, merge allows manager (`src/bernstein/core/planning/workflow.py:124`). DSL phases use the same fields parsed from YAML: `name`, `allowed_roles`, `requires_approval`, and `entry_guard` (`src/bernstein/core/planning/workflow_dsl.py:503`). The audit example declares four phases:
```yaml
phases:
  - name: scope
    allowed_roles: [manager, architect]
  - name: collect
  - name: validate
    allowed_roles: [qa, security]
  - name: deliver
    allowed_roles: [security, manager]
```
The source of this excerpt is `.bernstein/workflows/audit-evidence-pack.yaml:12`. A phase counts as complete when every task whose role matches `allowed_roles` is in a terminal status; with no role restriction, all tasks must be terminal (`src/bernstein/core/planning/workflow.py:286`). Phase output shape is also checked: each of research, plan, implement, and verify has its own JSON schema (JSON = JavaScript Object Notation, a text format for structured data), and the implement schema requires `files_changed`, `tests_added`, and `tests_passing` while verify requires `verdict` (`src/bernstein/core/orchestration/phase_schemas.py:118`, `src/bernstein/core/orchestration/phase_schemas.py:147`).
## Conditional edges (status == failed / done)
A DSL dependency is either a plain string (unconditional) or a mapping with `source`, optional `condition`, and optional `edge_type` (`src/bernstein/core/planning/workflow_dsl.py:606`). The module docstring shows both guarded directions:
```yaml
      fix-bugs:
        phase: implement
        role: backend
        depends_on:
          - source: run-tests
            condition: "status == 'failed'"
        retry:
          max_attempts: 3
          until: "status == 'done'"
      deploy:
        phase: merge
        role: manager
        depends_on:
          - source: run-tests
            condition: "status == 'done'"
```
The source of this excerpt is `src/bernstein/core/planning/workflow_dsl.py:47`. The audit example uses the same pair: `remediate-findings` runs when `mock-auditor-pass` has `status == 'failed'`, and `sign-and-deliver` runs when it has `status == 'done'` (`.bernstein/workflows/audit-evidence-pack.yaml:79`, `.bernstein/workflows/audit-evidence-pack.yaml:90`). Conditions are evaluated against `status`, `result`, and `output` built from the upstream task (`src/bernstein/core/planning/workflow_dsl.py:296`). At run time an unconditional edge is satisfied when the source succeeded, a conditional edge is satisfied only when its guard evaluates true, and a node with all inbound edges skipped is recorded as stranded rather than left absent (`src/bernstein/core/planning/workflow_dsl.py:935`, `src/bernstein/core/planning/workflow_dsl.py:1050`). In the YAML manifest flavour the same idea is spelled `when`: a bash (bash = a command-line shell language) predicate checked after `depends_on` is met; exit 0 runs the node, non-zero marks it skipped without blocking its dependents (`src/bernstein/core/workflows/workflow_spec.py:118`, `src/bernstein/core/workflows/workflow_runner.py:693`).
## Retry and until semantics
The manifest flavour loops a node with `loop: {until, max_iterations}` (`src/bernstein/core/workflows/workflow_spec.py:75`). The runner re-fires the node, checks the `until` bash predicate after each try (exit 0 stops), and marks the node failed when the budget runs out (`src/bernstein/core/workflows/workflow_runner.py:791`). The default cap is 10 with an allowed range of 1 to 1000 (`src/bernstein/core/workflows/workflow_spec.py:87`). The DSL flavour retries with `retry: {max_attempts, until}` where `until` is a condition expression on the node's own output (`src/bernstein/core/planning/workflow_dsl.py:323`, `src/bernstein/core/planning/workflow_dsl.py:587`). A failed task retries only when its node declares a policy, attempts remain, and the `until` condition is not already met (`src/bernstein/core/planning/workflow_dsl.py:1183`). The audit example caps `remediate-findings` at 3 attempts until `status == 'done'` (`.bernstein/workflows/audit-evidence-pack.yaml:86`).
## Artifact contracts (non-code deliverables completing on signed lineage receipt)
A task declares what it produces with `artifact_spec`: `kind`, `canonicalisation`, `criteria`, and `output_path` (`src/bernstein/core/tasks/artifacts.py:489`). Allowed kinds are `code_diff`, `report`, `dataset`, `action_log`, `ops_result`, `finding`, and `blob` (`src/bernstein/core/tasks/artifacts.py:40`). The parser is fail-closed: `kind` is required, any non-`code_diff` kind requires a workdir-relative `output_path`, `code_diff` takes no `output_path` and no criteria, and unknown keys are rejected (`src/bernstein/core/tasks/artifacts.py:605`). The three typed criteria are `schema_valid`, `criteria_match`, and `hash_stable` (`src/bernstein/core/tasks/artifacts.py:77`). Each kind has one canonical byte form (sorted-key JSON, one-JSON-object-per-line JSONL, normalised text, or raw bytes), and the content hash is `sha256:` plus the hex digest (`src/bernstein/core/tasks/artifacts.py:246`, `src/bernstein/core/tasks/artifacts.py:269`). The completion identity for such a task is the signed lineage entry hash of those canonical bytes, not a git commit (`src/bernstein/core/tasks/artifact_completion.py:11`). The order is load, evaluate every declared check, and record only on a full pass (`src/bernstein/core/tasks/artifact_completion.py:21`). Plan steps can carry the same block under `artifact_spec` and it is parsed by the one shared strict parser (`src/bernstein/core/planning/plan_loader.py:428`).
## Recipe registry
A recipe adds an operator-facing `params` block to the workflow body; each param has `name`, `type`, `default`, `required`, `help`, and optional `choices` (`src/bernstein/core/workflows/recipe_spec.py:78`). The name `goal` is reserved because the runner substitutes it from `--goal` (`src/bernstein/core/workflows/recipe_spec.py:111`). Rendering substitutes `{param}` in `prompt`, `command`, and `loop.until` only, so a recipe cannot rewire its own `id` or `depends_on` at launch (`src/bernstein/core/workflows/recipe_spec.py:335`). Registration hashes the canonical body (params, nodes, schedules, triggers, sandbox pool, collision policy, pins) with SHA-256; that hash is the recipe identity (`src/bernstein/core/workflows/recipe_registry.py:330`, `src/bernstein/core/workflows/recipe_registry.py:288`). Re-registering changed bytes under the same name writes a supersede receipt; rollback re-points the name at a prior hash without deleting; pause and resume stop and restart firing while keeping identity (`src/bernstein/core/workflows/recipe_registry.py:943`, `src/bernstein/core/workflows/recipe_registry.py:1067`, `src/bernstein/core/workflows/recipe_registry.py:1111`). A fleet manifest applies many recipes at once: `plan` computes a byte-identical diff with `plan_hash`, and `apply` refuses when the live state drifted from the approved hash (`src/bernstein/core/workflows/recipe_fleet.py:105`, `src/bernstein/core/workflows/recipe_fleet.py:149`).
## plan.yaml stages shape from docs
A plan file is the stage-oriented sibling of a workflow manifest (per docs; not verified in source). Its top-level keys are `name`, `stages`, plus optional `description`, `cli`, `budget`, `max_agents`, `constraints`, `context_files`, and `repos` (per docs; not verified in source) (`docs/architecture/plans.md:43`). Each stage has `name`, `steps`, and optional `description`, `depends_on`, and `repo` (per docs; not verified in source) (`docs/architecture/plans.md:60`). The in-repo seed shows the skeleton:
```yaml
stages:
  - name: "Stage Name"
```
The source of this excerpt is `templates/plan.yaml:105`. Each step compiles into one task with `title`, `role`, `scope`, `complexity`, `files`, and `completion_signals` (per docs; not verified in source) (`docs/architecture/plans.md:74`). Stages run in order and steps inside one stage run in parallel; step-level `depends_on` is not on the schema and stage dependencies are expanded into per-step links by the loader (per docs; not verified in source) (`docs/architecture/plans.md:25`, `docs/architecture/plans.md:99`). The loader requires a `stages` list and rejects a seed-shaped file without one (`src/bernstein/core/planning/plan_loader.py:284`).
**Covers:** src/bernstein/core/workflows/workflow_spec.py, src/bernstein/core/workflows/workflow_runner.py, src/bernstein/core/workflows/recipe_spec.py, src/bernstein/core/workflows/recipe_registry.py, src/bernstein/core/workflows/recipe_fleet.py, src/bernstein/core/planning/workflow.py, src/bernstein/core/planning/workflow_dsl.py, src/bernstein/core/planning/workflow_importer.py, .bernstein/workflows/audit-evidence-pack.yaml, src/bernstein/core/orchestration/phase_schemas.py, src/bernstein/core/tasks/artifacts.py, src/bernstein/core/tasks/artifact_completion.py, src/bernstein/cli/commands/workflow_cmd.py, src/bernstein/core/planning/plan_loader.py, templates/plan.yaml, docs/architecture/plans.md
