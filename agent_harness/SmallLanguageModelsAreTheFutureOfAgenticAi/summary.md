# Small Language Models are the Future of Agentic AI

**Paper:** [Small Language Models are the Future of Agentic AI (Belcak et al., 2025)](https://arxiv.org/abs/2506.02153)

## Human Readable TL;DR

Think of agentic AI as a kitchen: today we use a celebrity chef (a giant general-purpose model) to chop onions, stir soup, and fry eggs -- tasks any line cook could do faster and cheaper. This paper argues the same principle for AI agents: most of what they do is narrow, repetitive, and specialized, so small purpose-built models (the line cooks) are a better fit than giant LLMs. The authors say we should build AI agents from a team of small models, bringing in the celebrity chef only for the rare moments when real creativity or broad conversation is needed.

## TL;DR

The authors position small language models (SLMs, loosely under ~10B parameters) as the principal substrate for agentic AI, arguing they are sufficiently powerful, inherently more operationally suitable, and substantially more economical than LLMs for the narrow, repetitive sub-tasks that dominate agent workflows. They defend this with capability evidence (modern SLMs matching or beating 30-70B LLMs on reasoning, tool-use, and instruction-following), economic analysis (10-30x cheaper inference), and a six-step LLM-to-SLM agent conversion algorithm. They advocate heterogeneous agentic systems that default to SLMs and invoke LLMs only for genuinely general conversational or open-ended reasoning needs.

---

## Problem & Motivation

Commercial agentic AI overwhelmingly routes every sub-task -- tool-call formatting, intent parsing, code stub generation, routine planning -- through a single large centralized LLM via API. This is misaligned with how agents actually operate:

- Agent sub-tasks are narrow, repetitive, and have tightly scoped output formats.
- Large general-purpose LLMs are trained for open-ended conversation, a capability mostly unused inside agents.
- The industry has already poured ~$57B into LLM inference infrastructure (2024) against ~$5.6B in agent market revenue, a structural over-provisioning.
- Inference costs, latency, and energy scale poorly when every tool call hits a frontier model.

The authors frame this as both a technical mismatch and an economic inefficiency, and argue the default deployment pattern should be inverted.

---

## Main Original Ideas

1. **SLM sufficiency thesis.** Modern SLMs (e.g., Phi-3, Nemotron-H, SmolLM2, DeepSeek-R1-Distill-Qwen-7B, Salesforce xLAM-2-8B) already match or exceed 30-70B LLMs on the specific capabilities agents need -- instruction following, tool/function calling, structured output, and code generation -- making "LLM-by-default" an unjustified architectural choice.
2. **SLM operational suitability.** Small models are strictly better on the axes that matter for agents: lower latency per step (critical for multi-step pipelines), local/edge deployability, easier fine-tuning to new tools or formats, and behavioral predictability on narrow outputs.
3. **SLM economic dominance.** Per-token inference of a ~7B SLM is roughly 10-30x cheaper than a 70-175B LLM, with parameter-efficient fine-tuning achievable on commodity GPUs in hours rather than clusters-days -- collapsing the unit economics of agent operation.
4. **Heterogeneous-by-default agent architecture.** Agents should be built from a fleet of specialized SLMs for the vast majority of sub-tasks, with a single shared LLM reserved as a fallback for genuinely open-ended conversation or novel reasoning -- not the reverse.
5. **LLM-to-SLM conversion algorithm.** A concrete six-step methodology (usage logging -> data curation -> task clustering -> SLM selection -> specialized fine-tuning -> iterative refinement) that lets teams migrate an existing LLM-centric agent to a heterogeneous SLM-first system without redesigning the agent from scratch.
6. **Rebuttal of the standard LLM-first defenses.** Point-by-point responses to the three typical objections (LLMs have better general understanding; centralized LLM inference is cheaper at scale; LLMs get all the industry attention) showing each is either empirically weaker than claimed or a self-fulfilling prophecy of current investment, not a technical necessity.

---

## Key Findings

- **Capability parity is here.** Representative SLMs already reach or exceed much larger models on agent-relevant benchmarks: Phi-3-small (7B) rivals 70B models on commonsense/code; Nemotron-H (2-9B) matches 30B dense models at a fraction of the FLOPs; xLAM-2-8B tops leading function-calling leaderboards, beating GPT-4o and Claude on tool use.
- **Cost gap is large and structural.** SLM inference is ~10-30x cheaper per token than frontier LLMs; fine-tuning needs hours on consumer GPUs instead of cluster-weeks; parameter-efficient methods (LoRA, DoRA) make per-task specialization cheap enough to be routine.
- **Agent workloads are narrow.** Empirical inspection of agent trajectories (MetaGPT, Open Operator, Cradle) shows the overwhelming majority of LLM calls produce short, structured, low-variance outputs -- exactly the regime where SLMs match LLMs most closely.
- **Latency compounds.** Because agents chain many model calls, SLM per-step latency gains multiply across a trajectory, improving end-to-end responsiveness beyond what single-call benchmarks suggest.
- **Migration is feasible today.** The conversion algorithm has been demonstrated on production-style agent codebases; existing LLM API logs contain enough signal to bootstrap specialized SLMs with modest labeling effort.

---

## Suggestions & Future Directions

1. **Default to SLMs; justify every LLM call.** Invert the design convention so that introducing an LLM into an agent pipeline requires a specific justification, not the reverse.
2. **Build SLM-native agent frameworks.** Current frameworks assume one large model behind the scenes; future tooling should be first-class for routing, caching, and orchestrating many small specialists.
3. **Invest in data infrastructure for migration.** The bottleneck is curated task-specific datasets extracted from existing LLM traffic -- tooling for logging, clustering, and labeling agent trajectories is the highest-leverage investment.
4. **Develop SLM-specific training recipes.** Post-training methods (reasoning distillation, tool-use SFT, output-format RL) tailored to SLMs rather than downscaled LLM recipes.
5. **Address the acknowledged limitations.** The authors flag (a) remaining gaps in complex multi-step reasoning, (b) the coordination overhead of many-model systems, (c) weaker broad-world knowledge, and (d) entrenched LLM-centric infrastructure as open problems for the community.
6. **Publish a living critique record.** The authors commit to publishing responses and rebuttals at their project site, inviting explicit disagreement as part of the paper's positional format.

---

## Authors & Institutions

Peter Belcak (NVIDIA), Greg Heinrich (NVIDIA), Shizhe Diao (NVIDIA), Yonggan Fu (NVIDIA / Georgia Institute of Technology), Xin Dong (NVIDIA), Saurav Muralidharan (NVIDIA), Yingyan Celine Lin (Georgia Institute of Technology), Pavlo Molchanov (NVIDIA).
