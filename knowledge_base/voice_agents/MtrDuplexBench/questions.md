---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: ZhangHe0918/MTR-DuplexBench

### Q1. What is MTR-DuplexBench and what kind of models does it evaluate?

> [!tip]- Answer
> MTR-DuplexBench is an ACL 2026 Findings benchmark that evaluates full-duplex speech language models on multi-round conversations. It distributes a paper, a HuggingFace dataset, and evaluation scripts for user-model evaluation. Its standard workflow runs scenario-encoding → stereo-audio inference → Eval-script scoring. See [[wiki/01-overview|Overview]].

### Q2. How do you obtain MTR-DuplexBench and what does its top-level layout contain?

> [!tip]- Answer
> After `git lfs install`, clone it with `git clone https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench`. The tree has three top-level areas: `code/` with evaluation scripts under `Eval/`, `data/` with evaluation data, and `envs/` with environment configurations. Core dependencies install via `pip install openai whisper torch`, and GPT-4o judging requires `OPENAI_API_KEY` to be set. See [[wiki/01-overview|Overview]].

### Q3. What are the four evaluation dimensions and how do their scripts, audio formats, and judges differ?

> [!tip]- Answer
> The four dimensions are Dialogue Quality (script `gpt4o_mark_in_turn_GT_condor.py`, MP3, GPT-4o judge), Conversational Features single- and multi-scenario (`eval_1/2/3/4_scenarios.py` plus pause-handling/background scripts, WAV, no LLM judge), Instruction Following (`instruction_following_evaluation.py`, WAV, GPT-4o), and Safety (`safety_evaluation.py`, WAV, GPT-4o). Conversational Features is the only dimension scored purely by computed metrics rather than an LLM judge. Dialogue Quality is also the only dimension using MP3 instead of WAV. See [[wiki/01-overview|Overview]].

### Q4. What is the three-step evaluation pipeline and what stereo audio convention must model output follow?

> [!tip]- Answer
> The pipeline is: read JSON scenario encodings from `Scenarios_encoding/`, run your own full-duplex model inference, then run the `Eval/` scripts that handle Whisper ASR plus metric computation. Scenario encodings define dialogue structure, turn-taking patterns, and timing, with per-dimension files such as `scenario_encoding_{smooth,interruption,pause,background}.json`. Model output must be stereo audio with the left channel as user audio and the right channel as model audio, following per-dimension naming conventions. See [[wiki/01-overview|Overview]].

### Q5. How is the Dialogue Quality dimension scored?

> [!tip]- Answer
> Dialogue Quality scores whether model turns are semantically meaningful on a 0–5 scale using GPT-4o as judge via `gpt4o_mark_in_turn_GT_condor.py`. Inference input is `data/Dialogue_Quality/*.mp3` plus turn boundaries in `data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl`, and output is stereo MP3 files with user on the left and model on the right. The run writes a JSONL file with per-turn scores and prints an average model turn score. See [[wiki/01-overview|Overview]].

### Q6. How are Conversational Features evaluated across single- and multi-scenario settings?

> [!tip]- Answer
> This dimension measures turn-taking behavior — latency, backchannel frequency, and correct handling of interruptions, pauses, and background noise — reporting success, latency, and frequency metrics on stereo WAV output. Single scenarios map to dedicated scripts: smooth-turntaking to `eval_1_scenario.py`, pause-handling to `eval_single_scenario_pause_handling.py`, and background to `eval_single_scenario_background.py`. Multi-scenario scripts `eval_2/3/4_scenarios.py` form a layered hierarchy delegating to lower ones, and the usage pattern is library-style: transcribe with `asr_incremental_save.py`, load each dialogue's encoding, call the matching `eval_N_scenarios()` function, and aggregate the metrics. See [[wiki/01-overview|Overview]].

### Q7. How do the Instruction Following and Safety evaluations work, and what does the shared ASR utility provide?

> [!tip]- Answer
> Both use GPT-4o as a binary judge on stereo WAV conversations: Instruction Following scores 0/1 for whether the model followed user instructions (inputs `data/Instruction_Following/audios/*.wav` plus `instruction_following_data.json`), while Safety scores 0=safe versus 1=unsafe for responses to harmful requests (inputs `data/Safety/audios/*.wav` plus `safety_data.json`). Each writes a JSON results file with per-round scores plus an overall following rate or safe/unsafe rate statistics, supporting `--asr_cache_file`, `--round_start_json`, and `--max_round` options. The shared `asr_incremental_save.py` utility provides Whisper-based transcription with independent left/right channel handling, incremental saving, and JSON caching for reuse across dimensions. See [[wiki/01-overview|Overview]].

### Q8. Would you recommend MTR-DuplexBench as the primary benchmark for a team building a multi-round full-duplex speech LLM, and why?

> [!tip]- Answer
> Yes, for teams whose core risk is full-duplex interaction rather than single-turn quality, because it is the only benchmark in this snapshot combining graded dialogue quality, signal-level turn-taking metrics, instruction obedience, and safety over multi-round stereo audio in one reproducible three-step pipeline. The caveats are its dependence on GPT-4o as judge (API key, cost, judge bias), Whisper transcription quality, and strict stereo/encoding conventions. The team should therefore budget for API costs and validate a sample of scores against human listening before treating them as definitive. See [[wiki/01-overview|Overview]].
