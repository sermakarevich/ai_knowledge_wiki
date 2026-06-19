# Build Agentic AI Workflows on Your Mac with MLX

**Video:** [Build Agentic AI Workflows on Your Mac with MLX (Angelos, Apple MLX Team, 2025)](https://youtu.be/wykPErJ8M-8)

## Human Readable TL;DR

Imagine your laptop could be your own private AI assistant that can browse files, run programs, and write code -- no internet required. This video shows how Apple's Mac computers can now run powerful AI "agents" (AIs that take actions, not just answer questions) entirely on-device using the M-series chips. The presenter walks through how to set it up in three simple steps and demonstrates the AI building a drawing app from scratch in under 2 minutes, all without a single cloud server being involved.

## TL;DR

Apple engineer Angelos presents the four-layer local agentic AI stack for Mac: MLX (Metal-accelerated array framework) → MLX-LM (model loading/quantization) → MLX-LM Server (OpenAI-compatible HTTP server with tool calling) → any agent framework. The talk covers three hardware optimizations that make this practical -- Neural Accelerators (4x matrix multiply speedup on M5), continuous batching for concurrent subagents, and distributed inference across multiple Macs via Thunderbolt RDMA -- and live-demos PR summarization, SwiftUI app generation, and Xcode bug-fixing, all fully on-device.

---

## Problem & Motivation

Cloud-based LLM APIs introduce latency, per-token cost, data privacy risks, and offline unavailability. As agentic workflows -- where models call tools repeatedly in a loop -- become common, these drawbacks are amplified: a single task may consume hundreds of thousands of tokens across many round trips. Apple silicon's unified memory architecture (up to 512 GB RAM, Metal GPU, Neural Engine) offers a viable on-device alternative, but until recently there was no complete, production-ready local serving stack to support the full agentic loop.

---

## Main Original Ideas

1. **Four-layer local agent stack** -- MLX (low-level array ops + Metal acceleration) → MLX-LM (model lifecycle: load, quantize, fine-tune) → MLX-LM Server (OpenAI-compatible REST API with structured tool calling and reasoning model support) → any agent framework (OpenCode, Xcode Intelligence, custom scripts). Because the server implements the standard OpenAI chat completions protocol, any agent framework works without modification.

2. **Neural Accelerator targeting for prompt processing** -- Agentic sessions are token-processing-heavy, not token-generation-heavy (tool outputs flood the context). M5's dedicated Neural Accelerators make matrix multiplication 4× faster than M4. MLX automatically selects the optimal kernel for available hardware -- no code changes or special flags required.

3. **Continuous batching for concurrent subagents** -- Multi-agent patterns spawn parallel subagents that hit the local server simultaneously. MLX-LM Server dynamically groups incoming requests into batches processed together on the GPU; new requests join an in-flight batch without queueing, preventing subagent stalls.

4. **Distributed inference over Thunderbolt/Ethernet** -- Models too large for a single machine (e.g., DeepSeek's 1.6T-parameter model requiring 800+ GB) can be sharded across multiple Macs using `mlx.launch` + a hostfile. macOS 26.2 adds Thunderbolt RDMA support, enabling up to 3× speedup with four nodes. This also parallelizes prompt processing, directly accelerating the agentic loop.

---

## Key Findings

| Optimization | Metric | Detail |
|---|---|---|
| Neural Accelerators (M5 vs M4) | 4× matrix multiply | Prompt processing speedup; automatic kernel selection |
| Continuous batching | Concurrent requests | In-flight batch joining; no per-request queueing |
| Distributed inference (Thunderbolt RDMA, macOS 26.2) | Up to 3× with 4 nodes | Prompt processing + enables models >512 GB |

- Setup is three commands: `pip install mlx-lm`, `mlx_lm.server --model <name>`, set `base_url=localhost` in the agent config.
- MLX-LM Server is a drop-in replacement for any OpenAI-compatible cloud API.
- Ecosystem builds on the same stack: Ollama, LM Studio, vLLM all run on MLX under the hood.
- Live demo: agent built a functional SwiftUI iPad drawing app from a blank Xcode project in ~2 minutes, then iterated (added rounded end caps) with compile-and-fix loops -- all locally.
- Xcode Intelligence can be pointed at a local MLX server via Settings → Intelligence → Add Chat Provider → Locally Hosted, enabling on-device code understanding and bug fixing without code leaving the machine.

---

## Suggestions & Future Directions

1. **Distributed session on setup** -- "Explore distributed inference and training with MLX" WWDC session covers multi-Mac Thunderbolt RDMA setup in depth.
2. **Ecosystem expansion** -- The standard OpenAI-compatible API means any new agent framework or IDE plugin can target the local server without Apple-specific integration.
3. **Model size roadmap** -- Distributed support enables running frontier-scale models (1T+ parameter class) on multi-Mac clusters, suggesting a path toward local equivalents of the largest cloud models.
4. **Iterative agentic coding** -- The SwiftUI demo illustrates a pattern: agent writes → builds → observes errors → fixes → repeats, without human copy-paste. This loop can run indefinitely until quality criteria are met.

---

## Authors & Institutions

Angelos (MLX team, Apple Inc.)
