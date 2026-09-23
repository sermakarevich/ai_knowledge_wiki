# Technical Analysis: MatthewCYM/VoiceBench

**Repository:** https://github.com/MatthewCYM/VoiceBench
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Text-only benchmarks do not measure how LLM-based voice assistants behave when instructions arrive as speech, where acoustic variation, spoken phrasing, and audio front-ends change the outcome. The primary user is a voice-assistant developer or researcher who needs a standardized, reproducible spoken evaluation with a public leaderboard.

The repo addresses this by packaging an 11-subset spoken-instruction suite hosted as `hlt-lab/voicebench` on Hugging Face and loaded per subset with `load_dataset` (README.md:48-62), covering open-ended QA, multiple-choice QA, reference-based QA, multi-turn QA, instruction following, reasoning, and safety with Google TTS and human audio sources (README.md:66-79). It adds a fixed three-step harness — response generation via `main.py`, GPT-based judging via `api_judge.py` for a gated subset list, final scoring via `evaluate.py` — plus setup pins (`python=3.10`, `torch==2.1.2`, `xformers==0.0.23`) (README.md:37-44, README.md:85-114).

## 2. High-Level Architecture

```
Hugging Face dataset ─► main.py ─► <model>-<data>-<split>-<modality>.jsonl
hlt-lab/voicebench  │   model_cls_mapping      │ response records (audio stripped)
                    │                          ▼
                    │                   api_judge.py ─► result-<src_file>.jsonl
                    │                   gpt-4o-mini, Pool(4)      │ scored records
                    │                                            ▼
                    └──────────────────── evaluate.py ─► logged score
                                          evaluator_mapping[evaluator].evaluate(data)
```

Data flow:

1. `main.py` loads `hlt-lab/voicebench` for the requested `<subset>` and split, casts `audio` to 16 kHz, and instantiates the model from `model_cls_mapping` (main.py:24-26).
2. Each item is dispatched by `--modality` to `generate_text`, `generate_audio`, or `generate_ttft` (with a cold-start warmup call for `ttft`), and the input record minus `audio` plus a `response` field is appended to `{model}-{data}-{split}-{modality}.jsonl` (main.py:29-48).
3. `api_judge.py` reads that JSONL and, only for `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa`, calls `gpt-4o-mini` with one of two prompts and writes `result-<src_file>` (README.md:101-108, api_judge.py:45-48, api_judge.py:81-85).
4. `evaluate.py` reads the (judged or raw) JSONL line by line, instantiates the `--evaluator` from `evaluator_mapping`, and logs `evaluator.evaluate(data)` with no output file (evaluate.py:12-18).
5. Evaluator choice is fixed per task family: `open` for `alpacaeval`/`commoneval`/`wildvoice`, `qa` for `sd-qa`, `ifeval`, `harm`, `mcq`, `bbh` (README.md:115-122).

Persistent state lives outside the repo: the versioned dataset on Hugging Face (`hlt-lab/voicebench`), intermediate `.jsonl` response and `result-` files on local disk, and the external leaderboard. The repo itself holds no database; `evaluate.py` persists nothing beyond the log line (evaluate.py:17-18).

## 3. The Spoken-Instruction Subset

The central concept is the named data subset: a task-typed slice of the Hugging Face dataset selected by the `--data` argument and passed directly to `load_dataset('hlt-lab/voicebench', args.data, split=args.split)` (main.py:24). Representation is a Hugging Face row with `prompt`, optional `reference`, `audio` (cast to `Audio(sampling_rate=16_000)`), plus task metadata; `main.py` strips `audio` before writing output (`{k: v for k, v in item.items() if k != 'audio'}`) (main.py:25, main.py:32-33).

Named kinds, with sizes and sources from README.md:66-79:

