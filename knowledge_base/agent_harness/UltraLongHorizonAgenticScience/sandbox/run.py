"""Entry point for the HCC sandbox.

Runs ML-Master 2.0's full context migration loop (Prefetch -> Plan/Execute ->
P1 -> ... -> P2) against a small synthetic task, printing intermediate state at
each node so the three cache tiers are visible in action.
"""

from __future__ import annotations

import os
import sys
from typing import Any

from examples.sample_data import SAMPLE_TASK, build_prior_wisdom_store
from src.graph import graph
from src.state import HCCState


HEADER = "=" * 72


def _banner(title: str) -> None:
    print(f"\n{HEADER}\n{title}\n{HEADER}")


def _print_tier_snapshot(state: dict[str, Any]) -> None:
    l1 = state.get("current_phase_events") or []
    l2 = state.get("refined_knowledge") or []
    l3_retrieved = state.get("retrieved_wisdom") or []
    print(f"  L1 events in active phase   : {len(l1)}")
    print(f"  L2 refined-knowledge entries: {len(l2)}")
    print(f"  L3 retrieved at task start  : {len(l3_retrieved)}")


def main() -> int:
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    embed_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    _banner(f"HCC sandbox  |  chat model: {model}  |  embed model: {embed_model}")

    try:
        print("Warming up L3 prior-wisdom store (embedding 3 seed entries)...")
        prior_wisdom = build_prior_wisdom_store()
    except Exception as exc:  # pragma: no cover -- operator-facing guidance
        print(f"\nERROR setting up Ollama embeddings: {exc}", file=sys.stderr)
        print("\nIs Ollama running? Try:\n  just setup\nor manually:\n  ollama serve &\n  ollama pull llama3.2\n  ollama pull nomic-embed-text", file=sys.stderr)
        return 1

    initial: HCCState = {
        "task_description": SAMPLE_TASK,
        "user_instructions": "Be concise. Prefer simple models first.",
        "prior_wisdom_store": prior_wisdom,
        "max_phases": 2,
        "trajectories_per_phase": 2,
    }

    _banner("TASK")
    print(SAMPLE_TASK)

    final_state: dict[str, Any] | None = None
    try:
        for step in graph.stream(initial, stream_mode="updates"):
            node_name = next(iter(step.keys()))
            update = step[node_name]
            _banner(f"node: {node_name}")
            if node_name == "prefetch":
                print("Context Prefetch -- L3 cosine retrieval")
                for w in update.get("retrieved_wisdom", []):
                    print(f"  * {w[:180]}")
            elif node_name == "plan":
                hyp = update.get("_hypothesis", "")
                sketch = update.get("_code_sketch", "")
                print(f"  HYPOTHESIS: {hyp[:200]}")
                print(f"  SKETCH    : {sketch[:200]}")
            elif node_name == "execute":
                events = update.get("current_phase_events", [])
                if events:
                    last = events[-1]
                    print(f"  traj={last['trajectory_idx']}  score={last['score']:.2f}")
                    print(f"  observation: {last['observation'][:220]}")
            elif node_name == "p1_promote":
                kappas = update.get("refined_knowledge", [])
                if kappas:
                    print("  kappa_p (L2 entry):")
                    print("    " + kappas[-1].replace("\n", "\n    ")[:800])
            elif node_name == "p2_promote":
                w = update.get("new_wisdom") or {}
                print("  L3 wisdom written:")
                print(f"    descriptor: {w.get('descriptor', '')[:200]}")
                print(f"    text      : {w.get('wisdom_text', '')[:400]}")
                print(f"  final_solution: {update.get('final_solution', '')[:200]}")
            _print_tier_snapshot(update)
            final_state = update
    except Exception as exc:
        print(f"\nERROR during graph execution: {exc}", file=sys.stderr)
        print("\nIs Ollama running? Try:\n  just setup", file=sys.stderr)
        return 1

    _banner("DONE")
    if final_state:
        print("final_solution:", final_state.get("final_solution", "(none)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
