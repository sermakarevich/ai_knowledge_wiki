# SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

**Paper:** [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks (Li et al., 2026)](https://arxiv.org/abs/2602.12670)

## Human Readable TL;DR

Imagine you hire a new employee who is smart but unfamiliar with your company's specific procedures. You could either give them a well-written handbook of step-by-step instructions, or ask them to figure out the procedures on their own. This paper tests exactly that idea, but for AI assistants: it measures whether giving AI agents curated "recipe books" (called Skills) for specific tasks actually makes them better at their jobs. The answer is yes -- curated handbooks boost performance significantly, especially in specialized fields like healthcare -- but asking the AI to write its own handbook does not help at all. Interestingly, a short, focused guide works better than a massive manual.

## TL;DR

SkillsBench is the first benchmark to systematically evaluate Agent Skills -- structured packages of procedural knowledge injected at inference time -- across 86 tasks in 11 domains using 7 model-harness configurations and 7,308 trajectories. Curated Skills raise average pass rates by +16.2 percentage points, with domain-dependent variance ranging from +4.5pp (Software Engineering) to +51.9pp (Healthcare). Self-generated Skills provide no benefit on average (-1.3pp), demonstrating that models cannot reliably author the procedural knowledge they benefit from consuming. Focused Skills with 2--3 modules outperform comprehensive documentation, and smaller models equipped with Skills can match larger models without them.

---

## Problem & Motivation

LLM agents possess broad capabilities but lack the specific procedural knowledge needed for domain-specific workflows. Fine-tuning is expensive and sacrifices generality. Agent Skills -- modular packages of instructions, templates, and resources -- have been rapidly adopted as an inference-time augmentation strategy, with community repositories hosting tens of thousands of user-contributed Skills. However, no benchmark existed to systematically measure whether Skills actually help, which design factors matter, or when Skills fail. Practitioners could not make informed decisions about Skills adoption, and researchers lacked empirical grounding for Skills design principles.

---

## Main Original Ideas

1. **SkillsBench benchmark.** The first benchmark treating Agent Skills as first-class evaluation artifacts, comprising 84 tasks across 11 domains (Healthcare, Manufacturing, Cybersecurity, Natural Science, Energy, Office & White Collar, Finance, Media & Content Production, Robotics, Mathematics, Software Engineering) with curated Skills and deterministic pytest verifiers.

2. **Three-condition evaluation protocol.** Each task is evaluated under three conditions -- no Skills, curated Skills, and self-generated Skills -- enabling direct measurement of Skills impact and isolating whether models can produce their own procedural knowledge.

3. **Skills design factor analysis.** Systematic study of how Skills quantity (1, 2--3, 4+), complexity (compact, detailed, standard, comprehensive), and domain alignment affect agent performance, yielding actionable authoring guidelines.

4. **Cross-harness, cross-model evaluation.** Testing across 3 commercial agent harnesses (Claude Code, Gemini CLI, Codex CLI) and 7 frontier models (Claude Opus 4.5/4.6, Sonnet 4.5, Haiku 4.5, Gemini 3 Pro/Flash, GPT-5.2) to assess generalizability.

5. **Leakage prevention pipeline.** A CI-based validation agent that audits Skills for task-specific solutions, ensuring Skills encode procedural guidance rather than declarative answers.

---

## Key Findings

### Main Results: Pass Rates Across Skills Conditions

| Harness | Model | No Skills | With Skills | Delta | Self-Generated | Delta |
|---|---|---|---|---|---|---|
| Gemini CLI | Gemini 3 Flash | 31.3% | **48.7%** | +17.4 | -- | -- |
| Claude Code | Opus 4.5 | 22.0% | **45.3%** | +23.3 | 21.6% | -0.4 |
| Codex | GPT-5.2 | 30.6% | **44.7%** | +14.1 | 25.0% | -5.6 |
| Claude Code | Opus 4.6 | 30.6% | **44.5%** | +13.9 | 32.0% | +1.4 |
| Gemini CLI | Gemini 3 Pro | 27.6% | **41.2%** | +13.6 | -- | -- |
| Claude Code | Sonnet 4.5 | 17.3% | **31.8%** | +14.5 | 15.2% | -2.1 |
| Claude Code | Haiku 4.5 | 11.0% | **27.7%** | +16.7 | 11.0% | 0.0 |
| **Mean** | | **24.3%** | **40.6%** | **+16.2** | **21.0%** | **-1.8** |

### Domain-Level Skills Efficacy

| Domain | With Skills | No Skills | Delta (pp) |
|---|---|---|---|
| Healthcare | **86.1%** | 34.2% | +51.9 |
| Manufacturing | **42.9%** | 1.0% | +41.9 |
| Cybersecurity | **44.0%** | 20.8% | +23.2 |
| Natural Science | **44.9%** | 23.1% | +21.9 |
| Energy | **47.5%** | 29.5% | +17.9 |
| Office & White Collar | **42.5%** | 24.7% | +17.8 |
| Finance | **27.6%** | 12.5% | +15.1 |
| Media & Content Production | **37.6%** | 23.8% | +13.9 |
| Robotics | **27.0%** | 20.0% | +7.0 |
| Mathematics | **47.3%** | 41.3% | +6.0 |
| Software Engineering | **38.9%** | 34.4% | +4.5 |

### Skills Design Factors

| Skills Count | With Skills | No Skills | Delta (pp) |
|---|---|---|---|
| 1 skill | 42.2% | 24.4% | +17.8 |
| **2--3 skills** | **42.0%** | 23.4% | **+18.6** |
| 4+ skills | 32.7% | 26.9% | +5.9 |

| Complexity | Pass Rate | Delta (pp) |
|---|---|---|
| **Detailed** | **42.7%** | **+18.8** |
| Compact | 37.6% | +17.1 |
| Standard | 37.1% | +10.1 |
| Comprehensive | 39.9% | -2.9 |

### Qualitative Findings

- Self-generated Skills provide negligible or negative benefit (-1.3pp average), demonstrating models cannot reliably author their own procedural knowledge
- 16 out of 84 tasks showed negative deltas with curated Skills, indicating Skills can sometimes hinder performance
- Domains with specialized workflows underrepresented in pretraining data (e.g., clinical data harmonization, manufacturing) benefit most from Skills
- Claude Haiku 4.5 with Skills (27.7%) outperforms Claude Opus 4.5 without Skills (22.0%), showing Skills can partially compensate for model scale
- Gemini 3 Flash compensates for smaller model size by consuming 2.3x more input tokens per task than Pro, but its 4x lower per-token cost makes it 44% cheaper per task

---

## Suggestions & Future Directions

1. **Multi-modal Skills.** Extend Skills to vision-language agents operating in GUI environments, multi-agent coordination, and longer-horizon workflows.

2. **Causal attribution controls.** Develop length-matched baselines (random/irrelevant text, retrieval-only documentation) to disentangle the benefit of procedural structure from the benefit of simply having more context.

3. **Automatic Skills synthesis.** Study whether effective Skills can be automatically generated from demonstrations or documentation, and isolate which components (steps, examples, code resources) drive improvements.

4. **Ecosystem-representative evaluation.** Test with real-world Skill distributions that include lower-quality and automatically-selected Skills, rather than only curated ones.

5. **Skills composition research.** Investigate when multiple Skills help or interfere with each other, and whether compositional effects can be predicted.

6. **Authoring best practices.** Concise, stepwise guidance with at least one working example outperforms exhaustive documentation; modular Skills compose better on multi-part tasks; Skills should explicitly match harness constraints (e.g., format reminders for JSON-only protocols).

---

## Authors & Institutions

Xiangyi Li (BenchFlow), Wenbo Chen (Amazon), Yimin Liu (Ohio State University), Shenghan Zheng (Dartmouth College), Xiaokun Chen (Stanford University), Yifeng He (UC Davis), Yubo Li (Carnegie Mellon University), Bingran You (UC Berkeley), Haotian Shen (Independent), Jiankai Sun (Independent), Shuyi Wang (Independent), Qunhong Zeng (Beijing Institute of Technology), Di Wang (Foxconn), Xuandong Zhao (UC Berkeley), Yuanli Wang (Boston University), Roey Ben Chaim (Zenity), Zonglin Di (UC Santa Cruz), Yipeng Gao (USC), Junwei He (ByteDance), Yizhuo He (Carnegie Mellon University), Liqiang Jing (UT Dallas), Luyang Kong (Independent), Xin Lan (Michigan State University), Jiachen Li (UT Austin), Songlin Li (Stanford University), Yijiang Li (UC San Diego), Yueqian Lin (Duke University), Xinyi Liu (Independent), Xuanqing Liu (Independent), Haoran Lyu (Independent), Ze Ma (Columbia University), Bowei Wang (Independent), Runhui Wang (Independent), Tianyu Wang (Independent), Wengao Ye (University of Oxford), Yue Zhang (UT Dallas), Hanwen Xing (Independent), Yiqi Xue (USC), Steven Dillmann (Stanford University), Han-chung Lee (Independent)
