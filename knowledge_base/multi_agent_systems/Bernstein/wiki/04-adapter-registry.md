> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Multi-Harness Support: The Adapter Registry

**In one sentence:** Bernstein runs many different coding-agent CLIs (CLI = Command-Line Interface) through one registry that maps a short name such as `claude` to an adapter class implementing a shared `spawn` interface.

## Key points

- The registry is a plain dict named `_ADAPTERS` mapping short names to adapter classes or instances, defined in `src/bernstein/adapters/registry.py:86`.
- `get_adapter()` in `src/bernstein/adapters/registry.py:232` instantiates the class for a name and stamps the name on the instance (`src/bernstein/adapters/registry.py:293`), raising `ValueError` for unknown names (`src/bernstein/adapters/registry.py:284`).
- Every adapter implements the `CLIAdapter` interface in `src/bernstein/adapters/base.py:528`, whose two required methods are `spawn()` (`src/bernstein/adapters/base.py:812`) and `name()` (`src/bernstein/adapters/base.py:1069`).
- Provider strings such as `openai` resolve to adapters through the `provides` tuples declared per adapter (default `src/bernstein/adapters/base.py:1251`), consumed by `adapter_name_for_provider()` in `src/bernstein/adapters/registry.py:517`.
- The `generic` adapter (`src/bernstein/adapters/generic.py:17`) wraps any CLI with a configurable `--prompt` / `--model` command shape, and `get_adapter()` special-cases it in `src/bernstein/adapters/registry.py:266`.
- Third-party adapters register without source edits via the `bernstein.adapters` entry-point group, loaded in `src/bernstein/adapters/registry.py:207` and declared in `pyproject.toml:351`.
- New agents can ship as data-only declarations: `profile_built_adapter_classes()` in `src/bernstein/adapters/capability_profile.py:1507` builds adapter classes from profiles and merges them into the registry in `src/bernstein/adapters/registry.py:160`.
- Each adapter declares a five-axis strategy row (resume, dangerous-mode, event-channel, output-mode, session-state) in `STRATEGY_MATRIX` (`src/bernstein/adapters/_contract.py:659`), read through `strategy_for()` (`src/bernstein/adapters/_contract.py:884`).

---

## Registry lookup mechanics

The centerpiece is the `_ADAPTERS` dict (`src/bernstein/adapters/registry.py:86`):

```
_ADAPTERS: dict[str, type[CLIAdapter] | CLIAdapter] = {
```

Each key is a short name and each value is an adapter class (or, rarely, a pre-built instance). Examples from the table:

```
    "claude": ClaudeCodeAdapter,
```

`src/bernstein/adapters/registry.py:98`

Two keys can point at one class: both `"antigravity"` and `"gemini"` resolve to `GeminiAdapter` (`src/bernstein/adapters/registry.py:119`, `src/bernstein/adapters/registry.py:120`) because the upstream Google CLI is changing binary names and the adapter discovers either binary at spawn time.

Lookup happens in `get_adapter()` (`src/bernstein/adapters/registry.py:232`):

```
def get_adapter(cli_name: str, *, admission_gate: AdmissionGateLike | None = None) -> CLIAdapter:
```

The function reads the table (`src/bernstein/adapters/registry.py:275`):

```
    adapter_cls = _ADAPTERS.get(cli_name)
```

It then instantiates classes but passes through instances unchanged (`src/bernstein/adapters/registry.py:292`):

```
    instance = adapter_cls if isinstance(adapter_cls, CLIAdapter) else adapter_cls()  # type: ignore[assignment]  # dynamic adapter resolution
```

and stamps the lookup name on the result (`src/bernstein/adapters/registry.py:293`):

```
    instance.registry_name = cli_name
```

Unknown names raise `ValueError` listing what exists (`src/bernstein/adapters/registry.py:284`):

```
        raise ValueError(f"Unknown adapter '{cli_name}'. Available: {available}")
```