- Open-ended QA: `alpacaeval` (199, Google TTS), `alpacaeval_full` (636, Google TTS; leaderboard variant per README.md:81), `commoneval` (200, human), `wildvoice` (1000, human).
- Multiple-choice QA: `openbookqa` (455, Google TTS), `mmsu` (3074, Google TTS).
- Reference-based QA: `sd-qa` (553, human; split is a region code such as `aus`/`usa` per README.md:91-97).
- Multi-turn QA: `mtbench` (46, Google TTS).
- Instruction following: `ifeval` (345, Google TTS).
- Reasoning: `bbh` (1000, human).
- Safety: `advbench` (520, Google TTS).

Key queries are subset loads and record-field tests. Verbatim load pattern (README.md:56-62):

```python
from datasets import load_dataset

# Load the VoiceBench dataset
# Available subset: alpacaeval, commoneval, sd-qa, ifeval, advbench, ...
dataset = load_dataset("hlt-lab/voicebench", 'alpacaeval')
```

Judge routing keys off the same representation — presence of a `reference` key selects the QA prompt, absence selects the open-ended rubric (api_judge.py:45-48):

```python
def generate(item):
    if "reference" in item:
        prompt = meta_prompt_qa.replace('{prompt}', item['prompt']).replace('{reference}', item['reference']).replace('{response}', item['response'])
    else:
        prompt = meta_prompt_open.replace("{prompt}", item['prompt']).replace('{response}', item['response'])
```

## 4. LLM / External Service Integration

Providers: Hugging Face Hub (dataset fetch via `datasets.load_dataset`) and OpenAI (`gpt-4o-mini` judge via `OpenAI()` client and `src.api.generate_text_chat`) (main.py:24, api_judge.py:9, api_judge.py:50-63).

Required calls: dataset download in `main.py` on every run; `gpt-4o-mini` scoring in `api_judge.py` (`n=3`, `temperature=0.5`, `top_p=0.95`, `max_tokens=1024`) for the four judged subsets (api_judge.py:62-74, README.md:101-108). Optional/skipped calls: judging is explicitly skipped for all subsets other than `alpacaeval`, `commoneval`, `wildvoice`, `sd-qa` (README.md:108); those go directly from `main.py` output to `evaluate.py`.

Env vars: no env-var table is documented in the wiki pages. `api_judge.py` constructs `OpenAI()` with no explicit key argument (api_judge.py:9), so the standard `OPENAI_API_KEY` credential chain is required at runtime, and `.gitignore` excludes `.env` files (`.gitignore:132-140`). No other API keys, endpoints, or model-hosting integrations are described in the covered pages; the assistant models under test are local classes behind `model_cls_mapping`, not remote API calls (main.py:26).

## 5. The Generate-Judge-Score Pipeline

Step 1 — Generate responses (`main.py:1-57`). Parse `--model/--data/--split/--modality` (main.py:11-14); load and resample the dataset with `load_dataset` plus `cast_column("audio", Audio(sampling_rate=16_000))` (main.py:24-25); instantiate `model_cls_mapping[args.model]()` (main.py:26); for `ttft`, issue one warmup `generate_ttft(data[0]['audio'])` to avoid cold start (main.py:29-31); loop with `tqdm`, dispatch to `model.generate_text(item['prompt'])` (main.py:35), `model.generate_audio(item['audio'])` (main.py:37), or `model.generate_ttft(item['audio'])` (main.py:39); write `{model}-{data}-{split}-{modality}.jsonl` with `response` added and `audio` removed (main.py:48, main.py:32-45).

Step 2 — GPT judge (`api_judge.py:1-93`). Select prompt per record by `reference`-key presence (api_judge.py:45-48); call `generate_text_chat` with `model='gpt-4o-mini'`, system role `You are a helpful assistant who tries to help answer the user's question`, `n=3` (api_judge.py:62-74); store the list of stripped contents as `item['score']` (api_judge.py:76); run over the file with `multiprocessing.Pool(4)` and `pool.imap` under `tqdm` (api_judge.py:81-85); write `'result-' + args.src_file` as one JSON object per line (api_judge.py:81-85). CLI takes only required `--src_file` (api_judge.py:68-85).

