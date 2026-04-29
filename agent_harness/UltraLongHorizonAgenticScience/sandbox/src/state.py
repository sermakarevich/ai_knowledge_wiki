"""Graph state for the HCC sandbox.

Maps to paper notation from Section 3 of ML-Master 2.0 (arxiv 2601.10402).
"""

from typing import TypedDict


class WisdomEntry(TypedDict):
    descriptor: str  # d_n -- compact task descriptor (DATA/MODEL summary)
    wisdom_text: str  # w_n -- the full DATA + MODEL SUMMARY text
    embedding: list[float]  # E(d_n) -- cached embedding for cosine retrieval


class TrajectoryEvent(TypedDict):
    trajectory_idx: int  # which parallel trajectory within the current phase
    hypothesis: str  # the research direction proposed by plan_node
    code_sketch: str  # pseudocode / summary of what was "executed"
    observation: str  # simulated outcome / metric / error
    score: float  # validation-like score in [0, 1]


class HCCState(TypedDict, total=False):
    # ---- Task inputs ----
    task_description: str  # tau -- user-provided task description
    user_instructions: str  # u_user

    # ---- L1 Evolving Experience (active phase only) ----
    # Raw events for the current phase. Cleared after P1 promotion.
    current_phase_events: list[TrajectoryEvent]
    current_phase_index: int  # p

    # ---- L2 Refined Knowledge (this task, across phases) ----
    # kappa_p for each completed phase p. One string per phase.
    refined_knowledge: list[str]

    # ---- L3 Prior Wisdom (cross-task, persistent) ----
    # Populated from examples/sample_data.py at runtime (simulates warm-up from 407 Kaggle comps).
    prior_wisdom_store: list[WisdomEntry]
    # What was pulled into context by Context Prefetch for THIS task.
    retrieved_wisdom: list[str]

    # ---- Control flow ----
    max_phases: int  # upper bound on how many phases the task will run
    trajectories_per_phase: int  # m * q in the paper (simplified to a single number here)
    current_trajectory_idx: int  # counter for trajectories within the active phase
    phase_done: bool  # true once current_trajectory_idx == trajectories_per_phase
    task_done: bool  # true once max_phases reached or early-stop condition met

    # ---- Outputs ----
    final_solution: str  # best hypothesis/code at the end of the task
    new_wisdom: WisdomEntry  # the L3 entry written by P2 at task end
