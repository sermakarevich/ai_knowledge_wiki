> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Announcing the Artificial Analysis Speech to Speech Index
**In one sentence:** Artificial Analysis announced the Speech to Speech Index, a synthesis metric for native Speech to Speech model quality that equally weights Big Bench Audio (Speech Reasoning), a Full Duplex Bench subset (Conversational Dynamics), and τ-Voice (Agentic Performance), requiring valid results on all three for inclusion.
## Key points
- The index equally weights three datasets — Big Bench Audio, Full Duplex Bench subset, and τ-Voice — and models must have valid results for all three to be included.
- OpenAI GPT-Realtime-2 (High) leads the index at 77.2%, followed by xAI Grok Voice Think Fast 1.0 at 75.7%, GPT-Realtime-1.5 at 72.0%, and Google Gemini 3.1 Flash Live Preview (High) at 69.5%.
- Conversational Dynamics and Agentic Performance are the key differentiators of frontier models: GPT-Realtime-2 leads in Conversational Dynamics while Grok Voice Think Fast 1.0 leads in Agentic Performance.
- Agentic Performance (τ-Voice) is the hardest dimension by a wide margin — Grok Voice Think Fast 1.0 leads at 52.1% ahead of GPT-Realtime-2 (High) at 39.8%, with every model below 53%.
- Speech Reasoning (Big Bench Audio) is tightly clustered at the top, led by Grok Voice Think Fast 1.0 at 97.1%.
- Deepslate Opal is the fastest model in the index with a time to first audio (TTFA) of 0.44s (62.1% index score), versus GPT-Realtime-1.5 at 0.82s, Grok Voice Think Fast 1.0 at 1.25s, GPT-Realtime-2 (High) at 2.33s, and Gemini 3.1 Flash Live Preview (High) at 2.98s.
- Gemini 3.1 Flash Live Preview (Minimal) is the lowest-cost model at $1.50 per hour of input audio (56.6% score), followed by Gemini 3.1 Flash Live Preview (High) at $1.75, Grok Voice Think Fast 1.0 at $3.00, and GPT-Realtime-2 (High) at $4.14.
- The team states it will continue to iterate on these benchmarks and plans to add more models.
---
## Index definition and methodology
**Covers:** Announcement header and index definition (June 23, 2026 article)

The announcement describes the index as "our new synthesis metric for native Speech to Speech model quality, comprising of Big Bench Audio, Full Duplex Bench, and 𝜏-Voice".

> "The index provides a single measure of how well native Speech to Speech models perform, assessing Speech Reasoning (Big Bench Audio), Conversational Dynamics (Full Duplex Bench subset), and Agentic Performance (𝜏-Voice). Weighting is equal across all three datasets, and models must have valid results for all three to be included."

| Dimension | Dataset |
|---|---|
| Speech Reasoning | Big Bench Audio |
| Conversational Dynamics | Full Duplex Bench subset |
| Agentic Performance | τ-Voice |

## Leaderboard takeaways
**Covers:** Key takeaways — model performance

| Model | Index score |
|---|---|
| OpenAI GPT-Realtime-2 (High) | 77.2% |
| xAI Grok Voice Think Fast 1.0 | 75.7% |
| GPT-Realtime-1.5 | 72.0% |
| Google Gemini 3.1 Flash Live Preview (High) | 69.5% |

> "Conversational Dynamics and Agentic Performance are key differentiators of frontier models, with GPT-Realtime-2 leading in Conversational Dynamics, and Grok Voice Think Fast 1.0 leading in Agentic Performance."

## Performance dimensions in detail
**Covers:** Conversational Dynamics, Agentic Performance, and Speech Reasoning breakdown

- Conversational Dynamics (Full Duplex Bench): GPT-Realtime-2 (Minimal) tops at 96.1%.
- Agentic Performance (τ-Voice): Grok Voice Think Fast 1.0 leads at 52.1%, ahead of GPT-Realtime-2 (High) at 39.8%, with every model below 53%; described as "the hardest dimension by a wide margin".
- Speech Reasoning (Big Bench Audio): "tightly clustered at the top, led by Grok Voice Think Fast 1.0 at 97.1%."

> "Conversational Dynamics and Agentic Performance are the key differentiators of frontier native audio models, with GPT-Realtime-2 leading in Conversational Dynamics and Grok Voice Think Fast 1.0 leading in Agentic Performance."

## Speed (TTFA)
**Covers:** Speed takeaways and TTFA breakdown

| Model | TTFA | Index score (where stated) |
|---|---|---|
| Deepslate Opal | 0.44s | 62.1% |
| GPT-Realtime-1.5 | 0.82s | 72.0% |
| Grok Voice Think Fast 1.0 | 1.25s | 75.7% |
| GPT-Realtime-2 (High) | 2.33s | 77.2% |
| Gemini 3.1 Flash Live Preview (High) | 2.98s | 69.5% |

## Cost
**Covers:** Cost takeaways and cost breakdown (per hour of input audio)

| Model | Cost per hour of input audio | Index score (where stated) |
|---|---|---|
| Gemini 3.1 Flash Live Preview (Minimal) | $1.50 | 56.6% |
| Gemini 3.1 Flash Live Preview (High) | $1.75 | 69.5% |
| Grok Voice Think Fast 1.0 | $3.00 | 75.7% |
| GPT-Realtime-2 (High) | $4.14 | 77.2% |

## Datasets incorporated
**Covers:** Dataset descriptions

- Big Bench Audio: 1,000 reasoning questions across Formal Fallacies, Navigate, Object Counting, and Web of Lies.
- Full Duplex Bench: pause handling, turn taking, interruption and backchannel handling.
- τ-Voice: end-to-end customer service task completion across Airline, Retail, and Telecom situations.

> "As always, we will continue to iterate on these benchmarks and plan to add more models."

## Links
**Covers:** Full breakdown and methodology links

- Full breakdown: https://artificialanalysis.ai/speech-to-speech
- Methodology: https://artificialanalysis.ai/methodology/speech-to-speech-benchmarking
