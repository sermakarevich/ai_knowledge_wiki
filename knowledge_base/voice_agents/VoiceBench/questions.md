---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: MatthewCYM/VoiceBench

### Q1. What is VoiceBench and what two components make up its benchmark harness?
> [!tip]- Answer
> VoiceBench is a benchmark harness for LLM-based voice assistants that pairs a multi-subset spoken-instruction dataset suite with a three-step generate-then-judge-then-score evaluation flow. The dataset suite lives on Hugging Face as `hlt-lab/voicebench`, while the flow runs through `main.py`, `api_judge.py`, and `evaluate.py`. See [[wiki/01-overview|Overview]].

### Q2. Which 11 subsets does the VoiceBench dataset suite cover, and how do their task types and audio sources differ?
> [!tip]- Answer
> The suite spans open-ended QA (`alpacaeval`, `alpacaeval_full`, `commoneval`, `wildvoice`), multiple-choice QA (`openbookqa`, `mmsu`), reference-based QA (`sd-qa`), multi-turn QA (`mtbench`), instruction following (`ifeval`), reasoning (`bbh`), and safety (`advbench`). Audio comes from Google TTS for most subsets and from human recordings for `commoneval`, `wildvoice`, `sd-qa`, and `bbh`. See [[wiki/01-overview|Overview]].

### Q3. What are the three steps of the VoiceBench evaluation flow, and which subsets skip the GPT-judging step?
> [!tip]- Answer
> Step 1 generates assistant responses with `main.py`, step 2 applies `gpt-4o-mini` judging via `api_judge.py`, and step 3 computes final scores with `evaluate.py` and a per-subset evaluator. Judging applies only to `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa`, and is skipped for all other subsets. See [[wiki/01-overview|Overview]].

### Q4. How does `main.py` generate responses, and what do its `--modality` options do?
> [!tip]- Answer
> `main.py` loads the chosen subset via `load_dataset('hlt-lab/voicebench', ...)`, casts audio to 16 kHz, instantiates a model from `model_cls_mapping`, and writes `{model}-{data}-{split}-{modality}.jsonl`. The `text` modality calls `generate_text` on the prompt, `audio` calls `generate_audio` on the waveform, and `ttft` calls `generate_ttft` after a cold-start warmup call. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. How does `api_judge.py` score response files, and how does it choose between its two judge prompts?
> [!tip]- Answer
> It scores each JSONL record with `gpt-4o-mini` via `generate_text_chat` (`n=3`, `temperature=0.5`, `top_p=0.95`, `max_tokens=1024`) using a 4-worker pool, writing `result-<src_file>`. Records without a `reference` key get the 1–5 open-ended speech-interaction rubric, while records with one get the Yes/No reference-grounded prompt. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. How does `evaluate.py` produce final scores, and what environment and dependency pins support reproducible runs?
> [!tip]- Answer
> `evaluate.py` reads the JSONL `--src_file` line by line, instantiates the `--evaluator` from `evaluator_mapping` keys (`open|qa|ifeval|harm|mcq|bbh`), and logs the score without writing an output file. Reproducibility rests on `python=3.10`, `torch==2.1.2` / `torchvision==0.16.2` / `torchaudio==2.1.2` (cu121), `xformers==0.0.23 --no-deps`, and `requirements.txt` pins such as `transformers==4.47.0` and `datasets==3.0.0`. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Would you recommend VoiceBench as the primary benchmark for a new voice assistant, and what judgment supports that?
> [!tip]- Answer
> Recommend it as a strong breadth-first starting point but not the sole verdict, since its 11 subsets cover open-ended, multi-turn, instruction-following, reasoning, and safety cases in both audio and text modalities. Treat GPT-judged open-ended scores as noisy signals to triangulate with the deterministic `mcq`/`ifeval`/`bbh` evaluators, and confirm any safety claim with dedicated red-teaming beyond `advbench`. See [[wiki/01-overview|Overview]].
