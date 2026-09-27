> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Harness Plugin Layer (multi-provider AI tools)

**In one sentence:** A registry plus a small tool protocol abstracts every coding agent behind one launch pipeline, so built-ins (Claude, Pi, Droid, OpenCode, ClawCore) and config-registered custom tools are launched identically from `owt new --ai-tool <name>`.

## Key points

- The contract is `AIToolProtocol` (`core/tool_protocol.py:14-99`): `name/binary/supports_hooks/supports_headless/supports_plan_mode/task_via_args/install_hint` plus `get_command/is_installed/get_known_paths/install_hooks`.
- Built-ins are bespoke classes in `core/tool_registry.py`: `claude` (:96-141), `droid` (:144-180), `pi` (:183-232), `opencode` (:235-271), one-shot `clawcore` (:325-352, `task_via_args=True`), plus plain `CustomTool` entries for codex/gemini/aider/amp/kilo-code (:277-283, registered :362-369).
- Custom tools need no code changes: `[tools.<name>]` tables in config (`binary`, `command_template`, `prompt_flag`, capability flags) are registered before validation in `load_config` (`config.py:322-326`), so validators accept the new names.
- One-shot argv tools substitute shell-quoted `{{task}}`/`{{worktree}}` into `command_template` (`core/tool_registry.py:67-74`); paste-based REPL tools receive the prompt through the multiplexer instead.
- Auto-detection priority is `claude > pi > droid > opencode` (`core/agent_detector.py:14`); one installed tool is auto-picked, several produce an interactive numbered picker (`commands/worktree/_shared.py:24-41`).
- `--workflow` is plan-first framing, not a separate engine: the task classifier (`core/prompt_builder.py:34-43`) picks a protocol preamble that is prepended to the prompt (`commands/worktree/new.py:162-170`).
- Headless mode shells out with stdin piping and requires `supports_headless` (only Claude and Pi); it is incompatible with `--herdr/--workflow/--in-place`.

---

## Built-ins and their launch shapes

Each built-in class implements `get_command()` returning the exact argv (`core/tool_registry.py`):

| Tool | Defined | Launch shape |
|---|---|---|
| `claude` | :96-141 | `<bin> --permission-mode plan` in plan mode else `<bin> --dangerously-skip-permissions`, plus `-p` with a prompt (:115-125); hooks + headless supported |
| `droid` | :144-180 | `<bin> --skip-permissions-unsafe` (:163-164); hooks yes, headless no |
| `pi` | :183-232 | `<bin>` + `-p` with a prompt (:207-213); headless yes, hooks no |
| `opencode` | :235-271 | bare `<bin>` (:254); hooks/headless no |
| `clawcore` | :325-352 | `{binary} run {{task}} {{worktree}} --json`, `task_via_args=True` (:341-342); headless yes |
| extras | :277-283 | plain `CustomTool("{binary}")`: codex, gemini-cli, aider, amp, kilo-code; registered :362-369 |

Each class carries known-path fallbacks (Claude :130-131, Droid :169-170, Pi :218-224, OpenCode :259-263, ClawCore :343-347) and an `install_hint` (e.g. :105) shown when the binary is missing.

```python
# core/tool_registry.py:107-125 — Claude plan/headless split
def get_command(self, *, executable_path=None, plan_mode=False, prompt=None, worktree=None) -> str:
    binary = shlex.quote(executable_path) if executable_path else self.binary
    parts = [binary]
    if plan_mode:
        parts.append("--permission-mode plan")
    else:
        parts.append("--dangerously-skip-permissions")
    if prompt:
        parts.append("-p")
    return " ".join(parts)
```

## The plugin contract and custom tools

`AIToolProtocol` (`core/tool_protocol.py:14-99`, `runtime_checkable` at :13) requires the capability properties and `get_command(executable_path, plan_mode, prompt, worktree)` (:64-78), `is_installed` (:80), `get_known_paths` (:84), `install_hooks` (:88-99). `CustomTool` (`core/tool_registry.py:39-93`) implements the protocol generically from `command_template + prompt_flag` (:58-78); built-ins are bespoke subclasses only where plan/hook logic differs. `ToolRegistry` (:286-322) offers `register/get/require/list_names/list_installed/supports_hooks`; the singleton plus `_register_builtins` live at :355-400.

