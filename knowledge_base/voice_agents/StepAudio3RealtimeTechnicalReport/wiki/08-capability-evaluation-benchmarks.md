> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Capability Evaluation Benchmarks (Table 10)

**In one sentence:** Table 10 compares StepAudio 3 Realtime against domain-specific baselines across audio understanding, dialogue and reasoning, general text, full duplex, and agentic tasks, showing strong audio understanding and floor management with variation across reasoning and tool-use tasks.

## Key points

- Table 10 uses a 0–100 scale (higher is better), with protocols and aggregation specified in Section 8.3, and bold/underline marking best/second-best per row.
- For Dialogue and Reasoning evaluation, StepAudio 3 Realtime uses realtime mode while the other models use reasoning mode.
- On audio understanding, StepAudio 3 Realtime leads Step-Caption (78.2) and MTalk-Bench (91.7), leads MMSU (90.6) and MMAR (86.5), and trails Gemini 3.1 Pro on Big Bench Audio (98.1 vs 99.6), AudioMultiChallenge (49.3 vs 67.0), MMAU (79.0 vs 80.5), and WildSpeech (77.1 vs 77.7).
- On StepAudioChat dialogue/reasoning, StepAudio 3 Realtime (Interactive) reaches 70.4 macro average, comparable to Doubao 2.0 Lite at 70.5 and DeepSeek-V4-Flash at 71.4, behind Kimi K3 at 77.1, with its best subscore in Persona and Role Consistency (78.3).
- On general text, StepAudio 3 Realtime leads HMMT 2026 Feb with 86.8 (vs 73.9 Doubao, 85.9 Gemini 3 Flash) but trails Gemini 3 Flash on GPQA Diamond (83.0 vs 90.3) and MultiChallenge (59.7 vs 68.1).
- On full duplex, StepAudio 3 Realtime ranks first on AA Full-Duplex Bench with 98.9 overall, including 100.0 on turn taking and 99.0 on interruption handling, while remaining strong on pauses and backchannels.
- On agentic τ-Voice, StepAudio 3 Realtime reaches 56.0, close to the best reported 56.5 (Grok Voice Think Fast 2.0 High), ahead of Qwen Audio 3.0 Realtime Plus (54.6) and GPT-Realtime-2.1 High (45.7).

---

## Table 10: method note

Table 10 is described as "Capability evaluation of StepAudio 3 Realtime and domain-specific baselines. Scores use a 0–100 scale (higher is better), with protocols and aggregation specified in Section 8.3. For Dialogue and Reasoning evaluation, StepAudio 3 Realtime uses realtime mode while others use reasoning mode. Bold and underlining mark the best and second-best results in each row."

**Covers:** Table 10 caption and evaluation protocol note

## Audio Understanding (Score ↑)

| Benchmark | StepAudio 3 Realtime | Doubao 2.0 Lite | Gemini 3 Flash | Gemini 3.1 Pro |
|---|---|---|---|---|
| Big Bench Audio | 98.1 | 98.8 | 99.4 | 99.6 |
| AudioMultiChallenge | 49.3 | 48.5 | 56.6 | 67.0 |
| MMSU | 90.6 | 80.0 | 77.0 | 83.6 |
| MMAU | 79.0 | 77.5 | 77.6 | 80.5 |
| WildSpeech | 77.1 | 73.9 | 74.4 | 77.7 |
| MMAR | 86.5 | 75.9 | 75.4 | 81.7 |
| Step-Caption | 78.2 | 76.8 | 67.8 | 74.8 |
| MTalk-Bench | 91.7 | 89.9 | 88.5 | 89.1 |

**Covers:** Table 10, Audio Understanding rows

## Dialogue and Reasoning (Score ↑)

