> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Policy as Code and Quality Gates
**In one sentence:** Bernstein declares checks and limits in YAML (YAML Ain't Markup Language, a text config format) files and enforces them in code that can block merges, tool calls, task starts, and credential use.
## Key points
- Quality gates are declared in `bernstein.yaml` under `quality_gates:` and loaded as `QualityGatesConfig` defaults in code (src/bernstein/core/quality/quality_gates.py:201, bernstein.yaml:33).
- The gate runner treats the run as passing only when no result is marked blocked, and refuses bypass unless config allows it (src/bernstein/core/quality/gate_runner.py:96, src/bernstein/core/quality/gate_runner.py:138).
- A change that contains a run-configuration path is blocked by the run-config gate, which checks the changed-file names (src/bernstein/core/quality/run_config_gate.py:73, src/bernstein/core/quality/gate_pipeline.py:394).
- Tool-call approval defaults to off (`interactive=False`) with a 10 minute TTL (TTL, Time To Live, how long a request waits) and an opt-in classifier shortcut (src/bernstein/core/approval/gate.py:97, src/bernstein/core/approval/queue.py:45).
- Task-start approval uses files under `.sdd/runtime/approvals/` with `.pending`, `.approved`, and `.rejected` sentinels (src/bernstein/core/orchestration/approval_gate.py:57, src/bernstein/core/orchestration/approval_gate.py:416).
- Adapter spawn requires proof: the adapter admission gate seals admit or refusal receipts and anchors them in the audit chain (src/bernstein/adapters/admission.py:1198, src/bernstein/adapters/registry.py:267).
- Per-agent credentials are scoped grants bound to task, audience (the service the token may be shown to), expiry, and capability ceiling (a list that caps what the token may do), signed and hash-chained (src/bernstein/core/identity/grants.py:109, src/bernstein/core/identity/grants.py:540).
- Cost-aware routing uses LinUCB (Linear Upper Confidence Bound, a math method that balances trying new options and reusing good ones) plus UCB1 for effort, with reward `quality * (1 - normalized_cost)` (src/bernstein/core/routing/bandit_router.py:1129, src/bernstein/core/routing/bandit_router.py:1647).
---
## What policy as code concretely means
Policy as code means rules live in versioned text files and code reads them at runtime. The repo-root example sets lint, tests, timeout, and merge checks (bernstein.yaml:33, bernstein.yaml:62):

```
quality_gates:
  enabled: true
  lint: true
  lint_command: uv run ruff check .
  type_check: false
  tests: true
```

The same file declares the autofix cost cap and ladder flag (bernstein.yaml:62, src/bernstein/core/autofix/ladder.py:72):

```
autofix:
  cost_cap_per_pr: 1.0
  ladder:
    enabled: false
```

Enforcement points in code include `run_quality_gates()` which builds a `GateRunner` and runs the pipeline (src/bernstein/core/quality/quality_gates.py:1097, src/bernstein/core/quality/quality_gates.py:1135), `load_approval_config()` which reads the `approvals:` block (src/bernstein/core/approval/gate.py:102), `load_ladder_settings()` which reads the `autofix` block (src/bernstein/core/autofix/ladder.py:72), and `policy_input_from_project()` which builds a policy-engine snapshot from the same compliance checks used by the audit (src/bernstein/core/govern/compliance_checks.py:347).

Governance composition is also code, not comments. `PolicySet` holds layers in declaration order and `compose()` applies them in fixed order (src/bernstein/core/govern/policy_layers.py:68, src/bernstein/core/govern/policy_layers.py:258):

```
COMPOSITION_ORDER: tuple[LayerKind, ...] = tuple(LayerKind)
```

Layer order is classification, then baseline, then instrumentation, then exactly one class overlay (src/bernstein/core/govern/policy_layers.py:48, src/bernstein/core/govern/policy_layers.py:56). Zero or multiple matching overlays produce a finding instead of picking one silently (src/bernstein/core/govern/policy_layers.py:299).

## Gate kinds
Gate names are a closed set including lint, type check, tests, PII (Personally Identifiable Information, secrets and personal data) scan, DLP (Data Loss Prevention, license and regulated-data) scan, mutation testing, intent verification, and review rubric (src/bernstein/core/quality/gate_pipeline.py:57). The default pipeline maps config flags to steps with required flags and run conditions (src/bernstein/core/quality/gate_pipeline.py:378, src/bernstein/core/quality/gate_pipeline.py:417):

```
    ("auto_format", "auto_format", False, "any_changed"),
    ("lint", "lint", True, "always"),
    ("type_check", "type_check", True, "python_changed"),
```

Defaults in `QualityGatesConfig` show lint on, type check off, tests off in the library default (src/bernstein/core/quality/quality_gates.py:201):

```
    enabled: bool = True
    lint: bool = True
    lint_command: str = "ruff check ."
    type_check: bool = False
    type_check_command: str = "pyright"
    tests: bool = False
    test_command: str = "uv run python scripts/run_tests.py -x"
```

Lint, type check, and tests run shell commands with a timeout and return success, output, and exit code (src/bernstein/core/quality/quality_gates.py:516). PII scanning checks changed files for secrets and blocks on high severity (src/bernstein/core/quality/quality_gates.py:869). DLP scanning adds license, regulated-data, and proprietary-data checks with separate block flags (src/bernstein/core/quality/quality_gates.py:988, src/bernstein/core/quality/quality_gates.py:271). Mutation testing parses a score and compares it to a threshold (src/bernstein/core/quality/quality_gates.py:604). Intent verification asks an LLM (Large Language Model, an AI text model) whether the diff matches the task and blocks on "no" by default (src/bernstein/core/quality/quality_gates.py:480, src/bernstein/core/quality/quality_gates.py:88). The run-config gate blocks any change containing `bernstein.yaml` or related overlay paths (src/bernstein/core/quality/run_config_gate.py:73, src/bernstein/core/quality/run_config_gate.py:102). Each gate writes JSONL (JSON Lines, one JSON object per line) events to `.sdd/metrics/quality_gates.jsonl` (src/bernstein/core/quality/quality_gates.py:1202). The retrospective step is separate: it reads completed tasks and costs and writes `.sdd/runtime/retrospective.md` (src/bernstein/core/quality/retrospective.py:1).

Bypass is closed by default. The runner raises when a skip is requested but `allow_bypass` is false (src/bernstein/core/quality/gate_runner.py:96):

```
        if skip_set and not self._config.allow_bypass:
            raise ValueError("quality gate bypass is disabled by configuration")
```

The final verdict is a conjunction over blocked flags (src/bernstein/core/quality/gate_runner.py:136):

```
        report = GateReport(
            task_id=task.id,
            overall_pass=all(not result.blocked for result in results),
```

## Approval and hold flow
Two approval layers exist. The tool-call gate (`src/bernstein/core/approval/gate.py`) checks each tool use. The task gate (`src/bernstein/core/orchestration/approval_gate.py`) blocks a task before it runs until a human approves.

Tool-call approval config defaults to non-interactive (src/bernstein/core/approval/gate.py:77):

```
    interactive: bool = False
    timeout_seconds: int = DEFAULT_TTL_SECONDS
    smart_auto_approve: bool = False
```

Order is policy deny first, then classifier deny, then allow-list or queue (src/bernstein/core/approval/gate.py:435, src/bernstein/core/approval/gate.py:452). A pending tool approval carries session, role, tool name, args, TTL, and a single-use nonce (a random value that must be echoed back to prevent replay) (src/bernstein/core/approval/models.py:230, src/bernstein/core/approval/models.py:222). Decisions are ALLOW, REJECT, or ALWAYS, where ALWAYS also promotes the pattern to the allow-list (src/bernstein/core/approval/models.py:201, src/bernstein/core/approval/gate.py:488). Timeout raises and must be treated as reject (src/bernstein/core/approval/models.py:18, src/bernstein/core/approval/models.py:272). The queue persists under `.sdd/runtime/approvals/*.json` with atomic writes and a default TTL of 600 seconds (src/bernstein/core/approval/queue.py:1, src/bernstein/core/approval/queue.py:45).

Task approval is file-driven. The sentinel directory is (src/bernstein/core/orchestration/approval_gate.py:57):

```
_RUNTIME_REL = Path(".sdd") / "runtime" / "approvals"
```

`wait_for_approval()` writes `<task_id>.pending`, polls for `<task_id>.approved` or `<task_id>.rejected`, and applies `default_action` on timeout (src/bernstein/core/orchestration/approval_gate.py:416, src/bernstein/core/orchestration/approval_gate.py:350). Approval files win by arriving first through atomic replace (src/bernstein/core/orchestration/approval_gate.py:173).

Holds are different from approvals: they keep the orchestrator from stopping while idle. A caller acquires a hold with a reason and TTL, renews it as a heartbeat, and releases it when done (src/bernstein/core/orchestration/holds.py:1, src/bernstein/core/orchestration/holds.py:104). The default grace window is 45 seconds (src/bernstein/core/orchestration/holds.py:45).

## Admission gate
Two admission gates exist. The adapter admission gate controls which CLI (Command Line Interface, a text tool) adapter may spawn. The resource admission engine controls how many tasks may run at once.

`AdmissionGate.admit()` returns None for exempt or disabled paths, otherwise seals and anchors a receipt, and raises refusal under enforce policy when proof is missing (src/bernstein/adapters/admission.py:1198):

```
    def admit(self, adapter: str) -> AdmissionDecision | None:
        """Check admission for ``adapter``; refuse when it cannot be proved.
```

The verdict folds live evidence (binary version, contract hash, replay output) against the sealed receipt and refuses on stale receipt or fingerprint mismatch (src/bernstein/adapters/admission.py:1225, src/bernstein/adapters/admission.py:751). Policy modes are warn, enforce, and off (src/bernstein/adapters/admission.py:271, src/bernstein/adapters/admission.py:276, src/bernstein/adapters/admission.py:279).

The resource engine `request_grant()` appends a grant row only when admissible; under enforce a full pool refuses, under advise it grants over-limit with a signed waiver, under off the gate is inert (src/bernstein/core/admission/engine.py:201). State is re-projected from the chain, never held as mutable memory (src/bernstein/core/admission/engine.py:1, src/bernstein/core/admission/projection.py:95).

## Credential scoping per agent
Workers do not share one install-wide secret. The orchestrator issues a scoped grant per task with task id, backing-secret reference, audience, expiry, and capability ceiling (src/bernstein/core/identity/grants.py:1, src/bernstein/core/identity/grants.py:540):

```
    def issue_grant(
        self,
        *,
        run_id: str,
        task_id: str,
        secret_name: str,
        audience: str,
```

Only a salted hash of the secret name is stored, never the raw name (src/bernstein/core/identity/grants.py:211). Each record carries an Ed25519 signature (a public-key signature that proves who authorized it) plus an HMAC (Hash-based Message Authentication Code, a keyed checksum that proves no tampering) chained to the prior record from a genesis anchor (src/bernstein/core/identity/grants.py:21, src/bernstein/core/identity/grants.py:109):

```
GENESIS_HMAC: Final[str] = "0" * 64
```

Delegation receipts add narrowing: each hop records a `DelegationScope` with permissions, duties, task ids, path prefixes, expiry, use count, and depth (src/bernstein/core/identity/delegation_scope.py:174). A child that widens the parent on any axis is a violation (src/bernstein/core/identity/delegation_scope.py:259). Duties use a small vocabulary with maker-checker separation (src/bernstein/core/identity/delegation_scope.py:133):

```
DUTY_SPAWN: str = "spawn"
DUTY_APPROVE: str = "approve"
DUTY_MERGE: str = "merge"
```

The same principal may not hold separated pairs such as spawn plus approve (src/bernstein/core/identity/delegation_scope.py:140, src/bernstein/core/identity/delegation_scope.py:612).

## Cost-aware routing
Found in source, not per-docs only. `BanditRouter.select()` picks model plus effort; during cold start it uses static routing, after warmup the LinUCB policy picks and a capability floor clamps high-stakes tasks to a safe minimum (src/bernstein/core/routing/bandit_router.py:1129, src/bernstein/core/routing/bandit_router.py:1148). Effort uses a separate UCB1 bandit keyed on task type and model (src/bernstein/core/routing/bandit_router.py:9, src/bernstein/core/routing/bandit_router.py:1201). The composite reward is (src/bernstein/core/routing/bandit_router.py:1647):

```
    quality = max(0.0, min(1.0, quality_score))
    if budget_ceiling <= 0.0:
        return quality
    norm_cost = max(0.0, min(1.0, cost_usd / budget_ceiling))
    return quality * (1.0 - norm_cost)
```

Policy state persists under `.sdd/routing/policy.json` and `.sdd/routing/bandit_state.json` (src/bernstein/core/routing/bandit_router.py:26).

## Autofix daemon
Found in source. The daemon watches configured repos for CI (Continuous Integration, automatic build and test on each change) failures and dispatches repairs (src/bernstein/core/autofix/__init__.py:1, src/bernstein/core/autofix/daemon.py:7). The ladder has four rungs from cheapest to most invasive: rung 0 lint fix in place, rung 1 single-file test failure, rung 2 multi-file failure, rung 3 out-of-scope human handoff (src/bernstein/core/autofix/ladder.py:1). The daemon picks the lowest matching rung and refuses any rung above the per-PR (Pull Request, a proposed change) cost cap (src/bernstein/core/autofix/ladder.py:20). When the flag is off the helper skips (src/bernstein/core/autofix/ladder.py:690):

```
    if not settings.enabled:
        return AutofixOutcome(
            outcome="skipped",
            rung_id="rung-3-out-of-scope",
            message="autofix.ladder.enabled is false; ladder is operator-flagged off.",
        )
```

**Covers:** bernstein.yaml, config/eu_ai_act_clause_map.yaml, src/bernstein/core/quality/quality_gates.py, src/bernstein/core/quality/gate_runner.py, src/bernstein/core/quality/gate_pipeline.py, src/bernstein/core/quality/run_config_gate.py, src/bernstein/core/quality/retrospective.py, src/bernstein/core/govern/policy_layers.py, src/bernstein/core/govern/compliance_checks.py, src/bernstein/core/approval/gate.py, src/bernstein/core/approval/models.py, src/bernstein/core/approval/queue.py, src/bernstein/core/orchestration/approval_gate.py, src/bernstein/core/orchestration/holds.py, src/bernstein/adapters/admission.py, src/bernstein/core/admission/engine.py, src/bernstein/core/identity/delegation_scope.py, src/bernstein/core/identity/grants.py, src/bernstein/core/routing/bandit_router.py, src/bernstein/core/autofix/ladder.py, src/bernstein/core/autofix/daemon.py
