> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Cognitive Accumulation Paradigm

### Core Motivation: Why Long-Horizon Agentic Science Is Fundamentally Different

The paper's central claim is that scientific discovery is not a short-horizon reasoning problem -- it is an *ultra-long-horizon* process whose structure is qualitatively distinct from the tasks on which LLMs have so far excelled. The authors define ultra-long-horizon autonomy as:

> "The capacity to sustain strategic coherence and perform iterative correction over extended temporal scales without being overwhelmed by the accumulation of execution details."

This characterisation picks out three properties that jointly distinguish real scientific work from, say, a single coding task or a multi-step math problem:

1. **Delayed feedback.** In chemistry or biology, validation can require "specialized equipment and months of latency." Even in the purely computational substrate of MLE-Bench, the feedback loop is the result of a training run, not an immediate error message. A bad decision made at step 10 may only manifest as a score drop at step 200.

2. **High-dimensional exploration.** The search space is not a small branching tree. A Kaggle competition requires navigating model architectures, data preprocessing choices, augmentation strategies, hyperparameter ranges, ensembling decisions, and submission logistics -- all simultaneously, with partial information.

3. **Hours-to-weeks temporal scale.** The paper notes experimental cycles "spanning days or weeks." MLE-Bench tasks run under a 24-hour budget with tens of thousands of individual interaction steps. The agent's event sequence $\mathcal{E}_t \triangleq \{e_0, e_1, \ldots, e_t\}$ grows rapidly because it includes every tool call, code patch, terminal output, and plan revision.

The failure mode the paper diagnoses is **context saturation**: naively concatenating the most recent events causes the active context to overflow with low-level execution noise -- error tracebacks, metric logs, intermediate code patches -- which crowds out the strategic signal. The agent loses the thread of its own reasoning. It cannot consolidate sparse feedback into coherent long-term guidance.

Critically, the paper frames this not as a capacity problem ("the context window is too small") but as a **structural problem**: the agent lacks a principled way to distinguish information at different levels of abstraction and stability.

---

### The AI-for-AI Framing

The paper situates itself within the paradigm of *AI-for-AI (AI4AI)*:

> "AI systems autonomously drive the advancement of AI itself."

MLE -- Kaggle-style machine learning engineering -- is chosen as the "quintessential challenge" of this paradigm because it offers a purely computational substrate with immediate feedback, allowing experimentation at a pace impossible in physical science. MLE-Bench (75 real-world Kaggle competitions) is used as the benchmark because it:

- Far exceeds simple code generation.
- Requires agents to navigate a "vast, unstructured search space through prolonged trial and error."
- Demands "accumulation of experience across iterations, rather than by single-step correctness."

The paper's explicit ambition is that methods developed here should generalise: MLE is treated as a "specific instance of ultra-long-horizon inquiry," and the goal is "generalizable methods that enable agents to evolve their context and sustain strategic focus over the tens of hours required for genuine breakthrough."

---

### The Three-Stage Evolution: Experience → Knowledge → Wisdom

The paper's most important theoretical contribution is the articulation of a three-level cognitive hierarchy. The authors argue that ultra-long-horizon autonomy is:

> "Not a linear aggregation of historical context, but an evolutionary process of refinement, stabilization, and reuse."

The three stages are:

#### Stage 1 -- Raw Experience

> "From a cognitive perspective, agents generate large amounts of raw *experience*."

Experience is the unfiltered stream of execution: research plan proposals, code patches, terminal outputs, error messages, metric logs. It is high-fidelity, high-volume, and short-lived in its utility. In the formal model, the evolving experience cache $\mathcal{L}_1$ at time $t \in [t_{p-1}, t_p)$ is defined as:

$$\mathcal{L}_1(t) = \mathcal{E}_{t_0-1} \cup \mathcal{P}_{p-1} \cup \mathcal{E}_{t_{p-1}+1:t}$$

