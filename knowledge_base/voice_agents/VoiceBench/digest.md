> [[index|Wiki]] | [[summary|Summary]]
# MatthewCYM/VoiceBench — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** VoiceBench is a benchmark harness for LLM-based voice assistants that pairs a multi-subset spoken-instruction dataset suite with a three-step generate-then-judge-then-score evaluation flow.
## Key points
- VoiceBench benchmarks LLM-based voice assistants via spoken (and text) instructions, exposing a leaderboard, paper, and Hugging Face dataset from the repo header (README.md:7-13).
- The dataset suite is hosted as `hlt-lab/voicebench` on Hugging Face and loaded with `load_dataset("hlt-lab/voicebench", '<subset>')` (README.md:48-62).
- The suite covers 11 subsets spanning open-ended QA, multiple-choice QA, reference-based QA, multi-turn QA, instruction following, reasoning, and safety, with Google TTS or human audio sources (README.md:66-79).
- Response generation runs via `python main.py --model <name> --data <subset> --split <split> --modality <audio|text>`, writing e.g. `naive-alpacaeval-test-audio.jsonl` (README.md:87-99).
- GPT-based judging with `gpt-4o-mini` via `api_judge.py` applies only to `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa`, and is skipped for all other subsets (README.md:101-108).
- Final scoring runs via `python evaluate.py --src_file <judged-file> --evaluator <open|qa|ifeval|harm|mcq|bbh>` with a per-subset evaluator mapping (README.md:111-122).
- Setup pins `python=3.10`, `torch==2.1.2` / `torchvision==0.16.2` / `torchaudio==2.1.2` (cu121) plus `xformers==0.0.23 --no-deps` and `requirements.txt` (README.md:37-44).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repo root holds the three runnable entry points (`main.py`, `api_judge.py`, `evaluate.py`), the pinned `requirements.txt` dependency set, and a standard Python `.gitignore`.
## Key points
- `main.py` is the response-generation entry point: it loads `hlt-lab/voicebench` via `load_dataset`, instantiates a model from `model_cls_mapping`, and writes `{model}-{data}-{split}-{modality}.jsonl` (main.py:11-14, main.py:18-22, main.py:48).
- `main.py` supports three inference modalities — `text` via `generate_text`, `audio` via `generate_audio`, and `ttft` via `generate_ttft` with a cold-start warmup call — selected by `--modality` (main.py:14, main.py:25-40).
- `api_judge.py` is the GPT-based judge: it scores each JSONL record with `gpt-4o-mini` through `src.api.generate_text_chat` (`n=3`, `temperature=0.5`, `top_p=0.95`, `max_tokens=1024`) using 4 workers, and writes `result-<src_file>` (api_judge.py:45-65, api_judge.py:70, api_judge.py:81-85).
- `api_judge.py` picks one of two judge prompts per record: the 1–5 open-ended rubric (`meta_prompt_open`) when no `reference` key exists, or the Yes/No reference-grounded prompt (`meta_prompt_qa`) when it does (api_judge.py:11-42, api_judge.py:45-48).
- `evaluate.py` is the final-scoring entry point: it reads a JSONL `--src_file`, instantiates the `--evaluator` chosen from `evaluator_mapping` keys, and logs `evaluator.evaluate(data)` (evaluate.py:9-10, evaluate.py:17-18).
- `requirements.txt` pins the evaluation stack including `transformers==4.47.0`, `datasets==3.0.0`, `openai==1.48.0`, `loguru==0.7.2`, plus audio/speech packages (`librosa==0.10.2.post1`, `openai-whisper==20231117`, `whisperspeech==0.8`, `snac==1.2.0`) (requirements.txt:4, requirements.txt:9, requirements.txt:11-12, requirements.txt:24, requirements.txt:29-32).
- `.gitignore` is the standard Python template (163 lines) excluding bytecode (`__pycache__/`, `*.py[cod]`), packaging artefacts (`build/`, `dist/`, `*.egg-info/`), test/coverage outputs, and environments (`.env`, `.venv`, `env/`, `venv/`) (`.gitignore:1-12`, `.gitignore:17-35`, `.gitignore:47-60`, `.gitignore:132-140`).

## The system in five moves
1. VoiceBench frames evaluation of LLM-based voice assistants around spoken instructions drawn from the Hugging Face `hlt-lab/voicebench` suite across 11 task-type subsets.
2. The pinned conda/torch/xformers/requirements environment grounds reproducible runs in audio and text modalities.
3. `main.py` generates assistant responses per subset/split/modality and persists them as `{model}-{data}-{split}-{modality}.jsonl`.
4. `api_judge.py` applies `gpt-4o-mini` judging — 1–5 open-ended rubric or Yes/No reference-grounded prompt, gated to four subsets — and writes `result-` files.
5. `evaluate.py` maps each subset to its final evaluator (`open|qa|ifeval|harm|mcq|bbh`) and logs the score, completing the generate-then-judge-then-score arc.
