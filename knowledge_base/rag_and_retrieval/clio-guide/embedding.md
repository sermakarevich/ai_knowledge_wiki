> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Embedding

### Goal
Convert each summary into a 768-dimensional dense vector for clustering.

### CLIO's exact configuration
- **Model:** `all-mpnet-base-v2` from sentence-transformers
- **Dimensionality:** 768
- **Input:** The extracted English summary text (not the raw document)

### Code

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-mpnet-base-v2")

summaries = [doc["summary"] for doc in documents]
embeddings = model.encode(
    summaries,
    show_progress_bar=True,
    batch_size=256,       # increase if you have GPU
    normalize_embeddings=True,  # important for cosine-based k-means
)

# Save checkpoint
np.save("step3_embeddings.npy", embeddings)
print(f"Embeddings shape: {embeddings.shape}")  # (N, 768)
```

### Performance notes
- `all-mpnet-base-v2` encodes ~2000 sentences/sec on GPU, ~200/sec on CPU
- 100K documents takes ~1 min on GPU, ~8 min on CPU
- Memory: 100K x 768 x 4 bytes = ~300MB (trivial)

### Alternative embedding models

If you want better quality or multilingual support:

| Model | Dims | Speed | Quality | Notes |
|-------|------|-------|---------|-------|
| `all-mpnet-base-v2` | 768 | Fast | Good | CLIO's choice |
| `all-MiniLM-L6-v2` | 384 | Very fast | OK | Half memory, slightly worse |
| `BAAI/bge-large-en-v1.5` | 1024 | Medium | Better | State-of-art for English |
| `intfloat/multilingual-e5-large` | 1024 | Medium | Good | If docs are multilingual |

---
