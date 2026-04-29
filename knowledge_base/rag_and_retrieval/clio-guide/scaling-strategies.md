> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Scaling Strategies

### For 10K-50K documents
- Run everything sequentially. It's fast enough.
- Use async API calls with concurrency of 50 for extraction.

### For 100K-500K documents

1. **Batch API endpoints.** Anthropic and OpenAI both offer batch APIs at 50% discount with 24h turnaround. Perfect for extraction.

```python
# Anthropic Batch API example
batch = client.batches.create(
    requests=[
        {"custom_id": doc["id"], "params": {"model": "claude-3-5-haiku-20241022",
         "max_tokens": 200, "messages": [{"role": "user", "content": prompt}]}}
        for doc, prompt in zip(documents, prompts)
    ]
)
```

2. **Checkpoint aggressively.** Save after every step. Each step can be re-run independently.

3. **Chunk and merge.** Process in 100K chunks, then merge embeddings and re-cluster globally.

4. **Use MiniBatchKMeans** for clustering over 100K documents.

5. **Local extraction + API naming.** Run Llama 3.3 locally for extraction ($0 cost), use Claude Sonnet only for the ~1000 cluster naming calls.

### For 500K+ documents

Consider **sampling**: run CLIO on a random 100K sample first. If the taxonomy is stable across different 100K samples, the full dataset won't reveal new categories -- it'll just refine cluster sizes.
