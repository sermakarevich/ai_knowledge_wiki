"""Graph state for the QChunker pipeline.

Maps to the paper's composite chunking formulation F = f_com ∘ f_seg:
- document → question_outline → chunks (f_seg phase)
- chunks → chunk_reviews → completed_chunks (f_com phase)
"""

from typing import TypedDict


class ChunkReview(TypedDict):
    """Output of the Integrity Reviewer (A_IR) for a single chunk.

    Fields:
        chunk: The original chunk text
        missing_knowledge: List of identified missing knowledge points (M_i)
        needs_completion: Whether the chunk needs knowledge completion (b_i)
    """
    chunk: str
    missing_knowledge: list[str]
    needs_completion: bool


class QChunkerState(TypedDict):
    """Full pipeline state flowing through the LangGraph.

    The pipeline follows four stages matching the paper's four agents:
    1. A_QG: document → question_outline
    2. A_SEG: (document, question_outline) → chunks
    3. A_IR: (chunks, document) → chunk_reviews
    4. A_KC: (chunk_reviews, document) → completed_chunks
    """
    # Input
    document: str

    # After A_QG (Question Outline Generator)
    question_outline: str

    # After A_SEG (Text Segmenter)
    chunks: list[str]

    # After A_IR (Integrity Reviewer)
    chunk_reviews: list[ChunkReview]

    # After A_KC (Knowledge Completer) -- final output
    completed_chunks: list[str]
