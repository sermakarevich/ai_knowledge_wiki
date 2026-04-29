# How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings

**Paper:** [How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings (Liu, Ji et al., 2025)](https://arxiv.org/abs/2604.04323)

## Human Readable TL;DR

Imagine you have a huge recipe book, but when you actually try to cook, you can't find the right recipe, the instructions don't quite match what's in your fridge, and sometimes a bad recipe leads you astray. This paper tests whether AI coding assistants actually benefit from "skills" -- reusable instruction sheets -- when they have to find and adapt those skills themselves, rather than being hand-fed the perfect one. The answer: benefits shrink dramatically under realistic conditions, and weaker assistants can actually perform worse with bad skills than with none at all.

## TL;DR

This paper systematically evaluates LLM agentic skills under progressively realistic conditions -- from hand-curated and force-loaded to autonomously retrieved from a 34K skill collection. Skill benefits degrade sharply as agents must independently select, retrieve, and adapt skills, with weaker models even performing below no-skill baselines when given irrelevant skills. A query-specific refinement strategy recovers substantial performance by enabling task-aware skill synthesis at inference time.

---

## Problem & Motivation

Agentic skills -- reusable, domain-specific knowledge artifacts (API patterns, coding conventions, workflows) -- are widely adopted in platforms like Claude Code, Codex, and open-source agent frameworks. However, existing benchmarks (e.g., SKILLSBENCH) evaluate skills under idealized conditions: small sets of hand-crafted, task-specific skills directly injected into context. This bypasses three critical real-world challenges:

1. **Skill selection** -- choosing which skills to load from available options
2. **Skill retrieval** -- finding relevant skills from a large, unorganized repository
3. **Skill adaptation** -- extracting value from general-purpose skills that don't perfectly match the task

No prior work had rigorously measured how skill utility degrades as these challenges are introduced.

---

## Main Original Ideas

1. **Progressive realism evaluation framework** -- Six evaluation settings that systematically introduce selection, retrieval, and adaptation challenges, moving from idealized force-loaded curated skills down to fully autonomous retrieval from a 34K real-world skill collection without curated skills present.

2. **Large-scale real-world skill collection** -- Assembly of 34,198 permissively-licensed skills from open-source repositories via aggregation platforms (skillhub.club, skills.sh), providing the first realistic-scale retrieval testbed for agentic skills.

3. **Comprehensive skill retrieval study** -- Comparison of five retrieval strategies (direct semantic, agentic keyword, agentic semantic, agentic hybrid w/o content, agentic hybrid w/ content), demonstrating agentic hybrid search outperforms naive semantic search by 18.7 percentage points on Recall@3.

4. **Query-specific skill refinement** -- An inference-time strategy where the agent reads the task, examines retrieved skills, attempts an initial solution, self-evaluates, and then synthesizes a refined skill set tailored to the specific task -- recovering significant performance losses from realistic retrieval.

5. **Cross-model and cross-benchmark generality** -- Evaluation across three model-harness pairs (Claude Opus 4.6/Claude Code, Kimi K2.5/Terminus-2, Qwen3.5-397B/Qwen-Code) and two benchmarks (SKILLSBENCH, TERMINAL-BENCH 2.0), demonstrating findings generalize beyond a single system.

---

## Key Findings

### Skill Retrieval Performance

| Method | Recall@3 | Recall@5 | Recall@10 |
|---|---|---|---|
| Direct Semantic | 38.1% | 44.5% | -- |
| Agentic Keyword | 43.9% | 49.0% | 56.8% |
| Agentic Semantic | 50.0% | 54.2% | 60.0% |
| Agentic Hybrid w/o content | 54.2% | 58.1% | 65.8% |
| **Agentic Hybrid w/ content** | **56.8%** | **61.3%** | **68.3%** |

### Performance Degradation Across Settings (SKILLSBENCH Pass Rate)

| Setting | Claude Opus 4.6 | Kimi K2.5 | Qwen3.5-397B |
|---|---|---|---|
| Curated + forced load | **55.4%** | **26.6%** | **27.4%** |
| Curated (agent selects) | 51.2% | 24.0% | 23.8% |
| Curated + distractors | 43.5% | 19.1% | 24.4% |
| Retrieved w/ curated | 40.1% | 21.0% | 22.6% |
| Retrieved w/o curated | 38.4% | 19.8% | 19.7% |
| No skills | 35.4% | 21.8% | 20.5% |

- Weaker models (Kimi, Qwen) perform **below no-skill baselines** when given irrelevant retrieved skills, indicating active misleading
- Even with curated skills available, agents often fail to load them -- only 49% of Claude trajectories loaded all curated skills
- Query-specific refinement recovers substantial losses: Claude 40.1% -> 48.2% on retrieved w/ curated; improvements generalize to TERMINAL-BENCH 2.0 (Claude 61.4% -> 65.5%, Kimi 50.6% -> 56.2%, Qwen 44.2% -> 49.1%)
- Query-agnostic refinement provides only moderate, inconsistent gains due to lack of task context
- Refinement effectiveness correlates with initial retrieved skill quality (coverage score >= 3.83 predicts gains)

---

## Suggestions & Future Directions

1. **Improve core skill retrieval algorithms** -- Current best (agentic hybrid w/ content) still only achieves 68.3% Recall@10, leaving significant room for better skill discovery mechanisms.

2. **Develop more sophisticated offline refinement** -- Query-agnostic refinement underperforms; better methods are needed to enhance skill quality without requiring task-specific context.

3. **Design robust skill ecosystems** -- Skill platforms should account for varying LLM capabilities, since weaker models are actively harmed by low-quality skills while stronger models can partially filter noise.

4. **Address the skill selection bottleneck** -- Agents frequently fail to load even available relevant skills; better mechanisms for skill evaluation and loading decisions are needed.

5. **Explore safety implications** -- The finding that irrelevant skills can degrade performance below no-skill baselines raises concerns about adversarial or low-quality skills in open repositories.

6. **Scale refinement approaches** -- Query-specific refinement shows promise but adds inference-time cost; finding efficient ways to achieve similar adaptation is an open problem.

---

## Authors & Institutions

Yujian Liu (UC Santa Barbara), Jiabao Ji (UC Santa Barbara), Li An (UC Santa Barbara), Tommi Jaakkola (MIT CSAIL), Yang Zhang (MIT-IBM Watson AI Lab), Shiyu Chang (UC Santa Barbara)
