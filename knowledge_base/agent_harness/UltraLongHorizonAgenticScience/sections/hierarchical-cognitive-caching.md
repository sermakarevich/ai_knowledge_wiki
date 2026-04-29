> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Hierarchical Cognitive Caching

Hierarchical Cognitive Caching (HCC) is the core long-horizon context management architecture of [[ml-master-architecture|ML-Master 2.0]]. It is not a single monolithic mechanism but a coordinated design composed of two complementary components: (1) **hierarchical caching**, which provides the structural architecture for organizing context into multiple tiers according to their temporal stability and reuse value, and (2) **context migration** (the [[context-migration-protocol]]), which dictates the governance protocol for how information is dynamically promoted, consolidated, or discarded across these tiers as exploration unfolds.

The central insight motivating HCC is articulated directly in the paper: *"ultra-long-horizon autonomy is not a linear aggregation of historical context, but an evolutionary process of refinement, stabilization, and reuse."* Agents accumulate raw experience, but only a small fraction of that experience, once repeatedly validated, is distilled into reusable knowledge. When such knowledge is further abstracted and remains stable across tasks, it forms higher-level wisdom. HCC operationalizes this [[cognitive-accumulation-paradigm|cognitive accumulation]] view by structurally separating these three qualitatively different types of cognitive state rather than treating context as a homogeneous sequence of tokens to be retained or discarded wholesale.

---

### The CPU-Cache Analogy

The necessity to separate transient processing from stable state, the paper states, "mirrors the fundamental design of multi-level-cache hierarchy in computer systems." The analogy is deliberate and load-bearing -- not decorative.

In a CPU memory hierarchy:

- **L1 cache** is small, fast, and physically close to the processor. It holds the data the CPU is actively computing over right now. Access latency is ~1 cycle. Capacity is kilobytes. Contents are volatile and evicted frequently.
- **L2 cache** is larger and slightly slower. It holds recently used blocks that are no longer in the hot register file but are still likely to be needed soon. Capacity is hundreds of kilobytes to a few megabytes. Latency is ~4--10 cycles.
- **L3 cache** is the largest on-chip level, shared across cores, with capacity in the tens of megabytes. Latency is ~30--50 cycles. It holds broader working sets and is the last resort before going off-chip to main memory.

HCC maps these properties onto cognitive state as follows:

| CPU Tier | HCC Tier | Contents | Stability | Capacity pressure | Latency analogy |
|---|---|---|---|---|---|
| L1 cache | L1 -- Evolving Experience | Raw execution traces of the active phase | Volatile; evicted per-phase | High -- fills rapidly with logs and outputs | Zero latency; always in-context |
| L2 cache | L2 -- Refined Knowledge | Phase-level summaries, judgments, insights | Medium; stable across phases within a task | Moderate -- one unit per completed phase | Low; retrieved by hit policy into context |
| L3 cache | L3 -- Prior Wisdom | Cross-task strategies, templates, hyperparameter priors | Persistent across tasks | Low -- one entry per completed task | Higher; retrieved by embedding similarity |

The key tradeoff in CPU caches -- capacity vs. latency vs. staleness -- has a direct cognitive analogue. Raw traces (L1) provide maximum fidelity for immediate reasoning but are large and become stale as soon as the phase ends. Summaries (L2) lose execution detail but preserve strategic signal compactly and remain valid across phases. Task-level wisdom (L3) is maximally stable and reusable but requires semantic retrieval rather than direct in-context presence.

The paper states this design goal precisely: "This explicit separation allows rapidly changing signals to remain close to the active loop, while progressively consolidating stable, reusable cognition into persistent memory."

---

### Formal Notation and State Variables

The paper establishes the following formal objects. Let:

