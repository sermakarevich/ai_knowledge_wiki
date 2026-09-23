---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Announcing the Artificial Analysis Speech to Speech Index | Artificial Analysis

### Q1. What is the Speech to Speech Index, which three dimensions does it combine, and what is required for a model to be included?
> [!tip]- Answer
> The index is a synthesis metric for native Speech to Speech model quality that equally weights Speech Reasoning (Big Bench Audio), Conversational Dynamics (a Full Duplex Bench subset), and Agentic Performance (τ-Voice). Equal weighting means no single dimension dominates the score, so a model must be well-rounded rather than spiky. A model is only included if it has valid results on all three datasets. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q2. Which four models top the Speech to Speech Index leaderboard, and what are their scores in order?
> [!tip]- Answer
> OpenAI GPT-Realtime-2 (High) leads at 77.2%, followed by xAI Grok Voice Think Fast 1.0 at 75.7%, GPT-Realtime-1.5 at 72.0%, and Google Gemini 3.1 Flash Live Preview (High) at 69.5%. The gap from first to fourth is under eight points, so the frontier is closely contested. No other model's index score is stated in the chunk. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q3. Which two dimensions differentiate frontier models, and who leads each one?
> [!tip]- Answer
> Conversational Dynamics and Agentic Performance are the key differentiators of frontier native audio models. GPT-Realtime-2 leads in Conversational Dynamics, while Grok Voice Think Fast 1.0 leads in Agentic Performance. Speech Reasoning, by contrast, is tightly clustered at the top and separates the leaders far less. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q4. Why is Agentic Performance (τ-Voice) called the hardest dimension, and what numbers support that?
> [!tip]- Answer
> Agentic Performance is described as the hardest dimension by a wide margin because every model scores below 53% on it. Grok Voice Think Fast 1.0 leads at just 52.1%, ahead of GPT-Realtime-2 (High) at 39.8%, which shows even the best models complete barely half of the end-to-end tasks. Those low ceilings contrast sharply with Speech Reasoning near 97% and Conversational Dynamics near 96%. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q5. What does each incorporated dataset actually test: Big Bench Audio, Full Duplex Bench, and τ-Voice?
> [!tip]- Answer
> Big Bench Audio tests speech reasoning with 1,000 questions across Formal Fallacies, Navigate, Object Counting, and Web of Lies. Full Duplex Bench tests conversational behavior such as pause handling, turn taking, and interruption and backchannel handling. τ-Voice tests end-to-end customer service task completion across Airline, Retail, and Telecom situations. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q6. How does the speed (time to first audio) ranking compare to the quality ranking, and what is the core trade-off?
> [!tip]- Answer
> Deepslate Opal is fastest at 0.44s TTFA but scores only 62.1% on the index, while the quality leader GPT-Realtime-2 (High) is much slower at 2.33s, and Gemini 3.1 Flash Live Preview (High) is slowest at 2.98s. In between sit GPT-Realtime-1.5 at 0.82s and Grok Voice Think Fast 1.0 at 1.25s. The trade-off is that the highest index scores come with multi-second first-audio latency, so real-time use cases must weigh responsiveness against quality. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].

### Q7. Evaluation: a team needs a low-latency, low-cost voice agent for simple customer-service calls and is tempted by the index leader — what should they choose and why?
> [!tip]- Answer
> They should not default to the index leader GPT-Realtime-2 (High), because it is the most expensive listed model at $4.14 per hour of input audio and slow at 2.33s TTFA. For simple calls where τ-Voice agentic skill matters less, the cheaper and faster options fit better: Gemini 3.1 Flash Live Preview (Minimal) costs only $1.50 per hour, and Deepslate Opal answers in 0.44s. The right pick weighs index score against latency and price rather than chasing the top-ranked model alone. See [[wiki/01-speech-to-speech-index|Announcing the Artificial Analysis Speech to Speech Index]].