Removed names get replacement guidance instead of the generic error: `_REMOVED_ADAPTERS` (`src/bernstein/adapters/registry.py:170`) currently maps `"cloudflare"` to instructions pointing at other adapters. Enumeration is alphabetical and deterministic via `iter_adapter_specs()` (`src/bernstein/adapters/registry.py:358`), which triggers entry-point discovery first (`src/bernstein/adapters/registry.py:370`) and yields sorted pairs (`src/bernstein/adapters/registry.py:371`, `src/bernstein/adapters/registry.py:372`). The selectable set for runs (minus the `mock` test stub) comes from `selectable_adapter_names()` (`src/bernstein/adapters/registry.py:384`).

## CLIAdapter contract (methods a new adapter implements)

`CLIAdapter` is the shared interface for launching and monitoring CLI coding agents (`src/bernstein/adapters/base.py:528`). A new adapter subclasses it and implements two abstract (must-implement) methods. The first starts the agent process:

```
    @abstractmethod
    def spawn(
```

`src/bernstein/adapters/base.py:811`, `src/bernstein/adapters/base.py:812`

`spawn()` takes the task prompt, a working directory, a model config, a session id, an optional MCP (MCP = Model Context Protocol) server config, a timeout, and optional protocol text, and returns a `SpawnResult` with the process id and log path (`src/bernstein/adapters/base.py:812`). The second returns the human-readable name:

```
    @abstractmethod
    def name(self) -> str:
```

`src/bernstein/adapters/base.py:1068`, `src/bernstein/adapters/base.py:1069`

Useful optional overrides with safe defaults: `stream_signal_parser()` translates one stdout line into a canonical signal (`src/bernstein/adapters/base.py:1188`); `resume()` reattaches to a prior session and returns `None` when unsupported (`src/bernstein/adapters/base.py:1124`); `strategy()` resolves the adapter's declared strategy row (`src/bernstein/adapters/base.py:1259`); `provides` declares provider-string aliases, empty by default (`src/bernstein/adapters/base.py:1251`); `registry_name` namespaces session ids, blank by default (`src/bernstein/adapters/base.py:1242`). Shared behavior inherited for free includes the timeout watchdog, process-group kill, and the fast-exit probe described below.

## How to add a new adapter step-by-step

1. Create `src/bernstein/adapters/<name>.py` with a `CLIAdapter` subclass implementing `spawn()` (`src/bernstein/adapters/base.py:812`) and `name()` (`src/bernstein/adapters/base.py:1069`). The per-folder guide states the rule as one module per tool (`src/bernstein/adapters/AGENTS.md:3`, `src/bernstein/adapters/AGENTS.md:4`).
2. Import the class in `src/bernstein/adapters/registry.py:13` (the import block) and add one line to `_ADAPTERS` (`src/bernstein/adapters/registry.py:86`), e.g. `"myagent": MyAgentAdapter,`. For programmatic use, `register_adapter()` writes the same table (`src/bernstein/adapters/registry.py:348`).
3. Add a strategy row to `STRATEGY_MATRIX` in `src/bernstein/adapters/_contract.py:659`; the conformance harness fails on missing rows. Example row:
```
    "claude": AdapterStrategy(
        resume=ResumeStrategy.FLAG,
        dangerous_mode=DangerousModeStrategy.CLI_FLAG,
        event_channel=EventChannel.STREAM_JSON,
    ),
```
`src/bernstein/adapters/_contract.py:661`, `src/bernstein/adapters/_contract.py:662`, `src/bernstein/adapters/_contract.py:663`, `src/bernstein/adapters/_contract.py:664`
4. Add a YAML contract `tests/contract/contracts/<name>.yaml` naming the binary, required flags, and subcommands; contracts are loaded by `ContractSpec.load()` (`src/bernstein/adapters/_contract.py:116`), and every adapter must have one (`src/bernstein/adapters/AGENTS.md:22`).
5. Optionally declare `provides` aliases (e.g. `provides = ("codex", "openai", "gpt")` in `src/bernstein/adapters/codex.py:321`) so provider-name routing in `src/bernstein/adapters/registry.py:517` finds the adapter, and a `session_id_flag` in the contract YAML when the CLI accepts a caller-supplied session id (`src/bernstein/adapters/_contract.py:88`).