- $\mathcal{E}_t \triangleq \{e_0, e_1, \ldots, e_t\}$ -- the full interaction history up to step $t$, where even-indexed events are environment-originated ($e_{2k} \in \mathcal{U}$: task descriptions, user instructions, execution feedback) and odd-indexed events are agent-originated ($e_{2k+1} \in \mathcal{A}$: code patches, commands, plans).
- $g(\cdot)$ -- the context construction function that maps interaction history to the model's input context: $C_{t-1} = g(\mathcal{E}_{t-1})$.
- $T_p = \{t_0, t_1, \ldots, t_p\}$ -- the set of phase boundary time steps, where $[t_{p-1}, t_p)$ is one exploration phase.
- $\mathcal{P}_{p-1} \triangleq \{e_{t_r}\}_{r=0}^{p-1}$ -- the set of plan-boundary events up to the current phase (all high-level plan proposals generated at prior phase boundaries).
- $\kappa_{i:j}$ -- the compact knowledge summary produced from the raw event segment $\mathcal{E}_{i:j}$ via the phase-level context promotion operator $P_1$.
- $d_n$ -- the compact descriptor of past task $\tau_n$; a high-level textual task summary generated by an LLM (see the context-prefetching prompt in Appendix A.1).
- $E(\cdot)$ -- the semantic embedding function applied to compact descriptors.
- $\mathbf{h}_n = E(d_n)$ -- the retrieval key for prior wisdom entry $n$.
- $w_n$ -- the distilled task-level wisdom text corresponding to task $\tau_n$, produced by the task-level promotion operator $P_2$.
- $w_\tau$ -- the wisdom representation produced at the end of task $\tau$.
- $\delta$ -- the cosine similarity threshold for prior wisdom retrieval.

The three cache tiers are then formally defined as:

$$\mathcal{L}_1(t) = \mathcal{E}_{t_0 - 1} \cup \mathcal{P}_{p-1} \cup \mathcal{E}_{t_{p-1}+1:t}$$

$$\mathcal{L}_2(t) = \{\kappa_{t_{r-1}+1:t_r-1}\}_{r=1}^{p-1}$$

$$\mathcal{L}_3 \triangleq \{(\mathbf{h}_n, w_n)\}_{n=1}^{N}$$

where $N$ is the number of stored past tasks.

---

### L1 Cache -- Evolving Experience

**Role in the system:** The agent's *working memory*. It holds the raw, high-fidelity execution traces required for immediate reasoning -- precise debugging and execution-aware decision-making.

**Formal definition:** At any time step $t \in [t_{p-1}, t_p)$, the L1 cache is:

$$\mathcal{L}_1(t) = \mathcal{E}_{t_0-1} \cup \mathcal{P}_{p-1} \cup \mathcal{E}_{t_{p-1}+1:t}$$

This decomposes into three parts:

1. $\mathcal{E}_{t_0-1}$ -- all events that occurred *before* the agent generated the initial code and its results (the bootstrapping context, including the task description, user instructions, and retrieved prior wisdom injected at context prefetch time).
2. $\mathcal{P}_{p-1}$ -- all high-level plan proposals generated at phase boundaries up to the current phase. These are the JSON-structured research plans that mark each phase transition.
3. $\mathcal{E}_{t_{p-1}+1:t}$ -- the raw execution traces of the *currently active* plan, from the moment the current phase began up to the present step.

**Exact contents of the active-phase traces ($\mathcal{E}_{t_{p-1}+1:t}$):**

- The current research plan (JSON object with major directions and concrete implementation suggestions)
- Code patches generated by the agent for each exploration direction
- Terminal outputs from code execution
- Error messages from runtime failures
- Metric logs (e.g., `Epoch 8/8 - Loss: 0.1677 - Val F1 (0.5): 0.87701`)
- Plan state (which directions have been attempted, which are pending)

**Contents of $\mathcal{P}_{p-1}$ (plan-boundary events):**

These are the series of hierarchical research plans that marked the transitions between all prior phases. They are kept in raw form, not summarized, because they carry the strategic scaffolding that frames what the agent was trying to do at each stage of exploration.

**Lifetime:** Within the active phase. Once a phase boundary $t_p$ is reached and the context promotion operator $P_1$ fires, the raw trajectories in $\mathcal{E}_{t_{p-1}+1:t_p-1}$ are evicted from L1 and replaced by a single refined knowledge unit $\kappa_p$ written to L2. The update rule is:

$$\mathcal{L}_2 \leftarrow \mathcal{L}_2 \cup \{\kappa_p\}, \quad \mathcal{L}_1 \leftarrow \mathcal{L}_1 \setminus \{e \mid \exists(i,j) \in \mathcal{I}_p,\ e \in \sigma_{p,i,j}\}$$

where $\sigma_{p,i,j} = (e_{a_{p,i,j}}, e_{a_{p,i,j}+1}, \ldots, e_{b_{p,i,j}})$ is the interaction trajectory induced by the $(i,j)$-th implementation suggestion in the plan.

**Size characteristics:** L1 grows rapidly during a phase because of repeated trial-and-error, tool logs, and iterative debugging. Without intervention, the paper notes that context length can exceed 200k tokens. Figure 4 in the paper ("random-acts-of-pizza" case study) shows the full context (orange line) ballooning well past 200k tokens as the agent iterates through Research Plans 1--3. The L1 strategy of retaining only the active phase, not all prior phases, is what keeps L1 from becoming unbounded.

**Format/schema:** Unstructured -- raw event sequence. The interaction trace is heterogeneous: it includes natural language plan text, Python code blocks in markdown fences, terminal stdout/stderr as plain text, and JSON metric objects as emitted by the training scripts.

**Example entry (illustrative, from Figure 3 context-hit panel):**

```
[terminal output]
Epoch 8/8 - Loss: 0.1677 - Val F1 (0.5): 0.87701

The research confirmed that interventions like
Asymmetric Loss proved ...

[research plan]
Please implement the idea xxx based on current
best code ...
[current best code ...]
```

---

### L2 Cache -- Refined Knowledge

**Role in the system:** The agent's *mid-term strategic memory*. It holds intermediate stabilized cognition distilled from *completed* exploration phases -- the results of applying the phase-level promotion operator $P_1$ to L1 traces. Its purpose is to maintain coherence across iterative trial-and-error without carrying verbose execution logs.

**Formal definition:** At any time step $t \in [t_{p-1}, t_p)$, the L2 cache is:

$$\mathcal{L}_2(t) = \{\kappa_{t_{r-1}+1:t_r-1}\}_{r=1}^{p-1}$$

That is, L2 is a sequence of $p-1$ compact knowledge summaries, one per completed phase prior to the current one. The $r$-th entry $\kappa_{t_{r-1}+1:t_r-1}$ is the refined knowledge unit produced from all the raw trajectories of phase $r$.

**How $\kappa_p$ is produced -- the phase-level promotion operator $P_1$:**

At the start of phase $p$, the agent proposes a hierarchical research plan with $m$ exploration directions, each containing $q$ concrete implementation suggestions. Each suggestion $(i,j) \in \mathcal{I}_p \triangleq \{1,\ldots,m\} \times \{1,\ldots,q\}$ induces a trajectory:

$$\sigma_{p,i,j} \triangleq (e_{a_{p,i,j}}, e_{a_{p,i,j}+1}, \ldots, e_{b_{p,i,j}})$$

The phase-level promotion operator maps all these trajectories to a single knowledge summary:

$$\kappa_p \triangleq \kappa_{t_{p-1}+1:t_p-1} = P_1\!\left(\{\sigma_{p,i,j}\}_{(i,j) \in \mathcal{I}_p}\right)$$

This is performed by the LLM itself via the Appendix A.3 prompt for $P_1$ (phase-level context promotion). The prompt instructs the model to act as a Kaggle Grandmaster with critical thinking skills and to produce a deep analysis covering two aspects:

1. **Execution Summary** -- whether the plan worked as intended and what performance was achieved.
2. **Strategic Insights and Future Direction** -- identifying High-Potential Directions (which to amplify or iterate) and Dead Ends / Low-Value Paths (explicitly advising against specific directions to save compute).

