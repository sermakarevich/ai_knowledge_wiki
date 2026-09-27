[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Dialogue Systems
**In one sentence:** LLM-centered spoken dialogue systems need low-latency text normalization of non-standard words before TTS, and the authors propose StreamTN — a lightweight Qwen3-0.6B-based Chinese streaming TN model with a dual-track streaming framework — plus a diverse TN benchmark.
## Key points
- TTS in an LLM-centered spoken dialogue system (SDS) requires converting LLM responses into TTS-readable formats via text normalization (TN), with strict low-latency requirements in real-time scenarios.
- Existing TN solutions are largely rule-based, rely on manual engineering, and generalize poorly to unseen patterns.
- Using a general LLM itself for TN via prompt engineering suffers high first-token latency from non-streaming processing, hallucination risks, and degraded reasoning when the core LLM is fine-tuned solely for TN.
- StreamTN is a lightweight LLM-based Chinese streaming TN model built on Qwen3-0.6B, using a dual-track streaming framework where input tokens and output tokens are processed on two parallel tracks for low-latency real-time inference without complex prompting.
- Task-specific fine-tuning gives StreamTN superior TN performance and fewer hallucinations than rule-based systems and general-purpose LLMs (as claimed in the abstract).
- The authors introduce a TN benchmark spanning diverse text scenarios as an evaluation standard for speech generation in SDS; experiments are said to demonstrate effectiveness in accuracy and inference latency.
- LLM outputs contain non-standard words (NSWs) — numbers, dates, time expressions, phone numbers, units, chemical formulas, mathematical expressions — whose pronunciation depends on context (e.g., a number read as a date vs. phone number vs. amount vs. math expression), causing mispronunciations, unnatural prosody, or synthesis failures without TN.
---
## Abstract and proposal
**Covers:** Abstract (arXiv:2609.24267v1 [eess.AS] 21 Sep 2026)

The paper proposes "StreamTN, a lightweight LLM-based Chinese streaming TN model. Built on Qwen3-0.6B, StreamTN employs a dual-track streaming framework in which input tokens and output tokens are processed on two parallel tracks, enabling low-latency real-time inference without complex prompting."

Verbatim claims from the abstract:
- "Existing TN solutions are largely rule-based, rely on manual engineering, and generalize poorly to unseen patterns."
- "Although an LLM itself can perform TN through prompt engineering, it faces key limitations: high first-token latency due to non-streaming processing, hallucination risks, and degraded intelligence or reasoning when the core LLM module is fine-tuned solely for TN."
- "Moreover, task-specific fine-tuning yields superior TN performance and fewer hallucinations than rule-based systems and general-purpose LLMs."
- "We also introduce a TN benchmark that spans diverse text scenarios, providing a comprehensive evaluation standard for speech generation in spoken dialogue systems."

Index Terms (verbatim): "text normalization, spoken dialogue systems, low-latency inference".

## Dialogue-system setting
**Covers:** Section I (Introduction), cascaded vs. end-to-end SDS

- Modern LLM-centered SDS follow either an end-to-end paradigm (speech understanding, response generation, and speech synthesis jointly modeled) or a cascaded paradigm (ASR, LLM module, and TTS as independent components).
- Recent speech-language models explore speech-native or real-time interaction with LLMs; although end-to-end systems show "promising progress, cascaded systems remain widely used in practical applications due to their controllability, modularity, ease of debugging, and flexibility in integrating external knowledge or retrieval modules."
- In a cascaded SDS, the LLM module's textual response is the direct input to the TTS module (Fig. 1 shows: User Speech → LLM Response Module (streaming T1…Tn) → StreamTN (streaming) → TTS Module (streaming T1…Tn) → Response Speech, labeled "StreamTN Dual-Track Streaming Architecture").

## The TN problem: non-standard words
**Covers:** Section I, NSW definition and ambiguity

- LLM-generated responses contain NSWs "readable to humans but… ambiguous or unsuitable for direct speech synthesis," e.g. "a single number may correspond to different pronunciations depending on whether it appears in a date, a phone number, an amount, or a mathematical expression."
- "Without proper text normalization (TN), such ambiguity may cause mispronunciations, unnatural prosody, or even synthesis failures in downstream TTS systems."

## Prior TN work and gap
**Covers:** Section I, related-work survey within the chunk

- Traditional industrial TN relies on "handcrafted rules, regular expressions, and WFST-based grammars," giving controllability at the cost of "substantial language-specific engineering."
- Neural approaches formulate TN as sequence modeling predicting "context-appropriate verbalizations from written input," but "purely neural approaches may produce rare but severe unrecoverable errors, which is particularly problematic for TTS."
- For Mandarin, hybrid rule-plus-neural models (e.g., multi-head self-attention) and "FlatTN," a "rule-guided flat-lattice Transformer" with a large-scale Chinese TN dataset, advanced modeling and resources — but "they mainly focus on offline or sentence-level normalization rather than low-latency streaming normalization in LLM-centered dialogue systems," which is the gap StreamTN targets.
