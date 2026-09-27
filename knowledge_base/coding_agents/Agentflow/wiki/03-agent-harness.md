> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Agent harnesses: codex, claude, kimi nodes
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

---
## Codex node constructor
`codex()` takes a task id, a prompt, and optional settings (`agentflow/dsl.py:350`):

```python
def codex(*, task_id: str, prompt: str, **kwargs: Any) -> NodeBuilder:
    return _node(AgentKind.CODEX, task_id=task_id, prompt=prompt, **kwargs)
```

## Codex harness command
`CodexAdapter.prepare()` builds the Codex CLI (CLI = Command-Line Interface) call and picks the sandbox from `tools=` (`agentflow/agents/codex.py:67`, `agentflow/agents/codex.py:70`):

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
            "-c",
            'approval_policy="never"',
            "-c",
            "suppress_unstable_features_warning=true",
            "--sandbox",
            sandbox,
        ]
```

## Claude node constructor
`claude()` has the same shape as `codex()` (`agentflow/dsl.py:354`):

```python
def claude(*, task_id: str, prompt: str, **kwargs: Any) -> NodeBuilder:
    return _node(AgentKind.CLAUDE, task_id=task_id, prompt=prompt, **kwargs)
```

## Claude harness command
`ClaudeAdapter.prepare()` builds the Claude CLI call with streaming JSON output and permission bypass (`agentflow/agents/claude.py:37`, `agentflow/agents/claude.py:52`):

```python
class ClaudeAdapter(AgentAdapter):
    def prepare(self, node: NodeSpec, prompt: str, paths: ExecutionPaths) -> PreparedExecution:
        provider = self.provider_config(node.provider, node.agent)
        executable = node.executable or "claude"
        command = [
            executable,
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--verbose",
            "--permission-mode",
            "bypassPermissions",
        ]
```

## Kimi node constructor
`kimi()` has the same shape as the other two (`agentflow/dsl.py:358`):

```python
def kimi(*, task_id: str, prompt: str, **kwargs: Any) -> NodeBuilder:
    return _node(AgentKind.KIMI, task_id=task_id, prompt=prompt, **kwargs)
```

## Kimi harness command
`KimiAdapter.prepare()` builds the Kimi CLI call with print mode, streaming JSON output, and auto-approve (`agentflow/agents/kimi.py:14`, `agentflow/agents/kimi.py:16`):

```python
class KimiAdapter(AgentAdapter):
    def prepare(self, node: NodeSpec, prompt: str, paths: ExecutionPaths) -> PreparedExecution:
        provider = self.provider_config(node.provider, node.agent)
        executable = node.executable or "kimi"
        command = [
            executable,
            "--print",
            "--output-format",
            "stream-json",
            "--yolo",
            "-p",
            prompt,
        ]
```

## How prompts connect nodes
Each adapter receives an already-rendered `prompt: str`, so templating happens before launch; `render_node_prompt()` builds the node context and then renders the template (`agentflow/context.py:212`, `agentflow/context.py:231`).

## Multi-agent debate wiring
The example runs two solvers in parallel, then two critiques that read the other side's output, then one synthesis node that reads all four (`examples/multi_agent_debate.py:5`, `examples/multi_agent_debate.py:29`, `examples/multi_agent_debate.py:41`).

**Covers:** agentflow/agents/*.py, agentflow/context.py, agentflow/scratchboard.py, agentflow/skills.py, examples/multi_agent_debate.py
