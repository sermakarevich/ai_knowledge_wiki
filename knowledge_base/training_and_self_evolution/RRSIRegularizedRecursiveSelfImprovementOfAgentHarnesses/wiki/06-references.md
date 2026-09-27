> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References (Anthropic Claude Opus 4.8 onward)
**In one sentence:** This chunk is the bibliography segment (pp. 11–14) listing cited model releases, harness-evolution methods, benchmarks, and background theory, beginning with Anthropic's Claude Opus 4.8 (2026a) and Sonnet 4.6 (2026b) announcements.
## Key points
- The chunk opens with two Anthropic model announcements: Claude Opus 4.8 (2026a) at `anthropic.com/news/claude-opus-4-8` and Claude Sonnet 4.6 (2026b) at `anthropic.com/news/claude-sonnet-4-6`.
- It cites two Google model references: Gemini 3.1 Pro (2026a) at `deepmind.google/models/gemini/pro/` and Gemini 3.5 (2026b) at the Google blog Gemini-models page.
- It lists harness foundry/adaptation works including HarnessX (arXiv:2606.14249), AutoHarness (arXiv:2603.03329), Meta-Harness (COLM 2026b), and Adaptive Auto-Harness (arXiv:2606.01770).
- It lists harness-evolution benchmarks and studies including Evo-Bench (arXiv:2608.09096), Evoharnessbench (arXiv:2609.04280), SWE-bench (ICLR 2024, pp. 54107–54157), and Terminal-bench (ICLR 2026, pp. 40903–40986).
- It cites recursive/self-improving agent works including Recursive Harness Self-Improvement (arXiv:2607.15524), Self-Harness (arXiv:2606.09498), Darwin Gödel Machine (ICLR 2026, pp. 104223–104294), and Huxley-Gödel Machine (arXiv:2510.21614).
- It cites memory/reasoning/RL works including EvolveMem (arXiv:2605.13941), ReasoningBank (ICLR 2026, pp. 94327–94354), SkillRL (arXiv:2602.08234), Agent0 (COLM 2026c), and R-Zero (ICLR 2026, pp. 130770–130790).
- It cites background theory and engineering commentary including Dwork et al. 2015 on adaptive data analysis (NeurIPS 28), Haarnoja et al. 2018 on Soft Actor-Critic (ICML pp. 1861–1870), Louizos et al. 2018 on L0 regularization (ICLR), Hastie et al. 2009 (Springer vol. 2), Goodfellow et al. 2016 (MIT Press vol. 1), plus blog posts by Weng (July 2026), Rajasekaran (2026), Lopopolo/OpenAI (2026), Zhang/Khattab (July 2026), Niklaus (2026), and Ding et al. (Aug 2026).
---
## Model releases and lab announcements
**Covers:** pp. 11–14, entries Anthropic (2026a/b) through Qwen Team (Apr 2026)

| Entry | Year | URL / venue |
|---|---|---|
| Anthropic. Introducing Claude Opus 4.8 | 2026a | https://www.anthropic.com/news/claude-opus-4-8 |
| Anthropic. Introducing Claude Sonnet 4.6 | 2026b | https://www.anthropic.com/news/claude-sonnet-4-6 |
| Google. Gemini 3.1 Pro | 2026a | https://deepmind.google/models/gemini/pro/ |
| Google. Gemini 3.5 | 2026b | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ |
| Qwen Team. Qwen3.6-Plus: Towards real world agents | April 2026 | https://qwen.ai/blog?id=qwen3.6 |
| Harvey AI. Harvey lab: The legal agent benchmark (v1.0) | 2026 | https://github.com/harveyai/harvey-labs/tree/v1.0; announcement at https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark |
| RSI-Exam Team. RSI-Exam | 2026 | https://github.com/aiming-lab/RSI-Exam |

## Harness foundries, adaptation, and evolution methods
**Covers:** pp. 11–14, HarnessX through Continual Harness entries

