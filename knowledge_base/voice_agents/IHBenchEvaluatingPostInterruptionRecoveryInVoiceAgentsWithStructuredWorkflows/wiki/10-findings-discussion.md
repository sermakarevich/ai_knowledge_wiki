> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Findings and Discussion: Post-Interruption Recovery as a Distinct Capability
**In one sentence:** Post-interruption recovery is a distinct capability with wide spread across models, partially independent of task fulfillment, with filler handling differentiating model families and recovery quality uncorrelated with general audio-benchmark performance.
## Key points
- Post-interruption recovery is a distinct capability with wide spread across models.
- Filler handling — resuming an utterance after a backchannel — is a strong family-level differentiator despite being the simplest type conceptually.
- The GPT family and the newer Gemini 3.x line handle filler interruptions far less reliably than the Gemini 2.5 family.
- Task fulfillment and recovery quality are partially independent axes: the task-fulfillment leader ranks only mid-pack on recovery quality, while the recovery-quality leader has lower task fulfillment.
- Against AudioMultiChallenge, IHBench's recovery quality is the lowest-correlated of the six joint evaluation axes (the four AMC axes plus the two IHBench metrics), indicating it is not already captured by a strong general audio benchmark.
- IHBENCH is limited to synthetic English-only conversations across 10 enterprise domains, with rubrics inheriting generator and judge biases, and evaluates recovery on textual content only, not prosodic or acoustic behavior.
- Planned extensions are multilingual coverage, validation on real end-user live interactions, integration with full-duplex timing benchmarks, and post-training on the benchmark rubrics and generated data.
---
## Core findings
**Covers:** discussion findings on recovery capability

> "Post-interruption recovery is a distinct capability with wide spread across models."

> "Filler handling (resuming an utterance after a backchannel) is a strong family-level differentiator despite being the simplest type conceptually: the GPT family and the newer Gemini 3.x line handle it far less reliably than the Gemini 2.5 family."

> "Task fulfillment and recovery quality are partially independent axes: the task-fulfillment leader ranks only mid-pack on recovery quality, while the recovery-quality leader has lower task fulfillment."

> "Against AudioMultiChallenge, IHBench's recovery quality is the lowest-correlated of the six joint evaluation axes (the four AMC axes plus our two metrics). This is evidence that recovery quality is a largely distinct capability axis, not already captured by a strong general audio benchmark."

## Limitations
**Covers:** limitations paragraph

> "Limitations. IHBENCH is built from synthetic conversations rather than real user interactions, is English-only, and spans 10 enterprise domains; its rubrics inherit the biases of the generator model and the judge."

> "We evaluate recovery on the textual content of responses only, not on prosodic or acoustic recovery behavior (e.g. timing or intonation after a barge-in)."

## Future work
**Covers:** future-work paragraph

> "Future work. Natural extensions include multilingual coverage, validation against real end-user interactions in live deployment, integration with full-duplex timing benchmarks for end-to-end interruption evaluation (timing and recovery), and turning the benchmark, or the synthetic pipeline behind it, into a training signal: post-training on its rubrics and generated data to strengthen the recovery behavior we currently only measure."

**Covers:** chunk 10-7-post-interruption-recovery-is-a (findings, limitations, future work; references excluded)
