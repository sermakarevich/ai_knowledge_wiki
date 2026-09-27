[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Background, Related Work, and Research Questions
**In one sentence:** The paper frames code review as scaling-strained but essential, surveys LLM-for-review work as missing the preferred human–AI interaction question, and launches a two-phase WirelessCar study (RQ1: current practices/challenges/AI opportunities; RQ2: perceived interaction preference) built on interviews plus a two-mode field experiment.
## Key points
- Code review is positioned as a cornerstone for quality, defect detection, and knowledge sharing that now struggles with inefficiencies, reviewer fatigue, and inconsistent outcomes as systems scale and cycles accelerate.
- LLMs are credited with strong results on code generation and bug detection and smooth integration into coding activities, but their full potential in code review remains underexplored.
- Prior LLM-for-review work covers replicating reviewer changes, controlled issue-detection/time effects, emotional responses to AI vs human feedback, large-scale standards enforcement, fine-tuning for detection, and multi-agent autonomous review — leaving the preferred collaboration interaction as the gap.
- The study's stance is support-not-replace: LLMs are not treated as human replacements because they remain prone to hallucinations, so RQ2 focuses on practical integration strategies.
- RQ1 is diagnostic (current practices, challenges, expectations, where AI can help and the automation–human balance); RQ2 is exploratory (trust, satisfaction, barriers, usability, and preferred interaction mode).
- The design is two-phase at WirelessCar Sweden AB, where some but not all teams may use AI: Phase 1 exploratory interviews yielding RQ1, then Phase 2 field experiment with AI-led co-reviewer vs interactive assistant yielding RQ2.
- Both phases use semi-structured interviews with thematic analysis, and Phase 2 deliberately emphasizes qualitative interaction value over performance metrics or tool comparisons.
---
## Introduction
**Covers:** Section I

Code review (CR) is described as a cornerstone of modern software engineering for code quality, defect detection, and team knowledge sharing. Traditional manual review struggles as systems scale and delivery accelerates, producing inefficiencies, reviewer fatigue, and inconsistent outcomes. Large Language Models [1]–[3] have shown strong capabilities on software tasks including code generation and bug detection; integration into coding has been smooth but review remains underexplored.

The study combines observational research and field experiments at WirelessCar Sweden AB, where some but not all teams are permitted to use AI in development, to investigate how LLMs can be meaningfully integrated into review workflows to improve developer experience and potentially support review efficiency.

## Related work
**Covers:** Section II

Since ChatGPT, LLMs have been widely adopted for code generation, test-case creation, and documentation; readers are pointed to a 2024 review paper [4]. Recent works [5]–[10] target review:

| Work | Contribution as stated in chunk |
|---|---|
| Tufano et al. [10] (early) | Deep-learning model trained to replicate reviewer-suggested code changes, aiming to partially automate review. |
| Tufano et al. [5] | Controlled experiments on code with injected issues/smells; measures LLM performance and effects on issue detection, time spent, and reviewer behavior. |
| Alami et al. [9] | Qualitative, interview-based exploration of developers' emotional and cognitive responses to AI vs human feedback. |
| Vijayvergiya et al. [7] | Deployed large-scale automated system enforcing coding standards and code smells with LLMs. |
| Lin et al. [6] | Fine-tuning LLMs for better issue detection in reviews. |
| Rasheed et al. [8] | Multi-agent LLM system for autonomous reviews, focused on technical accuracy, issue detection, and actionable suggestions. |

Stated gap and differentiators: the critical gap is study of the preferred interaction for an engineer doing review in collaboration with an LLM assistant (primary focus, RQ2); the work targets supporting not replacing reviewers, citing hallucination risk [11]; it adds semi-structured interviews plus thematic analysis of pain points in complex-software development (RQ1), which then drive prototype design for RQ2.

## Research questions
**Covers:** Section III

> RQ1: "What practices, challenges, and expectations characterize modern code review processes, and where do developers see potential for AI-based assistance?"

RQ1 aims to capture how reviews are performed, what challenges developers face, what tasks AI can support, and the optimal automation–human balance.

> RQ2: "How do developers perceive LLM-assisted code review tools, and what is the preferred interaction?"

RQ2 explores qualitative aspects — trust, satisfaction, adoption barriers — across interaction modes to inform usability and design decisions.

The chunk characterizes RQ1 as diagnostic (current practice + AI opportunities) and RQ2 as exploratory (perception and interaction with LLM tools during review tasks).

## Methodology overview and Phase 1 setup
**Covers:** Section IV (intro + IV.A), Fig. 1, Table I

The design is a two-phase qualitative program (Fig. 1 flowchart: literature/database search → Phase 1 interview design, participants, interviews, thematic analysis → RQ1 results; → Phase 2 experiment/mode design, tool development, experiment, post-experiment interviews, thematic analysis → RQ2 results):

- Phase 1: exploratory case study of manual review (workflow steps, why inefficiencies arise, how success is evaluated, technical/organizational environment, AI improvement areas).
- Phase 2: field intervention with two LLM-review variations — AI-led mode (co-reviewer) and interactive mode — designed from Phase 1 findings plus literature, with RAG-based contextual support; assessment centers on interaction experience, valuable support kinds, and ideal real-world integration rather than metric comparisons.

Method details for Phase 1:

- Semi-structured interviews balancing a core question set with follow-up flexibility [13], covering review processes, challenges, success measurement, and current/potential AI use cases.
- Designed for 30 minutes; actual range 15–40 minutes, mostly about half an hour.
- Convenience sampling [14] via Slack channel announcements and informal messages; sought varied code ownership, reviewer seniorities, and multiple voices from the same team.
- Seven participants (Table I): P1 Quality Assurance Specialist (Team A); P2 Application Developer (Team A); P3 Software Engineer (Team A); P4 Software Engineer (Team A); P5 Security Engineer (Team B); P6 Software Engineer (Team C); P7 Software Engineer (Teams D & B); sample varied in gender and age and spanned security, QA, developer, and engineer roles across four teams sized from under five to around sixteen members.
- Saturation claimed after the seventh interview with no new themes emerging; a scheduled eighth interview was canceled and not rescheduled; saturation is defined as no new themes observed, often reached within twelve interviews with basic elements present by six [15].
- Interviews in English in the active work environment — on-site or remotely via Microsoft Teams (two remote) — so participants could reference real PRs, channels, and tasks such as a large refactoring PR or an urgent bug fix.

Phase 2 data collection begins in the chunk with two methods: post-interaction interviews as the primary source and researcher observation notes during review sessions as the secondary source (Table II header only in this chunk).

**Covers:** Sections I–IV (Introduction through Methodology Phase 1 setup and Phase 2 data-collection opening), Fig. 1, Table I.
