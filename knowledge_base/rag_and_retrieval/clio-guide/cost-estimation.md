> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Cost Estimation

### CLIO's published costs (from Table 2 in paper)

For 100K documents at original CLIO pricing:

| Step | Model | Input Tokens | Output Tokens | Cost |
|------|-------|-------------|---------------|------|
| Facet Extraction | Claude 3 Haiku | 130M | 10M | $45.00 |
| Cluster Labeling | Claude 3.5 Sonnet | 1M | 50K | $3.75 |
| Hierarchy Generation | Claude 3.5 Sonnet | 18K | 600 | $0.06 |
| **Total** | | | | **$48.81** |

### Updated cost estimates with current models (2025-2026 pricing)

| Step | Model | 10K docs | 50K docs | 100K docs | 500K docs |
|------|-------|----------|----------|-----------|-----------|
| Extraction | Claude 3.5 Haiku | $4.50 | $22.50 | $45 | $225 |
| Extraction | GPT-4.1-mini | ~$2 | ~$10 | ~$20 | ~$100 |
| Extraction | Local (vLLM) | $0 | $0 | $0 | $0 |
| Cluster naming | Claude Sonnet | $0.40 | $1.50 | $3.75 | $15 |
| Hierarchy | Claude Sonnet | ~$0.01 | ~$0.03 | ~$0.06 | ~$0.30 |

**Bottom line:** At 100K documents, expect $20-50 with API models, or $4-15 if you use a local model for extraction and API only for cluster naming.
