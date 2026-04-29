> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Cluster Description Generation

### Goal
Generate a descriptive title and 2-sentence summary for each cluster. This is the most important LLM step -- it determines the quality of your taxonomy.

### CLIO's exact configuration
- **Model:** Claude 3.5 Sonnet (`claude-3-5-sonnet-20240620`), temperature 1.0
- **Samples:** 50 summaries from WITHIN the cluster + 50 summaries CLOSEST to centroid but NOT in the cluster (contrastive)
- **Key technique:** The contrastive samples tell the LLM what to differentiate from

### Why contrastive samples matter

Without contrastive samples, a cluster of "Python web development" documents might get a vague label like "Software development." With contrastive samples from nearby clusters (e.g., "Python data science" and "JavaScript web development"), the LLM is forced to identify what is *distinctive*: "Python web application development using Django and Flask."

### Code

```python
import random
from anthropic import Anthropic

client = Anthropic()

CLUSTER_DESCRIPTION_PROMPT = """You are tasked with summarizing a group of related statements into a short, precise, and accurate description and name. Your goal is to create a concise summary that captures the essence of these statements and distinguishes them from other similar groups of statements.

Summarize all the statements into a clear, precise, two-sentence description in the past tense. Your summary should be specific to this group and distinguish it from the contrastive answers of the other groups.

After creating the summary, generate a short name for the group of statements. This name should be at most ten words long (perhaps less) and be specific but also reflective of most of the statements (rather than reflecting only one or two). The name should distinguish this group from the contrastive examples. Be as descriptive as possible.

Present your output in the following format:
<summary> [Insert your two-sentence summary here] </summary>
<name> [Insert your generated short name here] </name>

Below are the related statements:
<answers>
{answers}
</answers>

For context, here are statements from nearby groups that are NOT part of the group you're summarizing:
<contrastive_answers>
{contrastive_answers}
</contrastive_answers>

Do not elaborate beyond what you say in the tags. Remember to analyze both the statements and the contrastive statements carefully to ensure your summary and name accurately represent the specific group while distinguishing it from others."""


def get_contrastive_samples(
    cluster_id: int,
    embeddings: np.ndarray,
    labels: np.ndarray,
    centroids: np.ndarray,
    n_samples: int = 50,
) -> list[int]:
    """Get indices of documents closest to centroid but NOT in the cluster."""
    centroid = centroids[cluster_id]
    # Distance from every point to this centroid
    dists = np.linalg.norm(embeddings - centroid, axis=1)
    # Mask in-cluster documents with infinite distance
    dists[labels == cluster_id] = np.inf
    # Get closest n_samples
    return np.argsort(dists)[:n_samples].tolist()


def describe_cluster(
    cluster_id: int,
    documents: list[dict],
    embeddings: np.ndarray,
    labels: np.ndarray,
    centroids: np.ndarray,
) -> dict:
    """Generate name and description for a cluster using contrastive prompting."""
    # Get in-cluster documents
    in_cluster = [doc for doc in documents if doc["cluster_id"] == cluster_id]
    # Sample up to 50
    in_sample = random.sample(in_cluster, min(50, len(in_cluster)))
    answers = "\n".join(f"- {doc['summary']}" for doc in in_sample)

    # Get contrastive samples
    contrast_indices = get_contrastive_samples(
        cluster_id, embeddings, labels, centroids, n_samples=50
    )
    contrastive_answers = "\n".join(
        f"- {documents[i]['summary']}" for i in contrast_indices
    )

    prompt = CLUSTER_DESCRIPTION_PROMPT.format(
        answers=answers,
        contrastive_answers=contrastive_answers,
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    name_match = re.search(r"<name>(.*?)</name>", raw, re.DOTALL)
    summary_match = re.search(r"<summary>(.*?)</summary>", raw, re.DOTALL)

    return {
        "cluster_id": cluster_id,
        "name": name_match.group(1).strip() if name_match else f"Cluster {cluster_id}",
        "description": summary_match.group(1).strip() if summary_match else "",
        "size": len(in_cluster),
    }


# Generate descriptions for all clusters
unique_clusters = sorted(set(doc["cluster_id"] for doc in documents))
cluster_descriptions = {}

for cid in tqdm(unique_clusters, desc="Describing clusters"):
    cluster_descriptions[cid] = describe_cluster(
        cid, documents, embeddings, labels, centroids
    )

# Save checkpoint
with open("step5_cluster_descriptions.json", "w") as f:
    json.dump(cluster_descriptions, f, indent=2)
```

### Async version for speed

```python
async def describe_cluster_async(cluster_id, documents, embeddings, labels, centroids):
    async with SEMAPHORE:  # reuse semaphore from step 2
        # ... same logic as above but with async client ...
        response = await async_client.messages.create(...)
        return parse_response(response)

# Run all cluster descriptions in parallel
tasks = [describe_cluster_async(cid, ...) for cid in unique_clusters]
cluster_descriptions = await asyncio.gather(*tasks)
```

---
