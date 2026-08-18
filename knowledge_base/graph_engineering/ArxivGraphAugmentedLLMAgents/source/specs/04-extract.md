# Task: Extract wiki page 04 — Graph-Augmented Multi-Agent Systems

You are writing ONE wiki page for a knowledge-base entry summarizing an academic survey paper: "Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects" (arXiv 2507.21407).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the PDF):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/source/chunks/04.txt`

It covers Section 3 "Graph-Augmented LLM Multi-Agent Systems (MAS)", with three subsections: 3.1 Graphs for MAS Orchestration (fixed vs. task-dynamic MAS topology — e.g. static workflow graphs optimized via search, and task-adaptive topology construction), 3.2 Graph for MAS Efficiency (reducing communication overhead — e.g. edge redundancy in MAS, when debate/communication is actually necessary), and 3.3 Graphs for Trustworthy MAS (safety, detecting malicious agents, threat propagation modeling).

Two figures are available for this page (already extracted as page-render PNGs, do not open them — just reference by filename):
- `fig6-mas-orchestration.png` — Figure 6: Graphs for MAS Orchestration.
- `fig7-mas-efficiency.png` — Figure 7: Graphs for MAS Efficiency.

## Output

Write the page to (absolute path):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/wiki/04-graph-augmented-multi-agent-systems.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph-Augmented Multi-Agent Systems

**In one sentence:** <the chunk's whole argument — how graph modeling improves multi-agent system orchestration, efficiency, and trustworthiness>

## Key points

- <5-8 bullets, each a complete standalone claim with real content. Cover all three sub-topics: MAS topology (static/task-independent vs. task-adaptive), efficiency (edge redundancy, when communication/debate is worth its cost), and trustworthiness (detecting malicious agents, threat propagation via graph neural networks). Cite named methods/systems as they appear in the chunk (e.g. G-Designer, DyLAN, G-Safeguard, or whichever names actually appear — do not invent names not present).>

---

## Graphs for MAS Orchestration

<Full detail on 3.1: static/predefined workflow topologies vs. task-dynamic topology construction, named systems, mechanisms.>

![Figure 6: Graphs for MAS Orchestration](images/fig6-mas-orchestration.png)

## Graph for MAS Efficiency

<Full detail on 3.2: the three efficiency perspectives the paper examines, edge redundancy, adaptive debate/communication decisions, named systems.>

![Figure 7: Graphs for MAS Efficiency](images/fig7-mas-efficiency.png)

## Graphs for Trustworthy MAS

<Full detail on 3.3: security/safety threats (prompt injection, memory poisoning), graph-based malicious-agent detection, named systems and benchmarks.>

**Covers:** Section 3 (3.1 Graphs for MAS Orchestration, 3.2 Graph for MAS Efficiency, 3.3 Graphs for Trustworthy MAS)
```

Embed each image under its matching subsection. Use the relative image paths `images/fig6-mas-orchestration.png` and `images/fig7-mas-efficiency.png` exactly (the page lives in `wiki/`, images live in `wiki/images/`).

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than closing your own bead.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 04 extracted"`.
