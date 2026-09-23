> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: awesome full duplex speech-to-speech
## Claims vs. evidence
- Claim: true full-duplex (simultaneous listen-and-speak with turn-taking, overlap, backchanneling, interruption) is a critical milestone toward human-like interaction.
- Assessment: definitionally plausible and consistent with conversational-behavior literature, but this chunk supplies the definition only — no user studies, latency numbers, or preference scores to back "critical milestone."
- Claim: half-duplex cascades (STT → LLM → TTS) are structurally blocked from natural conversational behavior by sequential listen-think-speak cycles.
- Assessment: directionally true for naive cascades, but overstated as stated — chunk gives no evidence ruling out low-latency cascades with VAD plus barge-in, which ship in production today.
- Claim: end-to-end full-duplex spoken LMs replace the cascade with parallel encoding and generation in unified cycles.
- Assessment: architectural claim presented without a single diagram, codec, or training objective in this chunk; asserted, not demonstrated.
- Claim: a decisive paradigm shift since 2022–2023, anchored on Moshi, SyncLLM, GPT-4o Realtime, and Gemini Live.
- Assessment: the four landmarks are real named systems, but the chunk cites zero metrics, ablations, or adoption figures — the "shift" is narrated, not measured.
- Claim: the guide "comprehensively maps the landscape" across models, representations, datasets, benchmarks, and projects.
- Assessment: scope claim is contradicted by the chunk itself — every table is an empty placeholder, so comprehensiveness is a plan, not a property.
- Overall: strong framing-to-evidence ratio problem — confident synthesis voice over placeholder tables with no model, dataset, or benchmark rows in this chunk.
## Genuinely new vs. repackaged
- Genuinely useful framing: the TFD vs. half-duplex distinction (continuous parallel encode/generate vs. sequential listen-think-speak) is a crisp lens for comparing voice systems.
- Genuinely useful framing: active listening, backchanneling, and interruption as first-class capabilities rather than edge-case handling.
- Genuinely useful scope: one map spanning models, representations, datasets, benchmarks, challenges, publications, workshops, and open-source/commercial projects — if ever filled in.
- Repackaged: the cascade-pipeline critique rehearses well-known STT→LLM→TTS limitations without new analysis.
- Repackaged: the landmark name-drops (Moshi, SyncLLM, GPT-4o Realtime, Gemini Live) add no technical detail beyond existence and date in this chunk.
- Repackaged: the 2022–2023 "paradigm shift" periodization follows the standard LLM-audio timeline without dating evidence in-chunk.
- Repackaged: the "comprehensively maps the landscape" self-description is aspirational — this chunk is a skeleton, and the curation value lives or dies in the unpopulated tables.
## Weaknesses and blind spots
- Empty evidence base: every substantive section (models, representations, datasets, benchmarks, challenges, events, publications, projects, products) is a placeholder line in this chunk — nothing to audit, reproduce, or compare.
- No evaluation content: no latency, interruption-success, backchannel-appropriateness, overlap-handling, or MOS-style quality metrics; no benchmark rows to choose from.
- No engineering failure modes: echo cancellation, feedback loops, endpointing under noise, barge-in false triggers, and streaming-inference cost are absent.
- No representation analysis: neural codecs vs. discrete units vs. continuous features — the central design decision — gets a header and nothing else.
- No data discussion: overlap-rich conversational corpora, licensing, and privacy/redaction for always-listening systems are unaddressed.
- Commercial opacity: GPT-4o Realtime and Gemini Live are cited as proof of deployment, but closed systems contribute no architecture or eval detail — survivorship framing without caveats.
- Version risk: v0.1.0 accessed 2026-05-28 is an early snapshot of a fast field; tables will rot quickly without maintenance, and the citation target is a repo, not a versioned paper.
- Overclaim check: "decisive paradigm" language outruns what placeholder tables can support; a reader acting on this chunk alone would have definitions but zero buildable specifics.
- No cost or latency model: streaming duplex inference, codec overhead, and always-on compute get no numbers, so build-vs-buy cannot be reasoned from this chunk.
- No safety or misuse note: always-listening voice systems raise consent, recording-disclosure, and spoofing questions the front matter never mentions.
- Single-chunk limitation (fairness note): deeper wiki pages or later repo versions may fill the tables — this critique covers only the ingested digest plus one wiki chunk, not the live repo.
## Applicability
- Direct use today: low — this chunk alone cannot select a model, codec, dataset, or benchmark; treat it as a vocabulary setter, not a build guide.
- Near-term use: moderate — once populated, the tables could shortcut landscape scans for voice-mode features (interruption handling, backchanneling UX).
- Practical filter for reuse: adopt only the TFD definition and the section checklist (models → representations → datasets → benchmarks → challenges) as a review template for any voice-system proposal.
- Practical filter for reuse: require any cited duplex system to report endpointing latency, interruption handling, and overlap behavior before it enters a shortlist.
- Strategic use: real — the TFD framing correctly anticipates where conversational agents must go (continuous listening, graceful interruption), so the concepts transfer even while the tables are empty.
- **Relevance to my work**
  - AI/ML engineering: borrow the TFD vocabulary (endpointing, barge-in, backchannel policy, duplex latency budget) for voice-interface evals; do not adopt any architecture from this chunk — none is specified.
  - Agentic systems: interruption and overlap handling generalize to multi-turn agents (user corrects mid-tool-call, conflicting instructions mid-stream); design agent loops as interruptible, not run-to-completion, mirroring the full-duplex lesson.
  - Elisity data platform: always-listening audio implies redaction, retention, and consent requirements at ingest; any future voice telemetry needs PII-scrubbed, access-controlled storage before model work begins — this chunk's silence on privacy is itself the warning.
## What this changes
- Changes the target: acceptable voice UX moves from fast turn-taking to continuous co-presence — a system that cannot be interrupted reads as broken, not merely slow.
- Changes eval design: turn-level accuracy is insufficient; interruption precision/recall, backchannel timing, and perceived naturalness under overlap become required metrics.
- Changes architecture taste: streaming parallel encode/generate with incremental state beats batch listen-think-speak for interactive feel, at higher infra complexity.
- Does not change this quarter's stack: no evidence here justifies replacing a working cascaded voice pipeline; the cost (echo control, streaming infra, eval harness) is concrete while the payoff evidence is absent.
- Sharpens the review question for any voice proposal: "show me the interruption path" — what happens when the user speaks mid-reply, and what is the measured recovery time.
- Sharpens the data question: any duplex pilot must state what audio is retained, for how long, and under whose consent before architecture talk starts.
- Useful as a watching brief: track whether the repo's tables fill with open weights, reproducible benchmarks, and codec comparisons — that is the event that would convert framing into tooling.
## Verdict
- As ingested (front matter plus empty tables), this is a promising map with no territory drawn yet: strong definitions, honest scope, zero actionable rows.
- Do not cite it as evidence for architectural decisions; cite it at most as a pointer to the landscape it intends to cover.
- Do not cite it as evidence for architectural decisions; cite it at most as a pointer to the landscape it intends to cover.
- Revisit when models, representation, dataset, and benchmark tables carry dated entries with links and metrics; until then the value is conceptual.
- The honest one-liner: good compass, no map yet — the framing survives scrutiny, the substance is still to come.
- Watch trigger: populated benchmark and codec-comparison tables with reproducible links would upgrade this from **watch** to **trial**.
- Call: **watch**