Custom tools come from `Config.tools: dict[str, dict]` (`config.py:175`); the `[tools.<name>]` schema (`binary`, `command_template="{binary}"`, `prompt_flag`, `supports_hooks/headless/plan_mode`, `task_via_args`, `known_paths`) is documented in `docs/configuration.md:130-154`. `register_custom_tools()` (`core/tool_registry.py:372-392`) builds `CustomTool`s while reserving `{"claude","opencode","droid","pi"}` (:374), and it runs before Pydantic validation in `load_config` (`config.py:322-326`) so `WorktreeTemplate.ai_tool` (:69-81) and `TmuxConfig.ai_tool` (:107-116) validators accept custom names.

```python
# core/tool_registry.py:58-78 — generic plugin command builder
def get_command(self, *, executable_path=None, plan_mode=False, prompt=None, worktree=None) -> str:
    binary = shlex.quote(executable_path) if executable_path else self.binary
    if self.task_via_args:
        cmd = self.command_template.replace("{binary}", binary)
        cmd = cmd.replace("{{task}}", shlex.quote(prompt or ""))
        cmd = cmd.replace("{{worktree}}", shlex.quote(worktree or "."))
        return cmd
```

Note: `core/tool_search.py` is unrelated to harnesses — it is deferred in-agent tool-schema loading (`ToolSearchProvider:61`, `DeferredToolLoader:127`, budget cap at :28).

## Detection, prompt building, launch flow

Auto-detection: `_PRIORITY = ("claude","pi","droid","opencode")` (`core/agent_detector.py:14`); `detect_installed_agents()` sorts `list_installed()` by it (:24-27). `_resolve_ai_tool` (`commands/worktree/_shared.py:24-41`): an explicit name passes through; zero installed errors; one auto-picks; several show an interactive numbered picker (:37-41).

Prompt flow: `prompt = task_description` (`commands/worktree/new.py:158`) with template instructions prepended (:159-160). With `--workflow`, `get_protocol_for_task(task)` (`new.py:165-169` → `core/prompt_builder.py:210-213`) classifies via keyword-first-match defaulting to FEATURE (`classify_task`, :34-43) and prepends the matching protocol from `_PROTOCOLS` (:123-207, plus `COMMIT_SAFETY` :104 and `TURN_EFFICIENCY` :113), marking the display task `⟳ ...`.

```python
# commands/worktree/new.py:162-170 — workflow framing
display_task = task_description or None
if workflow and task_description:
    from open_orchestrator.core.prompt_builder import get_protocol_for_task
    protocol = get_protocol_for_task(task_description)
    prompt = f"{protocol}\n\n{prompt}" if prompt else protocol
    display_task = f"⟳ {task_description}"
```

`owt new` flags are defined at `commands/worktree/new.py:19-42`; `workflow → plan_mode=True` (:84-85); branch via `generate_branch_name` (`commands/worktree/_shared.py:44-68` → `core/branch_namer.py:128-195`); template overlay (:131-141); tool resolution plus guards including "workflow requires `supports_plan_mode`" (:143-156); then `LaunchRequest(...plan_mode, prompt, display_task="⟳ ...")` (:184-195) → `AgentLauncher.launch` (`core/agent_launcher.py:133-230`: resolve tool :138, worktree :151, env :155, backend session :185-208). Delivery skips pasting for `task_via_args` (:209-210); tmux uses `wait_and_paste` (:396), herdr uses `submit_prompt`/`send_text` (:387-389); headless builds `tool.get_command(...prompt, worktree)` (:465-470) with stdin piping, or `DEVNULL` for argv tools (:475-485); herdr+argv is rejected (:177-184). tmux has a non-interactive shortcut `cat <tmpfile> | claude|pi -p` (`core/tmux_manager.py:327-329`). Supporting cast (not harness logic): `core/project_detector.py:80-131` picks the dependency installer; `core/branch_namer.py` only names branches.

**Covers:** `core/agent_launcher.py`, `core/agent_detector.py`, `core/tool_registry.py`, `core/tool_protocol.py`, `core/tool_search.py` (disambiguated), `core/prompt_builder.py`, `core/project_detector.py`, `core/branch_namer.py`, `config.py` (tool sections), `commands/worktree/new.py`, `commands/worktree/_shared.py`, `docs/configuration.md`
