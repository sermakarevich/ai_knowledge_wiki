> [[index|Wiki]] | [[summary|Summary]]
# livekit/eot-bench — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** eot-bench is an open, reproducible benchmark for end-of-turn detection that evaluates models at real pauses in real human-to-agent conversations under explicit latency and interruption budgets.
## Key points
- eot-bench answers the per-pause question "is the user done talking?", where answering too early causes talk-overs and too late causes dead air (README.md:16).
- It provides common ground for the field because prior results came from different private datasets and methodologies that are difficult to reproduce or compare (README.md:23).
- It pairs an open benchmark with the first open dataset `livekit/eot-bench-data` of real human-to-agent conversations in 14 languages, evaluated at real pauses under real latency and interruption budgets (README.md:29).
- Each dataset row is a complete user turn annotated with every silence pause of at least 100 ms, where the final pause is the true end of turn and earlier pauses are mid-turn hesitations to listen through (README.md:46).
- Models are ranked by the false-cutoff vs. latency tradeoff, reporting best latency at a fixed false-cutoff budget and vice versa plus the full Pareto frontier, not by single accuracy scores (README.md:122).
- Latency is conversational dead air (how long the policy holds before confident the turn is over), not model inference/compute time (README.md:117).
- LiveKit Turn Detector v1 posts the strongest overall results in English and across all 14 languages, with committed reproducible artifacts under `output/` and an interactive leaderboard (README.md:55).
- A silence-only VAD baseline runs through the identical evaluation/policy grid so every learned and commercial detector is measured against timing alone (README.md:98).

## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The top level carries no code, only a 20-line `.gitignore` for local caches, secrets, and generated outputs plus a 14-line `requirements.txt` pinning the data/audio/eval dependency stack.
## Key points
- The component contains exactly 2 source files, `.gitignore` (20 lines) and `requirements.txt` (14 lines), with no top-level executable code (`.gitignore:1`, `requirements.txt:1`).
- `.gitignore` excludes OS and Python byproducts `.DS_Store`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, and `*egg-info` (`.gitignore:1`, `.gitignore:6`, `.gitignore:8-9`, `.gitignore:19`).
- `.gitignore` excludes local virtualenvs `.venv/` and `.venv-test/` (`.gitignore:7`, `.gitignore:18`).
- `.gitignore` excludes Hugging Face local caches `.hf_datasets_cache/`, `.hf_home/`, `.hf_tmp/`, plus generic `.cache/` (`.gitignore:2-4`, `.gitignore:10`).
- `.gitignore` excludes secrets `eot_harness/.env`, `.env`, and `/.env` (`.gitignore:11`, `.gitignore:16-17`).
- `.gitignore` excludes generated/local working trees `eot_harness/output/`, `eot_harness/notebooks/`, and `tmp/` (`.gitignore:12-14`).
- `requirements.txt` pins the data/eval stack to `datasets>=3.2.0`, `pandas>=2.2.0`, `pyarrow>=18.0.0`, `numpy<2`, and `scikit-learn>=1.5.0` (`requirements.txt:1`, `requirements.txt:6-8`, `requirements.txt:10`).
- `requirements.txt` pins audio, plotting, infra, and async deps to `librosa>=0.10.0`, `soundfile>=0.12.1`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `modal>=1.0.0`, `websockets>=15.0.0`, `huggingface_hub>=0.30.0`, and `python-dotenv>=1.0.0` (`requirements.txt:2-5`, `requirements.txt:9`, `requirements.txt:11-13`).

## The system in five moves
1. Every pause in a voice conversation forces the same live decision — is the user done talking — where firing early talks over people and waiting late creates dead air.
2. eot-bench grounds that decision in real human-to-agent turns in 14 languages, annotating every ≥100 ms silence so the final pause is the true end of turn and earlier pauses are hesitations to hold through.
3. Models are judged on the false-cutoff vs. latency tradeoff under explicit budgets plus the Pareto frontier, with latency defined as conversational dead air rather than inference time.
4. A silence-only VAD baseline runs the identical policy grid so learned and commercial detectors are all measured against timing alone, with LiveKit Turn Detector v1 leading and artifacts committed under `output/`.
5. The repo's top level supports that reproducibility with no code of its own — just a `.gitignore` keeping caches, secrets, and generated outputs out of version control and a `requirements.txt` pinning the data, audio, and eval stack.
