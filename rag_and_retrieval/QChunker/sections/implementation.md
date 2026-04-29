> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Implementation Details

### 1. Data Generation Pipeline

Training data for QChunker is generated through the multi-agent debate framework, which uses **DeepSeek-R1** as the backbone LLM for constructing the core training data (as well as the HChemSafety dataset). To foster diversity in generated content, the generation parameters are set to **temperature = 0.7** and **top_p = 0.8**.

The framework produces training data for three specialized small language models (SLMs):

| SLM | Role | Training Data Format |
|-----|------|---------------------|
| M_Gen | Generates question outline Q and optimal segmentation C_opt from document D | (D, (Q, C_opt)) |
| M_Disc | Discriminator -- determines whether chunk c_i has missing information given D | (D, c_i) -> accept/reject |
| M_Ref | Knowledge completer -- identifies missing parts and rewrites chunks | (D, c_i) -> c'_i |

Each model receives **45K training samples** (45K per model, for a total of 135K samples across the three SLMs). The optimal segmentation C_opt used in M_Gen training is selected via **multi-path sampling** over candidate segmentations scored by ChunkScore.

### 2. Model Training Configuration

**Base model:** Qwen2.5-3B (instruction version)

All three SLMs (M_Gen, M_Disc, M_Ref) are trained with **full-parameter fine-tuning** (not LoRA or adapter-based) using the following hyperparameters:

| Parameter | Value |
|-----------|-------|
| Learning rate | 1.0 x 10^-5 |
| LR schedule | Cosine annealing |
| Warm-up | 10% of training steps |
| Batch size per device | 2 |
| Gradient accumulation steps | 16 |
| Effective batch size | 2 x 16 = 32 |
| Precision | BF16 mixed-precision |

**Loss function:** Standard cross-entropy on target sequence tokens:

```
L_F(theta) = -(1/tau) * sum_{t=1}^{tau} log P(o_t | o_{<t}, s; theta)
```

Where:
- `o_t` is the t-th token in the target sequence `o`
- `o_{<t}` is the prefix of the target sequence up to position t-1
- `s` is the input context
- `theta` represents the learnable parameters of the SLM
- `tau` is the total length of the target output sequence

### 3. Hardware

| Purpose | Hardware |
|---------|----------|
| Model training and evaluation | **NVIDIA A800 80G GPUs** |
| Data processing and dataset construction | **Huawei Ascend AI technology stack** |

The work was supported by Huawei's AI Hundred Schools Program and carried out using the Huawei Ascend AI technology stack for data-side operations.

### 4. RAG Pipeline Configuration

All experimental comparisons use a strictly identical RAG pipeline, differing only in the text chunking strategy:

