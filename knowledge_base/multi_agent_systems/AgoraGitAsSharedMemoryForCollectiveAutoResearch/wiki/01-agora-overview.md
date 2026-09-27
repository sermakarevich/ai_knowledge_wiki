> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Agora: Git as Shared Memory for Collective AutoResearch — Overview
**In one sentence:** Agora is an append-only Git-stored DAG of immutable research commits plus a derived index and diversity-aware selection rule that lets uncoordinated agents share a public frontier, lineage, and verification status, demonstrated by 13 task-free workers over nearly 12 days publishing 1,703 contributions and driving a frozen hybrid model from 3.39 to 1.899 bits per byte.
## Key points
- Single coding agents (e.g. AutoResearch) improve setups unattended, but parallel sessions start from scratch, so more agents mean more duplicated search rather than more discovery.
- Agora records research as an append-only directed acyclic graph (DAG) stored in Git: each result, insight, hypothesis, verification, and report is an immutable commit whose parent edges say what it builds on.
- Every claim is a commit anyone can check out and rerun; a derived index exposes the frontier, neglected branches, and verification status of each claim.
- A diversity-aware selection rule keeps the community from collapsing onto one leader; the system makes claims, dependencies, verification status, and untried alternatives visible without dictating a single workflow.
- Git supplies immutable, content-addressed artifacts while a database supplies searchable views; the Git history is the only state and nothing else passes between workers.
- First sustained run: nearly 12 days, 13 language-model workers with no assigned tasks and no central planner, on a weight-transfer problem with 141 pretrained donors and a frozen 119.6M-parameter attention-SSM hybrid matching no donor, without training data or gradient updates.
- Run outcome: 1,703 contributions, evaluator from 3.39 to 1.899 bits per byte, closing 62% of the gap to a trained GPT-2 124M; winning recipe compresses donor next-token statistics into target embedding/output head plus short-range context via sparse edits to attention, feed-forward, and state-space blocks, with 145-commit ancestry across 15 accounts and 165 independent reproductions, none failed.
- The run required a single mid-run human intervention that pulled the community out of a monoculture; existing multi-agent frameworks organize conversations/roles within one task, while Agora serves asynchronous participants sharing no conversation, manager, role graph, runtime, or filesystem.
---
## Abstract
**Covers:** title block, authors, arXiv:2609.18094v1 [cs.LG] 16 Sep 2026, Abstract

Paper: "Agora: Git as Shared Memory for Collective AutoResearch" — Yifan Zhang, Yunheng Zou, Shaokun Zhang, Jian Hu, Hao Zhang, Binfeng Xu, Jan Kautz, Yi Dong (NVIDIA).

Core claim (paraphrased strictly from chunk):

- Autonomous loops like AutoResearch show one coding agent can improve a training setup unattended; running several means each session starts from scratch, so more agents tend to mean duplicated search rather than discovery.
- Agora is shared memory for such agents: research recorded as an append-only DAG stored in Git, so every claim is a commit anyone can check out and rerun.
- Each result, insight, hypothesis, verification, and report is an immutable commit with parent edges saying what it builds on; a derived index exposes the frontier, neglected branches, and verification status; a diversity-aware selection rule prevents collapse onto one leader.

First sustained use (exact numbers from Abstract):

| Fact | Value |
|---|---|
| Duration | nearly 12 days |
| Workers | 13 language-model workers, no assigned tasks, no central planner |
| Task | weight-transfer: 141 pretrained donor models; frozen 119.6M-parameter attention-SSM hybrid whose dimensions match no donor; initialize target without training data or gradient updates |
| Contributions | 1,703 |
| Evaluator | 3.39 → 1.899 bits per byte |
| Gap closed | 62% of gap to trained GPT-2 124M |
| Winning recipe | compresses donor next-token statistics into target's embedding and output head, then adds short-range context signal through sparse edits to attention, feed-forward, and state-space blocks |
| Winning ancestry | 145-commit ancestry spanning 15 accounts |
| Reproductions | 165 independent reproductions posted, none failed |

Open items named in Abstract: the single mid-run human intervention that pulled the community out of a monoculture; what the trace does and does not establish; the controlled comparison that would settle whether shared research state improves discovery per unit of compute.

## 1. Introduction
**Covers:** Section 1 (Introduction), incl. Contributions (i)–(v)

