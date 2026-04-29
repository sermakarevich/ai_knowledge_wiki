"""LangGraph definition for the QChunker pipeline.

Wires the four agents into a sequential graph matching the paper's
pipeline: A_QG → A_SEG → A_IR → A_KC.

The full paper uses multi-path sampling and ChunkScore-based selection
in the segmentation step. This sandbox simplifies to a single-pass
pipeline to demonstrate the core idea of question-aware chunking
with knowledge completion.
"""

from langgraph.graph import StateGraph, START, END

from .state import QChunkerState
from .nodes import (
    generate_question_outline,
    segment_text,
    review_chunks,
    complete_knowledge,
)


def build_graph() -> StateGraph:
    builder = StateGraph(QChunkerState)

    builder.add_node("generate_questions", generate_question_outline)
    builder.add_node("segment_text", segment_text)
    builder.add_node("review_chunks", review_chunks)
    builder.add_node("complete_knowledge", complete_knowledge)

    builder.add_edge(START, "generate_questions")
    builder.add_edge("generate_questions", "segment_text")
    builder.add_edge("segment_text", "review_chunks")
    builder.add_edge("review_chunks", "complete_knowledge")
    builder.add_edge("complete_knowledge", END)

    return builder.compile()


graph = build_graph()
