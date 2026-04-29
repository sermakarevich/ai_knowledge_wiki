> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Facet Extraction via LLM

### Goal
For each document, produce a 1-2 sentence English-language topical summary. This is the most expensive step (one LLM call per document).

### CLIO's exact configuration
- **Model:** Claude 3 Haiku, temperature 0.2
- **Output:** 1-2 sentence summary, no proper nouns (privacy -- you can skip this)
- **Cost:** ~$0.45 per 1K documents at Haiku pricing

### Adapted prompt for document segmentation

```python
EXTRACTION_PROMPT = """The following is a document:
<document>
{document_text}
</document>

Your job is to answer the question about the preceding document.
Be descriptive. Get to the point in at most two sentences.

What is this document about? What is its main topic and purpose?

Output your answer inside <answer> tags. Be clear and concise.

Examples:
<answer>Technical analysis of semiconductor supply chain disruptions in East Asia during 2023, focusing on TSMC capacity constraints.</answer>
<answer>A customer complaint about delayed shipping for order #4521, requesting refund and escalation to management.</answer>
<answer>Research paper proposing a novel transformer architecture for protein structure prediction using multi-scale attention.</answer>
"""
```

### Batch extraction code

```python
import asyncio
from anthropic import AsyncAnthropic
from tqdm.asyncio import tqdm_asyncio
import re

client = AsyncAnthropic()
SEMAPHORE = asyncio.Semaphore(50)  # max concurrent requests

async def extract_summary(doc: dict) -> dict:
    """Extract a topical summary from a single document."""
    async with SEMAPHORE:
        prompt = EXTRACTION_PROMPT.format(document_text=doc["text"])
        response = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=200,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text
        # Parse <answer> tags
        match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
        summary = match.group(1).strip() if match else raw.strip()

        return {**doc, "summary": summary}

async def extract_all_summaries(documents: list[dict]) -> list[dict]:
    tasks = [extract_summary(doc) for doc in documents]
    results = await tqdm_asyncio.gather(*tasks, desc="Extracting summaries")
    return results

# Run it
documents = asyncio.run(extract_all_summaries(documents))

# Save checkpoint
import json
with open("step2_summaries.jsonl", "w") as f:
    for doc in documents:
        f.write(json.dumps(doc) + "\n")
```

### Categorical facets: The Two-Pass Discovery + Enforcement Pattern

Beyond the main topic summary (which gets embedded and clustered, so naming variability is absorbed), you may want categorical facets like document type, domain, audience, or language. These need **controlled vocabularies** -- if you let the LLM freely generate categories, you'll get hundreds of near-duplicates that destroy any downstream filtering or analysis.

The solution is a two-pass pipeline: **discover the taxonomy from a sample, then enforce it on the full dataset.**

#### Pass 1: Open extraction on a sample

Sample 1-2K documents and let the LLM say whatever it wants. Collect all raw values.

```python
DISCOVERY_PROMPT = """Analyze this document and extract the following attributes.
For each, give a short phrase (2-5 words). Be specific.

<document>
{document_text}
</document>

<facets>
<doc_type>[What kind of document is this?]</doc_type>
<domain>[What field/industry/domain does this belong to?]</domain>
<audience>[Who is the intended reader?]</audience>
<formality>[formal / semi-formal / informal]</formality>
</facets>"""

# Run on a random sample
sample = random.sample(documents, min(2000, len(documents)))
raw_facets = []  # list of {"doc_type": "...", "domain": "...", ...}

for doc in tqdm(sample, desc="Discovery pass"):
    resp = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=200,
        temperature=0.2,
        messages=[{"role": "user",
                   "content": DISCOVERY_PROMPT.format(document_text=doc["text"][:4000])}],
    )
    parsed = parse_facet_xml(resp.content[0].text)
    raw_facets.append(parsed)
```

This will produce something like:

```
doc_type values (2000 raw):
  "research paper" (312), "academic paper" (87), "scientific article" (45),
  "technical report" (203), "tech report" (31), "engineering report" (12),
  "email" (156), "email message" (23), "email correspondence" (8), ...
```

Hundreds of unique strings, many near-duplicates.

#### Normalize: Embed, cluster, and name the canonical taxonomy

