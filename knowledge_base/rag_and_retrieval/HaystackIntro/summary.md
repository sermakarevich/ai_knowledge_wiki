# Introduction to Haystack

**Source:** [Haystack Documentation -- Introduction](https://docs.haystack.deepset.ai/docs/intro)
**Publisher:** deepset GmbH | **Version:** 2.30 | **Date:** 2026-06-19

## Human Readable TL;DR

Haystack is like a set of LEGO bricks for building AI-powered apps. You snap together pre-built pieces -- one that reads your documents, one that searches them, one that talks to an AI -- and chain them into a pipeline that can answer questions, take actions, or search through huge collections of text. You can also give the AI a set of "tools" it can pick from on its own, turning it from a simple question-answerer into an autonomous agent that figures out what steps to take and in what order.

## TL;DR

Haystack is an open-source Python framework by deepset for building production-ready AI agents, RAG (Retrieval-Augmented Generation) pipelines, and multimodal search systems. Its core abstraction is the **Pipeline** -- a directed multigraph of typed **Components** -- which supports branching, loops, and async execution. An **Agent** component wraps the full LLM tool-calling loop with state management, streaming, and MCP server support. The framework integrates natively with OpenAI, Anthropic, Google, and Hugging Face models.

---

## Problem & Motivation

Building LLM-powered applications requires gluing together many heterogeneous pieces: vector stores, embedding models, rerankers, generators, and orchestration logic. Without a framework, each integration is bespoke and hard to test, swap, or scale. Haystack provides a unified component model where every piece exposes the same interface, so pipelines are composable, serializable (YAML), and swappable without rewriting orchestration code. It targets teams that need to move from prototype to production without rebuilding infrastructure.

---

## Main Original Ideas

1. **Component protocol** -- Any class decorated with `@component` and implementing a `run()` method becomes a first-class pipeline node. Inputs and outputs are typed sockets; the pipeline validates connections before execution. This enables mix-and-match between built-in and custom components.

2. **Directed multigraph Pipeline** -- Pipelines are not linear chains but graphs supporting multiple branches (e.g., different file converters in parallel), conditional routing via `ConditionalRouter`, and loops (e.g., generate → validate → retry). `AsyncPipeline` runs independent branches concurrently.

3. **Agent with typed state** -- The `Agent` component manages the full tool-calling loop: LLM decides which tool to invoke, tool executes, result feeds back into context, repeat. A `state_schema` accumulates typed data across invocations. Supports human-in-the-loop review of tool calls before execution.

4. **Layered tool system** -- Tools are composable at multiple levels of abstraction:
   - `@tool` decorator wraps a plain Python function
   - `ComponentTool` wraps any Haystack component
   - `PipelineTool` encapsulates an entire pipeline as a tool
   - `MCPTool` / `MCPToolset` connects to external MCP servers
   - `SearchableToolset` adds keyword-based discovery for large tool catalogs

5. **Serialization and governance** -- Pipelines serialize to YAML via `to_dict()` / `from_dict()`, enabling version control, sharing, and the enterprise platform's testing and governance layer.

---

## Key Findings

| Capability | Detail |
|---|---|
| Installation | `pip install haystack-ai` / `uv add haystack-ai` / `conda install conda-forge::haystack-ai` |
| LLM providers | OpenAI, Anthropic, Google, Hugging Face Transformers (open-source) |
| Pipeline execution | Sync (`Pipeline`) and async (`AsyncPipeline`) |
| Agent features | Streaming, typed state, multi-agent coordination, multimodal (image+text), MCP server exposure via Hayhooks |
| Optional deps | Installed on demand; missing deps raise `ImportError` with `pip install <package>` hint |
| Enterprise | Haystack Enterprise Starter (deployment) + Haystack Enterprise Platform (data, pipelines, testing, governance) |

**Custom component minimum:**

```python
from haystack import component

@component
class WelcomeTextGenerator:
    @component.output_types(welcome_text=str, note=str)
    def run(self, name: str):
        return {
            "welcome_text": f"Hello {name}, welcome to Haystack!".upper(),
            "note": "welcome message is ready",
        }
```

**Pipeline wiring:**

```python
p = Pipeline()
p.add_component("retriever", retriever)
p.add_component("generator", generator)
p.connect("retriever.documents", "generator.documents")
result = p.run({"retriever": {"query": "What is Haystack?"}})
```

---

## Suggestions & Future Directions

1. Multimodal support is an active focus -- agents already accept images alongside text; broader media types are likely next.
2. MCP (Model Context Protocol) integration is first-class, positioning Haystack to plug into the emerging MCP ecosystem for tool and server interoperability.
3. `SearchableToolset` addresses the "too many tools" problem for large agent catalogs; semantic tool routing is an open research direction.
4. Hayhooks exposes Haystack agents as MCP servers, enabling use from external clients (e.g., Claude Desktop, Cursor).
5. Enterprise platform targets governance gaps (testing, data lineage, pipeline versioning) that open-source deployments handle manually.

---

## Authors & Institutions

deepset GmbH (Berlin) -- core maintainers. Open-source community contributors via GitHub.
