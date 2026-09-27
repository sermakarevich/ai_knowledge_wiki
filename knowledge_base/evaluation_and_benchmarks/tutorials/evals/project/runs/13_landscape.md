# LLM eval / observability tooling landscape — chapter 13

Source: `research/SOURCES_tools.md` (web research, 2026-09-03). Stars are approximate.
Rows are the 8 tools the spec asks for, in spec order. Verdicts are for a
**local-first, no-paid-API, OSS** tutorial on Apple Silicon + Ollama.

| Tool | Licence | Self-host? | Datasets / experiments | Online scoring (live traffic) | Judge library (LLM-as-judge) | Price model | One-line verdict |
|---|---|---|---|---|---|---|---|
| **promptfoo** | MIT core (+ paid enterprise tier) | Yes — single binary/Docker; the YAML config runs anywhere | Yes — `prompts x inputs` eval matrices; CI-style regression tests | No — batch/CI focused, no live-trace ingest | Yes — LLM-as-judge assertions against any OpenAI-compatible API (incl. Ollama) | Free OSS; enterprise add-ons paid | Best zero-code YAML for CI regression gates; OpenAI acquired Mar-2026 but the core stays MIT |
| **Opik** (Comet) | Apache-2.0 | Yes — full stack via `docker compose`, free | Yes — datasets, experiments, evaluators UI | Yes — OTel-based tracing of live runs into the same UI | Yes — built-in LLM-as-judge evaluators + custom Python evaluators | Free self-host; Comet managed is paid | Strongest Apache-2.0 all-in-one (tracing + datasets + judge evaluators) |
| **Phoenix / arize-phoenix** | ELv2 (Elastic 2.0 — source-available, **not** OSI-open) | Yes — single container / one-liner Python app | Yes — datasets, experiments, auto-evaluators | Yes — OpenTelemetry ingest of live traffic (its core design) | Yes — `Evaluators` (RAG triad etc.) via LiteLLM, any Ollama endpoint | Free self-host; Arize platform is paid | Great UI and tracing, but ELv2 is source-available, not permissive OSS |
| **LangSmith** | SDK: MIT; platform: closed source | No free tier — Cloud SaaS or paid Enterprise self-host | Yes — datasets & experiments are its flagship feature | Yes — that's its reason for existence (live trace → score at ingest) | Yes — LLM-as-judge evaluators in the platform | Paid per-trace seats; no free self-host | Capable but not free/self-hostable at OSS tier → out of scope for this tutorial |
| **Braintrust** (incl. `autoevals`) | Library: MIT; platform: commercial | No for the platform; `autoevals` library runs standalone | Platform only — datasets/experiments live in the cloud | Platform only (live event scoring in the cloud) | `autoevals` is a clean, MIT, standalone LLM-as-judge library (works with any OpenAI client → Ollama) | Free tier, then paid; library free | Treat the `autoevals` library as the useful OSS part; the rest is a paid platform |
| **MLflow** (`mlflow.genai`) | Apache-2.0 | Yes — `mlflow server` / full cluster; heavy footprint | Experiments/tracking yes; "eval sets" go via `mlflow.genai.evaluate()` + scorers, not a first-class dataset product | Limited — logs live metrics, no live-eval pipeline built in | Yes — `Guidelines`/judge scorers; custom judge model overridable (rough edges in issue #22674) | Free OSS; Databricks MLOps paid | Powerful but a big dependency footprint; "if you already run MLflow" |
| **Weave** (Weights & Biases) | Apache-2.0 (library) | Partial — library is OSS; full UI wants a W&B account | Basic — eval datasets in the platform | Yes — `@weave.op` instrumented live calls, scores at call time | Yes — scoring functions incl. LLM-as-judge via any client incl. Ollama | Free W&B tier with limits; W&B core paid | Solid OSS library; full observability story nudges toward a paid W&B account |
| **Langfuse** | MIT (self-hosted) | **Yes — the whole stack is MIT and ships `docker compose` with an `ollama` service** | **Yes — first-class datasets, dataset items, and `runExperiment`** | **Yes — live trace ingestion with score attachments, dashboards, filters** | Yes — LLM-as-judge evaluator templates configurable against any OpenAI-compatible endpoint (incl. Ollama `/v1`) | Free self-host; Langfuse Cloud paid (optional) | The best "production observability + eval datasets + online scoring" story at fully MIT — **the tool this chapter builds on** |

### How the 8 line up with chapter 13's five production needs

| Need (from the spec) | promptfoo | Opik | **Phoenix** | **LangSmith** | **Braintrust** | **MLflow** | **Weave** | **Langfuse** |
|---|---|---|---|---|---|---|---|---|
| 1. Trace every (replayed) request | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓ (used)** |
| 2. Eval set stored as a dataset | inputs file | ✓ | ✓ | ✓ | platform | via evals | — | **✓ (used)** |
| 3. Prompt version = experiment + scores | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓ (used)** |
| 4. **CI gate (reproducible, offline, no server)** | **✓ (best-in-class)** | — | — | — | — | — | — | **✓ (we roll our own over committed predictions)** |
| 5. **Online monitor on a live sample** | — | ✓ | ✓ | ✓ | ✓ | — | ✓ | **✓ (we roll our own over committed traces)** |

Reading: **Langfuse** is the only MIT, fully self-hostable, all-five-needs tool; **promptfoo**
is the canonical way to do need #4 in CI with zero Python and any Ollama model;
**Opik/Phoenix** cover needs 1–3 and 5 with a bigger footprint; **LangSmith / Braintrust /
Weave** all gate the useful parts behind a paid platform; **MLflow** covers the tracking side
but not the dataset/experiment/online-scoring product loop.
