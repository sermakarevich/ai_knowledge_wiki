> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Results — GPT-4o-mini

**In one sentence:** The pt approach resulted in 61.2% fewer vulnerabilities, with RCI-from-prefix variants topping the table while the adversary pe-negative approach sharply increased scanner-agreed vulnerable samples.

## Key points
- The pt approach resulted in 61.2% fewer vulnerabilities versus the baseline.
- In the adversary "pe-negative" approach, "Scanners Agree Filtered Vulnerable Samples" increased 127.7% from the baseline.
- The best row, `rci-from-pe-03-a-iter-1`, shows 2.97% filtered vulnerable samples at +61.2% diff with 0.40 vulnerabilities per sample.
- Two baseline-RCI rows, `rci-from-baseline-iter-3` and `rci-from-baseline-iter-2`, each show 3.17% filtered vulnerable samples at +58.6% diff.
- `rci-from-baseline-iter-1` shows 3.86% filtered vulnerable samples at +49.5% diff with 0.38 vulnerabilities per sample.
- `ptfscg-cot-iter-1` (3.96%, +48.3%, 1.11 vuln/sample) and `pe-03-a` (4.06%, +47.0%, 1.11 vuln/sample) rank below the RCI rows.
- `ptfscg-comprehensive` and `ptfscg-naive-secure` each show 4.16% filtered vulnerable samples at +45.7% diff, with 0.78 and 1.10 vulnerabilities per sample respectively.

---

## Prefix-technique result and adversary comparison

The chunk text is partially garbled by PDF extraction, but the following claims and table values are legible verbatim.

Verbatim claims:

- "pt approach resulted in 61.2% fewer vulnerabilities."
- "In the adversary "pe-negative" approach, "Scanners Agree Filtered Vulnerable Samples" increased 127.7% from the baseline."

## Results table (as extracted)

| ID | Filtered Vuln. Samples (%) | diff (%) | Vuln. per Sample |
|---|---|---|---|
| rci-from-pe-03-a-iter-1 | 2.97 | +61.2 | 0.40 |
| rci-from-baseline-iter-3 | 3.17 | +58.6 | 0.42 |
| rci-from-baseline-iter-2 | 3.17 | +58.6 | 0.40 |
| rci-from-baseline-iter-1 | 3.86 | +49.5 | 0.38 |
| ptfscg-cot-iter-1 | 3.96 | +48.3 | 1.11 |
| pe-03-a | 4.06 | +47.0 | 1.11 |
| ptfscg-comprehensive | 4.16 | +45.7 | 0.78 |
| ptfscg-naive-secure | 4.16 | +45.7 | 1.10 |
| pe-01-b | 4.60 | +39.8 | 1.10 |
| pe-02-a | 4.60 | +39.8 | 1.13 |

**Covers:** Results for GPT-4o-mini, including prefix-technique improvements.
