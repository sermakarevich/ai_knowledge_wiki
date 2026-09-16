> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Multi-Harness Support

**In one sentence:** superharness dispatches work to five coding-agent runtimes (Claude Code, Codex CLI, Gemini CLI, opencode, Pi) through one `Harness` protocol (a shared interface, i.e. a contract every adapter must implement), YAML manifests (config files describing each adapter) plus a Python adapter registry (lookup/validation code), and per-harness launcher scripts — with golden parity tests proving adapter argv is byte-identical to the legacy path.

## Key points

- The `Harness` protocol (`src/superharness/harnesses/base.py:33-51`) requires only `build_invocation(task, project_dir, non_interactive) -> Invocation`; model discovery via `discover_models(auth_mode)` defaults to no-op `[]`.
- `Invocation` (`src/superharness/harnesses/base.py:16-30`) is a frozen dataclass (immutable, i.e. cannot be changed after creation) with `argv: tuple`, `env: dict`, `cwd: str`; tuple storage blocks both reassignment and in-place mutation.
- Two registries cooperate: `harnesses/__init__.py` maps runtime name → live `Harness` object (`register`/`get_harness`), while `engine/adapter_registry.py:190-283` maps adapter name → YAML manifest → launcher-script path, validation, and model tiers.
- Every manifest declares `name, version, type (native|external), launcher_script, capabilities, model_tiers, requires, validation` (`src/superharness/engine/adapter_registry.py:103-128`); new-schema tiers add `preferred / accept / auth_compat / capability_tags` (`src/superharness/adapter_manifests/codex-cli.yaml:23-43`).
- Claude is the special case: `ClaudeHarness.build_invocation` (`src/superharness/harnesses/claude.py:28-61`) builds argv by hand and never prefixes the model, while codex/gemini/opencode/pi all delegate to `build_generic_invocation` (`src/superharness/harnesses/base.py:93-132`), which applies provider/model prefixing.
- Discovery differs per harness: claude/codex/gemini probe via the manifest accept chain (`src/superharness/harnesses/base.py:64-90`); opencode runs `opencode models` natively (`src/superharness/harnesses/opencode.py:57-62`); Pi parses its offline `pi --offline ... --list-models` table (`src/superharness/harnesses/pi.py:15-23`).
- `shux adapter-payload` (`src/superharness/commands/adapter_payload.py:680-709`) emits one stable JSON snapshot (schema `1.4`) with tasks, edges, ledger, failures, decisions, inbox, agent pulse, rules, artifacts, heartbeats for external consumers such as Morpheme.
- Parity tests (`tests/unit/test_harness_registry.py:39-71`, `tests/unit/test_harness_adapters.py:37-123`) assert adapter argv tuples equal golden values captured from the live legacy `delegate.py::_launch_agent` path, including prompt-as-single-element injection safety.

---

## Harness protocol

`src/superharness/harnesses/base.py:1-132` defines the whole contract. Method/signature table:

| Member | Signature / shape | Semantics |
|---|---|---|
| `Invocation` | `argv: tuple[str,...]; env: dict[str,str]; cwd: str` (`base.py:16-30`) | Immutable ready-to-spawn subprocess description; `__post_init__` coerces argv to tuple (`base.py:29-30`) |
| `Harness.name` | `str` (`base.py:35`) | Registry key: `claude-code`, `codex-cli`, `gemini-cli`, `opencode`, `pi` |
| `Harness.build_invocation` | `(task: dict, project_dir: str, non_interactive: bool) -> Invocation` (`base.py:37-39`) | Only required method; turns a task dict into exact argv/env/cwd |
| `Harness.discover_models` | `(auth_mode: str = "unknown") -> list[DiscoveredModel]` (`base.py:41-51`) | Default returns `[]`; overridden per adapter |
| `_base_env` | `(overrides) -> dict` (`base.py:54-61`) | Returns overlay dict, empty by default — every current adapter inherits parent env |
| `discover_via_probe` | `(agent, auth_mode, budget_seconds=5.0)` (`base.py:64-90`) | Loads manifest, resolves `mini`-tier accept chain, runs one `ProbeDiscovery` pass; never raises, returns `[]` on failure |
| `build_generic_invocation` | `(name, task, project_dir, non_interactive)` (`base.py:93-132`) | Shared argv assembly: `bash <launcher> --project … --prompt … [--non-interactive] [--yolo] [--codex-bypass] [--model …] [--effort …]` with `apply_model_prefix` (`base.py:112-130`) |

Verbatim excerpt (`src/superharness/harnesses/base.py:33-51`):

