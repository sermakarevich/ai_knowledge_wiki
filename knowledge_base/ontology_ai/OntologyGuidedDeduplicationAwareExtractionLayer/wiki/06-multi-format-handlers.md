> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Solution: A Six-Signal Per-Page Classifier for PDF Routing
**In one sentence:** A six-signal priority-ordered per-page classifier using PyMuPDF routes each PDF page to text, OCR/vision, or skip, then routes the whole document by text-page ratio (≥80% text, ≤20% OCR, otherwise mixed split-and-merge) to eliminate binary-routing information loss.
## Key points
- Per-page decision is a priority-ordered cascade in Eq. (1): skip if `Ap = 0`, OCR if `Iblock > 0.15` or `Ixref > 0.15`, text if `C > 50`, OCR if `D > 200`, text if `C > 0`, else skip.
- Six structural signals per page (Table 8) cover degenerate area, raster image-block coverage, xref-hidden image coverage, extractable characters, vector drawing primitives, and xref image count gating signal 3.
- The 15% image-coverage threshold for Signals 2–3 is empirical: pages with small logos or decorative images below it still go to text extraction.
- The vector-text edge case (Signal 5) catches pages with zero characters but hundreds of drawing primitives (e.g. Fig. 5 page 6 with `D = 412`) that need OCR.
- Document-level routing in Eq. (2) uses text pages over usable (non-skip) pages: Text if ≥0.80, OCR if ≤0.20, Mixed otherwise (20–80%).
- Mixed extraction partitions indices (text pages through pypdf chunked pipeline with non-text slots blanked; OCR pages only through vision pipeline; skips ignored), then merges with `_merge_chunk_results()` plus relationship second pass and ID reassignment (Stages 3–4).
- Impact claim: for a 45-page document with 30 text + 15 scanned pages, binary routing either loses all scanned content or wastefully OCRs 30 born-digital pages, while the per-page classifier processes each page optimally.
---
## Per-page classifier cascade
**Covers:** Solution opening + Eq. (1) + Table 8 (p. 15)

A six-signal per-page classifier using "PyMuPDF's low-level page analysis API determines whether each page should be processed via text extraction, OCR/vision, or skipped entirely." Classification is "a priority-ordered cascade" with "image dominance is checked first, then extractable text, then the vector-text edge case, with skip as the final default":

| Priority | Condition | Routes to |
|---|---|---|
| 1 | `Ap = 0` | skip |
| 2 | `Iblock > 0.15` or `Ixref > 0.15` | ocr |
| 3 | `C > 50` | text |
| 4 | `D > 200` | ocr |
| 5 | `C > 0` | text |
| 6 | otherwise | skip |

Table 8 — the six per-page signals and their roles in the cascade of Eq. (1):

| # | Signal | Definition | Detects | Threshold |
|---|---|---|---|---|
| 1 | `Ap` | page area | degenerate pages | = 0 |
| 2 | `Iblock` | image-block area / `Ap` | scanned pages | > 0.15 |
| 3 | `Ixref` | xref-image area / `Ap` | images hidden from block analysis | > 0.15 |
| 4 | `C` | extractable characters | born-digital text | > 50 (or > 0) |
| 5 | `D` | drawing/path primitives | text drawn as vectors | > 200 |
| 6 | `X` | xref image count | gates signal 3's computation | > 0 |

Worked example (Fig. 5, mixed 10-page PDF under per-page classification):

| p1 | p2 | p3 | p4 | p5 | p6 | p7 | p8 | p9 | p10 |
|---|---|---|---|---|---|---|---|---|---|
| text | text | ocr | ocr | text | ocr | text | ocr | skip | text |
| `C=2840` | `C=3105` | `Iblk=.91` | `Iblk=.88` | `C=1990` | `D=412` | `C=2470` | `Ixref=.67` | `C=0` | `C=3320` |

"6 text / 9 usable = 0.67 ⇒ mixed route: text pages → text extraction, ocr pages → vision; merged downstream." The caption states: "Each page carries the signal that decided it: born-digital pages pass on character count, scanned pages trip the image-coverage thresholds, page 6 is the vector-drawn-text edge case (zero characters, 412 drawing primitives), and the empty page 9 is skipped."

