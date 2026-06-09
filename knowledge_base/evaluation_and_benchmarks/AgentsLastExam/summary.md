# Agents' Last Exam

**Paper:** [Agents' Last Exam (Yiyou Sun, Xinyang Han, Weichen Zhang, et al., 2026)](https://arxiv.org/abs/2606.05405)

## Human Readable TL;DR

AI systems have been acing school tests for years, but when it comes to actually doing real jobs -- filling out financial reports, running engineering simulations, creating professional-grade media -- they still struggle. This paper creates the equivalent of a professional licensing exam for AI: a massive collection of real work tasks donated by over 250 actual professionals (lawyers, engineers, scientists, designers), where an AI must complete the full job from start to finish on a real computer. Today's best AI passes only about 1 in 4 of even the easiest tasks, and nearly none of the hardest ones. The point is not just to rank AI systems, but to define what "truly useful AI" would look like -- and to push AI research toward building it.

## TL;DR

ALE (Agents' Last Exam) is a benchmark of 960 expert-authored task workflows (1,490 instances) across 55 digital industries grounded in the SOC/O*NET occupational taxonomy. Tasks are sourced from real completed projects, require sustained computer use (GUI + CLI + code), and are scored via deterministic automated rubrics -- not human judges. Frontier agents achieve only 2.6% mean pass rate on the hardest tier; the best configuration (Codex + GPT-5.5) scores 26.2% overall. Model capability matters 3× more than harness choice.

---

## Problem & Motivation

AI systems have achieved strong results on benchmarks spanning games, math olympiads, and competitive programming, yet measurable economic impact across core industries (finance, law, engineering, manufacturing) remains surprisingly muted. The authors frame this as a "utility problem": benchmarks that measure abstract knowledge or isolated actions do not capture the sustained, tool-intensive work that actually generates economic value. Because benchmarks shape research directions -- as ImageNet did for computer vision -- building evaluations grounded in real professional workflows is critical for driving progress that translates into GDP-relevant impact.

---

## Main Original Ideas

1. **Agents' Last Exam (ALE) Benchmark** -- A living benchmark of 1,490 task instances across 55 SOC/O*NET-grounded digital industries, each sourced from a real project completed by an industry expert. Tasks span hours to weeks of expert time, require full computer-use capability (GUI + shell + code + web), and are verified via deterministic rubrics rather than human judgment.

2. **Three Design Principles: Representativeness, Complexity, Verifiability** -- Tasks must use the real software domain experts use (e.g., SolidWorks for CAD, RPGMaker for game development), represent complete end-to-end deliverables (not single actions), and produce outputs checkable against objective rubrics or reference files.

3. **Generalist Computer-Use Agent (GCUA) Target Class** -- ALE explicitly targets a new agent class decomposed into five layers: Brain (LLM reasoning), Eyes (GUI perception), Body (orchestration), Hands (tool invocation), and Feet (runtime substrate). Existing CLI agents lack Eyes; GUI agents lack deep Hands/Feet. ALE requires the full union.

4. **Decoupled Evaluation Architecture** -- Each task is a `main.py` exposing three lifecycle hooks: `load()` (declares requirements), `start()` (provisions a VM to deterministic state), and `evaluate()` (scores agent output in [0,1]). This decoupling allows any agent and any task to be combined freely across cloud VMs or local containers.

5. **Anti-Contamination Release Strategy** -- Only 10% of tasks (150 of 1,490) are public. The private pool rotates periodically: retired public tasks are replaced by new ones, maintaining an uncontaminated evaluation surface. Empirical validation (Pearson r=0.89) confirms the public subset is representative of the full pool.

6. **GUI-as-Tool Integration** -- A unified CUA MCP bridge exposes 14 desktop-action tools (keyboard, mouse, screenshot, etc.) as standard tool-call entries in the agent's action loop, enabling foundation models without native GUI modules to interact with graphical software alongside shell and code tools.

---

## Key Findings

| Configuration | Near-Term Pass% | Full-Spectrum Pass% | Last-Exam Pass% | Overall Pass% |
|---|---|---|---|---|
| Codex (GPT-5.5) | 42.4 | 20.0 | 8.6 | **26.2** |
| ALE-Claw (GPT-5.5) | 35.6 | 21.8 | 8.6 | 24.2 |
| Cursor (GPT-5.5) | 36.4 | 20.0 | 2.9 | 22.5 |
| Claude Code (Sonnet 4.6) | 31.4 | 12.7 | 0.0 | 17.1 |
| Claude Code (Opus 4.7) | 23.7 | 12.7 | 0.0 | 14.1 |
| Gemini 3.1 Pro | 29.7 | 10.9 | 0.0 | 15.8 |

- **Last-Exam tier is far from saturated**: average full pass rate across all configurations is 2.6%; most agents record 0% on the hardest tier.
- **Domain imbalance**: Computational math and agriculture/environment score ~60%; visual media and education stay below 30% -- reflecting uneven tool-use training coverage.
- **GUI underutilization**: 34% of tasks designate graphical software as the primary tool, but GUI tool calls stay well below that share; agents substitute Bash/CLI workarounds.
- **Failure breakdown** (Claude Code + Opus 4.7): Understanding failures 31% (domain knowledge gaps + hallucination), Approach failures 47% (wrong strategy + incomplete/abandoned), Execution failures 22% (bugs, format errors, GUI failures). The dominant bottleneck is domain knowledge, not execution.
- **Model > Harness**: Varying the backbone model under a fixed harness produced an 18.0 pp spread; varying the harness under a fixed model produced only a 5.3--6.0 pp spread.
- **No cost-performance correlation**: Higher API cost, wall-clock time, and token usage do not reliably predict better task scores.

---

## Suggestions & Future Directions

1. **Grow the living benchmark**: Continuously onboard new workflows and emerging industries (e.g., frontier digital occupations not yet in SOC 2018) to stay ahead of benchmark saturation and maintain a valid evaluation surface.
2. **Improve GUI integration**: Close the gap between GUI task demand (~34% of tasks) and actual GUI tool usage; better visual perception and action grounding are near-term research targets.
3. **Address domain knowledge gaps**: Since 78% of failures trace to understanding or approach errors rooted in missing specialized knowledge, training data and retrieval strategies for professional domains are a critical investment.
4. **Rethink token/cost efficiency**: Build agent configurations that achieve strong performance without proportionally higher cost -- current results show high spend doesn't correlate with high quality.
5. **Extend ALE to physical-digital hybrid industries**: The current taxonomy excludes sectors whose core work is not primarily digital; future versions could include partial coverage of such domains.
6. **Use ALE-CLI as a fixed scaffold**: ALE-Claw (a Python port of OpenClaw's agent loop) enables ablation of harness components and GUI models against a stable task suite -- useful for systematic harness research.

---

## Authors & Institutions

Yiyou Sun\*, Xinyang Han\*, Weichen Zhang\*, Yuanbo Pang\*, Tianyu Wang\*, Yuhan Cao\*, Yixiao Huang\*, Chris Duroiu, Haoyun Zhang, Jeffrey Lin, Weishu Zhang, Tyler Zeng, Ying Yan, Bo Liu, Hanson Wen, Mingyang Xu, Xiaoyuan Liu, Zimeng Chen, Weiyan Shi, Amanda Dsouza, Vincent Sunn Chen, Dawn Song\* -- **University of California, Berkeley** (core team; \*core contributors). Advisory committee includes experts from SciLifeLab, Caltech, Brown, NYU, UCSF, and others. 300+ data contributors from Stanford, University of Michigan, Oxford, UIUC, Johns Hopkins, and numerous other institutions.
