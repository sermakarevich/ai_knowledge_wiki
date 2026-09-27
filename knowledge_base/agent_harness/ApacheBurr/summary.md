# Apache Burr: Build Reliable AI Agents and Applications

**Source:** [Apache Burr (HN Discussion)](https://news.ycombinator.com/item?id=48477400) | [burr.apache.org](https://burr.apache.org/)

---

## Human Readable TL;DR

Imagine you're building a robot assistant that reads emails, decides what to do, and sends replies. If it crashes halfway through, you have no idea what it did -- and debugging it is like trying to find a needle in a haystack. Apache Burr is like giving that robot a detailed logbook and a "pause and check with me" button: every step is recorded, the state is saved so it can resume after a crash, and you can watch it work in real-time through a dashboard.

## TL;DR

Apache Burr is a Python framework for building AI agents and pipelines using an action-based state machine model. It distinguishes itself from alternatives like LangGraph primarily through first-class observability (built-in tracing UI), state persistence (resume from checkpoints), and human-in-the-loop support -- all without imposing DSLs or complex abstractions. Applications are composed from plain Python functions decorated with `@action` that declare their state reads/writes, wired together via an `ApplicationBuilder`.

---

## Problem & Motivation

Building AI agents (chatbots, multi-step pipelines, multi-agent systems) is conceptually simple -- context management, LLM calls, tool execution -- but production use surfaces hard problems: lack of observability when something goes wrong, no easy way to replay or debug a specific run, and inability to pause execution for human review. Most agent frameworks either over-abstract and hide logic behind opaque layers (LangChain) or leave observability as an afterthought. Burr targets this gap: minimal abstraction over agent logic, but rich built-in infrastructure for debugging and reliability.

---

## Main Original Ideas

1. **Action-as-state-machine primitives** -- Each step in an agent is a pure Python function annotated with `@action(reads=[...], writes=[...])`, declaring what state it consumes and produces. The framework enforces this contract, enabling automatic state tracking without hidden side effects.

2. **Immutable State object** -- A central `State` object flows through the pipeline; each action returns a new state rather than mutating in place. This enables full replayability and deterministic debugging of any historical run.

3. **Built-in observability UI** -- Burr ships a local tracking server and web UI out of the box (`.with_tracker("local")`). No external APM required for development; each action's inputs/outputs and state transitions are stored and queryable.

4. **Human-in-the-loop as a first-class primitive** -- Execution can halt at any designated action to await external input or approval before continuing, without custom polling logic.

5. **BYO everything else** -- Burr deliberately avoids opinions on LLM client, prompt format, or tooling. It wraps whatever Python code you write, reducing lock-in.

---

## Key Findings

From the HN discussion (219 points, 107 comments):

| Theme | Signal |
|-------|--------|
| Framework necessity debate | Strong skepticism ("agents are 50 lines of code") but acknowledgment that observability/persistence justify frameworks |
| Observability as differentiator | Most upvoted counter-argument: hand-rolled agents skip tracing until production breaks |
| LangGraph comparison | Burr seen as lighter, more transparent; LangGraph as more opinionated/enterprise |
| Builder pattern criticism | `ApplicationBuilder` chaining viewed as un-Pythonic by some; co-creator defends it as explicit |
| Website backlash | Landing page criticized for JS-heavy animated UI ("performative"), seen as substance vs. style mismatch |

- Reported migration story: "moving from LangChain to Burr was a game-changer" with fast onboarding
- Alternatives cited: LangGraph, Strands Agents SDK, Pi, hand-rolled solutions
- No consensus winner; choice often comes down to whether observability infrastructure is worth the dependency

---

## Suggestions & Future Directions

1. Documentation and examples remain the primary onboarding friction -- co-creator acknowledged this is a work in progress.
2. Distributed/remote execution (beyond single-process) is a natural evolution for multi-agent orchestration.
3. Tighter integration with evaluation frameworks (evals, A/B testing of agent versions) was cited as a gap users want filled.
4. The builder pattern API could be revisited in favor of more idiomatic Python (dataclasses/keyword-arg config).
5. Apache incubation status raises long-term sustainability questions -- community governance is still forming.

---

## Technical Snapshot

```python
from burr.core import action, State, ApplicationBuilder

@action(reads=["messages"], writes=["messages"])
def chat(state: State, llm_client) -> State:
    response = llm_client.chat(state["messages"])
    return state.update(messages=[*state["messages"], response])

app = (
    ApplicationBuilder()
    .with_actions(chat)
    .with_transitions(("chat", "chat"))
    .with_state(messages=[])
    .with_tracker("local")   # enables observability UI
    .build()
)
```

Integrations: OpenAI, Anthropic, LangChain, Hamilton, Streamlit, FastAPI, Pydantic, PostgreSQL.

---

## Authors & Institutions

**Maintainers:** elijahbenizzy (co-creator, active in HN discussion) and contributors via Apache Software Foundation incubator. Project originally from DAGWorks Inc.
