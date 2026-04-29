# Brain-Inspired Graph Multi-Agent Systems for LLM Reasoning

**Paper:** [Brain-Inspired Graph Multi-Agent Systems for LLM Reasoning (Hao et al., 2025)](https://arxiv.org/abs/2603.15371)

## Human Readable TL;DR

Imagine you have a team of specialists working on a tough puzzle. Instead of having one person try to solve it all alone, a team leader first looks at the puzzle and decides which experts are needed and how they should collaborate -- maybe a number-cruncher, a fact-checker, and a strategy planner. They all share one whiteboard so everyone can see the full picture. This paper builds exactly that kind of "brain-like teamwork" for AI, where a designer AI creates a custom team of AI agents for each problem, and they all coordinate through a shared workspace -- just like how different brain regions form temporary teams to solve complex tasks.

## TL;DR

BIGMAS is a multi-agent LLM framework inspired by Global Workspace Theory that dynamically constructs task-specific directed agent graphs with a centralized shared workspace for each problem instance. A GraphDesigner agent autonomously determines agent roles, topology, and workspace contracts, while a global Orchestrator routes execution based on full state visibility. Evaluated on three combinatorial reasoning benchmarks across six frontier LLMs, BIGMAS consistently improves accuracy -- even for strong reasoning models like GPT-5 -- and outperforms ReAct and Tree of Thoughts baselines.

---

## Problem & Motivation

Large Language Models (LLMs) and Large Reasoning Models (LRMs) suffer from **accuracy collapse** on sufficiently complex multi-step reasoning tasks. This collapse persists even when explicit solution algorithms are provided, suggesting a fundamental bottleneck in consistent logical execution rather than solution discovery. Existing multi-agent frameworks (ReAct, Reflexion, Tree of Thoughts, Graph of Thoughts) partially address this but rely on fixed topologies and point-to-point communication, leading to fragmented task states and limited adaptability. BIGMAS aims to provide a structural remedy orthogonal to individual model capabilities, grounded in neuroscience principles of how the human brain flexibly coordinates distributed specialized processors.

---

## Main Original Ideas

1. **Problem-Adaptive Graph Design** -- A dedicated GraphDesigner agent analyzes each problem and autonomously constructs a task-specific directed agent graph (nodes, edges, source/sink), along with a workspace template and natural-language "workspace contract" specifying each agent's read/write responsibilities. This mirrors the dynamic coalition formation described in Global Workspace Theory.

2. **Centralized Shared Workspace (Global Broadcast)** -- All agent interactions are mediated exclusively through a structured workspace with four partitions: context (read-only problem input), work (read-write intermediate results), system metadata (execution history), and answer (final output). No direct point-to-point communication exists, ensuring globally consistent state visibility.

3. **Global Orchestrator with Full-State Conditioning** -- A global Orchestrator routes execution by conditioning on the complete workspace state and full execution history, enabling detection of convergence, identification of unproductive cycles, and routing to fallback nodes -- overcoming the local-view bottleneck of reactive approaches.

4. **Write Validation and Self-Correction Loop** -- Before any agent output modifies the workspace, a validation step checks path existence, action-type compatibility, and payload non-emptiness. Failures trigger a self-correction loop (up to R retries) with structured error feedback, ensuring data integrity without aborting execution.

5. **Neuroscience Grounding via Global Workspace Theory** -- The architecture operationalizes three GWT principles: processor specialization (distinct agent roles), dynamic coalition formation (per-problem graph construction), and global broadcast (centralized workspace coordination).

---

## Key Findings

### Performance Across Models and Tasks

| Model | Task | Base (%) | BIGMAS (%) | Gain |
|---|---|---|---|---|
| DeepSeek-V3.2 | Game24 | 25.0 | 36.0 | +11.0 |
| DeepSeek-V3.2 | Six Fives | 12.0 | 30.0 | +18.0 |
| DeepSeek-V3.2 | Tower of London | 6.0 | 20.0 | +14.0 |
| Claude 4.5 Sonnet | Game24 | 48.0 | 68.0 | +20.0 |
| Claude 4.5 Sonnet | Six Fives | 15.0 | 38.0 | +23.0 |
| Claude 4.5 (+thinking) | Tower of London | 57.0 | **93.0** | +36.0 |
| **GPT-5** | Game24 | 96.0 | **100.0** | +4.0 |
| **GPT-5** | Six Fives | 95.0 | **100.0** | +5.0 |
| **GPT-5** | Tower of London | 91.0 | **98.0** | +7.0 |

### Baseline Comparison (DeepSeek-V3.2)

| Method | Game24 | Six Fives | Tower of London |
|---|---|---|---|
| Base LLM | 25.0 | 12.0 | 6.0 |
| ReAct | 26.0 | 18.0 | 8.0 |
| Tree of Thoughts | 30.0 | 25.0 | 18.0 |
| **BIGMAS** | **36.0** | **30.0** | **20.0** |

### Qualitative Findings

- Gains are **orthogonal to model-level reasoning enhancements** -- LRMs with extended CoT still benefit substantially from BIGMAS
- The GraphDesigner autonomously produces **task-appropriate topologies** without explicit complexity constraints (mean 3.07 nodes for Game24, 4.82 for Tower of London)
- Node role distributions show **emergent functional decomposition**: Game24 favors Generator/Validator pipelines; Tower of London produces diverse compositions with more Analyzer (24%) and Optimizer (12%) nodes
- Incorrect runs require systematically **more routing decisions** than correct ones, offering a potential signal for early stopping
- Node execution accounts for 46--56% of token budget; orchestration overhead is bounded at 17--25%

---

## Suggestions & Future Directions

1. **Broader domain evaluation** -- Extend BIGMAS to open-domain QA, code generation, and other reasoning-intensive tasks beyond combinatorial puzzles.

2. **Episodic memory and meta-learning** -- Incorporate memory of past graph designs into the GraphDesigner to amortize design costs and improve efficiency across similar problem instances.

3. **Token-aware graph design** -- Develop cost-sensitive graph construction that balances reasoning depth against computational budget.

4. **Fine-tuned specialist agents** -- Explore heterogeneous multi-agent systems where individual nodes are fine-tuned for specific roles rather than using general-purpose LLMs for all positions.

5. **Adaptive hyperparameter tuning** -- Investigate dynamic adjustment of MAX_NODES, MAX_PATH_LENGTH, and step budgets based on problem characteristics.

6. **Acknowledged limitation** -- Current evaluation is limited to three combinatorial reasoning benchmarks; generalization to diverse real-world reasoning tasks remains to be demonstrated.

---

## Authors & Institutions

Guangfu Hao (CASIA, UCAS), Yuming Dai (UCAS), Xianzhe Qin (Taiyuan University of Technology), Shan Yu (CASIA, UCAS) -- corresponding author. Hao and Dai contributed equally.