## Capability profiles

Some agents ship as declarations instead of hand-written modules. A profile states the binary, flags, and capability claims; the factory builds a working adapter class from it. Only factory-owned profiles are built (`src/bernstein/adapters/capability_profile.py:1238`):

```
    if profile.implementation is not ProfileImplementation.FACTORY:
```

The first declaration-only agent is Pydantic AI's `clai` (`src/bernstein/adapters/capability_profile.py:1299`, `src/bernstein/adapters/capability_profile.py:1300`, `src/bernstein/adapters/capability_profile.py:1301`, `src/bernstein/adapters/capability_profile.py:1302`):

```
    AdapterCapabilityProfile(
        name="pydantic_ai",
        display_name="Pydantic AI",
        implementation=ProfileImplementation.FACTORY,
```

with provider aliases (`src/bernstein/adapters/capability_profile.py:1320`):

```
        provides=("pydantic_ai", "pydantic-ai", "clai"),
```

The registry merges generated classes into the same table (`src/bernstein/adapters/registry.py:160`):

```
_ADAPTERS.update(profile_built_adapter_classes())
```

so a profile-built adapter resolves through `get_adapter()` like any hand-written one. The factory entry point is `profile_built_adapter_classes()` (`src/bernstein/adapters/capability_profile.py:1507`). Declaration-only profiles for hand-written modules (droid, kimi, opencode, goose) document the capability surface without changing the spawn path (`src/bernstein/adapters/capability_profile.py:1323`).

## Generic fallback adapter

Agents nobody has profiled yet use `GenericAdapter` (`src/bernstein/adapters/generic.py:17`), constructed with a command and flag names; the prompt flag defaults to `--prompt` (`src/bernstein/adapters/generic.py:35`):

```
        prompt_flag: str = "--prompt",
```

Its command shape is fixed (`src/bernstein/adapters/generic.py:65`, `src/bernstein/adapters/generic.py:66`, `src/bernstein/adapters/generic.py:67`, `src/bernstein/adapters/generic.py:68`, `src/bernstein/adapters/generic.py:69`):

```
        cmd = [self._cli_command]
        if self._model_flag is not None:
            cmd.extend([self._model_flag, model_config.model])
        cmd.extend(self._extra_args)
        cmd.extend([self._prompt_flag, prompt])
```

`get_adapter()` handles `"generic"` before the table lookup (`src/bernstein/adapters/registry.py:266`):

```
    if cli_name == "generic":
```

returning a default instance (`src/bernstein/adapters/registry.py:269`):

```
        instance = GenericAdapter(cli_command="generic-cli", display_name="Generic CLI")
```

## Entry-point/plugin discovery

Third parties ship adapters as Python packages without editing Bernstein. The loader runs once on first use (`src/bernstein/adapters/registry.py:207`):

```
def _load_entrypoint_adapters() -> None:
```

and reads the `bernstein.adapters` group (`src/bernstein/adapters/registry.py:216`):

```
    for ep in entry_points(group="bernstein.adapters"):
```

Only values that are `CLIAdapter` subclasses or instances are accepted (`src/bernstein/adapters/registry.py:220`):

```
            if (inspect.isclass(loaded) and issubclass(loaded, CLIAdapter)) or isinstance(loaded, CLIAdapter):
```

and registered under the entry-point name (`src/bernstein/adapters/registry.py:221`):

```
                _ADAPTERS[name] = loaded
```

The group itself is declared for packagers in `pyproject.toml:351`:

```
[project.entry-points."bernstein.adapters"]
```

with usage (`bernstein run --cli myagent`) documented in the comment lines below it.

## Count of shipped adapters

