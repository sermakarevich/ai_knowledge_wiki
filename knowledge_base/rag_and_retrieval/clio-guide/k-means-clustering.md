> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## K-Means Clustering

### Goal
Group similar embeddings into base-level clusters.

### CLIO's configuration
- **Algorithm:** Standard k-means on 768-dim embeddings
- **k selection:** Dynamic based on dataset size (exact formula withheld in paper for security reasons)
- **Cluster size:** Average ~100 conversations per cluster in their 100K run (implying k ~ 1000)

### Recommended k values

CLIO withheld their exact formula, but from their cost table we know: for 100K documents, they used ~1000 base clusters. This gives us a practical heuristic:

```
k ~ N / 100     (where N is number of documents)
```

Adjusted for your scale:

| N documents | Recommended k | Avg docs/cluster |
|-------------|---------------|------------------|
| 10,000 | 100-200 | 50-100 |
| 50,000 | 400-600 | 80-125 |
| 100,000 | 800-1200 | 80-125 |
| 500,000 | 3000-5000 | 100-170 |

### Code

```python
from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np

embeddings = np.load("step3_embeddings.npy")
N = len(embeddings)

# Choose k
k = max(50, N // 100)  # at least 50 clusters
print(f"Using k={k} for {N} documents")

# For N < 100K, use standard k-means
if N < 100_000:
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10,
        max_iter=300,
    )
    labels = kmeans.fit_predict(embeddings)
else:
    # For larger datasets, use MiniBatchKMeans (much faster, slightly worse)
    kmeans = MiniBatchKMeans(
        n_clusters=k,
        random_state=42,
        batch_size=10_000,
        n_init=3,
        max_iter=300,
    )
    labels = kmeans.fit_predict(embeddings)

centroids = kmeans.cluster_centers_

# Assign labels to documents
for i, doc in enumerate(documents):
    doc["cluster_id"] = int(labels[i])

# Save checkpoint
np.save("step4_labels.npy", labels)
np.save("step4_centroids.npy", centroids)

# Report cluster size distribution
from collections import Counter
sizes = Counter(labels)
print(f"Cluster sizes: min={min(sizes.values())}, max={max(sizes.values())}, "
      f"median={sorted(sizes.values())[len(sizes)//2]}")
```

### Filtering small clusters

CLIO removes clusters that are too small. Since you don't have privacy constraints, the threshold can be lower:

```python
MIN_CLUSTER_SIZE = 5  # CLIO uses higher thresholds for privacy

# Identify small clusters
small_clusters = {cid for cid, count in sizes.items() if count < MIN_CLUSTER_SIZE}
print(f"Removing {len(small_clusters)} clusters with <{MIN_CLUSTER_SIZE} documents")

# Reassign orphaned documents to nearest valid cluster
valid_centroids = {cid: centroids[cid] for cid in range(k) if cid not in small_clusters}
for i, doc in enumerate(documents):
    if doc["cluster_id"] in small_clusters:
        # Find nearest valid centroid
        dists = {cid: np.linalg.norm(embeddings[i] - c)
                 for cid, c in valid_centroids.items()}
        doc["cluster_id"] = min(dists, key=dists.get)
```

### Choosing k with the elbow method (optional)

If you want a data-driven k:

```python
from sklearn.metrics import silhouette_score

# Test a range (subsample for speed)
sample_idx = np.random.choice(N, min(10_000, N), replace=False)
sample_emb = embeddings[sample_idx]

scores = {}
for k_test in [50, 100, 200, 500, 1000, 2000]:
    if k_test >= len(sample_idx):
        continue
    km = MiniBatchKMeans(n_clusters=k_test, random_state=42, batch_size=5000)
    labels_test = km.fit_predict(sample_emb)
    scores[k_test] = silhouette_score(sample_emb, labels_test, sample_size=5000)
    print(f"k={k_test}: silhouette={scores[k_test]:.4f}")
```

---