The prompt response format is free-form analytical text -- not JSON, not bullet points, not markdown headings. The output is a direct analysis paragraph, as the prompt specifies: "Output the content directly. Do not add any explanations, comments, greetings, or extra sentences before or after the summary."

**Exact contents of a $\kappa_p$ unit:**

- Whether the phase's plan executed as intended (execution summary)
- Performance metrics achieved (e.g., validation F1, loss values)
- Key judgments -- definitive verdicts on specific technical choices. Examples from the paper:
  - `"feature X is harmful"` -- a judgment
  - `"Asymmetric Loss proved effective under this label imbalance"` -- a judgment
- Experimental insights -- observations about data behavior. Examples:
  - `"CV leakage observed under split Y"` -- an insight
  - `"scaling to 384x384 resolution was the decisive factor"` -- an insight
- Condensed progress summary preserving decision rationale
- High-potential directions to pursue in the next phase
- Dead ends to explicitly avoid

**The distinction between a judgment and an insight:**

A **judgment** is a declarative verdict about whether a specific technique, hyperparameter, or architectural choice is effective or not. It has a binary or ternary valence -- works, does not work, or inconclusive (mirroring the YES/NO/MAYBE icons shown in Figure 2 for L2). An example: "feature X is harmful."

An **insight** is an observation about the data or problem structure that informs future strategy but is not itself a recommendation about a specific implementation choice. It describes something discovered about the environment. An example: "CV leakage observed under split Y."

This distinction matters because judgments drive action selection in future phases (do not re-attempt dead ends) while insights drive problem re-framing (change the split strategy before trying any new approach).

**Format:** Free-form analytical prose in natural language. The paper does not specify a rigid schema for the $\kappa_p$ unit itself -- its structure emerges from the LLM's response to the $P_1$ prompt. The prompt's response-format instruction is "Output the content directly," indicating unstructured text rather than a template with mandatory fields.

**Lifetime:** Across all phases within a single task. $\mathcal{L}_2$ grows by one unit per completed phase and is never evicted during the task. At task completion, the entire L2 (along with L1 and the terminal interaction history) is passed to the task-level promotion operator $P_2$ to produce the L3 entry. L2 does not persist between tasks; it is torn down when the task ends.

**What is excluded from L2 (and why):** Verbose execution logs (stdout/stderr), full code bodies, raw terminal output, iteration-level debugging traces. These are retained in L1 only for the duration of the phase they arose in. The entire point of $P_1$ is to evict this noise while preserving the strategic signal.

**Example entry (from Figure 3, context-hit panel -- the `[more refined knowledge]` block):**

```
The research confirmed that scaling to a
ConvNeXt-Large backbone with 384x384
resolution was the decisive factor.
[more refined knowledge ...]
```

And from the context-promotion panel (right side of Figure 3):

```
"model design": {
  "1": ".has ConvNeXt Large (timm:
        'convnext_large_in22ft1k') with [...]",
  "2": "[detailed ideas ...]"
},
"loss design": {[more detailed ideas...]}
```

This JSON-structured excerpt in the context-promotion panel appears to be part of the L2 output structure when the $P_1$ prompt elicits a more structured strategic plan -- though the paper's primary description of the $\kappa_p$ format is prose-based.

---

### L3 Cache -- Prior Wisdom

**Role in the system:** The agent's *long-term memory and warm-start engine*. It stores task-agnostic, transferable strategies distilled from previously solved machine learning tasks. It is persistent across tasks and enables both cross-task transfer and strong initialization for new tasks.

**Formal definition:**

$$\mathcal{L}_3 \triangleq \{(\mathbf{h}_n, w_n)\}_{n=1}^{N}$$

where $N$ is the total number of stored past tasks, $\mathbf{h}_n = E(d_n)$ is the embedding of the compact task descriptor $d_n$, and $w_n$ is the distilled task-level wisdom text.

**Exact contents of a $w_n$ (wisdom) entry:**

The task-level promotion operator $P_2$ produces $w_n$ from:

