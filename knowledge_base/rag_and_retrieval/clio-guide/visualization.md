> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## 2D Projection and Visualization

### CLIO's exact configuration
- **Algorithm:** UMAP
- **Parameters:** `n_neighbors=15, min_dist=0, metric="cosine"`

### Code

```python
import umap
import plotly.express as px
import pandas as pd

# Run UMAP
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
)
coords_2d = reducer.fit_transform(embeddings)

# Build dataframe for visualization
df = pd.DataFrame({
    "x": coords_2d[:, 0],
    "y": coords_2d[:, 1],
    "cluster_id": [doc["cluster_id"] for doc in documents],
    "summary": [doc["summary"][:100] for doc in documents],
    "cluster_name": [
        cluster_descriptions[doc["cluster_id"]]["name"] for doc in documents
    ],
})

# Interactive scatter plot
fig = px.scatter(
    df,
    x="x", y="y",
    color="cluster_name",
    hover_data=["summary"],
    title="Document Map (CLIO-style)",
    width=1200,
    height=800,
)
fig.update_traces(marker=dict(size=3, opacity=0.6))
fig.update_layout(showlegend=False)  # too many clusters for legend
fig.write_html("document_map.html")
fig.show()
```

### Cluster-level map (cleaner)

```python
# Compute cluster centroids in 2D space
cluster_centers_2d = {}
for cid in cluster_descriptions:
    mask = np.array([doc["cluster_id"] == cid for doc in documents])
    if mask.any():
        cluster_centers_2d[cid] = coords_2d[mask].mean(axis=0)

df_clusters = pd.DataFrame([
    {
        "x": cluster_centers_2d[cid][0],
        "y": cluster_centers_2d[cid][1],
        "name": cluster_descriptions[cid]["name"],
        "size": cluster_descriptions[cid]["size"],
        "description": cluster_descriptions[cid]["description"],
    }
    for cid in cluster_descriptions if cid in cluster_centers_2d
])

fig = px.scatter(
    df_clusters,
    x="x", y="y",
    size="size",
    hover_data=["name", "description", "size"],
    title="Cluster Map",
    width=1200,
    height=800,
)
fig.write_html("cluster_map.html")
```

### Tree view

```python
def print_hierarchy_tree(hierarchy: dict, indent: int = 0):
    """Print the hierarchy as a text tree."""
    top_level_key = f"level_{max(int(k.split('_')[1]) for k in hierarchy)}"
    top_clusters = hierarchy[top_level_key]

    for pid, parent in sorted(top_clusters.items(), key=lambda x: -x[1]["size"]):
        print(f"{'  ' * indent}{parent['name']} ({parent['size']} docs)")
        if "children" in parent:
            for child_id in parent["children"]:
                # Find child in the level below
                for level_key in hierarchy:
                    if child_id in hierarchy[level_key]:
                        child = hierarchy[level_key][child_id]
                        print(f"{'  ' * (indent+1)}- {child['name']} ({child['size']} docs)")
                        break

print_hierarchy_tree(hierarchy)
```