```python
@runtime_checkable
class Harness(Protocol):
    name: str

    def build_invocation(
        self, task: dict, project_dir: str, non_interactive: bool
    ) -> Invocation: ...

    def discover_models(
        self, auth_mode: str = "unknown"
    ) -> list["DiscoveredModel"]:
        """Return models available on this host for the given auth mode.
        ...
        """
        return []
```

## Adapter registry

Flow is register → discover → select → validate → resolve (`src/superharness/engine/adapter_registry.py:1-356`):

1. **Register (live objects):** `harnesses/__init__.py` keeps `_REGISTRY: dict[str, Harness]`, with `register(name, harness)` / `get_harness(name)` (raises `KeyError` listing known names) and `_register_builtins()` wiring the five harnesses; `KNOWN_HARNESSES` snapshots the sorted keys.
2. **Discover (manifests):** `list_adapters()` globs `MANIFEST_DIR/*.yaml` (`adapter_registry.py:190-194`); `MANIFEST_DIR` is `adapter_manifests/` (`adapter_registry.py:23`).
3. **Select/load:** `load_manifest(name)` parses YAML via `AdapterManifest.from_dict`, caches in `_manifest_cache`, raises `AdapterValidationError` for unknown/malformed manifests (`adapter_registry.py:197-227`).
4. **Validate:** `validate_adapter(name)` checks `requires.bin` via `shutil.which` when `validation.check_bin` is set, and `requires.env` vars when `check_env` is set (`adapter_registry.py:230-261`); `adapter_info(name)` returns the same checks as displayable `valid/issues` data (`adapter_registry.py:326-356`).
5. **Resolve:** `resolve_launcher(name, scripts_dir)` joins `scripts_dir + manifest.launcher_script` and errors if missing (`adapter_registry.py:264-283`); `resolve_model(owner, tier, version)` walks `model_tiers` with pass-through fallback `{id: tier, label: tier}` (`adapter_registry.py:286-302`); `flagship()/flagship_1m()/fallback_flagship()` resolve the `max`/`max-1m` tiers so model bumps touch only `claude-code.yaml` (`adapter_registry.py:305-323`).

Verbatim excerpt (`src/superharness/engine/adapter_registry.py:264-283`):

```python
def resolve_launcher(name: str, scripts_dir: str) -> str:
    """Resolve the launcher script path for an adapter.
    ...
    """
    manifest = load_manifest(name)
    launcher_path = os.path.join(scripts_dir, manifest.launcher_script)
    if not os.path.exists(launcher_path):
        raise AdapterValidationError(
            f"Adapter '{name}' launcher script not found: {launcher_path}"
        )
    return launcher_path
```

## Manifests

Six YAML files ship in `src/superharness/adapter_manifests/`: `claude-code`, `codex-cli`, `gemini-cli`, `opencode`, `pi`, `prime-agent`. Field table (parsed by `AdapterManifest.from_dict`, `adapter_registry.py:160-187`):

| Field | Meaning | Example |
|---|---|---|
| `name / version / description` | Identity | `name: claude-code`, `version: "1"` (`claude-code.yaml:1-3`) |
| `type` | `native` (first-party) vs `external` (third-party) | `pi.yaml:6` is `external`; `claude-code.yaml:4` is `native` |
| `launcher_script` | Bash entrypoint under `scripts/` | `delegate-to-claude.sh` (`claude-code.yaml:5`) |
| `capabilities` | Feature list | `code_generation, file_editing, test_execution, multi_file_refactor` (`codex-cli.yaml:6-10`) |
| `supports_effort` | Whether `--effort` is forwarded | `true` for claude/codex/pi; `false` for gemini/opencode |
| `model_tiers` | `mini / standard / max (/ max-1m)` → model ids | Two schemas: versioned `{versions: {"*": {id,label}}}` (claude, gemini, opencode) vs new-schema `{preferred, accept, auth_compat, capability_tags}` (codex, pi, prime-agent) |
| `requires.bin / requires.env` | Binary + env prerequisites | `requires: {bin: claude}` (`claude-code.yaml:33-35`) |
| `validation.check_bin / check_env` | Whether absence fails validation | `true/false` for claude+codex; `false/false` for gemini/opencode/pi/prime-agent |

Verbatim sample — versioned schema (`src/superharness/adapter_manifests/claude-code.yaml:15-32`):

```yaml
model_tiers:
  mini:
    versions:
      "*": { id: claude-haiku-4-5-20251001, label: "Haiku 4.5" }
  standard:
    versions:
      "*":   { id: claude-sonnet-4-6, label: "Sonnet 4.6" }
      "4.6": { id: claude-sonnet-4-6, label: "Sonnet 4.6" }
      "4.5": { id: claude-sonnet-4-5, label: "Sonnet 4.5" }
  max:
    versions:
      "*":   { id: claude-opus-4-8,   label: "Opus 4.8" }
      "4.7": { id: claude-opus-4-7,   label: "Opus 4.7" }  # pin available
      "4.6": { id: claude-opus-4-7,   label: "Opus 4.7" }  # 4.6 alias — same cost
```

