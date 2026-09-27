# Open-source LLM eval tooling landscape (as of 2026-09-03)

Research target: a hands-on tutorial that runs entirely **locally on Apple Silicon**, Python 3.12 + `uv`,
models served by **Ollama** — native API `http://127.0.0.1:11435`, OpenAI-compatible API
`http://127.0.0.1:11435/v1`, chat model `qwen3.8:27b`, embeddings `nomic-embed-text`. No paid API keys.

All numbers (stars, versions, dates) are approximate — pulled from web search in Sept 2026, not a live
GitHub API pull. Re-verify exact figures before publishing.

---

## 1. Comparison table — eval frameworks / harnesses

| Tool | Category | License | Stars (approx) | Last release (2026) | Local Ollama support | Verdict |
|---|---|---|---|---|---|---|
| **Inspect AI** | Framework/harness (also agent evals) | MIT | ~9k+ | actively released, May-2026 contribution-process change | Native `ollama` provider (via OpenAI-compatible layer); `pip install openai` needed | **Chapter** — best general-purpose local harness |
| **lm-evaluation-harness** (EleutherAI) | Academic benchmark harness | MIT | ~9k+ (v0.4.7 current) | v0.4.7 | `local-chat-completions` / `local-completions` model types hit any OpenAI-compatible server incl. Ollama | **Chapter** — canonical way to run GSM8K/MMLU-style benchmarks locally |
| **openai/evals** | Framework + benchmark registry | MIT | ~19k | still pushed (last push Apr-2026), not archived | Supports any OpenAI-compatible `base_url`, so Ollama works informally; not first-class | Comparison-table only — governance is OpenAI-benchmark-centric, weaker local-model ergonomics than the others |
| **promptfoo** | Prompt/LLM testing & red-teaming CLI | MIT core (+ paid enterprise) | ~22k | active; acquired by OpenAI (Mar-2026), still OSS | First-class `ollama:chat:<model>` / `ollama:embedding:<model>` provider, YAML config | **Chapter** — best "no-code YAML" option, great for CI-style regression testing |
| **DeepEval** | Pytest-style LLM unit-testing framework | Apache-2.0 | ~18k | active | `deepeval set-ollama <model>` CLI sets Ollama as default judge; also has `OllamaModel` class in Python | **Chapter** — best pytest-native DX; ships many ready metrics (faithfulness, answer relevancy, etc.) |
| **RAGAS** (now under vibrantlabsai org) | RAG-specific eval metrics | Apache-2.0 | large (10k+) | active (org rename `explodinggradients` → `vibrantlabsai` in 2026) | `LangchainLLMWrapper(ChatOllama(...))` + `LangchainEmbeddingsWrapper(OllamaEmbeddings(...))`; known rough edges with local LLMs (executor exceptions, NaNs) documented in GitHub issues | **Chapter** — the standard RAG-metric library despite local-model flakiness; worth showing workarounds |
| **Phoenix / arize-phoenix** | Observability + evals (tracing, datasets, experiments) | Elastic License 2.0 (ELv2, not OSI) | ~10k+ | active | Vendor-agnostic instrumentation; evals call any LLM via LiteLLM/OpenAI-compatible client, so point at `http://127.0.0.1:11435/v1` | Comparison-table (or optional chapter) — great UI but ELv2 license is source-available, not permissive OSS; mention the license caveat |
| **LangSmith** | Commercial eval/observability platform | SDK: MIT; platform: closed source | n/a (SDK) | active | SDK works against any model client (incl. local via custom wrapper) for eval runs; full platform requires LangSmith Cloud or Enterprise self-host (paid) | Comparison-table only — not free/self-hostable at OSS tier, out of scope for a no-paid-API tutorial |
| **Braintrust autoevals** | Scoring/eval library (LLM-as-judge, heuristics) | MIT (library); Braintrust platform is commercial | ~1-2k for autoevals repo | active | Reads `OPENAI_BASE_URL` / accepts custom OpenAI client → point at Ollama's `/v1`; needs `init(client=...)` override in newer versions | Comparison-table — library itself is usable standalone without the paid platform, worth a snippet, not a full chapter |
| **Opik** (Comet) | Observability + automated evals, self-hostable | Apache-2.0 | ~12-20k (fast-growing) | active | Documented Ollama integration; self-host via `docker compose` fully free | **Chapter candidate** — strong self-host story, Apache-2.0, growing fast; if only 5 chapters chosen, demote to table |
| **Langfuse** | LLM engineering platform: tracing, datasets, LLM-as-judge evaluators | MIT (self-host) | ~10k+ | active; v4 cutover Nov-2026 changes trace-level evaluators | `docker-compose.yml` ships an `ollama` service; judge evaluators configurable against Ollama's OpenAI-compatible endpoint | **Chapter** — best "production observability + eval datasets" story, fully MIT self-host |
| **MLflow `mlflow.genai`** | Eval/tracking framework, `evaluate()` API, scorers | Apache-2.0 | huge (mlflow overall ~19k) | active `genai` module in 2026 | Model spec `ollama:/<model-name>`; or wrap the OpenAI-compatible endpoint and use `mlflow.openai.autolog()`; custom judge model overridable in `Guidelines` scorer (some inconsistency reported in GitHub issue #22674) | Comparison-table — powerful but heavier dependency footprint for a from-scratch tutorial; mention as "if you already use MLflow" |
| **Weave** (W&B) | Tracing + evaluation harness | Apache-2.0 (weave lib) | mid-size, growing | active | Works with any local LLM call wrapped in a `@weave.op`; Ollama usable via OpenAI client pointed at local URL | Comparison-table — solid but W&B account nudge for full UI; secondary mention |
| **lighteval** (Hugging Face) | Academic benchmark harness, multi-backend | MIT | ~1-2k, growing | active in 2026 (litellm backend added) | No native Ollama backend, but `use-litellm-as-backend` — LiteLLM talks to any OpenAI-compatible endpoint, so Ollama works via LiteLLM passthrough | Comparison-table — good alternative to lm-eval-harness, redundant for a single chapter given EleutherAI's harness already covers this need |
| **OpenCompass** | Chinese-led broad model+dataset eval platform | Apache-2.0 | ~7-8k | active (Jul/Aug-2026 added OpenAI Responses API + LiteLLM gateway support, VLMEvalKit integration) | Generic `openai_api.py` model wrapper — point `openai_api_base` at Ollama's `/v1`; heavier install (100+ dataset deps) | Comparison-table — powerful but heavyweight/complex setup for a lean local tutorial |
| **HELM** (`crfm-helm`, Stanford) | Holistic multi-metric benchmark suite | Apache-2.0 | mid-size | active, v0.5.16 (Apr-2026) | Supports custom/local model clients through its model registry; less turnkey for Ollama specifically (more academic-benchmark oriented) | Comparison-table only — heavy, research-oriented, not a good "getting started" chapter |
| **evalica** | Ranking/statistics library (Elo, Bradley-Terry, win-rate, reliability) | Apache-2.0/MIT (check repo) | small (~40-ish reported, likely more by 2026) | maintained, Rust-core + Python bindings | Not a model-calling tool — pure stats library, no "local LLM" concept needed | Use in **statistics section**, not a standalone chapter — pairs with the judge-model chapter for producing leaderboards |

---

## 2. Hallucination / faithfulness detectors (local CPU/small-GPU)

| Tool | License | Size / hardware | What it does | Local integration |
|---|---|---|---|---|
| **Vectara HHEM-2.1-Open** | Open weights (community license on HF) | 110M params, <600MB RAM, ~1.5s per 2k-token input on CPU | Cross-encoder style classifier: scores how consistent a summary/answer is with a given source/context (RAG faithfulness) | `pip install transformers`, load `vectara/hallucination_evaluation_model` from Hugging Face, run `model.predict([(context, answer)])` locally on CPU — no server needed |
| **LettuceDetect** (KRLabsOrg) | MIT | ModernBERT-based, small variants down to 17M/32M/68M ("TinyLettuce"), GPU optional (30-60 examples/sec on GPU, CPU-capable for small variants) | Token-level span classification of hallucinated claims in RAG answers, outperforms sentence-level detectors (F1 79.22% on RAGTruth) | `pip install lettucedetect`; load pretrained `KRLabsOrg/lettucedect-*` checkpoints from HF, runs standalone, no LLM call required |
| **SelfCheckGPT** | MIT (research repo, `potsawee/selfcheckgpt`) | NLI variant uses DeBERTa-v3-large (~400M) | Zero-resource, black-box hallucination detection via self-consistency across multiple sampled generations (BERTScore / QA / n-gram / NLI / LLM-prompt variants) | Sample N completions from your local Ollama model at temperature>0, feed them + the target answer into `selfcheckgpt.SelfCheckNLI` (or `SelfCheckLLMPrompt` using your Ollama model as its own critic) — no external API |
| **MiniCheck / Bespoke-MiniCheck** | Open weights (Bespoke Labs), research paper (EMNLP 2024) | Small (~500M–7B class) fact-checking-as-classification model, deliberately optimized for CPU/low-GPU efficiency and outperforms GPT-4 on some fact-checking benchmarks at a fraction of the cost | Fine-grained claim-vs-document consistency check | Available via `pip install minicheck` or as HF checkpoint; runs standalone as classifier, doesn't need an LLM API |
| **General NLI checkers** (e.g. `roberta-large-mnli`, `cross-encoder/nli-deberta-v3-*`) | MIT/Apache (model dependent) | 300M-400M | Generic entailment/contradiction scoring, usable as premise=retrieved context, hypothesis=generated claim | `sentence-transformers` `CrossEncoder` — fully local, CPU-friendly, no LLM needed |

Recommendation: HHEM-2.1-Open and LettuceDetect are the two to demo in a tutorial chapter (both MIT/open-weight,
CPU-friendly, actively maintained, trivial `transformers`/pip install). SelfCheckGPT is good to *mention* because
it uses the local Ollama model itself as its own checker (no extra model download), which is pedagogically nice
for a "zero extra dependencies" example, but it's slower (multiple samples).

---

## 3. Judge-model options that run locally

| Model | Params | RewardBench-class ranking | Fits RTX 4090 24GB? | Ollama availability | Notes |
|---|---|---|---|---|---|
| **Prometheus 2** (prometheus-eval) | 7B and 8x7B variants | 7B ~85.5 overall on RewardBench; on par with Mixtral-8x7B | 7B: yes, easily (needs ~16GB VRAM per HF card); 8x7B: tight/no at 24GB without heavy quantization | Not an official Ollama model, but GGUF community conversions exist; supported natively via vLLM or LiteLLM | Repo `prometheus-eval/prometheus-eval` ships wrapper classes for absolute/relative grading rubrics |
| **Flow-Judge** (FlowAI, 3.8B) | 3.8B | Competitive with larger judges on RewardBench-style tasks | Yes, trivially | Runs fine as a small local model; check Ollama library/GGUF availability at publish time | Very cheap to run, good "judge on a laptop" story |
| **Selene-Mini** (Atla, 8B, Llama-3.1-8B post-trained) | 8B | Outperforms GPT-4o-mini and other SLMJs (SFR-Judge, Glider, Flow-Judge, Prometheus 2) on 11 benchmarks including RewardBench, EvalBiasBench, AutoJ | Yes, comfortably | **Yes — official Ollama model**: `ollama pull atla/selene-mini` (also `q4_k_m`, `q8_0` quant tags) | Best "just works with Ollama" judge model for this tutorial; GitHub `atla-ai/selene-mini` |
| **Skywork-Reward** (Skywork, various sizes incl. Llama-3.1-8B-based) | 8B/27B variants | Historically near top of RewardBench leaderboard | 8B: yes; 27B variants: fits comfortably at Q4-Q5 quantization | Not natively an Ollama model by default, but GGUF conversions circulate; runs cleanly on vLLM | Primarily a reward-model (scalar score) rather than a rubric/critique judge — good for RLHF-style ranking, less good for natural-language critique |
| **Glider** (Patronus AI, 3.8B) | 3.8B | Competitive with larger judges in comparisons cited in Selene-Mini paper | Yes, trivially | Available via Hugging Face; check for GGUF/Ollama port | Small, fast, permissively licensed judge — good secondary option to Selene-Mini |

**Can the tutorial's own `qwen3.8:27b` act as judge?** Yes for most rubric-style, single-answer grading and
pairwise comparisons — general-purpose 20B+ instruction-tuned models are commonly used as "LLM-as-judge" in
practice and this size class is squarely in the range research treats as "good enough" for many tasks, though it
will show known judge biases (position, verbosity, self-preference) more than a purpose-trained judge like
Selene-Mini. Recommendation: teach both — `qwen3.8:27b` as the "judge you already have" and `atla/selene-mini`
(via `ollama pull atla/selene-mini`) as the "purpose-built judge" comparison, since Selene-Mini is the only judge
model in this list with first-class Ollama distribution.

---

## 4. Statistics helpers

| Library | License | Purpose | Notes |
|---|---|---|---|
| **`krippendorff`** (PyPI) | permissive (BSD/MIT-class) | Fast Krippendorff's alpha for inter-rater reliability across N raters/missing data | `pip install krippendorff`; also an older `grrrr/krippendorff-alpha` reference implementation on GitHub |
| **`sklearn.metrics.cohen_kappa_score`** | BSD-3 | Cohen's kappa for 2-rater agreement | Already in `scikit-learn`, zero extra install |
| **`irrCAC`** | permissive | Broader chance-corrected agreement coefficients: Cohen's kappa, Conger's kappa, Fleiss' kappa, Krippendorff's alpha in one package | Alternative to `krippendorff` + manual Fleiss implementation |
| **`choix`** | MIT | Bradley-Terry and related pairwise-comparison / choice models, MLE fitting | Good for turning pairwise judge preferences into a ranked scale |
| **`evalica`** | Apache-2.0/MIT | Fast Rust-backed Elo, Bradley-Terry, average win-rate, plus reliability/uncertainty estimation, pandas/numpy native | Purpose-built for exactly this tutorial's "leaderboard from pairwise judgments" use case; from the Evalica paper ("Reliable, Reproducible, and Really Fast Leaderboards") |
| Bootstrap CI | n/a (do it yourself with `numpy`/`scipy`) | Standard nonparametric bootstrap for eval-metric confidence intervals | No dedicated widely-adopted package is needed — a 10-line `numpy` resampling function is standard practice in eval literature (see Miller et al., "error bars for evals", already in this project's `research/` folder) |

Recommendation for tutorial: use `krippendorff` (or `sklearn` for the 2-rater case) for annotator agreement, and
`evalica` for turning judge pairwise comparisons into an Elo/Bradley-Terry leaderboard — it's actively maintained,
fast, and directly answers "how do I rank multiple models/prompts from pairwise judgments."

---

## 5. Agent eval tooling (local, OpenAI-compatible)

| Tool | What it evaluates | Local/OpenAI-compatible model support |
|---|---|---|
| **Inspect AI** | General agent evals + benchmark tasks (tool use, multi-turn) | Native local model providers, incl. Ollama; can define custom `Solver`/`Scorer` for agent loops |
| **τ-bench / τ²-bench** (`sierra-research/tau2-bench`) | Tool-agent-user interaction in realistic domains (retail, airline, telecom) | Designed to be model-agnostic; needs a wrapper around any OpenAI-compatible client — plug in Ollama's `/v1` base URL for both the agent and the simulated user model |
| **SWE-bench (Lite/Verified) + mini-swe-agent** | Repo-level bug-fixing: agent gets a GitHub issue + repo snapshot, must produce a patch passing hidden tests | `mini-swe-agent` is a minimal scaffold that works with any OpenAI-compatible chat endpoint; runs each task in a Docker sandbox with no internet — practical to run a handful of SWE-bench Lite instances locally against `qwen3.8:27b`, though a 27B model will likely solve very few Verified-tier tasks (they're calibrated against frontier models) |
| **Terminal-Bench** | Realistic command-line agent tasks | Harness-agnostic scaffold; point the agent's model client at Ollama's OpenAI-compatible endpoint |

Practical note: agent benchmarks (SWE-bench Verified, τ-bench) are calibrated against frontier closed models;
a locally-served 27B model is useful for *demonstrating the harness mechanics* (how tasks are scored, how the
sandbox works, how to read a trajectory) but expect near-zero-to-low pass rates on the harder tasks. Good framing
for the tutorial: "run 3-5 SWE-bench Lite instances end-to-end to see the pipeline, not to benchmark the model."

---

## 6. Verified connection snippets

### Inspect AI → Ollama
```bash
uv add inspect-ai openai
export OLLAMA_BASE_URL=http://127.0.0.1:11435/v1
inspect eval inspect_evals/gsm8k --model ollama/qwen3.8:27b --limit 20
```
(Inspect's Ollama provider is layered on the `openai` package; per docs at inspect.aisi.org.uk/providers.html,
set `--model ollama/<model>` and point `OLLAMA_BASE_URL` at the local server.)

### lm-evaluation-harness → Ollama
```bash
uv add lm-eval
lm_eval --model local-chat-completions \
  --tasks gsm8k \
  --model_args model=qwen3.8:27b,base_url=http://127.0.0.1:11435/v1/chat/completions,api_key=ollama,num_concurrent=1 \
  --apply_chat_template \
  --limit 20
```
Use `local-completions` (not chat) only for loglikelihood-based tasks (MMLU, HellaSwag defaults) if the served
model exposes raw completions with logprobs — Ollama's OpenAI-compatible endpoint does not reliably expose
logprobs, so prefer generative tasks (gsm8k, ifeval, bbh) with `local-chat-completions`.

### promptfoo → Ollama
```yaml
# promptfooconfig.yaml
providers:
  - id: ollama:chat:qwen3.8:27b
    config:
      apiBaseUrl: http://127.0.0.1:11435
      temperature: 0
```
```bash
uv add --dev promptfoo   # or: npm/brew install promptfoo (Node-based CLI)
promptfoo eval
```
Note: promptfoo's core CLI is a Node.js tool, not a Python package — `uv` can still manage a Python-side test
harness that shells out to it, but it is not `uv add`-able as a Python dependency. Flag this explicitly in the
tutorial if choosing promptfoo for a full chapter.

### DeepEval → Ollama
```bash
uv add deepeval
deepeval set-ollama qwen3.8:27b --base-url http://127.0.0.1:11435
```
```python
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
metric = FaithfulnessMetric()  # uses the Ollama model set above as judge
```

### RAGAS → Ollama
```bash
uv add ragas langchain-ollama
```
```python
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

judge_llm = LangchainLLMWrapper(ChatOllama(model="qwen3.8:27b", base_url="http://127.0.0.1:11435"))
judge_emb = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11435"))
# pass judge_llm / judge_emb into ragas.evaluate(..., llm=judge_llm, embeddings=judge_emb)
```
Known caveat: multiple GitHub issues (#1099, #1120, #1226, #1246) report `NaN` scores and executor exceptions
with local Ollama models on large-context prompts — reduce concurrency and context size in the tutorial to
mitigate.

### Langfuse → Ollama (self-hosted)
```bash
git clone https://github.com/langfuse/langfuse && cd langfuse
docker compose up -d   # ships services incl. an ollama service in community fork setups
```
```python
from langfuse.openai import openai  # drop-in wrapper for tracing
client = openai.OpenAI(base_url="http://127.0.0.1:11435/v1", api_key="ollama")
```
Configure an LLM-as-judge evaluator in the Langfuse UI pointing its "model" config at the same base URL.

### MLflow `mlflow.genai` → Ollama
```bash
uv add mlflow
```
```python
import mlflow
mlflow.openai.autolog()
results = mlflow.genai.evaluate(
    data=eval_df,
    predict_fn=my_app,
    scorers=[mlflow.genai.scorers.Guidelines(name="concise", guidelines="Be concise.", model="ollama:/qwen3.8:27b")],
)
```
(Format is `<provider>:/<model-name>`; some inconsistency with the `Guidelines` scorer + Ollama is tracked in
mlflow/mlflow#22674 — spot-check output.)

### Braintrust autoevals → Ollama
```bash
uv add autoevals openai
```
```python
import os
os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:11435/v1"
os.environ["OPENAI_API_KEY"] = "ollama"
from autoevals import Factuality
result = Factuality()(output="...", expected="...", input="...")
```

### Opik → Ollama
```bash
uv add opik
docker compose -f opik/deployment/docker-compose/docker-compose.yaml up -d  # self-host
```
```python
from opik.evaluation.metrics import Hallucination
# configure the metric's model client to hit http://127.0.0.1:11435/v1 (OpenAI-compatible model wrapper)
```

### Atla Selene-Mini judge model, direct via Ollama
```bash
ollama pull atla/selene-mini          # or atla/selene-mini:q4_k_m for a smaller quant
```
```python
import requests
resp = requests.post("http://127.0.0.1:11435/api/generate", json={
    "model": "atla/selene-mini",
    "prompt": build_selene_prompt(context, response, criteria),
    "stream": False,
})
```

### HHEM-2.1-Open, local CPU
```bash
uv add transformers torch
```
```python
from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained(
    "vectara/hallucination_evaluation_model", trust_remote_code=True
)
scores = model.predict([(source_text, generated_summary)])
```

### LettuceDetect, local
```bash
uv add lettucedetect
```
```python
from lettucedetect.models.inference import HallucinationDetector
detector = HallucinationDetector(method="transformer", model_path="KRLabsOrg/lettucedect-base-modernbert-en-v1")
spans = detector.predict(context=[retrieved_chunks], question=question, answer=answer, output_format="spans")
```

### evalica leaderboard from pairwise judgments
```bash
uv add evalica
```
```python
import evalica, pandas as pd
result = evalica.bradley_terry(pd.Series(model_a), pd.Series(model_b), pd.Series(winners))
print(result.scores.sort_values(ascending=False))
```

---

## 7. Recommended chapter tools (4-6, each `uv add`-able, runs against Ollama, actively maintained)

1. **lm-evaluation-harness** (EleutherAI, MIT) — the standard way to run a real academic benchmark
   (GSM8K, MMLU-style) against a local Ollama model via `local-chat-completions`. Pure `pip`/`uv` install,
   no external services, directly teaches the `--limit` workflow for cheap local runs.

2. **DeepEval** (Apache-2.0) — pytest-native "LLM unit testing" DX, first-class one-line Ollama setup
   (`deepeval set-ollama`), ships ready metrics (faithfulness, answer relevancy, hallucination) that double
   as the RAG-evaluation teaching vehicle. Easiest on-ramp for developers already writing `pytest`.

3. **RAGAS** (Apache-2.0) — the de facto standard for RAG-specific metrics (faithfulness, context precision/
   recall). Worth a full chapter specifically *because* its local-model rough edges (NaNs, executor errors)
   are worth teaching how to work around, and it's the library readers will meet in the wild.

4. **Inspect AI** (MIT, UK AISI) — the most complete framework: benchmark tasks, agent solvers/scorers, and
   native local model providers in one coherent API. Best choice to show a "real" eval pipeline
   (dataset → solver → scorer → log viewer) end to end locally.

5. **Langfuse** (MIT, self-hosted via Docker) — the only tool on this list that also covers production
   observability + eval **datasets** + LLM-as-judge evaluators in one self-hostable stack, ships an
   `ollama` service in its docker-compose. Good closing chapter: "from eval script to a persistent
   dataset + dashboard."

6. **evalica** + **Atla Selene-Mini** (statistics + judge-model pairing, Apache-2.0 / open weights) —
   not a chapter on its own merit as a framework, but essential to close the loop: use `qwen3.8:27b` and
   `atla/selene-mini` (native `ollama pull`) as two judges, collect pairwise preferences, and fit a
   Bradley-Terry/Elo leaderboard with `evalica`. This is the only judge model in the whole survey with
   first-class Ollama distribution, making it the natural "local LLM-as-judge" chapter anchor.

**Comparison-table-only (mention, don't build a chapter around):**
- **promptfoo** — excellent tool but Node.js-based CLI, breaks the "everything is `uv add`" constraint; still
  worth one paragraph + config snippet since many teams meet it first.
- **openai/evals** — still maintained but registry/governance is OpenAI-benchmark-centric; local-model support
  is incidental, not a first-class feature.
- **Phoenix/arize-phoenix** — great UI/tracing but Elastic License 2.0 (source-available, not OSI-approved);
  flag the license explicitly if mentioned.
- **LangSmith** — SDK is MIT but the useful platform pieces require paid/self-hosted Enterprise; out of scope.
- **Opik** — genuinely close to chapter-worthy (Apache-2.0, fast-growing, good Ollama docs); demoted here only
  to keep the chapter count at 5-6 — swap it in for RAGAS or Langfuse if the tutorial's audience is more
  observability-focused than benchmark-focused.
- **MLflow genai / Weave** — powerful but heavy dependency footprint (full MLflow/W&B stack) relative to the
  payoff for a from-scratch local tutorial; mention as "if your org already runs this platform."
- **lighteval, OpenCompass, HELM** — all solid academic-benchmark harnesses, functionally overlapping with
  lm-evaluation-harness for this tutorial's purposes; cover in the comparison table with a one-line
  differentiator (lighteval = HF-native + LiteLLM backend; OpenCompass = broadest dataset catalog but heaviest
  install; HELM = most "holistic"/many-metric but most research-oriented, least turnkey).
- **Braintrust autoevals** — nice small scoring library, usable standalone without the paid platform, but
  thin enough to be a snippet inside the "statistics/judge" chapter rather than its own chapter.
- **Hallucination detectors (HHEM-2.1-Open, LettuceDetect, SelfCheckGPT, MiniCheck)** — cover as a
  comparison table + short code snippets inside the RAGAS or DeepEval chapter (as "beyond LLM-judge" add-ons)
  rather than a standalone chapter, since each is a 5-line integration, not a full framework.
- **Agent eval harnesses (τ-bench, SWE-bench/mini-swe-agent, Terminal-Bench)** — worth a table + "how to point
  the scaffold at Ollama" note, but a full chapter is lower-value given a 27B local model will pass very few
  tasks; better suited to a short "agent evals" appendix than a core chapter.