| Component | Configuration |
|-----------|--------------|
| Vector database | **Milvus** |
| Embedding model | **bge-base-zh-v1.5** |
| Retrieval top_k | **8** |
| Standardized average chunk length | **178 tokens** (adopted from LumberChunker's output) |
| Total retrieved context per query | **178 x 8 = 1,424 tokens** (strictly fixed) |
| Evaluation/generation model | **Qwen2.5-7B** (instruction version, float16 precision) |

All language models used in experiments are instruction versions loaded with **float16 precision**. The 178-token average chunk length is used as a primary control variable; the 1,424-token total context length serves as a secondary constraint to ensure fairness when different chunking algorithms cannot precisely match 178 tokens per chunk on average.

### 5. HChemSafety Dataset Construction

#### 5.1 Data Acquisition

1. **Chemical name repository:** Systematically establish an initial name repository covering common and high-risk chemicals.
2. **Web crawling:** Programmatically generate search engine query links to acquire web page entries from three types of authoritative platforms:
   - Chemical professional platforms
   - Encyclopedic resources
   - Academic databases

#### 5.2 Multi-Stage Cleaning Pipeline

Source URLs are clustered based on formatting patterns, then processed through three cleaning stages:

1. **Structural cleaning (DOM tree analysis):** Identify and remove non-core content areas -- navigation bars, sidebars, footers, advertising regions. Retain only the main content area.
2. **Functional cleaning:** Use regular expressions and HTML parsers to eliminate all interactive elements:
   - Complete removal of `<script>` and `<style>` tags
   - Strip all event-handling attributes (e.g., `onclick`)
3. **Attribute cleaning:** Remove all ID attributes and delete non-essential class attributes to simplify web structure.

#### 5.3 Quality Scoring and Filtering

- **LLM-based scoring:** Each cleaned document is assigned a precise score from **0 to 5** using a fine-grained LLM scoring mechanism.
- **Threshold:** Only documents with scores **> 3** are retained for the refinement stage.

#### 5.4 Text Refinement

- **Sliding window:** Long documents are segmented using text windows with overlapping regions to ensure contextual coherence and prevent information loss at boundaries.
- **LLM refinement:** Each text window is processed by **DeepSeek-V3** (not R1).
- **Fusion:** Results across all windows are fused, transforming raw web page text into high-value documents.

#### 5.5 Knowledge Graph Construction

- **Entity recognition and relation extraction:** LLM-based end-to-end knowledge acquisition.
- **Graph database:** Extracted triplets are imported into **Neo4j**.
- **Graph structure:** Nodes represent entities; edges denote relationships (properties, chemicals, chemical-property relations).

#### 5.6 QA Pair Generation

Four types of QA pairs are generated by traversing the knowledge graph:

| QA Type | Description |
|---------|-------------|
| **Single-hop** | Generated directly from a single triplet |
| **Multi-hop** | Requires reasoning across multiple edges |
| **Aggregative** | Requires summarizing information from multiple nodes |
| **Boolean** | Yes/no answers |

QA pairs are stored in JSON format including questions, standard answers, and reference content. Each pair is directly derived from the knowledge graph for traceability.

#### 5.7 Final Dataset Statistics

| Component | Size |
|-----------|------|
| Large-scale QA dataset | **135K QA pairs** |
| Retrieval corpus | **35K high-quality chemical documents** |
| Curated evaluation set | **19K representative questions** |

The evaluation set covers various types from basic factual QA to complex safety emergency protocols, enabling assessment of knowledge retrieval, information integration, and specialized reasoning.

### 6. Baseline Configurations

QChunker is evaluated against **six baseline methods** plus two direct LLM comparisons:

#### (a) Rule-Based Chunking Methods

| Method | Configuration |
|--------|--------------|
| **Original** | Divides long texts into fixed-length segments (~200 Chinese characters/words) without considering sentence boundaries |
| **Llama_index** | Uses `SimpleNodeParser` from Llama_index; prioritizes sentence boundaries while keeping token counts close to a preset threshold via the `chunk_size` parameter |

#### (b) Dynamic Chunking Methods

| Method | Configuration |
|--------|--------------|
| **Similarity Chunking** | Uses pre-trained sentence embedding models for cosine similarity between sentences; lower-similarity points become segmentation boundaries. Implemented via `SemanticSplitterNodeParser` from Llama_index |
| **LumberChunker** | Leverages LLM reasoning to predict segmentation points. Uses **Qwen2.5-14B at full precision** |
| **MoC MetaChunker** | Trains a lightweight chunker model for automatic long-text partitioning without fixed lengths or predefined rules. Strongest baseline with best cross-task generalization |

#### (c) Direct LLM Comparisons

| Method | Configuration |
|--------|--------------|
| **Qwen2.5-14B** | General-purpose LLM, instruction version |
| **Qwen3-14B** | General-purpose LLM, instruction version |

#### ChunkScore Parameters

The ChunkScore metric uses two key parameters:

| Parameter | Value | Description |
|-----------|-------|-------------|
| **alpha** | **10^-3** | Regularization constant for the semantic dispersion Gram matrix to ensure positive definiteness |
| **lambda** | **0.3** | Weight for logical independence in ChunkScore (semantic dispersion gets weight 0.7) |

The ChunkScore formula: `Phi_CS(C) = lambda * Phi_LI(C) + (1 - lambda) * Phi_SD(C)`

At lambda = 0.3, the Pearson correlation coefficient between ChunkScore and downstream ROUGE-L performance approaches **1.0** on the CRUD benchmark, and exceeds **0.85** on all three additional datasets.

#### Controlled Variable Design

All baselines are evaluated under strict controlled conditions:
- **Primary constraint:** Average chunk length standardized to **178 tokens** (LumberChunker's natural average)
- **Secondary constraint:** Total retrieved context fixed at **1,424 tokens** (178 x 8)
- **Same RAG pipeline:** Identical embedding model, vector database, retrieval settings, and generation model across all methods