| Benchmark | StepAudio 3 Realtime (Interactive) | Doubao 2.0 Lite (Reasoning) | DeepSeek-V4-Flash (Reasoning) | Kimi K3 (Reasoning) |
|---|---|---|---|---|
| Instruction Following | 54.1 | 72.9 | 71.4 | 68.9 |
| Faithfulness | 71.9 | 67.5 | 75.3 | 78.4 |
| Reasoning | 73.6 | 72.7 | 64.8 | 81.9 |
| Memory | 71.8 | 71.3 | 71.5 | 77.6 |
| Knowledge | 70.4 | 59.9 | 71.6 | 78.6 |
| Safety and Reliability | 75.1 | 75.9 | 79.9 | 84.8 |
| Conversational Pragmatics | 68.2 | 61.5 | 62.9 | 70.3 |
| Persona and Role Consistency | 78.3 | 82.6 | 73.6 | 76.5 |
| Macro Average | 70.4 | 70.5 | 71.4 | 77.1 |

The chunk notes Kimi K3 has "particularly competitive results in reasoning, memory, knowledge, conversational pragmatics, and persona consistency," and that "In realtime interaction, StepAudio 3 Realtime reaches a 70.41 macro average on StepAudioChat, comparable to Doubao 2.0 Lite at 70.5 and DeepSeek-V4-Flash at 71.4."

**Covers:** Table 10, Dialogue and Reasoning rows plus macro-average interpretation

## General Text (Accuracy ↑)

| Benchmark | StepAudio 3 Realtime | Doubao 2.0 Lite | Gemini 3 Flash |
|---|---|---|---|
| HMMT 2026 Feb | 86.8 | 73.9 | 85.9 |
| GPQA Diamond | 83.0 | 82.4 | 90.3 |
| MultiChallenge | 59.7 | 60.8 | 68.1 |

The chunk states the model "leads HMMT with 86.8, although GPQA Diamond and MultiChallenge remain below Gemini 3 Flash."

**Covers:** Table 10, General Text rows

## Full Duplex (Score ↑)

| Benchmark | StepAudio 3 Realtime | GPT-realtime-2 (High) | Qwen Audio 3.0 Realtime Plus | Grok Voice Think Fast 2.0 high |
|---|---|---|---|---|
| AA Full-Duplex Bench | 98.9 | 95.3 | 98.4 | 95.1 |

The chunk states: "The model ranks first on Full Duplex Bench with an Overall score of 98.9, including 100.0 on turn taking and 99.0 on interruption handling, while remaining strong on pauses and backchannels." It adds: "This balanced profile suggests that it can preserve conversational flow without treating every user sound as an interruption."

**Covers:** Table 10, Full Duplex row plus turn-taking/interruption detail

## Agentic (Success ↑)

| Benchmark | StepAudio 3 Realtime | Grok Voice Think Fast 2.0 High | Qwen Audio 3.0 Realtime Plus | GPT-Realtime-2.1 High |
|---|---|---|---|---|
| τ-Voice | 56.0 | 56.5 | 54.6 | 45.7 |

The chunk states: "The model reaches 56.0 on τ-Voice, close to the best reported 56.5."

**Covers:** Table 10, Agentic row

## Interpretation: Think-While-Speaking and conclusion

Verbatim claims from the chunk:

- "Together with Think-While-Speaking, this shows that the model can deliberate while producing speech and retain dialogue and reasoning performance comparable to dedicated reasoning models, rather than providing only low-latency surface responses."
- "The agentic and general-text results further demonstrate solid performance in tool use and text-based capabilities."
- "StepAudio 3 Realtime brings perception, conversational timing, reasoning, and tool use into a continuous spoken interaction. It allows deliberation and external tasks to proceed alongside the conversation, with new user input and returned evidence informing subsequent responses."
- "Evaluations show strong audio understanding and conversational-floor management, while revealing variation across reasoning and tool-use tasks."
- "Adaptive Thinking reduces the frequency of explicit reasoning, with uneven effects on answer quality."
- "Multi-turn constraint handling and retail task completion remain areas for improvement."

**Covers:** Table 10 interpretation paragraph and Section 9 Conclusion as present in chunk
