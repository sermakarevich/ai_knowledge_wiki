> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Benchmark Design & Construction

**In one sentence:** GraphRAG-Bench builds a college-level reasoning benchmark of 1,018 expert-screened questions drawn from the 20 most representative CS textbooks (chosen from 100+ publications across 16 subfields), extracted with a 4-stage PDF-to-tree pipeline (LayoutLMv3 layout analysis, YOLO-based formula detection, PaddleOCR, MinerU reordering), and annotates every question with an expert-crafted rationale and two-level topic label so that evaluation measures reasoning fidelity, not just answer correctness.

## Key points

- Question design targets five distinct reasoning capabilities, each explicitly mapped to a core competency of GraphRAG and crafted for college-level instructional or assessment contexts.
- The five question types are fill-in-blank (context-dependent completion testing local semantic dependencies and entity grounding), multi-choice (4 options with linguistically plausible distractors, testing discriminative reasoning over entity information and edge relationships), multi-select (2–4 correct out of 4 with overlapping distractors, testing multi-hop evidence aggregation and conflict resolution), true-or-false (factual verification requiring logical inference), and open-ended (holistic synthesis of multi-subfield knowledge into structured long-form answers).
- The source corpus was built by narrowing over 100 publications spanning 16 distinct computer-science subfields down to the 20 most representative textbooks; after rigorous screening and refinement by several domain experts, the dataset contains 1,018 high-quality challenging questions covering a broad spectrum of topics.
- Corpus extraction from PDF textbooks required a multi-stage pipeline — textbook preprocessing, content parsing, post-processing, hierarchy construction — because direct extraction is unreliable: pages mix text-based and scanned formats, inline formulas are garbled by OCR, and extracted elements arrive disordered.
- Preprocessing classifies each page as text-based (text extracted directly with PyMuPDF) or scanned (OCR required) using text density and image area proportion, and extracts per-textbook metadata (outline, total page count, page ranges per chapter/section) that later supports logical-structure construction.
- Content parsing applies LayoutLMv3 for multimodal layout analysis (segmenting each page into titles, paragraphs, figures, tables, decorative/irrelevant elements), pre-detects inline formulas with a pre-trained YOLO-based detector from PDF-Extract-Kit so formula images are extracted separately and OCR does not garble them, and transcribes title/paragraph regions of scanned pages with PaddleOCR in reading order.
- Post-processing uses MinerU to partition each page into logical reading regions, reordering and merging overlapping or fragmented elements to restore human reading order; hierarchy construction then maps the textbook metadata into a four-level tree — Book Title → Chapter → Section (Subchapter) → Knowledge Content Unit — with each node annotated with its contextual metadata and structural role.
- Unlike prior benchmarks that supply only final answers or explicit graph paths, every question carries an expert-crafted rationale that (i) isolates prerequisite concepts, (ii) describes the relationships among them, and (iii) specifies the inferential operations applied — paired with two-level topic labels (Level 1 subfield, Level 2 concept) this enables per-topic measurement of both answer accuracy and alignment of the model's generated rationale with the gold one, assessing reasoning fidelity rather than surface pattern matching.

---

## Question design

The benchmark is built on an authoritative textbook corpus assembled for college-level reasoning evaluation. Starting from **over 100 publications spanning 16 distinct subfields in computer science**, the authors systematically identified the **20 most representative textbooks** as the source corpus.

Against this corpus, **five question types** were defined, each targeting a different aspect of GraphRAG's reasoning capabilities and explicitly mapped to a core competency of the framework. Every question was crafted for application in college-level instructional or assessment contexts, on the premise that strong GraphRAG performance on these tasks would establish it as a practical educational tool. After **rigorous screening and refinement by several domain experts**, **1,018 high-quality challenging questions** covering a broad spectrum of topics were selected.

**Table 1: The description of different question types.**

| Question Type | Description |
|---|---|
| Fill-in-blank (FB) | Requires completing context-dependent statements with semantically precise terms. Assesses the model's ability to generate contextually coherent content by leveraging local semantic dependencies and entity grounding within graph-structured knowledge. |
| Multi-choice (MC) | Presents a question with 4 options, including linguistically plausible distractors. Assesses the model's capacity to discern correct answers through discriminative reasoning, integrating entity information and edge relationships to reject semantically similar but factually incorrect options. |
| Multi-select (MS) | Demands selecting 2–4 correct answers from 4 options, often requiring reasoning over interconnected concepts. The inclusion of overlapping distractors tests the model's ability to handle complex query semantics, aggregating evidence from multi-hop graph paths and resolving conflicts between related but non-essential attributes. |
| True-or-false (TF) | Involves verifying the correctness of statements. Measures the model's factual accuracy assessment, requiring logical inference over knowledge. |
| Open-ended (OE) | Allows for a wide range of responses, requiring methods to formulate detailed and comprehensive answers. Evaluates the model's holistic knowledge synthesis, demanding the integration of multi-subfield knowledge to generate structured, logically coherent long-form responses. |

