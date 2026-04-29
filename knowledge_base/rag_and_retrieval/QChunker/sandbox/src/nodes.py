"""Node functions for the QChunker LangGraph pipeline.

Each function implements one of the four specialized agents from
the paper's multi-agent debate framework.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from .state import QChunkerState, ChunkReview
from .prompts import (
    QUESTION_OUTLINE_PROMPT,
    TEXT_SEGMENTER_PROMPT,
    INTEGRITY_REVIEWER_PROMPT,
    KNOWLEDGE_COMPLETER_PROMPT,
)

MODEL_NAME = "llama3.2"


def _get_llm(temperature: float = 0.7) -> ChatOllama:
    return ChatOllama(model=MODEL_NAME, temperature=temperature)


def generate_question_outline(state: QChunkerState) -> dict:
    """Implements: Paper Section 3.2.1 -- Question Outline Generator (A_QG).

    Maps document D to structured question outline Q by simulating
    domain expert analysis. Questions serve as semantic priors for
    downstream segmentation.
    """
    llm = _get_llm(temperature=0.7)
    prompt = QUESTION_OUTLINE_PROMPT.format(document=state["document"])
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"question_outline": response.content}


def segment_text(state: QChunkerState) -> dict:
    """Implements: Paper Section 3.2.2 -- Text Segmenter (A_SEG).

    Uses the question outline Q as a semantic prior to generate
    an optimal text segmentation. In the full paper, this involves
    multi-path sampling + ChunkScore evaluation; here we use a
    single-pass segmentation guided by the outline.
    """
    llm = _get_llm(temperature=0.3)
    prompt = TEXT_SEGMENTER_PROMPT.format(
        question_outline=state["question_outline"],
        document=state["document"],
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    raw_chunks = response.content.split("===CHUNK===")
    chunks = [c.strip() for c in raw_chunks if c.strip()]
    return {"chunks": chunks}


def review_chunks(state: QChunkerState) -> dict:
    """Implements: Paper Section 3.2.3 -- Integrity Reviewer (A_IR).

    For each chunk c_i, performs comparative analysis against the full
    document D to identify missing knowledge points M_i and determine
    if completion is needed (b_i).
    """
    llm = _get_llm(temperature=0.2)
    reviews: list[ChunkReview] = []

    for chunk in state["chunks"]:
        prompt = INTEGRITY_REVIEWER_PROMPT.format(
            document=state["document"],
            chunk=chunk,
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        text = response.content

        needs_completion = "NEEDS_COMPLETION: YES" in text.upper()
        missing = []
        if needs_completion and "MISSING_KNOWLEDGE:" in text:
            lines = text.split("MISSING_KNOWLEDGE:")[-1].strip().split("\n")
            missing = [
                line.lstrip("- ").strip()
                for line in lines
                if line.strip() and line.strip() != "-"
            ]

        reviews.append(ChunkReview(
            chunk=chunk,
            missing_knowledge=missing,
            needs_completion=needs_completion,
        ))

    return {"chunk_reviews": reviews}


def complete_knowledge(state: QChunkerState) -> dict:
    """Implements: Paper Section 3.2.4 -- Knowledge Completer (A_KC).

    For each chunk where b_i = True, performs two-stage completion:
    Stage 1: Verify/filter missing knowledge points (implicit in prompt)
    Stage 2: Seamlessly rewrite chunk with integrated knowledge.
    Chunks with b_i = False pass through unchanged.
    """
    llm = _get_llm(temperature=0.3)
    completed: list[str] = []

    for review in state["chunk_reviews"]:
        if not review["needs_completion"] or not review["missing_knowledge"]:
            completed.append(review["chunk"])
            continue

        missing_str = "\n".join(f"- {m}" for m in review["missing_knowledge"])
        prompt = KNOWLEDGE_COMPLETER_PROMPT.format(
            document=state["document"],
            chunk=review["chunk"],
            missing_knowledge=missing_str,
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        completed.append(response.content)

    return {"completed_chunks": completed}