The `_ADAPTERS` literal holds 52 keys (51 agent adapters plus `mock`, with `gemini`/`antigravity` sharing one class), and the `pydantic_ai` profile-built class merges in at `src/bernstein/adapters/registry.py:160`, giving 53 resolvable names. The directory holds 98 `.py` files in total (`ls src/bernstein/adapters/*.py | wc -l` = 98), most of which are helpers (stream parsers, MCP loaders, conformance, admission) rather than adapters; the folder guide describes the layout as one adapter per CLI with 40+ tools covered (`src/bernstein/adapters/AGENTS.md:3`).

## Exit-code/stream-parser handling

All adapters share the fast-exit probe defined on the base class (`src/bernstein/adapters/base.py:983`):

```
    def _probe_fast_exit(
```

It waits a few seconds after spawn; an early non-zero exit becomes a typed error instead of a live session. Rate-limit output raises `RateLimitError` (`src/bernstein/adapters/base.py:1032`):

```
            raise RateLimitError(f"{provider_name} rate-limited during startup: {tail_text}")
```

and anything else raises `SpawnError` (`src/bernstein/adapters/base.py:1033`):

```
        raise SpawnError(f"{provider_name} exited early with code {exit_code}: {tail_text}")
```

Each concrete adapter calls it after `Popen`: codex (`src/bernstein/adapters/codex.py:500`):

```
        self._probe_fast_exit(proc, log_path, provider_name="codex")
```

gemini (`src/bernstein/adapters/gemini.py:303`):

```
        self._probe_fast_exit(proc, log_path, provider_name=binary)
```

Command shapes differ per CLI. Claude builds a `claude` argv with stream-json output (`src/bernstein/adapters/claude.py:477`, `src/bernstein/adapters/claude.py:478`, `src/bernstein/adapters/claude.py:487`, `src/bernstein/adapters/claude.py:488`) and passes the prompt with `-p` (`src/bernstein/adapters/claude.py:532`):

```
        cmd.extend(["-p", prompt])
```

Codex runs `codex exec` with `--json` (`src/bernstein/adapters/codex.py:440`, `src/bernstein/adapters/codex.py:441`, `src/bernstein/adapters/codex.py:442`, `src/bernstein/adapters/codex.py:446`). Gemini passes `-p <prompt> -m <model> --output-format json --yolo` (`src/bernstein/adapters/gemini.py:251`, `src/bernstein/adapters/gemini.py:252`, `src/bernstein/adapters/gemini.py:253`, `src/bernstein/adapters/gemini.py:257`, `src/bernstein/adapters/gemini.py:258`, `src/bernstein/adapters/gemini.py:259`). System-prompt delivery also differs: Claude has a separate `--append-system-prompt` channel (`src/bernstein/adapters/claude.py:530`), while codex and gemini graft the addendum onto the prompt (`src/bernstein/adapters/codex.py:470`, `src/bernstein/adapters/gemini.py:239`).

Output parsing is per-CLI: `ClaudeStreamParser` consumes stream-json lines (`src/bernstein/adapters/claude_stream_parser.py:123`, `src/bernstein/adapters/claude_stream_parser.py:168`), Claude exit codes map to retry/abort decisions via `interpret_exit_code()` (`src/bernstein/adapters/claude_exit_codes.py:102`), and Goose has its own parser in `parse_goose_stream()` (`src/bernstein/adapters/goose_stream_parser.py:85`). Adapters without a native protocol use the default text-signal parser, which delegates to the canonical `BERNSTEIN:<KIND>` grammar (`src/bernstein/adapters/base.py:1215`, `src/bernstein/adapters/base.py:1217`).

**Covers:** src/bernstein/adapters/registry.py, src/bernstein/adapters/base.py, src/bernstein/adapters/_contract.py, src/bernstein/adapters/capability_profile.py, src/bernstein/adapters/generic.py, src/bernstein/adapters/claude.py, src/bernstein/adapters/codex.py, src/bernstein/adapters/gemini.py, src/bernstein/adapters/AGENTS.md, src/bernstein/adapters/claude_exit_codes.py, src/bernstein/adapters/claude_stream_parser.py, src/bernstein/adapters/goose_stream_parser.py, pyproject.toml
