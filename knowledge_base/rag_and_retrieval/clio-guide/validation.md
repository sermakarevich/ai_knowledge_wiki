> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Validation and Quality Checks

### 1. Summary accuracy (spot check)

Manually review 50-100 random document-summary pairs:

```python
sample = random.sample(documents, 100)
for doc in sample:
    print(f"=== Document: {doc['path']} ===")
    print(f"Summary: {doc['summary']}")
    print(f"Cluster: {cluster_descriptions[doc['cluster_id']]['name']}")
    print()
    # Rate: accurate / partially accurate / wrong
```

Target: >90% accuracy (CLIO achieved 96%).

### 2. Cluster coherence

For each cluster, check that documents actually belong together:

```python
for cid in random.sample(list(cluster_descriptions.keys()), 20):
    desc = cluster_descriptions[cid]
    members = [doc for doc in documents if doc["cluster_id"] == cid]
    sample = random.sample(members, min(5, len(members)))
    print(f"\n=== {desc['name']} ({desc['size']} docs) ===")
    print(f"Description: {desc['description']}")
    for doc in sample:
        print(f"  - {doc['summary']}")
```

Target: >95% of sampled documents match the cluster description (CLIO achieved 97%).

### 3. Reconstruction test (if you have labeled data)

If you have any ground-truth labels for a subset:

```python
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

ari = adjusted_rand_score(true_labels, predicted_labels)
nmi = normalized_mutual_info_score(true_labels, predicted_labels)
print(f"ARI: {ari:.3f}, NMI: {nmi:.3f}")
```

### 4. Hierarchy sanity check

Verify each parent actually encompasses its children:

```python
for pid, parent in hierarchy["level_2"].items():
    print(f"\nParent: {parent['name']}")
    for child_id in parent["children"][:5]:
        child = hierarchy["level_1"].get(child_id, hierarchy["level_0"].get(child_id))
        if child:
            print(f"  Child: {child['name']}")
```
