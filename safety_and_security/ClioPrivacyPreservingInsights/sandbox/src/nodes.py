"""Node functions for the Clio LangGraph pipeline.

Each node takes the full state dict and returns a partial update.
LLM calls use ChatOllama (llama3.2) with temperature=0 for reproducibility.
"""

import json
import re

import numpy as np
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from .prompts import (
    CLUSTER_DESCRIPTION_PROMPT,
    FACET_EXTRACTION_PROMPT,
    HIERARCHY_PROMPT,
    PRIVACY_AUDIT_PROMPT,
)
from .state import ClioState

llm = ChatOllama(model="llama3.2", temperature=0)


def _format_conversation(conv: dict) -> str:
    """Flatten a conversation dict into a readable string."""
    lines = []
    for msg in conv["messages"]:
        role = msg["role"].upper()
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section 3.1 -- Facet Extraction
# ---------------------------------------------------------------------------

def extract_facets(state: ClioState) -> dict:
    """Call the LLM once per conversation to extract a PII-free topic facet."""
    facets: list[str] = []
    for conv in state["conversations"]:
        formatted = _format_conversation(conv)
        prompt = FACET_EXTRACTION_PROMPT.format(conversation=formatted)
        response = llm.invoke([HumanMessage(content=prompt)])
        facets.append(response.content.strip())
    return {"facets": facets}


# ---------------------------------------------------------------------------
# Section 3.2 -- Clustering (TF-IDF + KMeans as a simple proxy for
# real embedding-based clustering)
# ---------------------------------------------------------------------------

def cluster_conversations(state: ClioState) -> dict:
    """Vectorize facets with TF-IDF and cluster with KMeans."""
    facets = state["facets"]
    n_clusters = min(5, len(facets))  # keep k reasonable for small datasets

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(facets)
    embeddings = tfidf_matrix.toarray().tolist()

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(tfidf_matrix)

    return {
        "embeddings": embeddings,
        "cluster_assignments": labels.tolist(),
    }


# ---------------------------------------------------------------------------
# Section 3.3 -- Cluster Description
# ---------------------------------------------------------------------------

def describe_clusters(state: ClioState) -> dict:
    """For each cluster, sample its facets and ask the LLM for a title + description."""
    facets = state["facets"]
    assignments = state["cluster_assignments"]
    unique_clusters = sorted(set(assignments))

    descriptions: list[dict] = []
    for cid in unique_clusters:
        cluster_facets = [f for f, a in zip(facets, assignments) if a == cid]
        facets_text = "\n".join(f"- {f}" for f in cluster_facets)
        prompt = CLUSTER_DESCRIPTION_PROMPT.format(facets=facets_text)
        response = llm.invoke([HumanMessage(content=prompt)])

        # Parse the structured response
        text = response.content.strip()
        title = ""
        description = ""
        for line in text.splitlines():
            if line.upper().startswith("TITLE:"):
                title = line.split(":", 1)[1].strip()
            elif line.upper().startswith("DESCRIPTION:"):
                description = line.split(":", 1)[1].strip()

        descriptions.append({
            "cluster_id": cid,
            "title": title or text[:50],
            "description": description or text,
            "member_count": len(cluster_facets),
        })

    return {"cluster_descriptions": descriptions}


# ---------------------------------------------------------------------------
# Section 3.4 -- Privacy Audit
# ---------------------------------------------------------------------------

def audit_privacy(state: ClioState) -> dict:
    """Run a separate LLM pass to check each cluster description for PII."""
    results: list[dict] = []
    for desc in state["cluster_descriptions"]:
        prompt = PRIVACY_AUDIT_PROMPT.format(
            title=desc["title"],
            description=desc["description"],
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        text = response.content.strip()

        passed = True
        reason = ""
        for line in text.splitlines():
            if line.upper().startswith("PASSED:"):
                val = line.split(":", 1)[1].strip().lower()
                passed = val == "true"
            elif line.upper().startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()

        results.append({
            "cluster_id": desc["cluster_id"],
            "passed": passed,
            "reason": reason or text,
        })

    return {"privacy_audit_results": results}


# ---------------------------------------------------------------------------
# Section 3.4 -- Hierarchy Building
# ---------------------------------------------------------------------------

def build_hierarchy(state: ClioState) -> dict:
    """Ask the LLM to group clusters into higher-level categories."""
    clusters_text = "\n".join(
        f"Cluster {d['cluster_id']}: {d['title']} -- {d['description']}"
        for d in state["cluster_descriptions"]
    )
    prompt = HIERARCHY_PROMPT.format(clusters=clusters_text)
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    # Parse structured response into a list of category dicts
    hierarchy: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        line_stripped = line.strip()
        if line_stripped.upper().startswith("CATEGORY:"):
            if current is not None:
                hierarchy.append(current)
            current = {
                "category": line_stripped.split(":", 1)[1].strip(),
                "cluster_ids": [],
                "summary": "",
            }
        elif line_stripped.upper().startswith("CLUSTERS:") and current is not None:
            raw = line_stripped.split(":", 1)[1].strip()
            current["cluster_ids"] = [
                int(x.strip()) for x in re.findall(r"\d+", raw)
            ]
        elif line_stripped.upper().startswith("SUMMARY:") and current is not None:
            current["summary"] = line_stripped.split(":", 1)[1].strip()
    if current is not None:
        hierarchy.append(current)

    return {"hierarchy": hierarchy}


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(state: ClioState) -> dict:
    """Assemble a human-readable summary of the full analysis."""
    lines = [
        "=" * 60,
        "CLIO ANALYSIS REPORT",
        "=" * 60,
        "",
        f"Conversations analyzed: {len(state['conversations'])}",
        f"Facets extracted: {len(state['facets'])}",
        f"Clusters formed: {len(state['cluster_descriptions'])}",
        "",
        "-" * 40,
        "CLUSTERS",
        "-" * 40,
    ]
    for desc in state["cluster_descriptions"]:
        audit = next(
            (a for a in state["privacy_audit_results"] if a["cluster_id"] == desc["cluster_id"]),
            None,
        )
        privacy_status = "PASSED" if (audit and audit["passed"]) else "FLAGGED"
        lines.append(f"\n  Cluster {desc['cluster_id']}: {desc['title']}")
        lines.append(f"    Members: {desc['member_count']}")
        lines.append(f"    Description: {desc['description']}")
        lines.append(f"    Privacy audit: {privacy_status}")
        if audit and not audit["passed"]:
            lines.append(f"    Audit reason: {audit['reason']}")

    lines.extend([
        "",
        "-" * 40,
        "HIERARCHY",
        "-" * 40,
    ])
    for cat in state.get("hierarchy", []):
        lines.append(f"\n  {cat['category']}")
        lines.append(f"    Clusters: {cat['cluster_ids']}")
        lines.append(f"    Summary: {cat['summary']}")

    lines.append("\n" + "=" * 60)
    report = "\n".join(lines)
    return {"final_report": report}