- Research is narrated as individual breakthroughs but done by communities: researchers inherit prerequisites, reuse instruments/code, compete over open questions, and arrive at the same idea independently once the frontier makes it reachable; multiple discoveries are the rule (Merton, 1961); group output is not the strongest member's output (Woolley et al., 2010); agentic AI should be treated as social/institutional system, not one large reasoner (Evans et al., 2026).
- Coordination problem: a session can run code, read papers, launch experiments, but what it learns is stuck in a transcript or temporary worktree — next session does not know which learning rate diverged, which branch was abandoned, or which result still needs independent reproduction; adding workers worsens this (more attempts but more duplicate search, earlier convergence, more reconstruction of who did what).
- Existing multi-agent frameworks organize conversations or role-specific workflows (Hong et al., 2023; Li et al., 2023; Wu et al., 2023) — works within one task; a research community additionally needs state outliving any worker: public frontier, immutable lineage, negative results, independent verification, and attention-spreading without dictating one workflow.
- Agora is that layer: research is a DAG where every contribution is a Git commit and every parent edge means "builds on"; Git gives immutable content-addressed artifacts, a database gives searchable views, and the graph itself becomes the coordination and quality signal.
- Verbatim design stance: "The system does not try to decide what is true. It makes claims, dependencies, verification status, and untried alternatives visible enough that a mixed community of humans and agents can coordinate around them." And: "The Git history is the only state: workers read and write it, and nothing else passes between them."
- Test run restated in Intro: 12-day run, 13 coding-agent sessions given only a two-page brief, an evaluator, and the shared graph, initializing a frozen hybrid LM from a donor zoo with no training data; reached 1.899 bpb from random baseline 3.39, 165 mutual reproductions, and after a single human intervention showing them a map of their own concentration, left a five-day monoculture within a day.
- Contributions: (i) formulate multi-agent research as append-only DAG with artifacts, claims, metrics, provenance (Section 3); (ii) separate immutable storage from downstream evidence and diversity-aware attention allocation; (iii) describe Git, SQLite, API, CLI, web prototype; (iv) report first sustained run incl. method found, verification, coordination dynamics (Section 4); (v) use open questions to define matched, preregisterable evaluation (Appendix C).

## 2. Related Work
**Covers:** Section 2 (all four subsections in chunk)

- Collective intelligence / scientific institutions: discovery modeled as decentralized institution with local problem choice coordinated through shared public knowledge (Polanyi, 1962); simultaneous discoveries recurrent (Merton, 1961); group performance depends on interaction structure (Woolley et al., 2010); collaboration structure, topic choice, team scale linked to discovery production/diffusion (Fortunato et al., 2018); institutional perspective extended to agentic AI (Evans et al., 2026). Agora implements a narrow slice: durable public memory, attribution, verification, attention allocation for one research community.
- LLM multi-agent systems: role play (Li et al., 2023), programmable conversations (Wu et al., 2023), standard operating procedures (Hong et al., 2023), staged software-development dialogues (Qian et al., 2024); AgentVerse varies team composition (Chen et al., 2023); Magentic-One uses orchestrator (Fourney et al., 2024); persistent memory/social behavior (Park et al., 2023); repeated debate (Du et al., 2023). Distinction: "These systems coordinate a team inside one application or episode. Agora serves asynchronous participants that share no conversation, manager, role graph, runtime, or filesystem."
- Autonomous research agents: AutoResearch single-agent unattended training-setup improvement (Karpathy, 2026); ResearchAgent idea generation/refinement via reviewers (Baek et al., 2025); AI Scientist full-pipeline automation plus simulated review (Lu et al., 2024); Agent Laboratory staged workflow with optional human feedback (Schmidgall et al., 2025); benchmarks MLAgentBench, MLE-bench, ScienceAgentBench (Chan et al., 2024; Chen et al., 2024; Huang et al., 2023); ChemCrow/Coscientist tool and lab connections (Boiko et al., 2023; Bran et al., 2024). Distinction: "Agora is complementary: it prescribes no end-to-end researcher, and instead keeps durable state (negative results, lineage, verification) across researchers that are scheduled independently."
- Shared workspaces / reproducible artifacts: blackboard architectures via shared problem-solving state + control policy (Hayes-Roth, 1985); DataLad (Halchenko et al., 2021), ReproZip (Chirigati et al., 2013), Whole Tale and RO-Crate (Brinckman et al., 2019; Soiland-Reyes et al., 2022), Nextflow/Snakemake/MLflow (Di Tommaso et al., 2017; Mölder et al., 2021; Zaharia et al., 2018). Agora's level-up: "Agora applies the same idea one level up, to claims: its shared state is an append-only contribution DAG, and the same graph exposes verification status, neglected branches, and attention signals."

**Covers:** Abstract + Sections 1–2 of chunk 01-agora-git-as-shared-memory-for.md (lines 1–118; p.1–2 of paper).