| Entry | Venue / ID |
|---|---|
| Chen et al. HarnessX: A composable, adaptive, and evolvable agent harness foundry | arXiv:2606.14249, 2026 |
| Liu et al. Adaptive auto-harness | arXiv:2606.01770, 2026b |
| Lou et al. AutoHarness: improving LLM agents by automatically synthesizing a code harness | arXiv:2603.03329, 2026 |
| Lee et al. Meta-harness: End-to-end optimization of model harnesses | Third Conference on Language Modeling, 2026b |
| Lee et al. Recursive harness self-improvement | arXiv:2607.15524, 2026a |
| Karten et al. Continual harness: Online adaptation for self-improving foundation agents | arXiv:2605.09998, 2026b |
| Karten et al. Prime agent: A self-improving RLM harness | Prime Intellect Blog, 2026a |
| Lin et al. Agentic harness engineering: Observability-driven automatic evolution of coding-agent harnesses | arXiv:2604.25850, 2026a |
| Lin et al. Harness updating is not harness benefit | arXiv:2605.30621, 2026b |
| Luo et al. Self-evolving agent harnesses via gated semantic quality-diversity | arXiv:2607.13683, 2026 |
| Nie et al. TTHE: Test-time harness evolution | arXiv:2607.08124, 2026 |
| Pan et al. Retrospective harness optimization | arXiv:2606.05922, 2026 |
| Zhang et al. Self-harness: Harnesses that improve themselves | arXiv:2606.09498, 2026a |
| Yang et al. Better harnesses, smaller models: Building 90% cheaper agents via automated harness adaptation | arXiv:2607.08938, 2026a |
| Wang et al. Rethinking the evaluation of harness evolution for agents | COLM 2026 2nd Workshop on Lifelong Agents, 2026b |
| Wang et al. Harness handbook | arXiv:2607.13285, 2026a |
| Zhang & Khattab. Language model harnesses are compositional generalizers | July 2026, https://alexzhang13.github.io/blog/2026/harness/ |
| Ding et al. What evolves when we talk about harness evolution? | wenwen-d.github.io, August 2026, https://wenwen-d.github.io/blog/harness-delta-attribution/ |
| Weng. Harness engineering for self-improvement | lilianweng.github.io, July 2026, https://lilianweng.github.io/posts/2026-07-04-harness/ |
| Lopopolo. Harness engineering: leveraging Codex in an agent-first world | 2026, https://openai.com/index/harness-engineering/ |
| Rajasekaran. Harness design for long-running application development | 2026, https://www.anthropic.com/engineering/harness-design-long-running-apps |
| Niklaus. Don't train the model, evolve the harness | 2026, https://huggingface.co/spaces/joelniklaus/harness-optimization |

## Benchmarks and evaluation
**Covers:** pp. 11–14, Frontier-Eng through GDPVal entries

| Entry | Venue / ID |
|---|---|
| Chi et al. Frontier-eng | arXiv:2604.12290, 2026 |
| Guo et al. Toward engineering AGI | NeurIPS 2025 |
| Huang et al. Evo-bench: Can language models improve agent harness? | arXiv:2608.09096, 2026d |
| Jimenez et al. SWE-bench | ICLR 2024, pp. 54107–54157 |
| Ke et al. Evoharnessbench | arXiv:2609.04280, 2026 |
| Li et al. Jobbench: Aligning agent work with human will | arXiv:2605.26329, 2026 |
| Merrill et al. Terminal-bench | ICLR 2026, pp. 40903–40986 |
| Patwardhan et al. GDPVal | ICLR 2026, pp. 24005–24040 |
| Vidgen et al. Apex-agents | arXiv:2601.14242, 2026 |
| Team et al. Neohorse-1 | arXiv:2609.08183, 2026 |

## Memory, reasoning, skills, and self-evolution
**Covers:** pp. 11–14, Envharness through SkillOpt entries

| Entry | Venue / ID |
|---|---|
| Huang et al. Envharness: Awakening static worlds for agent learning | arXiv:2608.19880, 2026b |
| Huang et al. G-zero: Self-play for open-ended generation from zero data | arXiv:2605.09959, 2026a |
| Huang et al. R-zero: Self-evolving reasoning LLM from zero data | ICLR 2026, pp. 130770–130790 (vol. 2026), 2026c |
| Liu et al. EvolveMem: Self-evolving memory architecture via autoresearch for LLM agents | arXiv:2605.13941, 2026a |
| Ouyang et al. ReasoningBank: Scaling agent self-evolving with reasoning memory | ICLR 2026, pp. 94327–94354 |
| Wu et al. AutoMem: Automated learning of memory as a cognitive skill | arXiv:2607.01224, 2026 |
| Xia et al. SkillRL | arXiv:2602.08234, 2026a |
| Xia et al. MetaClaw | arXiv:2603.17187, 2026b |
| Xia et al. Agent0: Unleashing self-evolving agents from zero data via tool-integrated reasoning | Third Conference on Language Modeling, 2026c |
| Yang et al. SkillOpt: Executive strategy for self-evolving agent skills | arXiv:2605.23904, 2026b |
| Tang et al. Agent KB: Leveraging cross-domain experience for agentic problem solving | arXiv:2507.06229, 2025 |
| Wang et al. Huxley-Gödel machine | arXiv:2510.21614, 2025 |
| Zhang et al. Darwin Gödel machine: open-ended evolution of self-improving agents | ICLR 2026, pp. 104223–104294, 2026b |
| Yao et al. ReAct: Synergizing reasoning and acting in language models | arXiv:2210.03629, 2022 |

## Background theory and methods
**Covers:** pp. 11–14, Dwork through Louizos entries

| Entry | Venue |
|---|---|
| Dwork et al. Generalization in adaptive data analysis and holdout reuse | NeurIPS 28, 2015 |
| Goodfellow, Bengio, Courville & Bengio. Deep learning, vol. 1 | MIT Press Cambridge, 2016 |
| Haarnoja et al. Soft actor-critic: Off-policy maximum entropy deep RL with a stochastic actor | ICML, pp. 1861–1870, PMLR, 2018 |
| Hastie, Tibshirani, Friedman & Friedman. The elements of statistical learning, vol. 2 | Springer, 2009 |
| Louizos, Welling & Kingma. Learning sparse neural networks through l0 regularization | ICLR, 2018 |

No verbatim quotes appear in this chunk; it consists solely of bibliography entries on pp. 11–14.
