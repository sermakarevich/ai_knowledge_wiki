# Structured Output Collapses Answer Diversity Across 44 Language Models

**Paper:** [Structured Output Collapses Answer Diversity Across 44 Language Models (Tapan Parikh, 2026)](https://arxiv.org/abs/2607.18476)

## Human Readable TL;DR

Imagine asking 44 different friends to "name a tree" in casual conversation -- you'd get oak, willow, maple, birch, all sorts of answers. Now ask the same 44 friends the same question but tell them "answer in a strict form-field format." Suddenly way more of them say "oak." That's what this paper finds happens to AI language models: when software asks a model for its answer as JSON (the format almost all AI tools and apps actually use, as opposed to the chatty back-and-forth people use to evaluate and rank models), the model's answers become noticeably more repetitive and generic than in normal chat. The effect is bigger for the models that were the most original in chat, and it comes specifically from JSON/XML -- formats models are heavily trained to produce for tool use -- not from structure in general (plain YAML or CSV barely does it).

## TL;DR

The paper re-runs a companion "One-Word Census" instrument (31 single-turn "Name a/an X" prompts, wide answer spaces, 4 samples, temperature 1.0) across 44 language models, this time appending a request to reply in JSON instead of prose, with no schema enforcement or constrained decoding. Field-mean answer-choice surprisal (a leave-one-out, exact-match diversity metric in bits) falls from 1.80 (plain chat) to 1.58 (JSON): the modal answer's population share rises from 41% to 64% and distinct answers fall from 52 to 36. The compression is progressive and concentrated -- 6 of 44 models show individually significant shifts, led by the most distinctive frontier model losing 1.31 bits, while the most conformist models barely move. Extending the test to XML, YAML, CSV, and an arbitrary bracket wrapper shows the compression is specific to JSON (-0.22 bits) and XML (-0.23 bits) -- the serialization formats models are trained to *speak* for tool use -- while YAML and CSV show no reliable effect and a non-data bracket wrapper actually *widens* diversity (+0.13 bits). Enforcing the schema at the decoder level (`response_format`) adds almost nothing beyond the plain text request (-0.03 bits vs. -0.22 from the request itself): the collapse lives in the model's learned response to the register, not in decoding constraints.

---

## Problem & Motivation

Software does not consume language models in prose -- it asks for JSON. Every agent tool call, every data-extraction pipeline, every classifier or router receives the model's answer inside a structured data format, and that traffic increasingly dwarfs the conversational chat interface in which models are actually benchmarked, ranked, and chosen by humans. The paper asks: when the same model answers the same question in a serialization format instead of prose, does it give the same answer? If not, then every diversity/personality measurement made in chat is an overstatement of the character actually exposed to the much larger volume of software-facing traffic.

This builds directly on the author's companion paper, "The One-Word Census" (arXiv:2607.12796), which established that 44 models converge on a small set of "monoculture" answers in plain chat (e.g., *oak* takes 94% of tree answers). This paper asks whether that convergence gets worse, unchanged, or better once the same questions are asked through the format software actually uses.

---

## Main Original Ideas

1. **Register-indexed answer-choice surprisal.** The paper reuses the census's *answer-choice surprisal* metric (a leave-one-out, add-one-smoothed, exact-match measure in bits of how unlikely a model's answers are relative to the pooled answers of the other 43 models) but computes it *within* each format column separately -- JSON answers scored only against other JSON answers, plain answers against other plain answers. This makes the metric an internal property of each register, so a column's convergence cannot be an artifact of comparing one register's text against another's.

