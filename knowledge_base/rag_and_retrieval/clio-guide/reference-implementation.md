> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Complete Reference Implementation

Save this as `clio_pipeline.py` and run end-to-end:

```python
#!/usr/bin/env python3
"""
CLIO-style document segmentation pipeline.
Usage: python clio_pipeline.py --input_dir ./documents --output_dir ./results
"""

import argparse
import asyncio
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from anthropic import AsyncAnthropic, Anthropic
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

# ─── Configuration ───────────────────────────────────────────────────────────

EXTRACTION_MODEL = "claude-3-5-haiku-20241022"
DESCRIPTION_MODEL = "claude-sonnet-4-20250514"
EMBEDDING_MODEL = "all-mpnet-base-v2"
MAX_DOC_CHARS = 8000
MAX_CONCURRENT = 50
N_TOP_CLUSTERS = 10
N_HIERARCHY_LEVELS = 3
MIN_CLUSTER_SIZE = 5


# ─── Step 1: Load and preprocess ─────────────────────────────────────────────

def load_documents(input_dir: str) -> list[dict]:
    docs = []
    for p in Path(input_dir).rglob("*"):
        if p.is_file() and p.suffix in {".txt", ".md", ".csv", ".json", ".html"}:
            text = p.read_text(encoding="utf-8", errors="replace")
            if len(text) > MAX_DOC_CHARS:
                half = MAX_DOC_CHARS // 2
                text = text[:half] + "\n[...]\n" + text[-half:]
            docs.append({
                "id": hashlib.sha256(str(p).encode()).hexdigest()[:16],
                "path": str(p),
                "text": text,
            })
    return docs


# ─── Step 2: Extract summaries ───────────────────────────────────────────────

EXTRACTION_PROMPT = """The following is a document:
<document>
{document_text}
</document>

What is this document about? What is its main topic and purpose?
Be descriptive. Answer in at most two sentences inside <answer> tags.
<answer>"""

async def extract_summaries(documents: list[dict]) -> list[dict]:
    client = AsyncAnthropic()
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def extract_one(doc):
        async with sem:
            resp = await client.messages.create(
                model=EXTRACTION_MODEL,
                max_tokens=200,
                temperature=0.2,
                messages=[{"role": "user", "content":
                    EXTRACTION_PROMPT.format(document_text=doc["text"])}],
            )
            raw = resp.content[0].text
            match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
            doc["summary"] = match.group(1).strip() if match else raw.strip()
            return doc

    return await tqdm_asyncio.gather(
        *[extract_one(d) for d in documents], desc="Extracting"
    )


# ─── Step 3: Embed ───────────────────────────────────────────────────────────

def embed_summaries(documents: list[dict]) -> np.ndarray:
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.encode(
        [d["summary"] for d in documents],
        show_progress_bar=True,
        batch_size=256,
        normalize_embeddings=True,
    )


# ─── Step 4: Cluster ─────────────────────────────────────────────────────────

def cluster_documents(embeddings: np.ndarray, documents: list[dict]):
    N = len(embeddings)
    k = max(50, N // 100)
    print(f"K-means with k={k}")

    cls = (MiniBatchKMeans if N > 100_000 else KMeans)(
        n_clusters=k, random_state=42, n_init=3 if N > 100_000 else 10,
    )
    labels = cls.fit_predict(embeddings)

    for i, doc in enumerate(documents):
        doc["cluster_id"] = int(labels[i])

    return labels, cls.cluster_centers_


# ─── Step 5: Describe clusters ───────────────────────────────────────────────

# (See full prompts from Step 5 section above -- omitted for brevity)


# ─── Step 6: Build hierarchy ─────────────────────────────────────────────────

# (See full implementation from Step 6 section above -- omitted for brevity)


# ─── Step 7: Visualize ───────────────────────────────────────────────────────

def visualize(embeddings, documents, cluster_descriptions, output_dir):
    import umap
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.0, metric="cosine", random_state=42)
    coords = reducer.fit_transform(embeddings)

    df = pd.DataFrame({
        "x": coords[:, 0], "y": coords[:, 1],
        "cluster": [cluster_descriptions[d["cluster_id"]]["name"] for d in documents],
        "summary": [d["summary"][:100] for d in documents],
    })

    import plotly.express as px
    fig = px.scatter(df, x="x", y="y", color="cluster", hover_data=["summary"],
                     width=1200, height=800)
    fig.update_traces(marker=dict(size=3, opacity=0.5))
    fig.update_layout(showlegend=False)
    fig.write_html(f"{output_dir}/map.html")
    print(f"Map saved to {output_dir}/map.html")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", default="./clio_results")
    args = parser.parse_args()

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    # Step 1
    print("Loading documents...")
    documents = load_documents(args.input_dir)
    print(f"  {len(documents)} documents loaded")

    # Step 2
    print("Extracting summaries...")
    documents = asyncio.run(extract_summaries(documents))
    with open(f"{args.output_dir}/summaries.jsonl", "w") as f:
        for d in documents:
            f.write(json.dumps({"id": d["id"], "path": d["path"],
                                "summary": d["summary"]}) + "\n")

    # Step 3
    print("Embedding...")
    embeddings = embed_summaries(documents)
    np.save(f"{args.output_dir}/embeddings.npy", embeddings)

    # Step 4
    print("Clustering...")
    labels, centroids = cluster_documents(embeddings, documents)
    np.save(f"{args.output_dir}/labels.npy", labels)

    # Step 5 (describe_cluster from above)
    print("Describing clusters...")
    # ... invoke describe_cluster for each unique cluster_id ...

    # Step 6 (build_hierarchy from above)
    print("Building hierarchy...")
    # ... invoke build_hierarchy ...

    # Step 7
    print("Visualizing...")
    # visualize(embeddings, documents, cluster_descriptions, args.output_dir)

    print("Done!")


if __name__ == "__main__":
    main()
```
