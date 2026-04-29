"""LangGraph pipeline wiring the HCC operators.

Topology:

    START -> prefetch -> plan -> execute -+-> plan            (if more trajectories)
                                          +-> p1_promote -+-> plan            (if more phases)
                                                          +-> p2_promote -> END
"""

from langgraph.graph import END, START, StateGraph

from src.nodes import (
    execute_node,
    p1_promote_node,
    p2_promote_node,
    plan_node,
    prefetch_node,
    route_after_execute,
    route_after_p1,
)
from src.state import HCCState


def build_graph():
    workflow = StateGraph(HCCState)

    workflow.add_node("prefetch", prefetch_node)
    workflow.add_node("plan", plan_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("p1_promote", p1_promote_node)
    workflow.add_node("p2_promote", p2_promote_node)

    workflow.add_edge(START, "prefetch")
    workflow.add_edge("prefetch", "plan")
    workflow.add_edge("plan", "execute")

    workflow.add_conditional_edges(
        "execute",
        route_after_execute,
        {"plan": "plan", "p1_promote": "p1_promote"},
    )
    workflow.add_conditional_edges(
        "p1_promote",
        route_after_p1,
        {"plan": "plan", "p2_promote": "p2_promote"},
    )

    workflow.add_edge("p2_promote", END)

    return workflow.compile()


graph = build_graph()
