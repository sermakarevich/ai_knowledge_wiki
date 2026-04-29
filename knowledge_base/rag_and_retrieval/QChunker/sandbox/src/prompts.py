"""Prompt templates for QChunker pipeline nodes.

Each prompt implements a specific agent from the paper's four-agent
multi-agent debate framework (Section 3.2).
"""

# Agent 1: Question Outline Generator (A_QG)
# Paper Section 3.2.1 -- Simulates domain expert analysis by probing
# motivation, core assumptions, methodology, conclusions, and logical chains.
QUESTION_OUTLINE_PROMPT = """\
You are a domain expert analyzing a document in depth. Your task is to generate \
a structured question outline that probes the document's key aspects. This outline \
will guide how the document should be segmented into self-contained chunks.

Generate questions covering:
1. **Motivation & Context**: Why does this document exist? What problem does it address?
2. **Core Concepts & Definitions**: What key terms, abbreviations, or symbols are introduced?
3. **Methodology & Process**: What steps, procedures, or methods are described?
4. **Key Claims & Evidence**: What are the main conclusions? What supports them?
5. **Logical Dependencies**: Which parts depend on information from other parts?

Document:
---
{document}
---

Output a numbered list of probing questions, grouped by the categories above. \
Focus on questions that reveal where semantic boundaries naturally fall and where \
context dependencies exist."""

# Agent 2: Text Segmenter (A_SEG)
# Paper Section 3.2.2 -- Uses the question outline as a semantic prior
# to identify optimal segmentation boundaries.
TEXT_SEGMENTER_PROMPT = """\
You are a text segmentation expert. Given a document and a question outline that \
highlights its key semantic structures, segment the document into logically coherent chunks.

Rules:
- Each chunk should be self-contained around a coherent topic or subtopic
- Respect natural semantic boundaries (don't split mid-argument or mid-definition)
- Use the question outline to identify where topic shifts occur
- Each chunk should ideally answer one or more of the outline questions
- Keep chunks roughly balanced in length (but prioritize semantic coherence over length)

Question Outline:
---
{question_outline}
---

Document:
---
{document}
---

Output the segmented chunks. Separate each chunk with the delimiter:
===CHUNK===
Output ONLY the chunks separated by the delimiter, no commentary."""

# Agent 3: Integrity Reviewer (A_IR)
# Paper Section 3.2.3 -- Performs comparative analysis between each chunk
# and the full document to identify missing knowledge.
INTEGRITY_REVIEWER_PROMPT = """\
You are an integrity reviewer. Given a text chunk extracted from a larger document, \
determine if the chunk is self-contained or if it references concepts, terms, \
abbreviations, or context that are defined elsewhere in the document.

STRICT CONSTRAINT: Only identify knowledge that is EXPLICITLY stated in the \
original document. Do not suggest adding external information.

Original Document:
---
{document}
---

Chunk to Review:
---
{chunk}
---

Analyze the chunk and respond in this exact format:
NEEDS_COMPLETION: [YES or NO]
MISSING_KNOWLEDGE:
- [item 1: specific term, definition, or context that is missing]
- [item 2: ...]
(leave empty if NEEDS_COMPLETION is NO)"""

# Agent 4: Knowledge Completer (A_KC)
# Paper Section 3.2.4 -- Two-stage process:
# Stage 1: Verify and filter missing knowledge points
# Stage 2: Seamlessly rewrite the chunk with integrated knowledge
KNOWLEDGE_COMPLETER_PROMPT = """\
You are a knowledge completer. A text chunk has been identified as missing some \
context from its source document. Your job is to rewrite the chunk so it becomes \
self-contained by seamlessly integrating the missing knowledge.

Rules:
- Only add information that is EXPLICITLY present in the original document
- Integrate missing knowledge at the most natural position in the text
- Maintain the original writing style and tone
- Do not add commentary, headers, or meta-text
- The result should read as if it was always written this way

Original Document:
---
{document}
---

Original Chunk:
---
{chunk}
---

Missing Knowledge to Integrate:
{missing_knowledge}

Output ONLY the rewritten chunk with the missing knowledge seamlessly integrated."""
