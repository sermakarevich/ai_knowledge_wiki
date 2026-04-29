# SoK: Agentic Skills -- Beyond Tool Use in LLM Agents

**Paper:** [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents (Jiang et al., 2025)](https://arxiv.org/abs/2602.20867)

## Human Readable TL;DR

Imagine you hire a new assistant every day who has amnesia -- they forget everything they learned yesterday and must figure out how to do your coffee order, file your reports, and schedule your meetings from scratch each morning. That is how most AI agents work today: they solve the same types of problems over and over without remembering *how* they did it before. This paper proposes giving AI agents a "recipe book" of reusable skills they can save, share, and improve over time -- much like how a chef builds expertise by mastering individual techniques. The authors also warn that these shared recipe books can be poisoned by bad actors, much like a tampered cookbook, and lay out safety guidelines to prevent that.

## TL;DR

This Systematization of Knowledge (SoK) introduces a formal definition of "agentic skills" as reusable procedural modules (distinct from tools, plans, or memories) for LLM agents, formalized as a four-tuple (applicability, policy, termination, interface). The paper maps a seven-stage skill lifecycle, proposes seven system-level design patterns and a representation-by-scope taxonomy, provides a security threat model anchored by the real-world ClawHavoc supply-chain attack, and presents evaluation evidence showing curated skills boost agent success rates by an average of +16.2 percentage points while self-generated skills without verification degrade performance.

---

## Problem & Motivation

LLM agents today suffer from **episodic knowledge loss**: they re-derive execution strategies from scratch for every new task, even when they have successfully completed identical tasks before. Procedural intelligence gained during one session vanishes when the context window ends. This leads to wasted computation, increased token consumption, reduced reliability, and a fundamental inability to accumulate expertise over time -- unlike human professionals who build a repertoire of practiced skills.

While prior surveys have covered LLM agents broadly, tool use, or multi-agent coordination, none have adopted a comprehensive **skill-centric lens**. This paper fills that gap by systematizing the concept of agentic skills as a distinct and critical abstraction layer for building robust, efficient LLM agents.

---

## Main Original Ideas

1. **Formal Skill Definition (Four-Tuple S = (C, pi, T, R))** -- An agentic skill is defined as an applicability condition (C), an executable policy (pi), a termination condition (T), and a reusable callable interface (R). This cleanly separates skills from atomic tools, one-off plans, and episodic memories.

2. **Seven-Stage Skill Lifecycle** -- A complete lifecycle model covering discovery, practice/refinement, distillation, storage, retrieval/composition, execution, and evaluation/update, with explicit feedback loops between stages. This frames skills as dynamic, evolving entities rather than static artifacts.

3. **Seven System-Level Design Patterns** -- Metadata-Driven Disclosure, Code-as-Skill, Workflow Enforcement, Self-Evolving Skill Libraries, Hybrid NL+Code Macros, Meta-Skills, and Plugin/Marketplace Distribution. These patterns capture how real systems package and execute skills, with documented trade-offs in context cost, determinism, composability, and governance.

4. **Representation x Scope Taxonomy** -- An orthogonal classification along representation (natural language, code, tool macros, policy-based, hybrid) and scope (single-tool, multi-tool, web, OS/desktop, software engineering, robotics). The analysis reveals most current systems cluster in sparse regions, highlighting large unexplored design spaces.

5. **Security Threat Model and Trust Framework** -- Six threat categories (poisoned retrieval, malicious payloads, cross-tenant leakage, skill drift exploitation, confused deputy via environmental injection, applicability condition poisoning) paired with a four-tier trust escalation model (metadata only, instruction access, supervised execution, autonomous execution).

6. **ClawHavoc Case Study** -- A detailed analysis of a real supply-chain attack on OpenClaw's ClawHub registry where 1,184+ malicious skills (36.8% of all published) exfiltrated API keys, crypto wallets, and credentials, demonstrating that traditional malware scanners fail against skill-native attacks.

---

## Key Findings

| Metric | Curated Skills | Self-Generated Skills |
|---|---|---|
| **Avg. success rate change** | **+16.2 pp** | -1.3 pp |
| Healthcare domain | +51.9 pp | -- |
| Manufacturing domain | +41.9 pp | -- |
| Optimal skill size | 2-3 focused modules | Overly broad degrades performance |

- Curated skills significantly improve agent success rates across domains, with the largest gains in healthcare (+51.9 pp) and manufacturing (+41.9 pp).
- Self-generated skills without iterative verification generally **degrade** performance, underscoring the importance of quality control.
- Smaller models equipped with curated skills can outperform larger models without them -- skills act as a "compute equalizer."
- Focused, narrow skills (2-3 modules) yield optimal improvement; overly comprehensive skill bundles hurt performance.
- Most existing systems cluster in sparse regions of the representation x scope design space, leaving large areas unexplored.
- More formal representations (code) are easier to govern and verify than natural-language policies.
- Rapid marketplace growth consistently outpaces security governance development.
- The formal (C, pi, T, R) definition explains why traditional binary malware scanners fail against skill-native attacks that target NL policies, applicability conditions, or interface metadata.

---

## Suggestions & Future Directions

1. **Verified Autonomous Skill Generation** -- Develop methods for agents to self-generate skills that are automatically verified for correctness and safety before library inclusion, closing the curation-scalability gap.

2. **Unsupervised Skill Discovery** -- Create techniques for agents to identify reusable behavioral patterns from interaction traces without human annotation or predefined templates.

3. **Formal Verification Across Representations** -- Extend formal verification methods to handle the full spectrum of skill representations, including natural-language and hybrid NL+code policies, not just pure code.

4. **Robustness Under Environmental Drift** -- Investigate how skills degrade as environments change over time and develop mechanisms for automatic detection, adaptation, and retirement of stale skills.

5. **Skill-Native Security Tooling** -- Build auditing and scanning tools that operate at the tuple level (C, pi, T, R) rather than relying on traditional binary or signature-based malware detection.

6. **Economics of Skill Governance** -- Study the incentive structures, certification models, and marketplace economics needed to sustain healthy, secure skill ecosystems at scale.

7. **Cross-Domain Skill Transfer** -- Explore whether skills learned in one domain (e.g., web navigation) can generalize or be adapted to different domains (e.g., robotics) through compositional or hierarchical methods.

---

## Authors & Institutions

Yanna Jiang (University of Technology Sydney), Delong Li (University of Technology Sydney), Haiyu Deng (University of Technology Sydney), Baihe Ma (University of Technology Sydney), Xu Wang (University of Technology Sydney), Qin Wang (University of Technology Sydney / CSIRO Data61), Guangsheng Yu (University of Technology Sydney)
