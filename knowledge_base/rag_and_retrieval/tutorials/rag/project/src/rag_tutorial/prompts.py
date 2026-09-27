"""The generation prompt, shared by every retrieval experiment from chapter 03
onward. Keeping the wording constant means that when a later chapter's
scoreboard row differs from this chapter's, the difference is due to the
retriever, not to a different prompt.
"""

from __future__ import annotations

SYSTEM_PROMPT = (
    "Answer only from the provided excerpts. Cite as [paper_short_name §section]. "
    "If the excerpts do not contain the answer, say: I cannot answer this from the "
    "provided documents."
)


def format_context(chunks: list[tuple[str, str, str]]) -> str:
    """Render `(short_name, section, text)` triples as one citation-labelled block."""
    blocks = []
    for short_name, section, text in chunks:
        label = f"[{short_name} §{section}]" if section else f"[{short_name}]"
        blocks.append(f"{label}\n{text}")
    return "\n\n".join(blocks)


def build_messages(question: str, chunks: list[tuple[str, str, str]]) -> list[dict]:
    """Build the chat messages for one question given its retrieved `(short_name, section, text)` chunks."""
    context = format_context(chunks)
    user = f"Excerpts:\n{context}\n\nQuestion: {question}" if chunks else f"Excerpts: (none retrieved)\n\nQuestion: {question}"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
