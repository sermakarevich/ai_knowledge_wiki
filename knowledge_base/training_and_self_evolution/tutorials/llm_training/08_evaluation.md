# 08 — Evaluation: lm-evaluation-harness, CyberMetric, LLM-as-judge, `metrics.json`

Previous: [07_export_to_ollama.md](07_export_to_ollama.md) · Next: 09 (coming next)

## What you will learn

- Why evaluation is built **before** fine-tuning, not after: chapters 09–10 need a fixed measuring
  instrument to answer "how good is it on the topic?" and "how much general ability did it lose?"
- **Loglikelihood vs generative tasks** — how `lm_eval` actually scores MMLU (comparing the summed
  log-probability of 4 answer continuations, never asking the model to "generate a letter") versus
  GSM8K/IFEval, which score real generated text
- Running EleutherAI's **`lm-evaluation-harness`** (`lm_eval` 0.4.12) against a saved HF checkpoint,
  and against an **Ollama** model through its OpenAI-compatible endpoint — and why only half the
  suite is possible over Ollama (no logprobs endpoint)
- The **CyberMetric** domain harness: a real item, the exact prompt, letter parsing, a more robust
  "loglik" scoring mode, and de-duplicating a training split against the eval split
- **Bootstrap confidence intervals** for accuracy — why a 1-2 point difference on 500 questions is
  routinely noise, not a real improvement
- **LLM-as-judge** for open-ended answers: a JSON-schema-constrained prompt, and the biases
  (position, verbosity, self-preference) this design does and does not solve
- The fixed **`metrics.json`** schema every run from here on writes, so chapters 09-10 can load and
  compare runs mechanically
- Real baseline numbers for `tiny-qwen35-110m-{base,sft,dpo}`, `Qwen/Qwen3.5-4B`, and `qwen3.8:27b`

Everything in this chapter needs GPU (`lm_eval --model hf`) or the Ollama endpoint on `rtx`. The CPU
test suite only exercises pure functions: `parse_letter`, `format_mcq`, `dedup_train`, `ci95`,
`parse_results_json`/`summarize`, `RunMetrics`, and the judge's prompt builder / JSON parser — no
subprocess, no network, no GPU.

---

## 1. Why evaluation comes before fine-tuning

Chapter 09 will LoRA-fine-tune `Qwen/Qwen3.5-4B` on a cybersecurity corpus, and chapter 10 will
apply a preference stage on top. Both chapters need to answer two very different questions after
each stage:

1. **Did it get better at the domain?** — a CyberMetric accuracy number.
2. **Did it get worse at everything else?** — a general-capability suite (MMLU, ARC, HellaSwag,
   WinoGrande, TruthfulQA, GSM8K, IFEval), run identically before and after.

If the harness, the prompts, the `--limit`, and the metrics schema are not fixed *before* any
fine-tuning happens, every "before vs after" comparison in chapters 09-10 is an apples-to-oranges
guess. This chapter builds and validates that instrument once, and measures it on models we already
have: our own 110M checkpoints (chapters 04-06) and the two models 09-10 actually touch
(`Qwen/Qwen3.5-4B`, and `qwen3.8:27b` as the judge).

## 2. Loglikelihood vs generative tasks

`lm_eval` tasks fall into two families, and understanding the difference is the single most
important thing in this chapter — it is *why* Ollama can only run half the suite (§4).

**Loglikelihood tasks** (`mmlu`, `arc_challenge`, `hellaswag`, `winogrande`, `truthfulqa_mc2`): the
model never generates anything. For each answer choice, `lm_eval` builds the string
`"<question><choice>"`, runs one forward pass, and reads off the model's own token
log-probabilities for exactly the `<choice>` tokens, summed. The choice with the highest summed
log-probability wins.

