# Natural-Language Agent Harnesses

**Paper:** [Natural-Language Agent Harnesses (Pan et al., 2025)](https://arxiv.org/abs/2603.25723)

## Human Readable TL;DR

Think of an AI agent like a worker following a complex recipe. Right now, the recipe instructions are baked into the kitchen equipment itself -- hard to change, share, or study. This paper proposes writing those recipes in plain English instead, so anyone can read, swap, or tweak them. They built a "smart kitchen" that can follow these English-language recipes directly, and showed that agents controlled this way perform comparably or better -- especially when they can write down intermediate notes on paper rather than trying to remember everything in their heads.

## TL;DR

This paper formalizes Natural-Language Agent Harnesses (NLAHs) -- explicit, portable, natural-language representations of agent control logic (contracts, roles, stages, state semantics, failure taxonomies) -- separated from runtime execution. An Intelligent Harness Runtime (IHR) interprets these harnesses directly. Controlled experiments on SWE-bench Verified and OSWorld show that NLAHs are operationally viable, support module-level composition/ablation, and enable code-to-text migration with a behavioral shift toward file-backed state and artifact-backed verification (47.2% vs 30.4% on OSWorld).

---

## Problem & Motivation

Agent "harnesses" -- the orchestration layers governing multi-step reasoning, tool use, memory, delegation, and stopping -- are critical determinants of performance, sometimes outweighing base model differences. Yet harness logic is typically embedded in controller code, framework defaults, and runtime-specific conventions. This makes harnesses:

- **Non-portable** across systems and runtimes
- **Hard to compare** -- performance differences conflate harness design with implementation details
- **Resistant to scientific study** -- individual modules cannot be cleanly isolated or ablated
- **Opaque** -- no explicit executable representation captures system-wide contracts, roles, state, and failure handling

While natural-language artifacts (e.g., AGENTS.md, skill bundles) have shown that control knowledge can be packaged as text, they attach local instructions without providing a full, executable harness-level representation. This paper bridges that gap.

---

## Main Original Ideas

1. **Natural-Language Agent Harnesses (NLAHs):** A formal specification for expressing complete agent control logic -- contracts, roles, stage structure, adapters, scripts, state semantics, and failure taxonomy -- in structured natural language, making harnesses first-class scientific objects that can be inspected, compared, composed, and migrated. This goes beyond prompt engineering or skill bundles to capture system-wide orchestration.

2. **Intelligent Harness Runtime (IHR):** A shared runtime that integrates an in-loop LLM to interpret NLAH logic directly. It cleanly separates generic runtime services (tool adapters, sandboxing, child lifecycle) from task-family policy (stages, artifact contracts, verifiers), enabling controlled experiments. The IHR lifts a single model completion into an "agent call" bounded by an explicit execution contract specifying required outputs, budgets, permission scope, and completion conditions.

3. **Harness-Runtime Boundary Formalization:** An explicit analytical boundary between what belongs to the runtime (generic services) and what belongs to the harness (task-specific stages, artifact contracts, verifiers). This separation is what makes ablation and migration studies scientifically meaningful.

4. **File-Backed State Module:** An optional mechanism that externalizes durable state into path-addressable artifacts, ensuring state survives context truncation, restarts, and delegation -- shifting reliability from transient context windows to persistent files. Enforces three properties: externalized (written to artifacts), path-addressable (accessed by path), and compaction-stable.

5. **Code-to-Text Migration Framework:** A methodology for reconstructing native code harnesses as NLAHs and evaluating migration fidelity, demonstrating that harness logic can be faithfully relocated from code to natural language with preserved (or improved) functionality.

---

## Key Findings

### SWE-bench Verified (Coding)

| Configuration | Resolved Rate | Key Observation |
|---|---|---|
| Full IHR (TRAE) | Narrow band around ablations | ~90% of process metrics in delegated children |
| No Runtime Skill | Similar outcome rate | Significant process metric reduction |
| No Harness Skill | Similar outcome rate | Less structured exploration |

- Full IHR reshapes **process behavior** (tokens, tool calls, runtime) far more than raw outcome scores
- Over 110/125 instances showed consistent outcomes across conditions; differences concentrated in a small "component-sensitive" frontier
- Full IHR acts as a **solved-set replacer** -- gains unique successes but loses others where simpler direct-path repairs suffice
- "Alignment failures" emerged where increased structure led to locally organized but benchmark-misaligned solutions

### OSWorld (Computer Use)

| Configuration | Success Rate |
|---|---|
| NLAH (migrated OS-Symphony) | **47.2%** |
| Native code harness | 30.4% |

- NLAH realization shifted from brittle GUI repair loops to **file-backed state and artifact-backed verification**
- Migrated traces were denser in logged events (58.5 avg vs 18.1 native steps), reflecting enhanced observability
- Verification shifted from screen plausibility to path-addressable evidence (written files, system queries)

### Module Ablations (RQ2)

- **Self-evolution module** improved solve loops by enforcing disciplined, acceptance-gated attempt cycles
- **File-backed state** and **evidence-backed answering** improved auditability but showed mild score gains
- **Dynamic orchestration**, **verifier**, and **multi-candidate search** acted as solved-set replacers rather than uniform improvers
- More structure does not uniformly improve performance -- modules must align intermediate acceptance with final evaluator criteria

---

## Suggestions & Future Directions

1. **Automated harness search:** With harnesses as explicit objects, they become a search space amenable to automated optimization -- potentially discovering better control strategies than manual engineering.

2. **Natural language precision limits:** Natural language is inherently less precise than code; future work should address faithful recovery of mechanisms relying on hidden service-side state or proprietary schedulers.

3. **Runtime contamination mitigation:** A strong shared runtime charter may absorb behaviors that should be attributed to harness text; stricter causal identification methods are needed.

4. **Confound control in ablations:** Textual representations introduce confounds (instruction salience, prompt length) that could influence outcomes independently of module logic.

5. **Security considerations:** Portable harness logic lowers barriers to deploying risky workflows. Future deployments should incorporate provenance tracking, review processes, permission controls, and sandbox isolation.

6. **Scale validation:** The authors plan to rerun full benchmarks with GPT-5.4-mini and update results to validate findings at different model scales.

---

## Authors & Institutions

Linyue Pan (Tsinghua University), Lexiao Zou (Harbin Institute of Technology, Shenzhen), Shuo Guo (Tsinghua University), Jingchen Ni (Tsinghua University), Hai-Tao Zheng (Tsinghua University, corresponding author)
