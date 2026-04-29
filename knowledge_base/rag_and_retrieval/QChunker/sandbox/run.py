"""Entry point for QChunker sandbox.

Runs the full four-agent pipeline on a sample document and prints
intermediate state at each stage so you can see the pipeline in action.
"""

import sys

from examples.sample_data import SAMPLE_DOCUMENT
from src.graph import graph


DIVIDER = "=" * 60


def print_stage(title: str, content: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)
    print(content)


def main() -> None:
    print("QChunker Sandbox -- Question-Aware Text Chunking Pipeline")
    print(f"Document length: {len(SAMPLE_DOCUMENT)} characters\n")

    try:
        # Stream through the graph to show intermediate state
        for event in graph.stream(
            {"document": SAMPLE_DOCUMENT},
            stream_mode="updates",
        ):
            for node_name, state_update in event.items():
                if node_name == "generate_questions":
                    print_stage(
                        "Stage 1: Question Outline (A_QG)",
                        state_update["question_outline"],
                    )

                elif node_name == "segment_text":
                    chunks = state_update["chunks"]
                    # print_stage(
                    #     f"Stage 2: Text Segmentation (A_SEG) -- {len(chunks)} chunks",
                    #     "\n---\n".join(
                    #         f"[Chunk {i+1}] {c[:120]}..."
                    #         if len(c) > 120 else f"[Chunk {i+1}] {c}"
                    #         for i, c in enumerate(chunks)
                    #     ),
                    # )
                    print_stage(
                        f"Stage 2: Text Segmentation (A_SEG) -- {len(chunks)} chunks",
                        "\n---\n".join(
                            f"[Chunk {i+1}] {c}..." for i, c in enumerate(chunks)
                        ),
                    )

                elif node_name == "review_chunks":
                    reviews = state_update["chunk_reviews"]
                    lines = []
                    for i, r in enumerate(reviews):
                        status = "NEEDS COMPLETION" if r["needs_completion"] else "OK"
                        lines.append(f"[Chunk {i+1}] {status}")
                        for m in r["missing_knowledge"]:
                            lines.append(f"  - Missing: {m}")
                    print_stage(
                        "Stage 3: Integrity Review (A_IR)",
                        "\n".join(lines),
                    )

                elif node_name == "complete_knowledge":
                    completed = state_update["completed_chunks"]
                    print_stage(
                        f"Stage 4: Knowledge Completion (A_KC) -- {len(completed)} final chunks",
                        "\n\n---\n\n".join(
                            f"[Final Chunk {i+1}]\n{c}"
                            for i, c in enumerate(completed)
                        ),
                    )

    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "ConnectError" in error_msg:
            print(
                "\nError: Cannot connect to Ollama. Make sure it's running:\n"
                "  1. Install Ollama: https://ollama.ai\n"
                "  2. Pull the model: ollama pull llama3.2\n"
                "  3. Start Ollama: ollama serve\n"
                "  4. Re-run: uv run python run.py",
                file=sys.stderr,
            )
        else:
            print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