where $\mathcal{E}_{t_0-1}$ contains all events before the initial code and its results, $\mathcal{P}_{p-1}$ stores all high-level plan proposals generated at phase boundaries, and $\mathcal{E}_{t_{p-1}+1:t}$ records the raw execution traces of the currently active plan. Experience acts as the agent's *working memory* -- it enables precise debugging and execution-aware decision-making, but it cannot be retained indefinitely.

#### Stage 2 -- Distilled Knowledge

> "Only a small fraction of these [experiences], once repeatedly validated, are distilled into reusable *knowledge*."

Knowledge is stabilised, intermediate cognition extracted from completed exploration phases. The paper's concrete examples: "feature X is harmful," "CV leakage observed under split Y," "condensed progress summaries that preserve decision rationale." It removes verbose execution details while preserving strategic signal.

Formally, define $\kappa_{i:j}$ as the compact knowledge summary from the raw event segment $\mathcal{E}_{i:j}$, obtained via a phase-level context promotion operator $P_1$. The refined knowledge cache at time $t \in [t_{p-1}, t_p)$ is:

$$\mathcal{L}_2(t) = \{\kappa_{t_{r-1}+1:t_{r-1}}\}_{r=1}^{p-1}$$

This layer serves as the agent's *mid-term strategic memory*, maintaining coherence across iterative trial-and-error. It allows the agent to revisit validated decisions and insights without carrying verbose execution logs, "thereby stabilizing strategic reasoning across tens of hours."

#### Stage 3 -- Transferable Wisdom

> "When such knowledge is further abstracted and remains stable across tasks, it forms higher-level *wisdom*."

Wisdom is task-agnostic and transferable. The paper's examples: "robust model templates, reusable preprocessing pipelines, and stable hyperparameter priors." It is the agent's *long-term memory* and enables warm-starting on new tasks.

The prior wisdom cache is stored as embedding-value pairs:

$$\mathcal{L}_3 \triangleq \{(\mathbf{h}_n, w_n)\}_{n=1}^N$$

where $N$ is the number of stored past tasks, $\mathbf{h}_n = E(d_n)$ is the semantic embedding of the compact task descriptor $d_n$ (a high-level textual summary generated by an LLM), and $w_n$ is the corresponding distilled task-level wisdom text produced by the task-level promotion operator $P_2$:

$$w_\tau \triangleq P_2(d_\tau, \mathcal{L}_1(t_{\max}), \mathcal{L}_2(t_{\max}), h(\mathcal{E}_{t_{\max}}))$$

$\mathcal{L}_3$ is persistent across tasks and updated only at task completion. It provides strong priors for the bootstrap phase: given a new task descriptor $d_\tau$ with embedding $\mathbf{q} = E(d_\tau)$, the agent retrieves relevant prior wisdom via a threshold-based prefetching operator:

$$\Omega_\tau = \{w_n \mid (\mathbf{h}_n, w_n) \in \mathcal{L}_3, \cos(\mathbf{q}, \mathbf{h}_n) > \delta\}$$

where $\delta$ is a similarity threshold and $\cos(\cdot, \cdot)$ denotes cosine similarity.

#### The Three Roles in a Single Sentence

The paper summarises the functional division of labour cleanly:

> "Short-term experience supports immediate decisions; relatively stable knowledge preserves strategic consistency throughout prolonged exploration; and further abstracted, consolidated wisdom enables transfer and reuse across tasks."

---

### Why "Bigger Context Window" Is the Wrong Framing

The paper explicitly rejects the framing of long-horizon autonomy as a context-length problem:

> "Cognitive accumulation therefore relies not on retaining ever more context, but on enabling context to undergo structural differentiation over time."

The argument has two layers.

**Layer 1 -- Scaling limits of static windows.** Even with an arbitrarily large context, naively concatenating all events "causes context saturation, degrading strategic coherence and preventing accumulation of reusable expertise over tens of hours." More tokens does not solve the signal-to-noise problem; it potentially makes it worse by increasing the volume of low-level noise the model must attend over.

**Layer 2 -- The right analogy is computer memory hierarchies, not tape.** The paper draws an explicit parallel to multi-level cache design in computer systems:

