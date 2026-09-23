> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Script Rationality Validation via Dual LLM Judges, Comparison, and Conclusion
**In one sentence:** The chunk defines a dual-LLM-judge validation of script rationality on three dimensions with Table 4 scores after filtering, introduces a Table 5 comparison against five prior corpora, and concludes DuplexDrama as the first TTS-synthesized dialogue dataset jointly covering four annotation dimensions with ~800 hours to be released.
## Key points
- Script rationality is evaluated on three dimensions: (i) asset rationality, (ii) rationality of background tags, and (iii) script-scenario consistency.
- Dimensions (i) and (iii) are cross-checked by both DeepSeek-v4.1-pro [12] and Gemini-3.1-pro-preview [13].
- Dimension (ii) is judged only by the Gemini-3.1-pro-preview multimodal model because the audio bank is manually curated.
- Table 4 is stated to report average scores after filtering, but no Table 4 scores or thresholds are legible in the chunk.
- Section 3.3 states Table 5 compares released DuplexDrama with five prior corpora, with Fisher [6] and CANDOR [7] named as supplying natural conversation before the sentence truncates.
- The conclusion claims DuplexDrama is the first TTS-synthesized spoken dialogue dataset jointly covering persona and scenario annotations, full-duplex behaviors, expressive speech, and sound events, built through a four-stage pipeline and evaluated along four objective audio metrics with dual-LLM cross-checking of script rationality.
- The chunk states approximately 800 hours will be released, and lists future work as more realistic duplex label distributions, paralinguistic phenomena in TTS output, and more flexible sound-event label matching.
---
## Dual-LLM script rationality validation (3.2.2)
**Covers:** chunk secs: 3.2.2 Script Rationality Validation via Dual LLM Judges; Table 4

Verbatim claims:

- "3.2.2. Script Rationality Validation via Dual LLM Judges"
- "We employ LLM judges to evaluate three dimensions: (i) asset rationality, (ii) rationality of background tags, and (iii) script-scenario consistency."
- "Dimensions (i) and (iii) are cross-checked by both DeepSeek-v4.1-pro [12] and Gemini-3.1-pro-preview [13]; dimension (ii) is judged by the single Gemini-3.1-pro-preview multimodal model since the audio bank is manually curated."
- "Table 4 reports average scores after filtering."

Table 4 cell values, score scales, and filtering thresholds are not legible in the chunk, so they are not stated here.

## Comparison with other datasets (3.3)
**Covers:** chunk secs: 3.3 Comparison with Other Datasets; Table 5 lead-in

Verbatim claims:

- "3.3. Comparison with Other Datasets"
- "Table 5 compares our released DuplexDrama with five prior corpora."
- "Fisher [6] and CANDOR [7] supply natural conver-" (sentence truncated in chunk; continuation not legible).

No further Table 5 rows or values are legible in this chunk, so they are not stated here.

## Conclusion and future work (Section 4)
**Covers:** chunk secs: 4 CONCLUSION

Verbatim conclusion (as legible in chunk):

- "We present DuplexDrama, the first TTS-synthesized spoken dialogue dataset jointly covering persona and scenario annotations, full-duplex behaviors, expressive speech, and sound events."
- "The corpus is built through a four-stage pipeline and evaluated along four objective audio metrics, with dual-LLM cross-checking of script rationality."
- "We will release approximately 800 hours of data to facilitate research on full-duplex spoken dialogue modeling."
- "Future work will pursue more realistic duplex label distributions, paralinguistic phenomena in TTS output, and more flexible sound-event label matching."

## Disclosure, ethics, and references in chunk
**Covers:** chunk secs: Acknowledgement / AI Disclosure / Compliance / References [1]–[18] as legible

Verbatim statements present in the chunk:

- "AI Disclosure. LLMs were used solely to polish English during manuscript preparation; all technical content is authored and verified by the human authors, who take full responsibility for the final text."
- "Compliance with Ethical Standards. DuplexDrama is constructed from TTS synthesis and publicly available audio; no human subject data was used; ethical approval was not required."
- "Conflicts of Interest. None."
- "[12] DeepSeek-AI, "DeepSeek-V4: Towards highly efficient million-token context intelligence," https://huggingface.co/deepseek-ai/ DeepSeek-V4, 2026."
- "[13] Google DeepMind, "Gemini 3.1 Pro Preview," https://ai.google.dev/gemini-api/ docs/models/gemini-3.1-pro-preview, 2026."
- References [1]–[11] and [14]–[18] are partially legible in the chunk but belong to other sections, so their details are not stated here beyond the judge/citation use above.

**Covers:** Dual-LLM script rationality scores, prior-corpora comparison, and conclusion/future work (chunk 05-3-2-2-script-rationality-validation-via-dual; Sec. 3.2.2, Sec. 3.3 lead-in, Sec. 4).