$$w_\tau = P_2(d_\tau, \mathcal{L}_1(t_{\max}), \mathcal{L}_2(t_{\max}), h(\mathcal{E}_{t_{\max}}))$$

where $h(\cdot)$ is the extraction function applied to the terminal interaction history. The $P_2$ prompt (Appendix A.3, "Prompts for phase-level context promotion $P_2$") instructs the model to summarize two specific aspects of the final high-performance code:

1. **Data loading and preprocessing** -- key points including feature engineering decisions, preprocessing choices, augmentation strategies, dataset handling.
2. **Model selection and model training** -- key points including backbone/architecture selection, loss functions, optimizer settings, hyperparameter values, training schedule details.

The output format is explicitly specified in the $P_2$ prompt:

```
DATA SUMMARY:
YOUR ANSWER
MODEL SUMMARY:
YOUR ANSWER
```

This is a structured two-section plain text format. The prompt instructs: "Your response should be concise but not too short. Do not omit any parameters. You should make sure a code engineer can basically reproduce the code with your summarization."

**Examples of $w_n$ content (from Figure 3, context-prefetch panel):**

```
Augmentation: Apply training augmentation including
cropping [more augmentation related wisdom ...]
Backbone: vit_base_patch16_224 (Vision
Transformer); Initialization: [more model related
wisdom ...]
```

**Examples of cross-task types of content held in L3:**

- Robust model templates (e.g., ViT-base with specific initialization)
- Reusable preprocessing pipelines (e.g., augmentation strategies for plant pathology images)
- Stable hyperparameter priors (e.g., learning rate ranges, batch sizes that worked for similar tasks)
- Data handling patterns (e.g., how to construct the submission CSV, how to handle missing labels)

**Compact descriptor $d_n$ -- how it is computed:**

The compact descriptor $d_n$ for task $\tau_n$ is a high-level textual task summary generated by an LLM. The prompt (Appendix A.1) instructs the model to produce a single dense paragraph, strictly below 250 tokens, that is "dense, precise, and semantic-rich" and covers:

- task type
- input format and output format
- evaluation metric and how it is computed
- dataset structure and key fields/modalities
- submission format
- any important constraints or rules

The format constraints are strict:

```
STRICT FORMAT REQUIREMENTS:
- Output MUST be a single paragraph.
- No bullet points, no numbering, no markdown.
- No headings, no blank lines, no lists.
- No backticks or code blocks.
- No special characters other than standard punctuation.
- Do NOT introduce information that is not explicitly
  present in the task description.
- Do NOT explain ML concepts or provide suggestions,
  analysis, or background.
```

This dense single-paragraph format is optimized for embedding-based retrieval -- it forces the descriptor to be semantically rich and compact without structural noise that could confuse the embedding model.

**Embedding model:** The paper uses the notation $E(\cdot)$ for the semantic embedding function but does not name the specific embedding model in the main text or appendix. The experimental setup (Section 4.1) identifies Deepseek-V3.2-Speciale as the backbone LLM and mentions Deepseek-V3.2 with thinking for context promotion, but the embedding model for L3 retrieval is not explicitly identified.

**Retrieval mechanism -- Context Prefetching:**

Given the current task's descriptor $d_\tau$, the system computes its embedding $\mathbf{q} = E(d_\tau)$ and retrieves a subset of prior wisdom via a threshold-based prefetching operator:

$$\Omega_\tau = \{w_n \mid (\mathbf{h}_n, w_n) \in \mathcal{L}_3,\ \cos(\mathbf{q}, \mathbf{h}_n) > \delta\}$$

where $\delta$ is the similarity threshold and $\cos(\cdot, \cdot)$ denotes cosine similarity. The retrieved set $\Omega_\tau$ represents a *view* of $\mathcal{L}_3$ -- the cache itself is unchanged. The initial environment event is then constructed by combining the task description, user instructions, and retrieved prior wisdom:

$$e_0 \triangleq \text{concat}(d_\tau, u_{\text{user}}, \Omega_\tau)$$

and the initial agent context is $C_0 = g(\mathcal{E}_0) = e_0$.