```python
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import numpy as np

embed_model = SentenceTransformer("all-mpnet-base-v2")


def build_canonical_taxonomy(
    raw_values: list[str],
    max_categories: int = 30,
    similarity_threshold: float = 0.65,
) -> dict[str, str]:
    """Cluster raw facet values into a canonical taxonomy.
    
    Returns: mapping from raw value -> canonical category name.
    """
    # Count frequencies
    counts = Counter(raw_values)
    unique_values = list(counts.keys())
    
    if len(unique_values) <= max_categories:
        # Already small enough, just return identity mapping
        return {v: v for v in unique_values}
    
    # Embed all unique values
    embeddings = embed_model.encode(unique_values, normalize_embeddings=True)
    
    # Agglomerative clustering with cosine distance
    # distance_threshold controls granularity:
    #   lower = more clusters (finer categories)
    #   higher = fewer clusters (coarser categories)
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=1.0 - similarity_threshold,  # cosine distance
        metric="cosine",
        linkage="average",
    )
    labels = clustering.fit_predict(embeddings)
    n_clusters = len(set(labels))
    
    # If still too many clusters, re-cluster with explicit n
    if n_clusters > max_categories:
        clustering = AgglomerativeClustering(
            n_clusters=max_categories,
            metric="cosine",
            linkage="average",
        )
        labels = clustering.fit_predict(embeddings)
    
    # For each cluster, pick the most frequent value as canonical name
    cluster_to_values = {}
    for val, label in zip(unique_values, labels):
        cluster_to_values.setdefault(label, []).append((val, counts[val]))
    
    # Build mapping: raw value -> canonical name (most frequent in cluster)
    raw_to_canonical = {}
    canonical_names = []
    for label, vals_counts in cluster_to_values.items():
        # Sort by frequency, pick the most common as canonical
        vals_counts.sort(key=lambda x: -x[1])
        canonical = vals_counts[0][0]
        canonical_names.append((canonical, sum(c for _, c in vals_counts)))
        for val, _ in vals_counts:
            raw_to_canonical[val] = canonical
    
    # Print the taxonomy
    canonical_names.sort(key=lambda x: -x[1])
    print(f"Taxonomy: {len(canonical_names)} categories from {len(unique_values)} raw values")
    for name, count in canonical_names:
        print(f"  {name}: {count} ({count/len(raw_values)*100:.1f}%)")
    
    return raw_to_canonical


# Build taxonomy for each facet independently
doc_type_taxonomy = build_canonical_taxonomy(
    [f["doc_type"] for f in raw_facets],
    max_categories=25,
    similarity_threshold=0.65,
)

domain_taxonomy = build_canonical_taxonomy(
    [f["domain"] for f in raw_facets],
    max_categories=40,
    similarity_threshold=0.60,  # domains are more varied, allow more clusters
)
```

Output:

```
Taxonomy: 18 categories from 247 raw values
  research paper: 444 (22.2%)    ← absorbed "academic paper", "scientific article"
  technical report: 246 (12.3%)  ← absorbed "tech report", "engineering report"  
  email: 187 (9.4%)             ← absorbed "email message", "email correspondence"
  ...
```

#### Optional: LLM-refined canonical names

The most-frequent-value heuristic works, but an LLM can produce cleaner names:

```python
def refine_taxonomy_names(
    cluster_to_values: dict[int, list[tuple[str, int]]],
) -> dict[int, str]:
    """Ask LLM to pick the best canonical name for each cluster."""
    refined = {}
    for label, vals_counts in cluster_to_values.items():
        vals_str = ", ".join(f'"{v}" ({c})' for v, c in vals_counts[:15])
        resp = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=30,
            temperature=0.0,
            messages=[{"role": "user",
                       "content": f"These are all names for the same category of document. "
                       f"Pick the single best canonical name (2-4 words, lowercase):\n{vals_str}\n\n"
                       f"Best name:"}],
        )
        refined[label] = resp.content[0].text.strip().strip('"')
    return refined
```

#### Pass 2: Constrained extraction on full dataset

Now extract facets from ALL documents, forcing the LLM to pick from the discovered taxonomy:

