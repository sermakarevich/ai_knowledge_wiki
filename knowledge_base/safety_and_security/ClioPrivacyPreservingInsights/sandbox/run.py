"""Entry point for the Clio sandbox pipeline.

Runs the full LangGraph pipeline on sample conversations and prints
each stage's output with clear headers.
"""

import sys


def main() -> None:
    try:
        from examples.sample_data import SAMPLE_CONVERSATIONS
        from src.graph import graph
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you ran 'uv sync' first.")
        sys.exit(1)

    initial_state = {"conversations": SAMPLE_CONVERSATIONS}

    print("=" * 60)
    print("CLIO SANDBOX -- Privacy-Preserving Conversation Analysis")
    print("=" * 60)
    print(f"\nLoaded {len(SAMPLE_CONVERSATIONS)} sample conversations.\n")

    try:
        # Stream through the graph to show progress per stage
        for step in graph.stream(initial_state, stream_mode="updates"):
            for node_name, update in step.items():
                print(f"\n{'─' * 50}")
                print(f"  Stage: {node_name}")
                print(f"{'─' * 50}")

                if node_name == "extract_facets":
                    for i, facet in enumerate(update["facets"]):
                        print(f"  [{i}] {facet}")

                elif node_name == "cluster_conversations":
                    assignments = update["cluster_assignments"]
                    print(f"  Clusters: {len(set(assignments))}")
                    print(f"  Assignments: {assignments}")

                elif node_name == "describe_clusters":
                    for desc in update["cluster_descriptions"]:
                        print(f"  Cluster {desc['cluster_id']}: {desc['title']}")
                        print(f"    {desc['description']}")
                        print(f"    ({desc['member_count']} members)")

                elif node_name == "audit_privacy":
                    for result in update["privacy_audit_results"]:
                        status = "PASS" if result["passed"] else "FAIL"
                        print(f"  Cluster {result['cluster_id']}: [{status}] {result['reason']}")

                elif node_name == "build_hierarchy":
                    for cat in update["hierarchy"]:
                        print(f"  {cat['category']}: clusters {cat['cluster_ids']}")
                        print(f"    {cat['summary']}")

                elif node_name == "generate_report":
                    print(update["final_report"])

    except Exception as e:
        error_msg = str(e).lower()
        if "connection" in error_msg or "refused" in error_msg or "ollama" in error_msg:
            print("\n[ERROR] Could not connect to Ollama.")
            print("Make sure Ollama is running and you have pulled the model:")
            print("  ollama serve")
            print("  ollama pull llama3.2")
        else:
            print(f"\n[ERROR] {e}")
            raise


if __name__ == "__main__":
    main()
