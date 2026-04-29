"""LangGraph wiring for the Clio pipeline.

Linear flow:
  extract_facets -> cluster_conversations -> describe_clusters
    -> audit_privacy -> build_hierarchy -> generate_report
"""

from langgraph.graph import END, StateGraph

from .nodes import (
    audit_privacy,
    build_hierarchy,
    cluster_conversations,
    describe_clusters,
    extract_facets,
    generate_report,
)
from .state import ClioState

builder = StateGraph(ClioState)

builder.add_node("extract_facets", extract_facets)
builder.add_node("cluster_conversations", cluster_conversations)
builder.add_node("describe_clusters", describe_clusters)
builder.add_node("audit_privacy", audit_privacy)
builder.add_node("build_hierarchy", build_hierarchy)
builder.add_node("generate_report", generate_report)

builder.set_entry_point("extract_facets")
builder.add_edge("extract_facets", "cluster_conversations")
builder.add_edge("cluster_conversations", "describe_clusters")
builder.add_edge("describe_clusters", "audit_privacy")
builder.add_edge("audit_privacy", "build_hierarchy")
builder.add_edge("build_hierarchy", "generate_report")
builder.add_edge("generate_report", END)

graph = builder.compile()
