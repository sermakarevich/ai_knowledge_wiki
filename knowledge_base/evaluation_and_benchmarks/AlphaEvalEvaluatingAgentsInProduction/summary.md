# AlphaEval: Evaluating Agents in Production

**Paper:** [AlphaEval: Evaluating Agents in Production (Pengrui Lu, Bingyu Xu et al., 2026)](https://arxiv.org/abs/2604.12162)

## Human Readable TL;DR

Imagine hiring a contractor to renovate your house, but the only tests you used were from a textbook -- perfect diagrams, no surprises, simple instructions. That's what most AI agent evaluations look like today. This paper builds a much harder test: real jobs from real companies, with missing information, unstated rules, and outputs judged by domain experts -- the way actual work gets done. The best AI agent only completed about 64% of the work correctly, revealing a large gap between lab performance and real-world usefulness.

## TL;DR

AlphaEval is a production-grounded benchmark of 94 tasks sourced from seven commercial deployments across six occupational domains. It reveals a significant research-to-production performance gap: the best agent (Claude Code + Claude Opus 4.6) scores 64.41/100, with extreme domain variance (30.0 in HR to 62.0 in Tech Research). A key finding is that the agent scaffold influences performance as much as the underlying model, and score rankings do not always align with economic value delivered.

---

## Problem & Motivation

Existing agent benchmarks (SWE-bench, WebArena, OSWorld) use curated tasks with explicit goals and deterministic metrics -- conditions that don't match commercial deployments. Production settings involve: implicit constraints, fragmented multi-modal inputs, undeclared domain knowledge requirements, long-horizon deliverables, and success criteria that evolve with business needs. This "research-production gap" means strong benchmark scores give false confidence about real-world agent readiness.

---

## Main Original Ideas

1. **Production-Grounded Benchmark (AlphaEval)** -- 94 tasks derived from active commercial AI deployments at seven companies, spanning six O*NET occupational domains (HR, Finance, Procurement, Software Engineering, Healthcare, Technology Research). Tasks preserve original under-specification and implicit constraints.

2. **Requirement-to-Benchmark Construction Framework** -- A four-stage pipeline (Partner Engagement → Requirement Elicitation → Task Formalization → Iterative Validation) that systematically transforms loosely worded production requirements into executable, automated evaluation tasks with standardized rubrics.

3. **Complete Agent Product Evaluation** -- Evaluates full agent systems (Claude Code, Codex, GitHub Copilot, Cursor) rather than underlying models alone, capturing scaffold-level performance variation invisible to model-centric benchmarks.

4. **Economic Value Annotation** -- Each task is annotated with human replacement cost (expert-calibrated). The 94 tasks represent ~2,420 professional hours, valued at $154K--$231K USD, enabling value-based rather than score-based agent selection.

5. **Evaluation Pluralism** -- Each task uses at least 2 of 4 evaluation paradigms (reference answer verification, formal logic verification, rubric-based, execution-based), with LLM-as-a-Judge (Claude Opus 4.6) as a cross-cutting semantic evaluator. Average 2.8 evaluation types per task.

6. **Production-Specific Failure Mode Taxonomy** -- Six distinct failure patterns identified qualitatively: cascade dependency failure, subjective judgment collapse, information retrieval failures, cross-section logical inconsistency, constraint misinterpretation, and format compliance failures.

---

## Key Findings

| Agent Configuration | Overall Score | HR | Finance | Procurement | SW Eng | Healthcare | Tech Research |
|---|---|---|---|---|---|---|---|
| Claude Code + Opus 4.6 | **64.41** | **38.91** | **70.35** | 72.40 | 58.00 | **50.06** | **71.20** |
| Cursor + Opus 4.6 | ~60 | -- | -- | **88.09** | -- | -- | -- |
| Copilot + GPT-5.2 | **54.91** | -- | -- | -- | -- | -- | -- |
| Codex + Opus 4.6 | 53.45 | -- | -- | -- | -- | -- | -- |
| Claude Code + GPT-5.2 | 39.47 | -- | -- | -- | -- | -- | -- |
| *Domain Average* | -- | *30.0* | *55.8* | *61.7* | *56.3* | *38.6* | *62.0* |

- Scaffold impact can swing performance by 15+ points for the same underlying model (GPT-5.2 via Claude Code: 39.47 vs. via Copilot: 54.91)
- Score rank ≠ value rank: Codex + Opus 4.6 (score 53.45) delivers $86K--$129K, while Claude Code + Gemini 3 Pro (score 50.78) delivers more at $89K--$133K due to better performance on higher-value domains
- Evaluation stability confirmed: ±1.83 confidence interval over 3 independent runs; LLM-judge agreement with experts Cohen's κ = 0.69--0.78 (substantial)
- Human Resources is the hardest domain (avg 30.0); no agent exceeded 38.91

---

## Suggestions & Future Directions

1. **Expand occupational coverage** -- The current six O*NET domains are not exhaustive; future work should extend to more occupation categories, particularly where human labor and economic value are concentrated.
2. **Longitudinal benchmarking** -- The current benchmark is a single time snapshot; continuous evolution of tasks and rubrics is needed as agent capabilities and business requirements shift.
3. **Improve subjective judgment capabilities** -- Agents consistently fail at tasks requiring nuanced human-like assessment (HR, soft-skill evaluation); research into value-aligned subjective reasoning is needed.
4. **Address implicit constraint handling** -- Agents tend to optimize explicit objectives while violating unstated rules; future work should improve constraint inference from context.
5. **Multi-modal reasoning** -- Better handling of fragmented information across PDFs, spreadsheets, scanned images within single task contexts.
6. **Long-form coherence** -- Agents produce internally contradictory long-form outputs; research into cross-section consistency is warranted.
7. **Organizational adoption** -- The requirement-to-benchmark framework is open-sourced to allow companies to build their own production-grounded benchmarks; community expansion is encouraged.

---

## Authors & Institutions

Pengrui Lu (SII, SJTU, GAIR, MiraclePlus, HIT, UCAS), Bingyu Xu (SII, SJTU, GAIR, MiraclePlus, HIT, UCAS), Wenjun Zhang, Shengjia Hua, Xuanjian Gao, Ranxiang Ge, Linxuan Wu, Yiran Li, Fengyue Meng, Yuchen Ni, Jiajun Li, Jinxiu Liu, Danfeng Zhang, Jingru Zhao (MiraclePlus), Lyumanshan Ye (SJTU, GAIR), Junfei Fish Yu (HunterAI), Yibo Zhang, Ruixin Li, Manxiang Li, Xiao Han (KuaFuAI), Xiaocong Zhou (POET), Guangyao Chi (LangCore), Zisheng Chen (Jiqizhixin), Kaishen Chen, Kun Wang (CinoCore), Qihua Xu. Corresponding author: Pengfei Liu (SII, SJTU, GAIR).
