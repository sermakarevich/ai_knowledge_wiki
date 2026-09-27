> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ablation study: tool-only evolution and Jaccard overlap
**In one sentence:** Table 6 ablates the three editable evolution levels on DDR-Bench averaged across four backbones, reporting tool-only evolution at 82.7 (+13.2), schema-only at 73.1 (+3.6), and full three-level evolution at 89.5 (+20.0), alongside a garbled pairwise Jaccard overlap matrix.
## Key points
- Table 6 is described as an ablation on the three editable levels of the evolution loop on DDR-Bench, averaged across four backbones.
- Tool-only evolution scores 82.7 with a gain of +13.2 reported in the chunk.
- Schema-only evolution scores 73.1 with a gain of +3.6 reported in the chunk.
- Full three-level evolution scores 89.5 with a gain of +20.0 reported in the chunk.
- The chunk contains a "Jaccard overlap" matrix with rows labeled GPT-5.6-sol, Claude-Sonnet-5, and Claude-Opus-4.8, but axis labels and cell alignment are garbled in extraction.
- Reported Jaccard row fragments are: GPT-5.6-sol 0.61 / 1.00 / 0.60 / 0.62; Claude-Sonnet-5 0.58 / 0.60 / 1.00 / 0.55; Claude-Opus-4.8 0.56 / 0.62 / 0.55 / 1.00, with diagonal 1.00 values intact but row-column mapping not recoverable from the chunk.
- Additional numeric fragments (e.g. Sonnet-5 73.1 / 76.8 / 81.3 / 82.1 and Opus-4.8 75.4 / 78.9 / 75.6 / 92.3 under an "Agent backbone (deployment)" axis) appear in the chunk but their column headers are garbled, so no claim about their meaning is made here.
---
## Ablation on evolution levels (Table 6)
**Covers:** Table 6 caption and three reported rows

Verbatim:

> "Table 6: Ablation on the three editable levels of the evolution"
> "loop on DDR-Bench, averaged across four backbones."

| Condition | Score | Gain |
|---|---|---|
| Tool-only evolution | 82.7 | +13.2 |
| Schema-only evolution | 73.1 | +3.6 |
| Full three-level evolution | 89.5 | +20.0 |

Verbatim rows:

> "Tool-only evolution              82.7         +13.2"
> "Schema-only evolution            73.1         +3.6"
> "Full three-level evolution         89.5         +20.0"

## Jaccard overlap matrix (garbled)
**Covers:** Jaccard overlap heading and pairwise matrix fragments

Verbatim:

> "Jaccard overlap"
> "GPT-5.6-sol 0.61    1.00     0.60    0.62"
> "Claude-Sonnet-5 0.58    0.60     1.00    0.55"
> "Claude-Opus-4.8 0.56    0.62     0.55    1.00"

- The chunk's axis labels around the matrix (fragments such as "GPT- GPT-5.6 e-Sonne e-Opus-", "Clau Clau", "Agent backbone (deployment)") are garbled and are not interpreted here.
- Numeric fragments "Sonnet-5    73.1   76.8    81.3   82.1" and "Opus-4.8    75.4   78.9    75.6   92.3" are present in the chunk adjacent to the matrix but without recoverable headers, so they are recorded as fragments only.

**Covers:** chunk file `09-jaccard-overlap-tool-only-evolution-82-7-13-2.md` lines 1–17, from the "Jaccard overlap" heading through the Table 6 caption ("Ablation on the three editable levels of the evolution loop on DDR-Bench, averaged across four backbones") and associated numeric fragments; matrix axes and surrounding figure text are garbled in extraction and not covered beyond the verbatim fragments above.
