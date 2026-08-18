> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice

Answer from memory first, then expand to check. Don't re-read the wiki before attempting these.

<details>
<summary><b>1. (Core recall, wiki 1) What four limitations of plain LLM agents motivate graph augmentation, and which agent module does each limitation map to?</b></summary>

Unreliable/hallucination-prone task planning (planning module), inefficient long-term memory from statelessness and limited context (memory module), difficulty managing large toolsets — selection, disambiguation, consistent reasoning over similar tools (tool module), and unresolved inter-agent communication/coordination once scaled to multi-agent systems (the MAS layer, beyond the single-agent framework).
</details>

<details>
<summary><b>2. (Core recall, wiki 2) Name the four ways graphs structure the planning module, and give one method for each.</b></summary>

Plan-as-graph (AFlow), sub-task-pool-as-graph / constrained task graph (Wu et al.'s GNN-based planner over HuggingGPT's pool), reasoning-thought-as-graph (Graph of Thought / GoT), and environment-as-graph (LocAgent for code, or the dynamic spatio-semantic safety graph for robots).
</details>

<details>
<summary><b>3. (Elaboration, wiki 2) Why does the paper draw a contrast between AFlow and AgentKit specifically, rather than just listing both as "graph-based planning"?</b></summary>

They represent the two poles of the same idea: AFlow builds a *static* workflow graph optimized ahead of time via Monte Carlo Tree Search, while AgentKit's graph is *dynamic* — it evolves during interaction. The contrast illustrates that "plan as a graph" isn't one technique but a spectrum from pre-computed to runtime-adaptive structure, which foreshadows the same static→dynamic progression the paper later describes for MAS topology.
</details>

<details>
<summary><b>4. (Core recall, wiki 3) What are the two categories of agent memory, and name one representative system for each.</b></summary>

Interaction memory (experiential — e.g. A-MEM's Zettelkasten-inspired evolving notes, or AriGraph which also merges in episodic memory) and knowledge memory (structured external facts — e.g. SLAK's location-based knowledge graph, or KG-Agent).
</details>

<details>
<summary><b>5. (Transfer, wiki 3) A team wants to fine-tune a small open model to call tools more reliably, but has no labeled tool-use dialogue data. Which technique from the paper addresses exactly this, and how does it work?</b></summary>

ToolFlow: build a parameter-level tool graph from semantic similarity between tool inputs/outputs, sample coherent tool combinations from that graph, then generate multi-turn dialogue plans from those combinations to use as supervised fine-tuning data — turning the tool graph itself into a synthetic-data generator.
</details>

<details>
<summary><b>6. (Core recall, wiki 4) The paper draws an explicit analogy between graph-learning problems and MAS engineering problems. What are the three MAS "redundancy" types, and what GNN concept does each mirror?</b></summary>

Edge redundancy (unnecessary inter-agent communication links, addressed by AgentPrune) mirrors classical edge/structure pruning; node redundancy (too many agents, addressed by AgentDropout) mirrors node dropping; layer/round redundancy (diminishing returns from more debate rounds, addressed by Residual MoA and DOWN) mirrors GNN over-smoothing from stacking too many layers.
</details>

<details>
<summary><b>7. (Transfer, wiki 4 + wiki 5) If you were designing a new multi-agent system today using this paper's framework, would you start with a static or task-adaptive topology, and what would make you upgrade to a process-dynamic one?</b></summary>

Start static/simple if task complexity is low and uniform (cheaper, easier to debug — the paper's own MacNet finding that more edges don't always help supports keeping it simple). Move to task-adaptive (G-Designer-style) once task difficulty varies enough that a fixed topology under- or over-provisions agents/edges. Upgrade further to process-dynamic (ReSo/EvoMAC-style) only when the task itself changes mid-execution or needs runtime fault tolerance — otherwise the added complexity isn't justified, which lines up with the paper's own framing of these as progressively more expensive tiers.
</details>

<details>
<summary><b>8. (Evaluation, drawing on critical_thinking.md) The paper claims its taxonomy is comprehensive. What's one concrete reason to be skeptical of "comprehensive" for a fast-moving arXiv-preprint literature, and how does that affect how you should use this survey?</b></summary>

See [[critical_thinking]] — a survey compiled from papers up to mid-2025 in a field where new GLA methods appear monthly is, at best, a snapshot; "comprehensive" here means "comprehensive as of writing," not evergreen. Practically: treat the taxonomy's *categories* (planning/memory/tools; orchestration/efficiency/trustworthiness) as the durable contribution, and treat the specific example methods cited as illustrative rather than an exhaustive or current list — check arXiv/venues directly for anything published after ~July 2025.
</details>
