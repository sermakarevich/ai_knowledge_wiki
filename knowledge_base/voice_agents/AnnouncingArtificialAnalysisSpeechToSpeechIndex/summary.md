# Announcing the Artificial Analysis Speech to Speech Index | Artificial Analysis

**Article:** [Announcing the Artificial Analysis Speech to Speech Index](https://artificialanalysis.ai/articles/announcing-the-artificial-analysis-speech-to-speech-index) — Artificial Analysis, June 23, 2026

## Human Readable TL;DR

Artificial Analysis has launched a single leaderboard score for voice AI models that talk and listen directly, much like a decathlon score that blends separate events into one overall ranking. The score blends three abilities equally: answering tricky spoken reasoning questions, handling the natural flow of conversation like pauses and interruptions, and completing real customer-service phone tasks. Right now OpenAI's GPT-Realtime-2 leads overall, while xAI's Grok voice model is the best at getting practical tasks done, and every model still finds those real-world tasks far harder than the other tests.

## TL;DR

Artificial Analysis announced the Speech to Speech Index as a synthesis metric for native Speech to Speech model quality that equally weights Speech Reasoning on Big Bench Audio, Conversational Dynamics on a Full Duplex Bench subset, and Agentic Performance on τ-Voice, with inclusion requiring valid results on all three benchmarks. OpenAI GPT-Realtime-2 (High) leads the index at 77.2%, followed by xAI Grok Voice Think Fast 1.0 at 75.7%, GPT-Realtime-1.5 at 72.0%, and Google Gemini 3.1 Flash Live Preview (High) at 69.5%. Conversational Dynamics and Agentic Performance are the key differentiators at the frontier, with GPT-Realtime-2 leading the former and Grok Voice Think Fast 1.0 leading the latter, while Agentic Performance remains the hardest dimension with all models below 53%. The announcement also frames the index alongside speed measured as time to first audio and cost per hour of input audio, and commits to iterating on the benchmarks and adding more models.

---

## Problem & Motivation

There was no single, easy-to-compare measure of how good native Speech to Speech models are as complete voice agents, since existing evaluations each probed a different slice such as reasoning over audio, fluid turn-taking, or end-to-end task completion. Artificial Analysis therefore set out to combine its three speech benchmarks into one synthesis metric that captures overall voice-model quality while still preserving the distinct dimensions underneath. The goal is to give builders and buyers a simple headline ranking without losing the ability to see why a model wins, whether through smarter reasoning, more natural conversation, or more reliable real-world task execution, and to do so alongside the practical constraints of latency and price.

## Main Original Ideas

1. **Speech to Speech Index as equal-weight synthesis:** the announcement defines the index as a single measure of native Speech to Speech quality that gives identical weight to Big Bench Audio, a Full Duplex Bench subset, and τ-Voice, so no single capability dominates the headline score.
2. **Three-dimension capability framing:** each component is mapped to a distinct facet, namely Speech Reasoning for answering spoken reasoning questions, Conversational Dynamics for pause handling, turn taking, interruption and backchannel behavior, and Agentic Performance for end-to-end customer-service task completion across Airline, Retail, and Telecom scenarios.
3. **Strict inclusion rule:** a model appears in the index only when it has valid results on all three datasets, which makes the leaderboard directly comparable and prevents a strong single-benchmark result from inflating a partial entry.
4. **Quality-plus-cost-and-speed presentation:** the index score is presented together with time to first audio and hourly input-audio cost, framing model choice as a trade-off between capability, responsiveness, and price rather than quality alone.

## Key Findings

OpenAI GPT-Realtime-2 (High) tops the inaugural index at 77.2%, with xAI Grok Voice Think Fast 1.0 close behind at 75.7%, followed by GPT-Realtime-1.5 at 72.0% and Google Gemini 3.1 Flash Live Preview (High) at 69.5%. The frontier is separated less by raw speech reasoning than by conversational and agentic skill, with GPT-Realtime-2 leading in Conversational Dynamics, including a 96.1% Full Duplex Bench result for the Minimal variant, while Grok Voice Think Fast 1.0 leads in Agentic Performance.

Agentic Performance on τ-Voice stands out as the hardest dimension by a wide margin, led by Grok Voice Think Fast 1.0 at 52.1% ahead of GPT-Realtime-2 (High) at 39.8%, with every indexed model scoring below 53%. By contrast, Speech Reasoning on Big Bench Audio is tightly clustered at the top and led by Grok Voice Think Fast 1.0 at 97.1%, suggesting that current differentiation comes from behaving naturally in live dialogue and completing multi-step spoken tasks rather than from answering structured reasoning questions.

On practical deployment axes, Deepslate Opal is the fastest indexed model with a time to first audio of 0.44 seconds at a 62.1% index score, compared with 0.82 seconds for GPT-Realtime-1.5, 1.25 seconds for Grok Voice Think Fast 1.0, 2.33 seconds for GPT-Realtime-2 (High), and 2.98 seconds for Gemini 3.1 Flash Live Preview (High). Cost per hour of input audio is lowest for Gemini 3.1 Flash Live Preview (Minimal) at $1.50 with a 56.6% score, followed by the High variant at $1.75, Grok Voice Think Fast 1.0 at $3.00, and GPT-Realtime-2 (High) at $4.14, highlighting a clear quality, speed, and price trade-off at the top of the table.

## Suggestions & Future Directions

The article explicitly states that the team will continue to iterate on these benchmarks and plans to add more models to the index over time. This points toward broader model coverage, refinement of the Big Bench Audio, Full Duplex Bench, and τ-Voice evaluations, and a living leaderboard rather than a one-off ranking. Readers looking for detail are directed to the full speech-to-speech breakdown and the published benchmarking methodology.

## Authors & Institutions

The wiki source attributes the announcement to the Artificial Analysis team without naming individual authors, and no separate institutional affiliations beyond Artificial Analysis are provided.
