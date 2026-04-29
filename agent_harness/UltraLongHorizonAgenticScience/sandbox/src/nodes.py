"""LangGraph nodes implementing the Context Migration Protocol from Section 3.4.

One node per operator: Context Prefetch, Plan, Execute, P1 Promote, P2 Promote,
plus two lightweight control-flow checks.
"""

from __future__ import annotations

import math
import os
import re

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.prompts import (
    EXECUTE_PROMPT,
    P1_PROMOTE_PROMPT,
    P2_PROMOTE_PROMPT,
    PLAN_PROMPT,
    TASK_DESCRIPTOR_PROMPT,
)
from src.state import HCCState, TrajectoryEvent, WisdomEntry

MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2")
EMBED_MODEL_NAME = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
WISDOM_SIM_THRESHOLD = float(os.environ.get("WISDOM_SIM_THRESHOLD", "0.55"))  # delta


def _chat() -> ChatOllama:
    return ChatOllama(model=MODEL_NAME, temperature=0.4)


def _embed() -> OllamaEmbeddings:
    return OllamaEmbeddings(model=EMBED_MODEL_NAME)


def _cosine(a: list[float], b: list[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(x * x for x in b))
    return num / (da * db) if da and db else 0.0


def _extract_field(text: str, key: str) -> str:
    match = re.search(rf"{key}\s*:\s*(.+?)(?=\n[A-Z ]{{2,}}:|\Z)", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_score(text: str) -> float:
    match = re.search(r"SCORE\s*:\s*([0-9.]+)", text)
    if not match:
        return 0.5
    try:
        value = float(match.group(1))
    except ValueError:
        return 0.5
    return max(0.0, min(1.0, value))


def prefetch_node(state: HCCState) -> dict:
    """Implements: Section 3.4.1 -- Context Prefetch.

    Embeds the task descriptor and retrieves any L3 wisdom entries whose
    cached embedding is above the cosine-similarity threshold delta.
    """
    chat = _chat()
    descriptor_response = chat.invoke(
        [HumanMessage(TASK_DESCRIPTOR_PROMPT.format(task_description=state["task_description"]))]
    )
    descriptor_text = descriptor_response.content if hasattr(descriptor_response, "content") else str(descriptor_response)

    embedder = _embed()
    query_vec = embedder.embed_query(descriptor_text)

    retrieved: list[str] = []
    for entry in state.get("prior_wisdom_store", []):
        sim = _cosine(query_vec, entry["embedding"])
        if sim >= WISDOM_SIM_THRESHOLD:
            retrieved.append(f"(sim={sim:.2f}) {entry['wisdom_text']}")

    if not retrieved:
        retrieved = ["(no prior wisdom above threshold -- cold start)"]

    return {
        "retrieved_wisdom": retrieved,
        "current_phase_index": 0,
        "current_trajectory_idx": 0,
        "current_phase_events": [],
        "refined_knowledge": [],
        "phase_done": False,
        "task_done": False,
    }


def plan_node(state: HCCState) -> dict:
    """Implements: Section 3.2.1 -- Hypothesis Generation.

    Uses L3 retrieved wisdom plus L2 refined knowledge to propose the next trajectory.
    """
    chat = _chat()
    prompt = PLAN_PROMPT.format(
        phase_index=state["current_phase_index"],
        task_description=state["task_description"],
        retrieved_wisdom="\n- " + "\n- ".join(state.get("retrieved_wisdom", [])),
        refined_knowledge="\n- " + "\n- ".join(state.get("refined_knowledge", []) or ["(none yet)"]),
        trajectory_idx=state["current_trajectory_idx"],
    )
    response = chat.invoke([HumanMessage(prompt)])
    text = response.content if hasattr(response, "content") else str(response)

    return {
        "_plan_text": text,
        "_hypothesis": _extract_field(text, "HYPOTHESIS") or text[:200],
        "_code_sketch": _extract_field(text, "CODE SKETCH") or "(no sketch)",
    }


def execute_node(state: HCCState) -> dict:
    """Implements: Section 3.2.2 -- Code Execution.

    In the real ML-Master 2.0 the agent runs actual Python; the sandbox simulates
    a plausible observation with the LLM so it runs locally with zero data setup.
    """
    chat = _chat()
    prompt = EXECUTE_PROMPT.format(
        hypothesis=state.get("_hypothesis", ""),
        code_sketch=state.get("_code_sketch", ""),
    )
    response = chat.invoke([HumanMessage(prompt)])
    text = response.content if hasattr(response, "content") else str(response)

    event: TrajectoryEvent = {
        "trajectory_idx": state["current_trajectory_idx"],
        "hypothesis": state.get("_hypothesis", ""),
        "code_sketch": state.get("_code_sketch", ""),
        "observation": _extract_field(text, "OBSERVATION") or text[:300],
        "score": _extract_score(text),
    }

    next_idx = state["current_trajectory_idx"] + 1
    phase_done = next_idx >= state["trajectories_per_phase"]

    return {
        "current_phase_events": state.get("current_phase_events", []) + [event],
        "current_trajectory_idx": next_idx,
        "phase_done": phase_done,
    }


def p1_promote_node(state: HCCState) -> dict:
    """Implements: Section 3.4.3 + Appendix A.3 -- Context Promotion P1.

    Compresses the current phase's parallel trajectories into a single
    refined-knowledge entry kappa_p, then evicts L1.
    """
    events = state.get("current_phase_events", [])
    traj_block = "\n\n".join(
        f"Trajectory {e['trajectory_idx']}:\n"
        f"  hypothesis: {e['hypothesis']}\n"
        f"  sketch: {e['code_sketch']}\n"
        f"  observation: {e['observation']}\n"
        f"  score: {e['score']:.2f}"
        for e in events
    ) or "(no trajectories)"

    chat = _chat()
    prompt = P1_PROMOTE_PROMPT.format(
        task_description=state["task_description"],
        trajectories_block=traj_block,
    )
    response = chat.invoke([HumanMessage(prompt)])
    text = response.content if hasattr(response, "content") else str(response)

    kappa_p = text.strip()
    next_phase = state["current_phase_index"] + 1
    task_done = next_phase >= state["max_phases"]

    return {
        "refined_knowledge": state.get("refined_knowledge", []) + [kappa_p],
        # Paper: L1 is cleared at phase boundary after P1 writes to L2.
        "current_phase_events": [],
        "current_phase_index": next_phase,
        "current_trajectory_idx": 0,
        "phase_done": False,
        "task_done": task_done,
    }


def p2_promote_node(state: HCCState) -> dict:
    """Implements: Section 3.4.3 + Appendix A.3 -- Context Promotion P2.

    Distills all per-phase refined knowledge into one cross-task wisdom entry
    written to L3. Also picks the best-scoring hypothesis as the final solution.
    """
    refined_block = "\n\n".join(
        f"Phase {i}:\n{k}" for i, k in enumerate(state.get("refined_knowledge", []))
    ) or "(none)"

    chat = _chat()
    prompt = P2_PROMOTE_PROMPT.format(
        task_description=state["task_description"],
        refined_knowledge_block=refined_block,
    )
    response = chat.invoke([HumanMessage(prompt)])
    wisdom_text = (response.content if hasattr(response, "content") else str(response)).strip()

    descriptor = (
        (_extract_field(wisdom_text, "DATA SUMMARY") + " | " + _extract_field(wisdom_text, "MODEL SUMMARY")).strip(" |")
        or wisdom_text[:200]
    )

    embedder = _embed()
    embedding = embedder.embed_query(descriptor)

    new_entry: WisdomEntry = {
        "descriptor": descriptor,
        "wisdom_text": wisdom_text,
        "embedding": embedding,
    }

    # Pick the best event seen across all phases as the "final solution".
    # In the real system this would be the best actual code/model; here it's the best hypothesis.
    best_event_text = ""
    best_score = -1.0
    for k in state.get("refined_knowledge", []):
        match = re.search(r"performed best[^\n]*", k, re.IGNORECASE)
        if match and match.group(0) > best_event_text:
            best_event_text = match.group(0)
            best_score = 1.0
    final_solution = best_event_text or "(see refined knowledge for best-performing direction)"

    return {
        "new_wisdom": new_entry,
        "final_solution": final_solution,
        "prior_wisdom_store": state.get("prior_wisdom_store", []) + [new_entry],
    }


def route_after_execute(state: HCCState) -> str:
    """Conditional edge: continue trajectories within phase, or promote at phase boundary."""
    return "p1_promote" if state.get("phase_done") else "plan"


def route_after_p1(state: HCCState) -> str:
    """Conditional edge: start next phase, or task-level promotion if we hit max_phases."""
    return "p2_promote" if state.get("task_done") else "plan"
