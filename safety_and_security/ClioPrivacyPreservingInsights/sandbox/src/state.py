"""State definition for the Clio analysis pipeline.

The pipeline state flows through stages mirroring the paper:
  conversations -> facets -> embeddings -> clusters -> descriptions -> audit -> hierarchy -> report
"""

from typing import TypedDict


class ClioState(TypedDict, total=False):
    # Raw conversation dicts with user/assistant turns
    conversations: list[dict]
    # One facet string per conversation -- PII-free topic summary (Section 3.1)
    facets: list[str]
    # Float vectors from TF-IDF (proxy for real embeddings, Section 3.2)
    embeddings: list[list[float]]
    # Cluster label per conversation
    cluster_assignments: list[int]
    # Title + summary per cluster (Section 3.3)
    cluster_descriptions: list[dict]
    # Privacy audit verdict per cluster (Section 3.4)
    privacy_audit_results: list[dict]
    # Multi-level taxonomy grouping clusters into categories (Section 3.4)
    hierarchy: list[dict]
    # Human-readable final output
    final_report: str
