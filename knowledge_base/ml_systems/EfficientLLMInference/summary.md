# Efficient LLM Inference: Systems, Algorithms & Production Engineering

**Source:** Interview Pocket Notes, Second Edition 2026
**Author:** Lamhot Siagian (AI Engineering Insider)
**Type:** Technical reference guide / interview prep book (not an arxiv paper)

---

## Human Readable TL;DR

Imagine you built an incredibly smart assistant, but every time someone asks it a question, it has to load its entire brain from a filing cabinet before it can say a single word -- and the filing cabinet is the bottleneck, not how smart it is. This book is the engineering manual for making that process fast and cheap: how to compress the brain, cache the filing cabinet cleverly, predict what it's about to say so you can skip steps, and run many conversations at once without running out of drawers. It covers everything from the physics of GPU memory to scheduling thousands of user requests per second.

---

## TL;DR

A comprehensive, interview-oriented reference covering the full stack of LLM inference optimization: from the hardware physics of GPU memory bandwidth (the fundamental bottleneck) through transformer mechanics (KV cache, prefill vs. decode asymmetry), to algorithms (quantization, speculative decoding, FlashAttention), production systems (vLLM, continuous batching, disaggregated serving), and emerging paradigms (inference-time compute scaling, o1/R1-style reasoning). Each chapter includes worked mock Q&A for interview preparation.

---

## Core Mental Model

**The Iron Triangle:** Every inference optimization navigates a trilemma:

| Metric | Definition | Key Lever |
|--------|-----------|-----------|
| **Latency** | TTFT + TPOT per request | Small model, speculative decoding, prefix caching |
| **Throughput** | Tokens/s across all users | Continuous batching, tensor parallelism |
| **Cost** | $/1M tokens | Quantization, GPU utilization, spot instances |

**The fundamental constraint:** LLM decode is *memory-bandwidth-bound*, not compute-bound. A 7B FP16 model = 14 GB; an A100 loads it in ~7 ms/step. You pay to move weights, not to multiply them. Prefill is compute-bound (GEMM); decode is memory-bound (GEMV). This asymmetry drives most of the book's content.

---

## Chapter-by-Chapter Key Ideas

### Ch 1 -- The Inference Problem
- Autoregressive loop: prefill (parallel, compute-bound) + decode (sequential, memory-bound)
- Roofline model: `Performance = min(Peak FLOP/s, Arithmetic Intensity × Peak Bandwidth)`
- Decode arithmetic intensity: ~1--2 FLOP/byte (far below the compute-bound threshold)
- Key metrics: **TTFT** (time to first token), **TPOT** (time per output token)

### Ch 2 -- Hardware Foundations
- H100 SXM: 132 SMs, 80 GB HBM3 @ 3.35 TB/s, NVLink @ 900 GB/s
- Tensor Cores: FP8/INT8 = 3,958 TFLOP/s (~2× FP16); inference favors lower precision
- Apple Silicon advantage: unified memory eliminates PCIe bottleneck; 192 GB @ 800 GB/s
- Emerging: Groq LPU (all-SRAM, ~500 tok/s), Cerebras WSE-3, photonic computing

### Ch 3 -- Transformer Inference Mechanics
- **KV cache** for LLaMA-2 70B at 4K context: ~10.7 GB per sequence
- Attention variants by KV cache size: MHA : GQA : MLA ≈ 8 : 2 : 1
- **RoPE** enables context length extrapolation via NTK-aware scaling or YaRN
- MLA (DeepSeek-V2): projects KV into low-dimensional latent space, 5--13× cache reduction

### Ch 4 -- Quantization
- 70B FP32 = 280 GB; INT8 = 70 GB (fits one H100); INT4 = 35 GB
- **GPTQ**: layer-wise Hessian-based PTQ, strong on 30B+
- **AWQ**: protects high-activation channels via scaling; faster than GPTQ, preferred in production
- **Activation quantization** challenge: outlier channels (100× larger magnitude) require LLM.int8(), SmoothQuant, or FP8
- QAT: better accuracy at 2--3 bit via Straight-Through Estimator during fine-tuning

### Ch 5 -- Speculative Decoding
- Draft small model (3--7B) → verify with target model in one parallel pass
- Expected speedup: `1/(1-α^(K+1)) / (1-α)` where α = acceptance rate
- α = 0.7--0.9 for code; 0.5--0.7 for open-ended chat; theoretical 3.3× at α=0.8, K=5
- **Medusa**: K lightweight linear heads on target model; no separate draft model; 2--3×
- **EAGLE-2**: autoregressive draft model using hidden state + token embedding; 3--4×; best acceptance rates
- Note: latency optimization only -- no throughput benefit at high batch sizes

### Ch 6 -- KV Cache Optimization
- **PagedAttention** (vLLM): virtual memory paging for KV cache; 2--4× batch size improvement; copy-on-write prefix sharing
- **Prefix caching**: reuse KV for shared system prompts; 50--90% prefill reduction
- **StreamingLLM**: keep 4 "attention sink" tokens + sliding window for infinite-length inference
- **KV quantization**: INT8 standard in TensorRT-LLM and vLLM; ~2× memory reduction

### Ch 7 -- Kernel Engineering and FlashAttention
- Standard attention materializes n×n matrix in HBM; at 16K tokens = 537 MB
- **FlashAttention**: tiling into SRAM, online softmax trick → O(n²/M) HBM reads vs. O(n²); 2--4× faster
- FA3 achieves ~75% of H100 peak FLOP/s via WGMMA + TMA + ping-pong pipelining
- **Triton**: Python DSL for GPU kernels; days vs. weeks for CUDA; 10--20% of peak performance gap