The mapping is deliberate in difficulty: FB probes local grounding, MC probes discriminative use of entity + edge information, MS probes multi-hop aggregation with overlapping distractors, TF probes factual verification via inference, and OE probes cross-subfield synthesis in long form.

## Corpus collection and processing

Extracting accurate content from the 20 PDF-format core textbooks presents significant challenges, so a multi-stage pipeline was implemented with four stages: preprocessing, content parsing, post-processing, and hierarchy construction.

**1. Textbook Preprocessing**

- *PDF Classification:* To distinguish text-based pages from scanned (image-based) pages, each page's text density and image area proportion are analyzed. Text-based pages are processed by extracting text directly using **PyMuPDF**, while scanned pages require optical character recognition (OCR) to extract their textual content.
- *Metadata Extraction:* Metadata is extracted for each textbook, including its outline, total page count, and the page ranges for each chapter or section. This metadata supports the later construction of the document's logical structure.

**2. Content Parsing**

After preprocessing, each page's layout is analyzed to extract textual and non-textual elements.

- *Layout Analysis:* **LayoutLMv3** is applied for multimodal document layout analysis. LayoutLMv3 is pre-trained with masked language modeling, masked image modeling, and cross-modal alignment, which lets it learn rich representations of document pages. It classifies page regions into semantic categories — titles, paragraphs, figures, tables, or decorative/irrelevant elements — yielding coherent content blocks on each page.
- *Formula Recognition:* Mathematical formulas embedded in text are often misrecognized by OCR. To prevent this, inline formulas are first detected using a **pre-trained YOLO-based model** (from PDF-Extract-Kit), which identifies the bounding boxes of formula regions so formula images can be extracted separately, ensuring OCR does not garble the formula content.
- *OCR:* **PaddleOCR** transcribes text from regions labeled as titles and body paragraphs via layout analysis. This produces the page's textual content in the correct reading order while preserving non-text elements as separate objects.

**3. Post-Processing**

Extracted elements (text blocks, formulas, figures, tables, etc.) may be disordered due to overlapping bounding boxes or fragmented text lines. These issues are resolved by reordering and merging page regions according to human reading order: **MinerU** partitions each page into logical reading regions and sequences them so the final text flow matches the natural reading sequence.

**4. Hierarchy Construction**

The extracted content is organized into a hierarchical textbook-tree structure. The textbook metadata (chapter titles, section divisions, page ranges) is mapped to a four-level hierarchy: **Book Title → Chapter → Section (Subchapter) → Knowledge Content Unit**. Each node is annotated with its contextual metadata and structural role. This textbook-tree provides an intuitive, pedagogical navigation framework aligned with the textbook's organization; the resulting corpus — with accurate content extraction, structural annotation, and hierarchical organization — forms a robust basis for evaluating GraphRAG's ability to leverage organized textbook knowledge for context-rich reasoning and retrieval-augmented generation.

## Expert-crafted rationale

Existing benchmarks typically supply only final answers or explicit graph paths. By contrast, this dataset supplies **expert-crafted rationales** that articulate the complete logical progression necessary to solve each problem. These rationales go beyond mere corpus aggregation: they are structured narratives that

1. isolate prerequisite concepts,
2. describe the relationships among these concepts, and
3. specify the inferential operations applied during problem solving.

By tracing each step of logical inference and knowledge interaction, evaluation can assess whether GraphRAG models truly generate contextually grounded explanations or simply exploit surface-level patterns — i.e., whether the model's *reasoning* is faithful, not merely whether its *answer* happens to be correct.

To enable fine-grained, topic-specific evaluation, each question also carries two hierarchical labels:

- **Level 1:** a broad subfield (e.g., "Machine Learning");
- **Level 2:** a more granular concept (e.g., "Unsupervised Learning").

These annotations structure the post-hoc analyses: for each topic, the evaluation measures not only the accuracy of the model's answer but also the degree to which its generated rationale aligns with the gold one. This converts evaluation into a multidimensional process, requiring models to produce both correct solutions and faithful reasoning patterns.

**Covers:** Section 3 (3.1-3.3) of GraphRAG-Bench (arXiv:2506.02404)