2. **The format tax is progressive, not uniform.** Rather than a flat shift, compression concentrates in the models that had the most distinctiveness to lose: DEEPSEEK-V3.2 (the census's most distinctive frontier model) falls from 2.63 to 1.32 bits (-1.31, roughly half its distinctiveness), while conformist models like CLAUDE-OPUS-4.8, GROK-4.5, and CLAUDE-SONNET-5 barely move (-0.16 to -0.05 bits). Six of 44 models show individually significant compression (BH-FDR q=.10); the rest form an unranked "noise plateau."

3. **A sharpener, not a re-indexer.** The register does not scramble answer identity -- it amplifies the model's existing mode. In 28 of 31 categories the JSON modal answer is the same word as the plain-chat mode, and less than 4% of JSON answer-mass lands on words the plain census never produced. The three exceptions (insect, board game, dance) are categories where the plain-chat mode was already weak, letting a secondary candidate win under the register's pressure.

4. **Mode movement, not sampling temperature.** A natural confound is that "structured request" might just mean "provider quietly lowers effective temperature." The paper rules this out using the census's self-distinctness statistic (distinct answers / samples) as an effective-temperature proxy: it stays nearly flat across all six format columns (0.39-0.43) while surprisal drops 0.22 bits under JSON. The collapse is *positional* (mass relocates onto the mode) not a shrinkage of the sampling distribution itself.

5. **Register-indexed personal defaults.** Using a within-run resample (n=20) rather than the noisier 4-sample scores, the paper shows individual models' *stable defaults* (an off-modal answer given repeatedly, e.g. Fable's *gouda* for cheese) are register-dependent, not fixed personality traits: JSON significantly shifts 53% of a model's stable chat defaults (mostly reverting to the crowd's modal answer), and *installs* new register-only defaults absent from chat entirely (e.g., Claude Fable 5 says *cerulean* for colour 0% of the time in chat but 100% of the time in JSON).

6. **A register gradient specific to trained serialization formats.** Testing JSON, XML, YAML, CSV, and an arbitrary "brackets" wrapper isolates *which* formats cause compression. Only JSON (-0.22 bits) and XML (-0.23 bits) -- the answer-delivery formats models are heavily post-trained to produce for tool calls and structured output -- show significant, robust compression. YAML and CSV (formats models mostly *read* rather than *write*) show no significant effect, and the non-data brackets wrapper *reverses* the effect, significantly *widening* the field (+0.13 bits). This points the causal mechanism toward tool-use post-training rather than a generic "structure suppresses creativity" story, though the paper notes a residual corpus-register component remains since every serialization format concentrates the unconstrained "Pick a word" pool to some degree.

7. **Decoder-level schema enforcement adds little beyond the request.** On the 36/44 models supporting a strict `response_format` JSON schema, enforcing the schema at the decoder compresses surprisal only marginally further than simply asking in prose for JSON (1.53 bits enforced vs. 1.56 bits requested vs. 1.79 bits plain chat, computed on the comparable 36-model subset) -- i.e., the request itself does essentially all the work (-0.22 bits) and enforcement adds only -0.03 bits more. The collapse is in the model's learned response to the register, not a side effect of constrained decoding.

---

## Key Findings

| Measure | Plain chat | JSON | XML | YAML | CSV | Brackets |
|---|---|---|---|---|---|---|
| Field-mean answer-choice surprisal | 1.80 bits | 1.58 bits | -- | -- | -- | -- |
| Δ-surprisal vs. plain chat (field mean) | -- | **-0.22** (p=.0002) | **-0.23** (p=.002) | -0.09 (n.s.) | -0.09 (n.s.) | **+0.13** (p=.009) |
| Modal answer's population share ("Pick a word") | 41% | 64% | -- | -- | -- | -- |
| Distinct answers ("Pick a word") | 52 | 36 | -- | -- | -- | -- |
| Self-distinctness (effective-temperature proxy, field mean) | 0.42 | 0.39 | 0.40 | 0.42 | 0.43 | 0.43 |