## Signal design rationale
**Covers:** Signal Design Rationale (p. 15–16)

"The six signals were chosen to cover distinct categories of page content":

- "Image block coverage (Signal 2) detects pages dominated by raster images embedded as block-level elements, the most common indicator of scanned pages."
- "Xref image coverage (Signal 3) catches images that are referenced via PDF cross-reference tables but may not appear as blocks in the structured page dictionary, providing a secondary detection mechanism."
- "Character count (Signal 4) identifies born-digital pages with extractable text, using a threshold of 50 characters to distinguish meaningful content from stray artefacts."
- "Drawing count (Signal 5) addresses an edge case where text is rendered as vector paths rather than font glyphs. Such pages report zero characters but contain hundreds of drawing primitives, requiring OCR to recover the text."
- "The 15% coverage threshold for Signals 2 and 3 was empirically determined: pages with small logos or decorative images below this threshold still contain predominantly extractable text."

## PDF routing logic
**Covers:** Section 5.1.2, Eq. (2) (p. 16)

"After classifying every page, the system computes the ratio of text pages to usable (non-skip) pages and routes the entire document through one of three extraction paths":

- Text path (≥80% text pages): "Extracts text from all pages using pypdf and processes via the existing chunked text extraction pipeline."
- OCR path (≤20% text pages): "Routes the entire PDF through vision-based extraction. When LLM_PROVIDER=local, pages are rendered as images and sent to the local VLM; when using Gemini, the Gemini File API handles native PDF processing."
- Mixed path (20–80% text pages): "Routes text pages and OCR pages through their respective extraction pipelines independently, then merges results using the existing cross-chunk merge infrastructure (Stage 3)."

## Mixed PDF extraction
**Covers:** Section 5.1.3 (p. 16–17)

"The mixed PDF extraction function partitions pages by their classification and processes each group through the appropriate pipeline":

1. "Text pages: Non-text page slots are blanked out in the page text array, and the remaining text is processed through the standard chunked text extraction pipeline."
2. "OCR pages: Only the OCR-classified page indices are sent to the vision extraction pipeline, avoiding unnecessary processing of born-digital pages."
3. "Skip pages: Ignored entirely; no extraction is attempted on empty or zero-area pages."
4. "Merge: Partial results from both paths are merged using _merge_chunk_results(), followed by a relationship second pass and consistent ID reassignment (Stages 3–4)."

Robustness: "When all extraction paths fail (e.g., due to corrupted pages), the system returns an empty but valid ExtractionResult rather than raising an exception, ensuring downstream pipeline stability."

## Impact
**Covers:** Impact paragraph (p. 17)

"Mixed PDF support eliminates the information loss caused by binary routing. For a 45-page document with 30 text pages and 15 scanned pages, the previous approach would either miss all scanned content (text path) or wastefully OCR all 30 born-digital pages (OCR path). The per-page classifier processes each page optimally."

## Chunk tail: deduplication lead-in (belongs to Section 6)
**Covers:** Sections 6–6.1 opening (p. 17)

The chunk tails into "6 Deduplication and entity resolution," presenting "the output schema that carries deduplication evidence, six zero-inference rule-based algorithms, their orchestration as a guarded composition, and the complementary embedding-based resolution layer." Under 6.1, "The output schema evolved from a minimal entity–relationship container into a deduplication-aware data model. The legacy schema carried a single alias per entity and a bare disambiguation fingerprint," with no record of alias provenance, distinguishing context, or merge rationale; the revised schema "introduces three dedicated record types (ContextAttribute, AliasOccurrence, and PossibleDuplicate)" with "five-plus aliases with per-alias provenance (AliasOccurrence: discovery source, occurrence count, confidence)," contextual attributes (role, organisation, location), scored duplicate flags with merge recommendations, `dedup_candidates` export, and a `coverage_warnings` list for soft quality signals. Full detail is covered by the deduplication wiki page, not this page.

**Covers:** Solution classifier Eq. (1) + Table 8 + Fig. 5 example, Signal Design Rationale, Sections 5.1.2–5.1.3 with Eq. (2) and Impact (pp. 15–17), plus Section 6–6.1 lead-in tail
