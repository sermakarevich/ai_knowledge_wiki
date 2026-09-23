[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo root holds the three runnable entry points (`main.py`, `api_judge.py`, `evaluate.py`), the pinned `requirements.txt` dependency set, and a standard Python `.gitignore`.
## Key points
- `main.py` is the response-generation entry point: it loads `hlt-lab/voicebench` via `load_dataset`, instantiates a model from `model_cls_mapping`, and writes `{model}-{data}-{split}-{modality}.jsonl` (main.py:11-14, main.py:18-22, main.py:48).
- `main.py` supports three inference modalities — `text` via `generate_text`, `audio` via `generate_audio`, and `ttft` via `generate_ttft` with a cold-start warmup call — selected by `--modality` (main.py:14, main.py:25-40).
- `api_judge.py` is the GPT-based judge: it scores each JSONL record with `gpt-4o-mini` through `src.api.generate_text_chat` (`n=3`, `temperature=0.5`, `top_p=0.95`, `max_tokens=1024`) using 4 workers, and writes `result-<src_file>` (api_judge.py:45-65, api_judge.py:70, api_judge.py:81-85).
- `api_judge.py` picks one of two judge prompts per record: the 1–5 open-ended rubric (`meta_prompt_open`) when no `reference` key exists, or the Yes/No reference-grounded prompt (`meta_prompt_qa`) when it does (api_judge.py:11-42, api_judge.py:45-48).
- `evaluate.py` is the final-scoring entry point: it reads a JSONL `--src_file`, instantiates the `--evaluator` chosen from `evaluator_mapping` keys, and logs `evaluator.evaluate(data)` (evaluate.py:9-10, evaluate.py:17-18).
- `requirements.txt` pins the evaluation stack including `transformers==4.47.0`, `datasets==3.0.0`, `openai==1.48.0`, `loguru==0.7.2`, plus audio/speech packages (`librosa==0.10.2.post1`, `openai-whisper==20231117`, `whisperspeech==0.8`, `snac==1.2.0`) (requirements.txt:4, requirements.txt:9, requirements.txt:11-12, requirements.txt:24, requirements.txt:29-32).
- `.gitignore` is the standard Python template (163 lines) excluding bytecode (`__pycache__/`, `*.py[cod]`), packaging artefacts (`build/`, `dist/`, `*.egg-info/`), test/coverage outputs, and environments (`.env`, `.venv`, `env/`, `venv/`) (`.gitignore:1-12`, `.gitignore:17-35`, `.gitignore:47-60`, `.gitignore:132-140`).
---
## main.py
Response generation driver (main.py:1-57). Verbatim imports and dispatch (main.py:1-5, main.py:32-40):
```python
from datasets import load_dataset, Audio
from argparse import ArgumentParser
from src.models import model_cls_mapping
import json
from tqdm import tqdm
from loguru import logger
```
```python
data = load_dataset('hlt-lab/voicebench', args.data, split=args.split)
data = data.cast_column("audio", Audio(sampling_rate=16_000))
model = model_cls_mapping[args.model]()
```
```python
if args.modality == 'ttft':
    # avoid cold start
    _ = model.generate_ttft(data[0]['audio'])
for item in tqdm(data, total=len(data)):
    tmp = {k: v for k, v in item.items() if k != 'audio'}
    if args.modality == 'text':
        response = model.generate_text(item['prompt'])
    elif args.modality == 'audio':
        response = model.generate_audio(item['audio'])
    elif args.modality == 'ttft':
        response = model.generate_ttft(item['audio'])
```
Flags (main.py:11-14):

| Flag | Default | Choices / meaning |
|---|---|---|
| `--model` | `qwen2` | keys of `model_cls_mapping` |
| `--data` | `alpacaeval` | VoiceBench subset name passed to `load_dataset` |
| `--split` | `test` | dataset split |
| `--modality` | `audio` | `audio` \| `text` \| `ttft` |

Output filename pattern (main.py:48):
```python
output_file = f'{args.model}-{args.data}-{args.split}-{args.modality}.jsonl'
```
Each output record is the input item minus `audio` plus a `response` field, logged with `logger.info` per item (main.py:32-45).

## api_judge.py
GPT judge driver (api_judge.py:1-93). Verbatim client and scoring call (api_judge.py:9, api_judge.py:50-63):
```python
client = OpenAI()
```
```python
rtn = [
    item.message.content.strip() for item in generate_text_chat(
        client=client,
        model='gpt-4o-mini',
        messages=[{"role": "system",
                   "content": "You are a helpful assistant who tries to help answer the user's question."},
                  {"role": "user", "content": prompt}],
        max_tokens=1024,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        temperature=0.5, top_p=0.95, n=3
    ).choices
]
item['score'] = rtn
```
Prompt selection (api_judge.py:45-48):
```python
def generate(item):
    if "reference" in item:
        prompt = meta_prompt_qa.replace('{prompt}', item['prompt']).replace('{reference}', item['reference']).replace('{response}', item['response'])
    else:
        prompt = meta_prompt_open.replace("{prompt}", item['prompt']).replace('{response}', item['response'])
```
Verbatim prompts: `meta_prompt_open` is the 1–5 speech-interaction rubric ending in `After evaluating, please output the score only without anything else. You don't need to provide any explanations.` with `{prompt}` / `{response}` slots (api_judge.py:11-28); `meta_prompt_qa` is the `### Question / ### Reference answer / ### Candidate answer` template ending in `Please only output a single "Yes" or "No". Do not output anything else.` (api_judge.py:30-42).
CLI and I/O (api_judge.py:68-85):

| Flag | Meaning |
|---|---|
| `--src_file` (required) | input `.jsonl`, one JSON object per line |

Parallelism is `multiprocessing.Pool(4)` over `pool.imap(generate, data)` with a `tqdm` bar, and output is `'result-' + args.src_file`, one JSON record per line (api_judge.py:81-85).

## evaluate.py
Final scoring driver, 23 lines (evaluate.py:1-23). Verbatim core (evaluate.py:9-18):
```python
parser.add_argument('--src_file', type=str, required=True)
parser.add_argument('--evaluator', type=str, required=True, choices=list(evaluator_mapping.keys()))
```
```python
evaluator = evaluator_mapping[args.evaluator]()
logger.info(evaluator.evaluate(data))
```
Input is read line-by-line with `json.loads(line.strip())` (evaluate.py:12-16); no output file is written — the score is only logged.

## requirements.txt
Pinned dependency list, 36 lines (requirements.txt:1-36). Exact pins include (requirements.txt:2-6, requirements.txt:24):
```
accelerate==0.33.0
bitsandbytes==0.43.1
datasets==3.0.0
evaluate==0.4.3
huggingface-hub==0.23.5
transformers==4.47.0
```
Audio/speech and metric packages (requirements.txt:11-12, requirements.txt:16-17, requirements.txt:29-32):
```
openai==1.48.0
openai-whisper==20231117
qa_metrics==0.2.17
sacrebleu==2.4.3
librosa==0.10.2.post1
snac==1.2.0
whisperspeech==0.8
```
Unpinned entries are `absl-py`, `immutabledict`, `langdetect`, `nltk`, `webdataset`, `vector_quantize_pytorch` (requirements.txt:1, requirements.txt:7-8, requirements.txt:10, requirements.txt:33-34).

## .gitignore
Standard Python template, 163 lines (`.gitignore:1-163`). It ignores bytecode (`__pycache__/`, `*.py[cod]`, `*$py.class`), C extensions (`*.so`), packaging outputs (`build/`, `dist/`, `*.egg-info/`, `*.egg`, `MANIFEST`), installer logs, test/coverage reports (`.tox/`, `.coverage*`, `.pytest_cache/`, `htmlcov/`), environments (`.env`, `.venv`, `env/`, `venv/`), and editor/type-checker caches (`.mypy_cache/`, `.pyre/`, `.pytype/`, `cython_debug/`) (`.gitignore:1-12`, `.gitignore:17-35`, `.gitignore:47-60`, `.gitignore:132-164`).

No files were noted as truncated in this chunk; all five source files are covered in full.

**Covers:** `main.py`, `api_judge.py`, `evaluate.py`, `requirements.txt`, `.gitignore` (repo root top-level files)
