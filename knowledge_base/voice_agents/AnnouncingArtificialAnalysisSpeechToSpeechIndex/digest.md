> [[index|Wiki]] | [[summary|Summary]]
# Announcing the Artificial Analysis Speech to Speech Index | Artificial Analysis — Digest

## 1. [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]]
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

## The argument in five moves
1. Native Speech to Speech quality needs a single synthesis metric, so the Speech to Speech Index combines Speech Reasoning, Conversational Dynamics, and Agentic Performance with equal weighting.
2. Inclusion requires valid results on all three datasets (Big Bench Audio, Full Duplex Bench subset, τ-Voice), making the index a complete three-dimensional comparison.
3. The leaderboard puts OpenAI GPT-Realtime-2 (High) on top at 77.2%, with Grok Voice Think Fast 1.0, GPT-Realtime-1.5, and Gemini 3.1 Flash Live Preview (High) close behind.
4. Frontier differentiation comes from Conversational Dynamics (led by GPT-Realtime-2) and Agentic Performance (led by Grok Voice Think Fast 1.0), while Speech Reasoning is tightly clustered and τ-Voice remains the hardest dimension with every model below 53%.
5. Quality trades against speed (Deepslate Opal fastest at 0.44s TTFA) and cost (Gemini Minimal cheapest at $1.50/hr), so buyers must weigh index score against latency and price.
6. The benchmarks and model coverage will keep iterating, with more models to be added over time.