> "This necessity to separate transient processing from stable state mirrors the fundamental design of multi-level-cache hierarchy in computer systems. It does not attempt to retain all information indefinitely, but instead relies on hierarchical structures to clearly separate short-lived, frequently accessed information from long-term, stable and reusable state under finite resources."

A modern CPU cache does not get "bigger context" to handle more computation -- it promotes frequently or strategically valuable data up through L1/L2/L3 hierarchies and evicts stale data. The paper's [[hierarchical-cognitive-caching]] architecture ($\mathcal{L}_1 \rightarrow \mathcal{L}_2 \rightarrow \mathcal{L}_3$) directly mirrors this design. The [[context-migration-protocol]] is the governance mechanism that decides what gets promoted, what gets evicted, and when.

---

### The Cognitive Accumulation Loop

The paper describes cognitive accumulation as a **closed feedback loop**, not a one-way pipeline. The loop has the following structure:

1. **Prefetch** -- Before a new task begins, retrieve relevant prior wisdom from $\mathcal{L}_3$ based on semantic similarity to the task descriptor. Construct the initial context as $e_0 \triangleq \text{concat}(d_\tau, u_{\text{user}}, \Omega_\tau)$, giving the agent a warm start informed by transferable strategies from past tasks.

2. **Execute** -- The agent runs a hierarchical research plan with $m$ exploration directions, each containing $q$ implementation suggestions, executed in parallel. Raw traces accumulate in $\mathcal{L}_1$, forming the evolving experience.

3. **Promote** -- At each phase boundary $t_p$, the phase-level promotion operator $P_1$ compresses the raw parallel exploration trajectories into a refined knowledge unit $\kappa_p$, written to $\mathcal{L}_2$. The corresponding raw traces are evicted from $\mathcal{L}_1$: $\mathcal{L}_2 \leftarrow \mathcal{L}_2 \cup \{\kappa_p\}$, $\mathcal{L}_1 \leftarrow \mathcal{L}_1 \setminus \{e \mid \exists(i,j) \in \mathcal{I}_p, e \in \sigma_{p,i,j}\}$.

4. **Retrieve** -- The context constructor $g(\cdot)$ manages historical indices via a cache-like hit policy $\Psi_t(k)$: raw events are retrieved from $\mathcal{L}_1$ when available; otherwise, compact summaries from $\mathcal{L}_2$ are used; events not in either cache are silently dropped. This ensures the constructed context $C_{t-1} = g(\mathcal{E}_{t-1}) = \text{concat}\{\Psi_t(k)\}_{k=0}^{t-1}$ always keeps active execution traces close to the reasoning loop while representing completed phases compactly.

5. **Crystallise** -- At task completion (step limit $t_{\max}$), the task-level promotion operator $P_2$ distils the entire task history into transferable wisdom $w_\tau$, which is embedded and stored in $\mathcal{L}_3$. "Through this process, transient execution-level context is progressively crystallized into persistent, retrieval-ready wisdom, completing the cognitive accumulation loop."

The loop is visualised in Figure 2 of the paper (reproduced as ASCII below):

```
                     Context              Hierarchical Cognitive Caching (HCC)
                                          ┌──────────────────────────────────────┐
  ┌──────────┐                            │  L3  Prior Wisdom                    │
  │  task    │──prefetch─────────────────▶│      models | parameters | pipelines │
  │  wisdom  │◀─────────────────────────── │                                      │
  │  initial │              context        │          ▲  context promotion         │
  │  code    │◀──────────── hit ──────────▶│  L2  Refined Knowledge               │
  │  result  │                            │      judgements | insights            │
  │  plan 1  │◀─────────────────────────── │                                      │
  │  knowledge│                            │          ▲  context promotion         │
  │  plan 2  │                            │  L1  Evolving Experience              │
  │  code    │──save──────────────────────▶│      research plan | code | logs      │
  │  result  │                            │                                       │
  └──────────┘                            └──────────────────────────────────────┘
```

*(HC = Hierarchical Caching, CM = Context Migration; both are components of HCC.)*

---

### Relation to and Differences from Prior Agent Memory Frameworks