Step 3 — Score (`evaluate.py:1-23`). Parse required `--src_file` and `--evaluator` with `choices=list(evaluator_mapping.keys())` (evaluate.py:9-10); read records with `json.loads(line.strip())` (evaluate.py:12-16); run `evaluator = evaluator_mapping[args.evaluator]()` then `logger.info(evaluator.evaluate(data))` (evaluate.py:17-18).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| README.md | 149+ (truncated at 149) | Project header, leaderboard/paper/dataset links, news log 2024.10.30–2026.04.20, setup, 11-subset table, three-step pipeline, Awesome Voice Assistants catalog (README.md:7-149) |
| main.py | 1-57 | Response-generation entry point; arg parsing, dataset load/resample, model dispatch across text/audio/ttft, JSONL writer (main.py:11-48) |
| api_judge.py | 1-93 | GPT-judge entry point; two prompt templates, gpt-4o-mini scoring call, Pool(4) driver, result- writer (api_judge.py:11-85) |
| evaluate.py | 1-23 | Final-scoring entry point; src_file/evaluator args, JSONL reader, evaluator dispatch and log-only output (evaluate.py:9-18) |
| requirements.txt | 1-36 | Pinned evaluation stack (transformers, datasets, openai, audio/speech, metrics) plus unpinned utilities (requirements.txt:1-36) |
| .gitignore | 1-163 | Standard Python template: bytecode, packaging, test/coverage, environments, editor caches (`.gitignore:1-164`) |
| src/models (referenced) | n/a in wiki | Provides `model_cls_mapping` imported by main.py; keys define valid `--model` values such as `naive`, `qwen2`, `diva` (main.py:3, main.py:26, README.md:91-97) |
| src/api (referenced) | n/a in wiki | Provides `generate_text_chat` wrapping the OpenAI chat call used by the judge (api_judge.py:50-63) |
| src/evaluators (referenced) | n/a in wiki | Provides `evaluator_mapping` with keys `open`, `qa`, `ifeval`, `harm`, `mcq`, `bbh` used by evaluate.py (evaluate.py:9-18, README.md:115-122) |
| Hugging Face `hlt-lab/voicebench` (external data) | n/a (remote) | Canonical persistent dataset; 11 subsets loaded per name plus split (README.md:48-62, README.md:66-79) |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| torch | `==2.1.2` | Model compute backend (cu121 wheel) (README.md:37-44) |
| torchvision | `==0.16.2` | Vision companion pin for torch stack (README.md:37-44) |
| torchaudio | `==2.1.2` | Audio I/O and resampling for 16 kHz pipeline (README.md:37-44) |
| xformers | `==0.0.23 --no-deps` | Memory-efficient attention for local models (README.md:37-44) |
| transformers | `==4.47.0` | Local model implementations behind model_cls_mapping (requirements.txt:4) |
| datasets | `==3.0.0` | `load_dataset` / `Audio` casting of hlt-lab/voicebench (requirements.txt:4, main.py:1) |
| openai | `==1.48.0` | `OpenAI()` judge client (requirements.txt:11-12, api_judge.py:9) |
| accelerate | `==0.33.0` | Distributed/quantized inference support (requirements.txt:2-6) |
| bitsandbytes | `==0.43.1` | Quantization for local model loading (requirements.txt:2-6) |
| evaluate | `==0.4.3` | Metric helpers for final scoring (requirements.txt:2-6) |
| huggingface-hub | `==0.23.5` | Hub access for dataset and checkpoints (requirements.txt:2-6) |
| librosa | `==0.10.2.post1` | Audio feature handling (requirements.txt:29-32) |
| openai-whisper | `==20231117` | Speech-recognition component (requirements.txt:29-32) |
| whisperspeech | `==0.8` | Speech synthesis/tokenizer component (requirements.txt:29-32) |
| snac | `==1.2.0` | Neural audio codec (requirements.txt:29-32) |
| qa_metrics | `==0.2.17` | QA scoring metrics (requirements.txt:16-17) |
| sacrebleu | `==2.4.3` | BLEU scoring for reference-based sets (requirements.txt:16-17) |
| absl-py | unpinned | Utility library (requirements.txt:1) |
| immutabledict | unpinned | Immutable mapping utility (requirements.txt:7-8) |
| langdetect | unpinned | Language detection helper (requirements.txt:7-8) |
| nltk | unpinned | Text metric tokenizer (requirements.txt:10) |
| webdataset | unpinned | Large-scale dataset loading (requirements.txt:33-34) |
| vector_quantize_pytorch | unpinned | Vector quantization ops (requirements.txt:33-34) |

