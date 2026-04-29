> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Document Preprocessing

### Goal
Standardize documents into a consistent format the LLM can process efficiently.

### What to do

```python
import hashlib
from pathlib import Path

def preprocess_document(doc_path: str, max_chars: int = 8000) -> dict:
    """Load and normalize a document for facet extraction.

    CLIO averaged ~1000 tokens per conversation. For longer documents,
    truncation is fine because we only need topic identification.
    """
    text = Path(doc_path).read_text(encoding="utf-8", errors="replace")

    # Truncate very long documents -- keep beginning + end
    if len(text) > max_chars:
        half = max_chars // 2
        text = text[:half] + "\n\n[...truncated...]\n\n" + text[-half:]

    return {
        "id": hashlib.sha256(doc_path.encode()).hexdigest()[:16],
        "path": doc_path,
        "text": text,
    }

doc_paths = list(Path("./my_documents").rglob("*.txt"))
documents = [preprocess_document(str(p)) for p in doc_paths]
print(f"Loaded {len(documents)} documents")
```

### Key decisions
- **Max document length:** 4000-8000 chars is usually enough for topic extraction. The LLM only identifies what the document is about, not reproducing content.
- **Multi-topic documents:** If your documents span multiple topics (long reports, books), split them into sections first and treat each section as a separate document.
- **File formats:** Convert PDFs, DOCXs, etc. to plain text first. Use `pymupdf`, `python-docx`, or `unstructured` library.

---