New-schema sample (auth-aware chains, `src/superharness/adapter_manifests/codex-cli.yaml:23-29`): `mini.preferred: gpt-5.1-codex-mini`, `accept: [gpt-5.1-codex-mini, gpt-5.4]`, `auth_compat: {chatgpt: [gpt-5.4], apikey: [gpt-5.1-codex-mini, gpt-5-codex-mini]}` — measured live 2026-08-07 because ChatGPT-login hosts reject mini/standard codex models with HTTP 400. Gemini is deprecated upstream (standalone CLI killed 2026-08, `gemini-cli.yaml:2`). `prime-agent.yaml:1-18` is explicitly EXPERIMENTAL/INERT — its `delegate-to-prime-agent.sh` refuses everything but `--help` until a real binary is probed.

## Per-harness adapters

| Harness | Launcher | Session / hook mechanism | Notable quirk (file:line) |
|---|---|---|---|
| `claude-code` (`harnesses/claude.py:21-61`) | `bash delegate-to-claude.sh --project … --prompt …` → `exec claude … "$PROMPT"` (`scripts/delegate-to-claude.sh:52`) | Stateless CLI turn; `--non-interactive` maps to `-p --dangerously-skip-permissions` (`scripts/delegate-to-claude.sh:33-37`) | Bespoke argv builder, never model-prefixes — Claude CLI rejects the `anthropic/` prefix (`harnesses/base.py:101-102`); `env={}` inherits parent env (`harnesses/claude.py:61`) |
| `codex-cli` (`harnesses/codex.py:12-22`) | `bash delegate-to-codex.sh …` → `exec codex … "$PROMPT"` (`scripts/delegate-to-codex.sh:77`) with `-C $PROJECT_DIR` fallback (`scripts/delegate-to-codex.sh:81-83`) | Stateless CLI turn; effort maps to `-c model_reasoning_effort=` (`codex-cli.yaml:11`, `scripts/delegate-to-codex.sh:35`) | Uses `build_generic_invocation`, so model gets `openai/` prefix — parity test expects `openai/gpt-5-codex` (`tests/unit/test_harness_adapters.py:52-53`) |
| `gemini-cli` (`harnesses/gemini.py:12-22`) | `bash delegate-to-gemini.sh …` → `exec gemini … "$PROMPT" < /dev/null` (`scripts/delegate-to-gemini.sh:141`) | Piped-stdin forbidden (EOF kills Gemini); `< /dev/null` plus bootstrap prompt instead (`scripts/delegate-to-gemini.sh:121-126`); retries once on `ETIMEDOUT/ECONNRESET` (`scripts/delegate-to-gemini.sh:130-131`) | Preflight requires `GEMINI.md` with protocol sections or dispatch stalls (`scripts/delegate-to-gemini.sh:99-104`); `supports_effort: false` (`gemini-cli.yaml:10`) |
| `opencode` (`harnesses/opencode.py:47-83`) | `bash delegate-to-opencode.sh …` → `exec opencode … "$PROMPT"` (`scripts/delegate-to-opencode.sh:45`) | Multi-provider CLI; native discovery parses `opencode models` (`provider/model` per line, junk skipped, `harnesses/opencode.py:19-44`), never raises (`harnesses/opencode.py:50-78`) | Generic invocation with prefixing — `claude-sonnet-4-6` becomes `anthropic/claude-sonnet-4-6` (`tests/unit/test_harness_adapters.py:96-97`); default tiers point at DeepSeek (`opencode.yaml:11-20`) |
| `pi` (`harnesses/pi.py:50-91`) | `bash delegate-to-pi.sh …` → `exec "$PYTHON_BIN" -m superharness.engine.pi_runtime "$@"` (`scripts/delegate-to-pi.sh:12`) | Not a raw CLI exec: `pi_runtime.build_command` builds `pi --mode json --no-session --no-extensions --no-skills --no-prompt-templates [--model …] [--thinking …] -p <prompt>` (`engine/pi_runtime.py:39-71`); `PiEventParser` enforces `session → message_end → agent_end` with bounded capture (`engine/pi_runtime.py:74-206`); effort maps `low/medium/high/xhigh/max→thinking` (`engine/pi_runtime.py:24-30`) | Discovery is offline-only: parses `pi --offline --no-extensions --no-skills --no-prompt-templates --list-models` provider/model table, trying stdout then stderr (Pi 0.73.1 writes table to stderr), never raises (`harnesses/pi.py:15-23,53-86`) |

