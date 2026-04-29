# From Code Foundation Models to Agents and Applications: A Comprehensive Survey and Practical Guide to Code Intelligence

**Paper:** [From Code Foundation Models to Agents and Applications: A Comprehensive Survey and Practical Guide to Code Intelligence (Shi, Gao, Li et al., 2025)](https://arxiv.org/abs/2511.18538)

## Human Readable TL;DR

Imagine AI assistants that can write computer programs just by being told what to do in plain English -- tools like GitHub Copilot already do this. This massive survey is like an encyclopedia for that entire field: it explains how these AI coding helpers are built (what data they learn from, how they're trained), what they can and can't do today, and where they're headed. It also runs hands-on experiments to give practical recipes for anyone building such systems, and it warns that these tools can accidentally write insecure code if not carefully designed.

## TL;DR

This 200+ page survey systematically covers the full lifecycle of code LLMs -- from data curation, pre-training objectives, and architectural innovations (dense, MoE, diffusion, hybrid) through SFT, RLVR alignment, and autonomous SWE agents. It complements the literature review with original scaling-law experiments across seven languages, SFT hyperparameter sweeps, and RL training-recipe ablations, producing concrete guidelines for compute-efficient training. It also provides a thorough treatment of code LLM safety, red-teaming, and agentic safety frameworks.

---

## Problem & Motivation

LLMs have transformed automated software development -- HumanEval pass rates jumped from single digits to >95% in a few years, and commercial tools (GitHub Copilot, Claude Code, Cursor) are widely adopted. Yet prior surveys were either panoramic but shallow, or focused on earlier-generation models, leaving a critical gap: no single resource synthesizes contemporary advances in data strategies, alignment techniques, agentic systems, and safety while also providing empirical training recipes. This paper fills that gap by offering both a comprehensive synthesis and a practical guide, explicitly targeting the research-practice divide.

---

## Main Original Ideas

1. **Full-lifecycle taxonomy of code LLMs** -- A unified framework covering data curation, pre-training (next-token, multi-token, fill-in-the-middle, diffusion), post-training (SFT, RL/RLVR), prompting, and deployment for both general-purpose and code-specialized models.

2. **Language-specific scaling laws for code pre-training** -- Chinchilla-style scaling experiments across Python, Java, JavaScript, TypeScript, C#, Go, and Rust, revealing that interpreted languages (Python) benefit more from scale while statically-typed languages (Rust, Go) saturate faster with lower irreducible loss.

3. **Empirical SFT training recipes** -- Systematic framework comparisons (Megatron-LM, DeepSpeed, LLaMA-Factory, MS-Swift, VERL), hyperparameter sweeps (batch size, LR, scheduler, warmup), and dataset ablations on both dense (Qwen2.5-Coder-14B) and MoE (Qwen3-30B-A3B) architectures.

4. **RLVR ablation suite for code** -- Comparative evaluation of advantage estimators (GRPO, RLOO, REINFORCE++), response-length scaling (1K--30K tokens), and rollout-width scaling (4--512), with distinct recipe recommendations for Pass@1 vs. Pass@5 optimization.

5. **Code as a generalist agent medium** -- A conceptual framework positioning code not only as an output artifact but as a universal interaction protocol (tool use, MCP, multi-agent coordination), an agentic capability (planning and memory in code), and an environment interface (simulation gyms, GUI/terminal agents).

6. **End-to-end safety taxonomy for code LLMs** -- Structured analysis of threats and defenses across pre-training safety, post-training alignment, red-teaming (prompt-level, semantic, agentic), and runtime oversight for autonomous agents.

---

## Key Findings

### Scaling Laws

| Language | Alpha_N (model size) | Alpha_D (data volume) | L_infinity (irreducible loss) | Interpretation |
|---|---|---|---|---|
| Python | High | High | Higher | Benefits most from scale |
| Java / C# | Medium | Medium | Medium | Moderate saturation |
| Rust / Go | Low | Low | Lower | Saturates quickly |

### SFT Results

- **Global batch size** is the single most impactful SFT hyperparameter; smaller effective batches (64--256) preserve gradient signal best.
- **MoE models** are more sensitive to hyperparameters and require more epochs to stabilize than dense models.
- **Datasets with executable test supervision** (e.g., KodCode-V1) outperform purely instructional datasets on execution-based benchmarks (MBPP+).

### RLVR Results

| Setting | Best for Pass@1 | Best for Pass@5 |
|---|---|---|
| Advantage estimator | REINFORCE++_baseline | RLOO |
| Max response length | 16K tokens | 2K tokens |
| Rollouts per prompt | Moderate (N=16) | Higher (N=16--64) |
| Recommended default | 4K tokens, N=16, REINFORCE++ | -- |

### Broader Survey Findings

- Repository-level and multi-file tasks remain significantly harder than function-level generation; LLMs still struggle with long-context cross-file reasoning.
- SWE agents now span the full SDLC -- requirements, design, coding, testing, review, maintenance, and DevOps.
- Code LLMs are **insecure by default** because they learn from vulnerable public corpora; safety must be proactive, not reactive.

---

## Suggestions & Future Directions

1. **Repository-level intelligence** -- Current models falter on cross-file dependencies, long-horizon edits, and project-wide refactoring; advancing repository-level reasoning is a top priority.

2. **Reliable code correctness** -- Moving beyond pass@k on curated benchmarks toward verified functional correctness in production-scale, multi-dependency environments.

3. **Security-by-design training** -- Integrating vulnerability detection, secure coding patterns, and verifiable security rewards directly into pre-training and alignment pipelines rather than as post-hoc filters.

4. **Multilingual and multimodal code understanding** -- Better support for low-resource languages, cross-lingual transfer, and grounding code generation in visual/UI contexts.

5. **Scalable alignment and evaluation** -- Developing more robust LLM-as-a-judge frameworks, execution-based evaluation at scale, and benchmarks that reflect real-world software engineering complexity (beyond HumanEval/MBPP).

6. **Agentic safety and oversight** -- Establishing principled frameworks for sandboxing, runtime oversight, multi-agent review, and human-in-the-loop governance as coding agents gain autonomy.

7. **Compute-efficient training** -- Extending scaling-law analysis to MoE, hybrid, and diffusion architectures; optimizing data mixtures for multilingual pre-training.

---

## Authors & Institutions

Yupeng Shi, Yaowei Gao, Zhangyue Li, and 80+ contributors from Beihang University (SKLCCSE), Alibaba Group, ByteDance, OPPO, Huawei Cloud, Tencent, Kuaishou, TeleAI (China Telecom), Shanghai AI Lab, HKUST (Guangzhou), University of Manchester, University of Sheffield, Monash University / CSIRO Data61, Nanyang Technological University, National University of Singapore, Peking University, Nanjing University, Zhejiang University, Harbin Institute of Technology, Sichuan University, and others.