### Ch 8 -- Serving Systems Architecture
- **Continuous batching** (Orca/vLLM): iteration-level scheduling; 2--23× throughput over static batching
- **Chunked prefill** (Sarathi-Serve): prevents prefill piracy; interleaves 512-token chunks with decode steps
- **Disaggregated serving** (Splitwise, Mooncake): separate prefill and decode nodes; KV migration via RDMA is the hard part (~200 ms for 10 GB over 400 Gb/s InfiniBand)
- **SLO-aware scheduling**: priority queuing, preemption, admission control

### Ch 9 -- Parallelism
- 405B model in BF16 = 810 GB; requires multi-GPU
- **Tensor parallelism**: shard weight matrices across GPUs; one AllReduce per layer; scales to 8 GPUs on NVLink node
- **Pipeline parallelism**: different layers on different GPUs; pipeline bubble = (p-1)/p, mitigated by micro-batching
- **MoE** (Mixtral, DeepSeek-V2, Grok-1): top-K expert routing; AllToAll for expert parallelism; load imbalance and expert offloading challenges

### Ch 10 -- Long-Context and Memory Management
- 1M context naive attention matrix = 2 petabytes
- FlashAttention reduces HBM requirement from O(n²) to O(n); makes 128K feasible
- **Ring Attention**: distributes sequence across p devices; no extra communication overhead
- **LLMlingua**: 4--20× context compression with <5% quality loss
- **Mamba/SSMs**: O(n) compute, O(1) memory; weaker precise retrieval than attention; use for streaming/evolving-state tasks

### Ch 11 -- Edge and On-Device Inference
- iPhone 16 Pro (8 GB): can run Llama 3 8B at 4-bit via llama.cpp
- **llama.cpp**: C/C++, CPU/Metal/CUDA/Vulkan, k-quant formats (Q4_K_M is the practical sweet spot)
- **Apple MLX**: unified memory, no PCIe bottleneck; 70B at 4-bit on M3 Ultra ~30 tok/s
- NAS/OFA: train one supernet → extract sub-networks of different sizes for target hardware budgets

### Ch 12 -- Inference-Time Compute Scaling
- New paradigm (2024--2025): spending more compute at inference time improves quality
- CoT multiplies inference cost by 50× for a 10-token answer
- **Best-of-N**: N=64 can match a 10× larger model on math benchmarks
- **Process Reward Models (PRMs)**: score intermediate reasoning steps; enable MCTS/beam search
- **DeepSeek-R1 / o1**: RL-trained reasoning via GRPO; extended internal monologues ("thinking"); reasoning emerges from verifiable reward without supervised traces

### Ch 13 -- Observability and Production Engineering
- Key metrics: TTFT, TPOT, **Goodput** (fraction meeting all SLOs simultaneously), MFU
- Goodput formula: if TTFT SLO = 95% and TPOT SLO = 95%, goodput ≈ 90%
- Failure mode table: TTFT spikes → prefill piracy; TPOT regression → KV evictions; OOM → KV overflow
- Cost = (GPU cost/hr × hours) / total tokens; reduce via quantization, higher utilization, spot instances

### Ch 14 -- The Future of Inference
- **Diffusion LMs** (MDLM, LLaDA): parallel generation, not yet quality-competitive with AR
- **Multi-token prediction** (Meta): K output heads; 1.8--2.5× decode speedup; better training efficiency
- **Mixture of Depths**: tokens skip layers based on difficulty; 50% FLOP cost at similar perplexity
- **Photonic computing**: near-zero energy matrix multiply using light; currently limited to 512×512 matrices
- **Inference-first design**: GQA/MLA, SwiGLU, activation sparsity, depth over width (Phi-3, Gemma)

---

## Key Formulas Reference

| Concept | Formula |
|---------|---------|
| KV Cache Size | `2 × L × n × H × d_h × bytes` |
| Speculative Speedup | `E[accepted] = (1 - α^(K+1)) / (1 - α)` |
| Pipeline Bubble Fraction | `(p-1) / (m+p-1)` |
| MFU | `Achieved FLOP/s / Peak FLOP/s` |
| Cost per Token | `GPU cost/hr / tokens/hr` |
| Roofline | `Perf = min(Peak FLOP/s, I × B_mem)` |

---

## Essential Paper Reading List

1. **Attention Is All You Need** (Vaswani et al., 2017)
2. **FlashAttention** (Dao et al., 2022) + **FlashAttention-2** (2023)
3. **vLLM/PagedAttention** (Kwon et al., 2023)
4. **GPTQ** (Frantar et al., 2022) + **AWQ** (Lin et al., 2023)
5. **Speculative Decoding** (Leviathan et al., 2023)
6. **Medusa** (Cai et al., 2024), **EAGLE-2** (Li et al., 2024)
7. **DeepSeek-V2** (2024) -- MLA + MoE
8. **Mamba** (Gu & Dao, 2023)
9. **Sarathi-Serve** (Agrawal et al., 2024) -- chunked prefill
10. **DeepSeek-R1** (2025) -- GRPO reasoning

---

## Author & Source

**Lamhot Siagian** -- AI Engineering Insider
LinkedIn: linkedin.com/in/lamhotsiagian
Second Edition, 2026