```
question: "The capital of France is"
choice A: " Paris"   -> forward pass on "...is Paris"   -> sum log P(tok) for " Paris" tokens = -0.31
choice B: " Berlin"  -> forward pass on "...is Berlin"  -> sum log P(tok) for " Berlin" tokens = -6.82
choice C: " Madrid"  -> forward pass on "...is Madrid"  -> sum log P(tok) for " Madrid" tokens = -7.44
choice D: " Rome"    -> forward pass on "...is Rome"    -> sum log P(tok) for " Rome" tokens   = -8.10
                                                        -> argmax = A ("Paris")  ✓
```

This is why loglikelihood scoring needs direct access to the model's logits — it requires
`transformers`, not a chat endpoint.

**Generative tasks** (`gsm8k`, `ifeval`): the model actually generates free text (a worked-out
answer, an instruction-following response), which is then checked by a separate rule (exact numeric
match on GSM8K's final answer; a programmatic instruction-following checker on IFEval). This needs
no logits, only text — any chat endpoint that can generate can run these.

## 3. The general suite: `eval_general.py`

`configs/eval_general.yaml` fixes the suite everyone in chapters 08-10 must use:

```yaml
tasks: [mmlu, arc_challenge, hellaswag, winogrande, truthfulqa_mc2, gsm8k, ifeval]
limit: {mmlu: 20, arc_challenge: 300, hellaswag: 300, winogrande: 300, truthfulqa_mc2: 200, gsm8k: 200, ifeval: 200}
num_fewshot: {mmlu: 5, gsm8k: 5, others: 0}
batch_size: auto:4
seed: 1234
```

`--limit` follows `lm_eval`'s own semantics: an integer N means "the first N examples of **each**
task". MMLU is special — `lm_eval` implements it as one task per subject (57 subjects), so
`limit: 20` means 20 questions **per subject**, ~1140 questions total, not 20 total. Every MMLU
number quoted in this chapter is therefore a ~1140-question estimate of the real ~14,000-question
benchmark, not the benchmark itself — say so every time it's quoted.

`run_hf(model_dir, out_dir)` shells out to the `lm_eval` CLI once per task (each task can have its
own `--num_fewshot`/`--limit`):

```
lm_eval --model hf \
  --model_args pretrained=<model_dir>,dtype=bfloat16,trust_remote_code=False \
  --tasks mmlu --num_fewshot 5 --limit 20 \
  --batch_size auto:4 --seed 1234 \
  --output_path runs/eval_baselines/<name>/mmlu --log_samples
```

The CLI (not `lm_eval`'s Python API) is used deliberately: it is the interface EleutherAI documents
and version-pins, it prints its own progress bars for a suite that can run 20-45 minutes, and it
writes one `results.json` per invocation that `_load_task_results`/`parse_results_json` only need to
glob and parse — `<out_dir>/<hashed-run-dir>/results_*.json`, `{"results": {task: {"metric,filter":
value, ...}}}`. `summarize()` picks each task's conventional primary metric (`acc,none` for MMLU,
`acc_norm,none` for ARC/HellaSwag, `exact_match,flexible-extract` for GSM8K, ...) and adds
`general_mean`, the mean across tasks — a single number chapters 09-10 can plot before/after.

For a LoRA adapter (chapter 09), add `peft=<adapter_dir>` to `--model_args` — `run_hf`'s `adapter`
argument does this.

## 4. Running against Ollama, and the logprobs limitation

`run_ollama(model_name, out_dir)` uses `lm_eval --model local-chat-completions`, which speaks
Ollama's OpenAI-compatible `/v1/chat/completions`, plus `--apply_chat_template`:

```
lm_eval --model local-chat-completions \
  --model_args model=qwen3.8:27b,base_url=http://127.0.0.1:11434/v1/chat/completions,num_concurrent=1,max_retries=3 \
  --tasks gsm8k --num_fewshot 5 --apply_chat_template \
  --output_path runs/eval_baselines/qwen3_8_27b/gsm8k --log_samples
```

**Only the generative tasks (`gsm8k`, `ifeval`) can run this way.** Ollama's OpenAI-compatible
`/v1/completions` does not return per-token `logprobs` for arbitrary continuations, and
`/v1/chat/completions` never returns them at all — so `lm_eval`'s `local-completions`/
`local-chat-completions` model types have no way to compute the summed log-probability §2 needs.
`run_ollama` detects this itself: any of `mmlu`/`arc_challenge`/`hellaswag`/`winogrande`/
`truthfulqa_mc2` requested against an Ollama model are **skipped with a warning**, not silently
dropped — "skipping loglikelihood tasks over Ollama (no logprobs endpoint) ... run these against
the HF checkpoint instead". This is also why a GGUF model can only be evaluated through Ollama in
this chapter's tooling, never directly with `lm_eval --model hf` (see Troubleshooting).

## 5. The CyberMetric domain harness

[CyberMetric](https://huggingface.co/datasets/tihanyin/CyberMetric) is a 4-option multiple-choice
cybersecurity quiz, published as three splits (`-500-`, `-2000-`, `-10000-v1.json`) at
`https://huggingface.co/datasets/tihanyin/CyberMetric/resolve/main/`. A real item
(`CyberMetric-500-v1.json`, index 0):

```json
{
  "question": "Which of the following is a desirable property of a biometric system?",
  "answers": {"A": "Permanent", "B": "Transferability", "C": "Uniformity", "D": "Forgiveness"},
  "solution": "A"
}
```

`format_mcq` renders it as:

```
Which of the following is a desirable property of a biometric system?

A) Permanent
B) Transferability
C) Uniformity
D) Forgiveness

Answer with the letter only.
```

`parse_letter` extracts the first standalone A-D from the reply — a bare `"B"`, `"Answer: C"`,
`"(D)"`, and `"The answer is A."` all parse correctly; an unparsable/refused reply returns `None`
and is scored wrong.

**Two scoring modes.** `mode="letter"` (default): greedy-generate up to 8 tokens, parse a letter.
Simple and matches how a chat model is actually used, but a model that never learned to answer
"just the letter" can score near 0 even if it "knows" the right answer — small/undertrained models
are especially prone to this. `mode="loglik"`: score `P(A)` vs `P(B)` vs `P(C)` vs `P(D)` directly
from the next-token logits after the prompt and take the argmax — the same idea as §2's MMLU
scoring, ~20 lines (`_score_loglik`), and far more robust for small models since it never depends
on the model *formatting* its answer.

**De-duplication.** CyberMetric-10000 was built independently of the -2000/-500 splits, so if it
were ever used as a training set (chapter 09's domain SFT data), some of its questions would leak
into the eval set. `dedup_train(train_items, eval_items)` normalises whitespace/case
(`unicodedata.normalize("NFKC")`, lowercase, collapse whitespace) and drops any train question whose
normalised text also appears in the eval set. Measured for real on `CyberMetric-10000-v1.json`
against `CyberMetric-2000-v1.json`: **10,180 → 8,187 items, 1,993 removed** — almost the entire
2000-question eval split is contained verbatim in the 10000-question split, confirming the
dedup step is not optional.

**Bootstrap confidence interval.** `ci95(correct)` resamples the list of 0/1 correctness values
with replacement 2000 times and reports the 2.5th/97.5th percentile of the resampled means. On
CyberMetric-500 (n=500), this interval is typically **±3-4 accuracy points wide** — so a 1-2 point
difference between two runs (e.g. base vs. SFT below) is routinely *inside* the interval, i.e. noise,
not a real improvement. Every accuracy number in this chapter is reported with its `ci95`.

## 6. LLM-as-judge

Multiple-choice accuracy can't score an open-ended answer. `judge(question, reference, candidate)`
sends one `POST /api/chat` to the local `qwen3.8:27b`, with `think: false`, `temperature: 0`, and
`format` set to a Pydantic JSON schema (`Verdict: {score: 1-5, verdict, reason}`) — the same
constrained-decoding pattern the `graph_rag` tutorial's `chat_json` uses. The system prompt fixes
the rubric (1 = wrong, 5 = fully correct) and instructs "`verdict` is `correct` if `score >= 4`".

`configs/judge_set.yaml` holds 20 open cybersecurity questions, built by taking 20 CyberMetric-500
items, dropping the 4 multiple-choice options, and using the correct option's text as the
reference answer — e.g. item `cm500-1`: *"What type of policies and procedures should an
organization develop to implement the HIPAA Security requirements?"* → reference *"Policies/
standards, procedures, tools/infrastructure, and operational activities."*

**Position-bias note.** This judge only ever sees **one** candidate answer at a time (question +
reference + candidate), never a pair of candidates to rank against each other — so classic
position bias (favouring whichever answer is shown first) is sidestepped entirely, at the cost of
not being able to directly compare two models' *phrasing* against each other, only their scores
against the same reference. Two biases this design does **not** solve: **verbosity bias** (a judge
model can reward longer answers regardless of correctness) and **self-preference bias** (a judge
can favour answers written in its own style). This chapter names them as open caveats, not solved
problems — nothing here corrects for them.

Judging `qwen3.8:27b`'s own answers with `qwen3.8:27b` as the judge would be circular (a model
grading itself), so the baselines table below skips the judge for that model entirely.

## 7. `metrics.json`: the fixed schema

Every run from chapter 08 onward writes (merges into) `runs/<run_name>/metrics.json`, validated by
the `RunMetrics` Pydantic model in `config.py`:

```python
class RunMetrics(BaseModel):
    run_name: str
    model: str
    base: str | None = None
    stage: str
    created_at: str                          # ISO-8601 UTC, auto-filled
    train: dict = {}
    general: dict[str, GeneralTaskResult]    # {task: {metric, value, stderr}}
    general_mean: float | None = None
    domain: DomainResult | None = None       # {dataset, split, n, accuracy, ci95, per_category}
    judge: JudgeResult | None = None         # {n, mean_score}
    cost: CostResult | None = None           # {wall_seconds, peak_gb}
```

Every section is optional on its own — a domain-only run does not need a `general` suite — but any
section that *is* present must match this shape, so chapters 09-10 can load and compare runs
mechanically (e.g. plot `general_mean` before/after a fine-tuning stage, or diff two `domain.accuracy`
values against their `ci95`). `write_metrics(run_dir, metrics)` merges new keys into an existing
`metrics.json` rather than overwriting it, since `eval_general`, `eval_domain` and `judge` are run
as separate commands against the same run directory.

## 8. Baselines

Real numbers, `configs/eval_general.yaml`'s small limits (§3), CyberMetric-500 (110M models) /
CyberMetric-2000 (`Qwen/Qwen3.5-4B`, `qwen3.8:27b`), measured on `rtx` (RTX 4090, 24 GB), 2026-08-30.

### General suite

| model | mmlu | arc_challenge | hellaswag | winogrande | truthfulqa_mc2 | gsm8k | ifeval | general_mean | wall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny-qwen35-110m-base | 25.3% | 25.3% | 37.0% | 52.3% | 46.1% | 0.5% | 9.0% | 27.9% | 4.7 min |
| tiny-qwen35-110m-sft | 25.7% | 24.0% | 36.7% | 51.7% | 46.8% | 2.0% | 16.0% | 29.0% | 3.9 min |
| tiny-qwen35-110m-dpo | 26.1% | 24.0% | 36.7% | 51.3% | 46.9% | 1.5% | 16.0% | 28.9% | 8.9 min |
| `Qwen/Qwen3.5-4B` | 71.5% | 52.3% | 66.0% | 70.0% | 48.4% | 73.0% | 23.5% | 57.8% | 93.0 min |
| `qwen3.8:27b` (Ollama, generative only) | skipped¹ | skipped¹ | skipped¹ | skipped¹ | skipped¹ | 42.5% | 69.5% | 56.0%² | 39.5 min |

¹ loglikelihood tasks need real logits (§4) — not runnable over Ollama's chat endpoint.

² `general_mean` for the Ollama row averages only the two generative tasks it actually ran
(gsm8k, ifeval) — it is not comparable to an HF row's seven-task mean.

MMLU here is ~1140 questions (57 subjects × 20, §3), not the full ~14,000-question benchmark. Note
the 110M models sit at or just above **chance on every multiple-choice task** (25% for 4-choice
MMLU/ARC, ~50% for 2-choice WinoGrande) — expected for a model this small, undertrained on ~1.5B
tokens against a Chinchilla target of ~2.2B (chapter 04-07): these baselines exist to give chapter
09-10 a floor, not to demonstrate general capability. GSM8K near-0% and IFEval 9-16% follow the same
story — arithmetic and precise instruction-following are exactly the abilities undertrained small
models lack most. SFT/DPO nudge IFEval and GSM8K up (formatting/instruction-following is one of the
easiest things post-training teaches) while the loglikelihood tasks stay within noise of each other
and of chance — post-training does not, and should not, move raw factual-recall accuracy much.

`Qwen/Qwen3.5-4B`'s 93.0-minute wall-clock **exceeds** this chapter's ≤45-minute target for a 4B
model on a shared RTX 4090 — mostly `mmlu` (1140 loglikelihood forward passes at a conservative
`batch_size auto:4`, chosen over the default `auto` to avoid the OOM-churn described in
Troubleshooting) plus `ifeval`'s slow greedy generation. To bring a re-run under 45 minutes, lower
`limit.mmlu` (e.g. 10 per subject) and `limit.ifeval` (e.g. 100) in a copy of
`configs/eval_general.yaml`, or run on a GPU that isn't shared with another live workload — both cut
wall-clock roughly linearly with the reduced sample counts.

### CyberMetric domain accuracy

| model | split | n | accuracy | 95% CI |
|---|---|---:|---:|---|
| tiny-qwen35-110m-base | 500 | 500 | 24.6% | [20.8%, 28.6%] |
| tiny-qwen35-110m-sft | 500 | 500 | 25.0% | [21.2%, 29.0%] |
| tiny-qwen35-110m-dpo | 500 | 500 | 25.0% | [21.2%, 29.0%] |
| `Qwen/Qwen3.5-4B` | 2000 | 2000 | 87.6% | [86.2%, 89.0%] |
| `qwen3.8:27b` (Ollama) | 2000 | 2000 | 92.2% | [91.05%, 93.35%] |

All three 110M numbers are inside each other's confidence intervals — exactly §5's point: on n=500,
a 0.4-point difference is pure noise, not evidence that SFT/DPO changed cybersecurity knowledge at
all (they shouldn't have — neither stage's training data touched this domain).

### LLM-as-judge (20-question `configs/judge_set.yaml`, judged by `qwen3.8:27b`)

| model | n | mean score (1-5) |
|---|---:|---:|
| `Qwen/Qwen3.5-4B` | 20 | 4.0 |
| `qwen3.8:27b` | — | skipped (self-judging is circular, §6) |

`just eval-baselines` reproduces every number in this chapter end-to-end.

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `lm_eval` errors with an unknown task name | task registry names don't always match a benchmark's common name (e.g. it's `truthfulqa_mc2`, not `truthfulqa`) | `lm_eval --tasks list` (or `lm_eval ls tasks` on 0.4.12) to see every registered name before writing a config |
| never point `--model hf` at a GGUF file | `transformers` tries to rebuild a tokenizer from GGUF metadata without an explicit `tokenizer=<hf id>` `--model_args` key, and can hang for hours doing it | GGUFs are evaluated only through Ollama in this chapter (`run_ollama`, §4) — never `run_hf` |
| `CUDA out of memory` mid-suite, especially with a large Ollama model already loaded | `batch_size: auto` probes upward from a large batch and repeatedly OOM-churns before settling, on top of whatever headroom the shared GPU actually has | `batch_size: auto:4` bounds the number of probing steps (`configs/eval_general.yaml`); for a known-tight headroom, set a small fixed integer batch size instead (`configs/eval_general_4b.yaml` uses `2`) |
| Ollama request to `local-chat-completions` times out | a 27B (or larger) model on a shared GPU can take much longer per request than `lm_eval`'s default timeout expects, especially under GPU contention from another job | `--model_args ...,max_retries=3` already retries; if it still fails, lower `num_concurrent` to 1 (already the default here) and re-run just the failing task with `--tasks <name>` |
| generated replies are extremely long, sometimes truncating before answering | a thinking-capable model emitting its chain-of-thought before the final answer | `enable_thinking=False` in `apply_chat_template` for HF (`chat.py`'s `render`), `"think": false` in the Ollama payload (both already set everywhere in this chapter's code) |
| `parse_letter` returns `None` for a reply that "looks" correct | the model answered with the option's *text* instead of its letter, or wrapped the letter in unexpected punctuation the regex doesn't cover | inspect the raw reply; consider `mode="loglik"` (§5) instead, which never depends on the model formatting a letter at all |
| Ollama eval connects, but every request fails or hangs even though `ollama list` shows the model | `base_url` pointed at a port/path that isn't Ollama's actual OpenAI-compatible endpoint on the host the script runs on — e.g. an SSH-tunnel-forwarded port from a *different* machine, or `/v1/completions` when the model type is `local-chat-completions` (which needs `/v1/chat/completions`) | always verify which host the eval process itself runs on and hit `curl <base_url>/chat/completions` from *that* host before trusting a "default" URL; this chapter's default is `http://127.0.0.1:11434/v1` (Ollama's standard local port) — a value copied from a differently-configured shell (e.g. one with an SSH port-forward) will silently point at the wrong thing |
| CyberMetric domain accuracy for a thinking-capable model comes back near or below chance (e.g. ~5-6% on 4 options, worse than random guessing) | `max_new_tokens=8` truncates mid chain-of-thought before the model ever emits its answer letter, if `enable_thinking`/`think` wasn't disabled | set `enable_thinking=False` in `apply_chat_template` (`chat.py`'s `render`) for HF, `"think": false` in the `/api/chat` payload for Ollama — both already the default in this chapter's code; a sub-chance domain accuracy is a strong signal to check this first before suspecting the model itself |

## Exercises

1. **Run the full (non-limited) MMLU** on `Qwen/Qwen3.5-4B` (`limit: null` in a copy of
   `configs/eval_general.yaml`) — how far does the ~1140-question estimate (§3) drift from the real
   ~14,000-question number, and how much longer does it take?
2. **Compare `mode="letter"` vs `mode="loglik"`** on `tiny-qwen35-110m-base` (§5) — does the
   undertrained 110M model's CyberMetric accuracy change meaningfully between the two scoring
   modes, confirming or refuting the claim that small models are penalised by letter-formatting
   requirements?
3. **Widen `configs/judge_set.yaml`** to 50 questions and re-run the judge on `Qwen/Qwen3.5-4B`'s
   answers — does `mean_score` move outside a bootstrap confidence interval computed the same way
   as `ci95` (§5), or is 20 questions already enough to see a stable signal?
4. **Deliberately verbose answer test**: hand the judge (§6) two candidates for the same question —
   one correct-and-short, one correct-but-padded with irrelevant detail — and see whether
   `qwen3.8:27b` scores them differently, to observe verbosity bias directly rather than take the
   chapter's word for it.

---

Previous: [07_export_to_ollama.md](07_export_to_ollama.md) · Next: 09 (coming next)

Numbers in this chapter: `project/runs/eval_baselines/**/metrics.json`, produced on `rtx` (RTX 4090,
24 GB) on 2026-08-30 with `lm_eval` 0.4.12, `transformers 5.16.1`, `torch 2.13.0+cu130`, Ollama
0.32.12.