- **Individually significant compressors (BH-FDR q=.10, 6 of 44):** DEEPSEEK-V3.2 -1.31 bits, HERMES-4 -0.91, GPT-4O-MINI -0.92, GPT-4-TURBO -0.87, GPT-5.6-SOL -0.65, plus one more; the conformist floor (CLAUDE-OPUS-4.8, GROK-4.5, CLAUDE-SONNET-5) moves only -0.16 to -0.05 bits.
- **Raw surprisal range is nearly unchanged** (2.2 → 2.0 bits) even though the mean compresses -- the compression is concentrated in the mean and the collapsing tail, not the extremes; a register-invariant minority (e.g. LLAMA-4-MAVERICK, +0.56 bits, 100% JSON-compliant) holds its ground or even gains relative distinctiveness as the rest of the field slides toward it ("stranding," not divergence).
- **Reliability check:** split-half test-retest reliability of the census score is r=0.94, so regression-to-the-mean alone would predict only 0.05 bits of shrinkage for the most distinctive model against the 1.31 bits actually observed -- every individually significant compressor clears the re-measurement-noise null by 3.7-10σ.
- **Defaults are real and register-erodable:** at n=20, 144 stable chat defaults are flagged as genuine (median per-sample probability 0.90); JSON significantly shifts 76 of 144 (53%), with 29% reverting outright to the field's modal answer.
- **Defaults are also register-installed:** 81% of JSON-only "four-of-four but never-in-chat" answers survive at n=20 as genuine register-only defaults (e.g., FABLE *cerulean* for colour 0%→100% in JSON, p≈10⁻¹¹; OPUS-4.8 *carpenter* for occupation 0%→90%, p≈10⁻⁹).
- **Same nominal chat default, opposite register response:** GPT-5.6-TERRA and FABLE both answer *mango* 20/20 in chat for fruit; under JSON, TERRA flips to *apple* (20/20, p≈10⁻¹¹) while FABLE holds *mango* (19/20) -- personality is a per-register profile, not a single fixed trait.
- **Compliant-subset robustness:** restricting to the 34 of 44 models compliant in *all five* formats reproduces and sharpens the gradient (JSON -0.27, XML -0.26, brackets +0.13), while YAML/CSV stay weakly negative and non-significant -- ruling out differing compliance rates as the driver.
- **Format incompetence is a distinct confound, controlled for:** GRANITE and MYTHOMAX emit a valid CSV wrapper only ~1% of the time; scored naively (uncompliant replies included) GRANITE shows a spurious +1.49-bit CSV surprisal that vanishes once compliance-conditioning is applied.
- **Parse/hygiene:** of 27,280 format cells, only 91 (0.3%) are unrecoverable nulls (56 in YAML, 1 in JSON); parse-plus-junk survival is at least 99% per model per column.
- **Decoder enforcement (`response_format`) vs. plain request**, on the 36-model comparable subset: 1.79 bits open chat → 1.56 bits requested JSON → 1.53 bits schema-enforced JSON. The request does -0.22 bits of work; enforcement adds only -0.03 bits more.

---

## Suggestions & Future Directions

1. The immediate next columns proposed are a provider-controlled native-`response_format` enforcement replication (rather than the current heterogeneous gateway-mediated enforcement), tool-call framing as a register distinct from a bare JSON request, and clause-paraphrase columns to separate "register" effects from the specific wording of the format-request clause used here.
2. The paper explicitly declines to rank the ~38 models whose individual Δ-surprisal is not significantly different from zero, calling their mid-table ordering uninformative noise -- future work with larger sample counts per cell could sharpen this.
3. Because format compliance itself varies by model and is acquired over model generations (older models cannot speak some of these registers at all), the authors suggest a fixed, repeatable instrument re-run over time could double as a generational capability tracker for structured-output competence.
4. **Limitations acknowledged:** data is a single snapshot served through one channel (OpenRouter); requested temperature 1.0 is not honored uniformly across providers (mitigated by reporting self-distinctness alongside surprisal); surprisal is panel-relative so absolute bit values don't port across different model panels, though within-column and Δ comparisons are internal and valid; each format is probed with only a single clause wording, so register and exact phrasing are not fully separated (though the multi-format gradient argues against a simple key-priming or fill-in-template artifact, since all four serialization clauses share the same `word` slot and template but only JSON/XML compress).
5. The authors frame the core practical implication for consumers of the paper: diversity numbers collected via chat-based benchmarks/leaderboards are a measurable overstatement of the diversity actually exposed through software/agent-facing structured-output interfaces -- this matters where a task admits many acceptable answers (surveys, brainstorming, recommendations, judgement, tool choice) and is a non-issue where structured output already has one correct value (extraction, classification, routing).

---

## Authors & Institutions

Tapan Parikh, Cornell Tech (tsp53@cornell.edu). Note on AI usage: the work was done in collaboration with Claude (Opus 4.8 and Fable 5), which helped run the experiment battery, build the analysis, and draft the text; the authors state the research questions and interpretation are the author's own, and note that both Claude models are also among the 44 subjects studied.
