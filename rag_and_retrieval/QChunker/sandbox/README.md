> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

# QChunker -- Code Sandbox

Minimal implementation of core ideas from the paper using LangGraph + Ollama.

## What This Implements

- **Node 1: Question Outline Generator (A_QG)** -- Generates structured probing questions about the document (Section 3.2.1)
- **Node 2: Text Segmenter (A_SEG)** -- Uses the question outline as a semantic prior to segment the document into coherent chunks (Section 3.2.2)
- **Node 3: Integrity Reviewer (A_IR)** -- Reviews each chunk against the full document to identify missing context, terms, and dependencies (Section 3.2.3)
- **Node 4: Knowledge Completer (A_KC)** -- Rewrites chunks that need completion by seamlessly integrating missing knowledge (Section 3.2.4)

## What This Does NOT Implement

- Multi-path sampling with ChunkScore evaluation (A_SEG uses single-pass instead)
- ChunkScore metric computation (Logical Independence + Semantic Dispersion)
- SLM training pipeline (we use Ollama directly instead of fine-tuned Qwen2.5-3B)
- The full 45K dataset generation process
- HChemSafety dataset construction

## Prerequisites

1. Install [Ollama](https://ollama.ai) and pull a model:
   ```bash
   ollama pull llama3.2
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Run

```bash
uv run python run.py
```

The pipeline streams intermediate results so you can see each stage:
1. Question outline generated from the document
2. Text segmented into chunks guided by the outline
3. Each chunk reviewed for completeness
4. Incomplete chunks rewritten with missing knowledge

## Graph Topology

```
[START]
   │
   ▼
[generate_questions]  ← A_QG: Document → Question Outline
   │
   ▼
[segment_text]        ← A_SEG: (Document, Questions) → Chunks
   │
   ▼
[review_chunks]       ← A_IR: (Chunks, Document) → Reviews
   │
   ▼
[complete_knowledge]  ← A_KC: (Reviews, Document) → Completed Chunks
   │
   ▼
[END]
```

## Customization

- Change the model in `src/nodes.py` (`MODEL_NAME` variable)
- Edit prompts in `src/prompts.py`
- Replace the sample document in `examples/sample_data.py` with your own domain text
