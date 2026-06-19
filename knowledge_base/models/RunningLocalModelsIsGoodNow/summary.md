# Running Local Models is Good Now

**Article:** [Running local models is good now (Vicki Boykis, 2026)](https://vickiboykis.com/2026/06/15/running-local-models-is-good-now/)

## Human Readable TL;DR

Running AI models on your own computer used to be like trying to watch a 4K movie on a 2005 laptop -- technically possible but frustratingly slow and low quality. That's changed. A software engineer tried using modern small AI models on her personal machine for everyday coding tasks -- cleaning up code, writing tests, proofreading -- and found they now work well enough that she rarely needs to reach for the expensive cloud-based alternatives. The key shift happened recently, driven by better model designs and smarter compression techniques.

## TL;DR

Vicki Boykis documents the maturation of local LLM inference in mid-2026, arguing that quantized open-weight models (particularly Gemma 4 and Qwen families) running via llama.cpp/LM Studio now achieve ~75% of frontier model accuracy for routine software engineering tasks. The inflection point was OpenAI OSS-20B, after which she could complete real coding workflows -- refactoring, type-hint linting, unit test generation, repo bootstrapping -- without API fallback. Remaining bottlenecks are inference speed and hardware-bound context length.

---

## Problem & Motivation

Until recently, running large language models locally produced results too slow and inaccurate to be useful for real work. Cloud APIs were the only practical option for anything beyond experimentation, introducing cost, latency, and privacy concerns. Boykis argues a threshold was crossed around late 2025/early 2026 where local models became good enough to replace cloud APIs for a meaningful slice of day-to-day software engineering tasks.

---

## Main Original Ideas

1. **The 75% threshold is the key milestone.** Local models don't need to match frontier models -- they need to be good enough to handle routine tasks without constant API fallback. Gemma 4 variants now sit at roughly 75% accuracy relative to frontier models, which is sufficient for non-production coding workflows.

2. **Agentic use is now the real test.** Single-turn chat accuracy is a weak signal. The meaningful bar is whether a local model can sustain multi-step agentic workflows (refactoring a notebook into a modular repo, generating test suites) without derailing. The author used the Pi agent harness with LM Studio as the backend.

3. **Security-first local inference via Docker isolation.** Rather than running agents with broad system access, Boykis recommends constraining agentic workflows inside Docker containers with permissions limited to bash only -- no Python execution, no web browsing. This makes local agentic AI safer for experimenting on real codebases.

4. **Observability as a local-only advantage.** Running inference locally lets you watch the token generation process live, inspect KV cache utilization, and introspect internal model behavior -- capabilities unavailable via cloud APIs. This is framed as a genuine investigative and learning advantage, not just a privacy benefit.

---

## Key Findings

| Task | Local Model Used | Assessment |
|------|-----------------|------------|
| Python notebook refactoring | Gemma 4 / LM Studio + Pi | Successful, no API fallback needed |
| Type hint linting | Qwen 2.5 Coder / Qwen 3 MOE | Successful |
| Blog post proofreading | Gemma 4 12b-qat | Successful |
| Unit test generation | GPT-OSS-20B | Successful; was the inflection point model |
| Two-tower recommender bootstrapping | Gemma 4 26b-a4b | Successful |

- Tasks that "used to be impossible for local models as recently as 6 months ago" now work reliably.
- KV cache can saturate full 64GB RAM on current consumer hardware.
- Prompt template mismatches (a common local inference pain point) are now patched quickly by the open-source ecosystem.

---

## Suggestions & Future Directions

1. Try local inference now -- the current capability level is worth experiencing firsthand even if production use isn't yet practical.
2. Use Docker container isolation for any agentic workflow to contain blast radius of model errors.
3. Prefer LM Studio over Ollama for agentic workflows (better integration surface).
4. Monitor inference speed improvements -- this remains the binding constraint for heavier workflows.
5. Context length is hardware-bound; plan hardware upgrades if long-context tasks are the goal.

---

## Authors & Institutions

Vicki Boykis (independent; staff ML engineer / writer at vickiboykis.com)