```python
def build_enforcement_prompt(
    doc_type_categories: list[str],
    domain_categories: list[str],
) -> str:
    doc_types = " | ".join(doc_type_categories)
    domains = " | ".join(domain_categories)
    
    return """Classify this document. You MUST pick from the provided options only.
If none fit perfectly, pick the closest match.

<document>
{document_text}
</document>

Allowed doc_type values: """ + doc_types + """
Allowed domain values: """ + domains + """

Respond in this exact format, one value per line:
<doc_type>[pick exactly one from the list above]</doc_type>
<domain>[pick exactly one from the list above]</domain>
<formality>[formal | semi-formal | informal]</formality>
<complexity>[1 | 2 | 3 | 4 | 5]</complexity>"""


ENFORCEMENT_PROMPT = build_enforcement_prompt(
    doc_type_categories=list(set(doc_type_taxonomy.values())),
    domain_categories=list(set(domain_taxonomy.values())),
)

# Now extract on the full dataset -- guaranteed controlled vocabulary
async def extract_facets_enforced(doc: dict) -> dict:
    async with SEMAPHORE:
        resp = await async_client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=100,
            temperature=0.0,   # deterministic = more consistent picks
            messages=[{"role": "user",
                       "content": ENFORCEMENT_PROMPT.format(
                           document_text=doc["text"][:4000])}],
        )
        return {**doc, "facets": parse_facet_xml(resp.content[0].text)}
```

#### Handling taxonomy growth (escape hatch)

What if the full dataset has document types the 2K sample missed? Add a controlled escape hatch:

```python
ENFORCEMENT_PROMPT_WITH_ESCAPE = """Classify this document. Pick from the provided
options. If NONE of the options are even remotely close, you may write OTHER: [your
suggested new category] -- but only if truly nothing fits.

Allowed doc_type values: {doc_types}
...
"""

# After full extraction, collect all OTHER: values
other_values = [f["doc_type"] for f in all_facets if f["doc_type"].startswith("OTHER:")]

if other_values:
    # Cluster the OTHER values
    other_taxonomy = build_canonical_taxonomy(other_values, max_categories=10)
    print(f"Discovered {len(set(other_taxonomy.values()))} new categories:")
    for cat in set(other_taxonomy.values()):
        print(f"  {cat}")
    # Decide whether to add them to the taxonomy or merge into existing
```

#### Numeric and scale facets (no vocabulary problem)

For facets that are numbers or fixed scales, there's no variability issue. Use these freely:

```python
# These are safe -- constrained by design
COMPLEXITY_PROMPT = """Rate document complexity 1-5. Answer with ONLY a number.
1=simple everyday language, 5=extremely technical/specialized."""

LENGTH_FACET = len(doc["text"].split())  # computed, no LLM needed

CONCERN_PROMPT = """Rate how sensitive/confidential this document appears, 1-5.
Answer with ONLY a number.
1=completely public/generic, 5=highly confidential/sensitive."""
```

#### The full facet extraction architecture

```
                    ┌─────────────────────────────────────────┐
                    │         FACET EXTRACTION DESIGN          │
                    └─────────────────────────────────────────┘

    Facet Type          Strategy              Variability Risk
    ──────────          ────────              ────────────────
    Topic summary       Free text → embed     None (clustering absorbs it)
    Numeric (1-5)       Constrained scale     None (integer output)
    Categorical         Two-pass discovery    Eliminated by enforcement
    Computed            Code, no LLM          None (deterministic)
    
    Categorical facets MUST go through:
    1. Sample 1-2K docs → open extraction
    2. Embed + cluster raw values → canonical taxonomy
    3. Full dataset → constrained extraction with enum
```

### Using local models (zero API cost)

```python
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Use a local model for extraction
summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",  # or use vLLM with Llama/Qwen
    max_new_tokens=100,
)

def extract_summary_local(doc: dict) -> dict:
    prompt = f"Summarize the main topic of this document in one sentence:\n\n{doc['text'][:2000]}"
    result = summarizer(prompt)[0]["generated_text"]
    return {**doc, "summary": result}
```

For higher quality with local models, use **vLLM** or **Ollama** with Llama 3.3 8B or Qwen 3 8B:

```python
from openai import OpenAI

# Point to local vLLM server
local_client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

def extract_summary_local(doc: dict) -> dict:
    response = local_client.chat.completions.create(
        model="meta-llama/Llama-3.3-8B-Instruct",
        messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(
            document_text=doc["text"]
        )}],
        max_tokens=200,
        temperature=0.2,
    )
    return {**doc, "summary": response.choices[0].message.content}
```

---
