# Diversity Collapse in Multi-Agent LLM Systems

**Paper:** [Diversity Collapse in Multi-Agent LLM Systems (Nuo Chen et al., 2025)](https://arxiv.org/abs/2604.18005)

## Human Readable TL;DR

Imagine you ask 10 people to brainstorm independently and they come up with wildly different ideas -- but when you put them in a meeting room, social pressure kicks in and they all start agreeing with the most confident voice in the room, leaving you with one mediocre idea instead of ten good ones. This paper shows the exact same thing happens with AI agents: the more you let them talk to each other, the more they end up repeating the same idea. Surprisingly, teams of "junior" agents who don't defer to authority explore far more creative territory than teams of senior experts. The fix isn't more agents -- it's better meeting structure: make agents write ideas independently before sharing, or split them into small subgroups that compete.

## TL;DR

This paper systematically studies how collaborative interaction among LLM agents affects the diversity of generated ideas in open-ended tasks (scientific research proposals). It finds that multi-agent interaction frequently causes "diversity collapse" -- a premature convergence driven by structural coupling rather than model weakness. Junior-dominated horizontal teams outperform expert hierarchies on diversity (Vendi 8.08 vs. 4.65). Process interventions (Nominal Group Technique, subgroups) robustly counteract collapse by preserving agent independence.

---

## Problem & Motivation

Multi-agent systems (MAS) are increasingly deployed for creative tasks under the assumption that more agents = more diverse ideas. This assumption is largely untested. The authors observe that MAS built on homogeneous LLMs -- even with distinct role prompts -- tend to amplify shared pre-training biases rather than explore new territory. In domains like scientific discovery, the value of the system lies in covering a *wide* solution space, not converging on a single "best" answer. A premature consensus is a functional failure: it traps users in narrow regions, suppresses unconventional hypotheses, and wastes compute without broadening the search.

---

## Main Original Ideas

1. **Diversity Collapse as a Structural Phenomenon** -- Diversity loss in MAS is primarily a structural failure caused by how agents interact (topology, authority, group size), not a limitation of individual model capability. Even powerful models collapse when forced into high-coordination structures.

2. **Three-Level Hierarchical Analysis** -- The paper introduces a structured decomposition: (a) Model Intelligence (inherent quality-diversity of base LLMs), (b) Agent Cognition (how persona composition shapes idea space), and (c) System Dynamics (how group size, rounds, and topology evolve diversity over time).

3. **Compute Efficiency Paradox** -- Stronger, more-aligned models produce higher per-sample quality but lower diversity. Alignment acts as a global semantic regularizer, compressing the accessible idea space without proportional quality gains.

4. **False Consensus Trap** -- Agents with distinct personas still share pre-training inductive biases. Interaction triggers social deference dynamics (sycophancy, polite consensus collapse) that synchronize trajectories toward a single semantic centroid.

5. **Junior-Dominated Superiority** -- Flat horizontal teams of junior personas achieve significantly higher diversity than expert-led or interdisciplinary teams, because they lack the authority gradient that drives deference.

6. **Process Interventions as Structural Fixes** -- Nominal Group Technique (blind-writing phase before discussion) and subgroup partitioning create "local pockets of divergence" that resist premature consensus, mirroring well-known social psychology interventions for human groups.

---

## Key Findings

| Structure / Condition | Vendi Score (Diversity) | Overall Quality |
|---|---|---|
| Horizontal (junior-dominated) | **8.08** | 7.88 |
| Vertical (hierarchical mix) | ~6.5 | ~8.1 |
| Naive (no persona) | ~5.8 | ~7.5 |
| Leader-Led | ~5.2 | ~8.0 |
| Interdisciplinary (expert) | 4.65 | **8.50** |

| Topology | Diversity Behavior |
|---|---|
| Standard (round-robin) | Baseline; collapses over rounds |
| Nominal Group Technique (NGT) | Highest initial diversity; mitigates anchoring |
| Subgroups | Highest sustained diversity; resilience spike midway |

- **Group size scaling:** Diversity Utilization Ratio (Vendi/N) drops from 1.03 at N=3 to 0.47 at N=7 -- more agents yield diminishing and sub-linear diversity returns.
- **Temporal dynamics:** Rounds show "stable expansion" -- global consensus tightens while local session exploration broadens; no chaotic drift.
- **Heterogeneous models:** Mixing DeepSeek-V3, GPT-4o, and Claude-Sonnet-4 rescues diversity in authority-heavy structures, complementing structural interventions.
- **Robustness:** Topology ranking (NGT/Subgroups > Standard) held across different persona types and was replicated with GPT-5.1.
- Human-LLM alignment on diversity judgments: 87% agreement with Vendi Score.

---

## Suggestions & Future Directions

1. **Adaptive topology switching** -- Dynamically switch communication structures mid-session based on real-time diversity monitoring to prevent collapse.
2. **Heterogeneous model ensembles** -- Combine agents backed by diverse base models as a complementary strategy to structural interventions.
3. **Diversity-aware orchestration** -- Build MAS orchestrators that explicitly optimize for maintaining semantic dispersion, not just task completion.
4. **Broader domain validation** -- Extend findings beyond AI research proposals to other open-ended domains (drug discovery, strategic planning, creative writing).
5. **Longitudinal and real-world studies** -- Study diversity dynamics in deployed MAS where agent memory, tool use, and human feedback introduce additional convergence pressures.
6. **Formal theory of structural coupling** -- Develop mathematical models of how interaction topologies map to diversity trajectories, grounding empirical findings in a predictive framework.

---

## Authors & Institutions

Nuo Chen, Yicheng Tong, Yufei He, Qingyun Zou, Qian Wang, Bingsheng He (National University of Singapore); Yuzhe Yang, Xueyi Zhang (The Chinese University of Hong Kong, Shenzhen)
