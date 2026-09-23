> [[index|Wiki]] | [[summary|Summary]]
# We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil — Digest

## 1. [[wiki/01-the-wrong-question|The Wrong Question]]

**In one sentence:** The "which model is best at coding" debate is the wrong question because changing only the edit tool in the harness improved 16 models by ~15 points on average with zero training compute.

## Key points

- Only the edit tool changed — "In fact only the edit tool changed. That's it" — yielding +15 pts avg over patch across 16 models with $0 training compute.
- Weakest models gained the most: Grok Code Fast 1 went from 6.7% to 68.3%, "a tenfold improvement," because catastrophic patch failures had hidden its actual coding ability.
- Hashline beats patch in 14/16 models, and the v2 revision improves further in 12/16, with the largest v2 gain GPT-5.1 Codex Mini, 60.0% → 77.5%.
- Best-case output tokens fell 61% (Grok 4 Fast), because it "stopped burning tokens on retry loops."
- Patch is the worst format for nearly every model: Grok 4's patch failure rate was 50.7% and GLM-4.7's was 46.2% — "These aren't bad models — they just don't speak the language."
- The harness, not the model, is where most failures happen in practice: "everything between 'the model knows what to change' and 'the issue is resolved.'"
- A +8% success-rate gain for Gemini from the harness alone is "bigger than most model upgrades deliver," costing only "~$300 spent benchmarking."

## The argument in five moves

1. The "which model is best at coding" framing is misleading because it treats the model as the only variable, when the harness — tool schemas, error messages, state management — is where most failures happen in practice.
2. Existing edit tools all force the model to reproduce content it already saw: patch blobs with strict rules, str_replace with exact-match fragility, and even Cursor's merger model still losing to full rewrites on small files.
3. Hashline replaces content reproduction with content-hash line tags, so the model references anchors like "replace range 1:a3 through 3:0e" and stale reads are rejected before corrupting anything.
4. A 16-model, 180-task benchmark changing only the edit tool shows hashline beating patch in 14/16 models, weakest models gaining the most, and output tokens falling by up to 61% as retry loops disappear.
5. An ~$300 harness experiment delivering Gemini +8% beats most model upgrades at zero training compute, so vendors blocking open harnesses are burning the bridge that carries their own models forward.