Python itself is pinned to `3.10` via conda (README.md:37-44).

## 8. CLI / Usage Surface

Entry points: `main.py` (generate), `api_judge.py` (judge), `evaluate.py` (score). No packaged console scripts or config files are described in the wiki pages.

| Command | Purpose |
|---|---|
| `python main.py --model naive --data alpacaeval --split test --modality audio` | Generate assistant responses to JSONL (README.md:87-99, main.py:11-48) |
| `python api_judge.py --src_file naive-alpacaeval-test-audio.jsonl` | Add gpt-4o-mini scores; writes `result-` prefixed file (README.md:101-108, api_judge.py:68-85) |
| `python evaluate.py --src_file result-naive-alpacaeval-test-audio.jsonl --evaluator open` | Compute and log final score (README.md:111-122, evaluate.py:9-18) |

`main.py` flags (main.py:11-14):

| Flag | Default | Meaning |
|---|---|---|
| `--model` | `qwen2` | Keys of `model_cls_mapping` (e.g. `naive`, `qwen2`, `diva`) |
| `--data` | `alpacaeval` | VoiceBench subset passed to `load_dataset` |
| `--split` | `test` | Dataset split; region code for `sd-qa` |
| `--modality` | `audio` | `audio` \| `text` \| `ttft` |

`api_judge.py` / `evaluate.py` flags (api_judge.py:68-85, evaluate.py:9-10):

| Flag | Required | Meaning |
|---|---|---|
| `--src_file` (judge) | yes | Input `.jsonl`, one JSON object per line |
| `--src_file` (evaluate) | yes | Judged or raw `.jsonl` |
| `--evaluator` | yes | One of `open`, `qa`, `ifeval`, `harm`, `mcq`, `bbh` |

Env-var and config tables:

| Variable / file | Status in wiki | Effect |
|---|---|---|
| `OPENAI_API_KEY` (implied) | Not named; `OpenAI()` takes no args (api_judge.py:9) | Authenticates gpt-4o-mini judge calls |
| `.env` | Ignored by `.gitignore` (`.gitignore:132-140`) | Conventional local credential store |
| Config files | None documented | All configuration is CLI flags plus hardcoded judge parameters |

## 9. Extensibility Points

- New voice assistant: add a class to the module behind `model_cls_mapping` and register its key in the mapping imported by `main.py` (main.py:3, main.py:26); it must implement `generate_text`, `generate_audio`, and `generate_ttft` to cover all `--modality` paths (main.py:35-39).
- New task family scoring: add an evaluator class to the module behind `evaluator_mapping` and register its key; `evaluate.py` picks it up automatically via `choices=list(evaluator_mapping.keys())` (evaluate.py:9-18).
- New dataset subset: publish it under `hlt-lab/voicebench` and pass its name as `--data`; no `main.py` change is needed because the name flows straight into `load_dataset` (main.py:24), though `sd-qa`-style splits and the README evaluator map need matching entries (README.md:91-122).
- Judge behavior: edit `meta_prompt_open` / `meta_prompt_qa` templates or the `generate_text_chat` parameters (`model`, `n`, `temperature`, `top_p`, `max_tokens`) in `api_judge.py` (api_judge.py:11-42, api_judge.py:62-74), and the `Pool(4)` width for throughput (api_judge.py:81-85).