The paper positions cognitive accumulation against a landscape of earlier context management and experiential learning approaches. The survey spans Section 2 (Related Work), with two sub-sections: §2.1 Context Management and §2.2 Autonomous Machine Learning.

#### MemGPT

MemGPT (Packer et al., cited as [19]) introduces an OS-inspired design that separates active context from external memory, enabling agents to page information in and out via explicit memory operations -- "often implemented through summarization or compression mechanisms." The paper acknowledges this as foundational for hierarchical context buffering, but identifies a key gap:

> "Memory promotion or summarization is typically applied in a heuristic manner, without explicitly modeling how execution experience evolves over time or how raw interaction traces should be selectively retained or discarded across different stages of task execution."

In other words, MemGPT provides hierarchical *storage* but no *experiential abstraction*. It does not model the three-stage evolution of experience → knowledge → wisdom. Promotion decisions are ad hoc rather than governed by an explicit lifecycle policy.

#### HiAgent

HiAgent ([6] in the paper) is described as a "subsequent hierarchical memory system" that "further organizes contextual information into multiple layers, allowing agents to retrieve high-level abstractions while preserving access to low-level details." The paper groups HiAgent with MemGPT under the critique that these methods "largely emphasize resource allocation aspects of context management, focusing on *where* information is stored and *how* it is retrieved" -- not on how information should structurally differentiate and evolve through the course of a task.

#### G-Memory

G-Memory ([29]) is a graph-based memory framework, also grouped with HiAgent in the paper's critique. It organises context into hierarchical graph structures, enabling retrieval of high-level summaries while retaining fine-grained details. The paper's critique is the same: it handles storage and retrieval topology, but it is task-specific and does not provide a mechanism for governing when raw interaction traces should be promoted, consolidated, or evicted during ongoing execution.

#### HippoRAG

The paper also cites HippoRAG ([5]) as a "graph-based retrieval framework" in the same cluster. Like G-Memory, it addresses retrieval architecture but not the cognitive lifecycle of information as an agent executes over extended horizons.

#### Reflexion, Memento, ReasoningBank and Related Experiential Methods

A second cluster of prior work approaches context from an experience-driven perspective:

- **Reflexion** ([22]) transforms raw trajectories into reusable feedback.
- **Memento** ([32]) converts reasoning traces into reusable cases.
- **ReasoningBank** ([18]) extracts strategy items from trajectories.
- **Buffer of Thoughts** ([27]) produces abstract thought templates.
- **AWM** ([25]) generates abstract workflows.
- **Evo-Memory** ([26]) implements self-evolving memory mechanisms.

The paper credits these approaches for "highlighting the importance of converting raw interaction history into compact and reusable representations." However, it notes a structural deficiency: "they typically operate with flat or loosely structured memory stores and lack explicit mechanisms for regulating memory growth and lifecycle." They treat memory as a single pool rather than a tiered hierarchy with explicit promotion and eviction policies.

#### AIDE, R&D-Agent, AIRA, AutoMLGen, FM Agent

In the autonomous ML engineering space, the paper reviews:

- **AIDE** ([9]) and **R&D-Agent** ([28]) use iterative refinement and distinct planning phases but "manage context through linear aggregation or summarization, failing to structurally distinguish between transient execution details and the stable strategic insights required for ultra-long-horizon autonomy."
- **AIRA** ([23]), **AutoMLGen** ([3]), and **FM Agent** ([11]) introduce cross-branch knowledge sharing and island-based evolution. While these enable information transfer, "they generally treat 'knowledge' as a homogeneous entity. They lack the cognitive differentiation necessary to distill raw *experience* into reusable *wisdom*, limiting their ability to sustain focus over prolonged scientific discovery."

#### The Gap HCC Fills

Taken together, the paper identifies that prior work has explored hierarchical organisation and experiential abstraction as **separate design dimensions**:

> "There remains limited investigation into frameworks that jointly regulate how short-term working context, accumulated execution experience, and abstracted memory interact within a unified control process. In particular, the absence of structured policies governing when raw interaction traces should be accumulated, promoted, or evicted constrains the ability of context management to simultaneously support scalable execution and continual adaptation."

