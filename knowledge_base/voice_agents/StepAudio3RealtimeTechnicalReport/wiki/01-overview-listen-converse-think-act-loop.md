> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview: Listen-Converse-Think-Act Loop

**In one sentence:** StepAudio 3 Realtime is an audio-language foundation model organized around a continuous listen-converse-think-act loop that combines Deep Perception, Seamless Duplex, Think-While-Speaking, and a streaming Voice Agent to deliver deep reasoning in real-time spoken interaction.

## Key points
- The core problem is the tension between deep deliberation and latency: the model must reason carefully about complex requests while keeping pauses, backchannels, and interruptions fluid.
- Deep Perception captures linguistic and nonverbal acoustic evidence to interpret user intent, while Seamless Duplex models synchronized user and model audio streams to manage the conversational floor.
- Think-While-Speaking executes private reasoning in parallel with spoken delivery, supported by Adaptive Thinking and multi-token prediction, reaching 73.0 macro average on StepAudioChat in reasoning mode.
- With Think-While-Speaking it achieves dialogue and reasoning performance comparable to dedicated reasoning models while speaking in real time (Interactive mode 70.4 on StepAudioChat dialogue average).
- An integrated streaming Voice Agent handles asynchronous tool execution without disrupting dialogue flow, carrying conversational intent into tools and folding results back into subsequent dialogue.
- Headline results: 90.6 on MMSU, 98.9 Overall on the Artificial Analysis Full-Duplex Bench, and 56.0% macro task-success on τ-Voice; leads reported baselines on four of eight audio-understanding benchmarks.
- StepAudio 3 ASR Max reports error rates of 1.18 (LibriSpeech clean), 4.35 (WenetSpeech meeting), and 0.49 (AISHELL-1); remaining gaps are noted in multi-turn constraint following and retail tool-use tasks.

---

## Abstract

StepAudio 3 Realtime targets realtime spoken interaction demanding deep reasoning, prompt responses, and fluid turn-taking. Its organization is a continuous listen-converse-think-act loop:

| Function | Role as stated in abstract |
|---|---|
| Deep Perception | Captures rich acoustic cues to interpret user intent |
| Seamless Duplex | Models synchronized audio streams to handle pauses, backchannels, and interruptions naturally |
| Think-While-Speaking | Resolves deliberation-vs-latency tension by executing private reasoning in parallel with spoken delivery |
| Voice Agent | Handles asynchronous tool execution without disrupting dialogue flow |

Reported headline scores from the abstract:

| Benchmark | StepAudio 3 Realtime score |
|---|---|
| StepAudioChat (reasoning mode, macro average) | 73.0 |
| MMSU | 90.6 |
| Artificial Analysis Full-Duplex Bench (Overall) | 98.9 |
| τ-Voice (macro task-success rate) | 56.0% |

> "Crucially, we resolve the tension between deep deliberation and latency via Think-While-Speaking, executing private reasoning in parallel with spoken delivery."

**Covers:** Abstract (arXiv:2609.14005v2 [cs.SD] 19 Sep 2026, StepFun-Audio Team).

## Figure 1 headline results

Figure 1 compares StepAudio 3 ASR Max and StepAudio 3 Realtime (blue) against baselines (gray); lower is better for ASR error rates, higher is better elsewhere. Values stated in the chunk:

Audio Understanding (higher is better):

| Benchmark | StepAudio 3 Realtime | Baselines |
|---|---|---|
| AudioMultiChallenge | 49.3 | Doubao 2.0 Lite 48.5; Gemini 3 Flash 56.6; Gemini 3.1 Pro 67.0 |
| MMSU | 90.6 | Doubao 2.0 Lite 80.0; Gemini 3 Flash 77.0; Gemini 3.1 Pro 83.6 |
| MMAR | 86.5 | Doubao 2.0 Lite 75.9; Gemini 3 Flash 75.4; Gemini 3.1 Pro 81.7 |

Interactive Intelligence (higher is better):

| Benchmark | StepAudio 3 Realtime | Baselines |
|---|---|---|
| StepAudioChat Dialogue | 70.4 (Interactive, realtime mode test) | Doubao 2.0 Lite (Reasoning) 70.5; DeepSeek-V4-Flash (Reasoning) 71.4; Kimi K3 (Reasoning) 77.1 |
| AA Full-Duplex Bench Full Duplex (Overall) | 98.9 | GPT-realtime-2 (High) 95.3; Qwen Audio 3.0 Realtime Plus 98.4; Grok Voice Think Fast 2.0 high 95.1 |
| τ-Voice Agentic | 56.0 | Grok Voice Think Fast 2.0 High 56.5; Qwen Audio 3.0 Realtime Plus 54.6; GPT-Realtime-2.1 High 45.7 |

General Text (higher is better):

| Benchmark | StepAudio 3 Realtime | Baselines |
|---|---|---|
| HMMT 2026 Feb | 86.8 | Doubao 2.0 Lite 73.9; Gemini 3 Flash 85.9 |
| GPQA Diamond | 83.0 | Doubao 2.0 Lite 82.4; Gemini 3 Flash 90.3 |
| MultiChallenge | 59.7 | Doubao 2.0 Lite 60.8; Gemini 3 Flash 68.1 |

ASR error rates (lower is better):

| Benchmark | StepAudio 3 ASR Max | Baselines |
|---|---|---|
| LibriSpeech clean | 1.18 | Doubao 2.0 ASR 2.94; Seed 2.0 Lite 1.47; HY3.0 ASR Preview 1.38 |
| WenetSpeech meeting | 4.35 | Doubao 2.0 ASR 5.09; Seed 2.0 Lite 4.80; HY3.0 ASR Preview 4.12 |
| AISHELL-1 | 0.49 | Doubao 2.0 ASR 2.07; Seed 2.0 Lite 1.66; HY3.0 ASR Preview 1.22 |

Notes from the figure caption: Dialogue averages eight dimensions, full duplex reports Overall, and τ-Voice averages three domains.

**Covers:** Figure 1 with Tables 1 and 10 pointer.

## Introduction

Spoken interaction requires following the user (a pause may precede a complete request; speech during model output may be an acknowledgment or a substantive interruption) while managing the model's own response, reasoning carefully on complex requests, and sustaining tool use that may outlast the exchange that initiated it. The chunk traces the lineage: acoustic representations combined with LLM linguistic knowledge, broader audio-language understanding with direct speech generation, and streaming/full-duplex overlap of listening and speaking, so responses account for linguistic content, vocal delivery, and conversational timing.

StepAudio 3 Realtime builds on the Step-Audio series' shared audio-language foundation and focuses on coordinating perception, reasoning, and action as conversation unfolds — the listen, converse, think, and act loop. Functions operate concurrently as needed, with new user input shaping the ongoing interaction. The intro's summary of results: the realtime model leads reported baselines on four of eight audio-understanding benchmarks and achieves the highest reported Overall score on the Artificial Analysis Full-Duplex Bench, with remaining gaps in multi-turn constraint following and retail tool-use tasks (Section 8 protocols and domain analysis).

**Covers:** Section 1 Introduction.

## Realtime Conversational Loop (overview)

StepAudio 3 Realtime coordinates listening, speaking, reasoning, and action through an evolving conversational context in which user speech, model speech, and tool results can arrive while other parts of the interaction remain in progress; Figure 2 gives an overview of these coupled functions. The chunk ends at the start of Section 2.1 (Shared Conversational Context heading only, no body).

**Covers:** Section 2 opening through Section 2.1 heading.