## 10. Limitations and Gotchas

- **Judge coverage is gated to 4 of 11 subsets.** Only `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa` go through `gpt-4o-mini`; every other subset skips `api_judge.py` entirely (README.md:101-108). Running the judge on an `ifeval` or `mcq` file applies the wrong rubric.
- **`evaluate.py` writes no file.** The final score is only emitted via `logger.info` (evaluate.py:17-18), so results are lost unless stdout is captured; there is no `--out` flag.
- **Audio is dropped from output records.** `main.py` strips the `audio` column before writing JSONL (main.py:32-33), so downstream debugging cannot replay the exact waveform that produced a response.
- **Judge cost and latency are hardcoded.** Every judged record costs 3 `gpt-4o-mini` completions at 1024 max tokens (`n=3`, `temperature=0.5`, `top_p=0.95`) over a fixed `Pool(4)` (api_judge.py:62-85); large subsets such as the 1000-sample `wildvoice` therefore incur predictable but non-trivial API spend with no batching or retry flags.
- **`sd-qa` breaks the `--split test` convention.** Its split is a region code (e.g. `aus`, `usa`), not `test` (README.md:91-97); copying the Step 1 example verbatim fails for that subset.
- **Coverage ceiling in the analyzed snapshot.** The Awesome Voice Assistants table is cut off mid-row at the `Audio Flamingo 3` entry (README.md:149 per 01-overview.md:90), and `src/` internals behind `model_cls_mapping`, `generate_text_chat`, and `evaluator_mapping` are referenced but not detailed in the two wiki pages, so extension work requires reading source directly.

## 11. How It Compares to Alternatives

- **AudioBench (topical voice-assistant benchmark):** task-overlapping open-ended speech QA evaluation; VoiceBench differs by bundling 11 subsets across QA, instruction-following, reasoning (`bbh`), and safety (`advbench`) with an explicit audio-vs-text modality switch in one harness.
- **AIR-Bench (audio instruction benchmark):** broad audio-instruction coverage including speech and sound; VoiceBench is narrower (spoken instructions over a fixed Hugging Face dataset) but adds the generate-judge-score split with per-family evaluators (`open`/`qa`/`ifeval`/`harm`/`mcq`/`bbh`).
- **SUPERB (speech representation benchmark):** frozen-encoder, multi-task speech understanding suite; VoiceBench instead evaluates end-to-end LLM-based assistants by response quality rather than encoder representations.
- **OpenAI / open-source model evaluation harnesses (e.g. generic LLM eval scaffolds):** text-prompt oriented with pluggable tasks; VoiceBench's differentiator is first-class audio input (16 kHz cast, `generate_audio`/`generate_ttft` paths) plus human-recorded accent variation (`wildvoice`, `commoneval`, `sd-qa`, `bbh`).

Positioning: VoiceBench is the modality-comparison harness — same tasks in `audio` and `text` through one pipeline — rather than a pure speech-understanding suite or a generic text eval framework.

## Appendix: Selected Code Snippets

1. Response-generation dispatch, `main.py:29-40`:

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

2. GPT-judge scoring call, `api_judge.py:50-76`:

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

3. Final-scoring dispatch, `evaluate.py:9-18`:

```python
parser.add_argument('--src_file', type=str, required=True)
parser.add_argument('--evaluator', type=str, required=True, choices=list(evaluator_mapping.keys()))
```

```python
evaluator = evaluator_mapping[args.evaluator]()
logger.info(evaluator.evaluate(data))
```

4. Dataset load and output naming, `main.py:24-26` and `main.py:48`:

```python
data = load_dataset('hlt-lab/voicebench', args.data, split=args.split)
data = data.cast_column("audio", Audio(sampling_rate=16_000))
model = model_cls_mapping[args.model]()
```

```python
output_file = f'{args.model}-{args.data}-{args.split}-{args.modality}.jsonl'
```