The HCC architecture (detailed in [[hierarchical-cognitive-caching]]) and the context migration protocol (detailed in [[context-migration-protocol]]) jointly fill this gap by providing a unified three-tier structure with explicit governance rules for information lifecycle.

---

### Philosophical and Scientific-Methodology Framing

Beyond the engineering claims, the paper makes a deeper argument about the *nature* of intelligent long-horizon behaviour. Several framing choices are worth noting.

**Scientific research as the canonical ultra-long-horizon process.** The paper repeatedly uses the scientific research cycle as both motivation and analogy. The abstract states that MLE "is a representative microcosm of scientific discovery." The introduction frames scientific discovery as "inherently a ultra-long-horizon process, characterized not by momentary acts of reasoning but by delayed feedback, high-dimensional exploration, and experimental cycles spanning days or weeks." The implication is that any agent capable of genuine scientific autonomy must internalise this structure -- not just tolerate longer contexts.

**Exploration and exploitation as phases, not a single continuous tradeoff.** The hierarchical research plan divides work into distinct *exploration phases* $[t_{p-1}, t_p)$, each consisting of $m$ parallel exploration directions with $q$ concrete implementation suggestions each. This introduces a phase-level temporal structure that mirrors real scientific workflows: run a batch of experiments, consolidate what was learned, revise the hypothesis, repeat. The consolidation step at each phase boundary is not optional bookkeeping -- it is where experience becomes knowledge.

**Reflection as a first-class operation.** The context promotion operator $P$ (decomposed as $P \triangleq (P_1, P_2)$) is an LLM-based retrospective abstraction. It is not a simple summary; it is a structured act of reflection that compresses "execution traces into concise knowledge or transferable wisdom." The paper's framing implies that reflection -- pausing to abstract what has been learned -- is not a cognitive luxury but a structural requirement for sustained coherent exploration.

**The evolutionary metaphor.** The paper explicitly uses the language of evolutionary refinement:

> "Ultra-long-horizon autonomy is not a linear aggregation of historical context, but an evolutionary process of refinement, stabilization, and reuse."

This framing is deliberate: experience is raw material, knowledge is stabilised phenotype, and wisdom is heritable trait. The cognitive accumulation loop is a selection and abstraction mechanism -- noisy, high-volume raw data is filtered, and only the most validated, stable insights propagate forward and across tasks.

**Decoupling immediate execution from long-term strategy.** One of the paper's most actionable architectural claims is that HCC allows agents to "decouple immediate execution from long-term experimental strategy." This is not just about efficiency -- it is about *coherence*. An agent that carries all execution details in its active context is at risk of local optimisation: it will attend to the most recent error, not the most important strategic direction. By migrating completed-phase context to $\mathcal{L}_2$ and retaining only active-phase traces in $\mathcal{L}_1$, HCC structurally enforces this decoupling.

---

### Summary

The cognitive accumulation paradigm can be condensed into three claims, each building on the previous:

1. **Long-horizon scientific tasks are structurally different** -- not just harder. They require sustaining strategic coherence over hundreds of interdependent steps with delayed, sparse feedback. Context saturation is the primary failure mode, and it is structural, not a capacity problem.

2. **The right model is cognitive differentiation, not context expansion.** Raw experience, distilled knowledge, and transferable wisdom are qualitatively different forms of information operating at different temporal scales. An agent that treats all context as homogeneous will be overwhelmed. An agent that structurally differentiates and promotes information through its lifecycle can sustain coherent exploration indefinitely.

3. **The cognitive accumulation loop closes.** Wisdom feeds warm-starts on new tasks, experience accrues within a task, knowledge stabilises across exploration phases, and completed tasks crystallise new wisdom. This is not a linear pipeline -- it is a closed loop that compounds with scale, which is precisely what "ultra-long-horizon autonomy" requires.

The implementation of this paradigm is [[hierarchical-cognitive-caching]], governed by the [[context-migration-protocol]].
