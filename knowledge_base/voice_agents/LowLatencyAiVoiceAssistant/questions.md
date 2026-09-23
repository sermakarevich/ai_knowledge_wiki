---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Ankur2606/Low-latency-AI-Voice-Assistant

### Q1. What are the stages of the end-to-end voice assistant pipeline and which models handle each?
> [!tip]- Answer
> Voice flows through faster-whisper (tiny) for speech-to-text, a Hugging Face LLM for response generation, and Edge-TTS for text-to-speech output. The chain is voice → transcribed text → concise LLM reply → spoken audio played back to the user. See [[wiki/01-overview|Overview]].

### Q2. What does Voice Activity Detection (VAD) do in this pipeline and how is it configured?
> [!tip]- Answer
> VAD gates the pipeline by detecting actual speech and ignoring silence so only real utterances reach transcription. It lives in the faster-whisper STT path with an adjustable threshold configured at 0.1, using 16 kHz mono audio. See [[wiki/01-overview|Overview]].

### Q3. What are the exact STT, LLM, and TTS model configurations?
> [!tip]- Answer
> STT uses faster-whisper (tiny) at 16 kHz sampling, mono channel, with VAD threshold 0.1. The LLM is a selectable Hugging Face model capped at 60 tokens / 2 sentences for concise replies, and TTS uses edge-tts with tunable pitch, male/female voice type, and speed. See [[wiki/01-overview|Overview]].

### Q4. What is the latency target and which techniques are suggested to hit it?
> [!tip]- Answer
> The target is sub-500 ms response latency. The suggested techniques are WRTC low-latency streaming frameworks, efficient threading/pipelines, async handoff of transcribed text to the inference API, and capping LLM output at 60 tokens / 2 sentences. See [[wiki/01-overview|Overview]].

### Q5. How does the Streamlit entry point (app.py) drive the speak → respond → speak-back flow?
> [!tip]- Answer
> A "Start Speaking" button triggers asyncio capture_and_transcribe_audio, then generate_llm_response with the transcript plus joined conversation history, then convert_text_to_speech and play_audio. Per-session chat state persists in st.session_state.conversation_history via update_conversation / display_conversation helpers, and the sidebar exposes pitch (−10 to +10), speed (−50 to +50), and voice (JennyNeural/GuyNeural) controls. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. How does the CLI entry point (main.py) loop, and how is the TTS backend selected?
> [!tip]- Answer
> main_interaction_loop transcribes audio in a forever loop, exits on a spoken "stop" keyword, and threads flattened conversation history into each generate_llm_response call. The --kokoro / -k flag selects local Kokoro-82M streaming (stream_kokoro_tts) versus the default cloud Edge-TTS path (convert_text_to_speech with fixed +0% rate / +0Hz pitch plus play_audio). See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. (Evaluation) Would you recommend this repo as the basis for a latency-sensitive production voice assistant, and why?
> [!tip]- Answer
> I would recommend it only as a prototype or starting point, not as production-ready, because its sub-500 ms target rests on suggested streaming, async, and threading optimizations rather than measured results, and the tiny STT model plus 60-token cap trade quality for speed. A production decision should benchmark real latency and accuracy first, verify the ~2GB initial model download and the HF_API_KEY / GROQ_API_KEY handling, and harden the Streamlit path before committing. See [[wiki/01-overview|Overview]].
