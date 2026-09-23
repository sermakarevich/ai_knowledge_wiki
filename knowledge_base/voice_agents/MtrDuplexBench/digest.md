> [[index|Wiki]] | [[summary|Summary]]
# ZhangHe0918/MTR-DuplexBench — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** MTR-DuplexBench is an ACL 2026 Findings benchmark that evaluates full-duplex speech language models on multi-round conversations by running a scenario-encoding → stereo-audio inference → Eval-script scoring pipeline.
## Key points
- MTR-DuplexBench was accepted by ACL 2026 Findings and distributes paper, HuggingFace dataset, and evaluation scripts for user-model evaluation (01-overview.md:9-13).
- The cloned tree has three top-level areas: `code/` evaluation scripts under `Eval/`, `data/` evaluation data, and `envs/` environment configurations (01-overview.md:30-51).
- Evaluation covers four dimensions — Dialogue Quality, Conversational Features (single/multi scenario), Instruction Following, and Safety — each with its own scripts, audio format, and judge (01-overview.md:67-75).
- GPT-4o is the LLM judge for Dialogue Quality, Instruction Following, and Safety, requiring `OPENAI_API_KEY` to be set (01-overview.md:61-61).
- The standard workflow is three steps: read JSON scenario encodings from `Scenarios_encoding/`, run own-model inference to stereo audio, then run `Eval/` scripts that handle Whisper ASR plus metric computation (01-overview.md:81-85, 01-overview.md:88-90, 01-overview.md:110-117, 01-overview.md:119-121).
- Model output must be stereo audio with left channel = user audio and right channel = model audio, following per-dimension naming conventions (01-overview.md:112-117).
- Whisper-based `asr_incremental_save.py` is the shared ASR utility with independent left/right transcription, incremental saving, and JSON caching (01-overview.md:275-281).
## The system in five moves
1. Start from JSON scenario encodings that define dialogue structure, turn-taking patterns, and timing per dimension.
2. Run your own full-duplex model inference to produce stereo audio with user on the left channel and model on the right.
3. Transcribe both channels with the shared Whisper utility `asr_incremental_save.py`, caching results incrementally.
4. Score each dimension with its dedicated Eval script — GPT-4o judges for Dialogue Quality, Instruction Following, and Safety, and latency/success/frequency metrics for Conversational Features.
5. Aggregate per-turn and per-round scores into overall rates and averages for multi-round duplex comparison.
