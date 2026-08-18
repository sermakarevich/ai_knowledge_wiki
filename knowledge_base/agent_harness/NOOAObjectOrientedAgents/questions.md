---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Native Python Object-Oriented Agents

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. In NOOA's programming model, what visually and functionally distinguishes an "agentic method" from an ordinary Python method on the same `Agent` class, and how does Principle P3 explain why this particular split matters?

> [!tip]- Answer
> An agentic method's body is literally the ellipsis `...`; at runtime the harness intercepts it and drives an LLM-based loop, using the method's docstring as the prompt and its signature as the input/output contract, whereas a method with a real body executes as ordinary deterministic Python. P3 states that only semantic, open-ended work belongs in the agentic loop while exact rules, arithmetic, and state transitions stay in deterministic methods — the `...`-vs-real-body split is the visible, in-code marker of that boundary, which is what lets the other four design principles compose cleanly over a single class. See [[wiki/01-introduction-and-design-principles|Introduction and Design Principles]].

### Q2. When a CodeAct method is called with a large argument (say, a 100-item list), what does the model actually see in its rendered context, versus what does it actually operate on when it writes code?

> [!tip]- Answer
> The model sees only a bounded preview in the context window — the concrete type, the true length, and a short head/tail sample (e.g. `list(len=100, [:5]=[...], [-5:]=[...])`) — but the full, untruncated object is bound as the real local variable in the execution environment. This "pass by reference" means generated code (loops, slices, indexing) operates on the complete object, so the amount of data an agent can process is bounded by the execution environment, not by the context window. See [[wiki/02-agent-loop-strategies-and-context|Agent Loop, Strategies, and Context]].

### Q3. NOOA splits context into a static prefix, an append-only event history, and a dynamic suffix re-rendered every turn. Why does this specific ordering matter for running long CodeAct loops cheaply, and what would be lost if volatile state were interleaved earlier in the prompt instead of appended at the tail?

> [!tip]- Answer
> The static prefix never changes and the event history only grows by appending (never rewriting) earlier turns, so everything before the dynamic suffix stays byte-identical turn to turn, letting the model provider reuse the KV cache instead of recomputing it. If volatile dynamic state were placed earlier in the prompt, every turn would invalidate the cache from that point onward, forcing full reprocessing of the accumulated history on every single turn. See [[wiki/02-agent-loop-strategies-and-context|Agent Loop, Strategies, and Context]].

### Q4. NOOA's long-term memory can store `kind:key` references inside a memory record instead of copied values. What problem does this solve at recall time, and how is the reference resolved safely?

> [!tip]- Answer
> A referenced value is resolved against live agent state at the moment of recall via strict name lookup (never `eval`), returning either the current live value or an explicitly marked dangling snapshot if it no longer exists. This eliminates the "stale copy" failure mode, where a memory would otherwise answer with an outdated value that no longer matches the agent's actual state, extending the same pass-by-reference principle used for method arguments into the persistence layer. See [[wiki/03-execution-validation-and-memory|Execution, Validation, and Memory]].

### Q5. Section 4.1's reasoning-mode ablation on the Nemotron 3 family shows the benefit of turning reasoning on growing as base model capability falls. What pattern did the paper find, and what did the authors conclude from it?

> [!tip]- Answer
> Frontier models (e.g. Opus 4.8, GPT-5.5) were already near-saturated on the capability suite regardless of reasoning mode, but within the Nemotron 3 family the improvement from enabling reasoning grew larger as base capability fell — Nano jumped from 52.5% to 84.8%, far more than Ultra's 93.4% to 94.1%. The authors read this as inference-time reasoning acting as a "capability equalizer" that closes much of the interface-fluency gap between smaller and frontier models. See [[wiki/04-capability-tests-and-stress-test-appendix|Capability Tests and the Stress-Test Deep Dive]].

### Q6. Appendix B's four `sentiment_batch` transcripts show Claude Opus 4.8 failing despite having already computed the correct answer, while GPT-5.5 passes using a fully manual, unsophisticated approach. What general lesson about evaluating agentic harness use does this pair of outcomes suggest?

