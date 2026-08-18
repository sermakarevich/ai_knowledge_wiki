> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Design Principles

**In one sentence:** The paper argues that fragmented agent frameworks force developers to relearn programming-model concepts Python already has, so NOOA models an agent as a plain Python object (methods as actions, fields as state, docstrings as prompts, type annotations as contracts) and derives five design principles (P1-P5) that cash out into six model-facing interface capabilities — Typed I/O, Pass by reference, Code as action, Loop engineering, Object state, and Harness APIs — which the paper claims to be the first to combine on a single surface.

## Key points

- Existing agent development kits scatter agent logic across prompt templates, schemas, callbacks, configuration files, and orchestration code, forcing developers to relearn abstractions (typed interfaces, scoping, control flow, async execution, object state) that already exist in ordinary programming languages — wasteful because those abstractions are both familiar to developers and well-represented in the data LLMs were trained on.
- NOOA takes explicit inspiration from PyTorch's pairing of a powerful runtime with a simple Python programming model: where a mature Python abstraction already exists, NOOA uses it directly, and introduces new Pythonic APIs only for agent-specific concepts with no standard equivalent (context construction, event history, model-visible state) — yielding a "dual benefit" of no learning curve for developers and immediate agent readiness.
- The central move is "an agent is a Python object": methods are the actions the model can take, fields are its state, docstrings are its prompts, and type annotations are contracts; a method with an ellipsis (`...`) body is completed at runtime by an LLM-driven agentic loop, while a normal body stays deterministic Python, so both share one calling convention and agent behavior can be tested, traced, refactored, and improved like ordinary software.
- The paper frames three contributions: (1) the agent-as-a-Python-object programming model and its design principles, (2) six model-facing ideas it claims to be first to combine on one surface — after surveying fourteen other frameworks converging on them individually and partially — and (3) empirical demonstration via targeted capability tests plus results on SWE-bench Verified, Terminal-Bench 2.0, and ARC-AGI-3, where the interface compresses a multi-agent world-model system into a single agent with a one-page skill while advancing the benchmark's score-cost Pareto frontier.
- The worked `SupportAgent` example (Figure 1) puts a real-bodied deterministic method (`is_refund_eligible`), a single-shot agentic method using `PredictStrategy` (`classify`), and an iterative agentic method using `CodeActStrategy` (`triage`) on one class; `triage` takes a live `Order` object and an image passed by reference rather than serialized into the prompt, and its `Ticket` return value is validated by the runtime before the call returns.
- Five design principles map to concrete capabilities: P1 (reuse Python abstractions) yields Loop engineering and Object state; P2 (reframe agentic loops as method calls) yields Typed I/O and Pass by reference; P4 (unlock the model's existing Python knowledge) yields Code as action; P5 (expose the harness as explicit APIs) yields Harness APIs. P3 (move deterministic work out of the agentic loop) is the odd one out — it names no capability of its own, instead supplying the organizing rule (the real-body-vs-ellipsis-body split) that lets the other five compose cleanly on a single class.
- The five principles cash out into exactly six named model-facing capabilities — Typed I/O, Pass by reference, Code as action, Loop engineering (elsewhere "programmable loop engineering"), Object state (the abstract's "explicit object state"), and Harness APIs (the abstract's "model-callable harness APIs for context and events") — which later serve as the columns scoring NOOA against fourteen other frameworks in Sec 5 and as the categories for Sec 4's targeted capability tests.

---

This page covers Section 1 (Introduction) and Section 2 (Design Principles) of the NOOA paper: the problem the authors observe in existing agent development kits, the core pitch — "an agent is a Python object" — illustrated by the paper's own `SupportAgent` example (Figure 1), and the five design principles (P1-P5) that the rest of the framework is built to satisfy. Each principle is tied by the paper to one or more of six named model-facing interface capabilities, which recur throughout the rest of the paper (and this wiki) as the vocabulary for comparing NOOA to other frameworks.

## The Problem: Fragmented Agent Development

The authors' starting observation is that agent development has proliferated into many agent development kits (ADKs), each introducing its own developer-facing and model-facing abstractions. The recurring failure mode they identify:

- Agent source code ends up **split across prompt templates, schemas, callbacks, configuration files, and orchestration code** — useful primitives (tools, memory, workflows, handoffs, traces, code execution) exist, but not as one coherent surface.
- Consequently, **learning a new agent framework often means learning a new programming model** for capabilities that already have mature equivalents in ordinary programming languages: typed interfaces, variable scoping, control flow, asynchronous execution, and object state.
- This duplication is wasteful twice over: these abstractions are already familiar to human developers, *and* they are broadly represented in the data LLMs were trained on — so reinventing them as a bespoke DSL throws away both kinds of familiarity.

**Inspiration: PyTorch.** NOOA (NVIDIA Object-Oriented Agents, also read "NVIDIA double-O Agents") takes explicit inspiration from PyTorch, which the authors credit with showing that a powerful runtime can still present users with a simple Python programming model. NOOA applies the same move to agents: **where Python already has the right abstraction, NOOA uses it directly**, rather than introducing new domain-specific concepts. Agent actions, helper logic, and harness extension points are written as ordinary Python — familiar to developers, close to the distribution of code LLMs were trained on, and therefore directly understandable by coding agents themselves. Only where agent-specific concepts have no standard Python equivalent — context construction, event history, model-visible state — does NOOA introduce new, deliberately simple Pythonic APIs.

This yields what the paper calls a **dual benefit**: it eliminates the learning curve for human developers, and it ensures immediate agent readiness (models already "know" ordinary Python).

## The Core Idea: Agent-as-a-Python-Object

The paper's central move, stated directly: **an agent is a Python object**.

- Its **methods** are the actions the model can take.
- Its **fields** are its state.
- Its **docstrings** are its prompts.
- Its **type annotations** are contracts.

A method whose body is literally `...` (an ellipsis) is completed at runtime by an LLM-driven agent loop — it becomes an *agentic method*. A method with a normal body remains standard deterministic Python. Because both kinds of methods live on the same class with the same calling convention, **developers and agents share the same interface**, and agent behavior can be tested, traced, refactored, and improved just like any other software.

### Three Contributions

The paper frames its contribution in three parts:

1. **The agent-as-a-Python-object programming model** and the design principles behind it (this page's subject). Where Python already has an abstraction, NOOA adopts it: agents are classes, capabilities are methods, type annotations are contracts, asynchronous work is `asyncio`, tools and orchestration are normal Python code. Agent-specific capabilities — context, events, state rendering, long-term memory, and validated LLM loops — are exposed through simple Pythonic APIs.
2. **Six model-facing ideas**, which the paper claims NOOA is, to its authors' knowledge, the first to combine on a single surface (see below). The paper surveys fourteen other agent frameworks and harnesses and finds the community already converging on several of these ideas individually, often as experimental or partial features.
3. **Empirical demonstration** that current models use this interface effectively — targeted capability tests plus results on SWE-bench Verified and Terminal-Bench 2.0, and on the ARC-AGI-3 interactive-reasoning benchmark, where the interface compresses a multi-agent world-model system into a single agent with a one-page skill while advancing the benchmark's score-cost Pareto frontier.

### The `SupportAgent` Example (Figure 1)

The paper illustrates the whole idea with a single worked example: a complete agent as one Python class, combining object state, deterministic code, and two agentic methods — a single-shot `Predict` method and an iterative `CodeAct` method. Note: "Figure 1" in the paper *is* this code listing (not a diagram) — reproduced verbatim below.

```python
from nooa import Agent

TicketKind = Literal["refund", "damaged", "other"]

# Return type: validated by the runtime before triage() returns.
# Descriptions and constraints are model-visible.
class Ticket(BaseModel):
   kind: TicketKind
   priority: int = Field(ge=1, le=5, description="Urgency from 1 (low) to 5 (high).")
   summary: str = Field(description="Customer-visible summary of the issue.")

# The Agent is a Python object.
class SupportAgent(Agent):
   """You are a support agent for a customer service system."""

   # Object state: model-visible, passed by reference.
   order_db: OrderDB

   # Real body: ordinary Python. Deterministic, testable, callable by the model.
   def is_refund_eligible(self, order: Order) -> bool:
       """Return whether an order is eligible for a refund."""
       return order.delivered and order.days_since_delivery <= 30

   # "..." body: an agentic method. Predict makes a single typed LLM call.
   @strategy(PredictStrategy())
   async def classify(self, message: str) -> TicketKind:
       """Classify the customer message into the best ticket kind."""
       ...

   # The default strategy, CodeAct, runs a loop in which the model writes
   # Python: it can inspect order, call is_refund_eligible() and classify(),
   # and must return a Ticket. Inputs are live objects, not serialized text.
   @strategy(CodeActStrategy())
   async def triage(self, message: str, photo: Image | None, order: Order | None) -> Ticket:
       """Triage a customer message and create a support ticket."""
       ...
```

*Figure 1 | Implementation of a simple Agent in NOOA.*

**Reading the example.** The class is simultaneously source code, prompt surface, type contract, tool interface, and state boundary:

- `is_refund_eligible` has a real body: it executes as ordinary, deterministic Python.
- `classify` and `triage` have an ellipsis (`...`) body: the harness runs each as an LLM-driven loop, using a **strategy** (`PredictStrategy` for a single typed call, `CodeActStrategy` for an iterative loop where the model writes Python).
- The method declaration itself specifies the loop: the **signature** gives the model structured inputs and an output-validation contract; the **docstring** becomes the prompt; methods on `self` and imported libraries become callable tools.
- Inputs are not limited to text: `triage` receives an image and a live `Order` object, **passed by reference rather than serialized into the prompt**.

The authors summarize the payoff as bringing prompt engineering back into software engineering: because agent behavior lives in ordinary class/method form, it can be tested, traced, refactored, versioned, and optimized using standard software-engineering practice.

### Roadmap of the Paper

The introduction closes by previewing the rest of the paper's structure: Sec 2 presents the design principles (below); Sec 3 shows how they are realized in the programming model and harness; Sec 4 tests whether current models can use the interface, with capability tests and results on SWE-bench Verified, Terminal-Bench 2.0, and ARC-AGI-3; Sec 5 compares fourteen other frameworks and harnesses against the six interface capabilities; Sec 6 situates the capabilities in the broader literature; Sec 7 discusses limitations and future work. The programming-model and harness realization of these principles is elaborated further in pages such as [[03-execution-validation-and-memory|Execution, Validation, and Memory]]; the cross-framework comparison against the six capabilities below is covered in the framework-survey page later in this wiki.

## Design Principles (P1-P5)

Section 2 states that five principles guided NOOA's design. Each principle materializes as one or more concrete **interface capabilities**. The paper marks each principle with a square (▪) and calls out the corresponding capability name(s) — reproduced exactly below.

### P1. Reuse Python Abstractions

> If a mature Python abstraction already exists, adopt it rather than introducing a domain-specific language (DSL).

In NOOA: classes define agents, methods define capabilities, fields hold explicit, model-visible durable state, type annotations define contracts, `asyncio` expresses concurrency, exceptions signal failures, and control flow is ordinary Python — available to developers and agents alike.

- **Loop engineering.** Control flow for single- and multi-agent orchestration is ordinary Python.
- **Object state.** Durable state is stored on the agent object, rather than only in conversation history.

### P2. Reframe Agentic Loops as Method Calls

> The application sees an agentic loop as a normal Python method call with typed input/output, not an unstructured text exchange.

Arguments are passed by reference as live Python objects, while the harness renders bounded previews and context to the agent, injects arguments and object state into the loop, and validates return values before returning to the caller.

- **Typed I/O.** Agentic methods have typed inputs and typed return values.
- **Pass by reference.** The model operates on live Python objects by reference.

### P3. Move Deterministic Work Out of the Agentic Loop

> LLMs are useful for semantic judgment, synthesis, and open-ended tasks. Exact rules, arithmetic, parsing, and state transitions belong in deterministic methods.

The boundary between the two kinds of work is local and visible directly in the code: a real method body signals deterministic work, an ellipsis (`...`) body signals an agentic loop. Unlike the other four principles, the source text does not attach a distinct named capability callout to P3 — it states the design commitment (push non-semantic work into ordinary methods) that the `...`-vs-real-body distinction in the `SupportAgent` example already demonstrates, rather than introducing a further interface feature of its own.

### P4. Unlock the Model's Existing Python Knowledge

> LLMs already know how to write Python and use popular Python libraries. By letting models write normal Python code instead of tool calls, NOOA draws on that knowledge.

CodeAct code can use ordinary loops and conditionals, `asyncio` for concurrency, database clients for queries, plotting libraries for visualization, and ordinary imports for extension — without bespoke prompting, reading documentation, or learning a new DSL. This is framed as making NOOA exceptionally easy to use while maximizing agent readiness: the library is meant to be as intuitive for autonomous coding agents to build with as it is for human developers.

- **Code as action.** The model acts by writing Python code, control flow and method calls directly.

### P5. Expose the Harness as Explicit APIs

> Agent-specific concepts — structured context, context rendering, and event history — are exposed as Python APIs to developers and the model.

Where possible, these interfaces mirror built-in types or existing libraries so they remain familiar and obvious. The Agent has access to its own context and can manage it via Pythonic primitives.

- **Harness APIs.** Harness and Context are exposed through explicit APIs both to the user and to the agent.

## The Six Model-Facing Capabilities

Collecting the callouts above, the five principles cash out into exactly the **six model-facing ideas** the abstract claims NOOA is first to combine on one surface:

| Capability (paper's exact name) | Originating principle |
|---|---|
| **Typed I/O** | P2 — Reframe agentic loops as method calls |
| **Pass by reference** | P2 — Reframe agentic loops as method calls |
| **Code as action** | P4 — Unlock the model's existing Python knowledge |
| **Loop engineering** (the paper elsewhere calls the fuller idea "programmable loop engineering") | P1 — Reuse Python abstractions |
| **Object state** (the abstract's "explicit object state") | P1 — Reuse Python abstractions |
| **Harness APIs** (the abstract's "model-callable harness APIs for context and events") | P5 — Expose the harness as explicit APIs |

P3 (moving deterministic work out of the agentic loop) is the odd one out: it names no separate capability of its own — it is the *organizing rule* that makes the `...`-vs-real-body split legible in code, which is what lets the other five capabilities compose cleanly on a single class.

These same six capabilities are the columns used later in the paper (Sec 5) to score NOOA against fourteen other agent frameworks and harnesses, and are the categories used in Sec 4's targeted capability tests.

---

**Covers:** Section 1 (Introduction), Section 2 (Design Principles)
