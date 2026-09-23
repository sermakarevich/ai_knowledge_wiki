> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
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
---
## .gitignore
Verbatim content (`.gitignore:1-20`):
```
.DS_Store
.cache/
.hf_datasets_cache/
.hf_home/
.hf_tmp/
.pytest_cache/
.venv/
__pycache__/
*.py[cod]
eot_harness/.env
eot_harness/output/
eot_harness/notebooks/
tmp/

.env
/.env
.venv-test/

*egg-info
```
| Ignored path (`.gitignore:1-20`) | Category |
|---|---|
| `.DS_Store` (`.gitignore:1`) | macOS artifact |
| `.cache/`, `.hf_datasets_cache/`, `.hf_home/`, `.hf_tmp/` (`.gitignore:2-5`) | cache dirs |
| `.pytest_cache/` (`.gitignore:6`) | test cache |
| `.venv/`, `.venv-test/` (`.gitignore:7`, `.gitignore:18`) | virtualenvs |
| `__pycache__/`, `*.py[cod]` (`.gitignore:8-9`) | Python byproducts |
| `eot_harness/.env`, `.env`, `/.env` (`.gitignore:10`, `.gitignore:15-16`) | secrets |
| `eot_harness/output/`, `eot_harness/notebooks/`, `tmp/` (`.gitignore:11-13`) | generated/working dirs |
| `*egg-info` (`.gitignore:19`) | packaging byproduct |

## requirements.txt
Verbatim content (`requirements.txt:1-14`):
```
datasets>=3.2.0
huggingface_hub>=0.30.0
librosa>=0.10.0
matplotlib>=3.8.0
modal>=1.0.0
numpy<2
pandas>=2.2.0
pyarrow>=18.0.0
python-dotenv>=1.0.0
scikit-learn>=1.5.0
seaborn>=0.13.0
soundfile>=0.12.1
websockets>=15.0.0
```
| Dependency (`requirements.txt:1-13`) | Constraint |
|---|---|
| `datasets` (`requirements.txt:1`) | `>=3.2.0` |
| `huggingface_hub` (`requirements.txt:2`) | `>=0.30.0` |
| `librosa` (`requirements.txt:3`) | `>=0.10.0` |
| `matplotlib` (`requirements.txt:4`) | `>=3.8.0` |
| `modal` (`requirements.txt:5`) | `>=1.0.0` |
| `numpy` (`requirements.txt:6`) | `<2` |
| `pandas` (`requirements.txt:7`) | `>=2.2.0` |
| `pyarrow` (`requirements.txt:8`) | `>=18.0.0` |
| `python-dotenv` (`requirements.txt:9`) | `>=1.0.0` |
| `scikit-learn` (`requirements.txt:10`) | `>=1.5.0` |
| `seaborn` (`requirements.txt:11`) | `>=0.13.0` |
| `soundfile` (`requirements.txt:12`) | `>=0.12.1` |
| `websockets` (`requirements.txt:13`) | `>=15.0.0` |

**Covers:** `.gitignore`, `requirements.txt`
