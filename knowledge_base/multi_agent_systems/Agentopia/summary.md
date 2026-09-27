# Agentopia: Long-Term Life Simulation and Learning in Agent Societies

**Paper:** [Agentopia: Long-Term Life Simulation and Learning in Agent Societies (Wang et al., 2026)](https://arxiv.org/abs/2606.07513)

## Human Readable TL;DR

Imagine a massive virtual city where 100 AI characters live out full years of social life -- making friends, pursuing careers, falling into rivalries, and dealing with money pressures. The researchers let this simulation run for ten virtual years and discovered that the characters developed surprisingly human-like habits and relationships on their own, without being scripted to do so. Better yet, the AI models that "lived" these simulated lives got noticeably better at impersonating fictional characters in other tasks -- as if the experience of social life actually taught them something about being human.

## TL;DR

Agentopia is a multi-agent simulation framework where 100 LLM-powered agents autonomously live through 10 simulated years of social life -- planning, socializing, building careers, and managing finances -- in three distinct fictional worlds. The system introduces a "life reward" grounded in Maslow's hierarchy of needs (social standing, subjective fulfillment, economic status) and uses rejection-sampling fine-tuning on high-advantage trajectories to train LLMs from simulated experience. Life reward training improves in-simulation agent well-being and generalizes to downstream role-playing benchmarks with a +15.6% gain on CoSER Test.

---

## Problem & Motivation

Prior LLM-based social simulations operate at the scale of days and focus on low-level physical interactions (e.g., "pick up wheat"), leaving long-term social dynamics -- personal growth, evolving relationships, career transitions -- unexplored. Meanwhile, persona simulation and role-playing research relies heavily on costly human-annotated or synthetic data that is difficult to scale. As human data approaches exhaustion, training LLMs through simulated experience represents a promising alternative. Agentopia asks: can LLMs learn anthropomorphic social intelligence by living years of simulated social life, the way humans do?

---

## Main Original Ideas

1. **Long-Term Life Simulation at Year Scale** -- Agentopia extends agent society simulation from days to 10 simulated years by structuring time into weekly cycles (Plan → Contact → Activity → Review) and annual settlements. Focusing on abstract social interactions rather than low-level operations achieves the token efficiency needed for this scale.

2. **Life Reward** -- A composite annual reward mirroring human well-being with three components: Social Reward (Weighted PageRank over affection/respect scores), Subjective Reward (Maslow-grounded fulfillment across mood, material, social, esteem), and Economy Reward (deposit change). Rewards are z-score normalized and summed to produce a scalar signal for optimization.

3. **File-System Long-Term Memory** -- Agents manage autonomous memory files (`general.txt`, `characters/<who>.txt`, `others/<name>.txt`) via function calls (read, update, list), with a read-before-write constraint. This lets agents decide what to remember across years without requiring retrieval-based search, and its summaries are auto-injected into the roleplay prompt.

4. **Generative Environment Engine** -- A separate stateless LLM replaces hard-coded simulation rules, serving as activity judge, speaker predictor, event generator, profile updater, and response verifier against 16 roleplay principles. This makes the environment flexibly adaptive without requiring exhaustive rule engineering.

5. **Life Reward Training** -- A rejection-sampling optimization method that computes per-agent self-referential advantages (improvement relative to one's own prior return, not cross-agent ranking) and selects the top 25% improvers per year. Their trajectories are mixed 50:50 with general instruction data (self-distillation) to prevent catastrophic forgetting.

---

## Key Findings

| Metric | Baseline (Qwen3.5-397B) | After Life Reward Training | Delta |
|--------|------------------------|---------------------------|-------|
| CoSER Test Overall | 42.51 | 49.16 | **+15.6%** |
| Anthropomorphism | 40.16 | 49.67 | **+23.7%** |
| Character Fidelity | 40.32 | 46.93 | **+16.4%** |
| Economy Reward (sim) | baseline | +2.5% | ↑ |
| Subjective Reward (sim) | baseline | +1.8% | ↑ |
| Respected by peers | baseline | +24.2% | ↑ |
| Liked by peers | baseline | +15.9% | ↑ |
| Material Fulfillment | baseline | -14.8% | ↓ (agents save more) |

- Agents exhibit rich emergent behaviors without explicit scripting: ice-breaking contact, mentorship, competitive training, career pivots for passion over pay, economic frugality, and intimacy evolution over years.
- Mutual friendship networks densified over 10 years, with world-specific topology (The Apartment: cross-community bridges; The Campus: tight communities).
- Gini coefficients for agent wealth decreased across all worlds (wealth equalizes), but overall reward rankings remained stable (top and bottom quartiles persist).
- "Striving" agents (high extra work, skill investment) accumulated more wealth but reported lower mood, social, and esteem fulfillment vs. "leisurely" agents -- a simulated well-being trade-off.
- Computational cost: ~13.7B tokens and ~186 wall-clock hours per 10-year simulation of 100 agents. Input tokens dominate (95%) and grow steadily as memory accumulates.

---

## Suggestions & Future Directions

1. **Memory management as the primary bottleneck** -- per-week runtime grows from ~80 to ~140 minutes over 10 years due to memory accumulation; better compression or selective forgetting mechanisms are critical.
2. **Finer credit assignment** -- the current method selects entire yearly trajectories; attributing reward to specific responses within a trajectory could improve training signal quality.
3. **Broader model families and more worlds** -- computational constraints limited experiments to one model family; testing on diverse LLMs and more world settings is needed.
4. **Alignment between life reward and true human well-being** -- the subjective fulfillment signal comes from AI models, not humans; closing this gap (e.g., with human-in-the-loop feedback) is an open challenge.
5. **Real-time vs. turn-based simulation** -- moving beyond discrete turn generation toward richer real-time perception remains a structural limitation to address.
6. **Privacy-preserving application to real individuals** -- the framework could potentially simulate real people, but doing so requires strict privacy regulation adherence and informed consent.

---

## Authors & Institutions

Xintao Wang (Fudan University, corresponding), Sirui Zheng (Independent), Hongqiu Wu (Independent), Weiyuan Li (Fudan University), Jen-tse Huang (Johns Hopkins University), Minghao Zhu (Independent), Can Zu (Independent), Qi Deng (Independent), Jiawei Wang (USTC), Qianyu He (Fudan University), Heng Wang (Independent), Xiaojian Wu (Independent), Yunzhe Tao (Independent)
