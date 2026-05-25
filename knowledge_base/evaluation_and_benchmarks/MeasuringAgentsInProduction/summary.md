# Measuring Agents in Production (MAP)

**Paper:** [Measuring Agents in Production (Pan, Arabzadeh, Zaharia, Ellis et al., 2025)](https://arxiv.org/abs/2512.04123)

## Human Readable TL;DR

Imagine you heard that self-driving cars were finally ready, but whenever companies actually put them on the road, they kept crashing or just being unreliable. You'd want to know: what are the companies that *do* have them working actually doing differently? This paper does exactly that for AI assistants that autonomously perform multi-step work tasks. The researchers interviewed 20 teams and surveyed 306 developers who have these AI "agents" running in real businesses right now -- handling finance, customer support, software development, and more. The main surprise: the teams that succeed aren't using the fanciest AI tricks. They keep things simple, keep humans in the loop, and treat reliability as job #1.

## TL;DR

MAP is the first large-scale empirical study of LLM-based agents already deployed in production, combining 20 in-depth case studies with a survey of 306 practitioners across 26 domains. The central finding is that successful production agents favor simple, controllable, system-level design over cutting-edge algorithmic complexity -- off-the-shelf models with manual prompts, structured workflows bounded to <10 steps, heavy human-in-the-loop evaluation, and custom in-house orchestration. Reliability is the dominant challenge, and the gap between research trends and practitioner choices reveals high-value directions for future agent engineering research.

---

## Problem & Motivation

LLM-based agents have generated enormous excitement, yet real-world deployments frequently fail or underperform. The root cause is a knowledge gap: the technical practices that make agents succeed in production are largely proprietary and undocumented. The research community builds on academic benchmarks and prototypes that may not reflect the constraints of live systems serving real users. MAP directly addresses this by collecting first-hand empirical data from practitioners -- the first study of its kind at this scale.

---

## Main Original Ideas

1. **First systematic production survey** -- A multi-method study (20 semi-structured case studies + 306-person online survey) that gathered typically-confidential deployment data across startups, banks, hospitals, and tech companies spanning 26 domains.

2. **Four research questions framing the field** -- The study operationalizes "how do production agents work?" into four concrete RQs: applications & motivation, models & architectures, evaluation practices, and top challenges. These provide a reusable framework for the emerging discipline of "agent engineering."

3. **Reliability-through-simplicity as a production principle** -- The paper provides empirical evidence that practitioners deliberately constrain agent autonomy (bounded step counts, structured workflows, read-only modes) not as a temporary workaround but as a stable architectural strategy, directly challenging the research trend toward unconstrained autonomous agents.

4. **Latency tolerance as an underexplored design axis** -- 66% of deployed agents tolerate minute-scale latency. This creates an unexploited design space where trading speed for correctness (e.g., test-time search, verification loops) is viable -- a direction largely ignored by benchmarks that optimize for per-token speed.

5. **Human-in-the-loop as enduring architecture** -- Rather than being a stepping stone to full automation, human oversight is treated as a deliberate, persistent design choice. 93% of agents serve human users, and 74% rely primarily on human evaluation, revealing that augmenting humans is a stable product strategy rather than a transitional one.

---

## Key Findings

| Finding | Statistic |
|---------|-----------|
| Primary motivation for building agents | Productivity gain (80%), reduce human task-hours (72%) |
| Agents with relaxed latency (≥ minutes) | 66% |
| Agents using proprietary frontier models | 17/20 case studies |
| Agents using multiple models | 59% |
| Agents using prompting only (no fine-tuning) | 70% (14/20 cases) |
| Manually constructed prompts | 79% |
| Automated prompt optimizers | 9% |
| Agents with structured workflows | 80% |
| Agents executing ≤10 steps before human intervention | 68% |
| Agents using custom in-house orchestration | 85% |
| Agents without formal benchmarks | 75% |
| Agents depending primarily on human evaluation | 74% |
| Agents handling confidential data | 69% |
| Top development priority: core technical performance | 38% |

**Qualitative highlights:**
- Finance & Banking (44%), Technology (48%), and Corporate Services (42%) lead early production adoption.
- Security and privacy are addressed implicitly via system-level constraints (read-only mode, internal deployments) rather than dedicated security mechanisms.
- Model brittleness under provider version upgrades is a persistent pain point; teams run legacy models alongside new ones to manage rollout risk.
- Custom benchmarks, when built, are highly domain-specific and not reusable across teams.

---

## Suggestions & Future Directions

1. **Model robustness across upgrades** -- Research into post-training methods (SFT, RL) that survive provider model updates without costly retraining; practitioners avoid these methods today due to brittleness.
2. **Latency-tolerant inference optimization** -- Explore throughput-oriented architectures (evolutionary search, test-verify pipelines, batched agent inference scheduling) for the majority of production cases that tolerate minute-scale latency.
3. **Multi-model orchestration** -- Better routing, dynamic model selection, and cost-aware scheduling for the 59% of systems running multiple models simultaneously.
4. **Production-grade evaluation tooling** -- Domain-specific benchmarks, synthetic data generation, correctness metrics, and runtime observability tools tailored to real-world agent tasks with delayed feedback loops.
5. **Human-agent collaboration interfaces** -- Intuitive oversight UIs, intervention triggers, and coordination protocols designed for long-running background agents.
6. **Bounded autonomy training** -- Train models that are natively responsive to step-budget constraints, safety specifications, and correctness criteria embedded in prompts or system design.
7. **Broader geographic and sector coverage** -- The current study skews toward Americas/Europe and tech/finance; future work should expand to emerging markets and healthcare-specific challenges.

---

## Authors & Institutions

Melissa Z. Pan, Negar Arabzadeh (co-leads, UC Berkeley), Matei Zaharia (UC Berkeley), Marquita Ellis (IBM Research), Dawn Song, Joseph E. Gonzalez, Ion Stoica (UC Berkeley), contributors from Stanford University, UIUC, Intesa Sanpaolo, and IBM Research.
