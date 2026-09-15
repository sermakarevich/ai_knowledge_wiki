> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conclusion and Limitations

**In one sentence:** Programmatic tool calling is a viable, reliable alternative to native JSON tool calling — matching or exceeding it in 11 of 14 models, with the remaining gap tracking model generation rather than family — while four explicit limitations (echo stubs, small ablation samples, judge-evaluator misalignment, and input-token overhead) bound how far these claims can be generalized.

## Key points

- Programmatic tool calling matches or exceeds native JSON tool calling in 11 of 14 models on BFCL v4.
- The GPT-5.6 family achieves a 10.7% improvement over the JSON tool calling baseline.
- Under parallel fan-out, programmatic tool calling matches or outperforms the baseline in 13 of 14 models.
- It holds stable under context rot conditions where the baseline degrades 2.3% on average.
- The remaining gap correlates with model generation rather than model family.
- BFCL v4 uses echo-return stubs: functions return arguments verbatim rather than executing real API calls, so the evaluation measures argument serialization accuracy, not end-to-end tool-use correctness.
- Ablation entry counts are small (n = 31–52 per condition), so individual model results have wide confidence intervals and are only directional; only aggregate patterns (11 of 14 on BFCL v4, consistent improvement under flood) are reliably interpretable.
- A recent audit found 20% evaluator-human misalignment in BFCL v4's LLM-judge evaluation mode, and the benchmark's ground-truth labels may still contain noise the deterministic scorer inherits.
- Programmatic tool calling carries a fixed input-token overhead: in the chaining ablation it uses 1.5× the input tokens of JSON tool calling (reversing at high fan-out), though output token counts do not differ across paradigms.

---

## Conclusion

The authors conclude that as language model agents increasingly rely on tool use to act beyond their training data, the choice of tool interface (structured JSON calls versus programmatic tool calling) has practical consequences for chaining, parallelism, and robustness under real-world conditions. Whether these advantages hold systematically across model generations and real-world task conditions on a standardized benchmark remained an open question. This work presented a systematic evaluation of programmatic tool calling against native JSON tool calling across 14 language models on BFCL v4, using typed Python stubs as the tool interface.

The results: programmatic tool calling matches or exceeds native JSON tool calling in 11 of 14 models, with the GPT-5.6 family achieving a 10.7% improvement over the JSON tool calling baseline. It matches or outperforms baseline in 13 of 14 models under parallel fan-out and holds stable under context rot conditions where the baseline degrades 2.3% on average. These results demonstrate that programmatic tool calling is a viable and reliable alternative to JSON tool calling, with the remaining gap correlating with model generation rather than model family.

## Limitations

Four limitations bound the claims in this paper.

- **Echo-return stubs.** BFCL v4 uses echo-return stubs: each function returns its arguments verbatim rather than executing real API calls. The evaluation therefore measures argument serialization accuracy, not end-to-end tool-use correctness. Results may not transfer to settings where return values affect downstream calls.
- **Small ablation samples.** The ablation entry counts are small (n = 31–52 per condition), so individual model results carry wide confidence intervals and should be read as directional. Only the aggregate cross-model patterns (11 of 14 on BFCL v4, consistent programmatic tool calling improvement under flood) are large enough to interpret reliably.
- **Evaluator misalignment in BFCL v4.** A recent audit found 20% evaluator-human misalignment in BFCL v4's LLM-judge evaluation mode (Vaghasiya et al., 2026). The authors' deterministic scorer avoids this path, but the benchmark's ground-truth labels may still contain noise that the scorer inherits.
- **Input-token overhead.** Programmatic tool calling carries a fixed input-token overhead relative to JSON tool calling: the system prompt embeds the full instruction template as prose, whereas JSON tool calling passes function schemas through the API tools parameter, which some providers count separately from conversation input tokens. On the chaining ablation, programmatic tool calling uses 1.5× the input tokens of JSON tool calling. This overhead reverses at high fan-out, as discussed in Section 4.3. Output token counts do not differ across paradigms.

**Covers:** Section 6 (Conclusion), Section 7 (Limitations)
