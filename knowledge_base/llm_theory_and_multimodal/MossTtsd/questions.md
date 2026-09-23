---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: OpenMOSS/MOSS-TTSD

### Q1. What "paradigm shift" does MOSS-TTSD claim, and how does it differ from conventional text-to-speech?
> [!tip]- Answer
> MOSS-TTSD reframes synthesis as "script-to-conversation" rather than "text-to-speech," prioritizing the flow and emotional nuance of continuous multi-party interaction over isolated single-speaker fidelity. It is described as the long-form dialogue specialist of the MOSS-TTS family, built as a backbone for creators needing seamless transitions between speaker personas without losing narrative continuity. See [[wiki/01-overview|Overview]].

### Q2. What are MOSS-TTSD's limits on speaker count, session duration, and language coverage?
> [!tip]- Answer
> MOSS-TTSD supports 1 to 5 speakers with flexible control, handling natural turn-taking, overlapping speech patterns, and distinct persona maintenance. It models up to 60 minutes of coherent audio in a single session with consistent identity, and covers 20 languages including Chinese, English, Japanese, and European languages with explicit per-language codes. See [[wiki/01-overview|Overview]].

### Q3. How does the continuation quick-start workflow perform zero-shot voice cloning?
> [!tip]- Answer
> The continuation workflow takes a short reference audio plus a prefix transcript per speaker, tagged with turn markers like [S1] and [S2], and the model continues generation in each speaker's identity. It loads OpenMOSS-Team/MOSS-TTSD-v1.0 with the OpenMOSS-Team/MOSS-Audio-Tokenizer via AutoProcessor/AutoModel, encodes reference audios, builds user/assistant messages, and decodes generated codes to per-segment wav files under output/. See [[wiki/01-overview|Overview]].

### Q4. What is the role of inference.py, and which modes and defaults does it expose?
> [!tip]- Answer
> inference.py is the multi-GPU batch entry point that shards an input JSONL over all visible CUDA devices, prepares each line via generation_utils.prepare_sample, and merges per-rank outputs into output.jsonl. It supports four modes — generation, continuation, voice_clone, voice_clone_and_continuation — defaulting to generation, with --text_normalize and --sample_rate_normalize off by default and batch_size defaulting to 1. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. What does generation_utils.py centralize, and how are sampling arguments resolved?
> [!tip]- Answer
> generation_utils.py centralizes text normalization (speaker-tag repair, laughter mapping, punctuation collapsing), sharded JSONL reading, path resolution, multi-speaker prompt-audio encoding, and sampling-arg resolution consumed by inference.py. Sampling args resolve as CLI value > generation_config.json > fallback (max_new_tokens 8192, temperature 1.1, top_p 0.9, top_k 50, repetition_penalty 1.1) via resolve_sampling_args. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What does the Gradio demo offer, and what pins the runtime environment?
> [!tip]- Answer
> gradio_demo.py is the interactive 1–5 speaker demo with hard-coded OpenMOSS-Team/MOSS-TTSD-v1.0 and MOSS-Audio-Tokenizer defaults, preset reference audios and dialogue text, and CUDA attention auto-selection between flash_attention_2, sdpa, and eager. The runtime is pinned by requirements.txt (torch==2.9.1+cu128, transformers==5.0.0, gradio==6.5.1, soundfile==0.13.1, with flash_attn commented out), installed via conda plus pip install -r requirements.txt and pip install flash-attn. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Would you recommend MOSS-TTSD for a 45-minute three-speaker multilingual podcast with cloned host voices, and why?
> [!tip]- Answer
> Yes, that scenario sits squarely in MOSS-TTSD's target: 3 speakers fit the 1–5 speaker range, 45 minutes fit the 60-minute single-session context, and zero-shot cloning needs only short reference audio per host. I would run it through the batch inference.py path in voice_clone_and_continuation mode with text normalization on, using the Gradio demo only for quick pilot tests before the full run. See [[wiki/01-overview|Overview]].
