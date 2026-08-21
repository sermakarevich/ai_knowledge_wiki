# GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs

**Paper:** [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs (Feng et al., 2026)](https://arxiv.org/abs/2604.23626)

## Human Readable TL;DR

Imagine a team of specialist consultants (LLMs of different sizes and skills) working on a hard problem. Someone needs to decide, at every step, both *what job* to do next (break the problem down? answer a piece of it? merge the pieces?) and *which consultant* should do it. Most existing routers only pick a consultant once, or pick one repeatedly without remembering how past teams solved similar problems. GraphPlanner gives the dispatcher a live notebook — shaped like a graph — that tracks who did what, how well it worked, and how much it cost, both for the current problem and for problems solved before. A reinforcement-learning-trained brain reads that notebook and picks the next job-and-consultant pair. The result routes better, cheaper, and generalizes to new problems and new consultants it has never seen.

## TL;DR

GraphPlanner casts agentic LLM routing as graph generation within an MDP: at each step it jointly selects an agent role (Planner/Executor/Summarizer) and an LLM backbone, using GARNet — a heterogeneous GNN that fuses a per-query workflow memory graph with a cross-episode historical memory graph through shared (LLM, role) hub nodes — trained end-to-end with PPO to balance task utility against computational cost. Across 14 tasks in 6 domains it beats single-round (RouterDC, GraphRouter) and multi-round (R2-Reasoner, Router-R1) routers by +3.8% (Phase 1) to +9.3% (Phase 2), generalizes to unseen tasks (78% avg. accuracy) and unseen LLMs with no fine-tuning, sits on the accuracy/cost Pareto frontier, and trains with the lowest GPU footprint (1.04 GiB) and fastest inference (1.2 s/query) of any router compared.

## Problem & Motivation

Routing across heterogeneous LLMs is necessary to exploit their differing cost/capability profiles, but existing routers are stuck in two limited settings: **single-round routers** (RouterDC, GraphRouter) make one-shot query-to-model assignments and cannot reason, decompose tasks, or coordinate; **multi-round routers** (R2-Reasoner, Router-R1) interleave reasoning and routing calls but treat each call independently, causing redundant calls, context conflicts, and no exploitation of complementary model strengths. The paper's motivating question: *"How can we extend routers to agentic LLM settings?"* Three challenges make this hard: (1) diverse, branching relations among queries/responses/models; (2) **deferred rewards** — early misrouting cascades into downstream cost or quality loss, a hard credit-assignment problem; (3) rich historical workflow traces (successful collaboration patterns, error modes) go largely unexploited by prior routers.

## Main Original Ideas

- **Agentic routing as MDP-driven graph generation.** The router's action at each step is a pair `(role, LLM)` — not just an LLM — spanning Planner (decompose), Executor (answer), Summarizer (integrate); the router builds the workflow graph as it decides.
- **GARNet: dual heterogeneous graph memory.** A per-query `G_workflow` graph and a cross-episode `G_history` graph share a single fixed set of role-hub nodes (one per LLM×role pair). Historical embeddings are computed first and injected into the workflow encoder (`H(loc) = GARNet(G_workflow; H(his))`), letting current decisions draw on accumulated experience without redundant nodes across steps or episodes.
- **Joint accuracy/cost objective via PPO.** Reward is task utility minus a cost penalty (`r_T = U(ŷ,y*) − αC`), with `α` a tunable knob that sweeps a controllable accuracy/cost Pareto curve rather than one fixed operating point.
- **Two-phase evaluation design.** Phase 1 optimizes routing *within* a fixed workflow (Depth/Width hyperparameters); Phase 2 requires the router to *generate* the workflow topology itself — isolating whether the gains come from better model choice or from better workflow structure.

## Key Findings

| Comparison | GraphPlanner | Best baseline |
|---|---|---|
| Phase 1 avg. accuracy gain | +3.8% min. | — |
| Phase 2 avg. accuracy gain | +9.3% | RouterDC 54.3% vs. GraphPlanner 63.6% |
| Unseen tasks (zero-shot), avg. Acc | 78% | RouterDC 58% |
| Unseen AIME dataset (zero-shot) | 14.7% | RouterDC 7.56% |
| Training GPU compute | 1.04 GiB | Router-R1 186.26 GiB |
| Total training time (Phase 2) | 120 min | Router-R1 300 min |
| Inference latency | 1.2 s/query | GraphRouter 2.1 s/query |
| History ablation (GARNet vs. w/o History) | — | GARNet strictly dominant on all 5 domains |
| Alt. graph encoders (GAT/GraphTransformer) | GARNet wins all 5 domains | 2.3–7.6% behind |

Additional results: generalizes zero-shot to two new agentic roles (Thinker, Verifier) without retraining, and improves further with as few as 50 historical interactions (1% of training queries); LLM-based history summarization/retrieval baselines barely help (GraphPlanner beats the best of them by up to 171% relative on World Knowledge); illustrative examples show workflow topology adapting to task complexity (flat fan-out for math, nested two-level planning for code, single-hop for simple QA).

## Suggestions & Future Directions

- The authors flag richer agent-role vocabularies beyond Planner/Executor/Summarizer as future work (partially previewed in Appendix E with Thinker/Verifier).
- Open questions not addressed by the paper: robustness under adversarial/poisoned history graphs, behavior at much larger LLM pools (>12 backbones), and whether GARNet's shared role-hub design scales to role sets that grow dynamically at inference time rather than being fixed a priori.

## Authors & Institutions

Tao Feng, Haozhen Zhang, Zijie Lei, Peixuan Han, Jiaxuan You — ICLR 2026.

## Figures

- **Figure 1** — router-comparison schematic: single-round vs. multi-round vs. agentic routing architectures ([[wiki/01-problem-and-preliminaries|wiki page 01]]).
- **Figure 2** — GraphPlanner's MDP formulation and dual-graph memory overview ([[wiki/02-graphplanner-method|wiki page 02]]).
- **Figure 3** — Phase 1 evaluation setup and accuracy/cost comparison ([[wiki/03-experiments-and-results|wiki page 03]]).
- **Figure 4** — accuracy/cost Pareto frontier vs. baseline routers ([[wiki/03-experiments-and-results|wiki page 03]]).
- **Figure 5** — generalization/ablation radar charts (unseen LLMs, history ablation, transductive vs. inductive) ([[wiki/03-experiments-and-results|wiki page 03]]).
- **Figure 6** — illustrative workflow-generation examples across task types ([[wiki/05-additional-ablations-and-generalization|wiki page 05]]).
