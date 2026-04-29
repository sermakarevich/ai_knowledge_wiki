> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

# Ultra-Long-Horizon Agentic Science -- Code Sandbox

Minimal, runnable implementation of the three Hierarchical Cognitive Caching
tiers and the Context Migration Protocol from ML-Master 2.0 (Zhu et al., 2026).
Runs locally with LangGraph + Ollama.

## What This Implements

- **Context Prefetch** (Section 3.4.1) -- `prefetch_node` in `src/nodes.py`: embeds the task descriptor with a local embedding model and pulls any L3 wisdom entries above a cosine threshold `delta`.
- **L1 / L2 / L3 tiers** (Section 3.3) -- typed state in `src/state.py`: `current_phase_events` (L1), `refined_knowledge` (L2), `prior_wisdom_store` (L3).
- **Plan / Execute inner loop** (Section 3.2) -- `plan_node` proposes a hypothesis using L3 wisdom + L2 refined knowledge; `execute_node` simulates running the experiment (the real system runs Python; we use the LLM so the sandbox has zero data setup).
- **P1 Phase-level Promotion** (Section 3.4.3, Appendix A.3) -- `p1_promote_node`: at each phase boundary, compresses parallel trajectories into one kappa_p refined-knowledge entry and evicts L1.
- **P2 Task-level Promotion** (Section 3.4.3, Appendix A.3) -- `p2_promote_node`: at task end, distills all kappa_p into one L3 wisdom entry (DATA SUMMARY + MODEL SUMMARY) and appends it to the L3 store.

## What This Does NOT Implement

- Real ML code execution -- the sandbox uses the LLM to imagine plausible
  experiment observations so it runs without a dataset or GPU.
- MCTS / parallel trajectory search -- trajectories run sequentially here.
- Kaggle grader integration, real MLE-Bench task loading, or 24h timeouts.
- Multi-task training curriculum -- `examples/sample_data.py` seeds L3 with 3
  hand-written entries instead of warming up from 407 Kaggle competitions.
- Any of the original paper's quantitative claims (56.4% medal rate etc).

## Prerequisites

1. Install [just](https://github.com/casey/just) (task runner).
2. Install [Ollama](https://ollama.ai) and make sure `ollama serve` is running.

## Setup

```bash
just setup            # sync deps + pull llama3.2 + pull nomic-embed-text + verify graph
```

## Run

```bash
just run              # run with default chat model (llama3.2)
just run llama3.3     # run with a different chat model
```

The embedding model is fixed to `nomic-embed-text` because it is what the L3
cosine retrieval uses; override with `OLLAMA_EMBED_MODEL=<name>` if needed.

## Graph Topology

```
START -> prefetch -> plan -> execute -+-> plan          (if more trajectories in phase)
                                      +-> p1_promote -+-> plan        (if more phases)
                                                      +-> p2_promote -> END
```

Each phase runs `trajectories_per_phase` (default 2) Plan/Execute cycles
before firing P1. After `max_phases` (default 2) phases, P2 writes a single
new L3 wisdom entry and the task ends.

## Tuning Knobs

- `OLLAMA_MODEL` -- chat backbone (default `llama3.2`).
- `OLLAMA_EMBED_MODEL` -- embedding model for L3 retrieval (default `nomic-embed-text`).
- `WISDOM_SIM_THRESHOLD` -- `delta` in the paper; cosine threshold for prefetch (default `0.55`).
- `max_phases`, `trajectories_per_phase` -- loop depth/width, set in `run.py`.

## File Layout

```
sandbox/
├── pyproject.toml         # uv project config
├── justfile               # just setup / just run / just check
├── run.py                 # entry point; streams node-by-node state
├── src/
│   ├── state.py           # TypedDict for HCC state (L1/L2/L3)
│   ├── prompts.py         # adapted from Appendix A.1 + A.3
│   ├── nodes.py           # prefetch, plan, execute, p1_promote, p2_promote
│   └── graph.py           # StateGraph wiring
└── examples/
    └── sample_data.py     # sample task + 3 seeded L3 wisdom entries
```