`shux adapters` surfaces all of this: `list` (`commands/adapters.py:147-187`), `info <name>` (`commands/adapters.py:190-239`), `test <name>` (`commands/adapters.py:242-258`), and `--probe` which runs discovery across every adapter with cache-first reads (`commands/adapters.py:23-76,93-144`).

## Adapter payload spec

`shux adapter-payload --json` (`src/superharness/commands/adapter_payload.py:1-8`, schema `SCHEMA_VERSION = "1.4"` at `adapter_payload.py:31`) emits one JSON document built by `build_payload(project_path)` (`adapter_payload.py:680-709`):

```python
return {
    "schema_version": SCHEMA_VERSION,
    "project_settings": project_settings,
    "contract_id": contract_doc.get("id") or "",
    "goal": contract_doc.get("goal") or "",
    "tasks": tasks,
    "edges": _build_edges(tasks),
    "ledger": _parse_ledger(sh_dir),
    "failures": _load_failures(sh_dir),
    "decisions": _load_decisions(sh_dir),
    "inbox": _load_inbox(sh_dir),
    "agent_pulse": _load_agent_pulse(sh_dir),
    "rules": _load_rules(str(sh_dir.parent)),
    "artifacts": _load_artifacts(project_path),
    "agent_heartbeats": _load_heartbeats(project_path),
}
```

Per-task entries carry `id/title/status/display_status/color/owner/resolved_model (via resolve_model, adapter_payload.py:523-532)/blocked_by/effort/acceptance_criteria/handoffs/subtasks/classifier/decomposer/retry/next_action/workflow/autonomy/require_tdd/visual_context` (`adapter_payload.py:588-658`); raw statuses map to display statuses via `_STATUS_MAP` (`adapter_payload.py:81-96`); missing `--project` exits nonzero with stderr (`adapter_payload.py:796-799`) so callers never trust an empty payload.

## Parity tests

What is proven (`tests/unit/test_harness_registry.py:39-71`, `tests/unit/test_harness_adapters.py:37-123`):

- Each adapter's `build_invocation` output equals a golden argv tuple captured from the live legacy `delegate.py::_launch_agent` path before the adapter existed ("capture first, hardcode, then extract" — `test_harness_registry.py:14-17`, `test_harness_adapters.py:6-11`).
- Claude golden keeps the model bare (`claude-sonnet-4-6`, `test_harness_registry.py:58-68`); codex/gemini/opencode/pi goldens assert prefixed ids (`openai/gpt-5-codex`, `google/gemini-3-pro`, `anthropic/claude-sonnet-4-6`, `deepseek/deepseek-v4-flash`).
- `Invocation` frozenness: attribute reassignment and tuple item assignment both raise (`test_harness_registry.py:74-79`).
- Prompt-injection safety: a `do the thing; rm -rf / …` prompt stays exactly one argv element for every adapter (`test_harness_registry.py:82-91`, `test_harness_adapters.py:241-250`); `get_harness("not-a-real-harness")` raises `KeyError` naming known harnesses (`test_harness_registry.py:33-36`); unknown dispatch owners fail cleanly (`test_harness_adapters.py:253+`).

Verbatim golden (`tests/unit/test_harness_adapters.py:37-56`):

```python
def test_codex_invocation_parity():
    launcher = resolve_launcher("codex-cli", _scripts_dir())
    invocation = get_harness("codex-cli").build_invocation(
        task={"prompt": "do the thing", "model": "gpt-5-codex", "effort": "high"},
        project_dir="/tmp/proj",
        non_interactive=True,
    )
    assert invocation.argv == (
        "bash",
        launcher,
        "--project",
        "/tmp/proj",
        "--prompt",
        "do the thing",
        "--non-interactive",
        "--model",
        "openai/gpt-5-codex",
        "--effort",
        "high",
    )
    assert invocation.cwd == "/tmp/proj"
```

**Covers:** `harnesses/base.py`, `harnesses/__init__.py`, `harnesses/claude.py`, `harnesses/codex.py`, `harnesses/gemini.py`, `harnesses/opencode.py`, `harnesses/pi.py`, `engine/adapter_registry.py`, `adapter_manifests/*.yaml`, `commands/adapters.py`, `commands/adapter_payload.py`, `scripts/delegate-to-*.sh`, `engine/pi_runtime.py`, `tests/unit/test_harness_adapters.py`, `test_harness_registry.py`, `test_adapter_payload.py` @ `9c2166d`.