**Storage format:** Embedding-value pairs $(\mathbf{h}_n, w_n)$ where $\mathbf{h}_n$ is a dense vector and $w_n$ is the two-section plain text wisdom string (DATA SUMMARY + MODEL SUMMARY).

**Persistence:** L3 is the only tier that persists across tasks. It is "only updated upon task completion via a task-level context promotion operator" ($P_2$). The update rule is:

$$\mathcal{L}_3 \leftarrow \mathcal{L}_3 \cup \{(E(d_\tau), w_\tau)\}$$

**Warm-up from Kaggle competitions:** To build a useful L3 prior quickly, ML-Master 2.0 uses 407 Kaggle competitions (those not in MLE-Bench's evaluation set) as a warm-up dataset. Each competition is processed through $P_2$ to produce a $(E(d_n), w_n)$ pair, pre-populating L3 before any MLE-Bench evaluation begins. This bootstrap is critical: ablation Row 3 (Table 2 in the paper) shows that removing $\mathcal{L}_3$ degrades the above-median rate from 81.8% to 72.7% and the any-medal rate from 72.7% to 54.5%, because the agent loses the strong initialization that reduces ineffective early exploration.

---

### How the Three Tiers Interact with the LLM's Active Context Window

At any moment $t$ within phase $p$, the agent's context $C_{t-1}$ is constructed by the context constructor $g(\cdot)$ using the **cache-like hit policy** $\Psi_t$. This policy governs which tier's representation of each historical event is inserted into the context:

$$\Psi_t(k) = \begin{cases} e_k, & e_k \in \mathcal{L}_1(t) \\ \kappa_{t_{r-1}+1:t_r-1}, & e_k \notin \mathcal{L}_1(t),\ e_k \in \mathcal{L}_2(t),\ k = t_{r-1}+1 \\ \varnothing, & \text{otherwise} \end{cases}$$

The context is then assembled as:

$$C_{t-1} = g(\mathcal{E}_{t-1}) = \text{concat}\{\Psi_t(k)\}_{k=0}^{t-1}$$

The practical effect of this policy on the active context window, in order of priority:

1. **Task description + user instructions** (from $\mathcal{E}_{t_0-1}$, always in L1) -- always present verbatim.
2. **Retrieved prior wisdom** $\Omega_\tau$ (prefetched from L3, injected into $e_0$, now part of L1's $\mathcal{E}_{t_0-1}$) -- always present verbatim for the duration of the task.
3. **Initial code and its results** (from $\mathcal{E}_{t_0-1}$, in L1) -- always present verbatim.
4. **Series of research plan proposals** $\mathcal{P}_{p-1}$ (plan-boundary events, kept raw in L1) -- present verbatim.
5. **Completed phases** -- each represented by its single compact knowledge unit $\kappa_r$ from L2, not by its raw traces. Only one $\kappa$ per completed phase enters the context (a "cache hit" to L2 replaces the entire raw trajectory for that phase).
6. **Current active phase traces** $\mathcal{E}_{t_{p-1}+1:t}$ (in L1) -- present verbatim, in full detail.

L3 itself is **never in-context during execution**. It is accessed only at task initialization (context prefetch) and written only at task completion (task-level promotion). During the task, L3's contributions are materialized as part of $e_0$ and thereafter treated as part of L1's initial segment.

The paper summarizes the policy's effect: "This policy retrieves all plan events and active-phase traces in raw form, while representing each completed phase by a single refined unit, preventing context saturation without losing strategic continuity."

---

### Context Size Behavior -- The "Random-Acts-of-Pizza" Case Study

Figure 4 in the paper provides a concrete demonstration of HCC's context compression effect on the MLE-Bench task *random-acts-of-pizza* (predicting which Reddit pizza requests will be fulfilled).

**Without HCC (full context -- orange line in Figure 4):**
- Context length grows monotonically across all four research plans.
- It exceeds 200k tokens by Research Plan 3.
- The agent accumulates all terminal outputs, debugging iterations, and code revisions in the context without compression.
- The paper notes this is especially severe "when debugging is introduced additionally to handle errors in terminal outputs."

**With HCC (blue line in Figure 4):**
- Context length rises during each research plan's active phase (L1 filling) but drops sharply at each phase boundary (L1 eviction + $\kappa$ written to L2).
- The peak context length is limited to approximately **70k tokens**.
- Despite this compression, the agent "retains critical insights from prior failed strategies."
- The agent secures a medal during the **fourth iteration** of the research plan proposal and verification cycle -- a result it could not have reached without the strategic continuity maintained by L2 summaries surviving across phase boundaries.

**The quantitative gap:** >200k tokens (full context) vs. ~70k tokens (HCC context) -- a reduction of approximately 3x in peak context usage. Critically, the HCC path achieves a *medal* while the full-context approach would saturate before reaching Research Plan 4.

The token counts correspond to the Deepseek-V3.2-Speciale backbone's tokenization. The paper does not state the exact context window limit of the backbone but the relevant operational threshold is the model's maximum context length; the HCC context stays safely below it while the full context would breach it before the task is resolved.

---

### Tier Initialization and Teardown

**Initialization at task start:**

1. Compute the compact task descriptor $d_\tau$ using the context-prefetching LLM prompt (Appendix A.1) -- a single dense paragraph under 250 tokens.
2. Embed $d_\tau$: $\mathbf{q} = E(d_\tau)$.
3. Retrieve prior wisdom: $\Omega_\tau = \{w_n \mid \cos(\mathbf{q}, \mathbf{h}_n) > \delta\}$ from $\mathcal{L}_3$.
4. Construct the initial event: $e_0 = \text{concat}(d_\tau, u_{\text{user}}, \Omega_\tau)$.
5. Set the initial context $C_0 = g(\mathcal{E}_0) = e_0$.
6. $\mathcal{L}_1$ starts as $\{e_0\}$; $\mathcal{L}_2$ starts empty; $\mathcal{L}_3$ is read-only during the task.
7. The agent generates the initial code via the coding prompt (Appendix A.2), which receives `{task_description}`, `{data_preview}`, `{data_knowledge}` (from $\Omega_\tau$), and `{model_knowledge}` (also from $\Omega_\tau$).

**During task execution -- per-phase transitions:**

At each phase boundary $t_p$:
1. The phase-level promotion operator $P_1$ fires.
2. $P_1$ takes as input: task description, current memory (existing $\mathcal{L}_2$), current research plan, and corresponding raw results from $\mathcal{L}_1$.
3. $P_1$ produces $\kappa_p$ -- the compact knowledge summary (free-form strategic prose).
4. $\mathcal{L}_2 \leftarrow \mathcal{L}_2 \cup \{\kappa_p\}$.
5. The raw trajectories $\{\sigma_{p,i,j}\}$ are evicted from $\mathcal{L}_1$.
6. The agent proposes the next research plan using the plan-generation prompt (Appendix A.2), which receives `{memory}` = current $\mathcal{L}_2$ contents (the series of $\kappa$ summaries).

**Teardown at task end:**

At step $t_{\max}$:
1. The task-level promotion operator $P_2$ fires.
2. $P_2$ receives: $d_\tau$, $\mathcal{L}_1(t_{\max})$, $\mathcal{L}_2(t_{\max})$, $h(\mathcal{E}_{t_{\max}})$ (the terminal interaction history extraction).
3. $P_2$ produces $w_\tau$ -- the task-level wisdom in DATA SUMMARY + MODEL SUMMARY format.
4. $\mathcal{L}_3 \leftarrow \mathcal{L}_3 \cup \{(E(d_\tau), w_\tau)\}$.
5. $\mathcal{L}_1$ and $\mathcal{L}_2$ are discarded (they are task-scoped).
6. $\mathcal{L}_3$ persists for all future tasks.

---

### Comparison Table

| Tier | Contents | Lifetime | Retrieval mechanism | Written by | Example entry |
|---|---|---|---|---|---|
| **L1 -- Evolving Experience** | Raw event traces: task description, user instructions, retrieved wisdom (from prefetch), initial code + results, all plan proposals, current-phase code patches + terminal outputs + error messages + metric logs | Within the active phase; evicted at each phase boundary | Direct concatenation -- always in-context | The agent (code/plans) and environment (feedback/logs) | `Epoch 8/8 - Loss: 0.1677 - Val F1 (0.5): 0.87701` |
| **L2 -- Refined Knowledge** | Phase-level summaries $\kappa_p$: execution status, key judgments (YES/NO/MAYBE on specific techniques), experimental insights, high-potential next directions, explicit dead-end warnings | Across all phases within one task; discarded at task end | Cache-hit policy: each completed phase represented by exactly one $\kappa$ unit in-context | LLM via $P_1$ prompt at each phase boundary | `"The research confirmed that Asymmetric Loss proved effective. CV leakage observed under split Y. Dead end: boosting feature counts above 512."` |
| **L3 -- Prior Wisdom** | Embedding-value pairs $(\mathbf{h}_n, w_n)$: task descriptor embedding + distilled DATA SUMMARY + MODEL SUMMARY text covering preprocessing pipelines, model templates, hyperparameter priors | Persistent across all tasks | Cosine similarity $> \delta$ against new task embedding; materialized into $e_0$ at task start | LLM via $P_2$ prompt at task completion | `DATA SUMMARY: Augmentation: Apply training augmentation including cropping [...] MODEL SUMMARY: Backbone: vit_base_patch16_224 (ViT), Initialization: [...]` |

---

### Ablation Evidence

Table 2 in the paper provides ablation results on MLE-Bench-Lite (single representative run per configuration) that directly validate the contribution of each tier:

| Config | L1 (Experience) | L2 (Knowledge) | L3 (Wisdom) | Valid Submission | Above Median | Any Medal |
|---|---|---|---|---|---|---|
| 1 | removed | -- (cascades) | present | 54.5% | 36.4% | 22.7% |
| 2 | present | removed | present | 95.5% | 81.8% | 59.1% |
| 3 | present | present | removed | 95.5% | 72.7% | 54.5% |
| 4 (full) | present | present | present | **95.5%** | **81.8%** | **72.7%** |

Key observations:

- **Removing L1** (Row 1) collapses the valid submission rate to 54.5% and the medal rate to 22.7%. Because L1 is what enables the agent to interact iteratively with the environment for code refinement, removing it also causally removes L2 (no execution traces means nothing to promote into L2). This underscores L1's foundational role.
- **Removing L2** (Row 2) costs 13.6 percentage points on any-medal rate (59.1% vs. 72.7%) despite retaining raw context. Raw context alone allows average performance but L2's strategic synthesis is indispensable for the complex, multi-phase solutions needed for top-tier performance.
- **Removing L3** (Row 3) costs 9.1 pp on above-median rate (72.7% vs. 81.8%) and 18.2 pp on any-medal rate (54.5% vs. 72.7%). Prior Wisdom provides the strong initialization that substantially reduces ineffective exploration in early phases -- a critical enabler for competitive performance within a fixed 24-hour budget.

---

### Relationship to the Broader Architecture

HCC is the structural component of ML-Master 2.0. Its companion component, the [[context-migration-protocol]], governs the *dynamics* -- the three operations (context prefetching, context hit, context promotion) that move information between tiers as the task unfolds.

The [[cognitive-accumulation-paradigm]] that motivates HCC frames the evolution of cognitive state as: raw *experience* (L1) -- once validated -- is distilled into stable *knowledge* (L2), which when abstracted across tasks becomes transferable *wisdom* (L3). HCC makes this conceptual hierarchy concrete and computationally operational.

The [[experimental-evaluation]] section validates HCC's design empirically: the 56.44% overall medal rate on MLE-Bench, the 92.7% relative improvement over ML-Master, and the ablation results in Table 2 all trace directly to the structural separation of cognitive state that HCC enforces.