> [!tip]- Answer
> Sophistication and success turned out to be orthogonal: Opus 4.8's advanced subagent fan-out failed because it then hand-transcribed its own already-correct printed results and dropped an item, while GPT-5.5's plain manual labeling passed because it disciplined itself to inspect every item and return the live, freshly-built list rather than a retyped copy. The transferable lesson is that agentic-evaluation failures often trace to lapses in mundane bookkeeping discipline (reusing a value already computed) rather than to any gap in understanding the interface itself. See [[wiki/04-capability-tests-and-stress-test-appendix|Capability Tests and the Stress-Test Deep Dive]].

### Q7. On Terminal-Bench, 77% of OpenCode's failed GPT-5.5 trials terminate within ten steps, while NOOA does not show this pattern. What harness-design difference explains it, and which broader NOOA principle does it illustrate?

> [!tip]- Answer
> OpenCode treats any model response without a tool call as a stopping signal, letting the agent declare victory informally at any point, whereas NOOA requires the model to return a type-validated `TaskResult` (root cause, evidence, and a verification command) that the harness checks before the loop can end, preventing unsupported completion claims. This illustrates the paper's broader argument that type annotations should function as executable, enforced contracts rather than informal conventions living only in the prompt. See [[wiki/05-swebench-terminal-bench-and-cybergym|SWE-bench, Terminal-Bench & CyberGym]].

### Q8. The ARC-AGI-3 world-model skill treats "retrodiction" as the sole refinement signal for the agent's learned dynamics model. What does this mean concretely, and what happened in the two games that abandoned this discipline for ad-hoc in-cell search instead?

> [!tip]- Answer
> Retrodiction means the agent compares its own `predict(z, action)` forecast against what it actually observed each turn, and any mismatch is the only signal used to refine the model — replacing DreamTeam's separate 4,690-line harness-side evaluation engine with a check the agent performs on itself. The two games that hung instead ran unbounded ad-hoc searches (one branched over 3,456 click targets with no depth or node budget) while leaving their own persisted `predict` model uncalled, showing durable curated model code was more reliably engineered than improvised code written fresh each turn. See [[wiki/06-arc-agi-3-and-world-models|ARC-AGI-3 and World Models]].

### Q9. Appendix A's rubric requires "Strong" pass-by-reference to mean a live object reference crosses the model boundary, not a serialized copy. Why do frameworks like Google ADK or the OpenAI Agents SDK — which let a model address files or artifacts by name — still only score "Partial" on this axis, and what would they need to change to reach "Strong"?

> [!tip]- Answer
> Both frameworks give the model a handle (an artifact name or file path) it can use to retrieve content, but the content itself is always serialized into or out of the prompt/tool boundary as a copy — the model never holds or mutates the actual live Python object. To score "Strong," a framework would need a mechanism like NOOA's CodeAct cells, where the model's generated code executes directly against the live object (with only a bounded preview ever rendered as text), removing the serialization step entirely. See [[wiki/07-comparison-to-other-frameworks|Comparison to Other Frameworks]].

### Q10. The paper states that NOOA's in-process execution model makes its isolation philosophy "identical" to that of any harness with a shell tool, and recommends pairing NOOA with an external sandbox like OpenShell. What tension does this create with NOOA's pass-by-reference design, and is the paper's framing of the trade-off as unavoidable fully convincing?

> [!tip]- Answer
> Pass-by-reference is only possible because model-written code runs in the same process as the live objects it manipulates; wrapping execution in an external sandbox would leave only serialized copies crossing the boundary, destroying the capability the whole framework is built around — so the authors treat the safety gap as a deliberate, structural trade-off rather than an oversight. Whether "identical to any shell-tool harness" is really the right comparison, and whether no intermediate position exists, is a framing worth pressure-testing further. See [[critical_thinking|Critical Analysis]].

### Q11. The related-work section argues that tool-as-CLI packaging has been displacing tool-as-MCP packaging among agent frameworks. What underlying difference in how a CLI invocation versus an MCP tool call delivers its output does the paper use to explain this shift?

> [!tip]- Answer
> A CLI is called from within model-written code, so its raw text output becomes just another value the generated program can filter, transform, and compose before anything reaches the model — whereas an MCP tool call is a single JSON round-trip whose entire result lands directly in the context window with no chance for the model to process it first. Because bash itself is framed as a weak form of code as action for the same reason (commands are little programs with pipes and loops), the authors read the CLI-over-MCP trend as agent tooling converging on that same code-as-action logic at the packaging level. See [[wiki/08-related-work-and-conclusion|Related Work and Conclusion]].
